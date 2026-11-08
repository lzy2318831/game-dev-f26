# Independent review handoff — not yet reviewed

Read in a fresh context that did not author this implementation; read-only
tools and findings only, no instruction to approve or merge. Existing reviewer
instructions: ../agents/rules-reviewer.md. This handoff is not review evidence.

Rules F1–F9 in ../RULES.md were specified before Fusion engine implementation.
All are intentional original design, with source-map/test locators in the
primary rule-source-map.md. No historical code/assets were imported.

Acceptance fixtures: vertical cue/object -> top-middle pot for 100, switches
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
