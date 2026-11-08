"""Prepared model boundary; transport injection only, no billable default.

A provider-specific callable must return text, model, usage metadata. No actual
provider adapter is included yet. Fake transports test application behavior.
"""
import copy
import json
import multiprocessing as mp

PUBLIC_FIELDS = {'player_id', 'active_player', 'table', 'balls', 'scores', 'attempts_remaining', 'scratches', 'invalid_actions', 'last_events', 'status'}
SYSTEM = '''You play Six-ball Pool. Choose your own shot to maximize your score
against the opponent. Return only JSON with integer angle (0..359 clockwise
from right) and power (1..3). Speeds are 180, 300, 420; friction 30 units/s^2;
equal-mass collisions, radius 10, rail restitution 0.9, pocket capture radius 24.
Each object scores one point. A cue scratch voids all points for that shot;
objects stay removed and cue respots. Turns alternate even after scoring.
Match ends on clearance or 24 attempts; higher score wins, ties draw.
Use only the public observation. You have no tools. Do not request code,
credentials, files or predicted engine results.'''


class ModelFailure(Exception):
    pass


def build_context(observation, legal_actions, history=()):
    if set(observation) != PUBLIC_FIELDS:
        raise ValueError('Unexpected observation fields')
    context = dict(observation=copy.deepcopy(observation),
                   actions=dict(angle_min=0, angle_max=359, powers=[1, 2, 3]))
    if not legal_actions:
        raise ValueError('No legal actions')
    records = copy.deepcopy(list(history)[-2:])
    while records and len(json.dumps(records)) > 2000:
        records.pop(0)
    if records:
        context['history'] = records
    return context


def _worker(send, transport, request):
    try:
        send.send(('ok', transport(request)))
    except Exception:
        send.send(('error', None))  # Never log exception text / credentials.
    finally:
        send.close()


class ModelPlayer:
    is_model = True

    def __init__(self, provider, model, transport, timeout=20, history=False):
        if not provider or not model or not callable(transport) or timeout <= 0:
            raise ValueError('Explicit provider/model/transport/timeout required')
        self.provider, self.model, self.transport = provider, model, transport
        self.timeout, self.use_history = timeout, history
        self.last_metadata = {}

    def decide(self, observation, legal_actions, history=(), timeout=None):
        request = dict(system=SYSTEM, context=build_context(observation, legal_actions, history if self.use_history else ()),
                       provider=self.provider, model=self.model, max_output_tokens=512)
        ctx = mp.get_context('spawn')
        receive, send = ctx.Pipe(duplex=False)
        process = ctx.Process(target=_worker, args=(send, self.transport, request), daemon=True)
        try:
            process.start()
            send.close()
            if not receive.poll(min(self.timeout, timeout if timeout is not None else self.timeout)):
                raise ModelFailure('request_timeout')
            try:
                status, response = receive.recv()
            except EOFError:
                raise ModelFailure('provider_error') from None
            if status != 'ok':
                raise ModelFailure('provider_error')
            try:
                action = json.loads(response['text'])
                if not isinstance(action, dict) or set(action) != {'angle', 'power'}:
                    raise ValueError('Missing shot')
            except (KeyError, TypeError, ValueError):
                raise ModelFailure('invalid_model_response') from None
            self.last_metadata = dict(provider=self.provider, requested_model=self.model,
                model=response.get('model', self.model), usage=response.get('usage', 'unknown'),
                live=self.provider != 'fake')
            return action
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
