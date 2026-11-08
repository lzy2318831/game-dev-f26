# Human playtest: observed independent play by a friend

## Session evidence and scope

I personally watched my friend play Kinetic Circuit independently. I did not
tell them how to aim, choose shot power or make moves. The problems below were
identified while I observed their actual gameplay, not only from feedback
collected afterward. The player is anonymous. These notes summarize the observed
problems and reported feedback; they are not verbatim quotes or an instrumented
record of the session. I have not
recorded the session date, duration, mode, exact scratch count or an action-by-action
account, so I do not make claims about those details.

This completes the observed other-person human playtest requirement: someone
else played while I watched without helping. No specific hesitation or guess
beyond the three findings below has been recorded.

## Observed gameplay problems and friend feedback

1. The cue ball scratched too easily. My friend found the scratches frustrating
   and scoring difficult.
2. Some balls ended up in awkward positions near the table edges or obstacles,
   making it harder for the player to aim and take effective follow-up shots.
3. The terrain layout could be improved to make play smoother.

## My interpretation and future improvements

I take this feedback as evidence that cue survival, awkward ball positions and
difficult follow-up shots need more attention. The current scratch rule removes
all points from a shot, including points earned before the cue falls into a pocket. That makes
scratches especially costly and helps explain why the player found scoring
frustrating. This explains the scoring consequence, not why a particular shot
scratched.

The official LLM evaluation also recorded frequent scratches: 25 in 66 LLM
shots. The human feedback suggests that pocket exposure and obstacle-driven
trajectories could be worth investigating alongside the agent's decisions.
However, one friend's feedback and the saved model results do not establish a
shared cause. Poor angle or power choices, awkward ball positions, difficult
follow-up shots and layout interactions are possibilities to test, not proven
explanations.

After submission, I would investigate scratch trajectories, awkward ball positions
and difficult follow-up shots with reproducible shot traces, then test whether
changes to pocket approaches, clearances or guide geometry improve recovery and flow. I would
compare both human experience and agent scratches before deciding on a fix.
These are future improvements only: I have made no changes to the frozen
physics, terrain, scoring or official evaluation in response to this playtest.

My earlier self-playtesting about late-match emptiness motivated the already
implemented limited replenishment. That is separate from this friend's feedback;
I do not attribute that earlier design decision to this session.

See [EVALUATION.md](EVALUATION.md) for the unchanged official results and
[SUBMISSION-CHECKLIST.md](SUBMISSION-CHECKLIST.md) for remaining evidence.
