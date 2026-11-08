"""Entirely offline adapter-to-engine smoke test. NEVER live LLM evidence."""
import json
import argparse
from pathlib import Path
from .llm import ModelPlayer,Ledger
from .runner import run_match,replay


def fixture(payload,timeout):
    return dict(status='completed',id='offline-fixture',model='OFFLINE_FIXTURE_NOT_REAL_MODEL',
        usage=dict(input_tokens=100,output_tokens=20,total_tokens=120),
        output=[dict(type='message',content=[dict(type='output_text',text='{"angle":180,"power":1}')])])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('evidence/llm-integration/offline-smoke'))
    output=parser.parse_args().output
    output.mkdir(parents=True,exist_ok=False)
    player=ModelPlayer('gpt-5.4-mini-2026-03-17',transport=fixture)
    player.ledger=Ledger(output/'calls.jsonl',6,1)
    trace=run_match(seats=('llm','baseline'),players={'llm':player})
    trace['evidence_kind']='OFFLINE_FIXTURE_ONLY_NOT_LIVE_LLM_EVALUATION'
    (output/'trace.json').write_text(json.dumps(trace,indent=2),encoding='utf-8')
    replay(trace)
    print(json.dumps(dict(kind=trace['evidence_kind'],calls=trace['model_calls'],outcome=trace['outcome']),indent=2))


if __name__=='__main__':main()
