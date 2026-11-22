#!/usr/bin/env python3
"""push_index.py: copies the changed files of public/qia/records to the page's KV namespace (IRIS_BENCH) as keys qia_rc/<path>, in one bulk put.
Only files whose sha256 differs from the last push (kept in .pushed.json) are sent. --dry-run lists them and sends nothing. Needs the same
wrangler login the other mirror publishers use. Usage: python3 -I push_index.py [--dry-run]"""
import os, sys, json, hashlib, subprocess, tempfile
H = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(H, 'public', 'qia', 'records'); LEDGER = os.path.join(H, '.pushed.json')
W = os.path.expanduser('~/forge/cloudflare-workers/heuremen-door'); NS = '<kv-namespace-id>'
def main():
    dry = '--dry-run' in sys.argv; old = json.load(open(LEDGER)) if os.path.exists(LEDGER) else {}; new, todo = {}, []
    for root, _, fs in os.walk(SRC):
        for f in fs:
            if not f.endswith('.json'): continue
            p = os.path.join(root, f); rel = os.path.relpath(p, SRC); h = hashlib.sha256(open(p, 'rb').read()).hexdigest(); new[rel] = h
            if old.get(rel) != h: todo.append(rel)
    print(len(todo), 'changed of', len(new), 'files')
    if dry or not todo: return
    bulk = [{'key': 'qia_rc/' + r, 'value': open(os.path.join(SRC, r), encoding='utf-8').read()} for r in sorted(todo)]
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as t: json.dump(bulk, t); tp = t.name
    sys.path.insert(0, os.path.expanduser('~/forge/lib')); import cf   # 22 Nov 2026 (P3): lib/cf.py is the only KV writer (kv token, timeout, rings on failure)
    r = cf.run_put(['/opt/homebrew/bin/npx', 'wrangler', 'kv', 'bulk', 'put', tp, '--namespace-id', NS, '--remote'], capture_output=True, text=True, timeout=300)
    os.unlink(tp)
    if r.returncode == 0: json.dump(new, open(LEDGER, 'w')); print('qia_rc published')
    else: print('qia_rc publish FAILED'); sys.exit(1)
main()
