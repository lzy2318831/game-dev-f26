"""Public-context boundary and interruptible policy calls; no API adapter."""
from copy import deepcopy
import json
import multiprocessing as mp

from pool.model import ModelFailure

PUBLIC_FIELDS={'player_id','active_player','table','balls','scores','timer','heat','heats',
               'extended','bonus_awarded','scratches','clearances','invalid_actions',
               'last_events','frames_per_step','status'}


def build_context(observation,legal_actions,history=()):
    if set(observation)!=PUBLIC_FIELDS or not legal_actions:
        raise ValueError('Unexpected fields or inactive player')
    # A serialization round trip prevents references reaching engine objects.
    public=json.loads(json.dumps(observation,allow_nan=False))
    records=deepcopy(list(history)[-2:])
    while records and len(json.dumps(records))>2000:
        records.pop(0)
    return dict(observation=public,actions=dict(x_min=0,x_max=15,y_min=0,y_max=15,
                neutral=[7,8],hold_frames=observation['frames_per_step']),history=records)


def _worker(send,policy,context,legal,timeout):
    try:
        action=policy.decide(context['observation'],legal,context['history'],timeout=timeout)
        send.send(('ok',action,getattr(policy,'last_metadata',None)))
    except ModelFailure as error:
        reason=str(error)
        send.send(('failure',reason if reason in {'provider_error','request_timeout','invalid_model_response'} else 'provider_error',None))
    except Exception:
        send.send(('failure','provider_error',None))
    finally:
        send.close()


def invoke(policy,observation,legal_actions,history,timeout):
    """Parent can terminate a hung model policy, even if adapter ignores timeout."""
    context=build_context(observation,legal_actions,history)
    ctx=mp.get_context('spawn')
    receive,send=ctx.Pipe(duplex=False)
    process=ctx.Process(target=_worker,args=(send,policy,context,legal_actions,timeout),daemon=True)
    try:
        process.start()
        send.close()
        if not receive.poll(timeout):
            raise ModelFailure('request_timeout')
        try:
            status,action,metadata=receive.recv()
        except EOFError:
            raise ModelFailure('provider_error') from None
        if status!='ok':
            raise ModelFailure(action)
        if not isinstance(action,dict):
            raise ModelFailure('invalid_model_response')
        return action,metadata
    except ModelFailure:
        raise
    except Exception:
        raise ModelFailure('provider_error') from None
    finally:
        receive.close()
        send.close()
        if process.pid is not None:
            if process.is_alive():
                process.terminate()
            process.join(timeout=1)
            if process.is_alive():
                process.kill()
                process.join(timeout=1)
