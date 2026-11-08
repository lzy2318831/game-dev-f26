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

