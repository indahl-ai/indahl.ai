#!/usr/bin/env python3
"""tape_tick.py: TAPE rider per PLAN.md. Appends feeds, pages and beacon entries to the chain, publishes the live feed, copies the chain to the public repository."""
import os, sys, re, json, time, glob, hashlib, subprocess, urllib.request, fcntl
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
from tapelib import merkle, beacon, entry_hash, sha
if not K.plan_committed(os.path.join(H, 'PLAN.md')): print('tape: plan not committed'); sys.exit(3)   # 22 Nov 2026: a refusal exits non-zero so the rider rings (it used to exit 0 and sat unseen for days)
_l = open('.lock', 'w')
try: fcntl.flock(_l, fcntl.LOCK_EX | fcntl.LOCK_NB)
except OSError: sys.exit(0)
R = os.path.expanduser('~/forge'); W = R + '/cloudflare-workers/heuremen-door'; PUB = R + '/public_mirror/indahl.ai/code/tape'
DRAND = 'https://api.drand.sh/52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971/public/latest'
SLUGS = 'support pkglicense hflicense hfsize secrecords pkginstall linkrot trials revise hpt hosts airq ailuminate weights airline fedsep time cada uptime forecast cadence launch arxivdrift campus seat change stack water neo'.split()
def get(url, t=40):
    try: return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'heuremen-tape/0.1'}), timeout=t).read()
    except Exception: return None
os.makedirs('leaves', exist_ok=True)
chain = [json.loads(l) for l in open('tape.jsonl') if l.strip()] if os.path.exists('tape.jsonl') else []
def append(kind, subject, root, leaves, extra=None):
    prev = chain[-1]['entry'] if chain else '0' * 64
    e = dict(n=len(chain) + 1, t=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), kind=kind, subject=subject, root=root, prev=prev); e['entry'] = entry_hash(e)
    json.dump(dict(kind=kind, leaves=[list(x) for x in leaves], extra=extra or {}), open('leaves/%d.json' % e['n'], 'w'))
    with open('tape.jsonl', 'a') as f: f.write(json.dumps(e) + '\n')
    chain.append(e); return e
# 1 pages: built public pages of the sitemap, asset version strings removed
sm = get('https://indahl.ai/sitemap.xml?x=%d' % time.time())
pages = []
if sm:
    for u in re.findall(r'<loc>(.*?)</loc>', sm.decode()):
        p = u[len('https://indahl.ai'):].strip('/'); f = None
        for c in (('index.html',) if not p else (p + '.html', p + '/index.html')):
            if os.path.exists(os.path.join(R, 'indahl-ai', c)): f = os.path.join(R, 'indahl-ai', c); break
        if f: pages.append((u, sha(re.sub(rb'\?v=[0-9a-f]{8}', b'', open(f, 'rb').read()))))
last_pages = json.load(open('pages_last.json')) if os.path.exists('pages_last.json') else {}
changed = [u for u, h in pages if last_pages.get(u) != h]
if pages and changed:
    e = append('pages', 'built pages, %d changed' % len(changed), merkle(pages), pages, dict(changed=changed[:400]))
    json.dump(dict(pages), open('pages_last.json', 'w'))
# 1b receipts: hashes people sent from their own browsers (VAULT), chained in batches
ENVC = dict(os.environ, CLOUDFLARE_ACCOUNT_ID='<cloudflare-account-id>', PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
def d1(sql):
    try:   # 22 Nov 2026 (P3): lib/cf.py runs the call (kv token from $HOME, timeout, rings on failure), not the heuremen-door .env
        import cf as _cf; rc, out = _cf.wrangler('d1', 'execute', 'tape-commits', '--remote', '--json', '--command', sql, timeout=300, stdout_only=True)
        if rc: _cf.ring('D1 CALL FAILED tape-commits (from tape_tick.py): %s' % _cf._why(out))
    except ImportError:
        out = subprocess.run(['/opt/homebrew/bin/npx', 'wrangler', 'd1', 'execute', 'tape-commits', '--remote', '--json', '--command', sql], cwd=W, env=ENVC, capture_output=True, text=True).stdout
    try: return json.loads(out)[0].get('results', [])
    except Exception: return None
pend = d1('SELECT h, t FROM commits WHERE n IS NULL ORDER BY t, h LIMIT 2000')
if pend:
    pend = [x for x in pend if re.fullmatch(r'[0-9a-f]{64}', str(x['h']))]
    if pend:
        lv = [(x['h'], str(x['t'])) for x in pend]
        ec = append('commits', 'receipts, %d received' % len(lv), merkle(lv), lv)
        d1("UPDATE commits SET n=%d WHERE n IS NULL AND h IN (%s)" % (ec['n'], ','.join("'%s'" % h for h, _ in lv)))
# 2b quantum bits: a finished QBITS run waiting in qbits/new becomes a qbits entry (PLAN Addendum 2)
os.makedirs('qbits/new', exist_ok=True); os.makedirs('qbits/done', exist_ok=True)
for qf in sorted(glob.glob('qbits/new/*.json')):
    try:
        q = json.load(open(qf)); rd = q['reading']
        lv = [('backend', q['backend']), ('job_id', q['job_id']), ('shots', str(q['shots'])), ('qubits', str(q['qubits'])), ('raw_sha256', q['raw_sha256']), ('extracted', q['extracted']), ('outcome', rd['outcome']), ('usable', str(rd['usable']))]
        append('qbits', 'quantum bits from %s, %s' % (q['backend'], 'usable under the plan flags' if rd['usable'] else 'not usable under the plan flags'), q['extracted'], lv, dict(run=os.path.basename(qf), mean_qubit_p1=rd['mean_qubit_p1'], mean_ci=rd['mean_ci'], flags=rd['flags']))
        os.rename(qf, 'qbits/done/' + os.path.basename(qf))
    except Exception as ex: print('tape: qbits file skipped,', os.path.basename(qf), type(ex).__name__)
# 2a ops (PLAN Addendum 4, 21 Nov 2026): the hash of the internal operations record as read now, written before feeds so this run's beacon covers it.
# Hash only: the record's bytes go to a private history folder beside it (never copied to any public tree), one file per run, gzipped after a day.
OPS_SRC = R + '/WATCHDOG.txt'; OPS_HIST = R + '/watch/watchdog_history'
try:
    ob = open(OPS_SRC, 'rb').read(); ot = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
except Exception: ob = None; ot = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
oh = sha(ob) if ob is not None else 'NOTHING_RETURNED'
if ob is not None:
    try:
        import gzip, shutil
        os.makedirs(OPS_HIST, exist_ok=True)
        hp = '%s/WATCHDOG-%s.txt' % (OPS_HIST, ot.replace('-', '').replace(':', ''))
        with open(hp + '.tmp', 'wb') as f: f.write(ob)
        os.replace(hp + '.tmp', hp)
        for old in glob.glob(OPS_HIST + '/WATCHDOG-*.txt'):
            if time.time() - os.path.getmtime(old) > 86400:
                with open(old, 'rb') as fi, gzip.open(old + '.gz', 'wb') as fo: shutil.copyfileobj(fi, fo)
                os.remove(old)
    except Exception as ex: print('tape: ops private copy failed (%s)' % type(ex).__name__)
append('ops', 'internal operations record, hash only', merkle([('record_sha256', oh), ('read_utc', ot)]), [('record_sha256', oh), ('read_utc', ot)])
# 2 feeds
fl = []; bodies = {}
for s in SLUGS + ['headlines']:
    b = get('https://indahl.ai/%s' % (s + '/live.json?x=%d' % time.time() if s != 'headlines' else 'headlines.json?x=%d' % time.time()))
    fl.append((s, sha(b) if b else 'NOTHING_RETURNED')); bodies[s] = b
ef = append('feeds', 'live feeds, %d of %d read' % (sum(1 for _, h in fl if h != 'NOTHING_RETURNED'), len(fl)), merkle(fl), fl)
# 3 beacon
dr = get(DRAND, 20); drd = json.loads(dr) if dr else None
rnd = str(drd['round']) if drd else 'NOTHING_RETURNED'; rr = drd['randomness'] if drd else 'NOTHING_RETURNED'
qlast = [e for e in chain if e['kind'] == 'qbits']; qroot = qlast[-1]['root'] if qlast else None
bv = beacon(rr, ef['root'], ef['entry'], qroot)
append('beacon', 'drand round %s' % rnd, bv, [('drand_randomness', rr), ('feeds_root', ef['root']), ('prev_entry', ef['entry']), ('qbits_root', qroot or 'NONE')], dict(drand_round=rnd, drand_chain='52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971'))
# anchoring: which entries a stamped ARCHIVE manifest covers
anch = dict(archive_id=None, covers_n=0, attested=False)
try:
    ac = [json.loads(l) for l in open(R + '/archive/chain.jsonl') if l.strip()]
    for a in reversed(ac):
        mp = R + '/archive/manifests/%s.json' % a['id']
        sh = json.load(open(mp))['files'].get('tape_index/tape.jsonl', {}).get('sha256')
        if not sh: continue
        hh = hashlib.sha256(); n = 0; txt = open('tape.jsonl').read().split('\n')
        for ln in txt:
            if not ln: continue
            hh.update((ln + '\n').encode()); n += 1
            if hh.hexdigest() == sh: anch = dict(archive_id=a['id'], covers_n=n, attested=False); break
        if anch['archive_id']: 
            anch['digest'] = a['digest']; anch.pop('attested', None); break   # 13 Nov 2026 (the owner): no Bitcoin; the anchor is our own archive hash chain
except Exception as ex: anch['note'] = type(ex).__name__
last = chain[-1]; bq = [e for e in chain if e['kind'] == 'beacon'][-1]
lf = [e for e in chain if e['kind'] == 'feeds'][-1]; lfl = json.load(open('leaves/%d.json' % lf['n']))['leaves']
feedrec = {k: dict(n=lf['n'], hash=h) for k, h in lfl}
# 14 Nov 2026 (what_changed tool, the referee third pass): content and stamp-only events per feed, beside the chain and never in it (tape_changes.py)
changes_out = {}
try:
    import tape_changes as TCH
    chs = json.load(open('changes.json')) if os.path.exists('changes.json') else {}
    nowt = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    for k, b in bodies.items():
        if b: TCH.update(chs, k, b, nowt, lf['n'])
    json.dump(chs, open('changes.json.tmp', 'w')); os.replace('changes.json.tmp', 'changes.json'); changes_out = TCH.publish(chs)
except Exception as ex: print('tape: change record skipped (%s)' % type(ex).__name__)
out = dict(updated=time.strftime('%d %b %H:%M', time.gmtime()), read=1, count=len(chain), head=dict(n=last['n'], entry=last['entry'], t=last['t']), beacon=dict(n=bq['n'], t=bq['t'], value=bq['root'], drand_round=bq['subject'].replace('drand round ', '')), anchor=anch,
           feeds=feedrec, changes=changes_out, entries=[dict(n=e['n'], t=e['t'], kind=e['kind'], subject=e['subject'], root=e['root'], entry=e['entry'], prev=e['prev'], leaves='https://github.com/indahl-ai/indahl.ai/blob/main/code/tape/leaves/%d.json' % e['n']) for e in reversed(chain[-150:])])
json.dump(out, open('summary_tape.json', 'w'), indent=1)
os.makedirs(PUB + '/leaves', exist_ok=True)
# 20 Nov 2026: the tick copies DATA only (the chain, the plan, the leaves). It used to copy its own scripts here raw, and tape_push.py then pushed
# them to the public repository with infrastructure ids and an internal name in a comment, around the scrubber and the internal gate.
# The scripts now reach the mirror only through push_public.sh at a release, which scrubs them first.
_PUBLISH and subprocess.run('cp tape.jsonl PLAN.md %s/ && cp leaves/* %s/leaves/' % (PUB, PUB), shell=True)
subprocess.run('mkdir -p %s/qbits/runs && cp qbits/PLAN_QBITS.md.text qbits/qbits_run.py qbits/synth_selftest.text %s/qbits/ && (cp qbits/runs/* %s/qbits/runs/ 2>/dev/null || true)' % (PUB, PUB, PUB), shell=True)
# 30 Oct (site pass I-6): the chain files are pushed to the public repository in the background after each run, so the leaf links on the page open soon after an entry is written and not at the next release. Only code/tape is committed.
if _PUBLISH and not os.environ.get('TAPE_NO_PUSH'): subprocess.Popen([sys.executable, '-I', os.path.join(H, 'tape_push.py')], stdout=open('push_last.log', 'w'), stderr=subprocess.STDOUT, start_new_session=True)
env = dict(os.environ, CLOUDFLARE_ACCOUNT_ID='<cloudflare-account-id>', PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
pr = _kv_put(['/opt/homebrew/bin/npx', 'wrangler', 'kv', 'key', 'put', 'tape_live', '--path', os.path.join(H, 'summary_tape.json'), '--namespace-id', '<kv-namespace-id>', '--remote'], cwd=W, env=env, capture_output=True, text=True)
print('tape: entries', len(chain), 'head', last['entry'][:12], 'beacon', bv[:12], 'anchor n', anch['covers_n'], 'published' if pr.returncode == 0 else 'publish FAILED', flush=True)
