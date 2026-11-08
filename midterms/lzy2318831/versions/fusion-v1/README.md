# Pool + Pinball: Arcade Fusion

An original two-player arcade billiards game by lzy2318831. This is a Pool
Shark-inspired adaptation, **not a historical reconstruction**. Status:
playable vertical slice, awaiting the student's gameplay and visual review.

## Play on Windows

Python 3.11+ and a modern Chrome/Edge/Firefox browser are sufficient. No pip,
Node, Pygame, model credentials, build step, external fonts or assets required.

From PowerShell:
```powershell
Set-Location 'C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831'
python -m fusion
```

Keep that terminal running. Open [the local game](http://127.0.0.1:8765).
If the port is occupied, use `python -m fusion --port 8766` and open port 8766.
The service binds only to 127.0.0.1. Ctrl+C stops it. Every command below runs
from the project folder shown above, not the repository root.

Choose VS BASELINE or 2 PLAYERS, then LET'S PLAY. Point to aim; press on the
table, pull backward along the cue line, and release. Pull farther for more
power. Tiny drags cancel. Right-click or Escape cancels. The guide shows first
contact, not a guaranteed future trajectory. Watch the shot finish before the
next player acts. New match resets the table. The baseline chooses its own
moves; humans never choose its shot.

## The complete loop

One cue ball, six objects, six pockets, two powered bumpers. Each player has
six alternating opportunities. A pot earns 100; a distinct cue-ball bumper
earns 15 once per shot; a pot after a bumper adds 50, as does each additional
pot in that shot. A scratch voids all shot points and respots the cue. Clear
the table or exhaust twelve opportunities; higher score wins, ties draw.
Repeated bumper contacts have scoring and energy caps. See [exact rules](RULES.md).

Navy/blue felt, metallic gold rails, illuminated cyan/gold bumpers, shaded
balls, cue/aim/power feedback, contact effects, scoreboards and a result screen
are generated with original Canvas/CSS code. Python owns physics and score.
The browser interpolates recorded 60-Hz snapshots from 240-Hz physics; render
rate cannot change game results.

## Test and run offline matches

```powershell
python -m unittest discover -s tests -v
python -m fusion.runner --p1 baseline --p2 baseline --trace evidence/my-fusion-match.json
python -m fusion.runner --p1 baseline --p2 direct --seed 101 --trace evidence/my-fusion-comparison.json
python -m fusion.runner --replay evidence/my-fusion-match.json
```

Fusion tests/headless matches use only the standard library. The full test
command also imports tkinter for preserved earlier-version UI-controller tests;
the normal Windows Python installer includes it. On Linux, install the matching
Python Tk runtime if you want to run those backup tests.

Seeds identify fixed-layout deterministic replays; changing a seed alone does
not produce a distinct randomized trial. The credible baseline uses direct-pot
ghost geometry plus bounded bumper-route candidates; direct aim is a weaker
diagnostic opponent. They share the same observation and angle/power vocabulary.

## Evidence and next decisions

- [Frozen evaluation and honest results status](EVALUATION.md)
- [Rule/source map](rule-source-map.md), [source and reuse record](SOURCES.md)
- [Actual slice evidence](evidence/FUSION-SLICE.md)
- [Browser UI test report](evidence/fusion-browser-check.json)
- [Table screenshot](evidence/fusion-table.png), [laptop layout](evidence/fusion-laptop.png)
- [Agent-team worksheet](AGENT-TEAM.md), [review handoff](fusion/REVIEW-HANDOFF.md)
- [Playtest protocol](PLAYTEST.md), [scope-change draft](WEEK3-SCOPE-CHANGE.md)

No paid APIs were called. Human vs LLM and a real provider adapter are not in
this slice. Data-only model-policy hooks, counted attempts, hard timeouts and
trace handling are prepared and tested with explicit offline fixtures. Live
trials, dated prices/cost, independent review, distinct-session skill evidence,
student-authored reflection, another person's observed playtest, recording,
remote CI and submission remain pending. No PR was pushed or submitted.
The current checkpoint is the student's gameplay/visual review, not submission.

## Preserved versions

`pool/` and its original tests remain the six-ball version; run
`python -m pool.ui --mode hvb`. `historical/` and its tests remain the interrupted
historical experiment; run `python -m historical`. Neither is the final game.
Their evidence remains under its original filenames. Pre-Fusion primary
documents and workflow are preserved in `versions/pre-fusion/`; earlier
six-ball snapshots remain in `backup-six-ball/`. Snapshot links retain their
original directory context. A hash manifest verifies older code/tests were not
changed. Never mix those earlier outcomes with Fusion evaluation.

