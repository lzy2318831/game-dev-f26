# Delivery plan and rubric acceptance checklist

Functional competition and evidence take priority over visual complexity.
Deadline: November 7, 2026, 11:59 p.m.; do not backdate missed checkpoints.

## Phases

1. Specification (complete): six-ball competitive scope, source/reuse record,
   complete rule specification, five-operation contract, frozen evaluation,
   local agent instructions and reusable skill. No claim of working gameplay.
2. Engine and offline players (implemented): source-map row then failing tests, physics,
   scoring/turns/limits, interface, geometric baseline, trace/replay runner.
   Record a real discovered defect and its reproducer for regression CI.
3. Playable view (implemented) and live adapter (boundary prepared; provider pending): minimal table/controls/status/restart;
   Human vs Human, Human vs Model, Model vs Baseline. Explicit provider/model
   selection, schema validation, counted failures, enforced timeouts. Add exact
   working commands/manifests and deterministic CI. No model traffic in CI.
4. Evidence: fresh independent read-only review and fixes; actual unassisted
   human playtest; frozen live comparison and memory test; clean-checkout run;
   student reflection and team log; three-to-five-minute recording and PR.

Once the base engine works, complete evidence before adding polish. Drop the
optional alternative opponent first. Do not drop the credible baseline,
required live trials, review, reusable-skill evidence, or recording to add balls.

## Deterministic checks

Project tests run from this folder with
`python -m unittest discover -s tests -v` once tests exist. The permitted
workflow must use this folder as its working directory, select only project
paths plus itself, request read-only repository permission, and use no secrets.
Pin project dependencies locally. Include these five rubric check kinds:

1. Invariants: stable IDs, score accounting including scratch removals, no
   invalid overlaps after separation, finite/bounded positions, no resurrection.
2. Legal/illegal actions: active seat, malformed schema, angle/power boundaries,
   wrong actor, snapshot mutation isolation, player-context whitelist.
3. Terminal outcome: repeatable completed match, correct winner/draw, final-shot
   scoring before comparison, table-clear precedence, terminal immutability.
4. Observed regression: record actual failure, minimal reproducer, failing test
   output, fix and passing output. A hypothetical defect is not evidence.
5. Episode limits: attempts, simulation ticks, model calls including errors,
   per-call timeout and match deadline using fake clocks/providers without sleep.

Additional checks: equal-mass collision examples, rail rebound, friction stop,
corner/side pocket capture, scratch respot, multi-pot scoring, and alternation
after miss/pot/scratch. Mocked provider tests validate the application only.
Also run repository-required root tests and offline headless diagnostics;
they supplement rather than replace project CI.

## Rubric traceability

| Check | Acceptance artifact / condition |
| --- | --- |
| 1a | rule-source-map.md covers all rules with code/manual/observed/assumed/design locators; tests and implementation locators added during development. |
| 1b | README scope matches actual build; RULES explains every historical adaptation. |
| 1c | SOURCES credits originals and verifies terms for anything copied; unresolved material excluded. |
| 2a | Human can play start to ending and restart without a crash. |
| 2b | Live model independently submits actions; trace shows model choices and labels failures/fallbacks (none planned). |
| 2c | Per-role context and legal-actions tests; fully observed information policy explained. |
| 3a | Fresh checkout executes documented setup/play/evaluation commands and both players. |
| 3b | Runner authority plus attempt/call/timeout caps enforced with logged terminal reasons. |
| 3c | Green submitted-version CI with all five check kinds listed above. |
| 3d | AGENTS.md plus actual implementation session; named skill used in two sessions; independent read-only review findings/session link. |
| 4a | RULES and evaluation explain each open choice and the alternative considered. |
| 4b | Geometric baseline is credible; three scenario families test differing decisions; results interpreted either way. |
| 5a | Dated pre-tuning declaration, held-out layouts, repeated live trials, seat reversal, all metrics/cost/failures in EVALUATION. |
| 5b | Student-written AGENT-TEAM and limitations name decisions and use actual human playtest observations or explain omission. |
| 5c | Accessible three-to-five-minute recording shows autonomous model play and states limits; linked from README and PR. |

## Dependencies requiring participation

- Student: choose explicit provider/model and privately configure credentials;
  approve a monetary cap before live evaluation. No live calls during review.
- Independent reviewer: separate read-only context that did not write the code;
  report evidence/tests/boundary findings, never approve or merge.
- Another human: play while student watches without helping; anonymous notes.
- Student: own-voice log, decisions, interpretation, limitations; scope-thread
  update; recording/access check; PR and CourseWorks submission. Staff merge.
- Instructor: uncertain publication rights or reduced evaluation equivalent if
  access/budget prevents the required suite. No deployment needed.

## Submission boundary

Keep source, dependency manifests, tests, agent artifacts, and small evidence
inside `midterms/lzy2318831/`. The only other allowed change is
`.github/workflows/midterm-lzy2318831.yml`. Stage these paths explicitly.
Preserve MIDTERM_REQUIREMENTS.txt. Do not alter shared starter code, root docs,
or the historical archive. No secrets, personal playtester data, installed
dependencies, caches, or large generated files in the PR.
