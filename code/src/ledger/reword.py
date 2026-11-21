#!/usr/bin/env python3
"""reword.py -- change one piece of public copy everywhere it lives, source file and ledger together (15 Nov 2026, the owner's
sitewide pass: no "we", "our", "you" in public copy). The ledger checks every public sentence against the built pages, so a sentence
changed only in the source would read MISSING; this changes both in one step.

  python3 reword.py FILE "old text" "new text"      exact substring; FILE must contain it; every ledger surface text containing
                                                    it is changed the same way. Prints what changed. Refuses if FILE lacks it.
  python3 reword.py --dry FILE "old" "new"           show only"""
import json, os, shutil, sys, time
B = os.path.expanduser('~/bones-forge')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import ledger as LG   # 21 Nov 2026: the ledger is written only through ledger.save (one lock, merge, refuse a conflict); this file used to write it directly
LEDGER = LG.LEDGER
a = sys.argv[1:]; dry = a[:1] == ['--dry']; a = a[1:] if dry else a
if len(a) != 3: raise SystemExit(__doc__)
f, old, new = a; f = os.path.join(B, f) if not f.startswith('/') else f
s = open(f, encoding='utf-8').read(); n = s.count(old)
if not n: raise SystemExit('REFUSED: %s does not contain the old text' % f)
rows = LG.load(); hit = []
for r in rows.values():
    for x in r.get('surfaces', []):
        if old in x.get('text', ''):
            hit.append(r['id'])
            if not dry: x['text'] = x['text'].replace(old, new)
print('%s: %d in %s; ledger rows: %s' % ('DRY' if dry else 'CHANGED', n, os.path.relpath(f, B), ', '.join(hit) or 'none'))
if dry: sys.exit(0)
stamp = time.strftime('%Y%m%d')
for p in (f, LEDGER):
    if not os.path.exists(p + '.bak-' + stamp + '-reword'): shutil.copy(p, p + '.bak-' + stamp + '-reword')
open(f, 'w', encoding='utf-8').write(s.replace(old, new))
if hit: print('ledger rows written: %d' % LG.save(rows))
