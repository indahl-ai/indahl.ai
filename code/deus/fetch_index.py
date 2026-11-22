#!/usr/bin/env python3
"""fetch_index.py: DEUS stated side, page discovery. Fetches each lab's public sitemap (named in its robots.txt), follows nested sitemaps,
and writes raw/stated/_index/<host>.urls.jsonl (url, lastmod). Used only to find the lab's own launch posts, model cards and system cards
dated in the frame. One request every 5 s per host, robots respected, untrusted XML parsed as text. No score is read here.
Usage: python3 -I fetch_index.py <host> [<host> ...]"""
import os, sys, re, json, gzip, time, urllib.request, urllib.robotparser
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, 'raw', 'stated', '_index'); os.makedirs(OUT, exist_ok=True)
UA = 'heuremen-deus/0.1 (+https://indahl.ai/deus)'; PACE = 5.0
ROOTS = {'openai.com': 'https://openai.com/sitemap.xml', 'www.anthropic.com': 'https://www.anthropic.com/sitemap.xml', 'x.ai': 'https://x.ai/sitemap.xml',
         'deepmind.google': 'https://deepmind.google/sitemap.xml', 'blog.google': 'https://blog.google/sitemap.xml',
         'ai.meta.com': 'https://ai.meta.com/sitemap/ai_meta_com_sitemap.xml.gz', 'api-docs.deepseek.com': 'https://api-docs.deepseek.com/sitemap.xml',
         'qwen.ai': 'https://qwen.ai/sitemap.xml'}
_last = [0.0]
def get(u):
    w = PACE - (time.time() - _last[0])
    if w > 0: time.sleep(w)
    _last[0] = time.time()
    with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=60) as r: b = r.read(50 * 1024 * 1024)
    if b[:2] == b'\x1f\x8b': b = gzip.decompress(b)
    return b.decode('utf-8', 'replace')
def crawl(host):
    rp = urllib.robotparser.RobotFileParser(); rp.parse(open(os.path.join(OUT, 'robots_%s.txt' % host)).read().splitlines())
    seen, todo, urls = set(), [ROOTS[host]], []
    while todo and len(seen) < 400:
        u = todo.pop(0)
        if u in seen or not rp.can_fetch(UA, u): continue
        seen.add(u)
        try: x = get(u)
        except Exception as e: print(host, 'failed', u, repr(e)[:80], file=sys.stderr); continue
        if '<sitemapindex' in x[:2000]:
            todo += [m for m in re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', x)]
            continue
        for blk in re.findall(r'<url>(.*?)</url>', x, re.S):
            loc = re.search(r'<loc>\s*([^<\s]+)\s*</loc>', blk); lm = re.search(r'<lastmod>\s*([^<\s]+)\s*</lastmod>', blk)
            if loc: urls.append(dict(url=loc.group(1).replace('&amp;', '&'), lastmod=lm.group(1) if lm else None))
    with open(os.path.join(OUT, host + '.urls.jsonl'), 'w') as f:
        for r in urls: f.write(json.dumps(r) + '\n')
    print(host, len(seen), 'sitemaps', len(urls), 'urls')
if __name__ == '__main__':
    for h in sys.argv[1:]: crawl(h)
