# Agent chat links in tables

Conversation UUID: `d33d4ead-6bc9-471a-a267-77e784068787` (transcript under `~/.cursor/projects/<workspace>/agent-transcripts/<uuid>/`).

## Primary (verified in Cursor chat)

```markdown
[Ubuntu prod server](d33d4ead-6bc9-471a-a267-77e784068787)
```

Use a short **title** from the first user message or SearchConversations; link target is the **full UUID** without `.jsonl`.

## Optional Quick Open prefix

```markdown
[d33d4ead (Title)](command:workbench.action.quickOpen?%5B%22d33d4ead%22%5D)
```

Opens file picker with prefix prefilled — use only as secondary hint.

## Discover title + id

SearchConversations tool, or read the first line of the matching `agent-transcripts/<uuid>/*.jsonl`.