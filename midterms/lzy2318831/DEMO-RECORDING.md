# Record the autonomous LLM demonstration

From Windows PowerShell, no API key or dependency install is needed:

```powershell
Set-Location C:\Users\lzy21\Documents\game-dev-f26\midterms\lzy2318831
py -m fusion.demo
```

Keep the terminal running. Open `http://127.0.0.1:8785` in Chrome/Edge.
Click **Watch LLM Agent Play** on the welcome screen or table page. It opens
the local recorded viewer and automatically starts the authentic completed
match. If opened directly at `http://127.0.0.1:8787`, press **START RECORDED
MATCH** or **Play**. No shot choices are required or accepted.

Controls: **Play** resumes automatic progression; **Pause after shot** pauses
at the next shot boundary; **Restart** restarts this same recorded match.
Pausing does not change a shot's physics. The viewer displays actual saved
angles/powers, recorded decision latency, player identities, points, pinball
events and final score. Do not call this live inference. It is labelled
**Recorded LLM Evaluation — NOT A LIVE API SESSION** throughout.

The default is `observation_only-bumper-102-p2`:LLM is Player2; Geometric wins
935:900. It was chosen as an informative close loss, not a best-case win. It
contains six genuine LLM decisions and six saved Geometric decisions. The
frozen engine regenerates motion; events, state fingerprints and final outcome
must match the saved trace. No decision policy or API is called by playback.

## Suggested 3–5 minute capture

1. Before recording, close private tabs/notifications and keep API terminals
   and credentials out of view. Use your existing recorder (for example,
   Snipping Tool's Record tab:New, select browser region, enable narration if
   desired, Start). Do not install software or change sharing automatically.
2. **0:00–0:25:** show the game title and Watch button. State:"Original Pool
   Shark-inspired Pool+Pinball game; this is an authentic recorded real-model
   evaluation, not a live API session. The LLM selected shots without human
   move selection." Then click the button once.
3. **About0:25–3:15:** let the whole match play. Read a few displayed LLM
   angles/powers; point out device chains, scratch penalties, six shots each,
   scoring and automatic opponent turns. Do not aim/drag or substitute moves.
   Calculated motion time is125.745833s; preview/turn/result delays bring playback
   to roughly174s, plus local compute/network overhead. This is calculated,
   not an observed screen-recording duration. Use boundary Pause/Play if you
   need explanation time; keep total recording within3–5minutes.
4. **About3:15–4:15:** show the final935:900 outcome, then EVALUATION.md's
   comparison. State2wins/9losses/1provider-failed official trial,0illegal
   actions,66successful recovery calls,$0.15966225 recovery estimate. Disclose
   that one replay is not proof of strength and that browser motion is a
   deterministic reconstruction of saved actions. Mention bounded calls,
   timeouts, observation-only input and separate Geometric/Smart/LLM policies.
5. Stop and review the complete recording yourself. Check duration, readable
   action labels and outcome, no private information, no cuts replacing moves,
   and honest recorded/live distinction. Save the recording or a permitted
   viewable link. Confirm access for instructor,TAs and assigned reviewers.

Add the genuine recording link to README.md and PR-DRAFT.md. A script, replay
page or planned timeline is not the required completed video. Human playtest
notes, student reflection and remote CI remain separate evidence.

If a port is occupied, stop the earlier local server withCtrl+C or use:

```powershell
py -m fusion.demo --port 8786 --replay-port 8788
```

Then open `http://127.0.0.1:8786`; the Watch button redirects to the correct
replay port. Normal Human/Human,Human/Geometric and Human/Smart play remains
available through this launcher. The older `py -m fusion.server` remains the
unchanged game-only launcher and does not add the Watch entry point.

**Live option deferred.** No Live LLM button or new paid demo session is enabled.
The existing secure Python adapter stays separate. A future live UI needs its
own explicit model/call/cost approval, server-only credentials and durable
no-retry ledger. Existing evaluation headroom is not new authorization.
