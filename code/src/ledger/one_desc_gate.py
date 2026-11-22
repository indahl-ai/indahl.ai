#!/usr/bin/env python3
"""one_desc_gate.py (22 Nov 2026): every desk's description lives in ONE place, indahl-ai/seo/seo_copy.json, which page() in build_site.py
uses over any other copy. Refuses (exit 1) when a desk in ledger/desks.json has no line there.

Why: on 21 Nov the same bundle was refused because DEUS had no seo_copy line, so build_site.py's own copy of its description shipped
(with a count in it), while the desk's build_page.py held a third copy. Fixing the page did nothing. Five places held desk descriptions.
A new desk adds its line to seo_copy.json. The copies in build_site.py PAGES and <desk>/build_page.py DESC never reach the served page."""
import json, os, sys
B = os.path.expanduser('~/forge')
desks = json.load(open(os.path.join(B, 'ledger', 'desks.json')))['desks']
have = {x['path']: x for x in json.load(open(os.path.join(B, 'indahl-ai', 'seo', 'seo_copy.json')))}
miss = [d['id'] for d in desks if d.get('path') and d['path'] not in have]
empty = [p for p, x in have.items() if not (x.get('description') or '').strip()]
print('one description gate: %d desks, %d without a seo_copy.json line, %d empty lines' % (len(desks), len(miss), len(empty)))
for m in miss: print('  BREACH no seo_copy.json line: %s' % m)
for p in empty: print('  BREACH empty description: %s' % p)
sys.exit(1 if miss or empty else 0)
