# Sources, credits and reuse — Arcade Fusion

The final game is an original design inspired by billiards and pinball and by
the earlier Pool Shark research. It is not Atari's game or a faithful port.

## Project-owned reuse

Fusion adapts the student's earlier independently written Python physics
structure and trace/testing patterns without changing those prior packages.
fusion/baseline.py imports project-owned distance/segment helpers from
pool/baseline.py. fusion/player.py reuses the project's bounded-worker helper
from historical/player.py; model failures use pool/model.py's exception type.
These are prior project implementation artifacts, not historical Atari code.
The complete submission retains those modules so a fresh clone is sufficient.

## Visuals and runtime

All Fusion rails, balls, felt texture, cue, bumpers, branding marks, particles,
lighting, scoreboards and screens are original Canvas/CSS/vector code. No
downloaded images, fonts, sound, sprites, ROMs, logos or historical lookup tables
are bundled. System font names select fonts already on the player's device.
Runtime uses Python standard library and the installed browser; no pip/Node
dependencies or third-party game engine are needed. Optional isolated Chrome
QA uses an installed browser and a separate ignored profile; no browser
binaries/profile caches belong in the PR.

## Historical attribution and limits

Research reference: [historicalsource/poolshark](https://github.com/historicalsource/poolshark),
revision b05b01fda70a69444a58fe1bea2b5127eb93e138. Its A7329.XX title carries
date 6/14/76 and initials TAH; PSHARK.DIR has a 6/13/77 update. No reuse grant
was established in the supplied archive. Historical code/assets were not
copied into Fusion, and the original archive was not modified. Do not infer
open licensing from public availability. Earlier detailed source locators and
research uncertainty are preserved in versions/pre-fusion/SOURCES.md and the
archived map, not presented as verification of the new original rules.

The course starter's five-operation interface and rule-change/reviewer process
are credited as architecture/process references (root AGENTS.md, README.md,
course_game/player_interface.py and .claude/ instructions). The student-provided
MIDTERM_REQUIREMENTS.txt remains unchanged and governs rubric deliverables.


Aurum Circuit v1.1 adds original capsule guide geometry, return sensors, a
traversable Orbit spinner and procedural Canvas mechanical artwork. No new
third-party assets, runtime dependencies or historical material were imported.
The earlier two-bumper Fusion implementation is preserved in versions/fusion-v1/.

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

Real LLM integration uses standard-library HTTPS,not imported game code/assets.
Official OpenAI Responses/structured-output/model/pricing docs checked2026-11-07;
exact links in LLM-SETUP.md. No key/source assets copied,SDKdependency or paid
call added to CI. Models' replies must be legaldata,never executable code.
