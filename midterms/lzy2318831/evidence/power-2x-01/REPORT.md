# Doubled candidate-power experiment

Decision: **keep the stabilized Live LLM runtime unchanged; do not add a 2x
enable switch.** More scoring is possible in these simulations, but the scratch
regression violates the safety criterion declared before running them.

## Preservation and scope

Before experimentation, saved [1,033 file hashes](preserved-before.json) and
byte-for-byte snapshots of the seven geometry runtime/launcher files in
`baseline/`. Existing code, tests, documents, historical evidence and the staged
submission remain unchanged. Only a separate offline analysis module, its tests
and this new evidence directory are added. Nothing is committed or pushed.

The actual `competitive-rule-change` skill was explicitly invoked and read in
session `01a1b6ef-6f18-72c2-9249-e06f0ee80045`. Applicable existing map text:
"`fusion/geometry_candidates.py` derives bounded options from public data";
the experiment concerns proposals under the existing F2/F3/F8 contract, not a
rule change. No runtime implementation is enabled. The original LLM, prompt-v2,
Geometric/Smart decisions, engine, scoring and frozen artifacts are untouched.

## Method

[Predeclared plan](PLAN.md): compare every current candidate on 34 genuine saved
prompt-v2 observations plus four genuine geometry-assisted observations from the
run containing the known simulation-limit failure. There are 38 observations
and 77 paired candidate trajectories. The proposed power is exactly
`min(100, original_power * 2)`; angle and intended target stay fixed. No LLM is
called to select these experiment trajectories. Live selection remains genuine
and unchanged. The analysis module is not imported by the live runtime.

Each arm uses the unchanged deterministic physics simulator and its fixed
9,600-tick limit. Pots, scratch, points and settlement are actual simulated
outcomes. The engine does not log individual ball-ball impacts: contact metrics
are explicitly sampled cue/object distance <=22.1 and intended-target movement,
not reconstructed collision logs. All original observations remain unchanged.

Before seeing results, reject enabling 2x if it introduces a simulation-limit
failure from a settled original trajectory or raises scratch rate by at least
five percentage points. Saved states are correlated development examples, not a
held-out sample or a match-performance evaluation.

## Results

| Metric, 77 paired trajectories | Original | Doubled |
| --- | ---: | ---: |
| Intended-target contact-radius sample / movement | 37 | 37 |
| Scratched shots | 1 (1.30%) | 14 (18.18%) |
| Simulation-limit failures | 0 | 0 |
| Physically potted object balls, including scratched shots | 2 | 58 |
| Object balls potted on scratch-free shots | 1 | 3 |
| Scratch-free shots with any pot | 1 | 2 |
| Total retained simulated points | 130 | 860 |

There are 14 newly scratched trajectories and one avoided scratch. Most of the
extra physical pots occur on scratches and therefore do not earn retained shot
points. Higher aggregate points here are a real tradeoff, not proof of better
LLM play or more wins. Intended contact was already reached in the measured
targeted routes; doubling did not improve this proxy.

Repeated openings account for part of the raw rate. After exact deduplication
of public balls/bumpers/devices plus action and target, there are 70 unique
physics/candidate pairs: scratches still increase from 1/70 to 7/70 (+8.57
percentage points), exceeding the same rejection threshold. See
[deduplicated totals](deduplicated-summary.json).

Concrete regression: the opening contact at angle 0, power 23 is scratch-free;
power 46 pots six objects but scratches, voiding the points. Five doubled escape
proposals also scratch, whereas none of the original escape proposals do.
Their original clear-stopping-segment risk notes cannot safely be assumed to
apply after extending travel by doubling power.

At the previously failing position, the stabilized target-5 contact is
266/power 1: settles in 354 ticks, zero events, no scratch, no pots. Doubling to
power 2 settles in 4,671 ticks with 184 events, two object pots and 355 retained
points, no scratch. This particular doubled shot does not hit the simulation
cap, but does trigger a much longer device cascade. It does not establish a
general safe multiplier. The historical power-4 failure remains unchanged.

[Raw paired simulations](simulation/pairs.jsonl), [summary](simulation/summary.json).

## Use and limitations

Live play continues at its existing 1x recommendations with its normal launcher.
There is no experimental runtime multiplier flag to enable or disable: the
unsafe blanket change was deliberately not implemented. To repeat the isolated
offline 1x-versus-2x comparison from the project directory, choose a new output
directory (existing evidence is never overwritten):

```powershell
python -B -m fusion.geometry_power_experiment --output evidence/power-2x-repeat-02
```

This makes no API calls and does not enable doubled power in live play. Power
percentage is not physical speed or energy: launch speed is `100+7*power`, and
powered-device interactions further prevent a linear outcome prediction.

## Review and validation

Independent read-only reviewer `/root/geometry_review` verified preservation of
all 1,033 original hashes, exact capped doubling, every candidate included on
the 38 saved observations, source hashes, aggregate totals and representative
re-simulations. The reviewer agreed that the predeclared scratch threshold is
exceeded. The reviewer found an offline-reporting test failure for an arm with
no settled shots (missing zero `settled_pots` key); initializing explicit zero
totals fixes it. This did not affect the all-settled 77-pair results or live code.
Five focused experiment tests pass after that fix. No student gate was approved.

Final full-suite/browser/preservation results are recorded alongside this report
in the validation files; none are paid model evaluations.


Final validation: **199 project Python tests passed** (return code 0, 291.512s),
all five JavaScript controller checks passed, all 24 historical traces replayed,
all 18 frozen artifacts passed and all 1,033 preservation hashes remain equal.
The first full run recorded one reporting-tool error before its correction;
[the final run](python-tests-final.txt) passes and both logs are retained.
Actual Chrome verified [two full 12-shot matches](browser-two-matches/summary.json)
on the same server plus budget-exhaustion/menu navigation, and separately
[simulation-limit failure, hung leave, menu and fresh match](browser-failure-recovery/summary.json).
Both Chrome runs have zero runtime errors and use synthetic model responses.
The current runtime and all previously staged submission bytes remain unchanged.
New experiment files/evidence are left unstaged. See [validation](VALIDATION.json)
and [independent review](INDEPENDENT-REVIEW.md).
