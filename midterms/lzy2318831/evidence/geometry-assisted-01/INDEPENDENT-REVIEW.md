# Independent read-only review: geometry-assisted v1

Reviewer context: `/root/geometry_review`; distinct from the implementation
context, spawned for the handoff required by `competitive-rule-change`.
The reviewer edited no files, made no API calls or Git mutations, and did not
approve a student/course gate. This file records their returned findings.

No remaining blocking findings in the reviewed scope after corrections.

1. Escape candidates ignored legal angle bounds. A schema restricted to90°
   returned0° escapes. Fixed with angle-bound filtering and a regression test.
2. Oblique banks incorrectly assumed specular reflection. Actual cushions damp
   only the normal velocity component by0.88. Reproducer: cue(200,300),
   object(600,300), no devices/bumpers; the old305°/power39 candidate left the
   object unmoved. Fixed by a damped mirror construction, normal-only reflected
   velocity, unrounded outgoing direction and corresponding energy estimate.
   The new oblique-bank engine-contact regression passes.

Requested additional worker tests were added: invalid candidate usage/attempt
accounting, live consent refusal, hanging-worker timeout/unknown reservation,
HTTP variant identity and paid-disabled state.

Independent checks after fixes:14 focused tests passed in6.266s; all18 frozen
artifacts passed; all389 recorded pre-existing evidence/official-code hashes
matched. Inspected generator, selector, browser entry, coverage analyzer,
contract, focused tests, reviewer instructions and the small live_session.py
extension. Checked public-only geometry, integer launch directions, obstruction
and portal screening, power estimates, strict ID selection, no silent action
replacement, failure metadata, inherited consent/cancel/deadline limits and
separate variant identity. Prompt-v2 defaults remain intact.

Limits: geometric contact is not guaranteed potting; subsequent rebounds,
powered exits and scratch consequences remain approximate. Saved-observation
coverage does not establish genuine model selection quality or improved wins.
