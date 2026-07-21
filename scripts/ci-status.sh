#!/bin/sh
# ci-status.sh — wait for the Woodpecker verdict on a commit (default: HEAD).
#
# Red pipelines are otherwise silent (a strict-build failure hid for 28h while
# the site served a stale deploy — ADR-001 §11a.5 gotcha 10). Run this after
# every push: it polls the Codeberg commit-status API and exits 0 on success,
# 1 on failure, 2 on timeout.
#
# Usage: scripts/ci-status.sh [commit-ish] [timeout-seconds]

set -eu
REPO_API="https://codeberg.org/api/v1/repos/TAPPaaS/Documentation"
SHA=$(git rev-parse "${1:-HEAD}")
TIMEOUT="${2:-900}"
ELAPSED=0

while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
  STATE=$(curl -sS --max-time 15 "$REPO_API/commits/$SHA/status" 2>/dev/null \
    | python3 -c 'import json,sys; print(json.load(sys.stdin).get("state",""))' 2>/dev/null || echo "")
  case "$STATE" in
    success) echo "CI green on ${SHA%????????????????????????????????}"; exit 0 ;;
    failure|error) echo "CI FAILED on ${SHA%????????????????????????????????} — see commit status on codeberg.org"; exit 1 ;;
    *) sleep 20; ELAPSED=$((ELAPSED + 20)) ;;
  esac
done
echo "CI still pending after ${TIMEOUT}s"; exit 2
