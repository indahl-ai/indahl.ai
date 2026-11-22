#!/usr/bin/env python3
"""mirror_check.py -- drift watcher for every published copy (15 Nov 2026, the owner: "automated updates the operator.....why you so dirty with them
man?" and the final call: "everything is on indahl.ai public repo and check there first").

Every check compares a copy against its source and names the gap. Nothing is fixed here; alerts_check.py turns each problem into an alert.
  1 GitHub: each local clone of an indahl-ai repo against origin/main (unpushed work, or a clone that stopped pulling)
  2 Hugging Face: each code mirror's newest commit names the GitHub commit it was built from; that must be the GitHub HEAD
  3 YO: the adapter on indahl/yo must be the adapter the live reader names (yo/LIVE_READER_ON)
  4 Addresses: no live script reads or dispatches through Heuremen-LLC (the archive) instead of indahl-ai
Writes watch/mirror_status.json: {"at", "checked", "problems": [{"id", "what"}]}.
  python3 mirror_check.py            run every check
  python3 mirror_check.py --quick    skip the network checks (1 remote side, 2, 3)"""
import glob, json, os, re, subprocess, sys, time
B = os.path.expanduser('~/forge'); OUT = os.path.join(B, 'watch', 'mirror_status.json')
QUICK = '--quick' in sys.argv; probs = []; checked = 0
def flag(i, w): probs.append(dict(id=i, what=w))
def git(repo, *a, t=60):
    r = subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True, timeout=t); return r.stdout.strip() if r.returncode == 0 else None

# 1 GitHub clones
clones = sorted(glob.glob(B + '/plugin_repos/*/.git')) + [B + '/public_mirror/indahl.ai/.git', B + '/nodes_repo/.git', B + '/internal_timestamped_archived_data/.git']
heads = {}
for g in clones:
    repo = os.path.dirname(g); url = git(repo, 'remote', 'get-url', 'origin') or ''
    m = re.search(r'github\.com[:/]([\w.-]+)/([\w.-]+?)(?:\.git)?$', url)
    if not m: continue
    owner, name = m.groups(); checked += 1
    if owner.lower() != 'indahl-ai': flag('git:%s' % name, '%s pushes to %s/%s, not indahl-ai' % (repo, owner, name)); continue
    local = git(repo, 'rev-parse', 'HEAD'); heads[name] = local
    if QUICK: continue
    rl = git(repo, 'ls-remote', 'origin', 'refs/heads/main')
    remote = rl.split()[0] if rl else None
    if remote is None: flag('git:%s' % name, 'indahl-ai/%s: could not read origin main' % name); continue
    heads[name] = remote
    if remote != local:
        if git(repo, 'merge-base', '--is-ancestor', remote, local) is not None and subprocess.run(['git', '-C', repo, 'merge-base', '--is-ancestor', remote, local]).returncode == 0:
            flag('git:%s' % name, 'indahl-ai/%s: local clone has commits not pushed (%s ahead of %s)' % (name, local[:8], remote[:8]))
        elif name not in ('nodes',):   # the runner commits to nodes on every probe; a nodes clone behind origin is normal between pulls
            flag('git:%s' % name, 'indahl-ai/%s: local clone %s differs from GitHub %s' % (name, local[:8], remote[:8]))

# 2 Hugging Face code mirrors, 3 YO
# HF WALL 18 Nov 2026 (the owner: hard wall, no Hugging Face): the HF repos are private and no longer synced, so they are not checked
if False:
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        for name, head in sorted(heads.items()):
            if name in ('nodes', 'internal-timestamped-archived-data') or not head: continue
            checked += 1
            try: title = api.list_repo_commits('indahl/' + name)[0].title
            except Exception as e: flag('hf:%s' % name, 'indahl/%s: not readable on Hugging Face (%s)' % (name, type(e).__name__)); continue
            m = re.search(r'github\.com/indahl-ai/%s at ([0-9a-f]{7,40})' % re.escape(name), title)
            if not m: flag('hf:%s' % name, 'indahl/%s: newest commit does not name its GitHub source ("%s")' % (name, title[:80])); continue
            if not head.startswith(m.group(1)):
                if name == 'indahl.ai':   # riders push the site repo every few minutes; the HF site mirror is flagged only when it is 6+ hours behind
                    t = git(os.path.join(B, 'public_mirror', 'indahl.ai'), 'log', '-1', '--format=%ct', m.group(1))
                    if t and int(git(os.path.join(B, 'public_mirror', 'indahl.ai'), 'log', '-1', '--format=%ct', 'HEAD') or 0) - int(t) < 6 * 3600: continue
                flag('hf:%s' % name, 'indahl/%s mirrors GitHub %s, GitHub is at %s' % (name, m.group(1)[:8], head[:8]))
        checked += 1
        want = open(os.path.join(B, 'yo', 'LIVE_READER_ON')).read().split()[-1]
        info = api.model_info('indahl/yo', files_metadata=True)
        got = next((s.lfs.sha256 if s.lfs else None) for s in info.siblings if s.rfilename == 'adapter/adapters.safetensors')
        if not got or not got.startswith(want): flag('hf:yo', 'indahl/yo adapter %s is not the live adapter %s' % ((got or 'missing')[:16], want))
    except ImportError:
        flag('hf:tools', 'huggingface_hub not importable; run with ~/forge/venv/bin/python')

# 4 old addresses in live scripts
pat = re.compile(r'raw\.githubusercontent\.com/Heuremen-LLC/|repos/Heuremen-LLC/[\w.-]+/(dispatches|contents)|github\.com/Heuremen-LLC/(nodes|indahl\.ai)/')
files = [f for d in ('*_index/*.py', '*_index/*/*.py', 'watch/*.py', 'ledger/*.py', 'ledger/*.sh', 'tools/*.py', 'nodes_repo/*/*.py', 'yo/*.py', 'qia_leads/matrix_page/*.py', 'indahl-ai/*.py')
         for f in glob.glob(os.path.join(B, d)) if not re.search(r'\.bak|\.pre-|_bak', f) and not f.endswith('mirror_check.py')]
checked += 1; hits = []
for f in files:
    try: s = open(f, encoding='utf-8', errors='ignore').read()
    except OSError: continue
    if pat.search(s): hits.append(os.path.relpath(f, B))
if hits: flag('addr:heuremen-llc', 'live scripts still use Heuremen-LLC addresses: ' + ', '.join(hits[:8]) + (' and %d more' % (len(hits) - 8) if len(hits) > 8 else ''))

json.dump(dict(at=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), checked=checked, problems=probs), open(OUT, 'w'), indent=1)
print('mirror_check: %d checks, %d problems' % (checked, len(probs)))
for p in probs: print('  ' + p['what'])
