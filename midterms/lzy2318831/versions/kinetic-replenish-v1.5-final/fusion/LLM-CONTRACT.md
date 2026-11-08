# LLM integration contract (2026-11-07, before implementation)
Frozen gameplay/visual/interface files remain byte-identical. New player uses
only frozen build_context public observation/legal_actions/history; no tools,
files,simulator,evaluator labels or credentials in provider payload. Static
prompt explains current rules. Exact JSON angle0..359/power1..100, no repair,
clamping,retry or baseline fallback. Malformed/refused/incomplete/illegal outputs
fail episode explicitly and preserve usage when available. Engine revalidates.

OpenAI Responses HTTPS adapter, environment key only, no redirects/retries,
storefalse/toolsnone. No API call without explicit CLIapproval/provider/model/
runbudget. Offline fixtures always marked nonlive. Parent watchdog stops hung
worker; failed/timeout calls count and reserve unknown costs conservatively.
Append-only audit logs before dispatch; never log credentials/error bodies.
Requests,model/prompt/config/game hashes,usage,cost rates,latencies,failures,
actual actions/outcomes and replay hashes recorded. Interrupted trials retained.

Frozen suite6 unchanged. Default12live matches (3cases*2seeds*2seats),6modelshots
maxeach=72calls, paired same-layout baselinecontrols. Optional bothmemory
conditions doubles to144calls, optionalSmart opponent separate. Seeds control
game,not stochastic model replies. Offline dryrun does not claim live evidence.
