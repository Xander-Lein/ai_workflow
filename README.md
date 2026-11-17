# AI Workflow for Cursor

User-level delivery of commands, skills, rules, and hooks for agent-driven development.

## Layout (this repo)

```text
ai_workflow/
├── .cursor/              # synced to the user profile (see below)
├── workflow_autoupdate/  # install + daily git pull → sync
├── LICENSE
└── README.md
```

## Install (recommended)

### Windows

From a clone of this repo:

```powershell
.\workflow_autoupdate\install.ps1
```

This copies scripts to `%USERPROFILE%\workflow_autoupdate\`, writes `config.ps1`, runs the first sync, and registers **Task Scheduler** job `AIWorkflowCursorSync` (daily 06:00).

Manual sync: `%USERPROFILE%\workflow_autoupdate\sync.ps1`

### Linux

```bash
chmod +x workflow_autoupdate/install.sh workflow_autoupdate/sync.sh
./workflow_autoupdate/install.sh
```

Installs `~/workflow_autoupdate/`, first sync, and a **cron** entry (06:00).

### Sync target

```
Windows: %USERPROFILE%\.cursor\
Linux:   ~/.cursor/
```

Contents come from this repo's `.cursor/` (robocopy/rsync). Existing `hooks.json` is kept unless you pass `-OverwriteHooksJson` on Windows.

**Project repos** still use their own `.cursor/hooks.json` and overrides (e.g. `dev-to-prod/gitlab-mr.ps1` in myfin). User-level skills apply globally; project skills merge per Cursor discovery rules.

## Slash commands

| Command | Role |
|---------|------|
| `/do-ask-questions` | Requirements + risk before code |
| `/do-new-feature` | Spec → TDD → docs → verification |
| `/do-review` | Diff review |
| `/do-branch-to-dev` | Feature → **dev** (GitLab first, else GitHub) |
| `/do-dev-to-prod` | **dev** → **master/main** (template; override in host) |

## Hooks

Under `.cursor/hooks/` — see [`.cursor/hooks/README.md`](.cursor/hooks/README.md). Example wiring: [`.cursor/hooks/hooks.json.example`](.cursor/hooks/hooks.json.example).

Tests: `py -m pytest .cursor/hooks/tests -q`

## Definition of Done

Acceptance criteria met, relevant tests green, docs staged when hooks are enabled, no false "done" without checks.

## Attribution

Skills derived from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) where noted in skill headers.