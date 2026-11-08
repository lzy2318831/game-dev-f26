# Independent review handoff — not yet reviewed

Current scope also includes P1–P5 in POLISH-RULES.md and the Aurum Circuit
expansion (fusion-1.1.0-aurum). Review devices.py/geometry.py and
web/aurum.js, plus test_fusion_polish.py. Pay attention to capsule normals,
crossing predicates, shot-local score/energy caps, multiplier event ordering,
and observation geometry. Current evidence is in ../evidence/polish-1/REPORT.md;
the prior evidence below remains archived-version evidence. No independent
review has been performed by the implementation author.

Read in a fresh context that did not author this implementation; read-only
tools and findings only, no instruction to approve or merge. Existing reviewer
instructions: ../agents/rules-reviewer.md. This handoff is not review evidence.

Rules F1–F9 in ../RULES.md were specified before Fusion engine implementation.
All are intentional original design, with source-map/test locators in the
primary rule-source-map.md. No historical code/assets were imported.

Acceptance fixtures: vertical cue/object -> bottom-middle pot for 100, switches
seat and terminates if last object; cue at top-middle opening -> scratch,
zero score, clear respot and switch. Invalid active action changes quota and
invalid counter, not balls/scores; wrong actor changes nothing. Bumper reentry
never rescores that bumper in one shot and boosts at most twice per ball/pair.

Review engine.py, baseline.py, player.py, runner.py, server.py, web/, tests/
test_fusion*.py, evaluation.json, rules and CI. Check scoring event order,
scratch/clearance precedence, rail/ball/bumper numerical behavior, end quotas,
respot spacing, baseline fairness, timeout cleanup and error attribution.
Check that the browser only plays engine snapshots and cannot steer in flight.
Verify the real restart-race regression in browser_check.py and viewport checks.
Review screenshots as application QA, not evidence of human experience.

Actual red/green summary is in ../evidence/FUSION-SLICE.md. Earlier engines and
tests are byte-preserved per versions/pre-fusion/preserved-hashes.json; their
results must not be substituted for Fusion evaluation. Live provider/evaluation,
student own-voice authorship, independent findings, human playtest, recording
and distinct-session skill evidence are still pending.

Current Aurum evidence: ../evidence/polish-1/REPORT.md. Top-middle Orbit
assisted fixture now expects 225; see test_full_spinner_assisted_pot. Fresh
independent read-only review requested after implementation on 2026-11-06.

Grand Circuit M1?M5 supersedes older counts and limits. Actual fresh review
and regression dispositions: ../evidence/maximal-1/REPORT.md and
INDEPENDENT-REVIEW.md in that directory. Eight focused tests independently
passed; student gate remains pending.

Current review scope: K1-K5 in KINETIC-RULES.md; engine/devices variable radii,
directed impulses, finite uses, Skyway occupancy, transfer chord exclusion,
ledger cap315 and scratch precedence. Baseline public radius/impulse formulas;
Canvas transfer snap/trail, variable-size rendering and zero-point labels.
Actual independent re-review: ../evidence/kinetic-1/INDEPENDENT-REVIEW.md.
All ten new mechanism tests passed by fresh /root/kinetic_review; no blocking
findings after corrections. Gate/student/human/live evidence remains pending.

Final15 review scope: FINAL-RULES.md; rack initialization/16palette, Smart
public-snapshot authoritative simulations/candidate budgets, Geometric SHA256,
unchanged devices/rules, broadphase exactness, serverthree modes and thinking
HUD, five operations, comparison metric rawpotsvscreditedpots and replay.
Fresh reviewer result: ../evidence/final-15/INDEPENDENT-REVIEW.md. No gate approval.

Current R1-R4 review: pure atomicplacement, no moving/final/invalid refill,
score/scratch before replenish, clearance after, counter/IDs/public copies,
shared trace hash and Smart terminal guard. New tests10pass; reviewer checked
100additional seeded clear states. See evidence/replenish-1/INDEPENDENT-REVIEW.md.
Smart physical preview omits post-refill position, search/budget unchanged.
No gate approval. Browser batch notification and offline replay evidence
recorded separately in evidence/replenish-1/REPORT.md.

LLM review scope: newllm.py/llm_eval.py and runner extensions only. Freeze18
passes. Check publicdataonly,paymentgates,budget/audit,metadataonfailure/deadline,
strictJSONvalidation,workertermination,unknowncosts,baselinecontrols,fixturelabel,
replay andreport fields. Fresh reviewer findings/fixes retained in
../evidence/llm-integration/INDEPENDENT-REVIEW.md. Real provider behavior remains
unverified until approval. This is no student/coursegate approval.
