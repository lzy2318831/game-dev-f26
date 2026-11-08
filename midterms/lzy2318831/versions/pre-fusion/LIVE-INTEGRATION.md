# Live player integration preparation

Status: application boundary prepared and tested offline; no provider transport,
credentials, paid calls, or live evaluation yet.

`pool/model.py:ModelPlayer` accepts an explicit provider/model and a picklable
top-level transport callable. The runner passes only public observation,
the action vocabulary and optional last-two-record history. A spawned worker
enforces an interruptible timeout; failed attempts count and terminate with
explicit reasons. Structured action values are still validated by the engine.
The runner never labels a baseline action as model play.

The transport contract receives system/context/model/output-cap settings and
returns `{"text": "<JSON shot>", "model": "<resolved id>", "usage": {...}}`.
It must use one provider's official API, private environment credentials,
request timeout, zero automatic retries, structured output where supported,
and sanitized failure handling. It must not attach tools, files, engine state,
evaluation answers or credentials to messages. Tests use provider `fake` and
mark returned metadata as non-live. This is not evidence of API compatibility.

Next integration steps, before paid execution:

1. Student chooses Vertex, Anthropic, or OpenAI and an accessible model; inspect
   official documentation for that exact API and add a pinned local dependency
   only if needed. Keep all manifests/configuration in this folder.
2. Implement the transport with mocked HTTP tests for valid action, refusal,
   quota/auth failure, malformed response, timeout, usage and resolved model ID.
3. Add explicit opt-in live CLI arguments and Human vs Model view support.
   No live calls on import, CI, routine tests, or default offline commands.
4. Record prompt/configuration hashes, selected provider/model, prices dated
   at execution, per-match/batch token and monetary caps, and redacted traces.
5. Obtain the student's paid-call approval, then execute the declared suite
   without changing frozen cases or replacing failures. One live provider is
   enough; multiple-provider spending is unnecessary.

Provider SDK credentials and model IDs are independent of the coding assistant's
subscription. Do not put secrets in this document, commands recorded on video,
prompts, traces, source, PR text, or agent configuration.
