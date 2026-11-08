# Pool + Pinball: Arcade Fusion — Aurum Circuit v1.1

The [Aurum Circuit specification](POLISH-RULES.md) P1–P5 supersedes the prior v1
two-bumper layout and scoring. The primary table has four bumpers, ten solid
guide segments, two return lanes and a traversable Orbit spinner. Caps are
60 bumper +20 lane +25 spinner points per shot. Orbit doubles subsequent pot
base value within that shot only. Controls and match loop are unchanged.
Previous rules and playable code are preserved in versions/fusion-v1/.

Declared before Fusion implementation/tuning. Original Pool Shark-inspired
design, not historical reconstruction. All F1–F9 rules are `design` evidence.

## F1: Table and initial state

Table interior 1000×500 units; top-left origin; x right, y down. Ball radius 11,
equal mass. Cue (230,250). Six object balls form a spaced triangle: rows 1/2/3
at x=700/721/742, y centered on 250 with spacing 24. Cyan bumpers are at
(330,112) and (670,388), gold at (670,112) and (330,388), radius 29 each.
Pocket centers (0,0), (500,0),
(1000,0), (0,500), (500,500), (1000,500); capture radius 29. Both scores zero,
P1 starts. Reset seed records reproducibility; the default rack is fixed.

## F2: Actions and shot ownership

Shot JSON: `{"angle": int 0..359, "power": int 1..100}`. Clockwise from right.
Speed = 100 + 7×power units/second. Same vocabulary for humans and policies.
Mouse: point to aim; press and pull back opposite the aim direction, release
to shoot. Drag under 8 screen-scaled table units cancels. Pullback is clamped
to 180 table units, mapped linearly to power. Aim locks on press; while held,
only power changes. Right-click/Escape cancels. No direct steering in flight.
Only the active role can submit a shot; the engine resolves it fully before
the next shot can be accepted. Browser input locks through shot playback.

## F3: Physics

Fixed 1/240-second ticks, independent of rendering. Stable ball-ID pair order;
approaching equal-mass normal impulses with restitution 0.98; cushion normal
restitution 0.88; friction reduces speed by 70 units/second squared, snapping
speeds under 3 to zero. Pocket capture precedes cushions/collisions and occurs
again after separation. Six-pocket mouths allow entry instead of bouncing on
the rail. At most 4800 ticks (20 simulated seconds) per shot. A simulation cap
is an execution failure, not a competitive win. No spin or jumping.

## F4: Bumpers and anti-farming

Ball–bumper collision separates ball centers to radius 40, reflects an inward
normal velocity (restitution 0.95), and adds outward normal speed 150. Clamp
resulting total speed to 950. Add the impulse only on contact entry, requiring
separation beyond radius 41 before rearming. Each ball may receive at most
two impulses per bumper per shot; later entries reflect without added energy.
This prevents indefinite acceleration; friction and the tick cap bound play.

Only cue-ball bumper entries score: 15 points per distinct bumper per shot,
at most 60 total. Object balls can use bumper physics but score no bumper
points. Repeated hits never earn more points in that shot. Six shots per
player bound bumper-only scoring at 360 points. Scoring does not depend on
animation frames or particle effects.

## F5: Pots and combos

Each object pocket = 100 points. In a shot with n object pots, multi-pot bonus
is 50×max(0,n−1). If at least one object is pocketed after the cue has triggered
a bumper in that shot, award a single +50 bumper-pot combo. Event order matters.
Final shot score also includes lane/spinner points and the shot-only Orbit pot multiplier bonus (P2–P4).
An otherwise valid miss scores zero. Potting never grants an extra turn.

## F6: Fouls and reset

Cue pocket = scratch. Record the foul and void every point from that shot,
including any earlier bumper/pot/combo points. Pocketed objects stay removed.
Respot cue at the first clear point: x=(230,180,130,80), for each x use
y=(250,200,300,150,350,100,400). Require center distance ≥23 from object balls
and ≥42 from bumpers, plus ≥16 from each guide centerline. No player-controlled ball-in-hand. Last-object clearance
still ends the game, even on a scratch; final scores determine the result.

## F7: Turns and endings

Each player has exactly six shot opportunities, alternating P1/P2. End early
if all six objects are removed, otherwise after twelve total opportunities.
Higher score wins, equal scores draw. Commit score/foul, respot, decrement the
shooter’s quota, switch player, then check clearance before shot exhaustion.
Malformed active-player actions consume an opportunity and increment invalid
count, leaving all balls/scores unchanged. Wrong-role calls change nothing.
Post-terminal calls change nothing, including counters. Unknown roles error.
Optional runner deadlines/call caps end as explicit execution failures without
a competitive winner. A UI cancellation is not an engine action.

## F8: Five operations and information

`reset(seed)` resets match and returns initial observation. `observe(player_id)`
returns detached public positions, geometry including all device segments/sensors, scores, shots remaining, active
seat, foul/invalid counters, status and visible last-shot events. No engine,
filesystem, credentials, private scenario labels or evaluator annotations.
`legal_actions(player_id)` returns a compact schema for all 36,000 angle/power
pairs only for the active role; inactive/terminal returns []. No shot rankings.
`step(player_id,action)` validates, resolves, scores, switches and returns
acceptance, events, optional playback frames, and next observation.
`outcome()` returns ongoing/terminal, reason, winner/draw/failure and metrics.
The game is fully observed at rest; velocities are zero at decision points.

## F9: Policies and evaluation

Geometric baseline uses ghost-ball contacts, clear-path checks, pot distance,
cut angle, scratch risk, plus bounded bumper-target candidates derived from
the same public geometry. No hidden state or authoritative engine rollouts.
Baseline and eventual model share observations, actions and shot quotas.
Freeze evaluation.json before policy tuning; keep held-out cases out of
development matches. No paid API calls in this slice. Max 12 model attempts
per match, including failures; timeout 20 s/request, deadline 300 s/match.
No automatic fallback mislabeled as model play. Failed trials remain failures.
