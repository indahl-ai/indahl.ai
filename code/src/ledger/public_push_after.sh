#!/bin/bash
# public_push_after.sh "<label>" (23 Nov 2026, house review): the public-repo mirror, moved out of the ship's critical path. It took 5 min 47 s
# of every ship (measured 23 Nov) while the live site never needs it. ship.sh starts this detached right after the deploy and commit; the
# privacy gate still runs inside push_public.sh BEFORE anything is pushed. One at a time (flock). Any failure rings pipe.log.
set -uo pipefail
B=~/forge; L=$B/ledger; MSG="${1:-site update}"; PIPE=$B/sagar/pipeline/pipe.log
[ -z "${PP_LOCKED:-}" ] && exec env PP_LOCKED=1 /usr/bin/lockf -k "$L/.public_push.lock" bash "$0" "$@"   # one public push at a time
# 23 Nov 2026 (review #7): also under the site lock, so it never copies pages while the next ship's builders are rewriting them. Started by a
# ship that still holds that lock, it waits its turn and runs right after. SITE_LOCK_HELD is inherited from that ship, so it is cleared first.
[ -z "${PP_SITE:-}" ] && exec env -u SITE_LOCK_HELD PP_SITE=1 PP_LOCKED=1 python3 "$L/site_lock.py" run --label "public push: $MSG" -- bash "$0" "$@"
note() { echo "  NOTE: $*"; echo "$(date +%Y-%m-%dT%H:%M:%S) RING: PUBLIC PUSH: $*" >> "$PIPE"; }
echo "== $(date +%H:%M:%S) public push for: $MSG"
# 31 Oct: the result is recorded for the watch (it was swallowed by "|| true" and a refusal went unseen for hours); a refusal is printed loud
set +e; PUBOUT=$(SHIP_DEPLOYED=1 "$L/push_public.sh" "$MSG" 2>&1); PUBRC=$?; set -e; echo "$PUBOUT"   # 10 Nov: SHIP_DEPLOYED=1 makes a skipped page mirror a hard failure (exit 3)
python3 - "$PUBRC" "$PUBOUT" > "$L/public_push_status.json" <<'PY'
import json, sys, time; rc = int(sys.argv[1]); out = sys.argv[2]; bad = rc != 0 or 'REFUSED' in out
print(json.dumps({'at': time.strftime('%Y-%m-%d %H:%M'), 'ok': not bad, 'site_pages': rc != 3 and 'site pages mirrored' in out, 'rc': rc, 'last': (out.strip().splitlines() or [''])[-1]}))
PY
if [ $PUBRC -eq 3 ]; then echo "!! 5b FAIL: the site deployed but its pages were NOT mirrored to the public indahl.ai repo (code only). Alert written for the operator."; fi
set +e; python3 "$L/public_privacy_gate.py"; PPG=$?; set -e; [ $PPG -ne 0 ] && note "public privacy gate FAILED"; if [ $PPG -ne 0 ]; then echo "!! 5b FAIL: a private name, address or key path is in the public indahl.ai repo"; printf -- '- [public:privacy] since %s: private item in the public repo (ledger/public_privacy_gate.py)\n' "$(date '+%Y-%m-%d %H:%M')" >> "$B/alerts/ALERTS_OPEN.txt"; fi   # 14 Nov: the privacy gate, after the house-folder leak
set +e; python3 "$L/served_public_gate.py"; SPG=$?; set -e; [ $SPG -ne 0 ] && note "served public gate FAILED"; printf '{"at": "%s", "privacy": %s, "served": %s}\n' "$(date '+%Y-%m-%d %H:%M')" "$([ $PPG -eq 0 ] && echo true || echo false)" "$([ $SPG -eq 0 ] && echo true || echo false)" > "$L/public_gates_status.json";   # 21 Nov 2026 (control audit #11): read by watch/alerts_check.py, so the alert stays open
 if [ $SPG -ne 0 ]; then echo "!! 5b FAIL: files the site serves are missing from the public indahl.ai repo"; printf -- '- [public:served] since %s: served files missing from the public indahl.ai repo (ledger/served_public_gate.py)\n' "$(date '+%Y-%m-%d %H:%M')" >> "$B/alerts/ALERTS_OPEN.txt"; fi   # 14 Nov (the owner caught it): everything the site serves is in the public repo, checked every release
if [ $PUBRC -ne 0 ] || echo "$PUBOUT" | grep -q REFUSED; then echo "!! PUBLIC REPOS REFUSED: the site shipped, the public code copies did not (see above; the watch shows this BAD until fixed)"; note "public repos not pushed (push_public.sh exit $PUBRC): $(echo "$PUBOUT" | grep -m1 -E 'REFUSED|FAIL' | cut -c1-200)"; fi
echo "== $(date +%H:%M:%S) public push done"
