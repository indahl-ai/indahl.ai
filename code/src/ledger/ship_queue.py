#!/usr/bin/env python3
"""ship_queue.py (21 Nov 2026): one ship for many callers, so ships stop running back to back and a hand change always finds a window.

Callers do not run ship.sh themselves. They append a request with ledger/ship_request.sh "<label>" and return. One runner (its own lock,
ledger/.ship_queue_runner.flock) takes every pending request, waits for the site lock (site_lock.py), runs ONE ship.sh labeled with all the
pending labels joined, marks each request done with the ship's exit code, and loops while new requests arrived during the run.
Each run logs one line to sagar/pipeline/pipe.log (22 Nov P2: the ONE ring per ship): `RING: SHIP FAILED at <step>: <reason> ...` from the FAIL line
ship.sh wrote to ledger/.ship_queue_result.txt, `RING: SHIP OK with N notes` for non-fatal problems, or `SHIP QUEUE: ship exit 0 ...` (no ring).

  python3 ship_queue.py add "<label>"            append a request (an identical label still pending is not added twice); prints its id
  (22 Nov) one bundled ship per hour; MONEY:/URGENT: labels ship at once. SHIP_CLOCK_S overrides.
  python3 ship_queue.py run                      the runner (ship_request.sh starts it; a second runner exits at once)
  python3 ship_queue.py wait <id> [--timeout S]  block until that request is done; exit with its ship's exit code (124 on timeout)
  python3 ship_queue.py status                   pending and running requests, and the last done ones

Queue file: ledger/ship_queue.jsonl, one JSON object per request, rewritten under ledger/.ship_queue.flock.
A ship started by hand (bash ledger/ship.sh "...") still works and simply waits for the site lock like before.
Standard library only, Python 3.9 safe."""
import fcntl, json, os, signal, subprocess, sys, time, uuid
from contextlib import contextmanager

L = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(L)
Q, QLOCK, RLOCK = L + '/ship_queue.jsonl', L + '/.ship_queue.flock', L + '/.ship_queue_runner.flock'
PIPE = B + '/sagar/pipeline/pipe.log'; LAST = L + '/ship_queue_last.log'
AUTO_STATUS = L + '/auto_ship_status.json'   # watch/alerts_check.py reads it; auto_ship.py now queues its ship, so the runner writes it
SHIP_TIMEOUT = 45 * 60   # 23 Nov 2026 (the designer review #6): a healthy ship is 1-7 min; was 3 h, which held MONEY fixes behind a hung ship.  lock wait plus ship; a hung ship is killed (its whole process group) and marked exit 124
KEEP_DONE = 200


def ts(): return time.strftime('%Y-%m-%dT%H:%M:%S')


@contextmanager
def qlock():
    f = open(QLOCK, 'a+'); fcntl.flock(f, fcntl.LOCK_EX)
    try: yield
    finally: fcntl.flock(f, fcntl.LOCK_UN); f.close()


def load():
    if not os.path.exists(Q): return []
    out = []
    for l in open(Q, encoding='utf-8'):
        l = l.strip()
        if l:
            try: out.append(json.loads(l))
            except ValueError: pass
    return out


def save(rows):
    done = [r for r in rows if r.get('status') == 'done']; rest = [r for r in rows if r.get('status') != 'done']
    rows = done[-KEEP_DONE:] + rest
    with open(Q + '.tmp', 'w', encoding='utf-8') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    os.replace(Q + '.tmp', Q)


def log(line):
    try:
        with open(PIPE, 'a') as f: f.write('%s %s\n' % (ts(), line))
    except OSError as e: sys.stderr.write('ship_queue: could not write pipe.log (%s)\n' % e)
    print(line, flush=True)


def add(label):
    with qlock():
        rows = load()
        for r in rows:
            if r.get('status') == 'pending' and r.get('label') == label:
                print(r['id']); return 0
        rid = time.strftime('%Y%m%d-%H%M%S-') + uuid.uuid4().hex[:6]
        rows.append({'id': rid, 'label': label, 'requested': ts(), 'status': 'pending'}); save(rows)
    # 22 Nov 2026: a MONEY request added with 'add' alone sat pending 8 minutes with no runner alive (only ship_request.sh started one).
    # Now 'add' starts the runner itself when none holds the runner lock, and says that ship_request.sh is the path that runs preflight.
    try:
        rf = open(RLOCK, 'a+'); fcntl.flock(rf, fcntl.LOCK_EX | fcntl.LOCK_NB); fcntl.flock(rf, fcntl.LOCK_UN); rf.close()
        subprocess.Popen([sys.executable, os.path.abspath(__file__), 'run'], stdout=open(L + '/ship_queue_runner.log', 'a'), stderr=subprocess.STDOUT,
                         stdin=subprocess.DEVNULL, start_new_session=True)
        sys.stderr.write('ship_queue: no runner was alive; started one. (ship_request.sh is the path that runs preflight first.)\n')
    except BlockingIOError: pass
    except Exception as e: sys.stderr.write('ship_queue: could not check or start the runner (%r)\n' % e)
    print(rid); return 0


def take():
    """mark every pending request running; returns them"""
    with qlock():
        rows = load(); got = []
        for r in rows:
            if r.get('status') == 'pending': r['status'] = 'running'; r['started'] = ts(); got.append(r)
        if got: save(rows)
    return got


def finish(ids, rc, label):
    with qlock():
        rows = load()
        for r in rows:
            if r.get('id') in ids: r.update(status='done', rc=rc, finished=ts(), ship_label=label)
        save(rows)


def pending():
    with qlock(): return any(r.get('status') == 'pending' for r in load())


RESULT = L + '/.ship_queue_result.txt'   # 22 Nov 2026 (P2 / A12): ship.sh writes FAIL/NOTE lines here (step, reason); this runner rings once from them


def ship(label):
    env = dict(os.environ, PATH='/opt/homebrew/bin:/usr/local/bin:' + os.environ.get('PATH', '')); env.pop('SITE_LOCK_HELD', None)
    env.update(SHIP_RUNNER='1', SHIP_RESULT=RESULT)   # ship.sh writes no RING lines of its own when SHIP_RUNNER is set
    try: os.remove(RESULT)
    except OSError: pass
    cmd = ['python3', L + '/site_lock.py', 'run', '--label', 'ship_queue: ' + label[:200], '--', 'bash', L + '/ship.sh', label]
    with open(LAST, 'w') as out:
        p = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT, env=env, cwd=B, start_new_session=True)
        try: return p.wait(timeout=SHIP_TIMEOUT)
        except subprocess.TimeoutExpired:
            try: os.killpg(p.pid, signal.SIGTERM)
            except OSError: pass
            try: p.wait(timeout=60)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, signal.SIGKILL)
            return 124


def auto_status(reqs, rc):
    # 21 Nov 2026: any clean ship clears the refused-ship alert (a clean ship proves every gate passes); only auto: requests write it on failure.
    # Cause: the alert stayed open for hours after later manual ships passed, because only an auto: ship could clear it.
    if rc == 0:
        if os.path.exists(AUTO_STATUS): os.remove(AUTO_STATUS)
    elif any(r['label'].startswith('auto:') for r in reqs):
        tail = open(LAST, errors='replace').read()[-1500:] if os.path.exists(LAST) else ''
        json.dump({'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'ok': False, 'rc': rc, 'tail': tail}, open(AUTO_STATUS, 'w'))


# 22 Nov 2026 (the owner; 14 ships on 21 Nov, 6 in one hour): ONE bundled ship per CLOCK seconds.
# A request whose label starts with MONEY: or URGENT: ships at once (money path first). Everything else waits for the next slot and rides
# in that bundle. The runner holds its lock while it waits, so later requests join the same bundle instead of starting a ship of their own.
CLOCK = int(os.environ.get('SHIP_CLOCK_S', '3600')); LASTAT = os.path.join(L, '.last_ship_at')
def _urgent():
    with qlock(): return any(r.get('status') == 'pending' and r.get('label', '').startswith(('MONEY:', 'URGENT:')) for r in load())
def hold_for_clock():
    try: last = float(open(LASTAT).read().strip())
    except Exception: return
    waited = False
    while time.time() - last < CLOCK and not _urgent():
        if not waited: print('%s ship_queue: next ship slot in %d min (MONEY:/URGENT: labels ship at once)' % (ts(), (CLOCK - (time.time() - last)) // 60), flush=True); waited = True
        time.sleep(30)


def ring_line(rc, n, label):
    """22 Nov 2026 (PIPELINE_AUDIT P2 / A12: one failed ship rang three times, from the gate, ship.sh's EXIT trap and here). This runner is now
    the one place that rings for a queued ship: ONE line, with the step that failed and its reason as ship.sh wrote them to RESULT, plus any
    non-fatal notes. A clean ship with no notes is logged without RING."""
    fails, notes = [], []
    try:
        for l in open(RESULT, errors='replace'):
            p = l.rstrip('\n').split('\t', 2)
            if len(p) == 3: (fails if p[0] == 'FAIL' else notes if p[0] == 'NOTE' else []).append('%s: %s' % (p[1], p[2]))
    except OSError: pass
    req = '%d request%s: %s' % (n, '' if n == 1 else 's', label[:160])
    nt = (' | notes: ' + ' | '.join(notes))[:400] if notes else ''
    if rc:
        why = fails[0] if fails else ('timed out after %d s, killed' % SHIP_TIMEOUT if rc == 124 else 'stopped with no reason written (see ledger/ship_queue_last.log)')
        return 'RING: SHIP FAILED at %s (exit %d, %s)%s' % (why[:320], rc, req, nt)
    if notes: return 'RING: SHIP OK with %d note%s (%s)%s' % (len(notes), '' if len(notes) == 1 else 's', req, nt)
    return 'SHIP QUEUE: ship exit 0 for %s' % req


def run():
    try: os.setsid()   # outlive the caller's session (a tick rider's process group)
    except OSError: pass
    while True:
        rf = open(RLOCK, 'a+')
        try: fcntl.flock(rf, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError: print('ship_queue: a runner is already running'); return 0
        try:
            with qlock():   # a runner that died mid-ship left requests 'running'; only the lock holder sets that, so they go back in line
                rows = load(); stale = [r for r in rows if r.get('status') == 'running']
                for r in stale: r['status'] = 'pending'
                if stale: save(rows)
            while True:
                hold_for_clock()
                reqs = take()
                if not reqs: break
                labels = []
                for r in reqs:
                    if r['label'] not in labels: labels.append(r['label'])
                label = ' + '.join(labels)
                print('%s ship_queue: shipping %d request(s): %s' % (ts(), len(reqs), label), flush=True)
                rc = ship(label)
                finish({r['id'] for r in reqs}, rc, label); auto_status(reqs, rc)
                open(LASTAT, 'w').write(str(time.time()))
                log(ring_line(rc, len(reqs), label))
        finally:
            fcntl.flock(rf, fcntl.LOCK_UN); rf.close()
        if not pending(): return 0   # a request added while this runner was exiting would find the runner lock held; re-check after release


def wait(rid, timeout):
    t0 = time.time()
    while time.time() - t0 < timeout:
        with qlock(): r = next((x for x in load() if x.get('id') == rid), None)
        if r is None: print('ship_queue: no request %s' % rid); return 2
        if r.get('status') == 'done': print('ship_queue: request %s done, ship exit %s' % (rid, r.get('rc'))); return int(r.get('rc') or 0)
        time.sleep(15)
    print('ship_queue: request %s still not done after %d s' % (rid, timeout)); return 124


def status():
    with qlock(): rows = load()
    for r in rows[-15:]: print('%-8s %s %s%s' % (r.get('status'), r.get('id'), r.get('label', '')[:120], '' if r.get('status') != 'done' else '  (exit %s, %s)' % (r.get('rc'), r.get('finished'))))
    return 0


def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return 2
    if a[0] == 'add' and len(a) > 1: return add(a[1])
    if a[0] == 'run': return run()
    if a[0] == 'wait' and len(a) > 1: return wait(a[1], int(a[a.index('--timeout') + 1]) if '--timeout' in a else 4 * 3600)
    if a[0] == 'status': return status()
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main())
