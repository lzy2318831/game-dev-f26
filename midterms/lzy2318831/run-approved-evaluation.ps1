# Exact user-approved official run. No automatic retries or evidence overwrite.
param([switch]$Offline)

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$evaluationPythonLauncher = (Get-Command py -CommandType Application -ErrorAction Stop).Source

function Get-EvaluationInterpreter {
    $evaluationProbe = & $evaluationPythonLauncher -c 'import sys; print(sys.executable)'
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($evaluationProbe)) {
        throw 'The py launcher could not identify its Python interpreter; no evaluation started.'
    }
    return [System.IO.Path]::GetFullPath(([string]$evaluationProbe).Trim())
}

$evaluationFreezeInterpreter = Get-EvaluationInterpreter
Write-Host "Python interpreter: $evaluationFreezeInterpreter"
$evaluationOutput = Join-Path $PSScriptRoot 'evidence/live-mini-approved-01'
if (-not $Offline -and (Test-Path -LiteralPath $evaluationOutput)) {
    throw 'An official run directory already exists. Preserve it; inspect its audit before any further calls. Do not delete or switch directories to reset the approved limits.'
}

$evaluationPreviousKey = $env:OPENAI_API_KEY
$evaluationSecret = $null
try {
    & $evaluationPythonLauncher -m fusion.freeze
    if ($LASTEXITCODE -ne 0) { throw 'Frozen game verification failed; no evaluation started.' }
    $evaluationRunInterpreter = Get-EvaluationInterpreter
    if (-not [string]::Equals($evaluationFreezeInterpreter, $evaluationRunInterpreter, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw 'py resolved to different interpreters for freeze and evaluation; no evaluation started.'
    }
    Write-Host 'PASS: freeze and evaluation use the same Python interpreter.'
    if ($Offline) {
        # No --live, credential prompt, output directory, or provider call.
        $evaluationPlanJson = & $evaluationPythonLauncher -m fusion.llm_eval --provider openai --model gpt-5.4-mini-2026-03-17 --memory observation_only --opponent baseline
        if ($LASTEXITCODE -ne 0) { throw 'Offline evaluation plan failed.' }
        $evaluationPlan = ($evaluationPlanJson -join "`n") | ConvertFrom-Json
        if ($evaluationPlan.kind -ne 'plan_only_not_live' -or $evaluationPlan.max_calls -ne 72 -or $evaluationPlan.live_matches -ne 12 -or $evaluationPlan.matched_baseline_controls -ne 12) {
            throw 'Offline plan does not match the approved scope.'
        }
        Write-Host 'PASS: offline plan, 12 live matches / 12 controls / maximum 72 calls. No API calls made.'
        return
    }
    if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) {
        $evaluationSecret = Read-Host 'OpenAI API key (masked; not saved)' -AsSecureString
        $env:OPENAI_API_KEY = [System.Net.NetworkCredential]::new('', $evaluationSecret).Password
    }
    if ([string]::IsNullOrWhiteSpace($env:OPENAI_API_KEY)) {
        throw 'No API key supplied; no evaluation started.'
    }

    Write-Host 'Approved official evaluation: observation-only, 12 LLM matches, 12 Geometric controls, maximum 72 model calls, $5 local estimated budget.'
    & $evaluationPythonLauncher -m fusion.llm_eval --live --approve-paid --provider openai --model gpt-5.4-mini-2026-03-17 --memory observation_only --opponent baseline --budget-usd 5 --max-calls 72 --output evidence/live-mini-approved-01
    if ($LASTEXITCODE -ne 0) {
        throw 'Evaluation stopped. Preserve all files; do not retry or reset limits without inspecting the recorded attempts.'
    }
    Write-Host 'Run finished. Inspect manifest.json, comparison.csv, summary.json and calls.jsonl in evidence/live-mini-approved-01. Failed/not-run trials remain recorded.'
}
finally {
    if ($null -eq $evaluationPreviousKey) {
        Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
    }
    else { $env:OPENAI_API_KEY = $evaluationPreviousKey }
    if ($null -ne $evaluationSecret) { $evaluationSecret.Dispose() }
    Remove-Variable evaluationSecret, evaluationPreviousKey -ErrorAction SilentlyContinue
}
