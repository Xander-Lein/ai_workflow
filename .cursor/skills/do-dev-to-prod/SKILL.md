---
name: do-dev-to-prod
description: >-
  Promote integration branch to production: sync dev, show dev-not-on-prod table,
  push, MR/PR to master/main, merge, then run the repo post-merge deploy script
  when present. Never delete dev or master/main. Do not pull a sibling clone.
disable-model-invocation: true
---

# /do-dev-to-prod

Host-specific paths, credentials, and deploy commands stay in the project repository.

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
- [ ] 8. Post-merge deploy script, or a same-named project skill; otherwise skip deploy
- [ ] 9. Tables: landed on prod; remaining dev-not-prod
```

## 3. Stop window

Before push/MR, show:

| commits | summary |

from `git log origin/<prod>..origin/dev --oneline`. User may abort.

## 8. After merge

Run a deploy only from the repository that was just merged.

1. On Windows, if `scripts/post_merge_deploy.ps1` exists at the repo root, run it. On Linux or macOS, if `scripts/post_merge_deploy.sh` exists, run it. A non-zero exit stops the skill.
2. Otherwise, if this repository has its own skill with the same command name and that skill describes a deploy, follow that skill.
3. Otherwise do not deploy. Do not `git pull` a sibling clone by default.

Product names, hosts, and project-specific launchers stay in the project repository, not in this skill.

## 9. After merge

**Landed on prod** — table of commits, summary, and follow-up. Write it only after merge and after step 8 succeeded or was skipped because no deploy was defined.