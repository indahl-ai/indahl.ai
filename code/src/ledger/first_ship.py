#!/usr/bin/env python3
"""first_ship.py (21 Nov 2026): the first-ship state of a new desk, ledger/desks.json field "first_ship".

Why: before a desk's first ship its feed /<desk>/live.json is not on the site yet (the worker route and the KV key go out with the ship), so
reproduce_kits.py refresh could not make its kit (HTTPError 404) and check_ledger.py held its live_headline row as LIVEFEED. With more than
three new desks at once the hold maximum refused every ship, so a new desk could never ship.

The rule, the same for every reader (live_headlines.check_rows, reproduce_kits.py refresh and gate):
  A desk is in first-ship state only when ALL hold: desks.json says "first_ship": true, the desk has never been seen live (no "first_live"
  stamp, no live value snapshot under ledger/live_values/<desk>/), AND the live feed answered HTTP 404 on this read. Then the reader uses the
  local built feed ("local_feed" in desks.json, default <folder>/data/<id>_live.json, the file the desk writes before it puts it in the KV).
  Any other answer is read as a live desk with every check in full: 200 flips the state to false at once (first_live stamped), and a
  timeout, a 5xx or any other error is never exempted. The hold maximum (check_ledger.py MAX_FEED) is not changed.
  A first_ship: true set on a desk that has been seen live is refused: the flag is reset to false and the refusal is rung.

  first_ship.py status            every desk in first-ship state, its live answer and its local feed
  first_ship.py set <desk>        the builders' command when a desk is added (refused once its feed has been live)
  first_ship.py flip              read each first-ship desk's live feed and flip those that answer 200 (the tick bus and live_headlines run call it)
Standard library only, Python 3.9."""
import fcntl, json, os, sys, time, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(HERE)
REG = os.path.join(HERE, 'desks.json'); LOCK = os.path.join(HERE, '.desks_json.lock')
SNAP = os.path.join(HERE, 'live_values'); PIPE_LOG = os.path.join(B, 'sagar', 'pipeline', 'pipe.log')
SITE = 'https://indahl.ai'
UA = {'User-Agent': 'heuremen-ledger/0.1 (+https://indahl.ai)'}


def _now(): return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def ring(msg):
    line = '%s RING: FIRST SHIP %s' % (time.strftime('%Y-%m-%dT%H:%M:%S'), msg.replace('\n', ' ')[:500])
    sys.stderr.write(line + '\n')
    try:
        with open(PIPE_LOG, 'a') as f: f.write(line + '\n')
    except Exception: pass


def _load():
    return json.load(open(REG, encoding='utf-8'))


def entry(slug, reg=None):
    try: reg = reg or _load()
    except Exception: return None
    return next((d for d in reg.get('desks', []) if d.get('id') == slug), None)


def local_feed(slug, e=None):
    e = e or entry(slug) or {}
    rel = e.get('local_feed') or ('%s/data/%s_live.json' % (e.get('folder') or slug + '_index', slug))
    return os.path.join(B, rel)


def feed_url(slug, e=None):
    e = e or entry(slug) or {}
    return SITE + (e.get('feed') or '/%s/live.json' % slug)


def was_live(slug, e=None):
    """has this desk ever been read live? a first_live stamp, or a live value snapshot (written only from the live feed)"""
    e = e or entry(slug) or {}
    if e.get('first_live'): return 'first_live %s' % e['first_live']
    d = os.path.join(SNAP, slug)
    try:
        if os.path.isdir(d) and any(f.endswith('.json') for f in os.listdir(d)): return 'live value snapshots under ledger/live_values/%s' % slug
    except OSError: pass
    return None


def _write(mut):
    """apply mut(reg) under the desks.json lock and replace the file atomically, in its own format (indent 1, UTF-8, trailing newline)"""
    with open(LOCK, 'a+') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        reg = _load(); changed = mut(reg)
        if changed:
            tmp = REG + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f: f.write(json.dumps(reg, indent=1, ensure_ascii=False) + '\n')
            os.replace(tmp, REG)
        return changed


def _set(slug, val, why):
    def mut(reg):
        e = next((d for d in reg['desks'] if d.get('id') == slug), None)
        if e is None or bool(e.get('first_ship')) == val: return False
        e['first_ship'] = val
        if not val: e['first_live'] = e.get('first_live') or _now()
        e.setdefault('first_ship_log', []).append('%s %s: %s' % (_now(), 'on' if val else 'off', why))
        return True
    try: return _write(mut)
    except Exception as ex:
        ring('%s: desks.json not written (%s: %s); readers still treat a 200 feed as live' % (slug, type(ex).__name__, ex)); return False


def flip_off(slug, why):
    if _set(slug, False, why): print('first ship: %s -> false (%s); every check applies in full from now on' % (slug, why), file=sys.stderr)


def decide(slug, err=None):
    """the reader's answer for one desk after it tried the live feed. err is None when the live feed answered and parsed, else the exception.
    Returns the local feed path when the desk is in first-ship state, else None (a live desk: full checks). Flips or refuses as the rule says."""
    try: e = entry(slug)
    except Exception: return None
    if not e or not e.get('first_ship'): return None
    if err is None:
        flip_off(slug, 'live feed answered 200'); return None
    wl = was_live(slug, e)
    if wl:
        ring('REFUSED: %s is marked first_ship but has been live (%s); flag reset, every check applies' % (slug, wl))
        _set(slug, False, 'refused: marked first-ship after its feed was live (%s)' % wl); return None
    if not (isinstance(err, urllib.error.HTTPError) and err.code == 404): return None   # a timeout or a 5xx is never exempted
    p = local_feed(slug, e)
    return p


def probe(slug, e=None):
    """HTTP status of the live feed (int), or the exception name"""
    try:
        r = urllib.request.urlopen(urllib.request.Request(feed_url(slug, e) + '?x=%d' % time.time(), headers=UA), timeout=30)
        json.loads(r.read()); return 200
    except urllib.error.HTTPError as ex: return ex.code
    except Exception as ex: return type(ex).__name__


def state(slug):
    """'first' (with local path) or 'live', after one live read; flips a desk whose feed answers 200"""
    e = entry(slug)
    if not e or not e.get('first_ship'): return 'live', None
    st = probe(slug, e)
    err = None if st == 200 else (urllib.error.HTTPError(feed_url(slug, e), st, 'status %s' % st, {}, None) if isinstance(st, int) else RuntimeError(st))
    p = decide(slug, err)
    return ('first', p) if p else ('live', None)


def flip_all():
    try: reg = _load()
    except Exception: return []
    out = []
    for e in reg.get('desks', []):
        if e.get('first_ship'): out.append((e['id'],) + state(e['id']))
    return out


def main(a):
    if a[:1] == ['status'] or not a:
        reg = _load(); n = 0
        for e in reg['desks']:
            if not e.get('first_ship'): continue
            n += 1; p = local_feed(e['id'], e)
            print('  %-14s live %-6s local %s %s' % (e['id'], probe(e['id'], e), os.path.relpath(p, B), 'present' if os.path.exists(p) else 'MISSING'))
        print('first ship: %d desk%s in first-ship state' % (n, '' if n == 1 else 's')); return 0
    if a[:1] == ['set'] and len(a) == 2:
        slug = a[1]; e = entry(slug)
        if not e: print('first ship: %s is not in ledger/desks.json (add the desk entry first)' % slug); return 1
        wl = was_live(slug, e); st = probe(slug, e)
        if wl or st == 200:
            print('REFUSED: %s has been live (%s); first-ship state is only for a desk whose feed has never been served' % (slug, wl or 'live feed answers 200')); return 1
        if _set(slug, True, 'set by the builder before the first ship (live feed %s)' % st) or e.get('first_ship'):
            print('first ship: %s -> true; local feed %s' % (slug, os.path.relpath(local_feed(slug, e), B))); return 0
        return 1
    if a[:1] == ['flip']:
        for slug, st, p in flip_all(): print('  %-14s %s' % (slug, 'first ship, local feed ' + os.path.relpath(p, B) if st == 'first' else 'live, full checks'))
        return 0
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
