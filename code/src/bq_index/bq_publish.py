#!/usr/bin/env python3
"""bq_publish.py: BIGQUERY rider per PLAN.md. Loads the public history files, the STACK rows, the hash chain and the queue readings into one public BigQuery dataset.
Uses the Google Cloud tools' bq command with the account signed in on this Mac. BQ_SETUP=1 creates the project, the dataset and its public access once."""
import os, sys, re, json, time, glob, subprocess, urllib.request, tempfile
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import heuremen_kit as K
if not K.plan_committed(os.path.join(H, 'PLAN.md')): print('bigquery: plan not committed'); sys.exit(0)
SDK = '/opt/homebrew/share/google-cloud-sdk/bin'; GC = SDK + '/gcloud'; BQ = SDK + '/bq'; PROJECT = open(os.path.join(H, 'PROJECT')).read().strip() if os.path.exists(os.path.join(H, 'PROJECT')) else 'heuremen-llc-data'; DS = 'heuremen_public'
PUB = os.path.expanduser('~/forge/public_mirror/indahl.ai/code')
TERMS = 'Heuremen LLC public data. Free to read, run and cite with attribution. Use to train machine learning models is not permitted. Source: github.com/indahl-ai/indahl.ai, plans in code/SLUG/PLAN.md. https://indahl.ai'
def run(cmd, to=300): return subprocess.run(cmd, capture_output=True, text=True, timeout=to, env=dict(os.environ, CLOUDSDK_PYTHON=os.environ.get('CLOUDSDK_PYTHON') or '/opt/homebrew/bin/python3', PATH=SDK + ':/opt/homebrew/bin:' + os.environ.get('PATH', '/usr/bin:/bin')))   # 22 Nov 2026: bq calls gcloud by name; the desk bus PATH lacks the SDK   # 21 Nov 2026 (control audit #13): the bq CLI ran on the tick's /usr/bin/python3 3.9 and its urllib3 failed every load
def legal(k): return re.sub(r'[^A-Za-z0-9_]', '_', k.replace('.', '__'))[:128] or 'col'
def clean_file(src, dst):
    n = 0
    with open(src) as f, open(dst, 'w') as o:
        for l in f:
            if not l.strip(): continue
            try: d = json.loads(l)
            except Exception: continue
            o.write(json.dumps({legal(k): v for k, v in d.items() if not isinstance(v, (dict, list))}) + '\n'); n += 1
    return n
def load(table, path, desc, replace=True):
    r = run([BQ, 'load', '--project_id=' + PROJECT, '--autodetect', '--source_format=NEWLINE_DELIMITED_JSON'] + (['--replace'] if replace else []) + ['%s.%s' % (DS, table), path])
    if r.returncode: print('bigquery: load failed for', table, (r.stderr or r.stdout)[-200:]); return False
    run([BQ, 'update', '--project_id=' + PROJECT, '--description', desc, '%s.%s' % (DS, table)]); return True
def count(table):
    r = run([BQ, 'query', '--project_id=' + PROJECT, '--use_legacy_sql=false', '--format=json', 'SELECT COUNT(*) AS n FROM `%s.%s.%s`' % (PROJECT, DS, table)])
    try: return int(json.loads(r.stdout)[0]['n'])
    except Exception: return None
if os.environ.get('BQ_SETUP'):
    r = run([GC, 'projects', 'create', PROJECT, '--name=Heuremen LLC data']); print('project:', (r.stderr or r.stdout).strip()[-160:])
    r = run([GC, 'services', 'enable', 'bigquery.googleapis.com', '--project=' + PROJECT]); print('api:', (r.stderr or r.stdout).strip()[-120:])
    r = run([BQ, 'mk', '--project_id=' + PROJECT, '--dataset', '--location=US', '--description', TERMS.replace('SLUG', '<page>'), DS]); print('dataset:', (r.stderr or r.stdout).strip()[-120:])
    acc = run([BQ, 'show', '--project_id=' + PROJECT, '--format=prettyjson', DS]); d = json.loads(acc.stdout)
    if not any(a.get('specialGroup') == 'allAuthenticatedUsers' for a in d.get('access', [])):
        d['access'].append({'role': 'READER', 'specialGroup': 'allAuthenticatedUsers'}); json.dump(d, open('/tmp/bq_ds.json', 'w'))
        r = run([BQ, 'update', '--project_id=' + PROJECT, '--source', '/tmp/bq_ds.json', DS]); print('access:', (r.stderr or r.stdout).strip()[-120:])
    sys.exit(0)
# 22 Nov 2026: an expired gcloud login failed every load and rang only as 'LOAD CHECK FAILED {} 0 tables'; say what it is and what fixes it
if run([GC, 'auth', 'print-access-token'], 60).returncode:
    print('bigquery: LOAD CHECK FAILED: GCLOUD LOGIN EXPIRED (the owner types: ! gcloud auth login)'); sys.exit(1)
ok = True; report = {}
tmp = tempfile.mkdtemp(prefix='bq_')
for f in sorted(glob.glob(PUB + '/*/history.jsonl')):
    slug = os.path.basename(os.path.dirname(f)).replace('-', '_'); dst = os.path.join(tmp, slug + '.jsonl'); n = clean_file(f, dst)
    if not n: continue
    if not load('history_' + slug, dst, TERMS.replace('SLUG', os.path.basename(os.path.dirname(f)))): ok = False; continue   # 22 Nov: a failed load is a failed run (an expired gcloud login failed silently)
    c = count('history_' + slug); report['history_' + slug] = (n, c); ok &= (c == n)
for name, rel in (('archive_chain', 'archive/chain.jsonl'),):
    f = PUB + '/' + rel; dst = os.path.join(tmp, name + '.jsonl'); n = clean_file(f, dst)
    if not n: continue
    if not load(name, dst, TERMS.replace('SLUG', 'archive')): ok = False; continue
    c = count(name); report[name] = (n, c); ok &= (c == n)
# 22 Nov 2026: the STACK desk is retired; tests_history is no longer appended.
print('bigquery:', 'LOAD OK' if ok else 'LOAD CHECK FAILED', {k: v for k, v in list(report.items())[:6]}, '...', len(report), 'tables')
json.dump(dict(t=time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime()), ok=ok, tables=report), open('last_load.json', 'w'))
if not ok: sys.exit(1)   # 22 Nov 2026: rider_wrap rings pipe.log on a nonzero exit
