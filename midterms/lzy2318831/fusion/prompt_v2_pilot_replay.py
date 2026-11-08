"""Visual replay of the best genuine completed v2 pilot; no API or replacement moves."""
import argparse
import hashlib
import json
from pathlib import Path
import threading
from .freeze import main as check_freeze
from .llm import digest
from .llm_resume import audit_rows,accounting
from .prompt_v2 import VARIANT,MODEL
from .prompt_v2_pilot import LIVE_OUTPUT
from .recorded_replay import Handler,ReplayHTTPServer
from .runner import replay


def load_best(directory=LIVE_OUTPUT):
    directory=Path(directory).resolve();manifest=json.loads((directory/'manifest.json').read_text())
    if manifest['kind']!='live_prompt_v2_pilot':raise ValueError('Only real live v2 results may be shown; no fixtures')
    complete=[t for t in manifest['trials'] if t['status']=='complete' and not t['metrics']['outcome']['failure']]
    if not complete:raise ValueError('No real completed v2 match available')
    def rank(record):
        o=record['metrics']['outcome'];seat=record['seat'];other='p2' if seat=='p1' else 'p1'
        return (o['scores'][seat]-o['scores'][other],o['scores'][seat],-o['scratches'][seat],-manifest['trials'].index(record))
    record=max(complete,key=rank);path=(directory/record['trace']).resolve()
    if path.parent!=directory:raise ValueError('Trace path outside evidence')
    trace=json.loads(path.read_text());_,requests,results=accounting(audit_rows(directory/'calls.jsonl'))
    calls=[(r,results[n]['metadata']) for n,r in requests.items() if r['trial']==record['id'] and n in results]
    model_rows=[r for r in trace['steps'] if r['source']=='model']
    if len(calls)!=len(model_rows) or not 1<=len(calls)<=6:raise ValueError('Incomplete real decisions')
    for row,(request,metadata) in zip(model_rows,calls):
        actual_prompt=hashlib.sha256(request['request']['input'][0]['content'].encode()).hexdigest()
        if (not request['live'] or not metadata.get('live') or metadata.get('http_status')!=200
            or request['request']['model']!=MODEL or metadata.get('agent_variant')!=VARIANT
            or actual_prompt!=manifest['protocol']['prompt_sha256'] or metadata.get('prompt_sha256')!=actual_prompt
            or row['action']!=metadata.get('action') or row['model_metadata']!=metadata
            or row['player']!=record['seat'] or metadata.get('request_sha256')!=digest(request['request'])):
            raise ValueError('Recorded action is not the genuine saved v2 reply')
    if trace['seed']!=record['seed'] or trace['outcome']!=record['metrics']['outcome']:
        raise ValueError('Trace differs from pilot outcome')
    replay(trace)
    info=dict(recorded_real_llm=True,live_api_session=False,agent_variant=VARIANT,
        trial=record['id'],case='separate prompt-v2 fresh-seed pilot',seed=record['seed'],model=MODEL,
        llm_seat=record['seat'],trace_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),outcome=trace['outcome'],
        note='Recorded real prompt-v2 pilot, not original official evaluation or live inference. Best by score margin, score, fewer scratches, declaration order.')
    return trace,info


def make_server(port=8791):
    trace,info=load_best();server=ReplayHTTPServer(('127.0.0.1',port),Handler)
    server.daemon_threads=True;server.trace=trace;server.info=info;server.sessions={};server.sessions_lock=threading.Lock()
    return server


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=8791);args=p.parse_args()
    check_freeze()
    try:server=make_server(args.port)
    except (FileNotFoundError,ValueError) as error:p.exit(1,f'No genuine completed pilot replay: {error}\n')
    print(f'RECORDED REAL PROMPT-V2 PILOT | http://127.0.0.1:{server.server_port}/#autoplay | no API calls',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
