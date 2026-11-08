# Pool + Pinball: Arcade Fusion - Kinetic Circuit v1.5 REPLENISH

Original Pool Shark-inspired design, not a historical reconstruction. All
rules below use `design` evidence. Current K1-K5 specification is in
fusion/KINETIC-RULES.md (project-relative); it was declared before implementation.
Prior rules/code/evidence remain in versions/grand-v1.2, aurum-v1.1 and fusion-v1.

## F1 / K1: Table and initial state
1000x500, top-left origin, x right/y down. Sixteen equal-mass radius11 balls: cue(230,250) and15numbered objects.
Five triangular rows0..4: x=700+row*24*sqrt(3)/2;
y=250+(column-row/2)*24 for column0..row. Deterministic24-unit spacing.
No devices moved. Scene layouts permit cue plus1..15objects for tests/evaluation.
Six pockets: (0,0),(500,0),(1000,0),(0,500),(500,500),(1000,500), capture radius29.
P1 starts, scores zero, fixed initial rack. Seed is recorded for reproducibility; it does not randomize this rack.
Ten pops: Cascade triangle(280,105),(375,105),(327,181),radius24; Reactor main
(670,112),radius29, posts(620,165),(725,165),radius16; lower pops(330,388),
(670,388),(435,405),(565,405),radius29. Fixed-device-free corridor y220..315.
Twenty-three passive and six powered capsule rail segments; exact public
endpoints are in fusion/devices.py and observations. Capsule radius4 plus
ball radius11 determines contact. Raised rail artwork follows this geometry.
Twenty-three passive includes three Reactor guides; remaining side/orbit routes
preserve Grand geometry. The raised Skyway is the explicitly marked exception:
its artwork represents a transfer, not an additional physical rail or overpass.

## F2: Shot controls and ownership
Action JSON {"angle":int0..359,"power":int1..100}; clockwise degrees from right.
Initial cue speed100+7*power. Point to aim; press on table, pull backward along
locked aim, release. Pullback max180 table units maps to100power; under8 cancels.
Escape/right-click cancels. No direct steering during motion. Only active seat
acts; Python resolves the complete shot; browser locks input through playback.
Same action vocabulary for human, geometric baseline and LLM player.

## F3: Deterministic physics and limits
Fixed1/240sec ticks, stable ID order. Equal-mass ball normal restitution0.98;
cushions0.88; guide rails0.90. Friction reduces speed70units/sec squared;
under3 stops. Pockets checked before cushions and after pair separation.
Max9600ticks(40simulation seconds)/shot: unresolved motion is explicit
simulation_limit failure, not a competitive winner. No spin or true3D jumping.
Rendering interpolates60Hz snapshots without changing game state. Transfer
frames snap rather than drawing a ball moving through intervening mechanisms.

## F4 / K1-K4: Interactive devices
Pops reflect an inward normal at0.95, add outward260 (radius16posts add200),
cap950. Re-arm after center separates beyond radius(ball+device)+1. Max two
extra impulses per ball per pop per shot; later contacts reflect passively.
Cue earns15 once/distinct body/shot, max150. Objects gain physics but no points.

Slings are triangles with vertices(175,330),(225,375),(165,400), mirrored right.
Incoming edge contact reflects0.90; first two per ball/sling add320 toward
(.8,-.6) left /(-.8,-.6) right, enforce separating normal velocity>=60, then
minimum powered exit speed420 and maximum950. Later contacts passive. Cue10
once/sling/shot, max20. Every contact emits feedback; repeated contacts score0.

Six lane sensors: left24..70/right930..976 at y270; outer100..132/868..900 at
y110; inner190..238/762..810 at y160. Crossing in either direction gives cue10
once/lane/shot, max60. Objects animate without points. Sensors do not steer.

Orbit spinner spans x470..530 at y84; moving crossing at speed>=25 loses8%
speed once per ball/shot. First cue crossing gives25 and2x only subsequent pot
base values in that shot. No stacking/carryover; other balls do not activate it.

Vault aperture(805,88),radius17: moving ball enters, emerges(775,88) and is
actively ejected at640 in direction(-135,24), toward Reactor main pop. Instant
zero-dwell kickout, once per ball/shot; cue40 once. Later entry traversable.
No points or timer simply for waiting in the aperture.

Skyway aperture(230,55),radius14: moving ball transfers once/ball/shot to
(630,75), launched at620 in normalized(.86,.51) direction into Reactor. Cue20
once. Exit blocked within23 of another active ball defers transfer without
score/use consumption. No sensors trigger along transfer chord. Artwork/ghost
trail suggests elevated return, but engine transfer is instantaneous: deliberate
2.5D illusion, no physical bridge collision, height or stored-ball simulation.

Device-only cap315/shot:150pops+60lanes+25Orbit+20slings+40Vault+20Skyway.
At most1890/player over six opportunities; no recurring device farming.
Every powered device has finite per-ball impulse/use budgets, no randomness.

## F5: Scoring and combos
Object pocket100, or200 if cue already activated Orbit this shot. Multi-pot
bonus50*max(0,n-1); one50 assist if object pocket follows cue bumper contact.
Combos/device points are not multiplied. Events processed in deterministic
ball-ID/tick order; shots never earn extra turns. Breakdown and outcome metrics
include new device points. Visual effects cannot award points.

## F6: Scratch and reset
Cue pocket scratches, voiding ALL shot points including earlier pots/devices/
combos. Object pots stay removed. Respot cue at first clear candidate with x
230,180,130,80, for each y250,200,300,150,350,100,400; center distance>=23 from
objects,>=42 from bumpers,>=16 from guide centerlines. No ball-in-hand.
After scoring and respotting, an eligible safe replenishment is attempted before
table-clear termination. Clearance ends the match only if no batch is added;
there is no replenishment after the final opportunity. Scores determine result.

## F7: Turns and outcomes
Six alternating opportunities per player, max12 total. Active malformed action
consumes opportunity/increments invalid counter, leaves balls/scores unchanged.
Wrong seat/postterminal calls change nothing; unknown seat errors. Accepted shot
resolves, commits points/foul, respots, attempts eligible replenishment, then
switches player and checks clearance before shot exhaustion. Higher final score wins, equality draws. Execution failures
(deadline, simulation cap, provider/call/timeout errors) have no competitive win.

## F8: Five operations and boundary
reset(seed), observe(player_id), legal_actions(player_id), step(player_id,action),
outcome(). Observation is detached public balls, all device geometry/directions/
speeds, scores/quotas/active seat, counters, status/visible last events; no engine,
credentials, hidden fixture labels or evaluator answers. Legal actions are the
same compact schema for360*100 shots; inactive/terminal[]. At rest all active
velocities zero. Model returns proposals; engine alone validates and commits.

## F9: Baseline and evaluation
Original public-geometry Geometric baseline (fusion/baseline.py unchanged): ghost-ball targeting, path/cut/power estimates and16
normals per bumper. Variable device radii/impulses respected; predictions through
slings/Skyway/Vault remain approximate, not an optimal search claim. Same public
context/action schema as the LLM. No hidden engine rollouts. Frozen suite6 is
current; previous declarations and overlap corrections remain archived. The
original official live evaluation is complete; results and failures are in
EVALUATION.md. Do not tune on held-out scenarios or silently substitute policies.
The generic runner defaults to at most12 model attempts/match,20sec/request and
300sec/episode. The official one-LLM-seat protocol allowed six model opportunities
per match and72 combined attempts, including the failed request and smoke test.
The separate browser live demo caps six requests and$0.25 per match, with a
20sec request timeout,600sec session deadline and60sec animation acknowledgement.
These transport budgets do not change the twelve-opportunity game rules.
Development shot sweeps/browser checks are not live evaluation or human playtest.

Final Z1-Z3 amendment: fusion/FINAL-RULES.md, declared before implementation.

## Z2-Z3: Three distinct player categories, final design freeze

Geometric AI remains the original baseline algorithm, byte-for-byte preserved.
Smart AI (fusion/smart.py) uses counterfactual authoritative physics on detached
public observations. It is a scripted simulator-based planner, NOT a real LLM.
The LLM receives public observations/legal actions and no simulator tool or
hidden state; no Smart result may be relabeled as a live LLM result. Simulator
access is an explicit computational capability difference, not extra state.

Smart max24candidate actions/40000total ticks,480-tick previews,9600per candidate;
resolves Geometric reference first, completes promising candidates, discards
unsettled predictions from final ranking. Exact ball IDs remain intact after
pots. Scores/pots/fouls/position and bounded match winning margin guide ranking.
Direct/combination/cushion/device/exploration angles and several powers searched.
The data-only predictor shares tick(), not a separately approximated engine.
Measured planning latency is reported; work bound is deterministic and hardware
wall time varies. UI auto-selects Smart actions with explicit thinking indicator.
Human/Human, Human/Geometric and Human/Smart are separate modes. Recorded LLM
evaluation playback and a separately consented live LLM demo are also available.
Recorded playback makes no model requests. No paid calls without approval.

The earlier Z amendment changed rack count and added the separate Smart opponent.
All pinball layout, coefficients, scoring and six-shot rules remain fixed.
Earlier six-ball Kinetic code/docs/tests are runnable in versions/kinetic-six-v1.3/.

Current R1-R4 authorized amendment: fusion/REPLENISH-RULES.md (design).
Supersedes early-clear precedence only while replenishments remain.

## R1-R4: limited ball replenishment (current amendment)

Opening remains15objects and cue. After a valid shot settles, scoring and any
scratch respot finish. If<=8objects remain, supply used<2, and another shot
opportunity exists, add one atomic batch of5resting objects before next shooter.
One batch per boundary. Refill precedes early table-clear check while supply
remains; a cleared table may therefore restart with5. After final opportunity
or execution failure no refill; after two batches ordinary clearance applies.
Six shots/player still bounds every match. Invalid proposals/reset/observation
calls never trigger replenishment. No points/extra turns for spawning.

Deterministic ordered open-grid placement, minimum23between ball centers,
bumper radius+12,16from guidecenterline,41from pocketcenter. Avoid device
apertures/exits,spinner/lane segments and sling interiors. Plan all5before
commit, defer without consuming supply if no full safe batch. No moving ball
allowed. Lowest inactive/missing IDs1..15reused, no simultaneous duplicates;
score pocket events even if number was potted before. Up to25objectpots/match.

Detached observation.replenishment contains threshold/batch/max/used/remaining,
objectcount,pending and rules/placement description for every policy. Outcomes
and replay include count and zero-point batchevent. New balls appear in boundary
playback frame; brief glow/toast. Scoring/device/controls otherwise unchanged.
Geometric source unchanged. Smart search/budget unchanged; only terminal-clear
bonus checks supplies. Its positional tiebreak still previews physical shot
before refill, a disclosed limitation. Exact spec: fusion/REPLENISH-RULES.md.
