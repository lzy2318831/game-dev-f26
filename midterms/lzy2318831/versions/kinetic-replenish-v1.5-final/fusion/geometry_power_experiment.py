"""Offline paired power experiment. Never imported by the Live LLM runtime."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
from .geometry_candidates import candidates
from .smart import Simulation

ROOT=Path(__file__).resolve().parents[1]
FAILURE='20261107T215634Z-8dbde2c0c71f'


def doubled_power(power):
    if type(power) is not int or not 1<=power<=100:
        raise ValueError('Expected a legal integer power')
    return min(100,power*2)


def saved_observations():
    """Executed genuine requests only; retain their recorded public observations."""
    folders=sorted((ROOT/'evidence/live-browser-v2').iterdir())
    folders.append(ROOT/'evidence/live-browser-geometry-v1'/FAILURE)
    for folder in folders:
        trace_path=folder/'trace.json';audit=folder/'calls.jsonl'
        if not trace_path.exists() or not audit.exists():continue
        trace=json.loads(trace_path.read_text())
        if trace.get('kind') not in ('LIVE_BROWSER_PROMPT_V2','LIVE_BROWSER_GEOMETRY_ASSISTED_V1'):continue
        records=[json.loads(line) for line in audit.read_text().splitlines() if line]
        requests=[r for r in records if r.get('kind')=='request' and r.get('live') is True]
        steps=[s for s in trace['steps'] if s['source']=='model']
        for index,step in enumerate(steps):
            context=json.loads(requests[index]['request']['input'][1]['content'])
            yield dict(source=folder.relative_to(ROOT).as_posix(),model_shot=index+1,
                observation=context['observation'],legal=context['actions'],
                historical_action=step['action'],source_sha256={
                    p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (trace_path,audit)})


def simulate(observation,action,target):
    """Unchanged authoritative ticks; non-invasive, sampled contact proxies."""
    sim=Simulation(observation,action)
    cue=next(b for b in sim.balls if b.id==0)
    objects=[b for b in sim.balls if b.id!=0]
    intended=next((b for b in objects if b.id==target),None)
    initial=(intended.x,intended.y) if intended else None
    proximity=False;target_proximity=False;target_moved=False
    while not sim.done and sim.ticks<9600:
        sim.advance(1)
        if cue.active:
            for ball in objects:
                if ball.active and math.hypot(cue.x-ball.x,cue.y-ball.y)<=22.1:
                    proximity=True
                    if ball is intended:target_proximity=True
        if intended and (not intended.active or math.dist(initial,(intended.x,intended.y))>.1):
            target_moved=True
    result=sim.result()
    result.update(cue_object_contact_radius_sample=proximity,
        intended_contact_radius_sample=target_proximity if intended else None,
        intended_target_moved=target_moved if intended else None,
        target_potted=target in result['potted'] if intended else None,
        simulation_limit=not result['settled'],events=len(sim.ledger.events))
    return result


def aggregate(rows):
    totals={name:Counter(settled_pots=0,settled_points=0) for name in ('original','doubled')};changes=Counter()
    for row in rows:
        for name in totals:
            r=row[name];t=totals[name];t['shots']+=1
            for metric in ('settled','foul','simulation_limit','cue_object_contact_radius_sample',
                           'intended_contact_radius_sample','intended_target_moved','target_potted'):
                t[metric]+=bool(r[metric])
            if r['settled']:
                t['settled_pots']+=len(r['potted']);t['settled_points']+=r['points']
        a,b=row['original'],row['doubled']
        changes['new_simulation_limits']+=a['settled'] and not b['settled']
        changes['resolved_simulation_limits']+=not a['settled'] and b['settled']
        changes['new_scratches']+=not a['foul'] and b['foul']
        changes['avoided_scratches']+=a['foul'] and not b['foul']
        if a['settled'] and b['settled']:
            changes['both_settled']+=1
            changes['doubled_more_pots']+=len(b['potted'])>len(a['potted'])
            changes['doubled_fewer_pots']+=len(b['potted'])<len(a['potted'])
    n=len(rows)
    unsafe=bool(changes['new_simulation_limits'] or
                n and (totals['doubled']['foul']-totals['original']['foul'])/n>=.05)
    return dict(totals={k:dict(v) for k,v in totals.items()},paired_changes=dict(changes),
        decision='KEEP_STABILIZED_RUNTIME_UNCHANGED' if unsafe else 'ELIGIBLE_FOR_FURTHER_REVIEW_NOT_AUTOMATIC_ENABLEMENT')


def run(output):
    output=Path(output);output.mkdir(exist_ok=False)
    rows=[];observations=list(saved_observations());source_hashes={}
    with (output/'pairs.jsonl').open('x',encoding='utf-8') as stream:
        for case in observations:
            source_hashes.update(case['source_sha256'])
            original_obs=deepcopy(case['observation'])
            for candidate in candidates(case['observation'],case['legal']):
                action={k:candidate[k] for k in ('angle','power')}
                doubled=dict(action,power=doubled_power(action['power']))
                row=dict(source=case['source'],model_shot=case['model_shot'],candidate=candidate,
                    original_action=action,doubled_action=doubled,
                    original=simulate(case['observation'],action,candidate['target']),
                    doubled=simulate(case['observation'],doubled,candidate['target']))
                assert case['observation']==original_obs
                rows.append(row);stream.write(json.dumps(row)+'\n');stream.flush()
            print(json.dumps(dict(source=case['source'],shot=case['model_shot'],pairs_so_far=len(rows))),flush=True)
    result=dict(kind='OFFLINE_PAIRED_POWER_SIMULATION_NOT_LLM_EVALUATION',
        observations=len(observations),candidate_pairs=len(rows),formula='min(100, original_power * 2)',
        **aggregate(rows),source_sha256=source_hashes,
        limitations='Correlated saved development states; every candidate tested, not LLM-selected. Contact-radius samples and target movement are proxies, not complete collision logs. Pots/points on unsettled trajectories are provisional and excluded from settled totals. No match win-rate or genuine LLM benefit measured.')
    (output/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args().output)
