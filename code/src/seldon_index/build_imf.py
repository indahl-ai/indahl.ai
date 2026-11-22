#!/usr/bin/env python3
"""build_imf.py: SELDON desk, IMF side (secondary cell seldon.imf_probability_events, PLAN.md section 4). The statements below were picked from
data/imf_scan.json (scan_imf.py): every sentence in a WEO chapter 1 that states a number for the chance of a defined global growth event in a named
year. Each quoted fragment is checked against the text of its page (pymupdf) and any miss refuses the build. The outturn for year Y is World Output
for Y in Table 1.1 of the October WEO of year Y + 1, as the IMF's own evaluation reads it (PLAN.md section 4). A missing October issue, or a year
whose October issue is not out, is held. Writes data/imf_events.json. The tick reads only that file. Run with python3 -I."""
import os, re, json, sys, hashlib, time, site
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
sys.path.append(site.getusersitepackages()); import pymupdf
def norm(t): return re.sub(r'\s+', ' ', t.replace('­', '').replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('–', '-').replace('—', '-').replace('−', '-')).strip()
def key(t): return re.sub(r'[^a-z0-9.]', '', norm(t).lower())
# kind: below (outturn < thr), at_most (<= thr), above (> thr), between [lo, hi], per_capita (no per capita world growth in Table 1.1: held)
S = [
 dict(id='2006-10.2007.at_most_3.25', issue='2006 october', page=7, years=[2007], kind='at_most', thr=3.25, p=1 / 6, p_text='one in six',
      quote='there is a one in six chance of growth in 2007 falling to'),
 dict(id='2008-04.2008-2009.at_most_3', issue='2008 april', page=31, years=[2008, 2009], kind='at_most', thr=3.0, p=0.25, p_text='25 percent',
      quote='sees a 25 percent chance of growth slowing to 3 percent or less in 2008 and 2009'),
 dict(id='2012-10.2013.below_2', issue='2012 october', page=14, years=[2013], kind='below', thr=2.0, p=0.17, p_text='about 17 percent',
      quote='The probability of global growth falling below 2 percent in 2013'),
 dict(id='2013-10.2014.below_2', issue='2013 october', page=14, years=[2014], kind='below', thr=2.0, p=0.06, p_text='about 6 percent',
      quote='the probability of global growth falling to less than 2 percent in 2014 is quite low, at about 6 percent'),
 dict(id='2014-10.2015.below_2', issue='2014 october', page=13, years=[2015], kind='below', thr=2.0, p=0.01, p_text='less than 1 percent', p_bound='under',
      quote='The probability of global growth falling below the 2 percent recession threshold in 2015 is less than 1 percent'),
 dict(id='2022-10.2023.below_2', issue='2022 october', page=20, years=[2023], kind='below', thr=2.0, p=0.25, p_text='about 25 percent',
      quote='The estimated probability of one-year-ahead global growth below 2.0 percent'),
 dict(id='2023-04.2023.below_2', issue='2023 april', page=15, years=[2023], kind='below', thr=2.0, p=0.25, p_text='about 25 percent',
      quote='the estimated probability of global growth in 2023 falling below 2.0 percent'),
 dict(id='2023-04.2023.per_capita', issue='2023 april', page=15, years=[2023], kind='per_capita', p=0.15, p_text='about 15 percent',
      quote='A con- traction in global per capita real GDP in 2023'),
 dict(id='2023-04.2023.between_1.0_3.8', issue='2023 april', page=28, years=[2023], kind='between', lo=1.0, hi=3.8, p=0.70, p_text='70 percent',
      quote='There is a 70 percent probability that 2023 global growth could be between 1.0 percent and 3.8 percent'),
 dict(id='2023-10.2023.below_2', issue='2023 october', page=22, years=[2023], kind='below', thr=2.0, p=0.05, p_text='about 5 percent',
      quote='The estimated probability that global growth in 2023 will fall below 2.0 percent'),
 dict(id='2023-10.2024.per_capita', issue='2023 october', page=22, years=[2024], kind='per_capita', p=0.10, p_text='below 10 percent', p_bound='under',
      quote='in 2024 has an estimated probability below 10 percent'),
 dict(id='2023-10.2024.above_3.8', issue='2023 october', page=22, years=[2024], kind='above', thr=3.8, p=0.20, p_text='less than 20 percent', p_bound='under',
      quote='the probability of global growth'),
 dict(id='2023-10.2023.between_2.6_3.4', issue='2023 october', page=30, years=[2023], kind='between', lo=2.6, hi=3.4, p=0.70, p_text='70 percent',
      quote='There is a 70 percent probability that global growth will be between 2.6 percent and 3.4 per- cent in 2023'),
 dict(id='2023-10.2024.between_1.9_4.0', issue='2023 october', page=30, years=[2024], kind='between', lo=1.9, hi=4.0, p=0.70, p_text='70 percent',
      quote='a 70 percent probability that growth will be between 1.9 percent and 4.0 percent in 2024'),
 dict(id='2024-04.2024.below_2', issue='2024 april', page=19, years=[2024], kind='below', thr=2.0, p=0.10, p_text='about 10 percent',
      quote='The estimated probability that global growth in 2024 will fall below 2.0 percent'),
 dict(id='2024-04.2024.per_capita', issue='2024 april', page=19, years=[2024], kind='per_capita', p=0.05, p_text='below 5 percent', p_bound='under',
      quote='in 2024 has an estimated probability below 5 percent'),
 dict(id='2024-04.2024.above_3.8', issue='2024 april', page=20, years=[2024], kind='above', thr=3.8, p=0.20, p_text='slightly above 20 percent', p_bound='over',
      quote='during 2000-19 is slightly above 20 percent for 2024'),
 dict(id='2024-04.2024.between_2.4_4.1', issue='2024 april', page=25, years=[2024], kind='between', lo=2.4, hi=4.1, p=0.70, p_text='70 percent',
      quote='there is a 70 percent probability that growth will be between 2.4 percent and 4.1 percent in 2024'),
 dict(id='2024-04.2025.between_2.2_4.3', issue='2024 april', page=25, years=[2025], kind='between', lo=2.2, hi=4.3, p=0.70, p_text='70 percent',
      quote='a 70 percent probability that growth will be between 2.2 percent and 4.3 percent in 2025'),
 dict(id='2024-10.2025.below_2', issue='2024 october', page=25, years=[2025], kind='below', thr=2.0, p=0.17, p_text='about 17 percent',
      quote='The probability of global growth in 2025 falling below 2 percent is assessed at about 17 percent'),
 dict(id='2025-04.2025.below_2', issue='2025 april', page=28, years=[2025], kind='below', thr=2.0, p=0.30, p_text='close to 30 percent',
      quote='The probability that global growth in 2025 will fall below 2 percent is assessed at close to 30 percent'),
 dict(id='2025-10.2026.below_2', issue='2025 october', page=31, years=[2026], kind='below', thr=2.0, p=0.25, p_text='about 25 percent',
      quote='The probability that global growth in 2026 will fall below 2 percent is assessed at about 25 percent'),
 dict(id='2026-04.2026.below_2', issue='2026 april', page=26, years=[2026], kind='below', thr=2.0, p=0.25, p_text='25 percent',
      quote='the probability that global growth in 2026 will fall below 2 percent has not changed and remains elevated at 25 percent'),
 dict(id='2026-10.2027.below_2', issue='2026 october', page=25, years=[2027], kind='below', thr=2.0, p=0.10, p_text='about 10 percent',
      quote='The probability that global growth in 2027 will fall below 2 percent is about 10 percent'),
]
NOT_COUNTED = [
 dict(issue='2010 october', page=26, why='no named year: the sentence reads the coming year', quote='the probability of global growth falling below 2 percent is less than 5 percent'),
 dict(issue='2011 october', page=17, why='no number for the chance', quote='The probability of global growth below 2 p'),
 dict(issue='2016 april', page=26, why='no number for the chance', quote='noticeable increase in the probability of global growth declining below 2 percent'),
]
def fpath(issue): y, m = issue.split(); return 'data/raw/imf_weo/weo_%s_%s_ch1.pdf' % (y, m)
_pages = {}
def page_text(f, p):
    if (f, p) not in _pages: _pages[(f, p)] = pymupdf.open(f)[p - 1].get_text()
    return _pages[(f, p)]
bad = []
for s in S + NOT_COUNTED:
    f = fpath(s['issue'])
    if not os.path.exists(f) or key(s['quote']) not in key(page_text(f, s['page'])): bad.append((s.get('id') or s['issue'], s['page'], s['quote'][:80]))
if bad:
    for b in bad: print('QUOTE NOT FOUND', b)
    sys.exit(1)
OUT = {}; OUT_SRC = {}
def outturn(y):
    """World Output for year y from Table 1.1 of the October WEO of y + 1. Returns (value, source) or (None, why)."""
    f = fpath('%d october' % (y + 1))
    if not os.path.exists(f): return None, 'the October %d WEO is not in the run' % (y + 1)
    d = pymupdf.open(f)
    for i, pg in enumerate(d):
        t = pg.get_text()
        m = re.search(r'World [Oo]utput', t)
        if not re.search(r'Table 1\.1\.?\s+Overview of the World Economic Outlook', t) or not m: continue
        head, rest = t[:m.start()], t[m.end():]
        yrs = [int(l.strip()) for l in head.split('Table 1.1', 1)[1].splitlines() if re.fullmatch(r'\s*(19|20)\d\d\s*', l)]
        vals = re.findall(r'[–−-]?\d+\.\d', re.split(r'Advanced [Ee]conomies', rest, maxsplit=1)[0])
        if y not in yrs: return None, 'year %d not in Table 1.1 of the October %d WEO' % (y, y + 1)
        v = float(vals[yrs.index(y)].replace('–', '-').replace('−', '-'))
        return v, 'October %d WEO, chapter 1, Table 1.1, page %d, World Output, %d' % (y + 1, i + 1, y)
    return None, 'Table 1.1 not found in the October %d WEO' % (y + 1)
rows = []
for s in S:
    r = dict(s); r['file'] = fpath(s['issue']); r['outturn'] = {}; r['held'] = None
    if s['kind'] == 'per_capita': r['held'] = 'Table 1.1 prints no per capita world growth, so the outturn is not read'
    else:
        for y in s['years']:
            v, src = outturn(y)
            if v is None: r['held'] = src; break
            r['outturn'][str(y)] = dict(value=v, source=src)
    if r['held'] is None:
        def hit(v):
            if s['kind'] == 'below': return v < s['thr']
            if s['kind'] == 'at_most': return v <= s['thr']
            if s['kind'] == 'above': return v > s['thr']
            if s['kind'] == 'between': return s['lo'] <= v <= s['hi']
        r['happened'] = all(hit(o['value']) for o in r['outturn'].values())
    else: r['happened'] = None
    rows.append(r)
shas = {f: hashlib.sha256(open(f, 'rb').read()).hexdigest() for f in sorted(set([fpath(s['issue']) for s in S + NOT_COUNTED] + [o['source'] and fpath('%d october' % (int(y) + 1)) for r in rows for y, o in r['outturn'].items()]))}
out = dict(built=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), statements=rows, not_counted=NOT_COUNTED, file_sha256=shas,
           read='Outturn: World Output in Table 1.1 of the next year October WEO, at its printed one decimal. Below is strictly under the threshold, at most includes it, between includes both ends.')
json.dump(out, open('data/imf_events.json', 'w'), indent=1, ensure_ascii=False)
print('statements', len(rows), 'resolved', sum(r['happened'] is not None for r in rows), 'held', sum(r['happened'] is None for r in rows), 'not counted', len(NOT_COUNTED))
for r in rows: print(r['id'], r['outturn'] and {k: v['value'] for k, v in r['outturn'].items()}, r['happened'], r['held'] or '')
