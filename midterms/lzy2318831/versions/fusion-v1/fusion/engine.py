"""Authoritative fixed-step game; deliberately independent of browser/rendering."""
from dataclasses import dataclass
from copy import deepcopy
import math

DT=1/240
RADIUS=11
POCKETS=((0,0),(500,0),(1000,0),(0,500),(500,500),(1000,500))
BUMPERS=({'id':0,'x':465,'y':165,'radius':29},{'id':1,'x':555,'y':335,'radius':29})
DEFAULT=((230,250),(700,250),(721,238),(721,262),(742,226),(742,250),(742,274))
FAILURES={'simulation_limit','episode_timeout','request_timeout','provider_error','invalid_model_response','model_call_limit'}


@dataclass
class Ball:
    id:int
    x:float
    y:float
    vx:float=0
    vy:float=0
    active:bool=True


class ShotLedger:
    def __init__(self):
        self.pots=[]
        self.scratch=False
        self.cue_bumpers=set()
        self.bumper_points=0
        self.assisted=False
        self.boosts={}
        self.contacts=set()
        self.events=[]
        self.time=0

    def bumper(self,ball,bumper,x,y):
        points=0
        if ball==0 and bumper not in self.cue_bumpers:
            self.cue_bumpers.add(bumper)
            self.bumper_points+=15
            points=15
        self.events.append(dict(type='bumper',ball=ball,bumper=bumper,x=x,y=y,points=points,t=self.time))

    def pocket(self,ball,x,y):
        if ball==0:
            self.scratch=True
        else:
            self.pots.append(ball)
            self.assisted |= bool(self.cue_bumpers)
        self.events.append(dict(type='scratch' if ball==0 else 'pocket',ball=ball,x=x,y=y,t=self.time))

    def breakdown(self):
        return dict(pots=100*len(self.pots),bumpers=self.bumper_points,
            multi=50*max(0,len(self.pots)-1),assisted=50 if self.assisted else 0,
            voided=self.scratch)

    def score(self):
        b=self.breakdown()
        return 0 if self.scratch else b['pots']+b['bumpers']+b['multi']+b['assisted']


def capture(ball,ledger):
    if ball.active and any(math.hypot(ball.x-x,ball.y-y)<=29 for x,y in POCKETS):
        ball.active=False
        ball.vx=ball.vy=0
        ledger.pocket(ball.id,ball.x,ball.y)
        return True
    return not ball.active


def constrain(ball):
    for pos,vel,low,high in (('x','vx',11,989),('y','vy',11,489)):
        p,v=getattr(ball,pos),getattr(ball,vel)
        if p<low:
            setattr(ball,pos,low)
            if v<0: setattr(ball,vel,-v*.88)
        elif p>high:
            setattr(ball,pos,high)
            if v>0: setattr(ball,vel,-v*.88)


def tick(balls,bumpers,ledger):
    live=sorted((b for b in balls if b.active),key=lambda b:b.id)
    for b in live:
        b.x+=b.vx*DT
        b.y+=b.vy*DT
        if capture(b,ledger): continue
        constrain(b)
        for bumper in bumpers:
            dx,dy=b.x-bumper['x'],b.y-bumper['y']
            d=math.hypot(dx,dy)
            r=RADIUS+bumper['radius']
            key=(b.id,bumper['id'])
            if d>r+1:
                ledger.contacts.discard(key)
            if d>r: continue
            nx,ny=(dx/d,dy/d) if d else (1,0)
            b.x,b.y=bumper['x']+nx*(r+.01),bumper['y']+ny*(r+.01)
            normal=b.vx*nx+b.vy*ny
            if normal<0:
                b.vx-=1.95*normal*nx
                b.vy-=1.95*normal*ny
                if key not in ledger.contacts:
                    if ledger.boosts.get(key,0)<2:
                        b.vx+=150*nx
                        b.vy+=150*ny
                        ledger.boosts[key]=ledger.boosts.get(key,0)+1
                    ledger.bumper(b.id,bumper['id'],b.x,b.y)
            ledger.contacts.add(key)
            speed=math.hypot(b.vx,b.vy)
            if speed>950:
                b.vx*=950/speed
                b.vy*=950/speed
    live=[b for b in live if b.active]
    for i,a in enumerate(live):
        for b in live[i+1:]:
            dx,dy=b.x-a.x,b.y-a.y
            distance=math.hypot(dx,dy)
            if distance>22: continue
            nx,ny=(dx/distance,dy/distance) if distance else (1,0)
            overlap=22-distance
            def room(ball,ux,uy):
                values=[overlap]
                for pos,direction,lo,hi in ((ball.x,ux,11,989),(ball.y,uy,11,489)):
                    if direction>0: values.append(max(0,(hi-pos)/direction))
                    elif direction<0: values.append(max(0,(lo-pos)/direction))
                return min(values)
            ra,rb=room(a,-nx,-ny),room(b,nx,ny)
            ma=min(ra,max(overlap/2,overlap-rb))
            mb=min(rb,overlap-ma)
            a.x-=nx*ma; a.y-=ny*ma
            b.x+=nx*mb; b.y+=ny*mb
            closing=(a.vx-b.vx)*nx+(a.vy-b.vy)*ny
            if closing>0:
                impulse=.99*closing
                a.vx-=impulse*nx; a.vy-=impulse*ny
                b.vx+=impulse*nx; b.vy+=impulse*ny
    for b in live:
        if capture(b,ledger): continue
        constrain(b)
        speed=math.hypot(b.vx,b.vy)
        remaining=max(0,speed-70*DT)
        factor=remaining/speed if speed and remaining>=3 else 0
        b.vx*=factor; b.vy*=factor


class Episode:
    def __init__(self,layout=None,max_ticks=4800):
        self.layout=tuple(tuple(p) for p in (layout or DEFAULT))
        if not 2<=len(self.layout)<=7 or type(max_ticks) is not int or max_ticks<1:
            raise ValueError('Cue plus 1..6 objects and positive tick cap required')
        if any(len(p)!=2 or any(type(v) not in (int,float) or not math.isfinite(v) for v in p) or not 0<=p[0]<=1000 or not 0<=p[1]<=500 for p in self.layout):
            raise ValueError('Invalid layout')
        self.max_ticks=max_ticks
        self.reset()

    def reset(self,seed=None):
        self.seed=seed
        self.balls=[Ball(i,*p) for i,p in enumerate(self.layout)]
        self.bumpers=deepcopy(list(BUMPERS))
        self.active_player='p1'
        self.scores=dict(p1=0,p2=0)
        self.shots_remaining=dict(p1=6,p2=6)
        self.scratches=dict(p1=0,p2=0)
        self.invalid=dict(p1=0,p2=0)
        self.metrics={p:dict(pots=0,bumper_points=0,combo_points=0) for p in ('p1','p2')}
        self.shots=0
        self.reason=''
        self.events=[]
        self.last_shot=None
        return self.observe('p1')

    @staticmethod
    def _check(player):
        if player not in ('p1','p2'): raise ValueError('Unknown player')

    @staticmethod
    def valid(action):
        return isinstance(action,dict) and set(action)=={'angle','power'} and type(action['angle']) is int and 0<=action['angle']<360 and type(action['power']) is int and 1<=action['power']<=100

    def legal_actions(self,player_id):
        self._check(player_id)
        if self.reason or player_id!=self.active_player: return []
        return dict(angle_min=0,angle_max=359,power_min=1,power_max=100)

    def observe(self,player_id):
        self._check(player_id)
        return deepcopy(dict(player_id=player_id,active_player=self.active_player,
            table=dict(width=1000,height=500,ball_radius=11,pocket_radius=29,pockets=POCKETS),
            balls=[dict(id=b.id,x=b.x,y=b.y) for b in self.balls if b.active],bumpers=self.bumpers,
            scores=self.scores,shots_remaining=self.shots_remaining,scratches=self.scratches,
            invalid_actions=self.invalid,last_events=self.events,last_shot=self.last_shot,
            status='terminal' if self.reason else 'ongoing'))

    def abort(self,reason):
        if reason not in FAILURES: raise ValueError('Unknown failure')
        if not self.reason: self.reason=reason

    def _finish(self):
        self.active_player='p2' if self.active_player=='p1' else 'p1'
        if not any(b.active and b.id for b in self.balls): self.reason='table_cleared'
        elif self.shots>=12: self.reason='shots_exhausted'

    def _respot(self):
        cue=self.balls[0]
        for x in (230,180,130,80):
            for y in (250,200,300,150,350,100,400):
                if all(not b.active or b.id==0 or math.hypot(b.x-x,b.y-y)>=23 for b in self.balls) and all(math.hypot(b['x']-x,b['y']-y)>=42 for b in self.bumpers):
                    cue.x,cue.y,cue.vx,cue.vy,cue.active=x,y,0,0,True
                    return
        raise RuntimeError('Respot candidates exhausted')

    def _frame(self,t):
        return dict(t=t,balls=[dict(id=b.id,x=b.x,y=b.y) for b in self.balls if b.active])

    def step(self,player_id,action,record_frames=False):
        self._check(player_id)
        if self.reason or player_id!=self.active_player:
            return dict(accepted=False,events=[],frames=[],observation=self.observe(player_id))
        self.shots+=1
        self.shots_remaining[player_id]-=1
        self.events=[]
        if not self.valid(action):
            self.invalid[player_id]+=1
            self.last_shot=dict(player=player_id,points=0,foul=False,invalid=True)
            self._finish()
            return dict(accepted=False,events=[],frames=[],observation=self.observe(player_id))
        ledger=ShotLedger()
        frames=[self._frame(0)] if record_frames else []
        cue=self.balls[0]
        angle=math.radians(action['angle'])
        speed=100+7*action['power']
        cue.vx,cue.vy=math.cos(angle)*speed,math.sin(angle)*speed
        for n in range(self.max_ticks):
            ledger.time=(n+1)*DT
            tick(self.balls,self.bumpers,ledger)
            if record_frames and n%4==3: frames.append(self._frame(ledger.time))
            if all(not b.active or (b.vx==0 and b.vy==0) for b in self.balls): break
        else:
            self.abort('simulation_limit')
        if record_frames: frames.append(self._frame(ledger.time))
        self.events=ledger.events
        if not self.reason:
            points=ledger.score()
            self.scores[player_id]+=points
            if ledger.scratch:
                self.scratches[player_id]+=1
                self._respot()
            else:
                self.metrics[player_id]['pots']+=len(ledger.pots)
                self.metrics[player_id]['bumper_points']+=ledger.bumper_points
                self.metrics[player_id]['combo_points']+=ledger.breakdown()['multi']+ledger.breakdown()['assisted']
            self.last_shot=dict(player=player_id,points=points,foul=ledger.scratch,
                invalid=False,breakdown=ledger.breakdown(),potted=ledger.pots)
            self._finish()
        return dict(accepted=True,events=deepcopy(self.events),frames=frames,
            duration=ledger.time,observation=self.observe(player_id),outcome=self.outcome())

    def outcome(self):
        terminal=bool(self.reason)
        failure=self.reason in FAILURES
        winner=None
        if terminal and not failure and self.scores['p1']!=self.scores['p2']:
            winner=max(self.scores,key=self.scores.get)
        return deepcopy(dict(status='terminal' if terminal else 'ongoing',reason=self.reason,
            winner=winner,draw=terminal and not failure and winner is None,failure=failure,
            scores=self.scores,shots=self.shots,shots_remaining=self.shots_remaining,
            scratches=self.scratches,invalid_actions=self.invalid,metrics=self.metrics))
