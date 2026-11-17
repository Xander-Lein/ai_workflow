---
name: do-development
description: Planned general development pack with backend, frontend, and devops references. On /do-development, read matching reference files and apply them with do-new-feature.
---

# /do-development (planned)

**Status:** content TBD — see [references/](references/).

| Area | File |
|------|------|
| Backend | [references/backend.md](references/backend.md) |
| Frontend | [references/frontend.md](references/frontend.md) |
| DevOps | [references/devops.md](references/devops.md) |

When invoked:

1. Detect topic (backend / frontend / devops) from the user message.
2. Read the matching reference if it has content; merge with host AGENTS.md.
3. Execute via `/do-new-feature` unless the user asked for design-only (`/do-system_design`).