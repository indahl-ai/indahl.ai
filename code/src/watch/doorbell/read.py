#!/usr/bin/env python3
"""read.py: print unread rings from the designer and mark them read. --peek prints without marking."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); INBOX = os.path.join(H, 'inbox.jsonl')
R = [json.loads(l) for l in open(INBOX)] if os.path.exists(INBOX) else []
u = [r for r in R if not r['read']]
for r in u: print('PR #%d %s %s\n   %s' % (r['pr'], r['at'][11:16] + 'Z', r['first'][:240], r['url']))
if not u: print('no unread rings')
if '--peek' not in sys.argv and u:
    for r in R: r['read'] = True
    open(INBOX + '.tmp', 'w').write(''.join(json.dumps(r) + '\n' for r in R)); os.replace(INBOX + '.tmp', INBOX)
