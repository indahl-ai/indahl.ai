#!/usr/bin/env python3
"""fetch_imf.py: SELDON desk, IMF side. Downloads chapter 1 of each World Economic Outlook issue (April and October, 2006 on) to data/raw/imf_weo,
from imf.org, or from the Internet Archive copy when imf.org does not serve it. One request at a time, 3 s apart. Untrusted data: read as text only."""
import os, re, json, time, urllib.request, sys
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
D = 'data/raw/imf_weo'; os.makedirs(D, exist_ok=True)
UA = 'heuremen-seldon/0.1 (+https://indahl.ai/seldon)'; last = [0.0]
def get(u):
    w = 3.0 - (time.time() - last[0])
    if w > 0: time.sleep(w)
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=180) as r: b = r.read()
    finally: last[0] = time.time()
    return b
M = {'01': 'april', '02': 'october'}
def urls(y, h):
    mon = M[h]
    if y <= 2016: return ['https://www.imf.org/external/pubs/ft/weo/%d/%s/pdf/c1.pdf' % (y, h)]
    if y == 2017: return ['https://www.imf.org/-/media/files/publications/weo/2017/april/pdf/c1.pdf'] if h == '01' else ['https://www.imf.org/-/media/files/publications/weo/2017/october/pdf/main-chapter/c1.pdf']
    if y == 2018: return ['https://www.imf.org/-/media/files/publications/weo/2018/%s/english/main-report/c1.pdf' % mon, 'https://www.imf.org/-/media/Files/Publications/WEO/2018/April/c1.ashx', 'https://www.imf.org/-/media/files/publications/weo/2018/april/c1.pdf']
    return ['https://www.imf.org/-/media/files/publications/weo/%d/%s/english/ch1.pdf' % (y, mon), 'https://www.imf.org/-/media/Files/Publications/WEO/%d/%s/English/ch1.ashx' % (y, mon.capitalize())]
idx = []
for y in range(2006, 2027):
    for h in ('01', '02'):
        fn = '%s/weo_%d_%s_ch1.pdf' % (D, y, M[h]); rec = dict(issue='%d %s' % (y, M[h]), file=fn)
        if os.path.exists(fn) and os.path.getsize(fn) > 5000: rec['have'] = True; idx.append(rec); continue
        got = None
        for u in urls(y, h):
            for src in (u, 'https://web.archive.org/web/2026id_/' + u):
                try:
                    b = get(src)
                    if b.startswith(b'%PDF'): got = (src, b); break
                except Exception as e: rec.setdefault('errors', []).append('%s %s' % (src[:100], str(e)[:80]))
            if got: break
        if got: open(fn, 'wb').write(got[1]); rec['url'] = got[0]; print('got', fn, len(got[1]), file=sys.stderr)
        else: rec['missing'] = True; print('missing', rec['issue'], file=sys.stderr)
        idx.append(rec)
json.dump(idx, open(D + '/index.json', 'w'), indent=0)
