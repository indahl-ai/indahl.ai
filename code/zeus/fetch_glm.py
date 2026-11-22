#!/usr/bin/env python3
"""fetch_glm.py: ZEUS delivered side. GOES GLM L2 LCFA flashes from NOAA open data on AWS (anonymous, no key).
Per convective day D (1200 UTC D to 1200 UTC D+1) and per satellite, streams every 20 s file into memory, keeps only flash
time, lat, lon and quality flag inside the CONUS box, and writes one compact file data/glm/<sat>/<D>.npz. Raw NetCDF never touches disk.
Resumable: a day whose npz exists is skipped. Polite: a bounded pool of parallel GETs, retries with backoff, nothing else.
Usage: .venv/bin/python fetch_glm.py --days 20260719 [20260720 ...] | --from 20260601 --to 20260831 [--sat east|west|both] [--workers 12]
Reads nothing about outlooks; computes no outlook-vs-lightning number (plan before reading)."""
import os, sys, io, json, time, calendar, re, argparse, threading, urllib.request, xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np, h5py
H = os.path.dirname(os.path.abspath(__file__))
UA = 'heuremen-zeus/0.1 (+https://indahl.ai/zeus)'
# CONUS box, generous margin; the reading frame clips further
LAT0, LAT1, LON0, LON1 = 23.0, 51.0, -126.0, -65.0
# Which platform holds each slot on a date (NOAA operational changes): GOES-19 East from 2025-04-07, GOES-16 before; GOES-18 West from 2023-01-04, GOES-17 before
def bucket(slot, day):
    if slot == 'east': return ('noaa-goes19', 'G19') if day >= '20250407' else ('noaa-goes16', 'G16')
    return ('noaa-goes18', 'G18') if day >= '20230104' else ('noaa-goes17', 'G17')
_tl = threading.local(); RANGED = False
def get(url, tries=4, timeout=60):
    err = None
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout) as r: return r.read()
        except Exception as e:
            err = e
            if getattr(e, 'code', 0) in (400, 403, 404): break
            time.sleep(2 * (a + 1) ** 2)
    raise RuntimeError('fetch failed %s: %r' % (url[-90:], err))
def list_prefix(bkt, prefix):
    keys = []; tok = None
    while True:
        u = 'https://%s.s3.amazonaws.com/?list-type=2&prefix=%s' % (bkt, prefix) + ('&continuation-token=' + urllib.request.quote(tok, safe='') if tok else '')
        root = ET.fromstring(get(u)); ns = {'s': root.tag.split('}')[0].strip('{')}
        for c in root.findall('s:Contents', ns): keys.append((c.find('s:Key', ns).text, int(c.find('s:Size', ns).text)))
        if root.findtext('s:IsTruncated', namespaces=ns) == 'true': tok = root.findtext('s:NextContinuationToken', namespaces=ns)
        else: return keys
def scaled(d):
    raw = d[()]
    if d.attrs.get('_Unsigned', b'') in (b'true', 'true') and raw.dtype.kind == 'i': raw = raw.view(raw.dtype.str.replace('i', 'u'))
    return raw.astype(np.float64) * float(np.ravel(d.attrs.get('scale_factor', [1.0]))[0]) + float(np.ravel(d.attrs.get('add_offset', [0.0]))[0])
def base_epoch(units):
    m = re.search(r'since (\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})', units.decode() if isinstance(units, bytes) else units)
    return calendar.timegm(time.strptime(m.group(1).replace('T', ' '), '%Y-%m-%d %H:%M:%S'))
class RangeFile(io.RawIOBase):
    """A read-only file over HTTP Range requests with a 4 KB block cache, so h5py reads only the blocks the flash variables need (about a third of a file)."""
    BLK = 4096
    def __init__(s, url, size):
        s.url = url; s.size = size; s.p = 0; s.blocks = {}; s.nbytes = 0; s._fetch(0, min(size, 4 * s.BLK))
    def _fetch(s, a, b):
        for t in range(4):
            try:
                req = urllib.request.Request(s.url, headers={'User-Agent': UA, 'Range': 'bytes=%d-%d' % (a, b - 1)})
                with urllib.request.urlopen(req, timeout=60) as r: data = r.read()
                break
            except Exception as e:
                if t == 3 or getattr(e, 'code', 0) in (400, 403, 404): raise RuntimeError('range fetch failed %s: %r' % (s.url[-90:], e))
                time.sleep(2 * (t + 1) ** 2)
        s.nbytes += len(data)
        for k in range(a // s.BLK, (a + len(data) + s.BLK - 1) // s.BLK): s.blocks[k] = data[(k * s.BLK - a):(k + 1) * s.BLK - a]
    def readable(s): return True
    def seekable(s): return True
    def seek(s, o, w=0): s.p = o if w == 0 else (s.p + o if w == 1 else s.size + o); return s.p
    def tell(s): return s.p
    def readinto(s, m):
        n = min(len(m), s.size - s.p)
        if n <= 0: return 0
        k0, k1 = s.p // s.BLK, (s.p + n - 1) // s.BLK; miss = [k for k in range(k0, k1 + 1) if k not in s.blocks]
        if miss: s._fetch(miss[0] * s.BLK, min(s.size, (miss[-1] + 1) * s.BLK))
        buf = b''.join(s.blocks[k] for k in range(k0, k1 + 1)); o = s.p - k0 * s.BLK
        m[:n] = buf[o:o + n]; s.p += n; return n
def read_file(b):
    """bytes (or a file object) of one LCFA file -> (t epoch float64, lat, lon float32, qf uint8) for flashes in the CONUS box, plus the total flash count."""
    with h5py.File(io.BytesIO(b) if isinstance(b, (bytes, bytearray)) else b, 'r') as f:
        lat = f['flash_lat'][()].astype(np.float32); lon = f['flash_lon'][()].astype(np.float32); n = len(lat)
        if n == 0: return np.zeros(0), lat, lon, np.zeros(0, np.uint8), 0
        to = f['flash_time_offset_of_first_event']; t = base_epoch(to.attrs['units']) + scaled(to)
        qf = f['flash_quality_flag'][()].view(np.uint16).astype(np.uint8)
    m = (lat >= LAT0) & (lat <= LAT1) & (lon >= LON0) & (lon <= LON1)
    return t[m], lat[m], lon[m], qf[m], n
def fetch_day(day, slot, workers, out_dir):
    bkt, sat = bucket(slot, day); out = os.path.join(out_dir, slot, day + '.npz')
    if os.path.exists(out): return json.load(open(out[:-4] + '.json'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    t0 = calendar.timegm(time.strptime(day + '12', '%Y%m%d%H')); T0 = time.time()
    keys = []
    for h in range(24):
        ts = time.gmtime(t0 + h * 3600)
        keys += list_prefix(bkt, 'GLM-L2-LCFA/%04d/%03d/%02d/' % (ts.tm_year, ts.tm_yday, ts.tm_hour))
    T, LA, LO, Q = [], [], [], []; nbytes = 0; nall = 0; failed = []; unreadable = []
    def one(k):
        if RANGED:
            rf = RangeFile('https://%s.s3.amazonaws.com/%s' % (bkt, k[0]), k[1]); out = read_file(rf); return k[0], rf.nbytes, out
        b = get('https://%s.s3.amazonaws.com/%s' % (bkt, k[0])); return k[0], len(b), read_file(b)
    with ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(one, k) for k in keys]
        for fu in as_completed(futs):
            try: k, nb, (t, la, lo, q, n) = fu.result()
            except RuntimeError as e: failed.append(str(e)[:160]); continue
            except Exception as e: unreadable.append(repr(e)[:160]); continue
            nbytes += nb; nall += n; T.append(t); LA.append(la); LO.append(lo); Q.append(q)
    t = np.concatenate(T) if T else np.zeros(0); o = np.argsort(t, kind='stable')
    t = t[o]; inday = (t >= t0) & (t < t0 + 86400)           # files straddling 1200 UTC: keep only flashes inside the convective day
    sec = (t - t0)[inday].astype(np.float32)
    la = (np.concatenate(LA) if LA else np.zeros(0, np.float32))[o][inday]; lo = (np.concatenate(LO) if LO else np.zeros(0, np.float32))[o][inday]
    q = (np.concatenate(Q) if Q else np.zeros(0, np.uint8))[o][inday]
    np.savez_compressed(out + '.part.npz', sec=sec, lat=la, lon=lo, qf=q)
    os.replace(out + '.part.npz', out)
    # coverage: file start times from the key names (…_sYYYYDDDHHMMSSs_…); gaps between consecutive starts over 40 s, and from the day edges
    st = sorted(calendar.timegm(time.strptime(re.search(r'_s(\d{13})', k[0]).group(1), '%Y%j%H%M%S')) for k in keys)
    edges = [t0 - 20] + [s for s in st if t0 - 20 <= s < t0 + 86400] + [t0 + 86400]
    gaps = [[int(a - t0), int(b - t0)] for a, b in zip(edges, edges[1:]) if b - a > 40]
    man = dict(day=day, slot=slot, bucket=bkt, platform=sat, files_listed=len(keys), files_expected=4320, files_failed=len(failed), files_unreadable=len(unreadable),
               gaps_s_from_1200=gaps, max_gap_s=max([b - a for a, b in gaps], default=20),
               bytes_streamed=nbytes, flashes_all_fov=int(nall), flashes_conus_box_in_day=int(len(sec)), box=[LAT0, LAT1, LON0, LON1],
               seconds=round(time.time() - T0, 1), npz_bytes=os.path.getsize(out), fetched_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               failed=failed[:20], unreadable=unreadable[:20])
    json.dump(man, open(out[:-4] + '.json', 'w'), indent=1)
    return man
def days_between(a, b):
    t = calendar.timegm(time.strptime(a, '%Y%m%d')); e = calendar.timegm(time.strptime(b, '%Y%m%d')); out = []
    while t <= e: out.append(time.strftime('%Y%m%d', time.gmtime(t))); t += 86400
    return out
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--days', nargs='*'); ap.add_argument('--from', dest='fr'); ap.add_argument('--to')
    ap.add_argument('--sat', default='both', choices=('east', 'west', 'both')); ap.add_argument('--workers', type=int, default=12)
    ap.add_argument('--ranged', action='store_true'); ap.add_argument('--out', default=os.path.join(H, 'data', 'glm')); ap.add_argument('--newest-first', action='store_true')
    a = ap.parse_args(); RANGED = a.ranged
    days = a.days or days_between(a.fr, a.to)
    if a.newest_first: days = days[::-1]
    slots = ('east', 'west') if a.sat == 'both' else (a.sat,)
    for d in days:
        for s in slots:
            try:
                m = fetch_day(d, s, a.workers, a.out)
                print('zeus glm', d, s, m['platform'], 'files', m['files_listed'], 'failed', m['files_failed'] + m['files_unreadable'], 'MB', round(m['bytes_streamed'] / 1e6), 'flashes', m['flashes_conus_box_in_day'],
                      'npz KB', m['npz_bytes'] // 1024, 's', m['seconds'], flush=True)
            except Exception as e: print('zeus glm', d, s, 'DAY FAILED', repr(e)[:200], flush=True)
