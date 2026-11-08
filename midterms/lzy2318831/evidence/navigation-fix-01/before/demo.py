"""Normal game plus prominent recorded-agent entry point. Offline, two loopback ports."""
import argparse
import threading
from .freeze import main as check_freeze
from .server import Handler,WEB
from .recorded_replay import make_server as replay_server,DEFAULT_TRIAL,ReplayHTTPServer


class DemoHandler(Handler):
    def do_GET(self):
        if self.path=='/watch':
            self.send_response(302)
            self.send_header('Location',f'http://127.0.0.1:{self.server.recorded_port}/#autoplay')
            self.send_header('Content-Length','0');self.end_headers();return
        if self.path=='/':
            page=(WEB/'index.html').read_text(encoding='utf-8')
            button=('<section class="heading-row" aria-label="Agent demonstration">'
                    '<a href="/watch" class="primary-button">Watch LLM Agent Play</a>'
                    '<p>Recorded LLM Evaluation · authentic saved match · no API calls</p></section>')
            page=page.replace('<section class="scoreboard"',button+'<section class="scoreboard"',1)
            # Also reachable before the normal game intro is dismissed.
            page=page.replace('<small class="modal-footnote">',
                '<p><a href="/watch" class="primary-button">Watch LLM Agent Play</a></p><small class="modal-footnote">',1)
            self.reply(200,page.encode('utf-8'),'text/html; charset=utf-8');return
        super().do_GET()


def make_servers(port=8765,replay_port=8767,trial=DEFAULT_TRIAL):
    recorded=replay_server(replay_port,trial)
    try:game=ReplayHTTPServer(('127.0.0.1',port),DemoHandler)
    except Exception:recorded.server_close();raise
    game.daemon_threads=True;game.sessions={};game.sessions_lock=threading.Lock()
    game.recorded_port=recorded.server_port
    return game,recorded


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=8785)
    p.add_argument('--replay-port',type=int,default=8787);p.add_argument('--trial',default=DEFAULT_TRIAL)
    args=p.parse_args();check_freeze()
    game,recorded=make_servers(args.port,args.replay_port,args.trial)
    worker=threading.Thread(target=recorded.serve_forever,daemon=True);worker.start()
    print(f'KINETIC CIRCUIT | http://127.0.0.1:{game.server_port} | click Watch LLM Agent Play | recorded evaluation, no API',flush=True)
    try:game.serve_forever()
    except KeyboardInterrupt:pass
    finally:game.server_close();recorded.shutdown();recorded.server_close();worker.join()


if __name__=='__main__':main()
