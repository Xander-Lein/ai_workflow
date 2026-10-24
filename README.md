# AI Workflow for Cursor

Переиспользуемый набор правил, skills и slash-команд для разработки с AI-агентом.

Workflow основан на пяти этапах:

1. Опрос требований.
2. Спецификация и план.
3. TDD-цикл: RED → GREEN.
4. Оркестрация независимых подзадач.
5. Изоляция через ветки и Git worktrees.

## Установка

Скопируйте папку `.cursor` в корень проекта. После этого Cursor сможет использовать общее правило, skills и команды.

```text
your-project/
└── .cursor/
    ├── commands/
    ├── rules/
    └── skills/
```

## Команды

### Текущие команды

- `/do-ask-questions` — опрос требований и классификация изменения.
- `/do-plan-and-specs` — спецификация, task graph, план и отдельная ветка.
- `/do-tdd-loop` — тесты, RED, минимальная реализация и GREEN.
- `/do-review` — review требований и стандартов, валидация набора и проверки.
- `/do-branch-to-master` — подтверждённые commit, push, MR, merge и production pull.
- `/do-documentation` — подготовка и проверка документации.
- `/do-security-review` — отдельная проверка security-sensitive изменений.
- `/do-release` — release-checklist, который запускается после merge в `master`.
- `/do-roadmap` — анализ развития проекта, фич, рефакторинга и приоритизированный план с чекбоксами.

### Будущие команды

Пока нет.

Подробные внутренние skills Matt Pocock (`tdd`, `code-review`, `classify-change`, `implement-spec`) сохранены как строительные блоки, но не требуют отдельных пользовательских команд.

## Definition of Done

Задача считается готовой только когда:

- выполнены критерии приёмки;
- автотесты написаны до реализации;
- тесты запущены после изменений и проходят;
- сложные подзадачи изолированы;
- итог проверен по исходному плану.

## Структура

```text
.cursor/
├── commands/                 # Короткие slash-команды
├── rules/                    # Общее правило для агента
└── skills/                   # Подробные переиспользуемые workflows
```

## Субагенты

Сложные задачи координирует сильная модель, а независимые части можно передавать
субагентам с более дешёвой моделью. Это не включается автоматически: сначала
определи границы задачи, права субагента, критерии приёмки и способ проверки.
Координатор обязан самостоятельно проверить результат и ограничивать число
параллельных задач и review-раундов.

## Источники

- [Anthropic: How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/)
- [Anthropic: Building effective AI agents](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic: Create custom subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [OpenAI: Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration)
- [OpenAI: Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)

## Attribution

Skills `implement-spec`, `classify-change`, `code-review` и `tdd` основаны на
материалах Matt Pocock из [mattpocock/skills](https://github.com/mattpocock/skills).
Сохраните это уведомление при копировании соответствующих skills:

```text
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Принцип работы

Не просите агента «просто написать код». Сначала превратите идею в проверяемый контракт, затем используйте тесты как executable specification и только после этого реализуйте решение.
