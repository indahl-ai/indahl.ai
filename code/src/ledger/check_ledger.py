#!/usr/bin/env python3
"""Compare every surface with the ledger.

  check_claims.py            report drift; exit 1 if any
  check_claims.py --coverage also list numbers printed on a surface that no live row covers

Drift is:
  MISSING    a live row's snippet is not on a surface the row says it is on (the surface changed; the ledger was not edited first)
  ZOMBIE     a withdrawn or held row's snippet is still printed on a surface
  SOURCE     the row's source file is gone, or no longer contains the row's grep text (the number lost its producer)
  LIVEFIELD  (10 Nov 2026) a live_headline row's feed no longer carries the field its headline comes from (or a field its rule reads)
  LIVESTALE  a live_headline row's feed stamp is older than the desk's cadence x 1.5
  LIVEFEED / LIVESTAMP  the feed could not be read, or its stamp does not read as a time
  The live value is not compared: it moves on every read. A new value row is written by live_headlines.py run on a material change only.
Text is compared after stripping HTML/LaTeX markup and normalising dashes, spaces and minus signs.
"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ledger import load, surface_path, ROOT, SURFACES


def norm(s):
    s = re.sub(r'<a class="rcpt"[^>]*>[^<]*</a>', '', s)   # 10 Nov 2026: a receipt link (ledger/receipts.py) is not page text, so it never splits a snippet
    s = re.sub(r'<a class="ent" href="[^"]*">([^<]*)</a><a class="fb nosig"[^>]*>Follow</a>', r'\1', s)   # 10 Nov 2026 evening: a Follow link beside a name (indahl-ai/entities.py) is not page text, and the name keeps its place
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = s.replace('CANNOT_TELL', 'CANNOT TELL').replace('NOTHING_RETURNED', 'NOTHING RETURNED').replace('STRADDLES_EDGE', 'STRADDLES EDGE')   # 16 Nov 2026: pages show outcome words without underscores (build_site.py _plain)
    s = s.replace('\\us{}', ' µs').replace('\\us', ' µs').replace('\\%', '%').replace('\\,', ' ').replace('\\textmu', 'µ')
    s = re.sub(r'\\(texttt|emph|textbf|mathrm)\{([^}]*)\}', r'\2', s)
    s = s.replace('\\pm', '±').replace('$', '').replace('{', '').replace('}', '').replace('^\\circ', '°').replace('\\circ', '°')
    s = s.replace('−', '-').replace('–', '-').replace('—', '-').replace('\u2009', ' ').replace('\xa0', ' ')
    s = s.replace('\\n', ' ')
    return re.sub(r'\s+', ' ', s).strip()


_cache = {}
def text_of(key):
    if key not in _cache:
        p = surface_path(key)
        if os.path.isdir(p):   # 17 Nov 2026, the owner: consistency site-wide; removal automated in the page builders. A folder surface (sagar_study) is every .html in it, so a stale study page left behind reads as ZOMBIE
            _cache[key] = '\n'.join(norm(open(os.path.join(p, f), errors='ignore').read()) for f in sorted(os.listdir(p)) if f.endswith('.html'))
            return _cache[key]
        _cache[key] = norm(open(p, errors='ignore').read()) if os.path.exists(p) else None
    return _cache[key]


def main():
    rows = load(); drift = []
    for r in rows.values():
        if r['status'] == 'staged':   # 10 Nov: a new desk's row before its first ship; not checked either way until the desk flips it to live in its ship
            continue
        src = r['source']['file']; sp = src if src.startswith('/') else os.path.join(ROOT, src)
        if r['status'] == 'live':
            if not os.path.exists(sp) or r['source']['grep'] not in open(sp, errors='ignore').read():
                drift.append(('SOURCE', r['id'], src, r['source']['grep']))
        for s in r['surfaces']:
            t = text_of(s['surface'])
            if t is None:
                if r['status'] == 'live':   # 10 Nov: a held/withdrawn row whose page is not built (or gone) does not block a ship
                    drift.append(('MISSING', r['id'], s['surface'], 'surface file not found'))
                continue
            present = norm(s['text']) in t
            if r['status'] == 'live' and not present:
                drift.append(('MISSING', r['id'], s['surface'], s['text'][:90]))
            if r['status'] in ('withdrawn', 'held') and present:   # 3 Nov: a held row (out for a rescore) must not be printed either
                drift.append(('ZOMBIE', r['id'], s['surface'], s['text'][:90]))
    from live_headlines import check_rows   # 10 Nov 2026 (cold read row 12): headline numbers that move on every read
    drift += check_rows(rows)
    # 21 Nov 2026 (control audit #25): every live_headline feed path has its hand-listed route in the worker (a new desk's row before its route
    # read as a 404 LIVEFEED). Reported as LIVEROUTE and scoped with LIVEFEED below.
    try:
        _w = open(os.path.expanduser('~/forge/cloudflare-workers/heuremen-door/worker.js'), encoding='utf-8').read()
        for _r in sorted(rows.values(), key=lambda r: r['id']):
            if _r.get('kind') != 'live_headline' or _r.get('status') != 'live': continue
            _p = re.sub(r'^https?://[^/]+', '', _r['live']['feed'])
            if '"%s"' % _p not in _w: drift.append(('LIVEROUTE', _r['id'], _p, 'no route for this feed path in cloudflare-workers/heuremen-door/worker.js'))
    except OSError as _e: drift.append(('LIVEROUTE', 'worker.js', '-', 'worker.js unreadable: %s' % type(_e).__name__))
    n_live = sum(1 for r in rows.values() if r['status'] == 'live')
    n_lh = sum(1 for r in rows.values() if r.get('kind') == 'live_headline' and r['status'] == 'live')
    print(f'ledger: {len(rows)} rows ({n_live} live, {n_lh} live headlines read against their feeds); drift: {len(drift)}')
    for d in drift:
        print('  %-8s %-28s %-26s %s' % d)
    if '--coverage' in sys.argv:
        num = re.compile(r'(?<![\w.])[+-]?\d+\.\d+')
        keys = list(SURFACES) + sorted({s['surface'] for r in rows.values() for s in r['surfaces'] if s['surface'].startswith('site:')})
        for k in keys:
            t = text_of(k)
            if t is None: continue
            covered = ' '.join(norm(s['text']) for r in rows.values() if r['status'] == 'live' for s in r['surfaces'] if s['surface'] == k)
            nums = num.findall(t); un = [x for x in nums if x not in covered]
            print(f'  coverage {k:<40} {len(nums) - len(un):>4} of {len(nums):>4} decimal numbers in a ledger row')
    # 15 Nov 2026, the owner ("why the fuck are we still waiting on the fucking scorecards"): a stale feed is reported here and by
    # alerts_check, and each live headline prints its own stamp, but it no longer holds every unrelated ship behind a slow refresh.
    # 21 Nov 2026 (control audit #1): one live feed that could not be read (LIVEFEED) or one desk that renamed a field (LIVEFIELD) refused the
    # whole site. Scoped like LIVESTALE and the reproduce gate: the failing desks are written to ledger/live_held.json (headlines.py takes
    # them off the home banner), rung to sagar/pipeline/pipe.log on change, and the ship refuses only when more than MAX_FEED desks fail.
    MAX_FEED = 3
    ff = [d for d in drift if d[0] in ('LIVEFEED', 'LIVEFIELD', 'LIVEROUTE')]
    held = sorted({d[1].split('.')[1] if d[1].count('.') >= 2 else d[1] for d in ff})
    hp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'live_held.json')
    try:
        was = json.load(open(hp)).get('held', []) if os.path.exists(hp) else []
        json.dump(dict(at=__import__('time').strftime('%Y-%m-%dT%H:%M:%SZ', __import__('time').gmtime()), held=held, why={d[1]: '%s %s' % (d[0], d[3]) for d in ff}), open(hp + '.tmp', 'w'), indent=1); os.replace(hp + '.tmp', hp)
        if held and held != was:
            open(os.path.expanduser('~/forge/sagar/pipeline/pipe.log'), 'a').write(__import__('time').strftime('%Y-%m-%dT%H:%M:%S ') + 'RING: LIVE FEED HELD (%d of max %d before the ship refuses): %s\n' % (len(held), MAX_FEED, '; '.join('%s %s' % (d[1], d[0]) for d in ff)[:400]))
    except Exception as e: print('  live_held.json could not be written: %s' % type(e).__name__); held = held + ['(unwritten)'] * (MAX_FEED + 1)   # fail closed: no hold record, no scoping
    if held: print('  live feeds held (off the home banner, not refusing until more than %d): %s' % (MAX_FEED, ', '.join(held)))
    sys.exit(1 if [d for d in drift if d[0] not in ('LIVESTALE', 'LIVEFEED', 'LIVEFIELD', 'LIVEROUTE')] or len(held) > MAX_FEED else 0)


if __name__ == '__main__':
    main()
