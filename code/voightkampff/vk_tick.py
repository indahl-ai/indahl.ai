#!/usr/bin/env python3
"""vk_tick.py: VOIGHT-KAMPFF run. AI-text detector makers' stated false positive rates against independent tests that release per-item output.
Plan: PLAN.md (indahl-ai/calibrations lane-research c9e4f8a), sealed in data/plan_seal.json, open questions answered in data/plan_answers.json
before any file was fetched. Offline: reads only what vk_fetch.py saved under data/raw (untrusted, read as data, never executed).

Writes summary_voightkampff.json, data/voightkampff_live.json (the feed, served at /voightkampff/live.json) and one line of data/voightkampff_history.jsonl.
  python3 -I vk_tick.py             score from the saved files
  python3 -I vk_tick.py --publish   also put the feed in the site KV as voightkampff_live
  python3 -I vk_tick.py --selftest  planted cases for the outcome rule
Outcome rule (PLAN.md sections 4 and 5), delivered relative to stated, on a Wilson 95 percent interval over human texts:
  ceiling c: ABOVE if lo > c, CONSISTENT if hi <= c, else CANNOT_TELL (STRADDLES_EDGE). BELOW is not reachable.
  point p:   ABOVE if lo > p, BELOW if hi < p, CONSISTENT if lo <= p <= hi.
  A stated figure is read only when it was in force at the test's query date (DATE_UNMATCHED otherwise), only at the maker's own operating point
  (NO_OPERATING_POINT otherwise), and a reading outside the figure with versions unmatched or unnamed reads CANNOT_TELL (VERSION_UNMATCHED) with the
  direction beside it. Nothing returned, refused and held are counted apart. Standard library only."""
import sys as _cfsys, os as _cfos
try:   # 22 Nov 2026: one shared Cloudflare part (lib/cf.py: kv token, rings on failure)
    _cfsys.path.insert(0, _cfos.path.expanduser('~/forge/lib')); from cf import run_put as _cf_run
except Exception:
    import subprocess as _cfsp; _cf_run = _cfsp.run
import os, sys, json, time, hashlib, re, subprocess, statistics
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import heuremen_kit as K
RAW = os.path.join('data', 'raw'); PUB = '--publish' in sys.argv
ABOVE, BELOW, CONSISTENT, CANNOT_TELL, NOTHING_RETURNED = K.ABOVE, K.BELOW, K.CONSISTENT, K.CANNOT_TELL, K.NOTHING_RETURNED
LABEL = 'PRELIMINARY: first run, not refereed'


def outcome(lo, hi, form, fig):
    """PLAN.md section 5 on one interval. form 'ceiling' or 'point'. Returns (outcome, reason)."""
    if lo is None or hi is None: return CANNOT_TELL, 'NO_INTERVAL_FORMABLE'
    if form == 'ceiling':
        if lo > fig: return ABOVE, None
        if hi <= fig: return CONSISTENT, None
        return CANNOT_TELL, 'STRADDLES_EDGE'
    if lo > fig: return ABOVE, None
    if hi < fig: return BELOW, None
    return CONSISTENT, None


def selftest():
    ok = True
    def ck(name, got, want):
        nonlocal ok; ok &= got == want; print(('OK   ' if got == want else 'FAIL ') + name, got)
    ck('ceiling, interval wholly over', outcome(0.02, 0.04, 'ceiling', 0.01), (ABOVE, None))
    ck('ceiling, interval at or under', outcome(0.0, 0.01, 'ceiling', 0.01), (CONSISTENT, None))
    ck('ceiling, interval straddles', outcome(0.005, 0.02, 'ceiling', 0.01), (CANNOT_TELL, 'STRADDLES_EDGE'))
    ck('ceiling, BELOW not reachable', outcome(0.0, 0.001, 'ceiling', 0.01)[0] != BELOW, True)
    ck('point, interval over', outcome(0.02, 0.03, 'point', 0.015), (ABOVE, None))
    ck('point, interval under', outcome(0.001, 0.005, 'point', 0.015), (BELOW, None))
    ck('point, interval holds the point', outcome(0.0, 0.0019, 'point', 0.0019), (CONSISTENT, None))
    ck('no interval', outcome(None, None, 'point', 0.01), (CANNOT_TELL, 'NO_INTERVAL_FORMABLE'))
    lo, hi = K.wilson(0, 1992); ck('Wilson 0 of 1992 starts at 0', lo, 0.0)
    ck('Wilson 0 of 1992 upper end near 0.19 percent', round(hi, 5), 0.00192)
    print('SELFTEST', 'PASSED' if ok else 'FAILED'); return ok


def sealed():
    s = json.load(open('data/plan_seal.json'))
    return s, hashlib.sha256(open('PLAN.md', 'rb').read()).hexdigest() == s['plan_sha256']


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
def words_day(v):
    v = (v or '').replace('-', '')
    return '%d %s %s' % (int(v[6:8]), MONTHS[int(v[4:6]) - 1], v[:4]) if len(v) >= 8 else 'not named'
def words(t): return len((t or '').split())
def meta(p):
    try: return json.load(open(p + '.meta.json'))
    except Exception: return {}


# ---------------------------------------------------------------------------------------------------------------- stated side
# Each figure is quoted word for word from the maker's page as this run saved it (data/raw/stated/<maker>/live.html.text.txt). A quote that is
# not found in the saved text fails the stated gate, and every reading turns CANNOT_TELL.
STATED = {
 'gptzero': dict(name='GPTZero', fpr=dict(form='ceiling', value=0.01, quote='We keep GPTZero’s false positive rate at no more than 1% when evaluating AI versus human text.', version=None),
                 accuracy=dict(value=0.965, quote='with a 96.5% accuracy rate', mix='mixed documents where both AI and human writing is involved'),
                 operating_point=None, operating_quote='These categories are tuned so that the average error rate is less than 1% for the “high” confidence predictions'),
 'originality': dict(name='Originality.ai', fpr=dict(form='point', value=0.015, quote='Even lower false positive rate of 1.5%.', version='3.0.2 Turbo, September 2025'),
                     fpr_other=[dict(form='ceiling', value=0.03, quote='(under 3% false positive rate)', version='3.0.1 Turbo, October 2024')],
                     accuracy=dict(value=0.99, quote='Originality.ai 5.0 and 5.0 Max have 99%+ accuracy', mix='not stated on the page'),
                     operating_point='the classification the API returns', operating_quote=None),
 'pangram': dict(name='Pangram', fpr=dict(form='point', value=0.0019, quote='Our model demonstrates 99.85% accuracy with 0.19% false positive rate', version='the model of the February 2024 technical report'),
                 accuracy=dict(value=0.9985, quote='Our model demonstrates 99.85% accuracy', mix='thousands of examples across ten different categories of writing and eight commonly used large language models'),
                 operating_point='the prediction label the API returns', operating_quote=None),
 'winston': dict(name='Winston AI', fpr=None, accuracy=dict(value=0.9987, quote='99.87% Accurate', mix='not stated on the page'), operating_point=None, operating_quote=None,
                 fpr_note='The page states no numeric false positive rate, only “Tuned to eliminate false positives.”'),
 'turnitin': dict(name='Turnitin', fpr=None, accuracy=None, operating_point=None, operating_quote=None),
 'copyleaks': dict(name='Copyleaks', fpr=None, accuracy=None, operating_point=None, operating_quote=None),
}


def read_stated(S):
    out = {}; gate_ok = True
    for mk in S['makers']:
        d = os.path.join(RAW, 'stated', mk['id']); m = meta(os.path.join(d, 'live.html')); st = STATED[mk['id']]
        rec = dict(id=mk['id'], name=mk['name'], url=mk['url'], read=m.get('fetched_utc'), http=m.get('status'))
        if m.get('status') != 200:
            rec['status'] = 'REFUSED' if m.get('status') in ('ROBOTS_DISALLOWED', 401, 403, 429) else NOTHING_RETURNED
            rec['why'] = {'ROBOTS_DISALLOWED': 'the site’s robots.txt does not allow this reader, or could not be read past a browser check'}.get(m.get('status'), str(m.get('error') or m.get('status')))
            out[mk['id']] = rec; continue
        text = re.sub(r'\s+', ' ', open(os.path.join(d, 'live.html.text.txt'), encoding='utf-8').read())
        rec['status'] = 'READ'; rec['sha256'] = m.get('sha256')
        for key in ('fpr', 'accuracy'):
            f = st.get(key)
            if f:
                found = f['quote'] in text; gate_ok &= found
                rec[key] = dict(f, found=found)
        rec['fpr_other'] = [dict(x, found=x['quote'] in text) for x in st.get('fpr_other', [])]
        for x in rec['fpr_other']: gate_ok &= x['found']
        if st.get('operating_quote'): rec['operating_quote'] = st['operating_quote']; rec['operating_found'] = st['operating_quote'] in text; gate_ok &= rec['operating_found']
        rec['operating_point'] = st['operating_point']; rec['fpr_note'] = st.get('fpr_note')
        cdx = os.path.join(d, 'cdx.json')
        try: rows = json.load(open(cdx))[1:]; rec['captures'] = len(rows); rec['first_capture'] = rows[0][0] if rows else None
        except Exception: rec['captures'] = None; rec['first_capture'] = None
        out[mk['id']] = rec
    return out, gate_ok


def capture_for(maker, qdate):
    """The latest Internet Archive capture of the maker's page on or before qdate (data/plan_answers.json answer 1), or None."""
    if not qdate: return None
    try: rows = json.load(open(os.path.join(RAW, 'stated', maker, 'cdx.json')))[1:]
    except Exception: return None
    prior = [r for r in rows if r[0] <= qdate.replace('-', '') + '235959']
    return prior[-1][0] if prior else None


# ---------------------------------------------------------------------------------------------------------------- delivered side
def liang():
    """Liang et al. 2023: per-detector result files. Human text = the folders the repository labels Human-Written whose texts no model edited
    (name.json kind Human-Written, folder name *_real_*)."""
    base = os.path.join(RAW, 'tests', 'liang2023', 'Data_and_Results', 'Human_Data'); sets = []; per = {'gptzero': [], 'originality': []}
    WRITERS = {'TOEFL_real_91': 'TOEFL essays by non-native English writers', 'CollegeEssay_real_70': 'US college admission essays',
               'CS224N_real_145': 'Stanford CS224N course project abstracts', 'HewlettStudentEssay_real_88': 'US 7th to 10th grade student essays (Hewlett)'}
    for fo in sorted(os.listdir(base)):
        nm = json.load(open(os.path.join(base, fo, 'name.json')))
        if nm.get('kind') != 'Human-Written' or '_real_' not in fo: continue
        data = json.load(open(os.path.join(base, fo, 'data.json')))
        sets.append(dict(subset=fo, name=nm.get('name'), writers=WRITERS.get(fo, 'not stated'), texts=len(data), mean_words=round(statistics.mean(words(x['document']) for x in data), 1)))
        for det, f in (('gptzero', 'GPTZero.json'), ('originality', 'OriginalityAI.json')):
            r = json.load(open(os.path.join(base, fo, f)))
            per[det].append(dict(subset=fo, n=len(r), scored=sum(1 for x in r if isinstance(x.get('score'), (int, float))), has_label=any(('label' in x or 'predicted_class' in x or 'classification' in x) for x in r)))
    return sets, per


def jabarian():
    """Jabarian and Imas 2025: merged_corpus_withDetectors_defaultProb.json, one row per human passage with each detector's verdict on it.
    Rows that repeat a passage word for word are counted once (the paper's 1,992 passages)."""
    rows = json.load(open(os.path.join(RAW, 'tests', 'jabarian2025', 'all_json', 'different_threshold_json_files', 'merged_corpus_withDetectors_defaultProb.json')))
    seen = {}; conflicts = 0
    for r in rows:
        t = r.get('text') or ''
        if t in seen:
            if json.dumps(seen[t]['human_verdict'], sort_keys=True) != json.dumps(r['human_verdict'], sort_keys=True): conflicts += 1
            continue
        seen[t] = r
    U = list(seen.values()); genres = {}
    for r in U: genres.setdefault(r['genre'], []).append(r)
    yrs = [r['year'] for r in U if isinstance(r.get('year'), int)]
    hset = dict(rows=len(rows), passages=len(U), repeated_rows=len(rows) - len(U), repeats_with_other_verdicts=conflicts,
                genres={g: len(v) for g, v in sorted(genres.items())}, years=[min(yrs), max(yrs)] if yrs else None,
                mean_words=round(statistics.mean(words(r['text']) for r in U), 1), placeholder_texts=sum(1 for r in U if not (r.get('text') or '').strip()))
    def tally(sel, mark, valid):
        out = dict(all=[0, 0], genres={})
        for r in U:
            v = r['human_verdict'].get(sel)
            if not valid(v): continue
            k = 1 if mark(v) else 0; out['all'][0] += k; out['all'][1] += 1
            g = out['genres'].setdefault(r['genre'], [0, 0]); g[0] += k; g[1] += 1
        out['nothing_returned'] = len(U) - out['all'][1]; return out
    ori = tally('originality', lambda v: v['classification'].get('AI') == 1, lambda v: isinstance(v, dict) and isinstance(v.get('classification'), dict))
    pan = tally('pengram', lambda v: v.get('prediction') != 'Unlikely AI', lambda v: isinstance(v, dict) and isinstance(v.get('prediction'), str))
    pan_strict = tally('pengram', lambda v: v.get('prediction') not in ('Unlikely AI', 'Possibly AI'), lambda v: isinstance(v, dict) and isinstance(v.get('prediction'), str))
    labels = {}
    for r in U:
        v = r['human_verdict'].get('pengram') or {}; labels[v.get('prediction')] = labels.get(v.get('prediction'), 0) + 1
    gz = tally('gptzero', lambda v: v.get('average_generated_prob') == 1, lambda v: isinstance(v, dict) and isinstance(v.get('average_generated_prob'), (int, float)))
    gvals = sorted({r['human_verdict']['gptzero'].get('average_generated_prob') for r in U if isinstance(r['human_verdict'].get('gptzero'), dict) and 'average_generated_prob' in r['human_verdict']['gptzero']})
    return hset, dict(originality=ori, pangram=pan, pangram_possibly_not_marked=pan_strict, pangram_labels=labels, gptzero_score1=gz, gptzero_values=gvals)


def raid():
    """RAID: the released data hold no detector output. Detector scores are released only in the leaderboard's predictions on the test split,
    whose labels are kept hidden, so no score can be set beside a known-human text. The leaderboard entries carry their own release dates."""
    sub = {}
    for d in ('gptzero', 'winston-ai'):
        try: sub[d] = json.load(open(os.path.join(RAW, 'tests', 'raid', 'leaderboard', 'submissions', d, 'metadata.json')))
        except Exception: sub[d] = None
    hf = open(os.path.join(RAW, 'tests', 'raid', 'hf_README.md'), encoding='utf-8').read()
    test_unlabeled = bool(re.search(r'\*\*RAID-test\*\*\|❌', hf))
    return dict(test_split_unlabeled=test_unlabeled, leaderboard={k: (dict(date_released=v.get('date_released'), detector_name=v.get('detector_name')) if v else None) for k, v in sub.items()})


# ---------------------------------------------------------------------------------------------------------------- pairings
def rate(k, n):
    lo, hi = K.wilson(k, n) if n else (None, None)
    return dict(k=k, n=n, rate=(k / n) if n else None, lo=lo if n else None, hi=hi if n else None)


def direction(r, f):
    if not f or r.get('lo') is None: return None
    o, _ = outcome(r['lo'], r['hi'], f['form'], f['value'])
    word = {ABOVE: 'lies above', BELOW: 'lies below', CONSISTENT: 'lies at or under' if f['form'] == 'ceiling' else 'holds', CANNOT_TELL: 'straddles'}[o]
    return dict(outcome_if_matched=o, text='the interval %s the stated %s%s percent (%s)' % (word, 'ceiling of ' if f['form'] == 'ceiling' else '', ('%g' % (100 * f['value'])), f.get('version') or 'no version named'))


def build(S, stated, gate_ok):
    P = []; nothing = []
    L_sets, L_per = liang(); J_set, J = jabarian(); R = raid()
    TESTS = {
     'raid': dict(name='RAID (Dugan and others, ACL 2024)', url='https://arxiv.org/abs/2405.07940', data='https://huggingface.co/datasets/liamdugan/raid', license='MIT',
                  human_set=dict(note='Eleven domains of human text in the released data. No detector output is released beside them.'), raid=R),
     'liang2023': dict(name='Liang and others 2023', url='https://arxiv.org/abs/2304.02819', data='https://github.com/Weixin-Liang/ChatGPT-Detector-Bias', license='MIT (repository badge)',
                       human_set=dict(subsets=L_sets, texts=sum(x['texts'] for x in L_sets), dates='not stated in the release'), queried='2023-03-15'),
     'jabarian2025': dict(name='Jabarian and Imas 2025 (NBER working paper 34223)', url='https://www.nber.org/papers/w34223', data='https://github.com/brianjabarian/DetectionAI', license='MIT',
                          human_set=J_set, queried=None),
    }
    for pr in S['pairings']:
        t, m = pr['test'], pr['maker']; st = stated.get(m, {}); f = st.get('fpr')
        p = dict(test=t, test_name=TESTS[t]['name'], detector=m, detector_name=STATED[m]['name'], test_version=pr.get('version'), query_date=pr.get('query_date'),
                 stated=f, stated_status=st.get('status'), reasons=[])
        if t == 'raid':
            lb = R['leaderboard'].get({'gptzero': 'gptzero', 'winston': 'winston-ai'}.get(m, ''), None)
            p.update(outcome=NOTHING_RETURNED, why='RAID releases no detector output beside its labeled texts. Per-item scores are released only for the test split, whose labels are hidden' +
                     (', in a leaderboard entry released %s' % words_day(lb['date_released']) if lb else ', and none for this detector') + '.')
            nothing.append(p); P.append(p); continue
        if t == 'liang2023':
            per = L_per[m]; n = sum(x['n'] for x in per); lab = any(x['has_label'] for x in per)
            p['human'] = dict(texts=n, subsets=[dict(subset=x['subset'], texts=x['n']) for x in per], output='a score for each text, no label' if not lab else 'a label for each text')
        if t == 'jabarian2025':
            if m == 'gptzero':
                g = J['gptzero_score1']; p['human'] = dict(texts=g['all'][1], nothing_returned=g['nothing_returned'], output='average_generated_prob for each text, a score field with values %s, no label' % J['gptzero_values'])
                p['display'] = dict(what='texts whose score field is 1, shown only, never read as a false positive rate', **rate(*g['all']))
            else:
                g = J[m]; r = rate(*g['all'])
                p['human'] = dict(texts=g['all'][1], nothing_returned=g['nothing_returned'],
                                  output='the classification the API returned for each text' if m == 'originality' else 'the prediction label the API returned for each text (%s)' % ', '.join('%s %d' % (k, v) for k, v in sorted(J['pangram_labels'].items())))
                p['measured'] = r; p['by_genre'] = [dict(genre=k, **rate(*v)) for k, v in sorted(g['genres'].items())]
                if m == 'pangram':
                    p['marking_rule'] = 'With Possibly AI counted as not marked, %d of %d' % tuple(J['pangram_possibly_not_marked']['all'])
        # order: the stated figure must be in force at the query date, then the operating point, then the interval, then the version
        cap = capture_for(m, pr.get('query_date'))
        p['capture_on_or_before_query'] = cap
        if not f: p['reasons'].append('NO_STATED_RATE')
        if not pr.get('query_date'): p['reasons'].append('DATE_UNMATCHED'); p['date_note'] = 'the test names no date on which this detector was queried'
        elif not cap: p['reasons'].append('DATE_UNMATCHED'); p['date_note'] = 'the Internet Archive holds no capture of the maker’s page on or before %s (first capture %s)' % (words_day(pr['query_date']), words_day(st.get('first_capture')))
        if not p.get('measured'): p['reasons'].append('NO_OPERATING_POINT'); p['operating_note'] = 'the test kept a score for each text, and the maker’s page states no numeric cut-off'
        if f and p.get('measured'):
            o, why = outcome(p['measured']['lo'], p['measured']['hi'], f['form'], f['value'])
            ver_ok = bool(pr.get('version') and f.get('version') and pr['version'] == f['version'])
            if o in (ABOVE, BELOW) and not ver_ok: p['reasons'].append('VERSION_UNMATCHED')
            if why: p['reasons'].append(why)
            p['direction'] = direction(p['measured'], f)
            p['direction_other'] = [direction(p['measured'], x) for x in st.get('fpr_other', [])]
            p['interval_reading'] = o
        if 'NO_STATED_RATE' in p['reasons']: p.update(outcome='NO_STATED_RATE')
        elif p['reasons']: p.update(outcome=CANNOT_TELL, reason=p['reasons'][0])
        else: p.update(outcome=p['interval_reading'], reason=None)
        if not gate_ok and p['outcome'] in (ABOVE, BELOW, CONSISTENT): p['outcome_before_gate'] = p['outcome']; p.update(outcome=CANNOT_TELL, reason='NO_INTERVAL_FORMABLE')
        # accuracy (secondary): read only where the test's mix matches the maker's figure. No test here matches a stated mix.
        acc = (stated.get(m) or {}).get('accuracy')
        p['accuracy'] = dict(stated=acc, outcome=CANNOT_TELL if acc else 'NO_STATED_RATE', reason='MIX_DIFFERS' if acc else None,
                             why='The test’s mix of human and machine text is not the mix the maker’s figure describes (%s).' % (acc or {}).get('mix', '') if acc else None)
        P.append(p)
    return P, TESTS


def count(P, key=None):
    c = {ABOVE: 0, BELOW: 0, CONSISTENT: 0, CANNOT_TELL: 0}; nr = 0; nsr = 0; by = {}
    for p in P:
        o = (p[key]['outcome'] if key else p['outcome']) if (not key or p['outcome'] != NOTHING_RETURNED) else NOTHING_RETURNED
        r = (p[key].get('reason') if key else p.get('reason')) if o == CANNOT_TELL else None
        if o == NOTHING_RETURNED: nr += 1
        elif o == 'NO_STATED_RATE': nsr += 1
        else:
            c[o] += 1
            if r: by[r] = by.get(r, 0) + 1
    return c, nr, nsr, by


def main():
    seal, ok_plan = sealed()
    if not ok_plan: sys.exit('vk_tick: PLAN.md does not match data/plan_seal.json, refusing to read')
    if not selftest(): sys.exit('vk_tick: outcome rule selftest failed')
    S = json.load(open('sources.json')); stated, gate_ok = read_stated(S)
    P, TESTS = build(S, stated, gate_ok)
    c, nr, nsr, by = count(P); ca, nra, nsra, bya = count(P, 'accuracy')
    refused = sorted(k for k, v in stated.items() if v.get('status') == 'REFUSED')
    covered = {p['detector'] for p in P}
    no_test = sorted(k for k in STATED if k not in covered)
    req = K.req13([p for p in P if p['outcome'] in (ABOVE, BELOW, CONSISTENT, CANNOT_TELL)], nothing_returned=nr)
    disp = '%d above, %d below, %d consistent, %d cannot tell' % (c[ABOVE], c[BELOW], c[CONSISTENT], c[CANNOT_TELL])
    fpr = dict(display=disp, counts=c, nothing_returned=nr, no_stated_rate=nsr, cannot_tell_by_reason=by, pairings=c[ABOVE] + c[BELOW] + c[CONSISTENT] + c[CANNOT_TELL],
               no_test=len(no_test), refused=len(refused), held=0)
    acc = dict(display='%d above, %d below, %d consistent, %d cannot tell' % (ca[ABOVE], ca[BELOW], ca[CONSISTENT], ca[CANNOT_TELL]), counts=ca, nothing_returned=nra, no_stated_rate=nsra, cannot_tell_by_reason=bya)
    now = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    raw_files = sorted(os.path.relpath(os.path.join(r, f), H) for r, _, fs in os.walk(RAW) for f in fs if not f.endswith(('.meta.json', '.text.txt')))
    out = dict(desk='VOIGHT-KAMPFF', publisher='Heuremen LLC', label=LABEL, generated=now, updated=now, plan='PLAN.md', plan_seal=seal,
               plan_answers=json.load(open('data/plan_answers.json'))['answers'], gates=dict(stated_quotes_found=gate_ok, outcome_rule_selftest=True, passed=gate_ok),
               voightkampff=dict(fpr_outcomes=fpr, accuracy_outcomes=acc, no_test_count=len(no_test)),
               no_test=[dict(detector=k, name=STATED[k]['name']) for k in no_test], refused=[dict(detector=k, name=STATED[k]['name'], url=stated[k]['url'], why=stated[k].get('why')) for k in refused],
               held=[], req13=req, stated=stated, tests=TESTS, pairings=P,
               inputs=[dict(path=f, sha256=sha(f)) for f in raw_files if os.path.getsize(f) < 30 * 1048576])
    json.dump(out, open('summary_voightkampff.json', 'w'), indent=1, ensure_ascii=False)
    live = {k: v for k, v in out.items() if k != 'inputs'}
    json.dump(live, open('data/voightkampff_live.json.tmp', 'w'), separators=(',', ':'), ensure_ascii=False); os.replace('data/voightkampff_live.json.tmp', 'data/voightkampff_live.json')
    with open('data/voightkampff_history.jsonl', 'a') as h: h.write(json.dumps(dict(at=now, fpr=disp, nothing_returned=nr, no_test=len(no_test), refused=len(refused))) + '\n')
    print('VOIGHT-KAMPFF', disp, '| nothing returned', nr, '| no stated rate', nsr, '| no test', no_test, '| refused', refused, '| gate', gate_ok)
    for p in P: print('  %-13s %-12s %-16s %s %s' % (p['test'], p['detector'], p['outcome'], p.get('reason') or '', (p.get('measured') or {}).get('k', ''), ))
    if PUB:
        env = dict(os.environ, CLOUDFLARE_ACCOUNT_ID='<cloudflare-account-id>', PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
        r = _cf_run(['/opt/homebrew/bin/npx', 'wrangler', 'kv', 'key', 'put', 'voightkampff_live', '--path', os.path.join(H, 'data', 'voightkampff_live.json'), '--namespace-id', '<kv-namespace-id>', '--remote'],
                           cwd=os.path.expanduser('~/forge/cloudflare-workers/heuremen-door'), env=env, capture_output=True, text=True)
        print('voightkampff_live', 'published' if r.returncode == 0 else 'publish FAILED ' + (r.stderr or '')[-300:])


if __name__ == '__main__':
    if '--selftest' in sys.argv: sys.exit(0 if selftest() else 1)
    main()
