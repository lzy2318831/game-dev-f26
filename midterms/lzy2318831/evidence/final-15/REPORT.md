# Final15 validation and freeze evidence

2026-11-07, fusion-1.4.0-final15. User authorizes final rack count and Smart AI
only; no table/device/scoring redesign. Original procedural assets/code. No
paid calls,external assets,push,PR submission or gate approval. Technical
freeze is authorized; remaining rubric evidence is not declared complete.

## Actual implementation / rule-change process

competitive-rule-change invoked by name; submission instructions and skill,
current rules/map/evaluation read. Z1-Z3 design amendment declared before code.
Rack acceptance first failed7!=16; after implementation exposed a test-author
mistake treating Ball as dict, corrected to .x. Smart tests initially errored
because smart.py and hvs mode did not exist. Logs/tool results are actual,
not invented regression evidence. New16-ball rack uses5rows with24spacing,
sqrt(3)/2horizontal step. No devices moved. UI renders solids/black8/stripes9..15.
All five operations and six-shot quotas/scoring/termination remain unchanged.

Smart is new deterministic simulator-based policy; Geometric source unchanged.
Smart receives only public positions/IDs/device geometry/scores/quotas; creates
new Ball objects and physics ledgers with authoritative tick(). No live Episode
or hidden evaluator data.24candidate maximum,40000total ticks,480tick previews,
9600per candidate. Includes original Geometric action then direct ghost pots,
combo contacts,mirror banks,all mechanism angles and fixed exploration at
several powers. Geometric reference resolved first; only settled predictions
can win final ranking. Scratch/points/pots/position and terminal margin ranked.
No portable hard wall-clock deadline: work bound deterministic, seconds measured.

Conservative broadphase avoids irrelevant distance projections without changing
coefficients. Local preserved-reference test and independent4break exact
per-tick comparison confirm identical ball states/events. No separate physics
approximation introduced. Preview/counterfactual states do not mutate live game.

## Verified results

- Full project suite90tests,59.319s,OK: tests.txt. Rack/no-overlap/determinism,
  multiball break/scoring, fullgame termination, all previous pinball rules,
  Smart legal/budget/determinism/ID preservation/matching predictions, wrong
  seat/state isolation/serverautonomy, archived physics equivalence.
- Fresh independent /root/final15_review:6final tests passed13.808s. Geometric
  baseline SHA256 equals preserved version. Archived physics exact after every
  tick at angles0/60/225/345,power85 on16balls, through6957/4987/830/7196ticks.
  No blocking findings. Reviewer edited no files or gates.
- Review caught thinking HUD staying stale after movie assignment. Added HUD
  refresh after assignment and INPLAY card label. Independent re-review and
  browserconfirm thinking->BALLSINMOTION; no game mechanics changed.
- Browser localhost8771:16balls rendered, all three modes, actual mouse drag,
  power/aim,baselineautomaticreply, inputlock, Orbit/reset, Skyway/Vault chain,
  fullmatchending, viewport fit, delayed-response restart regression and new
  automatic Smart turn. Smart example24candidates/40000ticks,9settled,7.157sec,
  choseangle120power85, predicted910pts/pots11,13,15; source smart, playback
  statusBALLSINMOTION, zeroJSexceptions. Raw fusion-browser-check.json and
  final15-smart-thinking/table/shot.png. Screenshots visually inspected.
  Time acceleration only for QA playback/event capture, not engine physics.
  This is automated application QA, not an observed human playtest.
- Six development matches fixed before Smart implementation, identical seeded
  situations/both seats. Smart6/6wins,mean2489.17score,54rawpots,0scratches;
  Geometricmean368.33,15rawpots(9credited),23scratches.0illegal/0failures both.
  All6ended shots_exhausted and replayed. Planning6.588secvs0.04382per shot.
  COMPARISON.md and comparison/summary.json include per-situation results/raw
  traces. Small deterministic suite, CPU contention during local checks; not
  a general strength guarantee or live LLM evaluation. No post-result tuning.
- Root starter36tests/4errors (SDK/Windows symlink prerequisites); setup remains
  incomplete (auth,Pyxel,root tests). Actual logs saved. Project uses stdlib;
  root failures not relabeled passing. git diff --check passed.
- CI workflow now includesSmart offline match/replay and freeze verification;
  remoteCI not run. No paid/model calls in CI. Model live_calls remains0.

## Preservation and freeze

Six-ball Kinetic snapshot and earlier versions/hash manifests remain unchanged;
original evidence kept separate. Geometric unchanged source explicitly verified.
Gameplay/visual manifest fusion/gameplay-freeze.json; `python -m fusion.freeze`
checks it. Freeze covers engine/devices/Smart/Geometric/art/rules/suites, while
pending real LLM transport/evidence work can proceed separately. No more table
redesign. Prepared local PR-DRAFT.md only; no remote PR created.

## Play and remaining Midterm obligations

From submission directory `python -m fusion --port 8771`, then localhost8771.
Python3.11+ and modern browser, no installs. Choose VSSMARTAI, VSGEOMETRIC or
2PLAYERS; point/pull/release,Escape/right-clickcancel. Smart thinks/shoots
without human action; simulation preview does not steer the actual shot.

Smart is not an LLM. Internal simulator access is disclosed; Geometric/future
LLM have no hidden-state/simulator tools. Work limits fixed, wall-time hardware
variable. Small search is not optimal. Higher ball count increases CPU work;
local tests and browser measured, no claim of universal latency.

Next: real provider transport, approved-budget repeated live LLM trials vs
Geometric(frozen suite5),cost/call/failure tracking,actual human playtest,
3-5minute recording,two independent skill-session references,student reflection
and approved PR preparation/push. MIDTERM-NEXT.md is explicit. No fabricated
experimental,reusable-skill-session,human,remoteCI or submission evidence.
