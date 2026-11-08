# Independent read-only review task

Run in a fresh session that did not implement the reviewed change. This file
is instructions, not evidence that review occurred. Read-only tools only;
no code edits, provider calls, approval instructions, gate decisions or merges.

Read the handoff, diff, RULES.md, rule-source-map.md, engine/interface, runner,
player adapter/context builder, tests, EVALUATION.md and source/reuse record.
Check evidence labels and locators, engine/test/spec agreement, real failing-
test evidence, neighboring illegal cases, score/turn/scratch/terminal precedence,
all bounded limits, serialized player boundary, fair baseline access, and
absence of unlicensed copied material. Verify all five deterministic CI kinds
including an actually observed regression. Identify deviations from the suite.

Return findings most serious first:
`[blocking | should fix | note] file:line: issue and evidence`.
If none, say `No findings` and list the files and checks examined. Do not
approve. The student decides how findings are handled. Save actual findings
as review.md or PR comments and link the separate session in AGENT-TEAM.md.
