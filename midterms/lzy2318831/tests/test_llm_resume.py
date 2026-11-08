"""OFFLINE fixtures only: never invokes the real provider."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from fusion import llm_resume as r
from fusion.llm import ModelPlayer, digest
from fusion.engine import Episode
from fusion.runner import replay


class Recovery(unittest.TestCase):
    def test_prior_attempts_and_budget(self):
        p=r.recovery_plan()
        self.assertEqual(p['max_additional_calls'],70)
        self.assertEqual(p['max_expected_new_calls'],66)
        self.assertEqual(len(p['trials']),11)
        self.assertLessEqual(p['additional_budget_usd'],4.9873055)
        self.assertNotIn('observation_only-direct-101-p1',[t['id'] for t in p['trials']])

    def test_ledger_restores_and_never_resets_limits(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'calls.jsonl'
            ledger=r.RecoveryLedger(path,1,1)
            reservation=ledger.reserve({'model':r.MODEL},False)
            ledger.finish(reservation,dict(estimated_cost_usd=.001))
            resumed=r.RecoveryLedger(path,1,1)
            self.assertEqual(resumed.calls,1)
            self.assertAlmostEqual(resumed.committed,.001)
            with self.assertRaises(Exception):resumed.reserve({'model':r.MODEL},False)

    def test_unanswered_request_is_not_retried(self):
        with tempfile.TemporaryDirectory() as d:
            ledger=r.RecoveryLedger(Path(d)/'calls.jsonl',70,1)
            ledger.trial='pending';ledger.reserve({'model':r.MODEL},False)
            with self.assertRaises(r.UnresolvedRequest):r.journal_events(ledger,'pending')
            self.assertEqual(r.RecoveryLedger(ledger.path,70,1).calls,1)

    def test_recorded_response_reused_without_network_and_replay(self):
        record=r.recovery_plan()['trials'][0]
        with tempfile.TemporaryDirectory() as d:
            output=Path(d);ledger=r.RecoveryLedger(output/'calls.jsonl',1,1)
            e=Episode(layout=record['layout']);e.reset(record['seed'])
            # p2 trial: reproduce the first Geometric action before the saved reply.
            if e.active_player!=record['seat']:
                action=r.geometric(e.observe(e.active_player),e.legal_actions(e.active_player))
                player=e.active_player;response=e.step(player,action)
                row=dict(player=player,action=action,accepted=response['accepted'],events=response['events'],
                    after=r.fingerprint(e.observe(player)),outcome=e.outcome(),source='baseline',model_metadata=None,
                    latency_seconds=0,active_elapsed_seconds=0)
                (output/(record['id']+'.steps.jsonl')).write_text(json.dumps(row)+'\n')
            payload=ModelPlayer(r.MODEL,False,False,lambda *_:None).request(e.observe(record['seat']),e.legal_actions(record['seat']),[])
            ledger.trial=record['id'];reservation=ledger.reserve(payload,False)
            ledger.finish(reservation,dict(action={'angle':345,'power':72},request_sha256=digest(payload),
                estimated_cost_usd=.001,latency_seconds=.1,live=False))
            with patch.object(r,'call_model',side_effect=AssertionError('No new request allowed')):
                trace=r.run_trial(record,output,ledger,False,lambda *_:None)
            self.assertEqual(ledger.calls,1)
            self.assertEqual(trace['steps'][1]['decision_origin'],'journal_recovered_no_new_API_call')
            replay(trace)

    def test_corrupt_journal_is_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'calls.jsonl';path.write_text('{partial')
            with self.assertRaises(ValueError):r.RecoveryLedger(path,70,1)
            self.assertEqual(path.read_text(),'{partial')

    def test_exclusive_process_lock(self):
        with tempfile.TemporaryDirectory() as d:
            with r.exclusive_run(Path(d)):
                with self.assertRaises(ValueError):
                    with r.exclusive_run(Path(d)):pass

    def test_prior_evidence_unchanged(self):
        before=(r.hashes(r.ORIGINAL),r.hashes(r.SMOKE))
        r.recovery_plan()
        self.assertEqual(before,(r.hashes(r.ORIGINAL),r.hashes(r.SMOKE)))

    def test_execute_skips_completed_trials_and_preserves_failure(self):
        proposal=r.recovery_plan()
        with tempfile.TemporaryDirectory() as d:
            output=Path(d)
            manifest=dict(kind='OFFLINE_RECOVERY_FIXTURE_NOT_LLM_RESULTS',plan=proposal,
                trials=[dict(t,status='complete') for t in proposal['trials']])
            r.save(output/'manifest.json',manifest)
            with patch.object(r,'run_trial',side_effect=AssertionError('Completed trial replayed')):
                r.execute(output,transport=lambda *_:None)
            summary=json.loads((output/'combined-report/summary.json').read_text())
            self.assertEqual(summary['completed'],11)
            self.assertEqual(summary['failed'],1)
            self.assertEqual(summary['accounting']['combined_api_attempts'],2)
            self.assertEqual(summary['rows'][0]['reason'],'provider_error')
            self.assertFalse((output/'calls.jsonl').exists())

    def test_live_output_cannot_reset_budget(self):
        with tempfile.TemporaryDirectory() as d,patch.dict('os.environ',{'OPENAI_API_KEY':'offline-test-only'}):
            with self.assertRaisesRegex(ValueError,'single approved output'):
                r.execute(Path(d)/'alternate',approved=True)
            self.assertFalse((Path(d)/'alternate').exists())

    def test_interrupted_trials_are_counted(self):
        proposal=r.recovery_plan()
        with tempfile.TemporaryDirectory() as d:
            output=Path(d)
            manifest=dict(kind='OFFLINE_RECOVERY_FIXTURE_NOT_LLM_RESULTS',plan=proposal,
                trials=[dict(t,status='interrupted' if i==0 else 'pending') for i,t in enumerate(proposal['trials'])])
            ledger=r.RecoveryLedger(output/'calls.jsonl',70,proposal['additional_budget_usd'])
            r.combined_report(output,manifest,ledger)
            summary=json.loads((output/'combined-report/summary.json').read_text())
            self.assertEqual((summary['failed'],summary['interrupted'],summary['not_run']),(1,1,10))
