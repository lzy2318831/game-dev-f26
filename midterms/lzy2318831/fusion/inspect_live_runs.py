"""Read-only diagnosis of saved browser runs; never requests replacement moves."""
from collections import Counter
import hashlib
import json
import math
import statistics
from .llm_resume import ROOT,audit_rows,accounting,hashes
from .llm import digest
from .runner import replay


def inspect():
    root=ROOT/'evidence/live-browser-v2';before=hashes(root);runs=[]
    for directory in sorted(root.iterdir()):
        if not (directory/'trace.json').exists():continue
        trace=json.loads((directory/'trace.json').read_text())
        state,requests,results=accounting(audit_rows(directory/'calls.jsonl'))
        shots=[];prior=0
        for index,row in enumerate(trace['steps'],1):
            if row['source']!='model':continue
            metadata=row['model_metadata'];request=next(r for r in requests.values() if r['request_sha256']==metadata['request_sha256'])
            if metadata['request_sha256']!=digest(request['request']):raise ValueError('Actual request hash mismatch')
            actual=[r['metadata'] for r in results.values() if r['metadata'].get('request_sha256')==metadata['request_sha256']]
            if actual!=[metadata] or row['action']!=metadata['action']:raise ValueError('Action/result evidence mismatch')
            obs=json.loads(request['request']['input'][1]['content'])['observation']
            cue=next(b for b in obs['balls'] if b['id']==0)
            events=Counter(e['type'] for e in row['events']);score=row['outcome']['scores']['p1']
            shots.append(dict(shot=index,action=row['action'],points=score-prior,scratch=events['scratch']>0,
                physical_pots=events['pocket'],events=dict(events),cue_before=cue,
                initial_velocity=[round(math.cos(math.radians(row['action']['angle']))*(100+7*row['action']['power']),3),
                                  round(math.sin(math.radians(row['action']['angle']))*(100+7*row['action']['power']),3)],
                preceding_feedback_player=(obs.get('last_shot') or {}).get('player')))
            prior=score
        if trace['run_status']=='complete':replay(trace)
        runs.append(dict(directory=directory.name,kind=trace['kind'],run_status=trace['run_status'],outcome=trace['outcome'],
            accounting=state,shots=shots,mean_power=statistics.mean(r['action']['power'] for r in shots) if shots else None,
            real_requests=sum(bool(r.get('live')) for r in requests.values()),
            genuine_http200=sum(r['metadata'].get('http_status')==200 and bool(r['metadata'].get('live')) for r in results.values())))
    if hashes(root)!=before:raise ValueError('Saved live evidence changed')
    return dict(kind='READ_ONLY_POST_OFFICIAL_LIVE_DIAGNOSIS',runs=runs,source_hashes=before,
        caution='Mocked/incomplete records are separate. One completed live match is not a controlled prompt-v1/v2 comparison.')


if __name__=='__main__':print(json.dumps(inspect(),indent=2))
