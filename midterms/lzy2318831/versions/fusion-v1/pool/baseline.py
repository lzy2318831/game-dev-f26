"""Pure public-observation geometry. No engine import or future simulation."""
import math


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def segment_distance(point, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0, min(1, ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / max(1e-12, dx * dx + dy * dy)))
    return distance(point, (a[0] + t * dx, a[1] + t * dy))


def choose(observation, legal_actions):
    if not legal_actions:
        raise ValueError('No legal action')
    balls = observation['balls']
    cue = next((b['x'], b['y']) for b in balls if b['id'] == 0)
    objects = [b for b in balls if b['id']]
    radius = observation['table']['ball_radius']
    candidates = []
    for obj in objects:
        target = (obj['x'], obj['y'])
        blockers = [(b['x'], b['y']) for b in objects if b['id'] != obj['id']]
        for pocket in observation['table']['pockets']:
            length = distance(target, pocket)
            if not length:
                continue
            ux, uy = (pocket[0] - target[0]) / length, (pocket[1] - target[1]) / length
            ghost = (target[0] - 2 * radius * ux, target[1] - 2 * radius * uy)
            if not radius <= ghost[0] <= 1000 - radius or not radius <= ghost[1] <= 500 - radius:
                continue
            travel = distance(cue, ghost)
            if travel < 1:
                continue
            dx, dy = (ghost[0] - cue[0]) / travel, (ghost[1] - cue[1]) / travel
            cosine = dx * ux + dy * uy
            if cosine < .25 or any(segment_distance(b, cue, ghost) < 21 or segment_distance(b, target, pocket) < 21 for b in blockers):
                continue
            # Energy after travel and oblique impact must carry object to pocket.
            needed = math.sqrt(60 * (travel + length / cosine ** 2))
            power = next((i for i, speed in enumerate((180, 300, 420), 1) if speed >= needed * 1.08), 3)
            tangent = (dx - cosine * ux, dy - cosine * uy)
            tangent_len = math.hypot(*tangent)
            risk = 0
            if tangent_len > .05:
                end = (ghost[0] + tangent[0] / tangent_len * 250, ghost[1] + tangent[1] / tangent_len * 250)
                risk = sum(segment_distance(p, ghost, end) < 30 for p in observation['table']['pockets'])
            score = travel + length + 600 * (1 - cosine) + 500 * risk + max(0, needed - 420) * 20
            action = dict(angle=round(math.degrees(math.atan2(dy, dx))) % 360, power=power)
            candidates.append((score, obj['id'], action['angle'], action['power']))
    if candidates:
        _, _, angle, power = min(candidates)
        proposal = dict(angle=angle, power=power)
    else:
        target = min(objects, key=lambda b: (distance(cue, (b['x'], b['y'])), b['id']))
        proposal = dict(angle=round(math.degrees(math.atan2(target['y'] - cue[1], target['x'] - cue[0]))) % 360, power=2)
    return proposal if proposal in legal_actions else legal_actions[0].copy()


def direct(observation, legal_actions):
    """Secondary weak direct-aim opponent, not the primary baseline."""
    cue = next(b for b in observation['balls'] if b['id'] == 0)
    target = min((b for b in observation['balls'] if b['id']), key=lambda b: ((b['x'] - cue['x']) ** 2 + (b['y'] - cue['y']) ** 2, b['id']))
    return dict(angle=round(math.degrees(math.atan2(target['y'] - cue['y'], target['x'] - cue['x']))) % 360, power=2)
