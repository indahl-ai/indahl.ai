#!/usr/bin/env python3
"""build_page.py: writes ares.html, the desk's page draft, from summary_ares.json. Reads no network. The live page is built by the site build
(indahl-ai/build_site.py), which takes the body from this file, as for TORNADO and PROMETHEUS.

The map is dots only (PLAN.md section 4 and section 0): one dot per province-month at the province label point of the boundary file, area by
active_days, solid where both trackers agree, hollow where one tracker only. No borders, no country fills, no flags. Positions are written as page
pixels only, never as coordinates. The hard lines are checked by ares_lines.assert_page before the file is written."""
import html, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import ares_lines as L
from ares_headline import headline, mname, pc
S = json.load(open('summary_ares.json')); e = html.escape
F = S['frame']; N = S['counts']; A = S['ares']; SRC = S['sources']
NE = json.load(open('data/ne_admin1_props.json'))['rows']
def num(x): return '{:,}'.format(int(x))
def q(s): return '<q class="pl">%s</q>' % e(s) if s else ''

# ---- label point of each province unit (mean of the boundary file label points of the rows in the unit), as page pixels
UNIT = {}
for r in NE:
    k = 'F:' + r['fips'] if r.get('fips') else 'N:' + r['adm1_code']
    UNIT.setdefault(k, []).append((r['label_x'], r['label_y']))
W, LAT0, LAT1 = 960, 78.0, -56.0
HT = round(W * (LAT0 - LAT1) / 360)
def px(key):
    pts = UNIT.get(key)
    if not pts: return None
    lon = sum(p[0] for p in pts) / len(pts); lat = sum(p[1] for p in pts) / len(pts)
    return round((lon + 180) / 360 * W), round((LAT0 - max(LAT1, min(LAT0, lat))) / (LAT0 - LAT1) * HT)
KIND = {'both trackers': 0, 'UCDP only': 1, 'GDELT only': 2}
dots, unplaced = [], 0
for r in S['rows']:
    p = px(r['province_key'])
    if not p: unplaced += 1; continue
    names = [n for n in (r['ucdp_province'], r['gdelt_province']) if n]
    label = names[0] if len(set(names)) <= 1 else '%s (UCDP), %s (GDELT)' % tuple(names)
    dots.append([p[0], p[1], F['months'].index(r['month']), KIND[r['which']], r['active_days'], label])
MAPDATA = json.dumps(dict(months=[mname(m) for m in F['months']], kinds=['both trackers', 'UCDP only', 'GDELT only'], dots=dots), ensure_ascii=False, separators=(',', ':'))
L.assert_clean(json.loads(MAPDATA), 'map data')
MAP = ('<div class="aresmap"><p><label for="ares-month">Month</label> <select id="ares-month">%s</select></p>'
       '<svg id="ares-svg" viewBox="0 0 %d %d" role="img" aria-label="Dots at province label points, one per province-month with recorded armed violence, no borders drawn">'
       '<rect x="0" y="0" width="%d" height="%d" fill="none" stroke="#ccc"/><g id="ares-dots"></g></svg>'
       '<p class="bench-note">Solid dot: both trackers agree. Hollow dot: one tracker only. Dot area follows active days, from none to every day of the month. '
       'Hover a dot for the province as the source spells it, the month, which trackers, and the active days. No borders or country fills are drawn.</p></div>'
       % (''.join('<option value="%d"%s>%s</option>' % (i, ' selected' if i == len(F['months']) - 1 else '', e(mname(m))) for i, m in enumerate(F['months'])), W, HT, W, HT))
SCRIPT = ('<script type="application/json" id="ares-data">%s</script>\n<script src="/ares-map.js"></script>' % MAPDATA.replace('</', '<\\/'))   # 22 Nov 2026: the site CSP (default-src 'self') blocks inline scripts; the map never drew
open(os.path.expanduser('~/forge/cloudflare-workers/heuremen-door/public/ares-map.js'), 'w').write("(function(){var D=JSON.parse(document.getElementById('ares-data').textContent),g=document.getElementById('ares-dots'),s=document.getElementById('ares-month'),N='http://www.w3.org/2000/svg';\nfunction draw(m){while(g.firstChild)g.removeChild(g.firstChild);D.dots.forEach(function(d){if(d[2]!=m)return;var c=document.createElementNS(N,'circle');c.setAttribute('cx',d[0]);c.setAttribute('cy',d[1]);\nc.setAttribute('r',(2+2.2*Math.sqrt(d[4])).toFixed(1));if(d[3]==0){c.setAttribute('fill','#3b5b7a');c.setAttribute('fill-opacity','0.75');c.setAttribute('stroke','none');}else{c.setAttribute('fill','none');c.setAttribute('stroke','#3b5b7a');c.setAttribute('stroke-width','1.2');}\nvar t=document.createElementNS(N,'title');t.textContent=d[5]+', '+D.months[d[2]]+', '+D.kinds[d[3]]+', active days '+d[4];c.appendChild(t);g.appendChild(c);});}\ns.addEventListener('change',function(){draw(+s.value);});draw(+s.value);})();")


def month_rows():
    out = []
    for b in S['by_month']:
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (e(mname(b['month'])), e(b['release'] or 'held'),
                   num(b['province_months']), num(b['agreed']), num(b['ucdp_only']), num(b['gdelt_only'])))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Month</th><th>UCDP release read</th><th>Province-months</th><th>Both trackers agree</th>'
            '<th>UCDP only</th><th>GDELT only</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>')

def held_tables():
    hu = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (q(h['country']), q(h['adm_1']), num(h['province_months']), e(h['why'])) for h in S['held']['ucdp'])
    hg = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (e(h['code']), q(h['country']), q(h['province']), num(h['province_months']), e(h['why'])) for h in S['held']['gdelt'])
    return ('<details><summary>UCDP place names held</summary><div class="tw"><table class="bench"><thead><tr><th>Country, as UCDP spells it</th><th>First-order unit, as UCDP spells it</th>'
            '<th>Province-months held</th><th>Why</th></tr></thead><tbody>' + hu + '</tbody></table></div></details>'
            '<details><summary>GDELT province codes held</summary><div class="tw"><table class="bench"><thead><tr><th>FIPS code</th><th>Country, as GDELT spells it</th>'
            '<th>First-order unit, as GDELT spells it</th><th>Province-months held</th><th>Why</th></tr></thead><tbody>' + hg + '</tbody></table></div></details>')

HL_BIG, HL_LINE = headline(S)
h = A['agree_share']; uc = SRC['ucdp']; gd = SRC['gdelt']; cw = SRC['crosswalk']; nr = N['nothing_returned']
ged = [f for f in uc['files'] if f['release'].startswith('UCDP GED')]; cand = [f for f in uc['files'] if 'Candidate' in f['release']]
gcount = gd['counts']
hl = '<section id="hl-slot" class="hl-slot hl"><div class="hl-big">%s</div><p class="hl-line">%s</p></section>' % (e(HL_BIG), e(HL_LINE))
body = hl + '''<p class="meta crumb">Division: <a href="/hermes">HERMES</a></p>
<p class="meta">%(labels)s</p>
<h2>Do public conflict trackers agree on where armed violence happened?</h2>
<p>Two public trackers record organized armed violence around the world. The Uppsala Conflict Data Program (UCDP) codes an event as &ldquo;An incident where armed force was used by an organized actor against another organized actor, or against civilians&rdquo;, with at least one registered death at a specific location and a specific date. The GDELT Project codes events from news text by machine, and its Material Conflict class holds the CAMEO root codes for assault, fight and unconventional mass violence.</p>
<p>This page asks two questions for every province and month in the window. Do the trackers agree that organized armed violence happened there? Where they disagree, which tracker recorded it? Each is counted, not explained. A province-month is one first-level administrative unit, such as a province, state, oblast or governorate, in one calendar month.</p>
<h2>The frame, fixed before any data was read</h2>
<p>The window is the trailing twelve complete calendar months that ended at least 30 days before the run, %(w0)s to %(w1)s on this run. UCDP counts a province-month when it holds at least one event of any of its three types, placed at least to the province (where_prec 1 to 4), and in Candidate data with the status Clear. The types are pooled and never printed apart. UCDP GED version 26.1 is read for the months it covers and the Candidate release for the rest, GED first where both exist, since GED is the checked release. GDELT counts a province-month when it holds at least one root event with QuadClass 4 and root code 18, 19 or 20, placed at a world city or a first-order division (ActionGeo_Type 4 or 5), seen in at least two sources. Country-level matches are dropped, since they sit on a centroid.</p>
<p>Places are grouped into provinces through one public first-level boundary file, Natural Earth Admin 1 at 1:10m, which is never drawn. A crosswalk from UCDP&rsquo;s first-order names and GDELT&rsquo;s FIPS 10-4 province codes to that file was sealed before any province-month was counted. A name or code the crosswalk cannot match is held and listed by its source spelling, never guessed.</p>
<p>Dot size is active days: the number of distinct days in the month with at least one UCDP event placed in the province and dated to the exact day. It is not a human-cost figure, it runs from none to every day of the month on every map, and one long day of reporting counts as one day. GDELT days are not used for size, since duplicate stories inflate them.</p>
<h2>The map</h2>
%(map)s
<h2>The reading</h2>
<p>Province-months where either tracker recorded organized armed violence: %(m)s. Both trackers agree: %(n)s, a share of %(share)s percent, with a 95 percent interval of %(lo)s to %(hi)s percent from a block bootstrap by country and month. UCDP only: %(uo)s. GDELT only: %(go)s.</p>
<div class="tw"><table class="bench"><thead><tr><th>Outcome</th><th>Plain words</th><th>Province-months</th></tr></thead><tbody>
<tr><td>CONSISTENT</td><td>both trackers agree</td><td>%(n)s</td></tr>
<tr><td>CANNOT_TELL</td><td>one tracker only, UCDP</td><td>%(uo)s</td></tr>
<tr><td>CANNOT_TELL</td><td>one tracker only, GDELT</td><td>%(go)s</td></tr>
</tbody></table></div>
<p class="bench-note">No tracker states a claim for the other to be read against, so only two of the four outcome words are used. Above and below would need a stated figure, and there is none. One tracker only is cannot tell, with the tracker named.</p>
<h2>Month by month</h2>
%(months)s
<h2>Held and nothing returned</h2>
<p>Months held for a missing UCDP release: %(hm)s. UCDP place names held by the crosswalk: %(hun)s, covering %(hup)s province-months. GDELT province codes held: %(hgn)s, covering %(hgp)s province-months. These are listed below and are not in the counts above. Nothing returned: %(gbp)s GDELT rows with a blank place, %(gcg)s GDELT rows placed only at the country level, %(ubl)s UCDP rows with no first-order name, and %(gnr)s GDELT files that could not be read. Province-months with no place in the boundary file for the map: %(unp)s.</p>
%(held)s
<p>The crosswalk matched UCDP names as follows: %(cwu)s. GDELT codes: %(cwg)s. Every match that is not an exact name or code is listed in the crosswalk in the reproduction kit.</p>
<h2>What this page holds and what it leaves out</h2>
<p>UCDP&rsquo;s line is drawn by deaths: an event enters UCDP only if at least one death is registered. This page reads that as yes or no and never reads, stores or prints the number. GDELT&rsquo;s line is drawn by news reports, and Hammond and Weidmann (2014) found that &ldquo;at the local level major issues of geographic bias exist in how events are reported.&rdquo; As the filter is written, GDELT is read outside the United States only (ActionGeo_Type 4 or 5). Candidate events are preliminary and can change in the yearly GED release.</p>
<p>Left out on purpose: every count of people harmed, every name of a party or side, displacement figures, flags, borders, country fills, coordinates and towns. The finest place on this page is the first-order unit. Place names are quoted as each source spells them. ACLED is left out on its license terms and its account requirement.</p>
<p>A reading says where the trackers agree that violence was recorded. It does not say why they differ.</p>
<p class="meta">Sources: UCDP Georeferenced Event Dataset, version %(gedv)s (sha256 %(gedsha)s), and UCDP Candidate Events Dataset, version %(candv)s (sha256 %(candsha)s), CC BY 4.0, read from <a href="https://ucdp.uu.se/downloads/">ucdp.uu.se/downloads</a>. Cite: Sundberg, Ralph and Erik Melander (2013) Introducing the UCDP Georeferenced Event Dataset, Journal of Peace Research 50(4). Davies, Shawn, Therése Pettersson and Magnus Öberg (2026) Organized violence 1989 to 2025, and violent political protests, Journal of Peace Research, doi:10.1093/jopres/xjag046. Hegre, Håvard, Mihai Croicu, Kristine Eck and Stina Högbladh (2020) Introducing the UCDP Candidate Events Dataset, Research and Politics, doi:10.1177/2053168020935257.</p>
<p class="meta">GDELT 2.0 Event Database, the GDELT Project, <a href="https://www.gdeltproject.org/">www.gdeltproject.org</a>: %(gfr)s of %(gfl)s fifteen-minute event files in the window read, each checked against the MD5 in the master file list, %(gkept)s rows kept after the filter for the year. Boundary file: Natural Earth Admin 1, States and Provinces, 1:10m (public domain), never drawn. Read without a key. Generated %(gen)s. Heuremen LLC.</p>
<p class="meta">The newest run is always in <a href="/ares/live.json">/ares/live.json</a>.</p>
<p class="meta">Plan and code for this page are public: <a href="https://github.com/indahl-ai/indahl.ai/tree/main/code/ares">ares</a>. The plan was fixed before the comparison it describes.</p>
<p class="meta">%(foot)s</p>
%(script)s''' % dict(
    labels=e(' · '.join(S['labels'])), w0=e(mname(F['window'][0])), w1=e(mname(F['window'][1])), map=MAP, m=num(N['province_months']), n=num(N['agreed']),
    share=pc(h['value']) or 'none', lo=pc(h['lo']) or 'none', hi=pc(h['hi']) or 'none', uo=num(N['ucdp_only']), go=num(N['gdelt_only']), months=month_rows(),
    hm=e(', '.join(mname(m) for m in S['held']['months']) or 'none'), hun=num(N['held_ucdp_names']), hup=num(N['held_ucdp_province_months']),
    hgn=num(N['held_gdelt_codes']), hgp=num(N['held_gdelt_province_months']), gbp=num(nr.get('gdelt_blank_place', 0)), gcg=num(nr.get('gdelt_country_general_rows', 0)),
    ubl=num(nr.get('ucdp_blank_adm_1', 0)), gnr=num(nr.get('gdelt_files_not_read', 0)), unp=num(unplaced), held=held_tables(),
    cwu=e(', '.join('%s %s' % (k.replace('_', ' '), num(v)) for k, v in sorted(cw['ucdp_methods'].items()))),
    cwg=e(', '.join('%s %s' % (k.replace('_', ' '), num(v)) for k, v in sorted(cw['gdelt_methods'].items()))),
    gedv=e(ged[0]['version'] if ged else 'not read'), gedsha=e(ged[0]['sha256'][:12] if ged else ''), candv=e(cand[0]['version'] if cand else 'not read'),
    candsha=e(cand[0]['sha256'][:12] if cand else ''), gfr=num(gd['files_read']), gfl=num(gd['files_listed']), gkept=num(gcount.get('rows_kept', 0)),
    gen=e(S['generated'][:10]), foot=e(L.FOOTNOTE), script=SCRIPT)
TITLE = 'ARES | Where public conflict trackers agree | Heuremen LLC'
DESC = 'ARES: for every province and month, whether the UCDP and GDELT public trackers both recorded organized armed violence, and where only one did. No casualty figures, no sides, no borders.'
page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="https://indahl.ai/ares">
<meta name="author" content="Heuremen LLC">
<link rel="stylesheet" href="/style.css">
<style>.tw{overflow-x:auto}table.bench{border-collapse:collapse;font-size:.86rem}table.bench th,table.bench td{padding:.3rem .55rem;border-bottom:1px solid #ccc;text-align:left}q.pl{quotes:none}.aresmap svg{width:100%%;height:auto;background:transparent}</style>
</head>
<body>
<header class="top"><div class="wrap bar"><a class="brand" href="/"><span>Heuremen LLC</span></a></div></header>
<section class="hero slim"><div class="wrap"><h1><b class="ac">ARES</b> &middot; Where public conflict trackers agree</h1></div></section>
<main class="wrap">%s</main>
</body>
</html>
''' % (e(TITLE), e(DESC), body)
main = page.split('<main', 1)[1].split('</main>', 1)[0]
vis = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'(?is)<script.*?</script>', ' ', main))))
L.assert_page(page, vis)
assert ';' not in vis, 'ares: semicolon in page copy'
open('ares.html', 'w').write(page); print('ares.html', len(page), 'dots', len(dots), 'unplaced', unplaced)
