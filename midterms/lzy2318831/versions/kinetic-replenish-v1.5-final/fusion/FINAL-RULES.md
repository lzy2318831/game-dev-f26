# Final design amendment Z1-Z3 (design,2026-11-07)
Z1: 15 numbered objects plus cue. Five triangular rows, apex(700,250),
row horizontal step24*sqrt(3)/2, vertical step24, rows1..5 centered at250.
Cue230,250. Six shots/player, scoring/devices/playfield/controls unchanged.
Variable initial layouts may contain cue plus1..15 objects; pocketed ball IDs
must be preserved. Solids/apertures clear, deterministic seed-independent rack.
Z2: Original fusion/baseline.py remains byte-for-byte Geometric AI. Smart AI
is a separate deterministic bounded public-state planner, not an LLM. Uses
same authoritative physics on reconstructed detached observation snapshots;
no access to live Episode/private seed/evaluator. Candidate angles cover
geometry/direct balls/pockets/banks and all device apertures plus fixed sweep,
several powers. Rank settled predictions by points/pots/scratch and remaining
turns/position. Fixed candidate/tick work budget; partials cannot win. Geometric
proposal included. Log actual work and elapsed time; no paid model calls.
Z3: UI modes Human/Human, Human/Geometric, Human/Smart. Think automatically,
lock through planning/playback. Six-shot win/loss/draw rules unchanged. Freeze
table/rules/art after validation. Comparison suite declared before Smart tuning,
separate from frozen future live LLM vs Geometric suite. No external calls/push.
Acceptance:16 public balls IDs0..15; exact deterministic clear rack; stable
break and12-shot ending; Smart legal/deterministic/work-bounded/copy-isolated;
server autonomous Smart seat, distinct baseline; browser render all IDs/modes.

Planner frozen configuration: max24distinct candidates, max40000tick calls total,
480tick previews,9600max/candidate; Geometric proposal always fully resolved
first, then best preview utilities. Incomplete candidates cannot beat settled
ones. Candidate quotas cover ghost-ball pots, direct/combination contacts,
mirrored cushion paths, every mechanism and fixed angle exploration; multiple
power levels. Rank immediate points, credited pots, scratch penalty, tiny
cue-distance tiebreak; last-opportunity/table-clear win/draw margin dominates.
Work budget deterministic; elapsed time measured, not a portable hard deadline.
No geometry/device/scoring/turn/physics coefficient changes. Conservative
axis bounds only skip collision calculations that cannot intersect; reference
physics equivalence test verifies state/events against preserved implementation.
