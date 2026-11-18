"""Copy to scripts/docs_precommit_policy.py in a project repo.

The user hook ~/.cursor/hooks/update_docs_precommit.py loads this file when
it exists (or when DOCS_POLICY_FILE points at it). Do not add a second docs
hook in the project's .cursor/hooks.json.

required_docs_for_code(code_paths, repo_root=...) must return repo-relative
doc paths that have to be staged with that code. doc_triggers in the hook
calls this same function per path.
"""

from __future__ import annotations

from pathlib import Path


def required_docs_for_code(
    code_paths: set[str],
    *,
    repo_root: Path | None = None,
) -> set[str]:
    del repo_root
    required: set[str] = set()
    for path in code_paths:
        if path.endswith(".py") and not path.endswith(".md"):
            required.add("README.md")
    return required
