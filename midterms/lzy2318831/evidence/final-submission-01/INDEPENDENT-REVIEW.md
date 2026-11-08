# Independent read-only submission/replay review

Reviewer context:`/root/submission_replay_review`, separate from implementation.
Scope:recorded_replay.py,demo.py,replay_web,final_analysis.py and replay tests.
No reviewer file edits,provider calls,GUI actions or student gate approval.

Actual findings and disposition:

1. Blocking:Play/Resume called scheduleAI,which cleared the timer also used by
   an active shot preview and final-result modal. Fixed by returning before
   clearing timers while busy/notstarted/terminal. The reviewer inspected the
   fix and executed the actual extracted scheduler regression via Node built-in
   vm/assert; preview/final timers remain and automatic-next still schedules.
2. Minor:latency aggregation used controls.index(t). Changed to enumeration,
   avoiding equality-based wrong-seat indexing. Reviewer verified latest code.

Actual checks reported by reviewer:initial3replay tests passed4.854s; freeze18
passed repeatedly. Live model rows match saved liveHTTP200 request/result
actions/metadata. The backend executes unchanged recorded actions with frames
and validates events,fingerprints and outcomes. No policy substitution/API calls
observed. Reviewer inspected the fourth loopback HTTP test but did not run its
requests because that review was instructed not to use networking. Implementer
ran it separately. Full JavaScript parsing/timer assertions succeeded via the
existing Node runtime; node CLI was not on PATH. No browser visual check claimed.

Final follow-up before launcher-port update reported no additional blocking
static issues. Later launcher change uses8785/8787 and exclusive occupied-port
refusal; its5final replay/HTTP tests passed independently in implementation.
Final launcher follow-up:reviewer verified documented8785/8787CLI defaults,
occupied-port refusal,normal Handler session compatibility,actual-port redirect
with #autoplay and metadata-gated automatic start. Freeze18 passed again. No
blocking residual issue; reviewer did not run HTTP/GUI/API in this follow-up.

This review is development evidence,not a second saved skill session or student
authorship. Actual build/review session links still need student-supplied saved
session references where required.
