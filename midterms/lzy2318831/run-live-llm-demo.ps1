# Paid mode requires separate user approval AND browser match confirmation.
param([switch]$EnablePaid,[switch]$Mock)
$ErrorActionPreference='Stop'
if ($EnablePaid -and $Mock) { throw 'Choose genuine paid mode or explicitly mocked testing, never both.' }
Set-Location -LiteralPath $PSScriptRoot
$liveLauncher=(Get-Command py -CommandType Application -ErrorAction Stop).Source
$liveInterpreter=& $liveLauncher -c 'import sys; print(sys.executable)'
if ($LASTEXITCODE -ne 0) { throw 'py interpreter probe failed.' }
& $liveLauncher -m fusion.freeze
if ($LASTEXITCODE -ne 0) { throw 'Freeze failed; no request made.' }
$liveSecondInterpreter=& $liveLauncher -c 'import sys; print(sys.executable)'
if ($LASTEXITCODE -ne 0 -or $liveInterpreter -ne $liveSecondInterpreter) { throw 'Interpreter mismatch; no request.' }
Write-Host "Python interpreter: $liveInterpreter"
if ($Mock) {
    Write-Host 'MOCKED API ONLY: no real model calls or API charges.'
    & $liveLauncher -m fusion.live_demo --mock
    if ($LASTEXITCODE -ne 0) { throw 'Mocked server stopped with an error.' }
    return
}
if (-not $EnablePaid) {
    Write-Host 'Paid mode disabled. Browser cannot dispatch real model calls.'
    & $liveLauncher -m fusion.live_demo
    if ($LASTEXITCODE -ne 0) { throw 'Local server stopped with an error.' }
    return
}
$livePreviousKey=$env:OPENAI_API_KEY
$liveSecret=$null
try {
    $liveSecret=Read-Host 'OpenAI API key (masked; backend only; not saved)' -AsSecureString
    $env:OPENAI_API_KEY=[System.Net.NetworkCredential]::new('', $liveSecret).Password
    if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) { throw 'Empty key; no request.' }
    Write-Host 'Backend enabled; NO API call until explicit browser confirmation. ONE match, at most 6 calls/$0.25 estimated. No retries.'
    & $liveLauncher -m fusion.live_demo --enable-paid
    if ($LASTEXITCODE -ne 0) { throw 'Live server stopped. Preserve evidence/live-browser-v2 and inspect the status before another launch.' }
}
finally {
    if ($null -eq $livePreviousKey) { Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue }
    else { $env:OPENAI_API_KEY=$livePreviousKey }
    if ($null -ne $liveSecret) { $liveSecret.Dispose() }
    Remove-Variable liveSecret,livePreviousKey -ErrorAction SilentlyContinue
}
