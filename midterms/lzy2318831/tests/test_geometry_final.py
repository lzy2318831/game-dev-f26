"""Final preferred-launcher checks; network boundary is always synthetic."""
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch,MagicMock
from urllib.request import urlopen
from fusion.geometry_live import make_geometry_servers,GeometrySession
from fusion.geometry_agent import GeometryPlayer,_worker,offline_response,VARIANT
from fusion.engine import Episode
from test_live_demo import wait_for


def slow_geometry_response(payload,timeout):
    time.sleep(.5)
    return offline_response(payload,timeout)


class FinalGeometry(unittest.TestCase):
    def test_preferred_menu_failure_labels_and_navigation(self):
        with tempfile.TemporaryDirectory() as d:
            game,recorded,live=make_geometry_servers(0,0,0,root=Path(d))
            threads=[threading.Thread(target=s.serve_forever,daemon=True) for s in (game,recorded,live)]
            for t in threads:t.start()
            try:
                def get(server,path):
                    with urlopen('http://127.0.0.1:'+str(server.server_port)+path) as r:return r.read().decode()
                menu=get(game,'/menu.js');script=get(live,'/live.js')
                for label in ['Geometry-Assisted Live LLM','Recorded LLM Replay','Human vs Geometric AI','Human vs Smart AI']:
                    self.assertIn(label,menu)
                self.assertIn('No supported shot candidate',script)
                self.assertIn('no other agent',script)
                self.assertEqual(json.loads(get(live,'/navigation/info'))['menu_url'],game.menu_url)
                self.assertFalse(live.live_session.state()['live']['can_start'])
                self.assertIn('Back to Main Menu',script)
            finally:
                for s in (game,recorded,live):s.shutdown();s.server_close()
                for t in threads:t.join()

    def test_real_transport_branch_without_network(self):
        e=Episode();payload=GeometryPlayer().request(e.observe('p1'),e.legal_actions('p1'))
        rows=json.loads(payload['input'][1]['content'])['candidates']
        send=MagicMock();raw=offline_response(payload,1)
        raw['id']='SYNTHETIC_HTTP_CONTRACT_NOT_REAL_API'
        raw['output'][0]['content'][0]['text']=json.dumps(dict(candidate_id=rows[-1]['id']))
        with patch('fusion.geometry_agent.send_openai',return_value=raw) as api:
            _worker(send,dict(request=payload,timeout=1),rows,None)
        api.assert_called_once_with(payload,1)
        status,action,metadata=send.send.call_args.args[0]
        self.assertEqual(status,'ok');self.assertTrue(metadata['live'])
        self.assertEqual(action,{k:rows[-1][k] for k in ('angle','power')})
        self.assertEqual(payload['tools'],[]);self.assertEqual(payload['model'],'gpt-5.4-mini-2026-03-17')
        self.assertNotIn('OPENAI_API_KEY',json.dumps(payload))

    def test_masked_launcher_and_single_match_cancel(self):
        launcher=Path('run-geometry-live.ps1').read_text()
        self.assertIn('-AsSecureString',launcher);self.assertIn('finally',launcher)
        self.assertIn('fusion.geometry_live --enable-paid',launcher)
        self.assertIn('fusion.geometry_live --mock',launcher)
        with tempfile.TemporaryDirectory() as d:
            s=GeometrySession(Path(d),transport=offline_response);s.start(True,s.nonce)
            state=wait_for(s,{'playback','failed'});self.assertEqual(state['live']['phase'],'playback')
            s.cancel();s.worker.join(3)
            self.assertEqual(s.state()['live']['phase'],'cancelled')
            self.assertEqual(s.state()['live']['calls'],1)
            with self.assertRaises(ValueError):s.start(True,s.nonce)

    def test_actual_openai_http_adapter_with_synthetic_http(self):
        e=Episode();payload=GeometryPlayer().request(e.observe('p1'),e.legal_actions('p1'))
        rows=json.loads(payload['input'][1]['content'])['candidates'];send=MagicMock()
        response=MagicMock();response.status=200
        response.read.return_value=json.dumps(offline_response(payload,1)).encode()
        opener=MagicMock();opener.open.return_value.__enter__.return_value=response
        with patch.dict('os.environ',{'OPENAI_API_KEY':'offline-contract-fixture'}),patch('fusion.llm.http.build_opener',return_value=opener):
            _worker(send,dict(request=payload,timeout=1),rows,None)
        request=opener.open.call_args.args[0]
        self.assertEqual(request.full_url,'https://api.openai.com/v1/responses')
        self.assertEqual(request.get_header('Authorization'),'Bearer offline-contract-fixture')
        self.assertEqual(json.loads(request.data)['text']['format']['name'],'geometry_candidate')
        status,action,metadata=send.send.call_args.args[0]
        self.assertEqual(status,'ok');self.assertEqual(metadata['http_status'],200)
        self.assertEqual(action,{k:rows[0][k] for k in ('angle','power')})

    def test_cancel_inflight_selection_never_commits_move(self):
        with tempfile.TemporaryDirectory() as d:
            s=GeometrySession(Path(d),transport=slow_geometry_response);s.start(True,s.nonce)
            end=time.monotonic()+5
            while s.state()['live']['calls']==0 and time.monotonic()<end:time.sleep(.01)
            self.assertEqual(s.state()['live']['calls'],1)
            s.cancel();s.worker.join(3)
            self.assertEqual(s.state()['live']['phase'],'cancelled')
            self.assertEqual(s.trace['steps'],[])
            self.assertEqual(s.state()['live']['calls'],1)


if __name__=='__main__':unittest.main()
