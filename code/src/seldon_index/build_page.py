#!/usr/bin/env python3
"""build_page.py: writes seldon.html, the desk's page draft, from summary_seldon.json. Reads no network. The live page is built by the site build
(indahl-ai/build_site.py), which takes the body from this file, as for ZEUS."""
import json, os, sys, html
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
from seldon_headline import headline, W as Wd, pc
S = json.load(open('summary_seldon.json')); e = html.escape
Z = S['seldon']; G = S['gates']
MEAS = {'deficit': 'Deficit, percent of GDP', 'debt': 'Debt held by the public, percent of GDP', 'growth': 'Real GDP growth, percent a year'}
MON = {'01': 'January', '02': 'February', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '12': 'December'}
def month(m): y, mm = m.split('-'); return '%s %s' % (MON.get(mm, mm), y)
def tgt(r): return ('fiscal year %d' % r['year']) if r['measure'] in ('deficit', 'debt') else (('%d to %d average' % (r['start'], r['end'])) if r.get('start') else ('calendar %d' % r['year']))
def fmt(v, r): return ('%d' % round(v)) if r['measure'] == 'debt' else ('%.1f' % v)
def rng(r): return '%s to %s' % (fmt(r['lo'], r), fmt(r['hi'], r))
SIDE = {'inside': 'inside', 'above': 'above the range', 'below': 'below the range'}
def range_rows(rs, revised=True):
    out = []
    for r in rs:
        rv = '' if r.get('outturn_revised') is None else '%.2f' % r['outturn_revised']
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%d</td><td>%s</td><td>%.2f</td><td>%s</td>%s</tr>' % (
            e(month(r['report_month'])), e(MEAS[r['measure']]), e(tgt(r)), r['horizon'], e(rng(r)), r['outturn'], e(SIDE[r['side']]), ('<td>%s</td>' % rv) if revised else ''))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Report</th><th>Measure</th><th>Target</th><th>Years ahead</th><th>Stated two-thirds range</th><th>Outcome</th><th>Where it fell</th>'
            + ('<th>Growth on revised data</th>' if revised else '') + '</tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>')
def cell_rows():
    out = []
    for lab, c in (('Three or more years ahead (headline)', Z['cbo_range_hit_share']), ('Same ranges, outcome read unrounded', Z['cbo_range_hit_share_unrounded']),
                   ('Same ranges, growth on revised data', Z['cbo_range_hit_share_revised']), ('Under three years ahead', Z['cbo_short_horizon_hit_share'])):
        out.append('<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td><td>%s</td><td>%s to %s</td><td>%s</td></tr>' % (
            e(lab), c['reports'], c['ranges'], c['hits'], pc(c['value']), pc(c['lo']), pc(c['hi']), e(Wd(c))))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Cell</th><th>Reports</th><th>Ranges</th><th>Outcome inside</th><th>Share, percent</th><th>95% interval, percent</th>'
            '<th>Reading against two-thirds</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>')
KIND = {'below': 'below %s percent', 'at_most': 'at %s percent or less', 'above': 'above %s percent'}
def ev(s):
    yrs = ' and '.join(str(y) for y in s['years'])
    if s['kind'] == 'between': what = 'between %s and %s percent' % (s['lo'], s['hi'])
    elif s['kind'] == 'per_capita': what = 'a fall in world output per person'
    else: what = KIND[s['kind']] % ('%g' % s['thr'])
    return 'World growth in %s %s' % (yrs, what) if s['kind'] != 'per_capita' else '%s in %s' % (what[0].upper() + what[1:], yrs)
def imf_rows():
    out = []
    for s in Z['imf_probability_events']['events']:
        y, m = s['issue'].split(); o = ', '.join('%s: %.1f' % (k, v) for k, v in s['outturn'].items())
        res = 'held: ' + s['held'] if s['happened'] is None else ('happened' if s['happened'] else 'did not happen')
        out.append('<tr><td>%s %s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (m.capitalize(), y, e(ev(s)), e(s['p_text']), e(o), e(res)))
    return ('<div class="tw"><table class="bench"><thead><tr><th>WEO issue</th><th>Event</th><th>Stated chance</th><th>World growth, percent</th><th>Result</th></tr></thead><tbody>'
            + ''.join(out) + '</tbody></table></div>')
HL_BIG, HL_LINE = headline(S)
hl = '<section id="hl-slot" class="hl-slot hl"><div class="hl-big">%s</div><p class="hl-line">%s</p></section>' % (e(HL_BIG), e(HL_LINE))
gate_line = 'All known-good checks passed on this run.' if G['passed'] else 'A known-good check did not pass on this run, so every reading shows cannot tell.'
h = Z['cbo_range_hit_share']; im = Z['imf_probability_events']
_debt = [r for r in S['ranges'] if r['measure'] == 'debt']
_dy = sorted({r['year']: r['outturn'] for r in _debt}.items())
debt_line = ('Debt held by the public ended %s. Of the %d debt ranges three or more years ahead, %d sat below the outcome.' % (
    ' and '.join('fiscal year %d at %.1f percent of GDP' % (y, v) for y, v in _dy), len(_debt), sum(1 for r in _debt if r['side'] == 'above'))) if _debt else ''
held_line = 'Held, with no outcome yet and left out of every cell: ' + ', '.join('%s %s for %s' % (month(r['report_month']), r['measure'], tgt(r)) for r in S['held']) + '.'
body = hl + '''<p class="meta crumb">Division: <a href="/hermes">HERMES</a></p>
<p class="meta">%s</p>
<h2>When the Congressional Budget Office prints a two-thirds range years ahead, does the outcome land inside it?</h2>
<p>Since August 2016 the Congressional Budget Office has printed ranges around some of its projections for the deficit, federal debt held by the public and average real GDP growth. Each range comes with the same words: &ldquo;roughly a two-thirds chance&rdquo; or &ldquo;approximately a two-thirds chance&rdquo; that the outcome falls between two numbers. CBO says it builds these ranges &ldquo;based on historical&rdquo; differences between its past baseline projections and the outcomes. If the ranges are sized as stated, about two in three outcomes should land inside.</p>
<p>This desk reads every such range CBO printed with two endpoints, in the report that first printed it, and sets it beside the outcome. The deficit and the debt are fiscal-year figures as CBO records them in its own evaluation data, divided by fiscal-year GDP. Growth is the calendar-year average annual growth of real GDP, from the first CBO data release after the period in which the whole period is actual, with the latest revised figure printed beside it. A range holds the outcome when the outcome, rounded to the decimals the range prints, lies between the two endpoints, endpoints included. The headline counts ranges whose target year is three or more years after the report. The interval comes from a bootstrap that draws whole reports, so ranges from one report stay together. The plan, with the frame, the headline cell and the outcome rule, was fixed and committed before any outcome was read, and the list of ranges was copied from the reports and committed before any actual was opened. %s</p>
<h2>The reading</h2>
%s
<p class="bench-note">Reading: CBO states roughly two-thirds, read as 66.7 percent. Consistent if the 95%% interval contains 66.7 percent, above if the whole interval is higher, below if the whole interval is lower, cannot tell with the reason when fewer than ten ranges count. Above means more outcomes fell inside than stated, so the ranges were wider than needed. The headline is the first row. The second row reads the same ranges with the outcome unrounded, the third reads growth on the latest revised data.</p>
<p>Three things travel with every result. CBO projects under current law, so a later change in law can move an outcome away from a projection made under the law of its day. CBO sizes its ranges from its own past record, so a share near two-thirds is partly built in over the years that record covers. Few reports print ranges, which widens the interval. %s</p>
<h2>Every range three or more years ahead</h2>
%s
<h2>Ranges under three years ahead</h2>
<p>Printed apart, as the plan says.</p>
%s
<h2>Chances the IMF states for world growth</h2>
<p>A secondary reading. Each World Economic Outlook issue was searched for a sentence that puts a number on the chance of a defined world growth event in a named year. The outcome is World Output in Table 1.1 of the next October issue, as the IMF reads its own record. Of %d statements, %d have an outcome and %d are held. The plan reads this list as a measurement with no outcome unless at least twenty statements have one, so no reading is given.</p>
%s
<h2>Nothing returned</h2>
<p>%s %d ranges were read in full and none was refused. Spreads printed with no endpoints and ranges a later report printed again were listed apart and not counted.</p>
<h2>What this page holds and what it leaves out</h2>
<p>Left out: ranges CBO showed only in charts, ranges for inflation, unemployment and interest rates, and CBO reports before August 2016, which printed fan charts with no two-thirds endpoints for these measures. A reading says how often outcomes landed inside the stated ranges. It does not say why.</p>
<p class="meta">Sources: Congressional Budget Office reports, the US-CBO eval-projections data (actuals.csv, actual_GDP.csv) and the US-CBO cbo-data economic vintages. IMF World Economic Outlook, chapter 1 of each issue. All read without a key. Generated %s. Heuremen LLC.</p>
<p class="meta">The newest run is always in <a href="/seldon/live.json">/seldon/live.json</a>.</p>
<p class="meta">Plan and code for this page are public: <a href="https://github.com/indahl-ai/indahl.ai/tree/main/code/seldon">seldon</a>. The plan was fixed before the comparison it describes.</p>
<p class="meta">Data read from: <a href="https://www.cbo.gov/publication/61067">CBO deficit and debt ranges</a> &middot; <a href="https://github.com/US-CBO/eval-projections">US-CBO eval-projections</a> &middot; <a href="https://github.com/US-CBO/cbo-data">US-CBO cbo-data</a> &middot; <a href="https://www.cbo.gov/data/budget-economic-data">CBO budget and economic data</a> &middot; <a href="https://www.imf.org/en/publications/weo">IMF World Economic Outlook</a>.</p>
<p class="meta">Named here and want to answer a row? <a href="/respond?u=seldon-all">Respond</a></p>
<section id="replies" data-prefix="seldon"></section><script src="/replies.js" defer></script>''' % (
    e(' &middot; '.join(S['labels'])).replace('&amp;middot;', '&middot;'), gate_line, cell_rows(), e(debt_line), range_rows(S['ranges']), range_rows(S['short_ranges']),
    im['statements'], im['resolved'], im['held'], imf_rows(), e(held_line), len(S['ranges']) + len(S['short_ranges']), e(S['generated'][:10]))
TITLE = 'SELDON | Long-range budget and growth ranges against outcomes | Heuremen LLC'
DESC = 'SELDON: the two-thirds ranges the Congressional Budget Office printed for the deficit, debt and growth years ahead, set beside the outcomes, with a report block bootstrap interval against the stated two-thirds.'
page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="https://indahl.ai/seldon">
<meta name="author" content="Heuremen LLC">
<link rel="stylesheet" href="/style.css">
<style>.tw{overflow-x:auto}table.bench{border-collapse:collapse;font-size:.86rem}table.bench th,table.bench td{padding:.3rem .55rem;border-bottom:1px solid #ccc;text-align:left;white-space:nowrap}</style>
</head>
<body>
<header class="top"><div class="wrap bar"><a class="brand" href="/"><span>Heuremen LLC</span></a></div></header>
<section class="hero slim"><div class="wrap"><h1><b class="ac">SELDON</b> &middot; Long-range budget and growth ranges against outcomes</h1></div></section>
<main class="wrap">%s</main>
</body>
</html>
''' % (e(TITLE), e(DESC), body)
open('seldon.html', 'w').write(page); print('seldon.html', len(page))
