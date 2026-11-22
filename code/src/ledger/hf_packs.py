#!/usr/bin/env python3
"""Every indahl.ai desk data pack as a Hugging Face dataset, indahl/<desk>-data-pack (15 Nov 2026, the owner: "ANYTHING else from
Indahl.ai that you can put on hf"). Reads only what is COMMITTED in public_mirror/indahl.ai (git show HEAD:<desk>/<desk>-data-pack.zip),
unpacks it UNCHANGED into pack/ (so its SHA256SUMS.txt still verifies every file), and writes a separate dataset card as the top README: license "other" linked to the pack's LICENSE.txt (each part keeps
its source's terms), and one viewer config per results CSV. A dataset that already exists is updated only with --update (the hand-built
atlas and oy cards are never touched without it).
  python3 hf_packs.py [--update] [desk ...]"""
import io, os, subprocess, sys, tempfile, zipfile, json, urllib.request
M = os.path.expanduser('~/forge/public_mirror/indahl.ai'); UPDATE = '--update' in sys.argv
want = [a for a in sys.argv[1:] if not a.startswith('--')]
packs = [p for p in subprocess.run(['git', '-C', M, 'ls-files'], capture_output=True, text=True).stdout.split('\n') if p.endswith('-data-pack.zip')]
def exists(rid):
    try: urllib.request.urlopen('https://huggingface.co/api/datasets/' + rid, timeout=30); return True
    except Exception: return False
# 17 Nov 2026, the owner: one public list per desk; no study-list downloads (a copy already downloaded keeps a removed study on).
# indahl/qia-list, indahl/iris-list and indahl/qia-calibrated-studies were set PRIVATE (main session, 17 Nov). This script never creates, uploads to
# or changes the visibility of a study-list dataset, and refuses any pack whose name or desk says list.
NEVER = {'indahl/qia-list', 'indahl/iris-list', 'indahl/qia-calibrated-studies'}
for p in packs:
    desk = p.split('/')[0]
    if 'indahl/%s-data-pack' % desk in NEVER or desk.endswith('-list') or 'list-pack' in p: print('REFUSED %s (study list, not a data pack)' % p); continue
    if want and desk not in want: continue
    rid = 'indahl/%s-data-pack' % desk
    if exists(rid) and not UPDATE: print('SKIP %s (exists)' % rid); continue
    blob = subprocess.run(['git', '-C', M, 'show', 'HEAD:' + p], capture_output=True).stdout
    z = zipfile.ZipFile(io.BytesIO(blob)); t = tempfile.mkdtemp(); root = None
    for n in z.namelist():
        if n.endswith('/'): continue
        rel = n.split('/', 1)[1] if '/' in n else n; root = n.split('/')[0]
        dst = os.path.join(t, 'pack', rel); os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'wb').write(z.read(n))
    csvs = sorted(os.path.relpath(os.path.join(d, f), t) for d, _, fs in os.walk(os.path.join(t, 'pack')) for f in fs if f.endswith('.csv'))
    csvs.sort(key=lambda c: (not c.endswith('_outcomes.csv'), c))
    cfg = ''.join('- config_name: %s\n%s  data_files: %s\n' % (os.path.splitext(os.path.basename(c))[0], '  default: true\n' if i == 0 else '', c) for i, c in enumerate(csvs))
    head = ('---\npretty_name: "%s Data Pack"\nlicense: other\nlicense_name: per-part-see-license\nlicense_link: https://huggingface.co/datasets/%s/blob/main/pack/LICENSE.txt\n'
            'tags:\n- indahl\n- heuremen\n- %s\n- stated-vs-delivered\nconfigs:\n%s---\n') % (desk.upper(), rid, desk, cfg)
    src = os.path.join(t, 'pack', 'README.md'); body = open(src).read() if os.path.exists(src) else '# %s Data Pack\n' % desk.upper()
    note = ('\n\n---\n\nThe pack is in pack/ exactly as published at https://indahl.ai/%s/%s-data-pack.zip; pack/SHA256SUMS.txt verifies every file. '
            'Paths above are relative to pack/. Terms: pack/LICENSE.txt and pack/NOTICE.txt.\n') % (desk, desk)
    open(os.path.join(t, 'README.md'), 'w').write(head + body + note)
    subprocess.run(['hf', 'repos', 'create', rid, '--type', 'dataset', '--public', '--exist-ok'], capture_output=True)
    r = subprocess.run(['hf', 'upload', rid, t, '.', '--repo-type', 'dataset', '--delete', '*', '--commit-message', 'Data pack as committed at indahl.ai %s' % p], capture_output=True, text=True)
    print(('OK   ' if r.returncode == 0 else 'FAIL ') + rid + ('' if r.returncode == 0 else ' ' + r.stderr[-200:]), flush=True)
