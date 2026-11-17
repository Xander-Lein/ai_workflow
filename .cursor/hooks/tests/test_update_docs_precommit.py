"""Tests for update_docs_precommit hook."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = HOOKS_DIR.parents[1]
HOOK = HOOKS_DIR / "update_docs_precommit.py"
PY = Path(sys.executable)

sys.path.insert(0, str(HOOK.parent))
import update_docs_precommit as hook  # noqa: E402


def test_required_docs_hooks_folder() -> None:
    assert hook.required_docs_for_code({".cursor/hooks/deny_prod_write.py"}) == {"README.md"}


def test_doc_triggers() -> None:
    code = {"reports/src/marketing/foo/src/load.py"}
    missing = {"reports/src/marketing/foo/README.md"}
    triggers = hook.doc_triggers(code, missing)
    assert "reports/src/marketing/foo/src/load.py" in triggers["reports/src/marketing/foo/README.md"]


def test_hook_allows_non_commit() -> None:
    proc = subprocess.run(
        [str(PY), str(HOOK)],
        input=json.dumps({"command": "git status"}),
        text=True,
        capture_output=True,
        cwd=str(REPO_ROOT),
        check=False,
    )
    assert proc.returncode == 0
    assert json.loads(proc.stdout)["permission"] == "allow"
