#!/usr/bin/env python3
"""chain.py: entries.jsonl (append-only source) -> chain.json (with prev/hash) for the public page. --verify checks a chain.json."""
import json, hashlib, sys, os, datetime as D
H = os.path.dirname(os.path.abspath(__file__))
def canon(e): return json.dumps({k: v for k, v in e.items() if k != 'hash'}, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
def build():
    prev = '0' * 64; out = []
    for i, l in enumerate(open(os.path.join(H, 'entries.jsonl'))):
        if not l.strip(): continue
        e = json.loads(l); e['n'] = len(out) + 1; e['prev'] = prev; e['hash'] = hashlib.sha256(canon(e)).hexdigest(); prev = e['hash']; out.append(e)
    c = dict(updated=D.datetime.now(D.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), head=prev, count=len(out), entries=out,
             how_to_verify='python3 verify.py chain.json (in the public repository, code/qia-offchain) recomputes every hash from the first entry.')
    _t = os.path.join(H, 'chain.json.tmp'); json.dump(c, open(_t, 'w'), indent=1, ensure_ascii=False); os.replace(_t, os.path.join(H, 'chain.json')); summary(c); return c   # 12 Nov: atomic, a reader mid-write crashed a cal append and left the feed stale
def summary(c):
    # 16 Nov 2026 (teardown #12): the page loads this first; the full chain (off-record readings of every hourly run) loads only for a job check.
    def slim(e):
        if e.get('type') != 'calibration run': return e
        by = {}
        for o in e.get('off') or []: by[o.get('quantity')] = by.get(o.get('quantity'), 0) + 1
        return {k: v for k, v in e.items() if k != 'off'} | {'off_count': len(e.get('off') or []), 'off_by': by}
    sm = dict(c, entries=[slim(e) for e in c['entries']], note='Summary of chain.json: each hourly run lists counts in place of its off-record readings. Hashes are those of the full entries in chain.json.')
    _t = os.path.join(H, 'chain_summary.json.tmp'); json.dump(sm, open(_t, 'w'), ensure_ascii=False, separators=(',', ':')); os.replace(_t, os.path.join(H, 'chain_summary.json'))
def verify(path):
    c = json.load(open(path)); prev = '0' * 64
    for e in c['entries']:
        assert e['prev'] == prev, ('broken link at entry', e['n']); h = hashlib.sha256(canon(e)).hexdigest(); assert h == e['hash'], ('hash mismatch at entry', e['n']); prev = h
    assert prev == c['head'], 'head does not match the last entry'; return len(c['entries']), prev
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--verify': n, h = verify(sys.argv[2]); print('chain OK:', n, 'entries, head', h)
    else: c = build(); n, h = verify(os.path.join(H, 'chain.json')); print('built and verified:', n, 'entries, head', h[:16])
