---
name: competitive-rule-change
description: Change competitive billiards rules with source evidence, failing tests, player-boundary checks, and an independent-review handoff.
---

# Competitive rule change

Adapted from the course rule-change procedure; all paths below are relative
to midterms/lzy2318831/. Invoke this skill by name and record the real session.

1. Read RULES.md and quote the affected row in rule-source-map.md. Add missing
   design rules with a specification anchor and rationale. Preserve historical
   evidence labels and locators; never promote an inference without evidence.
2. Write the acceptance trace: actor, initial layout/scores, action, expected
   balls/scores/next turn/outcome. Include an adjacent invalid-action case.
3. Write and run a deterministic test before engine changes. Record its actual
   failure and cause. Specification-only work has no executed test evidence;
   explicitly mark implementation pending instead of claiming a red/green run.
4. Implement the smallest change in the project engine/interface. Models propose;
   engine validates and commits. Verify wrong-seat and post-terminal behavior.
5. Check observation copies, legal vocabulary, private-state exclusion, and
   attempt/call/time limits. Check scratch and final-shot scoring precedence.
6. Run project tests and update map rows with engine/test locators. Record any
   genuine observed defect with its reproducer. Do not invent a regression.
7. Produce a handoff listing rule/evidence, red/green tests, boundary effects,
   assumptions and open questions. Give it to a fresh read-only reviewer who
   did not implement the change. Do not mark your own work reviewed.
8. Record invocation session/date, recommendations, evidence path and the
   student's decision. At least two actual sessions must invoke this skill;
   two calls in one session do not satisfy that requirement.
