#!/usr/bin/env python3
"""headline_cover_gate.py (21 Nov 2026): the number on each headline card must be the number its ledger row reads, and the desk's reproduce kit
must compute that same field. Exit 1 on any breach. Runs in ledger/ship.sh beside spelling_gate.py.

Why: on 21 Nov 2026 the AIRQ card moved to the live panel while its ledger row and its kit still read the window read; every ship that day broke on
the kit. A card can move only together with its ledger row (ledger/live_headlines.py DESKS, moved with `live_headlines.py repoint SLUG`) and its kit.

  COVER  a desk with a live_headline row: the card's figure (headlines.json 'figure', or 'big' when there is none) must equal LH.display() of the
         row's fields on the same feed. When the two differ and the feed's stamp is newer than the card's as_of, the feed ticked after the card
         was built: noted, not a breach. A clock ('age', 'years') is not compared.
  ROW    the live_headline row's stored fields must be DESKS' fields (a DESKS edit without a repoint is a breach).
  KIT    a desk with a reproduce kit: kit.json's headline fields must be DESKS' fields (indahl-ai/reproduce_kits.py kit_json).
  NOROW  a card in headlines.json for a page with neither a live_headline row nor an entry in NOROW below is a breach.
Standard library only."""
import ast, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import live_headlines as LH   # noqa: E402
# cards with no live_headline row, and why (a new card must get a row or a line here, never neither)
NOROW = {'oy': 'one-time read of 25 October 2026, its numbers are value rows oy.s0_* on the oy_matrix surface',
         'qia': 'one-time QPU run of 11 November 2026, ledger rows qia.* on the QIA pages; the queue table is a display',
         'atlas': 'one-time build of 30 October 2026, arithmetic on published figures',
         'iris': 'the HOSTS feed, the same counts as the hosts row', 'hermes': 'a copy of the TRIALS card (the trials row)',
         'iris/lab': 'YO v7 reads from yo/live_reads.jsonl, no feed; the lab page prints every read'}
CLOCKS = ('age', 'years')


def _building():   # 22 Nov 2026: a desk still marked building in ledger/desk_expect.json cannot block other desks' ships (ARES did)
    try: return {k for k, v in json.load(open(os.path.join(B, 'ledger', 'desk_expect.json')))['desks'].items() if v.get('state') == 'building'}
    except Exception: return set()

def local_map():
    """The feed files watch/headlines.py reads instead of the public feed (its LOCAL), so the card and this check read the same bytes."""
    src = open(os.path.join(B, 'watch', 'headlines.py'), encoding='utf-8').read()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', None) == 'LOCAL' for t in node.targets):
            return {k.value: os.path.join(B, v.right.value.lstrip('/')) for k, v in zip(node.value.keys, node.value.values)}
    return {}


def feed(slug, local):
    p = local.get(slug)
    if p and os.path.exists(p): return json.load(open(p))
    return LH.get(LH.feed_url(slug))


def main():
    import ledger as L
    rows = L.load(); bad = []; notes = []; n = 0
    hl = json.load(open(os.path.join(B, 'watch', 'headlines.json')))
    pages = hl['pages']; local = local_map()
    _bd = _building()
    for slug, h in pages.items():
        if slug in _bd: notes.append('%s: desk still building, card not checked' % slug); continue
        if slug not in LH.DESKS:
            if slug not in NOROW: bad.append(('NOROW', slug, 'a card with no live_headline row and no NOROW reason'))
            continue
        spec = LH.DESKS[slug]; row = rows.get('live.%s.headline' % slug)
        if not row or row.get('status') != 'live': bad.append(('ROW', slug, 'no live live_headline row')); continue
        if row['live'].get('fields') != json.loads(json.dumps(dict(LH.fields_of(spec)))) or row['live'].get('show') != spec['show']:
            bad.append(('ROW', slug, 'the ledger row reads %s as %s, DESKS names %s as %s (run live_headlines.py repoint %s)' % (json.dumps(row['live'].get('field'), ensure_ascii=False), row['live'].get('show'), json.dumps(spec['field'], ensure_ascii=False), spec['show'], slug)))
        kj = os.path.join(B, 'reproduce_kits', 'kits', slug, 'kit.json')
        if os.path.exists(kj):
            want = {k: spec[k] for k in ('field', 'n', 'of', 'lo', 'hi', 'outcome', 'keys', 'show') if spec.get(k) is not None}
            if json.load(open(kj)).get('headline') != json.loads(json.dumps(want)): bad.append(('KIT', slug, 'the kit computes other headline fields than DESKS (reproduce_kits.py build %s)' % slug))
        if spec['show'] in CLOCKS: continue
        fig = h.get('figure') or h.get('big')
        try: d = feed(slug, local)
        except Exception as e: bad.append(('COVER', slug, 'feed not read (%s)' % type(e).__name__)); continue
        if any(LH.dig(d, p) is LH._MISS for _, p in LH.fields_of(spec)): bad.append(('COVER', slug, 'a ledger field is absent on the feed')); continue
        shown = LH.display(spec, d); n += 1
        if shown == fig: continue
        ts = LH.stamp_epoch(LH.dig(d, spec['stamp'])); hs = LH.stamp_epoch((h.get('as_of') or hl.get('updated') or '').replace('T', ' ').replace('Z', ''))
        if ts and hs and ts > hs + 60: notes.append('%s: card %r, feed now %r, the feed ticked after the card was built' % (slug, fig, shown)); continue
        bad.append(('COVER', slug, 'the card shows %r, the ledger row\'s fields read %r on the same feed' % (fig, shown)))
    print('headline cover gate: %d cards read against their ledger rows; breaches: %d' % (n, len(bad)))
    for b in bad: print('  %-6s %-12s %s' % b)
    for x in notes: print('  note: ' + x)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
