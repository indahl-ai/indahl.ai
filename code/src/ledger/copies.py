"""copies.py check|publish [NAME]|live -- the ledger for FILES (23 Oct 2026, his "faults and guards are in three places now ... set it up so it
updates across the board, no over-exposing cloud worker"). copies.json lists every file published in more than one place.
  check    every copy byte-identical to its canonical, and no source edited after its canonical was made  (run by the pre-commit hooks)
  publish  copy each canonical over all its copies (run after rendering a new canonical); then commit + deploy as usual
  live     fetch every public URL and compare it with the canonical (after a deploy)"""
import time, json, sys, os, hashlib, shutil, urllib.request
B = os.path.expanduser('~/forge'); M = json.load(open(os.path.join(B, 'ledger', 'copies.json')))
P = lambda p: p if p.startswith('/') else os.path.join(B, p)
h = lambda b: hashlib.sha256(b).hexdigest()[:12]
def items(): return [(k, v) for k, v in M.items() if not k.startswith('_') and (len(sys.argv) < 3 or k == sys.argv[2])]
def check():
    bad = 0
    for k, v in items():
        # 21 Nov 2026 (control audit #8): one missing canonical or source (a retired page left in copies.json) raised FileNotFoundError and
        # aborted the check for every set behind a `| tail -1`. Now each set is checked on its own; a missing file is named and still counts as drift.
        if not os.path.exists(P(v['canonical'])): print(f'  MISSING  {k}: canonical {v["canonical"]} (retired? prune ledger/copies.json)'); bad += 1; continue
        if v.get('source') and not os.path.exists(P(v['source'])): print(f'  MISSING  {k}: source {v["source"]} (retired? prune ledger/copies.json)'); bad += 1; continue
        if not os.path.exists(P(v['canonical'])): print(f'  MISSING  {k}: the canonical {v["canonical"]} is gone (restore it from a copy)'); bad += 1; continue   # 21 Nov 2026
        c = open(P(v['canonical']), 'rb').read(); hc = h(c)
        if v.get('source') and os.path.getmtime(P(v['source'])) > os.path.getmtime(P(v['canonical'])) + 1:
            print(f'  STALE    {k}: {v["source"]} edited after {v["canonical"]} was made -- render it'); bad += 1
        for cp in v['copies']:
            if not os.path.exists(P(cp)): print(f'  MISSING  {k}: {cp}'); bad += 1
            elif h(open(P(cp), 'rb').read()) != hc: print(f'  DIFFERS  {k}: {cp} != {v["canonical"]} ({hc})'); bad += 1
    print(f'copies: {sum(len(v["copies"]) + 1 for _, v in items())} files in {len(items())} sets; drift: {bad}'); return bad
def publish():
    for k, v in items():
        if not os.path.exists(P(v['canonical'])): print(f'  MISSING  {k}: canonical {v["canonical"]}, nothing copied'); continue   # control audit #8; check() below counts it
        for cp in v['copies']:
            try: shutil.copy2(P(v['canonical']), P(cp)); print(f'  copied {k} -> {cp}')
            except OSError as e: print(f'  FAILED   {k} -> {cp}: {type(e).__name__}')   # check() below counts it as MISSING or DIFFERS
    return check()
def live():
    bad = 0
    for k, v in items():
        if not os.path.exists(P(v['canonical'])): print(f'  MISSING  {k}: canonical {v["canonical"]}'); bad += 1; continue   # control audit #8
        hc = h(open(P(v['canonical']), 'rb').read())
        for u in v.get('live', []):
            try: b = urllib.request.urlopen(urllib.request.Request(u + ('&' if '?' in u else '?') + 'v=%d' % time.time(), headers={'User-Agent': 'copies.py', 'Cache-Control': 'no-cache'}), timeout=20).read(); hl = h(b)   # 23 Nov 2026: past the edge cache (max-age 3600); a fresh deploy read as LIVE OFF and rolled back
            except Exception as e: hl = 'ERR ' + type(e).__name__
            ok = hl == hc; bad += not ok; print(f'  {"LIVE OK " if ok else "LIVE OFF"} {k}: {u} {hl}')
    print(f'live drift: {bad}'); return bad
if __name__ == '__main__':
    sys.exit(1 if {'check': check, 'publish': publish, 'live': live}[sys.argv[1] if len(sys.argv) > 1 else 'check']() else 0)
