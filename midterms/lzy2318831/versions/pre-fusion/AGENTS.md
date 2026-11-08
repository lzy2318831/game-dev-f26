# Six-ball Pool implementation instructions

The student directs scope and owns decisions. Read README.md, RULES.md,
rule-source-map.md, EVALUATION.md, and PLAN.md before changing behavior.
Only edit this project folder and the permitted login-specific workflow.
Preserve the assignment file and user work; no merges, gate approvals, or
messages/submissions on the student's behalf.

Invoke `competitive-rule-change` from skills/competitive-rule-change/SKILL.md
for any rule/interface change. Map first, failing test second, engine third,
then boundary checks and a summary for a different read-only reviewer. Use
`design` for chosen adaptations; do not call them verified historical rules.
Do not copy historical code/assets without verified terms. The source archive
has no established reuse grant.

The engine owns state; policies receive detached serialized observations and
an action vocabulary. The model selects actions. No engine object, repository,
shell, answer key, or credentials in player context. Never silently substitute
a baseline or fixture for model play. Failed calls count toward limits.

Run project deterministic tests from this folder once implemented. Also follow
the root test/diagnostic requirements. Keep routine tests offline. Live calls
require an explicit provider/model, private credentials and agreed budget.
Do not tune on held-out cases. Report real failures; do not manufacture a
regression, playtest, review, skill invocation, or evaluation result.

Keep assistant-authored planning separate from the student's final own-voice
log and reflection. A separate fresh read-only review session must inspect
implementation before submission; the author cannot review their own change.
