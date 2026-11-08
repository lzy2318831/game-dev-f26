"""Offline geometric coverage on saved genuine browser requests, not live results."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from .geometry_candidates import candidates, contact, clear, pocket_exposure

ROOT=Path(__file__).resolve().parents[1]


def analyze():
    counts=Counter();rows=[];hashes={}
    for folder in sorted((ROOT/'evidence/live-browser-v2').iterdir()):
        trace_path=folder/'trace.json';audit=folder/'calls.jsonl'
        if not trace_path.exists() or not audit.exists():continue
        trace=json.loads(trace_path.read_text())
        if trace.get('kind')!='LIVE_BROWSER_PROMPT_V2':continue
        records=[json.loads(line) for line in audit.read_text().splitlines() if line]
        requests=[r for r in records if r.get('kind')=='request' and r.get('live') is True]
        steps=[s for s in trace['steps'] if s['source']=='model']
        for path in (audit,trace_path):hashes[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
        for index,step in enumerate(steps):
            request=requests[index]['request'];context=json.loads(request['input'][1]['content'])
            observation=context['observation'];legal=context['actions'];action=step['action']
            assert action==step['model_metadata']['action']
            generated=candidates(observation,legal);routes={r['route'] for r in generated}
            c=next(b for b in observation['balls'] if b['id']==0);cue=(c['x'],c['y'])
            raw_reach=(100+7*action['power'])**2/140
            raw_ray=any((h:=contact(cue,action['angle'],(b['x'],b['y']))) and h[1]<=raw_reach
                for b in observation['balls'] if b['id'])
            raw_clear=any((h:=contact(cue,action['angle'],(b['x'],b['y']))) and h[1]<=raw_reach
                and clear(cue,h[0],observation,(0,b['id'])) and not pocket_exposure(cue,h[0],observation)
                for b in observation['balls'] if b['id'])
            counts['shots']+=1
            counts['direct_contact_or_pot']+=bool(routes & {'contact','pot'})
            counts['bank_contact']+='bank-contact' in routes
            counts['contact_including_bank']+=bool(routes & {'contact','pot','bank-contact'})
            counts['ghost_pot']+='pot' in routes
            counts['device_route']+='device' in routes
            counts['escape_available']+='escape' in routes
            counts['escape_only']+=routes=={'escape'}
            counts['fallback_escape']+='fallback-escape' in routes
            counts['no_candidate']+=not generated
            counts['raw_ray_reaches_any_object_ignoring_blockers']+=bool(raw_ray)
            counts['raw_clear_reachable_contact']+=bool(raw_clear)
            counts['raw_scratches']+=any(e['type']=='scratch' for e in step['events'])
            rows.append(dict(run=folder.name,model_shot=index+1,raw_action=action,
                raw_ray_reaches_object_ignoring_blockers=bool(raw_ray),candidates=generated))
    return dict(kind='OFFLINE_GEOMETRIC_COVERAGE_NOT_LLM_PERFORMANCE',counts=dict(counts),rows=rows,
        source_sha256=hashes,limitations='Candidate clearance/reach is geometry, not simulated collision success, a pot, or a win. No LLM selection or paid calls. Saved v2 cases are development data, not held-out evaluation.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);args=p.parse_args()
    result=analyze()
    if args.output:
        with args.output.open('x',encoding='utf-8') as out:json.dump(result,out,indent=2)
    print(json.dumps(dict(kind=result['kind'],counts=result['counts'],limitations=result['limitations']),indent=2))


if __name__=='__main__':main()
