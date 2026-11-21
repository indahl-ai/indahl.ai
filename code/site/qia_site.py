#!/usr/bin/env python3
"""qia_site.py (17 Nov 2026, the owner: "Quantum Idle Audit.com, a straight-up biz page for the corporate emails ... a deck in website form
... clean, and just have links to indahl.ai").

Builds quantumidleaudit.com: a short business site for companies, all measurement and receipts, no physics papers, no names.
Pages go to cloudflare-workers/heuremen-door/public/_qiasite/; the heuremen-door worker serves them when the host is quantumidleaudit.com.
Every link out goes to indahl.ai (the record) or doi.org. No email address anywhere (the site gate refuses them).
PRICES below stays empty until the owner names the numbers; an empty price prints "Quoted per engagement".
Usage: python3 indahl-ai/qia_site.py"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'cloudflare-workers', 'heuremen-door', 'public', '_qiasite')
I = 'https://indahl.ai'
SAMPLE_PDF = '/qia-2026-002.pdf'   # 20 Nov 2026 (the owner): the sample is a calibrated run report; the IBM bill stays on indahl.ai/qia only
SAMPLE_DOI = 'https://doi.org/10.5281/zenodo.23169755'
CONTACT = I + '/contact'
PRICES = {'audit': '$500', 'monitor': '$2,500 a month', 'pilot': '$2,500 for 30 days'}   # 18 Nov 2026: the owner's decided sheet    # the owner's numbers go here, e.g. 'From $X'


def price(k):
    return html.escape(PRICES[k]) if PRICES[k] else 'Quoted per engagement'


CSS = """
:root{--bg:#fbf8f1;--fg:#1a1208;--mute:#5a4830;--line:#e2d7bf;--soft:#f4ecdb;--ink:#1a1208;--ink2:#2a1f0e;--gold:#806012;--gold2:#c8902a;--on:#fbf8f1;--card:#fffdf8;--fez:#806012;--phx:#2a6f73}
@media (prefers-color-scheme:dark){:root{--bg:#14100a;--fg:#f3ead6;--mute:#bfae8c;--line:#3a2f20;--soft:#1c160e;--ink:#f3ead6;--ink2:#ffffff;--gold:#d9a548;--gold2:#e6bc6a;--on:#14100a;--card:#1a140c;--fez:#d9a548;--phx:#6cc3c7;color-scheme:dark}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
h1,h2,h3{font-family:Lora,Georgia,"Times New Roman",serif;font-weight:600}
.eyebrow,.k,.brand,.tag,.out b,ol.steps li::before{font-family:Cinzel,Georgia,serif}
a{color:var(--ink)}
.wrap{max-width:1040px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left));padding-right:max(20px,env(safe-area-inset-right))}
header{border-bottom:1px solid var(--line)}
header .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:18px;flex-wrap:wrap}
.brand{display:inline-flex;align-items:center;gap:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:15px;color:var(--fg);text-decoration:none}
.brand svg{width:30px;height:30px;color:var(--gold)}
.brand small{display:block;font-size:10px;letter-spacing:.22em;color:var(--mute);font-weight:400}
nav a{color:var(--mute);text-decoration:none;font-size:14px;margin-left:22px;white-space:nowrap;display:inline-block}
nav a:hover,nav a[aria-current]{color:var(--fg)}
.hero{padding-block:44px 32px}
.eyebrow{font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);font-weight:600;margin:0 0 18px}
h1{font-size:clamp(30px,4.4vw,46px);line-height:1.14;letter-spacing:-.01em;margin:0 0 20px;max-width:30ch;text-wrap:balance}
.lede{font-size:clamp(17px,2vw,20px);color:var(--mute);max-width:60ch;margin:0 0 34px}
.btns{display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-block;padding:13px 22px;border-radius:6px;font-weight:600;font-size:15px;text-decoration:none;background:var(--ink);color:var(--on);border:1px solid var(--ink)}
.btn:hover{background:var(--ink2);border-color:var(--ink2)}
.btn.ghost{background:transparent;color:var(--ink)}
section{padding-block:40px;border-top:1px solid var(--line)}
section.soft{background:var(--soft)}
h2{font-size:clamp(22px,2.8vw,30px);letter-spacing:-.01em;margin:0 0 10px;text-wrap:balance}
.sub{color:var(--mute);margin:0 0 34px;max-width:62ch}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px}
.card{border:1px solid var(--line);border-radius:10px;padding:26px;background:var(--card);min-width:0}
.card h3{font-size:17px;margin:0 0 8px}
.card p{margin:0;color:var(--mute);font-size:15px}
.card .price{margin-top:18px;font-weight:600;color:var(--fg);font-size:15px}
.card .k{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:600;margin:0 0 12px}
.report{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:36px;align-items:center}
.sheet{border:1px solid var(--line);border-radius:10px;background:var(--card);padding:26px;font-size:14px}
.sheet .row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;padding:9px 0;border-bottom:1px solid var(--line)}
.sheet .row:last-child{border-bottom:0}
.sheet .row span:last-child{font-variant-numeric:tabular-nums;color:var(--mute);text-align:right}
.tag{display:inline-block;font-size:11.5px;letter-spacing:.1em;font-weight:700;padding:2px 8px;border-radius:4px;border:1px solid currentColor}
.out{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.out div{border:1px solid var(--line);border-radius:10px;padding:18px;background:var(--card)}
.out b{display:block;font-size:13px;letter-spacing:.12em;margin-bottom:6px}
.out p{margin:0;color:var(--mute);font-size:14px}
ol.steps{list-style:none;counter-reset:s;padding:0;margin:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
ol.steps li{counter-increment:s;min-width:0}
ol.steps li::before{content:counter(s,decimal-leading-zero);display:block;font-weight:700;color:var(--gold);font-size:13px;letter-spacing:.1em;margin-bottom:8px}
ol.steps b{display:block;margin-bottom:4px}
ol.steps span{color:var(--mute);font-size:15px}
.prose{max-width:68ch}
.prose h3{font-size:18px;margin:34px 0 8px}
.prose p,.prose li{color:var(--fg)}
.prose ul{padding-left:20px}
.band{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}
.band p{margin:0;color:var(--mute);max-width:56ch}
footer{border-top:1px solid var(--line);padding-block:40px;color:var(--mute);font-size:14px}
footer .cols{display:grid;grid-template-columns:minmax(0,1.4fr) repeat(2,minmax(0,1fr));gap:28px}
footer ul{list-style:none;padding:0;margin:0}
footer li{margin:0 0 8px}
footer a{color:var(--mute)}
footer .fine{margin-top:28px;font-size:12.5px}
.herogrid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:48px;align-items:center}
figure.fig{margin:0;border:1px solid var(--line);border-radius:12px;background:var(--card);padding:18px 18px 14px}
figure.fig svg{display:block;width:100%;height:auto}
figure.fig .figt{font-weight:600;margin:0 0 6px;font-size:14px}
figure.fig figcaption{font-size:12.5px;color:var(--mute);margin-top:8px;line-height:1.5}
.legend{display:flex;gap:18px;flex-wrap:wrap;font-size:12.5px;color:var(--mute);margin:2px 0 6px}
.legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:middle}
.cover{display:block;border:1px solid var(--line);border-radius:6px;box-shadow:0 18px 40px -22px rgba(42,31,14,.45);max-width:100%;height:auto;background:#fff}
.rule{height:1px;background:linear-gradient(90deg,var(--gold2),transparent);border:0;margin:0 0 18px;width:120px}
@media (max-width:820px){.herogrid{grid-template-columns:minmax(0,1fr)}.grid,.report,footer .cols{grid-template-columns:minmax(0,1fr)}.out,ol.steps{grid-template-columns:repeat(2,minmax(0,1fr))}.hero{padding-block:28px 24px}nav a{margin:0 18px 0 0}}
@media (max-width:480px){.out,ol.steps{grid-template-columns:minmax(0,1fr)}}
.qfoot{border-top:1px solid var(--line);padding:22px 0 26px;margin-top:24px}.qfoot .fl{display:flex;flex-wrap:wrap;justify-content:center;gap:4px 22px;margin:0 0 2px}.qfoot .fl a{font-size:13px}.qfoot .fs{margin:6px 0 0;font-size:13px;color:var(--mute);text-align:center}.qfoot .ai{font-size:12.5px;color:var(--mute);max-width:720px;margin:10px auto 0;line-height:1.5;text-align:center}.demosub{font-size:21px;line-height:1.45;max-width:none;color:var(--fg)}.democard{display:block;text-decoration:none;color:inherit}.democard:hover{border-color:var(--gold)}.democard p b{font-size:17px;color:var(--fg)}.cases{display:grid;gap:20px}.case{border:1px solid var(--line);border-radius:8px;padding:18px 20px;background:var(--card)}.case h3{margin:4px 0 2px}.case .who{color:var(--mute);margin:0 0 10px}.case dt{font-weight:600;margin-top:8px}.case dd{margin:2px 0 0}.foundlist{margin:0;padding-left:20px}.foundlist li{margin:6px 0}.foundlist a{color:var(--fg);text-decoration:none;border-bottom:1px solid var(--line)}.foundlist a:hover{border-color:var(--gold)}
@media (max-width:720px){table.qt thead{display:none}table.qt,table.qt tbody,table.qt tr,table.qt td{display:block;width:100%}table.qt tr{border-top:2px solid var(--line);padding:10px 0}table.qt td{border:0;padding:4px 0;min-width:0!important}table.qt td[data-l]::before{content:attr(data-l);display:block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}}
"""

MARK = '<svg viewBox="0 0 100 100" aria-hidden="true"><polygon points="50,10.1 96,89.9 4,89.9" fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round"/><polygon points="50,89.9 72.5,40.6 27.5,40.6" fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round"/><circle cx="50" cy="57" r="4" fill="currentColor"/></svg>'

NAV = [('/', 'Overview'), ('/examples', 'Examples'), ('/findings', 'Findings'), ('/calibrations', 'Calibrations'), ('/services', 'Services'), ('/method', 'Method')]


def page(path, title, desc, body):
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == path else '', t) for h, t in NAV)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://quantumidleaudit.com{'' if path == '/' else path}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website">
<meta name="tdm-reservation" content="1"><meta name="tdm-policy" content="{I}/terms#ai-training">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Lora:wght@500;600&family=Inter:wght@400;500;600&display=swap">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<style>{CSS}{TABLE_CSS}</style></head><body>
<header><div class="wrap"><a class="brand" href="/">{MARK}<span>Quantum Idle Audit<small>Heuremen LLC</small></span></a><nav>{nav}</nav></div></header>
<main>{body}</main>
<footer class="qfoot"><div class="wrap">
<p class="fl"><a href="{I}/qia">QIA on indahl.ai</a><a href="{CONTACT}">Inquiries</a><a href="{I}/conflict-of-interest">Conflict of interest</a><a href="{I}/terms">Terms</a><a href="{I}/privacy">Privacy</a></p>
<p class="fs">Quantum Idle Audit &middot; A division of Heuremen LLC. &ldquo;We found it.&rdquo;</p>
<p class="ai">Independent measurement of quantum hardware against the vendor&rsquo;s published calibration. Mutual NDA before any engagement. Nothing published without written consent. Fees are independent of findings. It runs its measurements on IBM Quantum under its own account and is not otherwise affiliated with IBM; IBM and the processor names are trademarks of IBM. &copy; 2026 Heuremen LLC. Retrieval and answering are permitted; use as AI training data is not.</p>
</div></footer>
</body></html>
'''


OUTCOMES = '''<div class="out">
<div><b>ABOVE</b><p>The measured value sits above the stated value, outside the interval.</p></div>
<div><b>BELOW</b><p>The measured value sits below the stated value, outside the interval.</p></div>
<div><b>CONSISTENT</b><p>The stated value sits inside the interval. The bound is printed.</p></div>
<div><b>CANNOT TELL</b><p>The data cannot separate the stated value from the size that would matter.</p></div>
</div>'''

OFFERS = f'''<div class="grid">
<div class="card"><p class="k">Full audit of a research paper</p><h3>A paper read in full and recounted</h3>
<p>Every claim quoted, located and recomputed from the released data or rerun on hardware, delivered as a line-item report with an evidence package.</p><p class="price">{price('audit')}</p></div>
<div class="card"><p class="k">Monitoring</p><h3>Calibration watched over time</h3>
<p>The processors a team depends on, read against their published calibration on a fixed schedule, with each deviation reported as it lands.</p><p class="price">{price('monitor')}</p><p class="fine">Billed monthly, cancel any month. Or $25,500 a year prepaid (15% off); $23,000 if signed during the pilot. A prepaid year is not refundable and cannot be canceled.</p></div>
<div class="card"><p class="k">30-day pilot</p><h3>Monitoring on your own processors, for a month</h3>
<p>Your backends and qubits read against their published calibration for 30 days: signed receipts for each run, one variance report, and the measured corrections.</p><p class="price">{price('pilot')}</p><p class="fine">If you stop within the 30 days, the unused days are refunded pro rata. The pilot fee counts toward a prepaid year signed during the pilot.</p></div>
</div>''' 

SHEET = '''<div class="sheet" aria-label="Report format">
<div class="row"><span><b>Your run</b></span><span>your circuit, layout and shots, unchanged</span></div>
<div class="row"><span>Their run against ours</span><span>the same shots, with a 99% interval</span></div>
<div class="row"><span>Figures the run depended on</span><span>stated against measured that day</span></div>
<div class="row"><span>What we changed</span><span>each setting and the job it came from</span></div>
<div class="row"><span>Outcome</span><span><span class="tag">ABOVE</span> <span class="tag">BELOW</span> <span class="tag">CONSISTENT</span> <span class="tag">CANNOT TELL</span></span></div>
</div>'''

ZZ = os.path.join(HERE, '..', 'heuremen.org', 'experiments', '2026-10-22-direct-zz')
ZZ_URL = 'https://heuremen.org/experiments/2026-10-22-direct-zz/'


def zz_points(fn):
    import re
    t = open(os.path.join(ZZ, fn), encoding='utf-8').read()
    m = re.search(r'per edge \(A, B, stated kHz, \|df\| kHz\): (.*)', t)
    pts = [(float(s), float(d)) for _, _, s, d in re.findall(r'\((\d+),(\d+),([\d.]+),([\d.]+)\)', m.group(1))]
    job = re.search(r'job (\S+)', t).group(1)
    return pts, job


def zz_figure():
    """IBM's stated zz against the shift measured on the same edge, ibm_fez and ibm_phoenix, log-log. From the public results files."""
    import math
    fez, jf = zz_points('results_direct.text'); phx, jp = zz_points('results_direct_phoenix.text')
    allp = [p for p in fez + phx if p[0] > 0 and p[1] > 0]
    lo, hi = 1.0, 100.0
    W, H, L, R, T, B = 520, 400, 56, 14, 14, 46
    X = lambda v: L + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (W - L - R)
    Y = lambda v: H - B - (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (H - T - B)
    clip = lambda v: min(max(v, lo), hi)
    g = []
    for v in (1, 2, 5, 10, 20, 50, 100):
        g.append(f'<line x1="{X(v):.1f}" y1="{T}" x2="{X(v):.1f}" y2="{H-B}" stroke="var(--line)" stroke-width="1"/>')
        g.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{W-R}" y2="{Y(v):.1f}" stroke="var(--line)" stroke-width="1"/>')
        g.append(f'<text x="{X(v):.1f}" y="{H-B+18}" text-anchor="middle" font-size="12" fill="var(--mute)">{v}</text>')
        g.append(f'<text x="{L-8}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="12" fill="var(--mute)">{v}</text>')
    g.append(f'<line x1="{X(lo):.1f}" y1="{Y(lo):.1f}" x2="{X(hi):.1f}" y2="{Y(hi):.1f}" stroke="var(--mute)" stroke-width="1.2" stroke-dasharray="5 4"/>')
    g.append(f'<text x="{X(60):.1f}" y="{Y(60)-8:.1f}" text-anchor="end" font-size="12" fill="var(--mute)">measured = stated</text>')
    for pts, col in ((fez, 'var(--fez)'), (phx, 'var(--phx)')):
        for s, d in pts:
            if s <= 0: continue
            g.append(f'<circle cx="{X(clip(s)):.1f}" cy="{Y(clip(d)):.1f}" r="4" fill="{col}" fill-opacity=".78" stroke="var(--card)" stroke-width="1"/>')
    g.append(f'<text x="{(L+W-R)/2:.0f}" y="{H-8}" text-anchor="middle" font-size="12.5" fill="var(--fg)">IBM stated zz, kHz</text>')
    g.append(f'<text transform="translate(16 {(T+H-B)/2:.0f}) rotate(-90)" text-anchor="middle" font-size="12.5" fill="var(--fg)">measured shift, kHz</text>')
    nz = sum(1 for s, _ in phx if s <= 0)
    svg = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="IBM stated zz coupling against the measured shift on the same edge, ibm_fez and ibm_phoenix" font-family="Inter,system-ui,sans-serif">' + ''.join(g) + '</svg>'
    legend = (f'<div class="legend"><span><i style="background:var(--fez)"></i>ibm_fez, {len(fez)} edges: slope 0.92 [0.83, 1.02], consistent with 1</span>'
              f'<span><i style="background:var(--phx)"></i>ibm_phoenix, {len(phx)} edges: slope &minus;0.06 [&minus;0.63, 0.32], below 1</span></div>')
    cap = (f'Same code, same day, two IBM Heron processors. Each point is one coupled pair: the zz IBM states for it against the shift measured on it. '
           f'Slopes on log&ndash;log axes with 95% intervals; {nz} ibm_phoenix edges stated 0.00 are not drawn. Jobs {jf} and {jp}. '
           f'<a href="{ZZ_URL}">Data and code</a>.')
    return f'<figure class="fig">{legend}{svg}<figcaption>{cap}</figcaption></figure>'


def finance_figure():
    """20 Nov 2026 (the owner): the hero chart is the finance sample report (QIA-2026-002): option-price error as a percent of the exact
    price, all 32 copies pooled, client run against ours, both runs on each processor. Numbers from the report and /demo-finance."""
    rows = [('ibm_fez', 'run 1', 8.4, 0.36), ('ibm_fez', 'run 2', 17.8, 0.75), ('ibm_kingston', 'run 1', 6.4, 2.55), ('ibm_kingston', 'run 2', 6.2, 0.01),
            ('ibm_marrakesh', 'run 1', 23.1, 4.34), ('ibm_marrakesh', 'run 2', 22.5, 4.34)]
    W, L, R, T, bh, gap, grp = 520, 112, 50, 10, 16, 5, 16
    H = T + len(rows) * (2 * bh + gap) + 3 * grp + 30
    mx = 25.0; X = lambda v: L + v / mx * (W - L - R)
    g = []
    for v in (0, 5, 10, 15, 20, 25):
        g.append(f'<line x1="{X(v):.1f}" y1="{T}" x2="{X(v):.1f}" y2="{H-30}" stroke="var(--line)" stroke-width="1"/>')
        g.append(f'<text x="{X(v):.1f}" y="{H-14}" text-anchor="middle" font-size="12.5" fill="var(--mute)">{v}%</text>')
    y = T; last = None
    for chip, run, th, ou in rows:
        if chip != last:
            y += grp if last else 4
            g.append(f'<text x="{L-8}" y="{y+bh+gap/2+(0 if chip == "ibm_marrakesh" else 5):.1f}" text-anchor="end" font-size="13" fill="var(--fg)">{chip}</text>')
            if chip == 'ibm_marrakesh': g.append(f'<text x="{L-8}" y="{y+bh+gap/2+15:.1f}" text-anchor="end" font-size="11.5" fill="var(--mute)">control</text>')
            last = chip
        g.append(f'<rect x="{L}" y="{y:.1f}" width="{X(th)-L:.1f}" height="{bh}" rx="2" fill="var(--mute)" fill-opacity=".45"/>')
        g.append(f'<text x="{X(th)+5:.1f}" y="{y+bh-2:.1f}" font-size="12.5" fill="var(--mute)">{th:g}%</text>')
        g.append(f'<rect x="{L}" y="{y+bh:.1f}" width="{max(X(ou)-L,2):.1f}" height="{bh}" rx="2" fill="var(--fez)"/>')
        g.append(f'<text x="{max(X(ou),L+2)+5:.1f}" y="{y+2*bh-2:.1f}" font-size="12.5" font-weight="600" fill="var(--fg)">{ou:g}%</text>')
        y += 2 * bh + gap
    svg = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Option-price error, client run against calibrated run, on ibm_fez, ibm_kingston and ibm_marrakesh" font-family="Inter,system-ui,sans-serif">' + ''.join(g) + '</svg>'
    legend = ('<div class="legend"><span><i style="background:var(--mute);opacity:.45"></i>Their run, the default</span>'
              '<span><i style="background:var(--fez)"></i>Ours, calibrated</span></div>')
    cap = ('Error in the option price, as a percent of the exact price, with all 32 copies pooled. Same circuit, same processor, same shots, '
           'run twice on each processor, 19 November 2026. ibm_marrakesh is our layout-fault control. '
           '<a href="/qia-2026-002.pdf">Sample report</a> &middot; <a href="/demo-finance">Job records</a>.')
    return f'<figure class="fig"><p class="figt">Option pricing: their run against ours</p>{legend}{svg}<figcaption>{cap}</figcaption></figure>'


FIG = finance_figure()

DEMOS = '''<section id="demos"><div class="wrap"><p class="eyebrow">Demonstrations</p><p class="sub demosub">Two rounds on three separate processors, across six industry workloads.</p><div class="grid demogrid"><a class="card democard" href="/demo-finance"><p class="k">Finance</p><h3>Option price error</h3><p><b>Default: up to 23% off. Calibrated: within 4.4%.</b></p></a><a class="card democard" href="/demo-chemistry"><p class="k">Chemistry</p><h3>Molecular energy error</h3><p><b>Default: 12.8&ndash;17.8 mHa. Calibrated: 0.9&ndash;4.6 mHa.</b></p></a><a class="card democard" href="/demo-optimization"><p class="k">Logistics</p><h3>Short of the noiseless answer</h3><p><b>Default: 3.1&ndash;6.7%. Calibrated: 1.6&ndash;4.6%.</b></p></a><a class="card democard" href="/demo-simulation"><p class="k">Simulation</p><h3>Error against the exact answer</h3><p><b>Default: 0.064&ndash;0.103. Calibrated: 0.020&ndash;0.077.</b></p></a><a class="card democard" href="/demo-error-correction"><p class="k">Error correction</p><h3>Logical failures per round</h3><p><b>Default: 17&ndash;28%. Calibrated: 10&ndash;18%.</b></p></a><a class="card democard" href="/demo-ai"><p class="k">AI and machine learning</p><h3>Shot bill at 40 qubits</h3><p><b>3.6&ndash;12&times; the published-figure plan. Measured in 23 seconds.</b></p></a></div></div></section>'''

HOME = f'''
<div class="hero wrap herogrid"><div><h1>Independent checks of quantum hardware claims against the vendor&rsquo;s own calibration.</h1>
<p class="lede">Each line gives the published value, our measurement with its interval, and the record the job ran under.</p>
<div class="btns"><a class="btn" href="{SAMPLE_PDF}">See a sample report</a></div></div>
{FIG}</div>
{DEMOS}
<section class="soft"><div class="wrap report"><div>
<p class="eyebrow">Sample report</p><h2>QIA-2026-002: option pricing, calibrated</h2>
<p class="sub">A bank desk&rsquo;s option-pricing run, done their way and calibrated, twice on three processors. On ibm_fez the price error fell 15.5 times. With every copy pooled, the default price stayed 6 to 23 % off; the calibrated price landed within 4.4 %.</p>
<div class="btns"><a class="btn" href="/qia-2026-002.pdf">Report (PDF)</a><a class="btn ghost" href="/demo-finance">Job records</a></div>
<div style="margin-top:30px">{SHEET}</div></div>
<a href="/qia-2026-002.pdf" aria-label="QIA-2026-002 report, PDF"><img class="cover" src="/qia-2026-002-cover.jpg" width="695" height="900" alt="First page of QIA-2026-002: option-pricing error, their run against ours, on ibm_fez, ibm_marrakesh and ibm_kingston"></a></div></section>

<section><div class="wrap"><p class="eyebrow">What is delivered</p><h2>Findings, method and evidence</h2><p class="sub">The same three parts in every engagement.</p>
<div class="grid">
<div class="card"><h3>A line-item report</h3><p>Every figure checked, its stated and measured value, an interval, and one of four outcomes.</p></div>
<div class="card"><h3>Metrics of completion, set in advance</h3><p>What the engagement measures and when it is done, agreed before any data is read.</p></div>
<div class="card"><h3>An evidence package</h3><p>Raw job records and run IDs, code and checksums, so any line can be rerun independently.</p></div>
</div></div></section>

<section class="soft"><div class="wrap"><p class="eyebrow">Services</p><h2>Three ways to engage</h2><p class="sub">Each is scoped under a statement of work after a mutual NDA.</p>
{OFFERS}<p style="margin-top:26px"><a href="/services">Services in detail</a></p></div></section>

<section><div class="wrap"><p class="eyebrow">Method</p><h2>Four outcomes, never folded</h2><p class="sub">Every reading lands in one of four outcomes against what was stated.</p>
{OUTCOMES}<p style="margin-top:26px"><a href="/method">How a reading is made</a></p></div></section>

'''

SERVICES = f'''
<div class="hero wrap"><p class="eyebrow">Services</p><h1>Full audits and monitoring.</h1>
<p class="lede">A mutual NDA comes first; each engagement is then scoped and quoted under a statement of work. Paid, collaborative and pro bono research engagements are considered.</p>
<div class="btns"><a class="btn" href="{SAMPLE_PDF}">See a sample report</a></div></div>
<section class="soft"><div class="wrap">{OFFERS}</div></section>
<section><div class="wrap"><p class="eyebrow">How an engagement runs</p><h2>From scope to delivery</h2><p class="sub">Fixed steps, the same for every client.</p>
<ol class="steps">
<li><b>Scope</b><span>Mutual NDA, then the figures in question and the metrics of completion, set in writing.</span></li>
<li><b>Measure</b><span>Runs and recounts against the calibration record each job ran under.</span></li>
<li><b>Report</b><span>A line-item report: stated, measured, interval, outcome.</span></li>
<li><b>Hand over</b><span>The evidence package, rerunnable by the client or anyone the client names.</span></li>
</ol></div></section>
<section class="soft"><div class="wrap band"><div><h2>Confidentiality</h2><p>Mutual NDA first. Nothing about an engagement is published without written consent. Fees are independent of findings.</p></div><a class="btn" href="{CONTACT}">Inquiries</a></div></section>
'''

METHOD = f'''
<div class="hero wrap"><p class="eyebrow">Method</p><h1>How a reading is made.</h1>
<p class="lede">Stated value first, then the measurement, then the interval, then the outcome. The comparison is fixed before any data is read.</p></div>
<section class="soft"><div class="wrap"><h2>Four outcomes</h2><p class="sub">Against the stated value, with both the zero and the size that would matter tested.</p>{OUTCOMES}</div></section>
<section><div class="wrap prose">
<h3>The stated value, named</h3><p>Each line names what the published figure is (its definition, its averaging and the record it comes from) before anything is compared against it.</p>
<h3>The record the job ran under</h3><p>IBM states that its published properties come from calibration run about once a day (<a href="https://quantum.cloud.ibm.com/docs/tutorials/real-time-benchmarking-for-qubit-selection">IBM tutorial</a>). Each measured value is compared with the record in force when its job ran, not a daily median.</p>
<h3>Intervals</h3><p>Brackets are 95% intervals unless the row names another; each row names its interval and the units it is taken over (qubits, pairs, trials or jobs). A result inside the interval is reported as consistent, with the bound printed. Where a row tests a size that matters, it states that margin.</p>
<h3>Comparisons built in advance</h3><p>The comparison arm, the counts and the outcome rule are written down before the data is read. Anything defined after the data is labeled as such.</p>
<h3>Easily repeatable evidence</h3><p>Job IDs, raw counts, code and checksums ship with every report. The public standards behind these rules are at <a href="{I}/standard">indahl.ai/standard</a>.</p>
</div></section>
'''

LISTED = f'''
<div class="hero wrap"><p class="eyebrow">Your study is listed</p><h1>A listing is an index entry, not a verdict.</h1>
<p class="lede">The QIA List indexes published quantum-hardware studies and records which claims were checked against data. Each listing is a classification for indexing, not an assessment of the study or its authors.</p>
<div class="btns"><a class="btn" href="{I}/qia/list">Find your entry</a><a class="btn ghost" href="{I}/correction">Correct or remove an entry</a></div></div>
<section class="soft"><div class="wrap"><h2>What an entry shows</h2><p class="sub">Every entry carries the version read, the date indexed, and the basis for each code.</p>
<div class="grid">
<div class="card"><h3>The version read</h3><p>The exact version of the study the entry rests on, and when it was indexed.</p></div>
<div class="card"><h3>Claim codes</h3><p>Each code points to the <a href="{I}/qia/key">QIA Key</a>, which defines it. A dash means the study was read in full and no code applies.</p></div>
<div class="card"><h3>The basis</h3><p>The quoted text and the location behind each code, so the reading can be checked against the study itself.</p></div>
</div></div></section>
<section><div class="wrap prose">
<h3>Correcting an entry</h3><p>Corrections and removal requests go through <a href="{I}/correction">indahl.ai/correction</a> and are answered by email within five business days. A correct correction changes the entry.</p>
<h3>Replying to an entry</h3><p>Authors may send a reply through the same form. With the authors&rsquo; permission, the reply is shown with the entry.</p>
<h3>Commercial relationships</h3><p>Any commercial relationship connected to a listed entry is flagged on that entry, under the <a href="{I}/conflict-of-interest#relationships">conflict-of-interest policy</a>.</p>
<h3>Going further</h3><p>Teams that want their own processors or studies measured line by line can commission a full audit.</p>
<p><a class="btn" href="/services">Services</a></p>
</div></section>
'''

# 17 Nov 2026 (the owner: "start building out these tables on quantumidleaudit.com ... the pitch points there"): the findings and the
# calibrations tables, rendered from indahl-ai/qiasite_tables.json (one data file; edit there, run this script). Internal source paths in the
# data are not printed; each row prints where a reader can check both IBM's side and ours.
import json as _json
_TB = _json.load(open(os.path.join(HERE, 'qiasite_tables.json'), encoding='utf-8'))
TABLE_CSS = ("table.qt{width:100%;border-collapse:collapse;font-size:.92rem;margin:1rem 0}table.qt th,table.qt td{border-top:1px solid var(--line);"
             "padding:.6rem .55rem;vertical-align:top;text-align:left}table.qt th{font-weight:600;color:var(--fg);white-space:nowrap}"
             "table.qt td.id{font-weight:600;white-space:nowrap;color:var(--gold)}.tscroll{overflow-x:auto;-webkit-overflow-scrolling:touch}"
             "table.qt small{color:var(--mute)}.wrap.wide{max-width:1280px}table.qt td:nth-child(4){min-width:22ch}table.qt td:nth-child(2){min-width:14ch}")
def _e(s): return html.escape(s or '')
def _findings():
    rows = ''.join('<tr id="%s"><td class="id" data-l="Item">%s</td><td data-l="What"><b>%s</b></td><td data-l="IBM&rsquo;s figure">%s</td><td data-l="Measured">%s</td><td data-l="Date and interval">%s<br><small>%s</small></td><td data-l="How to check"><small>IBM: %s<br>Ours: %s</small></td><td data-l="Status">%s</td></tr>' % (
        _e(r['id'].lower()), _e(r['id']), _e(r['what']), _e(r['ibm']), _e(r['ours']), _e(r['date']), _e(r['interval']), _e(r['repro_ibm']), _e(r['repro_ours']), _e(r['status'])) for r in _TB['findings'])
    return f"""<div class="hero wrap"><p class="eyebrow">Findings</p><h1>IBM&rsquo;s published calibration, set beside what the hardware delivered.</h1>
<p class="lede">Each row prints IBM&rsquo;s figure as published, our measurement with its interval and date, and how a reader can check both sides. Heuremen LLC is not affiliated with IBM. Record facts are dated reads of IBM&rsquo;s backend properties. Effects with no field in the record are stated as of the date the record was read.</p></div>
<section><div class="wrap wide"><div class="tscroll"><table class="qt"><thead><tr><th>Item</th><th>What</th><th>IBM&rsquo;s figure</th><th>Measured</th><th>Date and interval</th><th>How to check</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="fine">Outcomes follow the <a href="/method">method</a>: ABOVE, BELOW, CONSISTENT (printed as a bound) or CANNOT TELL. Papers cited as Zenodo records are preprints, not peer reviewed. Rows marked &ldquo;computed after the hardware result&rdquo; are labeled as such. <a href="{CONTACT}">Request full records of any listed run.</a></p></div></section>"""
def _calibs():
    rows = ''.join('<tr id="%s"><td data-l="Calibration"><b>%s</b>%s</td><td class="id" data-l="Addresses">%s</td><td data-l="Your run: without / with">%s</td><td data-l="Result on hardware">%s%s</td><td data-l="Cost">%s</td><td data-l="Status">%s</td></tr>' % (
        _e(c['name'].split(' (')[0].split()[0].lower() if c['name'].startswith('Combinations') else __import__('re').sub(r'[^a-z0-9]+','-',c['name'].lower())[:40].strip('-')), _e(c['name']), ('<br><small>%s</small>' % _e(c['prior_art'])) if c['prior_art'] else '', _e(c['fixes']), _e(c.get('client', '')) or '&mdash;', _e(c['result']),
        ('<br><small>%s</small>' % _e(c['interval'])) if c['interval'] else '', _e(c['cost']), _e(c['status'])) for c in _TB['calibrations'])
    return f"""<div class="hero wrap"><p class="eyebrow">Calibrations</p><h1>What can be corrected, and what each correction returns.</h1>
<p class="lede">A calibration here is applied to a workload and measured against an uncorrected reference in the same job. Each row says which finding it addresses, what it returned on hardware, and its status. Combinations are measured only after each part reads on its own.</p></div>
<section><div class="wrap wide"><div class="tscroll"><table class="qt"><thead><tr><th>Calibration</th><th>Addresses</th><th>Your run: without / with</th><th>Result on hardware</th><th>Cost</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="fine">Where a correction was proposed by others, the row names them.</p></div></section>"""
FINDINGS, CALIBS = _findings(), _calibs()
_LS = os.path.expanduser('~/bones-forge/calibrations/demos/release/letter_sent.json')   # 19 Nov 2026: dated line goes up only when the IBM letter is actually sent (on_send.sh)
if os.path.exists(_LS):
    _ls = _json.load(open(_LS)); FINDINGS = FINDINGS.replace('the date the record was read.</p></div>\n', 'the date the record was read.</p><p class="lede"><b>Letter sent to IBM Corporate Media Relations on %s,</b> with our findings, calibrations and demonstrations, and an advance copy of our launch release.</p></div>\n' % _e(_ls['date']), 1)
def _case(tag, who, title, checked, came, handed, src):
    return ('<div class="case"><p class="k">%s</p><h3>%s</h3><p class="who">%s</p><dl>'
            '<dt>What we checked</dt><dd>%s</dd><dt>What came back</dt><dd>%s</dd><dt>What the client gets</dt><dd>%s</dd></dl>'
            '<p class="fine">%s</p></div>') % (tag, title, who, checked, came, handed, src)
WE = 'Worked example (from our record)'
EXAMPLES = f"""<div class="hero wrap"><p class="eyebrow">Examples</p><h1>What a check looks like, by the work you do.</h1>
<p class="lede">Each example below is a worked example from our own record: real runs on IBM processors, with the outcome word the method assigned.</p></div>
<section><div class="wrap cases">
{_case(WE, 'For teams running mid-circuit measurements: error correction, dynamic circuits, feed-forward.', 'Mid-circuit readouts on IBM processors', 'The turn a mid-circuit readout gives the phase of qubits that are not read, per qubit, on ibm_fez, ibm_kingston and ibm_marrakesh (17 November 2026).', 'Turn per readout, with 39 qubits read at once: 1.75 to 2.51 degrees on the three processors, same direction on all three and on both dates measured (99&nbsp;% intervals in the source).', 'A per-qubit correction table measured minutes before the job (it returned 86 to 93&nbsp;% of the turn; in 6,000 random shuffles of the table across ibm_kingston and ibm_marrakesh, none returned more than half), an echo where the circuit puts pairs beside a readout, and whether to re-measure: a 27-day-old table still returned 82 and 90&nbsp;% on two processors, and on ibm_marrakesh it had drifted by about a degree.', 'Source: <a href="/calibrations#per-qubit-phase-correction-after-each-re">phase correction</a>, <a href="/calibrations#combinations">combinations</a>, <a href="/findings#e1">finding E1</a>.')}
{_case(WE, 'For anyone who corrects readout with published figures (readout mitigation).', 'What an old readout snapshot does to a correction', 'IBM&rsquo;s published readout figures for ibm_fez qubit 155 against our own measurement of the qubit, and what a correction built from each does to an entangled pair read on it (17 to 18 November 2026).', 'IBM&rsquo;s record stated P(1|0) = 0.982. Correcting with that figure divides by 0.007, and the pair read fidelity 26 and 72 (impossible values; 1 is the maximum). Our readout guard flags any qubit whose published figures leave less than half the signal and refuses to correct with them; corrected with the same job&rsquo;s calibration, the pair read normally.', 'A list of the qubits in your circuit whose published readout figures fall outside the guard, and the same-job calibration to use instead.', 'Source: <a href="/calibrations#readout-assignment-correction-from-a-min">readout correction</a>, <a href="/findings#r10">finding R10</a>.')}
{_case(WE, 'For teams that depend on the same processors week after week.', 'Monitoring the same processors over time', 'Each qubit&rsquo;s readout and T1 measured against the record in force on a regular cadence (129 runs in eight days), with a signed receipt per run; and, once, the per-qubit phase table re-measured against its 27-day-old copy.', 'Our regular runs saw bad-readout episodes on ibm_marrakesh qubits 64 and 76 about 4.4 and 2.5 hours before IBM&rsquo;s refresh of 13 November recorded them. The phase table had drifted by about one degree in four weeks, and the old table overshot by the amount predicted before the run.', 'A reading of your processors on a fixed cadence, signed receipts you can hand to a third party, and a flag when a correction table needs re-measuring. Any qubit can be read live through the free <a href="' + I + '/try">Test Drive</a>.', 'Source: <a href="/findings#r10">finding R10</a>, <a href="/calibrations#per-qubit-phase-correction-after-each-re">phase correction</a>.')}
</div></section>
"""

CORRECTIONS = f"""<div class="hero wrap"><p class="eyebrow">Corrections</p><h1>Report an error in a finding.</h1>
<p class="lede">Every finding prints its data and method so it can be checked. To report an error, use the <a href="{I}/correction">correction form</a> and name the row (for example R10). We reply within five business days, and any change is made on the row itself and dated.</p></div>
<section><div class="wrap"><h2>Dated changes</h2><ul class="foundlist">
<li>18 Nov 2026, C1: the gate-error runs were 16 on 7 processors, not 8; the row now names each processor. The 17 Nov readings on five kingston qubits did not repeat the 23 Oct result, and the row says so.</li>
<li>18 Nov 2026, R10: times re-read in UTC. IBM stamps its records in US Eastern time and an earlier reading dropped the offset, which reversed the order of our runs and IBM&rsquo;s refresh. Our runs saw the qubit 155 episode before IBM&rsquo;s refresh. The count of runs under IBM&rsquo;s entry was recounted from the corrected times and replaced.</li>
<li>18 Nov 2026, readout table withdrawn: a table of readout entries that looked misstated was withdrawn, because IBM&rsquo;s own refreshes several days apart disagree as often. It is not a finding.</li>
</ul></div></section>"""

PAGES = {
    '/': ('Quantum Idle Audit | Independent checks of quantum hardware claims', 'Independent checks of quantum hardware claims against the vendor’s own calibration, with line-item reports and evidence anyone can rerun.', HOME),
    '/findings': ('Findings | Quantum Idle Audit', 'IBM published calibration figures set beside measured hardware values, with intervals, dates and how to check both sides.', FINDINGS),
    '/calibrations': ('Calibrations | Quantum Idle Audit', 'Corrections applied on IBM hardware against an uncorrected reference: what each returns, its cost and status.', CALIBS),
    '/services': ('Services | Quantum Idle Audit', 'Full audits of research papers and monitoring of quantum hardware, scoped under a statement of work after a mutual NDA.', SERVICES),
    '/method': ('Method | Quantum Idle Audit', 'How a Quantum Idle Audit reading is made: the stated value, the record the job ran under, intervals and four outcomes.', METHOD),
    '/examples': ('Examples | Quantum Idle Audit', 'Worked examples of a Quantum Idle Audit check by the work you do, with real runs on IBM processors and the outcome printed first.', EXAMPLES),
    # '/corrections' archived 19 Nov 2026 (the owner): back with a reliable private update pipeline (~/bones-forge/archive/qia_corrections_page_20261119)
    # '/listed' archived 19 Nov 2026 (the owner): study listings live on indahl.ai, not the business site
}



if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for p, (t, d, b) in PAGES.items():
        name = 'index.html' if p == '/' else p.strip('/') + '.html'
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write(page(p, t, d, b))
    # private plan: rendered by a module outside the public code, if present on this machine
    _pp = os.path.expanduser('~/bones-forge/private_plan/plan_render.py')
    if os.path.exists(_pp):
        import importlib.util as _iu; _sp = _iu.spec_from_file_location('plan_render', _pp); _m = _iu.module_from_spec(_sp); _sp.loader.exec_module(_m)
        open(os.path.join(os.path.dirname(_pp), 'plan.html'), 'w', encoding='utf-8').write(page('/plan', 'Plan', 'Plan.', _m.build(HERE, _e)).replace('<meta name="description"', '<meta name="robots" content="noindex, nofollow"><meta name="description"', 1))
    _pd = os.path.expanduser('~/bones-forge/calibrations/site/demos_render.py')   # 19 Nov 2026: industry demo pages (the designer), noindex, out of nav and sitemap
    if os.path.exists(_pd):
        import importlib.util as _iu2; _sp2 = _iu2.spec_from_file_location('demos_render', _pd); _m2 = _iu2.module_from_spec(_sp2); _sp2.loader.exec_module(_m2)
        _m2.write_all(page, OUT)
    _pc = os.path.expanduser('~/bones-forge/calibrations/site/console/build.py')   # 21 Nov 2026 (the owner: "Go with console"; ship now): The designer's Console pages replace home, demos, calibrations and add /runs, /monitoring, /inquiries
    if os.path.exists(_pc):
        import importlib.util as _iu3; _sp3 = _iu3.spec_from_file_location('console_build', _pc); _m3 = _iu3.module_from_spec(_sp3); _sp3.loader.exec_module(_m3)
        _m3.write_all(OUT, inquiry_form=CONTACT)
        assert not _m3.unresolved() and not _m3.placeholders(), 'REFUSED: the Console build still has unresolved links or placeholder copy: %r %r' % (_m3.unresolved(), _m3.placeholders())
    open(os.path.join(OUT, 'favicon.svg'), 'w').write(MARK.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"').replace('currentColor', '#806012'))
    open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: https://quantumidleaudit.com/sitemap.xml\n')
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join('<url><loc>https://quantumidleaudit.com%s</loc></url>\n' % ('' if p == '/' else p) for p in PAGES) + '</urlset>\n')
    print('qia site: %d pages in %s' % (len(PAGES), os.path.relpath(OUT, os.path.join(HERE, '..'))))
