# Midterm submission checklist

This checklist follows [MIDTERM_REQUIREMENTS.txt](MIDTERM_REQUIREMENTS.txt).
**The submission is not complete.** Technical implementation and the original
live comparison are present; personal evidence and the actual hand-in remain.

## Completed and inspectable locally

- [x] Original, bounded Pool + Pinball game with a complete match and clear outcome.
- [x] Public five-operation interface, validated proposals and detached observations.
- [x] Original Geometric baseline; Smart and LLM implementations kept distinct.
- [x] Genuine original LLM evaluation: 11 completed games, 2 wins, 9 losses,
  original HTTP 429 failure preserved; scores, legality, scratches, usage,
  latency, dated costs and matched controls in [EVALUATION.md](EVALUATION.md).
- [x] Authentic autonomous recorded replay and separately guarded live mode.
- [x] Local deterministic tests, trace replay, controller/cancellation regressions
  and frozen gameplay verification. Latest completed development run: 164 tests.
- [x] Scoped, credential-free CI workflow exists. This does **not** mean remote CI is green.
- [x] Reusable skill artifact and invocation reports exist.
- [x] Separate read-only review artifacts record findings, fixes and rechecks.
- [x] Source/reuse terms, rule map, prior versions and original evidence are retained.
- [x] Six final submission documents prepared; final student approval is still needed.

## Required personal evidence — pending

| Requirement | Current evidence | What I need to do |
| --- | --- | --- |
| **3–5 minute recording** | Replay and recording guide exist; no completed video URL supplied. | Record autonomous agent play, state recorded/live distinction and limits, check duration/access, add the actual URL to README and PR description. |
| **Observed human playtest** | My own testing is reported; PLAYTEST.md has no actual other-person session notes. | Watch someone else play without coaching; add anonymous actions, hesitation/guesses and changes. If impossible, give the actual reason and what the test would check. |
| **Two independent reusable-skill sessions** | SKILL.md and reports exist; two distinct saved session references are not verified. | Attach genuine URLs/logs showing the named skill used in two separate sessions. Repeated turns/reviewer agents are not a substitute. |
| **Implementation session reference** | Project instructions and source exist. | Link the actual building session/cloud task/CLI record from AGENT-TEAM and PR. |
| **Student reflection** | Assistant-assisted first-person draft based on documented decisions. | Read, correct and approve my own explanation; add genuine human feedback and my interpretation of the failures. |
| **Week 3 scope change** | WEEK3-SCOPE-CHANGE.md exists. | Confirm the corresponding discussion post and supply its actual link. |
| **Remote CI** | Workflow and local passing checks exist; no current remote run verified. | After approving the push, inspect both Python jobs and link the green run for the submitted version. |

## Final hand-in — not performed

- [ ] Review the six documents and resolve or honestly disclose every pending item.
- [ ] Check all links, video access and the final limitations paragraph.
- [ ] Review the diff: only this submission folder and the permitted workflow;
  no keys, private playtester data, dependency caches or browser profiles.
- [ ] Explicitly approve staging/committing and pushing the intended branch.
- [ ] Open **one PR** to `columbia-university-ai-games/game-dev-f26`, targeting
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
