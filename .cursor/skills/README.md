# Skills layout

## Active (slash / workflow)

| Skill | Command |
|-------|---------|
| `do-ask-questions` | `/do-ask-questions` |
| `do-new-feature` | `/do-new-feature` |
| `do-review` | `/do-review` |
| `do-branch-to-dev` | `/do-branch-to-dev` |
| `do-dev-to-prod` | `/do-dev-to-prod` |

## Shared libraries (used by active skills, no public command)

| Skill | Used by |
|-------|---------|
| `classify-change` | `/do-ask-questions`, high-risk paths in `/do-review` |
| `code-review` | `/do-review` (Standards + Spec axes) |
| `tdd` | `/do-new-feature` (RED/GREEN reference) |
| `worktree-isolation` | parallel / risky work per `ai-workflow` rule |

## Planned domain packs

`consider-ux_ui`, `consider-analytics`, `consider-system_design`, `consider-development` (`/consider-*`, backend/frontend/devops references) — stubs until content is added.