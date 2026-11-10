---
name: do-ask-questions
description: Requirements interview and change-risk classification before implementation. Use for any new feature, bug fix, refactor, or task with uncertain scope.
disable-model-invocation: true
---

# Requirements interview

## Checklist

- [ ] 1. Read the request, available context, and existing constraints.
- [ ] 2. See what is already known; avoid redundant questions.
- [ ] 3. Ask 3–5 questions about goal, inputs, outputs, edge cases, constraints, and acceptance criteria.
- [ ] 4. Classify the change: feature, bug fix, refactor, documentation, or configuration.
- [ ] 5. Assess risk, affected contracts, and mandatory verification.
- [ ] 6. Summarize understood requirements and open decisions for the user.
- [ ] 7. Stop and wait for answers; do not write main code before that.

## Rules

- Do not ask what the user or codebase already states clearly.
- For bug fixes: reproduction, expected vs actual behavior.
- For features: public contract and acceptance criteria.
- For refactors: behavior that must stay unchanged.
- Hand off to `/do-new-feature` after answers (not legacy plan/tdd/docs commands).
