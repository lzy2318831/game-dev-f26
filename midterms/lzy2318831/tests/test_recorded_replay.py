"""Authentic saved decisions only; no provider or policy invocation."""
import copy
import http.client
import json
import threading
import unittest
from unittest.mock import patch
from fusion.recorded_replay import load_match,ReplaySession,DEFAULT_TRIAL


class RecordedReplay(unittest.TestCase):
    def test_authentic_source_and_failed_trial_rejection(self):
        trace,info=load_match(DEFAULT_TRIAL)
        self.assertEqual(info['trial'],DEFAULT_TRIAL)
        self.assertTrue(info['recorded_real_llm'])
        self.assertEqual(sum(r['source']=='model' for r in trace['steps']),6)
        with self.assertRaises(ValueError):load_match('observation_only-direct-101-p1')
        with self.assertRaises(ValueError):load_match('../arbitrary-file')

    def test_automatic_sequence_matches_recorded_outcome(self):
        trace,info=load_match(DEFAULT_TRIAL);session=ReplaySession(trace,info)
        with patch('fusion.baseline.choose',side_effect=AssertionError('No replacement decisions')):
            for index,row in enumerate(trace['steps']):
                result=session.next()
                self.assertEqual(result['action'],row['action'])
                self.assertEqual(result['shot']['events'],row['events'])
                self.assertEqual(result['recording']['shot'],index+1)
                self.assertTrue(result['shot']['frames'])
                with self.assertRaises(ValueError):session.next()
                session.ready()
        self.assertEqual(session.state()['outcome'],trace['outcome'])
        with self.assertRaises(ValueError):session.next()
        session.reset();self.assertEqual(session.index,0)

    def test_tampering_stops_playback(self):
        trace,info=load_match(DEFAULT_TRIAL);trace=copy.deepcopy(trace)
        trace['steps'][0]['after']='altered'
        session=ReplaySession(trace,info)
        with self.assertRaises(ValueError):session.next()

    def test_game_button_replay_assets_and_manual_action_rejection(self):
        from fusion.demo import make_servers
        game,recorded=make_servers(0,0)
        threads=[threading.Thread(target=s.serve_forever,daemon=True) for s in (game,recorded)]
        for t in threads:t.start()
        try:
            c=http.client.HTTPConnection('127.0.0.1',game.server_port)
            c.request('GET','/');response=c.getresponse();html=response.read().decode()
            self.assertIn('Watch LLM Agent Play',html)
            c.request('GET','/watch');response=c.getresponse();response.read()
            self.assertEqual(response.status,302)
            self.assertEqual(response.getheader('Location'),f'http://127.0.0.1:{recorded.server_port}/#autoplay')
            c.close();c=http.client.HTTPConnection('127.0.0.1',recorded.server_port)
            c.request('GET','/');response=c.getresponse();self.assertIn('/replay.js',response.read().decode())
            c.request('GET','/replay.js');response=c.getresponse();js=response.read().decode()
            self.assertIn('Recorded LLM Evaluation',js)
            self.assertIn('replayPlay',js);self.assertIn('replayPause',js);self.assertIn('replayRestart',js)
            c.request('POST','/replay/next',json.dumps({'angle':0}),{'Content-Type':'application/json'})
            response=c.getresponse();response.read();self.assertEqual(response.status,400)
            c.request('POST','/replay/reset','{}',{'Content-Type':'application/json','Origin':'https://untrusted.invalid'})
            response=c.getresponse();response.read();self.assertEqual(response.status,403)
            c.close()
        finally:
            for s in (game,recorded):s.shutdown();s.server_close()
            for t in threads:t.join()

    def test_occupied_port_is_refused(self):
        from fusion.recorded_replay import ReplayHTTPServer,Handler
        from fusion.demo import make_servers
        held=ReplayHTTPServer(('127.0.0.1',0),Handler)
        try:
            with self.assertRaises(OSError):make_servers(held.server_port,0)
        finally:held.server_close()
