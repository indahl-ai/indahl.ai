#!/usr/bin/env python3
"""scan_stated.py: SELDON desk, stated side, step 1. Reads each CBO report PDF in data/raw/cbo_reports as text (pymupdf, data only) and writes every
passage that states a two-thirds chance or likelihood, with its page, to data/stated_scan.json. No actual is read here. The ranges themselves are
copied from these passages, word for word, into data/stated_ranges.json (by hand, before any actual is opened), and build_stated.py checks every
quote there against this scan."""
import os, re, json, sys, glob
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
import site; sys.path.append(site.getusersitepackages()); import pymupdf   # run with python3 -I, so the user site is added by name
PAT = re.compile(r'two[- ]?thirds|2/3|66 percent|67 percent|68 percent', re.I)
CTX = re.compile(r'chance|likel|probab|confidence|range|band|outcomes', re.I)
def norm(t): return re.sub(r'\s+', ' ', t.replace('­', '').replace('‑', '-').replace('‐', '-').replace('ﬁ', 'fi').replace('ﬂ', 'fl')).strip()
out = []
for f in sorted(glob.glob('data/raw/cbo_reports/*.pdf')):
    try: doc = pymupdf.open(f)
    except Exception as e: out.append(dict(file=f, error=str(e)[:200])); continue
    hits = []
    for i, pg in enumerate(doc):
        t = norm(pg.get_text())
        for m in PAT.finditer(t):
            a, b = max(0, m.start() - 450), min(len(t), m.end() + 450); c = t[a:b]
            if CTX.search(c): hits.append(dict(page=i + 1, at=m.start(), text=c))
    first = norm(doc[0].get_text())[:300] if len(doc) else ''
    out.append(dict(file=f, pages=len(doc), title=first, hits=hits))
json.dump(out, open('data/stated_scan.json', 'w'), indent=0)
print('files', len(out), 'with hits', sum(1 for o in out if o.get('hits')), 'passages', sum(len(o.get('hits', [])) for o in out))
