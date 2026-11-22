#!/usr/bin/env python3
"""read_reruns.py: DEUS delivered side parser (PLAN.md sections 3 and 4). Reads the Epoch AI zip snapshot unpacked by fetch_reruns.py as text.
Never executes anything from it. Gives, per benchmark in the frame, every rerun row with: model version string, display name and lab (from
model_metadata.csv), score as a fraction, the interval the plan's interval rule gives, what the interval measures, run kind (Epoch internal
or external third party), and the eleven-plus-four setup fields as the source names them (None when the source does not name a field).

Interval rule (PLAN.md section 4), applied as fixed:
  - Epoch internal rows carry `stderr`. Epoch's FAQ (https://epoch.ai/benchmarks/about, read 2026-11-22, raw/epoch/pages/benchmarks_about.text.txt):
    "we run most models multiple times on each benchmark" and the plot shows "plus and minus one standard error around the 'true' mean".
    So the error bar is the standard error of the mean score over runs. The plan asks for the rerun's 95% interval, so the interval is
    mean +- 1.96 x stderr, labelled "Epoch standard error of the mean over runs, x1.96".
  - A row with no stderr but a known item count: Wilson 95% on round(score x items) of items, labelled "item sampling, single run".
  - Neither: no interval (CANNOT_TELL, NO_INTERVAL_FORMABLE downstream).
  - External HLE rows carry "Accuracy Standard Error": the same x1.96 rule, labelled with the source's own words.
Score column: Epoch internal files have `mean_score` (the mean over runs, which the stderr belongs to) and `Best score (across scorers)`.
The interval belongs to the mean, so the mean is the rerun value. Values above 1 in a column mark the column as percent."""
import os, csv, glob, math, json, re
H = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, H); import heuremen_kit as K

def snapshot_dir():
    ds = sorted(glob.glob(os.path.join(H, 'raw', 'epoch', '2*', 'csv')))
    if not ds: raise SystemExit('no Epoch snapshot under raw/epoch/')
    return ds[-1]

# Benchmarks in the frame (PLAN.md section 4) -> the Epoch files that hold runs of that dataset version and item set.
# AIME 2025: the zip holds no AIME 2025 file. OTIS Mock AIME 2024-2025 is a different item set, so it is not a run of AIME 2025 (dropped, named).
FILES = {
    'GPQA Diamond': [dict(file='gpqa_diamond.csv', kind='Epoch internal', version='GPQA Diamond, 198 questions', items=198, col='mean_score', se='stderr')],
    'SWE-bench Verified': [dict(file='swe_bench_verified.csv', kind='Epoch internal', version='SWE-bench Verified, Epoch 484 of 500 samples', items=484, col='mean_score', se='stderr')],
    'FrontierMath': [dict(file='frontiermath.csv', kind='Epoch internal', version='FrontierMath 2025-02-28 private (Tiers 1-3, before the v2 update)', items=None, col='mean_score', se='stderr'),
                     dict(file='frontiermath_tiers_1_3_v2.csv', kind='Epoch internal', version='FrontierMath Tiers 1-3 v2 private (2026-06-12 update)', items=None, col='mean_score', se='stderr')],
    "Humanity's Last Exam": [dict(file='hle_external.csv', kind='external', version='HLE as on the leaderboard Epoch cites', items=None, col='Accuracy', se='Accuracy Standard Error')],
    'AIME 2025': [],
}
DROPPED = {'AIME 2025': 'The Epoch zip holds no run of AIME 2025. OTIS Mock AIME 2024-2025 is a different item set (benchmark_metadata.csv lists it apart), so AIME 2025 is dropped and nothing replaces it (PLAN.md section 4).'}

SETUP_FIELDS = ['harness', 'prompt format', 'chat template', 'few-shot', 'max tokens', 'temperature', 'stop', 'extraction rule', 'dataset version', 'items', 'seeds',
                'reasoning effort', 'tools and scaffold', 'attempts', 'trials averaged']
# What each source names, quoted from its own pages (raw/epoch/pages/*.text.txt). A field the source does not name is None.
SETUP = {
    'gpqa_diamond.csv': {'harness': 'Inspect ("Our internal evaluations are powered by Inspect")', 'prompt format': 'simple-evals prompt ("We use the prompt from the simple-evals library")',
                         'extraction rule': '"If the model\'s answer is not of the form \'ANSWER: LETTER\', it receives no points"', 'dataset version': 'GPQA Diamond', 'items': '198',
                         'trials averaged': 'mean over runs ("for most models, 16 times on GPQA Diamond")', 'attempts': 'pass@1 per run, averaged'},
    'swe_bench_verified.csv': {'harness': 'Inspect', 'dataset version': 'SWE-bench Verified', 'items': '484 ("use 484 samples that are validated on our infrastructure")',
                               'tools and scaffold': 'Epoch scaffold, bash-only style ("close to that used in the SWE-bench developers\' bash-only runs")', 'attempts': 'pass@1'},
    'frontiermath.csv': {'harness': 'Inspect', 'tools and scaffold': 'Python execution ("Our implementation allows the model to reason and run Python code")', 'dataset version': 'FrontierMath 2025-02-28 private'},
    'frontiermath_tiers_1_3_v2.csv': {'harness': 'Inspect', 'tools and scaffold': 'Python execution', 'dataset version': 'FrontierMath Tiers 1-3 v2 private', 'items': '285 private of the 295-problem base set (ten made public)'},
    'hle_external.csv': {'dataset version': "Humanity's Last Exam (leaderboard)"},
}

def fnum(x):
    try:
        v = float(str(x).strip().rstrip('%'))
        return None if math.isnan(v) else v
    except Exception: return None

def meta(d):
    m = {}
    for r in csv.DictReader(open(os.path.join(d, 'model_metadata.csv'), encoding='utf-8')): m[r['model_version']] = r
    return m

def rows(benchmark):
    d = snapshot_dir(); M = meta(d); out = []
    for spec in FILES[benchmark]:
        p = os.path.join(d, spec['file'])
        if not os.path.exists(p): continue
        R = list(csv.DictReader(open(p, encoding='utf-8')))
        vals = [fnum(r.get(spec['col'])) for r in R]; pct = any(v is not None and v > 1.0 for v in vals)
        ses = [fnum(r.get(spec['se'])) for r in R]   # the error column is in the units of its score column
        for r, v, s in zip(R, vals, ses):
            if v is None: continue
            v = v / 100 if pct else v
            if s is not None and pct: s = s / 100
            mv = r.get('Model version') or ''; md = M.get(mv, {})
            if s is not None and s >= 0:
                lo, hi, what = max(0.0, v - 1.96 * s), min(1.0, v + 1.96 * s), ('Epoch standard error of the mean over runs, x1.96' if spec['kind'] == 'Epoch internal' else 'source standard error ("Accuracy Standard Error"), x1.96')
            elif spec['items']:
                k = round(v * spec['items']); lo, hi = K.wilson(k, spec['items']); what = 'item sampling, single run (Wilson 95%% on %d items)' % spec['items']
            else: lo = hi = None; what = 'no interval: no error bar and no item count'
            setup = {f: SETUP.get(spec['file'], {}).get(f) for f in SETUP_FIELDS}
            out.append(dict(benchmark=benchmark, file=spec['file'], kind=spec['kind'], version=spec['version'], model_version=mv,
                            name=r.get('Name') or md.get('display_name') or mv, group=md.get('model_group'), lab=md.get('organization') or r.get('Organization'),
                            value=v, se=s, lo=lo, hi=hi, interval_what=what, notes=(r.get('Notes') or '')[:300], row_id=r.get('id'), setup=setup,
                            source=r.get('Source'), source_link=r.get('Source link'), started=r.get('Started at')))
    return out

def all_rows():
    return {b: rows(b) for b in FILES}

if __name__ == '__main__':
    # Structure only: counts of rows per benchmark. Prints no score (L2: no rate before the parser is read).
    for b, rs in all_rows().items(): print(b, len(rs), 'rows', sorted({r['kind'] for r in rs}), DROPPED.get(b, ''))
