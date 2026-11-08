# Approved eleven-trial continuation

The student approved continuing the eleven previously not-run trials with
`gpt-5.4-mini-2026-03-17`, observation-only memory and the original Geometric
baseline. Smart AI is not used. Gameplay, scenarios and presentation stay frozen.

Run in Windows PowerShell:

```powershell
Set-Location C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831
.\run-recovery-evaluation.ps1 -Offline
.\run-recovery-evaluation.ps1
```

The second command prompts for a masked API key, supplies it only through the
process environment, and restores the previous environment value on exit. Never
paste the key into chat or a command argument. Both stages resolve the same `py`
launcher and check `sys.executable`; freeze verification remains mandatory.

## Scope and combined accounting

Preserve `evidence/live-mini-approved-01` (one HTTP429 failure, eleven not-run)
and `evidence/api-smoke-mini-01` (HTTP200, valid345/72, 2132 input +24 output
tokens, estimated $0.001707). The original provider body was unavailable;
HTTP429 alone does not prove which quota/billing condition occurred.

These are two prior attempts. The continuation can make at most70 additional
requests; eleven full matches need at most66 (six model shots each). The old
unknown-cost reservation $0.0109875 stays charged against the local estimate.
The remainder of the original $5 cap is at most $4.9873055, rounded downward
to twelve decimal places. Reservations happen before network dispatch; known
usage reconciles them and unknown usage retains the reservation. Local estimates
are not a provider billing guarantee. No retries or policy fallback are enabled.

Only `evidence/live-mini-recovery-01` is allowed for live continuation. Changing
the output directory cannot create another live budget. A process lock prevents
concurrent invocations. Do not delete or rename that directory to reset limits.

## Resume and interruption

Run the same command again after a clean interruption. Completed/failed trials
are skipped. Committed steps replay through the unchanged engine. A durable
successful model response not yet executed is reused only when its public
request hash and legal action match. No new API request is needed for that shot.
An unanswered request, malformed journal, changed configuration, or provider/
budget hold stops for inspection instead of automatically resending a request.
Do not remove a hold or edit journals; obtain review of the saved evidence.

New requests/results and steps are append-only JSONL; trial/control traces and
the recovery manifest are checkpointed. The combined-report directory is a
derived view: twelve official trial rows retain the original failure and replace
only the eleven not-run rows. The smoke is separately accounted, not a scored
match. CSV and JSON report scores, invalid actions/proposals, failures, latency,
usage, estimated costs and matched Geometric controls. Unknown usage remains
explicit. Existing evidence folders are hashed and checked unchanged.

## Verification and remaining work

Preparation is offline; fixture tests do not establish LLM performance. This
agent process has no API credential. Actual continuation scores and costs must
come from the student's masked local launch and its saved reports.

After the run: inspect failures and replay traces; write the measured evaluation
interpretation; verify remote CI when a push is authorized; supply genuine human
playtest notes, two independent reusable-skill session references, student
reflection and the 3–5 minute recording; finalize README/EVALUATION/AGENT-TEAM
and the draft PR. Independent review of recovery tooling is development evidence,
not student gate approval. No final PR is pushed or submitted by this command.
