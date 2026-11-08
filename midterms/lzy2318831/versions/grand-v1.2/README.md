# Pool + Pinball: Arcade Fusion

An original two-player arcade billiards game by lzy2318831. This is a Pool
Shark-inspired adaptation, **not a historical reconstruction**. Status:
Aurum Circuit polish pass complete, awaiting the student's gameplay and visual review.

## Play on Windows

Python 3.11+ and a modern Chrome/Edge/Firefox browser are sufficient. No pip,
Node, Pygame, model credentials, build step, external fonts or assets required.

From PowerShell:
```powershell
Set-Location 'C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831'
python -m fusion --port 8768
```

Keep that terminal running. Open [the local game](http://127.0.0.1:8768).
If the port is occupied, use `python -m fusion --port 8767` and open port 8767.
The service binds only to 127.0.0.1. Ctrl+C stops it. Every command below runs
from the project folder shown above, not the repository root.

Choose VS BASELINE or 2 PLAYERS, then LET'S PLAY. Point to aim; press on the
table, pull backward along the cue line, and release. Pull farther for more
power. Tiny drags cancel. Right-click or Escape cancels. The guide shows first
contact, not a guaranteed future trajectory. Watch the shot finish before the
next player acts. New match resets the table. The baseline chooses its own
moves; humans never choose its shot.

## The complete loop

### Aurum Circuit — the single finished playfield

Ten solid rounded guide segments form two open-ended side return channels and
the top Orbit funnel. Lower elbows bank the ball inward; channels never steer
or teleport it. Each cue return crossing earns 10 once per side/shot. Orbit
earns 25 and doubles only later pot base values within that shot, never
stacking or carrying into another turn. Device-only points are capped at 105
per shot; scratch voids everything. See [mechanism rules](fusion/POLISH-RULES.md).
The central billiards area stays clear. Raised rails match their actual
collision geometry; etched panels and lighting are decoration.

One cue ball, six objects, six pockets, four powered bumpers, guided side return channels and a traversable Orbit spinner. Each player has
six alternating opportunities. A pot earns 100 (200 after activating Orbit); a distinct cue-ball bumper
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
- [Current polish evidence](evidence/polish-1/REPORT.md)
- [Browser UI test report](evidence/polish-1/fusion-browser-check.json)
- [Table screenshot](evidence/polish-1/fusion-table.png), [laptop layout](evidence/polish-1/fusion-laptop.png)
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

The previous two-bumper Fusion game is a runnable snapshot in
`versions/fusion-v1/` (change to that directory and run
`python -m fusion --port 8767`). Its tests, original art and previous evidence
are preserved. Current evidence is under `evidence/polish-1/`. Stop any old
running server before reusing its port; Python backends do not hot-reload on
browser refresh.

`pool/` and its original tests remain the six-ball version; run
`python -m pool.ui --mode hvb`. `historical/` and its tests remain the interrupted
historical experiment; run `python -m historical`. Neither is the final game.
Their evidence remains under its original filenames. Pre-Fusion primary
documents and workflow are preserved in `versions/pre-fusion/`; earlier
six-ball snapshots remain in `backup-six-ball/`. Snapshot links retain their
original directory context. A hash manifest verifies older code/tests were not
changed. Never mix those earlier outcomes with Fusion evaluation.


## Grand Circuit: current maximal playfield

This is the current playable version. Aurum is runnable in versions/aurum-v1.1/;
its screenshots, tests and evidence remain separate. No historical source or
assets were imported. Python + browser Canvas and the five-operation interface
remain unchanged; no installation beyond Python3.11+ and a modern browser.

Six bumpers, six lane sensors and26 physical rail segments create outer orbit
routes, split side paths, passive return channels and angled lower banks.
Twenty segments are passive; six form two powered triangular slings. The
central y185..315 corridor remains clear of fixed devices. Slings reflect and
boost; the Vault scoop kicks a moving ball radially outward once per ball/shot.
There are no overpasses, gates or ball-storage timers. The original Orbit
spinner doubles subsequent pot base values only for the remainder of the shot.

Cue scoring:15 per distinct pop(max90),10 per lane(max60),10 per sling(max20),
Vault40, Orbit25. Device-only cap235 per shot. Objects interact physically but
receive no device points. Existing100/200 pots and50 combos remain. Scratch
voids everything. Impulses have finite per-ball budgets and speed caps. Max9600
fixed ticks(40 simulation seconds) per shot; failure at bound is explicit.
See fusion/MAXIMAL-RULES.md for exact design rules, evidence/maximal-1/REPORT.md
for actual tests/review. No live policy performance is claimed for this table.

PowerShell:
```powershell
Set-Location 'C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831'
python -m fusion --port 8768
```
Open http://127.0.0.1:8768. Choose VS BASELINE or2PLAYERS, start, point to aim,
press/pull backward/release. Right-click/Escape cancels. Let the shot finish.
Try the six lit lane crossings, outer banks, triangular slings and top-right
Vault. Not all directions lead to a pocket: the extra banks deliberately trade
open pot lines for device combinations. New match resets all shot budgets.
This version stops for student gameplay and visual review.
