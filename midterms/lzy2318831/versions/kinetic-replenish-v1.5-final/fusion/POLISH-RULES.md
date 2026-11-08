# Aurum Circuit — focused expansion specification

Design declaration before implementation, following competitive-rule-change.
Controls, twelve alternating opportunities, six objects, six pockets, and the
five methods do not change. This is one table, not a collection of game modes.

## P1: Four pop bumpers

Move bumpers to (330,112), (670,112), (330,388), (670,388), radius 29.
Existing reflection/boost/rearm/energy caps stay unchanged. The cue scores
15 once per distinct bumper per shot, max 60. The four bumpers frame a clear
central billiards strip, y=185..315, rather than obstructing the break.

## P2: Return channels and guide rails

Left inner tubular rails: (125,85)–(88,125), (88,125)–(88,330),
(88,330)–(140,365). Return elbow: (18,380)–(76,440). Mirror x about 500 for
the right channel. Top funnel: (410,52)–(440,95), (590,52)–(560,95).
All ten are two-sided capsules, radius 4; ball contact distance 15. Apply
nearest-point separation and approaching normal restitution 0.90, without
energy injection or invisible steering. Rounded ends avoid snags. The side
cushions are the outer channel walls; open ends allow entry and exit. Balls
can stop inside a lane and be played normally next turn.

Crossing y=270 at x=24..70 (left) or 930..976 (right) registers a return lane.
Only the cue scores: 10 once per side per shot, max 20. It must cross, not sit
on the line. Object balls do not score. Lower elbows bank downward-moving
balls inward; no powered lane kick is added.

## P3: Orbit spinner and shot-only multiplier

A freely turning spinner gate spans x=470..530 at y=84 within the top funnel.
It is traversable, not a fixed solid wall. Crossing at speed at least 25 makes
each ball lose 8% speed on its first crossing of that shot and emits a visible
spinner event. Other crossings may animate but do not rescore or lose energy.
The first cue crossing earns 25 and lights 2× pot value for the rest of that
shot. Object crossings animate but never award points or activate 2×.

Each later object pot earns normal 100 plus 100 multiplier bonus. Earlier
pots are not retroactively doubled. The multiplier never stacks above 2× and
resets to 1× next shot. Existing bumper-pot/multi-pot bonuses stay flat; device
points are not multiplied. Scratch voids everything as before.

## P4: Scoring and farming limits

Score = 100×pots + distinct bumper points + lane points + spinner points +
multiplier bonus + existing combo bonuses. Maximum device-only score is
60+20+25=105/shot, or 630/player across six opportunities. Repeated contacts
and crossings cannot raise these caps. Keep the two-boost-per-ball/bumper
limit, 950 bumper speed cap, and 4800-tick cap. Geometry/scoring are public;
no secret bonuses. This expansion's results are separate from v1 results.

## P5: Presentation and guidance

Original navy/gold/cyan art depicts colliding raised rails, flush lane inlays,
metallic housings, spinner supports and a rotating paddle. Decoration outside
raised collision surfaces is not a hidden obstacle. The first-contact guide
includes rails and actual bumper radii. Event-driven particles/light sweeps,
spinner rotation and small camera recoil do not affect deterministic physics.
