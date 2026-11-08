# Kinetic Circuit gameplay pass: actual evidence

2026-11-06. fusion-1.3.0-kinetic. Original Pool Shark-inspired design; no
historical code/assets or paid calls. Student requested a more energetic table.
This is one finite gameplay pass, stopped for student review, not a submission.

## Skill, implementation and preservation

competitive-rule-change invoked by name. Read submission instructions/skill,
current rules/source map/evaluation protocol. K1-K5 specification and map
amendment preceded engine work. All new mechanics use design evidence labels.
Snapshot versions/grand-v1.2 contains48 unchanged files; Aurum46, original
Fusion36, earlier source18 also unchanged by SHA256 (preservation.txt). Earlier
code/tests/evidence/results remain separate, not overwritten or relabeled.

Cascade: three closely arranged radius24 pops; Reactor: main pop plus two
radius16 relay posts and compact banks. Ten total bumpers,29 capsule guides,
stronger finite inward slings, directed Vault eject and Skyway return into the
Reactor. All are interactive. Cue aiming, six pockets, central corridor,
turns, fixed physics and five operations unchanged. Public baseline now uses
actual device radii and impulses. There is no hidden steering or randomness.
Open felt friction unchanged; devices provide the added energy.

## Test-first and genuine defects

Initial Kinetic suite (red-tests.txt) failed2/asserted missing geometry and
stronger sling direction, errored3 because new occupancy-aware sensor argument
did not exist. Implemented then passed. Extended tests exercise Vault->pop,
Skyway->pop, repeated-use limits, blocked exits, object physics without device
points, idle balls, scratch voiding, score cap and detached observation copies.

The first inward sling version could partially cancel reflected velocity on
some faces. Declared minimum powered exit420; strengthened regression ran red
at408.67 before the minimum was implemented. Two boosts/pair/shot and speed950
cap remain. The old sling test now requires stronger powered output while
retaining exactly90 passive speed after boost budget exhaustion.

Fresh reviewer identified a3.36-unit overlap between relay post8 and chamber
bank, and repeated sling impacts lacking feedback. Added tests first; actual
failures were16.6448<20 physical clearance and event awards[10]!=[10,0]. Moved
bank endpoint to590,195; all post/rail solids disjoint. Repeated sling contact
now emits zero-point events without rescoring. Corrected ten-pop labels and
help's directed Vault wording. Reviewer rechecked all changes.

Browser QA's previous spinner action no longer reached Orbit after the layout
change. Replaced with a deterministic current default-layout action15deg/85power.
That shot completes shortly after spinner activation, exposing a QA shortcut
accessing movie.start after movie became null. Guarded only the acceleration
helper, not game logic. Final automated browser pass is clean. These were QA
fixture/timing mismatches, not fabricated gameplay regressions.

Static held-out placement clearance found an old bumper-case overlap; suite4
relocates only invalid solids. Exact changes in layout-clearance.json. Grand
suite archived. No held-out policy trials or tuning occurred.

## Final executed results

- Full submission suite:84tests,31.276s,OK (tests.txt). Includes old engines,
  legal/illegal seats/outcomes/limits, determinism, player budget/failure
  boundary, playback recording independence and10 Kinetic mechanism tests.
- Fresh independent /root/kinetic_review reran10 Kinetic tests,0.995s,allpass;
  earlier player-boundary2tests passed1.593s. No blocking findings after fixes.
  No files edited by reviewer; no student gate approval.
- Same24default shots in archived Grand and final Kinetic: angles0..345step15,
  power85. Mean cue bumper hits3.9167->8.7917; cue bumper/rail contacts
  13.9583->24.0; mean shot simulated duration8.4844->10.116sec. Zero failures
  in either version. Physical contacts include passive repeated hits, not
  score payouts; common event types avoid award-suppression counting bias.
  Data: chain-comparison-final.json, stress-final.json. Initial measurements
  retained under stress-initial.json and chain-comparison.json, not final data.
  This development sweep supports richer collision chains on these shots;
  it is not live-model evaluation, human enjoyment evidence or general proof.
- Default angle345power85 regression runs through Skyway, Reactor and Vault,
  hits>=5distinct pops, settles; record_frames on/off identical. Custom cluster
  entry(325,125),angle0power70 hits all three cluster pops and Skyway, then
  settles. Raw public-API browser chain in fusion-browser-check.json.
- Browser against localhost8770: real mouse drag/power, bumper contacts,
  playback input lock, autonomous baseline reply, Orbit activation/reset,
  default Skyway+Vault+Reactor chain,12-shot ending, desktop/laptop fit and
  reset/late-response guard; zero JavaScript exceptions. Screenshots are real
  browser captures, visually inspected. Presentation time accelerated only
  for event snapshots/ending; engine still resolves actual authoritative shots.
  Browser QA is not a human playtest. Main screenshot refreshed after final
  cosmetic labels. No GUI/API evaluation success fabricated.
- Default seed101 offline development matches: baseline(P1)390 vs direct570;
  direct(P1)490 vs baseline440. Both12shots_exhausted, no execution failure;
  baseline-p1 replay passed. Baseline lost both: geometric predictions remain
  approximate, with many scratches. These are not benchmark/live-model claims.
- Root starter:36tests,4errors (SDK/symlink prerequisites), root setup incomplete
  (GitHub auth, optional Pyxel/root tests). Exact raw logs saved. These failures
  are separate from84passing dependency-free project tests. No fixture replaces
  live evaluation. git diff --check passed.

## Human review / limitations

Server launched at http://127.0.0.1:8770. From project folder run
`python -m fusion --port 8770`. Choose2PLAYERS orVSBASELINE, start, aim/pull/release.
For a reproducible lively opening aim15degrees above horizontal right (345deg)
and85%power. Watch the Cascade, Skyway transfer and repeated Reactor/Vault hits.
Try banking into an inward sling. Six shots each, no direct in-flight steering.

Device-only cap315/shot (150pops+60lanes+25Orbit+20slings+40Vault+20Skyway),
unique awards and finite impulses/transfers prevent farming; scratches void all.
The bridge is an immediate deterministic2.5D transfer with visual arc/ghost;
no true elevated flight, hidden rail collision, storage timer or full3D physics.
Exits blocked within23 defer Skyway use. Vault is instantaneous directed eject.
Some shots stay brief or scratch early; longer motion depends on device contact.
No guarantee every shot chains. Human readability/risk/enjoyment needs review.

Stopped. Paid model calls, live repeated trials, human playtest, recording,
remoteCI, proof of two distinct skill sessions and student acceptance remain
pending. No push, PR, gate approval or final submission.
