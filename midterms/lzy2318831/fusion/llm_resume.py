"""Journaled continuation of the eleven approved, previously not-run trials.

No network by default. Original failed run and smoke evidence are immutable.
Only already-recorded genuine model decisions may be replayed after interruption.
Unknown/incomplete requests fail closed, never retried automatically.
"""
import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime,timezone
from decimal import Decimal,ROUND_FLOOR
import hashlib
import json
import math
import os
from pathlib import Path
import time
from . import VERSION
from .engine import Episode
from .freeze import main as check_freeze
from .llm import ModelPlayer,Ledger,CallFailure,call_model,digest,SYSTEM
from .baseline import choose as geometric
from .runner import replay,fingerprint
from .llm_eval import plan,metrics,save,report

ROOT=Path(__file__).resolve().parents[1]
MODEL='gpt-5.4-mini-2026-03-17'
ORIGINAL=ROOT/'evidence/live-mini-approved-01'
SMOKE=ROOT/'evidence/api-smoke-mini-01'
OUTPUT=ROOT/'evidence/live-mini-recovery-01'


def hashes(folder):
    return {str(f.relative_to(folder)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in folder.rglob('*') if f.is_file()}


def audit_rows(path):
    if not path.exists():return []
    # Partial/corrupt lines are retained, not truncated or silently discarded.
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]


def accounting(rows):
    requests={};results={};committed=Decimal(0);known=Decimal(0)
    for row in rows:
        number=row.get('call')
        if type(number) is not int or number<1:raise ValueError('Invalid audit call index')
        if row['kind']=='request':
            if number!=len(requests)+1:raise ValueError('Duplicate/missing audit request')
            if row['request_sha256']!=digest(row['request']):raise ValueError('Request audit hash mismatch')
            amount=Decimal(str(row['reserved_usd']))
            if not amount.is_finite() or amount<0:raise ValueError('Invalid reservation')
            requests[number]=row;committed+=amount
        elif row['kind']=='result':
            if number not in requests or number in results:raise ValueError('Unpaired/duplicate result')
            results[number]=row
            cost=row['metadata'].get('estimated_cost_usd')
            if cost is not None:
                cost=Decimal(str(cost))
                if not cost.is_finite() or cost<0:raise ValueError('Invalid usage cost')
                known+=cost;committed+=cost-Decimal(str(requests[number]['reserved_usd']))
        else:raise ValueError('Unexpected audit record')
    unknown=sum(n not in results or results[n]['metadata'].get('estimated_cost_usd') is None for n in requests)
    return dict(calls=len(requests),known_estimated_usd=float(known),cost_unknown_calls=unknown,
                conservative_charged_or_reserved_usd=float(committed)),requests,results


def recovery_plan():
    check_freeze()
    old=json.loads((ORIGINAL/'manifest.json').read_text())
    smoke=json.loads((SMOKE/'result.json').read_text())
    fresh=plan(MODEL,'observation_only','baseline')
    if old['protocol']['model']!=MODEL or old['protocol']['suite_sha256']!=fresh['suite_sha256'] or old['protocol']['prompt_sha256']!=fresh['prompt_sha256']:
        raise ValueError('Original evaluation model/scenario/prompt mismatch')
    if smoke['status']!='success' or smoke['kind']!='real_single_api_smoke' or smoke['model']!=MODEL or smoke['http_status']!=200 or not smoke['metadata']['live']:
        raise ValueError('Successful genuine pinned-model smoke evidence required')
    if smoke['metadata']['prompt_sha256']!=fresh['prompt_sha256']:raise ValueError('Smoke prompt mismatch')
    a,_,_=accounting(audit_rows(ORIGINAL/'calls.jsonl'))
    b,_,_=accounting(audit_rows(SMOKE/'calls.jsonl'))
    if a['calls']!=1 or b['calls']!=1:raise ValueError('Prior history differs from approved two-attempt recovery')
    pending=[deepcopy(t) for t in old['trials'] if t['status']=='not_run']
    if len(pending)!=11 or sum(t['status']=='failed' for t in old['trials'])!=1:raise ValueError('Expected one preserved failure and eleven not-run trials')
    expected={t['id']:t for t in fresh['trials']}
    for trial in pending:
        for key in ('memory','case','seed','seat','layout','opponent'):
            if trial[key]!=expected[trial['id']][key]:raise ValueError('Pending trial changed')
    remaining=(Decimal(5)-Decimal(str(a['conservative_charged_or_reserved_usd']))-Decimal(str(b['conservative_charged_or_reserved_usd']))).quantize(Decimal('.000000000001'),rounding=ROUND_FLOOR)
    if remaining<=0:raise ValueError('No remaining original budget')
    return dict(kind='approved_recovery_plan_NO_CALLS_YET',model=MODEL,memory='observation_only',opponent='baseline',
        original_api_attempts=a['calls'],smoke_api_attempts=b['calls'],max_additional_calls=72-a['calls']-b['calls'],
        original_costs=a,smoke_costs=b,additional_budget_usd=float(remaining),original_combined_cap_usd=5,
        planned_live_trials=11,planned_matched_controls=11,max_expected_new_calls=66,
        original_failure_retained=True,smoke_is_not_official_trial=True,
        protocol=fresh,trials=[expected[t['id']] for t in pending],
        original_hashes=hashes(ORIGINAL),smoke_hashes=hashes(SMOKE),
        recovery_code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


class RecoveryLedger(Ledger):
    def __init__(self,path,max_calls,budget_usd):
        self.path=Path(path);self.max_calls=max_calls;self.budget_usd=budget_usd;self.trial=None
        state,_,_=accounting(audit_rows(self.path))
        self.calls=state['calls'];self.committed=state['conservative_charged_or_reserved_usd']
        self.estimated=state['known_estimated_usd'];self.unknown=state['cost_unknown_calls']
        if self.calls>max_calls or self.committed>budget_usd:raise ValueError('Persisted run exceeds approval')


@contextmanager
def exclusive_run(output):
    output.mkdir(parents=True,exist_ok=True)
    handle=(output/'run.lock').open('a+b')
    if handle.seek(0,2)==0:handle.write(b'0');handle.flush()
    handle.seek(0)
    try:
        if os.name=='nt':
            import msvcrt
            msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except Exception:
        handle.close();raise ValueError('Recovery already running; no concurrent evaluation allowed') from None
    try:yield
    finally:handle.close() # OS releases on exit/crash too; no stale lock deletion.


class UnresolvedRequest(Exception):pass


def journal_events(ledger,trial):
    _,requests,results=accounting(audit_rows(ledger.path))
    pairs=[]
    for number,r in requests.items():
        if r.get('trial')!=trial:continue
        if number not in results:raise UnresolvedRequest('Paid attempt has no durable result; do not resend automatically')
        pairs.append((r,results[number]['metadata']))
    return pairs


def run_trial(record,output,ledger,approved,transport=None):
    """Replay committed steps, reuse any journaled model reply, then continue."""
    e=Episode(layout=record['layout']);e.reset(record['seed'])
    path=output/(record['id']+'.steps.jsonl');rows=audit_rows(path)
    for row in rows:
        response=e.step(row['player'],row['action'])
        if response['accepted']!=row['accepted'] or response['events']!=row['events'] or fingerprint(e.observe(row['player']))!=row['after'] or e.outcome()!=row['outcome']:
            raise ValueError('Committed-step replay diverged')
    used={row['model_metadata']['request_sha256'] for row in rows if row['source']=='model'}
    prior_elapsed=rows[-1].get('active_elapsed_seconds',0) if rows else 0
    begin=time.monotonic();player=ModelPlayer(MODEL,approved,False,transport)
    ledger.trial=record['id']
    while not e.reason:
        elapsed=prior_elapsed+time.monotonic()-begin
        if elapsed>=300:e.abort('episode_timeout');break
        seat=e.active_player;metadata=None;origin='fresh'
        if seat==record['seat']:
            pairs=journal_events(ledger,record['id'])
            outstanding=[(r,m) for r,m in pairs if r['request_sha256'] not in used]
            if len(outstanding)>1:raise ValueError('Multiple uncommitted replies; review required')
            if outstanding:
                r,metadata=outstanding[0]
                expected=digest(player.request(e.observe(seat),e.legal_actions(seat),[]))
                if r['request_sha256']!=expected:raise ValueError('Cached reply belongs to different game state')
                if metadata.get('failure'):e.abort(metadata['failure']);break
                action=metadata.get('action')
                if not e.valid(action):raise ValueError('No recorded legal LLM decision; cannot substitute')
                prior_elapsed+=metadata.get('latency_seconds',0)
                origin='journal_recovered_no_new_API_call'
            else:
                if ledger.calls>=ledger.max_calls:e.abort('model_call_limit');break
                try:action,metadata=call_model(player,e.observe(seat),e.legal_actions(seat),[],min(20,300-elapsed),ledger)
                except CallFailure as error:
                    record['last_call_error']=error.metadata;e.abort(str(error));break
            used.add(metadata['request_sha256'])
        else:
            planning_start=time.monotonic()
            action=geometric(e.observe(seat),e.legal_actions(seat))
            planning_latency=time.monotonic()-planning_start
        if prior_elapsed+time.monotonic()-begin>=300:e.abort('episode_timeout');break
        response=e.step(seat,action)
        row=dict(player=seat,action=action,accepted=response['accepted'],events=response['events'],
            after=fingerprint(e.observe(seat)),outcome=e.outcome(),
            source='model' if seat==record['seat'] else 'baseline',model_metadata=metadata,
            latency_seconds=metadata['latency_seconds'] if metadata else planning_latency,
            decision_origin=origin,active_elapsed_seconds=prior_elapsed+time.monotonic()-begin)
        with path.open('a',encoding='utf-8') as audit:
            audit.write(json.dumps(row,allow_nan=False)+'\n');audit.flush();os.fsync(audit.fileno())
        rows.append(row)
        print(json.dumps(dict(trial=record['id'],player=seat,source=row['source'],action=action,scores=e.scores)),flush=True)
    calls=[dict(player=record['seat'],reason=m.get('failure'),latency_seconds=m.get('latency_seconds',0),metadata=m)
           for _,m in journal_events(ledger,record['id'])]
    # Reuse the authoritative trace header without asking a policy or calling an API.
    from .runner import run_match
    header=run_match(seed=record['seed'],seats=('baseline','baseline'),layout=record['layout'],deadline_seconds=0)
    header.update(seats=['llm','baseline'] if record['seat']=='p1' else ['baseline','llm'],
        steps=rows,call_events=calls,model_calls=len(calls),outcome=e.outcome(),
        elapsed_seconds=prior_elapsed+time.monotonic()-begin,
        evaluation=dict(trial_id=record['id'],memory='observation_only',provider='openai',model=MODEL,
                        recovery=True,original_failed_trial_not_retried=True))
    replay(header)
    return header


def combined_report(output,manifest,ledger):
    old=json.loads((ORIGINAL/'manifest.json').read_text());merged=deepcopy(old)
    replacements={t['id']:t for t in manifest['trials']}
    merged['trials']=[deepcopy(replacements.get(t['id'],t)) for t in old['trials']]
    merged['kind']='live' if manifest['kind']=='live_recovery' else 'OFFLINE_RECOVERY_FIXTURE_NOT_LLM_RESULTS'
    base=manifest['plan'];state,_,_=accounting(audit_rows(ledger.path))
    merged['accounting']=dict(combined_api_attempts=2+state['calls'],combined_attempt_limit=72,
        known_estimated_usd=base['original_costs']['known_estimated_usd']+base['smoke_costs']['known_estimated_usd']+state['known_estimated_usd'],
        conservative_charged_or_reserved_usd=base['original_costs']['conservative_charged_or_reserved_usd']+base['smoke_costs']['conservative_charged_or_reserved_usd']+state['conservative_charged_or_reserved_usd'],
        cost_unknown_calls=base['original_costs']['cost_unknown_calls']+base['smoke_costs']['cost_unknown_calls']+state['cost_unknown_calls'],
        smoke_usage_separate=json.loads((SMOKE/'result.json').read_text())['actual_reported_usage'])
    folder=output/'combined-report';folder.mkdir(exist_ok=True)
    for trial in merged['trials']:
        if trial.get('trace'):
            trial['trace']=str(Path('..')/trial['trace']) if trial['id'] in replacements else str(Path('..')/'..'/ORIGINAL.name/trial['trace'])
    save(folder/'manifest.json',merged);report(folder)
    summary=json.loads((folder/'summary.json').read_text())
    rows=summary['rows'];known=[t for t in rows if t['score'] is not None]
    summary['interrupted']=sum(t['status'] in ('running','interrupted') for t in rows)
    summary['totals']=dict(scores=sum(t['score'] for t in known),
        completed_match_scores=[dict(trial=t['trial'],score=t['score'],opponent_score=t['opponent_score']) for t in rows if t['status']=='complete'],
        input_tokens=sum(t['input_tokens'] for t in rows),output_tokens=sum(t['output_tokens'] for t in rows),
        official_trial_calls=sum(t['calls'] or 0 for t in rows),
        usage_unknown_calls=sum(t['usage_unknown_calls'] for t in rows),
        invalid_actions=sum(t['invalid_actions'] or 0 for t in rows),invalid_proposals=sum(t['invalid_proposals'] or 0 for t in rows),
        latency_seconds=sum(t['latency_seconds'] or 0 for t in rows),
        note='Smoke usage/cost is separate in accounting; failed trial remains included. Unknown usage is not zero usage.')
    save(folder/'summary.json',summary)


def execute(output,approved=False,transport=None):
    if transport is None and not approved:raise ValueError('Explicit continuation approval required')
    if transport is None and not os.environ.get('OPENAI_API_KEY'):raise ValueError('Configure API key locally; never paste into chat')
    proposal=recovery_plan();output=Path(output).resolve()
    if transport is None and output!=OUTPUT.resolve():
        raise ValueError('Live continuation must use the single approved output; cannot reset aggregate limits')
    if any(output==source.resolve() or source.resolve() in output.parents for source in (ORIGINAL,SMOKE)):
        raise ValueError('Cannot write into prior evidence')
    with exclusive_run(output):
        target=output/'manifest.json';kind='live_recovery' if transport is None else 'OFFLINE_RECOVERY_FIXTURE_NOT_LLM_RESULTS'
        if target.exists():
            manifest=json.loads(target.read_text())
            if manifest['kind']!=kind or manifest['plan']!=proposal:raise ValueError('Recovery configuration/evidence changed; do not reset limits')
            if manifest.get('hold_reason'):raise ValueError('Prior unresolved/provider error requires review; no automatic retry')
        else:
            if any(p.name!='run.lock' for p in output.iterdir()):raise ValueError('Unrecognized existing output; preserve and inspect')
            manifest=dict(kind=kind,plan=proposal,approval_recorded=approved,
                started_utc=datetime.now(timezone.utc).isoformat(),
                trials=[dict(t,status='pending') for t in proposal['trials']])
            save(target,manifest)
        ledger=RecoveryLedger(output/'calls.jsonl',proposal['max_additional_calls'],proposal['additional_budget_usd'])
        for record in manifest['trials']:
            if record['status'] in ('complete','failed'):continue
            record['status']='running';save(target,manifest)
            try:
                trace_path=output/(record['id']+'.json')
                if trace_path.exists():trace=json.loads(trace_path.read_text());replay(trace)
                else:
                    trace=run_trial(record,output,ledger,approved,transport);save(trace_path,trace)
                record.update(trace=trace_path.name,metrics=metrics(trace,record['seat']))
                control_path=output/(record['id']+'-control.json')
                if control_path.exists():control=json.loads(control_path.read_text());replay(control)
                else:
                    from .runner import run_match
                    control=run_match(seed=record['seed'],seats=('baseline','baseline'),layout=record['layout'])
                    save(control_path,control);replay(control)
                record['control_metrics']=metrics(control,record['seat'])
                record['status']='failed' if trace['outcome']['failure'] else 'complete'
                for call in trace['call_events']:
                    m=call.get('metadata') or {}
                    if m.get('http_status') in (400,401,403,404,429) or m.get('error_kind') in ('run_call_or_cost_budget','missing_credentials'):
                        manifest['hold_reason']='provider_or_budget_error_requires_review'
                if trace['outcome']['reason']=='model_call_limit':manifest['hold_reason']='call_budget_exhausted'
            except UnresolvedRequest:
                record['status']='interrupted';manifest['hold_reason']='paid_request_missing_result_do_not_retry'
            except KeyboardInterrupt:
                record['status']='interrupted';save(target,manifest);combined_report(output,manifest,ledger);raise
            except Exception:
                record['status']='interrupted';manifest['hold_reason']='checkpoint_or_replay_error_requires_review'
            state,_,_=accounting(audit_rows(ledger.path));manifest['accounting']=state
            save(target,manifest);combined_report(output,manifest,ledger)
            if manifest.get('hold_reason'):break
        assert hashes(ORIGINAL)==proposal['original_hashes'] and hashes(SMOKE)==proposal['smoke_hashes']
        combined_report(output,manifest,ledger)
        return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live',action='store_true');parser.add_argument('--approve-paid',action='store_true')
    parser.add_argument('--output',type=Path,default=OUTPUT)
    args=parser.parse_args()
    if not args.live:
        p=recovery_plan();print(json.dumps(p,indent=2));return
    if not args.approve_paid:parser.error('Explicit approval flag required')
    m=execute(args.output,True)
    print(json.dumps(dict(status='stopped_for_review' if m.get('hold_reason') else 'finished',
                         accounting=m.get('accounting'),hold_reason=m.get('hold_reason')),indent=2))
    if m.get('hold_reason'):raise SystemExit(1)


if __name__=='__main__':main()
