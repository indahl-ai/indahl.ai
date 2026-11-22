#!/usr/bin/env python3
"""Read-only preflight for ENV_PLAN.md (PARTS #22 + #26). Changes nothing.

Run it with the interpreter being checked, from anywhere:
  ~/forge/busenv/bin/python -I bus_preflight.py --batch 1     # check one batch
  ~/forge/busenv/bin/python -I bus_preflight.py --imports     # third-party names for requirements.in

It imports ~/forge/watch/desk_riders.py (RIDERS = [(every, [argv]), ...] and the
BATCH table from ENV_PLAN.md), takes each rider's first *.py argument, and for each script:
compiles it, lists its top-level imports, checks each one resolves under THIS interpreter
(local modules next to the script, in watch/, ~/forge or ~/forge/lib count as
found), and flags modules that Python 3.12 removed. It prints script and module names only.
Exit 1 if anything in the batch fails. Needs Python 3.10+ (sys.stdlib_module_names).
"""
import argparse, ast, importlib.util, os, sys

FORGE = os.path.expanduser('~/forge')
WATCH = os.path.join(FORGE, 'watch')
REMOVED_312 = {'distutils', 'imp', 'asynchat', 'asyncore', 'smtpd'}


def load_riders():
    sys.path.insert(0, WATCH)
    import desk_riders
    sys.path.pop(0)
    return desk_riders


def script_of(argv):
    for a in argv[1:]:
        if a.endswith('.py'):
            return a if os.path.isabs(a) else os.path.normpath(os.path.join(WATCH, a))
    return None


def top_imports(path):
    tree = ast.parse(open(path, encoding='utf-8').read(), filename=path)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split('.')[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split('.')[0])
    return names


def is_local(name, script):
    for d in (os.path.dirname(script), WATCH, FORGE, os.path.join(FORGE, 'lib')):
        if os.path.exists(os.path.join(d, name + '.py')) or os.path.isdir(os.path.join(d, name)):
            return True
    return False


def third_party(names, script):
    return sorted(n for n in names if n not in sys.stdlib_module_names and n not in REMOVED_312 and not is_local(n, script))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch', type=int)
    ap.add_argument('--imports', action='store_true')
    a = ap.parse_args()
    d = load_riders()
    batch = getattr(d, 'BATCH', {})
    picked, seen = [], {}
    for every, argv in d.RIDERS:
        s = script_of(argv)
        if not s:
            continue
        b = batch.get(os.path.basename(s), 0)
        seen.setdefault(os.path.basename(s), set()).add(s)
        if (a.imports and b) or (a.batch is not None and b == a.batch):
            picked.append((every, argv, s))
    bad = 0
    for base, paths in sorted(seen.items()):
        if base in batch and len(paths) > 1:
            print('DUPLICATE BASENAME in BATCH: %s -> %d scripts' % (base, len(paths))); bad += 1
    if a.imports:
        allnames = set()
        for _, _, s in picked:
            if os.path.exists(s):
                allnames.update(third_party(top_imports(s), s))
        print('\n'.join(sorted(allnames)))
        return 1 if bad else 0
    print('interpreter %s  %s' % (sys.executable, sys.version.split()[0]))
    for every, argv, s in picked:
        name = os.path.relpath(s, FORGE)
        if not os.path.exists(s):
            print('MISSING  %s' % name); bad += 1; continue
        try:
            compile(open(s, encoding='utf-8').read(), s, 'exec')
        except (SyntaxError, ValueError) as e:
            print('SYNTAX   %s  line %s' % (name, getattr(e, 'lineno', '?'))); bad += 1; continue
        names = top_imports(s)
        gone = sorted(names & REMOVED_312)
        missing = [n for n in third_party(names, s) if importlib.util.find_spec(n) is None]
        status = 'OK      ' if not (gone or missing) else 'FAIL    '
        bad += bool(gone or missing)
        print('%s %s  every=%s%s%s' % (status, name, every,
              ('  removed-in-3.12: ' + ','.join(gone)) if gone else '',
              ('  not installed: ' + ','.join(missing)) if missing else ''))
    print('%d riders, %d problems' % (len(picked), bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
