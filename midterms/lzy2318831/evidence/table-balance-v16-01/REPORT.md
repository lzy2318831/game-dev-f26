# Final confirmed table: fusion-1.6.0-balanced

This completes the two confirmed physical adjustments while retaining the
working cue-contact and Live-restart fixes. The student explicitly selected
the two named entry diagonals and lower triangular Slingshots, with0.75scaling.
No additional gameplay mechanism, scoring change or AI tuning was introduced.

## Exact physical delta

- Removed only `left-entry` (125,85)→(88,125) and `right-entry`
  (875,85)→(912,125) from `fusion/devices.py`'s guide construction.
- The remaining27guide records equal the original29-record list filtered by
  just those two IDs. Larger Orbit rise/crown/roof assemblies, center Orbit
  guides, return channels, all powered triangle segments, portals, pockets,
  table boundaries and bumper definitions are unchanged.
- Rail visuals are rendered from the same observation guide list. Removing
  those records removes both capsule collision segments and their rail art.
  No renderer-wide hiding rule or pocket deletion was used. The larger housing
  art remains byte-identical in `aurum.js`.
- Added a single Slingshot scale0.75: impulse320→240, separating-speed
  floor60→45 and launch-speed floor420→315. The vector remains(±.8,-.6).
  Reflection coefficient0.90, global950speed cap, two boosts/ball/sling/shot,
  event eligibility, scoring awards and280ms visual flash remain unchanged.
  Scaling only the vector would have left the old420floor overriding weak
  impacts, so all three boost-related values are scaled consistently.

This is a25% reduction of the boost parameters, not a promise that every
outgoing ball velocity falls25%; existing reflection, floors and caps still
combine with incoming velocity. No unrelated bumper impulse was changed.

The removed segments are internal guides. Global cushions/capture boundaries
still constrain active ball centers to x11..989/y11..489. Regression samples
cross the former segments and exercise upper/side boundaries at high speed;
active balls remain bounded and any disappearance must be a recorded pocket
scratch. No additional local geometry correction was necessary.

## Version and historical compatibility

Current gameplay identifier: **fusion-1.6.0-balanced**. Scoring formulas and
six-shot quotas are unchanged, but trajectories, contacts, scoring opportunities
and outcomes can differ. Original evaluation results do not describe this table.

`versions/kinetic-replenish-v1.5-final/` preserves all108original source/test/spec
files and its original18-artifact freeze, plus49byte-exact original approved,
recovery and smoke evidence files. Separate source/evidence hash manifests
verify157files; neither historical source nor source evidence was rewritten.
Additional historical browser/development evidence remains byte-identical at
its original root locations. The archive can load its own official inputs and
derives the same11complete/2wins/9losses plus the original failed trial.

`fusion/legacy.py` requires both manifests, verifies all157files and loads the
original package under a separate namespace. `runner.replay` dispatches only
the recognized original version to that original runner, which still enforces
its exact engine fingerprint and every event/outcome/observation hash. New1.6
traces use the current runner/fingerprint. Unknown or tampered versions are
not silently regenerated or played under different physics.

The recorded viewer constructs the original Episode and reports/displays its
original1.5version. It draws the old29guides from that observation while retaining
the current working cue presentation. Legacy prompt-v2 Live hosting is also
bound to1.5so its unchanged historical prompt facts remain accurate; preferred
Geometry-Assisted Live explicitly overrides the host to1.6. No prompt, model,
planning algorithm, power option, API credential setting or spending cap changed.
Historical saved-state power tools explicitly use the original simulator instead
of recalculating old benchmarks under new Slingshot physics.

## Tests and actual browser evidence

[Executed red tests](red-tests.txt) failed before implementation for missing
version/segment/strength changes. Five focused table tests now cover exact
guide delta, Orbit/device/bumper preservation, crossing/open former segments,
remaining boundaries/pockets, high-speed vector reduction, low-speed launch
floor, unchanged activation/scoring events, historical tamper rejection and
explicit original/current host versions.

An existing broadphase regression initially compared the new Slingshot response
against old320/420response. The preserved naive kernel now uses the same current
device response as the optimized kernel, isolating the optimization it tests.
Original physics is separately exercised by the archived version/fingerprint
tests. The original test source remains unchanged in the archive, and the first
failed run is retained. This does not claim old and revised trajectories match.

- [Full final suite](final-tests/python-module-results.json):217expected and
  217executed tests across all31discovered modules, every returncode0.
- [Seven JS checks](javascript-final.json): cue, replay, navigation, live and
  power controllers pass.
- [24 historical traces](original-replays.json): all replay under original
  archived physics; original11complete/2wins/9losses preserved.
- Current18-artifact freeze and original archived18-artifact freeze pass;
  all157archive file hashes pass, including49copies matching root originals.
- [Actual Chrome final](browser-presentation/summary.json): current1.6table
  renders27guides, no entry IDs, all six larger Orbit assembly IDs and six
  pockets; old recorded viewer reports1.5and retains29guides/entry IDs.
  [Current playfield](browser-presentation/balanced-playfield.png) and
  [original playfield](browser-presentation/original-v15-playfield.png) are direct
  actual Chrome canvas exports, not regenerated artwork.
- Cue frames at140/260/300ms show pullback, surface contact before movement,
  then follow-through; [timing proof](browser-presentation/cue-contact-proof.json).
  The test manually steps RAF for that observation, then accelerates rendering
  for full matches. Server physics is unchanged by QA clocks.
- Two complete12-shot2x/1xmatches on the same server; one Back button, two menu
  returns, QA-delayed worker settlement, fresh consent, shared budget6then12,
  and explicit exhausted-allowance explanation. Settings cannot re-enable spend.
- [Adaptive regression](browser-adaptive/summary.json): unchanged Adaptive energy
  also completes12shots on1.6and rolls back to a fresh full1xmatch, with the same
  cue/readiness/table/budget checks. These are synthetic replies, not real-model
  performance evidence. All browser reports record zero runtime errors and
  zero real API calls.

## Preservation and independent review

The physical kernel's engine.py, Geometric/Smart algorithms, Geometry planning,
Adaptive and1x/2xrecommendation code, original LLM/prompt-v2sources, server-budget
implementation and masked launcher are byte-identical to the prior checkpoint.
[Unchanged controls](unchanged-controls.json) records those checks. Only the
confirmed device definitions/boost parameters change physical behavior.

The actual `competitive-rule-change` skill was invoked in session
`01a1b6ef-6f18-72c2-9249-e06f0ee80045`; confirmed B1-B3specification and failing
tests preceded the change. Independent read-only reviewer
`/root/geometry_review` found no remaining findings after explicit version/UI/
manifest compatibility comments were resolved. It independently passed5table
tests,6final-rack/Smart/reference-kernel tests, current/original freezes and
157hashes. It made no edits or paid calls and approved no student/course gate.

## Limits and operational note

No genuine1.6LLM evaluation or new human playtest was run. Old friend-playtest,
power-calibration and official evaluation evidence belongs to1.5. Chaotic device
cascades/scratches and future simulation-limit failures remain possible; weaker
Slingshots do not prove universally better play. No win-rate gain is claimed.

Restart an already-running old Python server once to load the new physical
definitions and version. Thereafter menu returns and power changes do not need
server restarts when the remaining allowance permits another full match. A new
server process is an explicit new allowance, never an automatic spending-cap
reset. No paid API calls, commits, pushes, PR or CourseWorks submission occurred.
