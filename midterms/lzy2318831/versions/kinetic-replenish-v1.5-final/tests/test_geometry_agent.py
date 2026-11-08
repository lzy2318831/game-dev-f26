"""Public geometry and synthetic selection only; no paid requests."""
import copy
import json
import math
import tempfile
from pathlib import Path
import unittest
import time
from fusion.engine import Episode
from fusion.geometry_candidates import candidates, direction_angle, minimum_power
from fusion.geometry_agent import GeometryPlayer, select_candidate, parse_selection
from fusion.llm import CallFailure, Ledger


def fixture(payload, timeout):
    return dict(status='completed',model=payload['model'],usage=dict(input_tokens=100,output_tokens=12),
        output=[dict(type='message',content=[dict(type='output_text',text='{"candidate_id":1}')])])


def bad_fixture(payload,timeout):
    r=fixture(payload,timeout);r['output'][0]['content'][0]['text']='{"candidate_id":999}'
    return r


def hanging_fixture(payload,timeout):
    time.sleep(10)
    return fixture(payload,timeout)


class GeometryTests(unittest.TestCase):
    def test_opening_contact_and_reach(self):
        e=Episode();o=e.observe('p1');before=copy.deepcopy(o)
        rows=candidates(o,e.legal_actions('p1'))
        row=next(r for r in rows if r['route']=='contact' and r['target']==1)
        self.assertEqual(row['angle'],0)
        self.assertGreaterEqual(row['minimum_power'],22)
        self.assertGreaterEqual(row['power'],row['minimum_power'])
        self.assertEqual(rows,candidates(o,e.legal_actions('p1')));self.assertEqual(o,before)
        self.assertEqual(candidates(o,[]),[])

    def test_quadrants_and_insufficient_power(self):
        for v,a in [((1,1),45),((-1,1),135),((-1,-1),225),((1,-1),315)]:
            self.assertEqual(direction_angle(v),a)
        self.assertGreater(minimum_power(448),15)
        self.assertGreater(minimum_power(10000),100)

    def test_blocked_target(self):
        e=Episode(layout=[(230,250),(700,250)]);o=e.observe('p1')
        o['devices']['guides']=[dict(id='block',a=[450,200],b=[450,300],radius=4)]
        rows=candidates(o,e.legal_actions('p1'))
        self.assertFalse(any(r['route']=='contact' and r['target']==1 for r in rows))
        o['devices']['guides']=[];o['bumpers']=[]
        o['balls'].append(dict(id=2,x=450,y=250))
        self.assertFalse(any(r['route']=='contact' and r['target']==1 for r in candidates(o,e.legal_actions('p1'))))

    def test_ghost_pot_and_scratch_screen(self):
        e=Episode(layout=[(500,350),(500,445)]);o=e.observe('p1');o['devices']['guides']=[];o['bumpers']=[]
        rows=candidates(o,e.legal_actions('p1'))
        pot=next(r for r in rows if r['route']=='pot' and r['pocket']==[500,500])
        self.assertEqual(pot['angle'],90)
        self.assertIn('not guaranteed',pot['risk'])
        # A miss toward the top-middle pocket must not be advertised as an escape.
        o['balls']=[dict(id=0,x=500,y=100),dict(id=1,x=700,y=250)]
        self.assertFalse(any(r['route']=='escape' and r['angle']==270 for r in candidates(o,e.legal_actions('p1'))))

    def test_selection_strict_and_no_default(self):
        rows=[dict(id=1,angle=0,power=30),dict(id=2,angle=90,power=20)]
        self.assertEqual(select_candidate('{"candidate_id":2}',rows),dict(angle=90,power=20))
        for value in ['bad','{"candidate_id":true}','{"candidate_id":3}',
                      '{"candidate_id":1,"angle":0}','{"candidate_id":1,"candidate_id":2}']:
            with self.assertRaises(ValueError):select_candidate(value,rows)
        with self.assertRaises(ValueError):select_candidate('{"candidate_id":1}',[])

    def test_offline_selection_and_empty_failure(self):
        e=Episode();p=GeometryPlayer(transport=fixture)
        with tempfile.TemporaryDirectory() as d:
            p.ledger=Ledger(Path(d)/'calls.jsonl',2,1)
            rows=candidates(e.observe('p1'),e.legal_actions('p1'))
            a,m=p.select(e.observe('p1'),e.legal_actions('p1'),[],3)
            self.assertEqual(a,{k:rows[0][k] for k in ('angle','power')})
            self.assertEqual(m['selected_candidate_id'],1);self.assertFalse(m['live'])
            self.assertEqual(m['usage']['input_tokens'],100)
            with self.assertRaises(CallFailure):p.select(e.observe('p1'),[],[],3)
            self.assertEqual(p.ledger.calls,1)

    def test_minimum_energy_fallback_is_still_selected_by_model(self):
        e=Episode();o=e.observe('p1')
        o['bumpers']=[dict(id=0,x=230,y=250,radius=2000)]
        rows=candidates(o,e.legal_actions('p1'))
        self.assertTrue(rows)
        self.assertTrue(all(r['route']=='fallback-escape' and r['power']==1 for r in rows))
        self.assertTrue(all('no guaranteed' in r['risk'] for r in rows))
        action,meta=GeometryPlayer(transport=fixture).select(o,e.legal_actions('p1'),[],3)
        self.assertEqual(action,{k:rows[0][k] for k in ('angle','power')})
        self.assertEqual(meta['selected_candidate_id'],1)

    def test_invalid_selection_retains_usage(self):
        response=fixture(dict(model='fixture'),1)
        response['output'][0]['content'][0]['text']='{"candidate_id":999}'
        with self.assertRaises(CallFailure) as caught:
            parse_selection(response,[dict(id=1,angle=0,power=30)],False)
        self.assertEqual(caught.exception.metadata['error_kind'],'invalid_candidate_selection')
        self.assertEqual(caught.exception.metadata['usage']['input_tokens'],100)

    def test_quadrant_candidates_and_portal_obstruction(self):
        e=Episode();o=e.observe('p1');o['devices']['guides']=[];o['bumpers']=[]
        o['devices'].pop('bridge',None);o['devices'].pop('scoop',None)
        for x,y,a in [(600,350,45),(400,350,135),(400,150,225),(600,150,315)]:
            o['balls']=[dict(id=0,x=500,y=250),dict(id=1,x=x,y=y)]
            row=next(r for r in candidates(o,e.legal_actions('p1')) if r['route']=='contact')
            self.assertEqual(row['angle'],a)
        o['balls']=[dict(id=0,x=230,y=250),dict(id=1,x=700,y=250)]
        o['devices']['bridge']=dict(x=450,y=250,radius=14)
        self.assertFalse(any(r['route']=='contact' for r in candidates(o,e.legal_actions('p1'))))

    def test_live_variant_identity_and_executed_mock_selection(self):
        from fusion.geometry_live import GeometrySession
        from test_live_demo import wait_for
        from fusion.runner import replay
        with tempfile.TemporaryDirectory() as d:
            s=GeometrySession(Path(d),transport=fixture);s.start(True,s.nonce)
            state=wait_for(s,{'playback','failed'})
            self.assertEqual(state['live']['phase'],'playback')
            packet=s.packet();metadata=s.trace['steps'][0]['model_metadata']
            self.assertEqual(packet['action'],{k:metadata['selected_candidate'][k] for k in ('angle','power')})
            self.assertEqual(state['live']['variant'],'kinetic-geometry-assisted-v1')
            s.cancel();s.worker.join(3);replay(s.trace)
            self.assertEqual(s.trace['consent']['variant'],'kinetic-geometry-assisted-v1')

    def test_restricted_angles_and_bank(self):
        e=Episode();legal=e.legal_actions('p1');legal.update(angle_min=90,angle_max=90)
        self.assertTrue(all(r['angle']==90 for r in candidates(e.observe('p1'),legal)))
        e=Episode(layout=[(230,250),(700,250)]);o=e.observe('p1');o['bumpers']=[]
        o['devices']['guides']=[];o['devices'].pop('bridge',None);o['devices'].pop('scoop',None)
        self.assertTrue(any(r['route']=='bank-contact' for r in candidates(o,e.legal_actions('p1'))))

    def test_oblique_bank_matches_normal_only_cushion_loss(self):
        e=Episode(layout=[(200,300),(600,300)])
        e.bumpers=[];e.devices['guides']=[]
        e.devices.pop('bridge',None);e.devices.pop('scoop',None)
        rows=candidates(e.observe('p1'),e.legal_actions('p1'))
        bank=next(r for r in rows if r['route']=='bank-contact' and 180<r['angle']<360)
        e.replenishments_used=2
        e.step('p1',{k:bank[k] for k in ('angle','power')})
        target=next(b for b in e.balls if b.id==1)
        self.assertGreater(math.dist((target.x,target.y),(600,300)),1)

    def test_worker_failure_budget_timeout_and_consent(self):
        e=Episode();o=e.observe('p1');legal=e.legal_actions('p1')
        with self.assertRaises(CallFailure) as caught:GeometryPlayer().select(o,legal,[],1)
        self.assertEqual(caught.exception.metadata['error_kind'],'paid_call_not_approved')
        with tempfile.TemporaryDirectory() as d:
            p=GeometryPlayer(transport=bad_fixture);p.ledger=Ledger(Path(d)/'bad.jsonl',1,1)
            with self.assertRaises(CallFailure) as caught:p.select(o,legal,[],3)
            self.assertEqual(p.ledger.calls,1)
            self.assertEqual(caught.exception.metadata['usage']['input_tokens'],100)
            self.assertNotIn('action',caught.exception.metadata)
            p=GeometryPlayer(transport=hanging_fixture);p.ledger=Ledger(Path(d)/'hung.jsonl',1,1)
            start=time.monotonic()
            with self.assertRaises(CallFailure) as caught:p.select(o,legal,[],.2)
            self.assertEqual(str(caught.exception),'request_timeout')
            self.assertEqual(p.ledger.calls,1);self.assertEqual(p.ledger.unknown,1)
            self.assertLess(time.monotonic()-start,3)

    def test_geometry_http_identity_and_paid_disabled(self):
        import threading
        from urllib.request import urlopen
        from fusion.geometry_live import make_geometry_servers
        with tempfile.TemporaryDirectory() as d:
            game,recorded,live=make_geometry_servers(0,0,0,root=Path(d))
            worker=threading.Thread(target=live.serve_forever,daemon=True);worker.start()
            try:
                with urlopen('http://127.0.0.1:'+str(live.server_port)+'/live.js') as response:
                    script=response.read().decode()
                self.assertIn('kinetic-geometry-assisted-v1',script)
                self.assertNotIn('kinetic-prompt-v2-risk-aware',script)
                self.assertFalse(live.live_session.state()['live']['can_start'])
                self.assertEqual(live.live_session.state()['live']['calls'],0)
            finally:
                live.shutdown();worker.join();live.server_close();game.server_close();recorded.server_close()


if __name__=='__main__':unittest.main()
