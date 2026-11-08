# Actual development regressions

## Collision separation crossed a cushion

Discovered in Phase 2 boundary exploration after the first engine passed its
11 tests. An overlapping pair near a rail produced cue x=2.5. A reachable
reproducer using a touching pair is now
`test_pool.PhysicsTests.test_collision_at_cushion_keeps_centers_inside`:
cue at (10,200), object at (30,200) moving left at 100 units/second; one tick.

Actual red run (12 tests, one failure):
`AssertionError: 9.791666666666666 not greater than or equal to 10`.

Cause: equal half-overlap separation ran after cushion handling and ignored
rail constraints. Fix: compute available displacement along each separation
normal and assign the other ball the displacement a rail-constrained ball
cannot take. The reproducer now checks both the rail bound and 20-unit spacing.
This refines R3; it does not change aiming, scoring or turn rules.

## Replay ignored a changed acceptance flag

Discovered while checking trace validation. The original replay conditional
entered an error branch on mismatched acceptance, then only raised if the
observation also differed. An altered acceptance flag alone was accepted.

Actual red run (19 tests, one failure), reproducer
`test_pool.RunnerTests.test_trace_rejects_altered_acceptance`:
`AssertionError: ValueError not raised`.

Fix: compare acceptance, events and normalized snapshots independently in one
condition. The reproducer now passes. These are application regressions;
neither is fabricated human feedback or a live model failure.
