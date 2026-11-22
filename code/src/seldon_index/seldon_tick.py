#!/usr/bin/env python3
"""seldon_tick.py: SELDON reader (see PLAN.md, frame fixed before any outcome was read). Sets CBO's stated two-thirds ranges for the deficit, debt
held by the public and average real GDP growth beside the outcomes, and lists the WEO's stated probabilities for global growth events.
Inputs, all built or fetched before this runs: data/stated_ranges.json (build_stated.py, the ranges with their quotes checked against the reports),
data/imf_events.json (build_imf.py), data/raw/cbo_actuals (US-CBO/eval-projections input_data and output_data), data/raw/cbo_data (US-CBO/cbo-data
economic vintages). Writes summary_seldon.json, data/seldon_live.json, data/seldon_rows.json, data/seldon_history.jsonl.
--selftest: rule checks only, no data. Standard library only (busenv python -I)."""
import os, sys, json, time, csv, random, hashlib, collections as C
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
PUB = '--publish' in sys.argv or os.environ.get('HEUREMEN_PUBLISH') == '1'   # the tick bus exports HEUREMEN_PUBLISH=1, as for the other desks; a kit or test copy never publishes
def refuse(why, code=4):
    print('seldon: REFUSED: ' + why, file=sys.stderr, flush=True); sys.exit(code)
def log(*a): print('seldon:', *a, file=sys.stderr, flush=True)
# ---------------- frame (PLAN.md sections 4 and 5) ----------------
STATED_SHARE = 0.667            # "roughly two-thirds, read as 0.667"
LONG_H = 3                      # a range counts toward the headline when its target year is at least three years after the report year
LAST_FY = 2025                  # the last fiscal year with actuals in the Jan 2026 accuracy report. Calendar 2025 ends after FY 2025, so it is held
MIN_RANGES = 10                 # fewer than 10 ranges: CANNOT_TELL
NBOOT = 10000; SEED = 20261122
LABELS = ['PRELIMINARY: first run, not refereed']
# growth outturn, first published (PLAN.md section 4): the first cbo-data vintage after the period ended in which the period's last year is actual.
# Read from the vintages before this tick ran: the winter outlooks carry the year just ended as projected (calendar_2024-02 has 2023 projected,
# calendar_2025-01 has 2024 projected), the spring and summer ones as actual (calendar_2024-06 2023 actual, calendar_2025-09 2024 actual).
FIRST = {2020: 'historical_economic_quarterly_2022-05.csv', 2021: 'historical_economic_quarterly_2022-05.csv', 2022: 'historical_economic_quarterly_2023-07.csv',
         2023: 'historical_economic_quarterly_2024-06.csv', 2024: 'SPLICE_2025-09'}
REVISED = 'historical_economic_annual_cy_2026-02.csv'
OUTS = ('ABOVE', 'BELOW', 'CONSISTENT', 'CANNOT_TELL')
# ---------------- rules ----------------
def outcome(lo, hi, n):
    """PLAN.md section 5. CONSISTENT if the 95% interval contains 0.667, ABOVE if the whole interval is above it, BELOW if the whole interval is
    below it, CANNOT_TELL with the reason when fewer than 10 ranges or no interval."""
    if n < MIN_RANGES: return 'CANNOT_TELL', 'fewer than %d ranges (%d)' % (MIN_RANGES, n)
    if lo is None or hi is None: return 'CANNOT_TELL', 'no interval formable'
    if lo > STATED_SHARE: return 'ABOVE', None
    if hi < STATED_SHARE: return 'BELOW', None
    return 'CONSISTENT', None
def decimals(r): return 0 if r['measure'] == 'debt' else 1
def rnd(x, d):
    """Half away from zero at d decimals, as a printed figure reads."""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))
def is_hit(v, r):
    """PLAN.md section 4: inside the range, endpoints included, the range read at its printed rounding. The outcome is rounded to the decimals the
    range prints (whole percent for debt, one decimal otherwise) and then compared."""
    x = rnd(v, decimals(r)); return r['lo'] <= x <= r['hi']
def block_boot(rows, seed=SEED, n=NBOOT):
    """Share of hits with a 95% percentile interval from a bootstrap that draws whole reports (PLAN.md section 4)."""
    if not rows: return None, None, None
    by = C.OrderedDict()
    for r in rows: by.setdefault(r['report_month'], []).append(1 if r['hit'] else 0)
    blocks = list(by.values()); rng = random.Random(seed); sh = []
    for _ in range(n):
        pick = [blocks[rng.randrange(len(blocks))] for _ in blocks]; k = sum(sum(b) for b in pick); m = sum(len(b) for b in pick); sh.append(k / m)
    sh.sort(); v = sum(sum(b) for b in blocks) / sum(len(b) for b in blocks)
    return v, sh[int(0.025 * n)], sh[int(0.975 * n) - 1]
def horizon(r): return (r.get('end') or r.get('year')) - int(r['report_month'][:4])
def target_ends_by_fy(r):
    if r['measure'] in ('deficit', 'debt'): return r['year'] <= LAST_FY
    return (r.get('end') or r.get('year')) <= LAST_FY - 1          # a calendar year ends after the fiscal year of the same number
def rule_selftest():
    t = []
    t.append(outcome(0.60, 0.80, 13) == ('CONSISTENT', None)); t.append(outcome(0.70, 0.95, 13) == ('ABOVE', None)); t.append(outcome(0.30, 0.60, 13) == ('BELOW', None))
    t.append(outcome(0.60, 0.80, 9)[0] == 'CANNOT_TELL'); t.append(outcome(None, None, 13)[0] == 'CANNOT_TELL'); t.append(outcome(0.667, 0.9, 13) == ('CONSISTENT', None))
    t.append(is_hit(97.4, dict(measure='debt', lo=79, hi=97)) and not is_hit(97.5, dict(measure='debt', lo=79, hi=97)) and is_hit(78.5, dict(measure='debt', lo=79, hi=97)))
    t.append(is_hit(6.74, dict(measure='deficit', lo=2.9, hi=6.7)) and not is_hit(6.75, dict(measure='deficit', lo=2.9, hi=6.7)) and is_hit(-0.95, dict(measure='growth', lo=-1.0, hi=3.5)))
    t.append(horizon(dict(report_month='2019-01', year=2024)) == 5 and horizon(dict(report_month='2017-01', end=2020, start=2017)) == 3)
    t.append(target_ends_by_fy(dict(measure='deficit', year=2025)) and not target_ends_by_fy(dict(measure='growth', end=2025)) and target_ends_by_fy(dict(measure='growth', year=2024)))
    rows = [dict(report_month='a', hit=1), dict(report_month='a', hit=0), dict(report_month='b', hit=1)]
    v, lo, hi = block_boot(rows, n=2000); t.append(abs(v - 2 / 3) < 1e-12 and lo <= v <= hi)
    return all(t), t
if '--selftest' in sys.argv:
    ok, t = rule_selftest(); print('seldon rule selftest', 'PASSED' if ok else 'FAILED', t); sys.exit(0 if ok else 1)

# ======================= the reading (runs only with a plan seal) =======================
seal_f = 'data/plan_seal.json'
if not os.path.exists(seal_f): refuse('no data/plan_seal.json. PLAN.md must be committed and sealed before any reading.')
if not os.path.exists('PLAN.md'): refuse('no PLAN.md beside the tick.')
try:
    SEAL = json.load(open(seal_f)); _want = SEAL['plan_sha256']
except Exception as _e: refuse('data/plan_seal.json is unreadable or has no plan_sha256 (%r).' % _e)
if hashlib.sha256(open('PLAN.md', 'rb').read()).hexdigest() != _want: refuse('PLAN.md differs from the sealed plan. No reading formed.')
for f in ('data/stated_ranges.json', 'data/imf_events.json', 'data/raw/cbo_actuals/actuals.csv', 'data/raw/cbo_actuals/actual_GDP.csv',
          'data/raw/cbo_actuals/deficit_actuals_pct_GDP.csv', 'data/raw/cbo_actuals/debt_actuals_pct_GDP.csv', 'data/raw/cbo_data/' + REVISED,
          'data/raw/cbo_data/economic_projections_calendar_2025-09.csv', 'data/raw/cbo_data/historical_economic_quarterly_2025-01.csv') + tuple('data/raw/cbo_data/' + v for v in set(FIRST.values()) if not v.startswith('SPLICE')):
    if not os.path.exists(f): refuse('input missing: %s. No reading formed.' % f)
NOW = time.time(); STAMP = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(NOW))
ST = json.load(open('data/stated_ranges.json'))
if not ST.get('built') or not ST.get('quotes_checked') or not ST.get('ranges'): refuse('data/stated_ranges.json was not built by build_stated.py (no built stamp, no checked quotes).')
# ---- known-good gates ----
kg = {}
_bad = [f for f, s in ST['report_sha256'].items() if os.path.exists('data/raw/cbo_reports/%s.pdf' % f) and hashlib.sha256(open('data/raw/cbo_reports/%s.pdf' % f, 'rb').read()).hexdigest() != s]
_miss = sorted({r['file'] for r in ST['ranges']} - set(ST['report_sha256']))
kg['stated_files'] = not _bad and not _miss
if not kg['stated_files']: log('stated file check: changed', _bad, 'no hash', _miss)
# ---- budget actuals: actuals.csv over actual_GDP.csv, fiscal years ----
GDP = {int(r['fiscal_year']): float(r['GDP']) for r in csv.DictReader(open('data/raw/cbo_actuals/actual_GDP.csv'))}
ACT = {}
for r in csv.DictReader(open('data/raw/cbo_actuals/actuals.csv')):
    if r['category'] == 'Total' and r['subcategory'] == 'Total' and r['component'] in ('deficit', 'debt'): ACT[(r['component'], int(r['fiscal_year']))] = float(r['actual_value'])
def budget_pct(comp, fy):
    if (comp, fy) not in ACT or fy not in GDP: return None
    v = ACT[(comp, fy)] / GDP[fy] * 100.0
    return -v if comp == 'deficit' else v                          # actuals.csv carries a deficit as a negative balance
# gate: our percent of GDP equals CBO's own published one (output_data/*_actuals_pct_GDP.csv, one decimal) for every fiscal year 2016 to 2025
cbo_pct = {}
for comp in ('deficit', 'debt'):
    for r in csv.DictReader(open('data/raw/cbo_actuals/%s_actuals_pct_GDP.csv' % comp)):
        if r['category'] == 'Total' and r['subcategory'] == 'Total': cbo_pct[(comp, int(r['fiscal_year']))] = float(r['actuals_pct_GDP'])
_pct_ok = []
for comp in ('deficit', 'debt'):
    for fy in range(2016, LAST_FY + 1):
        ours = budget_pct(comp, fy); theirs = cbo_pct.get((comp, fy))
        _pct_ok.append(ours is not None and theirs is not None and abs(rnd(ours, 1) - (-theirs if comp == 'deficit' else theirs)) < 1e-9)
kg['budget_actuals'] = all(_pct_ok)
# ---- growth: calendar-year real GDP levels by vintage ----
def load(f):
    out = {}
    for r in csv.DictReader(open('data/raw/cbo_data/' + f)):
        if r['variable'] == 'real_gdp': out[r['date']] = (float(r['value']), r.get('estimate_type'))
    return out
_V = {}
def V(f):
    if f not in _V: _V[f] = load(f)
    return _V[f]
def annual(f, y):
    d = V(f)
    if str(y) in d: return d[str(y)][0]
    q = [d.get('%dq%d' % (y, i)) for i in range(1, 5)]
    return None if any(x is None for x in q) else sum(x[0] for x in q) / 4.0
CAL0925 = 'economic_projections_calendar_2025-09.csv'; Q0125 = 'historical_economic_quarterly_2025-01.csv'
def level_first(end, y):
    """Level of year y in the first-published vintage for a period ending in `end`."""
    f = FIRST[end]
    if f != 'SPLICE_2025-09': return annual(f, y)
    # 2024: calendar_2025-09 carries 2022 to 2024 as actual and no earlier year. Earlier years come from the January 2025 vintage, which holds the
    # same BEA vintage (gate splice_2025: 2022 and 2023 equal in both, to the printed 0.1)
    d = V(CAL0925)
    if str(y) in d and d[str(y)][1] == 'actual': return d[str(y)][0]
    return annual(Q0125, y)
def growth(level, start, end):
    a, b = level(start - 1), level(end)
    if a is None or b is None: return None
    return ((b / a) ** (1.0 / (end - start + 1)) - 1.0) * 100.0
# gates: quarterly averages reproduce the calendar files where both exist, the 2025-09 splice holds one BEA vintage, the flags say actual
def _cal(f, y): return V(f).get(str(y))
_g = []
for qf, cf_, yrs in (('historical_economic_quarterly_2024-06.csv', 'economic_projections_calendar_2024-06.csv', (2022, 2023)), (Q0125, 'economic_projections_calendar_2025-01.csv', (2022, 2023))):
    for y in yrs:
        c = _cal(cf_, y); a = annual(qf, y); _g.append(c is not None and a is not None and abs(rnd(a, 1) - c[0]) <= 0.051)
kg['quarterly_to_calendar'] = all(_g)
kg['splice_2025'] = all(abs(rnd(annual(Q0125, y), 1) - V(CAL0925)[str(y)][0]) <= 0.051 for y in (2022, 2023)) and V(CAL0925)['2024'][1] == 'actual'
kg['flags'] = _cal('economic_projections_calendar_2024-06.csv', 2023)[1] == 'actual' and _cal('economic_projections_calendar_2024-02.csv', 2023)[1] == 'projected' and _cal('economic_projections_calendar_2025-01.csv', 2024)[1] == 'projected'
kg['rule'] = rule_selftest()[0]
GATE = all(kg.values())
# ---- every range ----
rows, held, short, refused = [], [], [], []
for r in ST['ranges']:
    o = dict(id=r['id'], report=r['report'], report_month=r['report_month'], file=r['file'], measure=r['measure'], lo=r['lo'], hi=r['hi'],
             year=r.get('year'), start=r.get('start'), end=r.get('end'), horizon=horizon(r), quote=r['quote'][-1]['text'], page=r['quote'][-1]['page'], note=(r.get('note') or '').replace('; ', '. ').replace(';', ',') or None)   # house copy: no semicolons in the public feed
    if not target_ends_by_fy(r):
        o['why'] = 'target year ends after fiscal year %d, no actual yet' % LAST_FY; held.append(o); continue
    if r['measure'] in ('deficit', 'debt'):
        v = budget_pct(r['measure'], r['year'])
        if v is None: o['why'] = 'no actual in actuals.csv'; refused.append(o); continue
        o['outturn'] = round(v, 4); o['outturn_source'] = 'US-CBO/eval-projections actuals.csv over actual_GDP.csv, fiscal year %d' % r['year']; o['outturn_revised'] = None
    else:
        s, e = (r['start'], r['end']) if r.get('start') else (r['year'], r['year'])
        if e not in FIRST: o['why'] = 'no first-published vintage named for %d' % e; refused.append(o); continue
        v = growth(lambda y: level_first(e, y), s, e)
        if v is None: o['why'] = 'a level is missing in the vintage'; refused.append(o); continue
        o['outturn'] = round(v, 4); o['outturn_source'] = 'US-CBO/cbo-data %s, calendar-year real GDP %d to %d' % ('calendar_2025-09 with quarterly_2025-01' if FIRST[e].startswith('SPLICE') else FIRST[e].replace('.csv', ''), s - 1, e)
        rv = growth(lambda y: annual(REVISED, y), s, e); o['outturn_revised'] = None if rv is None else round(rv, 4)
        o['hit_revised'] = None if rv is None else is_hit(rv, r)
    o['outturn_printed'] = rnd(o['outturn'], decimals(r)); o['hit'] = is_hit(o['outturn'], r); o['hit_unrounded'] = r['lo'] <= o['outturn'] <= r['hi']
    o['side'] = 'inside' if o['hit'] else ('above' if o['outturn_printed'] > r['hi'] else 'below')
    (rows if o['horizon'] >= LONG_H else short).append(o)
def cell(rs, key='hit', seed=SEED):
    use = [dict(x, hit=x[key]) for x in rs if x.get(key) is not None]
    v, lo, hi = block_boot(use, seed=seed)
    out, why = outcome(lo, hi, len(use))
    c = dict(ranges=len(use), hits=sum(1 for x in use if x['hit']), reports=len({x['report_month'] for x in use}), value=None if v is None else round(v, 4),
             lo=None if lo is None else round(lo, 4), hi=None if hi is None else round(hi, 4), stated=STATED_SHARE, outcome=out, reason=why)
    if not GATE and c['outcome'] in OUTS[:3]: c['outcome_before_gate'] = c['outcome']; c['outcome'] = 'CANNOT_TELL'; c['reason'] = 'a known-good check did not pass'
    return c
head = cell(rows)
head_strict = cell(rows, 'hit_unrounded', SEED + 1)
revised_rows = [dict(x, hit_revised=x['hit_revised']) if x['measure'] == 'growth' else dict(x, hit_revised=x['hit']) for x in rows]
head_rev = cell(revised_rows, 'hit_revised', SEED + 2)
short_c = cell(short, 'hit', SEED + 3)
IMF = json.load(open('data/imf_events.json'))
imf_res = [s for s in IMF['statements'] if s['happened'] is not None]
imf = dict(statements=len(IMF['statements']), resolved=len(imf_res), held=len(IMF['statements']) - len(imf_res), happened=sum(1 for s in imf_res if s['happened']),
           outcome=None, reason='fewer than 20 resolved statements, so the list is a measurement with no outcome (PLAN.md section 4)' if len(imf_res) < 20 else 'the plan names no outcome rule for the IMF list',
           events=[dict(id=s['id'], issue=s['issue'], page=s['page'], years=s['years'], kind=s['kind'], thr=s.get('thr'), lo=s.get('lo'), hi=s.get('hi'), p=s['p'], p_text=s['p_text'],
                        quote=s['quote'], outturn={k: v['value'] for k, v in s['outturn'].items()}, outturn_source=' and '.join(v['source'] for v in s['outturn'].values()), happened=s['happened'], held=s['held']) for s in IMF['statements']],
           not_counted=IMF['not_counted'])
summary = dict(desk='SELDON', publisher='Heuremen LLC', generated=STAMP, updated=STAMP, plan='PLAN.md', plan_seal=SEAL, labels=LABELS,
    claim=dict(stated='CBO: "There is roughly a two-thirds chance" that the outcome falls inside each stated range, built from "historical errors in its baseline projections" (CBO 60664). Read as 0.667.',
               carriers=['CBO projects under current law, so a later change in law can move an outcome away from a projection made under the law of its day.',
                         'CBO builds its ranges from its own past errors, so a share near two-thirds is partly built in over the years those errors cover.',
                         'Few reports print ranges, which widens the interval.']),
    frame=dict(long_horizon_years=LONG_H, last_fiscal_year=LAST_FY, stated_share=STATED_SHARE, min_ranges=MIN_RANGES, hit='inside the range, endpoints included, the outcome rounded to the decimals the range prints',
               growth_first=dict((str(k), v) for k, v in FIRST.items()), growth_revised=REVISED, budget='actuals.csv over actual_GDP.csv (fiscal years), US-CBO/eval-projections',
               bootstrap=dict(resamples=NBOOT, seed=SEED, block='report')),
    gates=dict(kg, passed=GATE),
    seldon=dict(cbo_range_hit_share=head, cbo_range_hit_share_unrounded=head_strict, cbo_range_hit_share_revised=head_rev, cbo_short_horizon_hit_share=short_c, imf_probability_events=imf),
    ranges=rows, short_ranges=short, held=held, refused=refused, not_counted=[dict(file=x['file'], why=x.get('why') or x.get('reason')) for x in ST['not_counted']],
    reports_read=len(ST['reports_read']), stated_built=ST['built'], after_data_note='')
json.dump(summary, open('summary_seldon.json.tmp', 'w'), indent=1, ensure_ascii=False); os.replace('summary_seldon.json.tmp', 'summary_seldon.json')
json.dump(summary, open('data/seldon_live.json.tmp', 'w'), separators=(',', ':'), ensure_ascii=False); os.replace('data/seldon_live.json.tmp', 'data/seldon_live.json')
# the rows the reproduce kit recomputes the headline from (reproduce_kits/extracts/seldon_score.py)
json.dump(dict(generated=STAMP, gate_passed=GATE, seed=SEED, nboot=NBOOT, stated=STATED_SHARE, min_ranges=MIN_RANGES,
               ranges=[dict(id=x['id'], report_month=x['report_month'], measure=x['measure'], lo=x['lo'], hi=x['hi'], horizon=x['horizon'], outturn=x['outturn'], hit=x['hit']) for x in rows]),
          open('data/seldon_rows.json.tmp', 'w'), indent=1); os.replace('data/seldon_rows.json.tmp', 'data/seldon_rows.json')
PUB_FAILED = False
if PUB:   # the one Cloudflare part (lib/cf.py kv_put: kv token, rings on failure). A failed put exits non-zero after the history line.
    try:
        sys.path.insert(0, os.path.expanduser('~/forge/lib')); import cf
        PUB_FAILED = not cf.kv_put('seldon_live', os.path.join(H, 'data', 'seldon_live.json'), who='seldon_tick.py')
    except Exception as _e: log('publish part failed', repr(_e)[:200]); PUB_FAILED = True
    log('seldon_live', 'publish FAILED' if PUB_FAILED else 'published')
with open('data/seldon_history.jsonl', 'a') as f:
    f.write(json.dumps(dict(t=STAMP, gate=GATE, head=(head['value'], head['lo'], head['hi'], head['outcome'], head['reason'], head['hits'], head['ranges']), short=(short_c['value'], short_c['outcome']), held=len(held))) + '\n')
log('gates', kg); log('headline', head); log('unrounded', head_strict); log('revised', head_rev); log('short', short_c); log('imf', {k: imf[k] for k in ('statements', 'resolved', 'happened')})
if PUB_FAILED: sys.exit(3)
