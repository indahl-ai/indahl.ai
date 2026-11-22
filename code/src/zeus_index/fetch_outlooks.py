#!/usr/bin/env python3
"""fetch_outlooks.py: ZEUS stated side. SPC Day 1 Convective Outlooks from the Iowa Environmental Mesonet archive, the same source and
the same reader as tornado_index (IEM_OTL, shpread.read_zip). One zip per year in data/raw/outlooks/day1_YYYY.zip; a year tornado_index already
holds is hard-linked, not refetched (the current year is refetched when older than 20 h). Writes data/outlooks_cat13.json: for every 1300 UTC
(CYCLE 13) Day 1 issuance, the categorical layers (TSTM, MRGL, SLGT, ENH, MDT, HIGH) as rings of (lon, lat), plus ISSUE, EXPIRE and PRODISS.
Polygons only; nothing about lightning is read here. Usage: python3 fetch_outlooks.py --years 2025 2026"""
import os, sys, json, time, argparse
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(H, '..', 'tornado_index')
sys.path.insert(0, H)
import shpread
IEM_OTL = 'https://mesonet.agron.iastate.edu/cgi-bin/request/gis/outlooks.py?d=1&type=C&sts=%d-01-01T00:00Z&ets=%d-01-01T00:00Z&geom=geom_layers'
UA = 'heuremen-zeus/0.1 (+https://indahl.ai/zeus)'
CATS = ('TSTM', 'MRGL', 'SLGT', 'ENH', 'MDT', 'HIGH')
def get(url, tries=3, timeout=900):
    import urllib.request; err = None
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout) as r: return r.read()
        except Exception as e:
            err = e
            if getattr(e, 'code', 0) in (400, 404, 422): break
            time.sleep(5 * (a + 1) ** 2)
    raise RuntimeError('fetch failed %s: %r' % (url[:140], err))
def year_zip(y, now):
    d = os.path.join(H, 'data', 'raw', 'outlooks'); os.makedirs(d, exist_ok=True); f = os.path.join(d, 'day1_%d.zip' % y)
    cur = y == int(time.strftime('%Y', time.gmtime(now))); tf = os.path.join(T, 'data', 'raw', 'outlooks', 'day1_%d.zip' % y)
    fresh = lambda p: os.path.exists(p) and (not cur or (now - os.path.getmtime(p)) / 3600 < 20)
    if fresh(f): return f
    if fresh(tf):
        if os.path.exists(f): os.remove(f)
        os.link(tf, f); return f
    b = get(IEM_OTL % (y, y + 1))
    if b[:2] != b'PK': raise RuntimeError('not a zip for %d' % y)
    open(f + '.part', 'wb').write(b); os.replace(f + '.part', f); time.sleep(1.5); return f
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--years', nargs='+', type=int, required=True); a = ap.parse_args(); now = time.time()
    out = {}; odd = {}
    for y in a.years:
        f = year_zip(y, now); fn, recs = shpread.read_zip(f)
        need = ('ISSUE', 'EXPIRE', 'THRESHOLD', 'CATEGORY', 'CYCLE', 'PRODISS')
        if not all(k in fn for k in need): raise SystemExit('format gate: %s lacks %s' % (f, need))
        for r in recs:
            if r['CYCLE'] != '13' or r.get('DAY', '1') != '1' or r.get('TYPE', 'C') != 'C': continue
            d = r['ISSUE'][:8]
            if not d.startswith(str(y)): continue
            day = out.setdefault(d, dict(issue=r['ISSUE'], expire=r['EXPIRE'], prodiss=r['PRODISS'], layers={}))
            if r['CATEGORY'] != 'CATEGORICAL': continue
            if r['THRESHOLD'] not in CATS: odd[r['THRESHOLD']] = odd.get(r['THRESHOLD'], 0) + 1; continue
            day['layers'].setdefault(r['THRESHOLD'], []).append(r['rings'])
    p = os.path.join(H, 'data', 'outlooks_cat13.json')
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(out); json.dump(old, open(p + '.part', 'w')); os.replace(p + '.part', p)
    print('zeus outlooks: 1300 UTC days', len(out), 'with TSTM layer', sum(1 for v in out.values() if 'TSTM' in v['layers']), 'odd thresholds', odd)
