"""Offline derived statistics; preserves every source evaluation artifact."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import statistics
from .llm_resume import OUTPUT,ORIGINAL,SMOKE,accounting,audit_rows,hashes
from .recorded_replay import load_match
from .runner import replay
from .llm_eval import save


def result(trace,seat):
    o=trace['outcome']
    return 'failure' if o['failure'] else 'draw' if o['draw'] else 'win' if o['winner']==seat else 'loss'


def analyze(verify=False):
    sources=(ORIGINAL,SMOKE,OUTPUT);before=[hashes(p) for p in sources]
    original=json.loads((ORIGINAL/'manifest.json').read_text())
    recovery=json.loads((OUTPUT/'manifest.json').read_text())
    records=[original['trials'][0]]+recovery['trials']
    rows=[];traces=[];controls=[]
    for i,t in enumerate(records):
        folder=ORIGINAL if i==0 else OUTPUT
        if i==0:trace=json.loads((folder/t['trace']).read_text())
        else:trace,_=load_match(t['id'])
        control=json.loads((folder/(t['id']+'-control.json')).read_text())
        if verify:replay(trace);replay(control)
        seat=t['seat'];other='p2' if seat=='p1' else 'p1';o=trace['outcome'];co=control['outcome']
        rows.append(dict(trial=t['id'],case=t['case'],seat=seat,status=t['status'],
            llm_result=result(trace,seat),llm_score=o['scores'][seat],opponent_score=o['scores'][other],
            control_result=result(control,seat),control_score=co['scores'][seat],
            llm_scratches=o['scratches'][seat],opponent_scratches=o['scratches'][other],control_scratches=co['scratches'][seat],
            llm_pots=o['metrics'][seat]['pots'],opponent_pots=o['metrics'][other]['pots'],control_pots=co['metrics'][seat]['pots'],
            llm_illegal=o['invalid_actions'][seat],opponent_illegal=o['invalid_actions'][other],control_illegal=co['invalid_actions'][seat],
            reason=o['reason']))
        traces.append(trace);controls.append(control)
    finished=rows[1:];calls=[c for trace in traces for c in trace['call_events']]
    metadata=[c['metadata'] for c in calls];successful=[m for m in metadata if m.get('http_status')==200]
    prior,_,_=accounting(audit_rows(ORIGINAL/'calls.jsonl'))
    smoke,_,_=accounting(audit_rows(SMOKE/'calls.jsonl'))
    current,_,_=accounting(audit_rows(OUTPUT/'calls.jsonl'))
    lat=[m['latency_seconds'] for m in successful]
    control_lat=[r['latency_seconds'] for i,t in enumerate(controls) for r in t['steps'] if r['player']==rows[i]['seat']]
    data=dict(kind='verified_saved_live_results_not_new_API_calls',model=recovery['plan']['model'],rows=rows,
        completed=11,failed=1,not_run=0,llm_results=dict(Counter(r['llm_result'] for r in rows)),
        control_results=dict(Counter(r['control_result'] for r in rows)),
        completed_llm_mean_score=statistics.mean(r['llm_score'] for r in finished),
        completed_opponent_mean_score=statistics.mean(r['opponent_score'] for r in finished),
        paired_control_mean_score=statistics.mean(r['control_score'] for r in finished),
        all12_llm_mean_score=statistics.mean(r['llm_score'] for r in rows),
        all12_control_mean_score=statistics.mean(r['control_score'] for r in rows),
        completed_total_llm_score=sum(r['llm_score'] for r in finished),
        completed_total_opponent_score=sum(r['opponent_score'] for r in finished),
        control_total_score=sum(r['control_score'] for r in rows),
        llm_pots=sum(r['llm_pots'] for r in rows),opponent_pots=sum(r['opponent_pots'] for r in rows),control_pots=sum(r['control_pots'] for r in rows),
        llm_scratches=sum(r['llm_scratches'] for r in rows),opponent_scratches=sum(r['opponent_scratches'] for r in rows),control_scratches=sum(r['control_scratches'] for r in rows),
        llm_illegal=sum(r['llm_illegal'] for r in rows),opponent_illegal=sum(r['opponent_illegal'] for r in rows),control_illegal=sum(r['control_illegal'] for r in rows),
        official_calls=len(calls),successful_calls=len(successful),combined_calls=prior['calls']+smoke['calls']+current['calls'],
        usage=dict(input_tokens=sum(m.get('usage',{}).get('input_tokens',0) for m in successful),
            output_tokens=sum(m.get('usage',{}).get('output_tokens',0) for m in successful),unknown_calls=prior['cost_unknown_calls']),
        latency=dict(successful_total_seconds=sum(lat),successful_mean_seconds=statistics.mean(lat),successful_median_seconds=statistics.median(lat),
            successful_min_seconds=min(lat),successful_max_seconds=max(lat),official_total_seconds=sum(c['latency_seconds'] for c in calls),
            control_total_seconds=sum(control_lat),control_shots=len(control_lat),control_mean_seconds=statistics.mean(control_lat)),
        costs=dict(recovery_estimated_usd=current['known_estimated_usd'],smoke_estimated_usd=smoke['known_estimated_usd'],
            combined_known_usd=current['known_estimated_usd']+smoke['known_estimated_usd'],
            original_unknown_reservation_usd=prior['conservative_charged_or_reserved_usd'],
            conservative_combined_usd=current['conservative_charged_or_reserved_usd']+smoke['conservative_charged_or_reserved_usd']+prior['conservative_charged_or_reserved_usd']),
        scenarios={},source_hashes={p.name:h for p,h in zip(sources,before)},all24_traces_replayed=verify)
    for case in ('direct','bumper','risk'):
        subset=[r for r in rows if r['case']==case];complete=[r for r in subset if r['status']=='complete']
        data['scenarios'][case]=dict(results=dict(Counter(r['llm_result'] for r in subset)),
            completed_mean_llm=statistics.mean(r['llm_score'] for r in complete),
            completed_mean_opponent=statistics.mean(r['opponent_score'] for r in complete),
            paired_mean_control=statistics.mean(r['control_score'] for r in complete),
            all4_mean_llm=statistics.mean(r['llm_score'] for r in subset),all4_mean_control=statistics.mean(r['control_score'] for r in subset))
    if before!=[hashes(p) for p in sources]:raise ValueError('Source evidence changed')
    return data


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify',action='store_true');p.add_argument('--output',type=Path)
    args=p.parse_args();data=analyze(args.verify)
    if args.output:
        if args.output.exists():raise ValueError('Preserve previous derived analysis')
        if any(args.output.resolve().is_relative_to(s.resolve()) for s in (ORIGINAL,SMOKE,OUTPUT)):raise ValueError('Do not alter source evidence')
        args.output.parent.mkdir(parents=True,exist_ok=True);save(args.output,data)
    print(json.dumps({k:v for k,v in data.items() if k!='source_hashes'},indent=2))


if __name__=='__main__':main()
