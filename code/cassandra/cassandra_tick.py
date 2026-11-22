#!/usr/bin/env python3
"""cassandra_tick.py: CASSANDRA (see PLAN.md and PLAN_ADDENDUM_build.md). Rerunnable. Installs no timer. Reads the files cassandra_fetch.py put in data/raw
(public, no key): IEM storm-based Flash Flood Warnings, NCEI Storm Events, IEM Local Storm Reports. Sets every Flash Flood Warning issued 2008 to 2025
beside the flash flood reports inside its polygon before it expired. Writes summary_cassandra.json, data/cassandra_live.json, data/cassandra_history.jsonl.
--fetch: run cassandra_fetch.py first. --publish: also put data/cassandra_live.json in the site KV as cassandra_live, served at /cassandra/live.json.
--selftest: rule, pairing and time zone checks only, no files read."""
import sys as _cfsys, os as _cfos
try:   # 22 Nov 2026: one shared Cloudflare part (lib/cf.py: kv token, rings on failure)
    _cfsys.path.insert(0, _cfos.path.expanduser('~/forge/lib')); from cf import run_put as _cf_run
except Exception:
    import subprocess as _cfsp; _cf_run = _cfsp.run
import os, sys, json, time, re, csv, gzip, io, hashlib, subprocess, calendar, collections as C
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import numpy as np
from matplotlib.path import Path
import heuremen_kit as K, shpread
PUB = '--publish' in sys.argv
FIRST, LAST = 2008, 2025
NBOOT = 2000; SEED = 20261122
LIKELY = (0.5, 1.0)          # PLAN.md section 5: the run's reading of "likely", more often than not
LABEL_PRE = 'PRELIMINARY: first run, not refereed'
LABEL_REP = 'floods reported, not floods'
NOW = time.time()
def log(*a): print('cassandra:', *a, file=sys.stderr, flush=True)
def ep(s):
    """'YYYYmmddHHMM' -> epoch seconds UTC."""
    return calendar.timegm(time.strptime(s.strip()[:12], '%Y%m%d%H%M'))
BARE = dict(EST=-5, CST=-6, MST=-7, PST=-8, AKST=-9, HST=-10, AST=-4, SST=-11, GST=10)
def tz_offset(z):
    """Storm Events CZ_TIMEZONE -> hours to add to UTC to get local time, or None (held). 'CST-6' -> -6, 'GST10' -> 10, bare 'CST' -> -6."""
    z = (z or '').strip().upper()
    m = re.match(r'^([A-Z]+)(-?\d{1,2})$', z)
    if m: return int(m.group(2))
    return BARE.get(z)
def se_time(r):
    """Storm Events begin time in UTC epoch seconds, or None."""
    off = tz_offset(r.get('CZ_TIMEZONE'))
    if off is None: return None
    try:
        ym = r['BEGIN_YEARMONTH'].strip(); d = int(r['BEGIN_DAY']); hm = int(r['BEGIN_TIME'])
        t = calendar.timegm((int(ym[:4]), int(ym[4:6]), d, hm // 100, hm % 100, 0))
    except Exception: return None
    return t - off * 3600
def ring_paths(rings): return [Path(np.asarray(r)) for r in rings if len(r) >= 3]
def inside(paths, xy):
    """Even-odd over all rings: a point inside an odd number of rings is inside (a hole is outside)."""
    c = np.zeros(len(xy), int)
    for p in paths: c += p.contains_points(xy)
    return (c % 2) == 1
def pair(warns, rt, rx, ry):
    """warns: list of dicts (issue, expire, paths, bbox). Reports sorted by time rt with lon rx, lat ry.
    Returns (hit flag per warning, covered flag per report). Hit: a report with issue <= t <= expire inside the polygon."""
    hit = np.zeros(len(warns), bool); cov = np.zeros(len(rt), bool)
    for i, w in enumerate(warns):
        a = np.searchsorted(rt, w['issue'], 'left'); b = np.searchsorted(rt, w['expire'], 'right')
        if b <= a: continue
        x0, y0, x1, y1 = w['bbox']; idx = np.arange(a, b)
        m = (rx[idx] >= x0) & (rx[idx] <= x1) & (ry[idx] >= y0) & (ry[idx] <= y1); idx = idx[m]
        if not len(idx): continue
        ins = inside(w['paths'], np.column_stack([rx[idx], ry[idx]]))
        if ins.any(): hit[i] = True; cov[idx[ins]] = True
    return hit, cov
def boot_ratio(num, den, seed=SEED, n=NBOOT):
    """num, den: per-block sums. Block bootstrap of sum(num)/sum(den). Returns (value, lo, hi)."""
    num = np.asarray(num, float); den = np.asarray(den, float); D = len(num)
    if D == 0 or den.sum() <= 0: return None, None, None
    rng = np.random.default_rng(seed); w = rng.multinomial(D, np.full(D, 1.0 / D), size=n).astype(float)
    sn = w @ num; sd = w @ den; ok = sd > 0; r = sn[ok] / sd[ok]
    return float(num.sum() / den.sum()), float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))
def outcome(lo, hi):
    """PLAN.md section 5: CONSISTENT if the whole interval is at or above 0.5, BELOW if the whole interval is under 0.5, CANNOT_TELL otherwise. ABOVE cannot occur."""
    return K.read(lo, hi, band=LIKELY, edge='closed')
def rule_selftest():
    t = []
    t.append(outcome(0.55, 0.70) == (K.CONSISTENT, None)); t.append(outcome(0.50, 0.60) == (K.CONSISTENT, None))
    t.append(outcome(0.30, 0.45) == (K.BELOW, None)); t.append(outcome(0.40, 0.4999) == (K.BELOW, None))
    t.append(outcome(0.45, 0.55) == (K.CANNOT_TELL, K.STRADDLES_EDGE)); t.append(outcome(None, None) == (K.CANNOT_TELL, K.NO_INTERVAL_FORMABLE))
    t.append(all(outcome(a, b)[0] != K.ABOVE for a, b in ((0.9, 1.0), (0.99, 1.0), (0.0, 0.1))))
    t.append(tz_offset('CST-6') == -6 and tz_offset('GST10') == 10 and tz_offset('EST') == -5 and tz_offset('XYZ') is None and tz_offset('') is None)
    t.append(se_time(dict(CZ_TIMEZONE='CST-6', BEGIN_YEARMONTH='201506', BEGIN_DAY='1', BEGIN_TIME='1930')) == calendar.timegm((2015, 6, 2, 1, 30, 0)))
    t.append(se_time(dict(CZ_TIMEZONE='GST10', BEGIN_YEARMONTH='201506', BEGIN_DAY='1', BEGIN_TIME='5')) == calendar.timegm((2015, 5, 31, 14, 5, 0)))
    sq = [[(-98, 35), (-97, 35), (-97, 36), (-98, 36), (-98, 35)]]
    W = [dict(issue=1000.0, expire=4600.0, paths=ring_paths(sq), bbox=(-98, 35, -97, 36))]
    rt = np.array([900.0, 1000.0, 2000.0, 4600.0, 4700.0]); rx = np.array([-97.5, -90.0, -97.5, -97.2, -97.5]); ry = np.array([35.5, 35.5, 35.5, 35.2, 35.5])
    h, c = pair(W, rt, rx, ry); t.append(bool(h[0]) and list(c) == [False, False, True, True, False])
    h, c = pair(W, np.array([900.0, 4700.0]), np.array([-97.5, -97.5]), np.array([35.5, 35.5])); t.append(not h[0])
    hole = sq + [[(-97.9, 35.1), (-97.1, 35.1), (-97.1, 35.9), (-97.9, 35.9), (-97.9, 35.1)]]
    t.append(list(inside(ring_paths(hole), np.array([[-97.5, 35.5], [-97.95, 35.05]]))) == [False, True])
    v, lo, hi = boot_ratio([1, 1, 0, 0], [2, 2, 2, 2]); t.append(abs(v - 0.25) < 1e-12 and lo <= 0.25 <= hi)
    return all(t), t
if '--selftest' in sys.argv:
    ok, t = rule_selftest(); print('rule selftest', 'PASSED' if ok else 'FAILED', t); sys.exit(0 if ok and K.selftest() else 1)
if '--fetch' in sys.argv:
    rc = subprocess.run([sys.executable, '-I', os.path.join(H, 'cassandra_fetch.py')]).returncode
    log('fetch exit', rc)

seal = json.load(open('data/plan_seal.json'))
if hashlib.sha256(open('PLAN.md', 'rb').read()).hexdigest() != seal['plan_sha256']: sys.exit('cassandra: PLAN.md differs from its seal, refusing to read')
STALE = []; HELD = C.defaultdict(list); fmt_ok = True

# ---------------- 1. warnings ----------------
NEEDW = ('WFO', 'ISSUED', 'EXPIRED', 'INIT_EXP', 'ETN', 'VTEC_YR', 'STATUS', 'GTYPE', 'PHENOM', 'SIG')
warn_month = C.Counter(); WARN = []; warn_file_ok = {}; dup_rows = 0; extended = 0; unreadable = []; context = []
byk = {}
for y in range(FIRST - 1, LAST + 1):
    f = 'data/raw/warnings/ffw_%d.zip' % y
    if not os.path.exists(f): warn_file_ok[y] = False; continue
    try: fn, recs = shpread.read_zip(f)
    except Exception as e: log('warning file unreadable', f, repr(e)[:100]); warn_file_ok[y] = False; continue
    if not all(k in fn for k in NEEDW): fmt_ok = False; warn_file_ok[y] = False; continue
    warn_file_ok[y] = True
    for r in recs:
        if r['PHENOM'] != 'FF' or r['SIG'] != 'W' or r['GTYPE'] != 'P' or r['STATUS'] != 'NEW': continue
        try: iss = ep(r['ISSUED']); exp = ep(r['EXPIRED']); iexp = ep(r['INIT_EXP'])
        except Exception: unreadable.append(dict(key='%s %s %s' % (r['WFO'], r['VTEC_YR'], r['ETN']), why='time')); continue
        iy = int(time.strftime('%Y', time.gmtime(iss)))
        if iy != y: continue
        key = (r['WFO'], r['VTEC_YR'], r['ETN'])
        rings = [rg for rg in r['rings'] if len(rg) >= 3]
        if not rings: unreadable.append(dict(key='%s %s %s' % key, why='polygon')); continue
        allp = np.array([pt for rg in rings for pt in rg])
        w = dict(key=key, wfo=r['WFO'], year=iy, issue=float(iss), expire=float(exp), iexp=float(iexp), paths=ring_paths(rings),
                 bbox=(allp[:, 0].min(), allp[:, 1].min(), allp[:, 0].max(), allp[:, 1].max()), pid=r.get('PROD_ID'))
        if key in byk:
            dup_rows += 1
            if w['issue'] >= byk[key]['issue']: continue
        byk[key] = w
for w in byk.values():
    if FIRST <= w['year'] <= LAST:
        WARN.append(w); warn_month[(w['year'], int(time.strftime('%m', time.gmtime(w['issue']))))] += 1
        extended += w['expire'] > w['iexp']
    else: context.append(w)                      # 2007 warnings: read only so a report early on 1 January 2008 can find the warning in force
WARN.sort(key=lambda w: w['issue']); ALLW = sorted(WARN + context, key=lambda w: w['issue'])
log('warnings', len(WARN), 'context', len(context), 'duplicate rows', dup_rows, 'extended', extended, 'unreadable', len(unreadable))

# ---------------- 2. reports ----------------
def load_se(y):
    f = 'data/raw/stormevents/details_%d.csv.gz' % y
    if not os.path.exists(f): return None
    out = []; held = C.Counter(); seen = set(); months = C.Counter()
    try:
        rd = csv.DictReader(gzip.open(f, 'rt', encoding='latin-1', newline=''))
        need = ('BEGIN_YEARMONTH', 'BEGIN_DAY', 'BEGIN_TIME', 'CZ_TIMEZONE', 'EVENT_TYPE', 'EVENT_ID', 'WFO', 'BEGIN_LAT', 'BEGIN_LON')
        if not all(k in (rd.fieldnames or []) for k in need): return 'format'
        for r in rd:
            if r['EVENT_TYPE'] != 'Flash Flood': continue
            if r['EVENT_ID'] in seen: held['duplicate event id'] += 1; continue
            seen.add(r['EVENT_ID'])
            try: months[int(r['BEGIN_YEARMONTH'][4:6])] += 1
            except Exception: pass
            t = se_time(r)
            if t is None: held['no readable time or zone'] += 1; continue
            try: lat, lon = float(r['BEGIN_LAT']), float(r['BEGIN_LON'])
            except Exception: held['no begin position'] += 1; continue
            out.append((float(t), lon, lat, r['WFO'].strip().upper(), r['EVENT_ID']))
    except Exception as e: log('storm events unreadable', f, repr(e)[:100]); return None
    return dict(rows=out, held=held, months=months, name=(open(f.replace('.csv.gz', '.name')).read().strip() if os.path.exists(f.replace('.csv.gz', '.name')) else ''))
def load_lsr(y):
    f = 'data/raw/lsr/lsr_ff_%d.csv' % y
    if not os.path.exists(f): return None
    out = []; held = C.Counter(); seen = set(); months = C.Counter()
    try:
        rd = csv.DictReader(open(f, newline='', encoding='utf-8', errors='replace'))
        if not all(k in (rd.fieldnames or []) for k in ('VALID', 'LAT', 'LON', 'WFO', 'TYPETEXT')): return 'format'
        for r in rd:
            if (r.get('TYPETEXT') or '').strip().upper() != 'FLASH FLOOD': continue
            try: t = ep(r['VALID']); lat, lon = float(r['LAT']), float(r['LON'])
            except Exception: held['no readable time or position'] += 1; continue
            k = (r['VALID'], r['LAT'], r['LON'], r['WFO'])
            if k in seen: held['same time, place and office'] += 1; continue
            seen.add(k); months[int(r['VALID'][4:6])] += 1
            out.append((float(t), lon, lat, (r['WFO'] or '').strip().upper(), '%s %s %s' % k[:3]))
    except Exception as e: log('lsr unreadable', f, repr(e)[:100]); return None
    return dict(rows=out, held=held, months=months, name='')
SRC = {}
for name, loader in (('stormevents', load_se), ('lsr', load_lsr)):
    per = {}
    for y in range(FIRST, LAST + 2):
        d = loader(y)
        if d == 'format': fmt_ok = False; d = None
        per[y] = d
    SRC[name] = per
    log(name, {y: (len(d['rows']) if d else None) for y, d in per.items()})
last_exp = max(w['expire'] for w in WARN) if WARN else NOW

# ---------------- 3. held years (PLAN_ADDENDUM_build.md, fixed before the pairing) ----------------
def held_years(src):
    out = {}
    for y in range(FIRST, LAST + 1):
        why = []
        if not warn_file_ok.get(y): why.append('warning file not read')
        d = SRC[src].get(y)
        if d is None: why.append('report file not read')
        else:
            zm = [m for m in range(1, 13) if d['months'].get(m, 0) == 0]
            if zm: why.append('no report in month %s' % ', '.join(map(str, zm)))
        zw = [m for m in range(1, 13) if warn_month.get((y, m), 0) == 0]
        if warn_file_ok.get(y) and zw: why.append('no warning in month %s' % ', '.join(map(str, zw)))
        if why: out[y] = why
    return out

# ---------------- 4. the pairing ----------------
def reports(src, y0, y1, tmax=None):
    rows = []
    for y in range(y0, y1 + 1):
        d = SRC[src].get(y)
        if d: rows += [r for r in d['rows'] if tmax is None or y <= LAST or r[0] <= tmax]
    rows.sort(key=lambda r: r[0])
    return rows
def cell_hit(src):
    held = held_years(src); ws = [w for w in WARN if w['year'] not in held]
    R = reports(src, FIRST, LAST + 1, tmax=last_exp)
    rt = np.array([r[0] for r in R]); rx = np.array([r[1] for r in R]); ry = np.array([r[2] for r in R])
    hit, _ = pair(ws, rt, rx, ry)
    blk = C.defaultdict(lambda: [0, 0])
    for w, h in zip(ws, hit): b = blk[(w['wfo'], w['year'])]; b[0] += int(h); b[1] += 1
    ks = sorted(blk); v, lo, hi = boot_ratio([blk[k][0] for k in ks], [blk[k][1] for k in ks])
    o, why = outcome(lo, hi)
    years = []
    for y in range(FIRST, LAST + 1):
        if y in held: years.append(dict(year=y, held=held[y])); continue
        kk = [k for k in ks if k[1] == y]; yv, ylo, yhi = boot_ratio([blk[k][0] for k in kk], [blk[k][1] for k in kk], seed=SEED + y)
        yo, yw = outcome(ylo, yhi)
        years.append(dict(year=y, warnings=sum(blk[k][1] for k in kk), hits=sum(blk[k][0] for k in kk), value=None if yv is None else round(yv, 4),
                          lo=None if ylo is None else round(ylo, 4), hi=None if yhi is None else round(yhi, 4), outcome=yo, reason=yw))
    return dict(source=src, warnings=len(ws), hits=int(hit.sum()), blocks=len(ks), value=None if v is None else round(v, 4), lo=None if lo is None else round(lo, 4),
                hi=None if hi is None else round(hi, 4), outcome=o, reason=why, held_years={str(k): v for k, v in held.items()}, years=years,
                reports_read=len(R), label=LABEL_PRE, carrier=LABEL_REP), {w['key']: bool(h) for w, h in zip(ws, hit)}
def cell_warned(src):
    held = held_years(src)
    R = [r for r in reports(src, FIRST, LAST) if int(time.strftime('%Y', time.gmtime(r[0]))) not in held]
    rt = np.array([r[0] for r in R]); rx = np.array([r[1] for r in R]); ry = np.array([r[2] for r in R])
    _, cov = pair(ALLW, rt, rx, ry)
    blk = C.defaultdict(lambda: [0, 0])
    for r, c in zip(R, cov): b = blk[(r[3], int(time.strftime('%Y', time.gmtime(r[0]))))]; b[0] += int(c); b[1] += 1
    ks = sorted(blk); v, lo, hi = boot_ratio([blk[k][0] for k in ks], [blk[k][1] for k in ks], seed=SEED + 1)
    o, why = outcome(lo, hi)
    hc = C.Counter()
    for y in range(FIRST, LAST + 1):
        if y not in held and SRC[src].get(y): hc.update(SRC[src][y]['held'])
    return dict(source=src, reports=len(R), warned=int(cov.sum()), blocks=len(ks), value=None if v is None else round(v, 4), lo=None if lo is None else round(lo, 4),
                hi=None if hi is None else round(hi, 4), outcome=o, reason=why, reports_held=dict(hc), held_years={str(k): v for k, v in held.items()}, label=LABEL_PRE, carrier=LABEL_REP,
                display_only=True)

# ---------------- 5. known-good gates ----------------
kg = {}
kg['format'] = fmt_ok and len(WARN) > 0 and all(warn_file_ok.get(y) for y in range(FIRST, LAST + 1))
import contextlib
with contextlib.redirect_stdout(io.StringIO()): _kit_ok = K.selftest()
kg['rule'] = rule_selftest()[0] and _kit_ok
GATE = all(kg.values())

ffw, hitmap = cell_hit('stormevents'); ffw_lsr, _ = cell_hit('lsr'); warned = cell_warned('stormevents'); warned_lsr = cell_warned('lsr')
warned_lsr['note'] = 'display only, not a named cell'
def gate_all(obj):
    if GATE: return obj
    if isinstance(obj, dict):
        o = {k: gate_all(v) for k, v in obj.items()}
        if 'outcome' in o and o['outcome'] in K.OUTCOMES: o['outcome_before_gate'] = o['outcome']; o['outcome'] = K.CANNOT_TELL; o['reason'] = K.NO_INTERVAL_FORMABLE
        return o
    if isinstance(obj, list): return [gate_all(x) for x in obj]
    return obj
ffw, ffw_lsr, warned, warned_lsr = gate_all(ffw), gate_all(ffw_lsr), gate_all(warned), gate_all(warned_lsr)
# REQ-13: nothing returned counted apart, never folded. Held years and held warnings are listed and are outside the counts.
NR = ['year %s held: %s' % (y, '; '.join(v).replace(';', ',')) for y, v in ffw['held_years'].items()] + ['warning %s: %s' % (u['key'], u['why']) for u in unreadable]
REQ13 = K.req13([(ffw['outcome'], ffw.get('reason'))], nothing_returned=NR)
REQ13_ALL = K.req13([(c['outcome'], c.get('reason')) for c in (ffw, ffw_lsr, warned)] + [(y['outcome'], y.get('reason')) for c in (ffw, ffw_lsr) for y in c['years'] if 'outcome' in y], nothing_returned=NR)

# raw rows for the CHECKS entry (gate R): one warning and one Storm Events report, as read
raw = {}
if WARN:
    w = next((x for x in WARN if x['year'] == 2015), WARN[0])
    raw['warning'] = dict(key='%s %s %s' % w['key'], product=w['pid'], issue=time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime(w['issue'])), expire=time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime(w['expire'])))
d15 = SRC['stormevents'].get(2015)
if d15 and d15['rows']:
    r = d15['rows'][0]; raw['stormevents'] = dict(event_id=r[4], utc=time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime(r[0])), lon=r[1], lat=r[2], wfo=r[3])

# ---------------- 6. output ----------------
def git(*a): return subprocess.run(['git'] + list(a), cwd=H, capture_output=True, text=True).stdout.strip()
first_f = 'data/first_comparison.json'
if not os.path.exists(first_f): json.dump(dict(first_comparison=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(NOW)), plan_sha256=seal['plan_sha256']), open(first_f, 'w'), indent=1)
summary = dict(
    desk='CASSANDRA', publisher='Heuremen LLC', generated=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(NOW)), plan='PLAN.md', plan_seal=seal,
    plan_unchanged=hashlib.sha256(open('PLAN.md', 'rb').read()).hexdigest() == seal['plan_sha256'], first_comparison=json.load(open(first_f))['first_comparison'],
    preliminary=True, label=LABEL_PRE, carrier=LABEL_REP,
    claim=dict(text='Flash flood warnings are issued when flooding is imminent or likely.', source='NWSI 10-922', url='https://www.weather.gov/media/directives/010_pdfs/pd01009022curr.pdf',
               reading='likely read as more often than not, a share of 0.5, the run’s reading and not the National Weather Service’s'),
    frame=dict(window=[FIRST, LAST], phenomenon='FF', significance='W', polygon='issuance polygon held to the final expiry', bootstrap=dict(resamples=NBOOT, seed=SEED, block='forecast office and year'),
               band=list(LIKELY), edge='closed'),
    gates=dict(kg, passed=GATE),
    cassandra=dict(ffw_hit_share=ffw, ffw_hit_share_lsr=ffw_lsr, flood_warned_share=warned, flood_warned_share_lsr=warned_lsr),
    sources=dict(warnings=len(WARN), warnings_extended=extended, warnings_duplicate_rows=dup_rows, warnings_unreadable=unreadable, warnings_context_2007=len(context),
                 warnings_by_year={str(y): sum(1 for w in WARN if w['year'] == y) for y in range(FIRST, LAST + 1)},
                 stormevents_files={str(y): (d['name'] if d else None) for y, d in SRC['stormevents'].items()},
                 stormevents_rows_by_year={str(y): (len(d['rows']) if d else None) for y, d in SRC['stormevents'].items()},
                 stormevents_held={str(y): dict(d['held']) for y, d in SRC['stormevents'].items() if d},
                 lsr_rows_by_year={str(y): (len(d['rows']) if d else None) for y, d in SRC['lsr'].items()},
                 lsr_held={str(y): dict(d['held']) for y, d in SRC['lsr'].items() if d}, report_files_2026_present=dict(stormevents=bool(SRC['stormevents'].get(LAST + 1)), lsr=bool(SRC['lsr'].get(LAST + 1))),
                 stale=STALE),
    raw_rows=raw, req13=REQ13, req13_all=REQ13_ALL)
json.dump(summary, open('summary_cassandra.json.tmp', 'w'), indent=1); os.replace('summary_cassandra.json.tmp', 'summary_cassandra.json')
live = dict(summary, updated=summary['generated'])
json.dump(live, open('data/cassandra_live.json.tmp', 'w'), separators=(',', ':')); os.replace('data/cassandra_live.json.tmp', 'data/cassandra_live.json')
if PUB:
    env = dict(os.environ, CLOUDFLARE_ACCOUNT_ID='<cloudflare-account-id>', PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
    p = _cf_run(['/opt/homebrew/bin/npx', 'wrangler', 'kv', 'key', 'put', 'cassandra_live', '--path', os.path.join(H, 'data', 'cassandra_live.json'), '--namespace-id', '<kv-namespace-id>', '--remote'],
                       cwd=os.path.expanduser('~/forge/cloudflare-workers/heuremen-door'), env=env, capture_output=True, text=True)
    log('cassandra_live', 'published' if p.returncode == 0 else 'publish FAILED ' + (p.stderr or '')[-200:])
    if p.returncode: STALE.append('publish')
with open('data/cassandra_history.jsonl', 'a') as f:
    f.write(json.dumps(dict(t=summary['generated'], gate=GATE, ffw=(ffw['value'], ffw['lo'], ffw['hi'], ffw['outcome']), lsr=(ffw_lsr['value'], ffw_lsr['outcome']),
                            warned=(warned['value'], warned['outcome']), stale=STALE)) + '\n')
log('gates', kg)
for c in (ffw, ffw_lsr): log('hit share %-11s warnings %6d hits %6d  %s [%s, %s] %s %s  held %s' % (c['source'], c['warnings'], c['hits'], c['value'], c['lo'], c['hi'], c['outcome'], c['reason'] or '', list(c['held_years'])))
for c in (warned, warned_lsr): log('warned share %-11s reports %6d warned %6d  %s [%s, %s] %s' % (c['source'], c['reports'], c['warned'], c['value'], c['lo'], c['hi'], c['outcome']))
