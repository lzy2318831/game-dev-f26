# Student-selected Geometry-Assisted Live LLM power

The student explicitly reviewed the earlier offline experiment and accepts
increased scratch risk in exchange for more energetic demonstration shots.
The live launcher now initially prefers2x;1x remains selectable before any fresh
match. This decision is not evidence of better LLM performance or win rate.
The earlier [experiment report](../power-2x-01/REPORT.md) and all evidence retain
their original results and recommendation; this is a subsequent student choice.

## Exact implementation

`geometry_candidates.py`, engine/scoring, Geometric, Smart, original LLM and
prompt-v2 are unchanged. `GeometryPlayer` applies a detached post-generation
power transform: `min(100, original_power * power_multiplier)`. IDs, angle,
target, route, reach estimate and base candidate ordering remain intact. Each
row records original_power and power_multiplier;2x risk notes explicitly explain
that base stopping/scratch estimates do not establish safety. The model receives
these candidates and selects an ID. No scripted selection or replacement action
is used. Strict selection validation and failure behavior remain in force.

The server factory prefers2x. Low-level GeometryPlayer/GeometrySession defaults
remain1x for the stabilized programmatic path. The UI can change a waiting
session through `/live/power`, guarded by same origin, current token, strict
integer1/2 validation, the match lock and session lock. Match start and setting
mutation serialize under the session lock. Active/terminal/unsettled sessions
reject mutation: return to menu and prepare a fresh waiting match first.
The setting dispatches no model call, rotates no token, clears no cancellation
and resets no accounting. New matches preserve both setting and shared budget.

UI shows a Candidate power selector before consent, the active multiplier in
the live budget/status line and confirmation, and labels it again on results.
An uncertain setting-update response blocks consent until reload/Back; it does
not silently assume the requested setting. Trace root, consent, status and
per-call/selected-candidate metadata retain the setting and original power.
The1x candidate actions are unchanged; request metadata and the explanatory
system text now identify the setting and are not byte-identical historical
LLM requests.

## UI steps

1. Launch the existing Geometry live launcher (mock or authorized paid mode),
   then open http://127.0.0.1:8835/ and choose Geometry-Assisted Live LLM.
2. Before confirming, choose Candidate power: **2x - student demonstration
   preference**, or **1x - stabilized fallback**. A new server initially uses2x;
   within that process, the last setting persists between matches.
3. Confirm the match separately. Changing power alone sends no model request.
4. To change after a match/error/cancellation, use Back to Main Menu, reopen
   Geometry-Assisted Live LLM, choose the other setting and confirm the fresh
   match. Wait for old work to settle; remaining server allowance must cover
   the existing six-request/$0.25 match cap. No server restart or code edit is
   needed to switch. Loading this newly implemented code into an already running
   old Python process requires the usual one-time process restart.

The per-match6/$0.25 and server-wide12/$0.50 estimated limits, explicit consent,
credentials privacy, cancellation and no-retry protections remain unchanged.
Paid execution still requires separate enablement and browser consent. No paid
calls were made during implementation or verification.

## Executed regressions and browser proof

The first four new tests failed before implementation: multiplier keyword,
power transform and live setting metadata/endpoint did not exist. See
[initial red tests](red-tests.txt).

Independent review then found a cap alias: two candidates at the same angle
could both become power100, and the parser recovered the first matching action
for metadata. [The executed red regression](red-cap-alias.txt) recorded selected
ID1 instead of the model's ID2. The parser now retains the validated selected
ID directly, preserving target/route/risk provenance even when actions coincide.

Actual Chrome, real loopback HTTP, synthetic model transport only:

- [Final setting switch](browser-switch-final/summary.json): full12-shot2x match,
  Back/menu, select1x, full12-shot1x match on the same running server; cumulative
  requests6then12. At exhausted allowance, selecting2x still leaves start
  disabled and cumulative calls12. Declining confirmation sends no request.
- [HTTP failure recovery](browser-http-recovery/summary.json): failed2x request,
  Back/menu, select1x, fresh full12-shot match. Budget use is retained.
- [Historical simulation failure](browser-simulation-recovery/summary.json):
  QA-only historical action prefix reproduces actual simulation_limit at shot7;
  exactly one Back, deliberately hung leave response cannot trap navigation,
  fresh1x12-shot match completes without restarting the server. This historical
  reproduction fixture is separately labeled and not a production proposal.

All these browser summaries record zero runtime errors and zero real API calls.
The browser verifies every model shot's recorded ID/action/power setting on the
setting-switch runs. Screenshot evidence includes both waiting-state selectors.

[Known position check](known-position.json): the current candidate at266degrees
uses power1 at1x and power2 at2x. Both settle (354 and4671ticks), without scratch.
The historical power4 still reaches9600ticks in the regression test. No physics
cap was increased, and no universal settling claim is made. All76 requests for
both settings on the38saved genuine observations build offline within the size
cap; this is not a new genuine model evaluation.

## Independent review and remaining limits

The actual `competitive-rule-change` skill was explicitly invoked in session
`01a1b6ef-6f18-72c2-9249-e06f0ee80045`. Applicable F2/F3/F8 map/spec entries cover
public candidate proposals and the waiting-only setting. Seven focused tests
passed independently after the cap fix. Read-only reviewer
`/root/geometry_review` reported no remaining findings, confirmed the token/
origin/concurrency/accounting guards, passed the UI check and18freeze checks,
and independently replayed both2x/1x browser-switch traces. No student gate was
approved by an agent.

2x retains the observed scratch tradeoff and can trigger powered cascades; future
simulation-limit failures remain possible. The model still decides among listed
candidates. No new genuine LLM match outcomes or win-rate measurements exist.
Final complete-suite and preservation results are recorded in validation files.


Final validation: **206 Python tests passed** in321.913seconds, returncode0;
all six JavaScript checks passed; all24official historical replay verifications
passed; all18frozen artifacts passed. Of1,098previously present project files,
only the listed authorized current source/test/document files changed; zero
historical evidence or unexpected paths changed. All93checked local Markdown
links resolve. Credential-pattern scan found no matches. Independent review is
recorded [here](INDEPENDENT-REVIEW.md); [final validation](VALIDATION.json),
[Python log](python-tests-final.txt), [JavaScript checks](javascript-checks.json),
[historical replays](historical-replays.json) and [preservation](preservation-result.json)
contain the actual results. No paid calls, commits, pushes, PR or submission.
