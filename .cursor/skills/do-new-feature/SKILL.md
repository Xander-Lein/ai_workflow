---
name: do-new-feature
description: >-
  Spec then split tester and implementer subagents: tester writes/runs tests and
  reports failures; implementer changes product code until GREEN. Then docs and checks.
---

# New feature

## Checklist

1. Confirm scope from chat or the Q&A recap of `/do-ask-questions`.
2. Short spec: inputs, outputs, edge cases, files in scope. Name public seams (skill `tdd`).
3. **Split roles** (two subagents when the Task tool is available; otherwise two sequential passes by the same agent, still reported separately):

   | Role | May edit | Must do |
   |------|----------|---------|
   | **Tester** | tests only (`test_*.py`, `**/tests/**`) | Add/adjust tests for acceptance criteria; run them; report RED/GREEN, failures, and recommendations. Do not change product code. |
   | **Implementer** | product code, not tests (unless the tester asked for a fixture-only fix) | Minimal code to satisfy the tester report. Do not weaken assertions to go green. |

4. Loop: Tester runs → if fail, Implementer fixes → Tester re-runs. Stop at GREEN or after three failed loops (then stop and report).
5. Docs required by host hooks / `AGENTS.md`.
6. Project checks (pytest, lint, CI entrypoint).
7. Report:

   | tests (tester) | code (implementer) | checks | open risks |
   |----------------|--------------------|--------|------------|

## Deep references

- `tdd` (`tests.md`, `mocking.md`): RED before GREEN, no tautological tests.
- `classify-change` when the host enables it.
- `worktree-isolation` for parallel or risky work.

## Rules

- Tester and implementer reports stay separate even if one agent plays both roles.
- Do not claim done without a tester run that is GREEN.
- Docs hook on commit: stage docs, do not skip the hook.
