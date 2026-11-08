# Official evaluation failure: HTTP429 diagnosis and offline fix

## Confirmed historical facts

Originalrun:evidence/live-mini-approved-01. All six files preserved byte-for-byte,
SHA256 manifest failed-run-preservation.json. No rerun,overwrite,deletion or
provider request during this investigation. Both saved traces replay offline.

Trial observation_only-direct-101-p1 sent one request at
2026-11-07T07:22:10.847038+00:00. Result at07:22:12.642203+00:00:
HTTPstatus429, wrapperreasonprovider_error, wrapperkindhttp_error,
latency1.794072100019548sec. It failed before any LLMshot. Elevenremaining
trials were notrun because evaluator correctly fail-stopped on HTTPerror.
One matched Geometriccontrol completed(draw0:0); not substituted for an LLM.
No liveLLMmatches completed and no LLMquality/winrate can be concluded.

The exact provider message,error.type,error.code,error.param,requestID and
Retry-After are ABSENT. Previous send_openai caughtHTTPError but discarded
its body/headers. The labels provider_error/http_error are ours,not OpenAI's
original JSONerrorcode or message. The missing text cannot be recovered from
these saved files without independent provider-side evidence. No message or
insufficient_quota code is invented.

## Cause classification

| Candidate | Evidence and conclusion |
| --- | --- |
| Billing/credits/spend/usagequota | Possible429cause; exactcode notsaved,unconfirmed |
| Request/token/ramp ratelimit | Possible429cause; exactcode/header notsaved,unconfirmed |
| Authentication | Not diagnosed by this429; no saved401/invalidkeymessage |
| Model availability/access | Not diagnosed; no saved404/model_not_foundmessage |
| Unsupported parameters/schema | Not diagnosed; no saved400/unsupportedparammessage |
| Integration bug | Confirmed diagnosticloss: HTTPresponse body/headers discarded; fixed offline |

429alone is insufficient to distinguish the firsttwo. A quota/rate rejection
can precede other checks,so it does NOTprove key/model/parameters fullyvalid.
No requestparameter/prompt/model changes justified or made. Exact regenerated
request matches recorded payload byte-for-byte (request-and-preservation-check.json).
Officialreference:https://developers.openai.com/api/docs/guides/error-codes
(OpenAI documents several429billing/spend/quota and ratelimit conditions.)

## Integration fix

fusion.llm.http_error_metadata now retains allowlisted bounded
error.message/type/code/param,x-request-id and Retry-After. Exact available
message retained except credential/account/email redaction and lengthlimit;
rawbody/allheaders are notlogged. Bodyfingerprint/truncation flags record
nonJSON/oversized bodies without exposing contents. Response stream closed.
Clear diagnosticcategories distinguish explicitquota/ratecodes from unresolved
429. No retry,request changes or automatic continuation added. Existing
failurecounts,unknowncostreservation and fail-stop behavior retained.

Synthetic tests,not realprovider evidence: mocked429billing/rate,401keyredaction,
400unsupportedparam,nonJSON502. Originalfourtest run failedmissingdiagnostic
fields; afterfix4pass. Fullproject117tests111.721sOK(tests.txt). Independent
read-only reviewer4newtests0.012s+13existingLLMtests14.285sallpass,no blockers.
18frozenartifacts pass. Geometric,Smart,scenarios,physics/art untouched.

## Exact recovery steps - do not start another evaluation yet

1. Preserve originalfolder. Original launcher intentionally refuses existingrun;
   do NOTdelete/rename evidence or choose a fresh fullsuite to reset limits.
2. In the OpenAI APIorganization/project attached to the key,check available
   credits/billing and organization/project spend/usage limits; also check
   model-specific RPM/TPM and sharedprojectactivity. Look for thisrequest's
   timestamp/model in providerlogs if available. Share only redacted
   error.code/type/message,neverkey. No live validationcall has been made here.
3. Ifcode saysinsufficient_quota/credit_balance_exhausted or spend/usagecap,
   correct that billing/limit issue before retry; waiting/retrying alone is not
   a fix. Do not raise our$5limit. Ifcode saysrate_limit_exceeded/slow_down,
   follow Retry-After/providerlimits and reduce competingtraffic. Ifnoneofthese
   details are obtainable,exact429cause remainsunknown; request approval for
   ONE diagnostics-enabled call before anynewbatch,not an automaticrerun.
4. After externalissue is confirmed/resolved,obtain explicit continuation
   authorization. Keep the firsttrial asfailed; continue only11not-runtrials in
   linkednewsegment,not a replacement12-trialrun. Max66requests needed for
   those11. Originalcallcap72 has1attemptused =>71remaining. Localaccounting
   retains$0.0109875unknowncostreserve =>atmost$4.9890125conservative headroom.
   Actualcharge/tokenusage of429request isunknown,not assertedzero.
5. Preserve all failures and providerdiagnostics in linkedrecovery results.
   Retrying the firstfailedtrial is an additionaltrial and must be separately
   authorized/accounted. Newcontinuation is NOTstarted/approved by thisreport.
   Offline proposed-recovery-plan.json lists exactpendingIDs and ceilings;
   existing CLIhas no automaticresume path and oldlauncher shouldnotbererun.

No new APIcalls,push,PR,gamechange or deadlinechange. Officialfailure is evidence,
not erased or converted into a Geometric/Smart result. Primaryservicecause
remainsunresolved429 until providercode/message or account evidence is supplied.
