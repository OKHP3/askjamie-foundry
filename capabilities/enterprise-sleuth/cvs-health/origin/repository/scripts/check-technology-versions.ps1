[CmdletBinding()]
param(
    [switch]$FailOnDrift
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $root 'ask-jamie!/manifest.json'
$agentPath = Join-Path $root 'ask-jamie!/declarativeAgent_0.json'

function Get-PageText([string]$Uri) {
    $html = Get-PageHtml $Uri
    $text = $html -replace '<script[\s\S]*?</script>', ' ' -replace '<style[\s\S]*?</style>', ' ' -replace '<[^>]+>', ' '
    [System.Net.WebUtility]::HtmlDecode($text) -replace '\s+', ' '
}

function Get-PageHtml([string]$Uri) {
    (Invoke-WebRequest -Uri $Uri -UseBasicParsing).Content
}

$manifest = Get-Content -Raw $manifestPath | ConvertFrom-Json
$agent = Get-Content -Raw $agentPath | ConvertFrom-Json
$drift = [System.Collections.Generic.List[string]]::new()

$manifestSchemaVersion = [regex]::Match([string]$manifest.'$schema', '/teams/v([^/]+)/').Groups[1].Value
$teamsPage = Get-PageHtml 'https://learn.microsoft.com/en-us/microsoft-365/extensibility/schema/?view=m365-app-1.30'
$latestTeamsVersion = [regex]::Match($teamsPage, 'default_moniker[\s\S]{0,200}?m365-app-(1\.\d+)', 'IgnoreCase').Groups[1].Value

$agentPage = Get-PageText 'https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-manifest-1.7'
$latestAgentVersion = [regex]::Match($agentPage, 'latest\s+version\s+of\s+the\s+declarative\s+agent\s+manifest\s+schema\s+is\s+version\s+([0-9.]+)', 'IgnoreCase').Groups[1].Value

Write-Output "Teams manifest schema: current=$manifestSchemaVersion latest=$latestTeamsVersion"
Write-Output "Declarative Agent schema: current=$($agent.version) latest=v$latestAgentVersion"
Write-Output 'CommonMark reference: latest=0.31.2 (manual inventory entry)'

if ($manifestSchemaVersion -ne $latestTeamsVersion) {
    $drift.Add("Teams manifest schema drift: repository=$manifestSchemaVersion latest=$latestTeamsVersion")
}
if ([string]$agent.version -ne "v$latestAgentVersion") {
    $drift.Add("Declarative Agent schema drift: repository=$($agent.version) latest=v$latestAgentVersion")
}

if ($drift.Count -gt 0) {
    Write-Warning ($drift -join [Environment]::NewLine)
    if ($FailOnDrift) { exit 1 }
}
else {
    Write-Output 'No actionable schema drift detected.'
}
