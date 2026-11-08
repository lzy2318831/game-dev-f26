"""Aurum Circuit geometry and passive mechanisms. No rendering dependencies."""
import math
from .geometry import nearest_point,crosses_gate

_LEFT=(('entry',(125,85),(88,125)),('channel',(88,125),(88,330)),
       ('exit',(88,330),(140,365)),('return',(18,380),(76,440)))
GUIDES=[dict(id=f'{side}-{name}',a=[1000-a[0],a[1]] if side=='right' else list(a),
             b=[1000-b[0],b[1]] if side=='right' else list(b),radius=4)
        for side in ('left','right') for name,a,b in _LEFT]
GUIDES += [dict(id='orbit-left',a=[410,52],b=[440,95],radius=4),
           dict(id='orbit-right',a=[590,52],b=[560,95],radius=4)]
# Grand Circuit: mirrored outer orbit / split-return / lower slings.
for side in ('left','right'):
    def point(x,y): return [1000-x,y] if side=='right' else [x,y]
    for name,a,b in (
        ('orbit-rise',(148,150),(148,72)),
        ('orbit-crown',(148,72),(225,35)),
        ('orbit-roof',(225,35),(385,35)),
        ('split-return',(175,110),(175,180)),
        ('lower-bank',(120,455),(245,420))):
        GUIDES.append(dict(id=f'{side}-{name}',a=point(*a),b=point(*b),radius=4))
    triangle=[(175,330),(225,375),(165,400)]
    for i in range(3):
        GUIDES.append(dict(id=f'{side}-sling-{i}',a=point(*triangle[i]),
            b=point(*triangle[(i+1)%3]),radius=4,powered=f'{side}-sling'))
DEVICES=dict(guides=GUIDES,
    lanes=[dict(id='left',x_min=24,x_max=70,y=270),dict(id='right',x_min=930,x_max=976,y=270)],
    spinner=dict(id='orbit',x_min=470,x_max=530,y=84),
    scoop=dict(id='vault',x=805,y=88,radius=17))
DEVICES['lanes'] += [dict(id=name,x_min=lo,x_max=hi,y=y) for name,lo,hi,y in
    [('left-orbit',100,132,110),('right-orbit',868,900,110),
     ('left-inner',190,238,160),('right-inner',762,810,160)]]


def rail_collision(ball,rail,ledger):
    q=nearest_point((ball.x,ball.y),rail['a'],rail['b'])
    dx,dy=ball.x-q[0],ball.y-q[1]
    d=math.hypot(dx,dy); radius=11+rail['radius']
    if d>=radius: return False
    if d>1e-10: nx,ny=dx/d,dy/d
    else:
        tx,ty=rail['b'][0]-rail['a'][0],rail['b'][1]-rail['a'][1]
        length=math.hypot(tx,ty)
        nx,ny=(-ty/length,tx/length) if length else (1,0)
        if ball.vx*nx+ball.vy*ny>0: nx,ny=-nx,-ny
    ball.x,ball.y=q[0]+nx*(radius+.01),q[1]+ny*(radius+.01)
    normal=ball.vx*nx+ball.vy*ny
    if normal<0:
        ball.vx-=1.9*normal*nx; ball.vy-=1.9*normal*ny
        if rail.get('powered'):
            key=(ball.id,rail['powered'])
            if ledger.sling_boosts.get(key,0)<2:
                ball.vx+=180*nx; ball.vy+=180*ny
                ledger.sling_boosts[key]=ledger.sling_boosts.get(key,0)+1
            speed=math.hypot(ball.vx,ball.vy)
            if speed>950: ball.vx*=950/speed; ball.vy*=950/speed
            ledger.device(ball.id,rail['powered'],'sling',ball.x,ball.y,10)
        ledger.events.append(dict(type='rail',rail=rail['id'],ball=ball.id,
            x=ball.x,y=ball.y,t=ledger.time,points=0))
    return True


def process_sensors(ball,previous,devices,ledger):
    scoop=devices.get('scoop')
    if scoop and ball.id not in ledger.scoop_seen and math.hypot(ball.vx,ball.vy)>0:
        dx,dy=ball.x-scoop['x'],ball.y-scoop['y']; d=math.hypot(dx,dy)
        if d<=scoop['radius']:
            nx,ny=(dx/d,dy/d) if d else (0,1)
            ball.x,ball.y=scoop['x']+30*nx,scoop['y']+30*ny
            ball.vx,ball.vy=360*nx,360*ny
            ledger.scoop_seen.add(ball.id)
            ledger.device(ball.id,'vault','scoop',ball.x,ball.y,40)
    now=(ball.x,ball.y)
    for lane in devices['lanes']:
        if crosses_gate(previous,now,lane): ledger.lane(ball.id,lane['id'],ball.x,ball.y)
    spinner=devices['spinner']
    if math.hypot(ball.vx,ball.vy)>=25 and crosses_gate(previous,now,spinner):
        if ball.id not in ledger.spinner_seen:
            ball.vx*=.92; ball.vy*=.92
            ledger.spin(ball.id,ball.x,ball.y)
