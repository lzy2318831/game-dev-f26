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
