#!/usr/bin/env python3
"""build_page.py: writes cassandra.html, the desk's page draft, from summary_cassandra.json. Reads no network. The live page is built by the site build,
which takes the body from this file."""
import json, os, sys, html
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
from cassandra_headline import headline
S = json.load(open('summary_cassandra.json'))
e = html.escape
WORD = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell', None: ''}
def Wd(c): return WORD[c.get('outcome')] + (' (%s)' % c['reason'] if c.get('reason') else '')
def pc(x, d=1): return '' if x is None else ('%.' + str(d) + 'f') % (100 * x)
def num(x): return '{:,}'.format(int(x))
def iv(c): return '%s to %s' % (pc(c['lo']), pc(c['hi'])) if c.get('lo') is not None else ''
X = S['cassandra']; F = S['frame']; SR = S['sources']; G = S['gates']
ffw, lsr, wd, wdl = X['ffw_hit_share'], X['ffw_hit_share_lsr'], X['flood_warned_share'], X['flood_warned_share_lsr']
y0, y1 = F['window']
HL_BIG, HL_LINE = headline(S)
hl = '<section id="hl-slot" class="hl-slot hl"><div class="hl-big">%s</div><p class="hl-line">%s</p></section>' % (e(HL_BIG), e(HL_LINE))
gate_line = 'All known-good checks passed on this run.' if G['passed'] else 'A known-good check did not pass on this run, so every reading shows cannot tell.'
def held_text(c):
    h = c['held_years']
    return 'none' if not h else ', '.join('%s (%s)' % (y, ', '.join(v)) for y, v in sorted(h.items()))
def hit_row(name, c):
    return '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (e(name), num(c['warnings']), num(c['hits']), pc(c['value']), iv(c), Wd(c))
def warned_row(name, c):
    return '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (e(name), num(c['reports']), num(c['warned']), pc(c['value']), iv(c), Wd(c))
def year_rows():
    out = []; L = {y['year']: y for y in lsr['years']}
    for y in ffw['years']:
        l = L.get(y['year'], {})
        if 'held' in y: out.append('<tr><td>%d</td><td colspan="4">held: %s</td>' % (y['year'], e(', '.join(y['held']))))
        else: out.append('<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % (y['year'], num(y['warnings']), pc(y['value']), iv(y), Wd(y)))
        out.append('<td>%s</td><td>%s</td></tr>' % (('held' if 'held' in l else pc(l.get('value'))), ('' if 'held' in l else Wd(l))))
    return ''.join(out)
def held_counts(d):
    t = {}
    for v in d.values():
        for k, n in v.items(): t[k] = t.get(k, 0) + n
    return ', '.join('%s %s' % (num(n), k) for k, n in sorted(t.items())) or 'none'
TH_HIT = '<thead><tr><th>Reports read</th><th>Warnings</th><th>Followed by a report</th><th>Share, percent</th><th>95% interval, percent</th><th>Reading against 50 percent or more</th></tr></thead>'
TH_W = '<thead><tr><th>Reports read</th><th>Reports with a time and place</th><th>Inside a warning in force</th><th>Share, percent</th><th>95% interval, percent</th><th>Reading against 50 percent or more</th></tr></thead>'
body = hl + '''<p class="meta crumb">Division: <a href="/hermes">HERMES</a></p>
<p class="meta"><b>%s</b> Every share on this page counts %s.</p>
<h2>When a flash flood warning goes out, does a flood report follow?</h2>
<p>The National Weather Service directive on hydrologic products, NWSI 10-922, says: &ldquo;Flash flood warnings are issued when flooding is imminent or likely.&rdquo; Each warning carries its own polygon and its own expiry time, so each one states a place and a window. This page counts every flash flood warning issued from %d to %d, hits and misses alike, and asks whether a flash flood report followed inside the polygon before the warning expired. No warning is chosen.</p>
<p>The directive gives &ldquo;likely&rdquo; no number. This page reads it at its weakest plain meaning, more often than not, a share of 50 percent. That reading is the page&rsquo;s own, fixed in the plan before any data was read, and not the National Weather Service&rsquo;s. The share is a measurement first. The reading against 50 percent sits beside it.</p>
<p>The outcome is a report, not a flood. A flood in an empty place may go unreported and counts as a miss. Reporting effort may rise while a warning is out, which can raise the share. Neither effect is measured here. %s</p>
<h2>The headline cell</h2>
<p>Every flash flood warning in the window against the NCEI Storm Events record, the official record of flash flood events. A warning counts as followed when at least one flash flood event began inside its issuance polygon at or after the issue time and at or before the final expiry, extensions with the same event number included.</p>
<div class="tw"><table class="bench">%s<tbody>%s</tbody></table></div>
<p class="bench-note">%s Reading: consistent if the whole 95%% interval is at or above 50 percent, below if the whole interval is under 50 percent, otherwise cannot tell with the reason STRADDLES_EDGE. Above cannot occur against a floor. The interval is a block bootstrap that draws whole blocks of one forecast office in one year, %s resamples, so warnings from one office in one event stay together. No size that matters is named, so the both-alternatives test is not applied. Years held from this cell: %s.</p>
<h2>The same warnings against local storm reports</h2>
<p>The Iowa Environmental Mesonet keeps the Local Storm Reports the forecast offices send, and labels the archive not complete or official. The same warnings, read against its flash flood reports by the same rule. The two report sources are read apart and never merged. This cell is secondary and decides nothing.</p>
<div class="tw"><table class="bench">%s<tbody>%s</tbody></table></div>
<p class="bench-note">Years held from this cell: %s.</p>
<h2>Floods that came without a warning</h2>
<p>The other direction: of the flash flood reports in the window that carry a time and a place, the share that fell inside the polygon of a warning in force at the report time. This cell is secondary and decides nothing. The local storm report row is display only.</p>
<div class="tw"><table class="bench">%s<tbody>%s%s</tbody></table></div>
<p class="bench-note">Storm Events reports held for time or place: %s. Local storm reports held: %s. The block here is the forecast office named in the report and the year.</p>
<h2>Year by year</h2>
<p>Each year&rsquo;s warnings by the same rule. These rows are shown and are not in the headline.</p>
<div class="tw"><table class="bench"><thead><tr><th>Year</th><th>Warnings</th><th>Followed by a Storm Events report, percent</th><th>95%% interval, percent</th><th>Reading</th><th>Followed by a local storm report, percent</th><th>Reading</th></tr></thead><tbody>%s</tbody></table></div>
<h2>Nothing returned and held</h2>
<p>Counted apart and never folded into a reading. A year is held from a cell when the warning file or that cell&rsquo;s report file for the year could not be read, or when either holds no record at all for some month of the year. Held years are left out and never filled in. Warnings whose polygon or time could not be read: %s. Rows for the same warning more than once in the file, the earliest kept: %s. Warnings whose final expiry is later than the first stated expiry, an extension with the same event number: %s. Warnings issued in 2007, read only so a report early on 1 January 2008 can find the warning in force: %s.</p>
<h2>What this page holds and what it leaves out</h2>
<p>Held: every storm-based flash flood warning in the archive issued from 1 January %d to 31 December %d, in any state or territory, each with its issuance polygon held to the final expiry. Polygons redrawn in follow-up statements are not read. Left out: flash flood watches, areal flood warnings, river flood warnings and warnings before %d. Warning polygons before October 2007 were experimental, and the window starts after them. A reading says how often a report followed a warning. It does not say why.</p>
<p class="meta">Sources: storm-based Flash Flood Warnings as kept by the Iowa Environmental Mesonet, Iowa State University. NCEI Storm Events. Iowa Environmental Mesonet Local Storm Reports. All read without a key, one request at a time. Generated %s. Heuremen LLC.</p>
<p class="meta">The newest run is always in <a href="/cassandra/live.json">/cassandra/live.json</a>.</p>
<p class="meta">Plan and code for this page are public: <a href="https://github.com/indahl-ai/indahl.ai/tree/main/code/cassandra">cassandra</a>. The plan was fixed before the comparison it describes.</p>
<p class="meta">Data read from: <a href="https://mesonet.agron.iastate.edu/request/gis/watchwarn.phtml">Iowa Environmental Mesonet warning archive</a> &middot; <a href="https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/">NCEI Storm Events files</a> &middot; <a href="https://mesonet.agron.iastate.edu/request/gis/lsrs.phtml">Iowa Environmental Mesonet storm reports</a> &middot; <a href="https://www.weather.gov/media/directives/010_pdfs/pd01009022curr.pdf">NWSI 10-922</a>.</p>
<p class="meta">Named here and want to answer a row? <a href="/respond?u=cassandra-all">Respond</a></p>
<section id="replies" data-prefix="cassandra"></section><script src="/replies.js" defer></script>''' % (
    e(S['label']), e(S['carrier']), y0, y1, gate_line,
    TH_HIT, hit_row('NCEI Storm Events', ffw), 'Beside the reading: ' + S['req13']['line'], num(F['bootstrap']['resamples']), e(held_text(ffw)),
    TH_HIT, hit_row('Local Storm Reports', lsr), e(held_text(lsr)),
    TH_W, warned_row('NCEI Storm Events', wd), warned_row('Local Storm Reports', wdl), held_counts(SR['stormevents_held']), held_counts(SR['lsr_held']),
    year_rows(),
    num(len(SR['warnings_unreadable'])), num(SR['warnings_duplicate_rows']), num(SR['warnings_extended']), num(SR['warnings_context_2007']),
    y0, y1, y0, e(S['generated'][:10]))
TITLE = 'CASSANDRA | Warnings against what followed | Heuremen LLC'
DESC = 'CASSANDRA: every flash flood warning from 2008 to 2025 set beside the flash flood reports inside its polygon before it expired, every warning counted, none chosen.'
page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="https://indahl.ai/cassandra">
<meta name="author" content="Heuremen LLC">
<link rel="stylesheet" href="/style.css">
<style>.tw{overflow-x:auto}table.bench{border-collapse:collapse;font-size:.86rem}table.bench th,table.bench td{padding:.3rem .55rem;border-bottom:1px solid #ccc;text-align:left;white-space:nowrap}</style>
</head>
<body>
<header class="top"><div class="wrap bar"><a class="brand" href="/"><span>Heuremen LLC</span></a></div></header>
<section class="hero slim"><div class="wrap"><h1><b class="ac">CASSANDRA</b> &middot; Warnings against what followed</h1></div></section>
<main class="wrap">%s</main>
</body>
</html>
''' % (e(TITLE), e(DESC), body)
open('cassandra.html', 'w').write(page); print('cassandra.html', len(page))
