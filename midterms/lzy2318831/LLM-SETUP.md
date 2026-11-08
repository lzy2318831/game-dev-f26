# Current recovery hold
Official firstattempt failedHTTP429. Exactproviderbody wasnotpreserved by the
oldhandler; fixed sanitizeddiagnostics now. Do NOTrerun commands below yet.
See evidence/http429-diagnosis/DIAGNOSIS.md. Originalattempt1counts toward72;
remaining71 and$4.9890125conservative localbudget. Userrequests cause/recovery
report before anynewpaidcall; continuationawaits explicitauthorization.

# Current approval status
The user has now approved the exact pinnedMini observation-only12match/12control,
72call,$5scope below. No further budget confirmation needed. Credential checks
found no configured key; no live calls made. Use run-approved-evaluation.ps1
for a masked session-only local launch,or configure access for the agent.
Never paste the key in chat. Preserve official output directory across failures.

# Real LLM player: configuration and approval

Implementation ready for approved live validation; NO LIVE CALLS RUN.
The frozen game/visual18hashes remain unchanged. No new UI mode or gameplay.
LLM runs headlessly through actual reset/observe/legal_actions/step/outcome.
OpenAI is the implemented provider. Geometric is the official baseline; Smart
is a separate simulator-based opponent, never substituted for LLM results.

## Model options and dated estimates

Official documentation checked2026-11-07:
- GPT-6 Luna (gpt-6-luna):$0.10input/$0.50output per1Mtokens.
- GPT-5.4 mini pinned gpt-5.4-mini-2026-03-17:$0.75/$4.50per1Mtokens.
- GPT-6.1 Sol (gpt-6.1-sol):$2/$10per1Mtokens.
- Also supported pinned gpt-5.4-2026-03-05:$2.50/$15per1Mtokens.
The inexpensive nano page is markeddeprecated, so it is not offered here.
Availability/account/model access have NOT been tested live. Pinned Mini is a
reasonable reproducible first choice; no game-performance superiority claimed.

Sources: [standard pricing](https://developers.openai.com/api/docs/pricing),
[Mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini),
[Luna](https://developers.openai.com/api/docs/models/gpt-6-luna),
[Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol),
[structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs).
Prices are dated,not immutable. Standard tier explicitly requested. Estimates
ignore cache discounts,tax and any account-specific charges,not billing promises.

Default proposed suite:3situations*2seeds*2modelseats=12live matches, plus12
matched Geometric controls; max6LLMshots/match=72requests. At5000inputtokens and
full512outputtokens/request: Luna~$0.054,Mini~$0.436,Sol~$1.089,5.4~$1.453.
Both history conditions doubles these calls/estimates to144. Actual input varies;
output cap includes billed reasoning/output; reasoningeffortnone requested.
A proposed$5run budget for Mini leaves headroom. Local budget reserves a
conservative input-byte allowance+4096framingtokens plus512outputs before
sending,counts failures,keeps uncertain timeout reservations. It is an estimated
local limit,not a provider-side hard billing cap. Also configure provider project
budget alerts. No retry,fallback or approval implied by credentials alone.

## Secure credentials (local only, before recording)

No SDK installation needed,Python3.11+ stdlib HTTPS. Create/use an API project
with access to the selected model. In a local PowerShell session:

```powershell
Set-Location 'C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831'
$apiSecret = Read-Host 'OpenAI API key' -AsSecureString
$env:OPENAI_API_KEY = [System.Net.NetworkCredential]::new('', $apiSecret).Password
Remove-Variable apiSecret
```

Do not paste the key into chat,git,agent-config,prompts,recordings or files.
The key is read only by the HTTPS transport,never sent in the model context
or audit payload. Raw HTTP error bodies/arbitrary exception text are not logged; sanitized provider error fields are retained. No credential
redirects. Session-only environment; remove afterward:
`Remove-Item Env:OPENAI_API_KEY`. Never print the environment key on screen.

## Inspect plan now (FREE; no network/provider call)

```powershell
py -m fusion.llm_eval --model gpt-5.4-mini-2026-03-17 --memory observation_only
py -m fusion.freeze
```

Plan includes exact public layouts,seeds,seats,protocol/prompt/code/game hashes,
proposed rates and call count. Existing frozen suite6 is unchanged.

## Only AFTER explicit user approval

Proposed approval:OpenAI,pinnedMini,observation_only,Geometric opponent,
12live matches+12controls,max72calls,localbudget$5. The following command is
prepared,NOT executed by the assistant:

```powershell
py -m fusion.llm_eval --live --approve-paid --provider openai --model gpt-5.4-mini-2026-03-17 --memory observation_only --opponent baseline --budget-usd 5 --max-calls 72 --output evidence/live-mini-approved-01
```

Output directory must be new; existing evidence is never overwritten. Both
memory conditions require a separate explicit approval for144calls. Optional
Smart-opponent trials are separate additional paid trials and approvals.
Missing approval/provider/model/budget/output/key refuses live use. Model
access/schema/rate/latency behavior still requires first approved validation;
configuration HTTPerrors stop remaining suite rather than repeatedly spending.

## Logs, failure handling and replay

Each request receives only canonical public build_context data:state/legal
schema,plus0or2visible recent shots(max2000chars). Last_events capped to32;
no hidden case labels/seeds/evaluator instructions,repository or simulator tools.
Strict schema angle0..359/power1..100; engine revalidates. Malformed,duplicate
keys,refusal,incomplete or illegal responses fail explicitly,without repair,
clamping,automatic retry or baseline fallback. Invalid proposal count is distinct
from engine-invalid-actions (invalid proposals blocked before step).

calls.jsonl journals requests before dispatch and result metadata afterward:
provider/requested+returned model,request/responseID/hash,prompt,usage,latency,
dated rates,estimatedcost,unknowncosts,failure and legal action. No API headers.
Each trial has atomic manifest status,persistent *.steps.jsonl and replayable
trace. comparison.csv/summary.json retain failed,interrupted and not-run rows,
both scores,outcome,illegalproposals,pocket events,tokens/unknownusage,cost and
matched control metrics. A parent process watchdog enforces20sec/request;
12modelattempts/300sec episode,12gameopportunities. Timeouts may still bill:
usage/cost remainunknown and reservation kept,not falselyzero. Failed calls
count; no fixture substituted. Game seeds do not make provider replies
reproducible; recorded actions replay deterministically without another API call.

```powershell
py -m fusion.llm_eval --summarize evidence/live-mini-approved-01
py -m fusion.runner --replay evidence/live-mini-approved-01/observation_only-direct-101-p1.json
```

For interrupted runs,manifest statusrunning is reported asinterrupted; pending
rows staynotrun. Audit/committed-step logs remain inspectable. No automatic
resume/retry; reconcile provider unknown usage before approving another run.

## Recording without further paid calls

Record the approved evaluation's printed LLM actions/scores while it runs,
with credentials already configured offscreen. Show frozen playable game and
public interface,actual autonomous choices,results/failures,limits. Or clearly
label playback of an approved recorded trace as replay. Do not stage manual
moves as model decisions or imply offline smoke fixture is a real model.

Windows launcher now uses py for both stages and checks matching sys.executable.
Run .\run-approved-evaluation.ps1 -Offline to verify without paidcalls.
