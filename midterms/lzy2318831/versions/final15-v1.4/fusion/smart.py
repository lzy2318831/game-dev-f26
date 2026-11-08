"""Deterministic public-state physics planner. Not an LLM or the baseline.

Budget is work, never a hardware-dependent time cutoff: 24 proposals and
40,000 authoritative ticks. Incomplete predictions cannot beat settled ones.
"""
from copy import deepcopy
import math
import time
from .engine import Ball, ShotLedger, tick, DT
from .baseline import choose as geometric

MAX_CANDIDATES=24
MAX_TICKS=40000
PREVIEW_TICKS=480
SHOT_TICKS=9600


class Simulation:
    def __init__(self,observation,action):
        self.balls=[Ball(b['id'],b['x'],b['y']) for b in observation['balls']]
        self.bumpers=deepcopy(observation['bumpers'])
        self.devices=deepcopy(observation['devices'])
        self.ledger=ShotLedger()
        self.ticks=0
        self.done=False
        cue=next(b for b in self.balls if b.id==0)
        a=math.radians(action['angle']); speed=100+7*action['power']
        cue.vx,cue.vy=math.cos(a)*speed,math.sin(a)*speed

    def advance(self,count):
        before=self.ticks
        for _ in range(min(count,SHOT_TICKS-self.ticks)):
            if self.done: break
            self.ticks+=1; self.ledger.time=self.ticks*DT
            tick(self.balls,self.bumpers,self.ledger,self.devices)
            self.done=all(not b.active or (b.vx==0 and b.vy==0) for b in self.balls)
        return self.ticks-before

    def result(self):
        return dict(points=self.ledger.score(),foul=self.ledger.scratch,
                    potted=list(self.ledger.pots),settled=self.done,ticks=self.ticks)


def predict(observation,action):
    simulation=Simulation(observation,action)
    simulation.advance(SHOT_TICKS)
    return simulation.result()


def candidates(o,legal):
    """Round-robin coverage of direct, combo, bank, device and exploratory shots."""
    first=geometric(o,legal)
    cue=next((b['x'],b['y']) for b in o['balls'] if b['id']==0)
    objects=[b for b in o['balls'] if b['id']]
    def aim(p,power):
        return dict(angle=round(math.degrees(math.atan2(p[1]-cue[1],p[0]-cue[0])))%360,power=power)
    ghosts=[]
    for b in objects:
        for p in o['table']['pockets']:
            dx,dy=p[0]-b['x'],p[1]-b['y']; d=math.hypot(dx,dy)
            if d<1: continue
            target=(b['x']-22*dx/d,b['y']-22*dy/d)
            approach=math.dist(cue,target)
            if approach<1: continue
            cosine=((target[0]-cue[0])*dx+(target[1]-cue[1])*dy)/(approach*d)
            if cosine>.15:
                ghosts.append((approach+d+300*(1-cosine),target))
    ghosts.sort(key=lambda x:(x[0],x[1]))
    nearest=sorted(objects,key=lambda b:(math.dist(cue,(b['x'],b['y'])),b['id']))
    devices=o['devices']
    points=[(devices['bridge']['x'],devices['bridge']['y']),
            (devices['scoop']['x'],devices['scoop']['y']), (500,84),
            (327,140),(670,140),(200,350),(800,350)]
    # Explicit category quotas ensure every mechanism is actually considered.
    proposals=[first]
    proposals += [aim(p,power) for _,p in ghosts[:2] for power in (65,100)]
    proposals += [aim((b['x'],b['y']),85) for b in nearest[:2]]
    proposals += [aim((nearest[0]['x'], -nearest[0]['y'] if side==0 else 1000-nearest[0]['y']),85) for side in (0,1)]
    proposals += [aim(p,95 if i%2 else 65) for i,p in enumerate(points)]
    proposals += [dict(angle=a,power=85) for a in range(0,360,60)]
    proposals += [dict(angle=first['angle'],power=p) for p in (45,100)]
    out=[]; seen=set()
    for action in proposals:
        key=(action['angle'],action['power'])
        if key not in seen: out.append(action); seen.add(key)
    return out[:MAX_CANDIDATES]


def utility(s,o):
    l=s.ledger; player=o['active_player']; other='p2' if player=='p1' else 'p1'
    value=l.score()-180*l.scratch+15*len(l.pots)*(not l.scratch)
    if s.done:
        terminal=not any(b.active and b.id for b in s.balls) or sum(o['shots_remaining'].values())==1
        if terminal:
            margin=o['scores'][player]+l.score()-o['scores'][other]
            value+=10000 if margin>0 else 5000 if margin==0 else -10000
        cue=next(b for b in s.balls if b.id==0)
        if cue.active:
            # A small positional tiebreak, subordinate to one scoring point.
            targets=[math.hypot(cue.x-b.x,cue.y-b.y) for b in s.balls if b.active and b.id]
            if targets: value-=min(targets)/10000
    return value


def plan(observation,legal_actions):
    if not legal_actions or observation['player_id']!=observation['active_player']:
        raise ValueError('Inactive Smart AI')
    start=time.perf_counter()
    actions=candidates(observation,legal_actions)
    simulations=[]; used=0
    for action in actions:
        s=Simulation(observation,action)
        used+=s.advance(PREVIEW_TICKS)
        simulations.append(s)
    # Always resolve original Geometric proposal first, guaranteeing a fair
    # same-position reference when it settles. Then resolve promising previews.
    order=[0]+sorted(range(1,len(actions)),key=lambda i:(-utility(simulations[i],observation),i))
    for i in order:
        if used>=MAX_TICKS: break
        used+=simulations[i].advance(min(SHOT_TICKS,MAX_TICKS-used))
    settled=[i for i,s in enumerate(simulations) if s.done]
    winner=max(settled,key=lambda i:(utility(simulations[i],observation),-i)) if settled else 0
    return actions[winner],dict(candidates=len(actions),ticks=used,
        settled=len(settled),seconds=time.perf_counter()-start,
        prediction=simulations[winner].result(),simulator_access=True)


def choose(observation,legal_actions):
    return plan(observation,legal_actions)[0]
