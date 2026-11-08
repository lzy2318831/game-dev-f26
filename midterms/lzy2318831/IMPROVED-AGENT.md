# Separate prompt-v2 development experiment

Variant:`kinetic-prompt-v2-risk-aware`, pinned model
`gpt-5.4-mini-2026-03-17`. **No live v2 calls or measured v2 strength results.**
The official2wins/9losses/oneproviderfailure, official prompt, frozen game,
Geometric baseline, Smart, original reports/traces and recorded demo stay
unchanged. The Watch button continues showing the original authentic match.

## Diagnosis from actual traces

Read-only inspection of all66successful official decisions:

| Observed fact | Implication or hypothesis |
| --- | --- |
| 25scratches/66shots;44of80physical object pots occurred on scratched shots | Preventing cue scratches is a concrete target:those shots retained0points. A scratch voids awards,not removal of the pocketed objects. |
| Mean power76.80,median84;35shots>=80;power86chosen18times;range10–94 | Power often implies several table lengths of unimpeded travel. This suggests testing distance-calibrated energy,not proof high power alone caused losses. |
| 32zero-point shots | Not every zero was a scratch; speculative routes can also fail to earn points. |
| All66requests had empty history;61had preceding opponent last_shot,0had own last_shot;5opening shots had none | Prompt-only revision cannot remember its own previous action. Check last_shot.player and current geometry; do not invent feedback. |
| 30requests had32visible last_events | Event suffix is bounded. Missing events are not evidence a device was never hit. |
| Original prompt names ghost-ball/bank/combination aiming but supplies no procedure | Explicit geometry,power and risk instructions are a plausible improvement,not a measured explanation of the model's hidden reasoning. |

Concrete saved example:`observation_only-direct-102-p1`,match shot3,
angle241/power73:pockets7objects but scratches and scores0. Another:
direct102p2,shot10,angle288/power78,pockets7objects but scores0. These are
observations from original saved traces,not replayed replacement decisions.
Full per-shot facts:[diagnosis.json](evidence/prompt-v2-development-01/diagnosis.json).
Scoring reference:[RULES.md F2–F6](RULES.md); observation source:
`fusion/engine.py:Episode.observe`, `fusion/player.py:build_context`;
official prompt/request:`fusion/llm.py:SYSTEM/ModelPlayer.request`.

At power86,speed702 and unimpeded stopping distance702²/140≈3520table units.
This is a friction-only illustration,not a simulated trajectory:collisions
remove energy and powered devices add it. We did not simulate alternative
official shots or fit preferred actions to those cases.

## The sole policy change

`fusion/prompt_v2.py:GUIDANCE` prepends a compact decision checklist to the
unchanged original game facts:

- Identify clear object/pocket pairs; use ghost center O−22*unit(P−O), cut
  alignment and collision clearances rather than aiming directly at a ball.
- Convert atan2(dy,dx) to clockwise degrees:0right,90down,180left,270up.
- Estimate speed from distance/friction and cut energy; choose enough power
  without a fixed high default. The approximation does not predict mechanisms.
  No new power restriction or action clamping is added.
- Compare100point pots with safe distinct cue-device awards. Object-device
  contacts redirect without device scores. Repeated-body farming and Orbit
  multiplier scope are explicit; examine powered exits,not just their entries.
- Discount scratch exposure and uncertain chains; adjust risk for score gap
  and remaining turns. Qualitative estimates are not oracle probabilities.
- Use only actually supplied last_shot/last_events, attributed to the correct
  player. Refilled IDs do not provide persistent ball histories.

The request differs **only at `input[0].content`**. Observations, event
truncation, empty history, model, `reasoning.effort=none`, output-token limit,
tools=[], strict JSON schema, transport, parser and authoritative step are
unchanged. No external candidate generator, simulator or baseline move is
provided to the model. No chain-of-thought output or explanation is requested.
Policy quality is unproven until an approved real-model comparison.

OpenAI Docs guidance for mini recommends explicit steps,decision rules and
action/output definitions. This supports the structure choice,not a claim
that it will win. Sources fetched2026-11-07:
[mini-specific guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.4),
[exact mini snapshot/settings](https://developers.openai.com/api/docs/models/gpt-5.4-mini).
No model migration or reasoning-effort increase was implemented.

## Integration and audit isolation

`ImprovedModelPlayer` is separate from the original `ModelPlayer`. Direct
callers must use **`.select(...)`**, which preserves existing approval,
watchdog,budget,no-retry and validation handling. For the existing runner,
assign a fresh ledger through **`policy.ledger = Ledger(...)`**, then use the
distinct `prompt_v2` seat label. Never monkeypatch the official evaluator or
reuse its output directory/budget.

The legacy shared helper labels results with the original static prompt hash.
`VariantLedger` corrects that label before the result is durably written and
adds the variant ID and original prompt hash. It forwards the same reservations
and cost/call accounting. The actual request hash covers the actual new prompt.
**Do not call legacy `fusion.llm.call_model(v2,...,ledger=rawLedger)` directly:**
that bypasses the v2 wrapper and mislabels audit metadata. `.select` wraps an
explicit ledger safely; runner use is tested with `policy.ledger` attached.
Original helper/source bytes are preserved rather than retroactively changed.

No v2 live CLI or UI mode is enabled. The existing official recorded replay
is not replaced. The CLI below is network-free even when credentials exist.

Working directory:`midterms/lzy2318831/`:

```powershell
py -m fusion.prompt_v2
py -m unittest discover -s tests -p test_prompt_v2.py -v
py -m fusion.prompt_v2 --offline-match evidence/my-prompt-v2-offline-check
py -m fusion.freeze
```

The last new-match directory must not already exist. That match uses a clearly
labelled synthetic provider returning angle0/power1; it verifies parsing,
legal execution, full termination, traces and audit accounting, **not model
intelligence**. No fixture score may be reported as v2 live performance.
Final corrected-prompt evidence:
[plan](evidence/prompt-v2-development-02/plan.json),
[offline verification](evidence/prompt-v2-development-02/verification.json),
[test/review report](evidence/prompt-v2-development-02/REPORT.md).
Development01 retains the initial offline run before a reviewer clarified
"pot points" wording; it is not another paid evaluation.

## Fair future evaluation

These official cases were inspected to diagnose v2. They remain valid original
v1held-out results, but are now retrospective development cases for v2. Do not
claim a new v2result on them is an untouched held-out test. Freeze the v2prompt,
declare fresh held-out layouts/seeds before further tuning,then request a
separate provider/call/cost approval. Match seats and observations against the
unchanged Geometric baseline,report failures/scratches/retained scores,usage,
latency and cost under a separate output/variant. A legacy-case exploratory
comparison must be labelled as such. No new scenarios or original declarations
were altered in this task. Existing evaluation headroom is not new approval.

## Physics-assisted alternative — explained, not implemented

It could help with collision-rich routes because it can reject simulated
scratches and inspect actual device chains rather than relying on language
geometry. A separate hybrid could generate a small diverse set from the public
state, evaluate it with bounded counterfactual runs of the same deterministic
engine,then let the real LLM choose/refine a legal action. Disclose simulator
access,work/call budgets and all candidate information; no live Episode,hidden
state or evaluator answer keys should be given to the policy. All policies
still execute through the five-operation interface.

This would be a **hybrid simulator-assisted LLM**,not prompt-only v2 or the
original baseline. If code chooses the winning action and the LLM merely echoes
it,that is not credible evidence of meaningful model decision-making. To retain
a model-driven role,the LLM must make a substantive recorded final choice.
The simulator is an additional computational capability,so compare/report that
arm separately and explain its fairness implications; staff ultimately assess
the rubric. An LLM-propose/simulate/LLM-select loop could require more than one
paid call per turn and needs its own explicit approval. The course submission
does not need to risk that complexity before this prompt-only test.
