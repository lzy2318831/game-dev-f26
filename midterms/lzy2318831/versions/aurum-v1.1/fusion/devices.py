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
DEVICES=dict(guides=GUIDES,
    lanes=[dict(id='left',x_min=24,x_max=70,y=270),dict(id='right',x_min=930,x_max=976,y=270)],
    spinner=dict(id='orbit',x_min=470,x_max=530,y=84))


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
        ledger.events.append(dict(type='rail',rail=rail['id'],ball=ball.id,
            x=ball.x,y=ball.y,t=ledger.time,points=0))
    return True


def process_sensors(ball,previous,devices,ledger):
    now=(ball.x,ball.y)
    for lane in devices['lanes']:
        if crosses_gate(previous,now,lane): ledger.lane(ball.id,lane['id'],ball.x,ball.y)
    spinner=devices['spinner']
    if math.hypot(ball.vx,ball.vy)>=25 and crosses_gate(previous,now,spinner):
        if ball.id not in ledger.spinner_seen:
            ball.vx*=.92; ball.vy*=.92
            ledger.spin(ball.id,ball.x,ball.y)
