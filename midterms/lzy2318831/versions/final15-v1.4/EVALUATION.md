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
