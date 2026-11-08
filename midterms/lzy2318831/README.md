# Pool + Pinball: Kinetic Circuit

**Author:** lzy2318831 · **Game version:** `fusion-1.6.0-balanced`

The final balanced table removes only the short upper-corner entry diagonals
and reduces lower Slingshot boost parameters by25% (320/60/420to240/45/315).
Larger Orbit assemblies, pockets, boundaries, bumpers, timing, scoring and shot
quotas remain unchanged. Cue contact and reliable Live restart fixes are retained.
The original v1.5 package, specs, exact hashes and official evaluation inputs are
preserved in `versions/kinetic-replenish-v1.5-final/`. Historical replay uses
that original physics; its11matches/2wins/9losses do not evaluate the new table.
See [v1.6 validation](evidence/table-balance-v16-01/REPORT.md).

## Gameplay Demo

[Watch the final Kinetic Circuit gameplay demonstration](https://youtu.be/eLdDOiIwE84)

My final demonstration uses Geometry-Assisted Live LLM with Adaptive Distance v2.
The video description is student-provided; the historical evaluation below
remains associated with v1.5 physics.

## Quick Start

Requires Python 3.11+ and a current browser. From your clone's
`midterms/lzy2318831/` directory, run:

**Reference environment: Windows with CPython 3.11 or 3.12.** Exact historical
replays and this combined launcher depend on Windows C-library math results.
Linux returns a one-ULP-different sine for a recorded shot and fails strict
replay validation. The [runtime investigation](evidence/replay-compatibility-01/REPORT.md)
records the exact cause and unchanged evidence. CI runs all strict checks on
the reference platform; Linux numeric probes are diagnostic only.

```powershell
python -m fusion.geometry_live
```

Open **http://127.0.0.1:8835/**. Choose **Human vs Human**, **Human vs Geometric
AI**, or **Human vs Smart AI** to play. Choose **Recorded LLM Replay** to watch
the saved official LLM and Geometric actions play automatically without API
calls. Paid live inference is disabled by this launch. Keep the terminal open;
Ctrl+C stops the server. Use `py` or `python3` if that is your Python launcher.
Detailed setup, controls and mode distinctions follow below.

I wanted to combine the planning of a pool shot with the chain reactions of a
pinball machine. Kinetic Circuit is an original, two-player Pool Shark-inspired
game, not a reconstruction of Atari's rules or controls. I moved away from the
earlier six-ball and historical prototypes to focus on one complete table.
Those versions and their evidence are preserved separately.

The finished scope is one table, 15 object balls, six pockets, kinetic devices
and six alternating shots per player. It excludes spin, tournaments, network
multiplayer and historical fidelity. The balls, rails, lighting and interface
use original Canvas/CSS artwork. See [sources and reuse terms](SOURCES.md),
[rule/source map](rule-source-map.md) and [rules](RULES.md). The scope-change
record is [WEEK3-SCOPE-CHANGE.md](WEEK3-SCOPE-CHANGE.md). I confirmed that I
published “Midterm Scope Update — Kinetic Circuit” in the Week 3 CourseWorks
Discussion; that file preserves my supplied post verbatim. The direct
discussion URL is unavailable.

**Recording URL:** [Final gameplay demo](https://youtu.be/eLdDOiIwE84).
The instructor, TAs and assigned peer reviewers must be able to open it.
[Recording instructions](DEMO-RECORDING.md) are a guide, not the finished video.

## Setup and play

Use Python 3.11+ and a current Chrome, Edge or Firefox browser. The game needs
only the Python standard library: no pip packages, Node or downloaded assets.
Node is optional for the JavaScript checks and is installed by CI.

All commands in this README run from **`midterms/lzy2318831/`**. The detailed
Windows examples below use `py`; use `python` or `python3` if that is your
installed launcher (`python` worked in the final offline review). After cloning,
change the path below to your clone if necessary. Stop any old demo server first.

```powershell
Set-Location C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831
py -m fusion.geometry_live
```

Open **http://127.0.0.1:8835/** and keep PowerShell running. Ctrl+C stops it.
This launch has paid calls disabled. The Main Menu offers:

| Mode | Who chooses the shots? |
| --- | --- |
| Human vs Human | Two people alternate on the same computer. |
| Human vs Geometric AI | The human plays P1; the original geometric baseline plays P2. |
| Human vs Smart AI | The human plays P1; a separate bounded physics-search policy plays P2. |
| Recorded LLM Replay | Genuine saved official LLM and Geometric actions play automatically. No new inference. |
| Geometry-Assisted Live LLM | The preferred LLM selects a public-geometry candidate for P1 against Geometric, after paid mode and match consent are enabled. |

Point the mouse to aim. Click and pull backward to set power, then release.
Right-click or Escape cancels the drag. The guide and cue show the intended
direction. Input stays locked while the shot resolves and animates. Human and
recorded modes have **Restart Match**; agent pages have **Back to Main Menu**.
Returning from live play cancels and settles any in-flight request before
navigating. It does not reset the paid-call allowance.

## Gameplay and scoring

Each player has six shots, alternating even after a successful pot. Any object
ball can score for either player; ball numbers do not create solids/stripes
teams or an eight-ball win rule. Higher final score wins; equal scores draw.

| Event | Points |
| --- | ---: |
| Object ball pocketed | 100 |
| Object pocketed after the cue activates Orbit that shot | 200 instead of 100 |
| Each additional object pot in the same shot | +50 |
| At least one pot after a cue-ball bumper contact | +50 once per shot |
| Cue hits a distinct pop bumper | +15, once per bumper per shot |
| Cue crosses a distinct return lane | +10, once per lane per shot |
| Cue triggers a slingshot | +10 per sling per shot |
| Cue crosses Orbit / enters Vault / enters Skyway | +25 / +40 / +20, once each per shot |

Device-only awards are bounded at 315 per shot. Object balls receive device
physics but do not earn device awards. A cue scratch voids **all points from
that shot**, including earlier pots and combos; pocketed objects remain removed
and the cue is respotted. Repeated collisions cannot farm unlimited points.

To keep later shots active, five objects are replenished when eight or fewer
remain, at most twice per match. This happens only between settled valid shots,
after scoring and scratch handling, and not after the final opportunity. A full
safe batch must fit; spawning scores nothing. Replenishment is attempted before
clearance is checked, so clearing the table does not necessarily end the match
while supply remains. Otherwise the game ends on clearance or 12 opportunities.

Cascade pops, the Ricochet Reactor, Vault, Skyway, slings and Orbit redirect
balls around a central billiards corridor. Skyway is an instantaneous transfer
with an elevated-return visual effect, not a true 3D ramp. Physics runs at a
fixed 240 Hz; animation does not determine outcomes. Exact values and boundary
cases are in [RULES.md](RULES.md).

## Autonomous demonstrations

**Geometry-Assisted LLM v1** is the preferred Live LLM demonstration. To run a
mocked version without API costs:

```powershell
python -m fusion.geometry_live --mock
```

From `midterms/lzy2318831/`, open http://127.0.0.1:8835/ and choose
**Geometry-Assisted Live LLM**, or open http://127.0.0.1:8839/ directly.
This launcher labels that page `kinetic-geometry-assisted-v1`; `--mock`
uses a clearly labelled synthetic candidate selection and makes no API calls.
Omit `--mock` for a paid-disabled launch. Future real calls require separate
spending approval, `--enable-paid`, server credentials and browser match consent;
the existing six-request/$0.25 limits remain. No new paid calls were made here.

For a **student-authorized real OpenAI match**, the masked Windows launcher is:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run-geometry-live.ps1 -EnablePaid
```

The process-scoped execution-policy option lets this local script run without
changing the machine policy. It prompts privately for the API key, stores it
only in the backend process environment, and restores the previous environment
when the server exits. Do not put the key in a command argument, file, browser,
recording or Git. With `OPENAI_API_KEY` already configured privately, the
cross-platform equivalent is `python -m fusion.geometry_live --enable-paid`.
The model is pinned to OpenAI `gpt-5.4-mini-2026-03-17`; the backend sends
structured candidate-ID requests to the Responses API.

Open **http://127.0.0.1:8835/** and choose **Geometry-Assisted Live LLM**.
Before confirming, use **Candidate power**: **2x - student demonstration
preference** is the initial setting; choose **1x - stabilized fallback** to
retain the base recommendations. The setting is shown in the budget/status area,
confirmation and saved traces. It changes no physics, angle, target or route;
the LLM still selects a numbered candidate. Power is capped at100.

I chose2x for more energetic demonstration shots and accept its increased
scratch risk; it is **not a proven win-rate improvement**. The
[offline experiment](evidence/power-2x-01/REPORT.md) measured scratches1/77 versus
14/77, with no simulation-limit failures in that sample. Original1x stopping/
scratch notes do not establish safety at2x. To revert without restarting Python,
return to Main Menu, reopen Geometry-Assisted Live LLM, choose1x before confirming
the fresh match, and confirm again. The server retains the last selected setting
between matches; it rejects mid-match changes. Switching never resets spending
or starts a model request. See [setting validation](evidence/power-setting-01/REPORT.md).

For stronger contact shots, select **Adaptive energy - experimental** in the same
Candidate power menu before confirming. The current `adaptive-distance-v2`
profile directly recommends contact/pot/bank-contact power30–40 for travel0–150,
40–80 for150–350, and80–100 beyond350 (reaching100 at1000units).
It interpolates continuously, rounds half-up, and caps100; it is not a floor
over2x. Travel means the cue path to first contact, not the object's path to a
pocket. Escape/device routes retain their separate2x treatment.1x and2x remain
unchanged rollback choices; the initial default remains2x. The selected mode
persists between fresh matches. See the [current profile report](evidence/adaptive-distance-v2-01/REPORT.md)
for the exact formula and paired offline comparison. Stronger power is not a
proven improvement in LLM win rate; powered cascades remain possible.
The original-v1.5 [calibration report](evidence/power-calibration-01/REPORT.md) verifies the newest
genuine2x execution and compares96saved-state/candidate cases: adaptive increased
scratch-free pots11to42 and retained points2375to8270, with scratches9to15 and
no simulation-limit failures in this sample. This is not a human-experience or
LLM win-rate result; future powered cascades remain possible. Return to Main Menu
and reopen Live LLM to select a rollback before fresh consent.

Starting the server or opening the page sends no request. Confirm one match in
the browser: at most **6 requests**, **$0.25 estimated**, **20 seconds/request**,
no retries. Cancel or Back to Main Menu blocks further dispatch and settles an
in-flight work. Back to Main Menu returns within a bounded 1.5-second wait even
if the leave request stalls; the server must settle before a new match starts.
A sent call may still be charged. After a
completed, failed or cancelled match, return to the menu and reopen the live
page (or choose **New match (fresh consent)**). A new episode and token are
prepared without restarting Python; model dispatch still needs fresh consent.
The server-wide allowance is **12 requests/$0.50 estimated** across matches,
separate from each match's6/$0.25 cap. Reload, cancellation and new matches do
not reset it. A fresh match is disabled if the remaining server allowance cannot
cover all six requests/$0.25; the page explains this limit. Any new server launch
is a new allowance and still requires explicit paid enablement and consent.
When normal geometry routes are unsupported, the LLM is offered base-minimum-power
fallback directions with risk notes; it still selects the candidate itself.
These use the selected multiplier too, so2x is not minimum legal power.
API/model/time-limit failures show **match incomplete**, not a completed game.
HTTP wiring, cancellation and limits have offline tests, but real account
access and this variant's live quality await a student-authorized smoke test.

The new [candidate generator](fusion/geometry_candidates.py) supplies public-only
contact, ghost-ball pot, bank, device-entry and escape options with computed
angles, reach/power estimates and risk notes. The [LLM selector](fusion/geometry_agent.py)
chooses a numbered candidate; malformed/unknown selections fail without an
automatic Geometric/Smart replacement. Fallback choices rank initial clearance
at minimum legal power; they cannot guarantee a collision-free stop or no scratch.
Clearance is geometric, not a guarantee of a pot, safe powered exit or win.
Contact/bank power now budgets 15 units of object runout instead of 60 and omits
the extra 4% launch-speed margin; device-only proposals are omitted when a direct
contact or pot route exists. The saved 266-degree/power-4 failure reproduces a
powered cascade at 9,600 ticks; power 1 settles in 354 ticks in that same position.
This is a position-specific offline check, not proof of stronger play or universal
settlement. See [stabilization evidence](evidence/stabilization-01/REPORT.md).
The old `python -m fusion.live_demo` launcher still uses prompt-v2. Official and prompt-v2 results
remain separate; geometry-assisted traces use `evidence/live-browser-geometry-v1/`.
See [experimental coverage and limitations](EVALUATION.md#geometry-assisted-v1-offline-development-only)
and [the player contract](fusion/GEOMETRY-ASSISTED.md).

From the same project directory, the older recorded-only launcher also works:

```powershell
py -m fusion.demo
```

Open http://127.0.0.1:8785/ and click **Watch LLM Agent Play**. The default
recording is `observation_only-bumper-102-p2`: Geometric wins 935–900. The
renderer regenerates motion from actual saved actions and checks the trace;
it is labelled **Recorded LLM Evaluation**, not live inference or original video.

For a **legacy prompt-v2** offline controller check, stop the previous server and run:

```powershell
py -m fusion.live_demo --mock --port 8825 --replay-port 8827 --live-port 8829
```

Open http://127.0.0.1:8825/, choose Live LLM Agent and confirm the **mocked**
test. Synthetic responses are clearly labelled and are not model-performance
evidence. Both seats advance automatically. See [navigation notes](NAVIGATION-AND-AGENT-PLAN.md).

The preserved **legacy prompt-v2 paid launcher** below is optional and requires
separate spending approval; it is not the preferred geometry-assisted launcher:

```powershell
.\run-live-llm-demo.ps1 -EnablePaid
```

It uses http://127.0.0.1:8805/ and requires another explicit browser confirmation
for one match: at most six real requests and $0.25 estimated cost, no retries.
The API key stays on the Python backend. Cancel blocks further dispatch; an
already reserved/sent request may still be charged. Never put a key in code,
browser fields, URLs or recordings. [Live setup and limits](LIVE-LLM-DEMO.md)
also explain the PowerShell execution-policy limitation observed in preparation.
No paid command is part of the offline test workflow.

## Agent architecture and public API

Python owns all state, validation, physics and scoring. `fusion.engine.Episode`
provides the five operations:

| Operation | Purpose |
| --- | --- |
| `reset(seed)` | Start a deterministic episode. Seeds are recorded; they do not randomize the rack. |
| `observe(player_id)` | Return a detached public view of balls, devices, scores, quotas and visible feedback. |
| `legal_actions(player_id)` | Return angle/power bounds for the active player; otherwise an empty list. |
| `step(player_id, action)` | Validate and resolve a complete shot. |
| `outcome()` | Return status, scores, winner/draw, counters and an explicit terminal reason. |

Actions are integer angle 0–359 (clockwise from right) and power 1–100. The LLM
receives only permitted observations and legal actions, without engine objects,
repository tools, credentials or evaluator answers. Its proposal is parsed and
validated; it cannot directly edit state. No failed model move is replaced by
a baseline move.

The **Geometric baseline** uses public targeting geometry. **Smart AI** uses
the same physics in bounded counterfactual search (24 candidates/40,000 ticks);
it is not an LLM. The **original official LLM** uses `fusion/llm.py`. Later
**prompt-v2**, in `fusion/prompt_v2.py`, adds a risk/geometry checklist but still
has no simulator. Their results remain separate. The physics-assisted approach
in the navigation notes is a proposal only. See [agent-team evidence](AGENT-TEAM.md).

## Evaluation, tests and reproducibility

The original official evaluation completed **11 matches: 2 wins, 9 losses,
zero illegal actions**. Mean scores were **720.45 for the LLM and 1347.27 for
the actual Geometric opponent**. The initial HTTP 429 failure remains the
twelfth trial. There were 25 cue scratches in 66 LLM shots. These results do
not show that the LLM is stronger. [EVALUATION.md](EVALUATION.md) contains the
full comparison, raw evidence, usage, latency, cost and later-experiment labels.

From `midterms/lzy2318831/`, these commands are offline:

```powershell
py -m unittest discover -s tests -v
py -m fusion.freeze
py -m fusion.final_analysis --verify
py -m fusion.runner --p1 baseline --p2 baseline --seed 101 --trace evidence/my-offline-match.json
py -m fusion.runner --replay evidence/my-offline-match.json
```

Use a new trace filename to preserve previous results. On Linux/macOS, use
`python` or `python3` instead of `py`, from the same project directory. Recorded
traces replay deterministically; fresh model responses are not deterministic.
Final local validation results, including two consecutive actual-browser mock
matches, are recorded in [the lifecycle report](evidence/lifecycle-fix-01/REPORT.md).
Earlier finalization/controller/replay results are recorded in
[the final report](evidence/final-geometry-01/REPORT.md). The scoped
[CI workflow](../../.github/workflows/midterm-lzy2318831.yml) checks rules,
illegal actions, regressions, limits, replay, controllers and freeze without
provider credentials. The [first remote Midterm run](https://github.com/lzy2318831/game-dev-f26/actions/runs/42435757312)
failed on Linux/Python 3.11 with 13 historical replay-divergence errors and
5 skips; Python 3.12 was cancelled by matrix fail-fast. Local Windows/Python
3.15.1 checks passed. The cause is now verified: platform `sin(123°)` rounding
first changes shot9of the default archived match by one ULP. Windows Python3.11
replays it exactly. The workflow now runs all unchanged strict tests/replays on
Windows3.11/3.12, with a separate Linux diagnostic. Inspect the
[course PR checks](https://github.com/columbia-university-ai-games/game-dev-f26/pull/97/checks)
for current status; the original failed run remains preserved.

Small samples, deterministic repeated layouts, frequent scratches and no live
memory ablation limit the claims. My own playtesting motivated the bounded
refill. A separate real friend playtest is now documented in
[PLAYTEST.md](PLAYTEST.md): scratches were frustrating, some balls were hard to
recover near edges/obstacles, and the layout could flow better. I discuss these
as limitations, not verified causes of the LLM's scratches. I personally watched
my friend play independently without coaching; the human playtest requirement is
complete. Both distinct `competitive-rule-change` skill-use sessions are
documented in [AGENT-TEAM.md](AGENT-TEAM.md): implementation session
`01a1b37c-aa97-7781-91f4-ec7693968a43` and fresh read-only review session
`01a1b6ef-6f18-72c2-9249-e06f0ee80045`. The
[session audit](evidence/submission-readiness-01/SESSION-EVIDENCE.md) preserves
the first session's references; AGENT-TEAM.md records the second session's actual
invocation and transcript locators. I supplied the final video URL and finalized
my first-person PR reflection. Remote CI verification and the actual PR/CourseWorks
hand-in are tracked during final submission preparation. See the [submission checklist](SUBMISSION-CHECKLIST.md).


The1x/2x/Adaptive algorithms and paid-call settings are unchanged; they now play
v1.6in the preferred Geometry-Assisted launcher. No genuine v1.6LLM performance
measurement exists. The original prompt-v2 Live launcher remains bound to
archived v1.5physics so its historical prompt facts stay valid. Recorded replay
shows its original physics version. Restart an already-running old Python process
once to load this revision; later Live matches require no server restart while
allowance remains. My chosen final demonstration setting is Adaptive Distance v2;
1x/2x remain available and the initial runtime preference remains2x.
Final local validation passed222Python tests,7JavaScript suites,24historical
replays, both18-artifact freeze checks and157archive hashes. See
[final submission verification](evidence/submission-final-01/REPORT.md).
The [course PR](https://github.com/columbia-university-ai-games/game-dev-f26/pull/97)
is open against main from the student-specific course branch. CourseWorks
hand-in remains manual. The runtime correction changes no game physics or AI.
