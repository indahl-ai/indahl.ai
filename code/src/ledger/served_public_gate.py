#!/usr/bin/env python3
"""Every file the indahl.ai worker serves from public/ must be tracked in the public indahl.ai repo, and so must worker.js.
14 Nov 2026: the claim "everything on the site is in the public git" was never checked; 85 served files and the worker were missing."""
import os, subprocess, sys
B = os.path.expanduser('~/forge'); W = B + '/cloudflare-workers/heuremen-door'; M = B + '/public_mirror/indahl.ai'
tracked = set(subprocess.run(['git', '-C', M, 'ls-files'], capture_output=True, text=True).stdout.split('\n'))
served = [os.path.relpath(os.path.join(d, f), W + '/public') for d, _, fs in os.walk(W + '/public') for f in fs]
served = [x for x in served if not x.startswith('_studies/')]   # 17 Nov 2026, the owner: one public list per desk; public/_studies/ is read by the worker only (worker.js answers 404 to it), so it is not served and not mirrored
last = int(subprocess.run(['git', '-C', M, 'log', '-1', '--format=%ct'], capture_output=True, text=True).stdout.strip() or 0)
late = lambda x: x.startswith('receipts/stamps/') and os.path.getmtime(os.path.join(W, 'public', x)) > last   # 14 Nov: ship.sh stamps the release after its own public push, so the newest receipt goes public on the next ship
miss = [x for x in served if x not in tracked and not late(x)] + [x for x in ('code/worker/worker.js', 'code/worker/wrangler.toml') if x not in tracked]
# 20 Nov 2026: since 19 Nov (the owner: studies live on the site, never in the public git) push_public.sh strips every file that names a study id
# or sits on a study path (ledger/toast.py purge_tree). Those files are served and are off git ON PURPOSE, so this gate asks the same rule
# and counts them apart. Anything else that is served and not tracked still fails.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import toast as _T, zipfile as _Z
_S = _T.study_ids()
def _offgit(x):
    if x in ('code/worker/worker.js', 'code/worker/wrangler.toml'): return False
    if os.path.basename(x) in _T.NEVER_PUBLIC or _T.MIRROR_STUDY_PATHS.match(x): return True
    f = os.path.join(W, 'public', x)
    try:
        if os.path.getsize(f) > 60_000_000: return False
        if x.endswith('.zip'): return any(_T.found(_Z.ZipFile(f).read(n).decode('utf-8', 'ignore'), _S) for n in _Z.ZipFile(f).namelist())
        return bool(_T.found(open(f, 'rb').read().decode('utf-8', 'ignore'), _S))
    except Exception: return False
offgit = [x for x in miss if _offgit(x)]; miss = [x for x in miss if x not in set(offgit)]
if offgit: print('  %d served file(s) are off the public git by the studies rule (they name a study or sit on a study path)' % len(offgit))
held = [x for x in served if x not in tracked and late(x)]
if held: print('  %d release receipt(s) written after the last public push, carried by the next ship: %s' % (len(held), ', '.join(held)))
print('served-public gate: %d served files, %d missing from the public repo' % (len(served), len(miss)))
for x in miss[:20]: print('  MISSING', x)
sys.exit(1 if miss else 0)
