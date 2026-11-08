import unittest,math
from fusion.engine import Episode,Ball,ShotLedger
from fusion.devices import DEVICES,process_sensors,rail_collision
class Maximal(unittest.TestCase):
 def test_density_and_copy(self):
  e=Episode(); o=e.observe('p1'); self.assertEqual(len(o['bumpers']),10)
  self.assertEqual(len(o['devices']['guides']),29); self.assertEqual(len(o['devices']['lanes']),6)
  o['devices']['scoop']['x']=0; self.assertEqual(e.observe('p1')['devices']['scoop']['x'],805)
 def test_scoop_once_scratch(self):
  l=ShotLedger(); b=Ball(0,805,80,0,200); process_sensors(b,(805,79),DEVICES,l)
  self.assertLess(b.vx,0); self.assertAlmostEqual(math.hypot(b.vx,b.vy),640)
  self.assertEqual(l.breakdown()['devices'],40)
  b.x,b.y,b.vx,b.vy=805,80,0,200; process_sensors(b,(805,79),DEVICES,l)
  self.assertEqual(b.vy,200); self.assertEqual(l.score(),40)
  l.scratch=True; self.assertEqual(l.score(),0)
 def test_sling_cap(self):
  r=next(r for r in DEVICES['guides'] if r.get('powered')=='left-sling'); l=ShotLedger()
  ax,ay=r['a']; bx,by=r['b']; d=math.dist(r['a'],r['b']); nx,ny=-(by-ay)/d,(bx-ax)/d
  speeds=[]
  for _ in range(4):
   b=Ball(0,(ax+bx)/2+nx*14,(ay+by)/2+ny*14,-100*nx,-100*ny)
   rail_collision(b,r,l); speeds.append(math.hypot(b.vx,b.vy))
  self.assertGreater(speeds[0],200); self.assertAlmostEqual(speeds[2],90)
  self.assertEqual(l.breakdown()['devices'],10)
 def test_lane_caps(self):
  l=ShotLedger()
  for _ in range(4):
   for lane in DEVICES['lanes']: l.lane(0,lane['id'],0,0)
  self.assertEqual(l.lane_points,60)
 def test_wrong_seat(self):
  e=Episode(); before=e.observe('p1'); self.assertFalse(e.step('p2',dict(angle=0,power=50))['accepted']); self.assertEqual(before,e.observe('p1'))

 def test_objects_no_device_score_and_full_cap(self):
  l=ShotLedger(); b=Ball(1,805,80,0,200); process_sensors(b,(805,79),DEVICES,l)
  self.assertLess(b.vx,0); self.assertEqual(l.score(),0)
  for _ in range(4):
   for i in range(6): l.bumper(0,i,0,0)
   for r in DEVICES['lanes']: l.lane(0,r['id'],0,0)
   l.spin(0,0,0)
   l.device(0,'left-sling','sling',0,0,10); l.device(0,'right-sling','sling',0,0,10); l.device(0,'vault','scoop',0,0,40)
  self.assertEqual(l.score(),235)
 def test_default_clear_and_replay(self):
  from fusion.geometry import nearest_point
  e=Episode()
  for b in e.balls:
   self.assertTrue(all(math.dist((b.x,b.y),nearest_point((b.x,b.y),r['a'],r['b']))>=15 for r in e.devices['guides']))

 def test_long_cascade_settles(self):
  e=Episode(); e.step('p1',dict(angle=225,power=85))
  self.assertFalse(e.outcome()['failure'])
  self.assertTrue(all(not b.active or math.hypot(b.vx,b.vy)==0 for b in e.balls))
