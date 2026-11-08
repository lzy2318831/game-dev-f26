import copy
import json
import unittest

from historical.engine import Episode, Ball, axis_velocity, physics_frame
from historical.baseline import choose
from historical.runner import run_match, replay
from historical.player import build_context

NEUTRAL = {'x': 8, 'y': 8}


class HistoricalControls(unittest.TestCase):
    def test_fifteen_objects_mirrored_rack_and_reset(self):
        e = Episode()
        self.assertEqual(len(e.observe('p1')['balls']), 16)
        p1 = [(b.x, b.y) for b in e.balls]
        e._end_segment('scratch')
        self.assertEqual(e.active_player, 'p2')
        self.assertEqual([(b.x, b.y) for b in e.balls], [(256-x, y) for x,y in p1])
        e.reset(77)
        self.assertEqual(e.scores, {'p1': 0, 'p2': 0})
        self.assertEqual(e.heat, 1)

    def test_velocity_control_delay_and_neutral_stop(self):
        e = Episode(frames_per_step=1)
        x = e.balls[0].x
        e.step('p1', {'x': 15, 'y': 8})
        self.assertEqual(e.balls[0].x, x)  # input applied after motion
        self.assertEqual(e.balls[0].vx, 1.75)
        e.step('p1', NEUTRAL)
        self.assertEqual(e.balls[0].x, x+1.75)
        self.assertEqual(e.balls[0].vx, 0)
        e.step('p1', NEUTRAL)
        self.assertEqual(e.balls[0].x, x+1.75)
        self.assertEqual([axis_velocity(i) for i in (0,7,8,15)], [-1.75,0,0,1.75])

    def test_public_boundary_illegal_and_wrong_seat(self):
        e = Episode(frames_per_step=1)
        before = e.observe('p1')
        self.assertEqual(e.legal_actions('p2'), [])
        self.assertEqual(len(e.legal_actions('p1')), 256)
        self.assertFalse(e.step('p2', NEUTRAL)['accepted'])
        self.assertEqual(e.observe('p1'), before)
        for action in (None, {'x': True,'y':8}, {'x':16,'y':8}, {'x':8.0,'y':8}, {'x':8,'y':8,'z':0}):
            self.assertFalse(e.step('p1', action)['accepted'])
        self.assertEqual(e.invalid['p1'], 5)
        before['balls'].clear()
        self.assertEqual(len(e.observe('p1')['balls']), 16)
        self.assertNotIn('seed', e.observe('p1'))
        self.assertNotIn('contacts', e.observe('p1'))
        with self.assertRaises(ValueError):
            e.observe('bad')


class HistoricalPhysics(unittest.TestCase):
    def test_small_object_velocity_eventually_stops(self):
        ball=Ball(1,100,150,vx=1/16)
        for frame in range(256):
            physics_frame([ball],frame)
        self.assertEqual(ball.vx,0)

    def test_collision_transfer_friction_and_rebound(self):
        balls = [Ball(0,100,150), Ball(1,113,150,vx=-1)]
        physics_frame(balls,1)
        self.assertLess(balls[0].vx, -.9)
        self.assertAlmostEqual(balls[1].vx,0,places=2)
        ball = Ball(1,226,150,vx=1)
        physics_frame([ball],0)
        self.assertLess(ball.vx,0)
        ball = Ball(1,100,150,vx=1)
        physics_frame([ball],1)  # (frame xor id) & 3 == 0
        self.assertGreater(ball.vx,0)
        self.assertLess(ball.vx,1)

    def test_pocket_score_scratch_preserves_points(self):
        e = Episode(frames_per_step=1)
        e.balls[15] = Ball(15,127,64,vy=-1)
        e.step('p1', NEUTRAL)
        self.assertEqual(e.scores['p1'],1)
        self.assertEqual(e.active_player,'p1')
        self.assertFalse(e.balls[15].active)
        e.balls[0] = Ball(0,127,64,vy=-1)
        e.step('p1', NEUTRAL)
        self.assertEqual(e.active_player,'p2')
        self.assertEqual(e.scores['p1'],1)
        self.assertEqual(e.scratches['p1'],1)
        self.assertEqual(e.timer,30)
        self.assertEqual(len([b for b in e.balls if b.active]),16)

    def test_score_digit_wrap(self):
        e = Episode(frames_per_step=1)
        e.scores['p1'] = 99
        e.balls[15] = Ball(15,127,64,vy=-1)
        e.step('p1', NEUTRAL)
        self.assertEqual(e.scores['p1'],0)

    def test_corner_and_middle_openings(self):
        for x,y in ((26,70),(226,70),(127,64),(26,225),(226,225),(127,233)):
            balls=[Ball(1,x,y,vx=.5,vy=.5)]
            self.assertIn(1,physics_frame(balls,0))
        balls=[Ball(1,80,68,vy=-1)]
        self.assertEqual(physics_frame(balls,0),[])
        self.assertGreater(balls[0].vy,0)


class HistoricalProgression(unittest.TestCase):
    def test_default_limits_allow_five_extended_heats_at_gui_rate(self):
        e=Episode(heats=5,frames_per_step=1)
        # 30 + 15 bonus + the zero-display interval, twice per heat.
        theoretical_frames=46*64*2*5
        self.assertGreaterEqual(e.max_steps,theoretical_frames)
        self.assertGreaterEqual(e.max_frames,theoretical_frames)

    def test_countdown_zero_then_segment_transition(self):
        e = Episode(frames_per_step=64)
        e.step('p1', NEUTRAL)
        self.assertEqual(e.timer,29)
        for _ in range(29):
            e.step('p1', NEUTRAL)
        self.assertEqual(e.timer,0)
        self.assertEqual(e.active_player,'p1')
        e.step('p1', NEUTRAL)
        self.assertEqual(e.active_player,'p2')
        self.assertEqual(e.timer,30)

    def test_heat_progression_and_terminal_immutability(self):
        e = Episode(heats=2, frames_per_step=64)
        for _ in range(124):
            e.step(e.active_player, NEUTRAL)
        self.assertEqual(e.outcome()['reason'],'heats_complete')
        self.assertTrue(e.outcome()['draw'])
        state=copy.deepcopy(e.observe('p1'))
        self.assertFalse(e.step('p1', NEUTRAL)['accepted'])
        self.assertEqual(state,e.observe('p1'))
        self.assertEqual(e.legal_actions('p1'),[])

    def test_rerack_bonus_only_once_and_disabled(self):
        for extended in (False, True):
            e = Episode(extended=extended,frames_per_step=1)
            for b in e.balls[1:]:
                b.active=False
            e.step('p1',NEUTRAL)
            self.assertEqual(e.timer,45 if extended else 30)
            self.assertEqual(e.active_player,'p1')
            self.assertEqual(len([b for b in e.balls if b.active]),16)
            for b in e.balls[1:]:
                b.active=False
            e.step('p1',NEUTRAL)
            self.assertEqual(e.timer,45 if extended else 30)
            e._end_segment('scratch')
            self.assertFalse(e.bonus_awarded)

    def test_limits_and_invalid_state_isolation(self):
        e = Episode(frames_per_step=1,max_steps=2)
        before=[(b.x,b.y) for b in e.balls]
        e.step('p1',None)
        self.assertEqual(e.frames,0)
        self.assertEqual(before,[(b.x,b.y) for b in e.balls])
        e.step('p1',None)
        self.assertEqual(e.outcome()['reason'],'step_limit')
        self.assertIsNone(e.outcome()['winner'])
        self.assertFalse(e.outcome()['draw'])
        e = Episode(frames_per_step=8,max_frames=3)
        e.step('p1',NEUTRAL)
        self.assertEqual(e.frames,3)
        self.assertEqual(e.reason,'frame_limit')


class HistoricalRunner(unittest.TestCase):
    def test_baseline_handles_clearance_before_next_frame_rerack(self):
        from historical.baseline import direct
        e=Episode(frames_per_step=1)
        for b in e.balls[1:]:
            b.active=False
        for policy in (choose,direct):
            self.assertEqual(policy(e.observe('p1'),e.legal_actions('p1')),NEUTRAL)

    def test_model_call_budget_and_public_context(self):
        model=FakeControl()
        trace=run_match(seats=('model','neutral'),players={'model':model},model_call_limit=1)
        self.assertEqual(trace['model_calls'],1)
        self.assertEqual(trace['outcome']['reason'],'model_call_limit')
        self.assertEqual(trace['steps'][0]['action'],NEUTRAL)
        e=Episode()
        self.assertNotIn('seed',json.dumps(build_context(e.observe('p1'),e.legal_actions('p1'))))
        with self.assertRaises(ValueError):
            build_context(dict(e.observe('p1'),private='secret'),e.legal_actions('p1'))
        self.assertEqual(run_match(seats=('model','neutral'),players={'model':model},model_call_limit=0)['model_calls'],0)

    def test_model_timeout_and_failed_calls(self):
        for policy, reason in ((FailedControl(),'provider_error'),(HungControl(),'request_timeout')):
            trace=run_match(seats=('model','neutral'),players={'model':policy},request_timeout=.2)
            self.assertEqual(trace['outcome']['reason'],reason)
            self.assertEqual(trace['model_calls'],1)
            self.assertEqual(trace['steps'],[])

    def test_repeatable_baseline_trace_and_replay(self):
        a=run_match(seed=42,seats=('baseline','neutral'))
        b=run_match(seed=42,seats=('baseline','neutral'))
        self.assertEqual(a['outcome'],b['outcome'])
        self.assertEqual([r['action'] for r in a['steps']],[r['action'] for r in b['steps']])
        self.assertEqual(a['outcome'],replay(json.loads(json.dumps(a))))
        self.assertFalse(a['outcome']['failure'])
        self.assertEqual(a['model_calls'],0)
        e=Episode()
        self.assertIn(choose(e.observe('p1'),e.legal_actions('p1')),e.legal_actions('p1'))

    def test_trace_tampering_and_deadline(self):
        trace=run_match(max_steps=2)
        trace['steps'][0]['accepted']=False
        with self.assertRaises(ValueError):
            replay(trace)
        self.assertEqual(run_match(deadline_seconds=0)['outcome']['reason'],'episode_timeout')


class FakeControl:
    is_model=True
    last_metadata={'live':False,'model':'offline-fixture'}

    def decide(self,observation,legal_actions,history,timeout):
        return dict(x=8,y=8)


class FailedControl(FakeControl):
    def decide(self,*args,**kwargs):
        raise RuntimeError('must not leak provider details')


class HungControl(FakeControl):
    def decide(self,*args,**kwargs):
        import time
        time.sleep(10)
