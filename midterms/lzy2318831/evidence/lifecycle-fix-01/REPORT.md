# Geometry live early-stop and repeat-match repair

Student request: fix two reproducible lifecycle bugs offline; preserve six shots
per player, engine/visual freeze, original agents and all saved evidence. No
paid calls, commit, push or PR. `competitive-rule-change` was read/invoked in
continuing session01a1b6ef-6f18-72c2-9249-e06f0ee80045, not another distinct
skill-use session. Relevant source-map row F8 and RULES F7/F8 remain authoritative.

## Verified root causes

Saved mock trace `evidence/live-browser-geometry-v1/20261107T205520Z-ec5d25b8c9d0/trace.json`
and genuine trace `evidence/live-browser-geometry-v1/20261107T212159Z-84d3482b4eb8/trace.json`
both show4 total shots, shots_remaining p1=4/p2=4, phase failed, termination
no_reliable_candidate, and2 model calls. The next selection never dispatched
(network_attempted=false). This is not a legitimate table-clear/shots-exhausted
outcome, HTTP rejection, timeout or exhausted request allowance. Strict full-path
geometry rejected every ordinary candidate and the policy aborted the engine.

GeometrySession inherited one-match-per-launch state. Complete/failed/cancelled
never returned to waiting; the can_start predicate therefore stayed false after
Back to Main Menu. It was persistent backend lifecycle state, not just a stale
button or an exhausted six-shot quota.

## Changes and acceptance

- Minimum-power fallback-escape candidates rank initial clearance and direct
  pocket exposure, with explicit uncertainty if the full stopping segment is
  obstructed. They are options sent to the LLM, not an executed heuristic move.
  Ordinary direct/pot/bank/device candidates retain their conservative checks.
  No clear stop, pot or scratch-free outcome is guaranteed for fallback routes.
- A geometry-only fresh-match endpoint requires same-origin/current-token,
  a terminal/cancelled phase and a settled old worker. It creates a new episode,
  cancellation event, ledger and token while retaining the SAME server budget.
  It does not call a model. Old tokens cannot cancel/ack/start the new match.
- Browser Back settles the old session before navigating. Reopening the live
  page prepares the next match; dispatch still requires a new confirmation.
  A New match button has the same prepare/reload/confirm sequence. Failed
  provider/selection/time-budget episodes explicitly say match incomplete.
- Per-match6 requests/$0.25 estimated remains unchanged. A visible server-wide
  lifetime limit of12 requests/$0.50 is enforced separately. New match, reload,
  cancellation and failure do not reset spending or unknown reservations.
  Start is denied unless enough remains for another full6/$0.25 match. Two full
  matches exhaust the request allowance; a new server allowance is an explicit
  launch, not an automatic UI reset or retry. No new spending was authorized or
  performed by these tests.

Test-first HTTP reproductions failed before implementation: repeat preparation
returned400, and the first synthetic match failed with no_reliable_candidate
after4 total shots (tool completion70f8b8). After fixes, HTTP integration tests
ran two complete matches and exercised failure/cancel recovery, timeout unknown
reservation carryover, stale tokens, fresh consent and exhausted server caps.
Independent review details are recorded separately.

## Actual browser/server evidence

[Headless Chrome summary](browser-run-04/summary.json) records an actual isolated
Chrome browser loading the real served HTML/JS and local HTTP endpoints. It
clicked live/start, played all engine frames, clicked Back, returned to Main
Menu and repeated the full sequence without restarting Python. Each match has
12 shots,6 per player, shots_exhausted,6 synthetic selections, and separate
trace directories. The second starts at0 local calls but6 cumulative server
calls; after it finishes, the cumulative count is12. Both traces replayed and
there were0 browser runtime errors. Result screenshots are in the same folder.
Synthetic model responses select candidate IDs; the QA harness does not choose
individual shots manually. Browser rendering clocks/previews were accelerated
and mock consent accepted by a QA stub; engine physics and scoring were untouched.
This is engineering evidence, NOT genuine LLM performance or a new human playtest.

Initial browser attempts are not hidden: sandboxed Chrome disconnected during
CDP setup; the elevated shell's Python alias exited without running the test;
the first verified-interpreter attempt timed out because its menu assertion
inspected the first decorative link instead of the actual menu link. Corrected
QA selection then exercised both full matches. These are harness/environment
failures, not additional gameplay outcomes. The final browser rerun after the
prompt-clarity correction is recorded separately when complete.

Final current-prompt browser parity run:
[browser-run-05/summary.json](browser-run-05/summary.json) passed the same two
complete matches, two menu returns,24 total shots,12 synthetic selections,
both trace replays and0 browser runtime errors. The second result screenshot
was also visually inspected: it explicitly says Mocked test, shots_exhausted,
requests6/6 and offers Back to Main Menu. No genuine superiority is claimed.

On the34 saved public observations, [updated coverage](coverage.json) retains
16direct/18including-bank contact availability and provides a fallback choice
in the previously unsupported state, leaving0 empty candidate lists. This is
geometric availability only; the older coverage artifacts remain byte-identical.

No original official11-match/2-win/9-loss report, genuine failure trace, old
coverage report or frozen artifact is rewritten.444 pre-existing evidence/
original-agent/controller hashes were captured before changes. The old
prompt-v2 launcher retains its one-match behavior; repeat-match preparation and
cumulative accounting apply to the preferred geometry launcher only.

Remaining risks: minimum-power fallback may still collide, activate a device or
scratch. Real provider decisions/latency/access remain unmeasured after this
fix. Model/API errors are not retried or converted into wins/draws. A server
budget exhausted by failed or completed calls requires a separately enabled
new server allowance; the UI explains this instead of silently resetting it.

## Final validation

- Full project Python discovery passed191 tests in384.950s (chunk3fdc36).
- All four JavaScript controller checks passed, including fresh preparation
  without dispatch/consent, incomplete-error labels and cumulative budget UI.
- Original official24 trial/control replays passed; all18 freeze artifacts
  passed again after the suite. The masked launcher also passed PS syntax.
- All444 captured original-agent/controller/evidence hashes remained identical.
- The actual current-prompt Chrome run05 and earlier run04 each replayed both
  complete saved synthetic matches. Independent review found no remaining issue.
- No paid request, commit, push, PR or course submission was performed. Staging
  is limited to this repair's scoped source/tests/docs and evidence, preserving
  earlier staged work and leaving unrelated generated preflight caches out.
