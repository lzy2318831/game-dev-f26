"""Public-only experimental power floors; no engine, rollout or model selection."""
from copy import deepcopy

ADAPTIVE_SYSTEM=''' Adaptive energy is a separate experimental power mode, not
a multiplier. Contact/pot floors are25 at travel<=150,35 at<=350,50 beyond350;
banks add5. Power never falls below the listed2x recommendation, capped100.
Escape/device routes retain2x instead of assuming a stronger path is clear.
Base stopping/scratch estimates do not establish safety at these powers.
More movement and pots in saved-state simulations do not prove a win-rate or
human-experience improvement. Select a listed ID; never adjust its power.'''
ADAPTIVE_FORMULA='min(100, max(original_power * 2, route_distance_floor))'


def adaptive_recommendations(rows):
    result=deepcopy(rows)
    for row in result:
        base=row['power'];floor=0
        if row['route'] in ('contact','pot','bank-contact'):
            floor=25 if row['travel']<=150 else 35 if row['travel']<=350 else 50
            if row['route']=='bank-contact':floor+=5
        row.update(original_power=base,power_multiplier=None,power_mode='adaptive',
            adaptive_floor=floor,power=min(100,max(base*2,floor)))
        row['risk']='Adaptive energy: base stopping/scratch estimates below do not establish safety. '+row['risk']
    return result
