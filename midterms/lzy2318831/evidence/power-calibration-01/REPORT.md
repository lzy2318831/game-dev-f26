# Focused adaptive-power calibration

Conclusion: the newest genuine trace verifies2x works. Very low base power,
not a display or action-conversion error, explains most soft shots. A separate
optional **Adaptive energy - experimental** setting raises targeted-shot floors.
Existing1x/2x remain rollback choices; the initial default is still2x.

## Genuine trace audit

Newest saved genuine run: `20261107T225959Z-1c46d6d44202`, complete12shots,
trace multiplier2, six live model calls with HTTP200. For every model shot,
the request candidate, selected metadata and executed action agree:

| LLM shot | Route | Base | Offered2x | Executed |
| --- | --- | ---: | ---: | ---: |
| 1 | contact | 23 | 46 | 46 |
| 2 | contact | 1 | 2 | 2 |
| 3 | escape | 5 | 10 | 10 |
| 4 | fallback-escape | 1 | 2 | 2 |
| 5 | contact | 1 | 2 | 2 |
| 6 | contact | 1 | 2 | 2 |

[Audit](genuine-power-audit.json) also records the preceding genuine222659run.
It lacks original-power/multiplier metadata: its offered/executed powers are
verified, but no multiplier is invented for it. Neither run was made by this
repair. Saved requests provide the actual public observations; nothing missing
was reconstructed or substituted.

## Why the recommendations remain low

The base generator budgets only15units of object runout after contact, uses
speed=`100+7*power`, friction70 and normal transfer .99; power1 already launches
at107units/sec and has an ideal free stopping distance of81.8units. Doubling
the slider from1to2 changes speed only107to114, not to214. This reaches nearby
objects but often transfers little visible movement. Escape fallback uses legal
minimum1, becoming2under2x. Those choices are genuinely conservative.

At power25 speed275 gives an ideal free coast540.2units, power35 gives850.2,
and power50 gives1446.4. These engine-derived scales motivate testing stronger
floors, but rails, impacts, portals, powered devices and scratches make actual
outcomes nonlinear. We do not treat those free-space distances as guaranteed
routes or safe stopping distances.

## Offline comparison before runtime enablement

[Predeclared plan](PLAN.md), [raw trajectories](simulation/trajectories.jsonl),
[summary](simulation/summary.json). Corpus:34genuine prompt-v2 observations,
four from the known historical failure run, and12from the two newest genuine
geometry runs. Fifty saved observations yield96distinct physics/action/target/
route candidate cases after exact deduplication. Every current candidate is
tested, not selected by a model. The unchanged simulator runs at most9600ticks.

Three hypotheses: close travel<=150, medium<=350, long>350. Floors25/35/50,
30/40/55 and35/50/65. Bank floors add5 for the cushion route; the existing base
reach/energy estimates already account for normal transfer/friction/cushion
loss. Power=max(current2x,floor), capped100. Escape/fallback/device candidates
retain2x because a stronger unverified route is not a meaningful target shot.
This is an empirical energy floor on existing geometry, not a new aiming policy.

| Mode | Scratch-free object pots | Retained points | Scratches | Limits | Powered events |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1x | 1 | 155 | 2 | 0 | 32 |
| 2x | 11 | 2375 | 9 | 0 | 865 |
| Floors25/35/50 | 42 | 8270 | 15 | 0 | 1891 |
| Floors30/40/55 | 37 | 7220 | 18 | 0 | 1592 |
| Floors35/50/65 | 49 | 8885 | 15 | 0 | 2282 |

All modes show48intended-target contact-radius samples and target movements.
Relative to2x, selected floors25/35/50 produce about2.25times the object travel
proxy (474677versus211420 summed units) and about2.01times cue travel. Descriptive
cascades with>=50powered events rise7to15cases. Travel sums include portal
relocations and collision correction; they are not pure physical path length.
Individual ball-ball impacts are not logged by the engine, so contact proximity
and movement are identified as proxies. Pots/points are authoritative simulated
results only after settlement; no unfinished trajectory is credited as a result.

The lowest floor profile supplies substantially more measured movement and
retained scoring while using lower floors than the other hypotheses. Scratch
increase is visible (+6/96 versus2x) and is an accepted student tradeoff, not
hidden as improvement. All96cases settled, so none repeatedly hits the cap in
this corpus. This does not guarantee safety in unseen states; we did not add a
runtime simulator/filter or raise the engine cap. No genuine model/human test
establishes subjective engagement or stronger match performance.

## Mandatory266degree regression

[Actual comparison](mandatory-position.json), same public state and angle:

| Power | Settles | Ticks | Pots | Retained/provisional points |
| --- | --- | ---: | ---: | ---: |
| 1 (1x) | yes | 354 | 0 | 0 |
| 2 (2x) | yes | 4671 | 2 | 355 |
| 4 (historical failure) | no | 9600 | 4 provisional | 655 provisional, not credited |
| 25 (chosen adaptive) | yes | 844 | 1 | 100 |
| 30 | yes | 2635 | 2 | 355 |
| 35 | yes | 1029 | 0 | 0 |

The historical failure remains reproducible. More power is neither universally
safer nor monotonically better; powered-device trajectories differ sharply.

## Runtime scope and UI

Choose Candidate power → **Adaptive energy - experimental** before confirming
a fresh Geometry-Assisted Live LLM match. It changes only recommended power,
preserving IDs/angle/target/route and genuine model ID selection. It records
power_mode=`adaptive`, power_multiplier=`null`, original power, adaptive floor,
formula and adaptive prompt hash. It is not mislabeled as a single multiplier.

Contact/pot floor25at<=150,35at<=350,50beyond; bank+5; cap100; never below2x.
Repositioning/unknown-device routes may remain soft. The1x/2x request payloads
are byte-for-byte equal to the preserved pre-calibration implementation in the
rollback regression. Adaptive alone receives an additional prompt explanation.
No original LLM/prompt-v2, physics, scoring, Smart or Geometric changes.

The existing setting endpoint accepts the exact adaptive mode body under its
same waiting-state/current-token/same-origin/session-lock guards. Active changes
are rejected; no setting dispatches a model call or resets the server cap. Fresh
matches preserve the selected mode and cumulative accounting. Back, cancellation,
settlement, timeouts, no retries and fresh consent remain intact. To roll back,
return to Main Menu, reopen Live LLM and select1x or2x before fresh consent. No
server restart is needed for switching; an already-running old process needs
the usual one-time restart to load new source.

Actual Chrome [adaptive then1x](browser-adaptive/summary.json): two consecutive
complete12-shot matches through one server, one Back, declined confirmation sends
nothing, mode/selected-ID/formula checked for each model action, budget6then12,
and selecting2x at exhausted allowance does not enable start. This is synthetic
model inference, not a live evaluation. Failure recovery and full validation are
recorded in adjacent evidence files.

## Preservation, tests and independent review

All1195existing files were hashed before changes; baseline copies preserve the
current runtime. Historical evidence and18frozen artifacts remain unchanged.
The actual `competitive-rule-change` skill was explicitly invoked in actual
session `01a1b6ef-6f18-72c2-9249-e06f0ee80045` under the existing F2/F3/F8 proposal
contract. [Executed red tests](red-adaptive.txt): unsupported adaptive keyword
and missing floor module; legacy request parity already passed. Green tests add
distance/route/cap/identity, all50-state profile parity, known-position settlement
and HTTP lifecycle/rollback checks.

Independent read-only reviewer `/root/geometry_review` recomputed96case totals,
matched runtime powers against every recorded chosen-profile power, verified
the genuine six-shot2x audit and reproduced known-position2x/adaptive outputs.
It found a new HTTP test readiness race: bounded leave may precede worker replay/
audit completion. The test now explicitly joins/checks settlement before/new;
the production guard was not weakened. The reviewer made no edits or paid calls
and approved no student gate. Final checks are recorded separately.


Reproduce only the offline experiment from the project directory with a new
output path: `python -B -m fusion.geometry_power_calibration --output evidence/calibration-repeat-02`.
No output is overwritten and no model calls are made.

The initial full212-test run caught the new test settlement race described
above. After that correction, another full212-test run encountered Windows
WinError10053 during the existing stale-token rejection test; the local
connection was aborted before an HTTP response could be read. The complete
seven-test module passed on targeted rerun without a production change.
Both original logs are retained; the additional full outside-sandbox rerun is
recorded separately rather than relabeling either failed run as a pass.


The outside-sandbox full run reproduced the same Windows socket abort in the
invalid-token test. Its assertion is now transport-tolerant only for that
rejected request: HTTPError or ConnectionAbortedError, followed by explicit
checks that the server is reachable, multiplier remains2 and model calls remain0.
No production authentication/HTTP code changed for this test adjustment. The
independent reviewer approved this semantic-refusal assertion while noting that
an abort does not prove delivery of HTTP403. The subsequent complete suite is
recorded in `python-tests-complete.txt`, without overwriting earlier failures.


Final result: all212tests passed across all30isolated test modules, independently
checked against complete project-root discovery; every module returncode0.
The initial module runner miscounted expected tests because its own import path
omitted the project root, although all child commands already passed212tests.
Its raw report is retained; the corrected runner path and
[complete coverage verification](python-module-verification.json) establish
212expected/212executed, without relabeling any failed serial run.
All six JavaScript checks,24historical replay verifications and18frozen checks
pass. Actual Chrome also verified
[adaptive HTTP failure, Back and a fresh1xmatch](browser-adaptive-http/summary.json).
No historical evidence or unexpected baseline paths changed. Agent configuration
now references the verified optional setting/evidence; historical approvals and
model settings remain unchanged. [Validation](VALIDATION.json) records the final
results. Scoped files and necessary genuine-source traces are staged; no paid
calls, commit, push, PR or CourseWorks submission was made.
