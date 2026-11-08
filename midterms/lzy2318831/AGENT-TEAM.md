# Agent team and development record

**Student:** lzy2318831, Executive Producer and Creative Director.
**Student review: PENDING.** This account was prepared with coding-assistant
help from saved project evidence. I need to review the wording and supply the
remaining submission evidence before submitting; pending items are not
completed evidence.

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

The evidence-status fields in `agent-config.json` are an older snapshot: its
human-playtest pending flag predates my confirmed friend session. PLAYTEST.md
and the current checklist record completion. I left agent/configuration files
unchanged during this documentation-only review.

## Verified session references and remaining gap

My implementation session is `01a1b37c-aa97-7781-91f4-ec7693968a43`, started
2026-11-07T00:50:54.396Z. [The session audit](evidence/submission-readiness-01/SESSION-EVIDENCE.md)
links a sanitized CLI-log reference with exact source lines, timestamps and
hashes. It verifies actual Fusion creation and replenishment patches, skill
reads, and explicit `competitive-rule-change` invocations. No private full log
or account identifiers were copied into the submission.

- **Implementation session:** verified through that saved log reference.
- **Skill session 1:** verified in the same implementation session.
- **Skill session 2:** verified in the fresh read-only session recorded below.
- **My final interpretation and review of this log:** PENDING.

The available reviewer files identify separate child contexts, but their copies
of parent skill invocations are inherited history. Several rule-work turns in
one session do not satisfy two sessions. I will not relabel them as independent
uses. The existing read-only findings support independent review separately;
a prepared second-session prompt is not executed-session evidence. The new
session below supplies actual use after that earlier audit.

## Human feedback and limitations

My own reported playtesting led to refill and navigation requests. Separately,
I completed a real playtest with a friend. Their feedback concerned frustrating
scratches, balls difficult to recover near edges/obstacles, and smoother terrain
flow. [PLAYTEST.md](PLAYTEST.md) separates that feedback from my interpretation
and future improvements. I personally watched my friend play independently
without telling them how to aim, choose power or make moves. The issues were
identified during actual gameplay, completing the observed human playtest
requirement. I have kept the frozen game unchanged; no unreported actions,
hesitation, counts or session details have been invented.

I confirmed publishing the Week 3 scope update; the student-provided post is
preserved in [WEEK3-SCOPE-CHANGE.md](WEEK3-SCOPE-CHANGE.md), with no direct URL
supplied. I still need the 3–5 minute video, a current remote CI link, final
reflection review, and the approved PR/CourseWorks hand-in. No assistant review
or generated document approves those gates on my behalf. No paid calls were
made while preparing these final documents.

## Fresh independent review and actual second skill invocation — 2026-11-07

**Assistant-authored factual appendix; student interpretation remains pending.**
The reviewer in this new session did not implement the reviewed project. The
student requested read-only review, with this log update as the sole document
edit. No gameplay changes, paid requests, commits, pushes or gate approvals.

**Exact skill:** `competitive-rule-change`, read from
[skills/competitive-rule-change/SKILL.md](skills/competitive-rule-change/SKILL.md).
The assignment requires a reusable skill used in two sessions; it does not
prescribe this name. Project AGENTS.md prescribes this project's skill.
**New session ID:** `01a1b6ef-6f18-72c2-9249-e06f0ee80045`, obtained from
`CODEX_SESSION_ID` and `CODEX_THREAD_ID` and corroborated by session metadata.
This differs from implementation session `01a1b37c-aa97-7781-91f4-ec7693968a43`.

Actual invocation evidence, inspected in the current local CLI transcript:

- Local locator: `.codex/sessions/2026/11/07/rollout-2026-11-07T11-55-07-01a1b6ef-6f18-72c2-9249-e06f0ee80045.jsonl`
  under the user's home directory. Raw logs remain outside the submission.
- Line 1: session metadata identifies the new session above; payload start
  timestamp `2026-11-07T16:55:07.497Z`.
- Line 26, `2026-11-07T16:56:49.841Z`: actual `functions.exec` call
  `call_736e2cfa94ad415db8f2d55b9ac708ef` reads the skill and project documents.
  Its successful output has chunk ID `aea915` and includes all eight skill steps.
- Line 34, `2026-11-07T16:56:56.938Z`: this session's assistant explicitly says
  "which I now explicitly invoke" about `competitive-rule-change` and states
  that its evidence/boundary checks will be applied to the frozen project.
- Skill file SHA-256 at review:
  `118bf44402865cd9c5d953aa3c00fe5463d28a941bbea20d7f594f4402c75630`.

This was a named invocation followed by actual review, not inherited history
or a prepared prompt. Skill steps 1, 5, 6, 7 and 8 guided specification/source
inspection, boundary checks, existing tests and findings. Steps 2–4's new
acceptance/red-green/engine-edit sequence did not apply: no rule change was
requested. No new failing-test-first implementation or new regression is claimed.
This appendix is the fresh reviewer's findings, not self-approval by the builder.

### Reviewed scope and findings

Read MIDTERM_REQUIREMENTS.txt, AGENTS.md, the skill and reviewer instructions,
RULES.md, rule-source-map.md, SOURCES.md, README.md, EVALUATION.md,
SUBMISSION-CHECKLIST.md, PLAYTEST.md, agent-config.json, the review handoff,
engine five operations, player context, LLM adapter, runner, evaluation runner,
suite, freeze checker, saved-result analyzer, live entry point, portions of UI
code, and interface/LLM/replay/navigation tests. Inspected the scoped workflow
and previous session-evidence audit. This is code/evidence review, not a new
human playtest, browser visual inspection or fresh-clone/remote-CI certification.

- **Submission blocker:** README.md:19 has no actual 3–5 minute recording URL.
  Recorded replay code and a recording guide do not supply the video.
- **Submission blocker:** no green remote CI evidence for the submitted commit;
  the folder and scoped workflow are currently untracked, on branch
  `lzy2318831/midterm`. HEAD is `4a3b5b9`, a course merge, not a commit containing
  this project. A local pass cannot establish committed fresh-clone reproducibility.
  The course PR URL and CourseWorks hand-in remain unperformed in the checklist.
- **Should fix:** README.md:35 and test commands use `py`, unavailable in this
  review shell. Both attempted `py` checks failed before execution; `python`
  resolves to `C:/Users/lzy21/AppData/Local/Python/bin/python.exe` and runs.
  Document a working interpreter choice for the review environment.
- **Should fix:** stale status claims conflict with completed evidence:
  fusion/evaluation.json:250 says no live trials; rule-source-map.md:119 says no
  paid/live evidence; agent-config.json still marks human playtest/authorship
  and other statuses as older snapshots. README/EVALUATION/checklist also still
  say the second skill session is missing. This appendix supersedes that last
  claim; those documents were left unchanged. Preserve frozen declarations and
  historical evidence rather than rewriting them to look contemporaneous.
- **Student action:** review the assistant-assisted first-person log/reflection,
  confirm/post the Week 3 scope change and supply its actual discussion link.
  Existing PLAYTEST.md records the student's observed friend session; this
  reviewer did not observe it independently or invent missing session details.
- **Evaluation limits:** three situations, repeated deterministic boards, one
  failed trial and no live memory ablation remain explicit. The report explains
  observation-only memory for a fully observed game without proving memory
  cannot help. Cases later used for prompt-v2 are not untouched held-out tests
  for v2. No extra paid trials are recommended as part of this read-only review.

Boundary inspection found all five operations implemented, detached observations,
an inactive/terminal empty action schema, strict integer action validation,
wrong-seat/postterminal immutability and bounded invalid-action opportunities.
The runner holds state, counts failed model attempts, caps request/episode time,
and aborts explicitly without substituting a Geometric shot. The provider request
has no tools and contains serialized public context; credentials stay in the
transport. This establishes the remote model's data boundary, not an OS sandbox
for arbitrary local Python policy code. Geometric uses public geometry; Smart's
simulation access is disclosed separately and is not LLM-performance evidence.
Scratch voids shot scoring before refill/clearance; final-opportunity refill is
excluded. Existing tests exercise these cases and actual historical regressions.

### Checks actually executed in this session

From `midterms/lzy2318831/`, with bytecode writes disabled:

- `python -B -m fusion.freeze`: PASS, all 18 frozen artifacts.
- `python -B -m fusion.final_analysis --verify`: exit 0; all 24 saved trial/control
  traces replayed. Recomputed 11 completed matches, 2 wins/9 losses, one provider
  failure, zero illegal LLM actions, mean scores 720.45 versus 1347.27; 66
  successful official calls, 203991 input/1482 output tokens, known continuation
  estimate $0.15966225. This reads saved evidence and makes no model requests.
- `python -B -m unittest discover -s tests -v`: PASS, 164 tests in 219.002s,
  exit 0 (completion chunk `6d3081`). Fixtures/mock transports test the adapter;
  they are not new live-model performance evidence.
- Post-review `python -B -m fusion.freeze`: PASS again, all 18 artifacts
  (chunk `91dfe6`). Only this log was intentionally edited.
- Node is not on this shell's PATH; standalone JavaScript controller commands
  were not run. The workflow installs Node 22; remote results are still pending.

Recommendations belong to this reviewer. The student requested this review and
log update, retaining the freeze; their response to these findings and final
submission decision remain pending. No assistant approves the course gate.

## Final preferred live demonstration — factual assistant record

The student requested Geometry-Assisted LLM v1 as the preferred final Live LLM
demonstration, retaining original/prompt-v2 implementations and all historical
results. The same continuing session explicitly invoked
`competitive-rule-change` again; this is not an additional distinct session.
The earlier independent second-session evidence above remains the actual record.

The implementation added the masked `run-geometry-live.ps1` launcher, preferred
menu labels and readable no-candidate/invalid-selection/timeout messages while
preserving frozen visuals and gameplay. A real-provider branch and the original
OpenAI HTTP adapter were tested with synthetic responses, not real API requests.
The LLM still selects candidate IDs itself. No candidate stops safely, and
Cancel/Back cannot authorize a fresh match or substitute another agent.

Independent reviewer `/root/geometry_review` read the final changes without
editing or making provider/Git calls. It identified missing timeout-message
aliases; those were corrected and tested. Its findings and the final unit,
controller, replay, freeze, preservation and staging checks are recorded in
[the final preparation report](evidence/final-geometry-01/REPORT.md).
The current configuration now records the confirmed friend playtest and both
skill sessions; the older configuration note above describes the earlier audit.

Real account/model access and geometry-assisted performance remain unmeasured
pending a separately authorized smoke. The student's video, remote CI link,
personal reflection review and final PR/CourseWorks hand-in remain pending.
Week3 publication is confirmed by the student, with no permalink or publication
timestamp supplied. No assistant approved a course gate, committed, pushed or
submitted on the student's behalf.

## Lifecycle bug repair — factual assistant record

The student reported four-shot termination and inability to start a second
geometry-assisted match. Saved genuine and mocked traces confirmed
no_reliable_candidate with four shots still available to each player; the
single-use backend phase then prevented a fresh match. This was not a change
to the six-shot rule. The student authorized an offline repair, regression
testing and scoped staging, with no paid call or commit/push/PR.

`competitive-rule-change` was invoked in this same continuing session, not
counted as another distinct skill session. Minimum-energy fallback choices now
remain subject to LLM ID selection. Fresh match preparation rotates its token
and resets episode-local state only; per-match6/$0.25 and cumulative
server12/$0.50 limits are distinct and spending survives cancellation/reload.

Independent reviewer `/root/geometry_review` checked budget/nonce/cancellation
and action-selection boundaries, ran the HTTP lifecycle tests and replayed
two saved actual-browser synthetic traces. It requested clearer fallback-risk
prompt wording, which was corrected. An isolated Chrome run then completed
two consecutive12-shot matches with six selections per seat and two menu
returns on one running server. This is mock engineering evidence, not a new
genuine performance result or human playtest. [Repair evidence](evidence/lifecycle-fix-01/REPORT.md)
records actual failures, tests, browser traces, preserved hashes and limitations.


Stabilization session `01a1b6ef-6f18-72c2-9249-e06f0ee80045` explicitly invoked
`competitive-rule-change` from [the actual skill](skills/competitive-rule-change/SKILL.md).
This records the current session, not an additional independent student session.
The skill was read and applied to red/green navigation/proposal regressions,
public-boundary checks and an independent read-only handoff to
`/root/geometry_review`. That reviewer reported no remaining blocking findings,
independently reproduced 266?/4 at 9,600 ticks and 266?/1 settling at 354 ticks,
and confirmed all 18 frozen artifacts. The reviewer did not edit files or approve
a student/course gate. See [stabilization report](evidence/stabilization-01/REPORT.md).

Follow-up in the same actual session `01a1b6ef-6f18-72c2-9249-e06f0ee80045`:
explicitly invoked `competitive-rule-change` for the student-authorized2x
candidate-power preference and1x fallback. This is not another independent
skill session. The previous offline experiment and its rejection recommendation
remain historical evidence; the student now explicitly accepts the scratch
tradeoff. New specification/red tests, capped-ID regression, actual Chrome
switch/recovery evidence and independent review are recorded in
[power-setting evidence](evidence/power-setting-01/REPORT.md).
Independent read-only reviewer `/root/geometry_review` found the capped-action
metadata alias and verified its correction, seven focused tests, the power UI
check,18frozen artifacts and both2x/1x browser trace replays. The reviewer made
no edits and approved no student gate. Original official LLM results remain unchanged.

Focused adaptive calibration in the same actual session
`01a1b6ef-6f18-72c2-9249-e06f0ee80045` explicitly invoked the actual
`competitive-rule-change` skill again; this is not another independent session.
Newest genuine power audit, offline profile comparison, executed red/green
tests and actual mock Chrome evidence are in
[calibration evidence](evidence/power-calibration-01/REPORT.md). Independent
read-only reviewer `/root/geometry_review` recomputed the96-case summary,
verified recorded adaptive powers and the genuine2x audit, and reproduced the
known-position2x/adaptive settlement. Its test readiness-race finding was fixed
by waiting for worker settlement in the test, without weakening the new-match
guard. No student gate or new real-model performance result is claimed.


Cue/restart checkpoint in session `01a1b6ef-6f18-72c2-9249-e06f0ee80045` explicitly
invoked `competitive-rule-change`. Preserved108original files/hashes before any
edits. Executed red cue/restart regressions and actual Chrome verification;
independent read-only reviewer `/root/geometry_review` found no remaining issues
in those two UI fixes and verified original archive integrity. Corner removal
and flipper-strength changes remain unimplemented pending exact identification;
this is not a completed four-change table balance or a new independent skill
session. See [checkpoint evidence](evidence/table-balance-01/REPORT.md).


Following explicit identification/confirmation, session
`01a1b6ef-6f18-72c2-9249-e06f0ee80045` applied the same actual
`competitive-rule-change` skill to B1-B3: only entry diagonals removed and
Slingshot boost parameters scaled0.75 in `fusion-1.6.0-balanced`. This does not
create another independent skill session. Independent read-only reviewer
`/root/geometry_review` verified exact delta,5balanced-table tests,6reference/
Smart tests, original157file integrity and current18freeze checks. Review
comments were resolved by required evidence-manifest checks, explicit recorded
physics labeling and archived1.5binding for the unchanged legacy prompt-v2host.
No course/student gate was approved. [Final evidence](evidence/table-balance-v16-01/REPORT.md).

### Adaptive distance-v2 follow-up

Session `01a1b6ef-6f18-72c2-9249-e06f0ee80045` explicitly applied competitive-rule-change for this proposal-interface revision and requested independent read-only review from geometry_review. This is the same session, not an additional independent skill session. The reviewer verified formulas, preserved route fields and1x/2x payload parity, and found no code defect in the focused review. See [new evidence](evidence/adaptive-distance-v2-01/REPORT.md); previous records are preserved.
