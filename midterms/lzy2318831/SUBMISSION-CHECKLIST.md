# Midterm submission checklist

Final publication update: the reviewed commit was pushed to the student fork.
The [Midterm CI run](https://github.com/lzy2318831/game-dev-f26/actions/runs/42435757312)
failed with13historical replay-divergence errors on Linux/Python3.11;3.12was
cancelled. Local Windows/Python3.15.1 checks passed. The follow-up proves a
one-ULP platform sine difference; strict CI now uses the Windows reference
environment without changing engine/evidence or relaxing assertions.
[Course PR97](https://github.com/columbia-university-ai-games/game-dev-f26/pull/97)
is open from the authorized course student branch to main. Inspect its actual
checks for final status. CourseWorks remains manual.

This checklist follows [MIDTERM_REQUIREMENTS.txt](MIDTERM_REQUIREMENTS.txt).
**The course PR is published; CourseWorks hand-in is not complete.** Technical
implementation, the original live comparison, student video URL and finalized
reflection are present. Confirm recording access/duration and current CI status.

## Completed and inspectable locally

- [x] Original, bounded Pool + Pinball game with a complete match and clear outcome.
- [x] Public five-operation interface, validated proposals and detached observations.
- [x] Original Geometric baseline; Smart and LLM implementations kept distinct.
- [x] Genuine original LLM evaluation: 11 completed games, 2 wins, 9 losses,
  original HTTP 429 failure preserved; scores, legality, scratches, usage,
  latency, dated costs and matched controls in [EVALUATION.md](EVALUATION.md).
- [x] Authentic autonomous recorded replay and separately guarded live mode.
  Geometry-Assisted LLM v1 is the preferred final live demonstration; original
  and prompt-v2 implementations/results remain separate. Real HTTP wiring is
  tested with synthetic responses; an authorized real-provider smoke is pending.
  [Lifecycle regression](evidence/lifecycle-fix-01/REPORT.md) verifies two
  consecutive full matches in actual headless Chrome with synthetic model
  selections and fresh consent, without restarting the server. Per-match and
  cumulative server limits are displayed separately and retained across matches.
- [x] Local deterministic tests, trace replay, controller/cancellation regressions
  and frozen gameplay verification. Earlier local validation passed183 tests;
  [final validation](evidence/final-geometry-01/REPORT.md) records finalization checks.
- [x] Scoped, credential-free CI workflow exists. This does **not** mean remote CI is green.
- [x] Reusable skill artifact and two distinct actual skill-use sessions are
  documented in [AGENT-TEAM.md](AGENT-TEAM.md). The first skill-use session and
  implementation-session reference are verified in
  [the session audit](evidence/submission-readiness-01/SESSION-EVIDENCE.md);
  AGENT-TEAM.md records the fresh second session's invocation and log locators.
- [x] Local repository scope, candidate-file inventory and credential-pattern
  review completed; ignored browser/cache files remain excluded. See
  [readiness report](evidence/submission-readiness-01/REPORT.md).
- [x] Separate read-only review artifacts record findings, fixes and rechecks.
- [x] Source/reuse terms, rule map, prior versions and original evidence are retained.
- [x] Week 3 scope-change publication confirmed by the student in this Codex
  conversation. [WEEK3-SCOPE-CHANGE.md](WEEK3-SCOPE-CHANGE.md) preserves the
  supplied published post verbatim; the direct discussion URL is unavailable.
- [x] Six final submission documents prepared; final student approval is still needed.
- [x] Observed other-person human playtest completed: I watched my friend play
  independently without coaching aiming, power or moves. Three genuine findings
  are recorded separately from my analysis and future improvements in
  [PLAYTEST.md](PLAYTEST.md).

## Personal evidence status — pending

| Requirement | Current evidence | What I need to do |
| --- | --- | --- |
| **3–5 minute recording** | Student supplied the [final video](https://youtu.be/eLdDOiIwE84), linked in README and the complete PR description. | Confirm the required 3–5 minute duration and instructor/TA/peer access; these were not independently viewed by the assistant. |
| **Observed human playtest: completed** | I personally watched my friend play independently without helping. PLAYTEST.md records the three genuine findings, my interpretation and proposed future improvements. | No further playtest session is required for this item. Missing duration, identity and incident counts are not invented. |
| **Two distinct reusable-skill sessions: completed** | AGENT-TEAM.md records actual invocations in implementation session `01a1b37c-aa97-7781-91f4-ec7693968a43` and fresh read-only review session `01a1b6ef-6f18-72c2-9249-e06f0ee80045`, with transcript references. | Retain the actual invocation evidence; inherited reviewer history is not counted as a separate use. |
| **Implementation session reference: completed** | AGENT-TEAM and PR link the sanitized reference to actual session `01a1b37c-aa97-7781-91f4-ec7693968a43`, with source lines and hashes. | Retain the original local log for verification. No implementation session link remains missing. |
| **Student reflection** | Student finalized the first-person PR description and authorized publication. | Preserve the supplied reflection and substantial future-improvement discussion. |
| **Week 3 scope change: publication confirmed** | The student confirmed publishing “Midterm Scope Update — Kinetic Circuit” in the Week 3 CourseWorks Discussion. WEEK3-SCOPE-CHANGE.md preserves the student-provided text verbatim. | Direct URL unavailable; add it if available and required. Publication is student-confirmed, not independently verified through CourseWorks. |
| **Remote CI** | The first Linux run failed; platform sine rounding is verified as the cause. The unchanged strict suite now runs on Windows3.11/3.12. | Inspect the [course PR checks](https://github.com/columbia-university-ai-games/game-dev-f26/pull/97/checks) for the submitted head; Linux numeric probes are not replay passes. |
| **Geometry-assisted real-provider smoke** | Real HTTP wiring is exercised with a synthetic opener; no genuine new request or live quality result. | If desired, explicitly authorize the bounded paid smoke, supply the key privately and confirm the browser match. This is not a stronger-agent claim. |

## Final hand-in — not performed

- [ ] Review the six documents and resolve or honestly disclose every pending item.
- [ ] Check all links, video access and the final limitations paragraph.
- [ ] Review the diff: only this submission folder and the permitted workflow;
  no keys, private playtester data, dependency caches or browser profiles.
- [x] Authorize final scoped staging (student instruction in this session).
- [x] Explicitly approve committing and pushing the intended branch (student final submission instruction).
- [x] Open **one PR** to `columbia-university-ai-games/game-dev-f26`, targeting
  `main`; include login, title, README, evaluation, agent team, playtest and video links.
- [ ] Review the actual remote CI result and final source-branch links.
- [ ] Submit the **course-repository PR URL** to CourseWorks. A fork URL or archive
  alone is not the hand-in. PR merging is handled by the instructor/TAs.

The provided assignment states November 7, 11:59 p.m. The last push to the PR
branch determines the submitted version; later corrections follow the course's
late policy. Do not force-push after the deadline. No assistant can approve a
course gate or change that deadline on my behalf.

## Verification commands

Working directory: `midterms/lzy2318831/`. These checks are offline:

```powershell
py -m unittest discover -s tests -v
py -m fusion.freeze
py -m fusion.final_analysis --verify
```

Use [README.md](README.md) for launch commands and mode distinctions. Do not
rerun completed paid evaluation scripts as a routine submission check.
The documentation-only RULES corrections and original freeze record are
tracked in [the final documentation audit](evidence/final-docs-01/DOC-CORRECTIONS.md).

## After submission

The brief separately requires silent-playtester notes on three assigned
classmates' recordings: assignments at the November 9 session, notes due before
class November 16. These are not completed by this checklist. No Asana links are
required for this Midterm; the brief introduces Asana with the final project.


Geometry-assisted stabilization: one bounded Back control replaces duplicate
result controls; new-match consent and cumulative server allowances remain
enforced. Contact/bank runout is reduced to 15 units, without the extra speed
margin, and direct contact/pot routes take priority over device-only proposals.
The historical 266-degree/power-4 cascade is reproduced offline; power 1 settles
in 354 ticks at that position. This is not a new genuine LLM evaluation or a
performance claim. See [stabilization report](evidence/stabilization-01/REPORT.md).

Student demonstration preference:2x Geometry-Assisted Live LLM candidate power,
with1x selectable before fresh-match consent. The accepted increased scratch
risk is documented, without a win-rate claim. Previous experiment evidence is
preserved; [runtime setting validation](evidence/power-setting-01/REPORT.md)
records settings, trace labels and unchanged spending/navigation protections.


Final gameplay is `fusion-1.6.0-balanced`: only confirmed entry diagonals removed
and Slingshot boosts scaled0.75; cue/restart fixes retained. Originalv1.5release,
49official/smoke evidence files and exact hashes are archived. Historical24trace
verification uses original physics, not revised outcomes. No genuine v1.6LLM
performance claim. See [final table checks](evidence/table-balance-v16-01/REPORT.md).
The video URL and final PR reflection have now been supplied by the student.
Remote CI and actual PR/CourseWorks completion remain tracked separately.

The recorded friend playtest and original LLM/power experiments remain v1.5
evidence; no new v1.6human-experience or real-model performance result is claimed.

Adaptive distance-v2 is an optional v1.6 power-profile revision;1x/2x and historical evidence remain available. See [offline profile verification](evidence/adaptive-distance-v2-01/REPORT.md). The student finalized the video URL and PR reflection; remote CI and actual PR/CourseWorks completion remain separately tracked.

Final submission preparation: [complete student PR description](PR-DESCRIPTION.md), [demo](https://youtu.be/eLdDOiIwE84), and [fresh validation](evidence/submission-final-01/REPORT.md). The student explicitly authorized commit, fork push and one course PR; CourseWorks remains manual.
