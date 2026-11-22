#!/usr/bin/env python3
"""vk_fetch.py: VOIGHT-KAMPFF fetcher (plan: PLAN.md, sealed in data/plan_seal.json). Fetches only, computes nothing stated-vs-measured.

  python3 -I vk_fetch.py tests     the independent tests' released files (sources.json "tests"), into data/raw/tests/<test>/
  python3 -I vk_fetch.py stated    each maker's page live, and the Internet Archive capture list (CDX) for the same URL, into data/raw/stated/<maker>/
  python3 -I vk_fetch.py captures  for each test date in sources.json, the latest capture of the maker's page on or before it, into data/raw/stated/<maker>/

Every download is untrusted data: saved as bytes, read as data only, never executed or imported. One request at a time, PACE seconds apart per host,
robots.txt read first, a user agent that names this desk. Each saved file gets a .meta.json with URL, final URL, time, status, size and sha256.
Refuses to run unless PLAN.md matches the seal. Standard library only."""
import os, sys, re, json, time, hashlib, html, urllib.request, urllib.error, urllib.robotparser, urllib.parse
H = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(H, 'data', 'raw')
UA = 'heuremen-voightkampff/0.1 (+https://indahl.ai/voightkampff)'; PACE = 2.0; MAX = 80 * 1024 * 1024
_last, _robots = {}, {}
sys.path.insert(0, H)


def sealed():
    s = json.load(open(os.path.join(H, 'data', 'plan_seal.json')))
    return hashlib.sha256(open(os.path.join(H, 'PLAN.md'), 'rb').read()).hexdigest() == s['plan_sha256']


def _wait(host):
    w = PACE - (time.time() - _last.get(host, 0))
    if w > 0: time.sleep(w)
    _last[host] = time.time()


def raw_get(url, timeout=120):
    host = urllib.parse.urlsplit(url).netloc; _wait(host)
    import heuremen_kit as K
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    with K.opener().open(req, timeout=timeout) as r:
        b = r.read(MAX + 1)
        if len(b) > MAX: raise RuntimeError('larger than %d bytes' % MAX)
        return b, r.geturl(), r.status, r.headers.get('Content-Type', '')


def allowed(url):
    p = urllib.parse.urlsplit(url); root = '%s://%s' % (p.scheme, p.netloc)
    if root not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        try:
            b, _, _, _ = raw_get(root + '/robots.txt', timeout=30); rp.parse(b.decode('utf-8', 'replace').splitlines())
        except urllib.error.HTTPError as e:
            if e.code in (401, 403): rp.disallow_all = True
            else: rp.allow_all = True
        except Exception: rp.disallow_all = True
        _robots[root] = rp
    return _robots[root].can_fetch(UA, url)


def html_text(b):
    t = b.decode('utf-8', 'replace')
    t = re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>', ' ', t)
    t = re.sub(r'(?i)<br\s*/?>|</(p|div|li|tr|h[1-6]|table|section|article|header|footer|span)>', '\n', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    lines = [re.sub(r'[ \t\u00a0]+', ' ', x).strip() for x in t.split('\n')]
    return '\n'.join(x for x in lines if x)


def save(url, dest, robots=True, text=False):
    """Fetch url into dest (bytes as served) with dest.meta.json. Returns the meta dict. Skips a file already saved."""
    meta_p = dest + '.meta.json'
    if os.path.exists(meta_p):
        m = json.load(open(meta_p))
        if m.get('status') == 200: return m
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    m = dict(url=url, fetched_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    if robots and not allowed(url):
        m.update(status='ROBOTS_DISALLOWED'); json.dump(m, open(meta_p, 'w'), indent=1); return m
    try: b, final, st, ct = raw_get(url)
    except urllib.error.HTTPError as e: m.update(status=e.code, error='HTTP %d' % e.code); json.dump(m, open(meta_p, 'w'), indent=1); return m
    except Exception as e: m.update(status='NOTHING_RETURNED', error=repr(e)[:200]); json.dump(m, open(meta_p, 'w'), indent=1); return m
    open(dest, 'wb').write(b)
    m.update(status=st, final_url=final, content_type=ct, bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), saved=os.path.relpath(dest, H))
    if text:
        open(dest + '.text.txt', 'w', encoding='utf-8').write(html_text(b)); m['text'] = os.path.relpath(dest + '.text.txt', H)
    json.dump(m, open(meta_p, 'w'), indent=1)
    return m


def tests(S):
    for t in S['tests']:
        for f in t['files']:
            m = save(f['url'], os.path.join(RAW, 'tests', t['id'], f['path']), robots=False)   # raw file hosts (GitHub, Hugging Face) serve released data for download
            print(t['id'], f['path'], m.get('status'), m.get('bytes'))


def cdx(url, dest):
    q = 'https://web.archive.org/cdx/search/cdx?' + urllib.parse.urlencode(dict(url=url, output='json', fl='timestamp,original,statuscode,digest', filter='statuscode:200', collapse='digest'))
    return save(q, dest, robots=False)


def stated(S):
    for mk in S['makers']:
        d = os.path.join(RAW, 'stated', mk['id'])
        m = save(mk['url'], os.path.join(d, 'live.html'), text=True); print(mk['id'], 'live', m.get('status'), m.get('bytes'))
        m = cdx(mk['url'], os.path.join(d, 'cdx.json')); print(mk['id'], 'cdx', m.get('status'), m.get('bytes'))


def captures(S):
    for mk in S['makers']:
        d = os.path.join(RAW, 'stated', mk['id']); p = os.path.join(d, 'cdx.json')
        try: rows = json.load(open(p))[1:]
        except Exception: rows = []
        for td in sorted({x['query_date'] for x in S['pairings'] if x['maker'] == mk['id'] and x.get('query_date')}):
            cut = td.replace('-', '') + '235959'
            prior = [r for r in rows if r[0] <= cut]
            if not prior: print(mk['id'], td, 'no capture on or before'); continue
            ts = prior[-1][0]; url = 'https://web.archive.org/web/%sid_/%s' % (ts, prior[-1][1])
            m = save(url, os.path.join(d, 'capture_%s.html' % ts), robots=False, text=True); print(mk['id'], td, ts, m.get('status'), m.get('bytes'))


if __name__ == '__main__':
    if not sealed(): sys.exit('vk_fetch: PLAN.md does not match data/plan_seal.json, refusing')
    S = json.load(open(os.path.join(H, 'sources.json')))
    {'tests': tests, 'stated': stated, 'captures': captures}[sys.argv[1]](S)
