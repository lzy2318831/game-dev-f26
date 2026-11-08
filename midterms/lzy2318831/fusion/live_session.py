"""One consented autonomous browser match; credentials stay in the API adapter."""
from copy import deepcopy
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import secrets
import threading
import time
from . import VERSION
from .baseline import choose
from .engine import Episode,FAILURES
from .llm import Ledger,CallFailure
from .llm_eval import save
from .llm_resume import ROOT,accounting,audit_rows
from .prompt_v2 import MODEL,VARIANT,PROMPT_SHA256,ImprovedModelPlayer,protected_snapshot
from .runner import run_match,fingerprint,replay
from .legacy import VERSION as LEGACY_VERSION,module as legacy_module


class MatchLedger(Ledger):
    def __init__(self,path,cancel_event=None):
        super().__init__(path,6,.25);self.guard=threading.RLock();self.cancel_event=cancel_event
    def reserve(self,payload,live):
        with self.guard:
            if self.cancel_event is not None and self.cancel_event.is_set():
                raise CallFailure('provider_error',dict(error_kind='user_cancelled_before_dispatch',network_attempted=False,
                    estimated_cost_usd=0,usage=dict(input_tokens=0,output_tokens=0,total_tokens=0)))
            return super().reserve(payload,live)
    def finish(self,reserve,metadata):
        with self.guard:return super().finish(reserve,metadata)
    def snapshot(self):
        with self.guard:return accounting(audit_rows(self.path))[0]


class LiveSession:
    """Single match per server launch. Reload/start requests cannot reset caps."""
    policy_type=ImprovedModelPlayer
    variant=VARIANT
    prompt_sha256=PROMPT_SHA256
    trace_kind='LIVE_BROWSER_PROMPT_V2'
    evidence_folder='live-browser-v2'
    seat_name='prompt_v2'
    # Historical prompt-v2 rule facts belong to the preserved v1.5 environment.
    episode_type=legacy_module('engine').Episode
    physics_version=LEGACY_VERSION

    def initial_trace(self):
        return legacy_module('runner').run_match(seed=self.episode.seed,seats=('baseline','baseline'),deadline_seconds=0)
    def make_ledger(self,path):
        return MatchLedger(path,self.cancel_event)
    def __init__(self,root=None,enable_paid=False,transport=None):
        self.root=Path(root) if root is not None else ROOT/'evidence'/self.evidence_folder
        self.enable_paid=enable_paid;self.transport=transport;self.nonce=secrets.token_urlsafe(32)
        self.lock=threading.RLock();self.cancel_event=threading.Event();self.playback_done=threading.Event()
        self.episode=self.episode_type();self.episode.reset(2701201)
        self.phase='waiting';self.stop_reason=None;self.directory=None;self.ledger=None;self.worker=None
        self.pending=None;self.sequence=0;self.trace=None;self.started=None;self.selected=None;self.selected_player=None
        self.request_timeout=20;self.playback_timeout=60;self.session_timeout=600

    def _account(self):
        return self.ledger.snapshot() if self.ledger else dict(calls=0,known_estimated_usd=0,
            cost_unknown_calls=0,conservative_charged_or_reserved_usd=0)

    def state(self):
        with self.lock:
            a=self._account();mock=self.transport is not None
            return dict(version=self.physics_version,mode='hvh',busy=self.phase not in ('waiting','complete','failed','cancelled'),
                observation=self.episode.observe(self.episode.active_player),outcome=self.episode.outcome(),
                live=dict(phase=self.phase,reason=self.stop_reason,model=MODEL,variant=self.variant,mocked=mock,
                    paid_enabled=self.enable_paid,credentials_configured=bool(os.environ.get('OPENAI_API_KEY')),
                    can_start=self.phase=='waiting' and (mock or self.enable_paid and bool(os.environ.get('OPENAI_API_KEY'))),
                    calls=a['calls'],call_cap=6,cost_cap_usd=.25,estimated_cost_usd=a['known_estimated_usd'],
                    committed_or_reserved_usd=a['conservative_charged_or_reserved_usd'],unknown_cost_calls=a['cost_unknown_calls'],
                    sequence=self.pending['sequence'] if self.pending else None,selected_action=self.selected,
                    selected_player=self.selected_player,cancel_requested=self.cancel_event.is_set(),
                    artifact_directory=self.directory.name if self.directory else None))

    def start(self,confirmed,nonce):
        with self.lock:
            if self.phase!='waiting' or confirmed is not True or not isinstance(nonce,str) or not secrets.compare_digest(nonce,self.nonce):
                raise ValueError('Explicit fresh match confirmation required')
            if self.transport is None and (not self.enable_paid or not os.environ.get('OPENAI_API_KEY')):
                raise ValueError('Paid mode must be enabled locally with server-side credentials')
            self.before=protected_snapshot()
            self.directory=self.root/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+secrets.token_hex(6))
            self.directory.mkdir(parents=True,exist_ok=False)
            self.ledger=self.make_ledger(self.directory/'calls.jsonl');self.ledger.trial=self.directory.name
            self.policy=self.policy_type(approved=self.transport is None,transport=self.transport);self.policy.ledger=self.ledger
            self.trace=self.initial_trace()
            self.trace.update(kind=self.trace_kind if self.transport is None else 'MOCKED_LIVE_DEMO_NOT_REAL_LLM',
                seats=[self.seat_name,'baseline'],steps=[],call_events=[],model_calls=0,outcome=self.episode.outcome(),
                limits=dict(shots=12,model_calls=6,estimated_budget_usd=.25,request_timeout=20,session_timeout=600,playback_ack_timeout=60),
                consent=dict(confirmed=True,model=MODEL,variant=self.variant,prompt_sha256=self.prompt_sha256,
                    max_requests=6,budget_usd=.25,scope='one match; no retries; no automatic reset'))
            self.started=time.monotonic();self.phase='starting';self._persist()
            self.worker=threading.Thread(target=self._run,name='fusion-autonomous-live',daemon=True);self.worker.start()
            return self.state()

    def _persist(self):
        if not self.directory:return
        self.trace.update(model_calls=self._account()['calls'],outcome=self.episode.outcome(),
            run_status=self.phase,termination_reason=self.stop_reason,accounting=self._account(),
            elapsed_seconds=time.monotonic()-self.started)
        save(self.directory/'trace.json',self.trace)
        save(self.directory/'status.json',self.state())

    def _stop(self,phase,reason,engine_reason=None):
        if engine_reason and not self.episode.reason:self.episode.abort(engine_reason)
        if phase=='cancelled' and self.episode.reason and not self.episode.outcome()['failure']:
            phase='complete';reason=self.episode.reason
        self.phase=phase;self.stop_reason=reason;self.pending=None;self._persist()
        if self.directory:
            replay(self.trace)
            save(self.directory/'preservation.json',dict(unchanged=self.before==protected_snapshot(),before=self.before))

    def cancel(self):
        # Set this before waiting for the state lock: no returned API action can slip through.
        self.cancel_event.set();self.playback_done.set()
        with self.lock:
            self.playback_done.set() # A concurrent physics step may have cleared the first wake.
            if self.phase=='waiting':self.phase='cancelled';self.stop_reason='user_cancelled_before_confirmation'
            elif self.phase not in ('complete','failed','cancelled'):
                self.phase='stopping';self.stop_reason='user_cancelled';self._persist()
            return self.state()

    def packet(self):
        with self.lock:
            if self.phase!='playback' or not self.pending:raise ValueError('No active shot packet')
            return deepcopy(self.pending)

    def leave(self):
        """Cancel before navigating, then settle the bounded in-flight call/audit."""
        self.cancel()
        worker=self.worker
        if worker is not None and worker is not threading.current_thread():
            worker.join(self.request_timeout+5)
        return dict(safe_to_navigate=worker is None or not worker.is_alive(),state=self.state())

    def ready(self,sequence):
        with self.lock:
            if self.phase!='playback' or not self.pending or type(sequence) is not int or sequence!=self.pending['sequence']:
                raise ValueError('Playback acknowledgment mismatch')
            if self.pending.get('acknowledged'):raise ValueError('Shot already acknowledged')
            self.pending['acknowledged']=True;self.phase='advancing';self.playback_done.set();return self.state()

    def _run(self):
        try:
            while True:
                with self.lock:
                    if self.cancel_event.is_set():self._stop('cancelled','user_cancelled');return
                    if self.episode.reason:
                        self._stop('failed' if self.episode.outcome()['failure'] else 'complete',self.episode.reason);return
                    if time.monotonic()-self.started>=self.session_timeout:
                        self._stop('failed','session_timeout','episode_timeout');return
                    player=self.episode.active_player;obs=self.episode.observe(player);legal=self.episode.legal_actions(player)
                    self.phase='thinking' if player=='p1' else 'geometric';self._persist()
                metadata=None;call_event=None;begin=time.monotonic()
                if player=='p1':
                    try:action,metadata=self.policy.select(obs,legal,[],min(self.request_timeout,max(.001,self.session_timeout-(time.monotonic()-self.started))))
                    except CallFailure as error:
                        with self.lock:
                            self.trace['call_events'].append(dict(player=player,reason=str(error),executed=False,
                                latency_seconds=error.metadata.get('latency_seconds',0),metadata=error.metadata))
                            if self.cancel_event.is_set():self._stop('cancelled','user_cancelled')
                            else:self._stop('failed',error.metadata.get('error_kind',str(error)),str(error) if str(error) in FAILURES else 'provider_error')
                        return
                    with self.lock:
                        call_event=dict(player=player,reason=None,latency_seconds=metadata['latency_seconds'],metadata=metadata,executed=False)
                        self.trace['call_events'].append(call_event)
                else:action=choose(obs,legal)
                latency=time.monotonic()-begin
                with self.lock:
                    if self.cancel_event.is_set():self._stop('cancelled','user_cancelled');return
                    if time.monotonic()-self.started>=self.session_timeout:
                        self._stop('failed','session_timeout','episode_timeout');return
                    self.phase='simulating';self.selected=deepcopy(action);self.selected_player=player
                    before=dict(version=self.physics_version,mode='hvh',observation=obs,outcome=self.episode.outcome())
                    result=self.episode.step(player,action,record_frames=True)
                    if call_event is not None:call_event['executed']=True
                    row=dict(player=player,action=action,accepted=result['accepted'],events=result['events'],
                        after=fingerprint(self.episode.observe(player)),outcome=self.episode.outcome(),
                        source='model' if player=='p1' else 'baseline',model_metadata=metadata,latency_seconds=latency)
                    with (self.directory/'steps.jsonl').open('a',encoding='utf-8') as f:
                        f.write(json.dumps(row,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
                    self.trace['steps'].append(row);self.sequence+=1;self.playback_done.clear()
                    self.phase='playback'
                    self.pending=dict(sequence=self.sequence,player=player,source=row['source'],action=action,
                        shot=result,state=self.state(),before_state=before)
                    self._persist()
                acknowledged=self.playback_done.wait(min(self.playback_timeout,max(0,self.session_timeout-(time.monotonic()-self.started))))
                with self.lock:
                    if self.cancel_event.is_set():self._stop('cancelled','user_cancelled');return
                    if not acknowledged:
                        reason='session_timeout' if time.monotonic()-self.started>=self.session_timeout else 'playback_ack_timeout'
                        self._stop('failed',reason,'episode_timeout');return
                    self.pending=None
        except Exception as error:
            with self.lock:
                if self.trace:self.trace['internal_error_type']=type(error).__name__
                self._stop('failed','backend_error','provider_error')
