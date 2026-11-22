#!/usr/bin/env python3
"""fetch_reruns.py: DEUS independent side, phase 1 (fetch only, no reading).
Epoch AI Benchmarking Hub public download (https://epoch.ai/data/benchmark_data.zip, CC BY 4.0, keyless), linked from
https://epoch.ai/benchmarks/use-this-data#downloads. Saves the ZIP bytes untouched under raw/epoch/<UTC date>/, then unpacks only
.csv members (names flattened, no paths kept, nothing executed) beside it, and writes a manifest with URL, fetch time, size and sha256.
The bytes are untrusted: they are read as text by the reader later and never run. Computes nothing stated-vs-rerun (plan before reading).
Polite: one request, a user agent naming this desk, robots.txt checked first (epoch.ai disallows /assets/ and some benchmark problems, not /data/).
Usage: python3 -I fetch_reruns.py [--force]"""
import os, sys, io, json, time, zipfile, hashlib, urllib.request, urllib.robotparser
H = os.path.dirname(os.path.abspath(__file__))
UA = 'heuremen-deus/0.1 (+https://indahl.ai/deus)'
SOURCES = {
    'epoch': dict(url='https://epoch.ai/data/benchmark_data.zip', page='https://epoch.ai/benchmarks/use-this-data',
                  robots='https://epoch.ai/robots.txt', licence='CC BY 4.0 (Epoch AI, Capabilities & benchmarking); external rows keep their own licence'),
}
MAX_BYTES = 200 * 1024 * 1024

def get(url, timeout=120):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout) as r:
        b = r.read(MAX_BYTES + 1)
        if len(b) > MAX_BYTES: raise RuntimeError('too large')
        return b, r.geturl(), dict(r.headers)

def allowed(robots_url, url):
    rp = urllib.robotparser.RobotFileParser(); rp.set_url(robots_url)
    try:
        rp.parse(get(robots_url)[0].decode('utf-8', 'replace').splitlines())
    except Exception as e:
        print('robots unreadable, not fetching:', e, file=sys.stderr); return False
    return rp.can_fetch(UA, url)

def fetch(name, s, force=False):
    day = time.strftime('%Y%m%d', time.gmtime()); d = os.path.join(H, 'raw', name, day); os.makedirs(d, exist_ok=True)
    zp = os.path.join(d, os.path.basename(s['url']))
    if os.path.exists(zp) and not force: print(name, 'already fetched today:', zp); return
    if not allowed(s['robots'], s['url']): print(name, 'robots.txt disallows', s['url'], file=sys.stderr); return
    time.sleep(3)
    b, final, hdr = get(s['url'])
    open(zp + '.part', 'wb').write(b); os.replace(zp + '.part', zp)
    members = []
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        for info in z.infolist():
            base = os.path.basename(info.filename)
            if info.is_dir() or not base.lower().endswith('.csv') or base.startswith('.'): continue
            if info.file_size > MAX_BYTES: continue
            data = z.read(info)
            out = os.path.join(d, 'csv', base); os.makedirs(os.path.dirname(out), exist_ok=True)
            if os.path.exists(out): out = os.path.join(d, 'csv', info.filename.replace('/', '__'))
            open(out, 'wb').write(data)
            members.append(dict(member=info.filename, saved=os.path.relpath(out, H), bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    man = dict(source=name, url=s['url'], final_url=final, page=s['page'], licence=s['licence'], user_agent=UA,
               fetched_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(),
               last_modified=hdr.get('Last-Modified'), etag=hdr.get('ETag'), csv_members=members,
               note='untrusted bytes, read as text only, never executed')
    json.dump(man, open(os.path.join(d, 'manifest.json'), 'w'), indent=1)
    print(name, 'saved', zp, len(b), 'bytes,', len(members), 'csv members')

if __name__ == '__main__':
    for n, s in SOURCES.items(): fetch(n, s, '--force' in sys.argv)
