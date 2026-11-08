"""Approval-gated real LLM evaluation. Default is a network-free plan."""
import argparse
import csv
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
from . import VERSION
from .freeze import main as check_freeze
from .llm import ModelPlayer,Ledger,PRICES,PRICE_DATE,SYSTEM,digest
from .runner import run_match,replay

ROOT=Path(__file__).resolve().parents[1]


def plan(model,memory='observation_only',opponent='baseline'):
    suite=json.loads((ROOT/'fusion/evaluation.json').read_text())
    conditions=suite['trial_plan']['memory_conditions'] if memory=='both' else [memory]
    trials=[]
    for condition in conditions:
        for case in suite['situations']:
            for seed in suite['trial_plan']['seeds']:
                for seat in suite['trial_plan']['model_seats']:
                    trials.append(dict(id=f'{condition}-{case["id"]}-{seed}-{seat}',
                        memory=condition,case=case['id'],seed=seed,seat=seat,
                        layout=[case['cue']]+case['objects'],opponent=opponent))
    calls=len(trials)*6;rates=PRICES[model]
    result=dict(kind='plan_only_not_live',game_version=VERSION,suite_version=suite['version'],
        suite_sha256=hashlib.sha256((ROOT/'fusion/evaluation.json').read_bytes()).hexdigest(),
        gameplay_freeze_sha256=hashlib.sha256((ROOT/'fusion/gameplay-freeze.json').read_bytes()).hexdigest(),
        prompt_sha256=hashlib.sha256(SYSTEM.encode()).hexdigest(),model=model,provider='openai',
        prices=dict(date=PRICE_DATE,input_per_million=rates[0],output_per_million=rates[1]),
        max_calls=calls,live_matches=len(trials),matched_baseline_controls=len(trials),
        estimated_usd_5000_input_512_output_per_call=calls*(5000*rates[0]+512*rates[1])/1e6,
        note='Estimate, not billing guarantee. Seeds control game, not model sampling. No live results yet.',trials=trials)
    result['agent_code_sha256']=hashlib.sha256(b''.join((ROOT/'fusion'/name).read_bytes() for name in ('llm.py','llm_eval.py','runner.py'))).hexdigest()
    result['configuration_sha256']=digest(result)
    return result


def save(path,value):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value,indent=2,allow_nan=False),encoding='utf-8')
    temporary.replace(path)


def metrics(trace,seat):
    rows=[r for r in trace['steps'] if r['player']==seat]
    calls=[r for r in trace['call_events'] if r['player']==seat]
    metadata=[r.get('metadata') or {} for r in calls]
    return dict(outcome=trace['outcome'],seat=seat,score=trace['outcome']['scores'][seat],
        object_pots=sum(e['type']=='pocket' for r in rows for e in r['events']),
        engine_invalid_actions=trace['outcome']['invalid_actions'][seat],
        invalid_model_proposals=sum(m.get('error_kind') in ('illegal_action_proposal','invalid_action_shape','malformed_json') for m in metadata),
        model_calls=len(calls),latency_seconds=sum(r['latency_seconds'] for r in (calls if calls else rows)),
        usage=[m.get('usage') for m in metadata],
        estimated_cost_usd_known=sum(m['estimated_cost_usd'] for m in metadata if m.get('estimated_cost_usd') is not None),
        unknown_cost_calls=sum(m.get('estimated_cost_usd') is None for m in metadata),
        failure=trace['outcome']['failure'],reason=trace['outcome']['reason'])


def execute(protocol,output,approved,budget,max_calls,transport=None):
    if transport is None and not approved: raise ValueError('Explicit paid-call approval required')
    if transport is None and not os.environ.get('OPENAI_API_KEY'): raise ValueError('OPENAI_API_KEY is not configured; do not paste it into chat')
    check_freeze()
    output=Path(output);output.mkdir(parents=True,exist_ok=False) # Never overwrite evidence.
    ledger=Ledger(output/'calls.jsonl',max_calls,budget)
    manifest=dict(protocol=protocol,kind='live' if transport is None else 'offline_fixture_NOT_LLM_EVIDENCE',
        started_utc=datetime.now(timezone.utc).isoformat(),approval_recorded=approved,
        budget_usd=budget,max_calls=max_calls,trials=[dict(t,status='pending') for t in protocol['trials']])
    save(output/'manifest.json',manifest)
    stop_reason=None
    for record in manifest['trials']:
        if stop_reason:
            record.update(status='not_run',reason=stop_reason);save(output/'manifest.json',manifest);continue
        record['status']='running';save(output/'manifest.json',manifest)
        player=ModelPlayer(protocol['model'],approved,record['memory']=='last_two_visible_shots',transport)
        player.ledger=ledger;ledger.trial=record['id']
        seats=('llm',record['opponent']) if record['seat']=='p1' else (record['opponent'],'llm')
        def progress(row):
            # Commit each authoritative action before console output; survives interruption.
            with (output/(record['id']+'.steps.jsonl')).open('a',encoding='utf-8') as audit:
                audit.write(json.dumps(row,allow_nan=False)+'\n');audit.flush();os.fsync(audit.fileno())
            print(json.dumps(dict(trial=record['id'],player=row['player'],source=row['source'],
                action=row['action'],scores=row['outcome']['scores'])),flush=True)
        try:
            trace=run_match(seed=record['seed'],seats=seats,layout=record['layout'],players={'llm':player},on_step=progress)
            trace['evaluation']=dict(trial_id=record['id'],suite_sha256=protocol['suite_sha256'],
                prompt_sha256=protocol['prompt_sha256'],memory=record['memory'],provider='openai',model=protocol['model'])
            save(output/(record['id']+'.json'),trace);replay(trace)
            record.update(status='failed' if trace['outcome']['failure'] else 'complete',
                          trace=record['id']+'.json',metrics=metrics(trace,record['seat']))
            # Same starting case, seed and target seat; no model in the control.
            control_seats=('baseline',record['opponent']) if record['seat']=='p1' else (record['opponent'],'baseline')
            control=run_match(seed=record['seed'],seats=control_seats,layout=record['layout'])
            save(output/(record['id']+'-control.json'),control);replay(control)
            record['control_metrics']=metrics(control,record['seat'])
            for call in trace['call_events']:
                m=call.get('metadata') or {}
                if m.get('http_status') in (400,401,403,404,429) or m.get('error_kind') in ('run_call_or_cost_budget','missing_credentials'):
                    stop_reason=m.get('error_kind','provider_configuration');break
            if ledger.calls>=max_calls:stop_reason='run_call_budget'
        except Exception:
            # Keep prior requests/trace and mark interrupted/runner failure plainly.
            record.update(status='runner_error',reason='runner_or_replay_error')
            stop_reason='runner_or_replay_error'
        save(output/'manifest.json',manifest)
    manifest['finished_utc']=datetime.now(timezone.utc).isoformat()
    manifest['accounting']=dict(calls=ledger.calls,known_estimated_usd=ledger.estimated,
        cost_unknown_calls=ledger.unknown,conservative_charged_or_reserved_usd=ledger.committed)
    save(output/'manifest.json',manifest)
    report(output)
    return manifest


def report(output):
    output=Path(output);manifest=json.loads((output/'manifest.json').read_text())
    rows=[]
    for t in manifest['trials']:
        m=t.get('metrics',{});o=m.get('outcome',{})
        rows.append(dict(trial=t['id'],memory=t['memory'],case=t['case'],seed=t['seed'],seat=t['seat'],
            status=t['status'],reason=m.get('reason',t.get('reason')),score=m.get('score'),
            opponent_score=o.get('scores',{}).get('p2' if t['seat']=='p1' else 'p1'),
            winner=o.get('winner'),failure=o.get('failure'),object_pots=m.get('object_pots'),
            invalid_actions=m.get('engine_invalid_actions'),invalid_proposals=m.get('invalid_model_proposals'),
            calls=m.get('model_calls'),latency_seconds=m.get('latency_seconds'),
            input_tokens=sum((u or {}).get('input_tokens') or 0 for u in m.get('usage',[])),
            output_tokens=sum((u or {}).get('output_tokens') or 0 for u in m.get('usage',[])),
            usage_unknown_calls=sum(not u or any(type(u.get(k)) is not int or u[k]<0 for k in ('input_tokens','output_tokens')) for u in m.get('usage',[])),
            known_estimated_cost_usd=m.get('estimated_cost_usd_known'),unknown_cost_calls=m.get('unknown_cost_calls'),
            matched_baseline_score=t.get('control_metrics',{}).get('score'),
            matched_baseline_latency_seconds=t.get('control_metrics',{}).get('latency_seconds')))
    with (output/'comparison.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]) if rows else ['trial']);writer.writeheader();writer.writerows(rows)
    save(output/'summary.json',dict(kind=manifest['kind'],planned=len(rows),
        completed=sum(r['status']=='complete' for r in rows),failed=sum(r['status'] in ('failed','runner_error') for r in rows),
        interrupted=sum(r['status']=='running' for r in rows),not_run=sum(r['status'] in ('not_run','pending') for r in rows),
        rows=rows,accounting=manifest.get('accounting',{'status':'run_incomplete; inspect append-only audit'})))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provider',choices=['openai'])
    parser.add_argument('--model',choices=sorted(PRICES))
    parser.add_argument('--memory',choices=['observation_only','last_two_visible_shots','both'],default='observation_only')
    parser.add_argument('--opponent',choices=['baseline','smart'],default='baseline')
    parser.add_argument('--live',action='store_true');parser.add_argument('--approve-paid',action='store_true')
    parser.add_argument('--budget-usd',type=float);parser.add_argument('--max-calls',type=int)
    parser.add_argument('--output',type=Path);parser.add_argument('--summarize',type=Path)
    args=parser.parse_args()
    if args.summarize:report(args.summarize);return
    if args.max_calls is not None and args.max_calls<1:parser.error('--max-calls must be positive')
    protocol=plan(args.model or 'gpt-5.4-mini-2026-03-17',args.memory,args.opponent)
    if not args.live:
        print(json.dumps(protocol,indent=2));return
    if not args.approve_paid or not args.provider or not args.model or args.budget_usd is None or args.output is None:
        parser.error('Live requires explicit --approve-paid --provider --model --budget-usd --output')
    execute(protocol,args.output,True,args.budget_usd,args.max_calls if args.max_calls is not None else protocol['max_calls'])


if __name__=='__main__':main()
