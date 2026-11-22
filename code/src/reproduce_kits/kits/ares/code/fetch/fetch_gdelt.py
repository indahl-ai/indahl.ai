#!/usr/bin/env python3
"""fetch_gdelt.py: ARES, the GDELT side (PLAN.md sections 3 and 4). Reads the GDELT 2.0 master file list, then every 15-minute event export whose
timestamp falls in the window, one file at a time in memory (a few hundred kilobytes), checked against the MD5 the list gives, filtered and folded into
the province-month table at once. Nothing raw is kept: no article text, no mention table, no actor column, no coordinate, no town.

Filter (PLAN.md section 4, exactly): IsRootEvent 1, QuadClass 4, EventRootCode 18, 19 or 20, ActionGeo_Type 4 or 5, NumSources 2 or more.
The month is the event's SQLDATE month. The province is ActionGeo_ADM1Code (FIPS 10-4). The province spelling kept is GDELT's own first-order
name from ActionGeo_FullName: the part before the country for a type 5 match, the part before that for a type 4 match. The city part is dropped.

Resumable: state in data/gdelt_state.json (done files and the running table), written every 400 files. Peak memory stays small: downloads run in
a pool of WORKERS threads, each holding one file, and the table holds one entry per province code and month.

  fetch_gdelt.py --window 2025-10:2026-09
Standard library only."""
import collections, hashlib, io, json, os, sys, threading, time, urllib.request, zipfile
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, H)
import ares_lines as L

UA = 'Mozilla/5.0 (compatible; research-fetch)'
MASTER = 'https://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
WORKERS = 6
CHUNK = 48
STATE = os.path.join(H, 'data', 'gdelt_state.json')
G = L.GDELT_READ


def months(a, b):
    y, m = map(int, a.split('-')); out = []
    while '%04d-%02d' % (y, m) <= b:
        out.append('%04d-%02d' % (y, m)); m += 1
        if m > 12: y, m = y + 1, 1
    return out


def fetch(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url.replace('http://', 'https://'), headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=120) as r: return r.read(), None
        except urllib.error.HTTPError as e:
            if e.code == 404: return None, 'HTTP 404'
            last = 'HTTP %d' % e.code
        except Exception as e:
            last = type(e).__name__
        time.sleep(2 + 3 * i)
    return None, last


def adm1_name(full, typ):
    parts = [p.strip() for p in full.split(',')]
    if typ == '5' and len(parts) >= 2: return parts[-2]
    if typ == '4' and len(parts) >= 3: return parts[-2]
    return ''


def main():
    w = sys.argv[sys.argv.index('--window') + 1].split(':'); WIN = months(*w)
    t0, t1 = WIN[0].replace('-', '') + '01000000', None
    y, m = map(int, WIN[-1].split('-')); m += 1
    if m > 12: y, m = y + 1, 1
    t1 = '%04d%02d01000000' % (y, m)
    raw, err = fetch(MASTER)
    if raw is None: sys.exit('gdelt: master file list unreadable: %s' % err)
    master_sha = hashlib.sha256(raw).hexdigest()
    todo = []
    for line in raw.decode('utf-8', 'replace').splitlines():
        p = line.split()
        if len(p) != 3 or not p[2].endswith('.export.CSV.zip'): continue
        ts = p[2].rsplit('/', 1)[1][:14]
        if t0 <= ts < t1: todo.append((ts, int(p[0]), p[1], p[2]))
    del raw
    todo.sort()
    if os.path.exists(STATE):
        S = json.load(open(STATE))
        assert S['window'] == WIN, 'gdelt: state is for another window, move data/gdelt_state.json aside'
    else:
        S = dict(window=WIN, master_sha256=master_sha, listed=len(todo), done={}, table={}, spell={}, cname={}, counts=collections.Counter())
    C = collections.Counter(S['counts'])
    table = S['table']   # "FIPSADM1|YYYY-MM" -> qualifying root events
    spell = {k: collections.Counter(v) for k, v in S['spell'].items()}
    cname = {k: collections.Counter(v) for k, v in S['cname'].items()}
    done = S['done']
    left = [t for t in todo if t[0] not in done]
    print('gdelt: listed %d, done %d, left %d' % (len(todo), len(done), len(left)), file=sys.stderr, flush=True)
    winset = set(WIN)

    def save():
        S.update(counts=dict(C), table=table, spell={k: dict(v) for k, v in spell.items()}, cname={k: dict(v) for k, v in cname.items()}, done=done,
                 listed=len(todo), master_sha256=master_sha, saved=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        L.assert_clean({k: v for k, v in S.items() if k not in ('table', 'spell', 'cname', 'done')}, 'gdelt_state')
        json.dump(S, open(STATE + '.tmp', 'w'), separators=(',', ':')); os.replace(STATE + '.tmp', STATE)

    def one(item):
        ts, size, md5, url = item
        b, e = fetch(url)
        return item, b, e

    n = 0
    def bounded(ex):   # at most CHUNK files in memory at once, never the whole list queued with its bytes
        for i in range(0, len(left), CHUNK):
            for res in ex.map(one, left[i:i + CHUNK]): yield res

    with ThreadPoolExecutor(WORKERS) as ex:
        for item, b, e in bounded(ex):
            ts, size, md5, url = item
            if b is None:
                done[ts] = dict(ok=False, why=e); C['files_nothing_returned'] += 1
            elif hashlib.md5(b).hexdigest() != md5:
                done[ts] = dict(ok=False, why='md5 differs from the master list'); C['files_md5_mismatch'] += 1
            else:
                try:
                    z = zipfile.ZipFile(io.BytesIO(b)); data = z.read(z.namelist()[0])
                except Exception as ex2:
                    done[ts] = dict(ok=False, why='zip unreadable: %s' % type(ex2).__name__); C['files_unreadable'] += 1; continue
                kept = 0
                for line in data.decode('utf-8', 'replace').split('\n'):
                    if not line: continue
                    r = line.split('\t')
                    if len(r) != L.GDELT_COLS: C['rows_short'] += 1; continue
                    C['rows'] += 1
                    if r[G['QuadClass']] != '4' or r[G['EventRootCode']] not in ('18', '19', '20'): continue
                    C['rows_quad4_root18_20'] += 1
                    if r[G['IsRootEvent']] != '1': continue
                    C['rows_and_root_event'] += 1
                    try: ns = int(r[G['NumSources']])
                    except ValueError: ns = 0
                    if ns < 2: continue
                    C['rows_and_two_sources'] += 1
                    typ = r[G['ActionGeo_Type']]
                    if typ not in ('4', '5'):
                        C['rows_geo_type_%s' % (typ or 'blank')] += 1; continue
                    C['rows_and_geo_type_4_5'] += 1
                    code = r[G['ActionGeo_ADM1Code']].strip()
                    if len(code) < 3: C['rows_blank_place'] += 1; continue   # PLAN.md section 5: a blank place is nothing returned
                    if code[2:] == '00': C['rows_country_general'] += 1; continue   # GDELT's '(general)' code: no province, a country-level place
                    mo = r[G['SQLDATE']][:4] + '-' + r[G['SQLDATE']][4:6]
                    if mo not in winset: C['rows_sqldate_outside_window'] += 1; continue
                    C['rows_kept'] += 1; kept += 1
                    k = code + '|' + mo
                    table[k] = table.get(k, 0) + 1
                    nm = adm1_name(r[G['ActionGeo_FullName']], typ)
                    if nm: spell.setdefault(code, collections.Counter())[nm] += 1
                    cn = r[G['ActionGeo_FullName']].rsplit(',', 1)[-1].strip()
                    if cn: cname.setdefault(r[G['ActionGeo_CountryCode']].strip() or code[:2], collections.Counter())[cn] += 1
                del data, b
                done[ts] = dict(ok=True, md5=md5, bytes=size, kept=kept); C['files_read'] += 1
            n += 1
            if n % 400 == 0:
                save(); print('gdelt: %d of %d this run, kept rows %d' % (n, len(left), C['rows_kept']), file=sys.stderr, flush=True)
    save()
    # the province-month table (what the tick reads)
    rows = []
    for k, v in sorted(table.items()):
        code, mo = k.split('|')
        sp = spell.get(code)
        cc = code[:2]
        rows.append(dict(adm1_code=code, country_code=cc, country=(cname.get(cc) or collections.Counter({'': 1})).most_common(1)[0][0],
                         province=sp.most_common(1)[0][0] if sp else '', month=mo, root_events=v))
    bad = {ts: d['why'] for ts, d in done.items() if not d['ok']}
    out = dict(window=WIN, master=MASTER, master_sha256=S.get('master_sha256'), files_listed=len(todo), files_read=sum(1 for d in done.values() if d['ok']),
               files_not_read=bad, counts=dict(C), rows=rows, filter='IsRootEvent 1, QuadClass 4, EventRootCode 18 19 20, ActionGeo_Type 4 or 5, NumSources 2 or more',
               file_md5=hashlib.sha256(json.dumps({ts: d.get('md5') for ts, d in sorted(done.items())}).encode()).hexdigest(),
               note='Each file was checked against the MD5 in the master list and read in memory. Nothing raw is kept.')
    L.assert_clean(out, 'data/gdelt_pm.json')
    p = os.path.join(H, 'data', 'gdelt_pm.json')
    json.dump(out, open(p + '.tmp', 'w'), indent=0); os.replace(p + '.tmp', p)
    man = os.path.join(H, 'data', 'gdelt_files.tsv')
    with open(man + '.tmp', 'w') as f:
        f.write('timestamp\tok\tmd5\tbytes\tkept_rows\twhy\n')
        for ts, d in sorted(done.items()): f.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (ts, int(d['ok']), d.get('md5', ''), d.get('bytes', ''), d.get('kept', ''), d.get('why', '')))
    os.replace(man + '.tmp', man)
    print('gdelt: done. files read %d, not read %d, kept rows %d, province-months %d' % (out['files_read'], len(bad), C['rows_kept'], len(rows)), file=sys.stderr)


if __name__ == '__main__':
    main()
