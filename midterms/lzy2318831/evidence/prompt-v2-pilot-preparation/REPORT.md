# Three-match prompt-v2 pilot preparation — 2026-11-07

Live execution has **not** been approved or performed. No new paid requests,
PR changes,push,submission or changes to original official artifacts.

Declared scope:seeds2701101/2701102/2701103,seatsP1/P2/P1,standard15-ball rack,
six LLM opportunities each,originalGeometric opponent,same pinned mini model,
same request settings. New source modules are separate from the original
evaluator and current recorded demo. Seed novelty was checked before declaration
by whole-project rg with no matches. Seed does not randomize the frozen game:
these are repeated opening-state trials,not three distinct new layouts.

Caps:one shared18attempt/$0.25estimated ledger,no retries. Reservations precede
dispatch and unknown charges retain reservations. Live output is fixed and
atomically created; repeat/alternate-directory invocations are refused. Failure
or interruption ends the pilot and preserves all prior data. No unused original
official allowance is silently reused. All actual results remain pending.

## Actual offline checks

- Six initial new tests failed import before implementation,then passed70.032s,
  including18synthetic calls and all3full match/frame replays.
- Independent review found interrupted-call usage missing from summaries. A
  new regression reproduced it:expectedmodel_calls1,butgotNone after a known
  synthetic reply and interruption. Fixed summaries read durable requests/results
  by trial,including unanswered-request unknowns and retained reservations.
- Final10pilot tests passed70.050s,including the full corrected3fixture-match
  workflow,all3visual-frame replays,no-retryHTTP429 failure,original evidence
  preservation,18call limit,cost-reservation refusal,interruption accounting,
  cached-proof relocation and rejection of fixture replays as genuine.
- Full project suite: **152tests passed in151.052s**.
- Freeze verification: **PASS18artifacts**,repeatedly including final check.
- Source/protected evidence hashes matched:official game,baseline,original LLM,
  prompt-v2 strategy,original results and current working recorded demo unchanged.
- PowerShell parser passed. Direct `.ps1 -Offline` execution was blocked by
  this managed shell's **Restricted** policy. No policy change/bypass attempted;
  do not claim the complete script file ran. Its exact Python command stages
  were exercised separately with the actual working Windows `py` application:
  freeze and full cached offline-check passed; interpreter probes matched
  `C:\Users\lzy21\AppData\Local\Python\pythoncore-3.15-64\python.exe`.
- Final cached preflight result:passedtrue,real_api_calls0,synthetic_calls18,
  configurationSHA256
  `466bba6ea3b022520ebe7f76f7f97c4bf6e9e44b63225f0eec1301b5e6021923`.
  Proof directory:evidence/prompt-v2-pilot-preflight/466bba6ea3b022520ebe/.
  Earlier pre-fix offline proof is retained separately; neither is live evidence.
- Best-replay CLI refused before live results exist,as intended; the fixed live
  output directory was confirmed absent. There is no fabricated genuine v2
  match for visual verification. Browser movement compatibility was exercised
  by generating frames from fixture traces,not claimed as a GUI observation.

## Independent read-only review

Reviewer:`/root/v2_pilot_review`,separate context,no edits/API/network/GUI or
student gate approval. Findings:

1. Interrupted results omitted journal usage before complete runner return.
   Fixed and regression passed as above.
2. Cached proof returned an old absolute path after clone relocation. Fixed:
   persisted relative location,current path reconstructed on return; relocation
   regression passed.

Reviewer independently tested18call rejection and cost refusal before dispatch,
then ran all10finalpilot tests with existing cached proof:10passed0.774s.
Freeze18passed. Reviewed fixed output,atomic creation,explicit approval gate,
best-match ordering and genuine liveHTTP200/prompt/request/action checks.
No blocking residual issue reported. Documentation was clarified:the launcher
runs the fixture workflow; unittest checks were run separately.

## After separate approval

Use the masked local PowerShell launcher documented in PROMPT-V2-PILOT.md.
It writes fresh real actions,usage,latency,costs,scores,scratches,illegals and
failures under evidence/live-prompt-v2-pilot-01/. Best genuine completed match
can be replayed at8791 using fusion.prompt_v2_pilot_replay,without API calls.
Best selection is by score margin,then ownscore,fewer scratches,declaration
order; all3rows remain the performance report. Original v1comparison is not
overwritten or claimed a controlled A/B experiment.
