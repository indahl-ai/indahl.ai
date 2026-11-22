#!/usr/bin/env python3
"""build_page.py: writes voightkampff.html, the desk's page draft, from summary_voightkampff.json. Reads no network. The live page is built by the site
build (indahl-ai/build_site.py), which takes the body from this file."""
import json, os, sys, html
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
from vk_headline import headline
S = json.load(open('summary_voightkampff.json'))
e = html.escape
WORD = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell', 'NOTHING_RETURNED': 'nothing returned', 'NO_STATED_RATE': 'no stated rate'}
def W(o, r=None): return WORD.get(o, o) + (' (%s)' % r if r else '')
def pc(x, d=2):
    if x is None: return ''
    return ('%.' + str(d) + 'f') % (100 * x)
def num(x): return '{:,}'.format(int(x))
def day(iso):
    if not iso: return 'not named'
    y, m, d = iso[:10].split('-'); return '%d %s %s' % (int(d), ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][int(m) - 1], y)
def ts(t): return day('%s-%s-%s' % (t[:4], t[4:6], t[6:8])) if t else ''
ST = S['stated']; T = S['tests']; P = S['pairings']; F = S['voightkampff']['fpr_outcomes']; A = S['voightkampff']['accuracy_outcomes']
BIG, LINE = headline(S)
hl = '<section id="hl-slot" class="hl-slot hl"><div class="hl-big">%s</div><p class="hl-line">%s</p></section>' % (e(BIG), e(LINE))

def stated_rows():
    out = []
    for k in ('gptzero', 'originality', 'pangram', 'winston', 'turnitin', 'copyleaks'):
        s = ST[k]
        if s.get('status') != 'READ':
            out.append('<tr><td>%s</td><td><a href="%s">page</a></td><td>refused on this read (%s)</td><td></td><td></td></tr>' % (e(s['name']), e(s['url']), e(s.get('why') or '')))
            continue
        f = s.get('fpr'); figs = []
        if f: figs.append('&ldquo;%s&rdquo; (%s, %s)' % (e(f['quote']), 'a ceiling' if f['form'] == 'ceiling' else 'a point', e(f.get('version') or 'no version named')))
        for x in s.get('fpr_other') or []: figs.append('&ldquo;%s&rdquo; (%s, %s)' % (e(x['quote']), 'a ceiling' if x['form'] == 'ceiling' else 'a point', e(x['version'])))
        if not f: figs.append(e(s.get('fpr_note') or 'no numeric false positive rate'))
        a = s.get('accuracy')
        out.append('<tr><td>%s</td><td><a href="%s">page</a></td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            e(s['name']), e(s['url']), '<br>'.join(figs), ('&ldquo;%s&rdquo;' % e(a['quote'])) if a else '', e(day(s.get('read')))))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Detector</th><th>Maker&rsquo;s page</th><th>Stated false positive rate, quoted</th><th>Stated accuracy, quoted</th><th>Read</th></tr></thead><tbody>'
            + ''.join(out) + '</tbody></table></div>')

def pair_rows():
    out = []
    for p in P:
        m = p.get('measured') or {}; d = p.get('direction') or {}
        oth = '; '.join(x['text'] for x in (p.get('direction_other') or []) if x)
        beside = (d.get('text', '') + ((' and ' + oth) if oth else '')) if d else ''
        if p['outcome'] == 'NOTHING_RETURNED': beside = p.get('why', '')
        elif not d: beside = ' '.join(x for x in (p.get('date_note'), p.get('operating_note')) if x)
        hum = p.get('human') or {}
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            e(p['test_name']), e(p['detector_name']), e(p.get('test_version') or 'not named'), e(day(p.get('query_date')) if p.get('query_date') else 'not named'),
            num(hum['texts']) if hum.get('texts') is not None else '', ('%d' % m['k']) if m else '', pc(m.get('rate')) if m else '',
            ('%s to %s' % (pc(m['lo']), pc(m['hi']))) if m else '', e(W(p['outcome'], p.get('reason'))), e(beside.replace(';', ',') if beside else '')))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Test</th><th>Detector</th><th>Version the test ran</th><th>Queried</th><th>Human texts read</th><th>Marked machine-written</th>'
            '<th>Measured rate, percent</th><th>Wilson 95% interval, percent</th><th>Reading</th><th>Beside the reading</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>')

def genre_table():
    rows = []
    for p in P:
        for g in p.get('by_genre') or []:
            rows.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%d</td><td>%s</td><td>%s to %s</td></tr>' % (e(p['detector_name']), e(g['genre']), num(g['n']), g['k'], pc(g['rate']), pc(g['lo']), pc(g['hi'])))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Detector</th><th>Genre</th><th>Human passages</th><th>Marked machine-written</th><th>Rate, percent</th><th>Wilson 95% interval, percent</th></tr></thead><tbody>'
            + ''.join(rows) + '</tbody></table></div>')

def liang_sets():
    hs = T['liang2023']['human_set']
    return ''.join('<li>%s: %s texts, %s, mean %s words</li>' % (e(x['name']), num(x['texts']), e(x['writers']), x['mean_words']) for x in hs['subsets'])

J = T['jabarian2025']['human_set']; R = T['raid']['raid']
jp = next(p for p in P if p['test'] == 'jabarian2025' and p['detector'] == 'pangram'); jo = next(p for p in P if p['test'] == 'jabarian2025' and p['detector'] == 'originality')
jg = next(p for p in P if p['test'] == 'jabarian2025' and p['detector'] == 'gptzero')
lb = R['leaderboard']
gate_line = 'Every stated figure on this page was found word for word in the page as this run saved it, and the outcome rule passed its planted cases.' if S['gates']['passed'] else 'A stated figure was not found word for word in the saved page, so every reading shows cannot tell.'
seal = S['plan_seal']
body = hl + '''<p class="meta crumb">Division: <a href="/hermes">HERMES</a></p>
<p class="meta"><b>%s.</b> This desk stays off the home page until an outside read of the first run.</p>
<h2>When a detector maker states a false positive rate, what do independent tests show?</h2>
<p>Makers of tools that flag machine-written text state how often their tool marks human writing as machine-written. That rate matters most, since a false positive accuses a person who wrote their own words. This desk sets each stated rate beside independent tests that release their data, text by text, and reads the measured rate on known-human text against the stated one. It is not a ranking of detectors, and nothing on this page orders them.</p>
<p>The plan, with the detectors, the tests, the outcome rule and the headline cell, was fixed and committed before any test result was read (indahl-ai/calibrations, commit %s, %s). %s</p>
<h2>What the makers state</h2>
<p>Each figure is quoted from the maker&rsquo;s own page as this run read it. A figure written as &ldquo;no more than&rdquo; or &ldquo;under&rdquo; is a ceiling, which a measured rate can meet or exceed but never fall below. A figure written as a single number is a point.</p>
%s
<p class="bench-note">Two pages refused this reader, so their figures are not quoted here and count as refused. Neither detector has an independent test with released data in the plan, so no reading depends on them.</p>
<h2>The independent tests</h2>
<p><b>RAID</b> (Dugan and others, ACL 2024, <a href="https://arxiv.org/abs/2405.07940">paper</a>, <a href="https://huggingface.co/datasets/liamdugan/raid">data</a>, MIT license). The released data hold the texts and their labels and no detector output. Detector scores are released only in the RAID leaderboard&rsquo;s predictions on its test split, whose labels are kept hidden, so no score can be set beside a known-human text. The GPTZero leaderboard entry is dated %s and the Winston AI entry %s. No Originality.ai entry is in the leaderboard. RAID&rsquo;s own false positive figure is fixed at 5 percent by design and is never read here as a measured rate.</p>
<p><b>Liang and others 2023</b>, &ldquo;GPT detectors are biased against non-native English writers&rdquo; (<a href="https://arxiv.org/abs/2304.02819">paper</a>, <a href="https://github.com/Weixin-Liang/ChatGPT-Detector-Bias">data</a>, MIT badge on the repository). Detectors were queried on 15 March 2023. The human text read here is the four folders the repository labels human-written whose words no model edited:</p>
<ul>%s</ul>
<p>The folders of human essays rewritten or polished by a model are left out, since a model changed their words. For each text the release keeps a score from each detector and no label.</p>
<p><b>Jabarian and Imas 2025</b>, NBER working paper 34223 (<a href="https://www.nber.org/papers/w34223">paper</a>, <a href="https://github.com/brianjabarian/DetectionAI">data</a>, MIT license). The release holds %s rows of human text, %s distinct passages once %s repeated rows are counted once (%s repeats carry other verdicts, and the first is kept). Passages run from %d to %d, a mean of %s words, across six genres: %s. Every passage has its text, and none is a placeholder. The release keeps the classification Originality.ai returned for each passage, the prediction label Pangram returned, and a GPTZero score field. The paper names the API versions (Pangram v2025-05, GPTZero v2, Originality.ai Turbo) and no date on which the detectors were queried.</p>
<h2>The readings</h2>
<p>A text counts as a false positive when the detector&rsquo;s own output marks it machine-written at the maker&rsquo;s default decision. The interval is a Wilson 95 percent interval over the human texts read. Texts from one source or one writer may not be independent, and each test&rsquo;s own grouping is shown beside it.</p>
%s
<p class="bench-note">Reading, delivered relative to stated: above if the whole interval is over the stated rate or ceiling, below if the whole interval is under a stated point, consistent if the interval holds the stated point or lies at or under the stated ceiling, otherwise cannot tell. A stated figure is read only when it was in force on the date the test queried the detector, read from the Internet Archive&rsquo;s capture of the maker&rsquo;s own page on or before that date. Cannot tell carries one reason. DATE_UNMATCHED means the test names no query date, or no capture of the page exists on or before it. NO_OPERATING_POINT means the test kept only a score and the maker states no numeric cut-off, and this desk never picks one. VERSION_UNMATCHED means a rate outside the figure where the versions differ or one is not named. STRADDLES_EDGE means the interval crosses the figure. Where a rate was measured, the column beside the reading says where it lies against the figure on the maker&rsquo;s page today. That column decides nothing. Beside the pairings: %s</p>
<h3>Where the rates come from, by genre</h3>
<p>Jabarian and Imas, the two detectors whose release keeps a decision for each passage. For Pangram, any label other than Unlikely AI counts as marking a passage machine-written. %s. Originality.ai returned no classification for %s passages, which are counted as nothing returned. GPTZero&rsquo;s score field holds only the values 0 and 1 on these passages, %s of %s at 1, shown here only and never read as a false positive rate, since the maker&rsquo;s page states no cut-off and the field is not the document-level decision.</p>
%s
<h2>Accuracy, the secondary reading</h2>
<p>A stated accuracy is read only where the test&rsquo;s mix of human and machine text matches the mix the maker&rsquo;s figure describes. No test in the plan matches a stated mix, so every accuracy pairing with released output reads cannot tell (MIX_DIFFERS): %s. %s more returned no per-item output.</p>
<h2>Detectors with no independent test</h2>
<p>No independent test with released data covers Turnitin or Copyleaks. Their claims count as no independent test, and both pages refused this reader. Weber-Wulff and others 2023 tested Turnitin and released no data that the plan found.</p>
<h2>Nothing returned, refused and held</h2>
<p>Counted apart and never folded into a reading. Pairings with no per-item output on known-human text: %s, all from RAID. Maker pages that refused this reader: %s. Tests held: %s. Passages inside a returned pairing with no output from the detector: GPTZero %s and Originality.ai %s in Jabarian and Imas.</p>
<h2>What this page holds and what it leaves out</h2>
<p>Every reading prints the test&rsquo;s date and the detector version it ran. Detectors change often, so a test from 2023 or 2025 describes that version and no later one. A reading says how a stated rate and a measured rate compare. It does not say why they differ. ZeroGPT appears in the tests and states no figure this plan read, so it is left out. Every count on this page comes from the run log.</p>
<p class="meta">Sources: the makers&rsquo; own pages as linked above, read %s, and their Internet Archive captures. RAID, Liang and others 2023, and Jabarian and Imas 2025, each downloaded from its public home and credited under its license. All read without a key, one request at a time. Generated %s. Heuremen LLC.</p>
<p class="meta">The newest run is always in <a href="/voightkampff/live.json">/voightkampff/live.json</a>.</p>
<p class="meta">Plan and code for this page are public: <a href="https://github.com/indahl-ai/indahl.ai/tree/main/code/voightkampff">voightkampff</a>. The plan was fixed before the comparison it describes.</p>''' % (
    e(S['label']), e(seal['plan_commit'][:7]), e(day(seal['plan_commit_time'])), gate_line, stated_rows(),
    e(day(lb['gptzero']['date_released'])), e(day(lb['winston-ai']['date_released'])), liang_sets(),
    num(J['rows']), num(J['passages']), num(J['repeated_rows']), num(J['repeats_with_other_verdicts']), J['years'][0], J['years'][1], J['mean_words'],
    ', '.join('%s %s' % (k, num(v)) for k, v in J['genres'].items()),
    pair_rows(), e(S['req13']['line']),
    e(jp['marking_rule']), num(jo['human']['nothing_returned']), num(jg['display']['k']), num(jg['display']['n']), genre_table(),
    e(A['display']), num(A['nothing_returned']),
    num(F['nothing_returned']), e(', '.join(x['name'] for x in S['refused']) or 'none'), num(len(S['held'])), num(jg['human']['nothing_returned']), num(jo['human']['nothing_returned']),
    e(day(ST['gptzero'].get('read'))), e(day(S['generated'])))
TITLE = 'VOIGHT-KAMPFF | AI-text detector claims against independent tests | Heuremen LLC'
DESC = 'VOIGHT-KAMPFF: the false positive rates AI-text detector makers state, set beside independent tests that release their data text by text.'
page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="https://indahl.ai/voightkampff">
<meta name="author" content="Heuremen LLC">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header class="top"><div class="wrap bar"><a class="brand" href="/"><span>Heuremen LLC</span></a></div></header>
<section class="hero slim"><div class="wrap"><h1><b class="ac">VOIGHT-KAMPFF</b> &middot; AI-text detector claims against independent tests</h1></div></section>
<main class="wrap">%s</main>
</body>
</html>
''' % (e(TITLE), e(DESC), body)
open('voightkampff.html', 'w').write(page); print('voightkampff.html', len(page))
