#!/usr/bin/env python3
"""money_path_check.py (21 Nov 2026, owner-approved): after a ship deploys, check what a visitor actually gets on quantumidleaudit.com.

  1. the home page answers 200 and carries the Check a run box (qia-cr)
  2. every demo page (/demo-<slug>, slugs from calibrations/site/demos.json, the list console/build.py builds from) and /inquiries answer 200;
     21 Nov: the inquiry door too (/inquiries links indahl.ai/contact, its NDA form, /gate-ui.js, and a non-storing dry POST to /inquire), and
     ledger/inquiry_bell.py runs so a new inquiry rings after a ship as well as on the tick bus
  3. every file Check a run loads answers 200 with the right kind of body: /check_run.js, /qia/runcheck.js (JavaScript, not an HTML page),
     /qia/records/index.json, /qia/cal.json, /qia/offchain.json (JSON that parses), and for ibm_fez its records manifest, the day files a run
     today needs and the newest calibration job file /qia/cal/<job>.json
  4. a real functional run: the LIVE runcheck.js loaded in Node with a stub window (as qia_runcheck/tests/js_driver.js does), window.QIARunCheck.load
     against the LIVE JSON for ibm_fez, today's window, qubits 0,1,5; it must return a result with no exception

Any failure (rung once per new set of failures; see main) appends `MONEY PATH FAILED: <what>` to sagar/pipeline/pipe.log (watch/doorbell/poll.py rings it into the inbox) and exits 1.
Nothing here writes to the site. Run: python3 ledger/money_path_check.py   (--quiet prints only failures)."""
import datetime as D, json, os, re, subprocess, sys, tempfile, time, urllib.request

B = os.path.expanduser('~/forge'); SITE = 'https://quantumidleaudit.com'
PIPE_LOG = os.environ.get('MONEY_PATH_LOG') or os.path.join(B, 'sagar', 'pipeline', 'pipe.log')   # the env override: dry tests, and ship.sh step 4a (22 Nov 2026 P2: the ship's one ring, from ship_queue.py, carries the failure)
STATE = os.environ.get('MONEY_PATH_STATE') or os.path.join(B, 'ledger', '.money_path_state.json')
UA = {'User-Agent': 'research-client'}
PROC, QUBITS = 'ibm_fez', '0,1,5'
NODE = next((p for p in ('/opt/homebrew/bin/node', '/usr/local/bin/node') if os.path.exists(p)), 'node')
QUIET = '--quiet' in sys.argv
fails, oks = [], []


def ring(msg):
    line = '%s %s' % (time.strftime('%Y-%m-%dT%H:%M:%S'), msg.replace('\n', ' ')[:600])
    try:
        with open(PIPE_LOG, 'a') as f: f.write(line + '\n')
    except Exception as e: sys.stderr.write('money_path: could not write the pipeline log (%s)\n' % e)


def get(path, timeout=30):
    """-> (status, content_type, body bytes). Network errors come back as status 0."""
    u = path if path.startswith('http') else SITE + path
    try:
        r = urllib.request.urlopen(urllib.request.Request(u + ('&' if '?' in u else '?') + 'mpc=%d' % time.time(), headers=UA), timeout=timeout)
        return r.status, r.headers.get('Content-Type', ''), r.read()
    except urllib.error.HTTPError as e: return e.code, e.headers.get('Content-Type', '') if e.headers else '', b''
    except Exception as e: return 0, type(e).__name__ + ': ' + str(e)[:120], b''


def fail(what): fails.append(what)
def ok(what): oks.append(what)


def page(path, must=None):
    st, ct, body = get(path)
    if st != 200: return fail('%s answered %s %s' % (path, st, ct if not st else ''))
    if must and must.encode() not in body: return fail('%s has no %s' % (path, must))
    ok(path)


def js(path):
    st, ct, body = get(path)
    if st != 200: fail('%s answered %s' % (path, st)); return None
    head = body[:400].lstrip().lower()
    if not body.strip() or head.startswith(b'<!doctype') or head.startswith(b'<html'): fail('%s is not JavaScript (%s, %d bytes)' % (path, ct, len(body))); return None
    ok(path); return body


def jget(path):
    st, ct, body = get(path)
    if st != 200: fail('%s answered %s' % (path, st)); return None
    try: d = json.loads(body)
    except Exception: fail('%s is not JSON (%s, starts %r)' % (path, ct, body[:40])); return None
    ok(path); return d


def inquiry_door():
    """21 Nov 2026 (money-path check): /inquiries hands off to the NDA-gated form on indahl.ai. Check the hand-off page, the form's script, and
    the POST endpoint itself with a NON-STORING request: a POST with no fill-time field is refused by indahl-ai/inquire.js at line 30 ('too
    quickly', 400) before any store write, after it has proved the route answers, the store binding exists (503 otherwise) and the body parses."""
    st, ct, body = get('/inquiries')
    if st == 200 and b'indahl.ai/contact' not in body: fail('/inquiries no longer links the inquiry form (indahl.ai/contact)')
    st, ct, body = get('https://indahl.ai/contact')
    if st != 200: fail('indahl.ai/contact (the NDA step) answered %s' % st)
    elif b'action="/agree"' not in body: fail('indahl.ai/contact has no NDA agreement form (action="/agree")')
    else: ok('indahl.ai/contact NDA step')
    js('https://indahl.ai/gate-ui.js')
    try:
        req = urllib.request.Request('https://indahl.ai/inquire', data=b'money_path_check=1', method='POST',
                                     headers=dict(UA, **{'Content-Type': 'application/x-www-form-urlencoded'}))
        r = urllib.request.urlopen(req, timeout=30); st, body = r.status, r.read()
    except urllib.error.HTTPError as e: st, body = e.code, e.read()
    except Exception as e: return fail('indahl.ai/inquire POST did not answer (%s)' % type(e).__name__)
    if st == 400 and b'too quickly' in body: ok('indahl.ai/inquire POST endpoint (dry request refused, nothing stored)')
    else: fail('indahl.ai/inquire dry POST answered %s, not the 400 fill-time refusal (route, store binding or handler broken)' % st)


def demo_slugs():
    try: return [d['slug'] for d in json.load(open(os.path.join(B, 'calibrations', 'site', 'demos.json')))['demos']]
    except Exception as e:
        fail('demo list unreadable (calibrations/site/demos.json: %s)' % type(e).__name__); return []


DRIVER = r"""
// node driver: argv[2] = runcheck.js source path, argv[3] = site, argv[4] = backend, argv[5] = start, argv[6] = end, argv[7] = qubits
const fs = require('fs'), vm = require('vm');
const [src, site, backend, start, end, qubits] = process.argv.slice(2);
const sandbox = { window: {}, console, Promise, Date, Math, JSON, Number, String, Object, Array, isNaN, parseInt, parseFloat };
sandbox.globalThis = sandbox; vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(src, 'utf8'), sandbox, { filename: 'runcheck.js' });
const R = sandbox.window.QIARunCheck;
if (!R || typeof R.load !== 'function') { console.error('window.QIARunCheck.load is missing'); process.exit(2); }
const fetched = [];
const getJson = u => { fetched.push(u); return fetch(site + u, { headers: { 'User-Agent': 'research-client' } }).then(r => { if (!r.ok) throw new Error(u + ' ' + r.status); return r.json(); }); };
(async () => {
  const s = R.parseWhen(start), e = R.parseWhen(end), q = R.parseQubits(qubits);
  if (isNaN(s) || isNaN(e) || q.error) throw new Error('bad window or qubits: ' + start + ' / ' + end + ' / ' + qubits);
  const r = await R.load(getJson, backend, s, e, q);
  if (!r || !Array.isArray(r.flags) || !Array.isArray(r.during) || !r.manifest) throw new Error('result has no flags/during/manifest');
  process.stdout.write(JSON.stringify({ under: r.under ? r.under.iso : null, file: r.under ? r.under.file : null, during: r.during.length, flags: r.flags.length,
    changes: (r.changes || []).length, missing: r.missing, newest: r.manifest.newest, fetched }));
})().catch(err => { console.error(String(err && err.stack || err)); process.exit(1); });
"""


def functional(src_bytes):
    now = D.datetime.now(D.timezone.utc).replace(second=0, microsecond=0)
    start = max(now.replace(hour=0, minute=0), now - D.timedelta(hours=2)); end = now
    if start >= end: start = end - D.timedelta(minutes=10)
    fmt = lambda t: t.strftime('%Y-%m-%d %H:%M')
    with tempfile.TemporaryDirectory() as td:
        sp, dp = os.path.join(td, 'runcheck.js'), os.path.join(td, 'driver.js')
        open(sp, 'wb').write(src_bytes); open(dp, 'w').write(DRIVER)
        try: r = subprocess.run([NODE, dp, sp, SITE, PROC, fmt(start), fmt(end), QUBITS], capture_output=True, text=True, timeout=180)
        except Exception as e: return fail('functional run: node could not run (%s)' % type(e).__name__)
    if r.returncode != 0: return fail('functional run %s %s..%s q %s threw: %s' % (PROC, fmt(start), fmt(end), QUBITS, (r.stderr.strip().splitlines() or ['exit %d' % r.returncode])[0][:240]))
    try: res = json.loads(r.stdout)
    except Exception: return fail('functional run printed no result')
    if not res.get('under'): return fail('functional run %s %s..%s: no record in force at the start (mirror newest %s)' % (PROC, fmt(start), fmt(end), res.get('newest')))
    ok('functional run %s %s..%s q %s: record %s, %d flag rows, %d during, %d changes, day files %s'
       % (PROC, fmt(start), fmt(end), QUBITS, res['under'], res['flags'], res['during'], res['changes'], ','.join(u.rsplit('/', 1)[1] for u in res['fetched'] if not u.endswith('manifest.json'))))
    return res


def main():
    page('/', must='qia-cr')
    for s in demo_slugs(): page('/demo-' + s)
    page('/inquiries')
    inquiry_door()
    try: subprocess.run([sys.executable, os.path.join(B, 'ledger', 'inquiry_bell.py')], timeout=150, capture_output=True)   # rings any new inquiry after a ship too
    except Exception: pass
    js('/check_run.js')
    rc_src = js('/qia/runcheck.js')
    ix = jget('/qia/records/index.json')
    cal = jget('/qia/cal.json')
    jget('/qia/offchain.json')
    if ix is not None and PROC not in [p.get('backend') for p in ix.get('processors', [])]: fail('/qia/records/index.json does not list %s' % PROC)
    jget('/qia/records/%s/manifest.json' % PROC)
    if cal is not None:
        p = (cal.get('processors') or {}).get(PROC)
        if not p or not p.get('job_id'): fail('/qia/cal.json has no newest job for %s' % PROC)
        else: jget('/qia/cal/%s.json' % p['job_id'])
    if rc_src is not None: functional(rc_src)   # also fetches the day files a run today needs; a missing one throws there
    if not QUIET:
        for o in oks: print('ok   ' + o)
    # ring only when the set of failures changes (a new set, or cleared), so a standing failure rings once, not every run;
    # the last set is kept in ledger/.money_path_state.json. Every run still prints and exits 1 on any failure.
    key = sorted(re.sub(r'\d{4}-\d\d-\d\d \d\d:\d\d', 'T', f) for f in fails)   # the run window's times move every run
    try: last = json.load(open(STATE)).get('fails', [])
    except Exception: last = None
    for f in fails: print('FAIL ' + f)
    if key != last:
        for f in fails: ring('MONEY PATH FAILED: ' + f)
        if not fails and last: ring('money path: cleared, quantumidleaudit.com Check a run works end to end')
        try: tmp = STATE + '.tmp'; json.dump({'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'fails': key}, open(tmp, 'w'), indent=1); os.replace(tmp, STATE)
        except Exception: pass
    print('money path: %d checks ok, %d failed' % (len(oks), len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
