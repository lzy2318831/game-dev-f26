# Navigation fix and prospective physics-assisted agent

## Test navigation without spending credits

Stop the old Python demo process withCtrl+C so it loads the updated routes and
controllers. Then,from Windows PowerShell:

```powershell
Set-Location C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831
py -m fusion.live_demo --mock --port 8825 --replay-port 8827 --live-port 8829
```

Open **http://127.0.0.1:8825/**. This explicitly mocked setup never calls a
paid model,even if a key exists. Human play and Geometric/Smart modes are real;
only the LLM demo's API responses are mocked.

The Main Menu offers **Human vs Human**, **Human vs Geometric AI**,
**Human vs Smart AI**, **Recorded LLM Replay**, **Live LLM Agent**.
Choose any human mode to play. **Restart Match** restarts the selected mode;
**Main Menu** returns to mode selection,including during a result screen.
Old delayed result callbacks cannot reopen the overlay above the menu.

Recorded demo:choose **Recorded LLM Replay** (8827). **Back to Main Menu**
is available in the header and the intro/result dialogs. It clears playback/
preview/result/AI timers,invalidates pending responses and stops the animation
loop before returning. **Restart Match** replays the same authentic saved
actions from its beginning; neither actions nor scores are changed.

Live demo:choose **Live LLM Agent** (8829),check the mocked label,confirm the
mocked match,then press **Back to Main Menu** while thinking or moving. It stops
polling/preview/animation,posts cancellation and waits for the server worker to
settle before navigating. An in-flight request is logged and an unexecuted
reply discarded. If safe settlement is not confirmed,the page stays put with
a status message and a retryable Back button; no new match is authorized.
The return target is the actual bound menu port,not a hard-coded default.

Back is also available after a genuine paid match on a separately approved
paid-enabled launch; it makes no new model request. Already reserved/sent calls
may still be charged. The6-call/$0.25match ledger is never reset by Back.
Paid Live Restart is deliberately not automatic:a new live session still needs
a fresh backend launch and explicit confirmation. Restart is directly available
for human and recorded matches. Returning to the menu lets you play all human
modes without restarting the backend or spending credits.

Default ports remain8805/8807/8809 when no overrides are passed. Use the combined
launcher above for both viewers to know their parent menu. A standalone viewer
without a running parent menu reports that absence rather than guessing a port.
No paid API calls were made for this fix. No physics/rules/scoring,baseline,
prompt-v2 strategy or official evaluation data were changed.

## Why prompt-v2 is still weak — verified evidence versus inference

**Observed:**one completed genuine browser run,
`evidence/live-browser-v2/20261107T140001Z-d4531653511b/trace.json`,
is6successful liveHTTP200 decisions with the actual prompt-v2 hash. It ends
**LLM15 : Geometric1185**,4LLM scratches,0credited LLM pots,0illegal actions.
Six angles/powers:171/57,316/56,197/56,167/47,203/53,198/46.
Mean power52.5; this is lower than the original official mean76.80. Merely
reducing power therefore did not fix this run's trajectories. It is one run
on the standard rack,not a controlled v1/v2 comparison or a strength estimate.

**Observed:**on the opening shot,the cue is(230,250),rack is to its right,
but angle171initially sends the cue left. That shot records4rail contacts,
3bumper contacts and a scratch,with0points. The next shot scores0 with5rail
contacts. Only the third LLM shot retains points:15from a bumper. The fifth
shot hits mechanisms,pockets one object and scratches,voiding all shot points.
The final shot scratches after a rail contact. The original official evidence
is untouched; this later playtest is a separate result. The other saved browser
record is explicitly MOCKED/incomplete and is not counted as a real evaluation.

Read-only derived data:[live-diagnosis.json](evidence/navigation-fix-01/live-diagnosis.json).
The diagnostic matched actual action/request/result hashes and replayed the
completed trace through the frozen engine. Source files were hashed before and
after; no replacement shots were generated or tested.

**Code facts:**prompt-v2 supplies formulas and verbal risk advice but no actual
trajectory calculations (`fusion/prompt_v2.py:GUIDANCE`). Even power46implies
speed422 and about1272units of friction-only unimpeded travel; powered devices
add more energy. Accurate contact normals,rails and pocket capture are nonlinear.
Integer-degree aiming also needs precision:at500units,one degree is about8.7
units,close to the11unit ball radius. Actual observations include public last
events/last_shot but generally describe the opponent; v2has no own-shot history.

**Inference:**target selection and prediction of cue survival remain weak;
verbal geometry/risk instructions do not enforce a useful route. Lower power
alone is insufficient,and a low device return is easily erased by a scratch.
We cannot infer the model's internal intention from angle/power JSON. There is
no evidence that it deliberately targeted a particular device or reasoned about
the future path correctly. No new paid call or model-setting change was made.

## Minimum viable next agent — proposal only, not implemented

Separate prospective ID:**kinetic-hybrid-v1-candidate-review**. Preserve official
LLM,v2,Geometric and Smart as distinct implementations/evidence. The MVP would:

1. Take only detached public `observe` and `legal_actions`. Construct at most
   **four distinct legal shots** spanning a clear pot,controlled device route,
   conservative retained-score route and simple bank/exploration. Use small
   transparent geometry rules,not `Smart.choose`, `Smart.plan` or the complete
   Geometric policy to secretly choose a move.
2. Forecast each once using the same authoritative physics,not another model:
   maximum4×9600=38400ticks per decision,no adaptive search,tuning sweep or
   opponent tree. Reuse the existing public physics primitive where practical.
   Show whether it settles,net shot points,scratch,pots,device interactions and
   resulting cue/ball positions. Unfinished forecasts are unknown/failure risks,
   not confident scores. Include actual between-shot rules where position or
   match outcome is reported.
3. Send the public state/legal schema plus a compact **unranked** candidate
   forecast table to the real LLM. No "recommended winner" or preselected move.
   The LLM selects the final angle/power based on immediate points,cue safety,
   score gap,remaining turns and the resulting position. Its actual selection
   is authoritative only after ordinary engine validation.
4. Keep one real model call per turn and the same engine action JSON. A bounded
   candidate-selection arm can require an exact candidate pair; an off-list
   proposal must fail explicitly,never be silently replaced/clamped. This is
   a policy-level restriction,not a change to the game's legal_actions schema,
   and must be disclosed. Log all candidates,forecasts,budgets and actual model
   reply so the final choice is inspectable.

The LLM retains a real choice among distinct routes and risk/position tradeoffs.
It must not simply echo a host-selected argmax. When one candidate dominates,
the choice may be obvious; do not overclaim that the model supplied planning
value. A separate deterministic candidate-argmax ablation using the same table
would measure what the LLM contributes. Original Geometric remains the official
baseline. Staff decide rubric sufficiency; this plan does not approve a gate.

This is **simulator-assisted LLM play**,not prompt-only v2 and not a relabelled
Smart policy. It has extra computation derived from public state; report that
asymmetry explicitly as required by MIDTERM_REQUIREMENTS.txt. The model gets no
engine object,filesystem,shell,evaluator answers or hidden state. Candidate data
would be a separate policy-context field,not an alteration of frozen observe.

### Main risks and offline verification before approval

- Public snapshot cloning can lose pocketed/replenished IDs,turn quotas or cue
  respot behavior. The existing `smart.Simulation` reuses tick/ShotLedger but
  does not itself implement every post-shot transition; do not present its
  intermediate positions as final match state. Verify cloned predictions against
  actual `Episode.step` on independent snapshots,including scratches/refills.
- Four choices can omit the strongest shot. This is the intended small MVP,
  not an optimal planner. Measure planning time and enforce the tick budget;
  do not let simulation block navigation/cancellation.
- Accurate immediate forecasts do not solve multi-turn strategy. The model can
  still choose poorly; never override its valid choice to manufacture strength.
- The candidate table changes information processing and token cost. Retain
  budgets,no retry,usage/failure logging and observation-boundary tests. Local
  estimated cost must be checked before any future paid request.
- Freeze new candidate rules/prompt and declare genuinely fresh held-out
  physical layouts before tuning. New seeds alone do not randomize this engine.
  Compare hybrid,unchanged Geometric and candidate-argmax on the same cases,
  both seats,repeated trials,reporting scratch rate,retained points,all failures,
  simulator CPU/ticks,API latency,tokens and cost. Do not merge those results
  into the original official evaluation.

Only navigation and a read-only diagnosis were implemented in this task. The
candidate generator,physics forecasting context and hybrid policy require a
separate implementation decision; paid tests require separate explicit approval.
