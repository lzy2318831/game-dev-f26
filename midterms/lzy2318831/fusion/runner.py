"""Authoritative matches/replay, including separately gated real LLM policies."""
import argparse
import hashlib
import json
from pathlib import Path
import time
from . import VERSION
from .engine import Episode
from .baseline import choose,direct
from .smart import choose as smart
from .player import invoke
from .llm import call_model
from pool.model import ModelFailure


def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def run_match(seed=101,seats=('baseline','baseline'),deadline_seconds=300,layout=None,players=None,model_call_limit=12,request_timeout=20,on_step=None):
    policies=dict({'baseline':choose,'direct':direct,'smart':smart},**(players or {}))
    if len(seats)!=2 or any(p not in policies for p in seats): raise ValueError('Unknown seats')
    e=Episode(layout=layout)
    e.reset(seed)
    trace=dict(version=VERSION,seed=seed,seats=list(seats),layout=e.layout,steps=[],model_calls=0,call_events=[],
        limits=dict(shots=12,model_calls=model_call_limit,request_timeout=request_timeout,deadline_seconds=deadline_seconds),
        engine_sha256=hashlib.sha256(b''.join(name.encode()+Path(__file__).with_name(name).read_bytes() for name in ('engine.py','devices.py','geometry.py','replenish.py'))).hexdigest())
    begin=time.monotonic()
    history=[]
    while not e.reason:
        if time.monotonic()-begin>=deadline_seconds:
            e.abort('episode_timeout'); break
        player=e.active_player
        start=time.monotonic()
        policy=policies[seats[0 if player=='p1' else 1]]
        is_model=getattr(policy,'is_model',False)
        metadata=None
        if is_model:
            if trace['model_calls']>=model_call_limit:
                e.abort('model_call_limit'); break
            trace['model_calls']+=1
            try:
                model_invoke=call_model if getattr(policy,'genuine_llm',False) else invoke
                action,metadata=model_invoke(policy,e.observe(player),e.legal_actions(player),history,
                    max(.001,min(request_timeout,deadline_seconds-(time.monotonic()-begin))))
            except ModelFailure as error:
                reason='episode_timeout' if time.monotonic()-begin>=deadline_seconds else str(error)
                e.abort(reason)
                trace['call_events'].append(dict(player=player,reason=reason,latency_seconds=time.monotonic()-start,metadata=getattr(error,'metadata',{})))
                break
        else:
            action=policy(e.observe(player),e.legal_actions(player))
        latency=time.monotonic()-start
        expired=time.monotonic()-begin>=deadline_seconds
        if is_model:
            trace['call_events'].append(dict(player=player,reason='episode_timeout' if expired else None,latency_seconds=latency,metadata=metadata))
        if expired:
            e.abort('episode_timeout'); break
        result=e.step(player,action)
        trace['steps'].append(dict(player=player,action=action,accepted=result['accepted'],
            events=result['events'],after=fingerprint(e.observe(player)),latency_seconds=latency,
            source='model' if is_model else seats[0 if player=='p1' else 1],model_metadata=metadata,outcome=e.outcome()))
        if on_step:on_step(trace['steps'][-1])
        history.append(dict(player=player,action=action,shot=e.last_shot))
    trace['outcome']=e.outcome()
    trace['elapsed_seconds']=time.monotonic()-begin
    return trace


def replay(trace):
    from .legacy import VERSION as OLD_VERSION,module
    if trace['version']==OLD_VERSION:return module('runner').replay(trace)
    if trace['version']!=VERSION or trace['engine_sha256']!=hashlib.sha256(b''.join(name.encode()+Path(__file__).with_name(name).read_bytes() for name in ('engine.py','devices.py','geometry.py','replenish.py'))).hexdigest(): raise ValueError('Version mismatch')
    e=Episode(layout=trace['layout']); e.reset(trace['seed'])
    for row in trace['steps']:
        result=e.step(row['player'],row['action'])
        if result['accepted']!=row['accepted'] or result['events']!=row['events'] or fingerprint(e.observe(row['player']))!=row['after']: raise ValueError('Replay diverged')
        if 'outcome' in row and row['outcome']!=e.outcome(): raise ValueError('Step outcome mismatch')
    if trace['outcome']['failure'] and not e.reason: e.abort(trace['outcome']['reason'])
    if e.outcome()!=trace['outcome']: raise ValueError('Outcome mismatch')
    return e.outcome()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--p1',choices=('baseline','direct','smart'),default='baseline')
    p.add_argument('--p2',choices=('baseline','direct','smart'),default='baseline')
    p.add_argument('--seed',type=int,default=101)
    p.add_argument('--trace',type=Path)
    p.add_argument('--replay',type=Path)
    args=p.parse_args()
    if args.replay:
        print(json.dumps(replay(json.loads(args.replay.read_text())),indent=2)); return
    trace=run_match(seed=args.seed,seats=(args.p1,args.p2))
    if args.trace:
        args.trace.parent.mkdir(parents=True,exist_ok=True)
        args.trace.write_text(json.dumps(trace,indent=2),encoding='utf-8')
    print(json.dumps(trace['outcome'],indent=2))
    print('Elapsed:',round(trace['elapsed_seconds'],3),'seconds')


if __name__=='__main__': main()
