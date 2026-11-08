# Final verified live evaluation — 2026-11-07

The genuine OpenAI `gpt-5.4-mini-2026-03-17` player completed **11 matches**
against the original Geometric baseline: **2 wins, 9 losses, 0 draws**. The
original HTTP429 failure remains the twelfth official trial; it is a failure,
not a played draw or a replacement result. No trials remain not-run. Twelve
matched Geometric-vs-Geometric controls completed. Smart AI was not used.

Evidence: [combined CSV](evidence/live-mini-recovery-01/combined-report/comparison.csv),
[combined summary](evidence/live-mini-recovery-01/combined-report/summary.json),
[independently recomputed analysis](evidence/final-submission-01/analysis.json),
[original failed run](evidence/live-mini-approved-01/manifest.json),
[recovery traces and manifest](evidence/live-mini-recovery-01/manifest.json),
[separate smoke](evidence/api-smoke-mini-01/result.json).
All24 saved trial/control traces were re-executed offline through the unchanged
engine and matched their saved events, state fingerprints and final outcomes.
Source evidence was hashed before/after analysis and remained unchanged.

## Protocol and interpretation

Frozen [suite6](fusion/evaluation.json): direct pocket, bumper-assisted and
risky/obstructed situations; seeds101/102, both seats, observation-only memory.
These declared cases were held out from policy tuning. Original declarations
and rule amendments remain in the versioned documents below. Both policies see
public observations and legal angle0–359/power1–100 proposals; only the real
model chooses its own shots. Six model decisions per completed match, no
fallback/retry/Smart substitution. Local limits:300s episode,20s request,
72 combined API attempts, original$5 estimated cap. No gameplay was tuned after
the official results.

| Situation | Completed W/L/D; failures | Mean LLM score, completed | Mean actual opposing Geometric score | Mean matched control target-seat score |
| --- | --- | ---: | ---: | ---: |
| Direct | 0/3/0;1 | 760.00 | 1533.33 | 0.00 |
| Bumper-assisted | 1/3/0;0 | 993.75 | 1046.25 | 827.50 |
| Risk/obstructed | 1/3/0;0 | 417.50 | 1508.75 | 1450.00 |
| All11 completed | 2/9/0; original failure separate | 720.45 | 1347.27 | 828.18 |

Head-to-head completed win rate is2/11=18.18%; wins across all12 attempted
trials are2/12=16.67%, with one separately reported provider failure. Total
completed LLM score7925 versus actual opponents14820. Across all12 attempted
trial rows, including failed0:0, LLM mean660.42 versus matched-control759.17
(control total9110). The12 standalone Geometric controls have target-seat
4wins/4losses/4draws against another Geometric player; those are not additional
LLM head-to-head results. Corresponding11 controls exclude the failed-row
control and have mean828.18.

| Case / seed / LLM seat | LLM : actual opponent | LLM result | Matched control target score | Input / output tokens | Model latency total(s) | Estimated USD |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| direct /101/p1 | 0:0, no shots | HTTP429 failure | 0 | unknown | 1.796220 | unknown |
| direct /101/p2 | 990:1455 | loss | 0 | 21809/132 | 8.493848 | .01695075 |
| direct /102/p1 | 605:1660 | loss | 0 | 17237/126 | 7.276970 | .01349475 |
| direct /102/p2 | 685:1485 | loss | 0 | 21960/132 | 6.896482 | .01706400 |
| bumper /101/p1 | 1235:185 | win | 460 | 17530/126 | 6.087678 | .01371450 |
| bumper /101/p2 | 1095:1500 | loss | 1195 | 20910/138 | 6.492169 | .01630350 |
| bumper /102/p1 | 745:1565 | loss | 460 | 17411/126 | 5.997991 | .01362525 |
| bumper /102/p2 | 900:935 | loss | 1195 | 18589/144 | 6.443127 | .01458975 |
| risk /101/p1 | 295:555 | loss | 2875 | 15427/138 | 6.214251 | .01219125 |
| risk /101/p2 | 130:2670 | loss | 25 | 19503/144 | 6.012800 | .01527525 |
| risk /102/p1 | 1010:385 | win | 2875 | 15261/132 | 5.844375 | .01203975 |
| risk /102/p2 | 235:2425 | loss | 25 | 18354/144 | 6.625019 | .01441350 |

All11 completed matches ended `shots_exhausted`. Engine-illegal actions:0 for
LLM, actual opponents and controls; invalid model proposals:0. The failure is
provider_error/HTTP429, not an illegal proposal. Scratches:LLM25/66shots,
actual opponents20/66, controls38/72. Credited non-foul pots:LLM36, actual
opponents71, controls40. The existing comparison CSV's `object_pots` counts
physical pocket events including foul shots (LLM80), so it differs from the
engine's credited-pot metric; neither value has been rewritten.

## Usage, latency and cost

Recovery:66 real HTTP200 calls;203991 input +1482 output =205473 reported
tokens; estimated$0.15966225. Successful-call latency total72.384709s,
mean1.096738s, median1.063078s, range0.802775–1.866169s. Including the original
rejection, official model-call latency totals74.180930s. The72 target-seat
Geometric control decisions total3.276747s, mean0.045510s. These are recorded
decision/wall-clock measurements on the local machine, not animation duration
or guaranteed provider-only network time.

Original failed request:1attempt; usage/actual charge unknown; retained local
reservation$0.0109875. The old handler did not save the provider body, so the
exact quota/rate/billing error message remains unavailable. A later successful
smoke is separate:1call,2132input+24output=2156tokens,$0.001707.

Combined:68/72 attempts;207629 known tokens including smoke, plus unknown
failed-request usage; known estimated cost$0.16136925; conservative charged-or-
reserved total$0.17235675. No new API calls were made for analysis/replay.
Estimates use the saved2026-11-07 rates ($0.75 input/$4.50 output per million,
cache discounts ignored); these are estimates, not provider invoices. Remaining
call/budget capacity is not approval to spend it on a live demo.

## Reproduce and demonstrate offline

Working directory:`midterms/lzy2318831/`:

```powershell
py -m fusion.freeze
py -m unittest discover -s tests -v
py -m fusion.final_analysis --verify
py -m fusion.demo
```

Open `http://127.0.0.1:8785`, click **Watch LLM Agent Play**. The viewer shows
**Recorded LLM Evaluation**, automatic saved shots and the original result.
Default:bumper/102/p2, a close LLM loss900:935, selected for demonstration, not
as a representative estimate. Every model decision is matched to its saved
live HTTP200 journal result. Physics frames are regenerated using the frozen
engine and checked against every saved event/fingerprint/outcome; they were not
stored original video. No new inference or manual move selection occurs.
See [recording instructions](DEMO-RECORDING.md).

## Limitations and pending evidence

The LLM is not stronger overall:it loses9/11 completed head-to-head matches and
scores below the paired baseline mean. Its stronger bumper-control mean does
not establish general superiority. Direct controls repeatedly scratch; this
weakness is disclosed, not repaired after evaluation. Deterministic seed repeats
can produce identical control trajectories and are not independent samples.
Only three scenarios/two seeds and observation-only mini-model play were tested;
there is no live memory ablation or Smart-opponent experiment. One provider
failure reduces successful direct-case coverage and seat balance. No confidence
or broad generalization claim is made. Later official evaluation reuse may need
fresh held-out cases if tuning resumes; gameplay and policies remain frozen.

Actual remote CI, two distinct saved skill-session links, student-authored
reflection, an observed other-person playtest (or honest rubric5b omission
explanation), a3–5minute recording and approved PR/CourseWorks submission remain
pending. Automated checks do not replace human feedback. Browser visual control
was rejected by automatic approval review; recorded playback is verified by
offline/HTTP/JavaScript checks, not claimed visually observed.

---

## Archived pre-completion notes — statuses below are superseded

# Official live evaluation: one HTTP429 failure, investigation complete

Savedrun evidence/live-mini-approved-01 is preserved unchanged. One request,
firsttrialprovider_error/HTTP429;0LLMmatchescomplete,11trialsnotrun. One matched
Geometriccontrol completed. Provider message/code were discarded by oldhandler;
exactbillingvsratelimitcause is unresolved. Diagnosis/fix/recovery:
evidence/http429-diagnosis/DIAGNOSIS.md. No new APIrequest or automaticrerun.

Originalrequest's tokenusage/actualchargeunknown;localreservation$0.0109875.
1of72attemptsused,71remaining;keep originalfailure and original$5aggregatecap.
Continuation requires explicitnewauthorization under user's latestinstruction.
Logging repaired and verifiedoffline117tests;no frozenchanges. No LLMquality
conclusion can be drawn from provider rejection.

--- Historical preflight/implementation notes below ---

# Official live evaluation approved - awaiting credentials

User explicitly approved OpenAI gpt-5.4-mini-2026-03-17,observation_only,
12live LLMmatches,12matched originalGeometric controls,max72modelcalls,
$5localestimatedAPIcap. No Smartsubstitution,gamechanges,pushorPRauthorized.
Preflight:18freezehashespass; exact12/12/72protocolverified. OPENAI_API_KEY
absent in process,user,machine environment. Thus officialevaluation NOTSTARTED:
0modelcalls,$0APIcost,no live outcomes or failed-trial statistics fabricated.
Approval record:evidence/official-evaluation-preflight/approval-and-preflight.json.

Run .\run-approved-evaluation.ps1 locally from projectfolder for masked
session-onlykeyinput and exact approved command. It refuses an existing official
run directory,preserves failures and restores sessioncredentials afterward.
Do not delete/switch run directories to reset the approved limits. Return the
completed artifacts for analysis; no key in chat. Approval remains valid.

--- Previous implementation/protocol notes ---

# Current real LLM evaluation workflow - prepared, not run

Real adapter/evaluator implemented,live_calls=0 and no live results. See
LLM-SETUP.md for dated official modelprices and approval-gated commands.
Frozen suite6,allcases unchanged. Default12live matches(3situations,2seeds,both
seats),12matching Geometriccontrols,max72calls. Optionalhistoryboth doubles
calls; optionalSmartopponent is separate. Unknowncost/usage,failed/interrupted/
notrun trials retained. CSV and raw traces include all rubric fields.
113local tests and explicitoffline fixture verify workflow; not evidence of
real model strength. Game/visual18artifactfreeze unchanged. Recording,human
notes,distinctskill-sessionlinks,studentreflection,remoteCI stillpending.

---

# Current replenishment amendment - suite6

Current version fusion-1.5.0-replenish. Suite6 preserves every suite5ball
placement,seed andtrial plan; only transition metadata amended. Original
full declarations archived in versions/final15-v1.4/. Opening15objects,threshold8,
batch5,max2,initialused0. Live trials still pending; no tuning or paid calls.
Count total pocket events, not distinct recycled numbered IDs; maximum25pots.
All policies receive public replenishment state. Geometric algorithm unchanged;
Smart only adapts terminal-clear prediction to supplies, not search/budget.

Earlier Smart6match results below apply ONLY to v1.4without replenishment.
They are not re-executed or relabeled as current performance. Future LLM trials
must use current frozen suite6/gamehash and compare against Geometric. Any
Smart comparison rerun needs separate results. Current offline safety/replay
checks: evidence/replenish-1/REPORT.md. No live/human/recording evidence invented.

---

# FINAL15 evaluation protocol and current results

Current final game: fusion-1.4.0-final15. Physics/visuals frozen after rack/Smart
validation. Geometric baseline source unchanged. Smart and real LLM separate.

## Future live LLM evaluation (not executed)

Frozen suite5 in fusion/evaluation.json: direct pocket,bumper-assisted,and risky/
obstructed situations, now15objects each. Extended before Smart implementation;
only clear filler balls added, prior suite preserved. No tuning on these cases.
At least2live trials per situation, seeds101/102 and balanced model seats;
matching Geometric trials, optional Smart as alternative opponent. Public
observation/legal shots only; no model simulator tools. Report runtime provider/
model,prompt/config/game hashes, call attempts including failures,input/output
usage,dated price/cost,latency,outcomes and traces. No fixture substituted.
Max12calls/match,20sec/request,300sec/match. Memory comparison remains planned:
observation-only vs at most2visible shots,2000characters; do not claim it ran.

Provider/credentials/budget not yet chosen, live_calls=0. Human playtest and
recording pending. Repeated deterministic fixture seeds are not live trials.

## Completed Smart development comparison

Separate frozen fusion/smart-comparison.json,3cases(direct,pinball,rack),seed101,
each seat order,6matches. Smart has disclosed simulator access; original
Geometric does not. Neither is an LLM. Policy fixed before matches; no retuning.
Raw traces replayed, all shots_exhausted, no execution failures.

# Smart AI vs original Geometric AI - development comparison

Executed2026-11-07, final15engine. Protocol fusion/smart-comparison.json frozen
before Smart implementation/tuning:3fixed15-object situations, seed101,
both seats per situation =6matches,36opportunities each. Deterministic seeds
are not independent repeated stochastic trials. No held-out LLM scenario used.
No retuning after this run. Every trace replayed successfully. Both agents
receive detached public state; Smart additionally has a counterfactual physics
simulator. This capability difference is explicit, not hidden information.

| Measure | Smart AI | Geometric AI |
| --- | ---: | ---: |
| Average match score | 2489.17 | 368.33 |
| Total objects pocketed (including scratches) | 54 | 15 |
| Credited non-foul object pots | 54 | 9 |
| Wins /6 | 6 | 0 |
| Scratches /36shots | 0 | 23 |
| Illegal actions | 0 | 0 |
| Average planning sec/shot | 6.588 | 0.044 |
| Execution failures | 0 | 0 |

| Situation | Smart mean score | Geometric mean score | Smart wins |
| --- | ---: | ---: | ---: |
| direct | 2967.5 | 497.5 | 2/2 |
| pinball | 2445.0 | 0.0 | 2/2 |
| rack | 2055.0 | 607.5 | 2/2 |

Smart is stronger **on this small fixed development suite**:6/6wins,100% vs0%,
with higher scores/pot totals and fewer scratches. This does not prove general
optimality or replace real LLM evaluation. Direct/pinball labels describe the
initial situation; a player may choose any legal path. Metrics count physical
pocket events separately from scoring-credit pots, since scratches remove balls
but void scores. Geometric source SHA256 matches preserved Kinetic baseline.

Wall times measured during ordinary local test/browser activity (CPU contention),
not a dedicated hardware benchmark. Smart has max24candidate/40000tick work
budget, not a portable hard wall-clock deadline. Candidate counts/ticks are
bounded deterministically; UI thinking was7.157s in the automated browser run.
Raw per-shot latencies, events and outcomes: comparison/*.json. summary.json is
machine-readable. All6matches ended shots_exhausted, no provider/model calls.
LLM live trials and human-experience evidence remain pending.

## Limits

Small deterministic development suite, no uncertainty intervals/general
optimality claim. Hardware timings include contention. Smart work-bounded;
no hard portable wall deadline. Dense mechanisms and many balls increase
prediction cost; candidate search is shallow, not exhaustive. No spin/full3D.
Human fun/readability cannot be inferred from automated QA. Real live-model,
cost/provider and observed human evidence remain required before submission.
# Approved continuation after successful smoke

The student approved only the eleven previously not-run official trials after
HTTP200 smoke verification. See [RECOVERY-EVALUATION.md](RECOVERY-EVALUATION.md).
The combined view keeps the original HTTP429 failure; smoke usage/cost remains
separate. Preparation tests are offline fixtures, not measured LLM performance.
Use the recovery reports for actual scores and usage after local execution.

