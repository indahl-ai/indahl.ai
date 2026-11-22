#!/usr/bin/env python3
"""ares_tick.py: ARES, where public conflict trackers agree that armed violence happened. PLAN.md, copied unchanged and sealed in data/plan_seal.json
before any data file was read.

The frame (PLAN.md section 4): the trailing 12 complete calendar months that ended at least 30 days before the run. Unit: province (Natural Earth
first-level unit, grouped by FIPS 10-4 code, never drawn) and month. UCDP (GED 26.1 where it covers the month, Candidate otherwise): any event of the
three types, where_prec 1 to 4, Candidate status Clear. GDELT 2.0: root events, QuadClass 4, root codes 18 19 20, ActionGeo_Type 4 or 5, two sources
or more. Per province-month: CONSISTENT when both trackers recorded violence, CANNOT_TELL (one tracker only, which one named) otherwise.
Headline ares.agree_share with a 95 percent block bootstrap by country and month. Dot size active_days (UCDP exact-day dates only).

  ares_tick.py              fetch what is due (UCDP, then GDELT, one at a time), crosswalk, count
  ares_tick.py --offline    count from the tables on disk
  ares_tick.py --publish    also put data/ares_live.json in the site KV as ares_live, served at /ares/live.json
  ares_tick.py --selftest   the outcome rule and the hard-line checks against planted rows
ARES_NOW (seconds since 1970) pins the clock, so a rerun reads the same window. Standard library only."""
import sys as _cfsys, os as _cfos
try:   # 22 Nov 2026: one shared Cloudflare part (lib/cf.py: kv token, rings on failure)
    _cfsys.path.insert(0, _cfos.path.expanduser('~/forge/lib')); from cf import run_put as _cf_run
except Exception:
    import subprocess as _cfsp; _cf_run = _cfsp.run
import collections, csv, gzip, hashlib, io, json, os, random, subprocess, sys, time
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import heuremen_kit as K
import ares_lines as L
OFF = '--offline' in sys.argv; PUB = '--publish' in sys.argv
NOW = float(os.environ.get('ARES_NOW') or time.time())
LABELS = ['PRELIMINARY: first run, not refereed', 'At least 30 days old']
BOOT = 2000; SEED = 20261122


def log(*a): print('ares:', *a, file=sys.stderr, flush=True)


def window(now):
    """PLAN.md section 4: the 12 complete months that ended at least 30 days before the run."""
    t = time.gmtime(now - 30 * 86400)
    y, m = t.tm_year, t.tm_mon - 1   # the month that holds (now - 30 days) has not ended 30 days before; the one before it has
    if m == 0: y, m = y - 1, 12
    out = []
    for _ in range(12):
        out.append('%04d-%02d' % (y, m)); m -= 1
        if m == 0: y, m = y - 1, 12
    return out[::-1]


def outcome(ucdp_any, gdelt_any):
    """PLAN.md section 5. Both: CONSISTENT ("both trackers agree"). One: CANNOT_TELL ("one tracker only", with which one). ABOVE and BELOW are not used."""
    if ucdp_any and gdelt_any: return K.CONSISTENT, 'both trackers'
    if ucdp_any: return K.CANNOT_TELL, 'UCDP only'
    if gdelt_any: return K.CANNOT_TELL, 'GDELT only'
    return None, None


if '--selftest' in sys.argv:
    bad = []
    for a, w in [((1, 1), (K.CONSISTENT, 'both trackers')), ((1, 0), (K.CANNOT_TELL, 'UCDP only')), ((0, 1), (K.CANNOT_TELL, 'GDELT only')), ((0, 0), (None, None))]:
        if outcome(*a) != w: bad.append((a, outcome(*a)))
    if window(time.mktime((2026, 12, 3, 12, 0, 0, 0, 0, 0)))[0::11] != ['2025-11', '2026-10']: bad.append('window 3 December 2026 (October ended 33 days before)')
    if window(time.mktime((2026, 11, 30, 12, 0, 0, 0, 0, 0)))[-1] != '2026-09': bad.append('window 30 November 2026 (October ended 29 days before)')
    if window(time.mktime((2026, 11, 22, 12, 0, 0, 0, 0, 0)))[-1] != '2026-09': bad.append('window 22 November 2026')
    for planted in ({'deaths_a': 1}, {'side_a': 'x'}, {'latitude': 1.0}, {'rows': [{'best': 3}]}, {'dyad_name': 'x'}):
        try: L.assert_clean(planted, 'selftest'); bad.append('assert_clean let %r through' % planted)
        except AssertionError: pass
    print('selftest', 'passed' if not bad else 'FAILED %r' % bad); sys.exit(1 if bad else 0)

# ---------------- 1. the plan seal: no reading if PLAN.md moved since
seal = json.load(open('data/plan_seal.json'))
if hashlib.sha256(open('PLAN.md', 'rb').read()).hexdigest() != seal['plan_sha256']: sys.exit('ares: PLAN.md differs from data/plan_seal.json, refusing to read')
WIN = window(NOW); WS = '%s:%s' % (WIN[0], WIN[-1])

# ---------------- 2. fetch, one source at a time (memory: GDELT is streamed file by file)
STALE = []
def due(p, w):
    if not os.path.exists(p): return True
    try: return json.load(open(p)).get('window') != w
    except Exception: return True
BUSY = subprocess.run(['/usr/bin/pgrep', '-f', 'fetch_(ucdp|gdelt)[.]py'], capture_output=True, text=True).stdout.split()
if BUSY and not OFF: STALE.append('a fetch is already running (pid %s), this run counts the tables on disk' % ' '.join(BUSY)); OFF = True   # one fetch at a time
if not OFF:
    for script, out in (('fetch_ucdp.py', 'data/ucdp_pm.json'), ('fetch_gdelt.py', 'data/gdelt_pm.json')):
        if not due(out, WIN): continue
        if script == 'fetch_gdelt.py' and os.path.exists('data/gdelt_state.json') and json.load(open('data/gdelt_state.json')).get('window') != WIN:
            os.replace('data/gdelt_state.json', 'data/gdelt_state_%s.json' % json.load(open('data/gdelt_state.json'))['window'][-1])
        p = subprocess.run([sys.executable, '-P', os.path.join(H, 'fetch', script), '--window', WS], capture_output=True, text=True, timeout=6 * 3600)
        if p.returncode: STALE.append('%s exit %d' % (script, p.returncode)); log(script, 'FAILED', (p.stderr or '')[-300:])
    p = subprocess.run([sys.executable, '-P', os.path.join(H, 'build_crosswalk.py')], capture_output=True, text=True)
    if p.returncode: STALE.append('build_crosswalk.py exit %d' % p.returncode); log('crosswalk FAILED', (p.stderr or '')[-300:])
U = json.load(open('data/ucdp_pm.json')); G = json.load(open('data/gdelt_pm.json'))
for d, n in ((U, 'UCDP'), (G, 'GDELT')):
    if d['window'] != WIN: STALE.append('%s table is for %s to %s, not this window' % (n, d['window'][0], d['window'][-1]))
X = json.load(open('data/crosswalk.json')); XS = json.load(open('data/crosswalk_seal.json'))
if hashlib.sha256(open('data/crosswalk.json', 'rb').read()).hexdigest() != XS['crosswalk_sha256']: sys.exit('ares: data/crosswalk.json differs from its seal, refusing to count')
NEU = json.load(open('data/ne_units.json'))['unit_country']

# ---------------- 3. fold both tables into province-months
win = set(WIN)
pm = {}
def cell(key, mo): return pm.setdefault((key, mo), dict(u=False, g=False, days=set(), us=set(), uc=set(), gs=set(), gc=set(), codes=set()))
held_u, held_g, nothing = collections.Counter(), collections.Counter(), collections.Counter()
held_u_why, held_g_why = {}, {}
for r in U['rows']:
    if r['month'] not in win: continue
    x = X['ucdp'].get(r['country'] + '|' + r['adm_1'])
    if not x or not x['province_key']:
        k = (r['country'], r['adm_1']); held_u[k] += 1; held_u_why[k] = (x or {}).get('why') or 'not yet in the crosswalk'; continue
    c = cell(x['province_key'], r['month']); c['u'] = True; c['days'].update(r['exact_days']); c['us'].add(r['adm_1']); c['uc'].add(r['country'])
general = 0
for r in G['rows']:
    if r['month'] not in win: continue
    if r['adm1_code'][2:] == '00' or not r['adm1_code'][:2].isalpha(): general += r['root_events']; continue   # GDELT '(general)': country level, no province (nothing returned)
    x = X['gdelt'].get(r['adm1_code'])
    if not x or not x['province_key']:
        k = (r['adm1_code'], r['country'], r['province']); held_g[k] += 1; held_g_why[k] = (x or {}).get('why') or 'not yet in the crosswalk'; continue
    c = cell(x['province_key'], r['month']); c['g'] = True; c['gs'].add(r['province'] or r['adm1_code']); c['gc'].add(r['country']); c['codes'].add(r['adm1_code'])

def block_country(key):
    if key.startswith('F:'): return key[2:4]
    return NEU.get(key, key)

rows = []
for (key, mo), c in sorted(pm.items(), key=lambda kv: (kv[0][1], kv[0][0])):
    o, which = outcome(c['u'], c['g'])
    rows.append(dict(province_key=key, month=mo, ucdp_country=' / '.join(sorted(c['uc'])), ucdp_province=' / '.join(sorted(c['us'])),
                     gdelt_country=' / '.join(sorted(c['gc'])), gdelt_province=' / '.join(sorted(c['gs'])), gdelt_codes=' / '.join(sorted(c['codes'])),
                     ucdp_any=int(c['u']), gdelt_any=int(c['g']), active_days=len(c['days']), outcome=o, which=which, block=block_country(key) + '|' + mo))
for r in rows:
    assert 0 <= r['active_days'] <= 31, 'ares: active_days out of range'
    assert r['active_days'] == 0 or r['ucdp_any'], 'ares: active_days without a UCDP event'

# ---------------- 4. cells (PLAN.md section 4, headline named in advance)
M = len(rows); N = sum(1 for r in rows if r['outcome'] == K.CONSISTENT)
u_only = sum(1 for r in rows if r['which'] == 'UCDP only'); g_only = sum(1 for r in rows if r['which'] == 'GDELT only')
blocks = collections.defaultdict(lambda: [0, 0])
for r in rows: b = blocks[r['block']]; b[0] += r['outcome'] == K.CONSISTENT; b[1] += 1
bl = list(blocks.values()); rng = random.Random(SEED); shares = []
for _ in range(BOOT if bl else 0):
    s = [bl[rng.randrange(len(bl))] for _ in bl]; n_, m_ = sum(x[0] for x in s), sum(x[1] for x in s)
    if m_: shares.append(n_ / m_)
shares.sort()
lo = shares[int(0.025 * len(shares))] if shares else None; hi = shares[min(len(shares) - 1, int(0.975 * len(shares)))] if shares else None
share = N / M if M else None
by_month = []
for mo in WIN:
    rr = [r for r in rows if r['month'] == mo]
    by_month.append(dict(month=mo, release=U['month_release'].get(mo), province_months=len(rr), agreed=sum(1 for r in rr if r['outcome'] == K.CONSISTENT),
                         ucdp_only=sum(1 for r in rr if r['which'] == 'UCDP only'), gdelt_only=sum(1 for r in rr if r['which'] == 'GDELT only')))
ARES = dict(
    agree_share=dict(field='ares.agree_share', value=share, lo=lo, hi=hi, n=N, of=M, interval='95 percent block bootstrap by country and month, %d resamples of %d blocks, seed %d' % (BOOT, len(bl), SEED),
                     outcome=None, reason=None, display='%.1f%%' % (100 * share) if share is not None else 'none', headline=True,
                     note='No stated claim to read against, so the share has no four-way word (PLAN.md section 5). Per province-month outcomes are counted below.'),
    ucdp_only_count=dict(field='ares.ucdp_only_count', value=u_only), gdelt_only_count=dict(field='ares.gdelt_only_count', value=g_only),
    agreed_count=dict(field='ares.agreed_count', value=N), province_months=dict(field='ares.province_months', value=M))
OUTC = collections.Counter(r['outcome'] for r in rows)
held_months = [m for m in WIN if m not in U['month_release']]
gc = G.get('counts', {})
nothing_rows = dict(gdelt_blank_place=gc.get('rows_blank_place', 0), gdelt_country_general_rows=general + gc.get('rows_country_general', 0), gdelt_files_not_read=len(G.get('files_not_read', {})),
                    ucdp_blank_adm_1=sum(c.get('blank_adm_1', 0) for c in U['counts'].values()))

kit_cols = ['province_key', 'month', 'ucdp_country', 'ucdp_province', 'gdelt_country', 'gdelt_province', 'gdelt_codes', 'ucdp_any', 'gdelt_any', 'active_days', 'outcome', 'which']
summary = dict(
    desk='ARES', publisher='Heuremen LLC', generated=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(NOW)), plan='PLAN.md', plan_seal=seal, labels=LABELS,
    frame=dict(window=[WIN[0], WIN[-1]], months=WIN, delay_days=30, unit='province (first-level unit) and month', held_months=held_months,
               ucdp='any event of the three UCDP types, where_prec 1 to 4, Candidate status Clear, GED 26.1 preferred where it covers the month',
               gdelt='root events, QuadClass 4, root codes 18 19 20 (CAMEO: assault, fight, use unconventional mass violence), ActionGeo_Type 4 or 5, NumSources 2 or more',
               size='active_days: distinct days in the month with a UCDP event placed in the province and dated to the exact day (date_prec 1)'),
    sources=dict(
        ucdp=dict(files=U['files'], counts=U['counts'], month_release=U['month_release'],
                  cite=['Sundberg, Ralph and Erik Melander (2013) Introducing the UCDP Georeferenced Event Dataset. Journal of Peace Research 50(4). GED version 26.1.',
                        'Davies, Shawn, Therése Pettersson and Magnus Öberg (2026) Organized violence 1989 to 2025, and violent political protests. Journal of Peace Research. doi:10.1093/jopres/xjag046. GED version 26.1.',
                        'Hegre, Håvard, Mihai Croicu, Kristine Eck and Stina Högbladh (2020) Introducing the UCDP Candidate Events Dataset. Research and Politics. doi:10.1177/2053168020935257. Candidate version 26.01.26.09.'],
                  license='CC BY 4.0', url='https://ucdp.uu.se/downloads/'),
        gdelt=dict(master=G['master'], master_sha256=G.get('master_sha256'), files_listed=G['files_listed'], files_read=G['files_read'], files_not_read=len(G.get('files_not_read', {})),
                   file_md5_digest=G.get('file_md5'), counts=gc, filtered_rows_year=gc.get('rows_kept'), cite='The GDELT Project, https://www.gdeltproject.org/'),
        boundary=dict(name=X['boundary']['source'], url=X['boundary']['url'], sha256=X['boundary']['sha256'], drawn=False),
        crosswalk=dict(sha256=XS['crosswalk_sha256'], sealed=XS['sealed'], ucdp_entries=len(X['ucdp']), gdelt_entries=len(X['gdelt']),
                       ucdp_methods=dict(collections.Counter(v['method'] for v in X['ucdp'].values())), gdelt_methods=dict(collections.Counter(v['method'] for v in X['gdelt'].values()))),
        stale=STALE, excluded='ACLED (PLAN.md section 1: license terms and an account requirement)'),
    ares=ARES, by_month=by_month,
    counts=dict(province_months=M, agreed=N, ucdp_only=u_only, gdelt_only=g_only, consistent=OUTC[K.CONSISTENT], cannot_tell=OUTC[K.CANNOT_TELL],
                held_ucdp_names=len(held_u), held_ucdp_province_months=sum(held_u.values()), held_gdelt_codes=len(held_g), held_gdelt_province_months=sum(held_g.values()),
                held_months=len(held_months), nothing_returned=nothing_rows, blocks=len(bl)),
    held=dict(ucdp=[dict(country=k[0], adm_1=k[1], province_months=v, why=held_u_why[k]) for k, v in held_u.most_common()],
              gdelt=[dict(code=k[0], country=k[1], province=k[2], province_months=v, why=held_g_why[k]) for k, v in held_g.most_common()],
              months=held_months),
    rows=[{k: r[k] for k in kit_cols} for r in rows],
    carriers=["UCDP's line is drawn by deaths: an event enters UCDP only if at least one death is registered. ARES reads that as yes or no and never reads or stores the number.",
              "GDELT's line is drawn by news reports: machine-coded events from news text, which carry the geographic bias of reporting (Hammond and Weidmann 2014).",
              'GDELT places outside the United States only (ActionGeo_Type 4 or 5), as the filter is written, so a place in the United States can only be UCDP only.',
              'Candidate events are preliminary and can change in the yearly GED release.'],
    after_data_note='Build notes, not frame changes: the window month is the event date month for both sources (UCDP date_start, GDELT SQLDATE). A Natural Earth province unit is the set of rows that share one FIPS code.')
L.assert_clean(summary, 'summary_ares.json')
json.dump(summary, open('summary_ares.json.tmp', 'w'), indent=1, ensure_ascii=False); os.replace('summary_ares.json.tmp', 'summary_ares.json')
live = dict(summary, updated=summary['generated'])
json.dump(live, open('data/ares_live.json.tmp', 'w'), separators=(',', ':'), ensure_ascii=False); os.replace('data/ares_live.json.tmp', 'data/ares_live.json')
buf = io.StringIO(); w = csv.writer(buf); w.writerow(kit_cols); [w.writerow([r[k] for k in kit_cols]) for r in rows]
with gzip.GzipFile('data/ares_kit.csv.gz', 'wb', mtime=0) as f: f.write(buf.getvalue().encode('utf-8'))
if PUB:
    env = dict(os.environ, CLOUDFLARE_ACCOUNT_ID='<cloudflare-account-id>', PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
    p = _cf_run(['/opt/homebrew/bin/npx', 'wrangler', 'kv', 'key', 'put', 'ares_live', '--path', os.path.join(H, 'data', 'ares_live.json'), '--namespace-id', '<kv-namespace-id>', '--remote'],
                       cwd=os.path.expanduser('~/forge/cloudflare-workers/heuremen-door'), env=env, capture_output=True, text=True)
    log('ares_live', 'published' if p.returncode == 0 else 'publish FAILED ' + (p.stderr or '')[-200:])
    if p.returncode: STALE.append('publish')
with open('data/ares_history.jsonl', 'a') as f:
    f.write(json.dumps(dict(t=summary['generated'], window=[WIN[0], WIN[-1]], province_months=M, agreed=N, ucdp_only=u_only, gdelt_only=g_only, share=share, lo=lo, hi=hi, stale=STALE)) + '\n')
log('window %s to %s, province-months %d, both %d, UCDP only %d, GDELT only %d' % (WIN[0], WIN[-1], M, N, u_only, g_only))
log('headline ares.agree_share %s (95%% %s to %s)' % (share, lo, hi))
