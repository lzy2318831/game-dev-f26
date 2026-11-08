"""Public geometry helpers shared by device physics and observation-only policy."""
import math


def nearest_point(p,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1]
    length=dx*dx+dy*dy
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/length)) if length else 0
    return a[0]+dx*t,a[1]+dy*t


def segments_distance(a,b,c,d):
    def cross(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    if cross(a,b,c)*cross(a,b,d)<=0 and cross(c,d,a)*cross(c,d,b)<=0:
        if max(min(a[0],b[0]),min(c[0],d[0]))<=min(max(a[0],b[0]),max(c[0],d[0])) and max(min(a[1],b[1]),min(c[1],d[1]))<=min(max(a[1],b[1]),max(c[1],d[1])):
            return 0
    return min(math.dist(p,nearest_point(p,x,y)) for p,x,y in ((a,c,d),(b,c,d),(c,a,b),(d,a,b)))


def crosses_gate(old,new,gate):
    y=gate['y']; dy=new[1]-old[1]
    if not ((old[1]<y<=new[1]) or (new[1]<y<=old[1])) or dy==0: return False
    x=old[0]+(new[0]-old[0])*(y-old[1])/dy
    return gate['x_min']<=x<=gate['x_max']
