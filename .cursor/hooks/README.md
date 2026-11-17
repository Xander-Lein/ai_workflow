# Cursor hooks (ai_workflow)

Installed under `%USERPROFILE%\.cursor\hooks\` (Windows) or `~/.cursor/hooks/` (Linux) by [`workflow_autoupdate`](../workflow_autoupdate/sync.ps1).

| Script | Event | Role |
|--------|--------|------|
| `deny_secrets_read` | `beforeReadFile` | Block real `.env` / `secrets.env` |
| `deny_prod_write` | writes + shell | Block mutation under `*/prod/` |
| `update_docs_precommit` | `git commit` | Require staged docs for staged code |

Wire in `.cursor/hooks.json` (see `hooks.json.example`). Tests: `py -m pytest .cursor/hooks/tests -q` from repo root.