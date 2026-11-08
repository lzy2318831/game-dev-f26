# Agent team and development record

**Student:** lzy2318831, Executive Producer and Creative Director.
**Student review: PENDING.** This account was prepared with coding-assistant
help from saved project evidence. I need to review the wording and add my actual
session references before submitting; pending items are not completed evidence.

## My decisions

I changed direction from a six-ball prototype and historical reconstruction to
an original Pool + Pinball game. I wanted one visually coherent table with more
active collision chains, while keeping a readable billiards corridor. I kept
six alternating shots per player to bound the game and added limited refill
after my own testing suggested the table became empty late in a match.

I kept Geometric as the official baseline and Smart as a separate simulator
opponent. I approved a bounded real-model evaluation and preserved its initial
HTTP 429 failure. Later prompt-v2 and live-demo work remain separate from that
official result. The model's weak play is a limitation to report, not a reason
to replace its decisions with a stronger scripted policy.

## Who did what, with evidence

| Role | Actual workflow and access | Inspectable evidence |
| --- | --- | --- |
| Implementation assistant | Worked within my submission/workflow boundary; built rules, physics, UI, player adapter, tests and traces under my direction. Models in the game received public JSON, not development tools. | [AGENTS.md](AGENTS.md), [configuration](agent-config.json), [source map](rule-source-map.md), [implementation evidence](evidence/llm-integration/REPORT.md) |
| Reusable skill | `competitive-rule-change` was invoked during rule work: specification/map, failing tests, smallest engine change, boundary checks and a fresh reviewer. | [SKILL.md](skills/competitive-rule-change/SKILL.md), [Kinetic report](evidence/kinetic-1/REPORT.md), [replenishment report](evidence/replenish-1/REPORT.md) |
| Independent reviewers | Separate read-only contexts inspected code and tests, reported defects and rechecked fixes. They did not author their reviewed changes or approve student gates. | [LLM review](evidence/llm-integration/INDEPENDENT-REVIEW.md), [replay review](evidence/final-submission-01/INDEPENDENT-REVIEW.md), [live-mode review](evidence/live-browser-preparation-01/REPORT.md), [navigation review](evidence/navigation-fix-01/REPORT.md) |

The review findings were concrete. LLM review caught lost usage metadata and a
zero-limit fallback; replay review caught a timer that Play/Resume could cancel;
live review caught cancellation races; navigation review caught a delayed result
screen covering the menu. The implementation was corrected and tested rather
than treating review as a sign-off formality. Reports record the actual checks.

## Evidence that is still missing

- **Implementation session/task URL:** PENDING genuine saved reference.
- **Skill session 1 URL or CLI log:** PENDING genuine saved reference.
- **Skill session 2 URL or CLI log:** PENDING a distinct actual session/reference.
- **Student's final interpretation and review of this log:** PENDING.

The skill file and invocation reports exist, but I have not yet attached proof
of two independent skill sessions. Multiple turns or multiple reviewer contexts
in this conversation do not establish that requirement. A prepared second-session
prompt is not evidence that the session happened. The review artifacts above
support independent review; they do not make up the missing skill-session links.

## Human feedback and limitations

My own reported playtesting led to refill and navigation requests. It is not the
required session where another person plays while I watch without helping.
[PLAYTEST.md](PLAYTEST.md) still contains a worksheet rather than observations.
I must add anonymous notes about what that person did, where they guessed, and
what I changed or would change. If a session was genuinely impossible, I must
give the actual reason and what it would have checked, as the brief permits.

I also need the 3–5 minute video, a current remote CI link, confirmation of the
Week 3 scope post, and the approved PR/CourseWorks hand-in. No assistant review
or generated document approves those gates on my behalf. No paid calls were
made while preparing these final documents.
