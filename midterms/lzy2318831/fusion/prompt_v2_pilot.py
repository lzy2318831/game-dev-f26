"""Separate three-match pilot. Default and --offline-check never call an API."""
import argparse
import csv
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
from .engine import Episode
from .freeze import main as check_freeze
from .llm import Ledger,PRICES,PRICE_DATE,MAX_OUTPUT,canonical,digest
from .llm_eval import save,metrics
from .llm_resume import ROOT,audit_rows,accounting,hashes
from .prompt_v2 import MODEL,VARIANT,PROMPT_SHA256,ImprovedModelPlayer,offline_response,protected_snapshot
from .runner import run_match,replay

DECLARATION=Path(__file__).with_name('prompt-v2-pilot.json')
LIVE_OUTPUT=ROOT/'evidence/live-prompt-v2-pilot-01'
PREFLIGHT_ROOT=ROOT/'evidence/prompt-v2-pilot-preflight'


class PilotLedger(Ledger):
    def __init__(self,path):super().__init__(path,max_calls=18,budget_usd=.25)


def protocol():
    p=json.loads(DECLARATION.read_text())
    if (p['model']!=MODEL or p['agent_variant']!=VARIANT or p['max_calls']!=18 or p['budget_usd']!=.25
        or len(p['trials'])!=3 or len({t['seed'] for t in p['trials']})!=3):raise ValueError('Pilot declaration changed')
    e=Episode();e.reset(p['trials'][0]['seed'])
    request=ImprovedModelPlayer().request(e.observe('p1'),e.legal_actions('p1'),[])
    p.update(prompt_sha256=PROMPT_SHA256,request_settings={k:v for k,v in request.items() if k!='input'},
        protected_snapshot=protected_snapshot(),
        source_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in (
            'fusion/prompt_v2.py','fusion/prompt_v2_pilot.py','fusion/prompt_v2_pilot_replay.py',
            'fusion/prompt-v2-pilot.json','run-prompt-v2-evaluation.ps1')},
        estimated_usd_at_5000_input_512_output_tokens_per_call=18*(5000*PRICES[MODEL][0]+MAX_OUTPUT*PRICES[MODEL][1])/1e6,
        price_date=PRICE_DATE,live_execution_approved=False)
    p['configuration_sha256']=digest(p)
    return p


def write_summary(output,manifest):
    state,requests,results=accounting(audit_rows(output/'calls.jsonl'));rows=[]
    for record in manifest['trials']:
        m=record.get('metrics',{});o=m.get('outcome',{});seat=record['seat'];other='p2' if seat=='p1' else 'p1'
        attempts=[(n,r) for n,r in requests.items() if r.get('trial')==record['id']]
        replies=[results.get(n,{}).get('metadata',{}) for n,_ in attempts]
        usage=[r.get('usage') for r in replies]
        result=('win' if o.get('winner')==seat else 'loss' if o.get('winner')==other else 'draw' if o.get('draw') else record['status'])
        rows.append(dict(trial=record['id'],seed=record['seed'],seat=seat,status=record['status'],result=result,
            llm_score=m.get('score'),geometric_score=o.get('scores',{}).get(other),
            llm_shots=record.get('llm_shots'),model_calls=len(attempts),
            llm_scratches=o.get('scratches',{}).get(seat),geometric_scratches=o.get('scratches',{}).get(other),
            llm_illegal=m.get('engine_invalid_actions'),geometric_illegal=o.get('invalid_actions',{}).get(other),
            invalid_model_proposals=m.get('invalid_model_proposals'),reason=m.get('reason',record.get('reason')),
            input_tokens=sum((u or {}).get('input_tokens') or 0 for u in usage),
            output_tokens=sum((u or {}).get('output_tokens') or 0 for u in usage),
            usage_unknown_calls=sum(not u or any(type(u.get(k)) is not int for k in ('input_tokens','output_tokens')) for u in usage),
            latency_seconds=sum(r.get('latency_seconds',0) for r in replies),
            latency_unknown_calls=sum('latency_seconds' not in r for r in replies),
            estimated_cost_usd_known=sum(r['estimated_cost_usd'] for r in replies if r.get('estimated_cost_usd') is not None),
            unknown_cost_calls=sum(r.get('estimated_cost_usd') is None for r in replies)))
    manifest['accounting']=state;save(output/'manifest.json',manifest)
    with (output/'comparison.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary=dict(kind=manifest['kind'],agent_variant=VARIANT,rows=rows,accounting=state,
        completed=sum(r['status']=='complete' for r in rows),failed=sum(r['status']=='failed' for r in rows),
        interrupted=sum(r['status']=='interrupted' for r in rows),not_run=sum(r['status']=='not_run' for r in rows),
        wins=sum(r['result']=='win' for r in rows),losses=sum(r['result']=='loss' for r in rows),draws=sum(r['result']=='draw' for r in rows),
        input_tokens_known=sum(r['input_tokens'] for r in rows),output_tokens_known=sum(r['output_tokens'] for r in rows),
        limits=dict(max_calls=18,budget_usd=.25),note='Separate small v2 pilot, not original official results. Seed does not randomize the rack.')
    save(output/'summary.json',summary)
    return summary


def execute(output=LIVE_OUTPUT,approved=False,transport=None):
    output=Path(output).resolve()
    if transport is None:
        if not approved:raise ValueError('Separate live approval is required')
        if output!=LIVE_OUTPUT.resolve():raise ValueError('Use the single fixed live output; never reset caps')
        preflight() # Whole identical fixture workflow must pass before paid dispatch.
        if not os.environ.get('OPENAI_API_KEY'):raise ValueError('Configure the API key locally; never paste it in chat')
    check_freeze();p=protocol();before=protected_snapshot()
    # Atomic refusal also prevents concurrent launches and repeated paid batches.
    output.mkdir(parents=True,exist_ok=False)
    ledger=PilotLedger(output/'calls.jsonl')
    manifest=dict(kind='live_prompt_v2_pilot' if transport is None else 'OFFLINE_V2_PILOT_FIXTURE_NOT_LLM_RESULTS',
        protocol=p,approval_recorded=approved,started_utc=datetime.now(timezone.utc).isoformat(),
        trials=[dict(t,status='pending') for t in p['trials']])
    save(output/'manifest.json',manifest);stop=None
    try:
        for record in manifest['trials']:
            if stop:record.update(status='not_run',reason=stop);continue
            record['status']='running';save(output/'manifest.json',manifest)
            policy=ImprovedModelPlayer(approved=approved,transport=transport);policy.ledger=ledger;ledger.trial=record['id']
            seats=('prompt_v2','baseline') if record['seat']=='p1' else ('baseline','prompt_v2')
            def progress(row):
                with (output/(record['id']+'.steps.jsonl')).open('a',encoding='utf-8') as f:
                    f.write(json.dumps(row,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
                print(json.dumps(dict(trial=record['id'],player=row['player'],source=row['source'],
                    action=row['action'],scores=row['outcome']['scores'])),flush=True)
            try:
                trace=run_match(seed=record['seed'],seats=seats,players={'prompt_v2':policy},
                    model_call_limit=6,request_timeout=20,deadline_seconds=300,on_step=progress)
                trace.update(kind=manifest['kind'],evaluation=dict(agent_variant=VARIANT,trial_id=record['id'],
                    memory='observation_only',model=MODEL,prompt_sha256=PROMPT_SHA256,
                    configuration_sha256=p['configuration_sha256']))
                path=output/(record['id']+'.json');save(path,trace);replay(trace)
                record.update(status='failed' if trace['outcome']['failure'] else 'complete',trace=path.name,
                    metrics=metrics(trace,record['seat']),llm_shots=sum(r['source']=='model' for r in trace['steps']))
                if trace['outcome']['failure']:stop=trace['outcome']['reason']
            except KeyboardInterrupt:
                record.update(status='interrupted',reason='operator_interruption');stop='operator_interruption'
            except Exception as error:
                record.update(status='interrupted',reason='runner_or_replay_error',error_type=type(error).__name__)
                stop='runner_or_replay_error'
            write_summary(output,manifest)
        manifest['finished_utc']=datetime.now(timezone.utc).isoformat();write_summary(output,manifest)
    finally:
        unchanged=before==protected_snapshot()
        save(output/'preservation.json',dict(unchanged=unchanged,before=before))
        if not unchanged:raise ValueError('Protected official evidence or game changed')
    return manifest


def preflight():
    """Full network-free launcher path, content-addressed and never overwritten."""
    check_freeze();p=protocol();directory=PREFLIGHT_ROOT/p['configuration_sha256'][:20]
    target=directory/'verification.json'
    if target.exists():
        saved=json.loads(target.read_text())
        if saved['protocol_sha256']!=p['configuration_sha256'] or saved['protected_snapshot']!=protected_snapshot():
            raise ValueError('Preflight configuration/protected evidence mismatch')
        actual=hashes(directory);actual.pop('verification.json',None)
        if actual!=saved['artifact_hashes']:raise ValueError('Offline preflight evidence changed')
        return dict(saved,directory=str(directory))
    m=execute(directory,transport=offline_response)
    if m['kind']!='OFFLINE_V2_PILOT_FIXTURE_NOT_LLM_RESULTS' or m['accounting']['calls']!=18:
        raise ValueError('Full eighteen-call synthetic workflow did not complete')
    from .recorded_replay import ReplaySession
    outcomes=[]
    for record in m['trials']:
        trace=json.loads((directory/record['trace']).read_text())
        if record['status']!='complete' or record['llm_shots']!=6:raise ValueError('Six-shot offline fixture failed')
        session=ReplaySession(trace,dict(recorded_real_llm=False))
        for row in trace['steps']:
            frame=session.next()
            if not frame['shot']['frames']:raise ValueError('Missing visual frames')
            session.ready()
        if session.state()['outcome']!=trace['outcome']:raise ValueError('Visual-frame replay diverged')
        outcomes.append(trace['outcome'])
    saved=dict(kind='OFFLINE_PREFLIGHT_NOT_LLM_PERFORMANCE',passed=True,real_api_calls=0,synthetic_calls=18,
        protocol_sha256=p['configuration_sha256'],directory=str(directory.relative_to(ROOT)),protected_unchanged=True,
        protected_snapshot=protected_snapshot(),outcomes=outcomes,artifact_hashes=hashes(directory))
    save(target,saved);return dict(saved,directory=str(directory))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline-check',action='store_true');parser.add_argument('--live',action='store_true')
    parser.add_argument('--approve-paid',action='store_true');args=parser.parse_args()
    if args.live:
        if args.offline_check or not args.approve_paid:parser.error('Live requires a separate --approve-paid; cannot combine offline')
        m=execute(approved=True)
        print(json.dumps(dict(kind=m['kind'],accounting=m['accounting'],statuses=[t['status'] for t in m['trials']]),indent=2))
        if any(t['status']!='complete' for t in m['trials']):raise SystemExit(1)
    elif args.offline_check:
        result=preflight();print(json.dumps({k:result[k] for k in ('passed','directory','real_api_calls','synthetic_calls')},indent=2))
    else:print(json.dumps(protocol(),indent=2))


if __name__=='__main__':main()
