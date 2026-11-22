#!/usr/bin/env python3
"""scan_imf.py: SELDON desk, IMF side, step 1. Reads chapter 1 of each WEO issue in data/raw/imf_weo as text (pymupdf, data only) and writes every
sentence that states a probability as a number for global growth to data/imf_scan.json. No outcome is read here."""
import os, re, json, sys, glob, site
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
sys.path.append(site.getusersitepackages()); import pymupdf   # run with python3 -I, so the user site is added by name
def norm(t): return re.sub(r'\s+', ' ', t.replace('­', '').replace('ﬁ', 'fi').replace('ﬂ', 'fl')).strip()
out = []
for f in sorted(glob.glob('data/raw/imf_weo/*.pdf')):
    try: doc = pymupdf.open(f)
    except Exception as e: out.append(dict(file=f, error=str(e)[:200])); continue
    hits = []; seen = set()
    for i, pg in enumerate(doc):
        t = norm(pg.get_text())
        for s in re.split(r'(?<=[.;])\s+(?=[A-Z(])', t):
            if re.search(r'probabilit|chance|likelihood', s, re.I) and re.search(r'(global|world) (growth|GDP|recession)|global recession', s, re.I) and re.search(r'\d+(\.\d+)? percent|\d+%', s):
                k = s[:200]
                if k in seen: continue
                seen.add(k); hits.append(dict(page=i + 1, text=s[:900]))
    out.append(dict(file=f, pages=len(doc), hits=hits))
json.dump(out, open('data/imf_scan.json', 'w'), indent=0)
print('files', len(out), 'with hits', sum(1 for o in out if o.get('hits')), 'sentences', sum(len(o.get('hits', [])) for o in out))
