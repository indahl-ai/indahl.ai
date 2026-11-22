#!/usr/bin/env python3
"""build_page.py: writes prometheus.html, the desk's page draft, from summary_prometheus.json. Reads no network. The live page is built by the site build
(indahl-ai/build_site.py), which takes the body from this file, as for TORNADO."""
import json, os, sys, html
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
from prometheus_headline import headline, W as Wd, pc
S = json.load(open('summary_prometheus.json')); e = html.escape
F = S['frame']; N = S['counts']
def num(x): return '{:,}'.format(int(x))
ROWNAME = {'first month': 'first month', 'months two to four': 'months two to four'}
def cell_rows():
    out = []
    for c in S['cells']:
        lab = '%s, %s, %s acres or more, %s%s' % (c['rating'], c['counts'], num(c['acres']), c['months'], ' (headline)' if c['headline'] else '')
        iv = '%s to %s' % (pc(c['lo']), pc(c['hi'])) if c['lo'] is not None else 'not formed'
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            e(lab), num(c['psa_months']), num(c['exceeded']), pc(c['value']) or 'none', iv, e(Wd(c))))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Cell</th><th>Rated area-months</th><th>Meeting the cell</th><th>Share, percent</th>'
            '<th>95% interval, percent</th><th>Reading against more than half</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>')
def issue_rows():
    out = []
    for r in S['issues']:
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (e(r['issue']), e(r['status'].replace('_', ' ').lower()),
                   e(', '.join(r.get('member_kinds', [])) or 'none'), e(r['why'])))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Issue</th><th>Status</th><th>File kinds in the archive ZIP</th><th>Why</th></tr></thead><tbody>'
            + ''.join(out) + '</tbody></table></div>')
HL_BIG, HL_LINE = headline(S)
hl = '<section id="hl-slot" class="hl-slot hl"><div class="hl-big">%s</div><p class="hl-line">%s</p></section>' % (e(HL_BIG), e(HL_LINE))
body = hl + '''<p class="meta crumb">Division: <a href="/hermes">HERMES</a></p>
<p class="meta">%s</p>
<h2>When the national wildfire outlook rates an area above normal, do more large fires follow?</h2>
<p>Each month the National Interagency Fire Center publishes the Significant Wildland Fire Potential Outlook. The National Interagency Mobilization Guide 2026, chapter 60, says &ldquo;The Outlook identifies areas where significant wildland fire activity is expected to be above or below normal levels&rdquo; and &ldquo;covers a four-month period, divided into four one-month sections.&rdquo; Its unit is the Predictive Services Area. The NWCG mapping service describes a &ldquo;Forecast of significant fire potential by predictive service area (PSA)&rdquo;.</p>
<p>No numeric definition of above normal was found in the guide, the Predictive Services handbook, the outlooks page or the current outlook. The outlook states a direction and no number. This run reads above normal as a claim that an area-month has more large fires than its usual count more than half of the time, where the usual count is the median for that area and calendar month. That reading is the run&rsquo;s, not NIFC&rsquo;s, and it was fixed in the plan before any record was read.</p>
<h2>The frame, fixed before any outlook or fire record was read</h2>
<p>Every outlook issued from January 2023 to December 2025, %s issues, first month only, months two to four as a secondary reading. The unit is the Predictive Services Area and calendar month, rated above normal, normal or below normal. A large fire is one of 100 acres or more by final reported size, the lower threshold of the National Interagency Coordination Center, applied to all fuels, with 300 acres as a secondary reading. The usual count is the median count of large fires for that area and calendar month over 2001 to 2020 in the Fire Program Analysis fire-occurrence database, 6th edition. Outcome years come from the WFIGS wildland fire locations. The interval is a 95 percent block bootstrap by outlook issue, since areas in one issue share one weather pattern.</p>
<p>The ratings are read from the area polygons in NIFC&rsquo;s monthly archive, one ZIP per issue. An issue whose ZIP holds no area polygons is held and listed, never redrawn from a map image.</p>
<h2>The reading</h2>
<p>%s</p>
%s
<p class="bench-note">Reading: consistent if the whole 95 percent interval is above one half, below if the whole interval is at or below one half, otherwise cannot tell with the reason. Above cannot occur against a direction claim. An area-month is one Predictive Services Area in one calendar month.</p>
<h2>Issue by issue</h2>
<p>Held: %s. Nothing returned: %s. Read: %s. Months with no outlook while staff were off duty: none in the frame, since the archive lists an issue for every month.</p>
%s
<h2>What this page holds and what it leaves out</h2>
<p>Carried with every result: the baseline and the outcome years come from two databases, and the run counts both in 2020 and prints the difference once both are read. Above normal has no stated number. The 100-acre threshold ignores fuel type. NWCG says the fire records may be incomplete. The fire records were not read on this run, since no rated area-month was formed to set them beside. A reading says how often large fires came where a rating was drawn. It does not say why.</p>
<p class="meta">Sources: National Interagency Fire Center outlooks page and monthly outlook archive, National Interagency Mobilization Guide 2026, National Interagency Predictive Services Handbook 2023, NWCG Outlooks_Monthly_Extended map service. Read without a key. Generated %s. Heuremen LLC.</p>
<p class="meta">The newest run is always in <a href="/prometheus/live.json">/prometheus/live.json</a>.</p>
<p class="meta">Plan and code for this page are public: <a href="https://github.com/indahl-ai/indahl.ai/tree/main/code/prometheus">prometheus</a>. The plan was fixed before the comparison it describes.</p>
<p class="meta">Data read from: <a href="https://www.nifc.gov/nicc/predictive-services/outlooks">NIFC outlooks and archive</a> &middot; <a href="https://www.nifc.gov/sites/default/files/NICC/3-Logistics/Reference%%20Documents/Mob%%20Guide/2026/2026%%20Chapter%%2060.pdf">Mobilization Guide 2026, chapter 60</a> &middot; <a href="https://fsapps.nwcg.gov/psp/rest/services/npsg/Outlooks_Monthly_Extended/MapServer">NWCG outlook map service</a> &middot; <a href="https://www.fs.usda.gov/rds/archive/products/RDS-2013-0009.6/_metadata_RDS-2013-0009.6.html">FPA FOD 6th edition</a> &middot; <a href="https://data-nifc.opendata.arcgis.com/">NIFC Open Data</a>.</p>''' % (
    e(' · '.join(S['labels'])), num(F['frame_issues']), e(F['why_not_met'] if not F['met'] else ''), cell_rows(),
    num(N['held']), num(N['nothing_returned']), num(N['read']), issue_rows(), e(S['generated'][:10]))
TITLE = 'PROMETHEUS | Wildfire outlooks against the large fires that followed | Heuremen LLC'
DESC = 'PROMETHEUS: the NIFC Significant Wildland Fire Potential Outlook by Predictive Services Area, set beside the large fires that followed, read against more than half.'
page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="https://indahl.ai/prometheus">
<meta name="author" content="Heuremen LLC">
<link rel="stylesheet" href="/style.css">
<style>.tw{overflow-x:auto}table.bench{border-collapse:collapse;font-size:.86rem}table.bench th,table.bench td{padding:.3rem .55rem;border-bottom:1px solid #ccc;text-align:left}</style>
</head>
<body>
<header class="top"><div class="wrap bar"><a class="brand" href="/"><span>Heuremen LLC</span></a></div></header>
<section class="hero slim"><div class="wrap"><h1><b class="ac">PROMETHEUS</b> &middot; Wildfire outlooks against the large fires that followed</h1></div></section>
<main class="wrap">%s</main>
</body>
</html>
''' % (e(TITLE), e(DESC), body)
open('prometheus.html', 'w').write(page); print('prometheus.html', len(page))
