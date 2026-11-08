"""Offline runtime comparison; observes the archived engine without changing it."""
import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
from .legacy import module,verify
from .recorded_replay import load_match,DEFAULT_TRIAL
from .runner import fingerprint
from .llm_resume import OUTPUT


def first_difference(a,b,path='$'):
    if type(a) is not type(b):return dict(path=path,expected=a,actual=b,kind='type')
    if isinstance(a,dict):
        if set(a)!=set(b):return dict(path=path,kind='keys',expected=list(a),actual=list(b))
        for key in a:
            diff=first_difference(a[key],b[key],path+'.'+key)
            if diff:return diff
    elif isinstance(a,(list,tuple)):
        if len(a)!=len(b):return dict(path=path,kind='length',expected=len(a),actual=len(b))
        for i,(x,y) in enumerate(zip(a,b)):
            diff=first_difference(x,y,path+f'[{i}]')
            if diff:return diff
    elif a!=b:
        d=dict(path=path,kind='value',expected=a,actual=b)
        if isinstance(a,float):d.update(expected_hex=a.hex(),actual_hex=b.hex())
        return d
    return None


def encoded(value):
    if isinstance(value,float):return value.hex()
    if isinstance(value,(tuple,list)):return [encoded(x) for x in value]
    return value


def diagnose():
    trace,info=load_match(DEFAULT_TRIAL);engine=module('engine')
    episode=engine.Episode(layout=trace['layout']);episode.reset(trace['seed'])
    calls=[];ticks=[];original_tick=engine.tick
    names=('radians','cos','sin','hypot','dist','sqrt','atan2')
    originals={n:getattr(math,n) for n in names}
    def wrapped(name):
        def call(*args):
            value=originals[name](*args)
            if len(calls)<5000:calls.append(dict(function=name,args=encoded(args),result=encoded(value)))
            return value
        return call
    def tick(*args,**kwargs):
        original_tick(*args,**kwargs)
        if len(ticks)<16:ticks.append([dict(id=b.id,x=b.x,y=b.y,vx=b.vx,vy=b.vy,active=b.active) for b in args[0]])
    rows=[];first_observation=None
    try:
        for name in names:setattr(math,name,wrapped(name))
        engine.tick=tick
        for i,row in enumerate(trace['steps']):
            result=episode.step(row['player'],deepcopy(row['action']))
            if i==0:first_observation=episode.observe('p2')
            actual=fingerprint(episode.observe(row['player']))
            checks=dict(accepted=result['accepted']==row['accepted'],events=result['events']==row['events'],fingerprint=actual==row['after'],outcome=episode.outcome()==row['outcome'])
            rows.append(dict(shot=i+1,action=row['action'],checks=checks,expected_fingerprint=row['after'],actual_fingerprint=actual,first_event_difference=first_difference(row['events'],result['events'])))
            if not all(checks.values()):break
    finally:
        engine.tick=original_tick
        for name,value in originals.items():setattr(math,name,value)
    request=next(json.loads(line) for line in (OUTPUT/'calls.jsonl').read_text().splitlines() if json.loads(line).get('kind')=='request' and json.loads(line).get('trial')==DEFAULT_TRIAL)
    expected=json.loads(request['request']['input'][1]['content'])['observation']
    # This is the genuine first p2 request after the first p1 shot, not inferred data.
    # The historical prompt retained only the last32events; do not reconstruct
    # missing request data or mistake that truncation for a physics divergence.
    request_view=deepcopy(first_observation);request_view['last_events']=request_view['last_events'][-32:]
    return dict(kind='READ_ONLY_ARCHIVED_ENGINE_RUNTIME_DIAGNOSTIC',python=sys.version,platform=platform.platform(),archive_hashes=verify(),trial=DEFAULT_TRIAL,source_trace_sha256=info['trace_sha256'],source_request_sha256=request['request_sha256'],shots=rows,first_observation_difference=first_difference(expected,request_view),request_event_cap=32,first_observation=first_observation,first_ticks=ticks,math_calls=calls)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=diagnose();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('python','platform','archive_hashes','shots','first_observation_difference')},indent=2))


if __name__=='__main__':main()
