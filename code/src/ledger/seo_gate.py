#!/usr/bin/env python3
"""seo_gate.py (21 Nov 2026, owner's SEO re-index: the sitemap had to stay right as the site grew, so it is now a build output and this gate holds it).
A ship gate on the BUILT output of indahl.ai, before deploy. Refuses (exit 1) when
  - a page the worker serves (indahl-ai/pages.js) has no <title>, an empty one, or more than one;
  - an indexable page (not in build_site.py NOINDEX, no noindex robots meta) is missing from indahl-ai/sitemap.xml;
  - the sitemap lists a page that is not built, a noindex page, or a retired page (ledger/desks.json "retired" plus RETIRED below);
  - the sitemap the worker serves (SITEMAP in pages.js) differs from indahl-ai/sitemap.xml;
  - an indexable page has no canonical, or its canonical is not https://indahl.ai<its own path>;
  - the worker's robots.txt drops the Sitemap line or disallows the whole site to every crawler, Googlebot or Bingbot.
indahl.ai only (quantumidleaudit.com is not indexed yet, owner 21 Nov).
  python3 ledger/seo_gate.py            exit 1 on any finding
  python3 ledger/seo_gate.py --report   list, always exit 0"""
import json, os, re, sys
B = os.path.expanduser('~/forge'); IA = os.path.join(B, 'indahl-ai'); SITE = 'https://indahl.ai'
RETIRED = ['/stack', '/coin', '/qia/process', '/brand', '/newsletter', '/trackrecord', '/plan']   # and everything under each
def main():
    errs = []
    pj = open(os.path.join(IA, 'pages.js'), encoding='utf-8').read()
    imp = dict(re.findall(r"import (P\d+) from '\./([^']+)';", pj))
    table = re.findall(r"^  '([^']+)': (P\d+)", pj, re.M)
    pages = {p: imp[v] for p, v in table}
    if len(pages) < 50: errs.append('pages.js lists only %d pages; refusing to read it as the site' % len(pages))
    src = open(os.path.join(IA, 'build_site.py'), encoding='utf-8').read()
    m = re.search(r'^NOINDEX = (\{[^}]*\})', src, re.M)
    noindex = set(eval(m.group(1), {})) if m else set()
    if not m: errs.append('NOINDEX not found in build_site.py')
    d = json.load(open(os.path.join(B, 'ledger', 'desks.json'), encoding='utf-8'))
    retired = set(RETIRED) | {'/' + str(x).strip('/') for x in d.get('retired', [])}
    sm = open(os.path.join(IA, 'sitemap.xml'), encoding='utf-8').read()
    locs = re.findall(r'<loc>([^<]*)</loc>', sm)
    paths = [l[len(SITE):] or '/' for l in locs]
    sj = re.search(r'^export const SITEMAP = (".*");$', pj, re.M)
    if not sj: errs.append('pages.js exports no SITEMAP (the worker would serve nothing)')
    elif json.loads(sj.group(1)) != sm: errs.append('SITEMAP in pages.js differs from indahl-ai/sitemap.xml')
    if len(paths) != len(set(paths)): errs.append('sitemap lists a URL twice')
    for l in locs:
        if not l.startswith(SITE + '/'): errs.append('sitemap URL on another host: %s' % l)
    indexable = set()
    for p, f in pages.items():
        try: doc = open(os.path.join(IA, f), encoding='utf-8').read()
        except Exception as e: errs.append('%s: built file %s unreadable (%s)' % (p, f, type(e).__name__)); continue
        head = doc.split('</head>')[0]
        t = re.findall(r'<title[^>]*>(.*?)</title>', head, re.S)
        if len(t) != 1 or not t[0].strip(): errs.append('%s: %d title tags%s' % (p, len(t), ', empty' if t and not t[0].strip() else ''))
        if p in noindex or re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', head): continue
        indexable.add(p)
        c = re.findall(r'<link\s+rel="canonical"\s+href="([^"]*)"', head)
        want = SITE + ('/' if p == '/' else p)
        if c != [want]: errs.append('%s: canonical %s, want %s' % (p, c or 'none', want))
    for p in sorted(indexable - set(paths)): errs.append('%s: live and indexable, missing from the sitemap' % p)
    for p in paths:
        if p not in pages: errs.append('%s: in the sitemap, not a built page' % p)
        elif p not in indexable: errs.append('%s: in the sitemap, but noindex' % p)
        if any(p == r or p.startswith(r + '/') for r in retired): errs.append('%s: retired page in the sitemap' % p)
    w = open(os.path.join(B, 'cloudflare-workers', 'heuremen-door', 'worker.js'), encoding='utf-8').read()
    rm = re.search(r'u\.pathname === "/robots\.txt"\) return new Response\("((?:[^"\\]|\\.)*)"', w)
    if not rm: errs.append('worker.js: robots.txt route not found')
    else:
        rob = json.loads('"' + rm.group(1) + '"')
        if 'Sitemap: %s/sitemap.xml' % SITE not in rob: errs.append('robots.txt: no Sitemap line')
        for grp in re.split(r'\n\s*\n', rob):
            uas = [x.split(':', 1)[1].strip().lower() for x in grp.splitlines() if x.lower().startswith('user-agent:')]
            if set(uas) & {'*', 'googlebot', 'bingbot'} and re.search(r'^Disallow:\s*/\s*$', grp, re.M): errs.append('robots.txt: the whole site is disallowed for %s' % ', '.join(uas))
    print('seo_gate: %d pages served, %d indexable, %d in the sitemap, %d finding%s' % (len(pages), len(indexable), len(paths), len(errs), '' if len(errs) == 1 else 's'))
    for e in errs[:60]: print('  ' + e)
    if len(errs) > 60: print('  ... and %d more' % (len(errs) - 60))
    return 1 if errs and '--report' not in sys.argv else 0
if __name__ == '__main__': sys.exit(main())
