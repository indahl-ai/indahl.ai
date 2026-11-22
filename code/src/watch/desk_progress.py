"""desk_progress.py (31 Oct 2026, his "if this is live, can we get a loading bar or live action of something?"): a desk's rider reports
its pass as it runs. report(desk, done, total, what) writes watch/progress/<desk>.json and pushes it to KV key progress_<desk>
(served at indahl.ai/progress/<desk>.json), at most every 10 seconds, in a detached process so the pass never waits on the push.
finish(desk, total) marks the pass finished. Only counts and the public item being read are sent."""
import json, os, time, subprocess
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
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progress'); os.makedirs(D, exist_ok=True)
W = os.path.expanduser('~/forge/cloudflare-workers/heuremen-door'); NS = '<kv-namespace-id>'
_last = {}
def _push(desk, d):
    f = os.path.join(D, desk + '.json'); tmp = f + '.tmp'; json.dump(d, open(tmp, 'w')); os.replace(tmp, f)
    # 22 Nov 2026 (P3): the put goes through lib/cf.py (kv token, timeout, rings on failure), still in a detached child so the tick never waits on it
    try: (_PUBLISH or _pg_os.environ.get('HEUREMEN_PUBLISH') == '1') and subprocess.Popen([_pg_sys.executable, '-I', '-c', "import sys; sys.path.insert(0, sys.argv[3]); import cf; cf.kv_put(sys.argv[1], sys.argv[2], who='desk_progress.py')",
                          'progress_' + desk, f, _pg_os.path.expanduser('~/forge/lib')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    except Exception: pass
def report(desk, done, total, what='', label=''):
    now = time.time()
    if now - _last.get(desk, 0) < 10 and done < total: return
    _last[desk] = now
    _push(desk, dict(desk=desk, running=True, done=int(done), total=int(total), what=str(what)[:120], label=label, t=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now))))
def finish(desk, total, label=''):
    _push(desk, dict(desk=desk, running=False, done=int(total), total=int(total), what='', label=label, t=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
