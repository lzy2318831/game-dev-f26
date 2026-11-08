import math
import json
from pathlib import Path
import unittest
from fusion.engine import Episode,Ball,ShotLedger
from fusion.devices import DEVICES,rail_collision,process_sensors
from fusion.geometry import nearest_point,segments_distance
from fusion.player import build_context


class AurumDevices(unittest.TestCase):
    def test_frozen_layouts_clear_new_solids(self):
        e=Episode()
        suite=json.loads((Path(__file__).resolve().parents[1]/'fusion/evaluation.json').read_text())
        for case in suite['situations']:
            points=[case['cue']]+case['objects']
            for i,p in enumerate(points):
                self.assertTrue(all(math.dist(p,q)>=22 for q in points[i+1:]),case['id'])
                self.assertTrue(all(math.dist(p,(b['x'],b['y']))>=40 for b in e.bumpers),case['id'])
                self.assertTrue(all(math.dist(p,nearest_point(p,r['a'],r['b']))>=15 for r in e.devices['guides']),case['id'])

    def test_full_spinner_assisted_pot(self):
        e=Episode(layout=[(500,150),(500,55)])
        e.step('p1',dict(angle=270,power=20))
        self.assertEqual(e.scores['p1'],225)
        self.assertEqual(e.last_shot['breakdown']['multiplier'],100)
        self.assertEqual(e.outcome()['reason'],'table_cleared')

    def test_layout_is_open_and_public(self):
        e=Episode(); o=e.observe('p1')
        self.assertEqual(len(o['bumpers']),4)
        self.assertEqual(len(o['devices']['guides']),10)
        self.assertEqual(len(o['devices']['lanes']),2)
        self.assertEqual(o['devices']['spinner']['id'],'orbit')
        self.assertTrue(all(not 185<=b['y']<=315 for b in o['bumpers']))
        context=build_context(o,e.legal_actions('p1'))
        context['observation']['devices']['guides'].clear()
        self.assertEqual(len(e.observe('p1')['devices']['guides']),10)

    def test_rail_reflects_and_end_has_finite_normal(self):
        rail=dict(id='test',a=[100,100],b=[100,300],radius=4)
        b=Ball(0,86,200,vx=180); ledger=ShotLedger()
        rail_collision(b,rail,ledger)
        self.assertLess(b.vx,-160)
        self.assertLessEqual(b.x,85)
        self.assertEqual(ledger.events[0]['type'],'rail')
        end=Ball(1,100,100,vx=30)
        rail_collision(end,rail,ledger)
        self.assertTrue(all(math.isfinite(x) for x in (end.x,end.y,end.vx,end.vy)))

    def test_return_elbow_banks_downward_ball_inward(self):
        rail=next(r for r in DEVICES['guides'] if r['id']=='left-return')
        b=Ball(0,50,400,vy=300)
        rail_collision(b,rail,ShotLedger())
        self.assertGreater(b.vx,200)
        self.assertLess(abs(b.vy),60)

    def test_lane_scores_once_and_objects_do_not_score(self):
        ledger=ShotLedger(); cue=Ball(0,45,275,vy=120)
        for _ in range(4): process_sensors(cue,(45,265),DEVICES,ledger)
        self.assertEqual(ledger.lane_points,10)
        process_sensors(Ball(1,955,275,vy=120),(955,265),DEVICES,ledger)
        self.assertEqual(ledger.lane_points,10)
        process_sensors(Ball(0,955,275,vy=120),(955,265),DEVICES,ledger)
        self.assertEqual(ledger.lane_points,20)

    def test_spinner_doubles_later_pots_without_stacking(self):
        ledger=ShotLedger(); ledger.pocket(1,300,0)
        cue=Ball(0,500,88,vy=200)
        process_sensors(cue,(500,80),DEVICES,ledger)
        self.assertEqual(ledger.multiplier,2)
        self.assertEqual(ledger.spinner_points,25)
        self.assertAlmostEqual(cue.vy,184)
        process_sensors(cue,(500,80),DEVICES,ledger)
        self.assertEqual(ledger.spinner_points,25)
        self.assertAlmostEqual(cue.vy,184)
        ledger.pocket(2,1000,0)
        self.assertEqual(ledger.breakdown()['multiplier'],100)
        self.assertEqual(ledger.score(),375)
        ledger.pocket(0,0,0)
        self.assertEqual(ledger.score(),0)
        self.assertEqual(ShotLedger().multiplier,1)

    def test_spinner_object_and_minimum_speed(self):
        ledger=ShotLedger()
        process_sensors(Ball(1,500,88,vy=200),(500,80),DEVICES,ledger)
        self.assertEqual(ledger.multiplier,1)
        self.assertEqual(ledger.spinner_points,0)
        process_sensors(Ball(0,500,88,vy=10),(500,80),DEVICES,ledger)
        self.assertEqual(ledger.multiplier,1)

    def test_device_farming_is_bounded(self):
        ledger=ShotLedger()
        for _ in range(10):
            for i in range(4): ledger.bumper(0,i,0,0)
            process_sensors(Ball(0,45,275,vy=120),(45,265),DEVICES,ledger)
            process_sensors(Ball(0,955,275,vy=120),(955,265),DEVICES,ledger)
            process_sensors(Ball(0,500,88,vy=200),(500,80),DEVICES,ledger)
        self.assertEqual(ledger.score(),105)

    def test_recording_does_not_change_device_physics(self):
        a,b=Episode(),Episode(); action=dict(angle=305,power=65)
        a.step('p1',action,record_frames=True); b.step('p1',action)
        self.assertEqual(a.observe('p1'),b.observe('p1'))
        self.assertFalse(a.outcome()['failure'])

    def test_crossing_segments_are_obstacles(self):
        self.assertEqual(segments_distance((0,0),(100,100),(0,100),(100,0)),0)
        self.assertEqual(nearest_point((150,150),(100,100),(100,300)),(100,150))
