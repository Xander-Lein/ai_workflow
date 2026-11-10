# Workflow

## Command chain

1. **`/do-ask-questions`** — scope, risks, acceptance criteria. Stop until the human answers.
2. **`/do-new-feature`** — turn answers into a short spec, write failing tests, implement to GREEN, update docs, list verification.
3. **`/do-review`** — standards + security + “what to improve next”.
4. **`/do-branch-to-dev`** / **`/do-dev-to-prod`** — git flow (project-specific secrets stay in the host repo).

Do **not** use removed legacy commands (`do-plan-and-specs`, `do-tdd-loop`, `do-documentation`); their behavior lives inside `/do-new-feature`.

## Hooks (optional but recommended)

| Concern | Hook |
|---------|------|
| Secrets | `deny_secrets_read` |
| Prod clone | `deny_prod_write` (writes blocked; reads OK) |
| Docs in commit | `update_docs_precommit` |

## Orchestration

Use a strong model as coordinator for large features; delegate isolated subtasks with explicit acceptance tests. Prefer git worktrees for parallel or risky work ([Cursor worktrees](https://cursor.com/docs/configuration/worktrees)).
