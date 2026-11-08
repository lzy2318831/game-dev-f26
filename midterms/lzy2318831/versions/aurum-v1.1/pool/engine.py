"""Authoritative deterministic engine. No policy or rendering dependencies."""
from dataclasses import dataclass
import copy
import math

POCKETS = ((0, 0), (500, 0), (1000, 0), (0, 500), (500, 500), (1000, 500))
DEFAULT = ((250, 250), (700, 250), (718, 239), (718, 261), (736, 228), (736, 250), (736, 272))
DT = 1 / 240
FAILURES = {'simulation_limit', 'episode_timeout', 'request_timeout', 'model_call_limit', 'provider_error', 'invalid_model_response'}


@dataclass
class Ball:
    id: int
    x: float
    y: float
    vx: float = 0
    vy: float = 0
    active: bool = True


def tick(balls):
    """Move, capture, reflect x then y, separate/impulse ID pairs, decelerate."""
    pocketed = []
    live = sorted((b for b in balls if b.active), key=lambda b: b.id)
    for b in live:
        b.x += b.vx * DT
        b.y += b.vy * DT
        if any(math.hypot(b.x - x, b.y - y) <= 24 for x, y in POCKETS):
            b.active = False
            b.vx = b.vy = 0
            pocketed.append(b.id)
            continue
        for pos, vel, low, high in [('x', 'vx', 10, 990), ('y', 'vy', 10, 490)]:
            p, v = getattr(b, pos), getattr(b, vel)
            if p < low:
                setattr(b, pos, low)
                if v < 0:
                    setattr(b, vel, -v * .9)
            elif p > high:
                setattr(b, pos, high)
                if v > 0:
                    setattr(b, vel, -v * .9)
    live = [b for b in live if b.active]
    for i, a in enumerate(live):
        for b in live[i + 1:]:
            dx, dy = b.x - a.x, b.y - a.y
            distance = math.hypot(dx, dy)
            if distance > 20:
                continue
            nx, ny = (dx / distance, dy / distance) if distance else (1, 0)
            overlap = 20 - distance
            def room(ball, ux, uy):
                limits = [overlap]
                for pos, direction, low, high in ((ball.x, ux, 10, 990), (ball.y, uy, 10, 490)):
                    if direction > 0:
                        limits.append(max(0, (high - pos) / direction))
                    elif direction < 0:
                        limits.append(max(0, (low - pos) / direction))
                return min(limits)
            room_a, room_b = room(a, -nx, -ny), room(b, nx, ny)
            move_a = min(room_a, max(overlap / 2, overlap - room_b))
            move_b = min(room_b, overlap - move_a)
            a.x -= nx * move_a
            a.y -= ny * move_a
            b.x += nx * move_b
            b.y += ny * move_b
            closing = (a.vx - b.vx) * nx + (a.vy - b.vy) * ny
            if closing > 0:
                a.vx -= closing * nx
                a.vy -= closing * ny
                b.vx += closing * nx
                b.vy += closing * ny
    for b in live:
        speed = math.hypot(b.vx, b.vy)
        remaining = max(0, speed - 30 * DT)
        factor = remaining / speed if speed and remaining >= 1 else 0
        b.vx *= factor
        b.vy *= factor
    return pocketed


class Episode:
    def __init__(self, layout=None, max_attempts=24, max_ticks=4800):
        self.layout = tuple(tuple(p) for p in (layout or DEFAULT))
        if not 2 <= len(self.layout) <= 7:
            raise ValueError('Layout requires a cue and one to six objects')
        if any(len(p) != 2 or not all(math.isfinite(v) for v in p) or not 0 <= p[0] <= 1000 or not 0 <= p[1] <= 500 for p in self.layout):
            raise ValueError('Invalid layout coordinates')
        if max_attempts < 1 or max_ticks < 1:
            raise ValueError('Limits must be positive')
        self.max_attempts, self.max_ticks = max_attempts, max_ticks
        self.reset()

    def reset(self, seed=None):
        self.seed = seed  # deterministic layouts: recorded, not consumed by physics
        self.balls = [Ball(i, *p) for i, p in enumerate(self.layout)]
        self.active_player = 'p1'
        self.scores = dict(p1=0, p2=0)
        self.scratches = dict(p1=0, p2=0)
        self.invalid = dict(p1=0, p2=0)
        self.attempts = 0
        self.reason = ''
        self.events = []
        return self.observe('p1')

    @staticmethod
    def _check(player):
        if player not in ('p1', 'p2'):
            raise ValueError('Unknown player')

    def observe(self, player_id):
        self._check(player_id)
        return copy.deepcopy(dict(player_id=player_id, active_player=self.active_player,
            table=dict(width=1000, height=500, ball_radius=10, pocket_radius=24, pockets=POCKETS),
            balls=[dict(id=b.id, x=b.x, y=b.y) for b in self.balls if b.active],
            scores=self.scores, attempts_remaining=max(0, self.max_attempts - self.attempts),
            scratches=self.scratches, invalid_actions=self.invalid, last_events=self.events,
            status='terminal' if self.reason else 'ongoing'))

    def legal_actions(self, player_id):
        self._check(player_id)
        if self.reason or player_id != self.active_player:
            return []
        return [dict(angle=a, power=p) for a in range(360) for p in (1, 2, 3)]

    @staticmethod
    def valid(action):
        return (isinstance(action, dict) and set(action) == {'angle', 'power'}
                and type(action['angle']) is int and 0 <= action['angle'] <= 359
                and type(action['power']) is int and action['power'] in (1, 2, 3))

    def abort(self, reason):
        if reason not in FAILURES:
            raise ValueError('Unknown execution failure')
        if not self.reason:
            self.reason = reason

    def _finish_attempt(self):
        self.active_player = 'p2' if self.active_player == 'p1' else 'p1'
        if not any(b.active and b.id for b in self.balls):
            self.reason = 'table_cleared'
        elif self.attempts >= self.max_attempts:
            self.reason = 'attempt_limit'

    def step(self, player_id, action, frame_callback=None):
        self._check(player_id)
        if self.reason or player_id != self.active_player:
            return dict(accepted=False, events=[], observation=self.observe(player_id))
        self.attempts += 1
        self.events = []
        if not self.valid(action):
            self.invalid[player_id] += 1
            self.events = [dict(type='invalid_action')]
            self._finish_attempt()
            return dict(accepted=False, events=copy.deepcopy(self.events), observation=self.observe(player_id))
        cue = self.balls[0]
        rad = math.radians(action['angle'])
        speed = (180, 300, 420)[action['power'] - 1]
        cue.vx, cue.vy = math.cos(rad) * speed, math.sin(rad) * speed
        pocketed = []
        for n in range(self.max_ticks):
            pocketed.extend(tick(self.balls))
            if frame_callback and n % 8 == 0:
                frame_callback(self.observe(player_id))
            if all(not b.active or (b.vx == 0 and b.vy == 0) for b in self.balls):
                break
        else:
            self.abort('simulation_limit')
            return dict(accepted=True, events=[dict(type='simulation_limit')], observation=self.observe(player_id))
        self.events = [dict(type='pocket', ball=i) for i in pocketed]
        if 0 in pocketed:
            self.scratches[player_id] += 1
            self.events.append(dict(type='scratch'))
            for x in (250, 200, 150, 100, 50):
                for y in (250, 200, 300, 150, 350, 100, 400, 50, 450):
                    if all(not b.active or b.id == 0 or math.hypot(b.x - x, b.y - y) >= 21 for b in self.balls):
                        cue.x, cue.y, cue.active = x, y, True
                        break
                if cue.active:
                    break
        else:
            self.scores[player_id] += len(pocketed)
        self._finish_attempt()
        return dict(accepted=True, events=copy.deepcopy(self.events), observation=self.observe(player_id))

    def outcome(self):
        terminal = bool(self.reason)
        failure = self.reason in FAILURES
        winner = None
        if terminal and not failure and self.scores['p1'] != self.scores['p2']:
            winner = max(self.scores, key=self.scores.get)
        return copy.deepcopy(dict(status='terminal' if terminal else 'ongoing', reason=self.reason,
            scores=self.scores, winner=winner, draw=terminal and not failure and winner is None,
            failure=failure, attempts=self.attempts, invalid_actions=self.invalid, scratches=self.scratches))
