#!/usr/bin/env python3
"""fetch_stated.py: SELDON desk, stated side. cbo.gov refuses scripted reads (a browser check), so CBO reports are read from Internet Archive copies.
Lists candidate CBO report PDFs from the archive's index (data/raw/cdx, one CDX listing per cbo.gov file prefix), keeps one copy per report, and
downloads each copy not yet held to data/raw/cbo_reports, one request at a time, 2 s apart. Writes data/raw/cbo_reports/index.json.
The downloads are untrusted data: they are only read as text by build_stated.py (pymupdf), never run."""
import os, re, json, time, urllib.request, sys
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
D = 'data/raw/cbo_reports'; os.makedirs(D, exist_ok=True)
UA = 'heuremen-seldon/0.1 (+https://indahl.ai/seldon)'; last = [0.0]
def get(u, tries=3):
    err = None
    for a in range(tries):
        w = 2.0 - (time.time() - last[0])
        if w > 0: time.sleep(w)
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=180) as r: b = r.read()
            last[0] = time.time(); return b
        except Exception as e:
            last[0] = time.time(); err = e
            if getattr(e, 'code', 0) in (403, 404): break
            time.sleep(8 * (a + 1))
    raise RuntimeError('fetch failed %s %r' % (u[:120], err))
KEEP = re.compile(r'outlook|forecast|uncertain|deficits?-?debt|deficitsdebt|accuracy|budgetprojections|economicprojections|baseline|budgetupdate|update_to_outlook|updatetooutlook|outlookupdate|budeconoutlook|budgeteconupdate|2016_outlook_update|outlook-update', re.I)
DROP = re.compile(r'testimony|slide|presentation|ltbo|long-?term|l-tbudget|demograph|shipbuild|farm|medicaid|pell|costestimate|sequestration|debtlimit|debt-limit|qfr|questionsforrecord|revenue|labor|income|student|fydp|ssupdate|socsec|visualsummary|visual-summary|chapter|appendix|about|contents|notes|summary|cover|glance|tab%26fig|graphics|briefing|press|forecastersclub|forecasters-club|statementfortherecord|transparency|gseupdate|craig|conrad|hr\d|s369|table|reducing|reduction|options|egtrra|cyclical|fiscalcrisis|apb|grossdebt|debt-service|debtservice|debt_rates|debt%20rates|debttargets|gnp|primer|quiz|interest|military|navy|energy|health', re.I)
rows = {}
for f in sorted(os.listdir('data/raw/cdx')):
    for line in open('data/raw/cdx/' + f):
        p = line.split()
        if len(p) < 2: continue
        ts, orig = p[0], p[1]
        path = re.sub(r'^https?://(www\.)?cbo\.gov/', '', orig).replace('system/files?file=', 'system/files/').replace('%2F', '/')
        base = path.rsplit('/', 1)[-1]
        if not base.lower().endswith('.pdf') or not KEEP.search(base) or DROP.search(base): continue
        if int(ts[:4]) < 2000 and not re.search(r'(19|20)\d\d', path): continue
        m = re.search(r'(?:^|/)(\d{5})-', path) or re.search(r'doc(\d{4,5})/', path)
        key = m.group(1) if m else re.sub(r'(_\d|-\d|_one-?col(umn)?|onecol(umn)?)+(?=\.pdf$)', '', base.lower())
        if re.search(r'1975|1976|198\d|199\d', path): continue
        cur = rows.get(key)
        if cur is None or (len(base) < len(cur['base'])) or (len(base) == len(cur['base']) and ts > cur['ts']): rows[key] = dict(key=key, ts=ts, url=orig, path=path, base=base)
idx = sorted(rows.values(), key=lambda r: r['key'])
def prio(r):   # newest reports first (5-digit ids from 2013 on), then the older ftpdocs and dated names
    return (0, -int(r['key'])) if re.fullmatch(r'\d{5}', r['key']) else (1, r['key'])
ORDER = sorted(idx, key=prio)
print('candidate reports', len(idx), file=sys.stderr)
if '--list' in sys.argv:
    for r in idx: print(r['key'], r['ts'], r['path'])
    sys.exit(0)
for r in (ORDER[::-1] if "--reverse" in sys.argv else ORDER):   # a second runner may take the list from the other end
    fn = '%s/%s.pdf' % (D, re.sub(r'[^A-Za-z0-9._-]', '_', re.sub(r'\.pdf$', '', r['key'])))
    r['file'] = fn
    if os.path.exists(fn) and os.path.getsize(fn) > 2000: continue
    try:
        b = get('https://web.archive.org/web/%sid_/%s' % (r['ts'], r['url']))
        if not b.startswith(b'%PDF'): r['error'] = 'not a PDF'; print('not a PDF', r['key'], file=sys.stderr); continue
        open(fn + '.part', 'wb').write(b); os.replace(fn + '.part', fn); print('got', fn, len(b), file=sys.stderr)
    except Exception as e: r['error'] = str(e)[:200]; print('not fetched', r['key'], e, file=sys.stderr)
json.dump(idx, open(D + '/index.json', 'w'), indent=0)
