"""Confirmed table delta only; original physics remains separately executable."""
from copy import deepcopy
import math
import unittest
from fusion import VERSION
from fusion.devices import DEVICES,rail_collision
from fusion.engine import Ball,ShotLedger,Episode,tick,POCKETS


class BalancedTable(unittest.TestCase):
    def test_new_version_and_only_confirmed_segments_removed(self):
        self.assertEqual(VERSION,'fusion-1.6.0-balanced')
        from fusion.legacy import module
        old=module('devices').DEVICES
        expected=[r for r in old['guides'] if r['id'] not in ('left-entry','right-entry')]
        self.assertEqual(DEVICES['guides'],expected)
        self.assertEqual(len(expected),27)
        for side in ('left','right'):
            for part in ('orbit-rise','orbit-crown','orbit-roof'):
                self.assertTrue(any(r['id']==side+'-'+part for r in DEVICES['guides']))
        for key in old:
            if key!='guides':self.assertEqual(DEVICES[key],old[key])
        import fusion.engine as current_engine
        self.assertEqual(current_engine.BUMPERS,module('engine').BUMPERS)

    def test_former_diagonal_is_open_and_surrounding_boundary_remains(self):
        for x in (106.5,893.5):
            b=Ball(0,x,105,vx=0,vy=-50);ledger=ShotLedger()
            for rail in DEVICES['guides']:rail_collision(b,rail,ledger)
            self.assertFalse(any(e.get('rail') in ('left-entry','right-entry') for e in ledger.events))
            self.assertAlmostEqual(b.x,x);self.assertAlmostEqual(b.y,105)
        for x,y,vx,vy in [(20,220,-700,0),(980,220,700,0),(70,12,0,-700),(930,12,0,-700)]:
            balls=[Ball(0,x,y,vx=vx,vy=vy)];ledger=ShotLedger()
            for _ in range(1500):
                tick(balls,[],ledger,deepcopy(DEVICES))
                for b in balls:
                    if b.active:self.assertTrue(11<=b.x<=989 and 11<=b.y<=489,(b.x,b.y))
                    else:self.assertTrue(ledger.scratch,'disappearance must be a recorded pocket scratch')
        self.assertEqual(POCKETS,((0,0),(500,0),(1000,0),(0,500),(500,500),(1000,500)))

    def test_sling_vector_reduced_exactly_and_floor_scaled(self):
        from fusion.legacy import module
        old=module('devices');rail=next(r for r in DEVICES['guides'] if r.get('powered')=='left-sling')
        a,b=rail['a'],rail['b'];length=math.dist(a,b);nx,ny=(b[1]-a[1])/length,-(b[0]-a[0])/length
        def ball(speed):return Ball(0,(a[0]+b[0])/2+nx*14,(a[1]+b[1])/2+ny*14,vx=-nx*speed,vy=-ny*speed)
        original=ball(600);revised=ball(600);lo=ShotLedger();ln=ShotLedger()
        old.rail_collision(original,rail,lo);rail_collision(revised,rail,ln)
        self.assertAlmostEqual(original.vx-revised.vx,64)
        self.assertAlmostEqual(revised.vy-original.vy,48)
        original=ball(.1);revised=ball(.1)
        old.rail_collision(original,rail,ShotLedger());rail_collision(revised,rail,ShotLedger())
        self.assertAlmostEqual(math.hypot(original.vx,original.vy),420)
        self.assertAlmostEqual(math.hypot(revised.vx,revised.vy),315)
        self.assertEqual(ln.sling_boosts[(0,'left-sling')],1)
        self.assertEqual(ln.device_points,lo.device_points)
        self.assertEqual(ln.events,lo.events)
        import fusion.devices as current
        self.assertEqual((current.SLING_IMPULSE,current.SLING_SEPARATING_FLOOR,current.SLING_LAUNCH_FLOOR),(240,45,315))

    def test_historical_replay_remains_versioned_and_fingerprint_checked(self):
        import json
        from pathlib import Path
        from fusion.runner import replay
        from fusion.legacy import VERSION as old_version
        path=Path('evidence/live-browser-geometry-v1/20261107T215634Z-8dbde2c0c71f/trace.json')
        trace=json.loads(path.read_text())
        self.assertEqual(trace['version'],old_version)
        self.assertEqual(replay(trace),trace['outcome'])
        bad=deepcopy(trace);bad['engine_sha256']='0'*64
        with self.assertRaises(ValueError):replay(bad)

    def test_legacy_prompt_host_and_preferred_geometry_host_are_explicit(self):
        from fusion.live_session import LiveSession
        from fusion.geometry_live import GeometrySession
        self.assertEqual(LiveSession().state()['version'],'fusion-1.5.0-replenish')
        current=GeometrySession()
        self.assertEqual(current.state()['version'],'fusion-1.6.0-balanced')
        self.assertEqual(len(current.episode.devices['guides']),27)


if __name__=='__main__':unittest.main()
