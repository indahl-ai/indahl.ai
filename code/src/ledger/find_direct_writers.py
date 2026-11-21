#!/usr/bin/env python3
"""find_direct_writers.py (21 Nov 2026). Lists every program in the house that writes ledger.jsonl without going through ledger.save.

Why: ledger.save holds the one lock and merges; a program that opens the ledger file for writing itself is a second writer with no lock
(The referee, 21 Nov 02:02Z). On 21 Nov this search found one, ledger/reword.py, and it was routed through save the same hour.

How: walks ~/bones-forge for .py and .sh files that name `ledger.jsonl` exactly (look_ledger.jsonl, flywheel_ledger.jsonl and the like are
other files). In each, it finds every name bound to an expression holding that path, and reports a line that opens that name (or the literal
path) for writing or appending, replaces or renames onto it, copies onto it, or redirects into it. Backups, archives, mirrors and vendored
folders are skipped (the SKIP list below). A copy FROM the ledger to a backup name is not a write.
Allowed: ledger.py itself (its save is the one writer).   Exit 1 if anything else is found.   python3 find_direct_writers.py"""
import os, re, sys
B = os.path.expanduser('~/bones-forge')
SKIP = ('/.git/', '/node_modules/', '/archive/', '/public_mirror', '/hf_stage', '/scratch', '/sink_sorted', '/qia_leads/sweep_', '/.venv', '/venv/', '/site-packages/')
NAME = re.compile(r'(?<![A-Za-z_])ledger\.jsonl')
ALLOWED = {'ledger/ledger.py': 'its save() is the one writer',
           'gridsong/wire_clocked.py': "read 21 Nov 2026: its self-test binds LOG to a file named ledger.jsonl inside its own temporary folder (tmp), not the house ledger"}
found, n = [], 0
for d, ds, fs in os.walk(B):
    if any(s in '/' + os.path.relpath(d, B) + '/' for s in SKIP): ds[:] = []; continue   # tested against the path inside the house, so the house itself may live anywhere
    for f in fs:
        if not f.endswith(('.py', '.sh')) or '.bak' in f or f.startswith('pre-') or f == 'find_direct_writers.py' or f == 'test_two_writers.py': continue
        p = os.path.join(d, f)
        try: t = open(p, errors='ignore').read()
        except Exception: continue
        if not NAME.search(t): continue
        n += 1; L = t.split('\n'); names = set()
        for l in L:
            for m in re.finditer(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*=\s*[^=\n]*(?<![A-Za-z_])ledger\.jsonl[\'"]?\s*\)?\s*(?:[;#]|$)', l): names.add(m.group(1))
        for i, l in enumerate(L):
            hit = False
            for v in names:
                e = re.escape(v)
                if re.search(r"open\(\s*%s\s*,\s*['\"][wax]" % e, l) or re.search(r"os\.(replace|rename)\([^)]*,\s*%s\s*\)" % e, l) or re.search(r"%s\.write_text|>\s*\"?\$\{?%s\b" % (e, e), l) or re.search(r"shutil\.(copy2?|copyfile|move)\([^,]+,\s*%s\s*\)" % e, l): hit = True
            if NAME.search(l) and re.search(r"open\([^)]*ledger\.jsonl['\"]?\s*\)?\s*,\s*['\"][wax]|os\.(replace|rename)\([^)]*ledger\.jsonl['\"]?\s*\)\s*\)?|>\s*\S*(?<![A-Za-z_])ledger\.jsonl\b|shutil\.(copy2?|copyfile|move)\([^,]+,[^)]*(?<![A-Za-z_])ledger\.jsonl['\"]?\s*\)", l): hit = True
            if hit: found.append((os.path.relpath(p, B), i + 1, l.strip()[:160]))
out = [x for x in found if x[0] not in ALLOWED]
print('programs that name ledger.jsonl: %d | lines that write a file of that name: %d | allowed, each with its reason: %d | direct writers: %d' % (n, len(found), len(found) - len(out), len(out)))
for x in found:
    if x[0] in ALLOWED: print('  allowed %s line %d (%s)' % (x[0], x[1], ALLOWED[x[0]]))
for x in out: print('  DIRECT WRITER %s line %d: %s' % x)
sys.exit(1 if out else 0)
