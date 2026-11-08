# One request only, separately authorized. Does not invoke the evaluation suite.
param([switch]$Offline)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$smokeLauncher = (Get-Command py -CommandType Application -ErrorAction Stop).Source
$smokeInterpreter = & $smokeLauncher -c 'import sys; print(sys.executable)'
if ($LASTEXITCODE -ne 0) { throw 'py interpreter probe failed; no request made.' }
Write-Host "Python interpreter: $smokeInterpreter"
& $smokeLauncher -m fusion.freeze
if ($LASTEXITCODE -ne 0) { throw 'Freeze verification failed; no request made.' }
$smokeSecondInterpreter = & $smokeLauncher -c 'import sys; print(sys.executable)'
if ($LASTEXITCODE -ne 0 -or $smokeInterpreter -ne $smokeSecondInterpreter) { throw 'Python interpreter mismatch; no request made.' }
if ($Offline) {
    & $smokeLauncher -m fusion.api_smoke
    if ($LASTEXITCODE -ne 0) { throw 'Offline smoke preparation failed.' }
    return
}
if (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'evidence/api-smoke-mini-01')) {
    throw 'Smoke output already exists. Preserve it; do not retry or reset the one-call limit.'
}
$smokePreviousKey = $env:OPENAI_API_KEY
$smokeSecret = $null
try {
    $smokeSecret = Read-Host 'OpenAI API key (masked; not saved)' -AsSecureString
    $env:OPENAI_API_KEY = [System.Net.NetworkCredential]::new('', $smokeSecret).Password
    if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) { throw 'Empty key; no request made.' }
    Write-Host 'Single GPT-5.4 mini request only; estimated budget below $0.10; no retries or full evaluation.'
    & $smokeLauncher -m fusion.api_smoke --live --approve-paid
    if ($LASTEXITCODE -ne 0) { throw 'Smoke failed. Stop and inspect evidence/api-smoke-mini-01/result.json. Do not retry automatically.' }
    Write-Host 'Smoke succeeded. Results and approval-pending recovery plan saved. STOP: no evaluation continuation was started.'
}
finally {
    if ($null -eq $smokePreviousKey) { Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue }
    else { $env:OPENAI_API_KEY = $smokePreviousKey }
    if ($null -ne $smokeSecret) { $smokeSecret.Dispose() }
    Remove-Variable smokeSecret,smokePreviousKey -ErrorAction SilentlyContinue
}
