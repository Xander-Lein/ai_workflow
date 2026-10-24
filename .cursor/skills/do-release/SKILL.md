---
name: do-release
description: Prepare a safe release after merge into master by checking CI, commit scope, release notes, rollback, and production actions. Use only after an explicitly approved merge.
disable-model-invocation: true
---

# Release

## Чеклист

- [ ] 1. Подтвердить, что MR/PR влит в целевую ветку и зафиксировать commit SHA.
- [ ] 2. Проверить CI, обязательные review и отсутствие незакрытых blocking findings.
- [ ] 3. Составить release notes: что добавлено, изменено, исправлено и затронуто.
- [ ] 4. Определить требуемые миграции, настройки, ручные действия и обратимый rollback.
- [ ] 5. Проверить, что production pull выполняется из правильного каталога и ветки.
- [ ] 6. Передать результат в `do-branch-to-master`; production-действия выполнять только после подтверждения.
- [ ] 7. После pull сверить commit, статус рабочей директории и фактический результат.
- [ ] 8. Сформировать сообщение по шаблону promotion workflow.

## Ограничения

- Не считать merge успешным релизом без проверки CI и commit SHA.
- Не выполнять deploy, production pull, миграции или изменение настроек без явного разрешения.
- Если rollback не определён, остановиться до production-действий.
