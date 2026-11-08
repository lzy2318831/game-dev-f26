"""Offline development comparison, separate from required live LLM evaluation."""
import json
from pathlib import Path
from statistics import mean
from .runner import run_match,replay


def main():
    suite=json.loads(Path(__file__).with_name('smart-comparison.json').read_text())
    output=Path('evidence/final-15/comparison');output.mkdir(parents=True,exist_ok=True)
    results=[]
    for case in suite['situations']:
        for seed in suite['seeds']:
            for seats in suite['seat_orders']:
                name=f"{case['id']}-{seed}-{'-'.join(seats)}"
                trace=run_match(seed=seed,seats=tuple(seats),layout=[case['cue']]+case['objects'])
                (output/(name+'.json')).write_text(json.dumps(trace,indent=2))
                outcome=trace['outcome']
                replay(trace)
                for i,agent in enumerate(seats):
                    p=f'p{i+1}';steps=[s for s in trace['steps'] if s['player']==p]
                    results.append(dict(situation=case['id'],seed=seed,agent=agent,seat=p,
                        score=outcome['scores'][p],pots=outcome['metrics'][p]['pots'],
                        # Pots during scratched shots still physically disappear.
                        all_pots=sum(v['type']=='pocket' for s in steps for v in s['events']),
                        scratches=outcome['scratches'][p],illegal=outcome['invalid_actions'][p],
                        shots=len(steps),planning_seconds=sum(s['latency_seconds'] for s in steps),
                        win=not outcome['failure'] and outcome['winner']==p,
                        draw=outcome['draw'],failure=outcome['failure'],reason=outcome['reason']))
                print(name,outcome['scores'],outcome['reason'],flush=True)
    summaries={}
    for label in ['all']+[c['id'] for c in suite['situations']]:
        summaries[label]={}
        for agent in ('smart','baseline'):
            rows=[r for r in results if r['agent']==agent and (label=='all' or r['situation']==label)]
            summaries[label][agent]=dict(matches=len(rows),average_score=mean(r['score'] for r in rows),
                object_pots=sum(r['all_pots'] for r in rows),credited_pots=sum(r['pots'] for r in rows),
                wins=sum(r['win'] for r in rows),win_rate=mean(r['win'] for r in rows),
                scratches=sum(r['scratches'] for r in rows),scratch_rate=sum(r['scratches'] for r in rows)/sum(r['shots'] for r in rows),
                illegal_actions=sum(r['illegal'] for r in rows),
                planning_seconds_per_shot=sum(r['planning_seconds'] for r in rows)/sum(r['shots'] for r in rows),
                failures=sum(r['failure'] for r in rows))
    (output/'summary.json').write_text(json.dumps(dict(protocol=suite,results=results,summary=summaries),indent=2))
    print(json.dumps(summaries,indent=2),flush=True)


if __name__=='__main__':main()
