#!/usr/bin/env python3
"""poll.py (21 Nov 2026, the owner: "designer's map was done two hours ago, can we not have that be overlooked again?").
Runs forever (nohup). Every 45 s, every lane PR on indahl-ai/calibrations: any comment that starts (after markdown) with "Ball to the operator"
is appended to inbox.jsonl. The operator marks rings read with `python3 read.py` (prints unread, marks them). The per-prompt hook prints the unread
count and first lines on every message from the owner, so no ring waits on a monitor that expired."""
import json, os, re, subprocess, time
H = os.path.dirname(os.path.abspath(__file__)); INBOX = os.path.join(H, 'inbox.jsonl'); LAST = os.path.join(H, 'last.txt')
os.environ['PATH'] = '/opt/homebrew/bin:/usr/local/bin:' + os.environ.get('PATH', '')
# 21 Nov 2026 (cause fix for double rings): one poller only. A second start exits if the pid in poll.pid is alive.
PID = os.path.join(H, 'poll.pid')
try:
    _old = int(open(PID).read()); os.kill(_old, 0)
    if _old != os.getpid(): raise SystemExit('poll.py: already running as pid %d' % _old)
except (FileNotFoundError, ValueError, ProcessLookupError, PermissionError): pass
open(PID, 'w').write(str(os.getpid()))
seen = {json.loads(l)['id'] for l in open(INBOX)} if os.path.exists(INBOX) else set()
last = open(LAST).read().strip() if os.path.exists(LAST) else time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - 4 * 3600))
while True:
    now = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()); ok = True
    for n in (1, 2, 3, 4, 5, 6, 7, 8, 17):   # 22 Nov 2026: PR #17 is the flywheel doorbell; it was never polled, so the designer's balls skipped the inbox
        try:
            r = subprocess.run(['gh', 'api', 'repos/indahl-ai/calibrations/issues/%d/comments?since=%s&per_page=100' % (n, last)], capture_output=True, text=True, timeout=60)
            for c in json.loads(r.stdout or '[]'):
                if c['id'] in seen or (not re.search(r'ball to operator', (c.get('body') or '').split('\n')[0], re.I) or re.match(r'^[^A-Za-z]*(ball to designer|pointer)', c.get('body') or '', re.I)): continue
                seen.add(c['id']); open(INBOX, 'a').write(json.dumps({'id': c['id'], 'pr': n, 'at': c['created_at'], 'first': ' / '.join((c['body'] or '').split('\n')[:3])[:300], 'url': c['html_url'], 'read': False}) + '\n')
        except Exception as _e:
            ok = False   # 22 Nov 2026: was silent; three failed polls in a row ring once (GitHub login or network down = no the designer rings)
            try:
                _f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gh_fail'); _n = int(open(_f).read() or 0) + 1 if os.path.exists(_f) else 1; open(_f, 'w').write(str(_n))
                if _n == 3: open(os.path.expanduser('~/forge/sagar/pipeline/pipe.log'), 'a').write(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + ' RING: DOORBELL GITHUB POLL FAILING x3: %s\n' % type(_e).__name__)
            except Exception: pass
    # 21 Nov 2026 (the owner: "fix the problem that made that problem"): a SAGAR send refused at 15:13Z sat five hours because nothing told
    # anyone. Any refusal or failure line in the pipeline log now lands in the same inbox the per-prompt hook prints, so it reaches the operator
    # on the owner's next message even when no monitor is running.
    # 21 Nov 2026 (HARD rows): MONEY PATH FAILED (ledger/money_path_check.py), DESK BUILD FAILED (build_site.py per-desk units) and
    # DESK LIST GATE FAILED (ledger/desk_list_gate.py) and MCP GATE FAILED (ledger/mcp_gate.py) are named here; FAILED already matched them, the names keep them from being lost if it narrows.
    try:
        PL = os.path.expanduser('~/forge/sagar/pipeline/pipe.log'); OFF = os.path.join(H, 'pipe_offset.txt')
        off = int(open(OFF).read()) if os.path.exists(OFF) else os.path.getsize(PL)
        if os.path.getsize(PL) < off: off = 0   # 21 Nov 2026 (control audit #22): a truncated or rotated pipe.log read nothing forever
        with open(PL, errors='replace') as f:
            f.seek(off); new = f.read(); off = f.tell()
        for line in new.splitlines():
            # 21 Nov 2026 (blip fix): rider_wrap's first network blip and its recovery note are on record in pipe.log but do not ring,
            # whatever their quoted error text holds; a second failure in a row arrives as 'RING: RIDER FAILED' and rings below.
            if re.search(r'^\S+ RIDER (BLIP|RECOVERED) ', line): continue
            if re.search(r'SEND no queue|SEND failed|STOPPED|REFUSED|FAILED|failed:|Traceback|SHIP REFUSED|REPRODUCE KIT NOT REMADE:|REPRODUCE KIT BREACH:|SAGAR LANE MISSING:|RING:|MONEY PATH FAILED:|DESK BUILD FAILED:|DESK LIST GATE FAILED:|MCP GATE FAILED:|NEW INQUIRY:|NEW CORRECTION REQUEST:|INQUIRY MAIL FAILED:|INQUIRY BELL FAILED:', line) and 'refused for no pair' not in line:   # 21 Nov 2026: SAGAR LANE MISSING: (lane fail-closed) and RING: (control audit fixes) added; NEW INQUIRY etc. (ledger/inquiry_bell.py) added
                k = 'pipe:' + line[:19] + ':' + str(abs(hash(line)) % 10**8)
                if k not in seen: seen.add(k); open(INBOX, 'a').write(json.dumps({'id': k, 'pr': 0, 'at': line[:19].replace(' ', 'T') + 'Z', 'first': 'PIPELINE: ' + line[20:300], 'url': PL, 'read': False}) + '\n')
        open(OFF, 'w').write(str(off))
    except Exception as _e:   # 21 Nov 2026 (control audit #22): was a bare pass; a broken pipe.log read is now on record
        try: open(os.path.join(H, 'poll_errors.log'), 'a').write(time.strftime('%Y-%m-%dT%H:%M:%S ') + 'pipe.log scan failed: %r\n' % (_e,))
        except Exception: pass
    if ok:
        open(LAST, 'w').write(now); last = now
        try: os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gh_fail'))
        except OSError: pass
    time.sleep(45)
