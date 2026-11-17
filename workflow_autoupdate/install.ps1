#Requires -Version 5.1
<#
  One-time setup: install this folder to %USERPROFILE%\workflow_autoupdate,
  create config, run first sync, register daily Task Scheduler job.
#>
param(
    [string]$RepoUrl = "https://github.com/Xander-Lein/ai_workflow.git",
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Target = Join-Path $env:USERPROFILE "workflow_autoupdate"

if ($Here -ne $Target) {
    New-Item -ItemType Directory -Force -Path $Target | Out-Null
    Copy-Item -Path (Join-Path $Here "*") -Destination $Target -Recurse -Force
}

$ConfigPath = Join-Path $Target "config.ps1"
if (-not (Test-Path $ConfigPath)) {
    @"
`$AI_WORKFLOW_REPO_URL = '$RepoUrl'
`$AI_WORKFLOW_BRANCH = '$Branch'
`$AI_WORKFLOW_CLONE_DIR = Join-Path `$PSScriptRoot 'repo'
"@ | Set-Content -Path $ConfigPath -Encoding UTF8
}

& (Join-Path $Target "sync.ps1")

$TaskName = "AIWorkflowCursorSync"
$SyncScript = Join-Path $Target "sync.ps1"
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$SyncScript`""
$Trigger = New-ScheduledTaskTrigger -Daily -At 6:00AM
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Force | Out-Null
Write-Host "Registered scheduled task '$TaskName' (daily 06:00). First sync completed."