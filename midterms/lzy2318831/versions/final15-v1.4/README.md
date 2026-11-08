# Pool + Pinball: Kinetic Circuit - FINAL15

Original Pool Shark-inspired arcade billiards by lzy2318831, not a historical
reconstruction. Final playfield/gameplay design frozen:15objects plus cue,
three player modes, same navy/cyan/gold table, devices and six shots each.
Midterm submission evidence is still incomplete; see remaining work below.

## Play on Windows

Python3.11+ and a modern Chrome/Edge/Firefox browser. No pip,Node,build,external
fonts or game assets needed. From PowerShell:

```powershell
Set-Location 'C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831'
python -m fusion --port 8771
```

Open http://127.0.0.1:8771 and keep the terminal running. Ctrl+C stops it.
If already running, use the existing server. Choose VS GEOMETRIC, VS SMART AI
or2PLAYERS, then start. Point to aim, press/pull backward, release to shoot.
Pull farther for power; tiny drags cancel. Escape/right-click cancels. Input
locks through planning and playback. New match restarts. Smart shoots itself.

The five-row rack has numbered solids1..7,black8,stripes9..15. Six alternating
shots/player, end on table clearance or12opportunities; higher score wins,
equal scores draw. Pots100,Orbit doubles subsequent pot bases, multi/assist
combos50. Device-only points cap315/shot. Scratch voids ALL points that shot.
Clearance on a scratch still ends the game. Exact [rules](RULES.md).

## Final table and opponents

Cascade pop cluster, compact Reactor, directed Vault kickout, powered inward
slings, Orbit spinner, passive side returns and Skyway transfer all retained.
Central billiards corridor remains open. Skyway is a documented instantaneous
2.5D return illusion, not true3D ramp flight. Original procedural Canvas art.
Fixed240Hz Python physics; browser interpolates snapshots without affecting
results.9600ticks/40simulation seconds per shot, explicit execution failures.

- **Geometric AI:** original cheap public-geometry baseline, unchanged source.
- **Smart AI:** deterministic physics search, max24candidates/40000tick calls.
  Uses only detached public observation and authoritative game physics. Candidate
  direct/combination/bank/device/exploratory shots, multiple powers; settled
  score/pot/foul/position/match-margin ranking. Internal simulator capability
  is disclosed. Measured6.59sec/shot in this development run, hardware-dependent.
- **LLM Agent:** separate real model player still pending provider integration.
  Smart is not an LLM and its matches are not live-model evidence.

Development comparison: Smart won6/6fixed seat-balanced matches vs Geometric,
average score2489.17vs368.33; small suite, not a general strength guarantee.
[Full measured results](evidence/final-15/COMPARISON.md).
[Verification/review](evidence/final-15/REPORT.md).

## Reproduce offline

All commands below run from the project directory above:

```powershell
python -m unittest discover -s tests -v
python -m fusion.freeze
python -m fusion.runner --p1 smart --p2 baseline --seed 101 --trace evidence/my-final15-match.json
python -m fusion.runner --replay evidence/my-final15-match.json
python -m fusion.compare_smart
```

Comparison reruns overwrite only its dedicated output files; preserve published
results before rerunning. Browser QA tool requires a separately launched local
isolated Chrome debugging profile; it is developer application QA, not an end-user
requirement or a human playtest.90project tests passed; root starter diagnostics
remain incomplete due unrelated SDK/Windows/auth/Pyxel prerequisites.
CI workflow includes tests, offline matches/replays and gameplay freeze check;
remote CI has not run. No live calls in CI.

## Player interface and fairness

fusion.engine.Episode exposes reset(seed),observe(player_id),legal_actions,
step(player_id,action),outcome(). All agents submit integer angle0..359 and
power1..100. Engine validates/commits. Wrong seat/postterminal immutable;
malformed active proposals consume a shot. Public detached positions/device
geometry/scores/quotas/events, no files,credentials,evaluator labels or hidden
state. Smart reconstructs snapshots preserving pocketed IDs, never receives
the live Episode. Geometric/LLM do not receive simulator tools. Model budget
12attempts,20sec/request,300sec/match; failures count, no silent fallback.

## Evidence still required

Gameplay/visuals frozen by this final authorization; no further redesign.
Next work is real LLM transport/provider choice, approved-budget live repeated
trials on frozen suite5 against Geometric, costs/calls/failures, observed human
playtest,3-5minute recording, distinct-session skill evidence, student own-voice
reflection and PR review. See [remaining checklist](MIDTERM-NEXT.md),
[EVALUATION](EVALUATION.md),[AGENT-TEAM](AGENT-TEAM.md),[PLAYTEST](PLAYTEST.md).
No paid calls,push,PR submission or gate approval performed.

## Provenance and preserved versions

Original game using reusable project-owned Python infrastructure; no historical
code,ROM,sounds or copyrighted graphics imported. See [sources](SOURCES.md) and
[rule map](rule-source-map.md). Six-ball Kinetic snapshot in
versions/kinetic-six-v1.3; Grand,Aurum,original Fusion,six-ball pool and historical
experiments remain preserved, with their evidence separate. Final gameplay/
visual hashes in fusion/gameplay-freeze.json; ongoing LLM/report work stays separate.
