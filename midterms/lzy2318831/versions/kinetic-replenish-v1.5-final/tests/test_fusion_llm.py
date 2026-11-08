import unittest,json,copy,tempfile
from pathlib import Path
from fusion.engine import Episode

def valid_transport(payload,timeout):
 return dict(status='completed',model='offline-provider-response-fixture',id='fixture',usage=dict(input_tokens=100,output_tokens=20,total_tokens=120),output=[dict(type='message',content=[dict(type='output_text',text='{"angle":180,"power":1}')])])

def invalid_transport(payload,timeout):
 response=valid_transport(payload,timeout);response['output'][0]['content'][0]['text']='not json';return response

def secret_error(payload,timeout):raise RuntimeError('DO_NOT_LOG_PRIVATE_ERROR')

def hanging_transport(payload,timeout):
 import time
 time.sleep(10)
 return valid_transport(payload,timeout)

class LLMContracts(unittest.TestCase):
 def test_request_is_public_and_structured(self):
  from fusion.llm import ModelPlayer
  e=Episode();p=ModelPlayer('gpt-5.4-mini-2026-03-17');o=e.observe('p1');before=copy.deepcopy(o)
  request=p.request(o,e.legal_actions('p1'),[])
  self.assertEqual(request['tools'],[]);self.assertFalse(request['store'])
  self.assertTrue(request['text']['format']['strict']);self.assertEqual(request['service_tier'],'default');self.assertEqual(o,before)
  self.assertNotIn('OPENAI_API_KEY',json.dumps(request));self.assertNotIn('simulator',request['input'][1]['content'])
  with self.assertRaises(ValueError):p.request(dict(o,secret='x'),e.legal_actions('p1'),[])
 def test_parse_valid_invalid_and_usage(self):
  from fusion.llm import ModelPlayer,CallFailure
  p=ModelPlayer('gpt-5.4-mini-2026-03-17')
  def response(text):return dict(status='completed',model='actual-snapshot',id='resp-test',usage=dict(input_tokens=100,output_tokens=20),output=[dict(type='message',content=[dict(type='output_text',text=text)])])
  action,m=p.parse(response('{"angle":17,"power":65}'));self.assertEqual(action,dict(angle=17,power=65));self.assertGreater(m['estimated_cost_usd'],0)
  for text in ['bad','{"angle":360,"power":50}','{"angle":true,"power":50}','{"angle":5,"power":1,"tool":"shell"}']:
   with self.assertRaises(CallFailure) as caught:p.parse(response(text))
   self.assertEqual(caught.exception.metadata['usage']['input_tokens'],100)
 def test_live_requires_explicit_consent(self):
  from fusion.llm import ModelPlayer,call_model,Ledger,CallFailure
  e=Episode();p=ModelPlayer('gpt-5.4-mini-2026-03-17')
  with tempfile.TemporaryDirectory() as d:
   ledger=Ledger(Path(d)/'audit.jsonl',1,1)
   with self.assertRaises(CallFailure):call_model(p,e.observe('p1'),e.legal_actions('p1'),[],1,ledger=ledger)
   self.assertEqual(ledger.calls,0)

 def test_real_boundary_executes_fixture_action_and_replays(self):
  from fusion.llm import ModelPlayer,Ledger
  from fusion.runner import run_match,replay
  with tempfile.TemporaryDirectory() as d:
   p=ModelPlayer('gpt-5.4-mini-2026-03-17',transport=valid_transport);p.ledger=Ledger(Path(d)/'calls.jsonl',10,1)
   trace=run_match(seats=('llm','baseline'),players={'llm':p},model_call_limit=1)
   self.assertEqual(trace['steps'][0]['action'],dict(angle=180,power=1));self.assertEqual(replay(trace),trace['outcome'])
   self.assertFalse(trace['steps'][0]['model_metadata']['live'])
   self.assertEqual(trace['model_calls'],1);self.assertEqual(p.ledger.calls,1)
   self.assertEqual(len((Path(d)/'calls.jsonl').read_text().splitlines()),2)

 def test_invalid_keeps_usage_and_counts_failed_call(self):
  from fusion.llm import ModelPlayer,Ledger
  from fusion.runner import run_match
  with tempfile.TemporaryDirectory() as d:
   p=ModelPlayer('gpt-5.4-mini-2026-03-17',transport=invalid_transport);p.ledger=Ledger(Path(d)/'audit.jsonl',2,1)
   trace=run_match(seats=('llm','baseline'),players={'llm':p})
   self.assertEqual(trace['model_calls'],1);self.assertEqual(trace['outcome']['reason'],'invalid_model_response');self.assertEqual(trace['steps'],[])
   self.assertEqual(trace['call_events'][0]['metadata']['usage']['input_tokens'],100)
   self.assertGreater(p.ledger.estimated,0)

 def test_watchdog_unknown_cost_and_error_privacy(self):
  from fusion.llm import ModelPlayer,Ledger,call_model,CallFailure
  e=Episode()
  for transport in (hanging_transport,secret_error):
   with tempfile.TemporaryDirectory() as d:
    ledger=Ledger(Path(d)/'calls.jsonl',1,1);p=ModelPlayer('gpt-5.4-mini-2026-03-17',transport=transport)
    with self.assertRaises(CallFailure):call_model(p,e.observe('p1'),e.legal_actions('p1'),[],.5,ledger)
    self.assertEqual(ledger.calls,1);self.assertEqual(ledger.unknown,1)
    self.assertNotIn('DO_NOT_LOG',ledger.path.read_text())

 def test_ledger_budget_refuses_before_dispatch_and_no_overwrite(self):
  from fusion.llm import ModelPlayer,Ledger,CallFailure
  e=Episode();request=ModelPlayer('gpt-6-luna').request(e.observe('p1'),e.legal_actions('p1'),[])
  with tempfile.TemporaryDirectory() as d:
   ledger=Ledger(Path(d)/'audit',1,.000001)
   with self.assertRaises(CallFailure):ledger.reserve(request,True)
   self.assertEqual(ledger.calls,0)
   ledger=Ledger(Path(d)/'audit',1,1);ledger.reserve(request,False)
   with self.assertRaises(CallFailure):ledger.reserve(request,False)
   with self.assertRaises(ValueError):Ledger(Path(d)/'audit',1,1)

 def test_plan_counts_and_offline_fixture_suite(self):
  from fusion.llm_eval import plan,execute
  p=plan('gpt-6-luna');self.assertEqual(p['max_calls'],72);self.assertEqual(p['live_matches'],12)
  self.assertEqual(plan('gpt-6-luna','both')['max_calls'],144)
  p['trials']=p['trials'][:1];p['trials'][0]['layout']=[[230,250],[740,250]]
  with tempfile.TemporaryDirectory() as d:
   result=execute(p,Path(d)/'run',False,1,1,transport=valid_transport)
   self.assertEqual(result['kind'],'offline_fixture_NOT_LLM_EVIDENCE')
   self.assertTrue((Path(d)/'run/comparison.csv').exists());self.assertEqual(result['accounting']['calls'],1)

 def test_completed_reply_at_deadline_retains_metadata(self):
  from fusion.runner import run_match
  from unittest.mock import patch
  class Flag: is_model=True;genuine_llm=True
  times=iter([0,0,0,0,.2,.2,.2])
  with patch('fusion.runner.call_model',return_value=({'angle':0,'power':1},{'usage':{'input_tokens':7},'estimated_cost_usd':.1})),patch('fusion.runner.time.monotonic',side_effect=lambda:next(times)):
   trace=run_match(seats=('llm','baseline'),players={'llm':Flag()},deadline_seconds=.1)
  self.assertEqual(trace['outcome']['reason'],'episode_timeout');self.assertEqual(trace['steps'],[])
  self.assertEqual(trace['call_events'][0]['metadata']['usage']['input_tokens'],7)

 def test_malformed_envelopes_retain_usage_and_duplicate_keys_reject(self):
  from fusion.llm import ModelPlayer,CallFailure
  p=ModelPlayer('gpt-6-luna')
  for output in [None,[None],[{'type':'message','content':None}],[{'type':'message','content':[None]}],[{'type':'message','content':[{'type':'output_text','text':'{"angle":0,"angle":30,"power":5}'}]}]]:
   with self.assertRaises(CallFailure) as caught:p.parse(dict(status='completed',usage=dict(input_tokens=100,output_tokens=10),output=output))
   self.assertEqual(caught.exception.metadata['usage']['input_tokens'],100)
 def test_control_latency(self):
  from fusion.llm_eval import metrics
  trace=dict(steps=[dict(player='p1',events=[],latency_seconds=.4)],call_events=[],outcome=dict(scores={'p1':0},invalid_actions={'p1':0},failure=False,reason='shots_exhausted'))
  self.assertEqual(metrics(trace,'p1')['latency_seconds'],.4)

 def test_zero_cli_limit_rejected_without_network(self):
  from fusion.llm_eval import main
  from unittest.mock import patch
  import contextlib,io
  with patch('sys.argv',['llm_eval','--max-calls','0']),patch('fusion.llm_eval.execute') as execute,contextlib.redirect_stderr(io.StringIO()):
   with self.assertRaises(SystemExit):main()
   execute.assert_not_called()
 def test_http_adapter_contract_and_no_redirect(self):
  from fusion.llm import send_openai,NoRedirect
  from unittest.mock import patch,MagicMock
  response=MagicMock();response.__enter__.return_value.status=200;response.__enter__.return_value.read.return_value=json.dumps(valid_transport({},1)).encode()
  opener=MagicMock();opener.open.return_value=response
  with patch.dict('os.environ',{'OPENAI_API_KEY':'offline-test-secret'}),patch('fusion.llm.http.build_opener',return_value=opener):
   data=send_openai({'model':'offline-fixture'},1)
  self.assertEqual(data['status'],'completed');self.assertEqual(data['_transport_http_status'],200)
  req=opener.open.call_args.args[0];self.assertEqual(req.full_url,'https://api.openai.com/v1/responses')
  self.assertNotIn('offline-test-secret',req.data.decode());self.assertIsNone(NoRedirect().redirect_request(None))
