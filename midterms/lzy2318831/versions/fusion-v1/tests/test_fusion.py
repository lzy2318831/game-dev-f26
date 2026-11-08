import copy
import json
import unittest

from fusion.engine import Episode,Ball,tick,ShotLedger
from fusion.baseline import choose
from fusion.runner import run_match,replay


class FusionPhysics(unittest.TestCase):
    def test_equal_mass_transfer_and_friction(self):
        balls=[Ball(0,100,250,100,0),Ball(1,122,250)]
        tick(balls,[],ShotLedger())
        self.assertLess(balls[0].vx,2)
        self.assertGreater(balls[1].vx,95)
        self.assertLess(balls[0].vx+balls[1].vx,100)

    def test_rail_and_pocket(self):
        balls=[Ball(0,11,250,-100,0),Ball(1,500,15,0,-20)]
        ledger=ShotLedger()
        tick(balls,[],ledger)
        self.assertGreater(balls[0].vx,0)
        self.assertFalse(balls[1].active)
        self.assertEqual(ledger.pots,[1])

    def test_bumper_impulse_and_farming_caps(self):
        balls=[Ball(0,460,165,150,0)]
        bumper={'id':0,'x':500,'y':165,'radius':29}
        ledger=ShotLedger()
        tick(balls,[bumper],ledger)
        self.assertLess(balls[0].vx,-250)
        self.assertEqual(ledger.bumper_points,15)
        for _ in range(8):
            balls[0].x,balls[0].y=450,165
            balls[0].vx,balls[0].vy=0,0
            tick(balls,[bumper],ledger)
            balls[0].x,balls[0].vx=460,150
            tick(balls,[bumper],ledger)
        self.assertEqual(ledger.bumper_points,15)
        self.assertEqual(ledger.boosts[(0,0)],2)

    def test_combo_and_scratch_scoring(self):
        s=ShotLedger()
        s.bumper(0,0,0,0)
        s.pocket(1,0,0)
        s.pocket(2,0,0)
        self.assertEqual(s.score(),315)  # 200+15+50+50
        s.pocket(0,0,0)
        self.assertEqual(s.score(),0)


class FusionInterface(unittest.TestCase):
    def test_initial_state_and_isolation(self):
        e=Episode()
        o=e.reset(9)
        self.assertEqual(len(o['balls']),7)
        self.assertEqual(len(o['bumpers']),2)
        self.assertEqual(o['shots_remaining'],{'p1':6,'p2':6})
        o['balls'].clear()
        self.assertEqual(len(e.observe('p1')['balls']),7)
        self.assertEqual(e.legal_actions('p2'),[])
        self.assertEqual(e.legal_actions('p1')['power_max'],100)
        self.assertNotIn('seed',e.observe('p1'))
        with self.assertRaises(ValueError): e.observe('other')

    def test_illegal_wrong_seat_and_limits(self):
        e=Episode()
        before=e.observe('p1')
        self.assertFalse(e.step('p2',None)['accepted'])
        self.assertEqual(before,e.observe('p1'))
        balls=copy.deepcopy(before['balls'])
        for _ in range(12): e.step(e.active_player,{'angle':True,'power':20})
        self.assertEqual(e.observe('p1')['balls'],balls)
        self.assertEqual(e.outcome()['reason'],'shots_exhausted')
        self.assertTrue(e.outcome()['draw'])
        before=e.outcome()
        e.step('p1',{'angle':0,'power':20})
        self.assertEqual(before,e.outcome())

    def test_pot_end_and_final_score(self):
        e=Episode(layout=[(500,150),(500,55)])
        r=e.step('p1',{'angle':270,'power':20})
        self.assertTrue(r['accepted'])
        self.assertEqual(e.outcome()['reason'],'table_cleared')
        self.assertEqual(e.outcome()['scores']['p1'],100)
        self.assertEqual(e.outcome()['winner'],'p1')
        self.assertEqual(e.active_player,'p2')
        self.assertTrue(all(b.vx==0 and b.vy==0 for b in e.balls if b.active))

    def test_scratch_and_respot(self):
        e=Episode(layout=[(500,55),(800,250)])
        e.step('p1',{'angle':270,'power':20})
        self.assertEqual(e.scratches['p1'],1)
        self.assertEqual((e.balls[0].x,e.balls[0].y),(230,250))
        self.assertEqual(e.scores['p1'],0)
        self.assertEqual(e.active_player,'p2')

    def test_simulation_limit_and_frame_independence(self):
        e=Episode(max_ticks=1)
        e.step('p1',{'angle':0,'power':80})
        self.assertEqual(e.outcome()['reason'],'simulation_limit')
        self.assertFalse(e.outcome()['draw'])
        a,b=Episode(),Episode()
        action={'angle':15,'power':60}
        a.step('p1',action,record_frames=True)
        b.step('p1',action,record_frames=False)
        self.assertEqual(a.observe('p1'),b.observe('p1'))


class FusionRunner(unittest.TestCase):
    def test_baseline_complete_replay_and_determinism(self):
        trace=run_match(seed=17)
        self.assertFalse(trace['outcome']['failure'])
        self.assertLessEqual(trace['outcome']['shots'],12)
        self.assertEqual(trace['outcome'],replay(json.loads(json.dumps(trace))))
        other=run_match(seed=17)
        self.assertEqual(trace['outcome'],other['outcome'])
        self.assertEqual([r['action'] for r in trace['steps']],[r['action'] for r in other['steps']])
        self.assertEqual(trace['model_calls'],0)
        e=Episode()
        self.assertTrue(e.valid(choose(e.observe('p1'),e.legal_actions('p1'))))

    def test_deadline(self):
        self.assertEqual(run_match(deadline_seconds=0)['outcome']['reason'],'episode_timeout')
