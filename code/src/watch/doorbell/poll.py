#!/usr/bin/env python3
"""poll.py (21 Nov 2026, the owner: "dude's map was done two hours ago, can we not have that be overlooked again?").
Runs forever (nohup). Every 45 s, every lane PR on indahl-ai/calibrations: any comment that starts (after markdown) with "Ball to the operator"
is appended to inbox.jsonl. The operator marks rings read with `python3 read.py` (prints unread, marks them). The per-prompt hook prints the unread
count and first lines on every message from the owner, so no ring waits on a monitor that expired."""
import json, os, re, subprocess, time
H = os.path.dirname(os.path.abspath(__file__)); INBOX = os.path.join(H, 'inbox.jsonl'); LAST = os.path.join(H, 'last.txt')
os.environ['PATH'] = '/opt/homebrew/bin:/usr/local/bin:' + os.environ.get('PATH', '')
seen = {json.loads(l)['id'] for l in open(INBOX)} if os.path.exists(INBOX) else set()
last = open(LAST).read().strip() if os.path.exists(LAST) else time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - 4 * 3600))
while True:
    now = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()); ok = True
    for n in (1, 2, 3, 4, 5, 6, 7, 8):
        try:
            r = subprocess.run(['gh', 'api', 'repos/indahl-ai/calibrations/issues/%d/comments?since=%s&per_page=100' % (n, last)], capture_output=True, text=True, timeout=60)
            for c in json.loads(r.stdout or '[]'):
                if c['id'] in seen or (not re.search(r'ball to bones', (c.get('body') or '').split('\n')[0], re.I) or re.match(r'^[^A-Za-z]*(ball to dude|pointer)', c.get('body') or '', re.I)): continue
                seen.add(c['id']); open(INBOX, 'a').write(json.dumps({'id': c['id'], 'pr': n, 'at': c['created_at'], 'first': ' / '.join((c['body'] or '').split('\n')[:3])[:300], 'url': c['html_url'], 'read': False}) + '\n')
        except Exception: ok = False
    if ok: open(LAST, 'w').write(now); last = now
    time.sleep(45)
