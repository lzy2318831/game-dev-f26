"""Real local HTTP lifecycle, synthetic model choices; never paid requests."""
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from fusion.geometry_live import make_geometry_servers
from fusion.geometry_agent import offline_response
from fusion.llm import CallFailure


def failing_response(payload,timeout):
    raise CallFailure('provider_error',dict(error_kind='http_error',http_status=429,network_attempted=False))


def slow_response(payload,timeout):
    time.sleep(2)
    return offline_response(payload,timeout)


class GeometryLifecycle(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.game,self.recorded,self.live=make_geometry_servers(0,0,0,transport=offline_response,root=Path(self.temp.name),power_multiplier=1)
        self.servers=(self.game,self.recorded,self.live)
        self.threads=[threading.Thread(target=s.serve_forever,daemon=True) for s in self.servers]
        for t in self.threads:t.start()
        self.base='http://127.0.0.1:'+str(self.live.server_port)
        self.nonce=self.get('/live/info')['nonce']

    def tearDown(self):
        self.live.live_session.leave()
        for s in self.servers:s.shutdown();s.server_close()
        for t in self.threads:t.join()
        self.temp.cleanup()

    def get(self,path):
        with urlopen(self.base+path) as r:return json.load(r)

    def post(self,path,body=None,nonce=None):
        req=Request(self.base+path,data=json.dumps(body or {}).encode(),headers={
            'Content-Type':'application/json','Origin':self.base,'X-Live-Token':nonce or self.nonce})
        try:
            with urlopen(req,timeout=30) as r:return json.load(r)
        except HTTPError as error:
            error.close();raise

    def complete(self):
        self.post('/live/start',dict(confirmed=True));deadline=time.monotonic()+100
        shots=[]
        while time.monotonic()<deadline:
            state=self.get('/api/state');phase=state['live']['phase']
            if phase=='playback':
                packet=self.get('/live/packet');shots.append(packet['player'])
                self.post('/live/ready',dict(sequence=packet['sequence']))
            elif phase in ('complete','failed','cancelled'):return state,shots
            time.sleep(.01)
        self.fail('HTTP lifecycle timed out')

    def test_two_complete_matches_same_server_with_fresh_consent(self):
        first,shots=self.complete()
        self.assertEqual(first['live']['phase'],'complete',first['live'])
        self.assertEqual(first['outcome']['reason'],'shots_exhausted')
        self.assertEqual(first['outcome']['shots_remaining'],dict(p1=0,p2=0))
        self.assertEqual(shots.count('p1'),6);self.assertEqual(shots.count('p2'),6)
        directory=first['live']['artifact_directory'];old_token=self.nonce
        self.assertTrue(self.post('/live/leave')['safe_to_navigate'])
        prepared=self.post('/live/new');self.nonce=prepared['nonce']
        self.assertNotEqual(self.nonce,old_token)
        self.assertEqual(prepared['state']['outcome']['shots'],0)
        self.assertEqual(prepared['state']['live']['server_budget']['calls'],6)
        # An old token must be refused even if Windows aborts before HTTP status.
        with self.assertRaises((HTTPError,ConnectionAbortedError)):
            self.post('/live/start',dict(confirmed=True),nonce=old_token)
        refused=self.get('/api/state')['live']
        self.assertEqual(refused['calls'],0)
        self.assertEqual(refused['server_budget']['calls'],6)
        with self.assertRaises(HTTPError):self.post('/live/start',dict(confirmed=False))
        second,shots=self.complete()
        self.assertEqual(second['live']['phase'],'complete',second['live'])
        self.assertEqual(second['outcome']['reason'],'shots_exhausted')
        self.assertEqual(second['outcome']['shots'],12)
        self.assertEqual(shots.count('p1'),6);self.assertEqual(shots.count('p2'),6)
        self.assertNotEqual(directory,second['live']['artifact_directory'])
        self.assertEqual(second['live']['server_budget']['calls'],12)
        self.post('/live/leave');prepared=self.post('/live/new');self.nonce=prepared['nonce']
        self.assertFalse(prepared['state']['live']['can_start'])
        self.assertEqual(prepared['state']['live']['server_budget']['calls'],12)
        with self.assertRaises(HTTPError):self.post('/live/start',dict(confirmed=True))

    def test_failure_and_cancel_can_prepare_fresh_match_without_resetting_spend(self):
        self.live.live_session.transport=failing_response
        self.post('/live/start',dict(confirmed=True));deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            state=self.get('/api/state')
            if state['live']['phase']=='failed':break
            time.sleep(.01)
        self.assertEqual(state['live']['phase'],'failed')
        self.assertTrue(state['outcome']['failure']);self.assertEqual(state['outcome']['shots'],0)
        self.assertEqual(state['live']['reason'],'http_error')
        self.post('/live/leave');prepared=self.post('/live/new');self.nonce=prepared['nonce']
        self.assertEqual(prepared['state']['live']['server_budget']['calls'],1)
        self.live.live_session.transport=offline_response
        self.post('/live/start',dict(confirmed=True));self.post('/live/cancel')
        self.assertTrue(self.post('/live/leave')['safe_to_navigate'])
        spent=self.get('/api/state')['live']['server_budget']['calls']
        prepared=self.post('/live/new');self.nonce=prepared['nonce']
        self.assertEqual(prepared['state']['live']['server_budget']['calls'],spent)
        self.assertTrue(prepared['state']['live']['can_start'])

    def test_timeout_is_incomplete_and_unknown_reservation_survives_new_match(self):
        self.live.live_session.transport=slow_response;self.live.live_session.request_timeout=.15
        self.post('/live/start',dict(confirmed=True));deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            state=self.get('/api/state')
            if state['live']['phase']=='failed':break
            time.sleep(.01)
        self.assertEqual(state['live']['phase'],'failed')
        self.assertEqual(state['outcome']['reason'],'request_timeout')
        self.assertTrue(state['outcome']['failure']);self.assertEqual(state['outcome']['shots'],0)
        budget=state['live']['server_budget'];self.assertEqual(budget['unknown_cost_calls'],1)
        self.assertGreater(budget['committed_or_reserved_usd'],0)
        self.post('/live/leave');prepared=self.post('/live/new');self.nonce=prepared['nonce']
        self.assertEqual(prepared['state']['live']['server_budget'],budget)


if __name__=='__main__':unittest.main()
