"""Bounded public-geometry planning; no engine object or simulation access."""
import math
from pool.baseline import distance,segment_distance


def shot(direction,speed):
    return dict(angle=round(math.degrees(math.atan2(direction[1],direction[0])))%360,
                power=max(1,min(100,math.ceil((speed-100)/7))))


def choose(observation,legal_actions):
    if not legal_actions: raise ValueError('Inactive player')
    cue=next((b['x'],b['y']) for b in observation['balls'] if b['id']==0)
    objects=[b for b in observation['balls'] if b['id']]
    candidates=[]
    for obj in objects:
        target=(obj['x'],obj['y'])
        blockers=[(b['x'],b['y']) for b in objects if b['id']!=obj['id']]
        for pocket in observation['table']['pockets']:
            length=distance(target,pocket)
            if length<1: continue
            ux,uy=(pocket[0]-target[0])/length,(pocket[1]-target[1])/length
            ghost=(target[0]-22*ux,target[1]-22*uy)
            travel=distance(cue,ghost)
            if travel<1 or not 12<ghost[0]<988 or not 12<ghost[1]<488: continue
            dx,dy=(ghost[0]-cue[0])/travel,(ghost[1]-cue[1])/travel
            cosine=dx*ux+dy*uy
            blocked=any(segment_distance(b,cue,ghost)<23 or segment_distance(b,target,pocket)<23 for b in blockers)
            bumper_block=any(segment_distance((b['x'],b['y']),cue,ghost)<41 or segment_distance((b['x'],b['y']),target,pocket)<41 for b in observation['bumpers'])
            if cosine>.3 and not blocked and not bumper_block:
                speed=math.sqrt(140*(travel+length/cosine**2))*1.09
                risk=max(0,1-cosine)*300
                cost=travel+length+risk+max(0,speed-800)*10
                candidates.append((cost,obj['id'],shot((dx,dy),speed)))
            # Bounded bumper-assist search: 16 contact normals per bumper.
            for bumper in observation['bumpers']:
                for k in range(16):
                    a=k*math.tau/16
                    nx,ny=math.cos(a),math.sin(a)
                    q=(bumper['x']+40*nx,bumper['y']+40*ny)
                    first=distance(cue,q)
                    if first<1: continue
                    ix,iy=(q[0]-cue[0])/first,(q[1]-cue[1])/first
                    dot=ix*nx+iy*ny
                    if dot>=-.1: continue
                    ox,oy=450*(ix-1.95*dot*nx)+150*nx,450*(iy-1.95*dot*ny)+150*ny
                    olen=math.hypot(ox,oy)
                    second=distance(q,ghost)
                    if second<1: continue
                    align=(ox*(ghost[0]-q[0])+oy*(ghost[1]-q[1]))/(olen*second)
                    if align<.985: continue
                    if any(segment_distance(b,cue,q)<23 or segment_distance(b,q,ghost)<23 for b in blockers): continue
                    if any(other['id']!=bumper['id'] and (segment_distance((other['x'],other['y']),cue,q)<41 or segment_distance((other['x'],other['y']),q,ghost)<41) for other in observation['bumpers']): continue
                    candidates.append((first+second+length+160*(1-align)-100,obj['id'],shot((ix,iy),min(800,math.sqrt(140*(first+second+length))*1.1))))
    if candidates:
        return min(candidates,key=lambda c:(c[0],c[1],c[2]['angle']))[2]
    target=min(objects,key=lambda b:(distance(cue,(b['x'],b['y'])),b['id']))
    return shot((target['x']-cue[0],target['y']-cue[1]),430)


def direct(observation,legal_actions):
    cue=next(b for b in observation['balls'] if b['id']==0)
    target=min((b for b in observation['balls'] if b['id']),key=lambda b:math.hypot(b['x']-cue['x'],b['y']-cue['y']))
    return shot((target['x']-cue['x'],target['y']-cue['y']),430)
