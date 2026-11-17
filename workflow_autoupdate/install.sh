#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${HOME}/workflow_autoupdate"
REPO_URL="${1:-https://github.com/Xander-Lein/ai_workflow.git}"
BRANCH="${2:-main}"

mkdir -p "$TARGET"
rsync -a --exclude 'repo' "$HERE/" "$TARGET/"

CONFIG="${TARGET}/config.sh"
if [[ ! -f "$CONFIG" ]]; then
  cat >"$CONFIG" <<EOF
AI_WORKFLOW_REPO_URL='$REPO_URL'
AI_WORKFLOW_BRANCH='$BRANCH'
AI_WORKFLOW_CLONE_DIR="\${HOME}/workflow_autoupdate/repo"
EOF
  chmod 600 "$CONFIG"
fi

"$TARGET/sync.sh"

CRON_LINE="0 6 * * * ${TARGET}/sync.sh >> ${TARGET}/sync.log 2>&1"
(crontab -l 2>/dev/null | grep -vF "$TARGET/sync.sh" || true; echo "$CRON_LINE") | crontab -
echo "Cron installed: $CRON_LINE"