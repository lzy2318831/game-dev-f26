# Draft PR description — student review and submission approval pending

**Title:** Kinetic Circuit: an original Pool + Pinball game with an autonomous LLM player

**GitHub login:** lzy2318831  
**Project folder:** `midterms/lzy2318831/`  
**Target:** `columbia-university-ai-games/game-dev-f26`, branch `main`

## What this adds

Kinetic Circuit combines cue-shot billiards with bounded pinball chain reactions
on one original table. It has a 15-ball opening rack, six pockets, limited refill,
alternating six-shot turns, clear scoring and a complete win/loss/draw ending.
Human/Human, Human/Geometric and Human/Smart modes are playable locally.

The engine exposes reset, observe, legal_actions, step and outcome. A genuine
OpenAI player selects and submits angle/power actions from public observations.
The Geometric baseline is unchanged; Smart is a separately labelled physics-search
policy, not an LLM. An authentic recorded match and a separately consented live
prompt-v2 mode run autonomously, with Back to Main Menu and safe cancellation.

This is an original Pool Shark-inspired adaptation, not a faithful reconstruction.
The code and visual assets are original/project-owned; no historical code, ROM,
graphics or sounds were imported without permission. Earlier versions and their
evidence are preserved separately. Gameplay and table design are frozen.

## Original official evaluation

| Measure | Verified result |
| --- | --- |
| Completed LLM matches | 11 |
| LLM wins / losses / draws | 2 / 9 / 0 |
| Initial preserved failure | 1 HTTP 429 rejection |
| Mean LLM / actual Geometric opponent score | 720.45 / 1347.27 |
| LLM illegal actions | 0 |
| LLM cue scratches | 25 in 66 shots |
| Successful continuation calls / reported tokens | 66 / 205,473 |
| Continuation estimated cost | $0.15966225 |

The model did not outperform Geometric overall. Failed requests, unknown usage
and cost reservations are retained. Later prompt-v2 pilots/live demos are separate
development evidence and do not replace the original evaluation. There is no
claim of statistical certainty or a successful physics-assisted LLM planner.

## Validation and boundaries

Local development passed 164 project tests, controller regressions and the
18-artifact freeze verification. All 24 official trial/control traces replay
offline. CI is scoped to this folder and the one permitted workflow, requires no
provider secrets, and covers rule invariants, legal/illegal actions, terminal
outcomes, observed regressions and limits. A remote green run is still pending.

This PR is intended to contain only `midterms/lzy2318831/**` and
`.github/workflows/midterm-lzy2318831.yml`. No credentials, private playtester
information, installed dependencies or browser profiles should be submitted.
The final RULES edit corrects descriptions only; its updated documentation hash
and archived original freeze manifest do not change gameplay hashes or results.

## Required links and unfinished evidence

Verify these repository-relative links against the PR's source branch when pasting:

- [README and exact commands](midterms/lzy2318831/README.md)
- [Evaluation and raw evidence](midterms/lzy2318831/EVALUATION.md)
- [Agent-team log](midterms/lzy2318831/AGENT-TEAM.md)
- [Human playtest notes](midterms/lzy2318831/PLAYTEST.md) — **PENDING actual observations or a truthful omission explanation**
- [Independent review](midterms/lzy2318831/evidence/final-submission-01/INDEPENDENT-REVIEW.md)
- [Navigation/review evidence](midterms/lzy2318831/evidence/navigation-fix-01/REPORT.md)
- [Source/reuse terms](midterms/lzy2318831/SOURCES.md)
- **Recording URL: PENDING — insert the actual viewable 3–5 minute video.**
- **Remote CI URL for the submitted commit: PENDING.**
- **Implementation session and two independent skill-session references: PENDING.**
- **Week 3 scope-change discussion link: PENDING confirmation.**
- **Student review of the reflection, limitations and this description: PENDING.**

The replay program is not the submitted recording. Automated checks and my own
playtesting are not another-person observed playtest. This remains a draft until
the missing evidence and student review are addressed. No push, PR creation,
merge or CourseWorks submission is authorized by preparing this description.
