#!/bin/bash
# Runs ledger/preflight.sh first (22 Nov; since P2 that is ship.sh --check, the ship's own build and gates): every breach in one pass, nothing queued on a breach.
# ship_request.sh "<label>" [--wait [seconds]] (21 Nov 2026): ask for a ship instead of running one. The request goes into
# ledger/ship_queue.jsonl and one runner (ledger/ship_queue.py) ships every pending request together, under the site lock.
#   ship_request.sh "what changed"          append and return at once (the runner is started if none is running)
#   ship_request.sh "what changed" --wait   block until the ship that carries this request ends; exit with its exit code
# A caller that already holds the site lock (SITE_LOCK_HELD) cannot wait on a runner that needs the same lock, so it ships directly.
set -euo pipefail
L="$(cd "$(dirname "$0")" && pwd)"; export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
LABEL="${1:?usage: ship_request.sh \"what changed\" [--wait [seconds]]}"
case "$LABEL" in auto:*) ;; *) bash "$L/preflight.sh" > /tmp/preflight_last.txt 2>&1 || { cat /tmp/preflight_last.txt; echo "ship_request: NOT QUEUED, a copy gate breached (22 Nov: one bad page refused whole bundles four times)"; exit 1; } ;; esac   # auto: requests change data only, the ship gates read them, and a preflight build each would double the builds
if [ -n "${SITE_LOCK_HELD:-}" ]; then exec bash "$L/ship.sh" "$LABEL"; fi
ID=$(python3 "$L/ship_queue.py" add "$LABEL")
nohup python3 "$L/ship_queue.py" run >> "$L/ship_queue_runner.log" 2>&1 < /dev/null &
echo "ship_request: queued $ID ($LABEL)"
if [ "${2:-}" = "--wait" ]; then exec python3 "$L/ship_queue.py" wait "$ID" --timeout "${3:-14400}"; fi
