#!/usr/bin/env python3
"""Deny reading secret env files (beforeReadFile)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import PurePosixPath

DENIED_BASENAMES = frozenset({".env", "secrets.env"})


def _deny(msg: str) -> dict:
    return {
        "permission": "deny",
        "user_message": msg,
        "agent_message": msg,
    }


def _allow() -> dict:
    return {"permission": "allow"}


def _normalize_path(raw: str) -> str:
    return raw.strip().replace("\\", "/")


def _is_denied_secret_path(path: str) -> bool:
    norm = _normalize_path(path)
    if not norm:
        return False
    if norm.endswith("secrets.env.example") or norm.endswith(".env.example"):
        return False
    name = PurePosixPath(norm).name
    if name in DENIED_BASENAMES:
        return True
    if re.search(r"(^|/)shared/secrets\.env$", norm, re.I):
        return True
    if re.search(r"(^|/)reports/.+/\.env$", norm, re.I):
        return True
    return False


def _extract_read_path(payload: dict) -> str | None:
    for key in ("file_path", "path", "file"):
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    if isinstance(tool_input, dict):
        for key in ("file_path", "path", "file", "target_file"):
            val = tool_input.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
    args = payload.get("arguments") or {}
    if isinstance(args, dict):
        for key in ("file_path", "path", "file"):
            val = args.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
    return None


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

    path = _extract_read_path(payload)
    if path and _is_denied_secret_path(path):
        msg = (
            f"deny_secrets_read: read denied ({path}). "
            "Use *.env.example; load real values at runtime without printing secrets."
        )
        print(json.dumps(_deny(msg), ensure_ascii=False))
        return 0

    print(json.dumps(_allow()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
