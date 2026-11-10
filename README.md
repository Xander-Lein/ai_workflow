# AI Workflow for Cursor

Portable rules, skills, slash commands, and **project hooks** for agent-driven development.

Based on a five-step loop ([overview video](https://www.youtube.com/watch?v=1tCfHLFnXSw)): clarify → plan & implement with tests → document → review → ship (branch / dev / prod).

## Install

```powershell
git clone https://github.com/Xander-Lein/ai_workflow.git
cd your-project
..\ai_workflow\scripts\install.ps1 -TargetRoot (Get-Location)
```

This copies:

- `.cursor/commands`, `.cursor/rules`, `.cursor/skills`
- Hook scripts into `.cursor/hooks/` (secrets, prod write guard, docs pre-commit)
- Creates `.cursor/hooks.json` from [`hooks/hooks.json.example`](hooks/hooks.json.example) if missing

Point `command` entries in `hooks.json` at your venv Python. See [`docs/hooks.md`](docs/hooks.md).

## Slash commands

| Command | Role |
|---------|------|
| `/do-ask-questions` | Requirements interview and change classification |
| `/do-new-feature` | Plan → TDD (RED/GREEN) → docs sync → summary (replaces separate plan/tdd/docs commands) |
| `/do-review` | Code review, security-sensitive diff, improvement gaps |
| `/do-branch-to-dev` | Branch hygiene and merge request toward dev |
| `/do-dev-to-prod` | Release checklist template (override in your project for prod specifics) |

Domain skills (`/do-analytics`, `/do-ux_ui`, …) and `programs/*` (Tableau, GTM, YouTrack) are reserved for future knowledge packs.

## Definition of Done

A task is done only when:

- Acceptance criteria are met
- Tests were written against the spec and pass after implementation
- Relevant README/docs are staged (enforced by `update_docs_precommit` on agent `git commit` when hooks are enabled)
- Complex work used branches or worktrees where appropriate

## Repo layout

```text
ai_workflow/
├── README.md
├── WORKFLOW.md
├── docs/hooks.md
├── hooks/                    # install → .cursor/hooks/
├── scripts/install.ps1
└── .cursor/
    ├── commands/
    ├── rules/
    └── skills/
```

## Attribution

Skills `implement-spec`, `classify-change`, `code-review`, and `tdd` are derived from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT, Copyright (c) 2026 Matt Pocock). See LICENSE in upstream skill copies.
