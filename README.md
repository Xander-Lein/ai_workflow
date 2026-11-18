# AI Workflow for Cursor

User-level delivery of skills, rules, and hooks for agent-driven development. Slash menu entries are the skill folder names. There is no `.cursor/commands/` copy: that duplicated every `/do-*` item.

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

## Slash skills

| Command | Role |
|---------|------|
| `/do-ask-questions` | Requirements + risk before code |
| `/do-new-feature` | Spec → TDD → docs → verification |
| `/do-review` | Diff review |
| `/do-branch-to-dev` | Feature → **dev** (GitLab first, else GitHub) |
| `/do-dev-to-prod` | **dev** → **master/main** (template; override in host) |

### Запланировано (domain packs)

| Command | Skill | Note |
|---------|--------|------|
| `/consider-ux_ui` | `consider-ux_ui` | UX/UI — stub in git |
| `/consider-analytics` | `consider-analytics` | Analytics — stub |
| `/consider-system_design` | `consider-system_design` | Architecture — stub |
| `/consider-development` | `consider-development` | Backend / frontend / devops — stub references |

При вызове агент должен учитывать знания из соответствующего skill по мере заполнения; пока контент TBD — связка с `/do-new-feature` или `/do-ask-questions`.

Shared helpers (no slash): `classify-change`, `code-review`, `tdd`, `worktree-isolation` — см. [`.cursor/skills/README.md`](.cursor/skills/README.md).

## Hooks

Under `.cursor/hooks/` — see [`.cursor/hooks/README.md`](.cursor/hooks/README.md). Example user wiring: [`.cursor/hooks/hooks.json.example`](.cursor/hooks/hooks.json.example). The docs hook command is the profile script:

```text
python %USERPROFILE%\.cursor\hooks\update_docs_precommit.py
```

A project `hooks.json` must not add another docs hook. Put repo rules in `scripts/docs_precommit_policy.py` (copy [`scripts/docs_precommit_policy.example.py`](scripts/docs_precommit_policy.example.py)). If the repo has `docs/testing-and-ci.md`, that file is the default CI doc.

Tests: `py -m pytest .cursor/hooks/tests -q`

## Definition of Done

Acceptance criteria met, relevant tests green, docs staged when hooks are enabled, no false "done" without checks.

## Attribution

Skills derived from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) where noted in skill headers.