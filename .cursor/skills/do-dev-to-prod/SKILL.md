---
name: do-dev-to-prod
description: >-
  Promote integration branch to production: sync dev, show dev-not-on-prod table,
  push, MR/PR to master/main, merge, optional prod pull. Never delete dev or master/main.
  Override in host repo for paths, KB, and GitLab scripts.
disable-model-invocation: true
---

# /do-dev-to-prod

Template — **override** in the host repository for real prod roots and `gitlab-mr.ps1`.

## Branch guards

- Work on **`dev`** (or host integration branch).
- **Never delete** `dev`, `master`, or `main`.
- MR/PR **target** is `master` / `main` / host prod branch — **not** `dev` again.

## Checklist

```
- [ ] 1. checkout dev + ff-only pull
- [ ] 2. Credentials GitLab then GitHub (silent if OK)
- [ ] 3. Table: commits on dev not on prod (STOP window)
- [ ] 4. Local CI
- [ ] 5. Push dev or feat branch if protected
- [ ] 6. MR/PR → master/main + approve + merge
- [ ] 7. Remote CI only if runner available
- [ ] 8. Optional prod clone pull (host paths only)
- [ ] 9. Tables: landed on prod; remaining dev-not-prod
```

## 3. Stop window

Before push/MR, show:

| commits | summary |

from `git log origin/<prod>..origin/dev --oneline`. User may abort.

## 9. After merge

**Landed on prod** — same table shape as host `dev-to-prod` skill («Залито на прод»).

Reference implementation: myfin `.cursor/skills/dev-to-prod/SKILL.md` (KB sync, `config.toml`, `gitlab-mr.ps1`, prod pull).