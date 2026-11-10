#!/usr/bin/env python3
"""Cursor beforeShellExecution: require docs in the same commit as staged code (gate only)."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

NOISE_RE = re.compile(
    r"(^|/)(usage/logs/|usage/output/|reports/data/|__pycache__/|\.pytest_cache/)|"
    r"\.(csv|twbx|xlsx|hyper|log|pyc)$",
    re.I,
)

GIT_COMMIT_RE = re.compile(r"\bgit(\.exe)?\b", re.I)
COMMIT_WORD_RE = re.compile(r"\bcommit\b", re.I)
COMMIT_EXCLUDE_RE = re.compile(r"\bcommit-(tree|graph)\b", re.I)
GIT_ADD_RE = re.compile(r"\bgit\s+add\s+([^;&|]+)", re.I)
COMMIT_ALL_RE = re.compile(r"\bcommit\b[^;&|]*(-a|--all)\b|(-a|--all)[^;&|]*\bcommit\b", re.I)

AGENTS_DOC = os.environ.get("DOCS_AGENTS_FILE", "AGENTS.md")
CI_DOC = os.environ.get("DOCS_CI_FILE", "docs/hooks.md")
HOOKS_DOC = os.environ.get("DOCS_HOOKS_FILE", CI_DOC)


def _allow() -> dict:
    return {"permission": "allow"}


def _deny(user_message: str, agent_message: str) -> dict:
    return {
        "permission": "deny",
        "user_message": user_message,
        "agent_message": agent_message,
    }


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".git").is_dir():
            return parent
    return Path.cwd()


def normalize_path(raw: str) -> str:
    path = raw.strip().replace("\\", "/").strip('"').strip("'")
    if path.startswith("./"):
        path = path[2:]
    return path.lstrip("/")


def is_git_commit_command(command: str) -> bool:
    if not GIT_COMMIT_RE.search(command):
        return False
    if not COMMIT_WORD_RE.search(command):
        return False
    return not COMMIT_EXCLUDE_RE.search(command)


def should_skip_docs(command: str) -> bool:
    return "[skip-docs]" in command or "SKIP_DOCS_HOOK=" in command


def is_noise_path(path: str) -> bool:
    return bool(NOISE_RE.search(normalize_path(path)))


def is_test_path(path: str) -> bool:
    norm = normalize_path(path)
    name = norm.rsplit("/", 1)[-1]
    return "/tests/" in f"/{norm}/" or (name.startswith("test_") and name.endswith(".py"))


def paths_from_git_add(command: str) -> set[str]:
    paths: set[str] = set()
    for match in GIT_ADD_RE.finditer(command):
        for token in match.group(1).split():
            if token.startswith("-"):
                continue
            paths.add(normalize_path(token))
    return paths


def run_git(args: list[str], repo_root: Path) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.stdout


def git_cached_paths(repo_root: Path) -> set[str]:
    out = run_git(["diff", "--cached", "--name-only"], repo_root)
    return {normalize_path(line) for line in out.splitlines() if line.strip()}


def git_status_paths(repo_root: Path) -> set[str]:
    out = run_git(["status", "--porcelain"], repo_root)
    paths: set[str] = set()
    for line in out.splitlines():
        if len(line) < 4:
            continue
        path_part = line[3:].strip().strip('"')
        if " -> " in path_part:
            path_part = path_part.split(" -> ", 1)[-1].strip('"')
        paths.add(normalize_path(path_part))
    return paths


def git_modified_tracked(repo_root: Path) -> set[str]:
    out = run_git(["diff", "--name-only"], repo_root)
    cached = run_git(["diff", "--cached", "--name-only"], repo_root)
    combined = {normalize_path(line) for line in (out + cached).splitlines() if line.strip()}
    return combined


def git_unstaged_paths(repo_root: Path, doc_paths: set[str]) -> set[str]:
    unstaged: set[str] = set()
    for doc in sorted(doc_paths):
        if run_git(["diff", "--name-only", "--", doc], repo_root).strip():
            unstaged.add(doc)
    return unstaged


def command_implies_staging(command: str) -> bool:
    if GIT_ADD_RE.search(command):
        return True
    return bool(COMMIT_ALL_RE.search(command))


def commit_file_set(command: str, repo_root: Path) -> set[str]:
    cached = git_cached_paths(repo_root)
    paths = set(cached)
    paths |= paths_from_git_add(command)
    if COMMIT_ALL_RE.search(command):
        paths |= git_modified_tracked(repo_root)
    if command_implies_staging(command) and not cached:
        paths |= git_status_paths(repo_root)
    return paths


def meaningful_code_paths(paths: set[str]) -> set[str]:
    code: set[str] = set()
    for path in paths:
        norm = normalize_path(path)
        if not norm or is_noise_path(norm) or norm.endswith(".md"):
            continue
        code.add(norm)
    return code


def required_docs_for_code(code_paths: set[str]) -> set[str]:
    required: set[str] = set()
    for path in code_paths:
        required |= required_docs_for_single_path(normalize_path(path))
    return required


def required_docs_for_single_path(norm: str) -> set[str]:
    required: set[str] = set()
    if not norm or is_noise_path(norm) or norm.endswith(".md"):
        return required
    if is_test_path(norm):
        return required
    if norm.startswith("knowledge-base/data/") or norm.startswith("reports/data/"):
        return required

    if norm.startswith("hooks/") or norm.startswith(".cursor/hooks/"):
        required.add(HOOKS_DOC)
        return required

    if norm in {"compose.yaml", "Dockerfile", "pyproject.toml", "uv.lock"} or norm.startswith(
        "docker/"
    ):
        required.add(AGENTS_DOC)
        required.add(CI_DOC)
        return required

    if norm.startswith("shared/core_transforms/"):
        required.add(AGENTS_DOC)
        return required

    if norm.startswith("reports/src/template/"):
        required.add("reports/src/template/README.md")
        return required

    report = re.match(r"reports/(?:src/)?([^/]+)/([^/]+)/", norm)
    if report:
        category, slug = report.group(1), report.group(2)
        if category not in {"src", "data"} and slug != "src":
            prefix = "reports/src" if norm.startswith("reports/src/") else "reports"
            required.add(f"{prefix}/{category}/{slug}/README.md")
        return required

    if norm.startswith("jobs/"):
        required.add("jobs/README.md")
        required.add(AGENTS_DOC)
        return required

    if norm.startswith("shared/"):
        required.add(AGENTS_DOC)
        return required

    if norm.startswith("alerting/"):
        required.add("alerting/README.md")
        return required

    script = re.match(r"knowledge-base/scripts/([^/]+)/", norm)
    if script:
        required.add(f"knowledge-base/scripts/{script.group(1)}/README.md")
        return required

    if norm.startswith(".gitlab-ci.yml") or norm == "scripts/ci_checks.py":
        required.add(CI_DOC)
    return required


def doc_triggers(code_paths: set[str], missing_docs: set[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {doc: [] for doc in missing_docs}
    for path in sorted(code_paths):
        norm = normalize_path(path)
        for doc in required_docs_for_single_path(norm):
            if doc in out:
                out[doc].append(norm)
    return {k: v for k, v in out.items() if v}


def is_test_only_commit(code_paths: set[str]) -> bool:
    meaningful = {p for p in code_paths if not is_test_path(p)}
    return not meaningful


def evaluate_commit(command: str, repo_root: Path) -> dict | None:
    if not is_git_commit_command(command):
        return None
    if should_skip_docs(command):
        return None

    commit_files = commit_file_set(command, repo_root)
    code_paths = meaningful_code_paths(commit_files)
    if not code_paths or is_test_only_commit(code_paths):
        return None

    required = required_docs_for_code(code_paths)
    if not required:
        return None

    staged_docs = {p for p in required if p in commit_files}
    missing = required - staged_docs
    if not missing:
        return None

    unstaged = git_unstaged_paths(repo_root, missing)
    to_write = missing - unstaged
    to_stage = missing & unstaged
    triggers = doc_triggers(code_paths, missing)

    lines: list[str] = [
        "update_docs_precommit: stage documentation updates for this commit.",
    ]
    if triggers:
        lines.append("")
        lines.append("Required because of staged code:")
        for doc in sorted(triggers):
            sample = ", ".join(triggers[doc][:3])
            if len(triggers[doc]) > 3:
                sample += f", +{len(triggers[doc]) - 3} more"
            lines.append(f"- {doc} <- {sample}")

    if to_write:
        lines.append("")
        lines.append("Create or update:")
        for doc in sorted(to_write):
            lines.append(f"- {doc}")

    if to_stage:
        lines.append("")
        lines.append("Already changed locally; git add:")
        for doc in sorted(to_stage):
            lines.append(f"- git add {doc}")

    lines.append("")
    lines.append("Retry commit. Skip: [skip-docs] in message or SKIP_DOCS_HOOK=1.")

    message = "\n".join(lines)
    return _deny(message, message)


def _extract_command(payload: dict) -> str:
    cmd = payload.get("command")
    if isinstance(cmd, str) and cmd.strip():
        return cmd.strip()
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    if isinstance(tool_input, dict):
        inner = tool_input.get("command")
        if isinstance(inner, str) and inner.strip():
            return inner.strip()
    return ""


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

    command = _extract_command(payload)
    if not command:
        print(json.dumps(_allow()))
        return 0

    repo_root = _find_repo_root()
    result = evaluate_commit(command, repo_root)
    print(json.dumps(result if result else _allow(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
