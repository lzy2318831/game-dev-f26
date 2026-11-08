# Pool + Pinball: Kinetic Circuit - REPLENISH v1.5

Original Pool Shark-inspired arcade billiards by lzy2318831, not a historical
reconstruction. Final playfield/gameplay design frozen:15objects plus cue,
three player modes, same navy/cyan/gold table, devices and six shots each.
Midterm submission evidence is still incomplete; see remaining work below.

## Watch the real LLM agent's recorded match

From the project directory, run `py -m fusion.demo`, open
`http://127.0.0.1:8785`, and click **Watch LLM Agent Play**. The authentic
**Recorded LLM Evaluation** starts automatically; Play, Pause-after-shot and
Restart control playback only. Every angle/power comes from the saved match.
No API key or new API calls. See [3–5 minute recording steps](DEMO-RECORDING.md).
**Recording link: PENDING actual video**, not replaced by this replay page.

Official results:11 completed,2LLM wins/9losses,1preserved HTTP429 failed trial;
0illegal actions. Recovery66calls,$0.15966225 estimated. Full comparison,
usage,latency,limitations and all evidence:[EVALUATION.md](EVALUATION.md).

## Play on Windows

Python3.11+ and a modern Chrome/Edge/Firefox browser. No pip,Node,build,external
fonts or game assets needed. From PowerShell:

```powershell
Set-Location 'C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831'
py -m fusion.demo
```

Open http://127.0.0.1:8785 and keep the terminal running. Ctrl+C stops it.
If already running, use the existing server. Choose VS GEOMETRIC, VS SMART AI
or2PLAYERS, then start. Point to aim, press/pull backward, release to shoot.
Pull farther for power; tiny drags cancel. Escape/right-click cancels. Input
locks through planning and playback. New match restarts. Smart shoots itself.

The five-row rack has numbered solids1..7,black8,stripes9..15. Six alternating
shots/player, refill5at<=8objects,max2batches; end on clearance after supplies or12opportunities; higher score wins,
equal scores draw. Pots100,Orbit doubles subsequent pot bases, multi/assist
combos50. Device-only points cap315/shot. Scratch voids ALL points that shot.
Clearance on a scratch still ends the game. Exact [rules](RULES.md).

## Limited replenishment

The opening still has15objects. At8or fewer, five resting balls appear after
scoring/scratch respot and before the next shot, up to twice per match. No refill
after the final opportunity. Clear space is verified for the complete batch;
numbered IDs are reused. Spawning awards no points. A short glow/toast shows the
batch and used supply. All agents receive the same public replenishment state.
The table and controls are unchanged. Game design frozen again after validation.

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
- **LLM Agent:** real OpenAI Responses player, official live evaluation completed;
  the Watch button replays genuine completed evaluation actions without new calls.
  Smart is not an LLM and its matches are not live-model evidence.

Before replenishment (v1.4 only), development comparison: Smart won6/6fixed seat-balanced matches vs Geometric,
average score2489.17vs368.33; small suite, not a general strength guarantee.
[Full measured results](evidence/final-15/COMPARISON.md).
[Verification/review](evidence/replenish-1/REPORT.md).

## Reproduce offline

All commands below run from the project directory above:

```powershell
py -m unittest discover -s tests -v
py -m fusion.freeze
py -m fusion.final_analysis --verify
py -m fusion.runner --p1 smart --p2 baseline --seed 101 --trace evidence/my-final15-match.json
py -m fusion.runner --replay evidence/my-final15-match.json
```

Comparison reruns overwrite only its dedicated output files; preserve published
results before rerunning. Browser QA tool requires a separately launched local
isolated Chrome debugging profile; it is developer application QA, not an end-user
requirement or a human playtest. Current verification is recorded in
evidence/final-submission-01/VERIFICATION.md; root starter diagnostics
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
Official live evaluation on frozen suite6 is complete, including original failure.
Next work is observed human playtest,3-5minute recording, distinct-session skill evidence, student own-voice
reflection and PR review. See [remaining checklist](MIDTERM-NEXT.md),
[EVALUATION](EVALUATION.md),[AGENT-TEAM](AGENT-TEAM.md),[PLAYTEST](PLAYTEST.md).
No new paid demo calls,push,PR submission or student gate approval performed.

## Provenance and preserved versions

Original game using reusable project-owned Python infrastructure; no historical
code,ROM,sounds or copyrighted graphics imported. See [sources](SOURCES.md) and
[rule map](rule-source-map.md). Six-ball Kinetic snapshot in
versions/kinetic-six-v1.3; Grand,Aurum,original Fusion,six-ball pool and historical
experiments remain preserved, with their evidence separate. Final gameplay/
visual hashes in fusion/gameplay-freeze.json; ongoing LLM/report work stays separate.

## Real LLM integration (gameplay freeze unchanged)

Separate genuine LLM adapter is implemented. Read [LLM setup/options/costs](LLM-SETUP.md)
and [submission status](SUBMISSION-CHECKLIST.md). Official calls are complete;
do not rerun paid evaluation. Inspect the offline protocol safely with:
`py -m fusion.llm_eval --model gpt-5.4-mini-2026-03-17`.
Live use requires explicit approval/provider/model/budget/key,never credentials
in prompts. LLM has no simulator/tools; Geometric stays officialbaseline,Smart
separate. Headless printed autonomous actions can be recorded without changing
the frozen UI. Offline validation results are not real-model evidence.

## Preserved original live run failure (historical)
Firstrealrequest returnedHTTP429; at that time0LLMmatchescompleted,11notrun. Originalrun
preserved; providererrorbody was discarded,so exactquota-vs-ratecause unknown.
Sanitizeddiagnosticlogging fixed/testedoffline. No automaticrerun. See
[evidence/http429-diagnosis/DIAGNOSIS.md](evidence/http429-diagnosis/DIAGNOSIS.md).
# Completed live evaluation recovery

Use [RECOVERY-EVALUATION.md](RECOVERY-EVALUATION.md) and
`run-recovery-evaluation.ps1` for how the approved eleven-trial continuation ran.
It is complete; do not make more paid calls for this demo.
The earlier failed run and successful smoke stay separate. Do not restart the
original full-suite launcher or repeat the one-call smoke.

