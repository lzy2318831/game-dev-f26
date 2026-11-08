"""Synthetic HTTP errors only: no provider requests or real credentials."""
import io
import json
import unittest
from unittest.mock import patch,MagicMock
from urllib.error import HTTPError
from fusion.llm import send_openai,CallFailure


class HTTPDiagnostics(unittest.TestCase):
    def error(self,status,error):
        opener=MagicMock()
        opener.open.side_effect=HTTPError('https://api.openai.com/v1/responses',status,'fixture',
            {'x-request-id':'req_fixture_429','Retry-After':'60'},io.BytesIO(json.dumps({'error':error}).encode()))
        with patch.dict('os.environ',{'OPENAI_API_KEY':'offline-test-secret'}),patch('fusion.llm.http.build_opener',return_value=opener):
            with self.assertRaises(CallFailure) as caught:send_openai({'model':'offline-fixture'},1)
        opener.open.assert_called_once()
        return caught.exception.metadata

    def test_429_billing_keeps_provider_details_without_retry(self):
        error=dict(type='insufficient_quota',code='credit_balance_exhausted',param=None,message='Fixture: available API credits exhausted.')
        m=self.error(429,error)
        self.assertEqual(m['provider_error'],error)
        self.assertEqual(m['http_error_category'],'billing_or_quota')
        self.assertEqual(m['provider_request_id'],'req_fixture_429');self.assertEqual(m['retry_after'],'60')

    def test_429_rate_limit_and_unknown_are_distinct(self):
        m=self.error(429,dict(type='rate_limit_error',code='rate_limit_exceeded',message='Fixture: request rate reached.'))
        self.assertEqual(m['http_error_category'],'rate_limit')
        m=self.error(429,{})
        self.assertEqual(m['http_error_category'],'quota_or_rate_limit_unresolved')

    def test_auth_and_unsupported_parameter_redact_secrets(self):
        m=self.error(401,dict(type='invalid_request_error',code='invalid_api_key',message='Bad key offline-test-secret and sk-proj-fixture0123 Bearer fixturetoken'))
        text=json.dumps(m)
        for secret in ('offline-test-secret','sk-proj-fixture0123','fixturetoken'):self.assertNotIn(secret,text)
        self.assertEqual(m['http_error_category'],'authentication')
        m=self.error(400,dict(type='invalid_request_error',code='unsupported_parameter',param='reasoning.effort',message='Fixture: unsupported parameter.'))
        self.assertEqual(m['provider_error']['param'],'reasoning.effort')
        self.assertEqual(m['http_error_category'],'invalid_request_or_parameters')

    def test_non_json_body_is_not_logged(self):
        opener=MagicMock();opener.open.side_effect=HTTPError('https://api.openai.com/v1/responses',502,'fixture',{},io.BytesIO(b'<html>private-debug-body</html>'))
        with patch.dict('os.environ',{'OPENAI_API_KEY':'offline-test-secret'}),patch('fusion.llm.http.build_opener',return_value=opener):
            with self.assertRaises(CallFailure) as caught:send_openai({},1)
        m=caught.exception.metadata
        self.assertEqual(m['provider_error_body_format'],'unavailable_or_non_json')
        self.assertNotIn('private-debug-body',json.dumps(m))
