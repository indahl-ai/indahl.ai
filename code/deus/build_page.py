#!/usr/bin/env python3
"""build_page.py: writes deus.html, the desk page draft, from data/deus.json (the newest run of deus_read.py). Reads no network. The live page is
built by the site build, which takes the body from this file. Names of labs and models appear only in table rows, never in a title or heading,
and no table is ordered by score."""
import json, os, sys, html, time
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
from deus_headline import headline
D = json.load(open('data/deus.json'))
e = html.escape
WORD = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell', 'NOTHING_RETURNED': 'no rerun', 'HELD': 'held', 'BENCHMARK_DROPPED': 'benchmark dropped'}
COI_ROW = 'Conflict of interest: this desk is read and built by models made by Anthropic.'
def n(x): return '{:,}'.format(int(x))
def pc(x, d=1): return '' if x is None else ('%.' + str(d) + 'f') % (100 * x)
def day(s): return time.strftime('%d %B %Y', time.strptime(s[:10], '%Y-%m-%d')).lstrip('0') if s and len(s) >= 10 else (s or '')
def W(c): return WORD.get(c['outcome'], c['outcome'].lower()) + (' (%s)' % c['reason'] if c.get('reason') and c['outcome'] == 'CANNOT_TELL' else '')
MODEL_NAME = lambda c: c.get('model_label') or c['model']
def src_links(c):
    return ' '.join('<a href="%s">%s</a>' % (e(p['url']), e(p['page_date'] or 'page')) for p in c['pages'][:3])
def rerun_cell(c):
    return '<br>'.join('%s: %s (%s to %s)' % (e(r['name']), pc(r['value']), pc(r['lo']), pc(r['hi'])) for r in c.get('reruns', []))
read = [c for c in D['claims'] if c['outcome'] in ('ABOVE', 'BELOW', 'CONSISTENT', 'CANNOT_TELL')]
norr = [c for c in D['claims'] if c['outcome'] == 'NOTHING_RETURNED']
held = [c for c in D['claims'] if c['outcome'] == 'HELD']
drop = [c for c in D['claims'] if c['outcome'] == 'BENCHMARK_DROPPED']
key = lambda c: (c['benchmark'], c['lab'], c['model'], c['printed'])
def claim_rows(cs, with_rerun=True):
    out = []
    for c in sorted(cs, key=key):
        car = len(c.get('carriers') or [])
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>%s<td>%s</td><td>%s</td><td>%s</td></tr>' % (
            e(c['benchmark']), e(c['lab']), e(MODEL_NAME(c)), e(c.get('variant') or ''), e(c['printed']), e(c.get('effort') or 'not named'),
            ('<td>%s</td>' % rerun_cell(c)) if with_rerun else '', e(W(c)) + (', stated %s' % c['direction'] if c.get('direction') and c['outcome'] == 'CANNOT_TELL' else ''),
            ('%d fields' % car) if with_rerun and car else (e(c.get('reason') or '') if not with_rerun else ''), src_links(c) + (('<br><span class="bench-note">%s</span>' % COI_ROW) if c['lab'] == 'Anthropic' else '')))
    return ''.join(out)
TH = '<th>Benchmark</th><th>Lab</th><th>Model as printed</th><th>Variant printed</th><th>Stated</th><th>Reasoning effort</th>'
h = D['headline']; f = h['four']; nr = D['no_rerun']; o = D['order']; B = D['frame']['benchmarks']
HL_BIG, HL_LINE = headline(D)
hl = '<section id="hl-slot" class="hl-slot hl"><div class="hl-big">%s</div><p class="hl-line">%s</p></section>' % (e(HL_BIG), e(HL_LINE))
nrb = ''.join('<tr><td>%s</td><td>%s</td><td>%d</td></tr>' % (e(k.split(' | ')[0]), e(k.split(' | ')[1]), v) for k, v in sorted(nr['by_lab_benchmark'].items()))
bench_rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (e(b), e(v['status']), e(v['why'])) for b, v in B.items())
held_pages = ''.join('<li>%s, <a href="%s">%s page</a>: %s</li>' % (e(x['lab']), e(x['url']), e(x['url'].split('/')[2]), e(x['why'])) for x in D['pages']['held'])
ords = [x for x in D['orders'] if x['outcome'] != 'NOTHING_RETURNED']
ord_rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s %s</td><td>%s %s</td><td>%s</td></tr>' % (
    e(x['benchmark']), e(x['lab']), e(x['higher']), e(x['higher_printed']), e(x['lower']), e(x['lower_printed']),
    e(WORD[x['outcome']] + (' (%s)' % x['reason'] if x.get('reason') else '') + (', %s' % x['direction'] if x.get('direction') else ''))) for x in sorted(ords, key=lambda x: (x['benchmark'], x['lab'], x['higher'], x['lower'])))
labs_read = ', '.join(D['frame']['labs_with_pages_read'])
body = hl + '''<p class="meta crumb">Division: <a href="/hermes">HERMES</a></p>
<p class="bench-note"><b>%s.</b> %s</p>
<h2>When a lab states a benchmark score for its own model, where does an independent rerun put it?</h2>
<p>Model developers print benchmark scores for their own models in launch posts and model cards. This desk sets each printed score beside a rerun of the same model on the same benchmark by someone other than the developer, here the Epoch AI Benchmarking Hub, which runs models itself with one harness and states what its error bars measure. The frame was fixed in a plan before any rerun score was read: the labs named in the plan, launch posts and model cards dated 1 January to 31 October 2026, and the benchmarks GPQA Diamond, SWE-bench Verified, FrontierMath Tiers 1 to 3, Humanity’s Last Exam and AIME 2025. Each printed score is one claim. The same score printed again on another page of the same lab is the same claim.</p>
<p>Conflict of interest. The readers and builders of this desk are models made by Anthropic, one of the labs measured. Every Anthropic row carries this line. The method is the mitigation: a lab’s printed number is set beside someone else’s rerun, with the same rules and the same outcomes for every lab, and no rule written for one lab alone.</p>
<h2>Stated scores with an independent rerun</h2>
<p>%s claims from %s models have a rerun. Four-way: %s consistent, %s above, %s below, %s cannot tell. The share above is %s percent, with a 95 percent interval of %s to %s percent from a bootstrap that draws whole models, since claims for one model are not independent. Every draw is zero when no claim reads above, so that interval shows no spread.</p>
<div class="tw"><table class="bench"><thead><tr>%s<th>Rerun, percent (95%% interval)</th><th>Reading</th><th>Setup fields unnamed or different</th><th>Page</th></tr></thead><tbody>%s</tbody></table></div>
<p class="bench-note">Reading: above if the stated score, at its printed rounding, sits above the whole rerun interval with every setup field named and matching on both sides, below if it sits under the whole interval with the same, consistent if it falls inside the interval, otherwise cannot tell. A printed 88.2 means 88.15 to 88.25. The setup fields are harness, prompt format, chat template, few-shot, max tokens, temperature, stop, extraction rule, dataset version, items and seeds, plus reasoning effort, tools and scaffold, attempts and trials averaged. A score outside the interval with any field different or unnamed reads cannot tell, and the side the stated score falls on is written beside it. Where the claim names a reasoning effort, only reruns at that effort or at none named are paired with it. Where two reruns of one pairing fall on opposite sides of the stated score, the claim reads cannot tell. The rerun interval is Epoch’s standard error of the mean over runs times 1.96. Epoch’s own page says its error bars are plus and minus one standard error. No size that matters is named in this first run, so each reading is against the stated value alone.</p>
<h2>Stated scores with no independent rerun</h2>
<p>%s claims in the frame have no independent rerun. They are counted here and are not in the share above. A rerun that is the developer’s own figure would be counted apart as the claim repeated, and none was found.</p>
<div class="tw"><table class="bench"><thead><tr><th>Lab</th><th>Benchmark</th><th>Claims with no rerun</th></tr></thead><tbody>%s</tbody></table></div>
<div class="tw"><table class="bench"><thead><tr>%s<th>Reading</th><th>Why</th><th>Page</th></tr></thead><tbody>%s</tbody></table></div>
<h2>Benchmarks kept and dropped</h2>
<p>A benchmark stays in the frame only if the Epoch file holds at least one run of it that counts as independent. That test read the list of files and their columns, never a score.</p>
<div class="tw"><table class="bench"><thead><tr><th>Benchmark</th><th>Status</th><th>Why</th></tr></thead><tbody>%s</tbody></table></div>
<p>%s printed scores on the dropped benchmarks are listed in the feed and are not read.</p>
<h2>Held</h2>
<p>A page read only in part is held and left out of every count above. %s claims are held. For %s of them the page that introduces the model prints no date. Pages held:</p>
<ul>%s</ul>
<h2>Charts that put one model above another</h2>
<p>Launch tables print other models beside the lab’s own. Each pair the lab prints for a benchmark in the frame is one order claim, read where one independent source ran both models under the same setup. Consistent: the rerun puts the higher printed model above the other with the two intervals apart. Above: the rerun puts them the other way round with the intervals apart. Cannot tell: the intervals overlap or the two runs differ in a setup field. %s order claims: %s consistent, %s above, %s cannot tell, and %s with no rerun of both models.</p>
<div class="tw"><table class="bench"><thead><tr><th>Benchmark</th><th>Lab printing</th><th>Printed higher</th><th>Printed lower</th><th>Reading</th></tr></thead><tbody>%s</tbody></table></div>
<h2>Context windows, knowledge cutoffs, speed and price</h2>
<p>The plan reads these three kinds of claim only against an independent source with released data and a stated method, named and quoted before the read. None was named before this first run, so every one counts as no rerun: %s lines stating a context window, %s stating a knowledge cutoff and %s stating a price or a speed, counted from the text of the pages read (figures printed only in images are not in these counts).</p>
<h2>What this page holds and what it leaves out</h2>
<p>Pages read: %s, from %s. Left out: system cards, technical reports, pages of these labs not listed in the feed, and every benchmark outside the five named. A reading says where a printed score sits against a rerun with the setup each side names. It does not say why the two differ.</p>
<p class="meta">Sources: the labs’ own launch posts and model cards, read %s. Epoch AI, Capabilities and benchmarking, Benchmarking Hub data, %s, CC BY 4.0. Generated %s. Heuremen LLC.</p>
<p class="meta">The newest run is always in <a href="/deus/live.json">/deus/live.json</a>.</p>
<p class="meta">Plan and code for this page are public: <a href="https://github.com/indahl-ai/indahl.ai/tree/main/code/deus">deus</a>. The plan was fixed before the comparison it describes.</p>
<p class="meta">Data read from: <a href="https://epoch.ai/benchmarks/use-this-data">Epoch AI Benchmarking Hub</a> &middot; <a href="https://epoch.ai/benchmarks/about">Epoch AI methodology</a>.</p>
<p class="meta">Named here and want to answer a row? <a href="/respond?u=deus-all">Respond</a></p>
<section id="replies" data-prefix="deus"></section><script src="/replies.js" defer></script>''' % (
    e(D['label'][0]), e(D['label'][1] + ': lab pages read for ' + labs_read + '. Pages held are listed below.'),
    n(h['of']), n(h['models']), n(f['CONSISTENT']), n(f['ABOVE']), n(f['BELOW']), n(f['CANNOT_TELL']), pc(h['share']), pc(h['lo']), pc(h['hi']),
    TH, claim_rows(read),
    n(nr['count']), nrb, TH, claim_rows(norr, with_rerun=False),
    bench_rows, n(len(drop)),
    n(len(held)), n(sum(1 for c in held if 'prints no date' in (c.get('reason') or ''))), held_pages,
    n(o['count']), n(o['four']['CONSISTENT']), n(o['four']['ABOVE']), n(o['four']['CANNOT_TELL']), n(o['nothing_returned']), ord_rows,
    n(D['context']['candidates']), n(D['cutoff']['candidates']), n(D['speed_price']['candidates']),
    n(D['pages']['read']), labs_read, day(D['generated']), e(D['sources']['epoch']['fetched_utc'][:10]), day(D['generated']))
TITLE = 'DEUS | Stated benchmark scores against independent reruns | Heuremen LLC'
DESC = 'DEUS: benchmark scores model developers print for their own models, set beside independent reruns from the Epoch AI Benchmarking Hub, read as ABOVE, BELOW, CONSISTENT or CANNOT_TELL with every setup field named.'
page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="https://indahl.ai/deus">
<meta name="author" content="Heuremen LLC">
<link rel="stylesheet" href="/style.css">
<style>.tw{overflow-x:auto}table.bench{border-collapse:collapse;font-size:.86rem}table.bench th,table.bench td{padding:.3rem .55rem;border-bottom:1px solid #ccc;text-align:left;vertical-align:top}</style>
</head>
<body>
<header class="top"><div class="wrap bar"><a class="brand" href="/"><span>Heuremen LLC</span></a></div></header>
<section class="hero slim"><div class="wrap"><h1><b class="ac">DEUS</b> &middot; Stated benchmark scores against independent reruns</h1></div></section>
<main class="wrap">%s</main>
</body>
</html>
''' % (e(TITLE), e(DESC), body)
open('deus.html', 'w').write(page); print('deus.html', len(page))
