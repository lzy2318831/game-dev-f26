# Prepared separate prompt-v2 pilot — live execution not yet approved

This pilot does not replace the original official evaluation or the current
Watch LLM Agent Play demo. Frozen gameplay,physics,scoring,observations,original
prompt-v2 strategy,Geometric baseline and original result files are unchanged.
No live request was made during preparation.

Declaration:[fusion/prompt-v2-pilot.json](fusion/prompt-v2-pilot.json).

| Trial | Fresh seed | LLM seat | Opponent | LLM opportunities |
| --- | ---: | --- | --- | ---: |
| prompt-v2-seed-2701101-p1 | 2701101 | P1 | original Geometric | 6 |
| prompt-v2-seed-2701102-p2 | 2701102 | P2 | original Geometric | 6 |
| prompt-v2-seed-2701103-p1 | 2701103 | P1 | original Geometric | 6 |

Before declaration,a whole-project `rg -n '270110[123]' midterms/lzy2318831`
returned no matches. Offline fixture validation then uses these seeds,with no
paid calls. The frozen engine records a seed but does not randomize its rack:
these are repeated trials of the same standard15-ball opening,not three fresh
physical layouts. Seats are P1/P2/P1,not perfectly balanced. Model sampling can
vary. This small pilot can describe v2 versus Geometric,not establish a causal
improvement over v1's different official scenarios. A matched v1/v2 experiment
would need separate approval and more calls; it is not silently included here.

Same pinned model `gpt-5.4-mini-2026-03-17`,same observation-only context,
reasoning effort `none`,strict angle0..359/power1..100 JSON,512output-token cap,
tools=[],storefalse and default service tier. No Smart substitution,simulator
or fixture in live mode. Each match follows the frozen six-shot-per-player
loop; early clearance,failure or budget exhaustion may prevent six successful
LLM shots. No padding,replacement action,extra turn or extra request is added.

## Limits and evidence

One shared ledger:maximum18reserved API attempts across all three matches and
$0.25 locally estimated committed/reserved cost. Reservation occurs before
dispatch. Known usage reconciles it; failed/unanswered requests keep unknown
cost reservations. No automatic retries. Any match failure or interruption
stops later trials as not-run. Request20s and match300s deadlines remain.
Estimated cost at5000input+512output per call is$0.108972 for18calls using the
saved dated rates. Actual usage varies; the local ceiling is an estimate and
not a provider-invoice guarantee. Budget refusal may end the pilot early.

Live output is fixed to `evidence/live-prompt-v2-pilot-01/`. Creation is atomic,
and any existing directory is refused. This prevents concurrent/double runs
or a new --output resetting allowances. Do not delete/rename evidence to retry.
An interrupted pilot needs review before any further live execution.

Saved files:

- `manifest.json`:declared protocol,configuration/prompt/source hashes,statuses.
- `calls.jsonl`:durable actual request/result journal,usage,latency,cost,failures.
- `<trial>.steps.jsonl`:accepted authoritative actions and states committed as
  they happen,including partial interrupted matches.
- `<trial>.json`:full returned trace,whether successful or failed; offline replay
  checks its events,state fingerprints and final outcome.
- `comparison.csv` and `summary.json`:actual actions are in traces;summaries
  include scores,result,scratches,both players'illegal actions,invalid proposals,
  calls,tokens,latency,costs,unknowns and failures. Interrupted usage comes from
  the journal even if no completed match trace exists; no final score is invented.
- `preservation.json`:original official evidence/game/demo SHA256 preservation.

## Offline launch and later approved execution

Working directory:`midterms/lzy2318831/`. Windows PowerShell:

```powershell
Set-Location C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831
.\run-prompt-v2-evaluation.ps1 -Offline
```

Without flags it is also offline. It resolves the working `py` application once,
verifies the frozen18artifacts and runs the entire three-match fixture workflow,
including visual-frame compatibility. Strict ledger/no-retry unit tests are
run separately; the script does not silently invoke the unittest suite.
Interpreter probes before/after confirm the same Python for all commands.
Offline artifacts are labelled fixtures and cannot be opened as genuine LLM
replays. Content-addressed proof is preserved under
`evidence/prompt-v2-pilot-preflight/<configuration-hash>/`; unchanged proof is
hash-validated on repeat use. Code/configuration changes require new proof.

**Only after the student separately approves live execution**, run:

```powershell
.\run-prompt-v2-evaluation.ps1 -ApproveLive
```

This repeats the offline guard,then prompts for the API key with masked input.
Key stays in the process environment,never in browser code,prompts or files;
the previous environment value is restored in finally. Do not paste a key into
chat or put it in a command argument. No additional original evaluation,smoke,
live demo or PR command is chained. The flag is an explicit local execution
confirmation; preparation has not recorded that approval.

The managed preparation shell has Restricted execution policy:PowerShell syntax
can be checked,but running the `.ps1` file is blocked. The exact Python stages
are verified independently with `py`; no execution-policy bypass is used.
If your own terminal blocks scripts too,stop and report it rather than changing
security policy as part of this evaluation.

## Replay the best genuine completed v2 match

After approved execution finishes:

```powershell
py -m fusion.prompt_v2_pilot_replay --port 8791
```

Open `http://127.0.0.1:8791/#autoplay`. Both players'actual recorded decisions
play automatically with angle/power,ball motion,devices,score and final outcome.
Play,Pause-after-shot and Restart use the existing renderer. It is clearly a
Recorded LLM Evaluation,with the `prompt-v2-...` trial ID visible; not live
inference or the original official match. No API calls are made for replay.

"Best" is declared now:highest LLM-minus-Geometric score margin,then highest
LLM score,then fewer cue scratches,then declaration order. Only genuine
completed,nonfailed matches qualify. Each model action must match a saved live
HTTP200 request/result,model/variant/prompt hashes,and the actual authoritative
trace; no fixture or generated replacement action is accepted. If none finish,
the viewer refuses rather than inventing a demonstration. Selecting one match
for presentation is not the three-match performance estimate; report all rows.

Preparation details:[evidence/prompt-v2-pilot-preparation/REPORT.md](evidence/prompt-v2-pilot-preparation/REPORT.md).
The original official demo command remains `py -m fusion.demo` at8785/8787.
No PR changes,push or submission are made by this launcher.
