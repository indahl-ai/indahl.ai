#!/usr/bin/env python3
"""tape_push.py: commits and pushes only code/tape in the public mirror, so the leaf links on the TAPE page open soon after each run instead of at the next release.
Called in the background by tape_tick.py. Nothing else in the mirror is touched. Any failure is printed and left for the next run or the release script, which pulls and pushes the whole mirror."""
import os, sys, fcntl, subprocess
M = os.environ.get('TAPE_MIRROR') or os.path.expanduser('~/bones-forge/public_mirror/indahl.ai')
def git(*a): return subprocess.run(['git', '-C', M] + list(a), capture_output=True, text=True, timeout=180)
try:
    if os.path.exists(os.path.expanduser('~/bones-forge/ledger/PUBLIC_PUSH_HOLD')): print('tape push: HOLD (ledger/PUBLIC_PUSH_HOLD), skipped'); sys.exit(0)   # 20 Nov 2026: held during a history rewrite of the public repo
    if not os.path.isdir(M + '/.git'): print('tape push: no mirror clone'); sys.exit(0)
    lock = open(os.path.join(M, '.git', 'tape_push.lock'), 'w')
    try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError: print('tape push: another push is running'); sys.exit(0)
    uid = subprocess.run(['/opt/homebrew/bin/gh', 'api', 'user', '--jq', '.id'], capture_output=True, text=True, timeout=30).stdout.strip()
    if not uid: print('tape push: gh login missing, skipped'); sys.exit(0)
    # the remote must not be ahead of the mirror: a local commit on top of newer remote commits would make the release script's pull diverge
    if git('fetch', '-q', 'origin').returncode: print('tape push: fetch failed, skipped'); sys.exit(0)
    if git('rev-list', '--count', 'HEAD..origin/main').stdout.strip() not in ('0', ''): print('tape push: the remote has newer commits, left to the release script'); sys.exit(0)
    # 20 Nov 2026: the same internal-text gate the release runs, on code/tape, before anything is staged. A hit refuses the push (fail closed)
    # and writes an alert; nothing under code/tape reaches the public repository around the gate again.
    import re as _re
    _src = open(os.path.expanduser('~/bones-forge/ledger/internal_gate.py')).read(); _m = _re.search(r"BAD_TEXT = re\.compile\((.*?)\)\s*(?:#|\n)", _src, _re.S); _ns = {}
    exec('import re\nBAD_TEXT = re.compile(' + _m.group(1) + ')', _ns)
    _hits = [f for f in os.listdir(M + '/code/tape') if os.path.isfile(M + '/code/tape/' + f) and not f.endswith('.jsonl') and _ns['BAD_TEXT'].search(open(M + '/code/tape/' + f, errors='ignore').read())]
    if _hits:
        print('tape push: REFUSED, internal text in code/tape:', ', '.join(_hits))
        open(os.path.expanduser('~/bones-forge/alerts/ALERTS_OPEN.txt'), 'a').write('- [tape:push] internal text in public_mirror code/tape (%s); push refused (tape_index/tape_push.py)\n' % ', '.join(_hits))
        sys.exit(0)
    git('add', 'code/tape')
    if git('diff', '--cached', '--quiet', '--', 'code/tape').returncode == 0: print('tape push: current'); sys.exit(0)
    n = sum(1 for l in open(M + '/code/tape/tape.jsonl') if l.strip())
    c = git('-c', 'user.name=Heuremen LLC', '-c', 'user.email=%s+indahl-ai@users.noreply.github.com' % uid, 'commit', '-q', '-m',
            'TAPE: chain and leaves through entry %d\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>' % n, '--', 'code/tape')
    if c.returncode: print('tape push: commit failed', (c.stderr or c.stdout)[-200:]); sys.exit(0)
    p = git('push', '-q', 'origin', 'HEAD')
    if p.returncode and git('log', '-1', '--format=%s').stdout.startswith('TAPE: chain'): git('reset', '-q', '--soft', 'HEAD~1')   # undo our commit, the files stay staged for the release script
    print('tape push: entry', n, 'pushed' if p.returncode == 0 else 'not pushed, left for the release script: ' + (p.stderr or p.stdout)[-200:])
except Exception as e: print('tape push: failed', type(e).__name__)
