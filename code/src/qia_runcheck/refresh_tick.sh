#!/bin/sh
# refresh_tick.sh (16 Nov 2026): tick-bus rider beside ibm_mirror.py (every 5 ticks). Rebuilds the public QIA record index from the saved records and
# polls.jsonl (last_read, stamp_returned, read gaps per processor) and pushes only changed files to the site KV, so the QIA MCP tools can tell a fresh
# read from an old one (the referee MOVES 16 Nov: coverage before flags). Exit code is the push's; failures land in refresh.log.
cd ~/forge/qia_runcheck || exit 1
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
python3 -I build_index.py >> refresh.log 2>&1 && python3 -I push_index.py >> refresh.log 2>&1
