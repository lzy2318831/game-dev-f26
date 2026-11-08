"""Navigation first; all failures and responses are synthetic/offline."""
import json
from pathlib import Path
import threading
import time
import unittest
from fusion.geometry_live import GeometrySession
from fusion.geometry_agent import GeometryPlayer,offline_response
from fusion.engine import Episode
from fusion.smart import Simulation

FAILED=Path('evidence/live-browser-geometry-v1/20261107T215634Z-8dbde2c0c71f/trace.json')


def failing_position():
    trace=json.loads(FAILED.read_text());e=Episode(layout=trace['layout']);e.reset(trace['seed'])
    for row in trace['steps'][:-1]:e.step(row['player'],row['action'])
    return e,trace


class GeometryStability(unittest.TestCase):
    def test_leave_does_not_wait_for_locked_simulation_or_audit(self):
        s=GeometrySession(transport=offline_response);ready=threading.Event();release=threading.Event()
        def hold():
            with s.lock:ready.set();release.wait(3)
        worker=threading.Thread(target=hold);worker.start();ready.wait()
        completed=threading.Event()
        def leave():s.leave();completed.set()
        request=threading.Thread(target=leave);request.start()
        try:self.assertTrue(completed.wait(.7),'leave blocked behind session lock')
        finally:release.set();worker.join();request.join()

    def test_known_nonsettling_candidate_is_not_offered(self):
        e,trace=failing_position();payload=GeometryPlayer(transport=offline_response).request(e.observe('p1'),e.legal_actions('p1'))
        rows=json.loads(payload['input'][1]['content'])['candidates']
        self.assertFalse(any(r['angle']==266 and r['power']==4 for r in rows),'known simulation_limit candidate remains offered')


if __name__=='__main__':unittest.main()

class PowerRegression(unittest.TestCase):
    def test_replacement_contact_settles_in_frozen_simulator(self):
        e,_=failing_position()
        rows=json.loads(GeometryPlayer(transport=offline_response).request(e.observe('p1'),e.legal_actions('p1'))['input'][1]['content'])['candidates']
        row=next(r for r in rows if r['route']=='contact' and r['target']==5)
        self.assertEqual((row['angle'],row['power']),(266,1))
        sim=Simulation(e.observe('p1'),dict(angle=row['angle'],power=row['power']))
        sim.advance(9600)
        self.assertTrue(sim.result()['settled'])
        self.assertLess(sim.result()['ticks'],9600)
