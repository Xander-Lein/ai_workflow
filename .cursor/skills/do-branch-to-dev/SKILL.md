---
name: do-branch-to-dev
description: >-
  Sync feature branch, local CI, commit scope for this chat only, push, GitLab
  MR or GitHub PR into dev, auto-merge when allowed, report pending work elsewhere.
  Never delete dev or master/main. Use for /do-branch-to-dev.
disable-model-invocation: true
---

# /do-branch-to-dev

Language: follow the user. Do not print credentials or secret values.

## Branch guards

- **Never delete** remote or local branches named `dev`, `master`, or `main`.
- After merge, delete **only** the feature source branch (e.g. `feat/*`) if the host policy allows it.

## Checklist

```
- [ ] 1. Sync branch (create if missing — AskQuestion)
- [ ] 2. Credentials GitLab then GitHub (silent if OK)
- [ ] 3. Commit only changes tied to this chat
- [ ] 4. Table: other uncommitted work (default excluded from commit)
- [ ] 5. Security gate (update-mode review; no blocking Security findings)
- [ ] 6. Local CI (pre-push) per host repo
- [ ] 7. Push source branch
- [ ] 8. Open MR/PR → dev + approve + merge (CI: local required; remote if runner up)
- [ ] 9. Delete feature branch only (not dev/master/main)
- [ ] 10. Tables: shipped to dev; on dev not on prod
```

## 1. Branch sync

In the **host git repository** (not ai_workflow):

- `git fetch origin --prune`, inspect `git branch --show-current`, `git status`, `git log -5 --oneline`.
- Expected: a **feature** branch for this task (often created during `/do-new-feature`).
- On **`dev` / `master` / `main`** with task changes still uncommitted — suggest checking out or creating `feat/<slug>`, not committing directly to integration branches unless the user explicitly asked.

If no suitable feature branch exists: **AskQuestion** — title **«Ветка под эту задачу не обнаружена, создать новую?»** — options: create `feat/<slug>` and checkout / stay on current branch / cancel. Prefer nudging `/do-new-feature` for greenfield work.

## 2. Credentials

1. If host has `.cursor/skills/dev-to-prod/gitlab-mr.ps1` or project check script — run **check** first.
2. Else `gh auth status` (GitHub).
3. On failure: stop with setup instructions (no tokens in chat). On success: **say nothing**.

## 3. Commits (this chat only)

- Scope files using: stated paths in the thread, recent edits in the conversation summary, and `git diff` / `git status`.
- Do **not** commit unrelated dirty files unless the user explicitly lists them in this message.
- Respect host `docs_pre_commit` / `update_docs_precommit` on agent `git commit`.
- Forbidden patterns follow the **host** project (e.g. secrets, local `config.toml`).

## 4. Other work table (informational)

Group remaining dirty or unpushed work **by branch**; default **not** included in this commit.

Columns:

| open_chat | git_branch | git_commits | short_description |

**open_chat** — markdown citation link (primary, works in Cursor chat): `[Title](full-uuid-without-.jsonl)` — see [agent-links.md](references/agent-links.md).

Populate `short_description` from `git diff --stat`, last commit subject, or transcript snippet. If attribution is unknown, use branch name + file list.

List unpushed commits: `git log origin/dev..HEAD --oneline` (adjust default integration branch via host config).

## 5. Security gate

Before push, run `/do-review` security update mode on the commits about to ship (skill `do-review`, axis **Security** only is enough if Standards/Spec were just done in this chat).

- If `.cursor/skills/do-security-review/SKILL.md` exists, that subprocess is mandatory (same as `do-review`).
- **Blocking** Security findings (high/critical, or host skill says human approval): stop. Do not push until fixed or the user explicitly waives them in this chat.
- Record one line: `security: clear` or `security: waived by user`.

## 6. Local CI before push

Run the host pre-push entrypoint (e.g. `python scripts/ci_checks.py pre-push`). Fail → stop, no push.

## 7. Push

`git push -u origin HEAD` or named feature branch. If `dev` is protected, push `feat/<slug>` as MR source.

## 8. MR/PR → `dev`

- **GitLab first** (project script create → approve → merge) if check passed in step 2.
- Else **GitHub** `gh pr create --base dev` (or `main` if that is integration — read host docs).

Merge policy:

- Default: create + approve + merge when permitted.
- **Do not** wait on remote CI if no runner / pipeline unavailable (as host dev-to-prod skill).
- If runner is available and project requires it, wait for green before merge.

## 9. Cleanup

Delete **only** the merged feature branch (local + remote). **Do not** delete `dev`, `master`, `main`.

## 10. Report tables

**Shipped to dev** (this promotion):

| commits | summary | follow-up |

**On dev, not on prod** (ahead of prod branch):

`git fetch origin` then `git log origin/<prod-branch>..origin/dev --oneline` (branch names from host).

---

Project-specific GitLab scripts, protected paths, and prod clone paths live in **host overrides** (e.g. myfin `dev-to-prod`), not in this upstream skill.