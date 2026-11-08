# Fusion rule/source map

All rules are original `design` choices specified before implementation.
Historical inspiration is credited in the primary SOURCES.md; no historical
code, lookup tables, text, graphics, sound or ROM assets are reused.

| ID | Rule | Evidence / locator | Rationale |
| --- | --- | --- | --- |
| F1 | Six balls, pockets, two fixed bumpers | design: RULES.md F1 | Bounded table with open lanes and strategic interference. |
| F2 | Angle/power shot and drag controls | design: RULES.md F2 | Satisfying cue action rather than continuous historical steering. |
| F3 | Fixed-tick billiards simulation | design: RULES.md F3 | Predictable, testable behavior independent of rendering. |
| F4 | Bumper impulse and scoring limits | design: RULES.md F4 | Pinball energy without unbounded score/energy farming. |
| F5 | Pots and combos | design: RULES.md F5 | Reward productive bumper play and multi-pots. |
| F6 | Scratch voids shot and automatic respot | design: RULES.md F6 | Clear risk, no extra placement action. |
| F7 | Six alternating opportunities each, winner/draw | design: RULES.md F7 | Short complete match with fair quotas. |
| F8 | Interface and player boundary | design: RULES.md F8 | Same public game for humans, baseline and future model. |
| F9 | Baseline/evaluation/limits | design: RULES.md F9; evaluation.json | Real competitor and separately declared experiment. |

No `observed` playtest evidence or verified historical-rule fidelity is claimed.
Original choices use `design`, not `assumed`. Unimplemented behavior is not
labeled `code` merely because it appears in a specification. Implementation
and test locators are recorded after red/green execution in the primary
../rule-source-map.md.
