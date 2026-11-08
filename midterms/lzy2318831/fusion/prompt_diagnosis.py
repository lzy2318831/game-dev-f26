"""Read-only retrospective of actual official decisions; no counterfactual tuning."""
from collections import Counter
import json
import statistics
from .llm_resume import OUTPUT,audit_rows,accounting


def inspect():
    manifest=json.loads((OUTPUT/'manifest.json').read_text())
    _,requests,results=accounting(audit_rows(OUTPUT/'calls.jsonl'))
    by_hash={r['request_sha256']:r for r in requests.values()}
    shots=[]
    for trial in manifest['trials']:
        trace=json.loads((OUTPUT/trial['trace']).read_text())
        before={'p1':0,'p2':0}
        for number,row in enumerate(trace['steps'],1):
            if row['source']=='model':
                request=by_hash[row['model_metadata']['request_sha256']]['request']
                context=json.loads(request['input'][1]['content']);obs=context['observation']
                player=row['player'];events=row['events'];counts=Counter(e['type'] for e in events)
                shots.append(dict(trial=trial['id'],shot=number,player=player,action=row['action'],
                    points=row['outcome']['scores'][player]-before[player],scratch=counts['scratch']>0,
                    physical_pots=counts['pocket'],cue_device_events=sum(e.get('points',0)>0 for e in events if e['type']!='pocket'),
                    previous_visible_actor=(obs.get('last_shot') or {}).get('player'),
                    previous_visible_foul=(obs.get('last_shot') or {}).get('foul'),
                    history_records=len(context['history']),visible_event_count=len(obs['last_events'])))
            before=row['outcome']['scores']
    power=[s['action']['power'] for s in shots]
    return dict(kind='retrospective_official_trace_diagnosis_not_new_evaluation',shots=shots,
        summary=dict(model_shots=len(shots),scratches=sum(s['scratch'] for s in shots),
            total_points=sum(s['points'] for s in shots),physical_pots=sum(s['physical_pots'] for s in shots),
            mean_power=statistics.mean(power),median_power=statistics.median(power),min_power=min(power),max_power=max(power),
            power_frequencies=dict(Counter(power)),full_power_shots=power.count(100),power_at_least80=sum(p>=80 for p in power),
            empty_history_shots=sum(s['history_records']==0 for s in shots),
            preceding_opponent_feedback=sum(s['previous_visible_actor'] is not None and s['previous_visible_actor']!=s['player'] for s in shots),
            preceding_own_feedback=sum(s['previous_visible_actor']==s['player'] for s in shots),
            capped_last_events=sum(s['visible_event_count']==32 for s in shots),
            zero_point_shots=sum(s['points']==0 for s in shots),
            scratch_pots=sum(s['physical_pots'] for s in shots if s['scratch'])),
        examples=[s for s in shots if s['scratch'] and s['physical_pots']][:4],
        interpretation='Observed outcomes/actions, not proof of model internal reasoning. Original cases are now retrospective development evidence for any revised prompt.')


if __name__=='__main__':print(json.dumps(inspect(),indent=2))
