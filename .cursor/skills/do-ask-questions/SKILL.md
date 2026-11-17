---
name: do-ask-questions
description: >-
  Requirements interview before implementation. Research the repo first, then ask
  only via the AskQuestion tool. Recap Q&A in chat and offer /do-new-feature.
disable-model-invocation: true
---

# Requirements interview

## Checklist

- [ ] 1. Read the request and host constraints (`AGENTS.md`, rules).
- [ ] 2. **Research before ask.** Search the codebase for the feature area, existing contracts, and similar code. Drop any question the repo already answers. Note assumptions from code in one short paragraph (not a question).
- [ ] 3. Classify: feature, bug fix, refactor, documentation, or configuration. Note risk and required checks (use `classify-change` if the host enables it).
- [ ] 4. **Ask only through the AskQuestion tool** (client window with options). Do not ask the 3–5 questions as plain chat text. Batch related questions in one form (about 3–5). Topics: goal, inputs/outputs, edge cases, constraints, acceptance criteria. Skip anything already known.
- [ ] 5. After the user answers, **write a Q&A recap in the chat** as a table:

| # | Question | Answer |
|---|----------|--------|

- [ ] 6. Then either:
  - another AskQuestion round if blocking gaps remain, or
  - stop and offer **`/do-new-feature`** (recommended next step). Do not start implementation in this command.

## Rules

- Research first; questions second.
- Bug: reproduction, expected vs actual. Feature: contract and acceptance. Refactor: behavior that must stay the same.
- No main code before answers.
- Hand off to `/do-new-feature` only after the recap is in the chat.
