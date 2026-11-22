#!/usr/bin/env python3
"""name_gate.py (21 Nov 2026, owner: the published standard is named "The Heuremen Standard", never "Standards", no version number).
A ship gate. Scans every built page of indahl.ai (indahl-ai/pages.js and the files it imports, plus llms.txt from LLMS) and
quantumidleaudit.com (public/_qiasite/*.html), tags stripped, and refuses on the plural name: "Heuremen Standards", "the Standards"
(case-insensitive), "STANDARDS", "Standards" anywhere in our copy (SAGAR's expansion excepted), or a version number after the name
("Standards 2", "Heuremen Standard V1"). Owner 21 Nov 2026: the public name is "The Heuremen Standard", no version. Text inside curly double quotes,
<blockquote>/<q>/<code>/<pre> and pages made of other people's words (study pages, study lists, the lookup) is skipped.
The name itself lives in faultsguards/CURRENT.json; this gate refuses the old plural and any version label.
  python3 ledger/name_gate.py            exit 1 and list the hits if any
  python3 ledger/name_gate.py --report   list the hits, always exit 0"""
import glob, html, json, os, re, sys
B = os.path.expanduser('~/forge')
RX = [re.compile(r'\bHeuremen(?:\s+LLC)?\s+Standards\b', re.I), re.compile(r'\bthe\s+Standards\b', re.I),
      re.compile(r'\bSTANDARDS\b'), re.compile(r'\bStandards\s+v?\d', re.I),
      re.compile(r'\bHeuremen\s+Standard\s+v?\d', re.I),   # owner 21 Nov: no version number in the public name
      re.compile(r'(?<!\bof )\bStandards\b(?! Audit of Gravitational)')]   # "Institute of Standards" and the like are other bodies' names   # "Standards" in our copy; SAGAR's own expansion is a desk name, not the Standard
QUOTED = re.compile(r'^indahl\.ai/(hermes/datapapers|oy/school/|qia/data|e/)|/(study|studies|lookup)/|^indahl\.ai/(sagar|qia/list|iris/list|hermes/list|list)(\.html)?$|/list(\.html)?$')
def clean(h):
    h = re.sub(r'<(script|style|blockquote|q|code|pre)[\s\S]*?</\1>', ' ', h, flags=re.I)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    return re.sub(r'“[^”]{0,600}”', ' ', t)
def pages():
    pj = os.path.join(B, 'indahl-ai', 'pages.js')
    s = open(pj, encoding='utf-8', errors='replace').read(); files = dict(re.findall(r"import (P\d+) from '\./([^']+)'", s))
    paths = {v: k for k, v in re.findall(r'"(/[^"]*)"\s*:\s*(P\d+)', s)}
    for var, rel in files.items():
        f = os.path.join(B, 'indahl-ai', rel)
        if os.path.exists(f): yield 'indahl.ai' + paths.get(var, '/' + rel), open(f, encoding='utf-8', errors='replace').read()
    m = re.search(r'export const LLMS = ("(?:[^"\\]|\\.)*");', s)
    if m: yield 'indahl.ai/llms.txt', html.escape(json.loads(m.group(1)), quote=False)
    for f in glob.glob(os.path.join(B, 'cloudflare-workers', 'heuremen-door', 'public', '_qiasite', '*.html')):
        yield 'quantumidleaudit.com/' + os.path.basename(f)[:-5], open(f, encoding='utf-8', errors='replace').read()
hits = []
for url, h in pages():
    if QUOTED.search(url): continue
    t = clean(h)
    seen_at = set()
    for rx in RX:
        for m in rx.finditer(t):
            if m.start() in seen_at: continue
            seen_at.add(m.start()); hits.append((url, t[max(0, m.start() - 40):m.end() + 30].replace('\n', ' ')))
for u, ctx in hits: print('  %s: ...%s...' % (u, ctx.strip()))
print('name gate: %d plural names of the Heuremen Standard on our pages' % len(hits))
if hits and '--report' not in sys.argv: print('SHIP REFUSED: the published standard is "Heuremen Standard" (singular; name in faultsguards/CURRENT.json)'); sys.exit(1)
