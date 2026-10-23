---
name: orchestrate
description: Decompose complex development work into independent agent-sized subtasks with contracts, dependencies, ownership, and validation. Use when a task spans multiple modules or can be parallelized.
disable-model-invocation: true
---

# Orchestrate

Для сложной задачи:

1. Раздели работу по границам модулей, а не по случайным файлам.
2. Для каждой подзадачи укажи цель, входы, выходы, зависимости и критерии проверки.
3. Выдели критический путь и задачи, которые можно выполнять параллельно.
4. Назначь отдельный validation step для интеграции результатов.
5. Согласуй изменения общих контрактов до запуска параллельной работы.

Не запускай параллельные задачи, если они редактируют один и тот же хрупкий участок без изоляции.
