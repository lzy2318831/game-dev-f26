import unittest,copy,math
from fusion.engine import Episode
class Replenish(unittest.TestCase):
 def sparse(self,n):
  e=Episode()
  for b in e.balls:
   if b.id>n:b.active=False
  return e
 def test_threshold_count_and_isolation(self):
  e=self.sparse(8);e.step('p1',dict(angle=180,power=1))
  o=e.observe('p2');self.assertEqual(len(o['balls']),14)
  self.assertEqual(o['replenishment']['used'],1);self.assertEqual(e.active_player,'p2')
  o['replenishment']['used']=9;self.assertEqual(e.observe('p2')['replenishment']['used'],1)
  self.assertTrue(all(b.vx==b.vy==0 for b in e.balls if b.active))
 def test_nine_no_spawn_and_no_invalid_spawn(self):
  e=self.sparse(9);e.step('p1',dict(angle=180,power=1));self.assertEqual(e.replenishments_used,0)
  e=self.sparse(8);e.step('p1',None);self.assertEqual(e.replenishments_used,0)
 def test_max_two_and_empty_clear_priority(self):
  e=self.sparse(0)
  for player in ('p1','p2'):
   e.step(player,dict(angle=180,power=1));self.assertEqual(e.reason,'')
   for b in e.balls:
    if b.id:b.active=False
  self.assertEqual(e.replenishments_used,2)
  e.step('p1',dict(angle=180,power=1));self.assertEqual(e.reason,'table_cleared')
 def test_final_opportunity_never_spawns(self):
  e=self.sparse(8);e.shots=11;e.shots_remaining={'p1':1,'p2':0}
  e.step('p1',dict(angle=180,power=1));self.assertEqual(e.replenishments_used,0);self.assertEqual(e.reason,'shots_exhausted')
 def test_no_overlap_and_deterministic_positions(self):
  from fusion.replenish import placement_clear
  a=self.sparse(8);b=self.sparse(8)
  a.step('p1',dict(angle=180,power=1));b.step('p1',dict(angle=180,power=1))
  self.assertEqual(a.observe('p2'),b.observe('p2'))
  event=next(v for v in a.events if v['type']=='replenish')
  for p in event['balls']:
   others=[dict(id=v.id,x=v.x,y=v.y) for v in a.balls if v.active and v.id!=p['id']]
   self.assertTrue(placement_clear((p['x'],p['y']),others,a.bumpers,a.devices))
  self.assertEqual(len({v.id for v in a.balls if v.active}),len([v for v in a.balls if v.active]))
 def test_moving_or_blocked_batch_atomic(self):
  from unittest.mock import patch
  e=self.sparse(8);e.balls[0].vx=1;self.assertEqual(e._replenish(),[])
  e.balls[0].vx=0;before=copy.deepcopy(e.balls)
  with patch('fusion.engine.spawn_batch',return_value=[]):self.assertEqual(e._replenish(),[])
  self.assertEqual(e.balls,before);self.assertEqual(e.replenishments_used,0)
 def test_points_and_scratch_precedence(self):
  e=Episode(layout=[(500,350),(500,445)]);e.step('p1',dict(angle=90,power=20))
  self.assertEqual(e.scores['p1'],100);self.assertEqual(e.reason,'');self.assertEqual(len(e.last_shot['replenished']),5)
  e=Episode(layout=[(500,55),(800,250)]);e.step('p1',dict(angle=270,power=20))
  self.assertEqual(e.scores['p1'],0);self.assertEqual(e.scratches['p1'],1);self.assertEqual(e.replenishments_used,1)

 def test_replay_counters_events_and_tampering(self):
  from fusion.runner import run_match,replay
  from fusion.engine import DEFAULT
  trace=run_match(seats=('direct','direct'),layout=list(DEFAULT[:9]))
  self.assertEqual(trace['outcome'],replay(trace))
  self.assertGreaterEqual(trace['outcome']['replenishments_used'],1)
  self.assertLessEqual(trace['outcome']['replenishments_used'],2)
  self.assertLessEqual(trace['outcome']['shots'],12)
  event=next(v for s in trace['steps'] for v in s['events'] if v['type']=='replenish')
  event['balls'][0]['x']+=1
  with self.assertRaises(ValueError):replay(trace)
 def test_device_exclusion_and_many_states(self):
  from fusion.replenish import placement_clear,spawn_batch
  import random
  e=Episode()
  for point in [(0,0),(500,40),(805,88),(230,55),(630,75),(500,84),(51,270),(185,370),(280,105),(600,120)]:
   self.assertFalse(placement_clear(point,[],e.bumpers,e.devices),point)
  for seed in range(20):
   live=set(random.Random(seed).sample(range(1,16),8));e=Episode()
   for b in e.balls:
    if b.id and b.id not in live:b.active=False
   placements=spawn_batch(e.balls,e.bumpers,e.devices);self.assertEqual(len(placements),5)
   active=[dict(id=b.id,x=b.x,y=b.y) for b in e.balls if b.active]
   for p in placements:
    self.assertTrue(placement_clear((p['x'],p['y']),active,e.bumpers,e.devices));active.append(p)
 def test_reset_and_single_event_per_boundary(self):
  e=self.sparse(0);result=e.step('p1',dict(angle=180,power=1),record_frames=True)
  event=next(v for v in result['events'] if v['type']=='replenish')
  self.assertEqual(event['t'],result['frames'][-1]['t'])
  self.assertTrue({p['id'] for p in event['balls']}.issubset({p['id'] for p in result['frames'][-1]['balls']}))
  self.assertEqual(e.replenishments_used,1);self.assertEqual(sum(b.active and b.id!=0 for b in e.balls),5)
  before=e.observe('p2');e.observe('p1');self.assertEqual(before,e.observe('p2'))
  e.reset(101);self.assertEqual(e.replenishments_used,0);self.assertEqual(len(e.observe('p1')['balls']),16)
