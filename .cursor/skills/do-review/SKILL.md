---
name: do-review
description: Review diff against spec and repo standards; run checks; report findings. Use skill code-review for the two-axis pass.
disable-model-invocation: true
---

# Review

## Checklist

1. Pin base/head (branch, SHA, or uncommitted scope).
2. Run skill **`code-review`**: Standards + Spec in parallel where possible.
3. For high-risk areas, consult **`classify-change`** if the host project enables it.
4. Run project tests and linters (e.g. `ci_checks`, pytest).
5. Report: requirements findings, standards findings, checks run, open risks, human approval if needed.

## Rules

- Do not claim review complete without running available checks.
- Cap unproductive review rounds; after three, change approach.
- Separate requirements vs standards findings.