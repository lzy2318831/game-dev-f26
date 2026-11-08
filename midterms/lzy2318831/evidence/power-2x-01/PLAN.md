# Offline doubled-power experiment

Baseline code snapshots and SHA-256 hashes were saved before experimentation.
No runtime recommendations are changed. Proposed power = min(100, original * 2).
Use every current candidate on the 34 saved genuine prompt-v2 observations,
plus saved geometry-assisted selected-shot observations, including the known
266-degree simulation-limit position. Pair identical angle/target/route at both
powers using the unchanged deterministic physics simulator, capped at 9600 ticks.
Pots, scratch and settlement are exact simulator outputs. Track sampled cue-to-
object contact-radius proximity and target movement separately; the engine
does not record individual ball-ball collision events. These are contact
proxies, not complete collision logs. Failed trajectories are incomplete, and
provisional points/pots are excluded from settled performance totals.

Decision before results: do not enable 2x if it introduces simulation-limit
failures from previously settled candidates or worsens scratch rate by at least
5 percentage points. Report tradeoffs, not a claim of stronger LLM play.
All candidates are tested, not selected by a model. No paid calls.
