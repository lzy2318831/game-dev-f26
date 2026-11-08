# Arcade Fusion vertical-slice evidence

Implementation assistant: Codex, this user-authorized conversation turn.
Student decision: original Pool + Pinball game, six objects/two bumpers,
turn-based drag shots, premium presentation; stop at playable slice for review.
Session link must be supplied by the student. No independent review claimed.

## Named skill and test-first work

Invoked **competitive-rule-change** by name in the opening commentary and read
the saved skill. Created fusion/RULES.md F1–F9, the design-labeled rule map and
three-case frozen evaluation.json before Fusion engine/baseline implementation.
Wrote tests/test_fusion.py first; actual first run failed to import
fusion.engine (absent implementation). The eleven initial tests then executed
and passed after engine/runner/baseline implementation. This absent-package
failure is not falsely described as eleven executed failing assertions.
Later server/player tests were also written before their respective modules.

Final project unittest run: **55 tests pass**, including the 40 preserved
earlier-version tests and 15 Fusion tests. Exact latest output is saved in
fusion-tests.txt. Covers collision momentum, friction/rails/pockets, bumper
impulse/scoring caps, combo/foul scoring, invalid/wrong-seat behavior, state
isolation, quotas/ending, simulation cap, render-independent determinism,
replay, model-context/budget/failure handling and UI playback lock/modes.

The named skill has been invoked in multiple phase turns of one conversation.
That is not proof of two distinct sessions. A separately evidenced second
session and independent non-author review remain necessary for the rubric.

## Actual browser verification

Local service launched with python -m fusion, binds 127.0.0.1:8765. Default
browser URL launch returned successfully. The ordinary browser connection was
unavailable and native Chrome recovery could not restore a minimized window;
no success is fabricated for that tool path.

An isolated headless Chrome using a project-local QA profile rendered the app.
Inspected actual screenshots: original start screen, live table, laptop table,
motion/feedback and game-over. The Python standard-library browser_check.py
test drives this isolated app with Chrome DevTools; it does not access normal
user tabs. No external game assets or browser-testing pip packages required.

Actual passing check: mouse aim/press/drag/release charged 67% power, triggered
a cue bumper, played the shot, and automatically executed the geometric
baseline's own reply. It observed scores/quotas after both turns. A complete
scripted Human-vs-Human twelve-opportunity match reached its result screen
(15–15 draw in this diagnostic sequence). Only presentation playback was
time-accelerated for the end-screen check; physics still ran in Python.
Desktop 1440×1100 and laptop 1280×720 layouts fit; zero JavaScript exceptions.
Actual report: fusion-browser-check.json. This is automated application QA,
not a human playtest, a model evaluation or statistical gameplay evidence.

## Actual regressions and fixes

1. **Viewport overflow.** Initial table design required scrolling. The browser
   layout assertion then reproduced 1104 px content at a 1100 px viewport and
   757 px at the 720 px laptop viewport. Responsive width/spacing adjustments
   now pass both exact viewport assertions. Screenshots preserve actual output.
2. **Restart/late-response race.** With a 300 ms delayed shot response, the
   actual red test printed staleMovie=true, busy=false, shots={p1:6,p2:6} after
   restart and raised 'Late shot response leaked into restarted match'. Added
   match-generation tickets to reset/fire/playback completion so stale replies
   cannot overwrite a new match. Same test now reports staleMovie=false,
   busy=false, fresh six/six quotas. No fabricated regression or review.

The browser check also explicitly selects its test mode: a previous QA session
can retain Human-vs-Human mode. Mode selection is synchronized from app state.
Earlier failed browser-test setup attempts are not live-policy trial results.

## Offline development matches

Default triangle only, seed 101; frozen direct/bumper/risk layouts were not
used for performance tuning. Baseline P1 vs direct aim P2: 330–200,
table_cleared at opportunity 12. Reversed policies: 0–345, shots_exhausted at
12. Zero model calls/cost; both traces replay. These deterministic diagnostic
matches do not establish model superiority or a statistical win rate.

## Preservation and boundaries

Preserved pool/, historical/, their five original test files and all existing
evidence. Verified all 18 source/test hashes in versions/pre-fusion/
preserved-hashes.json unchanged. Saved pre-Fusion primary documents/config and
workflow before updating the final project's primary documentation. Only the
student folder and permitted workflow were edited; no original source archive
modification, paid call, external posting, push, PR or submission occurred.

No live player transport is enabled. Model hooks are tested with labeled fake
players and count failed attempts; they are not real-model evidence. Root
starter diagnostics have separate environment prerequisites; latest root-check
output is recorded separately and must not be called a Fusion test failure/pass.
The latest root run had 32 passing entries and four errors: two missing
anthropic SDK imports, and two Windows symlink-privilege errors. Root offline
setup also reported missing GitHub authentication and Pyxel engine readiness.
No shared dependency/runtime/security settings were changed to repair those
unrelated prerequisites. Fusion's standard-library game and 55 project tests
run successfully. See fusion-root-checks.txt for actual output.

## Stop point and limitations

Await student gameplay/visual review. Known scope limits: no spin/advanced
cloth simulation, approximate geometric predictions, no sound or Human-vs-LLM
mode, no live results or independent review. Original graphics are procedural;
the guide predicts first geometric contact only. A human playtest, recording,
student-written reflection, remote CI and final PR remain pending. No new
optional features or paid evaluations are authorized at this checkpoint.
