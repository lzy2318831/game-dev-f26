import json
import time
import unittest

from pool.model import ModelPlayer, build_context
from pool.engine import Episode
from pool.runner import run_match


def valid_transport(request):
    return {'text': '{"angle":0,"power":1}', 'model': 'offline-test', 'usage': {'input_tokens': 20, 'output_tokens': 8}}


def malformed_transport(request):
    return {'text': 'not JSON'}


def error_transport(request):
    raise RuntimeError('sensitive provider error must not be echoed')


def slow_transport(request):
    time.sleep(10)
    return valid_transport(request)


class ModelTests(unittest.TestCase):
    def test_public_context_and_history_budget(self):
        e = Episode()
        context = build_context(e.observe('p1'), e.legal_actions('p1'), [{'text': 'x' * 3000}])
        self.assertNotIn('history', context)
        self.assertNotIn('seed', json.dumps(context))
        with self.assertRaises(ValueError):
            build_context(dict(e.observe('p1'), private_state='secret'), e.legal_actions('p1'))

    def test_valid_fake_model_and_budget(self):
        model = ModelPlayer('fake', 'offline-test', valid_transport)
        trace = run_match(seats=('model', 'baseline'), players={'model': model}, max_attempts=2, model_call_limit=1)
        self.assertEqual(trace['model_calls'], 1)
        self.assertEqual(trace['steps'][0]['source'], 'model')
        self.assertEqual(trace['steps'][0]['model_metadata']['model'], 'offline-test')
        trace = run_match(seats=('model', 'baseline'), players={'model': model}, model_call_limit=0)
        self.assertEqual(trace['outcome']['reason'], 'model_call_limit')
        self.assertEqual(trace['model_calls'], 0)

    def test_failures_count_and_never_fallback(self):
        for transport, reason in [(malformed_transport, 'invalid_model_response'), (error_transport, 'provider_error')]:
            model = ModelPlayer('fake', 'offline-test', transport)
            trace = run_match(seats=('baseline', 'model'), players={'model': model}, max_attempts=4)
            self.assertEqual(trace['outcome']['reason'], reason)
            self.assertEqual(trace['model_calls'], 1)
            self.assertEqual(len(trace['steps']), 1)
            self.assertEqual(trace['failed_seat'], 'p2')
            self.assertNotIn('sensitive', json.dumps(trace))

    def test_hung_transport_is_terminated(self):
        model = ModelPlayer('fake', 'offline-test', slow_transport, timeout=.15)
        started = time.monotonic()
        trace = run_match(seats=('model', 'baseline'), players={'model': model})
        self.assertEqual(trace['outcome']['reason'], 'request_timeout')
        self.assertEqual(trace['model_calls'], 1)
        self.assertLess(time.monotonic() - started, 3)
