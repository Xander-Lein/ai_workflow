# Cursor hooks (ai_workflow)

Installed under `%USERPROFILE%\.cursor\hooks\` (Windows) or `~/.cursor/hooks/` (Linux) by [`workflow_autoupdate`](../workflow_autoupdate/sync.ps1).

| Script | Event | Role |
|--------|--------|------|
| `deny_secrets_read` | `beforeReadFile` | Block real `.env` / `secrets.env` |
| `deny_prod_write` | writes + shell | Block mutation under `*/prod/` |
| `update_docs_precommit` | `git commit` | Require staged docs for staged code |

Install the user `hooks.json` from `hooks.json.example`. Commands point at `%USERPROFILE%\.cursor\hooks\`, not at a project `.cursor/hooks/` path.

Do **not** register a second docs hook in a project `hooks.json`. Repo-specific rules belong in `scripts/docs_precommit_policy.py` (template: [`scripts/docs_precommit_policy.example.py`](../../scripts/docs_precommit_policy.example.py)). The hook loads that file, or `DOCS_POLICY_FILE`, and uses it for both the deny list and `doc_triggers`. If `docs/testing-and-ci.md` exists, it is the default CI doc unless `DOCS_CI_FILE` is set.

Tests: `py -m pytest .cursor/hooks/tests -q` from repo root.