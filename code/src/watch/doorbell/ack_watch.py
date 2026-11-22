#!/usr/bin/env python3
"""ack_watch.py (22 Nov 2026, the owner: "Hard Lockdown Full Comms with the designer"). Rides the tick (watch/desk_riders.py, 6-tick tier).
The cause it fixes: the build seat never acked three balls on PR #7 (02:42, 02:48, 04:12Z) and nothing noticed for eight hours.
Rule (LANES.md): The designer answers every ball with a "got it". So: every "Ball to the designer" on any lane PR that has no "Ball to the operator" on the
same PR after it within LIMIT minutes rings once: 'RING: THE DESIGNER BALL UNACKED PR #n ...' in sagar/pipeline/pipe.log -> the doorbell -> my prompt.
Rings once per ball (state file); an ack arriving later is logged as recovered. Read-only on GitHub."""
import json, os, subprocess, sys, time
from datetime import datetime, timezone
LIMIT = 30   # minutes
REPO = 'indahl-ai/calibrations'
H = os.path.dirname(os.path.abspath(__file__)); STATE = os.path.join(H, 'ack_watch_state.json')
PIPE_LOG = os.path.expanduser('~/forge/sagar/pipeline/pipe.log')
def log(msg):
    with open(PIPE_LOG, 'a') as f: f.write('%s %s\n' % (time.strftime('%Y-%m-%dT%H:%M:%S'), msg.replace('\n', ' ')[:500]))
since = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - 48 * 3600))
r = subprocess.run(['/opt/homebrew/bin/gh', 'api', '--paginate', 'repos/%s/issues/comments?since=%s&per_page=100' % (REPO, since),
                    '-q', '.[] | [.id, .created_at, (.issue_url|split("/")|last), (.body|.[0:120]|gsub("\n";" "))] | @tsv'],
                   capture_output=True, text=True, timeout=120)
if r.returncode: log('RING: ACK WATCH FAILED: gh api: ' + (r.stderr or '')[-200:]); sys.exit(1)
rows = []
for line in r.stdout.splitlines():
    p = line.split('\t')
    if len(p) == 4: rows.append((int(p[0]), datetime.strptime(p[1], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc), int(p[2]), p[3]))
st = json.load(open(STATE)) if os.path.exists(STATE) else {}
now = datetime.now(timezone.utc); open_n = 0
for cid, at, pr, body in rows:
    if not body.startswith('Ball to the designer's): continue
    acked = any(p2 == pr and a2 > at and b2.startswith('Ball to the operator's) for _, a2, p2, b2 in rows)
    k = str(cid)
    if acked:
        if st.get(k) == 'rang': log('ACK WATCH: recovered, PR #%d ball %s now acked' % (pr, at.strftime('%H:%MZ')))
        st[k] = 'acked'; continue
    if st.get(k) == 'retired': continue   # a superseded ball the operator retired by hand (e.g. PR #1, the old demos channel, 22 Nov)
    age = (now - at).total_seconds() / 60
    if age > LIMIT:
        open_n += 1
        if st.get(k) != 'rang':
            log('RING: THE DESIGNER BALL UNACKED PR #%d: ball at %s, %d min, no "got it" (LIMIT %d min): %s' % (pr, at.strftime('%H:%MZ'), age, LIMIT, body[:90]))
            st[k] = 'rang'
json.dump(st, open(STATE + '.tmp', 'w')); os.replace(STATE + '.tmp', STATE)
print('ack_watch: %d balls to the designer unacked past %d min' % (open_n, LIMIT))
