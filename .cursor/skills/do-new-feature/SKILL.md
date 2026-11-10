---
name: do-new-feature
description: End-to-end feature delivery: spec, TDD, documentation, verification. Use after do-ask-questions or when requirements are explicit.
---

# New feature (single command)

## Checklist

1. Confirm scope and acceptance criteria (from chat or `/do-ask-questions`).
2. Write a brief spec: inputs, outputs, edge cases, files in scope.
3. Add or extend tests for acceptance criteria; run and expect RED.
4. Implement minimal code; iterate until tests GREEN.
5. Update README/docs required by project hooks or AGENTS.md.
6. Run project checks (pytest, lint, CI entrypoint).
7. Report: files changed, tests run, docs updated, open risks.

## Rules

- Do not skip tests for non-trivial behavior.
- Do not claim done without running relevant checks.
- If docs hook blocks commit, fix docs and stage before retrying `git commit`.
