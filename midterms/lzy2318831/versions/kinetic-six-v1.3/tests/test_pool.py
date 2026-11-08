import copy
import math
import random
import unittest

from pool.engine import Ball, Episode, tick
from pool.baseline import choose
from pool.runner import run_match, replay


class PhysicsTests(unittest.TestCase):
    def test_collision_at_cushion_keeps_centers_inside(self):
        # Observed during boundary exploration: separation pushed cue past rail.
        balls = [Ball(0, 10, 200), Ball(1, 30, 200, -100, 0)]
        tick(balls)
        self.assertGreaterEqual(balls[0].x, 10)
        self.assertGreaterEqual(balls[1].x - balls[0].x, 20 - 1e-9)

    def test_equal_mass_collision(self):
        balls = [Ball(0, 100, 250, 100, 0), Ball(1, 120, 250)]
        tick(balls)
        self.assertAlmostEqual(balls[0].vx, 0, places=6)
        self.assertGreater(balls[1].vx, 99)

    def test_rail_friction_and_pocket(self):
        balls = [Ball(0, 10, 200, -100, 0), Ball(1, 500, 20, 0, -10)]
        events = tick(balls)
        self.assertGreater(balls[0].vx, 0)
        self.assertLess(balls[0].vx, 90)
        self.assertEqual(events, [1])
        self.assertFalse(balls[1].active)


class InterfaceTests(unittest.TestCase):
    def test_seeded_match_invariants_and_miss_turn(self):
        rng = random.Random(923)
        e = Episode()
        while not e.reason:
            actor = e.active_player
            e.step(actor, {'angle': rng.randrange(360), 'power': rng.randrange(1, 4)})
            self.assertNotEqual(e.active_player, actor)
            live = e.observe('p1')['balls']
            self.assertEqual(len({b['id'] for b in live}), len(live))
            for b in live:
                self.assertTrue(math.isfinite(b['x']) and math.isfinite(b['y']))
                self.assertTrue(10 - 1e-9 <= b['x'] <= 990 + 1e-9)
                self.assertTrue(10 - 1e-9 <= b['y'] <= 490 + 1e-9)
            self.assertLessEqual(sum(e.scores.values()), 7 - len(live))
        self.assertFalse(e.outcome()['failure'])

    def test_reset_isolation_and_boundary(self):
        e = Episode()
        a = e.reset(5)
        a['balls'].clear()
        self.assertEqual(len(e.observe('p1')['balls']), 7)
        self.assertEqual(set(e.observe('p1')), {'player_id', 'active_player', 'table', 'balls', 'scores', 'attempts_remaining', 'scratches', 'invalid_actions', 'last_events', 'status'})
        self.assertEqual(e.legal_actions('p2'), [])
        self.assertEqual(len(e.legal_actions('p1')), 1080)
        with self.assertRaises(ValueError):
            e.observe('other')

    def test_invalid_and_wrong_seat(self):
        invalid = [None, {'angle': True, 'power': 1}, {'angle': 0.0, 'power': 1}, {'angle': 360, 'power': 1}, {'angle': 0, 'power': 0}, {'angle': 0, 'power': 1, 'extra': 1}, {'angle': math.nan, 'power': 1}]
        for action in invalid:
            e = Episode()
            before = e.observe('p1')['balls']
            self.assertFalse(e.step('p2', action)['accepted'])
            self.assertEqual(e.outcome()['attempts'], 0)
            self.assertFalse(e.step('p1', action)['accepted'])
            self.assertEqual(e.observe('p2')['balls'], before)
            self.assertEqual(e.outcome()['invalid_actions']['p1'], 1)
            self.assertEqual(e.active_player, 'p2')

    def test_score_clearance_and_precedence(self):
        e = Episode(layout=[(500, 150), (500, 60)], max_attempts=1)
        r = e.step('p1', {'angle': 270, 'power': 1})
        self.assertTrue(r['accepted'])
        self.assertEqual(e.outcome()['scores']['p1'], 1)
        self.assertEqual(e.outcome()['reason'], 'table_cleared')
        self.assertEqual(e.outcome()['winner'], 'p1')
        before = copy.deepcopy(e.outcome())
        self.assertFalse(e.step('p2', {'angle': 0, 'power': 1})['accepted'])
        self.assertEqual(e.outcome(), before)

    def test_scratch_respot_and_turn(self):
        e = Episode(layout=[(500, 60), (800, 250)])
        e.step('p1', {'angle': 270, 'power': 1})
        o = e.observe('p2')
        self.assertEqual(o['scratches']['p1'], 1)
        self.assertEqual(o['scores']['p1'], 0)
        self.assertEqual(o['balls'][0], {'id': 0, 'x': 250, 'y': 250})
        self.assertEqual(o['active_player'], 'p2')

    def test_scratch_voids_object_points(self):
        e = Episode(layout=[(500, 20), (0, 20)])
        e.step('p1', {'angle': 270, 'power': 1})
        self.assertEqual(e.outcome()['scores']['p1'], 0)
        self.assertEqual(e.outcome()['scratches']['p1'], 1)
        self.assertEqual(e.outcome()['reason'], 'table_cleared')
        self.assertTrue(e.outcome()['draw'])

    def test_attempt_and_simulation_limits(self):
        e = Episode(max_attempts=2)
        e.step('p1', None)
        e.step('p2', None)
        self.assertEqual(e.outcome()['reason'], 'attempt_limit')
        e = Episode(max_ticks=1)
        e.step('p1', {'angle': 0, 'power': 3})
        self.assertEqual(e.outcome()['reason'], 'simulation_limit')
        self.assertFalse(e.outcome()['draw'])
        self.assertIsNone(e.outcome()['winner'])

    def test_determinism(self):
        a, b = Episode(), Episode()
        for _ in range(4):
            action = choose(a.observe(a.active_player), a.legal_actions(a.active_player))
            a.step(a.active_player, action)
            b.step(b.active_player, action)
            self.assertEqual(a.observe('p1'), b.observe('p1'))


class RunnerTests(unittest.TestCase):
    def test_trace_rejects_altered_acceptance(self):
        trace = run_match(max_attempts=1)
        trace['steps'][0]['accepted'] = False
        with self.assertRaises(ValueError):
            replay(trace)

    def test_trace_replay_and_seats(self):
        trace = run_match(seed=19, max_attempts=4, seats=('baseline', 'direct'))
        self.assertEqual(trace['outcome']['attempts'], 4)
        self.assertEqual(trace['outcome'], replay(trace))
        self.assertEqual([s['player'] for s in trace['steps']], ['p1', 'p2', 'p1', 'p2'])
        self.assertEqual(trace['model_calls'], 0)

    def test_episode_deadline(self):
        trace = run_match(deadline_seconds=0)
        self.assertEqual(trace['outcome']['reason'], 'episode_timeout')


if __name__ == '__main__':
    unittest.main()
