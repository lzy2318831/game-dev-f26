"""Loopback browser replay of authentic official traces. No API or policies."""
import argparse
from copy import deepcopy
import hashlib
from http.cookies import SimpleCookie
import json
from pathlib import Path
import secrets
import threading
from http.server import ThreadingHTTPServer
from . import VERSION
from .engine import Episode
from .freeze import main as check_freeze
from .runner import fingerprint,replay
from .server import Handler as GameHandler,WEB
from .llm_resume import audit_rows,accounting,ORIGINAL,OUTPUT,MODEL
from .llm import digest
from .navigation import respond as navigation_response,viewer_page

ASSETS=Path(__file__).with_name('replay_web')
DEFAULT_TRIAL='observation_only-bumper-102-p2'


class ReplayHTTPServer(ThreadingHTTPServer):
    # Windows must refuse an occupied port rather than sharing an older game's socket.
    allow_reuse_address=False


def load_match(trial=DEFAULT_TRIAL):
    """Allowlisted completed official match, verified against durable live replies."""
    manifest=json.loads((OUTPUT/'manifest.json').read_text())
    if manifest['kind']!='live_recovery':raise ValueError('Not real evaluation evidence')
    records=[t for t in manifest['trials'] if t['id']==trial and t['status']=='complete']
    if len(records)!=1:raise ValueError('Choose a genuine completed recovery trial')
    record=records[0]
    path=(OUTPUT/record['trace']).resolve()
    if path.parent!=OUTPUT.resolve():raise ValueError('Trace must be inside recovery evidence')
    trace=json.loads(path.read_text())
    _,requests,results=accounting(audit_rows(OUTPUT/'calls.jsonl'))
    calls=[(r,results[n]['metadata']) for n,r in requests.items() if r['trial']==trial and n in results]
    model_rows=[r for r in trace['steps'] if r['source']=='model']
    if len(calls)!=6 or len(model_rows)!=6 or trace['outcome']['failure']:raise ValueError('Incomplete genuine match')
    for row,(request,metadata) in zip(model_rows,calls):
        if not request['live'] or request['request']['model']!=MODEL or metadata.get('http_status')!=200 or not metadata.get('live'):
            raise ValueError('Genuine successful live model result required')
        if row['player']!=record['seat'] or row['action']!=metadata['action'] or row['model_metadata']!=metadata or request['request_sha256']!=metadata['request_sha256']:
            raise ValueError('Recorded decision differs from actual provider result')
    if trace['seed']!=record['seed'] or trace['layout']!=record['layout'] or trace['outcome']!=record['metrics']['outcome']:
        raise ValueError('Trace/official record mismatch')
    info=dict(recorded_real_llm=True,live_api_session=False,trial=trial,case=record['case'],seed=record['seed'],
        model=MODEL,llm_seat=record['seat'],trace_path=str(path.relative_to(OUTPUT.parent.parent)),
        trace_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),outcome=trace['outcome'],
        note='Recorded real LLM evaluation. Actions replayed unchanged; no new API calls or manual moves.')
    return trace,info


class ReplaySession:
    def __init__(self,trace,info):
        self.trace=deepcopy(trace);self.info=deepcopy(info);self.lock=threading.RLock();self.reset()

    def reset(self):
        self.episode=Episode(layout=self.trace['layout']);self.episode.reset(self.trace['seed'])
        self.index=0;self.playback_pending=False;self.invalid=False
        return self.state()

    def state(self):
        return dict(version=VERSION,mode='hvh',busy=self.playback_pending,
            observation=self.episode.observe(self.episode.active_player),outcome=self.episode.outcome(),
            recording=dict(self.info,completed_shots=self.index,total_shots=len(self.trace['steps'])))

    def ready(self):
        self.playback_pending=False;return self.state()

    def next(self):
        if self.invalid or self.playback_pending or self.index>=len(self.trace['steps']):raise ValueError('Replay is locked or finished')
        row=self.trace['steps'][self.index]
        result=self.episode.step(row['player'],deepcopy(row['action']),record_frames=True)
        if (result['accepted']!=row['accepted'] or result['events']!=row['events'] or
                fingerprint(self.episode.observe(row['player']))!=row['after'] or self.episode.outcome()!=row['outcome']):
            self.invalid=True;raise ValueError('Replay diverged; stopped without replacement actions')
        self.index+=1;self.playback_pending=True
        if self.index==len(self.trace['steps']) and self.episode.outcome()!=self.trace['outcome']:
            self.invalid=True;raise ValueError('Final outcome mismatch')
        return dict(shot=result,state=self.state(),action=deepcopy(row['action']),source=row['source'],
            recording=dict(shot=self.index,player=row['player'],source=row['source'],
                latency_seconds=row['latency_seconds'],model_metadata=row.get('model_metadata')))


class Handler(GameHandler):
    def session(self):
        cookies=SimpleCookie()
        try:cookies.load(self.headers.get('Cookie',''))
        except Exception:pass
        token=cookies['fusion_replay'].value if 'fusion_replay' in cookies else ''
        with self.server.sessions_lock:
            if token not in self.server.sessions:
                if len(self.server.sessions)>=16:self.server.sessions.pop(next(iter(self.server.sessions)))
                token=secrets.token_hex(24)
                self.server.sessions[token]=ReplaySession(self.server.trace,self.server.info)
            return self.server.sessions[token],f'fusion_replay={token}; Path=/; HttpOnly; SameSite=Strict'

    def do_GET(self):
        if navigation_response(self):return
        if self.path=='/':
            page=(WEB/'index.html').read_text(encoding='utf-8')
            page=page.replace('</head>','<link rel="stylesheet" href="/replay.css"></head>')
            page=page.replace('</body>','<script src="/replay.js"></script></body>')
            page=viewer_page(page,'replay.js')
            self.reply(200,page.encode('utf-8'),'text/html; charset=utf-8');return
        if self.path in ('/replay.js','/replay.css'):
            kind='text/javascript' if self.path.endswith('.js') else 'text/css'
            self.reply(200,(ASSETS/self.path[1:]).read_bytes(),kind+'; charset=utf-8');return
        if self.path in ('/api/state','/replay/info'):
            session,cookie=self.session()
            with session.lock:self.reply(200,session.state() if self.path=='/api/state' else session.info,cookie=cookie)
            return
        if self.path in ('/style.css','/game.js','/aurum.js'):super().do_GET();return
        self.reply(404,dict(error='No such replay resource'))

    def do_POST(self):
        expected={f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}
        if self.headers.get('Origin') and self.headers['Origin'] not in expected:
            self.reply(403,dict(error='Origin refused'));return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<2 or size>32 or not self.headers.get('Content-Type','').startswith('application/json'):raise ValueError()
            if json.loads(self.rfile.read(size))!={}:raise ValueError('No actions accepted')
            session,cookie=self.session()
            with session.lock:
                if self.path=='/replay/reset':result=session.reset()
                elif self.path=='/replay/next':result=session.next()
                elif self.path=='/replay/ready':result=session.ready()
                else:raise ValueError('No live play or action selection')
                self.reply(200,result,cookie=cookie)
        except (ValueError,TypeError,KeyError):self.reply(400,dict(error='Replay refused; no manual actions or divergent results permitted.'))


def make_server(port=8767,trial=DEFAULT_TRIAL):
    trace,info=load_match(trial)
    replay(trace) # Offline authority check before making the viewer available.
    server=ReplayHTTPServer(('127.0.0.1',port),Handler);server.daemon_threads=True
    server.trace=trace;server.info=info;server.sessions={};server.sessions_lock=threading.Lock()
    return server


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--port',type=int,default=8767)
    parser.add_argument('--trial',default=DEFAULT_TRIAL);args=parser.parse_args();check_freeze()
    server=make_server(args.port,args.trial)
    print(f'RECORDED REAL LLM EVALUATION | http://127.0.0.1:{server.server_port} | no API calls | Ctrl+C to stop',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
