# Limited replenishment implementation and validation

2026-11-07, fusion-1.5.0-replenish. User reported late-match emptiness and
explicitly authorized limited refill only. No other redesign, paid calls,
push,PR submission or course gate approval. Re-freeze follows this instruction.

## Current rules / actual process

competitive-rule-change invoked by name; read submission instructions/skill,
rules/source map/evaluation. R1-R4spec and map declaration before code/tests.
Opening15objects+cue unchanged. After VALID fully settled shot, score and any
scratch respot resolve, then at<=8objects add5, max2events/match, one/boundary.
No final-opportunity/failed/moving/invalid/reset/observe spawn. Replenishment
precedes earlyclear while supply remains (0becomes5), otherwise ordinaryclear.
Six shots each still the strict bound. Lowest inactive/missing IDs1..15reused,
no duplicateactiveIDs, zero velocity/zero spawn points. Max25physical objectpots.

Pure ordered-grid placement checks active balls,bumper bodies,guide capsules,
pockets,device apertures/exits,spinner/lanes,sling interiors. Whole5batch planned
before commit; unavailable batch defers without spending supply. No new devices,
physics coefficients,score rules or controls. Public detached replenishment
field includes threshold,batch,max/used/remaining,count,pending and rules.
Geometric byte-identical. Smart only adjusts prematureclear prediction; search,
candidates and budgets unchanged. It previews physical shot, not post-refill
positional tiebreak, a disclosed limitation. All agents get same public state.
Boundary event/frame, spawn glow and short toast notify without scoring.

Initial7acceptance tests red:3failures/4errors (missingrule/counter/helper and
oldclear behavior). Actual log red.txt. Implemented then allpass. Two old
clearance-only fixtures now explicitly exhaust supply to test unchanged end
behavior after stock runs out. No failure hidden or historical result relabeled.

## Executed checks

- Full project suite100tests97.419sOK (tests.txt). New10focused replenishment
  tests cover threshold8/9,two-eventlimit,one/boundary,zero-objectpriority,
  finalquota,scoring/scratch/reset,all-resting,atomicblockedbatch,IDcopies,
  overlap/geometry and replay/tamper. Updated boundary-frame assertions reran
  focused10tests19.846sOK (focused.txt).
- Fresh read-only /root/replenish_review independently ran10tests19.804sOK,
  plus100seeded placement states with0..8objects; all yielded5safeunique IDs.
  No blocking findings. Verified baseline/device/geometry unchanged, minimal
  Smart terminalguard; no edits/providercalls or gate approval.
- Default Geometric-vs-Geometric seed101:12shots,shots_exhausted,1320vs765,
 2replenishments,13objects left,0illegal/executionfailures. Trace replay exact:
  offline-match.json. Refills occurred after shots7and11. This is development
  safety/replay evidence, not a new policy-strength or live-model benchmark.
- Browser localhost8772:all prior aim/power/physicsdevice/turnlock/Smartautonomy/
  thinking/playback/fullending/viewport/resetrace checks pass,zeroJSexceptions.
  New normal-public-UI Geometric match captures shot7batch of5,used1,remaining1,
  objectcount13,0points,glow and visible toast. fusion-browser-check.json,
  replenishment-glow.png and replenishment-notice.png are actual captures.
  Playback accelerated for automation/capture, authoritative simulation intact.
  Original Smart-flow extension failed to capture a batch payload despite the
  completed match state havingused2; switched to exact reproducible Geometric
  fixture matching offline trace. No gameplay fix was inferred from that QA
  capture failure. A final separator cosmetic correction was rechecked visibly.
  Browser QA is not an observed human playtest.
- Root starter tests36run/4environmenterrors (missing SDK/Windows symlink
  prerequisites); setup incomplete(auth/Pyxel/root tests). Actual logs retained,
  separate from100passing project tests. No fixture replaces live evaluation.
  git diff --check passed. RemoteCI not run; current workflow checks freeze.

## Evaluation amendment, preservation and freeze

Suite6 changes rule metadata only: all suite5placements,seeds,trialplans exactly
unchanged/valid. Original declarations/results/code preserved in
versions/final15-v1.4/. Development comparison also version-amended without
running it; outputs now use a new directory to protect v1.4data. Old6match
Smart performance remains v1.4only, no current strength/liveLLM claim.
Count rawpocket events rather than distinct reused numbers, max25objectpots.

Preservation hashes verify every archived snapshot and old source manifest;
baseline.py/devices.py/geometry.py unchanged (preservation.txt). Exact minimal
Smart change in smart-compatibility.diff. Current gameplay/visual hashes in
fusion/gameplay-freeze.json, verified via python -m fusion.freeze. Only this
submission directory changed this turn. Student owns gates/interpretation.

## Play / remaining work

From projectdirectory python -m fusion --port 8772, open localhost8772. Server
launched. Same three modes/aim-pull-release. Watch replenishment notice after
objects fall to8or fewer. No replenishment after final shot; normal earlyclear
once both supplies used. No unlimited ball or score loop.

Game re-frozen after this authorized exception. Remaining work stays real LLM
transport/approved live trials/costs,observed humanplaytest,recording,independent
skill-session references,student reflection/approved PR. No fabricated evidence.
