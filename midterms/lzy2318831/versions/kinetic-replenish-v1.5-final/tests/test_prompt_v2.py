"""Prompt-only contracts; synthetic responses are never LLM performance evidence."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from fusion.engine import Episode
from fusion.llm import ModelPlayer,Ledger,CallFailure,SYSTEM as ORIGINAL_SYSTEM,call_model
from fusion.prompt_v2 import ImprovedModelPlayer,SYSTEM,VARIANT
from fusion.runner import run_match,replay


def response(payload,timeout):
    return dict(status='completed',model=payload['model'],usage=dict(input_tokens=100,output_tokens=20,total_tokens=120),
        output=[dict(type='message',content=[dict(type='output_text',text='{"angle":0,"power":1}')])])


def bad_response(payload,timeout):
    result=response(payload,timeout);result['output'][0]['content'][0]['text']='{"angle":360,"power":50}'
    return result


class PromptV2(unittest.TestCase):
    def test_only_developer_prompt_changes(self):
        e=Episode();o=e.observe('p1');legal=e.legal_actions('p1');snapshot=copy.deepcopy(o)
        old=ModelPlayer('gpt-5.4-mini-2026-03-17').request(o,legal,[])
        new=ImprovedModelPlayer().request(o,legal,[])
        self.assertNotEqual(old['input'][0]['content'],new['input'][0]['content'])
        new['input'][0]['content']=old['input'][0]['content']
        self.assertEqual(old,new);self.assertEqual(o,snapshot)
        self.assertIn(ORIGINAL_SYSTEM,SYSTEM)

    def test_same_public_feedback_no_added_history(self):
        e=Episode();o=e.observe('p1')
        o['last_shot']=dict(player='p2',foul=True,points=0)
        request=ImprovedModelPlayer().request(o,e.legal_actions('p1'),[dict(private='must_not_be_sent')])
        context=json.loads(request['input'][1]['content'])
        self.assertEqual(context['history'],[])
        self.assertEqual(context['observation']['last_shot'],o['last_shot'])
        self.assertNotIn('private',request['input'][1]['content'])
        with self.assertRaises(ValueError):ImprovedModelPlayer(memory=True)
        with self.assertRaises(ValueError):ImprovedModelPlayer().request(dict(o,secret='x'),e.legal_actions('p1'),[])

    def test_unchanged_strict_parser(self):
        p=ImprovedModelPlayer(transport=response)
        action,meta=p.parse(response({'model':p.model},1))
        self.assertEqual(action,dict(angle=0,power=1));self.assertFalse(meta['live'])
        with self.assertRaises(CallFailure):p.parse(bad_response({'model':p.model},1))

    def test_runner_and_audit_compatibility_no_replacement(self):
        with tempfile.TemporaryDirectory() as d:
            p=ImprovedModelPlayer(transport=response);p.ledger=Ledger(Path(d)/'calls.jsonl',1,1)
            trace=run_match(seats=('prompt_v2','baseline'),players={'prompt_v2':p},model_call_limit=1)
            self.assertEqual(trace['steps'][0]['action'],dict(angle=0,power=1));replay(trace)
            meta=trace['steps'][0]['model_metadata']
            self.assertEqual(meta['agent_variant'],VARIANT)
            self.assertEqual(meta['prompt_sha256'],hashlib.sha256(SYSTEM.encode()).hexdigest())
            self.assertNotEqual(meta['prompt_sha256'],hashlib.sha256(ORIGINAL_SYSTEM.encode()).hexdigest())
            audit=[json.loads(line) for line in (Path(d)/'calls.jsonl').read_text().splitlines()]
            self.assertEqual(audit[1]['metadata'],meta)
            self.assertEqual(audit[0]['request']['input'][0]['content'],SYSTEM)
            self.assertEqual(p.ledger.calls,1)

    def test_invalid_action_keeps_usage_and_v2_identity(self):
        with tempfile.TemporaryDirectory() as d:
            p=ImprovedModelPlayer(transport=bad_response);ledger=Ledger(Path(d)/'calls.jsonl',1,1)
            e=Episode()
            with self.assertRaises(CallFailure) as caught:p.select(e.observe('p1'),e.legal_actions('p1'),[],2,ledger)
            self.assertEqual(caught.exception.metadata['agent_variant'],VARIANT)
            self.assertEqual(caught.exception.metadata['usage']['input_tokens'],100)
            self.assertEqual(ledger.calls,1)

    def test_live_unapproved_refuses_without_request(self):
        e=Episode();p=ImprovedModelPlayer()
        with tempfile.TemporaryDirectory() as d:
            ledger=Ledger(Path(d)/'calls.jsonl',1,1)
            with self.assertRaises(CallFailure):p.select(e.observe('p1'),e.legal_actions('p1'),[],1,ledger)
            self.assertEqual(ledger.calls,0)
