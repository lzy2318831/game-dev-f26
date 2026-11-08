# Arcade Fusion rule/source map

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
