#!/usr/bin/env python3
"""link_gate.py (21 Nov 2026, the site link check: a retired page left a dead file in the copy list and links that pointed nowhere).
A ship gate on the BUILT output, before deploy: every same-site href/src (and every fetch("/...") literal in an inline script) on
  indahl.ai             the pages the worker serves (indahl-ai/pages.js imports)
  quantumidleaudit.com  cloudflare-workers/heuremen-door/public/_qiasite/*.html
must resolve to a built page, a file in public/ that the worker actually serves, or a route the worker answers itself (read from
worker.js and the handler modules it imports, so a new route counts without editing this file). Links to the other site are checked
against that site's rules. Refuses (exit 1) and lists each dead link with the pages that carry it.
  python3 ledger/link_gate.py            exit 1 on any dead link
  python3 ledger/link_gate.py --report   list, always exit 0
ALLOW below: reviewed exceptions, each with its reason.
21 Nov 2026 (retired STACK left desks.js loading /stack/live.json; now.js kept loading the study lists retired 17 Nov): the gate also reads every
script the built pages load (script src, and any .js a served script loads in turn, such as sw.js) and every inline script, and checks each
same-site URL they load (a literal handed to fetch/J/getJson/loadAsync/register and the like, or any literal ending in a data extension such as
.json) against the same pages, files and routes. A URL built at run time ('/progress/' + desk + '.json') cannot be checked; its fixed prefix must
be listed in ALLOW_DYNAMIC with its reason, or the gate refuses it as unreviewed."""
import glob, html, json, os, re, sys
from urllib.parse import urljoin, urlparse, unquote
B = os.path.expanduser('~/forge')
IA = os.path.join(B, 'indahl-ai')
CW = os.path.join(B, 'cloudflare-workers', 'heuremen-door')
PUB = os.path.join(CW, 'public')
ALLOW = {   # 'host/path': reason (reviewed exceptions only)
}
ALLOW_DYNAMIC = {   # 'host/prefix': reason. URLs a served script builds at run time; only the fixed prefix is in the source (reviewed 21 Nov 2026)
    'indahl.ai/progress/': "now.js, live-tags.js: '/progress/' + desk + '.json', one per desk that /activity.json names as live",
    'indahl.ai/iris/bench': "iris/bench.js: '/iris/bench' + n + '.json', the bench round the reader picks",
    'indahl.ai/qia/records/': "qia/runcheck.js: '/qia/records/' + backend + '/manifest.json', the processor the reader picks",
    'indahl.ai/qia/cal/': "qia/cal.js: '/qia/cal/' + job + '.json', one calibration record per job id (worker route, KV)",
    'quantumidleaudit.com/qia/cal/': "_qiasite/check_run.js: same as indahl.ai/qia/cal/, which the QIA site passes through to",
    'quantumidleaudit.com/qia/records/': "qia/runcheck.js on the QIA site: '/qia/records/' + backend + '/manifest.json', passed through to indahl.ai",
    'indahl.ai/tape/receipt/': "vault/app.js: '/tape/receipt/' + hash, the 64-character hash the reader enters (worker route)",
}
# ---- the worker's routes ----------------------------------------------------------------------------------------------
W = open(os.path.join(CW, 'worker.js'), encoding='utf-8').read()
qs_start = W.index('if (host === "quantumidleaudit.com"'); qs_end = W.index('if (u.pathname.startsWith("/_qiasite"))')
QBLOCK, IBLOCK = W[qs_start:qs_end], W[qs_end:]
REGEX_LIT = re.compile(r'(?<![\w)\]])/(\^(?:\\/|\\.|[^/\n])+)/[gimsuy]*')
def js_regex(src):
    s = src.replace('\\/', '/')
    s = re.sub(r'\(\?<(\w+)>', r'(?P<\1>', s)
    try: return re.compile(s)
    except re.error: return None
# Chunk the indahl.ai part of the worker into top-level statements, so each route knows whether it answers from the asset folder only
# (then the file must exist in public/) or answers itself (KV, a handler, an inline response, a redirect).
chunks, cur = [], []
for line in IBLOCK.split('\n'):
    if re.match(r'^ {4,6}(if \(|\{$|const |let )', line) and cur: chunks.append('\n'.join(cur)); cur = []
    cur.append(line)
if cur: chunks.append('\n'.join(cur))
SELF = re.compile(r'IRIS_BENCH|handle[A-Z]\w*\(|tape_commits|Response\.redirect|new Response\((?!r\.body|a\.body|q\.body|g\.body)|INDAHL_PAGES|GATE\.')
routes = []   # (kind, matcher, needs_file)
for c in chunks:
    if 'pathname' not in c: continue
    needs_file = 'env.ASSETS' in c and not SELF.search(c)
    if 'INDAHL_PAGES["/404"]' in c: needs_file = 'env.ASSETS' in c   # answers from the asset folder, else the 404 page
    for s in re.findall(r'u\.pathname === "([^"]+)"', c): routes.append(('eq', s, needs_file))
    for arr in re.findall(r'\[((?:"[^"]*",?\s*)+)\]\.includes\(u\.pathname\)', c):
        for s in re.findall(r'"([^"]+)"', arr): routes.append(('eq', s, needs_file))
    for s in re.findall(r'u\.pathname\.startsWith\("([^"]+)"\)', c): routes.append(('pre', s, needs_file))
    for m in REGEX_LIT.finditer(c):
        rx = js_regex(m.group(1))
        if rx and 'pathname' in c[m.end():m.end() + 40]: routes.append(('rx', rx, needs_file))
MOVED = dict(re.findall(r'"(/[^"]*)":\s*"(/[^"]*)"', re.search(r'const MOVED = \{([^}]*)\}', W).group(1)))
PDFS = re.findall(r'"(/[^"]+)"', re.search(r'const PDFS = \[([^\]]*)\]', W).group(1))
# handler modules the worker imports answer their own paths (each returns a response or null)
for mod in re.findall(r'from "\.\./\.\./indahl-ai/([a-z]+\.js)"', W):
    if mod == 'pages.js': continue
    t = open(os.path.join(IA, mod), encoding='utf-8', errors='replace').read()
    for s in re.findall(r'''(?:===|!==)\s*['"](/[^'"\s]*)['"]''', t): routes.append(('eq', s, False))
    for s in re.findall(r'''['"](/[a-z0-9._/-]+)['"]\s*:''', t): routes.append(('eq', s, False))
    for s in re.findall(r'''startsWith\(['"](/[^'"]+)['"]\)''', t): routes.append(('pre', s, False))
    for m in REGEX_LIT.finditer(t):
        rx = js_regex(m.group(1))
        if rx: routes.append(('rx', rx, False))   # a handler module's path patterns (route tests and consts such as SIG_BASE)
# ---- the built pages --------------------------------------------------------------------------------------------------
PJ = open(os.path.join(IA, 'pages.js'), encoding='utf-8', errors='replace').read()
FILES = dict(re.findall(r"import (P\d+) from '\./([^']+)'", PJ))
PATHS = {k: v for k, v in re.findall(r'''['"](/[^'"]*)['"]\s*:\s*(P\d+)''', PJ)}
PAGES = set(PATHS)
def pub(p): return os.path.isfile(os.path.join(PUB, unquote(p).lstrip('/')))
def indahl_ok(p):
    if p in ('', '/'): return True
    n = re.sub(r'/index\.html$', '/', p); n = re.sub(r'\.html$', '', n)
    if len(n) > 1: n = n.rstrip('/')
    if n in PAGES or p in MOVED or p in PDFS: return True
    if p.startswith('/r/') and (pub(p + '.html') or pub(p.rstrip('/') + '/index.html')): return True
    for kind, m, needs_file in routes:
        hit = (kind == 'eq' and p == m) or (kind == 'pre' and p.startswith(m)) or (kind == 'rx' and m.search(p))
        if hit and (not needs_file or pub(p)): return True
    return False
QS = dict(re.findall(r'"(/[^"]*)":\s*"(/[^"]*)"', re.search(r'const QS = \{([^}]*)\}', QBLOCK).group(1)))
QRX = [js_regex(m.group(1)) for m in REGEX_LIT.finditer(QBLOCK) if '.test(p)' in QBLOCK[m.end():m.end() + 10]]
def qia_ok(p):
    q = p if re.search(r'\.(jpg|svg|txt|xml|pdf)$', p) else (re.sub(r'/+$', '', re.sub(r'\.html$', '', p)) or '/')
    if q in QS: return q == '/' or pub(QS[q]) or pub(QS[q] + '.html')
    for rx in QRX:
        if rx and rx.search(q):
            if rx.pattern.startswith('^/qia/'):
                if pub(q) or indahl_ok(q): return True   # served from the indahl.ai asset folder, or (21 Nov 2026) passed through to the indahl.ai side of the worker
            elif pub('/_qiasite' + q + '.html') or pub('/_qiasite' + q): return True
    return False
# ---- scan -------------------------------------------------------------------------------------------------------------
REF = re.compile(r'''\b(?:href|src)\s*=\s*["']([^"'<>]+)["']''', re.I)
SRCSET = re.compile(r'''\bsrcset\s*=\s*["']([^"']+)["']''', re.I)
# data loads in scripts (21 Nov 2026): string literals that start with one '/', taken when handed to a loader call or ending in a data extension
LIT = re.compile(r'''(["'`])(/(?!/)[^"'`\s<>]*)\1''')
DATAEXT = re.compile(r'\.(json|csv|tsv|txt|xml|ndjson|geojson|zip|pdf|js|wasm|stl|bin)$', re.I)
LOADER = re.compile(r'(?:\bfetch|\bJ|\bget[Jj][Ss][Oo][Nn]|\bimportScripts|\.register|\bEventSource|\bload[A-Z]\w*|\bloadAsync|\bsendBeacon)\(\s*$')
def loads(js):
    js = re.sub(r'/\*[\s\S]*?\*/', '', js); js = re.sub(r'(?m)^\s*//.*$', '', js)
    out = set()
    for m in LIT.finditer(js):
        s, pre, post = m.group(2), js[max(0, m.start() - 40):m.start()], js[m.end():m.end() + 4]
        if re.search(r'\+\s*$', pre): continue   # the tail of a URL built at run time; its prefix literal is the one checked
        dyn = bool(re.match(r'\s*\+', post))
        if m.group(1) == '`' and '${' in s: s, dyn = s.split('${')[0], True
        path = s.split('#')[0]
        if '?' in path: path, dyn = path.split('?')[0], False   # only the query is built at run time; the path is whole
        if path in ('', '/') or not (LOADER.search(pre) or DATAEXT.search(path)): continue
        out.add((path, dyn))
    return out
SCRIPT = re.compile(r'''<script\b[^>]*\bsrc\s*=\s*["']([^"'<>]+)["']''', re.I)
def js_file(host, path):
    for f in ((os.path.join(PUB, '_qiasite', path.lstrip('/')),) if host == 'quantumidleaudit.com' else ()) + (os.path.join(PUB, unquote(path).lstrip('/')),):
        if os.path.isfile(f): return f
    return None
def built():
    for var, rel in FILES.items():
        f = os.path.join(IA, rel)
        if os.path.exists(f):
            path = next((k for k, v in PATHS.items() if v == var), '/' + rel[:-5])
            yield 'https://indahl.ai' + path, open(f, encoding='utf-8', errors='replace').read()
    for f in sorted(glob.glob(os.path.join(PUB, '_qiasite', '*.html'))):
        n = os.path.basename(f)[:-5]
        yield 'https://quantumidleaudit.com/' + ('' if n == 'index' else n), open(f, encoding='utf-8', errors='replace').read()
dead = {}
dyn_bad, dyn_used, scripts = {}, set(), {}   # scripts: (host, file) -> pages that load it
npages = nrefs = nloads = 0
def check_load(host, path, dyn, where):
    global nloads
    nloads += 1; key = host + path
    if dyn:
        hit = next((k for k in ALLOW_DYNAMIC if key.startswith(k)), None)
        if hit: dyn_used.add(hit)
        else: dyn_bad.setdefault(key, set()).add(where)
        return
    if key in ALLOW: return
    ok = indahl_ok(path) if host == 'indahl.ai' else qia_ok(path)
    if not ok: dead.setdefault(key, set()).add(where + ' (data load)' if not where.endswith(" url") else where + " (served URL)")
for page, h in built():
    npages += 1
    body = re.sub(r'<!--[\s\S]*?-->', '', h)
    refs = set(REF.findall(body))
    for s in SRCSET.findall(body): refs |= {x.strip().split()[0] for x in s.split(',') if x.strip()}
    ph = urlparse(page).hostname; pn = page.replace('https://', '')
    for attrs, blk in re.findall(r'<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)</script>', body, re.I):
        if 'json' in attrs.lower(): continue   # JSON-LD and data islands are not scripts
        for path, dyn in loads(blk): check_load(ph, path, dyn, pn + ' inline script')
    for src in SCRIPT.findall(body):
        u = urlparse(urljoin(page, html.unescape(src.strip()))); host = (u.hostname or '').removeprefix('www.')
        if host in ('indahl.ai', 'quantumidleaudit.com') and u.path.endswith('.js'):
            f = js_file(host, u.path)
            if f: scripts.setdefault((host, f), set()).add(pn)
    for r in refs:
        r = html.unescape(r.strip())
        if not r or r.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:', '{', '$')) or '${' in r or '__' in r: continue
        u = urlparse(urljoin(page, r))
        host = (u.hostname or '').removeprefix('www.')
        if u.scheme not in ('http', 'https') or host not in ('indahl.ai', 'quantumidleaudit.com'): continue
        nrefs += 1
        key = host + u.path
        if key in ALLOW: continue
        ok = indahl_ok(u.path) if host == 'indahl.ai' else qia_ok(u.path)
        if not ok: dead.setdefault(key, set()).add(page.replace('https://', ''))
# the worker's handler modules hand out page URLs too (the MCP division list in api.js: url: 'https://indahl.ai/<desk>'); each must resolve (21 Nov 2026)
for mod in sorted(set(re.findall(r'from "\.\./\.\./indahl-ai/([a-z_]+\.m?js)"', W)) - {'pages.js'}):
    t = re.sub(r'(?m)^\s*//.*$', '', open(os.path.join(IA, mod), encoding='utf-8', errors='replace').read())
    for host, path in re.findall(r'''\burl:\s*['"`]https://(?:www\.)?(indahl\.ai|quantumidleaudit\.com)(/[^'"`#?\s]*)''', t):
        check_load(host, path or '/', False, 'indahl-ai/' + mod + ' url')
# every script the pages load, and any script those load in turn (pwa.js registers sw.js)
done, todo = set(), list(scripts)
while todo:
    host, f = todo.pop()
    if (host, f) in done: continue
    done.add((host, f)); name = os.path.relpath(f, PUB)
    for path, dyn in loads(open(f, encoding='utf-8', errors='replace').read()):
        check_load(host, path, dyn, name)
        if not dyn and path.endswith('.js'):
            g = js_file(host, path)
            if g and (host, g) not in done: todo.append((host, g))
for k in sorted(dyn_bad):
    print('  UNREVIEWED RUN-TIME URL %s...  <- %s  (list its prefix in ALLOW_DYNAMIC with a reason, or load a fixed path)' % (k, ', '.join(sorted(dyn_bad[k])[:4])))
for k in sorted(set(ALLOW_DYNAMIC) - dyn_used): print('  note: ALLOW_DYNAMIC %s is no longer loaded by any served script; drop it' % k)
for k in sorted(dead):
    pg = sorted(dead[k]); print('  DEAD %s  <- %s%s' % (k, ', '.join(pg[:4]), ' (+%d more)' % (len(pg) - 4) if len(pg) > 4 else ''))
print('link gate: %d dead same-site links and data loads across %d built pages and %d scripts (%d references, %d data loads checked; %d allowed exceptions, %d run-time prefixes, %d unreviewed)' % (len(dead), npages, len(done), nrefs, nloads, len(ALLOW), len(dyn_used), len(dyn_bad)))
# 21 Nov 2026 (coordinator): no helper's backup ships. Any backup-shaped file in the served folder is refused, listed one per line.
import fnmatch
BAKPAT = ('*.bak*', '*.pre-*', '*.orig', '*~', '*.new')
baks = sorted(os.path.relpath(os.path.join(r, f), PUB) for r, ds, fs in os.walk(PUB) for f in fs if any(fnmatch.fnmatch(f, x) for x in BAKPAT))
for f in baks: print('  BACKUP IN SERVED FOLDER public/%s  (move it outside cloudflare-workers/heuremen-door/public/)' % f)
print('backup files in public/: %d' % len(baks))
if baks and '--report' not in sys.argv: print('SHIP REFUSED: backup files in the served folder (lines above)'); sys.exit(1)
if (dead or dyn_bad) and '--report' not in sys.argv: print('SHIP REFUSED: a link on our own pages points nowhere (lines above)'); sys.exit(1)
