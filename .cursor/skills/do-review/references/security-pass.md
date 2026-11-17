# Security pass (update mode)

Runs on **every** `/do-review`. Scope: **added/modified** code in the pinned diff, plus callers that the change can affect. Do not full-scan the repo unless the user asks for a full audit.

## Host override

If the workspace has `.cursor/skills/do-security-review/SKILL.md` (myfin and similar), **read and follow that skill** as the security subprocess. Merge its findings into `## Security`. Do not print secrets.

If that file is absent, use this checklist.

## Always (diff)

- Secrets in code, logs, errors, fixtures, commits (names only in the report).
- Authn/authz and trust-boundary changes.
- Injection: SQL, shell, path, deserialization.
- Unsafe file paths and command construction.

## OWASP-lite (analytics / jobs / ETL)

Apply when the diff touches SQL, `jobs/`, report pipelines, file paths, or env loading:

| Check | Look for |
|-------|----------|
| SQL injection | string-built SQL, unsanitized identifiers |
| Secrets | tokens in SQL, logs, Tableau publish, Telegram |
| Path traversal | user or config paths joined into `reports/data`, parquet, workbook paths |
| Command injection | shell built from job args |
| Sensitive data | PII columns written to git or logs |

## Dependencies (`pip-audit`) — trigger only

Run `pip-audit` (or the host lockfile audit) **only if** the diff changes `pyproject.toml`, `requirements*.txt`, `uv.lock`, or the user / classification marks supply-chain risk. Otherwise skip and note `deps: not triggered`.

## Report rows

Each finding: severity, file, evidence (no secret values), remediation.
