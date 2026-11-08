# Six-ball Pool: Pool Shark-inspired competitive billiards

GitHub login: `lzy2318831`. Status: Phase 2 offline implementation v0.2.0.

## Scope

Build an original implementation of a small two-player billiards match inspired
by Pool Shark. Six object balls and a cue ball move on a six-pocket table.
Players choose direction and power; the engine resolves collisions, cushion
rebounds, friction, and pocketing. Each object ball scores one point, except
that a scratch voids points from that shot. Turns alternate after every shot.
The higher score wins when the table is cleared or after 24 attempts; equal
scores draw. Support Human vs Human, Human vs Model, and Model vs Geometric
Baseline, with Baseline vs Baseline for offline verification.

This replaces the earlier three-ball single-player proposal. It preserves
competition and scoring while bounding implementation and API expense. Six
balls are the committed scope; fifteen balls, continuous joystick control,
historical coin/timer modes, advanced spin, tournaments, networking, elaborate
animation, and copied artwork/audio are excluded. Changing the count is a
scope/evaluation amendment, not an unrecorded tuning decision.

The historical program updates cue-ball velocity from joystick readings during
simulation. Discrete shots, fixed alternating turns, scratch handling, six-ball
layouts, and the attempt limit are our intentional adaptations. This is not a
claim to reproduce historical rules exactly. Original design and reconstruction
are both eligible under the assignment.

## Specification and evidence

- [Rules and five-operation interface](RULES.md)
- [Rule/source map](rule-source-map.md)
- [Historical provenance and reuse record](SOURCES.md)
- [Predeclared evaluation](EVALUATION.md)
- [Implementation phases and rubric checklist](PLAN.md)
- [Live integration preparation](LIVE-INTEGRATION.md)
- [Agent configuration](agent-config.json)
- [Agent instructions](AGENTS.md)
- [Reusable skill](skills/competitive-rule-change/SKILL.md)
- [Independent review instructions](agents/rules-reviewer.md)
- [Student team-log worksheet and evidence status](AGENT-TEAM.md)
- [Human playtest protocol](PLAYTEST.md)

## Setup, play, tests, and offline evaluation

From the repository root, change directory once:

```powershell
cd midterms/lzy2318831
```

Every command below runs from that project directory. Use Python 3.11 or
later (`python3` on systems that use that name). Offline play/evaluation has
no pip dependencies. The desktop view uses the CPython standard-library
`tkinter` binding: choose the Python installer's Tcl/Tk option on Windows/macOS;
on Linux install your distribution's matching Python Tk package if absent.
The headless runner does not require a display. The UI controller tests import
tkinter but mock widgets; they require the binding, not a running window.

```powershell
python --version
python -c "import tkinter; print(tkinter.TkVersion)"
python -m pool.ui --mode hvh
python -m pool.ui --mode hvb
python -m unittest discover -s tests -v
python -m pool.runner --p1 baseline --p2 baseline --seed 101 --trace evidence/my-match.json
python -m pool.runner --p1 baseline --p2 direct --seed 101 --trace evidence/my-comparison.json
python -m pool.runner --replay evidence/my-match.json
```

`hvh` is Human vs Human; `hvb` is human P1 versus geometric baseline P2.
Move/click on the table to aim; an arrow shows the direction. Choose power
1/2/3, then click Shoot or press Space. Left/Right adjust one degree; the
direction field supports exact angles. R/Restart starts a new match; Escape
closes. Scores, turn, remaining attempts and final result are visible. Ball
movement previews run quickly; all physics is fixed-step independent of view.

The direct-aim policy is a weaker diagnostic opponent, not the primary
baseline. To swap seats use `--p1 direct --p2 baseline`. Seeds are recorded
for reproducibility; the fixed default layout and policies consume no random
numbers, so changing a seed alone does not create an independent trial.
Replay checks action acceptance, events and public post-shot snapshots.

See [Phase 2 evidence](evidence/phase-2.md) for actual test results and limits.
No provider has been chosen and no live player calls have been made. The
prepared model boundary in `pool/model.py` uses injected transports, enforces
an interruptible timeout, and is tested with fake responses only. A real
provider transport, live CLI/view mode, dated cost cap and paid-call approval
remain pending. Human vs Model is not yet available.

## Submission status

Required but not yet produced: live model player/evaluation, green remote CI
for the submitted version, independent review findings, distinct-session skill
evidence, anonymous observed human playtest, student-written reflection, and
a three-to-five-minute recording. The offline game, baseline, tests, local
traces and deterministic workflow are implemented. Recording link: pending.

Submit one PR targeting `columbia-university-ai-games/game-dev-f26:main`, and
its URL on CourseWorks by November 7, 2026, 11:59 p.m. The PR must link this
README, evaluation, team log, playtest notes, and recording. Staff handle merge.
Only this folder and `.github/workflows/midterm-lzy2318831.yml` may change.
The midterm requires no Asana links. The student must update their Week 3
thread to reflect the revised scope; this document does not post that update.
