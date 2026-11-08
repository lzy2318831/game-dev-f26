# Pool + Pinball: Kinetic Circuit

**Author:** lzy2318831 · **Game version:** `fusion-1.5.0-replenish`

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
record is [WEEK3-SCOPE-CHANGE.md](WEEK3-SCOPE-CHANGE.md); its discussion-thread
post/link still needs my confirmation.

**Recording URL: PENDING — insert the actual, viewable 3–5 minute video link.**
The instructor, TAs and assigned peer reviewers must be able to open it.
[Recording instructions](DEMO-RECORDING.md) are a guide, not the finished video.

## Setup and play

Use Python 3.11+ and a current Chrome, Edge or Firefox browser. The game needs
only the Python standard library: no pip packages, Node or downloaded assets.
Node is optional for the JavaScript checks and is installed by CI.

All commands in this README run from **`midterms/lzy2318831/`**. On my Windows
machine, use `py`; `python` resolves to an application alias. After cloning,
change the path below to your clone if necessary. Stop any old demo server first.

```powershell
Set-Location C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831
py -m fusion.live_demo --port 8825 --replay-port 8827 --live-port 8829
```

Open **http://127.0.0.1:8825/** and keep PowerShell running. Ctrl+C stops it.
This launch has paid calls disabled. The Main Menu offers:

| Mode | Who chooses the shots? |
| --- | --- |
| Human vs Human | Two people alternate on the same computer. |
| Human vs Geometric AI | The human plays P1; the original geometric baseline plays P2. |
| Human vs Smart AI | The human plays P1; a separate bounded physics-search policy plays P2. |
| Recorded LLM Replay | Genuine saved official LLM and Geometric actions play automatically. No new inference. |
| Live LLM Agent | A separate prompt-v2 model plays P1 against Geometric, after paid mode and match consent are explicitly enabled. |

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

From the same project directory, the older recorded-only launcher also works:

```powershell
py -m fusion.demo
```

Open http://127.0.0.1:8785/ and click **Watch LLM Agent Play**. The default
recording is `observation_only-bumper-102-p2`: Geometric wins 935–900. The
renderer regenerates motion from actual saved actions and checks the trace;
it is labelled **Recorded LLM Evaluation**, not live inference or original video.

For an offline check of the live controller, stop the previous server and run:

```powershell
py -m fusion.live_demo --mock --port 8825 --replay-port 8827 --live-port 8829
```

Open http://127.0.0.1:8825/, choose Live LLM Agent and confirm the **mocked**
test. Synthetic responses are clearly labelled and are not model-performance
evidence. Both seats advance automatically. See [navigation notes](NAVIGATION-AND-AGENT-PLAN.md).

Actual live inference is optional for reviewing the saved submission and needs
separate spending approval. From the project directory, the masked launcher is:

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
The latest completed development run passed 164 project tests. The scoped
[CI workflow](../../.github/workflows/midterm-lzy2318831.yml) checks rules,
illegal actions, regressions, limits, replay, controllers and freeze without
provider credentials. A remote green run for the submitted commit is still pending.

Small samples, deterministic repeated layouts, frequent scratches and no live
memory ablation limit the claims. My own playtesting motivated the bounded
refill, but it is not the required other-person observed playtest. Its notes,
the video, two independent skill-session references, my final reflection and
the approved PR/CourseWorks submission remain unfinished. See the
[submission checklist](SUBMISSION-CHECKLIST.md) and [playtest worksheet](PLAYTEST.md).
