# Geometry-assisted stabilization

Offline repair only. No paid requests, physics changes, commit, push or PR.
Session: `01a1b6ef-6f18-72c2-9249-e06f0ee80045`.

## Verified navigation defect and repair

The generic navigation controller appended a result Back button while live.js
also reused `#playAgain` as Back. Both handlers could wait indefinitely for
`/live/leave` and navigation discovery. `LiveSession.leave()` also waited behind
the session lock during simulation/persistence. No historical browser network
capture establishes which exact wait trapped the student's original page.

Geometry mode now serves `geometry_navigation.js`, reusing one existing button
and moving it to the active panel. It navigates to the server-provided validated
local menu after at most a 1.5-second cancellation wait, even if the leave request
hangs. Backend leave signals cancellation before bounded lock/join waits and
reports settlement separately. Preparing another match still requires the old
worker to be dead, a current token and fresh consent; cumulative accounting is
preserved. Menu budget/settlement information is nonblocking. No request retry or
automatic substitute action was added. Failures display match incomplete.

## Verified simulation failure

Source: [genuine trace](../live-browser-geometry-v1/20261107T215634Z-8dbde2c0c71f/trace.json).
Total shot 7 / LLM shot 4 selected candidate 2: angle 266, power 4, target 5.
Cue (365.3569,302.2751), target (362,250), initial contact about 30.4 units away.
Initial cue speed 128 is low. First powered event was object 5 / bumper 7 at
0.8875 seconds; later powered rail/sling interactions sustained motion.
The saved shot contains 511 events through 39.929 seconds and reaches the
9,600-tick / 40-second cap with objects still moving. Exact offline replay
reproduced the failure. This is an extended powered cascade, not proof of an
infinite loop or an engine termination bug. Increasing the cap is not the fix.

The next genuine trace records `playback_ack_timeout`; it is a separate browser
acknowledgment failure. Its available evidence does not prove why acknowledgment
was absent. Historical traces have not been edited.

## Proposal corrections

Contact/bank estimates now reserve 15 rather than 60 units of object runout and
omit the extra 4% launch-speed margin. Minimum reach, collision transfer,
cushion loss, clearance, quantized angles and scratch screening remain in place.
Device-only candidates are omitted when a direct contact or pot route exists;
banks and escape choices remain supported. The LLM still selects a listed ID,
which is strictly validated before execution. No Smart/Geometric action replaces
that selection.

[Frozen-simulator comparison](shot-comparison.json): at the exact failing
position, 266/power 4 remains unsettled at 9,600 ticks; the current contact
proposal 266/power 1 settles in 354 ticks without a foul or pot. Powers 2 and 3
also settle in this position. This is a targeted regression result, not a claim
of stronger play or universal settlement. No runtime simulator was added.

[Saved-observation coverage](coverage.json): 34 historical genuine browser
observations, 16 direct contact/pot routes, 18 contact routes including banks,
no empty candidate lists. This is geometric coverage, not actual pots or wins.

## Before/after regressions

Before edits, `tests/geometry-navigation.cjs` failed with two result Back owners
(`2 !== 1`) and a null destination after hung leave. The new Python stability
tests failed because leave blocked behind the session lock and the known
266/power-4 proposal was still offered. These failures were actually executed
in this session before the corresponding fixes. After repair both checks pass,
including the exact replacement shot settling in the frozen simulator.

Actual Chrome + actual loopback HTTP, synthetic model responses only:

| Evidence | Verified lifecycle |
| --- | --- |
| [Two matches and exhausted budget](two-matches-budget/summary.json) | 12 shots then 12 shots on the same running server; one visible Back; reopening at 12 cumulative requests disables start; Back still returns |
| [Physics failure recovery](failure-recovery/summary.json) | Exact historical action prefix causes real local simulation_limit at shot 7; one visible Back; deliberately hung leave cannot trap browser; fresh 12-shot match completes on same server |
| [HTTP failure](browser-http_error/summary.json) | Incomplete failure, Back, fresh 12-shot match |
| [Invalid selection](browser-invalid_candidate_selection/summary.json) | Incomplete failure, Back, fresh 12-shot match |
| [Timeout](browser-request_timeout-final/summary.json) | Parent watchdog timeout, Back, fresh 12-shot match |
| [Cancellation](browser-user_cancelled-final/summary.json) | Cancelled in-flight synthetic request, Back, fresh 12-shot match |

The historical failure fixture deliberately offers the old proposal sequence in
the QA policy only, so the real engine failure remains reproducible after the
production generator filters that proposal. It does not bypass candidate-ID
selection. Rendering time is accelerated and mock confirmation is accepted by
the QA stub; simulation, HTTP, session lifecycle and request accounting are real.
[Selection proof](browser-selection-proof.json) checks all 46 executed P1 actions
against their recorded selected IDs and candidate angles/powers. No real model
inference or performance evaluation is claimed. The first HTTP/invalid summaries
have a generic `shots_each:12` field; their detailed outcomes and the consolidated
proof correctly record 0 then 12 shots. The first timeout harness attempt expected
`request_timeout` rather than the actual `parent_watchdog` reason and failed its
assertion; the corrected test accepts the existing timeout aliases.

## Validation and independent review

- Project Python: [194 tests, OK](python-tests.txt).
- JavaScript: replay timers, generic navigation, live controller, geometry
  controller and new geometry navigation all pass.
- [24 historical replays](replay-verification.json): verified unchanged official
  results, 11 complete / 2 wins / 9 losses.
- All 18 frozen gameplay/visual artifacts pass `python -m fusion.freeze`.
- [497 prior hashes](preservation-result.json): no changes.
- Root starter suite: 36 tests, four environment errors (missing `anthropic`
  for two imports, Windows privilege 1314 for two symlink tests), including
  an elevated rerun. See [root log](root-python-tests-elevated.txt). Unrelated
  dependencies/tests were not modified.

The actual `competitive-rule-change` skill was invoked and read. Independent
read-only reviewer `/root/geometry_review` reported no blocking findings,
independently passed three stability tests, the navigation JS check and 18 freeze
checks, and reproduced 266/power 4 versus power 1. The reviewer confirmed fresh
match guards preserve worker settlement, token rotation and cumulative budgets.
No student/course gate was approved by an agent.

Remaining limits: no genuine post-repair LLM performance measurement; future
powered cascades and scratches remain possible. Cancellation delivery cannot be
guaranteed during a network outage, but navigation is bounded and no new request
is authorized by returning. Menu cached status can briefly lag settlement;
authoritative start guards still apply. Restart the old Python process once to
load this code; subsequent match/menu cycles do not require a server restart.


## Git preparation

Branch `lzy2318831/midterm`. Scoped stabilization changes and supporting evidence
are staged alongside the previously prepared submission. Final scope/credential
scan found no paths outside the permitted project/workflow, credential patterns,
caches, virtual environments or temporary files. Local Markdown targets checked:
94, all resolve. Existing archived CRLF/trailing-space/blank-EOF warnings remain;
their bytes are preserved rather than reformatted. No commit, push or PR made.
