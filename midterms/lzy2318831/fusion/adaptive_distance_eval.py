"""Paired previous/v2 Adaptive simulations on saved v1.6 public observations."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from . import VERSION
from .engine import DEVICES
from .geometry_candidates import candidates
from .geometry_adaptive_power import adaptive_recommendations
from .smart import Simulation

ROOT=Path(__file__).resolve().parents[1]
BASELINE=ROOT/'evidence/adaptive-distance-v2-01/baseline/fusion/geometry_adaptive_power.py'


def previous(rows):
    spec=importlib.util.spec_from_file_location('_previous_adaptive_power',BASELINE)
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    return old.adaptive_recommendations(rows)


def saved_cases():
    folders=sorted((ROOT/'evidence/live-browser-geometry-v1').iterdir())
    for name in ('browser-presentation','browser-adaptive'):
        folders+=sorted((ROOT/'evidence/table-balance-v16-01'/name/'matches').iterdir())
    for folder in folders:
        tp,ap=folder/'trace.json',folder/'calls.jsonl'
        if not tp.exists() or not ap.exists():continue
        trace=json.loads(tp.read_text())
        if trace['version']!=VERSION:continue
        kind=trace.get('kind')
        if kind not in ('LIVE_BROWSER_GEOMETRY_ASSISTED_V1','MOCKED_LIVE_DEMO_NOT_REAL_LLM'):continue
        requests=[r for line in ap.read_text().splitlines() if line and (r:=json.loads(line)).get('kind')=='request']
        for i,step in enumerate(s for s in trace['steps'] if s.get('source')=='model'):
            ctx=json.loads(requests[i]['request']['input'][1]['content'])
            yield dict(source=folder.relative_to(ROOT).as_posix(),shot=i+1,
                evidence_kind='genuine_saved' if kind.startswith('LIVE_BROWSER_') else 'synthetic_saved',
                observation=ctx['observation'],legal=ctx['actions'])


def measure(o,action,target):
    sim=Simulation(o,action);initial={b.id:(b.x,b.y) for b in sim.balls}
    last=dict(initial);travel=Counter();contact=False;moved=False
    while not sim.done and sim.ticks<9600:
        sim.advance(1);cue=next(b for b in sim.balls if b.id==0)
        for b in sim.balls:
            p=(b.x,b.y);travel[b.id]+=math.dist(last[b.id],p);last[b.id]=p
            if b.id==target:
                moved|=not b.active or math.dist(initial[b.id],p)>.1
                contact|=cue.active and b.active and math.dist((cue.x,cue.y),p)<=22.1
    result=sim.result();events=sim.ledger.events
    powered=sum(e['type'] in ('bumper','sling','bridge','scoop','return') for e in events)
    result.update(target_contact_sample=contact if type(target) is int else None,
        target_moved=moved if type(target) is int else None,powered_events=powered,
        long_cascade=powered>=50,simulation_limit=not result['settled'],
        cue_travel=round(travel[0],2),object_travel=round(sum(v for k,v in travel.items() if k),2))
    if not sim.done:
        result.update(event_tail=events[-12:],moving=[dict(id=b.id,x=b.x,y=b.y,speed=math.hypot(b.vx,b.vy))
            for b in sim.balls if b.active and math.hypot(b.vx,b.vy)>0])
    return result


def totals(rows):
    result={}
    for arm in ('previous','v2'):
        t=Counter(cases=0,contacts=0,target_moved=0,scratches=0,limits=0,
            settled_pots=0,scratch_free_pots=0,retained_points=0,long_cascades=0,powered_events=0)
        for row in rows:
            r=row[arm];t['cases']+=1;t['contacts']+=bool(r['target_contact_sample']);t['target_moved']+=bool(r['target_moved'])
            t['scratches']+=r['foul'];t['limits']+=r['simulation_limit'];t['long_cascades']+=r['long_cascade'];t['powered_events']+=r['powered_events']
            if r['settled']:
                t['settled_pots']+=len(r['potted']);t['retained_points']+=r['points']
                if not r['foul']:t['scratch_free_pots']+=len(r['potted'])
        result[arm]=dict(t)
    return result


def run(output):
    output=Path(output);output.mkdir(exist_ok=False)
    cases=list(saved_cases());unique={};hashes={}
    for case in cases:
        for name in ('trace.json','calls.jsonl'):
            p=ROOT/case['source']/name;hashes[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
        for row in candidates(case['observation'],case['legal']):
            key=json.dumps(dict(physics={k:case['observation'][k] for k in ('balls','bumpers','devices')},
                candidate={k:v for k,v in row.items() if k not in ('id','risk')}),sort_keys=True)
            unique.setdefault(key,(case,row))
    rows=[];failures=[];cache={}
    with (output/'pairs.jsonl').open('x',encoding='utf-8') as stream:
        for key,(case,base) in unique.items():
            prior=previous([base])[0];new=adaptive_recommendations([base])[0];o=case['observation'];before=deepcopy(o)
            results={}
            for arm,candidate in (('previous',prior),('v2',new)):
                action={k:candidate[k] for k in ('angle','power')}
                ck=(key,candidate['power'])
                if ck not in cache:cache[ck]=measure(o,action,candidate['target'])
                results[arm]=cache[ck]
            row=dict(source=case['source'],shot=case['shot'],evidence_kind=case['evidence_kind'],
                base=base,previous_action={k:prior[k] for k in ('angle','power')},
                v2_action={k:new[k] for k in ('angle','power')},**results)
            assert o==before;rows.append(row);stream.write(json.dumps(row)+'\n');stream.flush()
            if results['v2']['simulation_limit']:
                repeat=measure(o,row['v2_action'],base['target'])
                assert repeat==results['v2']
                failures.append(dict(source=case['source'],shot=case['shot'],base=base,
                    action=row['v2_action'],previous=results['previous'],v2=repeat,repeat_identical=True))
            print('paired',len(rows),'/',len(unique),flush=True)
    # Mandatory saved historical position: explicitly a counterfactual under v1.6.
    from .geometry_power_calibration import observations
    historical=next(c for c in observations() if c['source'].endswith('8dbde2c0c71f') and c['model_shot']==4)
    o=deepcopy(historical['observation']);o['devices']=deepcopy(DEVICES)
    base=next(r for r in candidates(o,historical['legal']) if r['route']=='contact' and r['target']==5 and r['angle']==266)
    old,new=previous([base])[0],adaptive_recommendations([base])[0]
    mandatory=dict(kind='HISTORICAL_PUBLIC_POSITION_TRANSPLANTED_TO_REVISED_1_6_DEVICES_NOT_A_RECONSTRUCTED_MATCH',
        original_source=historical['source'],previous_action={k:old[k] for k in ('angle','power')},
        v2_action={k:new[k] for k in ('angle','power')},previous=measure(o,{k:old[k] for k in ('angle','power')},5),
        v2=measure(o,{k:new[k] for k in ('angle','power')},5))
    result=dict(kind='OFFLINE_CURRENT_1_6_PAIRED_ADAPTIVE_PROFILE_COMPARISON',physics_version=VERSION,
        observations=len(cases),observation_kinds=dict(Counter(c['evidence_kind'] for c in cases)),
        unique_candidate_states=len(rows),totals=totals(rows),mandatory=mandatory,
        repeated_v2_limits=len(failures),source_sha256=hashes,
        limitations='All-candidate correlated saved-state comparison, not new LLM choices/wins/human play. Contact/proximity and travel are proxies; travel includes transfers/correction. Unsettled points/pots are provisional and excluded from totals. Profile chosen by student, not optimized on this corpus.')
    (output/'summary.json').write_text(json.dumps(result,indent=2));(output/'limit-investigation.json').write_text(json.dumps(failures,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    run(p.parse_args().output)
