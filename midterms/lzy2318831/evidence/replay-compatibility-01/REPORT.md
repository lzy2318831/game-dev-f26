# Strict historical replay runtime compatibility

Course PR: https://github.com/columbia-university-ai-games/game-dev-f26/pull/97
Target main; head lzy2318831/midterm in the course repository. Write access was
verified and the branch was absent before the reviewed commit was pushed.
No force push, main update or other student's changes occurred.

## Verified first divergence behind the13CI errors

Every reported error enters the same default archived recorded match,
`observation_only-bumper-102-p2`, directly or while constructing its viewer.
On Linux CPython3.11/3.12 the first8shots match accepted status, all events,
the complete observation fingerprint and outcome exactly. Shot9 is123°/48.
The first differing elementary operation is `math.sin` of the identical input
`0x1.12c8ddffb6315p+1`:

| Runtime | sin result |
| --- | --- |
| Windows CPython3.11.9 /3.15.1 | `0x1.ad663a8ae2fdcp-1` |
| Linux CPython3.11.18 /3.12.16 | `0x1.ad663a8ae2fdbp-1` |

The one-ULP difference changes launch vy and then first-tick vy
365.4157553752208→365.4157553752207. The third event's x first differs at
320.3071141840224→320.30711418402234. Expected after-shot SHA256 is
`969045eb5a7a391b97a8d31c72745b812131eda439d68c90762cf6c936a21181`;
Linux produces `8caf2cecbc51a4d982c5d7fb611626379703c90207d59b50ae43069753af3464`.
Outcome at that shot still agrees; exact event/hash agreement does not.

The Windows3.11 control matches all12shots exactly. More decisively, changing
only that sine return value inside an isolated Windows diagnostic process
reproduces the identical Linux shot9event value and failing SHA256. This patch
is restored in finally and is NEVER used in gameplay, replay or CI validation.
The causal counterfactual is preserved in
windows-isolated-linux-sin-counterfactual.json. This rules out JSON formatting,
missing files, corrupt traces and Python3.11 alone as the cause of these13errors.

CPython's math functions wrap platform C-library functions; numerical results
are not a portable bit-for-bit replay ABI. See the official
[Python3.11 math documentation](https://docs.python.org/3.11/library/math.html).

## Compatibility correction and boundary

The permitted workflow's complete deterministic job now uses Windows runners
with the existing CPython3.11/3.12 matrix. Every unit test, JavaScript suite,
all24official replay checks, archive hashes and frozen-artifact checks remain
unchanged and strict. Matrix fail-fast is disabled to inspect both versions.
Nothing is rounded, ignored, regenerated, substituted or relabeled. The short
Windows/Linux numeric-provenance job is explicitly a diagnostic, not a claim
that Linux strict replay passed. It preserves evidence of the limitation.

This is a reproducibility-environment fix, not a portable physics rewrite.
Exact historical replay and the combined launcher that validates it require
Windows reference math. Future Linux bit-exact portability would need a
separately reviewed numerical implementation/version; that is outside this fix.
No archived source, saved trace, scoring, physics, AI power or model settings
were edited. All157archived hashes and18current/18archived freezes remain
mandatory. Final actual workflow outcomes are recorded separately after running.

## Reproduction

From midterms/lzy2318831/, offline:

```powershell
python -m fusion.replay_diagnostics --output evidence/my-runtime-probe.json
python -m unittest discover -s tests -v
python -m fusion.final_analysis --verify --output evidence/my-replay-check.json
python -m fusion.freeze
python -c "from fusion.legacy import verify; print(verify())"
```

The diagnostic temporarily records math calls and tick states and restores the
original functions. It does not propose or execute model moves, call providers,
or alter archived files. First-request observations retain the actual historical
32-event truncation; unavailable full request data is not reconstructed.
Raw downloaded artifacts retain their original bytes and identify the runtime.
