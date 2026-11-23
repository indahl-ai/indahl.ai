#!/usr/bin/env python3
"""spelling_gate.py (21 Nov 2026, the owner).
A ship gate, so the next British spelling is refused at build time instead of found by a reader. Scans every built page of indahl.ai
(indahl-ai/pages.js, the map the worker serves) and quantumidleaudit.com (public/_qiasite/*.html), with tags stripped, and refuses on
any word in BRIT. Text inside curly double quotes and <blockquote>/<q> is skipped: that is other people's words (SAGAR quotes papers
verbatim), and we never change a quote.
  python3 ledger/spelling_gate.py            exit 1 and list the hits if any
  python3 ledger/spelling_gate.py --report   list the hits, always exit 0"""
import glob, html, os, re, sys
B = os.path.expanduser('~/forge')
BRIT = {   # British form -> American form (whole words, case-insensitive)
 'colour': 'color', 'colours': 'colors', 'behaviour': 'behavior', 'behaviours': 'behaviors', 'favour': 'favor', 'favourable': 'favorable',
 'neighbour': 'neighbor', 'neighbours': 'neighbors', 'neighbouring': 'neighboring', 'honour': 'honor', 'labour': 'labor', 'rumour': 'rumor',
 'analyse': 'analyze', 'analysed': 'analyzed', 'analysing': 'analyzing', 'organise': 'organize', 'organised': 'organized', 'organisation': 'organization',
 'organisations': 'organizations', 'realise': 'realize', 'realised': 'realized', 'recognise': 'recognize', 'recognised': 'recognized', 'optimise': 'optimize',
 'optimised': 'optimized', 'optimisation': 'optimization', 'utilise': 'utilize', 'utilised': 'utilized', 'utilisation': 'utilization', 'minimise': 'minimize',
 'maximise': 'maximize', 'summarise': 'summarize', 'summarised': 'summarized', 'standardise': 'standardize', 'standardised': 'standardized', 'normalise': 'normalize',
 'normalised': 'normalized', 'categorise': 'categorize', 'prioritise': 'prioritize', 'emphasise': 'emphasize', 'characterise': 'characterize', 'characterised': 'characterized',
 'centre': 'center', 'centres': 'centers', 'centred': 'centered', 'metre': 'meter', 'metres': 'meters', 'litre': 'liter', 'litres': 'liters', 'fibre': 'fiber',
 'catalogue': 'catalog', 'catalogues': 'catalogs', 'dialogue': 'dialog', 'programme': 'program', 'programmes': 'programs', 'licence': 'license',
 'defence': 'defense', 'offence': 'offense', 'modelling': 'modeling', 'modelled': 'modeled', 'labelled': 'labeled', 'labelling': 'labeling', 'travelled': 'traveled',
 'cancelled': 'canceled', 'fulfil': 'fulfill', 'enrol': 'enroll', 'grey': 'gray', 'judgement': 'judgment', 'ageing': 'aging', 'artefact': 'artifact', 'artefacts': 'artifacts',
 'aluminium': 'aluminum', 'sceptical': 'skeptical', 'whilst': 'while', 'amongst': 'among', 'towards': 'toward', 'utilisations': 'utilizations', 'tonne': 'ton', 'tonnes': 'tons',
}
RX = re.compile(r'\b(' + '|'.join(sorted(BRIT, key=len, reverse=True)) + r')\b', re.I)
def clean(h):
    h = re.sub(r'<(script|style|blockquote|q|code|pre)[\s\S]*?</\1>', ' ', h, flags=re.I)
    h = re.sub(r'<a [^>]*href="https?://(arxiv\.org|doi\.org|export\.arxiv\.org)[^"]*"[^>]*>[\s\S]*?</a>', ' ', h, flags=re.I)   # a study's own title, linked to its record: their words
    h = re.sub(r'<a [^>]*href="/(sagar|qia|iris|hermes)/(study|studies)/[^"]*"[^>]*>[\s\S]*?</a>', ' ', h, flags=re.I)   # a study's title linking to its page: their words
    h = re.sub(r'<td[^>]*>\s*<a [^>]*href="https?://[^"]*"[^>]*>[\s\S]*?</td>', ' ', h, flags=re.I)
    h = re.sub(r'<h1[^>]*>[\s\S]*?</h1>', ' ', h, flags=re.I) if 'Errata study page' in h else h   # a study page's h1 is the paper's title
    h = re.sub(r'<(td|li|p)[^>]*class="[^"]*(quote|by)[^"]*"[^>]*>[\s\S]*?</\1>', ' ', h, flags=re.I)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    return re.sub(r'“[^”]{0,600}”', ' ', t)   # other people's words, quoted
def pages():
    pj = os.path.join(B, 'indahl-ai', 'pages.js')   # imports each page file: import P0 from './index.html'; then maps paths to P0
    if os.path.exists(pj):
        s = open(pj, encoding='utf-8', errors='replace').read(); files = dict(re.findall(r"import (P\d+) from '\./([^']+)'", s))
        paths = {v: k for k, v in re.findall(r'"(/[^"]*)"\s*:\s*(P\d+)', s)}
        for var, rel in files.items():
            f = os.path.join(B, 'indahl-ai', rel)
            if os.path.exists(f): yield 'indahl.ai' + paths.get(var, '/' + rel), open(f, encoding='utf-8', errors='replace').read()
    for f in glob.glob(os.path.join(B, 'cloudflare-workers', 'heuremen-door', 'public', '_qiasite', '*.html')):
        yield 'quantumidleaudit.com/' + os.path.basename(f)[:-5], open(f, encoding='utf-8', errors='replace').read()
# Pages that are made of other people's words (study pages, study lists, the lookup) quote papers' own terms inside our sentences
# ("the paper prints Run C labelled as..."; a table head "fitted centre"; a title "Portfolio optimisation"). We never change a quote, so
# those pages are not gated; every other page is ours and is.
QUOTED = re.compile(r'/(study|studies|lookup)/|^indahl\.ai/(sagar|qia/list|iris/list|hermes/list|list)(\.html)?$|/list(\.html)?$')
hits = []
for url, h in pages():
    if QUOTED.search(url): continue
    for m in RX.finditer(clean(h)):
        hits.append((url, m.group(1), BRIT[m.group(1).lower()]))
seen = {}
for u, w, a in hits: seen.setdefault((u, w.lower(), a), 0); seen[(u, w.lower(), a)] += 1
# BASELINE (allowed): occurrences already reviewed and kept on purpose: proper nouns (a UK school's own name, "Ofsted judgement", a
# programme's official title) and vendor text we quote. `--baseline` writes the current set after a fix pass; the gate then refuses only
# what is NOT in it: a new British spelling, or more of one on a page than the baseline allows.
# 23 Nov 2026 (owner: the Standard shown as written, never paraphrased): indahl.ai/standard and quantumidleaudit.com/standard print the stamped
# STANDARD.md verbatim. Its section 11 keeps the published spelling of fault and guard names (GRD-02 summarised, GRD-21 behaviour, GRD-36 catalogue)
# and its change log quotes the old FLT-23 wording (labelled). One each per page is in the baseline. Any other British word on those pages is refused.
BL = os.path.join(B, 'ledger', 'spelling_baseline.json')
import json as _j
if '--baseline' in sys.argv:
    _j.dump({'%s|%s' % (u, w): n for (u, w, a), n in seen.items()}, open(BL, 'w'), indent=0, sort_keys=True); print('baseline written: %d entries' % len(seen)); sys.exit(0)
allowed = _j.load(open(BL)) if os.path.exists(BL) else {}
new = {k: v for k, v in seen.items() if v > allowed.get('%s|%s' % (k[0], k[1]), 0)}
# 21 Nov 2026 (control audit #3): pages built from data rows (a paper's, school's, institution's or agency's own name: "Centre", "programme",
# "Defence") are reported and rung, not refused; the next such row would otherwise have stopped every ship. Our own template text is still gated.
DATA = re.compile(r'^indahl\.ai/(hermes/datapapers|oy/school/|qia/data|e/)')
data_new = {k: v for k, v in new.items() if DATA.search(k[0])}; new = {k: v for k, v in new.items() if k not in data_new}
for (u, w, a), n in sorted(new.items()): print('  %s: %s -> %s%s' % (u, w, a, ' (x%d)' % n if n > 1 else ''))
for (u, w, a), n in sorted(data_new.items()): print('  data page (reported, not refused): %s: %s -> %s%s' % (u, w, a, ' (x%d)' % n if n > 1 else ''))
if data_new and '--report' not in sys.argv:
    try:
        _rf = os.path.join(B, 'ledger', '.spelling_data_rung.json'); _was = set(_j.load(open(_rf))) if os.path.exists(_rf) else set(); _now = sorted('%s|%s' % (k[0], k[1]) for k in data_new)
        if set(_now) - _was: open(os.path.join(B, 'sagar', 'pipeline', 'pipe.log'), 'a').write(__import__('time').strftime('%Y-%m-%dT%H:%M:%S ') + 'RING: SPELLING on data-built pages, not refused: ' + '; '.join(sorted(set(_now) - _was))[:400] + '\n')
        _j.dump(_now, open(_rf + '.tmp', 'w')); os.replace(_rf + '.tmp', _rf)
    except Exception as _e: print('spelling gate: could not ring pipe.log (%s)' % type(_e).__name__)
print('spelling gate: %d British spellings outside the baseline (%d allowed in the baseline; %d more on data-built pages, reported)' % (sum(new.values()), sum(allowed.values()), sum(data_new.values())))
hits = [1] * sum(new.values())
if not os.path.exists(BL): print('spelling gate: no baseline yet (written after the legacy fix pass); reporting only'); sys.exit(0)
if hits and '--report' not in sys.argv: print('SHIP REFUSED: British spelling (American spelling everywhere public, the owner 18 Nov)'); sys.exit(1)
