# Fusion live-player boundary — prepared, not enabled

fusion/player.py builds a JSON-only public context and reuses the project's
bounded child-process worker. fusion/runner.py accepts an explicitly injected
model-policy object, counts every attempt before invocation, enforces the hard
request/deadline/call limits, records source/metadata/failures, and never
substitutes a baseline. Tests use labeled offline fixtures only.

No real provider transport, model ID, credentials, live GUI mode or paid call
exists in this slice. Human vs LLM remains a later integration task, after the
student reviews gameplay/visuals. The old pool/model.py prompt is six-ball
backup material and must not be sent as Fusion rules.

Before future live execution: choose one provider/model, implement and mock-test
the official API transport and Fusion prompt, record configuration/prompt
hashes and dated prices, obtain a concrete budget/approval, then run the frozen
suite without tuning on held-out cases. Keep secrets out of prompts, traces,
code, PRs and recordings. Root assistant subscriptions do not fund player APIs.

