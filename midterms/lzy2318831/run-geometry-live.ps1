# Preferred demonstration. Paid dispatch still requires browser match consent.
param([switch]$EnablePaid,[switch]$Mock)
$ErrorActionPreference='Stop'
if ($EnablePaid -and $Mock) { throw 'Choose paid or mock mode, never both.' }
Set-Location -LiteralPath $PSScriptRoot
function Resolve-GeometryPython {
    function Get-VerifiedGeometryPython {
        param($Executable,[switch]$PyLauncher)
        # Never coerce an array of Get-Command results into a command string.
        if ($Executable -isnot [string] -or [string]::IsNullOrWhiteSpace($Executable)) { return }
        if ($Executable -match '[\r\n]' -or $Executable -match '[\\/]Microsoft[\\/]WindowsApps[\\/]') { return }
        if (-not (Test-Path -LiteralPath $Executable -PathType Leaf)) { return }
        try {
            $probeArgs=@('-I','-c','import sys; print(sys.version_info.major, sys.version_info.minor); print(sys.executable)')
            if ($PyLauncher) { $probeArgs=@('-3')+$probeArgs }
            $probeOutput=@(& $Executable @probeArgs 2>$null)
            if ($LASTEXITCODE -ne 0 -or $probeOutput.Count -ne 2) { return }
            if ($probeOutput[0] -notmatch '^(\d+) (\d+)$') { return }
            $probeMajor=[int]$Matches[1]; $probeMinor=[int]$Matches[2]
            if ($probeMajor -lt 3 -or ($probeMajor -eq 3 -and $probeMinor -lt 11)) { return }
            $resolvedPython=([string]$probeOutput[1]).Trim()
            if (-not [System.IO.Path]::IsPathRooted($resolvedPython) -or
                -not (Test-Path -LiteralPath $resolvedPython -PathType Leaf)) { return }
            return [string](Get-Item -LiteralPath $resolvedPython).FullName
        }
        catch { return }
    }
    if (-not [string]::IsNullOrWhiteSpace($env:GEOMETRY_PYTHON)) {
        $verified=Get-VerifiedGeometryPython -Executable $env:GEOMETRY_PYTHON
        if ($verified) { return $verified }
        Write-Warning 'GEOMETRY_PYTHON is not a usable Python 3.11+ executable; checking installed launchers.'
    }
    foreach ($geometryName in @('py','python','python3')) {
        foreach ($geometryCommand in @(Get-Command $geometryName -CommandType Application -All -ErrorAction SilentlyContinue)) {
            $verified=Get-VerifiedGeometryPython -Executable $geometryCommand.Source -PyLauncher:($geometryName -eq 'py')
            if ($verified) { return $verified }
        }
    }
    throw 'No verified Python 3.11+ executable found. Set GEOMETRY_PYTHON to one executable path.'
}
$geometryPython=Resolve-GeometryPython
Write-Host "Verified Python 3.11+ interpreter: $geometryPython"
& $geometryPython -B -m fusion.freeze
if ($LASTEXITCODE -ne 0) { throw 'Freeze failed; server not started.' }
Write-Host 'Geometry-Assisted Live LLM v1 | OpenAI gpt-5.4-mini-2026-03-17'
Write-Host 'Main menu http://127.0.0.1:8835/ | live agent http://127.0.0.1:8839/'
Write-Host 'Per match: 6 requests/$0.25 estimated. Server total: 12 requests/$0.50 across freshly consented matches.'
if ($Mock) {
    Write-Host 'MOCK ONLY: synthetic selections, no API costs.'
    & $geometryPython -B -m fusion.geometry_live --mock
    if ($LASTEXITCODE -ne 0) { throw 'Mock server stopped with an error.' }
    return
}
if (-not $EnablePaid) {
    Write-Host 'Paid disabled; no request can be dispatched.'
    & $geometryPython -B -m fusion.geometry_live
    if ($LASTEXITCODE -ne 0) { throw 'Server stopped with an error.' }
    return
}
$geometryPreviousKey=$env:OPENAI_API_KEY
$geometrySecret=$null
try {
    $geometrySecret=Read-Host 'OpenAI API key (masked; backend only; not saved)' -AsSecureString
    $env:OPENAI_API_KEY=[System.Net.NetworkCredential]::new('', $geometrySecret).Password
    if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) { throw 'Empty key; no request.' }
    Write-Host 'Paid enabled; NO request before browser consent. One match: 6 requests/$0.25 estimate; no retries.'
    & $geometryPython -B -m fusion.geometry_live --enable-paid
    if ($LASTEXITCODE -ne 0) { throw 'Server failed; preserve evidence/live-browser-geometry-v1 before relaunching.' }
}
finally {
    if ($null -eq $geometryPreviousKey) { Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue }
    else { $env:OPENAI_API_KEY=$geometryPreviousKey }
    if ($null -ne $geometrySecret) { $geometrySecret.Dispose() }
    Remove-Variable geometrySecret,geometryPreviousKey -ErrorAction SilentlyContinue
}
