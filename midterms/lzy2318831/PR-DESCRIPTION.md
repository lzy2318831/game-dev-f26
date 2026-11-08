# Kinetic Circuit — Pool × Pinball AI Games Midterm

**GitHub login:** lzy2318831

**Final gameplay version:** `fusion-1.6.0-balanced`

**Demonstration:** Geometry-Assisted Live LLM with Adaptive Distance v2

Course submission links:

- [README and launch instructions](https://github.com/lzy2318831/game-dev-f26/blob/lzy2318831/midterm/midterms/lzy2318831/README.md)
- [Evaluation report](https://github.com/lzy2318831/game-dev-f26/blob/lzy2318831/midterm/midterms/lzy2318831/EVALUATION.md)
- [Agent team log](https://github.com/lzy2318831/game-dev-f26/blob/lzy2318831/midterm/midterms/lzy2318831/AGENT-TEAM.md)
- [Observed human playtest](https://github.com/lzy2318831/game-dev-f26/blob/lzy2318831/midterm/midterms/lzy2318831/PLAYTEST.md)
- [Implementation session and actual skill-use evidence](https://github.com/lzy2318831/game-dev-f26/blob/lzy2318831/midterm/midterms/lzy2318831/evidence/submission-readiness-01/SESSION-EVIDENCE.md)
- [Final gameplay demonstration](https://youtu.be/eLdDOiIwE84)

## 1. Project Overview

Kinetic Circuit is a browser-based game that combines traditional pool mechanics with pinball-inspired elements. My goal was to create a game where players need to think about more than just aiming at a ball and choosing the right power.

Unlike traditional pool, the table includes bumpers, powered slingshots, orbital mechanisms, and other interactive devices. These elements can change the direction and movement of the balls, creating more unpredictable situations.

I wanted to explore how these additional mechanics would affect both human players and AI agents, especially when an agent needs to make decisions in a more complicated physics environment.

## 2. Game Design and Mechanics

The game includes:

- A six-pocket pool table with 15 object balls.
- Turn-based gameplay with six shots per player.
- Mouse-controlled aiming and adjustable shot power.
- Cue animations showing both the pullback and forward strike.
- Pinball-inspired bumpers, slingshots, and orbital mechanisms.
- Multiple player modes, including human players and different AI opponents.
- A scoring system that rewards successful shots while penalizing scratches.

One of my main design goals was to make different shots lead to different outcomes. A direct shot may work well in one situation, while using the table's devices may create better opportunities in another.

The final gameplay version is `fusion-1.6.0-balanced`.

During development, I also revised the table layout by removing two short upper-corner barriers and reducing the powered slingshot strength by 25%. These changes were intended to make the table layout feel cleaner and the interactions easier to control.

## 3. AI Agent Design

The project includes several AI opponents, including a Geometry-Assisted Live LLM Agent.

The Geometry-Assisted Agent combines geometric shot planning with LLM-based decision-making.

Instead of asking the LLM to produce an arbitrary angle and power without guidance, the system first generates candidate shots based on the observable game state. The LLM then evaluates these options and selects a candidate to execute.

The process is:

1. Observe the current ball positions and table state.
2. Generate possible shot candidates using geometric information.
3. Provide the candidates and relevant context to the LLM.
4. Allow the LLM to select a shot.
5. Execute the selected action and observe the result.

The LLM still makes the final candidate selection, while the geometric system provides additional information to support its reasoning.

### Adaptive Shot Power

During testing, I noticed that the LLM often selected shots with very low power. Although these shots were sometimes safe, they did not produce particularly engaging gameplay.

To address this, I experimented with different power recommendations and eventually adopted Adaptive Distance v2 for the final demonstration.

The intended power ranges are:

| Shot Distance | Power |
|---|---|
| Close range (0–150 units) | 30–40 |
| Medium range (150–350 units) | 40–80 |
| Long range (greater than 350 units) | 80–100 |

These recommendations apply to normal contact and pocketing candidates, including bank-contact routes. Certain escape and device-related shots retain separate power handling. Distance means cue travel to first contact; the long band reaches 100 at 1,000 units. Existing 1x and 2x settings remain available.

My goal was to encourage stronger, more meaningful shots while still allowing the LLM to choose its actions.

## 4. Development and Iteration

This project went through several iterations.

Some of the challenges I encountered included:

- Balancing the strength of pinball devices.
- Preventing excessively long physics interactions.
- Improving the visual timing of the cue-strike animation.
- Making the Live LLM mode work correctly across multiple matches.
- Improving shot recommendations when the AI was playing too conservatively.
- Preserving previous evaluation results while updating the game's physics.

I also experimented with different power strategies and used offline simulations to compare their effects.

These experiments helped me understand that stronger shots do not automatically produce better results. A shot with more power may create additional scoring opportunities, but it can also increase the chance of a scratch or trigger longer device interactions.

## 5. Testing and Evaluation

The final local development validation on Windows/Python 3.15.1 included:

- 222 Python tests passed.
- 7 JavaScript test suites passed.
- 24 historical replay checks passed.
- Current and historical frozen-artifact verification passed.
- Browser tests for gameplay, Live LLM navigation, match restart, and failure recovery, using synthetic model responses without paid calls.

These are project-specific checks. Supplemental repository-starter diagnostics remain environment-incomplete locally because of missing optional dependencies and Windows symlink privileges; their output is preserved in the [final validation report](https://github.com/lzy2318831/game-dev-f26/blob/lzy2318831/midterm/midterms/lzy2318831/evidence/submission-final-01/REPORT.md).

**Remote CI and reproducibility:** The [first Linux Midterm run](https://github.com/lzy2318831/game-dev-f26/actions/runs/42435757312) failed with13historical replay errors. The [follow-up investigation](https://github.com/columbia-university-ai-games/game-dev-f26/blob/lzy2318831/midterm/midterms/lzy2318831/evidence/replay-compatibility-01/REPORT.md) identifies the exact cause: platform sine rounding differs by one ULP at123degrees, first changing shot9of the default recorded match. Windows Python3.11 reproduces all12shots exactly, and an isolated sine-only diagnostic substitution reproduces the Linux failure. I preserved the archived engine, traces and exact event/hash checks. All deterministic CI tests and24historical replays now run on the Windows reference environment with Python3.11/3.12. Linux bit-exact replay remains unsupported; its numeric probe is diagnostic only. See the [actual course PR checks](https://github.com/columbia-university-ai-games/game-dev-f26/pull/97/checks) for the current result. This changes reproducibility configuration, not gameplay physics or AI settings.

### Recorded LLM Evaluation

The original recorded LLM evaluation was conducted using the earlier v1.5 gameplay physics.

Across 11 completed matches against the Geometric AI:

- LLM wins: 2
- Geometric AI wins: 9
- Illegal actions: 0

These results show that the recorded LLM agent was able to participate legally, but its gameplay performance was still weaker than the Geometric opponent.

The historical evaluation is preserved and is not presented as a new evaluation of the final v1.6 physics or Adaptive Distance v2 strategy. The original HTTP 429 failure is also retained in the evaluation evidence.

The later Adaptive power experiments used saved game states and offline simulations. They helped guide development, but they do not establish an improved real-match win rate.

## 6. Known Limitations and Future Improvements

Although the current version is playable and includes the main features I planned, I still think the map and table design have significant room for improvement.

### Map Design

One area I would like to improve is the overall table layout. Some parts of the current map still feel relatively simple, and I believe the placement of the obstacles and devices could be more carefully designed.

In future versions, I would like to revise the map structure, improve the balance between different areas, and create more interesting shot opportunities.

### More Interactive Modules

I would also like to add more pinball-inspired mechanisms and interactive modules.

For example, future versions could include new types of bumpers, moving obstacles, additional launch mechanisms, or devices that interact with balls in different ways.

I think adding more variety would make each round more interesting and encourage players to experiment with different strategies.

### AI Decision-Making

The Geometry-Assisted LLM is an interesting starting point, but I think its decision-making could still be improved.

Currently, geometric information helps the agent select possible shots, but the agent does not always make the most effective choice.

In the future, I would like to explore better trajectory prediction, stronger evaluation of candidate shots, and potentially more advanced planning methods.

### Physics and Gameplay Balance

The combination of pool and pinball mechanics creates unpredictable interactions, which is part of the game's appeal. However, it also makes the game harder to balance.

Future work could include improving device behavior, reducing overly long ball interactions, and further tuning the relationship between shot power, difficulty, and scoring.

Live LLM gameplay also depends on an external API, which introduces costs, latency, and occasional request failures.

Overall, I see the current version as a foundation that I can continue building on. My main future goal is to make the map more creative, introduce more interesting devices, and provide a richer experience for both human players and AI agents.

The observed friend playtest and official comparison belong to v1.5. I do not present them as a fresh human playtest or model-performance evaluation of v1.6. Stronger Adaptive shots can trigger longer device cascades, and simulation-limit recovery does not guarantee that every future trajectory will settle.

## 7. AI Assistance and My Contributions

I used Codex as a development assistant for implementation, debugging, test generation, and documentation.

I made the main design decisions, including the Pool × Pinball concept, table mechanics, gameplay changes, agent direction, and final power settings.

I also reviewed the results of different iterations, identified problems during gameplay, and decided which changes should be included in the final version.

The AI tools supported the development process, while the project direction and final design choices were guided by my own goals and feedback.

## 8. Gameplay Demonstration

**[Watch the final Kinetic Circuit gameplay demo](https://youtu.be/eLdDOiIwE84)**

The video demonstrates the final `fusion-1.6.0-balanced` version with the Geometry-Assisted Live LLM Agent and Adaptive Distance v2 power settings. This description of the video is my supplied account, separate from the offline test evidence.
