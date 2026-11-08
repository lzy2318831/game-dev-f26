# Final preparation verification — 2026-11-07

No new paid API calls,push,PR submission or frozen gameplay/visual edits.
Source evidence originals,smoke and recovery including combined report remain
unchanged; analysis.json contains their SHA256 snapshots and exact derived
statistics. All24saved trial/control traces replayed through the frozen engine
to their exact final outcomes. Ledger-analysis.json is an earlier fast derived
snapshot; analysis.json includes full replay verification. Neither is new data.

Actual results/checks:

- `python -m fusion.final_analysis --verify --output evidence/final-submission-01/analysis.json`:
  passed,all24traces verified,11completed/oneoriginalfailed,66successful recovery
  calls,68combinedattempts. Recovery estimate$0.15966225,knowncombined$0.16136925,
  conservative reserve-inclusive$0.17235675. No API invoked by analysis.
- Test-first replay contracts initially failed with ModuleNotFoundError before
  recorded_replay.py existed; after implementation3tests passed5.243s.
- Four replay/HTTP tests passed13.494s. Button,redirect,assets,manual-action400
  and cross-origin403 checks used loopback HTTP,not browser automation.
- A full run begun before the autoplay redirect/test expectation was edited
  ended135tests/onefailure138.616s due the already-loaded old expectation.
  No frozen rule failure. The clean rerun passed **135tests in140.006s**.
- Final occupied-port launcher fix was followed by **5replay/HTTP tests passing
  in22.022s**; this focused run includes the newly added occupied-port test.
  Do not describe136tests as a completed full-suite run.
- Full replay.js parsed and tests/replay-timers.cjs assertions passed using the
  existing Node runtime through node_repl. `node --check` could not run directly
  because node CLI was not on PATH. Optional CI now installs Node22 to run this
  built-in-only test; normal game/replay needs Python and browser only.
- Freeze verification passed all18artifacts repeatedly,including after final
  launcher changes. agent-config.json parsed successfully.
- Actual demo launcher started,gameHTTP200 included Watch button and /watch
  redirected successfully to replayHTML at8787/#autoplay. No browser visual
  verification claimed. An older local server on8765 caused an initial default
  launch probe to reach the old page; final launcher uses8785/8787 and refuses
  occupied ports instead of sharing a Windows socket.
- Selected authentic replay has12shots,6genuine LLM calls,Geometric935:LLM900.
  Frame regeneration and every step checked against original saved evidence.
  Sum of recorded-motion simulation times125.745833s; approximately174s of
  playback with preview/turn/result delays,plus local overhead. This is computed,
  not a completed screen recording.

Visual verification limitation:browser-control host unavailable; Windows
Computer Use automatic approval rejected controlling Google Chrome with
"Computer Use was not approved to use Google Chrome". No UI workaround or
invented screenshot/playtest evidence. Full browser demonstration remains for
the student's local review and actual recording.

Independent read-only review findings/fixes are in INDEPENDENT-REVIEW.md.
Remaining:remoteCI(currentcommit),two genuine skill-session references,student
reflection,observed other-person playtest or honest omission explanation,
3–5minute video andlinks,Week3 scope-post confirmation,approved PR/CourseWorks.
