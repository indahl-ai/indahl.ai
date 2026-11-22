#!/usr/bin/env python3
"""inquiry_bell.py (21 Nov 2026, money-path check): ring the doorbell for every new inquiry in the private KV store INDAHL_INQUIRIES.

Both inquiry doors land in one store: indahl.ai/contact -> /agree -> /inquiry -> POST /inquire, and quantumidleaudit.com/inquiries hands off
to that same indahl.ai form. The worker emails each inquiry (indahl-ai/inquire.js notify); that email failed silently from 19 Nov (a
ReferenceError) and nothing read the store except a hand run of indahl-ai/inquiries.py. This reads KEY NAMES only (never a record, so no
personal data is touched) and appends to sagar/pipeline/pipe.log, which watch/doorbell/poll.py rings into the inbox:
  NEW INQUIRY: indahl.ai <date> (no personal data)
  NEW CORRECTION REQUEST: indahl.ai <date> (no personal data)
  INQUIRY MAIL FAILED: indahl.ai <date> (stored; read with indahl-ai/inquiries.py)
  INQUIRY BELL FAILED: <why>             (once per new failure kind; cleared line when it reads again)
Keys already rung are kept in ledger/.inquiry_bell_state.json; on the first run the baseline is indahl-ai/.inquiries_seen (already read).
Rides the tick bus (watch/tick_bus.py) and runs after every ship from ledger/money_path_check.py. Writes nothing to the store or the site."""
import sys as _cfsys, os as _cfos
try:   # 22 Nov 2026: one shared Cloudflare part (lib/cf.py: kv token, rings on failure)
    _cfsys.path.insert(0, _cfos.path.expanduser('~/forge/lib')); from cf import run_put as _cf_run
except Exception:
    import subprocess as _cfsp; _cf_run = _cfsp.run
import json, os, subprocess, sys, time
B = os.path.expanduser('~/forge')
NS = '<kv-namespace-id>'; W = os.path.join(B, 'cloudflare-workers', 'heuremen-door')
PIPE_LOG = os.environ.get('INQUIRY_BELL_LOG') or os.path.join(B, 'sagar', 'pipeline', 'pipe.log')   # override for dry tests only
STATE = os.environ.get('INQUIRY_BELL_STATE') or os.path.join(B, 'ledger', '.inquiry_bell_state.json')
SEEN = os.path.join(B, 'indahl-ai', '.inquiries_seen')
SITE = 'indahl.ai'   # the one inquiry door; quantumidleaudit.com/inquiries links to it
os.environ['PATH'] = '/opt/homebrew/bin:/usr/local/bin:' + os.environ.get('PATH', '')


def ring(msg):
    try:
        with open(PIPE_LOG, 'a') as f: f.write('%s %s\n' % (time.strftime('%Y-%m-%dT%H:%M:%S'), msg))
    except Exception as e: sys.stderr.write('inquiry_bell: could not write the pipeline log (%s)\n' % e)


def save(st):
    tmp = STATE + '.tmp'
    with open(tmp, 'w') as f: json.dump(st, f, indent=1)
    os.replace(tmp, STATE)


def main():
    try: st = json.load(open(STATE))
    except Exception: st = {'rung': sorted(set(open(SEEN).read().split())) if os.path.exists(SEEN) else [], 'fail': None}
    try:
        r = _cf_run(['npx', 'wrangler', 'kv', 'key', 'list', '--namespace-id', NS, '--remote'], cwd=W, capture_output=True, text=True, timeout=120)
        names = [k['name'] for k in json.loads(r.stdout)]
    except Exception as e:
        why = 'store unreadable (%s)' % type(e).__name__
        if st.get('fail') != why: ring('INQUIRY BELL FAILED: ' + why + '; new inquiries are not being rung'); st['fail'] = why; save(st)
        print('inquiry_bell: ' + why); return 1
    if st.get('fail'): ring('inquiry bell: cleared, the inquiry store reads again'); st['fail'] = None
    rung = set(st.get('rung', []))
    new = [n for n in sorted(names) if n.split(':', 1)[0] in ('inq', 'corr', 'notify-failed') and n not in rung]
    for n in new:
        if n.startswith('inq:'): ring('NEW INQUIRY: %s %s (no personal data)' % (SITE, n[4:14]))
        elif n.startswith('corr:'): ring('NEW CORRECTION REQUEST: %s %s (no personal data)' % (SITE, n.split(':')[1][:10]))
        else: ring('INQUIRY MAIL FAILED: %s %s (stored; read with indahl-ai/inquiries.py)' % (SITE, n.split(':', 2)[2][:10] if n.count(':') >= 2 else '?'))
        rung.add(n)
    st['rung'] = sorted(rung); st['at'] = time.strftime('%Y-%m-%dT%H:%M:%S'); save(st)
    c = lambda p: sum(1 for n in names if n.startswith(p))
    print('inquiry_bell: %d inquiries, %d correction requests, %d mail failures stored; %d newly rung' % (c('inq:'), c('corr:'), c('notify-failed:'), len(new)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
