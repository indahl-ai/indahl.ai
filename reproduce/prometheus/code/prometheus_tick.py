#!/usr/bin/env python3
"""prometheus_tick.py: PROMETHEUS, the NIFC Significant Wildland Fire Potential Outlook against the large fires that followed. PLAN.md, sealed in
data/plan_seal.json (indahl-ai/calibrations, branch lane-research, commit c1dfe97) before any outlook or fire record was read.

The frame (PLAN.md section 4): every issue January 2023 to December 2025, first month only, rated per Predictive Services Area (PSA). The ratings are
read from PSA polygons in NIFC's monthly archive ZIP for that issue. An issue whose ZIP holds no PSA polygons is held and listed, never redrawn from a
map image (PLAN.md section 5). When no issue in the frame can be read, every cell reads CANNOT_TELL with NO_INTERVAL_FORMABLE and the reason is named.

  prometheus_tick.py              fetch what is missing (fetch_outlooks.py, at most once per 20 h for the outlooks page), then read
  prometheus_tick.py --offline    read only what is on disk
  prometheus_tick.py --publish    also put data/prometheus_live.json in the site KV as prometheus_live, served at /prometheus/live.json
  prometheus_tick.py --selftest   the outcome rule against planted intervals
Downloads are data only: ZIP central directories are listed with zipfile, nothing inside them is extracted or run. Standard library only."""
import sys as _cfsys, os as _cfos
try:   # 22 Nov 2026: one shared Cloudflare part (lib/cf.py: kv token, rings on failure)
    _cfsys.path.insert(0, _cfos.path.expanduser('~/forge/lib')); from cf import run_put as _cf_run
except Exception:
    import subprocess as _cfsp; _cf_run = _cfsp.run
import hashlib, json, os, subprocess, sys, time, zipfile
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import heuremen_kit as K
OFF = '--offline' in sys.argv; PUB = '--publish' in sys.argv
NOW = time.time()
FRAME_ISSUES = ['%04d-%02d' % (y, m) for y in (2023, 2024, 2025) for m in range(1, 13)]
POLY = ('.shp', '.kml', '.kmz', '.geojson', '.gdb', '.gpkg')   # a PSA polygon file in any of the usual GIS formats
HALF = 0.5   # PLAN.md section 5: the run reads "above normal" as exceeding happening more than half the time
LABELS = ['PRELIMINARY: first run, not refereed', 'above normal has no stated number. The run reads it as more than half.']
CELLS = [('above_exceed_share', 'above normal', 'count above usual', 100, 'first month', True),
         ('below_under_share', 'below normal', 'count under usual', 100, 'first month', False),
         ('normal_exceed_share', 'normal', 'count above usual', 100, 'first month', False),
         ('above_exceed_share_300', 'above normal', 'count above usual', 300, 'first month', False),
         ('below_under_share_300', 'below normal', 'count under usual', 300, 'first month', False),
         ('normal_exceed_share_300', 'normal', 'count above usual', 300, 'first month', False),
         ('above_exceed_share_m2_4', 'above normal', 'count above usual', 100, 'months two to four', False),
         ('below_under_share_m2_4', 'below normal', 'count under usual', 100, 'months two to four', False),
         ('normal_exceed_share_m2_4', 'normal', 'count above usual', 100, 'months two to four', False)]


def log(*a): print('prometheus:', *a, file=sys.stderr, flush=True)


def outcome(lo, hi):
    """PLAN.md section 5, exactly. CONSISTENT: the whole interval is above 0.5. BELOW: the whole interval is at or below 0.5. CANNOT_TELL otherwise.
    ABOVE cannot occur against a direction claim."""
    if lo is None or hi is None or lo > hi: return K.CANNOT_TELL, K.NO_INTERVAL_FORMABLE
    if lo > HALF: return K.CONSISTENT, None
    if hi <= HALF: return K.BELOW, None
    return K.CANNOT_TELL, K.STRADDLES_EDGE


if '--selftest' in sys.argv:
    t = [((0.55, 0.7), (K.CONSISTENT, None)), ((0.5, 0.7), (K.CANNOT_TELL, K.STRADDLES_EDGE)), ((0.3, 0.5), (K.BELOW, None)),
         ((0.45, 0.55), (K.CANNOT_TELL, K.STRADDLES_EDGE)), ((None, None), (K.CANNOT_TELL, K.NO_INTERVAL_FORMABLE)), ((0.6, 0.4), (K.CANNOT_TELL, K.NO_INTERVAL_FORMABLE))]
    bad = [(a, outcome(*a), w) for a, w in t if outcome(*a) != w]
    print('selftest', 'passed' if not bad else 'FAILED %r' % bad); sys.exit(1 if bad else 0)

# ---------------- 1. the plan seal: no reading without it, and none if PLAN.md moved since
seal = json.load(open('data/plan_seal.json'))
plan_sha = hashlib.sha256(open('PLAN.md', 'rb').read()).hexdigest()
if plan_sha != seal['plan_sha256']: sys.exit('prometheus: PLAN.md differs from data/plan_seal.json, refusing to read')

# ---------------- 2. fetch (the archive is posted once a month, the page is read at most once per 20 h)
STALE = []
page = 'data/raw/nifc/outlooks_page.html'
if not OFF:
    args = [sys.executable, '-I', os.path.join(H, 'fetch_outlooks.py')]
    if not os.path.exists(page) or NOW - os.path.getmtime(page) > 20 * 3600: args.append('--refresh')
    p = subprocess.run(args, capture_output=True, text=True, timeout=3600)
    if p.returncode: STALE.append('fetch_outlooks.py exit %d' % p.returncode); log('fetch FAILED', (p.stderr or '')[-300:])
man = json.load(open('data/outlook_manifest.json'))
by_issue = {r['issue']: r for r in man['issues']}

# ---------------- 3. read every issue in the frame from its own ZIP (central directory only)
issues, held, nothing, readable = [], [], [], []
for iss in FRAME_ISSUES:
    r = by_issue.get(iss)
    row = dict(issue=iss)
    if not r or r.get('error') and not os.path.exists(os.path.join(H, r.get('file', ''))):
        row.update(status='NOTHING_RETURNED', why='no archive ZIP for this issue on the outlooks page' if not r else 'download failed: %s' % r.get('error'))
        nothing.append(row); issues.append(row); continue
    f = os.path.join(H, r['file'])
    try:
        with zipfile.ZipFile(f) as z: names = z.namelist()
    except (zipfile.BadZipFile, OSError) as e:
        row.update(status='NOTHING_RETURNED', why='ZIP unreadable: %s' % type(e).__name__); nothing.append(row); issues.append(row); continue
    sha = hashlib.sha256(open(f, 'rb').read()).hexdigest()
    poly = sorted(n for n in names if n.lower().endswith(POLY))
    kinds = sorted({os.path.splitext(n)[1].lower() or '(none)' for n in names})
    row.update(file=r['file'], url=r['url'], sha256=sha, members=len(names), member_kinds=kinds, psa_polygon_files=poly)
    if not poly:
        row.update(status='HELD', why='the archive ZIP holds maps and PDFs only (%s), no PSA polygons' % ', '.join(kinds)); held.append(row)
    else:
        # PLAN.md has the reader for PSA polygons in its frame, but no ZIP in the archive has held one when this code was written, so the polygon
        # reader is not built. An issue with polygons is listed and not counted, and the run says so, never a silent skip.
        row.update(status='HELD', why='PSA polygons found (%s), the polygon reader is not built yet' % ', '.join(poly)); held.append(row); readable.append(iss)
    issues.append(row)

# ---------------- 4. cells (PLAN.md section 4). With no rated PSA-month every cell has n = 0 and no interval.
FRAME_MET = False
why_frame = ('None of the %d issues in the frame could be read: %d held (archive ZIP with no PSA polygons), %d nothing returned. '
             'PLAN.md section 5 reads this as CANNOT_TELL, a frame item not met, until a PSA polygon source for the issues is found.'
             % (len(FRAME_ISSUES), len([h for h in held if not h['psa_polygon_files']]), len(nothing)))
if readable: why_frame += ' %d issue(s) hold polygon files that the run does not yet read: %s.' % (len(readable), ', '.join(readable))
cells = []
for key, rating, counts, acres, months, head in CELLS:
    o, reason = outcome(None, None)
    cells.append(dict(cell=key, field='prometheus.' + key, rating=rating, counts=counts, acres=acres, months=months, headline=head,
                      psa_months=0, exceeded=0, value=None, lo=None, hi=None, display='cannot tell', outcome=o, reason=reason, why=why_frame,
                      interval='95 percent block bootstrap by outlook issue (PLAN.md section 4), not formed: no rated PSA-month'))
P = {c['cell']: c for c in cells}
REQ13 = K.req13([(P['above_exceed_share']['outcome'], P['above_exceed_share']['reason'])], nothing_returned=[n['issue'] for n in nothing])
REQ13_ALL = K.req13([(c['outcome'], c['reason']) for c in cells], nothing_returned=[n['issue'] for n in nothing])

summary = dict(
    desk='PROMETHEUS', publisher='Heuremen LLC', generated=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(NOW)), plan='PLAN.md', plan_seal=seal,
    plan_unchanged_since_seal=True, labels=LABELS,
    claim=dict(product='NIFC Significant Wildland Fire Potential Outlook, monthly, by Predictive Services Area',
               stated='"The Outlook identifies areas where significant wildland fire activity is expected to be above or below normal levels." (National Interagency Mobilization Guide 2026, chapter 60)',
               number_stated=None, reading='The run reads "above normal" as a claim that a PSA-month exceeds its usual count more than half the time (PLAN.md section 5). This is the run\'s reading, not NIFC\'s.'),
    frame=dict(issues=[FRAME_ISSUES[0], FRAME_ISSUES[-1]], frame_issues=len(FRAME_ISSUES), months='first month of each issue (months two to four secondary)',
               unit='PSA and calendar month', large_fire_acres=[100, 300], usual_count='median large-fire count per PSA and calendar month, 2001 to 2020, FPA FOD 6th edition',
               exceed='large-fire count above the usual count', bound=HALF, interval='95 percent block bootstrap by outlook issue', met=FRAME_MET, why_not_met=why_frame),
    sources=dict(outlooks_page='https://www.nifc.gov/nicc/predictive-services/outlooks', manifest_fetched=man.get('fetched'), archive_issues_listed=len(man['issues']),
                 frame_issues_on_page=sum(1 for i in FRAME_ISSUES if i in by_issue), stale=STALE,
                 fires_outcome='NIFC Open Data, WFIGS Wildland Fire Locations Full History: not read on this run, since no outlook PSA-month is formed to set it beside',
                 fires_baseline='FPA FOD 6th edition (RDS-2013-0009.6): not read on this run, same reason'),
    issues=issues, held=[dict(issue=h['issue'], why=h['why']) for h in held], nothing_returned=[dict(issue=n['issue'], why=n['why']) for n in nothing],
    off_duty_months=[], counts=dict(frame_issues=len(FRAME_ISSUES), held=len(held), nothing_returned=len(nothing), read=0, rated_psa_months=0),
    prometheus=P, cells=cells, req13=REQ13, req13_all=REQ13_ALL,
    carriers=['The baseline comes from one database (FPA FOD, 1992 to 2020) and the outcome years from another (WFIGS). The run counts both in 2020 and prints the difference once both are read.',
              'above normal has no stated number. The run reads it as more than half.',
              'The large-fire threshold, 100 acres for all fuels, ignores fuel type.', 'Fire records may be incomplete (NWCG).'],
    after_data_note='None. Nothing was added after the data.')
json.dump(summary, open('summary_prometheus.json.tmp', 'w'), indent=1); os.replace('summary_prometheus.json.tmp', 'summary_prometheus.json')
live = dict(summary, updated=summary['generated'])
json.dump(live, open('data/prometheus_live.json.tmp', 'w'), separators=(',', ':')); os.replace('data/prometheus_live.json.tmp', 'data/prometheus_live.json')
if PUB:
    env = dict(os.environ, CLOUDFLARE_ACCOUNT_ID='<cloudflare-account-id>', PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
    p = _cf_run(['/opt/homebrew/bin/npx', 'wrangler', 'kv', 'key', 'put', 'prometheus_live', '--path', os.path.join(H, 'data', 'prometheus_live.json'), '--namespace-id', '<kv-namespace-id>', '--remote'],
                       cwd=os.path.expanduser('~/forge/cloudflare-workers/heuremen-door'), env=env, capture_output=True, text=True)
    log('prometheus_live', 'published' if p.returncode == 0 else 'publish FAILED ' + (p.stderr or '')[-200:])
    if p.returncode: STALE.append('publish')
with open('data/prometheus_history.jsonl', 'a') as f:
    f.write(json.dumps(dict(t=summary['generated'], held=len(held), nothing=len(nothing), read=0, headline=(P['above_exceed_share']['outcome'], P['above_exceed_share']['reason']), stale=STALE)) + '\n')
log('frame issues %d, held %d, nothing returned %d, read 0' % (len(FRAME_ISSUES), len(held), len(nothing)))
log('headline prometheus.above_exceed_share: %s (%s)' % (P['above_exceed_share']['outcome'], P['above_exceed_share']['reason']))
log(REQ13['line'])
