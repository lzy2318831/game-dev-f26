# Sources and publication/reuse record

Inspected locally November 6, 2026. Reference repository:
[historicalsource/poolshark](https://github.com/historicalsource/poolshark),
revision `b05b01fda70a69444a58fe1bea2b5127eb93e138`.
The archive's `A7329.XX` title identifies Poolshark, date 6/14/76, initials TAH;
`PSHARK.DIR` identifies a June 13, 1977 directory update. Designer/author
attribution beyond these archive markings still needs reliable verification;
do not expand initials or invent credits.

## Inspected evidence

| Archive file | Locator | What it supports |
| --- | --- | --- |
| `A7329.XX` | `BRACK`, lines 641-681 | Ball initialization and fifteen object-ball counter (assembly numerals require radix-aware interpretation). |
| `A7329.XX` | `MVB2` through `GETVAL`, lines 551-639 | Per-ball updates and joystick-derived cue velocity components; not a conventional discrete shot command. |
| `A7329.XX` | `SRATST`, lines 496-517; `PFG` score selection, lines 1290-1296 | Player switching paths and per-player score selection; not evidence for our alternating-shot rule. |
| `A7329.XX` | `PLAY`, lines 1208-1275 | Boundary checks, rebound velocity sign changes, and pocket paths. |
| `A7329.XX` | `SCORE` and `SCACH`, lines 1276-1333 | Separate object-ball scoring/removal and cue-ball scratch paths. |
| `A7329.XX` | `WALCKE`, `DECEL`, `COLCHK`, lines 1334-1507 | Motion, deceleration, and collision calculations. |
| `PSHARK.MAP` | `SWITCHES ENABLES DATA ONTO BUS` | Game-time and extended-time hardware settings. |
| `PSHARK.DIR` | Parts listing | Distinguishes program, graphics PROMs, and diagnostic files. |
| `PSDIAG.INS`, `PSDIAG.MAC` | Pot alignment, movement, sound diagnostics | Hardware/test context; not a player rulebook. |

Line references refer to this revision. Verify them when adding rule tests.
The archive was inspected as evidence, not executed as an emulator. No gameplay
observation or manual-derived claims have been established.

## Reuse decision

The supplied archive has no LICENSE, COPYING, README reuse grant, or other
explicit permission document. Public availability is not an open license.
Reuse permission for historical code, graphics PROMs, text, and sounds is
**not established**. Do not copy or translate assembly, lookup tables, initial
layout data, artwork, diagnostic prose, or audio into the submission.

Use independently written engine/player code and original geometric visuals.
Historical links and behavioral citations document inspiration. Keep third-party
dependency versions, license links, and any reused material in this record
when dependencies are selected. Ask the instructor to resolve any doubtful
publication rights before including that material. Historical creator attribution
and dependency license verification remain open source-record tasks, so rubric
1c is not yet claimed complete.

Phase 2 has no third-party pip or asset dependencies. Runtime is CPython and
its tkinter/Tcl/Tk distribution. License references:
[Python license](https://docs.python.org/3/license.html) and
[Tcl/Tk license](https://www.tcl-lang.org/software/tcltk/license.html).
No runtime source or Tcl/Tk assets are vendored; the view uses original canvas
circles, lines and text. GitHub Actions uses actions/checkout and setup-python
as hosted workflow actions, not copied game code.

## Course references

`MIDTERM_REQUIREMENTS.txt` is the student-supplied assignment/rubric and is
preserved unchanged. Root `AGENTS.md`, `README.md`,
`.claude/skills/rule-change/SKILL.md`, `.claude/agents/rules-reviewer.md`, and
`course_game/player_interface.py` guide the process and interface. Local
instructions below adapt that process to this submission's permitted paths
and the assignment's explicit `design` evidence label.
