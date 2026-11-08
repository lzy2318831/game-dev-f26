"""Loopback-only standard-library server. No remote service or paid API."""
import argparse
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path
import secrets
import threading
from http.cookies import SimpleCookie
from . import VERSION
from .engine import Episode
from .baseline import choose
from .smart import plan

WEB=Path(__file__).with_name('web')


class GameSession:
    def __init__(self):
        self.lock=threading.RLock()
        self.reset('hvb')

    def reset(self,mode):
        if mode not in ('hvh','hvb','hvs'): raise ValueError('Choose human or baseline mode')
        self.mode=mode
        self.episode=Episode()
        self.playback_pending=False
        return self.state()

    def state(self):
        return dict(version=VERSION,observation=self.episode.observe(self.episode.active_player),
            outcome=self.episode.outcome(),mode=self.mode,busy=self.playback_pending)

    def ready(self):
        self.playback_pending=False
        return self.state()

    def shoot(self,action=None,baseline=False):
        if self.playback_pending: raise ValueError('Wait for shot playback to finish')
        if self.episode.reason: raise ValueError('Match is over. Start a new match.')
        player=self.episode.active_player
        automated=self.mode in ('hvb','hvs') and player=='p2'
        if automated!=baseline: raise ValueError('This seat chooses its own action')
        planning=None
        if automated:
            if self.mode=='hvs': action,planning=plan(self.episode.observe(player),self.episode.legal_actions(player))
            else: action=choose(self.episode.observe(player),self.episode.legal_actions(player))
        if not self.episode.valid(action): raise ValueError('Invalid angle/power')
        result=self.episode.step(player,action,record_frames=True)
        self.playback_pending=True
        return dict(shot=result,state=self.state(),action=action,planning=planning,source=('smart' if self.mode=='hvs' else 'baseline') if automated else 'human')


class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass

    def reply(self,status,body,content_type='application/json; charset=utf-8',cookie=None):
        data=body if isinstance(body,bytes) else json.dumps(body,allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'")
        if cookie: self.send_header('Set-Cookie',cookie)
        self.end_headers()
        self.wfile.write(data)

    def session(self):
        cookies=SimpleCookie()
        try: cookies.load(self.headers.get('Cookie',''))
        except Exception: pass
        token=cookies['fusion'].value if 'fusion' in cookies else ''
        with self.server.sessions_lock:
            if token not in self.server.sessions:
                if len(self.server.sessions)>=64: self.server.sessions.pop(next(iter(self.server.sessions)))
                token=secrets.token_hex(24)
                self.server.sessions[token]=GameSession()
            return self.server.sessions[token],f'fusion={token}; Path=/; HttpOnly; SameSite=Strict'

    def do_GET(self):
        if self.path=='/api/state':
            session,cookie=self.session()
            with session.lock: self.reply(200,session.state(),cookie=cookie)
            return
        routes={'/':('index.html','text/html; charset=utf-8'),'/game.js':('game.js','text/javascript; charset=utf-8'),'/aurum.js':('aurum.js','text/javascript; charset=utf-8'),'/style.css':('style.css','text/css; charset=utf-8')}
        if self.path not in routes:
            self.reply(404,dict(error='Not found')); return
        name,kind=routes[self.path]
        self.reply(200,(WEB/name).read_bytes(),kind)

    def do_POST(self):
        expected={f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}
        origin=self.headers.get('Origin')
        if origin and origin not in expected:
            self.reply(403,dict(error='Origin refused')); return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<2 or size>4096 or not self.headers.get('Content-Type','').startswith('application/json'):
                raise ValueError('Expected a small JSON request')
            body=json.loads(self.rfile.read(size))
            if not isinstance(body,dict): raise ValueError('Expected JSON object')
            session,cookie=self.session()
            with session.lock:
                if self.path=='/api/reset': result=session.reset(body.get('mode','hvb'))
                elif self.path=='/api/ready': result=session.ready()
                elif self.path=='/api/shot': result=session.shoot(body.get('action'),body.get('baseline') is True)
                else:
                    self.reply(404,dict(error='Not found')); return
                self.reply(200,result,cookie=cookie)
        except (ValueError,TypeError,KeyError):
            self.reply(400,dict(error='Request refused. Check the turn, action, and playback state.'))


def make_server(port=8765):
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    server.daemon_threads=True
    server.sessions={}
    server.sessions_lock=threading.Lock()
    return server


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    try: server=make_server(args.port)
    except OSError as error:
        parser.exit(1,f'Cannot start local server ({type(error).__name__}). Try --port 8766.\n')
    print(f'ARCADE FUSION  |  http://127.0.0.1:{server.server_port}  |  Ctrl+C to stop',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


if __name__=='__main__': main()
