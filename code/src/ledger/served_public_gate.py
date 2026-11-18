#!/usr/bin/env python3
"""Every file the indahl.ai worker serves from public/ must be tracked in the public indahl.ai repo, and so must worker.js.
14 Nov 2026: the claim "everything on the site is in the public git" was never checked; 85 served files and the worker were missing."""
import os, subprocess, sys
B = os.path.expanduser('~/bones-forge'); W = B + '/cloudflare-workers/heuremen-door'; M = B + '/public_mirror/indahl.ai'
tracked = set(subprocess.run(['git', '-C', M, 'ls-files'], capture_output=True, text=True).stdout.split('\n'))
served = [os.path.relpath(os.path.join(d, f), W + '/public') for d, _, fs in os.walk(W + '/public') for f in fs]
served = [x for x in served if not x.startswith('_studies/')]   # 17 Nov 2026, the owner: one public list per desk; public/_studies/ is read by the worker only (worker.js answers 404 to it), so it is not served and not mirrored
last = int(subprocess.run(['git', '-C', M, 'log', '-1', '--format=%ct'], capture_output=True, text=True).stdout.strip() or 0)
late = lambda x: x.startswith('receipts/stamps/') and os.path.getmtime(os.path.join(W, 'public', x)) > last   # 14 Nov: ship.sh stamps the release after its own public push, so the newest receipt goes public on the next ship
miss = [x for x in served if x not in tracked and not late(x)] + [x for x in ('code/worker/worker.js', 'code/worker/wrangler.toml') if x not in tracked]
held = [x for x in served if x not in tracked and late(x)]
if held: print('  %d release receipt(s) written after the last public push, carried by the next ship: %s' % (len(held), ', '.join(held)))
print('served-public gate: %d served files, %d missing from the public repo' % (len(served), len(miss)))
for x in miss[:20]: print('  MISSING', x)
sys.exit(1 if miss else 0)
