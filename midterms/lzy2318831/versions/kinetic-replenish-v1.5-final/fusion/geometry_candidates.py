"""Conservative public geometry only. No engine state, rollout or file access."""
import math
from .geometry import nearest_point, segments_distance


def direction_angle(v):
    return round(math.degrees(math.atan2(v[1],v[0]))) % 360


def minimum_power(distance, terminal_speed=3):
    return max(1, math.ceil((math.sqrt(140*max(0,distance)+terminal_speed**2)-100)/7))


def point(ball): return ball['x'],ball['y']
def unit(a,b):
    d=math.dist(a,b)
    return ((b[0]-a[0])/d,(b[1]-a[1])/d) if d else (0,0)


def pocket_exposure(a,b,observation):
    return any(math.dist(p,nearest_point(p,a,b))<=30 for p in observation['table']['pockets'])


def clear(a,b,observation,exclude=(),device=None,margin=1):
    if any(z['id'] not in exclude and math.dist(point(z),nearest_point(point(z),a,b))<22+margin
           for z in observation['balls']): return False
    if any(math.dist(point(z),nearest_point(point(z),a,b))<z['radius']+11+margin
           for z in observation['bumpers']): return False
    if any(segments_distance(a,b,r['a'],r['b'])<11+r.get('radius',4)+margin
           for r in observation['devices'].get('guides',[])): return False
    for name in ('bridge','scoop'):
        z=observation['devices'].get(name)
        if z and name!=device and math.dist(point(z),nearest_point(point(z),a,b))<=z['radius']+1:
            return False
    return True


def contact(a,angle,target):
    """First radius22 contact along the actual quantized launch ray."""
    v=(math.cos(math.radians(angle)),math.sin(math.radians(angle)))
    return ray_contact(a,v,target)


def ray_contact(a,v,target):
    length=math.hypot(*v)
    v=(v[0]/length,v[1]/length)
    delta=(target[0]-a[0],target[1]-a[1]);along=sum(x*y for x,y in zip(delta,v))
    across=abs(delta[0]*v[1]-delta[1]*v[0])
    if along<=0 or across>=22:return None
    travel=max(0,along-math.sqrt(22**2-across**2))
    return (a[0]+travel*v[0],a[1]+travel*v[1]),travel


def candidates(observation,legal_actions):
    if not legal_actions:return []
    o=observation;objects=[b for b in o['balls'] if b['id']!=0]
    if not objects:return []
    cue=point(next(b for b in o['balls'] if b['id']==0));table=o['table']
    width,height=table['width'],table['height'];rows=[]
    def inside(p):return 11<=p[0]<=width-11 and 11<=p[1]<=height-11
    def add(route,target,angle,distance,energy_distance,risk,reach_energy=None,**extra):
        minimum=minimum_power(distance if reach_energy is None else reach_energy)
        recommended=max(minimum,minimum_power(energy_distance,25))
        # Small margin; never silently clamp an unreachable route into feasibility.
        if route not in ("contact","bank-contact"):
            recommended=max(recommended,math.ceil(((100+7*recommended)*1.04-100)/7))
        if recommended>legal_actions['power_max']:return
        power=max(legal_actions['power_min'],recommended)
        if not legal_actions['angle_min']<=angle<=legal_actions['angle_max']:return
        rows.append(dict(route=route,target=target,angle=angle,power=power,
            minimum_power=minimum,risk=risk,travel=round(distance,1),**extra))

    for obj in sorted(objects,key=lambda b:(math.dist(cue,point(b)),b['id'])):
        target=point(obj);exclude=(0,obj['id'])
        a=direction_angle((target[0]-cue[0],target[1]-cue[1]));hit=contact(cue,a,target)
        if hit and clear(cue,hit[0],o,exclude) and not pocket_exposure(cue,hit[0],o):
            # Reserve modest object movement rather than stopping just short of contact.
            add('contact',obj['id'],a,hit[1],hit[1]+15/.99**2,
                'clear initial contact; pocket/rebound outcome not guaranteed')
        for pocket in table['pockets']:
            length=math.dist(target,pocket)
            if length<1:continue
            u=unit(target,pocket);ghost=(target[0]-22*u[0],target[1]-22*u[1])
            if not inside(ghost):continue
            a=direction_angle((ghost[0]-cue[0],ghost[1]-cue[1]));hit=contact(cue,a,target)
            if hit is None or math.dist(hit[0],ghost)>4:continue
            v=unit(cue,hit[0]);cosine=sum(x*y for x,y in zip(v,u))
            if cosine<.65:continue
            if not clear(cue,hit[0],o,exclude) or pocket_exposure(cue,hit[0],o):continue
            if not clear(target,pocket,o,exclude):continue
            energy=hit[1]+length/(.99*cosine)**2
            # Approximate residual cue tangent; reject an obvious direct scratch line.
            tangent=(v[0]-.99*cosine*u[0],v[1]-.99*cosine*u[1])
            residual=max(0,energy-hit[1])*(tangent[0]**2+tangent[1]**2)*1.15
            n=math.hypot(*tangent)
            end=(hit[0][0]+residual*tangent[0]/n,hit[0][1]+residual*tangent[1]/n) if n else hit[0]
            if pocket_exposure(hit[0],end,o):continue
            add('pot',obj['id'],a,hit[1],energy,
                'ghost-ball estimate; cuts/rebounds/scratch not simulated; pot not guaranteed',pocket=list(pocket))

        # One ordinary cushion bank. Recompute reflection after integer-angle rounding.
        for axis,wall in ((0,11),(0,width-11),(1,11),(1,height-11)):
            # Cushion damps only the normal component (.88), not tangential speed.
            mirror=list(target);mirror[axis]=wall-(target[axis]-wall)/.88
            a=direction_angle((mirror[0]-cue[0],mirror[1]-cue[1]))
            v=[math.cos(math.radians(a)),math.sin(math.radians(a))]
            if abs(v[axis])<1e-8:continue
            t=(wall-cue[axis])/v[axis]
            if t<=1:continue
            bank=(cue[0]+t*v[0],cue[1]+t*v[1])
            if not inside(bank):continue
            v[axis]*=-.88;factor=v[0]**2+v[1]**2
            second=ray_contact(bank,v,target) # Only launch angle is quantized.
            if second is None:continue
            if not clear(cue,bank,o,(0,)) or not clear(bank,second[0],o,exclude):continue
            if pocket_exposure(cue,bank,o) or pocket_exposure(bank,second[0],o):continue
            add('bank-contact',obj['id'],a,t+second[1],t+(second[1]+15/.99**2)/factor,
                'one damped cushion, clear geometric contact; outcome not guaranteed',
                reach_energy=t+second[1]/factor)

    # Portal entry only, not a promise about powered exits or scoring chains.
    for name in ('bridge','scoop'):
        z=o['devices'].get(name)
        if not z or any(r['route'] in ('pot','contact') for r in rows):continue
        target=point(z);a=direction_angle((target[0]-cue[0],target[1]-cue[1]))
        v=(math.cos(math.radians(a)),math.sin(math.radians(a)))
        d=math.dist(cue,target);end=(cue[0]+d*v[0],cue[1]+d*v[1])
        if not inside(end) or math.dist(end,target)>z['radius']-1:continue
        if clear(cue,end,o,(0,),device=name) and not pocket_exposure(cue,end,o):
            add('device',name,a,d,d,'entry path only; powered exit/occupancy/scratch uncertain; not a pot route')

    # Bounded low-energy repositioning: full stopping segment must be unobstructed.
    escape=[]
    for a in range(0,360,15):
        if not legal_actions['angle_min']<=a<=legal_actions['angle_max']:continue
        v=(math.cos(math.radians(a)),math.sin(math.radians(a)))
        for power in (1,5,10,15):
            if not legal_actions['power_min']<=power<=legal_actions['power_max']:continue
            distance=(100+7*power)**2/140+3
            end=(cue[0]+distance*v[0],cue[1]+distance*v[1])
            if inside(end) and clear(cue,end,o,(0,)) and not pocket_exposure(cue,end,o):
                escape.append((math.dist(end,(width/2,height/2)),dict(route='escape',target=None,
                    angle=a,power=power,minimum_power=power,travel=round(distance,1),
                    risk='clear stopping segment; reposition only, no contact or pot claim')))
    if not any(r['route'] in ('pot','contact') for r in rows):
        for _,r in sorted(escape,key=lambda pair:(pair[0],pair[1]['power'],pair[1]['angle']))[:2]:rows.append(r)
    # Preserve diverse choices; model, not sorting, chooses the executed action.
    limits={'pot':5,'contact':5,'bank-contact':3,'device':2,'escape':2};result=[];seen=set()
    for route,limit in limits.items():
        chosen=0
        for row in sorted((r for r in rows if r['route']==route),key=lambda r:(r['power'],r['travel'],r['angle'])):
            key=(row['angle'],row['power'])
            if key in seen:continue
            seen.add(key);row=dict(row,id=len(result)+1);result.append(row);chosen+=1
            if chosen==limit:break
    if not result:
        # Legal minimum-energy choices even when a full collision-free stop is
        # impossible. Rank initial clearance, not hypothetical pots or wins.
        power=legal_actions['power_min'];distance=(100+7*power)**2/140+3
        choices=[]
        for a in range(legal_actions['angle_min'],legal_actions['angle_max']+1):
            v=(math.cos(math.radians(a)),math.sin(math.radians(a)))
            lo,hi=0.,distance
            for _ in range(8):
                middle=(lo+hi)/2;end=(cue[0]+middle*v[0],cue[1]+middle*v[1])
                if inside(end) and clear(cue,end,o,(0,),margin=0) and not pocket_exposure(cue,end,o):lo=middle
                else:hi=middle
            end=(cue[0]+distance*v[0],cue[1]+distance*v[1])
            exposure=pocket_exposure(cue,end,o)
            choices.append(((exposure,-lo,math.dist(end,(width/2,height/2)),a),dict(
                route='fallback-escape',target=None,angle=a,power=power,minimum_power=power,
                travel=round(distance,1),clear_distance=round(lo,1),
                risk='minimum-energy reposition; subsequent contact/device/scratch risk uncertain; no guaranteed clear stop or pot')))
        for _,row in sorted(choices):
            if any(abs((row['angle']-r['angle']+180)%360-180)<15 for r in result):continue
            result.append(dict(row,id=len(result)+1))
            if len(result)==3:break
    return result
