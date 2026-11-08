"""Offline pilot launcher tests; synthetic transports are never performance data."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from fusion.engine import Episode
from fusion.prompt_v2 import offline_response,VARIANT
from fusion.llm import CallFailure
from fusion.prompt_v2_pilot import protocol,execute,LIVE_OUTPUT,preflight,PilotLedger


def failure(payload,timeout):
    raise CallFailure('provider_error',dict(http_status=429,error_kind='http_error'))


class Pilot(unittest.TestCase):
    def test_declared_scope_and_settings(self):
        p=protocol()
        self.assertEqual(len(p['trials']),3);self.assertEqual(p['max_calls'],18)
        self.assertEqual(p['budget_usd'],.25)
        self.assertEqual(len({t['seed'] for t in p['trials']}),3)
        self.assertEqual([t['seat'] for t in p['trials']],['p1','p2','p1'])
        self.assertEqual(p['agent_variant'],VARIANT)
        self.assertEqual(p['request_settings']['reasoning'],{'effort':'none'})

    def test_unapproved_live_is_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'approval'):execute(Path(d)/'run')
            self.assertFalse((Path(d)/'run').exists())

    def test_live_alternate_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'fixed live output'):
                execute(Path(d)/'alternate',approved=True)
            self.assertFalse((Path(d)/'alternate').exists())

    def test_failure_stops_without_retries_and_preserves_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            output=Path(d)/'run'
            m=execute(output,transport=failure)
            self.assertEqual(m['accounting']['calls'],1)
            self.assertEqual([t['status'] for t in m['trials']],['failed','not_run','not_run'])
            self.assertTrue((output/'calls.jsonl').exists())
            with self.assertRaises(FileExistsError):execute(output,transport=failure)
            self.assertEqual(m['kind'],'OFFLINE_V2_PILOT_FIXTURE_NOT_LLM_RESULTS')

    def test_entire_three_match_workflow_offline(self):
        result=preflight()
        self.assertTrue(result['passed']);self.assertEqual(result['real_api_calls'],0)
        self.assertEqual(result['synthetic_calls'],18)
        self.assertEqual(len(result['outcomes']),3)
        self.assertTrue(result['protected_unchanged'])

    def test_fixture_cannot_be_replayed_as_genuine(self):
        from fusion.prompt_v2_pilot_replay import load_best
        result=preflight()
        with self.assertRaisesRegex(ValueError,'real'):
            load_best(Path(result['directory']))

    def test_interrupted_result_usage_is_in_summary(self):
        def interrupt(**kwargs):
            p=kwargs['players']['prompt_v2'];e=Episode()
            p.select(e.observe('p1'),e.legal_actions('p1'),[],3)
            raise KeyboardInterrupt()
        with tempfile.TemporaryDirectory() as d,patch('fusion.prompt_v2_pilot.run_match',side_effect=interrupt):
            execute(Path(d)/'run',transport=offline_response)
            summary=json.loads((Path(d)/'run/summary.json').read_text());row=summary['rows'][0]
            self.assertEqual(row['model_calls'],1)
            self.assertEqual(row['input_tokens'],100);self.assertEqual(row['output_tokens'],20)
            self.assertGreater(row['latency_seconds'],0)
            self.assertEqual(row['status'],'interrupted');self.assertIsNone(row['llm_score'])

    def test_call_limit_and_unknown_cost_reservations(self):
        from fusion.prompt_v2 import MODEL
        payload=dict(model=MODEL)
        with tempfile.TemporaryDirectory() as d:
            ledger=PilotLedger(Path(d)/'known.jsonl')
            for _ in range(18):
                reserved=ledger.reserve(payload,False);ledger.finish(reserved,dict(estimated_cost_usd=.001))
            with self.assertRaises(CallFailure):ledger.reserve(payload,False)
            self.assertEqual(ledger.calls,18)
            ledger=PilotLedger(Path(d)/'unknown.jsonl')
            large=dict(model=MODEL,input='x'*40000)
            for _ in range(18):
                try:reserved=ledger.reserve(large,False)
                except CallFailure:break
                ledger.finish(reserved,{})
            self.assertLess(ledger.calls,18);self.assertLessEqual(ledger.committed,.25)
            with self.assertRaises(CallFailure):ledger.reserve(large,False)

    def test_preflight_cache_can_be_relocated(self):
        import shutil
        result=preflight();p=protocol()
        with tempfile.TemporaryDirectory() as d:
            relocated=Path(d)/p['configuration_sha256'][:20]
            shutil.copytree(result['directory'],relocated)
            with patch('fusion.prompt_v2_pilot.PREFLIGHT_ROOT',Path(d)):
                cached=preflight()
            self.assertEqual(Path(cached['directory']),relocated)
            self.assertTrue(cached['passed'])

    def test_interrupted_unanswered_request_keeps_unknowns(self):
        def interrupt(**kwargs):
            p=kwargs['players']['prompt_v2'];e=Episode()
            payload=p.request(e.observe('p1'),e.legal_actions('p1'),[])
            p.ledger.reserve(payload,False)
            raise KeyboardInterrupt()
        with tempfile.TemporaryDirectory() as d,patch('fusion.prompt_v2_pilot.run_match',side_effect=interrupt):
            execute(Path(d)/'run',transport=offline_response)
            summary=json.loads((Path(d)/'run/summary.json').read_text());row=summary['rows'][0]
            self.assertEqual(row['model_calls'],1)
            self.assertEqual(row['usage_unknown_calls'],1);self.assertEqual(row['unknown_cost_calls'],1)
            self.assertEqual(summary['accounting']['cost_unknown_calls'],1)
