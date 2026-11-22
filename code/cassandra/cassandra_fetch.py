#!/usr/bin/env python3
"""cassandra_fetch.py: fetches the CASSANDRA sources into data/raw (see PLAN.md section 3 and PLAN_ADDENDUM_build.md). Public, no key, one request at a time,
paced. Never reads the files it fetches beyond a format check. Rerunnable: a file already on disk is kept, the current year's files are refreshed after 20 hours.
--years 2008-2026 limits the years."""
import os, sys, time, re, urllib.request, urllib.parse
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
UA = 'heuremen-cassandra/0.1 (+https://indahl.ai/cassandra)'
PACE = 2.0
WW = ('https://mesonet.agron.iastate.edu/cgi-bin/request/gis/watchwarn.py?accept=shapefile&sts=%d-01-01T00:00Z&ets=%d-01-01T00:00Z'
      '&limit1=1&limitps=1&phenomena=FF&significance=W')
LSR = 'https://mesonet.agron.iastate.edu/cgi-bin/request/gis/lsr.py?sts=%d-01-01T00:00Z&ets=%d-01-01T00:00Z&type=FLASH%%20FLOOD&fmt=csv&justcsv=1'
SE_DIR = 'https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/'
FIRST, LAST = 2008, 2026
for a in sys.argv:
    m = re.match(r'^(\d{4})-(\d{4})$', a)
    if m: FIRST, LAST = int(m.group(1)), int(m.group(2))
for d in ('data/raw/warnings', 'data/raw/stormevents', 'data/raw/lsr'): os.makedirs(d, exist_ok=True)
_last = [0.0]; FAILED = []
def get(url, tries=3, timeout=1800):
    err = None
    for a in range(tries):
        w = PACE - (time.time() - _last[0])
        if w > 0: time.sleep(w)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout) as r: b = r.read()
            _last[0] = time.time(); return b
        except Exception as e:
            _last[0] = time.time(); err = e
            if getattr(e, 'code', 0) in (400, 404, 422): break
            time.sleep(10 * (a + 1) ** 2)
    raise RuntimeError('fetch failed %s: %r' % (url[:160], err))
def fetch_to(path, url, refresh, must):
    if os.path.exists(path) and not (refresh and time.time() - os.path.getmtime(path) > 20 * 3600): return True
    try:
        b = get(url)
        if not must(b): raise RuntimeError('unexpected content %r' % b[:80])
        open(path + '.part', 'wb').write(b); os.replace(path + '.part', path); print('fetched', path, len(b), flush=True); return True
    except Exception as e:
        print('FAILED', path, repr(e)[:200], flush=True); FAILED.append(path); return os.path.exists(path)
this_year = int(time.strftime('%Y', time.gmtime()))
listing = get(SE_DIR).decode('latin-1')
if FIRST <= 2008: fetch_to('data/raw/warnings/ffw_2007.zip', WW % (2007, 2008), False, lambda b: b[:2] == b'PK')   # read only for warnings in force early on 1 January 2008
for y in range(FIRST, LAST + 1):
    cur = y >= this_year - 1
    if y <= 2025: fetch_to('data/raw/warnings/ffw_%d.zip' % y, WW % (y, y + 1), False, lambda b: b[:2] == b'PK')
    names = sorted(set(re.findall(r'StormEvents_details-ftp_v1\.0_d%d_c\d{8}\.csv\.gz' % y, listing)))
    if names:
        fetch_to('data/raw/stormevents/details_%d.csv.gz' % y, SE_DIR + names[-1], cur, lambda b: b[:2] == b'\x1f\x8b')
        open('data/raw/stormevents/details_%d.name' % y, 'w').write(names[-1] + '\n')
    else: print('no Storm Events file listed for', y); FAILED.append('stormevents %d' % y)
    fetch_to('data/raw/lsr/lsr_ff_%d.csv' % y, LSR % (y, y + 1), cur, lambda b: b[:5].upper().startswith(b'VALID'))
print('failed', FAILED)
sys.exit(1 if FAILED else 0)
