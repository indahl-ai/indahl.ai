#!/usr/bin/env python3
"""fetch_stated.py: DEUS stated side, phase 1 (fetch and quote, no comparison).
Reads stated_sources.json (the lab pages the plan names: model cards, system cards, launch posts), fetches each URL politely
(robots.txt respected, one request every PACE seconds per host, a user agent naming this desk), and saves under raw/stated/<host>/:
  <slug>.<html|pdf|txt>    the bytes as served (untrusted, never executed)
  <slug>.text.txt          the visible text (HTML tags stripped, scripts and styles dropped; PDF text by pypdf)
  <slug>.meta.json         URL, final URL, fetch time UTC, status, content type, size, sha256
Then, for every benchmark the source entry names, it writes quote candidates to raw/stated/quotes.jsonl: each line of the page text
that holds the benchmark's name (or an alias) and a number, with the URL and the fetch date. The quoted score is chosen from these
candidates in the reader by the plan's rules, and every chosen score must appear verbatim in a saved quote (row numbers gate).
Computes nothing stated-vs-rerun. Usage: python3 -I fetch_stated.py [--only <id>] [--force]

stated_sources.json: [{"id": "...", "lab": "...", "model": "...", "url": "...", "kind": "model card|system card|launch post",
                       "benchmarks": {"GPQA Diamond": ["GPQA Diamond", "GPQA"], ...}}, ...]"""
import os, sys, io, re, json, time, html, hashlib, urllib.request, urllib.error, urllib.robotparser, urllib.parse
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, 'raw', 'stated')
UA = 'heuremen-deus/0.1 (+https://indahl.ai/deus)'; PACE = 5.0; MAX = 60 * 1024 * 1024
_last = {}; _robots = {}

def wait(host):
    w = PACE - (time.time() - _last.get(host, 0))
    if w > 0: time.sleep(w)
    _last[host] = time.time()

def raw_get(url, timeout=90):
    host = urllib.parse.urlsplit(url).netloc; wait(host)
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,application/pdf,text/plain;q=0.9,*/*;q=0.5'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        b = r.read(MAX + 1)
        if len(b) > MAX: raise RuntimeError('too large')
        return b, r.geturl(), r.status, r.headers.get('Content-Type', '')

def allowed(url):
    p = urllib.parse.urlsplit(url); root = '%s://%s' % (p.scheme, p.netloc)
    if root not in _robots:
        rp = urllib.robotparser.RobotFileParser(); rp.set_url(root + '/robots.txt')
        try:
            b, _, st, _ = raw_get(root + '/robots.txt', timeout=30); rp.parse(b.decode('utf-8', 'replace').splitlines())
        except urllib.error.HTTPError as e:
            if e.code in (401, 403): rp.disallow_all = True
            else: rp.allow_all = True   # no robots.txt (404): crawling allowed by convention
        except Exception: rp.disallow_all = True   # unreadable: do not fetch
        _robots[root] = rp
    return _robots[root].can_fetch(UA, url)

def html_text(b):
    t = b.decode('utf-8', 'replace')
    t = re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>', ' ', t)
    t = re.sub(r'(?i)<br\s*/?>|</(p|div|li|tr|h[1-6]|table|section|article|header|footer)>', '\n', t)
    t = re.sub(r'(?i)</t[dh]>', ' | ', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    lines = [re.sub(r'[ \t\u00a0]+', ' ', x).strip() for x in t.split('\n')]
    return '\n'.join(x for x in lines if x)

def pdf_text(b):
    import pypdf
    r = pypdf.PdfReader(io.BytesIO(b)); out = []
    for i, pg in enumerate(r.pages):
        try: out.append('[page %d]\n%s' % (i + 1, pg.extract_text() or ''))
        except Exception as e: out.append('[page %d unreadable: %s]' % (i + 1, type(e).__name__))
    return '\n'.join(out)

NUM = re.compile(r'\d+(?:\.\d+)?\s*%?')
def quotes(text, aliases):
    out = []
    lines = text.split('\n')
    for i, ln in enumerate(lines):
        low = ln.lower()
        if any(a.lower() in low for a in aliases) and NUM.search(ln):
            out.append(dict(line_no=i + 1, line=ln[:600], next=(lines[i + 1][:300] if i + 1 < len(lines) else '')))
    return out

IMG_ALT = re.compile(r'(?i)benchmark|table|evaluat|eval\b|results|performance|comparison|chart')
def table_images(page, base_url, base):
    """Benchmark tables printed as images: save each <img> whose alt text names a table, benchmark, evaluation or chart (largest srcset
    candidate), with its alt text, so the score can be transcribed from the lab's own image. Saved bytes are images, never executed."""
    out = []
    for m in re.finditer(r'(?is)<img\b([^>]*)>', page):
        a = m.group(1); alt = re.search(r'(?is)\balt="([^"]*)"', a); alt = html.unescape(alt.group(1)) if alt else ''
        if alt and not IMG_ALT.search(alt): continue   # empty alt kept: some labs print the table as an image with no alt text
        src = None; ss = re.search(r'(?is)\bsrcset="([^"]*)"', a)
        if ss:
            c = [x.strip().split(' ') for x in html.unescape(ss.group(1)).split(',') if x.strip()]
            c = sorted(c, key=lambda p: int(re.sub(r'\D', '', p[1]) or 0) if len(p) > 1 else 0); src = c[-1][0] if c else None
        if not src:
            s2 = re.search(r'(?is)\bsrc="([^"]*)"', a); src = html.unescape(s2.group(1)) if s2 else None
        if not src or src.startswith('data:'): continue
        u = urllib.parse.urljoin(base_url, src)
        if any(o['url'] == u for o in out): continue
        rec = dict(alt=alt[:300], url=u)
        try:
            if allowed(u):
                b, _, _, ct = raw_get(u, timeout=60)
                ext = {'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp', 'image/avif': 'avif', 'image/svg+xml': 'svg.txt'}.get(ct.split(';')[0].strip(), 'img')
                p = '%s.img%d.%s' % (base, len(out) + 1, ext); open(p, 'wb').write(b)
                rec.update(saved=os.path.relpath(p, H), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), content_type=ct)
            else: rec['status'] = 'ROBOTS_DISALLOWED'
        except Exception as e: rec['status'] = 'NOTHING_RETURNED'; rec['error'] = repr(e)[:120]
        out.append(rec)
    return out

def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:80]

def main():
    src = json.load(open(os.path.join(H, 'stated_sources.json')))
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None; force = '--force' in sys.argv
    qpath = os.path.join(OUT, 'quotes.jsonl'); os.makedirs(OUT, exist_ok=True)
    done = set()
    if os.path.exists(qpath) and not force:
        for l in open(qpath): done.add(json.loads(l)['id'])
    log = open(os.path.join(OUT, 'fetch_log.jsonl'), 'a')
    for s in src:
        if only and s['id'] != only: continue
        if s['id'] in done and not force: continue
        url = s['url']; host = urllib.parse.urlsplit(url).netloc; d = os.path.join(OUT, slug(host)); os.makedirs(d, exist_ok=True)
        rec = dict(id=s['id'], url=url, fetched_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        if not allowed(url):
            rec.update(status='ROBOTS_DISALLOWED'); log.write(json.dumps(rec) + '\n'); log.flush(); print(s['id'], 'robots disallows'); continue
        try:
            b, final, st, ct = raw_get(url)
        except Exception as e:
            rec.update(status='NOTHING_RETURNED', error=repr(e)[:200]); log.write(json.dumps(rec) + '\n'); log.flush(); print(s['id'], 'failed', repr(e)[:100]); continue
        ispdf = b[:5] == b'%PDF-' or 'pdf' in ct.lower()
        ext = 'pdf' if ispdf else ('txt' if 'text/plain' in ct.lower() else 'html')
        base = os.path.join(d, slug(s['id'])); open(base + '.' + ext, 'wb').write(b)
        try: text = pdf_text(b) if ispdf else (b.decode('utf-8', 'replace') if ext == 'txt' else html_text(b))
        except Exception as e: text = ''; rec['text_error'] = repr(e)[:200]
        open(base + '.text.txt', 'w', encoding='utf-8').write(text)
        rec.update(status=st, final_url=final, content_type=ct, bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), saved=os.path.relpath(base + '.' + ext, H),
                   text=os.path.relpath(base + '.text.txt', H), text_chars=len(text), lab=s.get('lab'), model=s.get('model'), kind=s.get('kind'))
        if not ispdf and ext == 'html': rec['images'] = table_images(b.decode('utf-8', 'replace'), final, base)
        json.dump(rec, open(base + '.meta.json', 'w'), indent=1)
        with open(qpath, 'a', encoding='utf-8') as q:
            for bench, aliases in (s.get('benchmarks') or {}).items():
                cands = quotes(text, aliases)
                q.write(json.dumps(dict(id=s['id'], lab=s.get('lab'), model=s.get('model'), benchmark=bench, url=url, fetched_utc=rec['fetched_utc'],
                                        candidates=cands, nothing_found=not cands), ensure_ascii=False) + '\n')
        log.write(json.dumps(rec) + '\n'); log.flush()
        print(s['id'], st, ext, len(b), 'bytes,', len(text), 'chars')

if __name__ == '__main__': main()
