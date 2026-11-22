#!/usr/bin/env python3
"""seat_tick.py: SEAT rider. Asks the GitHub runner for a new probe (repository_dispatch) and publishes the runner's saved probes as the SEAT page, per PLAN.md.
The Mac only relays what the runner wrote to indahl-ai/nodes; it adds no reading of its own."""
import os, sys, json, time, subprocess, urllib.request, datetime as D
import os as _pg_os, sys as _pg_sys, subprocess as _pg_sp   # 10 Nov 2026 (publish guard): the site KV is written only by a run the tick bus or the house clock started
_PUBLISH = '--publish' in _pg_sys.argv or _pg_os.environ.get('HEUREMEN_PUBLISH') == '1'   # (they export HEUREMEN_PUBLISH=1) or a run given --publish. A copy run for a reproduce kit or a test never publishes
if _PUBLISH: _pg_os.environ['HEUREMEN_PUBLISH'] = '1'   # passed on to the scripts this one starts, and kept across a detach or re-exec
try:   # 22 Nov 2026: one shared upload part (lib/cf.py: kv token, rings on failure); this file's own guard stays as the fallback for kits
    _pg_sys.path.insert(0, _pg_os.path.expanduser('~/forge/lib')); from cf import guarded_put as _kv_put
except Exception:
    def _kv_put(cmd, **kw):
        if _PUBLISH: return _pg_sp.run(cmd, **kw)
        print('publish guard: %s not put to the site KV (run with --publish, or from the tick bus)' % cmd[5], file=_pg_sys.stderr)
        return _pg_sp.CompletedProcess(cmd, 0, '' if kw.get('text') or kw.get('universal_newlines') else b'', '' if kw.get('text') or kw.get('universal_newlines') else b'')
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import heuremen_kit as K
if not K.plan_committed(os.path.join(H, 'PLAN.md')): print('seat: plan not committed'); sys.exit(0)
W = os.path.expanduser('~/forge/cloudflare-workers/heuremen-door'); FIRST = '2026-10-29T11:57:00Z'
# keep the seat's target list in step with the site: every page in the menu is a page target, every corner with a live feed is a feed target (limit 40 hours unless set)
import re
NODES = os.path.expanduser('~/forge/nodes_repo'); TJ = NODES + '/drift/targets.json'
# 21 Nov 2026 (seat alerts after the headline ship): the pull ran AFTER targets.json was rewritten, so it refused on the dirty file, the commit
# stayed local and every push after was rejected (local main was 2616 behind, one ahead). Pull first, then edit, and say when a push fails.
g = lambda *a: subprocess.run(['git', '-C', NODES, '-c', 'user.name=Heuremen LLC', '-c', 'user.email=349448817+indahl-ai@users.noreply.github.com'] + list(a), capture_output=True, text=True)
# 21 Nov 2026: retired desks come from ledger/desks.json "retired" (STACK retired 21 Nov 2026 at the owner's word, COIN 30 Oct); they are never targets.
try: RETIRED = set(json.load(open(os.path.expanduser('~/forge/ledger/desks.json'))).get('retired', []))
except Exception: RETIRED = {'stack', 'coin'}
# 21 Nov 2026: a desk that ledger/desks.json lists with no feed gets no feed target (CHRONOS was about to be added with a /chronos/live.json that 404s).
try: FEEDLESS = {d['path'].strip('/') for d in json.load(open(os.path.expanduser('~/forge/ledger/desks.json')))['desks'] if not d.get('feed')}
except Exception: FEEDLESS = set()
# 19 Nov 2026 (nodes 3d5eba11f): pages that carry studies are on the site, not in the public repo, so the seat cannot compare them; this rider re-added them every tick.
NOT_MIRRORED = {'qia', 'yo', 'sagar', 'linkrot', 'arxivdrift'}
try:
    _pl = g('pull', '-q', '--rebase')
    if _pl.returncode: print('seat: nodes pull FAILED', _pl.stderr.strip()[-200:]); (open(os.path.expanduser('~/forge/sagar/pipeline/pipe.log'),'a').write(time.strftime('%Y-%m-%dT%H:%M:%S')+' RING: SEAT nodes pull FAILED (dirty or diverged nodes_repo; uncommitted target edits never reach the seat): '+_pl.stderr.strip()[-200:].replace(chr(10),' ')+chr(10)))   # 22 Nov 2026: a silent pull failure hid his 12 h water limit all night; now it rings
    src = open(os.path.expanduser('~/forge/indahl-ai/build_site.py')).read(); slugs = sorted(set(re.findall(r"\('/([a-z0-9]+)', '[A-Z0-9]+'[,)]", src)) - RETIRED - NOT_MIRRORED)   # 29 Oct: read the whole file (menu, desks), not one line
    T = json.load(open(TJ)); hf = {f[0] for f in T['feeds']}; ch = False
    _n = len(T['pages']) + len(T['feeds']); T['pages'] = [p for p in T['pages'] if p.split('/')[0] not in RETIRED]; T['feeds'] = [f for f in T['feeds'] if f[0].split('/')[0] not in RETIRED]
    if len(T['pages']) + len(T['feeds']) != _n: ch = True
    have = set(T['pages'])
    for sl in slugs:
        if sl not in have: T['pages'].append(sl); ch = True
        if sl in ('qia', 'iris', 'oy', 'atlas', 'sad', 'hermes', 'vault', 'yo', 'forecasters', 'brand', 'newsletter', 'corrections', 'alerts', 'week', 'receipts', 'sagar', 'standard') or sl in FEEDLESS: continue   # 10 Nov: summary/index pages with no live.json of their own   # 10 Nov: YO reads qia/yo.json + iris/yo.json, it has no yo/live.json   # 30 Oct: VAULT is a tool with no live feed   # 12 Nov: SAGAR pages are static builds, no sagar/live.json
        if sl + '/live.json' not in hf: T['feeds'].append([sl + '/live.json', 40]); ch = True
    if ch:
        json.dump(T, open(TJ, 'w'), indent=1)
        g('add', 'drift/targets.json'); g('commit', '-q', '-m', 'DRIFT seat: targets follow the site')
        _ps = g('push', '-q')
        if _ps.returncode:
            _ps = g('pull', '-q', '--rebase'); _ps = g('push', '-q') if _ps.returncode == 0 else _ps
        if _ps.returncode: print('seat: targets push FAILED', _ps.stderr.strip()[-200:]); (open(os.path.expanduser('~/forge/sagar/pipeline/pipe.log'),'a').write(time.strftime('%Y-%m-%dT%H:%M:%S')+' RING: SEAT targets push FAILED (dirty or diverged nodes_repo; uncommitted target edits never reach the seat): '+_ps.stderr.strip()[-200:].replace(chr(10),' ')+chr(10)))
except Exception as e: print('seat: targets not updated', type(e).__name__)
subprocess.run(['/opt/homebrew/bin/gh', 'api', 'repos/indahl-ai/nodes/dispatches', '-f', 'event_type=drift-probe'], capture_output=True, text=True)
# 21 Nov 2026: raw's main/ path is cached up to 5 minutes whatever the query string, so the probes are read at the commit main points to now
try: _rev = subprocess.run(['git', 'ls-remote', 'https://github.com/indahl-ai/nodes', 'refs/heads/main'], capture_output=True, text=True, timeout=60).stdout.split()[0]
except Exception: _rev = 'main'
raw = urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/indahl-ai/nodes/%s/data/drift/history.jsonl' % _rev, headers={'User-Agent': 'heuremen-seat/0.1'}), timeout=60).read().decode()
rows = [json.loads(l) for l in raw.splitlines() if l.strip()]; rows = [r for r in rows if r['t'] >= FIRST]
if not rows: print('seat: no runner probes yet'); sys.exit(0)
good = [r for r in rows if r['control'] == 'PASSED']; last = good[-1] if good else rows[-1]
def bad(r):
    if r['control'] != 'PASSED': return None
    pg = r['pages']; return dict(drift=[p for p in pg if pg[p] != 'MATCH'], feeds=[f for f, v in r['feeds'].items() if v['state'] != 'FRESH'], chain=r['chain']['state'] != 'OK')
# a page is DRIFT only when it differs in two consecutive probes
def drift_pages(i):
    a = good[i]['pages']; b = good[i - 1]['pages'] if i else {}
    return [p for p in a if a[p] != 'MATCH' and b.get(p, 'MATCH') != 'MATCH']
win = good[-24:]; flags = []; why = []
for k, r in enumerate(win):
    idx = len(good) - len(win) + k
    w = ['page /%s differs from the repository' % p for p in drift_pages(idx)] + ['feed /%s %s' % (f, v['state'].lower()) for f, v in r['feeds'].items() if v['state'] != 'FRESH'] + (['archive chain %s' % r['chain']['state'].lower()] if r['chain']['state'] != 'OK' else [])
    flags.append(bool(w)); why.append(w)
# 29 Oct (internal audit, Addendum 1): a standing fault is one incident however many probes see it, so the count is runs of consecutive flagged probes
nflag = sum(1 for k, f in enumerate(flags) if f and (k == 0 or not flags[k - 1]))
# 30 Oct (site pass I-7): each incident is listed with its first and last probe, how many probes saw it and what they saw
incidents = []; k = 0
while k < len(flags):
    if flags[k]:
        j = k
        while j + 1 < len(flags) and flags[j + 1]: j += 1
        fmt = lambda t: t.replace('T', ' ').replace('Z', ' UTC')[:-7] + ' UTC'
        incidents.append(dict(first=fmt(win[k]['t']), last=fmt(win[j]['t']), probes=j - k + 1, saw=', '.join(sorted({x for w in why[k:j + 1] for x in w}))))
        k = j + 1
    else: k += 1
import datetime as _D
age_h = (_D.datetime.now(_D.timezone.utc) - _D.datetime.strptime(last['t'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=_D.timezone.utc)).total_seconds() / 3600
# 12 Nov 2026 (PLAN_ADDENDUM_std2.md): one-sided. The incident count is exact (zero-width interval, O1), the bound is 3 and at least 3 reads ABOVE (edge closed at the bound for ABOVE), fewer reads BELOW, no CONSISTENT.
if age_h > 3: oc, why = K.CANNOT_TELL, K.NO_INTERVAL_FORMABLE   # the window cannot be read as current
elif len(win) < 24: oc, why = K.CANNOT_TELL, K.TOO_WIDE_TO_RESOLVE   # below the desk's minimum sample (O3)
else: oc, why = K.read(nflag, nflag, bound=3, edge='[)')
pg = last['pages']; fd = last['feeds']
out = dict(updated=time.strftime('%d %b %H:%M', time.gmtime()), probes=len(good), failed_controls=len(rows) - len(good), last_probe=last['t'].replace('T', ' ').replace('Z', ' UTC'),
           rolling={'Last 24 probes, counted as incidents': dict(of=len(win), n=nflag, outcome=oc, reason=why, newest_probe_hours=round(age_h, 1))},
           now={'Pages matching the public repository': dict(n=sum(1 for v in pg.values() if v == 'MATCH'), of=len(pg)), 'Feeds younger than their limit': dict(n=sum(1 for v in fd.values() if v['state'] == 'FRESH'), of=len(fd)),
                'Archive chain': dict(n=last['chain']['entries'], of=last['chain']['entries'], state=last['chain']['state'])},
           incidents=incidents, flagged_probes=sum(flags), req13=K.req13([(oc, why)], nothing_returned=len(rows) - len(good)), plan_addendum='PLAN_ADDENDUM_std2.md',
           feeds=[dict(feed='/' + f, age_h=v.get('age_h'), limit_h=v.get('limit_h'), state=v['state']) for f, v in fd.items()],
           not_matching=[dict(page='/' + p, state=v) for p, v in pg.items() if v != 'MATCH'])
json.dump(out, open('summary_seat.json', 'w'), indent=1)
env = dict(os.environ, CLOUDFLARE_ACCOUNT_ID='<cloudflare-account-id>', PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
pr = _kv_put(['/opt/homebrew/bin/npx', 'wrangler', 'kv', 'key', 'put', 'seat_live', '--path', os.path.join(H, 'summary_seat.json'), '--namespace-id', '<kv-namespace-id>', '--remote'], cwd=W, env=env, capture_output=True, text=True)
print('seat:', len(good), 'probes;', 'last', last['t'], 'published' if pr.returncode == 0 else 'publish FAILED', flush=True)
