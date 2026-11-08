"""Offline reproducible match runner and trace replay."""
import argparse
import hashlib
import json
import time
from pathlib import Path

from . import VERSION
from .engine import Episode
from .baseline import choose, direct
from .model import ModelFailure

POLICIES = {'baseline': choose, 'direct': direct}


def run_match(seed=101, seats=('baseline', 'baseline'), max_attempts=24,
              deadline_seconds=300, layout=None, players=None, model_call_limit=24):
    policies = dict(POLICIES, **(players or {}))
    if any(s not in policies for s in seats) or len(seats) != 2:
        raise ValueError('Expected two offline policies')
    episode = Episode(layout=layout, max_attempts=max_attempts)
    episode.reset(seed)
    started = time.monotonic()
    trace = dict(version=VERSION, seed=seed, seats=list(seats), layout=episode.layout,
                 max_attempts=max_attempts, model_calls=0, steps=[], call_events=[],
                 limits=dict(attempts=max_attempts, calls=model_call_limit, calls_per_seat=12, deadline_seconds=deadline_seconds))
    seat_calls = dict(p1=0, p2=0)
    history = []
    while not episode.reason:
        if time.monotonic() - started >= deadline_seconds:
            episode.abort('episode_timeout')
            break
        player = episode.active_player
        before = episode.observe(player)
        policy = policies[seats[0 if player == 'p1' else 1]]
        is_model = getattr(policy, 'is_model', False)
        call_start = time.monotonic()
        if is_model:
            if trace['model_calls'] >= model_call_limit or seat_calls[player] >= 12:
                episode.abort('model_call_limit')
                break
            trace['model_calls'] += 1
            seat_calls[player] += 1
            try:
                action = policy.decide(before, episode.legal_actions(player), history,
                                       timeout=max(.001, deadline_seconds - (time.monotonic() - started)))
            except ModelFailure as error:
                episode.abort('episode_timeout' if time.monotonic() - started >= deadline_seconds else str(error))
                trace['failed_seat'] = player
                trace['call_events'].append(dict(player=player, reason=episode.reason,
                    latency_seconds=time.monotonic() - call_start))
                break
        else:
            action = policy(before, episode.legal_actions(player))
        latency = time.monotonic() - call_start
        if time.monotonic() - started >= deadline_seconds:
            episode.abort('episode_timeout')
            break
        result = episode.step(player, action)
        trace['steps'].append(dict(player=player, observation=before, action=action,
            accepted=result['accepted'], events=result['events'], latency_seconds=latency,
            after=episode.observe(player), source='model' if is_model else seats[0 if player == 'p1' else 1],
            model_metadata=policy.last_metadata.copy() if is_model else None))
        history.append(dict(player=player, action=action, events=result['events'], scores=episode.outcome()['scores']))
        if time.monotonic() - started >= deadline_seconds:
            episode.abort('episode_timeout')
    trace['elapsed_seconds'] = time.monotonic() - started
    trace['outcome'] = episode.outcome()
    trace['engine_sha256'] = hashlib.sha256(Path(__file__).with_name('engine.py').read_bytes()).hexdigest()
    return trace


def replay(trace):
    e = Episode(layout=trace['layout'], max_attempts=trace['max_attempts'])
    e.reset(trace['seed'])
    for row in trace['steps']:
        result = e.step(row['player'], row['action'])
        # Normalize tuple/list differences from JSON round trips, but validate
        # acceptance and events independently of the resulting snapshot.
        if (result['accepted'] != row['accepted']
            or result['events'] != row['events']
            or json.dumps(e.observe(row['player']), sort_keys=True) != json.dumps(row['after'], sort_keys=True)):
            raise ValueError('Replay diverged')
    if trace['outcome']['failure'] and not e.reason:
        e.abort(trace['outcome']['reason'])
    return e.outcome()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seed', type=int, default=101)
    p.add_argument('--p1', choices=POLICIES, default='baseline')
    p.add_argument('--p2', choices=POLICIES, default='baseline')
    p.add_argument('--attempts', type=int, default=24)
    p.add_argument('--trace', type=Path)
    p.add_argument('--replay', type=Path)
    args = p.parse_args()
    if args.replay:
        print(json.dumps(replay(json.loads(args.replay.read_text())), indent=2))
        return
    trace = run_match(seed=args.seed, seats=(args.p1, args.p2), max_attempts=args.attempts)
    if args.trace:
        args.trace.parent.mkdir(parents=True, exist_ok=True)
        args.trace.write_text(json.dumps(trace, indent=2), encoding='utf-8')
    print(json.dumps(trace['outcome'], indent=2))
    print('Elapsed seconds:', round(trace['elapsed_seconds'], 3))


if __name__ == '__main__':
    main()
