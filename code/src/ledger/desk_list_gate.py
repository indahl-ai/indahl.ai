#!/usr/bin/env python3
"""desk_list_gate.py (21 Nov 2026, HARD row 26 of LEGACY_CONTROL_AUDIT): one desk list.

ledger/desks.json is the one registry of live desks (id, path, title, division, has_kit, on_home, and the fields the other lists carried).
Seven files used to carry their own hand lists, and retiring STACK left 'stack' behind in some of them. This gate reads every one of those
lists where it still exists and fails if it disagrees with desks.json. A file that reads desks.json instead of carrying a list passes.

  python3 ledger/desk_list_gate.py           check; exit 1 on any disagreement (prints each, rings DESK LIST GATE FAILED: to the pipeline log)
  python3 ledger/desk_list_gate.py --quiet   the same, one summary line
  python3 ledger/desk_list_gate.py --seed    print the registry the current lists imply (used once to write desks.json; never overwrites it)

Lists checked: indahl-ai/build_site.py (DESKS nav, _CODE, HOME breadcrumbs), ledger/live_headlines.py DESKS, indahl-ai/reproduce_kits.py
SPECS and NOKIT, watch/headlines.py HOME, ledger/push_public.sh DESKS, ledger/receipts.py CODE_DIRS, cloudflare-workers/heuremen-door/worker.js
/<desk>/live.json routes. Standard library only; nothing is imported from the files it reads (they are parsed)."""
import ast, json, os, re, sys, time

B = os.path.expanduser('~/forge'); REG = os.path.join(B, 'ledger', 'desks.json'); STATE = os.environ.get('DESK_GATE_STATE') or os.path.join(B, 'ledger', '.desk_list_gate_state.json')
PIPE_LOG = os.environ.get('DESK_GATE_LOG') or os.path.join(B, 'sagar', 'pipeline', 'pipe.log')   # the env override is for dry tests only
F = dict(build=os.path.join(B, 'indahl-ai', 'build_site.py'), lh=os.path.join(B, 'ledger', 'live_headlines.py'), rk=os.path.join(B, 'indahl-ai', 'reproduce_kits.py'),
         hl=os.path.join(B, 'watch', 'headlines.py'), pp=os.path.join(B, 'ledger', 'push_public.sh'), rc=os.path.join(B, 'ledger', 'receipts.py'),
         wk=os.path.join(B, 'cloudflare-workers', 'heuremen-door', 'worker.js'))


def load():
    return json.load(open(REG, encoding='utf-8'))


def _assign(path, name):
    """the literal value of the last module-level `name = <literal>` in a Python file, or None when the file reads it from elsewhere"""
    src = open(path, encoding='utf-8').read()
    rel = os.path.relpath(path, B)
    try: t = ast.parse(src)
    except SyntaxError as e:
        # a file this Python cannot parse (build_site.py uses newer f-string syntax than the bus's 3.9; receipts.py had a stray indent on 21 Nov)
        # is read by pattern: the `name = ...` line at the start of a line. A value that derives from desks.json counts as agreeing (None).
        m = re.search(r'^%s = (.*?)(?:\s*#[^\n]*)?\n(?=\S)' % re.escape(name), src, re.S | re.M)
        if not m: return None
        line = src[:m.start()].count('\n') + 1
        if re.search(r'desks\.json|_DESKREG|\bfor\b', m.group(1)): return None   # a comprehension over the registry, or any derived value
        try: _v = ast.literal_eval(m.group(1)); return _v if _v else None   # an empty literal is filled from desks.json
        except Exception as e2: raise ValueError('%s:%d: %s = ... is not a literal list (%s; the file does not parse here: %s line %s)' % (rel, line, name, type(e2).__name__, e.msg, e.lineno))
    v = first = None
    for n in t.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name:
            seg = ast.get_source_segment(src, n.value) or ''
            if 'desks.json' in seg or '_DESKREG' in seg: v = None; continue   # derived from the registry: agrees by construction
            try: v = ast.literal_eval(n.value)
            except Exception:
                if isinstance(n.value, ast.Dict):   # SPECS/NOKIT: dict(...) values, constant keys
                    try: v = {ast.literal_eval(k): None for k in n.value.keys}
                    except Exception: v = None
                elif isinstance(n.value, ast.ListComp):   # headlines HOME = [s for s in (<tuple>) if s in H]; a later HOME = [s for s in HOME ...] keeps it
                    try: v = list(ast.literal_eval(n.value.generators[0].iter))
                    except Exception: v = None
                else: v = None
            if v is not None and first is None: first = v
    v = v if v is not None else first
    return v if v else None   # an empty literal (DESKS = {} filled from desks.json) is no list of its own


def lists():
    """-> {name: value or None}. None means the file carries no literal list there (it reads desks.json, or the list is gone)."""
    out = {}
    out['build_site DESKS'] = _assign(F['build'], 'DESKS')
    m = re.search(r"DESKS\['/hermes'\] = sorted\(DESKS\['/hermes'\] \+ (\[.*?\]), key", open(F['build'], encoding='utf-8').read())
    if out['build_site DESKS'] is not None and m: out['build_site DESKS']['/hermes'] = out['build_site DESKS']['/hermes'] + ast.literal_eval(m.group(1))
    out['build_site _CODE'] = _assign(F['build'], '_CODE')
    out['build_site HOME'] = _assign(F['build'], 'HOME')
    out['live_headlines DESKS'] = _assign(F['lh'], 'DESKS')
    out['reproduce_kits SPECS'] = _assign(F['rk'], 'SPECS')
    out['reproduce_kits NOKIT'] = _assign(F['rk'], 'NOKIT')
    out['headlines HOME'] = _assign(F['hl'], 'HOME')
    s = open(F['pp'], encoding='utf-8').read(); m = re.search(r"^DESKS = (\{.*?\})\n", s, re.S | re.M)
    out['push_public DESKS'] = eval(m.group(1), {'A': 'add', 'U': 'update', '__builtins__': {}}) if m else None
    out['receipts CODE_DIRS'] = _assign(F['rc'], 'CODE_DIRS')
    out['worker live routes'] = sorted(set(re.findall(r'u\.pathname === ["\'](/[a-z0-9/-]+)/live\.json["\']', open(F['wk'], encoding='utf-8').read())))
    return out


def check(reg=None):
    reg = reg or load(); L = lists(); bad = []
    D = reg['desks']; ids = {d['id']: d for d in D}; retired = set(reg.get('retired', []))
    # build_site DESKS nav: the same paths, in the same order, under the same division
    nav = L['build_site DESKS']
    if nav is not None:
        want = {}
        for d in D:
            if d.get('nav', True): want.setdefault(d['division'], []).append(d['path'])
        have = {dv: [x[0] for x in l] for dv, l in nav.items()}
        for dv in sorted(set(want) | set(have)):
            if dv == '/hermes':   # HERMES is sorted by name at build time, so order is not compared there
                if sorted(want.get(dv, [])) != sorted(have.get(dv, [])): bad.append('build_site DESKS %s: %s' % (dv, _diff(want.get(dv, []), have.get(dv, []))))
            elif want.get(dv, []) != have.get(dv, []): bad.append('build_site DESKS %s: %s' % (dv, _diff(want.get(dv, []), have.get(dv, [])) or 'order differs'))
    # build_site _CODE: the desk entries match desks.json codeline; no retired desk
    code = L['build_site _CODE']
    if code is not None:
        for d in D:
            if d.get('codeline') and d['code_key'] not in code: bad.append('build_site _CODE: %s is missing' % d['code_key'])
            elif d.get('codeline') and [list(x) for x in code[d['code_key']]] != d['codeline']: bad.append('build_site _CODE: %s differs' % d['code_key'])
        for k in code:
            if k in retired: bad.append('build_site _CODE: retired desk %s still listed' % k)
    # build_site HOME breadcrumbs: a desk path's parent is its desks.json home_division
    home = L['build_site HOME'] or {}
    bypath = {d['path']: d for d in D}
    for p, dv in home.items():
        if p in bypath and bypath[p].get('home_division') != dv: bad.append('build_site HOME: %s -> %s, desks.json says %s' % (p, dv, bypath[p].get('home_division')))
        if p.strip('/') in retired: bad.append('build_site HOME: retired desk %s still listed' % p)
    for d in D:
        if d.get('home_division') and d['path'] not in home and L['build_site HOME'] is not None: bad.append('build_site HOME: %s is missing' % d['path'])
    # live_headlines, reproduce_kits, headlines: sets equal to the registry flags
    for name, flag in (('live_headlines DESKS', 'live_headline'), ('reproduce_kits SPECS', 'has_kit'), ('reproduce_kits NOKIT', 'nokit')):
        v = L[name]
        if v is None: continue
        want = {d['id'] for d in D if d.get(flag)}; have = set(v)
        if want != have: bad.append('%s: %s' % (name, _diff(sorted(want), sorted(have))))
    if L['headlines HOME'] is not None:
        want = [d['id'] for d in sorted((d for d in D if d.get('on_home')), key=lambda d: d['home_order'])]
        if list(L['headlines HOME']) != want: bad.append('headlines HOME: %s' % (_diff(want, list(L['headlines HOME'])) or 'order differs'))
    # push_public DESKS and receipts CODE_DIRS: every desk with code is there with the same folder; no retired desk; other keys must be named code_extra
    extra = set(reg.get('code_extra', []))
    pp = L['push_public DESKS']
    if pp is not None:
        for d in D:
            if d.get('code') and (d['code'] not in pp or pp[d['code']] != (d['folder'], d['code_mode'])): bad.append('push_public DESKS: %s %s' % (d['code'], 'missing' if d['code'] not in pp else 'differs %r' % (pp[d['code']],)))
        for k in pp:
            if k in retired: bad.append('push_public DESKS: retired desk %s still listed' % k)
            elif k not in extra and k not in {d.get('code') for d in D}: bad.append('push_public DESKS: %s is neither a desk nor a code_extra in desks.json' % k)
    rc = L['receipts CODE_DIRS']
    if rc is not None:
        inv = {v: k for k, v in rc.items()}
        for d in D:
            if d.get('code') and inv.get(d['code']) != d['folder']: bad.append('receipts CODE_DIRS: %s %s' % (d['code'], 'missing' if d['code'] not in inv else 'folder %s' % inv[d['code']]))
        for k, v in rc.items():
            if v in retired: bad.append('receipts CODE_DIRS: retired desk %s still listed' % v)
            elif v not in extra and v not in {d.get('code') for d in D}: bad.append('receipts CODE_DIRS: %s is neither a desk nor a code_extra in desks.json' % v)
    # worker routes: every desk feed has a route; no route for a retired desk
    routes = {r + '/live.json' for r in L['worker live routes']}
    for d in D:
        if d.get('feed') and d['feed'] not in routes: bad.append('worker.js: no /live.json route for %s (%s)' % (d['id'], d['feed']))
    for r in sorted(routes):
        if r[:-len('/live.json')].strip('/') in retired: bad.append('worker.js: route %s/live.json for a retired desk' % r)
    return bad, L


def _diff(want, have):
    a = [x for x in want if x not in have]; b = [x for x in have if x not in want]
    return ('desks.json only: %s' % ', '.join(map(str, a)) if a else '') + ('; ' if a and b else '') + ('file only: %s' % ', '.join(map(str, b)) if b else '')


def seed():
    """the registry the current lists imply, with every disagreement between them printed"""
    L = lists(); nav = L['build_site DESKS']; LHk = set(L['live_headlines DESKS'] or []); SP = set(L['reproduce_kits SPECS'] or []); NK = set(L['reproduce_kits NOKIT'] or [])
    HOMEl = list(L['headlines HOME'] or []); pp = L['push_public DESKS'] or {}; rc = L['receipts CODE_DIRS'] or {}; code = L['build_site _CODE'] or {}; bh = L['build_site HOME'] or {}
    routes = set(L['worker live routes'])
    SPECIAL = {'/census/revisions': 'census', '/census/coverage': 'census-coverage', '/census/fidelity': 'fidelity', '/census/vintages': 'census-vintages', '/census': 'census-division', '/iris/lab': 'lab', '/hermes/model': 'model', '/hermes/datapapers': 'datapapers'}
    CODE_OF = {'census': 'census', 'census-coverage': 'census-coverage', 'fidelity': 'fidelity', 'predictions': 'now'}
    desks = []
    for dv, l in nav.items():
        for path, title, what in l:
            i = SPECIAL.get(path) or path.strip('/').split('/')[-1]
            c = CODE_OF.get(i, i)
            ck = 'predictions' if i == 'predictions' else i
            feed = path + '/live.json' if path in routes else ('/%s/live.json' % i if '/%s' % i in routes else None)
            d = dict(id=i, path=path, title=title, what=what, division=dv, kind='division' if path in ('/oy', '/census') else 'desk', nav=True,
                     home_division=bh.get(path), live_headline=i in LHk, has_kit=i in SP, nokit=i in NK, on_home=i in HOMEl, home_order=HOMEl.index(i) if i in HOMEl else None,
                     feed=('/' + i if '/' + i in routes else (path if path in routes else None)), code=c if c in pp else None,
                     folder=pp[c][0] if c in pp else None, code_mode=pp[c][1] if c in pp else None, code_key=ck if ck in code else None,
                     codeline=[list(x) for x in code[ck]] if ck in code else None)
            if d['feed'] and d['kind'] == 'division': d['feed'] = None   # /census/live.json belongs to the REVISIONS desk
            if d['feed']: d['feed'] = d['feed'] + '/live.json'
            desks.append(d)
    known = {d['id'] for d in desks}; codes = {d['code'] for d in desks if d['code']}
    notes = []
    for name, s in (('live_headlines DESKS', LHk), ('reproduce_kits SPECS', SP), ('reproduce_kits NOKIT', NK), ('headlines HOME', set(HOMEl))):
        for x in sorted(s - known): notes.append('%s lists %s, which is not a nav desk' % (name, x))
    for k in pp:
        if k not in codes: notes.append('push_public DESKS lists code %s, which is no nav desk' % k)
    for v in rc.values():
        if v not in codes: notes.append('receipts CODE_DIRS lists code %s, which is no nav desk' % v)
    for k in code:
        if k not in {d['code_key'] for d in desks}: notes.append('build_site _CODE lists %s, which is no nav desk' % k)
    for r in sorted(routes):
        if r.strip('/') not in known and r not in {d['path'] for d in desks}: notes.append('worker.js serves %s/live.json, which is no nav desk' % r)
    for d in desks:
        if d['live_headline'] and not (d['has_kit'] or d['nokit']): notes.append('%s has a ledger headline but neither a kit nor a no-kit entry' % d['id'])
        if d['code'] and rc and d['code'] not in rc.values(): notes.append('%s: push_public has code %s, receipts CODE_DIRS does not' % (d['id'], d['code']))
        if d['kind'] == 'desk' and d['path'] not in bh: notes.append('%s: no build_site HOME breadcrumb' % d['path'])
    return dict(desks=desks), notes


def ring(msg):
    try:
        with open(PIPE_LOG, 'a') as f: f.write('%s %s\n' % (time.strftime('%Y-%m-%dT%H:%M:%S'), msg[:600]))
    except Exception: pass


def main():
    if '--seed' in sys.argv:
        r, notes = seed(); print(json.dumps(r, indent=1, ensure_ascii=False)); print('\n'.join('NOTE ' + n for n in notes), file=sys.stderr); return 0
    try: bad, L = check()
    except Exception as e:
        bad = ['could not read the lists (%s: %s)' % (type(e).__name__, str(e)[:240])]; print('DESK LIST GATE FAILED: ' + bad[0])
        try: last = json.load(open(STATE)).get('bad', [])
        except Exception: last = None
        if bad != last:
            ring('DESK LIST GATE FAILED: ' + bad[0])
            try: json.dump({'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'bad': bad}, open(STATE, 'w'))
            except Exception: pass
        return 1
    reads = [k for k, v in L.items() if v is None]
    if '--quiet' not in sys.argv:
        for b in bad: print('  ' + b)
        if reads: print('  reading desks.json (no own list): ' + ', '.join(reads))
    # 21 Nov 2026 (coordinator: the gate rang the doorbell on every alerts_check run): ring only when the set of disagreements changes
    # (a new set, or cleared); the last set is kept in ledger/.desk_list_gate_state.json. The exit code still reports every run.
    try: last = json.load(open(STATE)).get('bad', [])
    except Exception: last = None
    if sorted(bad) != last:
        if bad: ring('DESK LIST GATE FAILED: %d disagreement(s): %s' % (len(bad), '; '.join(bad)[:400]))
        elif last: ring('desk list gate: cleared, every list agrees with ledger/desks.json')
        try: tmp = STATE + '.tmp'; json.dump({'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'bad': sorted(bad)}, open(tmp, 'w'), indent=1); os.replace(tmp, STATE)
        except Exception: pass
    if bad:
        print('DESK LIST GATE FAILED: %d disagreement(s) with ledger/desks.json: %s' % (len(bad), '; '.join(bad)[:400])); return 1
    print('desk list gate: every list agrees with ledger/desks.json (%d desks)' % len(load()['desks'])); return 0


if __name__ == '__main__':
    sys.exit(main())
