# Week 3 scope change — student-confirmed published post

## Current submission status

**Publication status: confirmed by the student.** The student confirmed in this
Codex conversation that they already published the post below in the Week 3
CourseWorks Discussion. The title and text are preserved verbatim as
student-provided evidence. This records their confirmation, not independent
verification through CourseWorks. No CourseWorks access or search was performed.

**Direct discussion URL: unavailable.** No permalink or publication timestamp
was supplied; neither is inferred from this conversation.

## Published post: Midterm Scope Update — Kinetic Circuit

For my Midterm, I originally planned to recreate Pool Shark (Atari, 1977), but I decided to change the direction and build an original Pool + Pinball game called Kinetic Circuit.

I wanted to keep the basic pool mechanics while adding more interesting interactions, such as bumpers, special scoring areas, and chain reactions. I thought this would make the gameplay more engaging and also create a more challenging environment for an AI agent.

The final scope is one playable table with 15 object balls, six pockets, and six shots per player. I'm focusing on the physics, scoring system, and autonomous agent rather than trying to reproduce the original Atari game exactly.

For the AI part, I'm using an LLM agent that observes the game state and chooses its shot angle and power automatically. I'll compare its performance with a geometry-based baseline.

The main challenge is that the agent has to make decisions in a game where even a small change in angle or power can lead to very different results.

I think this new direction is more interesting to develop and gives me more opportunities to evaluate how an AI agent handles physics-based gameplay.

## Current game context

The final game is Kinetic Circuit:15 object balls plus cue, six shots per player,
limited five-ball replenishment at most twice, the fixed Kinetic devices, and
separate Geometric, Smart and genuine LLM policies. The original official live
evaluation and observed friend playtest are complete. The recording is deferred
and remote CI/hand-in remain pending. The earlier six-ball draft and dated phase
notes below describe historical checkpoints, not the current final status.

## Earlier draft and phase history


Historical assistant-prepared draft and phase notes follow. They are not the
published post reproduced above; their pending/posting statements describe
earlier checkpoints and are superseded by the student's confirmation above.

Final project direction: **Pool + Pinball: Arcade Fusion**, an original
Pool Shark-inspired arcade billiards adaptation implemented from scratch with
reusable project-owned Python infrastructure and original Canvas graphics.

The midterm is a complete two-player match: one cue, six objects, six pockets,
four impulse bumpers, passive side returns and a shot-only Orbit multiplier, mouse aim/pullback shots, pot/bumper/combo scoring, scratch
penalties and six alternating opportunities per player. Higher score wins,
ties draw. This replaces both the six-ball prototype and the historical
reconstruction attempt; neither prior version is presented as the final game.
Their code/tests/evidence remain preserved and results are kept separate.

The playing agent will submit angle/power through the five-operation interface
and face a geometric baseline on three predeclared situations. Repeated live
trials, model-call controls, CI, independent review, actual human playtest,
student reflection and recording remain the same rubric obligations.

Excluded: historical fidelity, original ROM/assets, advanced spin, tournaments,
network multiplayer, and optional features before the student reviews this
playable slice. Model API calls and final PR submission require later direction.


2026-11-06 Grand Circuit: student explicitly requested a denser original table.
Aurum archived; competitive-rule-change invoked by name, M1?M5 specified,
failing tests preceded implementation. Original procedural assets only.
Fresh read-only reviewer /root/grand_review ran8tests and found no blocking
issues after corrections; student gate/playtest pending. Actual evidence:
evidence/maximal-1/REPORT.md. No paid calls, push, posting or gate approval.
This assistant factual record does not substitute for student reflection or
two proven distinct skill sessions.

2026-11-06 Kinetic Circuit: student explicitly authorized a gameplay chain pass.
competitive-rule-change invoked by name; K1-K5 design spec, failing tests,
implementation, public boundary checks and fresh read-only reviewer completed.
Original code/vector assets, no historical imports or paid calls. Grand v1.2
snapshot preserved. Independent /root/kinetic_review ran10tests,0.995s, all OK
and no blocking findings after fixes. Exact evidence: evidence/kinetic-1/REPORT.md.
This factual assistant record is not student own-voice authorship, proof of
separate skill sessions, a posted scope change, human playtest or gate approval.
Live trials, recording, remoteCI and student acceptance remain pending.

2026-11-07 final authorization:15objects plus cue and distinct Smart simulator
opponent; no table redesign. competitive-rule-change invoked by name, Z1-Z3
specified, rack/Smart tests run red before relevant implementation. Snapshot
versions/kinetic-six-v1.3 preserved. Geometric source byte-identical. Fresh
/root/final15_review verified6focused tests13.808s, exact archived physics on
four16-ball breaks and corrected thinking/playback HUD; no blocking findings.
Actual final tests/browser/comparison evidence: evidence/final-15/REPORT.md.
90project tests passed, six development matches allreplayed; Smart6/6wins on
small fixed suite. Not live model trials/human playtest. No paid calls,push,
PR/gate approval. Technical freeze follows user's final-design instruction;
student still owns course gates and own-voice interpretation. This conversation
is not proof of two independent skill sessions. Remaining evidence in MIDTERM-NEXT.md.

Replenishment amendment2026-11-07: student reports late-match emptiness and
explicitly authorizes limited refill only. competitive-rule-change invoked by
name, R1-R4spec/map, failingtests before code, independent read-only review.
Fresh /root/replenish_review ran10tests19.804s,100seeded placement states,
no blocking findings. Geometric/device physics unchanged; Smart clearance guard
only. No new assets/devices. Factual assistant evidence: evidence/replenish-1/.
Student retains gate/authorship. Not proof of two independent skill sessions,
observed human playtest, paid LLM trials, posting or submission. No push/PR.
