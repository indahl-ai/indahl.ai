#!/bin/bash
# insured_flip.sh (25 Nov 2026): one-shot. Hiscox cover starts 26 Nov; the footer line is computed at build time, so both sites must be
# rebuilt after midnight to drop "from 26 November 2026". launchd (com.heuremen.insured-flip) runs this at 00:10 on 26 Nov, then it unloads
# itself. If either ship fails, alerts_check's insurance:stale-line still rings, so a miss cannot sit silent.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"; B=~/forge; LOG=$B/sagar/pipeline/pipe.log
[ "$(date +%Y%m%d)" -ge 20261126 ] || exit 0
bash $B/ledger/ship_qia.sh "insured line: cover in force from 26 Nov" >> $B/ledger/insured_flip.log 2>&1 || echo "$(date '+%Y-%m-%dT%H:%M:%S') RING: INSURED FLIP FAILED: ship_qia" >> $LOG
bash $B/ledger/ship_request.sh "URGENT: insured line: cover in force from 26 Nov" --wait 3600 >> $B/ledger/insured_flip.log 2>&1 || echo "$(date '+%Y-%m-%dT%H:%M:%S') RING: INSURED FLIP FAILED: indahl.ai ship" >> $LOG
python3 $B/watch/alerts_check.py >/dev/null 2>&1
launchctl bootout gui/$(id -u)/com.heuremen.insured-flip 2>/dev/null; mv ~/Library/LaunchAgents/com.heuremen.insured-flip.plist ~/Library/LaunchAgents/com.heuremen.insured-flip.plist.gone-20261126 2>/dev/null
