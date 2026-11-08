# py launcher correction - offline verification

User reported python Windows appalias exit9009; working py required.
run-approved-evaluation.ps1 now resolves Get-Command py once and uses that
same launcher for both freeze and actual evaluation. sys.executable probes
before each stage must match; mismatch/nonzero exit aborts before paid use.
Added -Offline: freeze+approved plan only,no credentialprompt/liveflag/output.
Existing max72calls/$5/model/observationalmemory/freeze/overwriteguards retained.

Actual checks:
- PowerShell parser:0syntaxerrors.
- Agent sandbox cannot accessWindowsApps launcher. Explicitly approved external
  command test found py at C:/Users/lzy21/AppData/Local/Microsoft/WindowsApps/py.exe.
- Both real interpreterprobes returned
  C:/Users/lzy21/AppData/Local/Python/pythoncore-3.15-64/python.exe.
- Real py -m fusion.freeze:PASS18artifacts.
- Real py -m fusion.llm_eval (without --live):plan_only_not_live,
  12liveplanned/12controls/72maxcalls,correctpinnedmodel/memory/opponent.
- This tool shell blocks .ps1files via executionpolicy. Fullfileexecution was
  not performed; syntax and exact commands were verified directly. No execution
  policy changed/bypassed. Use the user's workingPowerShellsession for thefile.
- No providerrequests,paidcalls,frozenfilechanges,pushorPR.

Run from projectdirectory:
.\run-approved-evaluation.ps1 -Offline
.\run-approved-evaluation.ps1
The secondcommand prompts for a masked sessionkey and starts the approvedrun.
