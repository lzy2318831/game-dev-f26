import unittest,math
from fusion.engine import Episode,DEFAULT
from fusion.geometry import nearest_point
class FinalRack(unittest.TestCase):
 def test_fifteen_clear_deterministic(self):
  e=Episode();o=e.reset(101);self.assertEqual(len(o['balls']),16)
  self.assertEqual([b['id'] for b in o['balls']],list(range(16)))
  self.assertEqual(o['balls'],e.reset(102)['balls'])
  self.assertEqual([sum(abs(b.x-(700+row*24*math.sqrt(3)/2))<1e-6 for b in e.balls if b.id) for row in range(5)],[1,2,3,4,5])
  for i,b in enumerate(e.balls):
   self.assertTrue(all(math.hypot(b.x-c.x,b.y-c.y)>=22 for c in e.balls[i+1:]))
   self.assertTrue(all(math.dist((b.x,b.y),(d['x'],d['y']))>=d['radius']+11 for d in e.bumpers))
   self.assertTrue(all(math.dist((b.x,b.y),nearest_point((b.x,b.y),r['a'],r['b']))>=15 for r in e.devices['guides']))
   self.assertTrue(all(math.dist((b.x,b.y),p)>=29 for p in o['table']['pockets']))
 def test_break_settles(self):
  e=Episode();e.step('p1',dict(angle=0,power=100));self.assertFalse(e.outcome()['failure'])
  self.assertTrue(all(not b.active or math.hypot(b.vx,b.vy)==0 for b in e.balls))

class SmartTests(unittest.TestCase):
 def test_public_legal_deterministic_budget(self):
  from fusion.smart import plan
  import copy,time
  e=Episode(layout=[(470,330),(500,405)]);o=e.observe('p1');before=copy.deepcopy(o)
  a,m=plan(o,e.legal_actions('p1'));b,n=plan(o,e.legal_actions('p1'))
  self.assertEqual(a,b);self.assertTrue(e.valid(a));self.assertEqual(o,before)
  self.assertLessEqual(m['ticks'],40000);self.assertLessEqual(m['candidates'],24)
  self.assertLess(m['seconds'],15)
 def test_prediction_matches_real_physics_preserving_ids(self):
  from fusion.smart import predict
  e=Episode();e.balls[1].active=False;o=e.observe('p1')
  action=dict(angle=0,power=65);prediction=predict(o,action)
  e.step('p1',action)
  self.assertEqual(prediction['points'],e.last_shot['points']);self.assertEqual(prediction['foul'],e.last_shot['foul'])
  self.assertEqual(prediction['potted'],e.last_shot['potted'])
 def test_smart_mode_automatic(self):
  from fusion.server import GameSession
  s=GameSession();s.reset('hvs');s.shoot(dict(angle=0,power=30));s.ready()
  with self.assertRaises(ValueError):s.shoot(dict(angle=0,power=30))
  result=s.shoot(baseline=True);self.assertEqual(result['source'],'smart');self.assertTrue(s.episode.valid(result['action']))

class PhysicsRegression(unittest.TestCase):
 def test_broadphase_matches_preserved_physics(self):
  import types,copy
  from pathlib import Path
  from fusion import engine
  base=Path(__file__).resolve().parents[1]/'versions/kinetic-six-v1.3/fusion'
  d=types.ModuleType('fusion.reference_devices');d.__package__='fusion'
  exec((base/'devices.py').read_text(),d.__dict__)
  old=types.ModuleType('fusion.reference_engine');old.__package__='fusion'
  import sys;sys.modules[old.__name__]=old
  exec((base/'engine.py').read_text(),old.__dict__)
  old.rail_collision=d.rail_collision;old.process_sensors=d.process_sensors
  a=engine.Episode();b=copy.deepcopy(a.balls);left=engine.ShotLedger();right=engine.ShotLedger()
  a.balls[0].vx=b[0].vx=800
  for i in range(960):
   left.time=right.time=(i+1)/240
   engine.tick(a.balls,a.bumpers,left,a.devices);old.tick(b,a.bumpers,right,a.devices)
  self.assertEqual([vars(v) for v in a.balls],[vars(v) for v in b]);self.assertEqual(left.events,right.events)
