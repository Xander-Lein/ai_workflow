#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${HERE}/config.sh"
if [[ ! -f "$CONFIG" ]]; then
  echo "Missing $CONFIG — copy from config.example" >&2
  exit 1
fi
# shellcheck source=/dev/null
source "$CONFIG"

: "${AI_WORKFLOW_REPO_URL:?}"
: "${AI_WORKFLOW_BRANCH:=main}"
CLONE_DIR="${AI_WORKFLOW_CLONE_DIR:-${HERE}/repo}"
USER_CURSOR="${HOME}/.cursor"

mkdir -p "$USER_CURSOR" "$CLONE_DIR"

if [[ -d "${CLONE_DIR}/.git" ]]; then
  git -C "$CLONE_DIR" fetch origin --prune
  git -C "$CLONE_DIR" checkout "$AI_WORKFLOW_BRANCH"
  git -C "$CLONE_DIR" pull --ff-only origin "$AI_WORKFLOW_BRANCH"
else
  git clone --branch "$AI_WORKFLOW_BRANCH" "$AI_WORKFLOW_REPO_URL" "$CLONE_DIR"
fi

SRC="${CLONE_DIR}/.cursor"
[[ -d "$SRC" ]] || { echo "No .cursor in clone" >&2; exit 1; }

rsync -a --delete \
  --exclude 'hooks.json' \
  "$SRC/" "$USER_CURSOR/"

EXAMPLE="${SRC}/hooks/hooks.json.example"
DEST_HOOKS="${USER_CURSOR}/hooks.json"
if [[ ! -f "$DEST_HOOKS" && -f "$EXAMPLE" ]]; then
  cp "$EXAMPLE" "$DEST_HOOKS"
fi

echo "Synced .cursor to $USER_CURSOR"