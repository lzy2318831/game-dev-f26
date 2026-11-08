# Approved continuation only: preserve the original failed run and single smoke.
param([switch]$Offline)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$recoveryLauncher = (Get-Command py -CommandType Application -ErrorAction Stop).Source
$recoveryInterpreter = & $recoveryLauncher -c 'import sys; print(sys.executable)'
if ($LASTEXITCODE -ne 0) { throw 'py interpreter probe failed; no request made.' }
Write-Host "Python interpreter: $recoveryInterpreter"
& $recoveryLauncher -m fusion.freeze
if ($LASTEXITCODE -ne 0) { throw 'Freeze verification failed; no request made.' }
$recoverySecondInterpreter = & $recoveryLauncher -c 'import sys; print(sys.executable)'
if ($LASTEXITCODE -ne 0 -or $recoveryInterpreter -ne $recoverySecondInterpreter) { throw 'Python interpreter mismatch; no request made.' }
# This command validates the immutable prior evidence and approval accounting offline.
& $recoveryLauncher -m fusion.llm_resume
if ($LASTEXITCODE -ne 0) { throw 'Recovery validation failed; no request made.' }
if ($Offline) { return }
$recoveryPreviousKey = $env:OPENAI_API_KEY
$recoverySecret = $null
try {
    $recoverySecret = Read-Host 'OpenAI API key (masked; not saved)' -AsSecureString
    $env:OPENAI_API_KEY = [System.Net.NetworkCredential]::new('', $recoverySecret).Password
    if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) { throw 'Empty key; no request made.' }
    Write-Host 'Approved 11-trial continuation; at most 70 additional requests; original aggregate $5 cap. No automatic request retries.'
    & $recoveryLauncher -m fusion.llm_resume --live --approve-paid
    if ($LASTEXITCODE -ne 0) { throw 'Recovery stopped. Preserve evidence/live-mini-recovery-01 and inspect its manifest before proceeding.' }
    Write-Host 'Finished. Inspect evidence/live-mini-recovery-01/combined-report; original failure and smoke preserved separately.'
}
finally {
    if ($null -eq $recoveryPreviousKey) { Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue }
    else { $env:OPENAI_API_KEY = $recoveryPreviousKey }
    if ($null -ne $recoverySecret) { $recoverySecret.Dispose() }
    Remove-Variable recoverySecret,recoveryPreviousKey -ErrorAction SilentlyContinue
}
