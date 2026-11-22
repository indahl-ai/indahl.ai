#!/usr/bin/env python3
"""auto_ship.py (11 Nov 2026, the owner: "we're not a static site, we dynamic").

The desk riders put fresh numbers in the live feeds every few ticks, but the page tables, brand and entity pages, /forecasters,
data packs, receipts and Zenodo only move when ship.sh runs. This rider closes that gap: when any desk summary has changed since
the last ship, and nobody holds the site lock, it runs the one release path (site_lock.py + ship.sh). It never edits anything itself.

  python3 auto_ship.py          ship if the desk summaries moved since the last ship and the lock is free
  python3 auto_ship.py --dry    say what it would do

State: ledger/auto_ship_state.json (fingerprint shipped last). A failed ship writes ledger/auto_ship_status.json for alerts_check.py."""
import fcntl, glob, hashlib, json, os, subprocess, sys, time

B = os.path.expanduser('~/forge'); L = B + '/ledger'
STATE, STATUS, FLOCK = L + '/auto_ship_state.json', L + '/auto_ship_status.json', L + '/.site_edit.flock'
MIN_GAP = 3 * 3600   # at most one automatic ship every three hours


def fingerprint():
    files = sorted(glob.glob(B + '/*_index/summary_*.json') + glob.glob(B + '/*_index/*/summary_*.json'))
    h = hashlib.sha256(); moved = []
    for f in files:
        try: b = open(f, 'rb').read()
        except OSError: continue
        h.update(f.encode() + b'\0' + hashlib.sha256(b).digest())
    return h.hexdigest(), files


def lock_free():
    try:
        f = open(FLOCK, 'a+'); fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB); fcntl.flock(f, fcntl.LOCK_UN); return True
    except OSError:
        return False


def main():
    dry = '--dry' in sys.argv
    st = json.load(open(STATE)) if os.path.exists(STATE) else {}
    fp, files = fingerprint()
    if fp == st.get('fingerprint'): print('auto_ship: desk summaries unchanged since the last ship'); return 0
    since = time.time() - st.get('at', 0)
    if since < MIN_GAP: print(f'auto_ship: changed, but the last automatic ship was {int(since / 60)} min ago (gap {MIN_GAP // 3600} h)'); return 0
    if not lock_free(): print('auto_ship: changed, but the site lock is held; next tick'); return 0
    if dry: print(f'auto_ship: would ship now ({len(files)} desk summaries read, fingerprint changed)'); return 0
    msg = 'auto: desk feeds moved since the last ship, pages, packs, receipts and Zenodo follow'
    # 21 Nov 2026: the ship is requested from the ship queue (ledger/ship_request.sh) and this rider returns; the queue runner ships every
    # pending request at once, rings pipe.log on a nonzero exit and writes/clears ledger/auto_ship_status.json for alerts_check.py.
    r = subprocess.run(['bash', L + '/ship_request.sh', msg], capture_output=True, text=True, timeout=120,
                       env=dict(os.environ, PATH='/opt/homebrew/bin:' + os.environ.get('PATH', '')))   # 11 Nov: same python3 as a hand ship (the bus PATH gave 3.9)
    if r.returncode:
        json.dump({'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'ok': False, 'rc': r.returncode, 'tail': (r.stdout + r.stderr)[-1500:]}, open(STATUS, 'w'))
        print(f'auto_ship: ship request failed (rc {r.returncode}); status written for the watch'); return 0
    json.dump({'fingerprint': fp, 'at': time.time(), 'files': len(files)}, open(STATE, 'w'))   # the MIN_GAP clock starts at the request
    print('auto_ship: ship requested from the queue: ' + r.stdout.strip().split('\n')[-1]); return 0


if __name__ == '__main__':
    sys.exit(main())
