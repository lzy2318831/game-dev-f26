# Rules and interface specification v1

Status: offline implementation v0.2.0; provider-specific live integration pending.
All numeric coordinates use a top-left origin, x rightwards, y downwards.

## R1: Table and initial state

The interior is 1000 by 500 units. Ball radius is 10 units. Six pocket centers
are (0,0), (500,0), (1000,0), (0,500), (500,500), (1000,500), each with capture
radius 24. A ball whose center enters that radius is pocketed. The cue starts
at (250,250). The default six-ball triangle is (700,250), (718,239),
(718,261), (736,228), (736,250), (736,272). Object IDs 1 through 6 follow this
order. No initial velocity; scores and counters start at zero; player `p1`
starts. Scenario layouts override positions, not rules. Seeded scenario
selection must use a local random generator, never global RNG state.

Six balls retain multiple targets and blocking decisions at low simulation
cost. A full rack adds evaluation and debugging work without a rubric bonus.

## R2: Shot vocabulary

A shot is `{"angle": integer, "power": integer}`. Angle is 0 through 359
degrees, clockwise from right; power is 1, 2, or 3, mapping to initial speeds
180, 300, or 420 units/second. Reject extra keys, booleans, nonfinite numbers,
floats, and out-of-range values. Only the active player may shoot. Humans,
the model, and the baseline use exactly this vocabulary.

One-degree directions give the geometric baseline useful aiming precision;
three powers keep the model's choice small. These replace the earlier proposed
five-degree grid, whose accuracy could dominate policy quality.

## R3: Shot resolution

The engine applies initial velocity to the stationary cue ball and advances at
1/240 second per tick. All balls have equal mass. Use normal elastic impulses
for approaching ball pairs, positional separation for overlaps, rail reflection
with restitution 0.9, and speed reduction of 30 units/second squared. Speeds
below 1 unit/second become zero. Process balls and pairs in stable ID order.
Pocket capture is checked before rail reflection. A pocketed ball is removed
before later collision processing. The shot finishes when all balls stop.

Use at most 4800 ticks per shot. Exceeding this cap ends the match as
`simulation_limit`, with no competitive winner and the partial shot's scoring
uncommitted. This is an execution failure, not a loss caused by strategy.
Tick ordering is: move in ID order; capture before reflecting x then y;
separate/impulse pairs in lexicographic ID order; apply friction. Separation
allocates displacement to whichever ball has rail clearance, so it does not
push centers through cushions. Dense multi-contact clusters are resolved over
successive ticks rather than a global constraint solver. Tests use 1e-9
geometric tolerances; exact replay is promised for the same Python runtime,
not bitwise equality across platforms.

This simple model supports aiming, rebounds, and collisions without spin,
cloth effects, or a general physics dependency. It is not historical physics.

## R4: Scoring and scratches

Each object pocketed in a shot gives the shooter one point. If the cue ball
is pocketed at any time in that shot, award zero points for the entire shot,
even if object balls also fell. Those object balls remain removed. Increment
the shooter's scratch counter. This prevents a scratch-and-pot shot earning
points; it can reduce the total score available in the match.

After resolving a scratch, place the cue at the first unoccupied candidate in
this order: x in (250,200,150,100,50), for each x use y in (250,200,300,150,350,
100,400,50,450). A candidate must be at least 21 units from every remaining
object ball. Six object balls cannot occupy all 45 widely separated candidates.
All candidate positions are inside rails and outside pockets. No ball-in-hand
phase or extra model call is needed. Scratch scoring and automatic respotting
are explicit design choices, not verified original behavior.

## R5: Turns and invalid actions

Switch to the other player after every completed shot, including a scoring
shot or scratch. A miss scores zero and also switches turn. Fixed alternation
keeps both players involved and bounds seat advantage; retaining turn after
scoring was considered but excluded.

A malformed action from the active player increments their invalid count,
consumes one attempt, and switches turn without changing balls or scores.
It is not a physics shot. A wrong-player call is rejected without consuming
an attempt or changing the turn; only the runner schedules policy calls.
Invalid player identifiers raise a documented input error. After termination,
all step calls are refused without modifying any counters or game state.

## R6: Competitive outcomes

After a completed shot, first commit scoring, then check table clearance,
then the attempt cap. End at zero object balls or 24 total attempts. Higher
score wins, equal score draws. No tie breaker. Report `table_cleared` or
`attempt_limit`, both scores, winner (`p1`, `p2`, or null), and draw flag.
Check clearance before the attempt cap if both happen together.

## R7: Runner limits and provider failures

The runner alone holds authoritative state and resets the episode. Permit
at most 24 API attempts across a match (12 per player in fixed alternation),
including failed calls. Each request has a 20-second timeout, no automatic
retries, and a 512-output-token cap. Each match has a 300-second deadline,
checked before/after every policy call and physics step; individual calls
must actually enforce the request timeout. A hung policy must be interruptible.

Provider error, timeout, refusal, or missing usable action ends an evaluated
match as `provider_error`, `request_timeout`, or `invalid_model_response`;
record the failing seat and no competitive winner. Syntactically valid action
objects with illegal values follow R5 and count as invalid attempts. Exhausted
call budget or deadline ends as `model_call_limit` or `episode_timeout`, with
no competitive winner. Count these as failed trials, never ordinary wins or
draws. No automatic baseline substitution. Log completed attempts and limits.

## R8: Five-operation interface

| Operation | Responsibility and return |
| --- | --- |
| `reset(seed)` | Runner-only operation; initialize the chosen scenario and return initial episode metadata. Scenario and seat configuration belong to constructor/runner, not player access. |
| `observe(player_id)` | Detached JSON snapshot: role ID, active player, table/pocket geometry, ball IDs/positions, both scores, attempts remaining, scratches, invalid counts, last-shot events, public status. No velocities are needed at settled decision points. |
| `legal_actions(player_id)` | Active seat: compact documented vocabulary equivalent to all 1080 angle/power pairs. Inactive/terminal seat: empty. No target ranking or predicted results. |
| `step(player_id, action)` | Engine validates the actor and payload, resolves an accepted shot, and returns acceptance, visible events, and detached observation. |
| `outcome()` | Ongoing/terminal, reason, scores, winner/draw or execution failure, attempts and invalid counts; runner adds call/latency/usage metadata. |

The table is fully observed; both roles see the same public table, with their
own role ID. Hidden seed, scenario name, RNG state, private engine object,
evaluation annotations, prompts, repository paths, and credentials are excluded.
Test snapshot mutation isolation and exact player-context fields. The model
adapter receives serialized observation, vocabulary, and optional bounded
visible history; no development tools. The baseline receives the same data,
not a World reference or private simulation API. A trusted adapter owns HTTP
credentials; they are never included in model messages.

## R9: Modes and history

Support Human vs Human, Human vs Model, Model vs Geometric Baseline, and
Baseline vs Baseline through one engine. Human controls choose the same angle
and power; rendering cannot change rules. Agent-vs-agent play requires no human
move selection. The baseline computes ghost-ball aiming, clear path checks,
cut angle/distance penalties, and scratch-risk estimates, with a fixed fallback.
It does not call the authoritative engine for future-state rollouts.

Default model context is current observation only. Compare this with the last
two public decision/result records, truncated to a fixed character budget.
Fully observed settled positions should make persistent memory unnecessary;
that is a hypothesis to test, not an evaluation result.
