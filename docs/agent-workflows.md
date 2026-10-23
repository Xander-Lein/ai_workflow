# Практики Anthropic и OpenAI для agent workflow

Этот документ фиксирует, какие идеи положены в основу rules и skills репозитория.
Ссылки ведут на официальные материалы и нужны для повторной проверки рекомендаций.

## Anthropic

- [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) —
  проверка должна быть многослойной: тесты и build, свежий review-контекст,
  отдельная security-проверка, risk-based human approval и быстрый rollback.
  Повторные review нужно ограничивать, а findings подтверждать и дедуплицировать.
- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) —
  начинать с простейшего решения; для фиксированного процесса использовать
  chaining, routing, parallelization или evaluator-optimizer, а agent loop
  оставлять для открытых задач с feedback от среды и stopping conditions.
- [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) —
  сохранять прогресс, делать маленькие независимые срезы, оставлять clean state
  и использовать Git как точку восстановления между сессиями.
- [Create custom subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents) —
  давать субагенту узкую роль, отдельный контекст, минимальные права и
  структурированный результат; дорогой координатор может делегировать рутинную
  разведку более дешёвым моделям.
- [Extend Claude with skills](https://docs.anthropic.com/en/docs/claude-code/skills) —
  повторяемые процедуры и чеклисты должны жить в skills, а не разрастаться в
  постоянных инструкциях проекта.
- [Code Review](https://docs.anthropic.com/en/docs/claude-code/code-review) —
  параллельные специализированные reviewers должны передавать findings на
  отдельную проверку, после чего их нужно дедуплицировать и ранжировать.
- [Effective context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) —
  держать в контексте только нужные указатели, сохранять детали во внешних
  файлах и не перегружать основной контекст логами и исследованиями.

## OpenAI

- [Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration) —
  использовать handoff, когда специалист должен принять дальнейшее решение, и
  `agents as tools`, когда координатор должен сохранить ownership финального ответа.
  Специалисты должны иметь узкие роли и короткие описания.
- [Multi-agent](https://developers.openai.com/api/docs/guides/agents-api/multi-agent) —
  независимые задачи можно запускать параллельно с ограничением concurrency;
  координация должна явно собирать результаты и состояние субагентов.
- [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) —
  сначала проверять отдельные traces, затем переносить повторяемые сценарии в
  datasets и eval runs.
- [Trace grading](https://developers.openai.com/api/docs/guides/trace-grading/) —
  оценивать не только ответ, но и выбор tools, handoffs, нарушения policy и
  регрессии в маршрутизации.
- [Agents](https://developers.openai.com/api/docs/guides/agents) —
  выбирать runtime и уровень оркестрации по нужной степени контроля, а не
  добавлять multi-agent слой автоматически.

## Правила, перенесённые в этот репозиторий

1. Дорогая модель выступает координатором только для сложных задач.
2. Субагент получает узкую задачу, входные данные, границы файлов, критерии
   приёмки и команду проверки.
3. Независимые задачи можно выполнять параллельно; общие или конфликтующие
   файлы требуют последовательной работы или worktree.
4. Субагент не считается завершившим работу, пока не вернул изменения,
   проверки, ограничения и ссылку на commit либо понятный результат read-only
   исследования.
5. Координатор проверяет результат самостоятельно и не принимает вывод
   субагента без фактических тестов.
6. Если задача хорошо описывается фиксированными шагами, используется workflow,
   а не автономная цепочка агентов.
7. Для дорогих или рискованных изменений обязательны свежий review-контекст,
   лимит review-раундов, человеческая точка принятия решения и план rollback.
