# Grand Circuit maximal playfield evidence

2026-11-06, fusion-1.2.0-grand. Original design and procedural art. No historical
assets, paid calls, pushes or PR. User authorized a denser table. Preserved
46 Aurum source/test/doc files under versions/aurum-v1.1; SHA256 unchanged
(preservation.txt). Earlier evidence is retained and not relabeled.

## Actual skill/rule/test workflow

competitive-rule-change invoked by name in this conversation. Read project
instructions and skill; M1?M4 design spec and rule-map amendment preceded code.
Initial correctly located five-test run: three failures (density4!=6,
lane20!=60, scoop incoming vy200 unchanged), one error (no sling), one pass
(wrong seat). An earlier command used the wrong working directory and created
nothing; another root invocation could not import fusion. Neither counted as
red gameplay evidence. New engine implements six bumpers,26 rails (20 passive,
six powered edges), six lanes, Orbit, two slings and Vault scoop. Both ball
types interact, only cue scores devices. Cap235/shot, scratch voids all.

All public device state remains detached observation data. No action vocabulary
change: angle/power, one resolved shot per step, six opportunities per player.
Baseline sees all geometry and avoids rails; detailed scoop/sling combinations
remain an approximate policy prediction. No policy tuning or live evaluation.
Suite3 placement amendment moves only invalid solid overlaps; old suite is
archived and exact relocations recorded in layout-clearance.json.

## Genuine regressions discovered and fixed

Aggregate replay identity was expanded to engine.py+devices.py+geometry.py;
initial full run caught old replay comparison still hashing engine.py only.
Both recording and replay now use matching aggregate identity; replay test
passes. Old version traces must use their archived implementation.

Initial24-shot development sweep (angles0..345 by15, power85) found one
simulation_limit: angle225. Late powered collisions left an object still
settling at the old20-second bound. Added test_long_cascade_settles and ran it
red (assertFalse failure flag failed). M5 then specifies9600 fixed ticks40sec,
finite and explicit on exhaustion. Final74-test run and same24-shot sweep pass
with0failures. Original shot-grid.json and shot-grid-after.json retained. This
is physics QA, not model win-rate evidence. Initial sweep exercised35 sling,
8scoop,25lane and12spinner events, including object-ball contacts.

## Final executed verification

- Current full project unittest suite:74 passed,24.675s, tests.txt.
- Independent read-only /root/grand_review:8 focused tests passed,0.769s.
  No blocking findings after corrections. Reviewer authored no implementation.
- Reviewer caught incorrect positive labels on object scoop/sling hits: now
  fx.points controls awards. Also fixed mirrored right labels, added device_points
  outcome metric and clarified20passive/sixpowered rails. Fresh re-review found
  dispositions addressed. This is independent review, not student gate approval.
- Browser QA on final localhost8768: actual drag/power, bumpers, playback lock,
  autonomous baseline turn, Orbit activation/reset, full12-shot ending,
  restart/late-response guard, desktop/laptop fit; zero JS exceptions.
  fusion-browser-check.json and captured images are actual application evidence.
  Final screenshot visually inspected for layout and readable labels. End-screen
  playback accelerated for automation; this is not a human playtest.
- Root starter tests:36 run,4errors; missing anthropic SDK and Windows symlink
  privilege environment errors remain separate. Root setup incomplete (auth,
  optional Pyxel, root tests); raw logs retained. No dependency installation or
  credential use. Project game uses only stdlib/browser. git diff --check passed.

## Review instructions and known limits

Start `python -m fusion --port 8768` from project directory; server currently
running there. Select2PLAYERS or VSBASELINE. Point, press/pullback, release.
Aim at top-right Vault aperture for radial kickout; bank into triangular slings
and side/orbit lane sensors. New match resets, Escape/right-click cancels drag.
Vault is instant zero-dwell, not storage; no raised overpasses/gates or spin.
Rails are real solid capsules, lighting/paneling is decorative. A ball can stop
in a lane and be shot normally. Some straight pocket paths are intentionally
obstructed by the denser geometry. Late cascades may play longer; all impulses
and simulation remain bounded. Human enjoyment/readability needs student review.

Stopped at requested playable checkpoint. Human playtest, recording, remote CI,
live repeated model trials, separate-session skill evidence and student gate
remain pending. No final submission claim.
