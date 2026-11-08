# Adaptive distance v2 — offline verification

Physics remains fusion-1.6.0-balanced. Profile identity: adaptive-distance-v2.
No paid requests, new official evaluation, or historical evidence rewrites.

## Intended power

For contact, pot and bank-contact, d=max(0, candidate travel) is cue travel to
first contact (including bank segments), not subsequent object-ball travel:

```
d <= 150:       p = 30 + d / 15
150 < d <=350:  p = 40 + (d - 150) / 5
d > 350:       p = min(100, 80 + (d - 350) / 32.5)
power = min(100, floor(p + 0.5))
```

The long band saturates at1000units (table width). There is no base-power floor
or bank bonus. Escape, fallback-escape and device routes keep their separate
min(100,2*original_power) treatment. A pot recommendation below the original
estimate explicitly warns that the outgoing route may undershoot. Candidate
IDs, angles, targets, route types and genuine LLM selection remain intact.

## Paired simulation

See simulation/summary.json, pairs.jsonl and source hashes. Both arms use current
v1.6 physics:30saved observations (6genuine,24synthetic) yield38distinct
candidate/state pairs. Previous Adaptive is loaded from the preserved baseline.

| Metric | Previous | Distance v2 |
| --- | ---: | ---: |
| Contact proxies |34|34|
| Physical object pots |19|18|
| Scratch-free pots |8|17|
| Retained points |1450|2935|
| Scratches |6|1|
| Long powered cascades (>=50events) |1|5|
| Powered events |460|721|
| Simulation limits |0|0|

The mandatory historical266° public position was explicitly transplanted onto
v1.6 devices, not reconstructed as a genuine v1.6 match. Previous25power settled
in844ticks with one pot/100points; v2 selected32power and settled2217ticks with
no pot/0points. Neither scratched or hit the limit. Object movement rose from
1875.9 to3910.05units. Movement includes portal relocation/collision correction;
contact is a sampled geometric proxy. Stronger power is not universally better.
No observed limit required investigation (limit-investigation.json is empty).
Future powered cascades and limits remain possible; recovery is preserved.
These correlated development cases do not establish LLM performance or win rate.

## Regression evidence

- red-tests.txt records the new tests failing before implementation.
- All222Python tests across32modules pass, including boundary/interpolation,
  caps, unchanged1x/2x payloads and mandatory266° safety regression.
- All7JavaScript suites pass (javascript.json).
- browser-profile/summary.json: actual headless Chrome, one server, Adaptive
  then1x, two complete12shot matches; genuine selection protocol exercised with
  synthetic model responses for every LLM turn, one Back button, cue contact,
  balanced table, original viewer, delayed settlement and nonresetting budget.
- browser-failure/summary.json: synthetic HTTP failure is incomplete, Back works,
  and a fresh1x match completes12shots on the same server. No paid calls.
- historical-replays.json verifies all24original traces under original v1.5.
- archive-freeze.txt:18current and18archived freeze checks;157archive hashes.

Before edits, preserved-before.json captured1774project files. Baseline helper,
agent, server and power UI are copied under baseline/. Previous evidence and
physics remain untouched. Independent geometry_review checked the targeted
formula, preserved fields and1x/2x parity; no implementation defect found.

## Selection and limits

With no match active, open Geometry-Assisted Live LLM and choose **Adaptive
energy - experimental** in Candidate power, then confirm fresh consent. Active
status identifies Adaptive energy v2. Choose1x or2x in that menu to roll back;
initial default remains2x. Restart an already-running old server once to load
the new code; never reset a spending cap merely to continue a paid session.
No runtime physics simulator/filter, engine changes, navigation changes or
budget changes were introduced. Video, remote CI and final submission remain
student tasks. This profile changes recommendations, not physics compatibility.
