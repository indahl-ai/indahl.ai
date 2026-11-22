#!/usr/bin/env python3
"""show_scan.py: prints, from data/stated_scan.json, the sentence around each two-thirds passage that also names a chance, likelihood or
probability (a stated range), one line per distinct sentence. A reading aid for building data/stated_ranges.json. Reads no actual."""
import json, re, sys
S = json.load(open('data/stated_scan.json')); seen = set(); only = sys.argv[1:]
for o in S:
    if only and not any(k in o['file'] for k in only): continue
    for h in o.get('hits', []):
        t = h['text']
        for m in re.finditer(r'two[- ]?thirds|66 percent|67 percent|68 percent', t, re.I):
            a = max(t.rfind('. ', 0, m.start()), 0); b = t.find('. ', m.end()); b = len(t) if b < 0 else b + 1
            s = t[a:b].strip('. ').strip()
            if not re.search(r'chance|likel|probab|confidence', s, re.I): continue
            k = re.sub(r'\W', '', s.lower())[:160]
            if k in seen: continue
            seen.add(k); print('%s p%d | %s' % (o['file'].rsplit('/', 1)[-1], h['page'], s[:700]))
