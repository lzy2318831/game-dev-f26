# R1-R4 limited replenishment amendment (design)

R1 Opening unchanged15objects+cue. After a VALID shot fully settles, score and
scratch respot resolve, then if at most8objects remain and another opportunity
exists, attempt ONE atomic batch of5objects. Max2events/match. No mid-motion,
invalid-call/reset/observe spawning, no batch after final opportunity/failure.
Replenishment precedes early table-clear termination while supplies remain;
0remaining therefore becomes5. After supplies exhausted, normal clearance ends.
One batch per shot boundary even if the result still has<=8objects. Six shots
per player remains the strict match bound; score/foul rules unchanged.

R2 Deterministic ordered open grid placements,23minimum ball center spacing,
16from guide centerlines,bumper radius+12,pocket radius+ball radius+1=41.
Avoid scoop/bridge apertures,bridge exit,spinner/lane sensor segments and sling
interiors. All5placements must be found before commit; otherwise defer without
consuming event, retry after next valid settled shot. Moving ball forbids refill.
Reuse lowest inactive/missing numbered IDs1..15; never duplicate active IDs.
New balls have zero velocity, no points for spawning. Max25object pots/match.

R3 Detached observation.replenishment exposes threshold,batch,maxevents,used,
remaining,objectcount,pending and placement/precedence description. All agents
receive same field. Geometric source unchanged. Smart search/budget unchanged;
only terminal-clear prediction accounts for available replenishment supplies.
Snapshots/trace outcomes include used count; replay validates new event/state.

R4 Boundary playback frame and zero-point batch event, subtle spawn glow and
short toast notification. No control,device,layout,scoring or aesthetic redesign.
Current15-object scenario placements stay valid; suite metadata amended for
new transition, prior declarations/results preserved. No old AI win rates are
relabeled as current results. No paid calls/push/PR.

Acceptance:8restingobjects ->13,nextseat,samepoints;9 ->no batch;0withsupply
->5notterminal;0exhausted ->clear;finalshot ->no batch. Two events max, one per
boundary; blocked batch atomic; scratch voids score then safe respot/refill.
Full episode12opportunities deterministic,replayevent/counter matches.
