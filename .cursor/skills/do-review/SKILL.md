---
name: do-review
description: >-
  Review a diff on three axes — Standards, Spec, and Security (mandatory update-mode
  pass). Use code-review plus host do-security-review when present.
disable-model-invocation: true
---

# Review

## Checklist

1. Pin base/head (branch, SHA, or uncommitted scope). Record the diff command.
2. **Standards + Spec:** skill `code-review` (parallel when possible).
3. **Security (mandatory, update mode):** every `/do-review`. Follow [references/security-pass.md](references/security-pass.md).
   - If `.cursor/skills/do-security-review/SKILL.md` exists in the **host repo**, read it and run that checklist as the security subprocess. Put findings only under Security.
   - Else use the reference checklist (OWASP-lite for SQL, secrets, path traversal in jobs).
4. **Dependencies:** `pip-audit` / lockfile audit **only** when the trigger in the reference matches. Otherwise state `deps: not triggered`.
5. If the host enables it, consult `classify-change` for high-risk paths (does not replace the security pass).
6. Run project tests and linters.
7. Report with **three** headings. Do not merge axes.

## Report

### Standards

Style, structure, duplication, project conventions.

### Spec

Requirements, regressions, callers, root cause for bugfixes.

### Security

Update-mode findings (severity, evidence, remediation). Note whether host `do-security-review` ran. Note `deps: not triggered` or audit result.

End with checks run, open risks, and whether **blocking** security findings exist (blocks `/do-branch-to-dev` until fixed or explicitly waived by the user).

## Rules

- Security is not optional and not folded into Standards.
- Do not print secret values.
- Cap unproductive rounds at three, then change approach.
- Absence of findings is not proof of safety — say what was in scope.
