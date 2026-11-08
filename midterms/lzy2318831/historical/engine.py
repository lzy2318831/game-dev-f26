"""Continuous-control arcade rules; no ROMs, assembly or asset tables included.

Coordinates are screen-space ball centers: x=256-H, y=V-7. Numerical
approximations and historical evidence are specified in RULES.md H1-H10.
"""
from dataclasses import dataclass
from copy import deepcopy
import math

FPS = 60
DIAMETER = 14
POCKETS = ((27,69),(127,65),(225,69),(27,228),(127,232),(225,228))
FAILURES = {'frame_limit','step_limit','model_call_limit','episode_timeout',
            'request_timeout','provider_error','invalid_model_response'}


def quantize(value):
    return round(value * 256) / 256


def axis_velocity(value):
    """4-bit axis -> pixels/frame, including the two neutral center values."""
    if type(value) is not int or not 0 <= value <= 15:
        raise ValueError('Axis must be an integer 0..15')
    return ((value - 7) if value < 8 else (value - 8)) / 4


@dataclass
class Ball:
    id: int
    x: float
    y: float
    vx: float = 0
    vy: float = 0
    active: bool = True


def boundary(ball):
    """Threshold mouths and perfect sign reversal, in screen coordinates."""
    x,y = ball.x,ball.y
    if y < 69 or y >= 228:
        if x > 221 or x <= 33:
            return True
        if 119 < x <= 134:
            return y < 65 or y >= 232
        if (y < 69 and ball.vy < 0) or (y >= 228 and ball.vy > 0):
            ball.vy = -ball.vy
    elif x > 225 or x <= 27:
        if y < 75 or y >= 222:
            return True
        if (x > 225 and ball.vx > 0) or (x <= 27 and ball.vx < 0):
            ball.vx = -ball.vx
    return False


def physics_frame(balls, frame):
    """One 60-Hz logical frame. Quantized independent normal-impulse model.

    Moving objects update descending ID, cue last. Boundary check precedes
    movement; each unordered pair transfers at most once per frame. Unlike
    the original, normals come from math, not packed historical lookup data.
    """
    pocketed, touched = [], set()
    ordered = sorted((b for b in balls if b.active),key=lambda b:-b.id)
    for a in ordered:
        if not a.active or (a.vx == 0 and a.vy == 0):
            continue
        if boundary(a):
            a.active = False
            a.vx = a.vy = 0
            pocketed.append(a.id)
            if a.id == 0:
                break
            continue
        a.x, a.y = quantize(a.x+a.vx), quantize(a.y+a.vy)
        if (frame ^ a.id) & 3 == 0:
            # Truncate toward rest: rounding can trap low speeds forever.
            a.vx, a.vy = math.trunc(a.vx*248)/256, math.trunc(a.vy*248)/256
            if abs(a.vx) < 1/64:
                a.vx=0
            if abs(a.vy) < 1/64:
                a.vy=0
        for b in ordered:
            pair=tuple(sorted((a.id,b.id)))
            if a is b or not b.active or pair in touched:
                continue
            dx,dy=b.x-a.x,b.y-a.y
            distance=math.hypot(dx,dy)
            if abs(dx)>13 or abs(dy)>13 or distance>DIAMETER:
                continue
            touched.add(pair)
            theta=round(math.atan2(dy,dx)*32/math.pi)*math.pi/32 if distance else 0
            nx,ny=math.cos(theta),math.sin(theta)
            closing=(a.vx-b.vx)*nx+(a.vy-b.vy)*ny
            if closing<=0:
                continue
            a.vx,a.vy=quantize(a.vx-closing*nx),quantize(a.vy-closing*ny)
            b.vx,b.vy=quantize(b.vx+closing*nx),quantize(b.vy+closing*ny)
            # Small independent overlap correction; arcade code uses contacts.
            correction=max(0,DIAMETER-distance)/2
            a.x,a.y=quantize(a.x-nx*correction),quantize(a.y-ny*correction)
            b.x,b.y=quantize(b.x+nx*correction),quantize(b.y+ny*correction)
    return pocketed


class Episode:
    def __init__(self,heats=2,extended=True,frames_per_step=64,max_steps=40000,max_frames=40000,scenario='opening'):
        if type(heats) is not int or not 2<=heats<=5:
            raise ValueError('Choose 2..5 heats')
        if type(extended) is not bool:
            raise ValueError('Extended must be boolean')
        if any(type(v) is not int or v<1 for v in (frames_per_step,max_steps,max_frames)):
            raise ValueError('Positive integer limits required')
        if scenario not in ('opening','scattered','danger'):
            raise ValueError('Unknown starting situation')
        self.scenario=scenario
        self.heats,self.extended,self.frames_per_step=heats,extended,frames_per_step
        self.max_steps,self.max_frames=max_steps,max_frames
        self.reset()

    def _rack(self,initial=False):
        # Independent regular triangle. Do not copy original BINIT bytes.
        positions=[(48,152)]
        for row in range(5):
            positions.extend((144+14*row,quantize(152+(column-row/2)*15)) for column in range(row+1))
        if initial and self.scenario!='opening':
            positions=[(48,152)]+[(96+26*column,105+40*row) for row in range(3) for column in range(5)]
            if self.scenario=='danger':
                positions[0]=(127,84)
                positions[2]=(127,105)
        if self.active_player=='p2':
            positions=[(256-x,y) for x,y in positions]
        self.balls=[Ball(i,*p) for i,p in enumerate(positions)]

    def reset(self,seed=None):
        self.seed=seed  # Fixed rack; no global RNG or hidden randomized targets.
        self.active_player='p1'
        self.heat=1
        self.timer=30
        self.frames=self.steps=0
        self.reason=''
        self.scores=dict(p1=0,p2=0)
        self.pockets=dict(p1=0,p2=0)
        self.scratches=dict(p1=0,p2=0)
        self.invalid=dict(p1=0,p2=0)
        self.clearances=dict(p1=0,p2=0)
        self.bonus_awarded=False
        self.events=[]
        self._rack(initial=True)
        return self.observe('p1')

    @staticmethod
    def _check(player):
        if player not in ('p1','p2'):
            raise ValueError('Unknown player')

    @staticmethod
    def valid(action):
        return isinstance(action,dict) and set(action)=={'x','y'} and all(type(v) is int and 0<=v<=15 for v in action.values())

    def legal_actions(self,player_id):
        self._check(player_id)
        if self.reason or player_id!=self.active_player:
            return []
        return [dict(x=x,y=y) for x in range(16) for y in range(16)]

    def observe(self,player_id):
        self._check(player_id)
        return deepcopy(dict(player_id=player_id,active_player=self.active_player,
            table=dict(width=256,height=256,left=27,right=225,top=69,bottom=228,
                       ball_radius=7,pockets=POCKETS),
            balls=[dict(id=b.id,x=b.x,y=b.y,vx=b.vx,vy=b.vy) for b in self.balls if b.active],
            scores=self.scores,timer=self.timer,heat=self.heat,heats=self.heats,
            extended=self.extended,bonus_awarded=self.bonus_awarded,
            scratches=self.scratches,clearances=self.clearances,invalid_actions=self.invalid,
            last_events=self.events,frames_per_step=self.frames_per_step,
            status='terminal' if self.reason else 'ongoing'))

    def _end_segment(self,cause):
        old=self.active_player
        self.events.append(dict(type='segment_end',player=old,reason=cause,heat=self.heat))
        if old=='p2' and self.heat==self.heats:
            self.reason='heats_complete'
            return
        if old=='p1':
            self.active_player='p2'
        else:
            self.active_player='p1'
            self.heat+=1
        self.timer=30
        self.bonus_awarded=False
        self._rack(initial=True)

    def abort(self,reason):
        if reason not in FAILURES:
            raise ValueError('Unknown failure')
        if not self.reason:
            self.reason=reason

    def _frame(self,action):
        self.frames+=1
        if self.frames%64==0:
            if self.timer==0:
                self._end_segment('timer_expired')
                return True
            self.timer-=1
        if not any(b.active for b in self.balls[1:]):
            self.clearances[self.active_player]+=1
            self.events.append(dict(type='rerack',player=self.active_player))
            if self.extended and not self.bonus_awarded:
                self.timer+=15
                self.bonus_awarded=True
                self.events.append(dict(type='bonus',units=15))
            self._rack()
        pocketed=physics_frame(self.balls,self.frames)
        for ball_id in pocketed:
            self.events.append(dict(type='pocket',ball=ball_id,player=self.active_player))
            if ball_id:
                self.scores[self.active_player]=(self.scores[self.active_player]+1)%100
                self.pockets[self.active_player]+=1
            else:
                self.scratches[self.active_player]+=1
                self._end_segment('scratch')
                return True
        cue=self.balls[0]
        cue.vx,cue.vy=axis_velocity(action['x']),axis_velocity(action['y'])
        return False

    def step(self,player_id,action):
        self._check(player_id)
        if self.reason or player_id!=self.active_player:
            return dict(accepted=False,events=[],frames_advanced=0,observation=self.observe(player_id))
        self.steps+=1
        self.events=[]
        accepted=self.valid(action)
        if not accepted:
            self.invalid[player_id]+=1
            self.events.append(dict(type='invalid_action',policy='refused_no_simulation'))
            if self.steps>=self.max_steps:
                self.abort('step_limit')
            return dict(accepted=False,events=deepcopy(self.events),frames_advanced=0,observation=self.observe(player_id))
        start=self.frames
        for _ in range(self.frames_per_step):
            changed=self._frame(action)
            if self.frames>=self.max_frames:
                self.abort('frame_limit')
            if changed or self.reason:
                break
        if self.steps>=self.max_steps:
            self.abort('step_limit')
        return dict(accepted=accepted,events=deepcopy(self.events),frames_advanced=self.frames-start,observation=self.observe(player_id))

    def outcome(self):
        terminal=bool(self.reason)
        failure=self.reason in FAILURES
        winner=None
        if terminal and not failure and self.scores['p1']!=self.scores['p2']:
            winner=max(self.scores,key=self.scores.get)
        return deepcopy(dict(status='terminal' if terminal else 'ongoing',reason=self.reason,
            failure=failure,winner=winner,draw=terminal and not failure and winner is None,
            scores=self.scores,total_pockets=self.pockets,scratches=self.scratches,
            clearances=self.clearances,invalid_actions=self.invalid,frames=self.frames,steps=self.steps,
            heat=self.heat,heats=self.heats))
