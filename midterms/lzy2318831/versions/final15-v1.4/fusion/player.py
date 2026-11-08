"""Prepared data-only player boundary. No provider, credentials or API calls."""
from copy import deepcopy
import json
import multiprocessing as mp
from historical.player import _worker
from pool.model import ModelFailure

PUBLIC={'player_id','active_player','table','balls','bumpers','devices','scores','shots_remaining',
        'scratches','invalid_actions','last_events','last_shot','status'}


def build_context(observation,legal_actions,history=()):
    if set(observation)!=PUBLIC or not legal_actions: raise ValueError('Unexpected player context')
    records=deepcopy(list(history)[-2:])
    while records and len(json.dumps(records))>2000: records.pop(0)
    return dict(observation=json.loads(json.dumps(observation,allow_nan=False)),
                actions=deepcopy(legal_actions),history=records)


def invoke(policy,observation,legal_actions,history,timeout):
    context=build_context(observation,legal_actions,history)
    ctx=mp.get_context('spawn'); receive,send=ctx.Pipe(duplex=False)
    process=ctx.Process(target=_worker,args=(send,policy,context,legal_actions,timeout),daemon=True)
    try:
        process.start(); send.close()
        if not receive.poll(timeout): raise ModelFailure('request_timeout')
        try: status,action,metadata=receive.recv()
        except EOFError: raise ModelFailure('provider_error') from None
        if status!='ok': raise ModelFailure(action)
        if not isinstance(action,dict): raise ModelFailure('invalid_model_response')
        return action,metadata
    except ModelFailure: raise
    except Exception: raise ModelFailure('provider_error') from None
    finally:
        receive.close(); send.close()
        if process.pid is not None:
            if process.is_alive(): process.terminate()
            process.join(timeout=1)
            if process.is_alive(): process.kill(); process.join(timeout=1)
