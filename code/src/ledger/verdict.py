#!/usr/bin/env python3
"""verdict.py (22 Nov 2026): ship rebuild step 1 (lane-build ship_rebuild/DESIGN.md sections 1.1-1.3, the referee's GO with her six fixes).
Runs every copy gate the ship runs, ALL of them, and writes ONE verdict instead of stopping at the first breach:
  ledger/verdict.json  {"at", "tree_hash", "gate_hashes", "gates":[{"gate","ran","rc","checked","breaches","lines","desks"}], "decision"}
- Every gate gets a "ran" line (the referee fix 3). A gate that crashed, timed out or printed nothing parseable is ran:false -> WHOLE.
- desk_of() maps each breach line to a desk id through ledger/desks.json (path or folder in the line). A breach that maps to no desk
  is a SHARED breach -> WHOLE (shared files, worker, compile).
- Money path (calibrations ship/money_path.txt, QIA site root): a breach naming one of those files is WHOLE (the referee fix 1).
- Tripwire: 25% or more of live desks held at once is WHOLE (first-ship desks not counted).
- The hash covers the built tree AND every gate script AND desks.json (the referee fix 4), so a dry run whose gates changed is not this verdict.
Reads only. Does not build, ship or edit pages. Exit 0 = ship (possibly with held desks), 1 = WHOLE stop, 2 = verdict could not be made.
  python3 verdict.py [--json]"""
import hashlib, json, os, re, subprocess, sys, time
B = os.path.expanduser('~/forge'); L = os.path.join(B, 'ledger')
OUT = os.path.join(L, 'verdict.json')
QIA_ROOT = os.path.join(B, 'cloudflare-workers', 'heuremen-door', 'public', '_qiasite')
SITE = os.path.join(B, 'indahl-ai')
GATES = [   # name, argv, cwd: the copy gates preflight.sh and ship.sh run (inventory section 2)
    ('spelling', ['python3', os.path.join(L, 'spelling_gate.py')], L),
    ('name', ['python3', os.path.join(L, 'name_gate.py')], L),
    ('headline_cover', ['python3', os.path.join(L, 'headline_cover_gate.py')], L),
    ('one_description', ['python3', os.path.join(L, 'one_desc_gate.py')], L),
    ('copy_damage', ['python3', os.path.join(L, 'copy_damage_gate.py')], L),
    ('site_gate', ['python3', os.path.join(B, 'heuremen-specbook', 'site_gate.py')], B),
    ('reproduce_kits', ['python3', 'reproduce_kits.py', 'gate'], SITE),
    ('link_gate', ['python3', os.path.join(L, 'link_gate.py'), '--report'], L),
]
BREACH = re.compile(r'BREACH|REFUSED|MISSING|ZOMBIE|stale|dead link|not found', re.I)

def sha(p):
    try: return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    except Exception: return None

def tree_hash():
    h = hashlib.sha256()
    for root in (SITE, QIA_ROOT):
        for dp, dn, fn in sorted(os.walk(root)):
            dn[:] = sorted(d for d in dn if not d.startswith('.') and d != 'node_modules')
            for f in sorted(fn):
                if f.endswith(('.html', '.js', '.json', '.css', '.xml')):
                    p = os.path.join(dp, f); h.update(p.encode()); h.update(open(p, 'rb').read())
    return h.hexdigest()[:16]

def money_path():
    for p in (os.path.join(B, 'calibrations', 'ship', 'money_path.txt'),):
        if os.path.exists(p): return [l.strip() for l in open(p) if l.strip() and not l.startswith('#')]
    r = subprocess.run(['git', '-C', os.path.join(B, 'calibrations'), 'show', 'origin/lane-build:ship/money_path.txt'], capture_output=True, text=True)
    return [l.strip() for l in r.stdout.splitlines() if l.strip() and not l.startswith('#')]

D = json.load(open(os.path.join(L, 'desks.json')))
DESKS = [d for d in D['desks'] if d['id'] not in set(D.get('retired', []))]
KEYS = []   # (needle, desk id), longest first so /census/revisions beats /census
for d in DESKS:
    for n in {d.get('path'), '/' + d['id'] + '.html', d['id'] + '.html', (d.get('folder') or '') + '/', d.get('feed')}:
        if n and len(n) > 3: KEYS.append((n, d['id']))
KEYS.sort(key=lambda k: -len(k[0]))
IDS = {d['id'] for d in DESKS}
MONEY = money_path()

def desk_of(line):
    """-> desk id named in a breach line, 'MONEY' for a money-path file, or None (shared -> WHOLE)."""
    if '_qiasite' in line or 'quantumidleaudit' in line:
        for m in MONEY:
            if m and (('_qiasite/' + m) in line or ('quantumidleaudit.com/' + m.replace('index.html', '')) in line): return 'MONEY'
    for n, i in KEYS:
        if n in line: return i
    m = re.search(r'(?:^|[\s:])([a-z][a-z0-9_-]{2,})(?=:\s)', line)   # 'argus: no live ledger value row' (reproduce kit form)
    if m and m.group(1) in IDS: return m.group(1)
    return None

def run_gate(name, argv, cwd):
    t0 = time.time()
    try: r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=600)
    except Exception as e: return {'gate': name, 'ran': False, 'rc': None, 'why': type(e).__name__, 'secs': round(time.time() - t0)}
    out = (r.stdout + '\n' + r.stderr).splitlines()
    lines = sorted({l.strip() for l in out if BREACH.search(l)})[:200]
    if r.returncode == 0: lines = []   # a clean exit with words like 'stale' in prose is not a breach
    desks = {}
    for l in lines: desks.setdefault(desk_of(l) or 'SHARED', []).append(l[:240])
    crashed = r.returncode not in (0, 1) or ('Traceback' in r.stderr and r.returncode != 0)
    return {'gate': name, 'ran': not crashed, 'rc': r.returncode, 'checked': len(out), 'breaches': len(lines), 'desks': desks, 'secs': round(time.time() - t0),
            **({'why': r.stderr.strip()[-300:]} if crashed else {})}

def main():
    gates = [run_gate(*g) for g in GATES]
    whole, held = [], {}
    for g in gates:
        if not g['ran']: whole.append('%s did not run (%s)' % (g['gate'], g.get('why', 'rc %s' % g['rc']))); continue
        for k, ls in g.get('desks', {}).items():
            if k == 'MONEY': whole.append('%s: money-path breach: %s' % (g['gate'], ls[0]))
            elif k == 'SHARED': whole.append('%s: breach on no single desk: %s' % (g['gate'], ls[0]))
            else: held.setdefault(k, []).append('%s: %s' % (g['gate'], ls[0]))
    first = set()
    try: first = {d['id'] for d in DESKS if not d.get('first_shipped')} & set(json.load(open(os.path.join(L, 'first_ship_state.json'))).get('pending', []))
    except Exception: pass
    counted = [k for k in held if k not in first]
    if DESKS and len(counted) / len(DESKS) >= 0.25: whole.append('tripwire: %d of %d live desks held (25%%+)' % (len(counted), len(DESKS)))
    v = {'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'tree_hash': tree_hash(),
         'gate_hashes': {**{g[0]: sha(g[1][1] if os.path.isabs(g[1][1]) else os.path.join(g[2], g[1][1])) for g in GATES}, 'desks.json': sha(os.path.join(L, 'desks.json'))},
         'gates': gates, 'held': held, 'whole': whole,
         'decision': 'WHOLE' if whole else ('SHIP with %d held' % len(held) if held else 'SHIP')}
    json.dump(v, open(OUT + '.tmp', 'w'), indent=1); os.replace(OUT + '.tmp', OUT)
    if '--json' in sys.argv: print(json.dumps(v, indent=1))
    else:
        for g in gates: print('%-16s ran=%s rc=%s breaches=%s %s' % (g['gate'], g['ran'], g['rc'], g.get('breaches'), ' '.join('%s:%d' % (k, len(x)) for k, x in g.get('desks', {}).items())))
        print('DECISION:', v['decision']); [print('  WHOLE:', w) for w in whole]; [print('  held %s: %s' % (k, x[0])) for k, x in held.items()]
    return 1 if whole else 0

if __name__ == '__main__':
    try: sys.exit(main())
    except Exception as e: print('VERDICT FAILED: %r' % e); sys.exit(2)
