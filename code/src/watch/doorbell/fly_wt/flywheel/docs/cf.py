"""One Cloudflare part for every job (22 Nov 2026, the owner: "interchangeable parts").

Every job that touches Cloudflare imports this instead of building its own wrangler call:

    import sys, os; sys.path.insert(0, os.path.expanduser('~/forge/lib')); import cf
    cf.kv_put('qia_cal', '/path/file.json')            # True/False, rings on failure
    cf.kv_get('headlines')                              # str or None, rings on failure
    cf.kv_list('al:')                                   # list of names or None
    cf.token('mail')                                    # token for direct API calls

Which credential each role uses (keychain service, never printed):
    deploy  cloudflare-api-token-ship   ledger/ship.sh deploys the worker
    kv      cloudflare-api-token-kv     every data push and read (default)
    mail    cloudflare-api-token-mail   email sending and delivery/analytics reads
Fallback for any role: the wrangler login (~/Library/Preferences/.wrangler).

Every failure writes one RING line to sagar/pipeline/pipe.log, so it reaches the operator.
Commands run from $HOME with the token passed explicitly, so no folder's .env decides which credential is used.
"""
import os, re, subprocess, time

ACCOUNT = '<cloudflare-account-id>'
NS_DEFAULT = '<kv-namespace-id>'   # the site's public data namespace (qia_cal, headlines, feeds)
SERVICE = {'deploy': 'cloudflare-api-token-ship', 'kv': 'cloudflare-api-token-kv', 'mail': 'cloudflare-api-token-mail'}
PIPE = os.path.expanduser('~/forge/sagar/pipeline/pipe.log')
NPX = '/opt/homebrew/bin/npx'
_cache = {}


def token(role='kv'):
    """The role's API token from the keychain, or '' (then wrangler falls back to the login)."""
    if role not in _cache:
        r = subprocess.run(['security', 'find-generic-password', '-s', SERVICE[role], '-w'], capture_output=True, text=True)
        _cache[role] = r.stdout.strip() if r.returncode == 0 else ''
    return _cache[role]


def ring(what):
    try:
        with open(PIPE, 'a') as f: f.write(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + ' RING: CLOUDFLARE ' + what.replace('\n', ' ')[:300] + '\n')
    except OSError: pass


def wrangler(*args, role='kv', timeout=180, stdout_only=False):
    """Run one wrangler command with the role's token. Returns (returncode, output without colour codes)."""
    env = {k: v for k, v in os.environ.items() if k != 'CLOUDFLARE_API_TOKEN'}
    env.update(CLOUDFLARE_ACCOUNT_ID=ACCOUNT, PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
    t = token(role)
    if t: env['CLOUDFLARE_API_TOKEN'] = t
    try:
        r = subprocess.run([NPX, 'wrangler', *args], cwd=os.path.expanduser('~'), env=env, capture_output=True, text=True, timeout=timeout)
        return r.returncode, re.sub(r'\x1b\[[0-9;]*m', '', r.stdout if (stdout_only and r.returncode == 0) else r.stdout + r.stderr)
    except subprocess.TimeoutExpired:
        return 124, 'timed out after %d s' % timeout


def _why(out):
    m = re.search(r'(Authentication error[^\n]*|code: \d+[^\n]*|ERROR[^\n]*)', out)
    return (m.group(1) if m else out.strip()[-160:])


def kv_put(key, path, ns=NS_DEFAULT, who='?'):
    rc, out = wrangler('kv', 'key', 'put', key, '--path', path, '--namespace-id', ns, '--remote')
    if rc: ring('KV PUT FAILED %s (from %s): %s' % (key, who, _why(out)))
    return rc == 0


def kv_put_value(key, value, ns=NS_DEFAULT, who='?'):
    rc, out = wrangler('kv', 'key', 'put', key, value, '--namespace-id', ns, '--remote')
    if rc: ring('KV PUT FAILED %s (from %s): %s' % (key, who, _why(out)))
    return rc == 0


def kv_get(key, ns=NS_DEFAULT, who='?'):
    rc, out = wrangler('kv', 'key', 'get', key, '--namespace-id', ns, '--remote', '--text', stdout_only=True)
    if rc: ring('KV GET FAILED %s (from %s): %s' % (key, who, _why(out))); return None
    return out


def kv_list(prefix='', ns=NS_DEFAULT, who='?'):
    import json
    rc, out = wrangler('kv', 'key', 'list', '--namespace-id', ns, '--remote', *(['--prefix', prefix] if prefix else []))
    if rc: ring('KV LIST FAILED %s (from %s): %s' % (prefix or '*', who, _why(out))); return None
    try: return [x['name'] for x in json.loads(out[out.index('['):])]
    except Exception: ring('KV LIST UNREADABLE %s (from %s)' % (prefix or '*', who)); return None


if __name__ == '__main__':   # self-test: each role's token is present and the KV role can list
    for r in SERVICE: print(r, 'token' if token(r) else 'NO TOKEN (login fallback)')
    k = kv_list('qia_cal', who='cf selftest'); print('kv list qia_cal*:', 'FAILED' if k is None else len(k))


def guarded_put(cmd, **kw):
    """Drop-in for the 58 identical `_kv_put(cmd, **kw)` publish guards in the desk ticks.
    Same contract: publishes only when the tick bus / house clock (HEUREMEN_PUBLISH=1) or --publish started the run,
    returns a CompletedProcess. Differences: runs with the kv token from $HOME, and rings on failure."""
    import sys, subprocess
    text = bool(kw.get('text') or kw.get('universal_newlines'))
    if not ('--publish' in sys.argv or os.environ.get('HEUREMEN_PUBLISH') == '1'):
        print('publish guard: %s not put to the site KV (run with --publish, or from the tick bus)' % (cmd[5] if len(cmd) > 5 else cmd), file=sys.stderr)
        return subprocess.CompletedProcess(cmd, 0, '' if text else b'', '' if text else b'')
    i = next((n for n, a in enumerate(cmd) if str(a).endswith('wrangler')), None)
    args = list(cmd[i + 1:]) if i is not None else list(cmd)
    rc, out = wrangler(*args, timeout=kw.get('timeout') or 180)
    if rc: ring('KV PUT FAILED %s (from %s): %s' % (args[3] if len(args) > 3 else '?', os.path.basename(sys.argv[0]), _why(out)))
    return subprocess.CompletedProcess(cmd, rc, out if text else out.encode(), '' if text else b'')


def run_put(cmd, **kw):
    """Drop-in for a bare `subprocess.run([... 'wrangler', 'kv', ...], **kw)` (no publish guard, same as before).
    Runs with the kv token from $HOME and rings on failure; returns a CompletedProcess."""
    import sys, subprocess
    text = bool(kw.get('text') or kw.get('universal_newlines'))
    i = next((n for n, a in enumerate(cmd) if str(a).endswith('wrangler')), None)
    args = list(cmd[i + 1:]) if i is not None else list(cmd)
    rc, out = wrangler(*args, timeout=kw.get('timeout') or 180)
    if rc: ring('KV CALL FAILED %s (from %s): %s' % (' '.join(map(str, args[:4])), os.path.basename(sys.argv[0]), _why(out)))
    return subprocess.CompletedProcess(cmd, rc, out if text else out.encode(), '' if text else b'')
