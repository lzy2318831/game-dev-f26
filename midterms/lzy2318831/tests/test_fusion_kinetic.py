import math,unittest
from fusion.engine import Episode,Ball,ShotLedger,tick
from fusion.devices import DEVICES,process_sensors,rail_collision
class Kinetic(unittest.TestCase):
 def test_cluster_public_geometry(self):
  e=Episode();o=e.observe('p1');self.assertEqual(len(o['bumpers']),10)
  self.assertEqual(len(o['devices']['guides']),27)
  self.assertTrue(all(not 220<=b['y']<=315 for b in o['bumpers']))
  self.assertEqual(o['devices']['bridge']['exit'],[630,75])
  o['devices']['bridge']['exit'][0]=0;self.assertEqual(e.observe('p1')['devices']['bridge']['exit'][0],630)
 def test_vault_fixed_launch_and_followup(self):
  e=Episode(); l=ShotLedger();b=Ball(0,805,80,0,200)
  process_sensors(b,(805,79),e.devices,l,[b])
  self.assertAlmostEqual(math.hypot(b.vx,b.vy),640);self.assertLess(b.vx,0)
  self.assertEqual(l.device_points,40)
  for i in range(400): l.time=(i+1)/240;tick([b],e.bumpers,l,e.devices)
  self.assertTrue(any(v['type']=='bumper' for v in l.events))
  self.assertEqual(sum(v['type']=='scoop' for v in l.events),1)
 def test_skyway_blocked_exit_and_once(self):
  e=Episode();l=ShotLedger();b=Ball(0,230,55,0,-100);block=Ball(1,630,75)
  process_sensors(b,(230,56),e.devices,l,[b,block]);self.assertEqual(b.x,230);self.assertEqual(l.device_points,0)
  process_sensors(b,(230,56),e.devices,l,[b]);self.assertEqual((b.x,b.y),(630,75));self.assertEqual(l.device_points,20)
  self.assertFalse(any(v['type']=='lane' for v in l.events))
  b.x,b.y=230,55;process_sensors(b,(230,56),e.devices,l,[b]);self.assertEqual(b.x,230)
  l.scratch=True;self.assertEqual(l.score(),0)
 def test_stronger_inward_sling(self):
  r=next(r for r in DEVICES['guides'] if r.get('powered')=='left-sling');a,c=r['a'],r['b'];d=math.dist(a,c);nx,ny=(c[1]-a[1])/d,-(c[0]-a[0])/d
  b=Ball(0,(a[0]+c[0])/2+nx*14,(a[1]+c[1])/2+ny*14,-100*nx,-100*ny);l=ShotLedger();rail_collision(b,r,l)
  self.assertGreater(b.vx,0);self.assertLess(b.vy,0);self.assertGreaterEqual(math.hypot(b.vx,b.vy),314.9)
 def test_no_stationary_device_launch(self):
  l=ShotLedger();b=Ball(0,230,55);process_sensors(b,(230,55),DEVICES,l,[b]);self.assertEqual((b.x,b.y),(230,55));self.assertEqual(l.score(),0)

 def test_cluster_chain_and_settling(self):
  e=Episode(layout=[(325,125),(700,250)]);e.step('p1',dict(angle=0,power=70))
  self.assertFalse(e.outcome()['failure'])
  ids={v['bumper'] for v in e.events if v['type']=='bumper' and v['ball']==0}
  self.assertTrue({0,6,7}.issubset(ids))
  self.assertTrue(any(v['type']=='bridge' for v in e.events))
  self.assertTrue(all(not b.active or math.hypot(b.vx,b.vy)==0 for b in e.balls))
 def test_skyway_followup_and_full_cap(self):
  e=Episode();l=ShotLedger();b=Ball(0,230,55,0,-100)
  process_sensors(b,(230,56),e.devices,l,[b])
  for i in range(480): l.time=(i+1)/240;tick([b],e.bumpers,l,e.devices)
  self.assertTrue(any(v['type']=='bumper' and v['bumper']==1 for v in l.events))
  l=ShotLedger()
  for _ in range(4):
   for b in e.bumpers:l.bumper(0,b['id'],0,0)
   for lane in e.devices['lanes']:l.lane(0,lane['id'],0,0)
   l.spin(0,0,0)
   for name,value in [('vault',40),('skyway',20),('left-sling',10),('right-sling',10)]:l.device(0,name,'test',0,0,value)
  self.assertEqual(l.score(),315);l.scratch=True;self.assertEqual(l.score(),0)

 def test_solids_do_not_overlap(self):
  from fusion.geometry import nearest_point
  e=Episode()
  for b in e.bumpers:
   for r in e.devices['guides']:
    self.assertGreaterEqual(math.dist((b['x'],b['y']),nearest_point((b['x'],b['y']),r['a'],r['b'])),b['radius']+r['radius'],(b['id'],r['id']))
 def test_repeat_sling_feedback_never_rescores(self):
  l=ShotLedger();l.device(0,'left-sling','sling',0,0,10);l.device(0,'left-sling','sling',0,0,10)
  self.assertEqual([v['points'] for v in l.events],[10,0]);self.assertEqual(l.score(),10)

 def test_default_skyway_vault_chain(self):
  e=Episode();r=e.step('p1',dict(angle=345,power=85),record_frames=True)
  events=[v for v in e.events if v.get('ball')==0]
  self.assertFalse(e.outcome()['failure'])
  self.assertTrue(any(v['type']=='bridge' for v in events));self.assertTrue(any(v['type']=='scoop' for v in events))
  self.assertGreaterEqual(len({v['bumper'] for v in events if v['type']=='bumper'}),5)
  other=Episode();other.step('p1',dict(angle=345,power=85))
  self.assertEqual(e.outcome(),other.outcome());self.assertEqual(e.events,other.events)
