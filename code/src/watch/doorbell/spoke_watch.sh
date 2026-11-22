#!/bin/bash
# spoke_watch.sh N (22 Nov 2026, the owner: "separate event watch for each flywheel spoke"). One Monitor per slot.
# Emits a line when slot N's status, task or question changes on origin/flywheel, or when its lane branch gets a new commit.
# Errors print as SPOKE N ERROR so a broken watch is never silent.
N=$1; cd ~/forge/calibrations || { echo "SPOKE $N ERROR: no repo"; exit 1; }
state() { git show origin/flywheel:flywheel/SLOTS.json 2>/dev/null | /usr/bin/python3 -c "
import sys,json
s=[x for x in json.load(sys.stdin) if x['slot']==$N][0]
print(s['id'],s['status'],s.get('lane'),'Q' if s.get('question') and not s.get('answer') else '-',sep='|')" 2>/dev/null; }
git fetch -q origin flywheel 2>/dev/null; prev=$(state); lane=$(echo "$prev" | cut -d'|' -f3)
lhead=$(git ls-remote origin "refs/heads/$lane" 2>/dev/null | cut -c1-40); fails=0
echo "SPOKE $N ARMED: $prev"
while true; do
  sleep 30
  if ! git fetch -q origin flywheel 2>/dev/null; then fails=$((fails+1)); [ $fails -ge 3 ] && echo "SPOKE $N ERROR: fetch failing ($fails)"; continue; fi
  fails=0; cur=$(state)
  [ -z "$cur" ] && { echo "SPOKE $N ERROR: slot unreadable"; continue; }
  if [ "$cur" != "$prev" ]; then echo "SPOKE $N CHANGED: $prev -> $cur"; prev=$cur; lane=$(echo "$cur" | cut -d'|' -f3); lhead=$(git ls-remote origin "refs/heads/$lane" | cut -c1-40); fi
  h=$(git ls-remote origin "refs/heads/$lane" 2>/dev/null | cut -c1-40)
  if [ -n "$h" ] && [ "$h" != "$lhead" ]; then git fetch -q origin "$lane" 2>/dev/null; echo "SPOKE $N LANE $lane: $(git log -1 --format='%h %s' $h 2>/dev/null)"; lhead=$h; fi
done
