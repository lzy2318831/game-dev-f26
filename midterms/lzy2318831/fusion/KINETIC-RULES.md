# v1.6 amendment to the original K1-K5 specification
Current table removes only the two short left-entry/right-entry diagonals.
K3 boost values below describe the preserved original; current values are
impulse240, separating floor45, launch floor315 (0.75scale). All other K rules,
activation limits, feedback timing and scoring remain unchanged. Original exact
specification is archived in versions/kinetic-replenish-v1.5-final/fusion/.

# Kinetic Circuit - current design rules K1-K5

K1 Pop cluster: three radius24 pops at (280,105),(375,105),(327,181).
Right ricochet chamber: main pop(670,112) radius29 and two radius16 posts at
(620,165),(725,165), plus three angled rail segments. Four lower pops remain.
Ten powered bumper bodies total. On incoming collision reflect restitution0.95,
add260 outward for large pops and200 for small posts, max two impulses per
ball per device per shot. Cap speed950. Cue15 once/body/shot; objects0.
Cluster geometry preserves a fixed-device-free y220..315 central corridor.

K2 Vault: keep entrance(805,88),radius17. On moving-ball entry, stage its center
30 units left of aperture and eject at640 towards target(670,112), inducing
follow-up chamber contacts. One eject per ball/shot. Cue40 once, object0.
No dwell, randomness or stored ball; later entries traversable/unpowered.

K3 Slings: two powered impulses per ball/sling/shot. Each incoming edge contact
reflects then adds320 along a fixed upward-inward vector (left .8,-.6; right
-.8,-.6), then enforce separating normal velocity at least60 to avoid
kicking through a rail; powered exit speed minimum420, cap950. Later contacts passive0.90 reflection. Cue10 once/sling/shot.
New chamber rails passive0.90. Existing friction70units/sec/sec unchanged so
open pool shots still settle; energy is added only by mechanisms.

K4 Skyway return: entrance(230,55),radius14, immediate transfer to(630,75),
eject at620 along(.86,.51) normalized. One transfer per ball/shot, cue20 once,
objects0. Exit must be clear of other active balls by23 units; blocked entry
stays traversable and does not consume use/score. Entrance/exit and direction
are public. Engine shows instantaneous transfer; curved raised bridge artwork,
entry/exit flashes and playback snap are a 2.5D illusion, not a physical3D ramp.
No scoring sensors may trigger along the transfer chord. No hidden steering.

K5 Device-only cap315/shot:150pop+60lane+25Orbit+20sling+40Vault+20Skyway.
Existing pocket/combos and scratch-void priority unchanged. Six alternating
opportunities/player;9600ticks/40sec bounded shot. Explicit failure on bound.
All impulses and transfers have finite per-shot budgets. Same five operations,
angle/power actions, public detached geometry. No paid API evaluations.

Acceptance: incoming Vault cue -> chamber bumper after eject; Skyway cue ->
chamber after return; object gets physics but no device score. Reentry cannot
recharge. Cluster-targeted shots must hit >=3 distinct device IDs and settle.
Wrong-seat/invalid/postterminal and observer isolation remain tested. Exact
stress cases added before relevant engine changes; frozen policy cases not used
for tuning. Evidence labels are design for rules and observed for actual runs.

Chamber-bank end at(590,195) avoids overlapping post8. Repeated physical sling
contacts emit zero-point feedback after first award; they never rescore.
