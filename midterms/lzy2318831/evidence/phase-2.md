# Phase 2 implementation evidence

Student authorization: approved the six-ball competitive scope and requested
Phase 2 implementation, playable Human vs Human/Human vs Baseline, offline
baseline/runner/tests, then preparation for live integration without paid calls.
Implementation assistant: Codex in the current conversation; actual shareable
session URL still must be linked by the student. No independent review claimed.

## Named skill and test-first sequence

Invoked **competitive-rule-change** by name at the start of this implementation
turn, and read its saved SKILL.md. Applicable map rows: R1 table/initial state,
R2 shot vocabulary, R3 physics, R4 scoring/scratches, R5 turns/invalids, R6 ending,
R7 limits, R8 interface, R9 modes/baseline. Each has label `design` and points
to the corresponding RULES.md section; historical references remain separate.

Wrote test_pool.py before creating the pool package. Actual initial command:
`python -m unittest discover -s tests -v`, exit 1, import failed with
`ModuleNotFoundError: No module named 'pool'`. This was an absent-implementation
failure, not eleven individually executed rule assertions. After implementing
engine, baseline and runner the eleven assertions/tests executed and passed.
Wrote test_model.py before creating model.py: actual import failure
`ModuleNotFoundError: No module named 'pool.model'`; then implemented the
prepared boundary and verified its tests with fake transports only.

Actual acceptance traces include: cue (500,150), object (500,60), shot
angle 270/power 1 with attempt cap 1 -> p1 score 1, table_cleared, p1 winner;
same active-player malformed action -> no ball/score changes, invalid +1,
attempt +1, p2 active. Wrong-seat actions change nothing. Scratch fixture
cue (500,60), object (800,250), shot 270/1 -> no score, scratch +1, cue respots
(250,250), p2 active. These are automated fixtures, not human observations.

Two actual red regression assertions and fixes are preserved in REGRESSIONS.md.
Final deterministic project run: **20 tests passed**, Python 3.15.1,
`python -m unittest discover -s tests -v`. Full latest output is in
project-tests.txt. Covers physics/score/turn/state boundaries, seeded match
invariants, limits, replay, model failures/timeouts and widget controllers.

The Phase 1 and Phase 2 invocations are distinct user-authorized phases within
one conversation. Do not call that two independent assistant sessions without
supporting session records; another distinct skill-use session is still needed.

## Offline development results

Default D0 only; no frozen S1/S2/S3 matches or tuning. Real local traces:

- dev-baseline-p1.json: geometric 5, direct aim 1; table_cleared at attempt 19.
- dev-baseline-p2.json: direct aim 2, geometric 4; table_cleared at attempt 24.
- dev-baseline-self.json: 3-3 draw; table_cleared at attempt 9.

All have zero invalid actions, no execution failure, no model calls. The
direct-aim p1 scratches once. These deterministic runs do not establish a
statistical advantage. Replay of the saved JSON trace was checked successfully.

## View verification limits

Implemented tkinter canvas, direction arrow, exact angle field, power controls,
scores, turn, attempts, result overlay, shot preview, restart, both offline
human modes. Actual GUI launch produced a window titled
`Six-ball Pool — competitive billiards` in the desktop window inventory.
Computer-use capture failed with `foreground window did not report a process
id`; recovery did not find a persistent target. No visual screenshot check or
human playtest is claimed. Automated widget-controller tests (mock widgets)
completed a Human vs Baseline match and restart, and tested Human vs Human
aiming/turns. They do not prove visual usability on the student's display.

## Root checks and boundary

Ran repository-required root unittest command: 36 collected entries, 32 passed,
4 errors: two provider-test imports lacked `anthropic`, two minigame symlink
tests lacked Windows privilege (WinError 1314). Root offline/headless setup
was incomplete: GitHub authentication, Pyxel engine, and root tests failed;
fixture/Python/Git checks passed. No live call was substituted. These are
existing environment limitations, not billiards test failures. Shared files
and runtime installations were not changed to repair unrelated setup.

Only submission files and the named workflow were edited. Workflow added but
not pushed/run remotely, so no remote CI pass is claimed. No API calls, merge,
gate approval, external posting or paid evaluation occurred.

## Independent review handoff (pending separate reviewer)

Review RULES.md R1-R9, rule-source-map.md, pool/engine.py, baseline.py,
runner.py, model.py, ui.py, tests/, workflow, and this evidence. Check that
code/test/spec agree, the physical simplification and scratch policy are
explicit, state stays runner-owned, no policy gets private tools, failures
count, and all five CI check kinds exist. Pay special attention to dense
multi-contact geometry, scratch-plus-final-pot scoring, hard provider timeout,
and replay integrity. Report findings read-only; do not approve.

Remaining: provider transport/live mode and dated budget, live trials and
memory comparison, distinct-session skill evidence, independent review,
actual visual/human playtest, student's own reflection/log, recording and
submitted-version remote CI. No historical copying or source license grant
is claimed; original creator attribution remains to verify.
