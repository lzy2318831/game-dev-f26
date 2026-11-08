"""Navigation regression: local HTTP and mocked providers only."""
import http.client
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from fusion.live_demo import make_live_servers
from fusion.live_session import LiveSession
from fusion.prompt_v2 import offline_response


def slow_mock(payload,timeout):
    time.sleep(.5);return offline_response(payload,timeout)


class Navigation(unittest.TestCase):
    def test_live_leave_waits_for_inflight_and_retains_budget(self):
        with tempfile.TemporaryDirectory() as d:
            s=LiveSession(Path(d),transport=slow_mock);s.start(True,s.nonce)
            end=time.monotonic()+5
            while s.state()['live']['calls']==0 and time.monotonic()<end:time.sleep(.01)
            result=s.leave()
            self.assertTrue(result['safe_to_navigate']);self.assertFalse(s.worker.is_alive())
            self.assertEqual(result['state']['live']['phase'],'cancelled')
            self.assertEqual(result['state']['live']['calls'],1)
            self.assertEqual(s.episode.shots,0)
            with self.assertRaises(ValueError):s.start(True,s.nonce)
            self.assertFalse(s.trace['call_events'][0]['executed'])

    def test_all_pages_return_to_actual_menu_and_modes_still_play(self):
        with tempfile.TemporaryDirectory() as d:
            servers=make_live_servers(0,0,0,transport=offline_response,root=Path(d))
            game,recorded,live=servers
            threads=[threading.Thread(target=s.serve_forever,daemon=True) for s in servers]
            for t in threads:t.start()
            try:
                expected=f'http://127.0.0.1:{game.server_port}/'
                for server in (recorded,live):
                    c=http.client.HTTPConnection('127.0.0.1',server.server_port)
                    c.request('GET','/navigation/info');r=c.getresponse();self.assertEqual(json.loads(r.read())['menu_url'],expected)
                    c.request('GET','/');r=c.getresponse();self.assertIn('/navigation.js',r.read().decode());c.close()
                c=http.client.HTTPConnection('127.0.0.1',game.server_port)
                c.request('GET','/');r=c.getresponse();self.assertIn('/menu.js',r.read().decode())
                c.request('GET','/menu.js');r=c.getresponse();js=r.read().decode()
                for label in ('Human vs Human','Human vs Geometric AI','Human vs Smart AI','Recorded LLM Replay','Live LLM Agent'):
                    self.assertIn(label,js)
                cookie=None
                for mode in ('hvh','hvb','hvs'):
                    headers={'Content-Type':'application/json'}
                    if cookie:headers['Cookie']=cookie
                    c.request('POST','/api/reset',json.dumps({'mode':mode}),headers)
                    r=c.getresponse();cookie=(r.getheader('Set-Cookie') or cookie).split(';')[0]
                    state=json.loads(r.read());self.assertEqual(state['mode'],mode)
                    self.assertEqual(state['observation']['shots_remaining'],{'p1':6,'p2':6})
                    headers['Cookie']=cookie
                    c.request('POST','/api/shot',json.dumps({'action':{'angle':0,'power':1}}),headers)
                    r=c.getresponse();self.assertTrue(json.loads(r.read())['shot']['accepted'])
                c.close()
                c=http.client.HTTPConnection('127.0.0.1',live.server_port)
                c.request('GET','/live/info');r=c.getresponse();info=json.loads(r.read())
                headers={'Content-Type':'application/json','Origin':f'http://127.0.0.1:{live.server_port}','X-Live-Token':info['nonce']}
                c.request('POST','/live/leave','{}',headers);r=c.getresponse();answer=json.loads(r.read())
                self.assertEqual(r.status,200);self.assertTrue(answer['safe_to_navigate'])
                self.assertEqual(answer['state']['live']['calls'],0);c.close()
            finally:
                live.live_session.leave()
                for s in servers:s.shutdown();s.server_close()
                for t in threads:t.join()
