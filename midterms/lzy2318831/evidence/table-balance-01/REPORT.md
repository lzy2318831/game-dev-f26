# Cue and Live restart checkpoint; physics identification pending

**Two UI repairs are implemented. The two requested physics changes are not.**
The instruction to identify objects before deletion/rebalancing remains binding;
the student has not yet answered the object-identification questions. No final
balanced-table version or new-physics evaluation is claimed.

## Exact physical objects found

There are no rotating paddle flippers in this implementation.

| Possible upper-corner interpretation | Actual collision definitions |
| --- | --- |
| Short mirrored entry diagonals | `left-entry` (125,85) to (88,125); `right-entry` (875,85) to (912,125), radius4 |
| Upper orbit assemblies | Each side has orbit-rise, orbit-crown, orbit-roof; left coordinates (148,150)→(148,72)→(225,35)→(385,35), mirrored right; separate decorative housing |

All guide collision bodies are in `fusion/devices.py` GUIDES. Their rail visuals
are drawn from public guide records by `drawGuide` in `fusion/web/aurum.js`.
Upper orbit housing decoration is separately drawn by `grandMechanisms` there.
These candidates are not pockets, external cushion boundaries or lower slings.
Deleting the wrong interpretation could remove a different table mechanism;
neither has been removed. Six pockets and all original boundaries remain intact.

The only powered rail activations are the two **lower triangular slingshots**,
three segments per side. `rail_collision` adds an impulse320 in direction
(±.8,-.6), enforces separating speed60 and launch speed420, at most two boosts
per ball per sling per shot, with cap950. Ordinary reflection uses1.9normal.
Visual activation is the existing280ms sling flash. Ten bumpers separately use
impulse200or260; they are not assumed to be the requested flippers.

Numerical discrepancy:0.85is a15% reduction, not25–30%. Proposed25% scaling, if
the student confirms lower slings, is0.75 on boost-related values, retaining
reflection, timing, activation limits and visuals. No scaling was applied.

## Preserved original and compatibility

Before any edits, copied all108source/test/spec files into
`versions/kinetic-replenish-v1.5-final/`. Its `snapshot-hashes.json` and original
18-artifact freeze remain exact. Existing project/evidence hashes were also
saved in [preserved-before](preserved-before.json).

Engine/devices/geometry/scoring/quotas and their replay fingerprint are unchanged.
The current game is still physical version fusion-1.5.0-replenish. The current
freeze updates only the cue renderer hash and labels this UI preparation;
the original manifest is archived. All24historical traces verify under their
original physics/version, without rewriting/regenerating their data. A distinct
revised physics version and compatibility routing are deferred until physical
object identity is confirmed. RULES.md therefore retains the original table.

## Cue repair

Before: `fire`/Live controllers created a movie immediately, `animate` advanced
ball frames from that start time, while the cue existed only in aiming preview.
There was no visible forward stroke or contact phase.

Now a presentation-only `cueStrokePose` drives pullback, forward stroke and
follow-through. Model/AI stroke reaches the radius11 cue-ball surface at260ms;
already-pulled human strokes reach it at120ms. The existing recorded ball/event
clock remains0until contact. Backend shot physics and actions do not change.
The same existing cue art is reused. Restart/cancellation clears the movie, so
its stroke cannot leak into the next match.

[Executed red regression](red-cue.txt): no forward-stroke phase. The new
`tests/cue-stroke.cjs` passes after implementation.

## Live restart repair

Verified defect: reopening after Back could see a terminal session whose worker
was still completing audit/replay. `geometryLoadInfo` previously threw after one
unsettled leave result, preventing initialization/polling from completing and
leaving start controls disabled. An initial generic credentials message could
also overwrite the actual server-budget reason.

A nonblocking `/live/settlement` status avoids waiting behind simulation locks.
Fresh-page preparation polls bounded leave/settlement for up to8seconds plus an
in-flight local-request bound. It never dispatches `/live/start`. On continued
unavailability, **Check Live readiness** reloads status; Back remains functional.
The server's original worker-dead/token/origin/new-match and cumulative-budget
guards are unchanged. The generic missing-key explanation no longer replaces
an exhausted-allowance explanation in real mode. No model retries or extra paid
requests, no reset of server caps and no paid configuration change.

[Executed red regression](red-restart.txt): the first settled=false result threw
instead of later preparing the available fresh session. Updated controller
regression passes after implementation, with no start request dispatched.

## Actual Chrome proof and checks

[Chrome summary](browser-ui/summary.json), [cue timing data](browser-ui/cue-contact-proof.json):
the cue pulled from gap22to50.98, moved forward to24.3267, then reached gap11at
260ms while the ball stayed exactly(230,250). At300ms, ball x=246.8275. These
checks executed the actual canvas controller in Chrome against a real local
HTTP server with synthetic model replies. RAF was manually stepped for this
cue observation, then the rendering clock accelerated for full-match QA;
server physics was unchanged.

Two complete12-shot matches on the same server:2x then1x. A QA-only1.6second
post-match worker delay reproduced late settlement; Back/menu and fresh-match
initialization completed without server restart. Cumulative calls6then12.
The exhausted-budget page explicitly says Server-wide allowance, remains unable
to start another paid match and still returns to the menu. One visible Back
owner, zero browser runtime errors, zero real API calls.

All212Python tests passed in the complete30-module isolated run. All seven
JavaScript checks passed. All24original replay checks and18current freeze checks
passed;108archived file hashes match. Independent read-only reviewer
`/root/geometry_review` verified the cue/controller/navigation checks, original
archive integrity, unchanged physical artifacts and the saved actual Chrome
proof. It found no remaining issues in the two implemented UI fixes, while
explicitly not approving unidentified physics changes.

Actual skill invoked: `competitive-rule-change`, session
`01a1b6ef-6f18-72c2-9249-e06f0ee80045`. No agent approved a student gate. No paid
calls, commit, push or PR. Remaining work requires the exact corner pair and
confirmation of what "flippers" refers to; no strength/collision regression for
an unimplemented table change is claimed.
