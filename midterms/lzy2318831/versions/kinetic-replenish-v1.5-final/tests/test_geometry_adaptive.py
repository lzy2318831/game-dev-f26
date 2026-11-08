"""Adaptive mode is separate; legacy request payloads remain rollback fixtures."""
import importlib.util
import json
from pathlib import Path
import unittest
import time
import test_geometry_lifecycle as lifecycle
from urllib.error import HTTPError
from fusion.engine import Episode
from fusion.geometry_agent import GeometryPlayer


class AdaptivePower(unittest.TestCase):
    def test_legacy_1x_2x_requests_are_unchanged(self):
        spec=importlib.util.spec_from_file_location('fusion._pre_adaptive',Path('evidence/power-calibration-01/baseline/fusion/geometry_agent.py'))
        before=importlib.util.module_from_spec(spec);spec.loader.exec_module(before)
        e=Episode()
        for multiplier in (1,2):
            self.assertEqual(GeometryPlayer(power_multiplier=multiplier).request(e.observe('p1'),e.legal_actions('p1')),
                before.GeometryPlayer(power_multiplier=multiplier).request(e.observe('p1'),e.legal_actions('p1')))

    def test_distance_route_floors_caps_and_escape(self):
        from fusion.geometry_adaptive_power import adaptive_recommendations
        rows=[dict(id=i,angle=0,target=1,route=route,travel=d,power=p,risk='base')
              for i,(route,d,p) in enumerate([('contact',100,1),('contact',200,5),('contact',400,22),
                  ('bank-contact',200,10),('pot',200,60),('fallback-escape',50,1)],1)]
        result=adaptive_recommendations(rows)
        self.assertEqual([r['power'] for r in result],[25,35,50,40,100,2])
        self.assertEqual(rows[0]['power'],1)
        for a,b in zip(rows,result):
            self.assertEqual((a['id'],a['angle'],a['target'],a['route']),
                             (b['id'],b['angle'],b['target'],b['route']))

    def test_adaptive_is_explicit_and_uses_genuine_candidate_ids(self):
        e=Episode();player=GeometryPlayer(adaptive=True)
        payload=player.request(e.observe('p1'),e.legal_actions('p1'))
        context=json.loads(payload['input'][1]['content'])
        self.assertEqual(context['power_mode'],'adaptive')
        self.assertIsNone(context['power_multiplier'])
        self.assertEqual(player.power_mode,'adaptive')
        self.assertNotEqual(payload['input'][0]['content'],GeometryPlayer().request(e.observe('p1'),e.legal_actions('p1'))['input'][0]['content'])

    def test_runtime_matches_tested_profile_on_all_saved_observations(self):
        from fusion.geometry_adaptive_power import adaptive_recommendations
        from fusion.geometry_power_calibration import observations,proposed_power
        from fusion.geometry_candidates import candidates
        for case in observations():
            rows=candidates(case['observation'],case['legal'])
            for base,changed in zip(rows,adaptive_recommendations(rows)):
                self.assertEqual(changed['power'],proposed_power(base,'floor25-35-50'))

    def test_known_position_adaptive_25_settles(self):
        from fusion.geometry_power_calibration import observations
        from fusion.smart import Simulation
        case=next(c for c in observations() if c['source'].endswith('8dbde2c0c71f') and c['model_shot']==4)
        payload=GeometryPlayer(adaptive=True).request(case['observation'],case['legal'])
        row=next(r for r in json.loads(payload['input'][1]['content'])['candidates'] if r['route']=='contact' and r['target']==5)
        self.assertEqual((row['angle'],row['power']),(266,25))
        sim=Simulation(case['observation'],dict(angle=266,power=25));sim.advance(9600)
        self.assertTrue(sim.result()['settled']);self.assertEqual(sim.result()['ticks'],844)


class AdaptiveHTTP(unittest.TestCase):
    setUp=lifecycle.GeometryLifecycle.setUp
    tearDown=lifecycle.GeometryLifecycle.tearDown
    get=lifecycle.GeometryLifecycle.get
    post=lifecycle.GeometryLifecycle.post

    def test_setting_trace_active_lock_fresh_match_and_rollback(self):
        state=self.post('/live/power',dict(power_mode='adaptive'))
        self.assertEqual(state['live']['power_mode'],'adaptive')
        self.assertIsNone(state['live']['power_multiplier'])
        self.assertEqual(state['live']['server_budget']['calls'],0)
        self.post('/live/start',dict(confirmed=True));deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            state=self.get('/api/state')
            if state['live']['phase'] in ('playback','failed'):break
            time.sleep(.01)
        self.assertEqual(state['live']['phase'],'playback')
        packet=self.get('/live/packet');self.assertEqual(packet['action']['power'],50)
        trace=self.live.live_session.trace
        self.assertEqual(trace['power_mode'],'adaptive')
        self.assertEqual(trace['consent']['power_mode'],'adaptive')
        self.assertEqual(trace['steps'][0]['model_metadata']['power_mode'],'adaptive')
        with self.assertRaises(HTTPError):self.post('/live/power',dict(power_multiplier=1))
        self.post('/live/cancel');self.post('/live/leave')
        # Navigation is bounded; new-match creation must still await settlement.
        self.live.live_session.worker.join(10)
        self.assertFalse(self.live.live_session.worker.is_alive())
        fresh=self.post('/live/new');self.nonce=fresh['nonce']
        self.assertEqual(fresh['state']['live']['power_mode'],'adaptive')
        budget=fresh['state']['live']['server_budget']
        for multiplier in (1,2):
            state=self.post('/live/power',dict(power_multiplier=multiplier))
            self.assertEqual(state['live']['power_mode'],str(multiplier)+'x')
            self.assertEqual(state['live']['server_budget'],budget)


if __name__=='__main__':unittest.main()
