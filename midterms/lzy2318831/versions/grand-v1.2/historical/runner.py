"""Offline historical match runner; fixed simulation time, JSON trace/replay."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import time

from . import VERSION
from .engine import Episode
from .baseline import choose,direct,neutral
from .player import invoke
from pool.model import ModelFailure

POLICIES={'baseline':choose,'direct':direct,'neutral':neutral}


def run_match(seed=101,seats=('baseline','baseline'),deadline_seconds=300,
              players=None,model_call_limit=128,request_timeout=20,**config):
    policies=dict(POLICIES,**(players or {}))
    if len(seats)!=2 or any(s not in policies for s in seats):
        raise ValueError('Choose two known policies')
    e=Episode(**config)
    e.reset(seed)
    started=time.monotonic()
    trace=dict(version=VERSION,seed=seed,seats=list(seats),config=config,
               engine_sha256=hashlib.sha256(Path(__file__).with_name('engine.py').read_bytes()).hexdigest(),
               steps=[],model_calls=0,call_events=[],limits=dict(model_calls=model_call_limit,request_timeout=request_timeout,deadline_seconds=deadline_seconds))
    history=[]
    while not e.reason:
        if time.monotonic()-started>=deadline_seconds:
            e.abort('episode_timeout')
            break
        player=e.active_player
        policy=policies[seats[0 if player=='p1' else 1]]
        obs=e.observe(player)
        model=getattr(policy,'is_model',False)
        model_metadata=None
        begin=time.monotonic()
        if model:
            if trace['model_calls']>=model_call_limit:
                e.abort('model_call_limit')
                break
            trace['model_calls']+=1
            try:
                action,model_metadata=invoke(policy,obs,e.legal_actions(player),history[-2:],
                    timeout=max(.001,min(request_timeout,deadline_seconds-(time.monotonic()-started))))
            except ModelFailure as error:
                reason=str(error)
                if time.monotonic()-started>=deadline_seconds:
                    reason='episode_timeout'
                e.abort(reason)
                trace['call_events'].append(dict(player=player,reason=reason,latency_seconds=time.monotonic()-begin))
                break
        else:
            action=policy(obs,e.legal_actions(player))
        latency=time.monotonic()-begin
        if time.monotonic()-started>=deadline_seconds:
            e.abort('episode_timeout')
            break
        result=e.step(player,action)
        trace['steps'].append(dict(player=player,action=action,accepted=result['accepted'],
            events=result['events'],frames_advanced=result['frames_advanced'],
            after_sha256=snapshot_hash(e.observe(player)),latency_seconds=latency,
            source='model' if model else seats[0 if player=='p1' else 1],
            model_metadata=deepcopy(model_metadata)))
        history.append(dict(player=player,action=action,events=result['events'],scores=e.scores.copy()))
        if time.monotonic()-started>=deadline_seconds:
            e.abort('episode_timeout')
    trace['outcome']=e.outcome()
    trace['elapsed_seconds']=time.monotonic()-started
    return trace


def snapshot_hash(observation):
    return hashlib.sha256(json.dumps(observation,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def replay(trace):
    if trace['version']!=VERSION or trace['engine_sha256']!=hashlib.sha256(Path(__file__).with_name('engine.py').read_bytes()).hexdigest():
        raise ValueError('Engine version/hash differs')
    e=Episode(**trace['config'])
    e.reset(trace['seed'])
    for row in trace['steps']:
        result=e.step(row['player'],row['action'])
        if result['accepted']!=row['accepted'] or result['events']!=row['events'] or result['frames_advanced']!=row['frames_advanced'] or snapshot_hash(e.observe(row['player']))!=row['after_sha256']:
            raise ValueError('Replay diverged')
    if trace['outcome']['failure'] and not e.reason:
        e.abort(trace['outcome']['reason'])
    if e.outcome()!=trace['outcome']:
        raise ValueError('Outcome differs')
    return e.outcome()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--p1',choices=POLICIES,default='baseline')
    p.add_argument('--p2',choices=POLICIES,default='baseline')
    p.add_argument('--seed',type=int,default=101)
    p.add_argument('--heats',type=int,choices=range(2,6),default=2)
    p.add_argument('--scenario',choices=('opening','scattered','danger'),default='opening')
    p.add_argument('--no-extended',action='store_true')
    p.add_argument('--frames-per-step',type=int,default=64)
    p.add_argument('--trace',type=Path)
    p.add_argument('--replay',type=Path)
    args=p.parse_args()
    if args.replay:
        print(json.dumps(replay(json.loads(args.replay.read_text(encoding='utf-8'))),indent=2))
        return
    trace=run_match(seed=args.seed,seats=(args.p1,args.p2),heats=args.heats,
        extended=not args.no_extended,frames_per_step=args.frames_per_step,scenario=args.scenario)
    if args.trace:
        args.trace.parent.mkdir(parents=True,exist_ok=True)
        args.trace.write_text(json.dumps(trace,indent=2),encoding='utf-8')
    print(json.dumps(trace['outcome'],indent=2))
    print('Elapsed seconds:',round(trace['elapsed_seconds'],3))


if __name__=='__main__':
    main()
