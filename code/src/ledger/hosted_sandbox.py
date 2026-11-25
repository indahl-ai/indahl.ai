#!/usr/bin/env python3
"""hosted_sandbox.py: a QIA-hosted demonstration sandbox for a prospect (24 Nov 2026, owner: "build the hosted sandbox").

  python3 ledger/hosted_sandbox.py grant "<who, for the record>" [--hours 24] [--clip | --link]
      Starts a CPU pod on the house RunPod account from the private template (JupyterLab on port 8888, same setup as the public
      template), with a fresh random password. Waits until the notebook answers, then prints the link, the password and a reply draft
      (--clip puts the draft on the clipboard; it is never sent from here). Refuses past CAP live sandboxes.
  python3 ledger/hosted_sandbox.py list         live hosted sandboxes, age, expiry
  python3 ledger/hosted_sandbox.py sweep        terminates every hosted sandbox past its expiry (a desk_bus rider runs this)

Record: ledger/gates/hosted_sandboxes.jsonl (who, pod id, created, expiry, terminated). The password is never written to the record.
Cost: the cpu3c-2-4 pod is $0.06 an hour, so a 24 h sandbox is about $1.44. The RunPod key is read from the keychain, never printed."""
import json, os, secrets, subprocess, sys, time, urllib.request

TEMPLATE = 'xkgdhxfb9o'          # private template "QIA hosted sandbox": public template's setup + ports 8888/http,22/tcp
INSTANCE = 'cpu3c-2-4'
CAP = 5
REC = os.path.expanduser('~/forge/ledger/gates/hosted_sandboxes.jsonl')
PREFIX = 'qia-hosted-'
NB = 'lab/tree/demo/QIA_demonstrations.ipynb'


def gql(q, v=None):
    k = subprocess.run(['security', 'find-generic-password', '-s', 'runpod-api-key', '-w'], capture_output=True, text=True).stdout.strip()
    r = urllib.request.Request('https://api.runpod.io/graphql?api_key=' + k, data=json.dumps({'query': q, 'variables': v or {}}).encode(),
                               headers={'Content-Type': 'application/json', 'User-Agent': 'curl/8.7.1'})
    out = json.load(urllib.request.urlopen(r, timeout=60))
    if out.get('errors'): raise SystemExit('RunPod: %s' % out['errors'][0].get('message'))
    return out['data']


def pods():
    return [p for p in gql('query { myself { pods { id name desiredStatus costPerHr } } }')['myself']['pods'] if p['name'].startswith(PREFIX)]


def records():
    if not os.path.exists(REC): return []
    return [json.loads(l) for l in open(REC) if l.strip()]


def write(rec):
    os.makedirs(os.path.dirname(REC), exist_ok=True)
    with open(REC, 'a') as f: f.write(json.dumps(rec) + '\n')


def grant(who, hours, clip):
    live = pods()
    if len(live) >= CAP: sys.exit('REFUSED: %d hosted sandboxes are live (cap %d). Run list, or sweep.' % (len(live), CAP))
    pw = secrets.token_urlsafe(12)
    name = PREFIX + time.strftime('%m%d-%H%M')
    d = gql('mutation($i: deployCpuPodInput!) { deployCpuPod(input: $i) { id costPerHr } }',
            {'i': dict(name=name, instanceId=INSTANCE, cloudType='SECURE', templateId=TEMPLATE, containerDiskInGb=10, startJupyter=True,
                       env=[{'key': 'JUPYTER_PASSWORD', 'value': pw}])})['deployCpuPod']
    if not d: sys.exit('RunPod returned no pod (no CPU capacity?). Try again in a minute.')
    pid, t0 = d['id'], time.time()
    write(dict(event='created', who=who, pod=pid, name=name, created=int(t0), expires=int(t0 + hours * 3600), cost_per_hr=d.get('costPerHr')))
    url = 'https://%s-8888.proxy.runpod.net/' % pid
    ok = False
    for i in range(60):                                   # up to 10 minutes: pod start, setup (about a minute), JupyterLab
        time.sleep(10)
        try:
            r = urllib.request.urlopen(urllib.request.Request(url + 'api/status', headers={'User-Agent': 'curl/8.7.1'}), timeout=15)
            if r.status in (200, 403): ok = True
        except urllib.error.HTTPError as e:
            if e.code in (401, 403): ok = True
        except Exception: pass
        if ok: break
    if not ok:
        print('JupyterLab did not answer within 10 minutes; terminating pod %s' % pid)
        gql('mutation { podTerminate(input:{podId:"%s"}) }' % pid); write(dict(event='terminated', pod=pid, at=int(time.time()), why='never answered'))
        sys.exit(1)
    link = url + NB + '?token=' + pw                   # the link carries the password, so one click opens the notebook
    exp = time.strftime('%d %b %Y %H:%M %Z', time.localtime(t0 + hours * 3600))
    draft = ('A sandbox is ready for the Quantum Idle Audit demonstrations.\n\n'
             'Link (opens the notebook directly): %s\nIf asked for a password or token: %s\n\n'
             'It opens a notebook with a finance replay already printed. Select Run > Run All Cells to recompute it, or change DEMO to '
             'chemistry, optimization, simulation, error_correction or ai_kernels. A live run on your own IBM Quantum account is optional and '
             'is switched on in its own cell. No account is needed for the sandbox itself.\n\n'
             'The sandbox is a private container that is deleted on %s, with everything in it. Nothing is sent to Heuremen.\n' % (link, pw, exp))
    print('READY in %.0f s: pod %s, expires %s\n' % (time.time() - t0, pid, exp))
    print(draft)
    if clip == 'link':                                   # 25 Nov: the bare link, for an internal test (draft clipboard got overwritten once)
        subprocess.run(['pbcopy'], input=link, text=True)                # 25 Nov: the clipboard came back empty twice, so also a file and the browser
        f = os.path.expanduser('~/Downloads/qia_sandbox_link.txt'); open(f, 'w').write(link + '\n'); os.chmod(f, 0o600)
        subprocess.run(['open', link]); print('(link on the clipboard, in ~/Downloads/qia_sandbox_link.txt, and opened in the browser)')
    elif clip:
        subprocess.run(['pbcopy'], input=draft, text=True); print('(reply draft on the clipboard)')


def sweep(quiet=False):
    rec = {r['pod']: r for r in records() if r.get('event') == 'created'}
    now = time.time(); n = 0
    for p in pods():
        r = rec.get(p['id'])
        exp = r['expires'] if r else 0                    # a hosted pod with no record is past its expiry by definition
        if now > exp:
            gql('mutation { podTerminate(input:{podId:"%s"}) }' % p['id']); n += 1
            write(dict(event='terminated', pod=p['id'], at=int(now), why='expired' if r else 'no record'))
    if n or not quiet: print('sweep: %d hosted sandbox(es) terminated' % n)


def lst():
    rec = {r['pod']: r for r in records() if r.get('event') == 'created'}
    live = pods()
    if not live: print('no hosted sandboxes live'); return
    for p in live:
        r = rec.get(p['id'], {})
        print('%s %s %s  for %s  age %.1f h  expires in %.1f h' % (p['id'], p['name'], p['desiredStatus'], r.get('who', '?'),
              (time.time() - r.get('created', time.time())) / 3600, (r.get('expires', 0) - time.time()) / 3600))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('grant', 'list', 'sweep'): sys.exit(__doc__)
    if a[0] == 'grant':
        if len(a) < 2: sys.exit('grant needs "<who>"')
        hours = float(a[a.index('--hours') + 1]) if '--hours' in a else 24.0
        grant(a[1], hours, 'link' if '--link' in a else '--clip' in a)
    elif a[0] == 'sweep': sweep('--quiet' in a)
    else: lst()
