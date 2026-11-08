# Kinetic Circuit evaluation

The original official evaluation completed **11 LLM matches: 2 wins, 9 losses,
0 draws and 0 illegal actions**. Mean scores were **720.45 for the LLM and
1347.27 for its actual Geometric opponent**. An initial HTTP 429 rejection is
preserved as the twelfth official trial, not treated as a draw or replaced.

The main conclusion is limited: the model submitted legal shots and completed
matches, but it did not outperform Geometric overall. Prompt-v2 and browser
experiments happened later and are reported separately below.

## Geometry-assisted v1: offline development only

`kinetic-geometry-assisted-v1` is a separate candidate-selecting LLM experiment,
implemented in `fusion/geometry_candidates.py`, `fusion/geometry_agent.py` and
`fusion/geometry_live.py`. Public geometry supplies bounded candidate directions
and power estimates; the model selects an ID rather than doing its own angle
arithmetic. This is geometry-assisted decision-making, not the original raw
LLM, Geometric baseline, Smart simulation, or a new official evaluation.

It is the preferred final Live LLM demonstration, with a dedicated masked
`run-geometry-live.ps1` launcher and clearly labelled menu entry. Its real
OpenAI HTTP branch has synthetic-boundary tests; no genuine request was made
during finalization. Therefore real account access and new live performance are
not verified. [Final validation](evidence/final-geometry-01/REPORT.md) records
the actual offline results; original official results are unchanged.

[Saved-observation coverage](evidence/geometry-assisted-01/coverage-reviewed.json)
uses 34 executed genuine browser prompt-v2 requests from six runs, excluding
mocked runs. It finds clear direct contact candidates in **16/34**, and contact
including single-cushion banks in **18/34**. Device entries occur in 9 states;
15 states have only a conservative escape and one has no supported candidate.
No ghost-ball pot clears every conservative check in these 34 layouts; a
synthetic clear pocket fixture verifies that route type separately. The old raw
actions have **3/34** reachable initial contact rays passing the same direct
clearance screen (14/34 intersect a reachable object if blockers are ignored).
This compares availability of several candidates with one historical action,
not matched policy success. A later genuine geometry-assisted browser run in the
project stopped after four total shots on unsupported candidate generation;
the lifecycle report diagnoses that saved failure. No completed post-fix real
evaluation or improved pots/wins are claimed.

Reproduce from `midterms/lzy2318831/` without API calls:

```powershell
python -m fusion.geometry_analysis
python -m unittest discover -s tests -p test_geometry_agent.py -v
python -m fusion.geometry_live --mock
```

Power uses speed `100+7*power`, friction70 and approximate ball/cushion transfer;
minimum power denotes first contact/entry reach, not a guaranteed pot. Integer
angles are checked again for obstruction. Device exits, multi-ball chains and
post-collision scratch risk are not simulated. Banks and pots remain estimates.
Escape is offered when no direct contact/pot is supported; it must have a clear
stopping segment. The original generator could return no candidates in one of
these34 states; that historical coverage report is unchanged. The lifecycle
fix now supplies minimum-power fallback candidates when ordinary routes fail,
with explicit collision/scratch uncertainty. The LLM still selects an ID;
malformed model choices retain failure/usage evidence without a replacement move. Old browser cases are
development data, not fresh held-out tests. The original official numbers and
all saved official/prompt-v2 traces below remain unchanged. See
[new implementation/review evidence](evidence/geometry-assisted-01/REPORT.md).

An actual headless Chrome regression ran two consecutive full matches through
the same running server, using synthetic responses only:12 shots per match,
six per player, fresh consent/state/token on the second visit and cumulative
server requests6 then12. Both traces replayed; no browser runtime error or paid
request occurred. [Browser evidence](evidence/lifecycle-fix-01/browser-run-04/summary.json)
and [lifecycle diagnosis](evidence/lifecycle-fix-01/REPORT.md) document the fix.
This is engineering verification, not genuine geometry-assisted performance.

## Official protocol and evidence

- Game: `fusion-1.5.0-replenish`; declaration: [suite 6](fusion/evaluation.json).
- Player: original `fusion/llm.py`, OpenAI `gpt-5.4-mini-2026-03-17`.
- Input: public observation/legal actions, observation-only memory; no simulator,
  repository tools, hidden state or Smart substitution.
- Situations: direct pockets, bumper-assisted play, risky/obstructed shots.
- Seeds: 101 and 102; both seats, four planned trials per situation.
- Each player has six opportunities. All 11 completed games ended `shots_exhausted`.
- Limits: 20-second requests, 300-second episodes, original shared 72-attempt
  allowance and $5 local estimated budget. Failures counted; no automatic retries.
- Twelve matched Geometric-vs-Geometric controls used the same layouts/seeds
  and target seats. They are separate from the Geometric opponents in LLM matches.

The layouts were declared before the original policy evaluation. Earlier
declarations and the replenishment amendment remain in the versioned files;
they were not replaced with easier situations after seeing results. Seeds do
not randomize this engine, so repeated seeds do not imply independent boards.
The original cases later informed v2 development and are not untouched held-out
cases for a new v2 strength claim.

Primary evidence:

- [Initial failed run](evidence/live-mini-approved-01/manifest.json)
- [Eleven-match continuation and traces](evidence/live-mini-recovery-01/manifest.json)
- [Combined CSV](evidence/live-mini-recovery-01/combined-report/comparison.csv)
- [Combined summary](evidence/live-mini-recovery-01/combined-report/summary.json)
- [Read-only recomputation and replay verification](evidence/final-docs-01/verified-evaluation.json)
- [Separate successful one-call smoke](evidence/api-smoke-mini-01/result.json)

All 24 official trial/control traces have been reproduced offline through the
unchanged engine, matching events, state fingerprints and outcomes. The old
freeze manifest and original rules document are preserved under
[the documentation archive](evidence/final-docs-01/previous/). Saved evaluation
hashes remain historical records; documentation corrections do not rewrite them.

## Scores and outcomes

Scores below put the LLM first regardless of seat. Control score means the
target seat in a separate Geometric-vs-Geometric match.

| Situation / seed / LLM seat | LLM : opponent | Result | Control score | Input / output tokens | Total decision latency (s) | Known estimated USD |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Direct / 101 / P1 | 0 : 0, no shots | HTTP 429 failure | 0 | unknown | 1.796220 | unknown |
| Direct / 101 / P2 | 990 : 1455 | Loss | 0 | 21809 / 132 | 8.493848 | 0.01695075 |
| Direct / 102 / P1 | 605 : 1660 | Loss | 0 | 17237 / 126 | 7.276970 | 0.01349475 |
| Direct / 102 / P2 | 685 : 1485 | Loss | 0 | 21960 / 132 | 6.896482 | 0.01706400 |
| Bumper / 101 / P1 | 1235 : 185 | Win | 460 | 17530 / 126 | 6.087678 | 0.01371450 |
| Bumper / 101 / P2 | 1095 : 1500 | Loss | 1195 | 20910 / 138 | 6.492169 | 0.01630350 |
| Bumper / 102 / P1 | 745 : 1565 | Loss | 460 | 17411 / 126 | 5.997991 | 0.01362525 |
| Bumper / 102 / P2 | 900 : 935 | Loss | 1195 | 18589 / 144 | 6.443127 | 0.01458975 |
| Risk / 101 / P1 | 295 : 555 | Loss | 2875 | 15427 / 138 | 6.214251 | 0.01219125 |
| Risk / 101 / P2 | 130 : 2670 | Loss | 25 | 19503 / 144 | 6.012800 | 0.01527525 |
| Risk / 102 / P1 | 1010 : 385 | Win | 2875 | 15261 / 132 | 5.844375 | 0.01203975 |
| Risk / 102 / P2 | 235 : 2425 | Loss | 25 | 18354 / 144 | 6.625019 | 0.01441350 |

| Completed situation | LLM wins/losses | Mean LLM score | Mean actual opponent score |
| --- | --- | ---: | ---: |
| Direct (3 complete; 1 failure) | 0 / 3 | 760.00 | 1533.33 |
| Bumper (4 complete) | 1 / 3 | 993.75 | 1046.25 |
| Risk (4 complete) | 1 / 3 | 417.50 | 1508.75 |
| All 11 completed | 2 / 9 | 720.45 | 1347.27 |

The completed head-to-head win rate is 2/11 (18.18%). Across all 12 attempted
trials it is 2/12, with one separately counted provider failure. Completed LLM
scores total 7,925; actual opponent scores total 14,820. The failure's recorded
0:0 is not a played draw.

For the 11 corresponding control seats, the mean is 828.18. Across all 12
controls, total score is 9,110 and mean is 759.17; their target seats have
4 wins, 4 losses and 4 draws against another Geometric player. These control
figures must not be confused with the 1347.27 in-match opponent mean.

## Scratches, legality and failure handling

There were **25 cue scratches in 66 LLM shots** (37.88%), compared with 20
scratches for the actual opponents. A scratch erases all points from the shot,
including earlier pots, device awards and combos, while pocketed objects stay
removed. Of the LLM's 80 physical object-pot events, **44 occurred on foul
shots**; only 36 counted as non-foul pots. The saved CSV counts physical pots,
so that column differs from the engine's credited-pot metric. Neither is edited.

The LLM had zero engine-illegal actions and zero invalid model proposals.
Actual opponents and controls also had zero illegal actions. A legal shot is
not necessarily a useful one: this distinction matters more here than parsing.
The HTTP 429 failure is a provider rejection, not an illegal move. Its exact
message/body was discarded by the old handler, so the saved evidence does not
establish the precise billing-versus-rate-limit cause. Later error logging was
fixed; the failed run was not overwritten.

## Calls, latency, tokens and estimated cost

The continuation made 66 successful real calls: **203,991 input + 1,482 output
= 205,473 reported tokens**, estimated **$0.15966225**. Successful decision
latency totalled 72.384709 seconds, mean 1.096738 seconds and median 1.063078
seconds. Including the failed first request gives 74.180930 seconds of recorded
official call latency. The 72 target-seat control decisions totalled 3.276747
seconds (mean 0.045510). These are local wall-clock decision timings, not video
duration or isolated provider-network measurements.

The original rejected request used one attempt; its tokens and actual charge
are unknown. Its $0.0109875 reservation remains. The separate successful smoke
used one call, 2,156 tokens and $0.001707 estimated cost; it is not a scored match.

Together, official attempts plus smoke used **68 of 72 attempts**, with
**207,629 known tokens plus unknown rejected-request usage**. Known estimated
cost is **$0.16136925**; the conservative reserve-inclusive total is
**$0.17235675**. These use the saved 2026-11-07 rates of $0.75 input/$4.50 output
per million tokens, ignoring cache discounts. They are estimates, not invoices.
Later v2/browser costs are not included in these official figures.

## Later development, kept separate

The [prompt-v2 pilot](evidence/live-prompt-v2-pilot-01/summary.json) now contains
three completed real matches: **1 win, 2 losses**, scores 615:805, 585:1825 and
1385:1205. It used 18 calls, 75,517 reported tokens, $0.05823525 estimated,
8 LLM scratches and zero illegal actions. Its three seeds share the standard
rack and P1/P2/P1 seats. This is a small, different experiment, not a controlled
proof of improvement over the original evaluation.

Saved [browser live-demo runs](evidence/live-browser-v2/) include a completed
15:1185 v2 loss with four scratches, a separate failed live session, and mocked
records. They are development/playtest records, not additions to the official
trial count. Mocked responses never count as real inference. The proposed
physics-assisted agent is not implemented. See [development notes](NAVIGATION-AND-AGENT-PLAN.md).

## Reproduction and limitations

Working directory: `midterms/lzy2318831/`. These commands make no API calls:

```powershell
py -m fusion.final_analysis --verify
py -m unittest discover -s tests -v
py -m fusion.freeze
```

For a recorded demonstration, use the [README launch commands](README.md).
The default replay is the genuine 900:935 LLM loss. It shows recorded choices
and regenerated physics, not a live API session or evidence that one match is
representative. Do not rerun the completed paid launchers to reproduce statistics.

I chose a bounded, observation-only agent so its decisions would be inspectable
and inexpensive to evaluate. The results show that valid JSON and a rules prompt
were not enough for reliable cue survival. Frequent scratches and poor retained
scores are the main limitations. There was no live memory ablation: the game is
fully observed between shots, but that does not prove history could never help.
Direct Geometric controls also repeatedly scratch; I kept that weakness visible
instead of improving the baseline after evaluation.

Three situations, repeated deterministic boards, reduced direct-case coverage
and unequal completed seats limit generalization. There is no confidence claim
or overall LLM-superiority claim. Simulator/Smart results from earlier versions
are not live-LLM evidence.

The earlier navigation checkpoint passed164 project tests and18 freeze checks;
[final validation](evidence/final-geometry-01/REPORT.md) records the current suite.
[Navigation verification](evidence/navigation-fix-01/REPORT.md)
also records controller checks. The [scoped CI workflow](../../.github/workflows/midterm-lzy2318831.yml)
exists, but a green remote run for the submitted commit is **pending**.
A real [friend playtest](PLAYTEST.md) is now documented separately from these
results. The player found scratches frustrating and some edge/obstacle positions
difficult to recover, and suggested smoother terrain flow. These issues may
warrant investigating alongside the LLM's 25 scratches, but a common cause has
not been established. No official results or frozen rules were changed.
I confirmed that I personally watched my friend play independently without
coaching; the observed human playtest requirement is complete. The actual video
URL (temporarily deferred) and my review of this reflection remain pending.
Both distinct skill sessions are documented in [AGENT-TEAM.md](AGENT-TEAM.md);
the implementation and first skill-session reference are verified in
[the session audit](evidence/submission-readiness-01/SESSION-EVIDENCE.md).
Automated checks do not replace human observations.


Geometry-assisted stabilization: one bounded Back control replaces duplicate
result controls; new-match consent and cumulative server allowances remain
enforced. Contact/bank runout is reduced to 15 units, without the extra speed
margin, and direct contact/pot routes take priority over device-only proposals.
The historical 266-degree/power-4 cascade is reproduced offline; power 1 settles
in 354 ticks at that position. This is not a new genuine LLM evaluation or a
performance claim. See [stabilization report](evidence/stabilization-01/REPORT.md).

The student subsequently reviewed the [paired power experiment](evidence/power-2x-01/REPORT.md)
and explicitly chose **2x candidate power** for a more energetic Live LLM
demonstration, accepting increased scratch risk. Scratches were1/77 at1x and
14/77 at2x; all77 candidates settled in both arms. This is an all-candidate,
correlated saved-state simulation, not a genuine LLM selection experiment,
held-out match result or proof of improved win rate. The original official
11completed matches /2wins /9losses remain unchanged.

The live page initially prefers2x; its waiting-state **Candidate power** selector
provides1x as a stabilized fallback without editing code or restarting Python.
Power alone becomes `min(100, original_power * multiplier)`. Candidate IDs,
angles, targets/routes and strict LLM selection are preserved. At2x base stopping
and scratch estimates are explicitly uncertain. Trace, consent and per-call
metadata record the multiplier and base power. The1x candidate actions remain
the same; multiplier explanations/metadata mean its new model request is not
byte-identical to a historical prompt. See [runtime setting checks](evidence/power-setting-01/REPORT.md).

Further focused calibration verified that the newest genuine live run used2x:
base23,1,5,1,1,1 became offered and executed46,2,10,2,2,2. The low powers are
conservative base estimates, not a multiplier/display mismatch. A separate
previous **Adaptive energy - experimental** profile floored contact/pot travel bands
at25/35/50 (<=150/<=350/>350units), banks+5, never below2x, capped100. Unknown
escape/device routes retain2x. The original1x/2x request payloads are preserved.

On50saved genuine observations yielding96distinct candidate/state pairs,2x
versus this adaptive profile produced scratch-free pots11versus42, retained
points2375versus8270 and scratches9versus15, with zero simulation limits in
either arm. All three tested profiles and limitations are in the
[calibration report](evidence/power-calibration-01/REPORT.md). At the known266degree
position, adaptive25settled in844ticks; historical4still reaches9600. Movement
metrics include portal relocations/collision correction and contact metrics
are proxies. These are all-candidate development simulations, not held-out,
model-selected matches, new official results or a human playtest. The original
official11completed/2wins/9losses are unchanged; no win-rate improvement is claimed.


## Revised table: fusion-1.6.0-balanced

The confirmed final revision removes only left-entry/right-entry diagonals and
scales lower Slingshot boost parameters0.75 (320/60/420to240/45/315). Scoring,
shot quotas, bumper forces, Orbit assemblies and all other devices are unchanged.
Paths and outcomes can differ: the original official11completed/2wins/9losses,
prompt-v2experiments and power-calibration numbers belong to v1.5, not this table.
They are preserved unchanged rather than regenerated or promoted to v1.6results.

The full original source/spec/test snapshot and49official/smoke evidence files
are in `versions/kinetic-replenish-v1.5-final/`, with108source hashes and49evidence
hashes. Historical replay dispatches by version and strictly validates the old
fingerprint under archived physics; the recorded viewer also uses that Episode
and labels its original version. Original prompt-v2 Live hosting is bound to
v1.5without editing its prompt/agent; preferred Geometry-Assisted Live uses1.6.
1x/2x/Adaptive planning and all API/consent/budget settings are unchanged. Earlier
saved-state power tools explicitly use the archived simulator, retaining the
meaning of their historical data. No new paid LLM evaluation was run.

[v1.6 verification](evidence/table-balance-v16-01/REPORT.md) covers regression tests,
corner safety, both-version replay, cue animation, two consecutive actual Chrome
Live matches with synthetic replies and cumulative-budget behavior. Synthetic
browser completion is functional evidence, not genuine LLM quality or win rate.

The documented friend playtest also belongs to the original1.5table. No fresh
human playtest or genuine model evaluation was performed for1.6during this pass.


## Adaptive distance v2 on unchanged v1.6 physics

The optional Adaptive menu setting now uses `adaptive-distance-v2`: direct
contact, pot and bank-contact recommendations interpolate30→40 over0–150 cue
travel units,40→80 over150–350, then80→100 over350–1000, capped100 and rounded
half-up. This replaces the previous floor policy for those routes only.
Escape/device recommendations remain2x; existing1x/2x modes are unchanged.

Paired deterministic v1.6 simulations on38distinct candidate/state pairs from
6genuine and24synthetic saved observations compared previous Adaptive with v2:
contact proxies34→34, physical pots19→18, scratch-free pots8→17, retained
points1450→2935, scratches6→1, long powered cascades1→5, simulation limits0→0.
These are development candidate simulations, not new LLM matches or win-rate
evidence. In the historical266° public position transplanted to the v1.6 table,
25→32power changed settlement844→2217ticks and one pot→no pots, without a
scratch or limit. This is a counterfactual position, not a historical replay.
See [method, evidence and limitations](evidence/adaptive-distance-v2-01/REPORT.md).
The original official11matches/2wins/9losses remain associated with v1.5.

## Final remote CI disclosure

The first fork [Midterm workflow run](https://github.com/lzy2318831/game-dev-f26/actions/runs/42435757312)
for commit `a8fd61c43d7eeac5c569d8f859a9826d37009bb0` failed on Linux/Python3.11:
222tests ran with13errors and5skips. All13errors involve historical recorded
replay divergence, including strict checks during server creation. The3.12job
was cancelled by matrix fail-fast. Shared Setup and Minigame workflows passed.
Local Windows/Python3.15.1 separately reports222tests OK and24historical replay
verifications. The initial diagnosis was unresolved; the follow-up below
identifies the exact platform-math cause. No archived code, trace, hash, strict replay
check or game logic was changed to conceal it. Remote logs are retained in
evidence/submission-final-01/remote-ci-failure.txt. Later documentation-only
pushes must be assessed through their own workflow runs, not assumed green.

Follow-up: [runtime evidence](evidence/replay-compatibility-01/REPORT.md) proves
that Linux sin(123degrees) differs from Windows by one ULP at the identical
radian input. The default recorded match first diverges on shot9, third event
x-coordinate, then its observation hash. An isolated one-function
counterfactual reproduces the exact failing Linux hash on Windows. Windows
CPython3.11 replays all12shots exactly; this is not a Python3.11-only issue.
The CI compatibility correction uses Windows3.11/3.12 for all unchanged strict
tests and24historical replays. No replay comparison, physics or expected
result was relaxed. Linux bit-exact replay remains unsupported; its separate
CI numeric probe is diagnostic only. Current actual results appear in
[course PR checks](https://github.com/columbia-university-ai-games/game-dev-f26/pull/97/checks).
