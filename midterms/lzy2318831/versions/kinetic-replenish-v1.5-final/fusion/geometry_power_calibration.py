"""Offline distance/route power-floor comparison; not imported by live play."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from .geometry_candidates import candidates
from .geometry_power_experiment import saved_observations,ROOT
from .smart import Simulation

PROFILES={'floor25-35-50':(25,35,50),'floor30-40-55':(30,40,55),'floor35-50-65':(35,50,65)}
NEW_RUNS=('20261107T222659Z-4aeca6ff4a00','20261107T225959Z-1c46d6d44202')


def proposed_power(row,profile):
    base=row['power']
    if profile=='1x':return base
    if profile=='2x':return min(100,2*base)
    close,medium,long=PROFILES[profile]
    if row['route'] not in ('contact','pot','bank-contact'):return min(100,2*base)
    floor=close if row['travel']<=150 else medium if row['travel']<=350 else long
    if row['route']=='bank-contact':floor+=5
    return min(100,max(2*base,floor))


def observations():
    yield from saved_observations()
    for name in NEW_RUNS:
        folder=ROOT/'evidence/live-browser-geometry-v1'/name
        trace=json.loads((folder/'trace.json').read_text())
        assert trace['kind']=='LIVE_BROWSER_GEOMETRY_ASSISTED_V1'
        requests=[r for line in (folder/'calls.jsonl').read_text().splitlines()
                  if line and (r:=json.loads(line)).get('kind')=='request' and r.get('live') is True]
        for index,step in enumerate(s for s in trace['steps'] if s.get('source')=='model'):
            context=json.loads(requests[index]['request']['input'][1]['content'])
            yield dict(source=folder.relative_to(ROOT).as_posix(),model_shot=index+1,
                observation=context['observation'],legal=context['actions'])


def measure(observation,action,target):
    simulation=Simulation(observation,action)
    initial={b.id:(b.x,b.y) for b in simulation.balls}
    previous=dict(initial);travel=Counter();proximity=False;target_moved=False
    while not simulation.done and simulation.ticks<9600:
        simulation.advance(1)
        cue=next(b for b in simulation.balls if b.id==0)
        for ball in simulation.balls:
            current=(ball.x,ball.y)
            travel[ball.id]+=math.dist(previous[ball.id],current);previous[ball.id]=current
            if ball.id==target:
                target_moved|=not ball.active or math.dist(initial[ball.id],current)>.1
                if cue.active and ball.active and math.dist((cue.x,cue.y),current)<=22.1:proximity=True
    result=simulation.result();events=simulation.ledger.events
    powered=sum(e['type'] in ('bumper','sling','bridge','scoop','return') for e in events)
    result.update(cue_travel=round(travel[0],2),object_travel=round(sum(v for k,v in travel.items() if k),2),
        intended_contact_radius_sample=proximity if type(target) is int else None,
        intended_target_moved=target_moved if type(target) is int else None,
        powered_events=powered,events=len(events),simulation_limit=not result['settled'],
        max_object_displacement=round(max((math.dist(initial[b.id],(b.x,b.y)) for b in simulation.balls if b.id),default=0),2))
    return result


def summarize(rows):
    result={}
    for name in ('1x','2x',*PROFILES):
        total=Counter(pairs=0,scratches=0,simulation_limits=0,settled_points=0,physical_pots=0,
            scratch_free_pots=0,powered_events=0,cue_travel=0.,object_travel=0.,target_proximity=0,
            target_moved=0,long_powered_cascades=0)
        for row in rows:
            r=row['results'][name];total['pairs']+=1;total['scratches']+=r['foul']
            total['simulation_limits']+=r['simulation_limit'];total['powered_events']+=r['powered_events']
            total['cue_travel']+=r['cue_travel'];total['object_travel']+=r['object_travel']
            total['target_proximity']+=bool(r['intended_contact_radius_sample'])
            total['target_moved']+=bool(r['intended_target_moved'])
            total['long_powered_cascades']+=r['powered_events']>=50
            if r['settled']:
                total['settled_points']+=r['points'];total['physical_pots']+=len(r['potted'])
                if not r['foul']:total['scratch_free_pots']+=len(r['potted'])
        result[name]=dict(total)
    return result


def run(output):
    output=Path(output);output.mkdir(exist_ok=False)
    cases=list(observations());unique={};aliases=0
    for case in cases:
        o=case['observation']
        for row in candidates(o,case['legal']):
            key=json.dumps(dict(physics={k:o[k] for k in ('balls','bumpers','devices')},
                angle=row['angle'],power=row['power'],target=row['target'],route=row['route']),sort_keys=True)
            if key in unique:aliases+=1
            else:unique[key]=(case,row)
    rows=[];cache={}
    with (output/'trajectories.jsonl').open('x',encoding='utf-8') as stream:
        for key,(case,candidate) in unique.items():
            results={};powers={};o=case['observation']
            physics=json.dumps({k:o[k] for k in ('balls','bumpers','devices')},sort_keys=True)
            for profile in ('1x','2x',*PROFILES):
                power=proposed_power(candidate,profile);powers[profile]=power
                cache_key=(physics,candidate['angle'],power,candidate['target'])
                if cache_key not in cache:
                    cache[cache_key]=measure(o,dict(angle=candidate['angle'],power=power),candidate['target'])
                results[profile]=cache[cache_key]
            row=dict(source=case['source'],model_shot=case['model_shot'],candidate=candidate,powers=powers,results=results)
            rows.append(row);stream.write(json.dumps(row)+'\n');stream.flush()
            print('completed',len(rows),'of',len(unique),flush=True)
    known=[]
    # Independent mandatory position even if exact dedup aliases its source.
    known_case=next(c for c in cases if c['source'].endswith('8dbde2c0c71f') and c['model_shot']==4)
    known_row=next(r for r in candidates(known_case['observation'],known_case['legal']) if r['route']=='contact' and r['target']==5)
    for profile in ('1x','2x',*PROFILES):
        power=proposed_power(known_row,profile)
        known.append(dict(profile=profile,angle=266,power=power,result=measure(known_case['observation'],dict(angle=266,power=power),5)))
    summary=dict(kind='OFFLINE_ADAPTIVE_FLOOR_HYPOTHESES_NOT_MODEL_EVALUATION',saved_observations=len(cases),
        unique_candidate_states=len(rows),duplicate_candidates_removed=aliases,totals=summarize(rows),mandatory_known_position=known,
        limitations='Contact samples/movement are proxies; travel includes portal relocations and collision correction, so it is not pure physical path length. >=50 powered events is a descriptive cascade threshold, not a game rule. All candidates tested, not selected by a model. Correlated development observations; no human experience or win-rate measurement.')
    (output/'summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args().output)
