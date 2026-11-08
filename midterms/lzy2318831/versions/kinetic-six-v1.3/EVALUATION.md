# Arcade Fusion evaluation — suite 1

## Declaration and separation

Current table: Aurum Circuit, fusion-1.1.0-aurum, suite 2. Its device/layout
amendment was declared in fusion/evaluation.json before implementation or
baseline adjustment. Two old bumper-case balls were moved out of the new
bumper footprints; the previous suite is preserved in versions/fusion-v1/.
No held-out policy performance trials were used to tune this pass. Current
default-layout development results and UI QA are in evidence/polish-1/REPORT.md.
The v1 match results below apply to the archived two-bumper version only.

The exact three situations in [fusion/evaluation.json](fusion/evaluation.json)
were recorded before Fusion policy implementation/tuning. The ordinary triangle
is development-only. The frozen cases are direct pocket opportunities,
bumper-assisted opportunities, and obstructed/scratch-risk shots. Do not tune
using their results and then describe them as held out.

This is a new original game. Earlier six-ball and historical results are
preserved in versions/pre-fusion/ and their evidence files, and do not validate
Fusion. No live model trial has occurred.

## Future live protocol (requires explicit paid-call approval)

At least two fresh live matches per situation, reversing model/baseline seats,
seeds 101/102, identical rules, observations, actions and six-shot quotas.
Run the baseline on matching cases. Compare observation-only with last-two-shot
public history on matched cases; explain whether memory helps this fully
observed game. Keep model, prompt, configuration and game hashes fixed within
a comparison. One provider suffices. No repair calls, automatic paid retries,
silent fallbacks or fabricated wins.

Record per trial: case/seed/seats, game/config/prompt IDs, requested/resolved
model IDs, W/L/D or execution failure, scores/pots/bumper/combo points, scratches,
invalid actions, shot/call/timeout limits, latency, token categories, dated
price source and estimated cost, and trace link. Unknown usage is unknown, not
zero. Include failed calls/trials in denominators; a classroom sample does not
establish statistical certainty. A narration-only model is not the player.

Limits prepared: twelve opportunities and at most twelve model attempts per
match, failed attempts included, 20-second hard request timeout and 300-second
match deadline. Exceptions/refusals/unusable responses terminate with explicit
failure reason and no competitive winner. No live transport is configured;
the GUI exposes only Human vs Human and Human vs Baseline.

## Actual development checks (not held-out/model results)

Default triangle only, seed 101, fusion-1.0.0:
- Geometric P1 vs direct P2: 330–200; twelve opportunities, table_cleared.
- Direct P1 vs geometric P2: 0–345; twelve opportunities, shots_exhausted.
- Zero model calls; no API tokens/cost. Traces are development evidence, not
  independent random samples or proof of superiority over a model.

Final executable results, test logs, browser evidence and any regressions are
recorded in evidence/FUSION-SLICE.md. CI is configured but has not run remotely
for a submitted commit. Independent review and a human playtest remain pending.
Browser automation is application QA, not a human playtest or model trial.

## Limitations and student authorship

This is an assistant-authored protocol, not the student's final reflection.
The student must write the final limitations and interpretation in their own
voice after actual play and evaluation. Current limits include simplified
2-D equal-mass physics without spin, approximate geometric policy predictions,
small fixed layouts, and no live-model result yet. Recording link: pending.


Aurum independent read-only review is complete; see
evidence/polish-1/INDEPENDENT-REVIEW.md. Student gate acceptance and human
playtest remain pending. Before live evaluation, strengthen trace identity
to include devices.py and geometry.py as well as engine.py.

Grand Circuit supersedes Aurum results; suite3 changes only physical placement
clearance (record: evidence/maximal-1/layout-clearance.json), with Aurum suite
preserved. No held-out policy trial or tuning ran this turn. Development shot
sweep is physics QA only. Trace hash now covers engine/devices/geometry in both
run and replay. New max9600ticks40sec, six shots each, same model-call budget.
Live repeated trials, human playtesting and recording remain pending.

## Current Kinetic protocol amendment

Version fusion-1.3.0-kinetic, suite4. Only physically overlapping ball placements
were relocated, no held-out policy trials or tuning (layout-clearance.json).
Grand suite and implementation preserved in versions/grand-v1.2/. Same frozen
three scenario purposes, two live trials each, seats/call-budget plan; live
runs remain unapproved/unexecuted. Ordinary shared-observation baseline updated
for public varying bumper radius/impulse. Detailed mechanism plans approximate.

Development comparison: same24default shots, angle0..345step15,power85. Grand
mean cue bumper hits3.9167 vs Kinetic8.7917; mean cue bumper/rail contacts13.9583
vs24.0. Physical contacts include repeated passive reflections, not only paid
score events. Both versions zero simulation failures; Kinetic mean simulated
duration10.116sec vs8.484sec. Data: evidence/kinetic-1/chain-comparison-final.json.
This supports collision-rich motion on this shot grid, not general game quality,
a statistically independent study or AI superiority. No held-out data used.

Two default-layout development matches seed101: baseline(P1)390 vs direct570;
direct(P1)490 vs baseline440. Both12shots_exhausted, no execution failure, first
replay verified. Baseline lost both; high scratch rates show it is not an expert
planner for powered chains. Do not substitute these for the required live
model evaluation or human playtest. More human review is needed before tuning.
