#Requires -Version 5.1
<#
  Pull (or clone) ai_workflow and merge .cursor into the user profile .cursor folder.
  Does not overwrite an existing hooks.json unless -OverwriteHooksJson.
#>
param(
    [switch]$OverwriteHooksJson
)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigPath = Join-Path $Here "config.ps1"
if (-not (Test-Path $ConfigPath)) {
    Write-Error "Missing $ConfigPath - copy from config.example and set AI_WORKFLOW_*."
}

. $ConfigPath

if (-not $AI_WORKFLOW_CLONE_DIR) {
    $AI_WORKFLOW_CLONE_DIR = Join-Path $Here "repo"
}

$UserCursor = Join-Path $env:USERPROFILE ".cursor"
New-Item -ItemType Directory -Force -Path $UserCursor | Out-Null
New-Item -ItemType Directory -Force -Path $AI_WORKFLOW_CLONE_DIR | Out-Null

if (Test-Path (Join-Path $AI_WORKFLOW_CLONE_DIR ".git")) {
    git -C $AI_WORKFLOW_CLONE_DIR fetch origin --prune
    git -C $AI_WORKFLOW_CLONE_DIR checkout $AI_WORKFLOW_BRANCH
    git -C $AI_WORKFLOW_CLONE_DIR pull --ff-only origin $AI_WORKFLOW_BRANCH
} else {
    git clone --branch $AI_WORKFLOW_BRANCH $AI_WORKFLOW_REPO_URL $AI_WORKFLOW_CLONE_DIR
}

$SrcCursor = Join-Path $AI_WORKFLOW_CLONE_DIR ".cursor"
if (-not (Test-Path $SrcCursor)) {
    Write-Error "No .cursor in cloned repo: $SrcCursor"
}

$robocopyArgs = @(
    $SrcCursor,
    $UserCursor,
    "/E",
    "/NFL", "/NDL", "/NJH", "/NJS", "/nc", "/ns", "/np"
)
if (-not $OverwriteHooksJson) {
    $robocopyArgs += "/XF", "hooks.json"
}
$null = & robocopy @robocopyArgs
# robocopy exit 0-7 = success
if ($LASTEXITCODE -ge 8) {
    throw "robocopy failed with exit $LASTEXITCODE"
}

$ExampleHooks = Join-Path $SrcCursor "hooks\hooks.json.example"
$DestHooks = Join-Path $UserCursor "hooks.json"
if (-not (Test-Path $DestHooks) -and (Test-Path $ExampleHooks)) {
    Copy-Item $ExampleHooks $DestHooks
}

# Command stubs duplicated skills in the slash menu. Drop leftovers from older syncs.
$retiredCommands = @(
    "do-analytics.md", "do-ask-questions.md", "do-branch-to-dev.md", "do-dev-to-prod.md",
    "do-development.md", "do-new-feature.md", "do-review.md", "do-system_design.md", "do-ux_ui.md"
)
$commandsDir = Join-Path $UserCursor "commands"
foreach ($name in $retiredCommands) {
    $path = Join-Path $commandsDir $name
    if (Test-Path $path) { Remove-Item $path -Force }
}

Write-Host "Synced .cursor to $UserCursor from $AI_WORKFLOW_CLONE_DIR"