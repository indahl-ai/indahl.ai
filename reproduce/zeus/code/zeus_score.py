"""zeus_score.py: the headline cell of zeus_index/zeus_tick.py (FLOOR, SEED, NBOOT, boot_ratio(), floor_outcome() and cell(), as written) over the
per-day counts that run wrote to data/zeus_rows.json: thunder-area grid points per outlook day and how many had a GLM flash within 25 and within
10 statute miles. The GLM files (about 1.4 GB a satellite a day, streamed and never stored) and the grid reduction stay with the desk; this kit
starts from the counts. A failed gate and held days are already written into the rows file. Writes out.json."""
import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import json
import numpy as np
import heuremen_kit as K
R = json.load(open('data/zeus_rows.json')); FLOOR = R['floor']; SEED = R['seed']; NBOOT = R['nboot']
def boot_ratio(num, den, seed=SEED, n=NBOOT):
    num = np.asarray(num, float); den = np.asarray(den, float); D = len(num)
    if D == 0 or den.sum() <= 0: return None, None, None
    rng = np.random.default_rng(seed); w = rng.multinomial(D, np.full(D, 1.0 / D), size=n).astype(float)
    sn = w @ num; sd = w @ den; ok = sd > 0; r = sn[ok] / sd[ok]
    return float(num.sum() / den.sum()), float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))
def floor_outcome(lo, hi): return K.read(lo, hi, band=(FLOOR, 1.0), edge='closed')
rows = R['days']
def cell(k):
    num = [r['hit_points_' + k] for r in rows]; den = [r['thunder_points'] for r in rows]
    v, lo, hi = boot_ratio(num, den, seed=SEED + (1 if k == 'primary' else 2))
    out, why = floor_outcome(lo, hi)
    if len(rows) < R['frame_days']: out, why = K.CANNOT_TELL, K.NO_INTERVAL_FORMABLE
    c = dict(days=len(rows), thunder_point_days=int(sum(den)), hit_point_days=int(sum(num)), value=None if v is None else round(v, 4),
             lo=None if lo is None else round(lo, 4), hi=None if hi is None else round(hi, 4), floor=FLOOR, outcome=out, reason=why)
    if not R['gate_passed'] and c['outcome'] in K.OUTCOMES: c['outcome'] = K.CANNOT_TELL; c['reason'] = K.NO_INTERVAL_FORMABLE
    return c
json.dump(dict(zeus=dict(tstm_hit_share=cell('primary'), tstm_hit_share_10mi=cell('secondary'))), open('out.json', 'w'), indent=1)
