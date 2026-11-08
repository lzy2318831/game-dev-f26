# Default is entirely offline. Use -ApproveLive only after separate execution approval.
param([switch]$Offline,[switch]$ApproveLive)
$ErrorActionPreference = 'Stop'
if ($Offline -and $ApproveLive) { throw 'Choose offline or separately approved live execution, never both.' }
Set-Location -LiteralPath $PSScriptRoot
$pilotLauncher = (Get-Command py -CommandType Application -ErrorAction Stop).Source
$pilotInterpreter = & $pilotLauncher -c 'import sys; print(sys.executable)'
if ($LASTEXITCODE -ne 0) { throw 'Python interpreter probe failed; no API request.' }
Write-Host "Python interpreter: $pilotInterpreter"
& $pilotLauncher -m fusion.freeze
if ($LASTEXITCODE -ne 0) { throw 'Freeze failed; no API request.' }
& $pilotLauncher -m fusion.prompt_v2_pilot --offline-check
if ($LASTEXITCODE -ne 0) { throw 'Complete offline evaluation/replay preflight failed; no API request.' }
$pilotSecondInterpreter = & $pilotLauncher -c 'import sys; print(sys.executable)'
if ($LASTEXITCODE -ne 0 -or $pilotInterpreter -ne $pilotSecondInterpreter) { throw 'Interpreter mismatch; no API request.' }
if (-not $ApproveLive) { Write-Host 'Offline only: zero API requests. Live execution awaits separate approval.'; return }
if (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'evidence/live-prompt-v2-pilot-01')) {
    throw 'Pilot evidence already exists. Preserve it; do not retry, rename or reset the 18-call/$0.25 limits.'
}
$pilotPreviousKey=$env:OPENAI_API_KEY
$pilotSecret=$null
try {
    $pilotSecret=Read-Host 'OpenAI API key (masked, never saved)' -AsSecureString
    $env:OPENAI_API_KEY=[System.Net.NetworkCredential]::new('', $pilotSecret).Password
    if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) { throw 'Empty key; no request.' }
    Write-Host 'Separate v2 pilot: 3 matches; strict shared 18-call/$0.25 estimated ceiling; no retries.'
    & $pilotLauncher -m fusion.prompt_v2_pilot --live --approve-paid
    if ($LASTEXITCODE -ne 0) { throw 'Pilot stopped. Preserve evidence/live-prompt-v2-pilot-01; inspect failures before any further execution.' }
    Write-Host 'Completed. Results: evidence/live-prompt-v2-pilot-01/summary.json and comparison.csv. No other evaluation launched.'
}
finally {
    if ($null -eq $pilotPreviousKey) { Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue }
    else { $env:OPENAI_API_KEY=$pilotPreviousKey }
    if ($null -ne $pilotSecret) { $pilotSecret.Dispose() }
    Remove-Variable pilotSecret,pilotPreviousKey -ErrorAction SilentlyContinue
}
