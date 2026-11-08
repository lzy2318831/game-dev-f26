# Rule/source map

## Historical reconstruction rules (primary game, h1)

Invocation: `competitive-rule-change`, historical implementation turn. These
rows are recorded before engine tests/code. All historical locators refer to
A7329.XX at b05b01fda70a69444a58fe1bea2b5127eb93e138, not executed ROM evidence.

| ID | Source-supported behavior | Evidence | Independent implementation / approximation |
| --- | --- | --- | --- |
| H1 | 16 balls, 15-object triangular rack, mirrored starts | code: 641-676 | Generate a regular triangle mathematically; approximately one-pixel placement differences; no table copied. |
| H2 | Two 4-bit axes continuously replace cue velocity, neutral center | code: 551-639, 677 | Screen-oriented x/y nibble actions; derive speed arithmetically, one-frame control delay. |
| H3 | Subpixel motion, phased deceleration, descending ball updates, quantized collisions | code: 1015-1023, 1334-1539, 790-864 | Q8 coordinates/velocities, 64-angle normal impulse and contact suppression; not CPU/lookup-table emulation. |
| H4 | Threshold pockets and sign-reversing rails | code: 1208-1275 | Translate hardware coordinates to screen centers; threshold conditions independently expressed. |
| H5 | One point/object, two decimal score digits | code: 1276-1308 | Display score modulo 100, keep total pockets separately for diagnostics. |
| H6 | Scratch terminates segment; timer starts at 30, updates every 64 RTC increments | code: 467-528, 1309-1333 | Preserve clock phase and zero-before-transition ordering; scratch sound/delay omitted. |
| H7 | P1 then P2, advance heat after P2; configurable 2-5 heats | code: 453-517 | Default two heats. Higher displayed score wins/tie draws is design evaluator interpretation; no score-comparison branch verified. |
| H8 | Clearance reracks, extended play adds 15 once per segment | code: 529-550 | Immediate next-frame rack reset; bonus flag survives clears and resets on segment change. |
| H9 | Compact monochrome table, score/time/rack and player arrows | code: 877-1013, 1065-1101; PSDIAG.INS 166-171 | Original canvas primitives/fonts only, no graphics/audio copied. |
| H10 | Five operations, detached public context, fixed control intervals and limits | design: RULES.md historical interface/limits | 64 frames per offline control, one per GUI frame; hidden internals excluded. |

`assumed`: supplied 1976 program matches production 1977 timing/behavior;
not established. 60 logical frames/second is a hardware-rate working assumption
used for presentation, not an observed cabinet measurement. No `observed`
historical gameplay label is claimed. H3 and H9 approximations are `design`.

## Six-ball version (preserved backup)

Every gameplay and interface rule in specification v1 is indexed below.
`design` means an intentional specified choice, not verified historical behavior.
Historical `code` evidence supports the cited reference mechanism only, not
the numerical parameters or adaptations of this implementation.

| ID | Rule / choice | Label and specification locator | Historical reference / adaptation |
| --- | --- | --- | --- |
| R1 | Table, pockets, six-ball layout, IDs, initial scores/player/seed | design: RULES.md, R1 | Six replaces fifteen. Independent coordinates; do not copy `BINIT`. Historical rack: code, A7329.XX BRACK 641-681. |
| R2 | Integer degree direction and three powers; validation | design: RULES.md, R2 | Replaces continuous control: code, A7329.XX 551-639. |
| R3 | Fixed timestep, collision order, equal-mass impulses, rails, friction, pocket capture, settle/cap | design: RULES.md, R3 | Mechanism references: code, A7329.XX PLAY 1208-1275 and WALCKE/COLCHK 1334-1507. All new numeric parameters are design. |
| R4 | One point/object; scratch voids shot score; removals and automatic respot | design: RULES.md, R4 | Scoring/removal and distinct scratch path: code, A7329.XX SCORE/SCACH 1276-1333. No claim historical scratch penalty equals ours. |
| R5 | Alternate after every shot; invalid attempt and actor handling | design: RULES.md, R5 | Preserves competition, replaces historical player/heat switching paths (code, A7329.XX SRATST 496-517). |
| R6 | Clear table / 24 attempts, score comparison, draw, precedence | design: RULES.md, R6 | Replaces historical timer/heat modes. Reference: code, A7329.XX 467-549; PSHARK.MAP time switch entries. |
| R7 | Call, request, simulation and episode limits; failure outcomes | design: RULES.md, R3 and R7 | Evaluation/runtime policy, not historical gameplay. |
| R8 | Five operations, full observation, legal vocabulary, role checks, detached snapshots | design: RULES.md, R8 | Course interface adapted to competitive billiards. No private evaluator data is player input. |
| R9 | Modes, geometric baseline, current observation vs two-record history | design: RULES.md, R9 | Experiment choices, not historical rules. |

## Implementation and acceptance locators (v0.2.0)

| Rule | Executable locator | Test locator |
| --- | --- | --- |
| R1 | pool/engine.py: DEFAULT, Episode.reset | test_pool.InterfaceTests.test_reset_isolation_and_boundary |
| R2 | pool/engine.py: Episode.valid, legal_actions | test_pool.InterfaceTests.test_invalid_and_wrong_seat |
| R3 | pool/engine.py: tick, Episode.step simulation loop | test_pool.PhysicsTests (all); InterfaceTests.test_determinism |
| R4 | pool/engine.py: Episode.step scoring/respot | test_pool.InterfaceTests.test_scratch_respot_and_turn, test_scratch_voids_object_points |
| R5 | pool/engine.py: Episode.step, _finish_attempt | test_pool.InterfaceTests.test_invalid_and_wrong_seat, test_seeded_match_invariants_and_miss_turn |
| R6 | pool/engine.py: _finish_attempt, outcome | test_pool.InterfaceTests.test_score_clearance_and_precedence, test_attempt_and_simulation_limits |
| R7 | pool/runner.py: run_match; pool/model.py: ModelPlayer.decide | test_pool.RunnerTests.test_episode_deadline; test_model.ModelTests (budget, timeout, failures) |
| R8 | pool/engine.py: five methods; pool/model.py: build_context | test_pool.InterfaceTests.test_reset_isolation_and_boundary; test_model.ModelTests.test_public_context_and_history_budget |
| R9 | pool/ui.py: TableApp; pool/baseline.py: choose/direct | test_ui.UITests; test_pool.RunnerTests.test_trace_replay_and_seats |

Live provider transport and Human vs Model remain pending. Execution-error
metadata belongs to the runner; policies never receive the episode object.
The settled UI and headless runner share the same step implementation.

Before each
implementation change, quote the applicable row, write and run the failing
test, then add code/test locators without replacing the historical evidence.
Never label a deliberate adaptation `assumed`. Unverified historical inferences
must be separately labeled `assumed` if introduced.
