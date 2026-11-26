#!/usr/bin/env python3
"""demo_replay_gate.py: the qia.com demo pages may not say what the public replay code does not print.

24 Nov 2026. Cause it guards: the demo data (calibrations/site/make_demos_json.py -> demos.json, impact.json) was written by hand
from check notes, and the chemistry headline said "Up to 16 times closer" on a ratio whose calibrated error had a 99% interval
reaching zero. Nothing compared the page with the replay code, and nothing tied the headline lines to the tables.

Two checks, run by ledger/ship_qia.sh before deploy:
  1 every demonstration whose verifier reads demos.json (demo_sandbox/<demo>/verify_replay.py) replays and must print ALL PASS.
    Slow (minutes), so it runs only when demos.json changed since the last pass (hash in ledger/gates/demo_replay_gate.ok).
  2 every "Up to N times" line in impact.json may not exceed the largest point ratio in that demonstration's chips table, and is
    refused when any chip in that table carries only a bound (">5x"): a maximum over a column with an open end is not a reading.
Exit 0 = pass, 1 = refuse (the reason on the last line)."""
import hashlib, json, os, re, subprocess, sys

B = os.path.expanduser('~/forge')
SITE = os.path.join(B, 'calibrations', 'site')
OK = os.path.join(B, 'ledger', 'gates', 'demo_replay_gate.ok')
PY = os.path.join(B, 'qvenv', 'bin', 'python')
VERIFIED = ('chemistry', 'ai_kernels')     # folders whose verify_replay.py takes demos.json


def ratio_check(demos, impact):
    bad = []
    for slug, lines in impact.items():
        for ln in lines:
            m = re.search(r'Up to ([\d.]+) times', ln)
            if not m: continue
            d = [x for x in demos if x['slug'] == slug]
            if not d or 'chips' not in d[0]: bad.append('%s: "Up to %s times" with no chips table to back it' % (slug, m.group(1))); continue
            toks = [c[3].split()[0] for c in d[0]['chips']]
            if any(t.startswith('>') for t in toks): bad.append('%s: "Up to %s times" over a column with a bound (%s)' % (slug, m.group(1), ', '.join(toks))); continue
            top = max(float(t.rstrip('x')) for t in toks)
            if float(m.group(1)) > top + 1e-9: bad.append('%s: "Up to %s times" but the table maximum is %g (a headline may not exceed its table)' % (slug, m.group(1), top))
    return bad


RETIRED = [r'16 ?(x|×|times)', r'3\.7 ?(x|×|times)', r'(up to|by) 1\.8 ?(x|×|times)', r'\$50\b']   # 24 Nov 2026: figures withdrawn from the pages
RELEASE_DIRS = [os.path.join(B, 'calibrations', 'demos', 'release'), os.path.join(B, 'biz')]


def retired_check():
    """The release and pitch drafts are written by hand from the pages; a figure withdrawn from the pages must not survive in them."""
    import glob
    bad = []
    files = sorted(glob.glob(os.path.join(RELEASE_DIRS[0], 'RELEASE_FINAL_*.md')), key=os.path.getmtime)[-1:]
    files += glob.glob(os.path.join(RELEASE_DIRS[1], '**', '*PITCH*.md'), recursive=True)
    files += glob.glob(os.path.join(B, 'calibrations', 'biz', '**', 'LAUNCH_NOTE*.md'), recursive=True)   # 25 Nov: the launch note kept 16x/3.7/1.8 unseen
    try:   # the launch note lives on lane-biz, not in the checked-out branch: read it from there
        _c = os.path.join(B, 'calibrations'); subprocess.run(['git', '-C', _c, 'fetch', '-q', 'origin', 'lane-biz'], capture_output=True, timeout=60)
        _t = subprocess.run(['git', '-C', _c, 'show', 'origin/lane-biz:biz/LAUNCH_NOTE_27NOV.md'], capture_output=True, text=True, timeout=30).stdout
        if _t:
            _lp = os.path.join(B, 'ledger', 'gates', 'lane_biz_LAUNCH_NOTE_27NOV.md'); os.makedirs(os.path.dirname(_lp), exist_ok=True); open(_lp, 'w').write(_t); files.append(_lp)
    except Exception as _e: bad.append('launch note on lane-biz unreadable: ' + type(_e).__name__)
    for f in files:
        t = open(f, encoding='utf-8', errors='replace').read()
        # 25 Nov 2026: the wire release must name no vendor and no processor (IBM courtesy rule); a 24 Nov edit put 'ibm_fez' in it unseen
        # 25 Nov 2026 (the referee): v12's top comment line ('withdrawn figures', 'Google Voice') rides along when the file is copied whole into
        # Business Wire. The release file carries the release text only; version notes live in RELEASE_FINAL_vN.NOTE.md.
        if os.path.basename(f).startswith('RELEASE_FINAL') and '<!--' in t:
            bad.append('%s: holds an internal comment (copied whole to the wire); move it to a .NOTE.md file' % os.path.relpath(f, B))
        if os.path.basename(f).startswith('RELEASE_FINAL') or 'LAUNCH_NOTE' in f:
            for m in re.finditer(r'\bibm\b|ibm_\w+|\b(fez|kingston|marrakesh|torino|brisbane|sherbrooke|heron|eagle|nighthawk)\b', t, re.I):
                if '<!--' in t[max(0, m.start() - 200):m.start()] and '-->' not in t[max(0, m.start() - 200):m.start()]: continue   # internal comment line
                bad.append('%s: names a vendor or processor %r (release names none)' % (os.path.relpath(f, B), m.group(0)))
        for pat in RETIRED:
            for m in re.finditer(pat, t, re.I):
                if 'q147' in t[max(0, m.start() - 40):m.end()]: continue      # 16.7x is a different figure (q147 readout)
                bad.append('%s: withdrawn figure %r' % (os.path.relpath(f, B), m.group(0)))
    return bad


def main():
    dj, ij = os.path.join(SITE, 'demos.json'), os.path.join(SITE, 'impact.json')
    demos = json.load(open(dj))['demos']; impact = json.load(open(ij))
    bad = ratio_check(demos, impact) + retired_check()
    if bad:
        print('\n'.join(bad)); print('REFUSED: impact line not backed by its table'); return 1
    h = hashlib.sha256(open(dj, 'rb').read()).hexdigest()
    if os.path.exists(OK) and open(OK).read().strip() == h:
        print('demo replay gate: demos.json unchanged since the last pass; impact lines ok'); return 0
    for f in VERIFIED:
        d = os.path.join(B, 'demo_sandbox', f)
        r = subprocess.run([PY, 'verify_replay.py', dj], cwd=d, capture_output=True, text=True, timeout=1800)
        out = r.stdout + r.stderr
        if '| FAIL' in out or r.returncode != 0 or '| PASS' not in out:
            fails = [l for l in out.splitlines() if '| FAIL' in l][:3]
            print('\n'.join(fails)); print('REFUSED: %s page figures differ from the replay code' % f); return 1
    os.makedirs(os.path.dirname(OK), exist_ok=True); open(OK, 'w').write(h + '\n')
    print('demo replay gate: %s replay ALL PASS against demos.json; impact lines ok' % ' and '.join(VERIFIED)); return 0


if __name__ == '__main__':
    sys.exit(main())
