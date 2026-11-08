"""Pure deterministic placement for the bounded between-shot rule."""
import math
from .geometry import nearest_point

THRESHOLD=8
BATCH=5
MAX_EVENTS=2
ROWS=(250,222,278,306,194,334,166,362,138,390)


def placement_clear(point,balls,bumpers,devices):
    x,y=point
    if not 23<=x<=977 or not 23<=y<=477: return False
    if any(math.dist(point,(b['x'],b['y']))<23 for b in balls): return False
    if any(math.dist(point,(b['x'],b['y']))<b['radius']+12 for b in bumpers): return False
    if any(math.dist(point,p)<41 for p in ((0,0),(500,0),(1000,0),(0,500),(500,500),(1000,500))): return False
    if any(math.dist(point,nearest_point(point,r['a'],r['b']))<16 for r in devices['guides']): return False
    # Do not place inside a closed sling even if clear of each edge.
    for side in ('left-sling','right-sling'):
        vertices=[r['a'] for r in devices['guides'] if r.get('powered')==side]
        if len(vertices)==3:
            cross=[(b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0])
                   for a,b in zip(vertices,vertices[1:]+vertices[:1])]
            if all(v>=0 for v in cross) or all(v<=0 for v in cross): return False
    for name in ('scoop','bridge'):
        device=devices[name]
        if math.dist(point,(device['x'],device['y']))<device['radius']+12: return False
        if 'exit' in device and math.dist(point,device['exit'])<23: return False
    for gate in devices['lanes']+[devices['spinner']]:
        if math.dist(point,nearest_point(point,(gate['x_min'],gate['y']),(gate['x_max'],gate['y'])))<12: return False
    return True


def spawn_batch(balls,bumpers,devices):
    """Return all five placements or none. Never mutate the supplied state."""
    active=[dict(id=b.id,x=b.x,y=b.y) for b in balls if b.active]
    used={b['id'] for b in active}
    identifiers=[i for i in range(1,16) if i not in used][:BATCH]
    if len(identifiers)<BATCH: return []
    chosen=[]
    for y in ROWS:
        for x in range(250,851,28):
            if placement_clear((x,y),active+chosen,bumpers,devices):
                chosen.append(dict(id=identifiers[len(chosen)],x=x,y=y))
                if len(chosen)==BATCH: return chosen
    return []
