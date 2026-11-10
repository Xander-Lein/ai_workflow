#Requires -Version 5.1
<#
.SYNOPSIS
  Copy ai_workflow .cursor assets and hooks into a target repository.
.PARAMETER TargetRoot
  Project root (must contain .git).
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$TargetRoot
)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$AiRoot = Resolve-Path (Join-Path $Here "..")
$TargetRoot = (Resolve-Path $TargetRoot).Path

if (-not (Test-Path (Join-Path $TargetRoot ".git"))) {
    throw "TargetRoot must be a git repository: $TargetRoot"
}

$cursorSrc = Join-Path $AiRoot ".cursor"
$cursorDst = Join-Path $TargetRoot ".cursor"
$hooksSrc = Join-Path $AiRoot "hooks"
$hooksDst = Join-Path $TargetRoot ".cursor\hooks"

if (-not (Test-Path $cursorDst)) { New-Item -ItemType Directory -Path $cursorDst | Out-Null }
if (-not (Test-Path $hooksDst)) { New-Item -ItemType Directory -Path $hooksDst | Out-Null }

Copy-Item -Path (Join-Path $cursorSrc "*") -Destination $cursorDst -Recurse -Force
$hookFiles = @(
    "deny_secrets_read.py",
    "deny_prod_write.py",
    "update_docs_precommit.py"
)
foreach ($f in $hookFiles) {
    Copy-Item -Path (Join-Path $hooksSrc $f) -Destination (Join-Path $hooksDst $f) -Force
}

$example = Join-Path $hooksSrc "hooks.json.example"
$hooksJson = Join-Path $TargetRoot ".cursor\hooks.json"
if (-not (Test-Path $hooksJson)) {
    Copy-Item -Path $example -Destination $hooksJson -Force
    Write-Host "Created $hooksJson from example (review paths to python.exe)."
} else {
    Write-Host "Left existing $hooksJson unchanged."
}

Write-Host "Installed ai_workflow into $TargetRoot"
