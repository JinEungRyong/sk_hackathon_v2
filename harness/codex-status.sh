#!/usr/bin/env bash
# codex-status.sh - show whether each Codex CLI session is working or waiting.
#
# Usage:
#   ./codex-status.sh            # one-shot
#   watch -n 2 ./codex-status.sh # refresh every 2 seconds
#
# Env:
#   CODEX_HOME   Codex home dir (default: ~/.codex)
#   STALL_SEC    seconds without log activity before a running turn is
#                flagged as "maybe waiting for approval" (default: 30)
#   RECENT_MIN   fallback: when no running codex process is found, show
#                rollout files modified within this many minutes (default: 30)

set -u

SESS_DIR="${CODEX_HOME:-$HOME/.codex}/sessions"
STALL_SEC="${STALL_SEC:-30}"
RECENT_MIN="${RECENT_MIN:-30}"
now=$(date +%s)

mtime() { stat -c %Y "$1" 2>/dev/null || stat -f %m "$1"; }

# 1) Map running codex processes -> open rollout-*.jsonl files.
pairs=""
if command -v lsof >/dev/null 2>&1; then
  pairs=$(lsof -c codex 2>/dev/null | awk '$NF ~ /rollout-.*\.jsonl$/ {print $2, $NF}' | sort -u)
fi

# 2) Fallback: recently modified rollout files (PID unknown).
if [ -z "$pairs" ]; then
  pairs=$(find "$SESS_DIR" -name 'rollout-*.jsonl' -mmin -"$RECENT_MIN" 2>/dev/null | sed 's/^/- /')
fi

if [ -z "$pairs" ]; then
  echo "No active Codex sessions found under $SESS_DIR"
  exit 0
fi

printf '%-8s %-28s %6s  %s\n' PID STATUS AGE CWD
echo "$pairs" | while read -r pid f; do
  [ -f "$f" ] || continue
  age=$(( now - $(mtime "$f") ))
  cwd=$(grep -m1 -o '"cwd":"[^"]*"' "$f" | cut -d'"' -f4)
  last=$(grep -oE '"type":"(task_started|task_complete|turn_aborted)"' "$f" | tail -n1 | cut -d'"' -f4)

  case "$last" in
    task_started)
      if [ "$age" -lt "$STALL_SEC" ]; then
        status="WORKING"
      else
        status="WAITING? (approval/long cmd)"
      fi ;;
    task_complete|turn_aborted) status="IDLE (waiting for input)" ;;
    *)                          status="IDLE (no turn yet)" ;;
  esac

  printf '%-8s %-28s %5ss  %s\n' "$pid" "$status" "$age" "${cwd:-?}"
done
