# Prompt-v2 offline verification — 2026-11-07

Separate post-official experiment; no new live model calls,paid spending,push
or PR. Policy variant `kinetic-prompt-v2-risk-aware`; final prompt SHA256
`c005b4ae1524b78020dbbfc817371c29d26e67660c6c124c9a1a03bc1b530db7`.
Original prompt SHA256 remains
`4063d80aee264642d48559e550428f013b32e6825d683496f6357bf7d1f56a16`.

Actual development checks:

- Test-first6newcontracts initially failed import before prompt_v2.py existed.
  First implementation then passed6tests in1.503s.
- Full project run: **142tests passed in143.686s**. This full run was started
  before the reviewer's one-word clarification of "pots" to "pot points".
- Final corrected-prompt focused run: **6tests passed in1.815s**.
- `py -m fusion.prompt_v2 --offline-match evidence/prompt-v2-development-02`:
  full synthetic match and replay passed. The adapter returns synthetic0/1
  proposals; saved trace/audit are labelled OFFLINE/nonlive. These are not
  model decisions,quality results or real token/cost measurements.
- Request comparison changes only input[0].content. Exact same public context,
  empty history,schema,model/settings and parser. No candidate generator or
  simulator is supplied. The original unchanged rule facts remain in the prompt.
- Valid proposal passes authoritative step/replay; illegal proposal is rejected
  while preserving synthetic usage. Missing approval refuses before reservation.
  V2 prompt ID/hash are correct in the request,returned metadata and durable
  journal when using the documented .select or runner policy.ledger entrypoints.
- Frozen18artifacts passed repeatedly. Final protected_snapshot equals the saved
  verification snapshot:official code,prompt,baseline,game/visual freeze,
  recorded viewer and originalfailed/smoke/recovery evidence,reports,README and
  agent-config unchanged. No official evaluation/replay was replaced.

Independent read-only reviewer:`/root/prompt_v2_review`. Reviewer ran6tests
(1.768s),freeze18 and independently recomputed diagnosis:66shots,25scratches,
44of80physicalpots on foul shots,medianpower84,61preceding-opponent feedback,
no own-shot history. Only prompt content changes; math is grounded and labelled
approximate. Reviewer suggested changing "erases ALL pots" to "ALL pot points"
because pocketed balls remain removed; implemented and rechecked above.
Reviewer noted raw legacy call_model with an explicitly raw ledger bypasses
variant tagging; documented direct entry is .select,while runner attaches
policy.ledger. No shared official helper edits,network calls or gate approval.

Initial development01 fixture is retained with its earlier prompt hash;
its diagnosis.json reads authentic official data. It is not a paid trial.

Performance statement: **unmeasured**. The actual original result remains
2wins/9losses/oneproviderfailure. Because these original traces informed v2,
fresh held-out cases are required for a new held-out claim. No new cases were
silently substituted or altered. New real comparison needs explicit separate
model/call/cost approval. Physics-assisted hybrid was explained in
IMPROVED-AGENT.md and not implemented.
