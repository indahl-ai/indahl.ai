"""site_gate.py [--list] -- every published page checked against site_rules.json (the specbook made machine-readable, 23 Oct 2026).
Exit 1 on any breach. Runs in the heuremen.org / indahl-ai pre-commit hooks and in ledger/ship.sh."""
ONE_INQUIRY_ALLOW = ()   # 22 Nov: FW-028 landed; no page is excused
import json, re, os, html, sys, glob, fnmatch
B = os.path.expanduser('~/forge'); R = json.load(open(os.path.join(B, 'heuremen-specbook', 'site_rules.json')))
_FILE = os.path.abspath(sys.argv[sys.argv.index('--file') + 1]) if '--file' in sys.argv else None   # 22 Nov 2026: --file <path> checks one rendered page (pagebuilder/desk_publish.py), as an indahl.ai page
_QIA = os.path.abspath(sys.argv[sys.argv.index('--qia') + 1]) if '--qia' in sys.argv else None   # 22 Nov 2026 (QIA split): --qia <dir> checks the built quantumidleaudit.com files (ledger/ship_qia.sh)
_QIA_FILES = (sorted(glob.glob(os.path.join(_QIA, '**', '*.html'), recursive=True)) + sorted(glob.glob(os.path.join(_QIA, '**', '*.js'), recursive=True))) if _QIA else []
def pages():
    if _FILE: yield 'indahl.ai', os.path.relpath(_FILE, B); return
    if _QIA:
        for p in _QIA_FILES:
            if p.endswith('.html'): yield 'quantumidleaudit.com', os.path.relpath(p, B)
        return
    for site, globs in R['pages'].items():
        for g in globs:
            for p in sorted(glob.glob(os.path.join(B, g), recursive=True)):
                rel = os.path.relpath(p, B)
                if not any(fnmatch.fnmatch(rel, s) for s in R['skip']): yield site, rel
bad = 0; n = 0
for site, rel in pages():
    n += 1; s = open(os.path.join(B, rel), encoding='utf-8', errors='replace').read()
    for f in R['forbid']:
        if f['where'] in ('all', site) and re.search(f['pattern'], s):
            print(f'  BREACH {f["rule"]:5} {rel}: {f["why"]}'); bad += 1
    ft = R['footer']
    if ft['where'] == site and rel not in ft['exempt'] and ('class="foot"' in s or '<footer' in s):
        txt = lambda h: ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())
        blocks = [txt(b) for b in re.findall(r'<p class="foot">(.*?)</p>|<footer>(.*?)</footer>', s, re.S) for b in b if b]
        if txt(ft['html']) not in blocks:
            print(f'  BREACH {ft["rule"]:5} {rel}: no footer block reads exactly the specbook footer'); bad += 1
import importlib.util as _u
_spec = _u.spec_from_file_location('count_scan', os.path.join(B, 'heuremen-specbook', 'count_scan.py')); _cs = _u.module_from_spec(_spec); _spec.loader.exec_module(_cs)
_files = [os.path.join(B, rel) for _, rel in pages()] + ([] if (_FILE or _QIA) else [os.path.join(B, 'ligera', f) for f in ('FAULTS.html', 'GUARDS.html')])   # 30 Oct (HEU1-12): experiment pages included
for rel, hit, ctx in _cs.scan(_files):
    print(f'  BREACH 0b.5  {rel}: count in a title/heading/label: {hit!r}'); bad += 1
_spec2 = _u.spec_from_file_location('tone_scan', os.path.join(B, 'heuremen-specbook', 'tone_scan.py')); _ts = _u.module_from_spec(_spec2); _spec2.loader.exec_module(_ts)
for site, rel in pages():
    if site != 'indahl.ai': continue
    for kind, hit in _ts.scan(os.path.join(B, rel)):
        print(f'  BREACH 0b.8  {rel}: tone {kind}: {hit!r}'); bad += 1
# 30 Oct 2026 (the owner ... "read in full is the best"): public copy says "read in full", never "by hand".
HANDS = re.compile(r'(?i)\bby hand\b|\bhand[- ](?:read|check|count)|\bhand-?checked\b')
_nh = 0
_served = set(re.findall(r"from '\./([^']+\.html)'", open(os.path.join(B, 'indahl-ai', 'pages.js')).read())) if os.path.exists(os.path.join(B, 'indahl-ai', 'pages.js')) else set()   # only pages the site serves (held pages stay on disk unserved)
for p in [_FILE] if _FILE else _QIA_FILES if _QIA else [os.path.join(B, 'indahl-ai', s) for s in sorted(_served)] + sorted(glob.glob(os.path.join(B, 'cloudflare-workers', 'heuremen-door', 'public', '**', '*.js'), recursive=True)):
    rel = os.path.relpath(p, B)
    if any(fnmatch.fnmatch(rel, s) for s in R['skip']) or '.pre-' in rel: continue
    _nh += 1
    if p.endswith('.html'):   # 10 Nov 2026 (cold read BLOCK 1): rules with where "served" run on every served page, subfolders included
        _st = open(p, encoding='utf-8', errors='replace').read()
        for f in R['forbid']:
            if f['where'] == 'served' and re.search(f['pattern'], _st):
                print(f'  BREACH {f["rule"]:5} {rel}: {f["why"]}'); bad += 1
    for m in HANDS.finditer(open(p, encoding='utf-8', errors='replace').read()):
        print(f'  BREACH 0b.9  {rel}: say "read in full": {m.group(0)!r}'); bad += 1; break
    # 22 Nov 2026 (the owner): no client exit or renewal wording on sale pages.
    if p.endswith('.html') and re.search(r'(_qiasite|services|inquiry|pricing)', rel):
        m = re.search(r'(?i)(cancel any month|can be canceled any month|if you stop within|stopped within the 30 days|renews? (automatically|each)|auto-?renew|month[- ]to[- ]month)', open(p, encoding='utf-8', errors='replace').read())
        if m: print(f'  BREACH 0b.15 {rel}: client exit or renewal wording: {m.group(0)!r}'); bad += 1
    # 22 Nov 2026 (the owner): our own cadence and timing phrases.
    if p.endswith('.html') and not re.search(r'(privacy|/study/|/studies/|predictions|model_all)', rel):
        m = re.search(r'(?i)\b((checked|read|polled|refreshed|hashed|rebuilt|re-read|fetched) (about |roughly )?every (\d+ |half )?(minutes?|hours?|hour|days?|weeks?|months?)|(checked|read|polled) about (once a|daily|hourly|weekly)\b|within the hour|reported as it lands|on a fixed schedule)', open(p, encoding='utf-8', errors='replace').read())
        if m: print(f'  BREACH 0b.14 {rel}: no timeline about our actions: {m.group(0)!r}'); bad += 1
    # 22 Nov 2026 (the owner): no
    # reply-time promise on any page. He answers when he sits down to. Legal response times in the privacy notice are the law, not a promise.
    if p.endswith('.html') and not re.search(r'privacy', rel):
        m = re.search(r'(?i)\b(we (reply|respond|answer|acknowledge)|(answered|replied to|responded to|acknowledged)( by email)?)[^.<]{0,80}? within [^.<]{0,30}(days?|hours?)\b', open(p, encoding='utf-8', errors='replace').read())
        if m: print(f'  BREACH 0b.13 {rel}: no reply-time promise: {m.group(0)!r}'); bad += 1
    # 22 Nov 2026 (the owner): ONE inquiry
    # button per page. Counts links whose text is exactly Inquiry/Inquiries/Inquire, plus any btn-class link to an inquiry path. Prose
    # references in legal text ("the inquiry form") are not buttons. ONE_INQUIRY_ALLOW lists pages still being fixed (FW-028); empty it after.
    if p.endswith('.html') and not p.endswith('model_all.html'):
        _h = open(p, encoding='utf-8', errors='replace').read()
        _lab = re.findall(r'<a\b[^>]*>\s*Inquir(?:y|ies|e)\s*</a>', _h, re.I)
        _btn = [x for x in re.findall(r'<a\b[^>]*class="[^"]*btn[^"]*"[^>]*href="[^"]*(?:contact|inquir)[^"]*"[^>]*>', _h, re.I) if not re.search(r'>\s*Inquir', x)]
        _ninq = len(_lab) + len(_btn)
        if _ninq > 1 and not any(rel.endswith(a) for a in ONE_INQUIRY_ALLOW):
            print(f'  BREACH 0b.12 {rel}: {_ninq} inquiry buttons on one page (one only: the menu link "Inquiry")'); bad += 1
    # 22 Nov 2026 (the owner): the one contact button says "Inquiry", nothing longer.
    for m in re.finditer(r'(?i)\b(start (an|your) (engagement )?inquiry|begin (an )?inquiry|send an inquiry now|make an inquiry)\b', open(p, encoding='utf-8', errors='replace').read()):
        print(f'  BREACH 0b.11 {rel}: the button says "Inquiry", not {m.group(0)!r}'); bad += 1; break
    # 8 Nov 2026 (the owner): public copy says "house", never "flock".
    for m in re.finditer(r'(?i)\bflock', open(p, encoding='utf-8', errors='replace').read()):
        print(f'  BREACH 0b.10 {rel}: say "house", not "flock": {m.group(0)!r}'); bad += 1; break
print(f'site gate: {n} pages, {_nh} served files read for wording; breaches: {bad}'); sys.exit(1 if bad else 0)
