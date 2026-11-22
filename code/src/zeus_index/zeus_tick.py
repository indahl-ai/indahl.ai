#!/usr/bin/env python3
"""zeus_tick.py: ZEUS reader (see PLAN.md, frame fixed before any reading). Sets the SPC 1300 UTC Day 1 thunder area (TSTM, with every higher
category inside it) beside GOES GLM flashes. Inputs: data/outlooks_cat13.json (fetch_outlooks.py), data/glm/<east|west>/<D>.npz and .json
(fetch_glm.py), the Census state boundary file (data/raw/boundaries, as tornado_index). Writes summary_zeus.json, data/zeus_live.json, data/zeus_history.jsonl.
--selftest: rule, distance, time and split checks only, no data. --offline: no network (gate 2 reads its cached answers).
Run with zeus_index/.venv/bin/python (numpy, matplotlib-free: polygon tests use a small even-odd ray cast)."""
import os, sys, json, time, math, calendar, random, urllib.request, collections as C
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import numpy as np
import heuremen_kit as K, shpread
OFF = '--offline' in sys.argv
PUB = '--publish' in sys.argv or os.environ.get('HEUREMEN_PUBLISH') == '1'   # 22 Nov 2026: the tick bus exports HEUREMEN_PUBLISH=1, as for the other desks; a kit or test copy never publishes
def refuse(why, code=4):
    print('zeus: REFUSED: ' + why, file=sys.stderr, flush=True); sys.exit(code)
UA = 'heuremen-zeus/0.1 (+https://indahl.ai/zeus)'
IEM_PT = 'https://mesonet.agron.iastate.edu/api/1/nws/outlook_by_point.json?lat=%.4f&lon=%.4f&valid=%s'
STATES = os.path.join(H, 'data', 'raw', 'boundaries', 'cb_2024_us_state_20m.zip')   # hard link of tornado_index's copy (same Census file)
# ---------------- frame (PLAN.md section 4) ----------------
WIN0, WIN1 = '20261022', '20261120'                     # outlooks issued, inclusive; the last valid period ends 2026-11-21 1200 UTC
MI = 1.609344
RADII = {'primary': 25 * MI, 'secondary': 10 * MI}       # km. primary: borrowed from SPC's severe definition; secondary fixed by the amendment
STEP = 0.1; LAT0, LAT1, LON0, LON1 = 24.0, 50.0, -125.0, -66.5
SPLIT = -106.2                                           # GOES-19 for points east of 106.2 W, GOES-18 west of it
FLOOR = 0.10                                             # SPC: "a 10% or higher probability of thunderstorms"
VALID = (3600.0, 86400.0)                                # seconds after 1200 UTC on the issue date: 1300 UTC to 1200 UTC next day
GAP_HOLD = 3600                                          # a gap of more than one hour in the valid period holds the day
CATS = ('TSTM', 'MRGL', 'SLGT', 'ENH', 'MDT', 'HIGH')
NBOOT = 2000; SEED = 20261121; R_E = 6371.0088
LABELS = ['PRELIMINARY: first run, not refereed', '30-day window, late autumn', 'borrowed radius']
def log(*a): print('zeus:', *a, file=sys.stderr, flush=True)
# ---------------- geometry ----------------
def hav(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2); dp = p2 - p1; dl = np.radians(np.asarray(lon2) - np.asarray(lon1))
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R_E * np.arcsin(np.sqrt(np.minimum(1.0, a)))
def in_rings(rings, lon, lat):
    """Even-odd over all rings of one record (a hole is outside). lon, lat arrays."""
    c = np.zeros(len(lon), bool)
    for r in rings:
        if len(r) < 3: continue
        a = np.asarray(r, float); x0, y0 = a[:, 0], a[:, 1]; x1, y1 = np.roll(x0, -1), np.roll(y0, -1)
        bb = (lon >= x0.min()) & (lon <= x0.max()) & (lat >= y0.min()) & (lat <= y0.max()); idx = np.nonzero(bb)[0]
        if not len(idx): continue
        X = lon[idx][:, None]; Y = lat[idx][:, None]
        for s in range(0, len(x0), 4000):
            xa, ya, xb, yb = x0[s:s + 4000], y0[s:s + 4000], x1[s:s + 4000], y1[s:s + 4000]
            cr = ((ya > Y) != (yb > Y)) & (X < (xb - xa) * (Y - ya) / np.where(yb == ya, 1e-300, yb - ya) + xa)
            c[idx] ^= (cr.sum(1) % 2).astype(bool)
    return c
GLAT = np.round(np.arange(LAT0, LAT1 + 1e-9, STEP), 4); GLON = np.round(np.arange(LON0, LON1 + 1e-9, STEP), 4)
NY, NX = len(GLAT), len(GLON)
def gidx(lat, lon): return np.rint((np.asarray(lat) - LAT0) / STEP).astype(int), np.rint((np.asarray(lon) - LON0) / STEP).astype(int)
def mark_near(src_lat, src_lon, r_km, shape=(NY, NX)):
    """Boolean grid: True at every 0.1 degree point within r_km (great circle) of any source point. Exact at the grid points."""
    out = np.zeros(shape, bool)
    if len(src_lat) == 0: return out
    src_lat = np.asarray(src_lat, float); src_lon = np.asarray(src_lon, float)
    iy, ix = gidx(src_lat, src_lon); dy = int(math.ceil(r_km / 111.0 / STEP)) + 1; dx = int(math.ceil(r_km / (111.32 * math.cos(math.radians(LAT1 + 1))) / STEP)) + 1
    for oy in range(-dy, dy + 1):
        jy = iy + oy; oky = (jy >= 0) & (jy < NY)
        for ox in range(-dx, dx + 1):
            jx = ix + ox; ok = oky & (jx >= 0) & (jx < NX)
            if not ok.any(): continue
            d = hav(src_lat[ok], src_lon[ok], GLAT[jy[ok]], GLON[jx[ok]]); m = d <= r_km
            out[jy[ok][m], jx[ok][m]] = True
    return out
def densify(rings, km=1.0):
    la, lo = [], []
    for r in rings:
        a = np.asarray(r, float)
        for (x0, y0), (x1, y1) in zip(a, np.roll(a, -1, 0)):
            n = max(1, int(math.ceil(float(hav(y0, x0, y1, x1)) / km))); t = np.arange(n) / n
            lo.append(x0 + t * (x1 - x0)); la.append(y0 + t * (y1 - y0))
    return (np.concatenate(la), np.concatenate(lo)) if la else (np.zeros(0), np.zeros(0))
# ---------------- rules ----------------
def floor_outcome(lo, hi):
    """PLAN.md section 5. SPC states 10% or more: the band [0.10, 1.0]. CONSISTENT if the whole interval is at or above 10%, BELOW if the whole interval is under it,
    CANNOT_TELL (STRADDLES_EDGE) otherwise. ABOVE is unreachable (nothing exceeds 1.0)."""
    return K.read(lo, hi, band=(FLOOR, 1.0), edge='closed')
def boot_ratio(num, den, seed=SEED, n=NBOOT):
    num = np.asarray(num, float); den = np.asarray(den, float); D = len(num)
    if D == 0 or den.sum() <= 0: return None, None, None
    rng = np.random.default_rng(seed); w = rng.multinomial(D, np.full(D, 1.0 / D), size=n).astype(float)
    sn = w @ num; sd = w @ den; ok = sd > 0; r = sn[ok] / sd[ok]
    return float(num.sum() / den.sum()), float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))
def in_valid(sec): return (sec >= VALID[0]) & (sec < VALID[1])
def max_gap_in_valid(gaps, failed):
    """gaps: [[a, b], ...] seconds from 1200 UTC between listed file starts. Failed or unreadable files are added as a bound (20 s each) to the largest gap."""
    g = [min(b, VALID[1]) - max(a, VALID[0]) for a, b in gaps if b > VALID[0] and a < VALID[1]]
    return max(g, default=0) + 20 * failed
def rule_selftest():
    t = []
    t.append(floor_outcome(0.20, 0.30) == (K.CONSISTENT, None)); t.append(floor_outcome(0.10, 0.12) == (K.CONSISTENT, None))
    t.append(floor_outcome(0.02, 0.09) == (K.BELOW, None)); t.append(floor_outcome(0.08, 0.12) == (K.CANNOT_TELL, K.STRADDLES_EDGE))
    t.append(floor_outcome(None, None) == (K.CANNOT_TELL, K.NO_INTERVAL_FORMABLE)); t.append(all(floor_outcome(a, b)[0] != K.ABOVE for a, b in ((0.5, 1.0), (0.99, 1.0))))
    # distance: a flash 40.1 km and 40.4 km north of a grid point (primary radius 40.234 km); 16.0 and 16.2 km (secondary 16.093 km)
    p = (35.0, -97.0); iy, ix = gidx(*p)
    for r, a, b in ((RADII['primary'], 40.1, 40.4), (RADII['secondary'], 16.0, 16.2)):
        la_in = p[0] + a / (R_E * math.pi / 180); la_out = p[0] + b / (R_E * math.pi / 180)
        t.append(bool(mark_near([la_in], [p[1]], r)[iy, ix]) and not bool(mark_near([la_out], [p[1]], r)[iy, ix]))
    # east-west at 49 N, where 0.1 degree of longitude is short
    q = (49.0, -100.0); jy, jx = gidx(*q); dlon = 40.1 / (R_E * math.cos(math.radians(49.0)) * math.pi / 180)
    t.append(bool(mark_near([q[0]], [q[1] + dlon], RADII['primary'])[jy, jx]) and not bool(mark_near([q[0]], [q[1] + dlon * 40.5 / 40.1], RADII['primary'])[jy, jx]))
    # time: a flash at 12:59:59 UTC is out, 13:00:00 in, 11:59:59 next day in, 12:00:00 next day out
    t.append(list(in_valid(np.array([3599.0, 3600.0, 86399.0, 86400.0]))) == [False, True, True, False])
    # satellite split: -106.21 is west, -106.19 east
    t.append(list(np.array([-106.21, -106.19]) > SPLIT) == [False, True])
    # polygons: a square with a hole
    sq = [[(-98, 35), (-97, 35), (-97, 36), (-98, 36), (-98, 35)], [(-97.9, 35.1), (-97.1, 35.1), (-97.1, 35.9), (-97.9, 35.9), (-97.9, 35.1)]]
    t.append(list(in_rings(sq, np.array([-97.5, -97.95, -96.5]), np.array([35.5, 35.05, 35.5]))) == [False, True, False])
    # gaps: one hour exactly does not hold; an hour and 20 s does; a gap before 1300 UTC does not count
    t.append(max_gap_in_valid([[5000, 8600]], 0) == 3600 and max_gap_in_valid([[5000, 8620]], 0) > GAP_HOLD and max_gap_in_valid([[0, 3600]], 0) == 0)
    v, lo, hi = boot_ratio([1, 1, 0, 0], [2, 2, 2, 2]); t.append(abs(v - 0.25) < 1e-12 and lo <= 0.25 <= hi)
    d, lo_ = densify([[(-98, 35), (-97, 35), (-97, 36), (-98, 36), (-98, 35)]]); t.append(len(d) > 400)
    return all(t), t
if '--selftest' in sys.argv:
    ok, t = rule_selftest(); print('zeus rule selftest', 'PASSED' if ok else 'FAILED', t); sys.exit(0 if ok and K.selftest() else 1)

# ======================= the reading (runs only with a plan seal) =======================
seal_f = 'data/plan_seal.json'; import hashlib
if not os.path.exists(seal_f): refuse('no data/plan_seal.json. The amended PLAN.md must be committed and sealed before any reading.')
if not os.path.exists('PLAN.md'): refuse('no PLAN.md beside the tick.')
try:
    SEAL = json.load(open(seal_f)); _want = SEAL['plan_sha256']
except Exception as _e: refuse('data/plan_seal.json is unreadable or has no plan_sha256 (%r).' % _e)
if hashlib.sha256(open('PLAN.md', 'rb').read()).hexdigest() != _want: refuse('PLAN.md differs from the sealed plan. No reading formed.')
NOW = time.time(); STAMP = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(NOW))
def days_between(a, b):
    t = calendar.timegm(time.strptime(a, '%Y%m%d')); e = calendar.timegm(time.strptime(b, '%Y%m%d')); out = []
    while t <= e: out.append(time.strftime('%Y%m%d', time.gmtime(t))); t += 86400
    return out
FRAME_DAYS = days_between(WIN0, WIN1)
# ---- domain: 0.1 degree points inside the 48 states (land) plus points within the primary radius of a land point (coastal waters) ----
_, states = shpread.read_zip(STATES)
LON2, LAT2 = np.meshgrid(GLON, GLAT); fl, fa = LON2.ravel(), LAT2.ravel(); land = np.zeros(fl.size, bool)
for s in states:
    if s['STUSPS'] in ('AK', 'HI', 'PR'): continue
    land |= in_rings(s['rings'], fl, fa)
LAND = land.reshape(NY, NX)
DOMAIN = LAND | mark_near(LAT2[LAND], LON2[LAND], RADII['primary'])
EAST = LON2 > SPLIT
log('domain points', int(DOMAIN.sum()), 'land', int(LAND.sum()), 'east', int((DOMAIN & EAST).sum()), 'west', int((DOMAIN & ~EAST).sum()))
# ---- stated side ----
OTL = json.load(open('data/outlooks_cat13.json'))
fmt_ok = all(all(k in OTL[d] for k in ('issue', 'expire', 'prodiss', 'layers')) for d in OTL)
# ---- per day ----
held = []; rows = []; POINTS = {k: [] for k in RADII}; FL = {k: [] for k in RADII}
for d in FRAME_DAYS:
    o = OTL.get(d)
    if o is None: held.append(dict(day=d, why='no 1300 UTC Day 1 outlook in the IEM archive')); continue
    mans = {}; why = None
    for slot in ('east', 'west'):
        mf = 'data/glm/%s/%s.json' % (slot, d)
        if not os.path.exists(mf): why = 'GLM %s day not fetched' % slot; break
        m = json.load(open(mf)); mans[slot] = m
        g = max_gap_in_valid(m.get('gaps_s_from_1200', []), m['files_failed'] + m['files_unreadable'])
        if g > GAP_HOLD: why = 'GLM %s gap of %d s in the valid period' % (slot, g); break
    if why: held.append(dict(day=d, why=why)); continue
    recs = [rings for c in CATS for rings in o['layers'].get(c, [])]
    thunder = np.zeros(fl.size, bool)
    for rings in recs: thunder |= in_rings(rings, fl, fa)
    TH = thunder.reshape(NY, NX) & DOMAIN
    # flashes: product quality flag good (0), inside the valid period; each point reads its own satellite, each flash belongs to the satellite of its side
    fx = {}
    for slot in ('east', 'west'):
        z = np.load('data/glm/%s/%s.npz' % (slot, d)); ok = (z['qf'] == 0) & in_valid(z['sec'])
        la, lo = z['lat'][ok].astype(float), z['lon'][ok].astype(float)
        side = lo > SPLIT if slot == 'east' else lo <= SPLIT
        fx[slot] = (la, lo, side, int((~(z['qf'] == 0) & in_valid(z['sec'])).sum()))
    # thunder boundary for the flash-side cell (inside a drawn area, or within the radius of its edge, densified at 1 km)
    bl, bo = (np.concatenate(x) if x else np.zeros(0) for x in zip(*[densify(r) for r in recs])) if recs else (np.zeros(0), np.zeros(0))
    row = dict(day=d, thunder_points=int(TH.sum()), layers=sorted(o['layers']), qf_dropped={s: fx[s][3] for s in fx},
               glm={s: dict(platform=mans[s]['platform'], files=mans[s]['files_listed'], failed=mans[s]['files_failed'] + mans[s]['files_unreadable'], max_gap_s=mans[s].get('max_gap_s')) for s in mans})
    for k, r in RADII.items():
        hitE = mark_near(fx['east'][0], fx['east'][1], r) & EAST; hitW = mark_near(fx['west'][0], fx['west'][1], r) & ~EAST
        HIT = (hitE | hitW) & DOMAIN
        row['hit_points_' + k] = int((HIT & TH).sum()); row['domain_lightning_points_' + k] = int(HIT.sum())
        n_all = 0; n_out = 0
        for s in ('east', 'west'):
            la, lo, side, _ = fx[s]; iy, ix = gidx(la, lo); inb = (iy >= 0) & (iy < NY) & (ix >= 0) & (ix < NX)
            dom = np.zeros(len(la), bool); dom[inb] = DOMAIN[iy[inb], ix[inb]]; sel = side & dom
            la, lo = la[sel], lo[sel]; n_all += len(la)
            if not len(la): continue
            inside = np.zeros(len(la), bool)
            for rings in recs: inside |= in_rings(rings, lo, la)
            near = inside.copy(); rest = np.nonzero(~inside)[0]
            if len(rest) and len(bl):
                # exact distance from each remaining flash to the densified edge, in blocks, prefiltered by a box
                for c0 in range(0, len(rest), 2000):
                    ii = rest[c0:c0 + 2000]; dmin = np.full(len(ii), np.inf)
                    for v0 in range(0, len(bl), 5000):
                        vb, vo = bl[v0:v0 + 5000], bo[v0:v0 + 5000]
                        dmin = np.minimum(dmin, hav(la[ii][:, None], lo[ii][:, None], vb[None, :], vo[None, :]).min(1))
                    near[ii] = dmin <= r
            n_out += int((~near).sum())
        row['flashes_' + k] = n_all; row['flashes_outside_' + k] = n_out
    rows.append(row)
    log(d, 'thunder pts', row['thunder_points'], 'hit25', row['hit_points_primary'], 'hit10', row['hit_points_secondary'], 'flashes', row['flashes_primary'], 'outside25', row['flashes_outside_primary'])
# ---- known-good gates ----
kg = {}
kg['format'] = fmt_ok and all(json.load(open('data/glm/%s/%s.json' % (s, r['day'])))['files_listed'] > 0 for r in rows for s in ('east', 'west'))
# gate 2: stated reader. 20 point-days with a fixed seed: inside-thunder from our reader against IEM's outlook-by-point service at one minute after the product issue time
pc_f = 'data/cache/pointcheck.json'; os.makedirs('data/cache', exist_ok=True); pc = json.load(open(pc_f)) if os.path.exists(pc_f) else {}
rng = random.Random(SEED); dd = [r['day'] for r in rows]; picks = []
for _ in range(20 if dd else 0):
    d = rng.choice(dd); jy = rng.randrange(NY); jx = rng.randrange(NX)
    while not DOMAIN[jy, jx]: jy = rng.randrange(NY); jx = rng.randrange(NX)
    picks.append((d, jy, jx))
agree = 0; pc_rows = []
for d, jy, jx in picks:
    la, lo = float(GLAT[jy]), float(GLON[jx]); key = '%s_%.2f_%.2f' % (d, la, lo)
    recs = [rings for c in CATS for rings in OTL[d]['layers'].get(c, [])]
    ours = bool(any(in_rings(r, np.array([lo]), np.array([la]))[0] for r in recs))
    if key not in pc and not OFF:
        pd = OTL[d]['prodiss']; v = '%s-%s-%sT%s:%sZ' % (pd[:4], pd[4:6], pd[6:8], pd[8:10], pd[10:12])
        v = time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime(calendar.timegm(time.strptime(v, '%Y-%m-%dT%H:%MZ')) + 60))
        try:
            with urllib.request.urlopen(urllib.request.Request(IEM_PT % (la, lo, v), headers={'User-Agent': UA}), timeout=60) as rr: pc[key] = json.loads(rr.read())
            time.sleep(1.5)
        except Exception as e: log('point check failed', key, repr(e)[:80])
    ans = pc.get(key)
    if ans is None: pc_rows.append(dict(day=d, lat=la, lon=lo, ours=ours, iem=None)); continue
    iem = any(x.get('day') == 1 and x.get('outlook_type') == 'C' and x.get('category') == 'CATEGORICAL' and x.get('issue', '').startswith('%s-%s-%sT13:00' % (d[:4], d[4:6], d[6:8])) for x in ans.get('data', []))
    agree += ours == iem; pc_rows.append(dict(day=d, lat=la, lon=lo, ours=ours, iem=iem))
json.dump(pc, open(pc_f, 'w'))
kg['stated_reader'] = sum(r['iem'] is not None for r in pc_rows) == len(picks) and agree >= len(picks) - 1
# gate 3: the GLM reader. Every kept flash time lies inside its convective day; lat and lon inside the box
def _glm_ok(r):
    for s in ('east', 'west'):
        z = np.load('data/glm/%s/%s.npz' % (s, r['day']))
        if len(z['sec']) and (z['sec'].min() < 0 or z['sec'].max() >= 86400 or z['lat'].min() < 23 or z['lon'].max() > -65): return False
    return True
kg['glm_reader'] = all(_glm_ok(r) for r in rows)
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()): _kit_ok = K.selftest()
kg['rule'] = rule_selftest()[0] and _kit_ok
GATE = all(kg.values())
# ---- cells ----
def cell(k):
    num = [r['hit_points_' + k] for r in rows]; den = [r['thunder_points'] for r in rows]
    v, lo, hi = boot_ratio(num, den, seed=SEED + (1 if k == 'primary' else 2))
    out, why = floor_outcome(lo, hi)
    frame_note = None
    if len(rows) < len(FRAME_DAYS):   # PLAN section 5: a frame item not met (a held day) reads CANNOT_TELL with the reason named; the held days are listed in held
        frame_note = '%d of %d frame days held: %s' % (len(FRAME_DAYS) - len(rows), len(FRAME_DAYS), ', '.join(h['day'] for h in held))
        out, why = K.CANNOT_TELL, K.NO_INTERVAL_FORMABLE
    c = dict(radius_mi=round(RADII[k] / MI, 3), radius_km=round(RADII[k], 3), days=len(rows), thunder_point_days=int(sum(den)), hit_point_days=int(sum(num)),
             value=None if v is None else round(v, 4), lo=None if lo is None else round(lo, 4), hi=None if hi is None else round(hi, 4), floor=FLOOR, outcome=out, reason=why, frame_note=frame_note)
    if not GATE and c['outcome'] in K.OUTCOMES: c['outcome_before_gate'] = c['outcome']; c['outcome'] = K.CANNOT_TELL; c['reason'] = K.NO_INTERVAL_FORMABLE
    fo = [r['flashes_outside_' + k] for r in rows]; fa_ = [r['flashes_' + k] for r in rows]; sv, slo, shi = boot_ratio(fo, fa_, seed=SEED + 3 + (k == 'secondary'))
    s = dict(radius_mi=round(RADII[k] / MI, 3), flashes=int(sum(fa_)), outside=int(sum(fo)), value=None if sv is None else round(sv, 4), lo=None if slo is None else round(slo, 4), hi=None if shi is None else round(shi, 4), outcome=None)
    return c, s
head, outside = cell('primary'); head10, outside10 = cell('secondary')
partial = len(rows) < len(FRAME_DAYS)
labels = LABELS + (['PRELIMINARY: partial window'] if partial else [])
summary = dict(desk='ZEUS', publisher='Heuremen LLC', generated=STAMP, updated=STAMP, plan='PLAN.md', plan_seal=SEAL, labels=labels,
    claim=dict(stated='SPC Day 1 Convective Outlook general thunder line: "a 10% or higher probability of thunderstorms during the valid period" (SPC_probotlk_info.html; NWSI 10-512 section 2.3.3)',
               radius='SPC states no radius for thunder. The primary radius, 25 statute miles, is borrowed from the SPC severe-probability definition; 10 statute miles is printed beside it.',
               lightning_type='GLM counts all lightning it sees from orbit, in-cloud and cloud-to-ground alike. A thunderstorm forecast is about thunder heard at the ground. Stated with every result, not measured.',
               glm_de='GLM requirement 70 percent flash detection efficiency; measured 0.81 bulk for GOES-18 (Jan to Sep 2023), lower near the limb; no published GOES-19 figure found. The observed share is a floor.'),
    frame=dict(issuance='1300 UTC Day 1', window=[WIN0, WIN1], window_label='30-day window, late autumn', frame_days=len(FRAME_DAYS), grid_deg=STEP, domain_points=int(DOMAIN.sum()), land_points=int(LAND.sum()),
               domain='0.1 degree points inside the 48 contiguous states plus points within 25 statute miles of such a point (coastal waters)',
               split_lon=SPLIT, east='GOES-19', west='GOES-18', quality='flash_quality_flag 0 (good_quality_qf) only', valid='1300 UTC to 1200 UTC next day',
               hold_gap_s=GAP_HOLD, bootstrap=dict(resamples=NBOOT, seed=SEED, block='outlook day')),
    gates=dict(kg, passed=GATE, point_check=dict(agree=agree, of=len(pc_rows), rows=pc_rows)),
    zeus=dict(tstm_hit_share=head, tstm_hit_share_10mi=head10, flash_outside_share=outside),
    held=held, days=rows, days_read=len(rows), days_held=len(held), partial=partial,
    after_data_note='')
json.dump(summary, open('summary_zeus.json.tmp', 'w'), indent=1); os.replace('summary_zeus.json.tmp', 'summary_zeus.json')
json.dump(summary, open('data/zeus_live.json.tmp', 'w'), separators=(',', ':')); os.replace('data/zeus_live.json.tmp', 'data/zeus_live.json')
# the rows the reproduce kit recomputes the headline from (reproduce_kits/extracts/zeus_score.py)
json.dump(dict(generated=STAMP, frame_days=len(FRAME_DAYS), gate_passed=GATE, held=held, seed=SEED, nboot=NBOOT, floor=FLOOR,
               days=[dict(day=r['day'], thunder_points=r['thunder_points'], hit_points_primary=r['hit_points_primary'], hit_points_secondary=r['hit_points_secondary']) for r in rows]),
          open('data/zeus_rows.json.tmp', 'w'), indent=1); os.replace('data/zeus_rows.json.tmp', 'data/zeus_rows.json')
PUB_FAILED = False
if PUB:   # 22 Nov 2026: the one Cloudflare part (lib/cf.py kv_put: kv token, rings on failure). A failed put exits non-zero after the history line.
    try:
        sys.path.insert(0, os.path.expanduser('~/forge/lib')); import cf
        PUB_FAILED = not cf.kv_put('zeus_live', os.path.join(H, 'data', 'zeus_live.json'), who='zeus_tick.py')
    except Exception as _e: log('publish part failed', repr(_e)[:200]); PUB_FAILED = True
    log('zeus_live', 'publish FAILED' if PUB_FAILED else 'published')
with open('data/zeus_history.jsonl', 'a') as f:
    f.write(json.dumps(dict(t=STAMP, gate=GATE, head=(head['value'], head['lo'], head['hi'], head['outcome'], head['reason']), head10=(head10['value'], head10['outcome']), outside=outside['value'], days=len(rows), held=len(held))) + '\n')
log('gates', kg); log('headline', head); log('10 mi', head10); log('outside', outside); log('held', held)
if PUB_FAILED: sys.exit(3)
