"""airq_live_score.py: the live panel of airq_index/airq_live_tick.py (PLAN.md Addenda 2 and 3), offline, from what that tick kept. The sensor pick
(the median-RMSE pair of each monitor of the main read, from data/pairs.json), metrics(), meets(), corrected(), ab_ok(), outcome() and the rolling
evaluation are copied as written. data/live_days.json holds the AirNow daily means (ref) and the PurpleAir daily rows (sens) the tick read. The
window is the last 60 UTC days the tick read: it ends on the newest AirNow day in data/live_days.json, since the tick adds a ref entry for every day
of its window on each run and its window end only moves forward. No key and no network. Writes out.json with the live block the feed serves."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import json, math, collections, datetime
import heuremen_kit as K
MINDAYS, WINDOW = 30, 60
def metrics(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n; sxx = sum((a - mx) ** 2 for a in x); sxy = sum((a - mx) * (b - my) for a, b in zip(x, y)); syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0: return None
    s = sxy / sxx; rmse = math.sqrt(sum((b - a) ** 2 for a, b in zip(x, y)) / n)
    return dict(slope=s, intercept=my - s * mx, r2=sxy * sxy / (sxx * syy), rmse=rmse, nrmse=(100 * rmse / mx if mx > 0 else None))
def meets(m): return bool(m and 0.65 <= m['slope'] <= 1.35 and -5 <= m['intercept'] <= 5 and m['r2'] >= 0.70 and (m['rmse'] <= 7 or (m['nrmse'] is not None and m['nrmse'] <= 30)))
def corrected(cf1, rh): return 0.524 * cf1 - 0.0862 * rh + 5.75
def ab_ok(a, b):
    d = abs(a - b); return d < 5 or (a + b > 0 and 2 * d / (a + b) * 100 < 61)
def outcome(n_not, n):
    if n == 0: return K.CANNOT_TELL, K.NO_INTERVAL_FORMABLE
    if n < 30: return K.CANNOT_TELL, K.TOO_WIDE_TO_RESOLVE
    lo, hi = K.wilson(n_not, n); lo = 0.0 if n_not == 0 else lo; hi = 1.0 if n_not == n else hi
    return K.read(lo, hi, bound=0.5)
# ---- selected sensors: the median-RMSE pair of each monitor of the main read (as written in the tick)
pairs = json.load(open('data/pairs.json')); by = collections.defaultdict(list)
for p in pairs: by[p['monitor']].append(p)
sel = {}
for m, ps in by.items():
    ps = sorted([p for p in ps if p.get('R3')], key=lambda p: p['R3']['rmse'])
    if ps: sel[m] = ps[(len(ps) - 1) // 2]['sensor']
mons = sorted(sel)
# ---- the window the tick read: 60 UTC days ending on its newest AirNow day
live = json.load(open('data/live_days.json')); ref = live.get('ref', {}); sens = live.get('sens', {})
end = datetime.date.fromisoformat(max(ref))
days = [end - datetime.timedelta(days=k) for k in range(WINDOW - 1, -1, -1)]
# ---- rolling evaluation (as written in the tick)
res = {'R1': [], 'R2': [], 'R3': []}; used = 0
for m in mons:
    X = []; R = {'R1': [], 'R2': [], 'R3': []}
    for d in days:
        rf = ref.get(d.isoformat(), {}).get(m); s = sens.get(d.isoformat(), {}).get(m)
        if rf is None or not s: continue
        aa, ab, ca, cb, rh = s
        if not ab_ok(ca, cb): continue
        X.append(rf); R['R1'].append((aa + ab) / 2); R['R2'].append((ca + cb) / 2); R['R3'].append(corrected((ca + cb) / 2, rh))
    if len(X) < MINDAYS: continue
    used += 1; X = X[-MINDAYS:]
    for k in R: res[k].append(metrics(X, R[k][-MINDAYS:]))
NAME = {'R1': 'Map reading (atm channels, raw)', 'R2': 'cf_1 channels, raw', 'R3': 'cf_1 corrected for humidity (Barkjohn 2021)'}
live_cmp = {}
for k in ('R1', 'R2', 'R3'):
    ms = [m for m in res[k] if m]; n = len(ms); nn = sum(1 for m in ms if not meets(m)); lo, hi = K.wilson(nn, n) if n else (0, 1); _o, _w = outcome(nn, n)
    live_cmp[NAME[k]] = dict(of=n, n=nn, share=round(nn / n, 4) if n else None, share_lo=round(lo, 4), share_hi=round(hi, 4), outcome=_o, reason=_w)
sens_days = [d for d in days if sens.get(d.isoformat())]; sens_through = max(sens_days) if sens_days else None
out = dict(live=dict(window='the last %d UTC days' % WINDOW, monitors_in_panel=len(mons), monitors_with_30_kept_days=used, comparison=live_cmp,
                     sensor_days_through=(sens_through.isoformat() if sens_through else None)))
json.dump(out, open('out.json', 'w'), indent=1)
