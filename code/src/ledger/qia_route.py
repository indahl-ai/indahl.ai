#!/usr/bin/env python3
"""qia_route.py (22 Nov 2026, QIA split): which worker serves quantumidleaudit.com.

  python3 ~/forge/ledger/qia_route.py            shows the worker on each route
  python3 ~/forge/ledger/qia_route.py qia        cutover: both routes -> qia-site (ledger/ship_qia.sh deploys it)
  python3 ~/forge/ledger/qia_route.py door       ROLLBACK: both routes -> heuremen-door (its quantumidleaudit.com branch is
                                                       kept for exactly this; it serves cloudflare-workers/heuremen-door/public/_qiasite/)
  python3 ~/forge/ledger/qia_route.py preview on|off   the qia-site workers.dev preview URL (off except while comparing)

Routes (zone quantumidleaudit.com): quantumidleaudit.com/* and www.quantumidleaudit.com/*. Token: lib/cf.py role 'deploy' (never printed).
A failure writes one RING line to sagar/pipeline/pipe.log (cf.ring) and exits 1."""
import json, os, sys, urllib.request, urllib.error
sys.path.insert(0, os.path.expanduser('~/forge/lib')); import cf

ZONE = '2549ec846ba9735d3db23020508f65b5'
ROUTES = {'4be71a573e09412abec8de878f97b77d': 'quantumidleaudit.com/*', 'a78b13e1bd1b42a8808a79e465e3fe80': 'www.quantumidleaudit.com/*'}
SCRIPT = {'qia': 'qia-site', 'door': 'heuremen-door'}


def api(path, method='GET', body=None):
    r = urllib.request.Request('https://api.cloudflare.com/client/v4' + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                               headers={'Authorization': 'Bearer ' + cf.token('deploy'), 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(r, timeout=60) as f: return json.loads(f.read())
    except urllib.error.HTTPError as e:
        try: return json.loads(e.read())
        except Exception: return {'success': False, 'errors': [{'message': 'HTTP %d' % e.code}]}


def show():
    d = api('/zones/%s/workers/routes' % ZONE)
    if not d.get('success'): cf.ring('QIA ROUTE READ FAILED: %s' % d.get('errors')); print('route read failed: %s' % d.get('errors')); sys.exit(1)
    for r in d['result']: print('%-28s -> %s' % (r['pattern'], r.get('script')))
    return {r['id']: r.get('script') for r in d['result']}


def switch(to):
    bad = []
    for rid, pat in ROUTES.items():
        d = api('/zones/%s/workers/routes/%s' % (ZONE, rid), 'PUT', {'pattern': pat, 'script': SCRIPT[to]})
        if not d.get('success'): bad.append('%s: %s' % (pat, d.get('errors')))
    now = show()
    if bad or any(now.get(rid) != SCRIPT[to] for rid in ROUTES):
        cf.ring('QIA ROUTE SWITCH TO %s FAILED: %s' % (SCRIPT[to], '; '.join(bad) or 'routes read back wrong'))
        print('switch FAILED: %s' % ('; '.join(bad) or 'routes read back wrong')); sys.exit(1)
    print('quantumidleaudit.com now served by %s' % SCRIPT[to])


def preview(on):
    d = api('/accounts/%s/workers/scripts/qia-site/subdomain' % cf.ACCOUNT, 'POST', {'enabled': on, 'previews_enabled': False})
    if not d.get('success'): print('preview toggle failed: %s' % d.get('errors')); sys.exit(1)
    print('qia-site workers.dev preview %s' % ('ON: https://qia-site.heuremen.workers.dev' if on else 'off'))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: show()
    elif a[0] in SCRIPT: switch(a[0])
    elif a[0] == 'preview' and len(a) > 1 and a[1] in ('on', 'off'): preview(a[1] == 'on')
    else: print(__doc__); sys.exit(2)
