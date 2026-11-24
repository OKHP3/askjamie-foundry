[CmdletBinding()]
param(
    [switch]$FailOnDrift
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$replitPath = Join-Path $repoRoot '.replit'
$replitText = Get-Content -Raw -LiteralPath $replitPath
$currentChannel = [regex]::Match($replitText, 'channel\s*=\s*"(?<channel>[^"]+)"').Groups['channel'].Value

if ([string]::IsNullOrWhiteSpace($currentChannel)) {
    Write-Error 'No Replit Nix channel was found in .replit.'
}

$releaseNotes = (Invoke-WebRequest -Uri 'https://nixos.org/manual/nixos/stable/release-notes' -UseBasicParsing).Content
$latestMatch = [regex]::Match($releaseNotes, 'Release (?<release>\d+\.\d+)')
if (-not $latestMatch.Success) {
    Write-Error 'Unable to determine the latest stable NixOS release.'
}

$latestRelease = $latestMatch.Groups['release'].Value
$currentReleaseMatch = [regex]::Match($currentChannel, '(?<release>\d+_\d+)')
$currentRelease = if ($currentReleaseMatch.Success) { $currentReleaseMatch.Groups['release'].Value.Replace('_', '.') } else { '' }

Write-Output "Replit channel: $currentChannel"
Write-Output "Latest NixOS stable release: $latestRelease"

if ($currentRelease -and ([version]$currentRelease -lt [version]$latestRelease)) {
    $message = "Technology drift detected: .replit uses stable-$($currentRelease.Replace('.', '_')), while NixOS reports $latestRelease as the latest stable release. Review Replit channel compatibility before updating the channel."
    Write-Warning $message
    if ($env:GITHUB_ACTIONS -eq 'true') {
        "drift=true" | Out-File -FilePath $env:GITHUB_OUTPUT -Append -Encoding utf8
        "message=$message" | Out-File -FilePath $env:GITHUB_OUTPUT -Append -Encoding utf8
    }
    if ($FailOnDrift) { exit 2 }
} elseif ($env:GITHUB_ACTIONS -eq 'true') {
    "drift=false" | Out-File -FilePath $env:GITHUB_OUTPUT -Append -Encoding utf8
}

