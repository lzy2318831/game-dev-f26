# Student-authorized demonstration power setting

The student explicitly accepts the measured scratch tradeoff and chooses2x
as the preferred Live Geometry setting. Preserve1x via a waiting-state-only
selector. Existing F2/F3/F8 public-candidate contract applies; no engine rules
change. Only generated candidate power changes, capped at100. Preserve IDs,
angles, targets/routes; show base power and updated risk notes, active setting
in public context, selection metadata, consent and saved trace. No runtime
rollout, scripted substitute, model retry or budget reset. Fresh matches keep
the selected setting. Settings mutation requires same origin/current token and
no active worker, sends no model request, and cannot re-enable a spent server.

Red/green tests first: multiplier keyword, caps/identity, preferred2x server,
waiting-only update, unchanged consent/accounting and persistence. Actual Chrome
checks use synthetic responses and both settings. Historic1x expectations
remain pinned to1x rather than reinterpreted as2x outcomes.
