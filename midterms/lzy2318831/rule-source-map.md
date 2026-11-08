# Arcade Fusion rule/source map

## Experimental geometry-assisted player (no game-rule changes)

Design: [player contract](fusion/GEOMETRY-ASSISTED.md), applying existing F2/F3/F8.
`fusion/geometry_candidates.py` derives bounded options from public data;
`geometry_agent.py` validates the LLM's ID selection; `geometry_live.py` provides
a separately labelled browser entry. `tests/test_geometry_agent.py` covers
directions, reach, obstruction, scratch screening, selection failures and public
boundaries. Existing rule rows and frozen gameplay are unchanged. Actual new
offline evidence and independent review: `evidence/geometry-assisted-01/`.

Lifecycle correction under the same F7/F8 rules: minimum-power fallback options,
fresh match/token preparation and cumulative server accounting are specified in
`fusion/GEOMETRY-ASSISTED.md`, implemented in geometry candidates/live/budget,
and tested by `tests/test_geometry_lifecycle.py` plus actual Chrome evidence in
`evidence/lifecycle-fix-01/`. Six shots per player and frozen physics are unchanged.

Stabilization under these existing F7/F8 contracts: one bounded geometry-only
navigation owner, bounded leave signaling, conservative contact/bank power and
contact-before-device proposals. Regressions: `tests/test_geometry_stability.py`,
`tests/geometry-navigation.cjs`; actual HTTP/Chrome: `fusion/geometry_lifecycle_check.py`.
Evidence and independent review: `evidence/stabilization-01/`. No engine rule changed.

Student-authorized demonstration power setting under the same public-proposal
contract: `fusion/geometry_agent.py` caps multiplied candidate power while keeping
ID/angle/target/route; `fusion/geometry_live.py` accepts only waiting-state local
settings; `fusion/geometry_power.js` labels preference and fallback. Regressions:
`tests/test_geometry_power_setting.py`, `tests/geometry-power.cjs`; evidence:
`evidence/power-setting-01/`. No physics/scoring/shot-quota changes.

Optional adaptive energy uses the same F2/F3/F8 public-proposal contract:
`fusion/geometry_adaptive_power.py` applies tested distance/route floors only;
`tests/test_geometry_adaptive.py` verifies legacy payload parity, caps, route
identity, known266degree settlement and guarded HTTP rollback. Offline evidence
and independent review: `evidence/power-calibration-01/`. No physics changes.

Cue/restart UI checkpoint under F7/F8: `fusion/web/game.js` gates presentation
frames until visible cue contact; `geometry_status.js` and `geometry_live.py`
prepare fresh sessions after bounded settlement and distinguish cumulative
allowance exhaustion. `tests/cue-stroke.cjs`, updated geometry controller test
and actual Chrome evidence: `evidence/table-balance-01/`. At that earlier checkpoint physics remained unchanged pending identification;
the confirmed B1-B3 amendment below now defines the revised table.

## Aurum Circuit v1.1 expansion — declared before implementation

All new rules use `design` evidence in fusion/POLISH-RULES.md:
P1 four perimeter bumpers/open center; P2 passive return channels and capsule
guide rails; P3 traversable Orbit spinner/shot-only 2×; P4 bounded score and
scratch interaction; P5 original layered artwork matching physical geometry.
Acceptance tests are tests/test_fusion_polish.py. Physical geometry and sensors
are in fusion/devices.py; scoring is ShotLedger in fusion/engine.py; original
artwork is fusion/web/aurum.js. Actual red/green and browser evidence is in
evidence/polish-1/REPORT.md. Previous
v1 results remain evidence for that version only.

The final game is original. All F1–F9 rules use **design** labels and point to
the exact specification and rationale in [RULES.md](RULES.md). No historical
physics/graphics fidelity is claimed.

| Rule | Evidence | Implementation | Tests |
| --- | --- | --- | --- |
| F1 table/rack | design: RULES F1 | fusion/engine.py DEFAULT, BUMPERS, Episode.reset | test_fusion.FusionInterface.test_initial_state_and_isolation |
| F2 angle/power/input | design: RULES F2 | Episode.valid/step; fusion/web/game.js pointer handlers | illegal/wrong-seat tests; actual browser drag check |
| F3 billiards | design: RULES F3 | fusion/engine.py tick/constrain/capture | FusionPhysics; frame-independence test |
| F4 bumpers/caps | design: RULES F4 | tick bumper branch; ShotLedger.bumper | test_bumper_impulse_and_farming_caps |
| F5 score/combos | design: RULES F5 | ShotLedger.score/breakdown/pocket | test_combo_and_scratch_scoring |
| F6 scratch/respot | design: RULES F6 | Episode._respot/step | test_scratch_and_respot |
| F7 opportunities/end | design: RULES F7 | Episode._finish/outcome | illegal/limits; pot_end tests |
| F8 player boundary | design: RULES F8 | Episode five methods; fusion/player.py | isolation/public-context tests |
| F9 baseline/evaluation | design: RULES F9; fusion/evaluation.json | fusion/baseline.py; fusion/runner.py | deterministic replay; budget/failure tests |

Observed application evidence is in evidence/FUSION-SLICE.md and the actual
browser test report. It is not historical gameplay observation or human
playtest evidence. Historical claims belong to the archived pre-Fusion map;
uncertain historical interpretations stay assumed and are irrelevant to these
original rules. Earlier source/code evidence is preserved, not relabeled.

The copied project-owned geometry and bounded-worker helpers are identified in
SOURCES.md. No historical source, assets, ROMs, lookup tables or prose were copied.


Current design amendment M1?M4: fusion/MAXIMAL-RULES.md (project-relative),
superseding earlier device counts and caps. Test-first evidence: evidence/maximal-1/.

## Current M1?M5 (design, not historical code)
| Rule | Implementation | Test |
| --- | --- | --- |
| M1 density/passive banks/lanes | fusion/devices.py GUIDES/DEVICES | Maximal.test_density_and_copy, test_lane_caps |
| M2 powered slings | rail_collision; ShotLedger.device | test_sling_cap |
| M3 zero-dwell Vault scoop | process_sensors | test_scoop_once_scratch, test_objects_no_device_score_and_full_cap |
| M4 bounded scores/public data | ShotLedger.score/breakdown; observe | test_density_and_copy, test_wrong_seat, test_objects_no_device_score_and_full_cap |
| M5 finite settling extension | Episode max_ticks9600 | test_long_cascade_settles |
Actual review/regression evidence: evidence/maximal-1/REPORT.md. Exact rule
specification: fusion/MAXIMAL-RULES.md. Previous maps/results are versioned.

Current K1-K5 design amendment: fusion/KINETIC-RULES.md (project-relative).
Supersedes M1-M5 mechanisms/counts; match actions and quotas unchanged.

## Current K1-K5: Kinetic Circuit (design evidence)

Supersedes earlier layout/device counts. Canonical RULES.md now consolidates
current rules; prior maps/rules remain in runnable version snapshots.

| Rule | Engine / presentation | Executed acceptance |
| --- | --- | --- |
| K1 Cascade triangle / Reactor / ten pops | engine.BUMPERS/tick, mechanicalBumper | Kinetic.test_cluster_public_geometry, test_cluster_chain_and_settling, test_solids_do_not_overlap |
| K2 directed Vault eject | devices.process_sensors | test_vault_fixed_launch_and_followup |
| K3 inward slings,420 minimum, finite boost | devices.rail_collision, ShotLedger.device | test_stronger_inward_sling, test_repeat_sling_feedback_never_rescores; Maximal.test_sling_cap |
| K4 blocked-exit Skyway,2.5D return | process_sensors, kineticDeck, animate transfer snap | test_skyway_blocked_exit_and_once, test_no_stationary_device_launch, test_skyway_followup_and_full_cap |
| K5 bounded cap315 / scratch / episode | ShotLedger, Episode, public context | test_skyway_followup_and_full_cap, test_default_skyway_vault_chain, existing quota/invalid/boundary tests |

`observed`: actual test logs, default-layout controlled contact comparison,
public-API browser screenshots and fresh independent review in
[evidence/kinetic-1/REPORT.md](evidence/kinetic-1/REPORT.md).
`code`: project source implements design; it is not historical evidence.
No new historical assumptions; no observed human or live model evaluation.

Final Z1-Z3 amendment: fusion/FINAL-RULES.md, declared before implementation.

## Final Z1-Z3 amendment (design,2026-11-07)

| Rule | Code | Deterministic evidence |
| --- | --- | --- |
| Z1 fifteen-object clear five-row rack | engine.DEFAULT/Episode; web palette/stripes | FinalRack tests, full16-ball matches, browser16render |
| Z2 separate bounded Smart physics planner | smart.Simulation/candidates/plan; original baseline unchanged | SmartTests, max40000ticks/24candidates, prediction/ID/determinism, fixed6match comparison |
| Z3 separate automatic Smart seat | server.GameSession; web modes/HUD | test_smart_mode_automatic, final15browserthinking/playback/autonomous shot |

Conservative broadphase is an implementation optimization, not a physics-rule
change: PhysicsRegression checks archived trajectories/events. Independent
review verified4full16-ball breaks tick-for-tick. Current results use final15
version only. Smart is not LLM evidence. Current frozen suite5 and separate
development comparison were declared before policy tuning. See evidence/final-15/.

Current R1-R4 authorized amendment: fusion/REPLENISH-RULES.md (design).
Supersedes early-clear precedence only while replenishments remain.

## R1-R4 current rule amendment: replenishment (design)

| Rule | Implementation | Executed tests |
| --- | --- | --- |
| R1 threshold/safe boundary/two-event limit/clear priority | Episode._replenish and step before _finish | test_threshold_count_and_isolation, test_nine_no_spawn_and_no_invalid_spawn, test_max_two_and_empty_clear_priority, test_final_opportunity_never_spawns |
| R2 atomic deterministic placements/IDs | replenish.spawn_batch/placement_clear | test_no_overlap_and_deterministic_positions, test_device_exclusion_and_many_states, test_moving_or_blocked_batch_atomic |
| R3 public counters/Smart clearance/replay | observe/outcome, player.PUBLIC, smart.utility, runner rules hash | test_replay_counters_events_and_tampering, test_threshold_count_and_isolation |
| R4 boundary frame/glow/toast | step._frame, aurum.deviceFeedback, finishMovie | test_reset_and_single_event_per_boundary, automated public-UI notification capture |

Observed evidence in evidence/replenish-1/REPORT.md. Existing placements/seeds
remain physically valid; suite6 amendment changes rule metadata only, old
suite5 declarations preserved in versions/final15-v1.4/. No live trials/tuning.
User reported their playtesting feedback; no independent human observation is
claimed by the assistant. Prior AI results stay explicitly v1.4only.

## Real LLM player integration - no frozen rule/interface changes

The18frozen gameplay/visual/public-interface artifacts remain unchanged.
New fusion/llm.py uses existing build_context and validates shot JSON; runner
commits via frozen Episode.step. No simulator or repository/evaluator tools.
New contract fusion/LLM-CONTRACT.md and tests/test_fusion_llm.py verify allowed
context,approval/budget,actualaction/replay,invalid/failure/timeout handling.
Official provider API/docs are code integration references,not historical rule
sources. Frozen suite6 unchanged. No paid/live model evidence exists yet.


## B1-B3 confirmed v1.6 balance (student design)

B1 removes only left-entry/right-entry diagonal guide IDs; remaining27guides
match the original list exactly after filtering those two. B2 scales only lower
Slingshot boost vector/separation/launch-floor by0.75; reflection,950cap,two
boosts/ball/sling, scoring and feedback remain unchanged. Source: explicit student
confirmation; current RULES.md and fusion/devices.py. B3 identifies new physics
as fusion-1.6.0-balanced; fusion/legacy.py loads hash-verified original1.5forold
traces/recordedviewer/legacy prompt-v2hosting. CurrentGeometryhostexplicitly1.6.
Regression: tests/test_balanced_table.py; evidence/table-balance-v16-01/.
Prior108sourcefiles and49official/smoke evidence copies remain immutable under
versions/kinetic-replenish-v1.5-final/. Older normative/amendment text there is
historical; no evaluation result is transferred to revised physics.

Adaptive-distance-v2 proposal amendment: explicit student distance bands map to
fusion/geometry_adaptive_power.py; tests/test_adaptive_distance_v2.py checks
boundaries, intended power, preserved route fields and mandatory266° position.
No legal action, scoring, physics or shot quota changes. Escape/device keep2x.
Evidence: evidence/adaptive-distance-v2-01/REPORT.md; independent geometry_review.
