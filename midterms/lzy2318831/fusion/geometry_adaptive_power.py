"""Experimental intended distance profile; no engine, rollout or model selection."""
from copy import deepcopy
import math

ADAPTIVE_PROFILE='adaptive-distance-v2'
ADAPTIVE_SYSTEM=''' Adaptive distance v2 is an experimental intended power
profile, not a multiplier or floor. Contact/pot/bank travel d uses linear30to40
over0to150,40to80 over150to350,80to100 over350to1000; saturate100beyond1000.
Round half up to legal integer power. No2xminimum or extra bank increment.
Escape/fallback/device routes retain their separate2x treatment. Distance is
the supplied cue-route travel, not full outgoing pot travel. Base reach/pot/
stopping/scratch estimates may not hold; a pot can undershoot even on a clear
route. More scratches are an accepted tradeoff, not a measured win-rate gain.
Select a listed ID; never adjust its power.'''
ADAPTIVE_FORMULA='half_up(30+d/15 if d<=150 else 40+(d-150)/5 if d<=350 else min(100,80+(d-350)/32.5)); d=max(0,travel); escape/device=min(100,2*original_power)'


def distance_power(distance):
    d=float(distance)
    if not math.isfinite(d):raise ValueError('Distance must be finite')
    d=max(0,d)
    raw=30+d/15 if d<=150 else 40+(d-150)/5 if d<=350 else min(100,80+(d-350)/32.5)
    return min(100,math.floor(raw+.5))


def adaptive_recommendations(rows):
    result=deepcopy(rows)
    for row in result:
        base=row['power'];targeted=row['route'] in ('contact','pot','bank-contact')
        row.update(original_power=base,power_multiplier=None,power_mode='adaptive',
            adaptive_profile=ADAPTIVE_PROFILE,power_policy='distance-v2' if targeted else 'separate-2x',
            power=distance_power(row['travel']) if targeted else min(100,base*2))
        row['risk']='Adaptive distance v2: base energy/stopping/scratch estimates do not establish safety or a pot. '+row['risk']
        if targeted and row['power']<base:row['risk']+=' Below base energy recommendation; pot may undershoot.'
    return result
