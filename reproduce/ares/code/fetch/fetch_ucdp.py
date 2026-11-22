#!/usr/bin/env python3
"""fetch_ucdp.py: ARES, the UCDP side (PLAN.md sections 3 and 4). Downloads UCDP GED 26.1 and the UCDP Candidate release that covers the window months,
hashes each file, streams it once and keeps only the province-month table. The raw file is deleted after the read, so no death, injury, actor, side,
dyad, coordinate or town field is ever stored (PLAN.md section 0, lines 1, 3 and 6).

Kept per row, in memory only while the row is read: code_status, type_of_violence, where_prec, adm_1, country, date_prec, date_start, date_end.
Written: data/ucdp_pm.json, one entry per (release, country, adm_1, month) with any_event and the exact-day dates used for active_days.

  fetch_ucdp.py --window 2025-10:2026-09
Standard library only."""
import csv, hashlib, io, json, os, sys, time, urllib.request, zipfile
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, H)
import ares_lines as L

UA = 'Mozilla/5.0 (compatible; research-fetch)'
TMP = os.path.join(H, 'data', 'tmp_ucdp')
RELEASES = [  # GED is preferred over Candidate where both cover a month (PLAN.md section 3)
    dict(name='UCDP GED 26.1', version='26.1', kind='ged', url='https://ucdp.uu.se/downloads/ged/ged261-csv.zip', covers=('1989-01', '2025-12')),
    dict(name='UCDP Candidate 26.01.26.09', version='26.01.26.09', kind='candidate', url='https://ucdp.uu.se/downloads/candidateged/GEDEvent_v26_01_26_09.csv', covers=('2026-01', '2026-09')),
]
csv.field_size_limit(1 << 26)


def months(a, b):
    y, m = map(int, a.split('-')); out = []
    while '%04d-%02d' % (y, m) <= b:
        out.append('%04d-%02d' % (y, m)); m += 1
        if m > 12: y, m = y + 1, 1
    return out


def get(url, path):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    h = hashlib.sha256(); n = 0
    with urllib.request.urlopen(req, timeout=600) as r, open(path, 'wb') as f:
        while True:
            b = r.read(1 << 20)
            if not b: break
            f.write(b); h.update(b); n += len(b)
    return h.hexdigest(), n


def rows_of(path, kind):
    if kind == 'ged':
        z = zipfile.ZipFile(path); name = [n for n in z.namelist() if n.lower().endswith('.csv')][0]
        fh = io.TextIOWrapper(z.open(name), encoding='utf-8', newline='')
    else:
        name = os.path.basename(path); fh = open(path, encoding='utf-8', newline='')
    rd = csv.reader(fh)
    head = next(rd)
    idx = {k: head.index(k) for k in L.UCDP_READ}   # only these columns are ever looked at
    yield name, None
    for r in rd:
        if len(r) != len(head): yield name, 'short'; continue
        yield name, {k: r[i] for k, i in idx.items()}
    fh.close()


def main():
    w = sys.argv[sys.argv.index('--window') + 1].split(':')
    WIN = months(*w)
    os.makedirs(TMP, exist_ok=True)
    month_src = {}
    for m in WIN:
        for rel in RELEASES:
            if rel['covers'][0] <= m <= rel['covers'][1]: month_src[m] = rel['name']; break
    agg, files, counts = {}, [], {}
    for rel in RELEASES:
        mine = [m for m in WIN if month_src.get(m) == rel['name']]
        if not mine: continue
        path = os.path.join(TMP, os.path.basename(rel['url']))
        sha, n = get(rel['url'], path)
        c = dict(rows=0, short_rows=0, outside_window_or_other_release=0, type_not_1_3=0, status_not_clear=0, where_prec_5_to_7=0,
                 blank_adm_1=0, kept=0, kept_exact_day=0)
        member = None
        for name, row in rows_of(path, rel['kind']):
            if row is None: member = name; continue
            if row == 'short': c['short_rows'] += 1; continue
            c['rows'] += 1
            m = row['date_start'][:7]
            if m not in mine: c['outside_window_or_other_release'] += 1; continue
            if row['type_of_violence'] not in ('1', '2', '3'): c['type_not_1_3'] += 1; continue
            if rel['kind'] == 'candidate' and row['code_status'].strip() != 'Clear': c['status_not_clear'] += 1; continue
            try: wp = int(row['where_prec'])
            except ValueError: wp = 9
            if not 1 <= wp <= 4: c['where_prec_5_to_7'] += 1; continue
            adm = row['adm_1'].strip(); cty = row['country'].strip()
            if not adm: c['blank_adm_1'] += 1; continue
            k = (rel['name'], cty, adm, m)
            e = agg.setdefault(k, set())
            c['kept'] += 1
            if row['date_prec'].strip() == '1' and row['date_start'][:10] == row['date_end'][:10]:
                e.add(row['date_start'][:10]); c['kept_exact_day'] += 1
        os.remove(path)   # PLAN.md section 3: only the table is kept
        files.append(dict(release=rel['name'], version=rel['version'], url=rel['url'], member=member, sha256=sha, bytes=n, months=mine,
                          read=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), raw_deleted_after_read=True))
        counts[rel['name']] = c
        print('ucdp:', rel['name'], json.dumps(c), file=sys.stderr)
    rows = [dict(release=k[0], country=k[1], adm_1=k[2], month=k[3], exact_days=sorted(v)) for k, v in sorted(agg.items())]
    out = dict(window=WIN, month_release=month_src, held_months=[m for m in WIN if m not in month_src], files=files, counts=counts, rows=rows,
               kept_columns=list(L.UCDP_READ), note='Raw files deleted after the read. No death, injury, actor, side, dyad, coordinate or town field was stored.')
    L.assert_clean(out, 'data/ucdp_pm.json')
    p = os.path.join(H, 'data', 'ucdp_pm.json')
    json.dump(out, open(p + '.tmp', 'w'), indent=0); os.replace(p + '.tmp', p)
    try: os.rmdir(TMP)
    except OSError: pass
    print('ucdp: rows', len(rows), file=sys.stderr)


if __name__ == '__main__':
    main()
