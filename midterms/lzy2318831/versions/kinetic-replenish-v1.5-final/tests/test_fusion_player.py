import json
import unittest
from fusion.engine import Episode
from fusion.player import build_context
from fusion.runner import run_match


class FakePlayer:
    is_model=True
    last_metadata={'live':False,'model':'offline-control-fixture'}
    def decide(self,observation,legal_actions,history,timeout):
        return {'angle':0,'power':30}


class FailedPlayer(FakePlayer):
    def decide(self,*args,**kwargs): raise RuntimeError('private error details')


class FusionPlayerTests(unittest.TestCase):
    def test_public_context_and_counted_budget(self):
        e=Episode()
        context=build_context(e.observe('p1'),e.legal_actions('p1'))
        self.assertNotIn('seed',json.dumps(context))
        with self.assertRaises(ValueError): build_context(dict(e.observe('p1'),world='private'),e.legal_actions('p1'))
        trace=run_match(seats=('model','baseline'),players={'model':FakePlayer()},model_call_limit=1)
        self.assertEqual(trace['model_calls'],1)
        self.assertEqual(trace['outcome']['reason'],'model_call_limit')
        self.assertEqual(trace['steps'][0]['source'],'model')
        self.assertFalse(trace['steps'][0]['model_metadata']['live'])

    def test_failed_request_counts_without_fallback(self):
        trace=run_match(seats=('model','baseline'),players={'model':FailedPlayer()})
        self.assertEqual(trace['model_calls'],1)
        self.assertEqual(trace['outcome']['reason'],'provider_error')
        self.assertEqual(trace['steps'],[])
        self.assertNotIn('private error',json.dumps(trace))
