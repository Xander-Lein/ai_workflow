# Cursor hooks

Install with [`scripts/install.ps1`](../scripts/install.ps1). Hooks live in the target repo under `.cursor/hooks/`.

| Hook | Event | Purpose |
|------|--------|---------|
| `deny_secrets_read` | `beforeReadFile` (Read) | Block `secrets.env` / `.env`; allow `*.example` |
| `deny_prod_write` | write tools + shell | Block writes and mutating shell under `.../prod/`; reads allowed |
| `update_docs_precommit` | shell `git commit` | Deny agent commit if required docs are not staged |

## Docs gate

`update_docs_precommit` is **gate-only**: it does not edit files. It maps staged code paths to required docs (report READMEs, `AGENTS.md`, etc.). Deny message lists which staged files triggered each doc.

Skip: `[skip-docs]` in the commit message or `SKIP_DOCS_HOOK=1` in the command.

Environment overrides:

| Variable | Default |
|----------|---------|
| `DOCS_AGENTS_FILE` | `AGENTS.md` |
| `DOCS_CI_FILE` | `docs/hooks.md` |
| `PROD_PATH_REGEX` | path segment `prod/` |

## Tests

```powershell
python -m pytest hooks/tests -q
```
