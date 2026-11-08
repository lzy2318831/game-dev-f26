# Kinetic Circuit evaluation

The original official evaluation completed **11 LLM matches: 2 wins, 9 losses,
0 draws and 0 illegal actions**. Mean scores were **720.45 for the LLM and
1347.27 for its actual Geometric opponent**. An initial HTTP 429 rejection is
preserved as the twelfth official trial, not treated as a draw or replaced.

The main conclusion is limited: the model submitted legal shots and completed
matches, but it did not outperform Geometric overall. Prompt-v2 and browser
experiments happened later and are reported separately below.

## Official protocol and evidence

- Game: `fusion-1.5.0-replenish`; declaration: [suite 6](fusion/evaluation.json).
- Player: original `fusion/llm.py`, OpenAI `gpt-5.4-mini-2026-03-17`.
- Input: public observation/legal actions, observation-only memory; no simulator,
  repository tools, hidden state or Smart substitution.
- Situations: direct pockets, bumper-assisted play, risky/obstructed shots.
- Seeds: 101 and 102; both seats, four planned trials per situation.
- Each player has six opportunities. All 11 completed games ended `shots_exhausted`.
- Limits: 20-second requests, 300-second episodes, original shared 72-attempt
  allowance and $5 local estimated budget. Failures counted; no automatic retries.
- Twelve matched Geometric-vs-Geometric controls used the same layouts/seeds
  and target seats. They are separate from the Geometric opponents in LLM matches.

The layouts were declared before the original policy evaluation. Earlier
declarations and the replenishment amendment remain in the versioned files;
they were not replaced with easier situations after seeing results. Seeds do
not randomize this engine, so repeated seeds do not imply independent boards.
The original cases later informed v2 development and are not untouched held-out
cases for a new v2 strength claim.

Primary evidence:

- [Initial failed run](evidence/live-mini-approved-01/manifest.json)
- [Eleven-match continuation and traces](evidence/live-mini-recovery-01/manifest.json)
- [Combined CSV](evidence/live-mini-recovery-01/combined-report/comparison.csv)
- [Combined summary](evidence/live-mini-recovery-01/combined-report/summary.json)
- [Read-only recomputation and replay verification](evidence/final-docs-01/verified-evaluation.json)
- [Separate successful one-call smoke](evidence/api-smoke-mini-01/result.json)

All 24 official trial/control traces have been reproduced offline through the
unchanged engine, matching events, state fingerprints and outcomes. The old
freeze manifest and original rules document are preserved under
[the documentation archive](evidence/final-docs-01/previous/). Saved evaluation
hashes remain historical records; documentation corrections do not rewrite them.

## Scores and outcomes

Scores below put the LLM first regardless of seat. Control score means the
target seat in a separate Geometric-vs-Geometric match.

| Situation / seed / LLM seat | LLM : opponent | Result | Control score | Input / output tokens | Total decision latency (s) | Known estimated USD |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Direct / 101 / P1 | 0 : 0, no shots | HTTP 429 failure | 0 | unknown | 1.796220 | unknown |
| Direct / 101 / P2 | 990 : 1455 | Loss | 0 | 21809 / 132 | 8.493848 | 0.01695075 |
| Direct / 102 / P1 | 605 : 1660 | Loss | 0 | 17237 / 126 | 7.276970 | 0.01349475 |
| Direct / 102 / P2 | 685 : 1485 | Loss | 0 | 21960 / 132 | 6.896482 | 0.01706400 |
| Bumper / 101 / P1 | 1235 : 185 | Win | 460 | 17530 / 126 | 6.087678 | 0.01371450 |
| Bumper / 101 / P2 | 1095 : 1500 | Loss | 1195 | 20910 / 138 | 6.492169 | 0.01630350 |
| Bumper / 102 / P1 | 745 : 1565 | Loss | 460 | 17411 / 126 | 5.997991 | 0.01362525 |
| Bumper / 102 / P2 | 900 : 935 | Loss | 1195 | 18589 / 144 | 6.443127 | 0.01458975 |
| Risk / 101 / P1 | 295 : 555 | Loss | 2875 | 15427 / 138 | 6.214251 | 0.01219125 |
| Risk / 101 / P2 | 130 : 2670 | Loss | 25 | 19503 / 144 | 6.012800 | 0.01527525 |
| Risk / 102 / P1 | 1010 : 385 | Win | 2875 | 15261 / 132 | 5.844375 | 0.01203975 |
| Risk / 102 / P2 | 235 : 2425 | Loss | 25 | 18354 / 144 | 6.625019 | 0.01441350 |

| Completed situation | LLM wins/losses | Mean LLM score | Mean actual opponent score |
| --- | --- | ---: | ---: |
| Direct (3 complete; 1 failure) | 0 / 3 | 760.00 | 1533.33 |
| Bumper (4 complete) | 1 / 3 | 993.75 | 1046.25 |
| Risk (4 complete) | 1 / 3 | 417.50 | 1508.75 |
| All 11 completed | 2 / 9 | 720.45 | 1347.27 |

The completed head-to-head win rate is 2/11 (18.18%). Across all 12 attempted
trials it is 2/12, with one separately counted provider failure. Completed LLM
scores total 7,925; actual opponent scores total 14,820. The failure's recorded
0:0 is not a played draw.

For the 11 corresponding control seats, the mean is 828.18. Across all 12
controls, total score is 9,110 and mean is 759.17; their target seats have
4 wins, 4 losses and 4 draws against another Geometric player. These control
figures must not be confused with the 1347.27 in-match opponent mean.

## Scratches, legality and failure handling

There were **25 cue scratches in 66 LLM shots** (37.88%), compared with 20
scratches for the actual opponents. A scratch erases all points from the shot,
including earlier pots, device awards and combos, while pocketed objects stay
removed. Of the LLM's 80 physical object-pot events, **44 occurred on foul
shots**; only 36 counted as non-foul pots. The saved CSV counts physical pots,
so that column differs from the engine's credited-pot metric. Neither is edited.

The LLM had zero engine-illegal actions and zero invalid model proposals.
Actual opponents and controls also had zero illegal actions. A legal shot is
not necessarily a useful one: this distinction matters more here than parsing.
The HTTP 429 failure is a provider rejection, not an illegal move. Its exact
message/body was discarded by the old handler, so the saved evidence does not
establish the precise billing-versus-rate-limit cause. Later error logging was
fixed; the failed run was not overwritten.

## Calls, latency, tokens and estimated cost

The continuation made 66 successful real calls: **203,991 input + 1,482 output
= 205,473 reported tokens**, estimated **$0.15966225**. Successful decision
latency totalled 72.384709 seconds, mean 1.096738 seconds and median 1.063078
seconds. Including the failed first request gives 74.180930 seconds of recorded
official call latency. The 72 target-seat control decisions totalled 3.276747
seconds (mean 0.045510). These are local wall-clock decision timings, not video
duration or isolated provider-network measurements.

The original rejected request used one attempt; its tokens and actual charge
are unknown. Its $0.0109875 reservation remains. The separate successful smoke
used one call, 2,156 tokens and $0.001707 estimated cost; it is not a scored match.

Together, official attempts plus smoke used **68 of 72 attempts**, with
**207,629 known tokens plus unknown rejected-request usage**. Known estimated
cost is **$0.16136925**; the conservative reserve-inclusive total is
**$0.17235675**. These use the saved 2026-11-07 rates of $0.75 input/$4.50 output
per million tokens, ignoring cache discounts. They are estimates, not invoices.
Later v2/browser costs are not included in these official figures.

## Later development, kept separate

The [prompt-v2 pilot](evidence/live-prompt-v2-pilot-01/summary.json) now contains
three completed real matches: **1 win, 2 losses**, scores 615:805, 585:1825 and
1385:1205. It used 18 calls, 75,517 reported tokens, $0.05823525 estimated,
8 LLM scratches and zero illegal actions. Its three seeds share the standard
rack and P1/P2/P1 seats. This is a small, different experiment, not a controlled
proof of improvement over the original evaluation.

Saved [browser live-demo runs](evidence/live-browser-v2/) include a completed
15:1185 v2 loss with four scratches, a separate failed live session, and mocked
records. They are development/playtest records, not additions to the official
trial count. Mocked responses never count as real inference. The proposed
physics-assisted agent is not implemented. See [development notes](NAVIGATION-AND-AGENT-PLAN.md).

## Reproduction and limitations

Working directory: `midterms/lzy2318831/`. These commands make no API calls:

```powershell
py -m fusion.final_analysis --verify
py -m unittest discover -s tests -v
py -m fusion.freeze
```

For a recorded demonstration, use the [README launch commands](README.md).
The default replay is the genuine 900:935 LLM loss. It shows recorded choices
and regenerated physics, not a live API session or evidence that one match is
representative. Do not rerun the completed paid launchers to reproduce statistics.

I chose a bounded, observation-only agent so its decisions would be inspectable
and inexpensive to evaluate. The results show that valid JSON and a rules prompt
were not enough for reliable cue survival. Frequent scratches and poor retained
scores are the main limitations. There was no live memory ablation: the game is
fully observed between shots, but that does not prove history could never help.
Direct Geometric controls also repeatedly scratch; I kept that weakness visible
instead of improving the baseline after evaluation.

Three situations, repeated deterministic boards, reduced direct-case coverage
and unequal completed seats limit generalization. There is no confidence claim
or overall LLM-superiority claim. Simulator/Smart results from earlier versions
are not live-LLM evidence.

Latest completed local development validation: 164 project tests and 18 freeze
checks passed; [navigation verification](evidence/navigation-fix-01/REPORT.md)
also records controller checks. The [scoped CI workflow](../../.github/workflows/midterm-lzy2318831.yml)
exists, but a green remote run for the submitted commit is **pending**.
The required observed other-person playtest, actual video URL, two independent
skill-session references and student review of this reflection are also pending.
My own playtesting and automated browser checks do not replace human observations.
