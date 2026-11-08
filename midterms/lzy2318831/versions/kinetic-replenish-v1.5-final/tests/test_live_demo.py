"""All provider replies here are mocked; never a live model evaluation."""
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from fusion.prompt_v2 import offline_response,VARIANT
from fusion.llm import CallFailure
from fusion.live_demo import LiveSession,MatchLedger
from fusion.runner import replay


def failure(payload,timeout):
    raise CallFailure('provider_error',dict(error_kind='http_error',http_status=429))


def slow_response(payload,timeout):
    time.sleep(.6)
    return offline_response(payload,timeout)


def wait_for(session,phases,seconds=20):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        state=session.state()
        if state['live']['phase'] in phases:return state
        time.sleep(.01)
    raise AssertionError('Timed out waiting for '+str(phases))


class LiveDemo(unittest.TestCase):
    def test_get_and_missing_confirmation_never_call(self):
        with tempfile.TemporaryDirectory() as d:
            s=LiveSession(Path(d),transport=offline_response)
            for _ in range(3):self.assertEqual(s.state()['live']['calls'],0)
            with self.assertRaises(ValueError):s.start(False,s.nonce)
            with self.assertRaises(ValueError):s.start(True,'wrong')
            self.assertFalse(list(Path(d).iterdir()))
            s.cancel();self.assertEqual(s.state()['live']['phase'],'cancelled')

    def test_paid_server_disabled_even_with_key(self):
        with tempfile.TemporaryDirectory() as d,patch.dict('os.environ',{'OPENAI_API_KEY':'offline-test-value'}):
            s=LiveSession(Path(d))
            with self.assertRaises(ValueError):s.start(True,s.nonce)
            self.assertEqual(s.state()['live']['calls'],0)

    def test_full_autonomous_mock_match_and_replay(self):
        with tempfile.TemporaryDirectory() as d:
            s=LiveSession(Path(d),transport=offline_response)
            s.start(True,s.nonce)
            with self.assertRaises(ValueError):s.start(True,s.nonce)
            while True:
                state=wait_for(s,{'playback','complete','failed','cancelled'})
                if state['live']['phase']!='playback':break
                packet=s.packet()
                self.assertTrue(packet['shot']['frames'])
                self.assertEqual(set(packet['action']),{'angle','power'})
                s.ready(packet['sequence'])
            s.worker.join(3)
            self.assertEqual(s.state()['live']['phase'],'complete')
            self.assertEqual(s.state()['live']['calls'],6)
            trace=json.loads((s.directory/'trace.json').read_text())
            self.assertEqual(trace['kind'],'MOCKED_LIVE_DEMO_NOT_REAL_LLM')
            self.assertEqual(trace['outcome']['shots'],12);replay(trace)
            model_rows=[r for r in trace['steps'] if r['source']=='model']
            self.assertEqual(len(model_rows),6)
            self.assertTrue(all(r['model_metadata']['agent_variant']==VARIANT for r in model_rows))
            self.assertNotIn('offline-test-value',json.dumps(s.state()))

    def test_provider_failure_no_retry(self):
        with tempfile.TemporaryDirectory() as d:
            s=LiveSession(Path(d),transport=failure);s.start(True,s.nonce)
            state=wait_for(s,{'failed'})
            self.assertEqual(state['live']['calls'],1)
            self.assertEqual(state['outcome']['reason'],'provider_error')
            s.worker.join(3);self.assertEqual(len(s.trace['steps']),0)

    def test_cancel_inflight_discards_reply_and_blocks_new_calls(self):
        with tempfile.TemporaryDirectory() as d:
            s=LiveSession(Path(d),transport=slow_response);s.start(True,s.nonce)
            end=time.monotonic()+5
            while s.state()['live']['calls']==0 and time.monotonic()<end:time.sleep(.01)
            s.cancel();s.worker.join(5)
            state=s.state()
            self.assertEqual(state['live']['phase'],'cancelled')
            self.assertEqual(state['live']['calls'],1)
            self.assertEqual(state['outcome']['shots'],0)
            self.assertFalse(s.trace['call_events'][0]['executed'])
            replay(s.trace)

    def test_match_ledger_has_strict_caps(self):
        from fusion.prompt_v2 import MODEL
        with tempfile.TemporaryDirectory() as d:
            ledger=MatchLedger(Path(d)/'calls.jsonl')
            for _ in range(6):
                reserved=ledger.reserve({'model':MODEL},False)
                ledger.finish(reserved,dict(estimated_cost_usd=.001))
            with self.assertRaises(CallFailure):ledger.reserve({'model':MODEL},False)
            self.assertEqual(ledger.calls,6);self.assertEqual(ledger.budget_usd,.25)
            ledger=MatchLedger(Path(d)/'budget.jsonl');ledger.committed=.249
            with self.assertRaises(CallFailure):ledger.reserve({'model':MODEL},False)
            self.assertEqual(ledger.calls,0)

    def test_cancel_before_reservation_blocks_dispatch(self):
        from fusion.prompt_v2 import ImprovedModelPlayer
        entered=threading.Event();release=threading.Event();original=ImprovedModelPlayer.select
        def delayed(policy,*args,**kwargs):
            entered.set();release.wait(3);return original(policy,*args,**kwargs)
        with tempfile.TemporaryDirectory() as d,patch.object(ImprovedModelPlayer,'select',new=delayed):
            s=LiveSession(Path(d),transport=offline_response);s.start(True,s.nonce)
            self.assertTrue(entered.wait(3));s.cancel();release.set();s.worker.join(3)
            self.assertEqual(s.state()['live']['phase'],'cancelled')
            self.assertEqual(s.state()['live']['calls'],0)
            self.assertEqual(s.episode.shots,0)

    def test_cancel_during_physics_cannot_lose_wake(self):
        from fusion.engine import Episode
        entered=threading.Event();release=threading.Event();original=Episode.step
        def delayed(episode,*args,**kwargs):
            entered.set();release.wait(3);return original(episode,*args,**kwargs)
        with tempfile.TemporaryDirectory() as d,patch.object(Episode,'step',new=delayed):
            s=LiveSession(Path(d),transport=offline_response);s.start(True,s.nonce)
            self.assertTrue(entered.wait(3))
            cancel=threading.Thread(target=s.cancel);cancel.start()
            self.assertTrue(s.cancel_event.wait(1));release.set();cancel.join(3);s.worker.join(3)
            if s.worker.is_alive():s.playback_done.set();s.worker.join(3);self.fail('Cancellation wake was lost')
            self.assertEqual(s.state()['live']['phase'],'cancelled')
            self.assertEqual(s.state()['live']['calls'],1)

    def test_missing_browser_ack_stops_safely(self):
        with tempfile.TemporaryDirectory() as d:
            s=LiveSession(Path(d),transport=offline_response);s.playback_timeout=.03;s.start(True,s.nonce)
            state=wait_for(s,{'failed'});s.worker.join(3)
            self.assertEqual(state['live']['calls'],1)
            self.assertEqual(state['live']['reason'],'playback_ack_timeout')
            self.assertTrue(state['outcome']['failure']);replay(s.trace)

    def test_http_confirmation_origin_and_no_manual_shots(self):
        import http.client
        from fusion.demo import make_servers
        from fusion.live_demo import make_live_server,EntryHandler
        with tempfile.TemporaryDirectory() as d,patch.dict('os.environ',{'OPENAI_API_KEY':'sentinel-not-for-browser'}):
            game,recorded=make_servers(0,0);live=make_live_server(0,transport=offline_response,root=Path(d))
            game.RequestHandlerClass=EntryHandler;game.live_port=live.server_port
            servers=(game,recorded,live);threads=[threading.Thread(target=s.serve_forever,daemon=True) for s in servers]
            for t in threads:t.start()
            try:
                c=http.client.HTTPConnection('127.0.0.1',game.server_port)
                c.request('GET','/');r=c.getresponse();page=r.read().decode()
                self.assertIn('Watch LLM Agent Play',page);self.assertIn('Start Live LLM Agent',page);c.close()
                c=http.client.HTTPConnection('127.0.0.1',live.server_port)
                c.request('GET','/live/info');r=c.getresponse();info=r.read().decode()
                self.assertNotIn('sentinel-not-for-browser',info);info=json.loads(info)
                headers={'Origin':f'http://127.0.0.1:{live.server_port}','Content-Type':'application/json','X-Live-Token':info['nonce']}
                for path,body,status in (('/live/start',{'confirmed':False},400),('/api/shot',{'action':{'angle':0,'power':1}},400)):
                    c.request('POST',path,json.dumps(body),headers);r=c.getresponse();r.read();self.assertEqual(r.status,status)
                bad=dict(headers,Origin='https://untrusted.invalid')
                c.request('POST','/live/start',json.dumps({'confirmed':True}),bad);r=c.getresponse();r.read();self.assertEqual(r.status,403)
                c.request('POST','/live/start',json.dumps({'confirmed':True}),{k:v for k,v in headers.items() if k!='X-Live-Token'})
                r=c.getresponse();r.read();self.assertEqual(r.status,403)
                self.assertEqual(live.live_session.state()['live']['calls'],0)
                c.request('GET','/live.js');r=c.getresponse();js=r.read().decode()
                self.assertIn('window.confirm',js);self.assertNotIn('sentinel-not-for-browser',js)
                c.request('POST','/live/start',json.dumps({'confirmed':True}),headers);r=c.getresponse();r.read();self.assertEqual(r.status,200)
                c.request('POST','/live/cancel','{}',headers);r=c.getresponse();r.read();self.assertEqual(r.status,200);c.close()
            finally:
                live.live_session.cancel()
                if live.live_session.worker:live.live_session.worker.join(5)
                for s in servers:s.shutdown();s.server_close()
                for t in threads:t.join()
