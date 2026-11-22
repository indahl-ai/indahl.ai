#!/usr/bin/env python3
"""build_page.py: writes zeus.html, the desk's page draft, from summary_zeus.json. Reads no network. The live page is built by the site build
(indahl-ai/build_site.py), which takes the body from this file, as for TORNADO."""
import json, os, sys, html, time
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
from zeus_headline import headline, W as Wd, pc, day
S = json.load(open('summary_zeus.json')); e = html.escape
Z = S['zeus']; F = S['frame']; G = S['gates']
def num(x): return '{:,}'.format(int(x))
def cell_rows():
    out = []
    for lab, c in (('25 statute miles, borrowed (headline)', Z['tstm_hit_share']), ('10 statute miles (secondary)', Z['tstm_hit_share_10mi'])):
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s to %s</td><td>%s</td></tr>' % (
            e(lab), num(c['thunder_point_days']), num(c['hit_point_days']), pc(c['value']), pc(c['lo']), pc(c['hi']), e(Wd(c))))
    o = Z['flash_outside_share']
    return ('<div class="tw"><table class="bench"><thead><tr><th>Radius</th><th>Thunder-area point-days</th><th>With a flash in the radius</th><th>Share, percent</th><th>95% interval, percent</th>'
            '<th>Reading against 10 percent or more</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>'
            '<p>Flashes over the domain in the valid periods: %s. Beyond 25 statute miles of every thunder area: %s, or %s percent (day block bootstrap 95%% interval %s to %s percent). SPC makes no statement about lightning outside its lines, so this share carries no reading.</p>' % (num(o['flashes']), num(o['outside']), pc(o['value']), pc(o['lo']), pc(o['hi'])))
def day_rows():
    out = []
    for r in S['days']:
        sh = (r['hit_points_primary'] / r['thunder_points']) if r['thunder_points'] else None
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            day(r['day']), num(r['thunder_points']), num(r['hit_points_primary']), pc(sh), num(r['hit_points_secondary']), num(r['flashes_primary']), num(r['flashes_outside_primary'])))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Outlook day</th><th>Thunder-area points</th><th>Flash within 25 miles</th><th>Share, percent</th><th>Flash within 10 miles</th>'
            '<th>Flashes over the domain</th><th>Beyond 25 miles of every thunder area</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>')
HL_BIG, HL_LINE = headline(S)
hl = '<section id="hl-slot" class="hl-slot hl"><div class="hl-big">%s</div><p class="hl-line">%s</p></section>' % (e(HL_BIG), e(HL_LINE))
gate_line = 'All known-good checks passed on this run.' if G['passed'] else 'A known-good check did not pass on this run, so every reading shows cannot tell.'
held = S['held']
held_line = ('Held, listed by date and left out of every cell: ' + ', '.join('%s (%s)' % (day(h['day']), h['why']) for h in held) + '.') if held else 'No day in the window was held.'
body = hl + '''<p class="meta crumb">Division: <a href="/hermes">HERMES</a></p>
<p class="meta">%s</p>
<h2>When the Storm Prediction Center draws a thunder line, how often does lightning strike inside it?</h2>
<p>Each Day 1 Convective Outlook from the NOAA Storm Prediction Center carries an unlabeled thunder line. The Center’s product page says the line &ldquo;depicts, to the right of the line,&rdquo; &ldquo;a 10%% or higher probability of thunderstorms during the valid period.&rdquo; NWS Instruction 10-512 says the outlooks &ldquo;define areas where there is a 10%% or greater probability of&rdquo; &ldquo;(general) thunderstorms.&rdquo; Neither names a radius for thunder. The only radius in either is for severe weather, 25 statute miles of a point. This page borrows that radius and prints a fixed second radius of 10 statute miles beside it.</p>
<p>The lightning is the flash record of the Geostationary Lightning Mapper on GOES-19 (east of 106.2 degrees west) and GOES-18 (west of it), from NOAA open data. NOAA states a 70 percent flash detection requirement and a measured 81 percent for GOES-18 in 2023, lower toward the edge of the view. No published figure for GOES-19 was found. A missed flash can only lower the share, so the share is a floor. GLM also counts all lightning it sees from orbit, in-cloud and cloud-to-ground alike, while a thunderstorm forecast is about thunder heard at the ground. That difference is stated here and not measured.</p>
<p>The outlook is the 1300 UTC issuance, valid from 1300 UTC to 1200 UTC the next day. The thunder area is the general thunder polygon with every higher category inside it. Points sit every 0.1 degree over the 48 contiguous states and the coastal waters within 25 statute miles of them, %s points in all. A point counts as struck when at least one flash with the product’s good quality flag fell within the radius during the valid period. The interval comes from a bootstrap that draws whole outlook days, so points on one day stay together. The plan, with the frame, the headline cell and the outcome rule, was fixed and committed before any outlook was set beside a flash. %s</p>
<h2>The window</h2>
<p>Outlooks issued from %s to %s, a 30-day window in late autumn, the low lightning season over the contiguous states. %s days read.</p>
%s
<p class="bench-note">Reading: SPC states 10 percent or more, a floor. Consistent if the whole 95%% interval is at or above 10 percent, below if the whole interval is under it, otherwise cannot tell with the reason. Above cannot occur against a floor. The share of flashes beyond the radius of every thunder area has no stated figure and carries no reading. A point-day is one grid point on one outlook day.</p>
<h2>Day by day</h2>
%s
<h2>Nothing returned</h2>
<p>%s A day with no 1300 UTC outlook in the archive, or with a gap of more than one hour in either satellite’s files in the valid period, is held and never filled in. Flashes without the good quality flag, counted and left out: %s.</p>
<h2>What this page holds and what it leaves out</h2>
<p>Left out: the other Day 1 issuances, the Day 2 and Day 3 outlooks, the severe probabilities, and years before this window. A years-long reading would be a later addendum. A reading says how often lightning struck where the line was drawn. It does not say why.</p>
<p class="meta">Sources: NOAA Storm Prediction Center Day 1 Convective Outlooks as kept by the Iowa Environmental Mesonet, Iowa State University. GOES-19 and GOES-18 Geostationary Lightning Mapper Level 2 flash files, NOAA Open Data Dissemination on AWS. US Census state boundaries. All read without a key. Generated %s. Heuremen LLC.</p>
<p class="meta">The newest run is always in <a href="/zeus/live.json">/zeus/live.json</a>.</p>
<p class="meta">Plan and code for this page are public: <a href="https://github.com/indahl-ai/indahl.ai/tree/main/code/zeus">zeus</a>. The plan was fixed before the comparison it describes.</p>
<p class="meta">Data read from: <a href="https://www.spc.noaa.gov/misc/SPC_probotlk_info.html">SPC outlook product page</a> &middot; <a href="https://www.weather.gov/media/directives/010_pdfs/pd01005012curr.pdf">NWSI 10-512</a> &middot; <a href="https://mesonet.agron.iastate.edu/request/gis/outlooks.phtml">Iowa Environmental Mesonet outlook archive</a> &middot; <a href="https://registry.opendata.aws/noaa-goes/">NOAA GOES on AWS</a> &middot; <a href="https://www.noaasis.noaa.gov/pdf/ps-pvr/goes18/GLM/Full/GOES18_GLM_PPG_20231117.pdf">GOES-18 GLM performance guide</a>.</p>
<p class="meta">Named here and want to answer a row? <a href="/respond?u=zeus-all">Respond</a></p>
<section id="replies" data-prefix="zeus"></section><script src="/replies.js" defer></script>''' % (
    e(' &middot; '.join(S['labels'])).replace('&amp;middot;', '&middot;'), num(F['domain_points']), gate_line, day(F['window'][0]), day(F['window'][1]), num(S['days_read']), cell_rows(), day_rows(),
    held_line, num(sum(sum(r['qf_dropped'].values()) for r in S['days'])), e(S['generated'][:10]))
TITLE = 'ZEUS | Thunderstorm outlooks against the lightning that struck | Heuremen LLC'
DESC = 'ZEUS: the Storm Prediction Center Day 1 general thunder area set beside GOES Geostationary Lightning Mapper flashes, with a day block bootstrap interval against the stated 10 percent.'
page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="https://indahl.ai/zeus">
<meta name="author" content="Heuremen LLC">
<link rel="stylesheet" href="/style.css">
<style>.tw{overflow-x:auto}table.bench{border-collapse:collapse;font-size:.86rem}table.bench th,table.bench td{padding:.3rem .55rem;border-bottom:1px solid #ccc;text-align:left;white-space:nowrap}</style>
</head>
<body>
<header class="top"><div class="wrap bar"><a class="brand" href="/"><span>Heuremen LLC</span></a></div></header>
<section class="hero slim"><div class="wrap"><h1><b class="ac">ZEUS</b> &middot; Thunderstorm outlooks against the lightning that struck</h1></div></section>
<main class="wrap">%s</main>
</body>
</html>
''' % (e(TITLE), e(DESC), body)
open('zeus.html', 'w').write(page); print('zeus.html', len(page))
