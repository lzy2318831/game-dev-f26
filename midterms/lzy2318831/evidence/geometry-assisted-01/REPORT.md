# Geometry-assisted v1 implementation record

Student authorization: implement a minimal separate candidate-selecting Live
LLM experiment; preserve game/official evaluation and historical evidence;
offline checks only, no paid calls, commit, push or PR. Student gate remains
the student's decision. No new human playtest or genuine model trial is claimed.

Skill actually invoked by name: `competitive-rule-change`, read from
`skills/competitive-rule-change/SKILL.md` in this continuing Codex session
`01a1b6ef-6f18-72c2-9249-e06f0ee80045`. This is another invocation within the
same session, not a third distinct skill-use session. Acceptance/specification
is in `fusion/GEOMETRY-ASSISTED.md`; existing F2/F3/F8 remain unchanged.

Initial test-first run: `python -B -m unittest discover -s tests -p
test_geometry_agent.py -v` failed with ModuleNotFoundError for
`fusion.geometry_candidates`, before implementation (tool chunk `e7c2d9`).
The first six acceptance tests then passed. Independent review identified
escape-angle and oblique-cushion errors; actual reproducers and fixes are
recorded in [INDEPENDENT-REVIEW.md](INDEPENDENT-REVIEW.md). Fourteen focused
tests now pass, including a bank contact against the unchanged engine.

Implementation:

- `fusion/geometry_candidates.py`: public geometry only, bounded pot/contact/
  bank/device/escape choices, quantized-path checks and power/risk estimates.
  Escape is offered only without a direct contact/pot. Unsupported states yield
  no candidates. Minimum power denotes first contact/entry reach.
- `fusion/geometry_agent.py`: concise candidate IDs in a structured request;
  the LLM must choose. Strict parsing, response usage, parent call ledger,
  watchdog/worker cleanup, consent and unknown-cost accounting are explicit.
  Invalid choices never trigger a scripted replacement.
- `fusion/geometry_live.py`: opt-in separate launcher and browser identity;
  defaults to paid-disabled. Uses existing HTTP consent/origin/token checks,
  cancellation, six-request/$0.25 allowance and session/playback deadlines.
  New trace folder: `evidence/live-browser-geometry-v1/`.
- `fusion/live_session.py`: small class-default extension only; existing
  prompt-v2 policy, seat name, identity, prompt, root and trace kind retain their
  defaults. No modifications to official llm.py or prompt_v2.py.
- `fusion/geometry_analysis.py`: reproducible offline coverage of saved public
  requests, with source hashes. New tests and README/EVALUATION/source-map
  references identify this experiment separately. `agent-config.json` adds
  artifact references only; the pinned provider/model settings remain unchanged.

Authoritative reviewed coverage: [coverage-reviewed.json](coverage-reviewed.json).
The earlier coverage.json and coverage-final.json are intermediate development
outputs before the bank correction; they are not the final candidate lists.
Across34 executed genuine browser-v2 shots: direct-contact availability16/34;
including one-cushion contact18/34; device entry9/34; escape-only15/34; no
supported candidate1/34; ghost-pot0/34 under conservative screening. Old raw
actions pass the same reachable direct-clearance screen3/34. This compares
multiple available choices with one historical action, not policy success.
No candidate selection by a real model, actual new pots or wins is established.

Validation completed so far:14 focused tests passed locally in6.231s; independent
review repeated14 in6.266s. Three existing JS controller checks and syntax of the
served geometry-labelled controller passed using VS Code's bundled Node24.22.1,
not GitHub's Node22. Authentic official analysis/replay exited0 with all24
traces reproduced. Final full-suite and preservation results are recorded below.

Final validation: `python -B -m unittest discover -s tests -v` passed178 tests
in293.372s (tool completion chunk `792dc4`). An earlier pre-review full run
passed174 tests in278.890s; it does not replace the final run. All14 final new
tests passed within the178. Post-run freeze verification again passed all18
artifacts. All389 hashes in preserved-before.json match. Coverage-reviewed.json
reproduces exactly with the current generator, and README's original official
results and EVALUATION's official protocol remain intact. No Git staging,
commit, push or PR was performed for this change; earlier staged work was left
alone. Existing pilot tests also created new content-addressed, explicitly
synthetic preflight caches; these are not new live results and no pre-existing
cache/evidence was overwritten.

Remaining limitations: no physical rollouts in the generator; conservative
screening rejects many real layouts. Banks and ghost pots are approximations,
not guaranteed outcomes. Powered exits, multi-contact chains and subsequent
scratch risk are not simulated. The model may choose an offered device or
escape; geometry-assisted performance requires separately authorized new live
trials on fresh held-out cases, never reuse of official results as this variant's
performance. No additional features or spending are implied by this report.
