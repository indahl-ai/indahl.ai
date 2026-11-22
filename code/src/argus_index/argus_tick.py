#!/usr/bin/env python3
"""argus_tick.py: ARGUS rider (see PLAN.md and mapping.json). Rerunnable. Installs no timer. Reads public sources with no key, one request at a time, paced:
the Zenodo record 6522639 of the Darwin's Ark release (Morrill et al., Science 2022, CC0), its README and DarwinsArk.zip, and the American Kennel Club
standard PDFs named in mapping.json. Sets each mapped breed standard phrase beside the breed's average on the mapped behavior factor.
Writes summary_argus.json, data/argus_live.json and data/argus_history.jsonl.
--offline: cached files only. --publish: also put data/argus_live.json in the site KV as argus_live, served at /argus/live.json.
--selftest: rule checks only, no network, no data."""
import sys as _cfsys, os as _cfos
try:   # 22 Nov 2026: one shared Cloudflare part (lib/cf.py: kv token, rings on failure)
    _cfsys.path.insert(0, _cfos.path.expanduser('~/forge/lib')); from cf import run_put as _cf_run
except Exception:
    import subprocess as _cfsp; _cf_run = _cfsp.run
import os, sys, json, time, csv, io, re, hashlib, zipfile, subprocess, contextlib, urllib.request, collections as C
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import numpy as np
import heuremen_kit as K
OFF = '--offline' in sys.argv; PUB = '--publish' in sys.argv
UA = 'heuremen-argus/0.1 (+https://indahl.ai/argus)'
REC = 'https://zenodo.org/api/records/6522639'
FILE = 'https://zenodo.org/api/records/6522639/files/%s/content'
THRESH = 0.85; MIN_DOGS = 25; NBOOT = 2000; SEED = 20261122; PACE = 2.0
NEED = ['DarwinsArk_20191115_breedcalls.csv', 'DarwinsArk_20191115_dogs.csv', 'DarwinsArk_20191115_factors.csv', 'DarwinsArk_20191115_questions.csv',
        'DarwinsArk_20191115_factor_scores.csv', 'DarwinsArk_20191115_answers.csv']
RAW = 'data/raw'; ZR = RAW + '/zenodo'; DA = RAW + '/darwinsark'; ST = RAW + '/standards'
for d in ('data', RAW, ZR, DA, ST): os.makedirs(d, exist_ok=True)
NOW = time.time()
def log(*a): print('argus:', *a, file=sys.stderr, flush=True)
_last = [0.0]; STALE = []
def get(url, tries=3, timeout=900):
    err = None
    for a in range(tries):
        w = PACE - (time.time() - _last[0])
        if w > 0: time.sleep(w)
        try:
            with K.opener().open(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout) as r: b = r.read()
            _last[0] = time.time(); return b
        except Exception as e:
            _last[0] = time.time(); err = e
            if getattr(e, 'code', 0) in (400, 403, 404, 410): break
            time.sleep(5 * (a + 1) ** 2)
    raise RuntimeError('fetch failed %s: %r' % (url[:140], err))
def fetch_to(path, url, max_age_h=None, must=None):
    fresh = os.path.exists(path) and (max_age_h is None or (NOW - os.path.getmtime(path)) / 3600 < max_age_h)
    if fresh or OFF: return os.path.exists(path)
    try:
        b = get(url)
        if must and not must(b): raise RuntimeError('unexpected content')
        open(path + '.part', 'wb').write(b); os.replace(path + '.part', path); return True
    except Exception as e:
        log('fetch FAILED', url[:120], repr(e)[:120]); STALE.append(os.path.basename(path)); return os.path.exists(path)

# ---------------- the rule (PLAN.md section 5) ----------------
def outcome(lo, hi, direction):
    """lo, hi: 95 percent interval on breed mean minus all-dog mean. direction: 'high' or 'low' as the standard states.
    CONSISTENT: whole interval on the stated side. ABOVE: stated low, whole interval above zero. BELOW: stated high, whole interval below zero.
    CANNOT_TELL otherwise (the interval holds zero: STRADDLES_EDGE, no interval: NO_INTERVAL_FORMABLE). Zero itself is not on either side."""
    o, why = K.read(lo, hi, bound=0.0, edge='closed')
    if o == K.CANNOT_TELL: return o, why
    if direction == 'high': return (K.CONSISTENT, None) if o == K.ABOVE else (K.BELOW, None)
    if direction == 'low': return (K.CONSISTENT, None) if o == K.BELOW else (K.ABOVE, None)
    raise ValueError('direction is high or low')
def boot_diff(s, m, seed, n=NBOOT):
    """s: scores of every dog with this factor. m: membership mask of the breed. Bootstrap over all dogs jointly: each draw resamples the whole release
    with replacement and takes the breed mean minus the mean of all other dogs in the draw (PLAN_ADDENDUM_referee1.md item 7). Returns (value, lo, hi)."""
    s = np.asarray(s, float); m = np.asarray(m, bool); N = len(s)
    if m.sum() < 2 or (~m).sum() < 2: return (float(s[m].mean() - s[~m].mean()) if m.sum() and (~m).sum() else None), None, None
    rng = np.random.default_rng(seed); out = []
    for _ in range(n):
        i = rng.integers(0, N, N); mm = m[i]
        if mm.sum() == 0 or mm.all(): continue
        si = s[i]; out.append(si[mm].mean() - si[~mm].mean())
    v = float(s[m].mean() - s[~m].mean())
    if len(out) < n // 2: return v, None, None
    return v, float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))
def rule_selftest():
    t = []
    t.append(outcome(0.1, 0.3, 'high') == (K.CONSISTENT, None)); t.append(outcome(-0.3, -0.1, 'high') == (K.BELOW, None))
    t.append(outcome(-0.3, -0.1, 'low') == (K.CONSISTENT, None)); t.append(outcome(0.1, 0.3, 'low') == (K.ABOVE, None))
    t.append(outcome(-0.1, 0.2, 'high') == (K.CANNOT_TELL, K.STRADDLES_EDGE)); t.append(outcome(0.0, 0.2, 'high') == (K.CANNOT_TELL, K.STRADDLES_EDGE))
    t.append(outcome(None, None, 'low') == (K.CANNOT_TELL, K.NO_INTERVAL_FORMABLE))
    rng = np.random.default_rng(1); s = rng.normal(0, 1, 3000); m = np.zeros(3000, bool); m[:60] = True; s[:60] += 1.0
    v, lo, hi = boot_diff(s, m, 3, 400); t.append(lo is not None and 0 < lo < v < hi)
    t.append(boot_diff(s, m, 3, 400) == boot_diff(s, m, 3, 400))
    m2 = np.zeros(3000, bool); m2[5] = True; t.append(boot_diff(s, m2, 3, 100)[1] is None)
    return all(t), t
if '--selftest' in sys.argv:
    ok, t = rule_selftest(); print('rule selftest', 'PASSED' if ok else 'FAILED', t)
    with contextlib.redirect_stdout(io.StringIO()): kok = K.selftest()
    sys.exit(0 if ok and kok else 1)

MAP = json.load(open('mapping.json'))
CLAIMS = json.load(open('dna_claims.json'))

# ---------------- 1. fetch ----------------
fetch_to(ZR + '/record_6522639.json', REC, max_age_h=24 * 7, must=lambda b: b[:1] == b'{')
rec = json.load(open(ZR + '/record_6522639.json'))
md5 = {f['key']: f['checksum'].split(':', 1)[1] for f in rec['files']}
fetch_to(ZR + '/README.md', FILE % 'README.md')
fetch_to(ZR + '/DarwinsArk.zip', FILE % 'DarwinsArk.zip', must=lambda b: b[:2] == b'PK')
def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for ch in iter(lambda: f.read(1 << 20), b''): h.update(ch)
    return h.hexdigest()
zip_ok = os.path.exists(ZR + '/DarwinsArk.zip') and md5f(ZR + '/DarwinsArk.zip') == md5.get('DarwinsArk.zip')
readme_ok = os.path.exists(ZR + '/README.md') and md5f(ZR + '/README.md') == md5.get('README.md')
if zip_ok:
    with zipfile.ZipFile(ZR + '/DarwinsArk.zip') as z:
        for n in NEED:
            if not os.path.exists(DA + '/' + n):
                with z.open('DarwinsArk/' + n) as src, open(DA + '/' + n + '.part', 'wb') as dst: dst.write(src.read())
                os.replace(DA + '/' + n + '.part', DA + '/' + n)
std_ok = {}
for b, sd in MAP['breeds'].items():
    f = ST + '/' + sd['url'].rsplit('/', 1)[1]
    fetch_to(f, sd['url'], must=lambda x: x[:4] == b'%PDF')
    try:
        import pypdf
        t = re.sub(r'\s+', ' ', ' '.join(p.extract_text() for p in pypdf.PdfReader(f).pages))
        std_ok[b] = re.sub(r'Page \d+ of \d+ ', '', sd['temperament']) in re.sub(r'Page \d+ of \d+ ', '', t)
    except Exception as e: log('standard unreadable', b, repr(e)[:80]); std_ok[b] = False

# ---------------- 2. breed list from the ancestry column alone ----------------
best = {}
for r in csv.DictReader(open(DA + '/DarwinsArk_20191115_breedcalls.csv')):
    p = float(r['pct'])
    if r['dog'] not in best or p > best[r['dog']][1]: best[r['dog']] = (r['breed'], p)
GEN = C.defaultdict(set)
for d, (b, p) in best.items():
    if p >= THRESH: GEN[b].add(d)
DOGS = {r['id']: r for r in csv.DictReader(open(DA + '/DarwinsArk_20191115_dogs.csv'))}
OWN = C.defaultdict(set)
for d, r in DOGS.items():
    if r['owner_breed']: OWN[r['owner_breed']].add(d)
listed = sorted([b for b, s in GEN.items() if len(s) >= MIN_DOGS], key=lambda b: -len(GEN[b]))
held = sorted([(b, len(s)) for b, s in GEN.items() if len(s) < MIN_DOGS], key=lambda x: (-x[1], x[0]))
refused = {b: MAP['refused'][b] for b in listed if b in MAP['refused']}
read_breeds = [b for b in listed if b in MAP['breeds']]
unlisted = [b for b in listed if b not in MAP['breeds'] and b not in MAP['refused']]   # a listed breed the table has no row for: refused, named

# ---------------- 3a. precondition: the mapping table read by the referee before the first run (PLAN.md section 4) ----------------
SR = json.load(open('data/referee_mapping_read.json')) if os.path.exists('data/referee_mapping_read.json') else None
map_sha = hashlib.sha256(open('mapping.json', 'rb').read()).hexdigest()
if not SR or SR.get('mapping_sha256') != map_sha or SR.get('verdict') != 'STANDS':
    log('REFUSED: the mapping table has no recorded read by the referee for sha256', map_sha[:12], '(data/referee_mapping_read.json). No reading formed.'); sys.exit(4)
def _sealed():   # a reproduce kit has no git: offline, the files must match the sha256 values the plan seal recorded at commit time
    try:
        P = json.load(open('data/plan_seal.json')); h = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()
        return OFF and P['plan_sha256'] == h('PLAN.md') and P['mapping_sha256'] == h('mapping.json') == map_sha
    except Exception: return False
if not ((K.plan_committed('PLAN.md') and K.plan_committed('mapping.json')) or _sealed()):
    log('REFUSED: PLAN.md or mapping.json is not committed unchanged'); sys.exit(4)

# ---------------- 3. known-good gates (before any reading) ----------------
kg = {}
fac_rows = list(csv.DictReader(open(DA + '/DarwinsArk_20191115_factors.csv')))
qrows = {r['id']: r for r in csv.DictReader(open(DA + '/DarwinsArk_20191115_questions.csv'))}
SC = C.defaultdict(dict)
with open(DA + '/DarwinsArk_20191115_factor_scores.csv', newline='') as fh:
    rd = csv.DictReader(fh); sc_fields = rd.fieldnames or []
    for r in rd:
        try: SC[r['factor']][r['dog']] = float(r[MAP['score_column']])
        except Exception: pass
FIDS = sorted(SC, key=int)
kg['format'] = zip_ok and readme_ok and all(os.path.exists(DA + '/' + n) for n in NEED) and FIDS == [str(i) for i in range(1, 9)] and MAP['score_column'] in sc_fields
# gate 2: our 85 percent membership against the release's own regseq_breed (reg_breed or at least 85 percent of one breed)
mem_ok = sum(1 for b, s in GEN.items() for d in s if DOGS.get(d, {}).get('regseq_breed') == b); mem_n = sum(len(s) for s in GEN.values())
kg['membership'] = mem_n > 0 and mem_ok == mem_n
# gate 3: score direction. For each scored factor, the correlation of the score with its top-loading item, coded agree 0 to disagree 4 in the order the
# questions file lists, has the sign of the pattern loading. This checks that high on the score is the released positive label.
top = {}
for r in fac_rows:
    try: pl = float(r['pattern'])
    except ValueError: continue
    if r['factor'] in SC and (r['factor'] not in top or abs(pl) > abs(top[r['factor']][1])): top[r['factor']] = (r['question'], pl)
want_q = {q for q, _ in top.values()}; ANS = C.defaultdict(dict)
with open(DA + '/DarwinsArk_20191115_answers.csv', newline='') as fh:
    for r in csv.DictReader(fh):
        if r['question'] in want_q:
            opts = qrows[r['question']]['options'].split('|')
            if r['option'] in opts: ANS[r['question']][r['dog']] = opts.index(r['option'])
dir_rows = []
for f, (q, pl) in sorted(top.items(), key=lambda x: int(x[0])):
    ds = [d for d in SC[f] if d in ANS[q]]; a = np.array([SC[f][d] for d in ds]); b = np.array([ANS[q][d] for d in ds], float)
    r_ = float(np.corrcoef(a, b)[0, 1]) if len(ds) > 2 else None
    dir_rows.append(dict(factor=f, question=q, text=qrows[q]['string'], pattern=pl, n=len(ds), r=None if r_ is None else round(r_, 4), agrees=r_ is not None and np.sign(r_) == np.sign(pl) and abs(r_) >= 0.3))
kg['direction'] = len(dir_rows) == 8 and all(x['agrees'] for x in dir_rows)
kg['standards_text'] = all(std_ok.get(b) for b in read_breeds)
with contextlib.redirect_stdout(io.StringIO()): _kok = K.selftest()
kg['rule'] = rule_selftest()[0] and _kok
GATE = all(kg.values())

# ---------------- 5. readings ----------------
def read_phrase(breed, ph, members, seed):
    f = ph['factor']; ds = list(SC[f]); s = np.array([SC[f][d] for d in ds]); m = np.array([d in members for d in ds])
    v, lo, hi = boot_diff(s, m, seed); o, why = outcome(lo, hi, ph['direction'])
    om = float(s[~m].mean()); n = int(m.sum()); side = (s[m] > om) if ph['direction'] == 'high' else (s[m] < om); k = int(side.sum())
    wl, wh = K.wilson(k, n) if n else (None, None)
    return dict(n=n, all_dogs=len(ds), breed_mean=None if not n else round(float(s[m].mean()), 4), others_mean=round(om, 4), others_n=int((~m).sum()), diff=None if v is None else round(v, 4),
                lo=None if lo is None else round(lo, 4), hi=None if hi is None else round(hi, 4), outcome=o, reason=why,
                stated_side_k=k, stated_side_share=None if not n else round(k / n, 4), share_lo=None if wl is None else round(wl, 4), share_hi=None if wh is None else round(wh, 4))
rows = []; unmappable = []; no_trait = []; si = 0
for b in read_breeds:
    sd = MAP['breeds'][b]
    for ph in sd['phrases']:
        if ph.get('no_trait'): no_trait.append(dict(breed=b, id=ph['id'], phrase=ph['phrase'])); continue
        if not ph['factor']: unmappable.append(dict(breed=b, id=ph['id'], phrase=ph['phrase'], why=ph['why'])); continue
        si += 1; g = read_phrase(b, ph, GEN[b], SEED + si); ow = read_phrase(b, ph, OWN.get(b, set()), SEED + 100 + si)
        fn = MAP['factors'][ph['factor']]
        rows.append(dict(breed=b, id=ph['id'], phrase=ph['phrase'], factor=ph['factor'], factor_name=fn['name'], direction=ph['direction'],
                         stated_side=fn[ph['direction']], deciding_items=ph.get('deciding_items') or fn['top_items'], genetic=g, owner_reported=dict(ow, display_only=True)))
if not GATE:
    for r in rows: r['genetic']['outcome_before_gate'] = r['genetic']['outcome']; r['genetic']['outcome'] = K.CANNOT_TELL; r['genetic']['reason'] = K.NO_INTERVAL_FORMABLE
# PLAN_ADDENDUM_referee1.md item 6: the headline counts each distinct breed, factor and direction once. A restated phrase reads the same dogs and factor, so its
# reading is identical. The phrase rows print beside it.
distinct = []
for r in rows:
    t = (r['breed'], r['factor'], r['direction'])
    if t not in [x['key'] for x in distinct]: distinct.append(dict(key=t, breed=r['breed'], factor=r['factor'], factor_name=r['factor_name'], direction=r['direction'], stated_side=r['stated_side'], phrases=[], genetic=r['genetic'], owner_reported=r['owner_reported'], deciding_items=r['deciding_items']))
    next(x for x in distinct if x['key'] == t)['phrases'].append(r['id'])
for x in distinct: x.pop('key')
dcnt = C.Counter(x['genetic']['outcome'] for x in distinct)
direction_outcomes = {k: dcnt.get(k, 0) for k in K.OUTCOMES}
cnt = C.Counter(r['genetic']['outcome'] for r in rows)
NR = [u['id'] for u in unmappable]
REQ13 = K.req13([(x['genetic']['outcome'], x['genetic']['reason']) for x in distinct], nothing_returned=NR)
own_cnt = C.Counter(x['owner_reported']['outcome'] for x in distinct)
dna_no_test = [c for c in CLAIMS['claims'] if c.get('figure') and not c.get('independent_test_with_released_data')]

# ---------------- 6. seal and output ----------------
def git(*a): return subprocess.run(['git'] + list(a), cwd=H, capture_output=True, text=True).stdout.strip()
seal_f = 'data/plan_seal.json'
if not os.path.exists(seal_f):
    json.dump(dict(plan_commit=git('log', '-1', '--format=%H', '--', 'PLAN.md'), plan_commit_time=git('log', '-1', '--format=%cI', '--', 'PLAN.md'), plan_sha256=hashlib.sha256(open('PLAN.md', 'rb').read()).hexdigest(),
                   plan_source='indahl-ai/calibrations lane-research c680778 argus_index/PLAN.md', mapping_commit=git('log', '-1', '--format=%H', '--', 'mapping.json'),
                   mapping_commit_time=git('log', '-1', '--format=%cI', '--', 'mapping.json'), mapping_sha256=map_sha, referee_read=SR,
                   first_comparison=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(NOW))), open(seal_f, 'w'), indent=1)
seal = json.load(open(seal_f))
gen = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(NOW))
summary = dict(
    desk='ARGUS', publisher='Heuremen LLC', generated=gen, label='PRELIMINARY: first run, not refereed', behavior_label='owner-reported behavior',
    plan='PLAN.md', plan_seal=seal, plan_unchanged_since_commit=K.plan_committed('PLAN.md'), mapping_unchanged_since_commit=K.plan_committed('mapping.json'),
    claim='Breed standard Temperament sections, American Kennel Club, read as written, each phrase mapped in advance to one Darwin’s Ark behavior factor and a direction',
    source=dict(release='Morrill et al., Ancestry-inclusive dog genomics challenges popular breed stereotypes, Science 376:eabk0639 (2022), DOI 10.1126/science.abk0639',
                data='Zenodo record 6522639 (DarwinsArk.zip, freeze 15 November 2019), DOI 10.5281/zenodo.6522639, license %s' % rec['metadata'].get('license', {}).get('id'),
                zip_md5=md5.get('DarwinsArk.zip'), zip_md5_matches=zip_ok, factors_scored=len(FIDS), score_column=MAP['score_column']),
    frame=dict(threshold=THRESH, min_dogs=MIN_DOGS, comparison='mean factor score of all other dogs in the release (PLAN_ADDENDUM_referee1.md item 7)', bootstrap=dict(draws=NBOOT, seed=SEED, unit='dog, whole release resampled jointly'),
               share_interval='Wilson 95 percent', dogs_with_ancestry=len(best), dogs_at_threshold=mem_n, factor_dogs={f: len(SC[f]) for f in FIDS}),
    breeds=dict(listed=[dict(breed=b, dogs=len(GEN[b])) for b in listed], read=read_breeds, refused=refused, unlisted_refused=unlisted, held=[dict(breed=b, dogs=n) for b, n in held]),
    gates=dict(kg, passed=GATE, membership_agree=mem_ok, membership_of=mem_n, direction=dir_rows),
    argus=dict(direction_outcomes=direction_outcomes, triples=len(distinct), phrase_rows=len(rows), phrase_row_outcomes={k: cnt.get(k, 0) for k in K.OUTCOMES},
               individual_stated_side_share=[dict(breed=x['breed'], phrases=x['phrases'], factor_name=x['factor_name'], stated_side=x['stated_side'],
                                                  share=x['genetic']['stated_side_share'], lo=x['genetic']['share_lo'], hi=x['genetic']['share_hi'], k=x['genetic']['stated_side_k'], n=x['genetic']['n']) for x in distinct],
               no_trait_left_out=len(no_trait),
               unmappable_count=len(unmappable), dna_test_no_test_count=len(dna_no_test),
               nothing_returned=len(unmappable), refused=len(refused) + len(unlisted), held=len(held), owner_reported_outcomes={k: own_cnt.get(k, 0) for k in K.OUTCOMES}),
    triples=distinct, rows=rows, unmappable=unmappable, no_trait=no_trait, addendum='PLAN_ADDENDUM_referee1.md', dna_claims=CLAIMS, req13=REQ13,
    carriers=['Behavior is owner-reported, not observed.', 'Dogs in the release are those whose owners joined, which is not a sample of all dogs.',
              'A standard describes the breed as its club wants it, which may be read as an ideal rather than a claim about every dog. The run still reads the words as written.'],
    sources_stale=STALE)
json.dump(summary, open('summary_argus.json.tmp', 'w'), indent=1); os.replace('summary_argus.json.tmp', 'summary_argus.json')
live = dict(summary, updated=gen)
json.dump(live, open('data/argus_live.json.tmp', 'w'), separators=(',', ':')); os.replace('data/argus_live.json.tmp', 'data/argus_live.json')
if PUB:
    env = dict(os.environ, CLOUDFLARE_ACCOUNT_ID='<cloudflare-account-id>', PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
    p = _cf_run(['/opt/homebrew/bin/npx', 'wrangler', 'kv', 'key', 'put', 'argus_live', '--path', os.path.join(H, 'data', 'argus_live.json'), '--namespace-id', '<kv-namespace-id>', '--remote'],
                       cwd=os.path.expanduser('~/forge/cloudflare-workers/heuremen-door'), env=env, capture_output=True, text=True)
    log('argus_live', 'published' if p.returncode == 0 else 'publish FAILED ' + (p.stderr or '')[-200:])
    if p.returncode: STALE.append('publish')
with open('data/argus_history.jsonl', 'a') as f:
    f.write(json.dumps(dict(t=gen, gate=GATE, direction_outcomes=direction_outcomes, unmappable=len(unmappable), dna_no_test=len(dna_no_test), stale=STALE)) + '\n')
log('gates', kg, 'membership %d of %d' % (mem_ok, mem_n))
for x in dir_rows: log('  direction F%s q%s r=%s pattern=%+.2f n=%d %s' % (x['factor'], x['question'], x['r'], x['pattern'], x['n'], 'ok' if x['agrees'] else 'NO'))
log('listed', [(b, len(GEN[b])) for b in listed], 'refused', list(refused), 'held', len(held))
for r in rows:
    g = r['genetic']; o = r['owner_reported']
    log('%-18s %-5s F%s %-4s n=%3d diff %s [%s, %s] %-11s share %s [%s, %s] | owner n=%d diff %s [%s, %s] %s' % (r['breed'], r['id'], r['factor'], r['direction'], g['n'], g['diff'], g['lo'], g['hi'], g['outcome'], g['stated_side_share'], g['share_lo'], g['share_hi'], o['n'], o['diff'], o['lo'], o['hi'], o['outcome']))
log('argus.direction_outcomes (distinct triples)', direction_outcomes, 'phrase rows', dict(cnt), 'unmappable', len(unmappable), 'dna no test', len(dna_no_test), REQ13['line'])
