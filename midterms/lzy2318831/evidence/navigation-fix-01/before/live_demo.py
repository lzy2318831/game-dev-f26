"""Game + unchanged recorded replay + separately consented live prompt-v2 mode."""
import argparse
import json
from pathlib import Path
import secrets
import threading
from .demo import DemoHandler,make_servers
from .freeze import main as check_freeze
from .recorded_replay import ReplayHTTPServer
from .server import Handler as BaseHandler,WEB
from .live_session import LiveSession,MatchLedger
from .prompt_v2 import offline_response

ASSETS=Path(__file__).with_name('live_web')


class EntryHandler(DemoHandler):
    def reply(self,status,body,content_type='application/json; charset=utf-8',cookie=None):
        if self.path=='/' and status==200 and content_type.startswith('text/html'):
            page=body.decode('utf-8')
            marker='<a href="/watch" class="primary-button">Watch LLM Agent Play</a>'
            page=page.replace(marker,marker+' <a href="/live" class="primary-button">Start Live LLM Agent</a>')
            body=page.encode('utf-8')
        super().reply(status,body,content_type,cookie)
    def do_GET(self):
        if self.path=='/live':
            self.send_response(302);self.send_header('Location',f'http://127.0.0.1:{self.server.live_port}/')
            self.send_header('Content-Length','0');self.end_headers();return
        super().do_GET()


class LiveHandler(BaseHandler):
    def valid_host(self):
        return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}')
    def do_GET(self):
        if not self.valid_host():self.reply(403,dict(error='Loopback host required'));return
        s=self.server.live_session
        if self.path=='/':
            page=(WEB/'index.html').read_text(encoding='utf-8')
            page=page.replace('</head>','<link rel="stylesheet" href="/live.css"></head>')
            page=page.replace('</body>','<script src="/live.js"></script></body>')
            self.reply(200,page.encode('utf-8'),'text/html; charset=utf-8');return
        if self.path=='/api/state':self.reply(200,s.state());return
        if self.path=='/live/info':self.reply(200,dict(nonce=s.nonce,state=s.state()));return
        if self.path=='/live/packet':
            try:self.reply(200,s.packet())
            except ValueError:self.reply(409,dict(error='No active shot packet'))
            return
        if self.path in ('/live.js','/live.css'):
            kind='text/javascript' if self.path.endswith('.js') else 'text/css'
            self.reply(200,(ASSETS/self.path[1:]).read_bytes(),kind+'; charset=utf-8');return
        if self.path in ('/game.js','/aurum.js','/style.css'):super().do_GET();return
        self.reply(404,dict(error='Not a live-demo resource'))
    def do_POST(self):
        expected={f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}
        if not self.valid_host() or self.headers.get('Origin') not in expected:
            self.reply(403,dict(error='Same-origin local confirmation required'));return
        s=self.server.live_session
        token=self.headers.get('X-Live-Token','')
        if not token or not secrets.compare_digest(token,s.nonce):self.reply(403,dict(error='Session token required'));return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<2 or size>512 or not self.headers.get('Content-Type','').startswith('application/json'):raise ValueError()
            body=json.loads(self.rfile.read(size))
            if not isinstance(body,dict):raise ValueError()
            if self.path=='/live/start' and set(body)=={'confirmed'}:result=s.start(body['confirmed'],token)
            elif self.path=='/live/ready' and set(body)=={'sequence'}:result=s.ready(body['sequence'])
            elif self.path=='/live/cancel' and not body:result=s.cancel()
            else:raise ValueError('No manual shot inputs or reset endpoint')
            self.reply(200,result)
        except (ValueError,TypeError,KeyError):
            self.reply(400,dict(error='Live request refused. Confirm one enabled match; manual actions and resets are not accepted.'))


def make_live_server(port=8809,enable_paid=False,transport=None,root=None):
    server=ReplayHTTPServer(('127.0.0.1',port),LiveHandler);server.daemon_threads=True
    server.live_session=LiveSession(root,enable_paid,transport)
    return server


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port',type=int,default=8805);p.add_argument('--replay-port',type=int,default=8807)
    p.add_argument('--live-port',type=int,default=8809)
    mode=p.add_mutually_exclusive_group();mode.add_argument('--enable-paid',action='store_true');mode.add_argument('--mock',action='store_true')
    args=p.parse_args();check_freeze()
    game,recorded=make_servers(args.port,args.replay_port)
    try:live=make_live_server(args.live_port,args.enable_paid,offline_response if args.mock else None)
    except Exception:game.server_close();recorded.server_close();raise
    game.RequestHandlerClass=EntryHandler;game.live_port=live.server_port
    threads=[threading.Thread(target=s.serve_forever,daemon=True) for s in (recorded,live)]
    for t in threads:t.start()
    print(f'KINETIC CIRCUIT | http://127.0.0.1:{game.server_port} | recorded and separate live buttons',flush=True)
    print('MOCKED API ONLY - NOT REAL LLM' if args.mock else 'Paid calls enabled only after browser match confirmation' if args.enable_paid else 'Paid calls DISABLED; no credential prompt or API request',flush=True)
    try:game.serve_forever()
    except KeyboardInterrupt:pass
    finally:
        live.live_session.cancel()
        if live.live_session.worker:live.live_session.worker.join(22)
        game.server_close()
        for s in (recorded,live):s.shutdown();s.server_close()
        for t in threads:t.join()


if __name__=='__main__':main()
