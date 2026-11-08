# Genuine live prompt-v2 browser mode

The new launcher has two distinct buttons: **Watch LLM Agent Play** opens the
unchanged authentic recorded evaluation; **Start Live LLM Agent** opens a
separate local live page. The original `fusion.demo` launcher/replay files,
original evaluation,prompt-v2 strategy,Geometric baseline and18frozen artifacts
are unchanged. Only new controller/backend/launcher/test/document files are added.

The live backend uses `ImprovedModelPlayer.select` and the existing HTTPS
adapter. It reads only `observe(player)` and `legal_actions(player)`,submits
the actual returned angle/power through `step`,then sends frozen-engine frames
to the existing renderer. P1 is the model,P2 is the original Geometric policy.
Both act autonomously. No recorded/evaluation actions or Smart fallback are used.

## Safe offline browser verification

Windows PowerShell,working directory `midterms/lzy2318831/`:

```powershell
Set-Location C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831
py -m fusion.live_demo --mock
```

This uses synthetic provider replies **even if a real key exists**. No paid
requests. Open `http://127.0.0.1:8805`:

1. Verify both buttons exist on the welcome screen and game page. Watch still
   redirects to the original recorded match at8807. Recorded and live controllers
   are separate; switching pages does not relabel recordings as live inference.
2. Click **Start Live LLM Agent**. It opens8809 and clearly says
   **MOCKED API TEST — NOT REAL LLM INFERENCE**. The model identifier names the
   intended real policy,but these test decisions are synthetic0°/power1,not
   evidence of model strength. Only the model seat is mocked; Geometric still
   computes its own actions.
3. Click the confirmation/start button,then **Cancel** the browser confirmation
   dialog. Requests must remain0. No match begins.
4. Confirm the mocked match. Observe automatic P1/P2 turns,selected angle/power,
   motion,device effects,scores and a final outcome. No aiming/dragging is needed
   or accepted. Thinking status may be brief with synthetic replies.
5. Refresh midway. The same backend match/budget is retained; it cannot start
   another match. Finishing playback acknowledges that shot before the next
   turn can begin. A refresh can replay the current packet without executing
   another engine step or another model request.
6. On another backend launch,test **Cancel live match** while thinking or while
   moving. No new requests may be reserved after cancellation. A returned but
   unused model proposal is discarded; current physics already in progress may
   finish and remains truthfully logged. No incomplete competitive winner is
   invented. Cancelled state and last committed scores are visible.
7. Stop the server withCtrl+C. To verify the default lock,run
   `py -m fusion.live_demo` without flags:live confirmation is disabled even
   when a credential exists. Existing human modes and recorded viewing work.

Optional script equivalents:

```powershell
.\run-live-llm-demo.ps1 -Mock
.\run-live-llm-demo.ps1
```

Browser visual checks must be performed/recorded by an actual observer; Python
and JavaScript tests are not human playtest notes. Preparation verified mocked
backend/HTTP/controller behavior,not real-model performance or a watched video.

## Real execution — only after separate approval

No real paid requests were made during implementation. After the student
separately approves live execution,run:

```powershell
Set-Location C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831
.\run-live-llm-demo.ps1 -EnablePaid
```

The script verifies freeze and the same `py` interpreter,then securely prompts
for a masked API key. It supplies the key only to the Python process environment
and restores the previous environment on exit. No key in browser JavaScript,
URLs,prompts,trace artifacts or repository files. Never paste it into chat.

Open `http://127.0.0.1:8805`,click **Start Live LLM Agent**,then read the live
confirmation. **Explicitly confirming authorizes one whole bounded match:**
up to6actual requests and$0.25locally estimated cost,no retries. It does not
authorize unlimited matches. Merely enabling the backend,opening the page,
reading state or cancelling the dialog makes no API request. No automatic
confirmation or call from a URL/autoplay fragment is implemented.

The real banner says **LIVE LLM AGENT**,not Recorded or Mocked. It shows
`kinetic-prompt-v2-risk-aware`,GPT-5.4mini,thinking/turn status,actual selected
angle/power,scores,request counter,known estimated spend and unknown-cost
reservations. Actual API/model account availability has not been retested here;
errors stop rather than falling back. Current model/settings are unchanged:
`gpt-5.4-mini-2026-03-17`,observation-only,reasoningnone,512output-token cap,
strict JSON,no tools. No extra reasoning/history/model change was introduced.

This managed environment has Restricted PowerShell execution policy; script
syntax and its exact `py` mocked command stages were checked separately. No
policy was changed. If your terminal blocks `.ps1` execution,report that error;
do not use an execution-policy bypass as part of these instructions.

## Bounds,cancellation and saved evidence

One match per backend launch,including all browser tabs. Duplicate starts and
refresh cannot reset the ledger. A new match requires stopping/relaunching the
backend and fresh browser confirmation. Never use relaunches as an automatic
retry loop; failure evidence and any further spending require review.

The shared ledger reserves before dispatch,limits6requests/$0.25estimated,
reconciles known usage and retains unknown reservations. No API retries,output
repair or baseline replacement for model decisions. Estimated cost is not a
provider-invoice guarantee. Failures/illegal proposals/cost refusal stop the
session. Request timeout20s; total session600s including playback; missing
playback acknowledgment60s stops with an explicit timeout. Core match still has
six alternating opportunities/player and unchanged early-ending/physics limits.

Cancel blocks new dispatch and signals playback waits. An already reserved or
sent request may still incur charges; its bounded in-flight call can take up
to20s plus process cleanup to finish. Its result/usage or unknown reservation
is preserved,and no unexecuted action is applied. Closing a tab is not a
guaranteed immediate cancel; use Cancel first. Without acknowledgments,the
backend stops at the timeout instead of running unattended further turns.

Artifacts are separate under `evidence/live-browser-v2/<UTC-and-random-id>/`:

- `calls.jsonl`:actual requests/results,usage,latency,estimated costs,failures.
- `steps.jsonl`:durable authoritative executed actions/events/state fingerprints.
- `trace.json`:engine-replayable full or partial trace,variant/model,consent
  scope,limits,run status,termination reason and accounting. Unused cancelled
  replies are marked `executed:false`. Cancellation is a session outcome,not a
  new game rule or a fabricated provider failure/winner.
- `status.json`:displayed phase,current scores and budget summary,never the key.
- `preservation.json`:original game/evaluation/replay hashes unchanged.

Mocked runs are explicitly `MOCKED_LIVE_DEMO_NOT_REAL_LLM`; real runs are
`LIVE_BROWSER_PROMPT_V2`. Mock usage/cost fields are synthetic adapter fixtures,
not actual API spending. Neither kind overwrites official evaluation evidence.
The one-time same-origin session token is not an API key; origin/Host checks and
the token protect POST operations. No browser endpoint accepts angles/powers or
manual reset commands. Sessions bind only to127.0.0.1.

Alternative ports if occupied:

```powershell
py -m fusion.live_demo --mock --port 8815 --replay-port 8817 --live-port 8819
```

For real execution use the masked launcher on its default ports,or explicitly
approved server-side credential configuration; never place keys in URL/CLI args.
Stop an earlier process withCtrl+C rather than altering security settings.

Tests from the project directory:

```powershell
py -m unittest discover -s tests -p test_live_demo.py -v
py -m unittest discover -s tests -v
py -m fusion.freeze
```

Optional Node built-in-only controller check:
`node -e "require('./tests/live-demo-controller.cjs').then(console.log)"`.
Node is not required to play. No paid requests are made by these tests.
