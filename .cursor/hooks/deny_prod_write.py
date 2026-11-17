#!/usr/bin/env python3
"""Deny writes and mutating shell into a prod clone; reads are allowed."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

_DEFAULT_PROD_RE = r"(?i)(?:^|[/\\])prod(?:[/\\]|$)"
PROD_PATH_RE = re.compile(os.environ.get("PROD_PATH_REGEX", _DEFAULT_PROD_RE))

WRITE_TOOLS = frozenset(
    {"Write", "StrReplace", "Delete", "EditNotebook", "WriteFile", "DeleteFile"}
)

SHELL_MUTATE = re.compile(
    r"(>\s*|Out-File|Set-Content|Add-Content|Move-Item|Copy-Item|New-Item|tee\s+|"
    r"git\s+(commit|push|reset|merge|rebase|checkout))",
    re.I,
)

CD_RE = re.compile(r"\b(cd|Set-Location)\b", re.I)


def _deny(msg: str) -> dict:
    return {
        "permission": "deny",
        "user_message": msg,
        "agent_message": msg,
    }


def _allow() -> dict:
    return {"permission": "allow"}


def targets_prod(text: str) -> bool:
    if not text.strip():
        return False
    return bool(PROD_PATH_RE.search(text.replace("\\", "/")))


def _extract_paths(payload: dict) -> list[str]:
    paths: list[str] = []
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    if isinstance(tool_input, dict):
        for key in ("path", "file_path", "target_notebook", "file", "cwd", "working_directory"):
            val = tool_input.get(key)
            if isinstance(val, str) and val.strip():
                paths.append(val.strip())
    for key in ("path", "file_path", "command", "cwd"):
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            paths.append(val.strip())
    return paths


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        print(json.dumps(_allow()))
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps(_allow()))
        return 0
    if not isinstance(payload, dict):
        print(json.dumps(_allow()))
        return 0

    event = str(
        payload.get("hook_event_name") or payload.get("event") or payload.get("type") or ""
    )
    tool = str(payload.get("tool_name") or payload.get("tool") or payload.get("name") or "")
    command = str(
        payload.get("command")
        or (payload.get("tool_input") or {}).get("command")
        or ""
    )

    if event == "beforeShellExecution" or (command and not tool):
        if targets_prod(command) and (SHELL_MUTATE.search(command) or CD_RE.search(command)):
            msg = "deny_prod_write: mutating shell in prod clone is denied (read-only prod)."
            print(json.dumps(_deny(msg), ensure_ascii=False))
            return 0
        print(json.dumps(_allow()))
        return 0

    for path in _extract_paths(payload):
        if not targets_prod(path):
            continue
        try:
            resolved = Path(path).expanduser().resolve().as_posix()
        except OSError:
            resolved = path.replace("\\", "/")
        if targets_prod(resolved) and (tool in WRITE_TOOLS or event == "preToolUse"):
            msg = f"deny_prod_write: write denied for prod path ({path})."
            print(json.dumps(_deny(msg), ensure_ascii=False))
            return 0

    print(json.dumps(_allow()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
