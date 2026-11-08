"""Continuous geometry controller; receives only public snapshots/actions."""
import math


def distance(a,b):
    return math.hypot(a[0]-b[0],a[1]-b[1])


def segment_distance(p,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1]
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/max(1e-12,dx*dx+dy*dy)))
    return distance(p,(a[0]+t*dx,a[1]+t*dy))


def nibble(speed):
    # Invert independent axis equation, choosing 8 for neutral.
    q=max(-7,min(7,round(speed*4)))
    return 8+q if q>=0 else 7+q


def steer(cue,target,interval):
    dx,dy=target[0]-cue[0],target[1]-cue[1]
    speed=min(1.75,max(.25,math.hypot(dx,dy)/max(1,interval)))
    scale=speed/max(1e-9,math.hypot(dx,dy))
    return dict(x=nibble(dx*scale),y=nibble(dy*scale))


def choose(observation,legal_actions):
    if not legal_actions:
        raise ValueError('Inactive player')
    cue_ball=next(b for b in observation['balls'] if b['id']==0)
    cue=(cue_ball['x'],cue_ball['y'])
    objects=[b for b in observation['balls'] if b['id']]
    if not objects:
        return dict(x=8,y=8)  # engine reracks at the next logical frame
    table=observation['table']
    interval=observation['frames_per_step']
    candidates=[]
    for obj in objects:
        pos=(obj['x'],obj['y'])
        blockers=[(b['x'],b['y']) for b in objects if b['id']!=obj['id']]
        for pocket in table['pockets']:
            length=distance(pos,pocket)
            if length<1:
                continue
            ux,uy=(pocket[0]-pos[0])/length,(pocket[1]-pos[1])/length
            ghost=(pos[0]-14*ux,pos[1]-14*uy)
            if not 29<ghost[0]<223 or not 71<ghost[1]<226:
                continue
            blocked=sum(segment_distance(b,cue,ghost)<14 for b in blockers)
            blocked+=sum(segment_distance(b,pos,pocket)<14 for b in blockers)
            approach=distance(cue,ghost)
            cosine=((ghost[0]-cue[0])*ux+(ghost[1]-cue[1])*uy)/max(1,approach)
            cost=approach+length*.65+max(0,1-cosine)*70+blocked*250
            # Reposition behind the object, then drive through it toward pocket.
            if approach<8:
                target=(pos[0]+ux*25,pos[1]+uy*25)
            else:
                target=ghost
            # Avoid steering cue into a pocket during a long open-loop hold.
            action=steer(cue,target,interval)
            vx=((action['x']-7) if action['x']<8 else action['x']-8)/4
            vy=((action['y']-7) if action['y']<8 else action['y']-8)/4
            end=(cue[0]+vx*interval,cue[1]+vy*interval)
            cost+=sum(segment_distance(p,cue,end)<10 for p in table['pockets'])*300
            candidates.append((cost,obj['id'],pocket[0],pocket[1],action))
    if candidates:
        action=min(candidates,key=lambda c:c[:4])[-1]
    else:
        target=min(objects,key=lambda b:(distance(cue,(b['x'],b['y'])),b['id']))
        action=steer(cue,(target['x'],target['y']),interval)
    return action if action in legal_actions else dict(x=8,y=8)


def direct(observation,legal_actions):
    """Secondary nearest-object chase policy; deliberately ignores pockets."""
    cue=next(b for b in observation['balls'] if b['id']==0)
    if not any(b['id'] for b in observation['balls']):
        return dict(x=8,y=8)
    obj=min((b for b in observation['balls'] if b['id']),key=lambda b:distance((cue['x'],cue['y']),(b['x'],b['y'])))
    return steer((cue['x'],cue['y']),(obj['x'],obj['y']),observation['frames_per_step'])


def neutral(observation,legal_actions):
    return dict(x=8,y=8)
