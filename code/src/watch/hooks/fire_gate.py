#!/usr/bin/env python3
"""PreToolUse gate on Bash: refuses any demo FIRE (a command running demo*.py --fire*) unless the demo's plan carries
WHO PAYS, STATED, POWER (with a ratio >= 3 written as 'POWER RATIO: <x>'), and SOURCES, and the plan is committed.
the owner, 19 Nov: "why the fuck would you fire on something you didn't check first?" (Pack Q #47, #50, #51)."""
import json, sys, re, os, subprocess, glob
d = json.load(sys.stdin); cmd = (d.get('tool_input') or {}).get('command', '')
m = re.search(r'(?:python\S*|\$PY)\s+(?:\S*/)?(demo[\w]*\.py)\s+--fire', cmd)
if not m: sys.exit(0)
cd = re.findall(r'cd\s+([^\s;&]+)', cmd); folder = os.path.expanduser(cd[-1]) if cd else os.getcwd()
script = m.group(1); v = re.search(r'_(v\d+)', script); tag = v.group(1) if v else ''
plans = [p for p in glob.glob(os.path.join(folder, 'PLAN*.md')) if (tag and tag in p) or (not tag and os.path.basename(p) == 'PLAN.md')]
def refuse(msg):
    import datetime
    q = '~/bones-forge/calibrations/demos/final/REDO_QUEUE.md'
    with open(q, 'a') as f: f.write('- [ ] %s REFUSED %s: %s -> REDESIGN with the next treatment on the ladder, power-check, fire\n' % (datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ'), folder.split('/')[-1], msg.splitlines()[0]))
    print('FIRE GATE REFUSED (%s): %s\nQueued in REDO_QUEUE.md: redesign and re-fire, do not stop.' % (folder, msg), file=sys.stderr); sys.exit(2)
if not plans: refuse('no PLAN%s.md next to %s' % ('_' + tag if tag else '', script))
txt = open(plans[0]).read()
for sec in ('WHO PAYS', 'STATED', 'POWER', 'SOURCES'):
    if sec not in txt.upper(): refuse('plan has no %s section' % sec)
r = re.search(r'POWER RATIO:\s*([0-9.]+)', txt, re.I)
if not r: refuse("plan has no 'POWER RATIO: <expected signal / our repeat floor>' line")
pw = txt.upper().split('POWER',1)[1].split('SOURCES',1)[0]
pilot = re.search(r'--pilot', cmd) is not None
if float(r.group(1)) < 3 and not pilot:
    refuse('POWER RATIO %s < 3. If that number came from a model (ideal circuit, exact algebra, Aer), it cannot drop the treatment: run the hardware pilot (demo --fire --pilot, <= 30 s) and set the ratio from the chip' % r.group(1))
st = subprocess.run(['git', '-C', folder, 'status', '--porcelain', '--', os.path.basename(plans[0]), script], capture_output=True, text=True).stdout.strip()
if st: refuse('plan or script not committed before the fire:\n' + st)
sys.exit(0)
