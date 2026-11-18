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


def test_ci_doc_uses_testing_and_ci_when_present(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "testing-and-ci.md").write_text("ci\n", encoding="utf-8")
    assert hook.required_docs_for_code({"scripts/ci_checks.py"}, repo_root=tmp_path) == {
        "docs/testing-and-ci.md"
    }
    assert hook.required_docs_for_code({".githooks/pre-commit"}, repo_root=tmp_path) == {
        "docs/testing-and-ci.md"
    }


def test_repo_policy_drives_required_docs_and_triggers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    policy_dir = tmp_path / "scripts"
    policy_dir.mkdir()
    (policy_dir / "docs_precommit_policy.py").write_text(
        "def required_docs_for_code(code_paths, repo_root=None):\n"
        "    if any(path.endswith('load.py') for path in code_paths):\n"
        "        return {'CUSTOM.md'}\n"
        "    return set()\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("DOCS_POLICY_FILE", raising=False)
    hook._POLICY_CACHE.clear()
    code = {"reports/src/marketing/foo/src/load.py"}
    assert hook.required_docs_for_code(code, repo_root=tmp_path) == {"CUSTOM.md"}
    triggers = hook.doc_triggers(code, {"CUSTOM.md"}, repo_root=tmp_path)
    assert triggers["CUSTOM.md"] == ["reports/src/marketing/foo/src/load.py"]


def test_docs_policy_file_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    policy = tmp_path / "custom_policy.py"
    policy.write_text(
        "def required_docs_for_code(code_paths, repo_root=None):\n    return {'ENV.md'}\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("DOCS_POLICY_FILE", str(policy))
    hook._POLICY_CACHE.clear()
    assert hook.required_docs_for_code({"a.py"}, repo_root=tmp_path / "repo") == {"ENV.md"}


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
