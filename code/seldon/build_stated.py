#!/usr/bin/env python3
"""build_stated.py: SELDON desk, stated side, step 2. Reads data/stated_src.json (the ranges copied by hand from the CBO reports, with the words
that print each one) and checks every quoted fragment against the text of its report page (pymupdf). Any fragment not found refuses the build.
Writes data/stated_ranges.json with each report file's sha256. Reads no actual. Run before seldon_tick.py; the tick reads only the output."""
import os, re, json, sys, hashlib, time, site
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
sys.path.append(site.getusersitepackages()); import pymupdf   # run with python3 -I, so the user site is added by name
def key(t): return re.sub(r'[^a-z0-9.]', '', t.lower().replace('−', '-').replace('–', '-').replace('‑', '-').replace('­', '').replace('ﬀ', 'ff').replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('ﬃ', 'ffi'))
S = json.load(open('data/stated_src.json')); bad = []; pages = {}; shas = {}
def page(f, p):
    if (f, p) not in pages:
        d = pymupdf.open('data/raw/cbo_reports/%s.pdf' % f); pages[(f, p)] = key(d[p - 1].get_text())
        shas[f] = hashlib.sha256(open('data/raw/cbo_reports/%s.pdf' % f, 'rb').read()).hexdigest()
    return pages[(f, p)]
for r in S['ranges'] + S['not_counted']:
    for q in r['quote']:
        if key(q['text']) not in page(r['file'], q['page']): bad.append((r.get('id') or r['file'], q['page'], q['text'][:90]))
for f in S['reports_read']:
    shas.setdefault(f['file'], hashlib.sha256(open('data/raw/cbo_reports/%s.pdf' % f['file'], 'rb').read()).hexdigest())
if bad:
    for b in bad: print('QUOTE NOT FOUND', b)
    sys.exit(1)
ids = [r['id'] for r in S['ranges']]
assert len(ids) == len(set(ids)), 'duplicate range id'
out = dict(S, built=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), report_sha256=shas, quotes_checked=sum(len(r['quote']) for r in S['ranges'] + S['not_counted']))
json.dump(out, open('data/stated_ranges.json', 'w'), indent=1, ensure_ascii=False)
print('ranges', len(S['ranges']), 'not counted', len(S['not_counted']), 'quotes checked', out['quotes_checked'], 'reports read', len(S['reports_read']))
