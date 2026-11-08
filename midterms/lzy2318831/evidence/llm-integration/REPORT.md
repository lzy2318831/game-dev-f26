# Real LLM integration: implemented, paid approval pending

2026-11-07. Frozen game versionfusion-1.5.0-replenish. No gameplay/visual changes,
no paid/provider API calls, no push/PR/submission. Real OpenAI HTTPS transport
implemented and mocked offline; real account/model compatibility is unverified
until an explicitly approved live call. No real-model results invented.

## Inspectable implementation

- fusion/llm.py: separate ModelPlayer,Responses JSONschema request,data-only
  public build_context,legal integer angle/power validation,secure environment
  transport,approvalgate,parent watchdog,append-only audit and run budget.
- fusion/llm_eval.py: network-free default plan; explicitly gated live suite,
  matched originalGeometric controls,optional separateSmart opponent/history,
  hashes,pertrial atomicmanifest,perstepJSONL,replay,CSV/JSON failure-inclusive
  reports. Default12live+12controls,max72calls; bothmemory24live/144calls.
- fusion/runner.py: newLLM route retains usage on failed/expired calls,actual
  engine.step commits proposals and records authoritative outcomes. Frozen
  player.py/engine interface untouched. Old model fixture route remains.
- fusion/llm_smoke.py: explicit OFFLINE fixture only; cannot prove live play.
- tests/test_fusion_llm.py:13offline contract/regression/accounting tests.

LLM receives developer rules plus canonical publicstate/legal schema,optional
last2visible shots(max2000chars); last_events capped32,request max60000bytes.
No repository/shell/simulator/provider credentials/evaluator labels in payload.
No modeltools,storefalse,standardtierdefault,reasoningnone,512outputcap. Model
selects action; adapter rejects malformed,duplicate,refused,incomplete or
illegal replies; no repair/retry/baselinefallback. Invalid model proposals
are reported separately from engine-invalid counters. Gameplay frozen.

Approval/provider/model/key/runbudget all required for CLI live use. Keyread
only forHTTPS authorization,never audit/prompt; no redirects/errorbody logs.
Before dispatch request journal+costreservation isfsynced. Returned legal action,
modelIDs/usage/dates/rates/cost/latency retained; callfailurescount. Unknown
costs/timeouts keep reservation,not falselyzero. Localbudget is conservative
estimate,not providerbillingguarantee. No credentials inspected or revealed.

## Actual executed checks

- Full project113tests,111.470s,OK:tests-final.txt. Earlier full113pass111.931s
  retained tests.txt. Final13focusedtests12.637sOK:focused-final.txt.
- RealHTTP request construction/header/no-redirect behavior tested using a
  mocked opener and fake testkey; no actual provider request. Network-free plan
  saved proposed-plan.json. Known usage/cost tests use fake token numbers,
  never represented as real usage or paid experimental evidence.
- Entire offline adapter->engine match6fixture responses,12shots,515vs905,
  shots_exhausted,1refill,0invalidactions,noexecutionfailure; replay passes.
  offline-smoke-final/trace.json and calls.jsonl clearly mark NONLIVE. These
  scores are fixtures,not LLMperformance. Earlier smoke preserved separately.
- Original v1.5offline trace replay remains compatible. Gameplayfreeze18artifacts
  passes; no manifest reset or byte change to engine,baseline,Smart,interface,
  art,rules or frozen suite. No new browser/gameplay claim this turn: UI unchanged.
- Fresh read-only /root/llm_integration_review independently ran13tests14.369s,
  checked freeze18and re-reviewed fixes; no remainingblockingfinding. No edits,
  API calls or gateapproval. Full findings in INDEPENDENT-REVIEW.md.
- Root starter36tests/4environmenterrors (SDK/Windows symlink); setup incomplete
  (auth/Pyxel/root tests). Rawlogs retained,separate from project113pass.
  No dependency installation or silent fixture replacement.
- CIworkflow adds offline adapter smoke/replay; no API credentials/livecalls.
  RemoteCI not executed because current changes unpushed/unsubmitted.

## Real defects found and fixed

1. Near-deadline completed replies were aborted before call-event append,
   losing traceusage/cost despite audit retaining it. Independent deterministic
   mock reproduced model_calls1/episode_timeout/emptycall_events. Movedappend
   before deadlineabort; regression now preserves inputusage7andcost.
2. Generic malformed envelope errors dropped usage. Validate output/content
   shapes after extracting metadata; test covers None/items/partialcontent.
3. Offline failure-accounting guard wrongly zeroed known fixtureusage0!=100;
   only nondispatched metadata withoutusage is zeroed now. Test passes.
4. CLI maxcalls0 used `or`default; nowexplicitpositivevalidation. Smartopponent
   controls nowpreserveopponent,replaceonlyLLMseat. Geometriccontrol latency
   uses realsteplatencies (review reproduced0reportedvs0.394measured).
5. DuplicateJSONkeys reject; unknownusage checks both input/output; perstep
   commits durable beforestdout; validatedaction included in successfulaudit.
6. Packaging: core.autocrlf=true would alter frozen CRLFbytes in Gitstorage.
   Actual precheck engine rawblob e730b15ef90167493dca1d640682cc27f3a2f85f
   differed from cleanedblob ff378021fc1fda811ed0157ea6c8a15c61234938.
   Project .gitattributes '* -text' preserves exact bytes without editing game.
   All18Gitclean/rawblob checks nowmatch(packaging-check.json),no staging/object
   writes. This prevents cleanLinuxcheckout freeze failure. git diff --checkpasses.

## Dated model options / proposed approval

Official OpenAI documentation verified2026-11-07,exact URLs LLM-SETUP.md.
Standard input/output per1M: Luna0.10/0.50, pinnedMini0.75/4.50,Sol2/10;
older pinned5.4also supported2.50/15. Deprecatednano not offered. At72requests,
5000input+512outputeach,estimates$0.054/$0.436/$1.089 respectively,not actual
measured costs. Cacheddiscounts ignored; taxes/accountavailability unverified.

Proposed scope for user approval:OpenAI,gpt-5.4-mini-2026-03-17,
observation_only,officialGeometric opponent,12live+12controls,max72calls,
localestimatedbudget$5. Credential setup uses masked localPowerShell input,
not chat/files. No live command has been executed. Wait explicitapproval.

## Submission audit and boundaries

SUBMISSION-CHECKLIST.md maps actual assignment requirements. Independentreview
and offlineCIconfiguration complete; currentremoteCI,realLLM trials/costs,
two distinct actualskill-sessionreferences,observed humannotes,studentownvoice
interpretation and3-5min recording remainpending. Ownplayfeedback is attributed
to user,not invented observed thirdparty evidence. No recordingartifact/link
recorded. PR-DRAFT.md prepared locally with login/title/requiredlinkplaceholders,
notready for submission. Midterm assignment explicitlyrequires noAsanalinks.
Studentowns approval,gates and finalCourseWorksPRURL. No deadlines changed.
