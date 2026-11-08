# Live browser mode preparation — 2026-11-07

Implementation/testing used only mocked responses. No real paid model requests,
live-evaluation reruns,push,PR modifications or submissions occurred.

New separate launcher `fusion.live_demo` wraps the existing game entry page
with an additional Start Live LLM Agent link. The old Watch link and recorded
server use unchanged original files. No frozen engine,scoring,physics,observation,
baseline,prompt-v2 strategy or recorded-replay assets were edited. Runtime live
controls are new assets in fusion/live_web,using the original frozen renderer.

## Actual verification

- Test-first live module contract initially failed import before implementation.
- Initial full mocked-session test exposed a real playback-ack race:after an
  accepted ACK,the old packet was still available in playback phase; immediate
  polling tried to acknowledge it twice. The test raised "Shot already
  acknowledged" and cleanup encountered a still-running worker. Fixed by
  entering advancing phase atomically with ACK. Full mocked match then passed.
- Final10live-mode tests passed37.097s. They exercise all12autonomous turns,
  sixsynthetic model requests,frozen-engine frame generation and exact replay;
  declined/missing confirmation; paid-disabled even with fixture credentials;
  origin/token/manual-action rejection; providerHTTP429failure without retry;
  cancellation before reservation,during request and during physics; missing
  playback ACK timeout; strict6call/$0.25estimated ledger refusal.
- Full project suite: **162tests passed in193.897s**.
- Actual new JavaScript parsed and tests/live-demo-controller.cjs assertions
  passed via existing Node runtime:declined native confirmation dispatches0,
  confirmed scope dispatches once,cancelled delayed packet cannot animate.
  This is controller testing,not a visually observed browser session.
- PowerShell launcher parser passed. Actual `py` interpreter probes matched
  `C:\Users\lzy21\AppData\Local\Python\pythoncore-3.15-64\python.exe`.
  Exact freeze/mock-server stages launched with that interpreter. The masked
  paid-launch branch was not executed; no key was requested/entered by agent.
  Managed shell Restricted policy prevents script-file execution,so no claim
  that the full .ps1 file ran or that policy was altered.
- Actual mocked server started at8805/8807/8809. Loopback HTTP confirmed both
  Watch LLM Agent Play and Start Live LLM Agent in entry HTML; live state showed
  mockedtrue andcalls0. No GUI observation or genuine API success was claimed.
- Freeze check passed all18artifacts repeatedly. Protected hashes matched the
  preexisting prompt-v2 pilot preflight snapshot:original game,baseline,prompt,
  original evaluations and current recorded demo remain unchanged.

## Independent read-only review

Reviewer:`/root/live_demo_review`,separate context,no source edits,API/network/
GUI calls or student gate approval. Three cancellation races found:

1. A delayed packet response could restart preview after Cancel. Added a
   generation/liveStopped check after awaiting the packet.
2. Cancellation between loop check and API selection could still reserve.
   Added the cancel predicate at MatchLedger.reserve before counting/dispatch.
   Already-reserved requests are explicitly considered in flight.
3. Cancellation during physics could lose its wake when packet construction
   cleared the playback event. Cancel re-signals under the acquired state lock.

Reviewer verified fixes,ran the3cancellation tests independently (passed1.203s),
ran the actual JavaScript confirmation/cancel assertions and checked freeze18.
Reviewed masked launcher defaults,exclusiveMock/EnablePaid options,interpreter
checks and finally restoration of the previous environment. No blocking residual
issue was reported in documented paths. Manual browser walkthrough remains in
LIVE-LLM-DEMO.md; automated checks are not human playtest or video evidence.

## Ready but not paid-tested

Real mode uses existing improved mini adapter. It requires local paid-enable
flag,server-only API credentials,and explicit browser confirmation for a single
match of at most6requests/$0.25estimated. Default and Mock cannot make paid
calls. One server session cannot reset caps on refresh,repeatedstart or another
tab. No automatic retries,output repairs or model-to-baseline fallback.

Cancellation blocks further dispatch and discards unexecuted replies. Existing
in-flight calls may still incur cost and finish within the request watchdog.
Known usage or unknown reservations are retained. Partial cancellation has
session status,not an invented competitive result or altered frozen rules.

Future real or mocked run artifacts are stored separately in
evidence/live-browser-v2/<UTC-id>/. Mock data is explicitly labelled and never
counts as real inference,live performance,official evaluation or human feedback.
The original working recorded demo remains available unchanged through the
new entry point and through its older launcher.
