"""One real request only; never starts an evaluation or retries. Default offline."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from .engine import Episode
from .freeze import main as check_freeze
from .llm import ModelPlayer,Ledger,CallFailure,call_model,canonical,PRICES,MAX_OUTPUT

ROOT=Path(__file__).resolve().parents[1]
MODEL='gpt-5.4-mini-2026-03-17'
BUDGET=.099 # Strictly below $0.10; reserve before any network request.


def context():
    suite=json.loads((ROOT/'fusion/evaluation.json').read_text())
    case=suite['situations'][0]
    episode=Episode(layout=[case['cue']]+case['objects']);episode.reset(101)
    return episode.observe('p1'),episode.legal_actions('p1')


def offline_plan():
    observation,legal=context();payload=ModelPlayer(MODEL).request(observation,legal,[])
    rate=PRICES[MODEL]
    reserve=((len(canonical(payload))+4096)*rate[0]+MAX_OUTPUT*rate[1])/1e6
    return dict(kind='offline_plan_NO_API_CALL',model=MODEL,memory='observation_only',
        max_api_requests=1,budget_usd=BUDGET,conservative_request_reservation_usd=reserve,
        below_ten_cents=reserve<.10,request_sha256=hashlib.sha256(canonical(payload)).hexdigest())


def run(output,approved=False,transport=None):
    if transport is None and not approved:raise ValueError('Explicit single-call approval required')
    if transport is None and not os.environ.get('OPENAI_API_KEY'):raise ValueError('No API key configured; no request made')
    check_freeze()
    original=ROOT/'evidence/live-mini-approved-01'
    manifest=json.loads((original/'manifest.json').read_text())
    if manifest['accounting']['calls']>=72 or manifest['accounting']['conservative_charged_or_reserved_usd']+BUDGET>5:
        raise ValueError('Original aggregate approval has insufficient remaining call/budget allowance')
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    preserved={str(f.relative_to(original)):hashlib.sha256(f.read_bytes()).hexdigest()
        for f in original.rglob('*') if f.is_file()}
    (output/'original-run-hashes.json').write_text(json.dumps(preserved,indent=2))
    ledger=Ledger(output/'calls.jsonl',1,BUDGET);ledger.trial='single-api-smoke'
    policy=ModelPlayer(MODEL,approved,False,transport)
    observation,legal=context()
    result=dict(kind='real_single_api_smoke' if transport is None else 'OFFLINE_FIXTURE_NOT_REAL_SMOKE',
                model=MODEL,max_api_requests=1,budget_usd=BUDGET,status='starting')
    (output/'result.json').write_text(json.dumps(result,indent=2))
    try:
        action,metadata=call_model(policy,observation,legal,[],20,ledger)
        status=metadata.get('http_status')
        if type(status) is not int or not 200<=status<300:
            raise CallFailure('provider_error',dict(metadata,error_kind='missing_success_http_status'))
        result.update(status='success',action=action,metadata=metadata)
    except CallFailure as error:
        result.update(status='failed',reason=str(error),metadata=error.metadata)
    result.update(api_attempts=ledger.calls,http_status=result.get('metadata',{}).get('http_status'),
        actual_reported_usage=result.get('metadata',{}).get('usage'),
        estimated_cost_usd=result.get('metadata',{}).get('estimated_cost_usd'),
        conservative_charged_or_reserved_usd=ledger.committed,cost_unknown_calls=ledger.unknown)
    assert ledger.calls<=1
    assert all(hashlib.sha256((original/n).read_bytes()).hexdigest()==h for n,h in preserved.items())
    result['original_failed_run_unchanged']=True
    # A successful smoke is not an official trial. Prepare a plan only, never execute it.
    if result['status']=='success':
        original_calls=manifest['accounting']['calls']
        old_reserve=manifest['accounting']['conservative_charged_or_reserved_usd']
        recovery=dict(status='AWAITING_USER_APPROVAL_NOT_EXECUTED',
            original_run=str(original.relative_to(ROOT)),smoke_run=str(output),
            pending_trial_ids=[t['id'] for t in manifest['trials'] if t['status']=='not_run'],
            original_failed_attempts=original_calls,smoke_attempts=ledger.calls,
            cumulative_attempts=original_calls+ledger.calls,
            remaining_original_72_call_allowance=72-original_calls-ledger.calls,
            max_calls_for_11_pending_trials=66,
            remaining_original_5_usd_local_budget=5-old_reserve-ledger.committed,
            preserve_first_trial_as_failure=True,automatic_continuation=False)
        if transport is not None:recovery['kind']='OFFLINE_FIXTURE_PLAN_ONLY'
        (output/'recovery-plan.json').write_text(json.dumps(recovery,indent=2))
    (output/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live',action='store_true');parser.add_argument('--approve-paid',action='store_true')
    parser.add_argument('--output',type=Path,default=ROOT/'evidence/api-smoke-mini-01')
    args=parser.parse_args()
    if not args.live:
        check_freeze();print(json.dumps(offline_plan(),indent=2));return
    if not args.approve_paid:parser.error('Single paid smoke requires --approve-paid')
    result=run(args.output,approved=True)
    print(json.dumps(result,indent=2)) # Only parsed action/allowlisted diagnostics, never raw headers/key.
    if result['status']!='success':raise SystemExit(1)


if __name__=='__main__':main()
