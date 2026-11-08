"""Student-selected power option; all model responses remain synthetic."""
import json
from copy import deepcopy
import tempfile
from pathlib import Path
import unittest
import time
import test_geometry_lifecycle as lifecycle
from urllib.error import HTTPError
from fusion.geometry_agent import GeometryPlayer,offline_response,select_candidate,parse_selection
from fusion.geometry_candidates import candidates
from fusion.geometry_live import GeometrySession,make_geometry_servers
from fusion.engine import Episode


class PowerSetting(unittest.TestCase):
    def test_only_candidate_power_changes_and_selection_is_genuine(self):
        e=Episode();o=e.observe('p1');legal=e.legal_actions('p1');before=deepcopy(o)
        a=GeometryPlayer(power_multiplier=1).request(o,legal)
        b=GeometryPlayer(power_multiplier=2).request(o,legal)
        original=json.loads(a['input'][1]['content'])['candidates']
        changed=json.loads(b['input'][1]['content'])['candidates']
        for x,y in zip(original,changed):
            for key in ('id','angle','target','route','minimum_power','travel'):
                self.assertEqual(x[key],y[key])
            self.assertEqual(y['power'],min(100,x['power']*2))
            self.assertEqual(y['original_power'],x['power'])
        chosen=changed[-1]
        self.assertEqual(select_candidate(json.dumps(dict(candidate_id=chosen['id'])),changed),
            dict(angle=chosen['angle'],power=chosen['power']))
        self.assertEqual(o,before)

    def test_power_cap_and_invalid_settings(self):
        from fusion.geometry_agent import power_recommendations
        rows=[dict(id=1,power=60,risk='original risk'),dict(id=2,power=100,risk='original risk')]
        self.assertEqual([r['power'] for r in power_recommendations(rows,2)],[100,100])
        self.assertEqual(rows[0]['power'],60)
        for value in (0,3,True,1.5,'2'):
            with self.assertRaises(ValueError):GeometryPlayer(power_multiplier=value)

    def test_capped_same_angle_candidates_keep_the_selected_id(self):
        from fusion.geometry_agent import power_recommendations
        rows=power_recommendations([dict(id=1,angle=0,power=60,target=1,risk='A'),
                                   dict(id=2,angle=0,power=70,target=2,risk='B')],2)
        response=offline_response({},1)
        response['output'][0]['content'][0]['text']='{"candidate_id":2}'
        action,metadata=parse_selection(response,rows,False)
        self.assertEqual(action,dict(angle=0,power=100))
        self.assertEqual(metadata['selected_candidate_id'],2)
        self.assertEqual(metadata['selected_candidate']['target'],2)

    def test_preferred_server_and_waiting_only_change_without_spend(self):
        game,recorded,live=make_geometry_servers(0,0,0,transport=offline_response)
        try:
            s=live.live_session
            self.assertEqual(s.state()['live']['power_multiplier'],2)
            original=s.server_budget.snapshot()
            s.set_power_multiplier(1)
            self.assertEqual(s.state()['live']['power_multiplier'],1)
            self.assertEqual(s.server_budget.snapshot(),original)
            s.phase='thinking'
            with self.assertRaises(ValueError):s.set_power_multiplier(2)
        finally:
            for server in (game,recorded,live):server.server_close()

    def test_snapshot_trace_consent_and_policy_match_setting(self):
        with tempfile.TemporaryDirectory() as folder:
            s=GeometrySession(Path(folder),transport=offline_response,power_multiplier=2)
            # Persist without dispatching any worker or synthetic request.
            s.trace={'consent':{}};s._persist()
            self.assertEqual(s.trace['power_multiplier'],2)
            self.assertEqual(s.trace['consent']['power_multiplier'],2)
            self.assertEqual(s.policy_type(transport=offline_response).power_multiplier,2)
            self.assertEqual(s.state()['live']['power_multiplier'],2)

    def test_known_simulation_limit_position_at_both_settings(self):
        from test_geometry_stability import failing_position
        from fusion.legacy import module as legacy_module
        Simulation=legacy_module('smart').Simulation
        episode,_=failing_position();observation=episode.observe('p1')
        for multiplier,power,ticks in ((1,1,354),(2,2,4671)):
            payload=GeometryPlayer(power_multiplier=multiplier).request(observation,episode.legal_actions('p1'))
            rows=json.loads(payload['input'][1]['content'])['candidates']
            row=next(r for r in rows if r['route']=='contact' and r['target']==5)
            self.assertEqual((row['angle'],row['power']),(266,power))
            sim=Simulation(observation,dict(angle=row['angle'],power=row['power']));sim.advance(9600)
            self.assertTrue(sim.result()['settled']);self.assertEqual(sim.result()['ticks'],ticks)
        historical=Simulation(observation,dict(angle=266,power=4));historical.advance(9600)
        self.assertFalse(historical.result()['settled'])


class PowerHTTP(unittest.TestCase):
    setUp=lifecycle.GeometryLifecycle.setUp
    tearDown=lifecycle.GeometryLifecycle.tearDown
    get=lifecycle.GeometryLifecycle.get
    post=lifecycle.GeometryLifecycle.post

    def test_settings_lock_failure_recovery_and_cumulative_budget(self):
        self.post('/live/power',dict(power_multiplier=2))
        state=self.get('/api/state')
        self.assertEqual(state['live']['power_multiplier'],2)
        self.assertEqual(state['live']['calls'],0)
        for body in (dict(power_multiplier=True),dict(power_multiplier=3),dict(power_multiplier=1,confirmed=True)):
            with self.assertRaises(HTTPError):self.post('/live/power',body)
        # Windows may abort a socket rejected before its request body is read.
        # Either transport refusal must preserve state and dispatch nothing.
        with self.assertRaises((HTTPError,ConnectionAbortedError)):
            self.post('/live/power',dict(power_multiplier=1),nonce='old-token')
        rejected=self.get('/api/state')['live']
        self.assertEqual(rejected['power_multiplier'],2)
        self.assertEqual(rejected['calls'],0)
        with self.assertRaises(HTTPError):self.post('/live/start',dict(confirmed=False))
        self.live.live_session.transport=lifecycle.failing_response
        self.post('/live/start',dict(confirmed=True))
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            state=self.get('/api/state')
            if state['live']['phase']=='failed':break
            time.sleep(.01)
        self.assertEqual(state['live']['phase'],'failed')
        self.assertEqual(state['live']['power_multiplier'],2)
        with self.assertRaises(HTTPError):self.post('/live/power',dict(power_multiplier=1))
        self.post('/live/leave');fresh=self.post('/live/new');self.nonce=fresh['nonce']
        budget=fresh['state']['live']['server_budget']
        self.assertEqual(fresh['state']['live']['power_multiplier'],2)
        changed=self.post('/live/power',dict(power_multiplier=1))
        self.assertEqual(changed['live']['server_budget'],budget)
        self.assertEqual(changed['live']['power_multiplier'],1)
        self.live.live_session.transport=offline_response
        self.post('/live/start',dict(confirmed=True))
        with self.assertRaises(HTTPError):self.post('/live/power',dict(power_multiplier=2))
        self.post('/live/cancel');self.post('/live/leave')
        self.assertEqual(self.live.live_session.trace['power_multiplier'],1)
        self.assertEqual(self.live.live_session.trace['consent']['power_multiplier'],1)


if __name__=='__main__':unittest.main()
