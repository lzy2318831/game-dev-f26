# Evaluation declaration v1

Declared November 6, 2026, before executable implementation or prompt tuning.
Status: protocol only; **no trials have run and no results are claimed**.
Commit this declaration before tuning and link that commit in the final report.
Coordinates and mechanics are specified in RULES.md. All matches start 0-0
with six object balls. IDs follow the order of coordinates below.

## Frozen situations

| Situation | Cue | Object positions | Decision being tested |
| --- | --- | --- | --- |
| S1 open lanes | (250,250) | (150,100), (450,100), (800,100), (150,400), (550,400), (850,400) | Direct pot selection and power; avoid wasting turns. |
| S2 obstruction / rails | (200,250) | (400,250), (600,250), (750,150), (750,350), (550,100), (550,400) | Blocking, cut shots, and cushion alternatives. Do not assert a forced bank without verifying it. |
| S3 scratch risk | (500,350) | (500,100), (100,100), (900,100), (200,350), (800,350), (650,200) | Immediate score versus scratch exposure and opponent opportunity. |

These three layouts are held out from prompt tuning and policy-weight fitting.
Do not use their match results to revise the submitted policy and still call
them held out. Separate development layout D0 is the default triangle in R1;
create any debugging layouts under a development-only manifest. Basic geometry
validation is allowed before evaluation; if a frozen layout is defective,
record a dated amendment and rationale before running tuned policies on it.

## Required main comparison

Run one observation-only model against the geometric baseline. For each
situation run two fresh live matches: model as p1 (seed 101), model as p2
(seed 102). These are six matches with real API decisions. Seeds identify
replays; physics is deterministic and the seed does not pretend to control
provider nondeterminism. Seat reversal controls first-move advantage but the
two matches remain a very small sample. Baseline vs Baseline on all three
layouts provides an offline seat/termination sanity check.

Use the same fixed model, prompt, baseline weights, rules, action vocabulary,
and limits for every main trial. Maximum 12 model attempts per match, hence
72 live requests across six main matches. Failed requests count. Do not use
model response replay in place of fresh live trials. No response repair calls
or hidden retries. No silent fallback moves.

## Memory experiment

Repeat the six matched games with the same model configuration except for
last-two-decision/result visible history (maximum 2000 characters; oldest
records dropped first). Both players can receive this same history, but the
geometric policy deliberately ignores it. Total planned budget: at most 144
live requests for main plus memory conditions. Compare outcomes, invalid
actions, tokens and latency. Fully observed state suggests memory may add
cost without improving decisions; test that hypothesis and explain the
observed result. No persistent cross-match memory or learning is claimed.

Select a provider and compute a monetary cap using current dated input,
output, and any reasoning-token prices before live execution. If access or
budget cannot cover the protocol, document the issue and seek an instructor-
agreed reduced equivalent; do not silently reduce trials or invent results.

## Optional alternative opponent

Only after the main comparison, CI, review, playtest, and recording are done,
consider a nearest-object direct-aim scripted opponent on the same situations
and both seats. It is a secondary opponent, not a replacement for the strong
geometric baseline. Model-vs-model self-play doubles call expense and is
excluded from the required scope. Repetition alone is not learning.

## Fairness and recording

Both players see the same public positions, scores, geometry, action ranges,
and limits. The baseline uses deterministic geometry with no engine rollouts;
the model uses remote inference. Record this compute asymmetry and the
baseline's elapsed time. Neither gets future states or privileged scenario
annotations. The model must return its own action; humans cannot select moves.

Capture each trial's game commit/version, scenario, seed, seat assignments,
provider, requested/resolved model ID, configuration/prompt hashes, history
condition, every action and acceptance result, visible events, scores,
terminal reason, winner/draw/failure, attempts, invalid actions, scratches,
request attempts/failures, limits reached, elapsed time, token usage by
reported category, and estimated cost with dated price URL and currency.
Unavailable usage is `unknown`, not zero. Retain provider failures and
truncated matches. Redact credentials and personal data. Keep small JSONL
traces in `evidence/`, not root-ignored `reports/`.

## Results (pending actual execution)

| Situation / condition / model seat / seed | W/L/D or failure | Scores | Invalids / scratches | Attempts / calls / limits | Latency | Tokens | Dated cost | Trace / version |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| No executed trials | pending | pending | pending | pending | pending | pending | pending | pending |

Aggregate by situation and condition; count failures in the trial denominator
separately from competitive W/L/D. Include baseline statistics and representative
success/failure analysis. Do not claim statistical certainty from this sample.

## Offline development checks (not held-out or live results)

Default D0 rack, seed 101, v0.2.0; no S1/S2/S3 matches run or used for tuning:

| Seats P1 / P2 | Scores P1 / P2 | Outcome | Attempts | Invalids | Scratches P1 / P2 | Model calls | Trace |
| --- | --- | --- | --- | --- | --- | --- | --- |
| geometric / direct aim | 5 / 1 | P1 wins, table_cleared | 19 | 0 | 0 / 0 | 0 | evidence/dev-baseline-p1.json |
| direct aim / geometric | 2 / 4 | P2 wins, table_cleared | 24 | 0 | 1 / 0 | 0 | evidence/dev-baseline-p2.json |
| geometric / geometric | 3 / 3 | draw, table_cleared | 9 | 0 | 0 / 0 | 0 | evidence/dev-baseline-self.json |

These are deterministic development runs, not independent samples or evidence
of model strength. No inference tokens or API cost were incurred. Traces
contain measured decision and match latency plus engine source hash. Baseline
weights were not tuned on the frozen suite. See evidence/phase-2.md for local
test evidence and remaining environment limitations.

CI workflow implemented and local tests pass; remote CI for the submitted
game version: pending. Independent review: pending.
Human playtest: pending. Recording: pending.

## Limitations / student authorship

This protocol was drafted by the implementation assistant. It is not the
student's final reflection. The student must write their own limitations
paragraph after examining actual results: what the sample supports, simulation
and source-fidelity limitations, memory findings, failures, and what the human
playtest changed. No live evaluation evidence exists yet.
