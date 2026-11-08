# Navigation fix and read-only agent investigation — 2026-11-07

No paid calls,PR push/submission,engine/rule/scoring/baseline/prompt changes.
Before editing,prior navigation/controller source was preserved byte-for-byte
under before/. Original failed/smoke/recovery evidence plus the two user browser
runs were hashed in evidence-before.json. Final hash comparison passed unchanged.
UI navigation changes are intentional; they do not alter recorded actions or
the frozen playfield. All18frozen artifact hashes still pass.

## Navigation result

The combined launcher's Main Menu explicitly lists Human/Human,Human/Geometric,
Human/Smart,Recorded LLM Replay and Live LLM Agent. Human/recorded Restart Match
is available. Main Menu from normal play invalidates stale callbacks; delayed
game-over rendering cannot cover the menu.

Recorded/live viewers have Back to Main Menu in header and intro/result dialogs.
Replay exit clears timers,invalidates old generation and stops animation.
Live exit stops polling/preview/animation,cancels and joins the bounded worker
outside its state lock. Only safe_to_navigatetrue permits redirect; unknown cost
reservations/in-flight replies remain in the audit. No paid allowance resets.
Both viewers receive the actual bound menu URL. A live restart still requires a
fresh backend launch and explicit financial confirmation,not a silent reset.

## Actual checks

- Test-first new navigation contract failed import before make_live_servers
  existed. After implementation2new navigation regressions passed6.316s.
- Tests exercise real loopback endpoints on ephemeral ports:both viewers'parent
  URL,menu asset and choices,all3human mode resets with accepted first shots,
  no-call live exit,and settled in-flight mocked exit retaining1request and0
  executed shots. Previously6paid-opportunities cannot restart through Back.
- Full project regression suite: **164tests passed in285.379s**. Includes existing
  replay,cancellation,provider/illegal-action/limits and frozen mechanism tests.
  Authorized navigation source changes legitimately invalidated the older
  content-addressed offline pilot proof; fresh mock proof was created without
  overwriting the old one or making live calls.
- Actual navigation/live/replay JavaScript parsed and built-in Node assertions
  passed:stop-before-redirect,false-safe blocks redirect,3modal/header Back
  controls,replay timer cleanup,live poll/preview cleanup,declined paid dialog
  dispatches0,stale packet/start responses cannot resume,and delayed game-over
  overlay cannot cover Main Menu. CI workflow now invokes the new controller
  assertions as offline checks; remoteCI was not run or claimed.
- Existing working Windows `py` launched the exact mocked command on8825/8827/
  8829. Both viewer /navigation/info routes returned http://127.0.0.1:8825/.
  This is server/HTTP verification,not a visually observed GUI or human playtest.
- Freeze18and all original/browser evidence hash preservation passed at end.

## Independent read-only review

Fresh `/root/navigation_review` found a delayed original showResult callback
could cover Main Menu after returning during the final-shot delay. Added a
presentation guard while startedfalse/menuvisible and actual JS regression.
Reviewer also suggested post-await Start/Ready/Cancel generation/leaving guards;
implemented to prevent stale live UI updates after Back. Backend cancellation
already blocked further dispatch. Reviewer verified all fixes,ran the mocked
live-leave test (passed0.846s),Node navigation/live/replay assertions andfreeze18.
No blocking residual issue reported. No reviewer edits,network/API/GUI calls or
course gate approval. No screenshots or playtester observations invented.

## Agent investigation

Read-only analysis verified one genuine completed browser-v2 trace through the
frozen engine:15:1185loss,4scratches/6modelshots,meanpower52.5,0creditedmodelpots,
0illegal actions. All6actualHTTP200results have the current v2prompt hash
c005b4ae1524b78020dbbfc817371c29d26e67660c6c124c9a1a03bc1b530db7.
The other browser record is explicitly mocked/incomplete and excluded from
real performance claims. Data/observations are in live-diagnosis.json; originals
were not rewritten. This is separate from official2wins/9losses/providerfailure.

NAVIGATION-AND-AGENT-PLAN.md separates observations from hypotheses and describes
a prospective4candidate/38400tick,one-model-call chooser. No simulator-assisted
policy,candidate generator,large planner,new model setting or paid experiment
was implemented. Model final choice,compute disclosure,forecast equivalence,
fresh held-out testing and independent review are prerequisites to any future
claim. The document does not grant a new paid-call authorization.
