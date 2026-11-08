import json
from pathlib import Path
import tempfile
import unittest
from fusion.llm import CallFailure
from fusion.api_smoke import run,offline_plan


def success(payload,timeout):
    return dict(status='completed',model=payload['model'],id='offline-fixture',
        _transport_http_status=200,usage=dict(input_tokens=100,output_tokens=20,total_tokens=120),
        output=[dict(type='message',content=[dict(type='output_text',text='{"angle":180,"power":1}')])])


def failure(payload,timeout):
    raise CallFailure('provider_error',dict(http_status=429,error_kind='http_error',provider_error=dict(code='insufficient_quota',message='Synthetic quota error.')))


class APISmoke(unittest.TestCase):
    def test_offline_budget_and_no_network(self):
        plan=offline_plan();self.assertLess(plan['conservative_request_reservation_usd'],.10)
        self.assertEqual(plan['max_api_requests'],1);self.assertLess(plan['budget_usd'],.10)

    def test_one_success_usage_and_recovery_only(self):
        with tempfile.TemporaryDirectory() as d:
            result=run(Path(d)/'smoke',transport=success)
            self.assertEqual(result['api_attempts'],1);self.assertEqual(result['http_status'],200)
            self.assertEqual(result['actual_reported_usage']['input_tokens'],100)
            self.assertLess(result['estimated_cost_usd'],.10)
            self.assertEqual(result['kind'],'OFFLINE_FIXTURE_NOT_REAL_SMOKE')
            recovery=json.loads((Path(d)/'smoke/recovery-plan.json').read_text())
            self.assertEqual(recovery['remaining_original_72_call_allowance'],70)
            self.assertEqual(len(recovery['pending_trial_ids']),11)
            self.assertFalse(recovery['automatic_continuation'])
            with self.assertRaises(FileExistsError):run(Path(d)/'smoke',transport=success)

    def test_one_failure_no_retry_or_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            result=run(Path(d)/'smoke',transport=failure)
            self.assertEqual(result['api_attempts'],1);self.assertEqual(result['status'],'failed')
            self.assertEqual(result['metadata']['provider_error']['code'],'insufficient_quota')
            self.assertFalse((Path(d)/'smoke/recovery-plan.json').exists())
            audit=[json.loads(line) for line in (Path(d)/'smoke/calls.jsonl').read_text().splitlines()]
            self.assertEqual(sum(r['kind']=='request' for r in audit),1)

    def test_non_json_success_status_is_retained(self):
        from unittest.mock import patch,MagicMock
        from fusion.llm import send_openai
        response=MagicMock();response.__enter__.return_value.status=200
        response.__enter__.return_value.read.return_value=b'not-json'
        opener=MagicMock();opener.open.return_value=response
        with patch.dict('os.environ',{'OPENAI_API_KEY':'offline-fixture-key'}),patch('fusion.llm.http.build_opener',return_value=opener):
            with self.assertRaises(CallFailure) as caught:send_openai({},1)
        self.assertEqual(caught.exception.metadata['http_status'],200)
        opener.open.assert_called_once()
