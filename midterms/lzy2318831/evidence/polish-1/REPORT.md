# Aurum Circuit: focused polish evidence

Date: 2026-11-06. Version: fusion-1.1.0-aurum. Original design; no historical
fidelity claim, imported historical assets, paid calls, push or submission.
Student gameplay/visual acceptance remains pending.

## Actual implementation and skill use

The implementation assistant invoked **competitive-rule-change** by name in
this conversation, read skills/competitive-rule-change/SKILL.md, and declared
P1?P5 in fusion/POLISH-RULES.md and the primary rule map before engine changes.
This is not proof of two distinct sessions. A fresh read-only reviewer was
requested after implementation; findings are recorded separately when returned.
No agent can approve the student's gate.

Four perimeter bumpers, ten passive capsule guides, two return sensors and a
traversable Orbit spinner enrich one table. Scoring is bounded: cue bumpers
15 each, returns 10 each, Orbit 25 once and 2x later pot base values only.
Maximum device-only points: 105/shot. Scratch voids all shot points. Central
space, six alternating opportunities and angle/power controls remain intact.
Devices are public observation data; the baseline avoids guide geometry using
only the same public state. No hidden search rollout or model call was added.

## Executed tests and observations

- Test-first: new polish suite initially failed import because fusion.devices
  did not yet exist. This was a collection failure, not individual red tests.
- New spinner behavior exposed an old fixture mismatch: the top-middle pot
  earned 225 rather than 100, correctly crossing Orbit first. The plain-pot
  fixture now targets the lower pocket and still requires 100; the new full
  spinner-assisted-pot test preserves the old path and requires 225.
- Current full project suite: **66 tests, OK**, 11.634 seconds. Raw output:
  tests.txt. Includes device collisions/sensors/caps/order, scratch voiding,
  multiplier reset, isolation/boundaries, frozen-layout clearance and old tests.
- Runnable archived v1 suite: **55 tests, OK**, 5.470 seconds. Raw output:
  preserved-v1-tests.txt. SHA256: all 36 snapshot files and all 18 earlier
  preservation-manifest files unchanged; see preservation.txt.
- Default-layout development shot grid: 24 angle/power combinations, no
  execution failures; shot-grid.json. This is development coverage, not live
  AI evaluation or held-out benchmark performance.
- Default-layout offline matches: baseline(P1) vs direct(P2), 310?0;
  direct(P1) vs baseline(P2), 160?85. Both ended shots_exhausted after 12
  opportunities without execution failure. The first trace replay passed.
  See development-p1.json and development-p2.json. These two matches do not
  establish policy superiority. Frozen suite2 cases were not tuned or scored.
- Isolated headless Chrome application QA against localhost:8766 passed real
  mouse drag/power, bumper and lane events, playback input lock, autonomous
  baseline reply, full ending, Orbit activation and next-shot multiplier reset,
  and delayed-response restart regression. Four bumpers/ten guides observed;
  no JavaScript exceptions. Browser report: fusion-browser-check.json.
  End-screen playback was accelerated only to reach the complete ending;
  this is automated application QA, not a human playtest.
- Visual inspection of captured table confirmed the clear center, layered
  mechanical housings, rails, gold trim and cyan/gold palette. QA found mirrored
  right-lane text and 723px content at a 720px viewport. Text transform and
  header padding fixes were applied; rerun reports 720px laptop fit. Screenshots
  include fusion-table.png, fusion-laptop.png, fusion-in-motion.png,
  fusion-game-over.png and aurum-orbit-active.png.
- Root offline setup diagnostic remains incomplete: GitHub authentication,
  optional Pyxel and root starter tests fail. Python/Git/scripted fixture pass.
  These are separate from the 66 passing dependency-free project tests.
  No fixture was substituted for a live model result. git diff --check passed.

## Stop and outstanding evidence

One table only; no further optional features before student review. The
localhost:8766 server was launched for review. Start from this project folder:
`python -m fusion --port 8766`. Aim, press and pull backward, then release;
Escape/right-click cancels. Try banking through a side return and sending the
cue through the top Orbit gate before pocketing an object. The channels are
passive; a ball can stop inside and be shot from there. Feedback is visual;
no audio was added. Physics is deterministic 2D, not full spin simulation.

Live model trials, human playtesting, recording, remote CI and a second actual
skill session are still outstanding. Earlier Fusion and historical results
remain separate and must not be relabeled as Aurum evaluation.

Independent review completed: INDEPENDENT-REVIEW.md. No blocking gameplay
findings; independently ran 11 polish tests successfully. Stale handoff fixed.
Known trace identity limitation: engine_sha256 excludes devices.py/geometry.py;
aggregate identity should be added before live evaluation. This is not gate approval.
