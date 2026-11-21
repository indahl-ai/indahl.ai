"""test_two_writers.py (21 Nov 2026): the ledger's save under two writers. It NEVER touches the live ledger: it copies ledger.py,
the old ledger.py (ledger.py.bak-20261121-onewriter) and ledger.jsonl into a fresh temporary folder and runs there.
  python3 test_two_writers.py        nine cases; exit 0 only if all pass. Case T7 runs the OLD save and must show lost updates.
Why: on 21 Nov 2026 at 00:12:07Z a ship's QUAKE refresh and the live-headline rider saved the ledger in the same seconds under two
different locks; the refresh's 23 rows were lost, its "23 rows refreshed" line was false, and every ship after it was refused."""
import os, shutil, subprocess, sys, tempfile
if os.environ.get('LEDGER_TEST_IN_COPY') != '1':
    H = os.path.dirname(os.path.abspath(__file__)); D = tempfile.mkdtemp(prefix='ledger_two_writers_')
    shutil.copy(H + '/ledger.py', D + '/ledger.py'); shutil.copy(H + '/ledger.py.bak-20261121-onewriter', D + '/ledger_old.py')
    shutil.copy(H + '/ledger.jsonl', D + '/ledger.jsonl'); shutil.copy(os.path.abspath(__file__), D + '/test_two_writers.py')
    rc = subprocess.run([sys.executable, D + '/test_two_writers.py'], env=dict(os.environ, LEDGER_TEST_IN_COPY='1')).returncode
    shutil.rmtree(D, ignore_errors=True); sys.exit(rc)
import hashlib, importlib.util, json, os, subprocess, sys, time
T = os.path.dirname(os.path.abspath(__file__))
def mod():
    sp = importlib.util.spec_from_file_location('ledger_copy_%d' % time.time_ns(), T + '/ledger.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
res = []
def ok(tag, cond, note=''): res.append(cond); print('%-58s %s %s' % (tag, 'PASS' if cond else 'FAIL', note))
A, B = mod(), mod(); assert A.LEDGER == T + '/ledger.jsonl'
# T1 a round trip with no change leaves the file byte for byte as it was
h0 = sha(A.LEDGER); r = A.load(); n = A.save(r); ok('T1 load and save with no change: file unchanged', sha(A.LEDGER) == h0 and n == 0, '(%d rows)' % len(r))
ids = sorted(k for k in r if k.startswith('quake.prob'))[:3] + sorted(k for k in r if k.startswith('live.campus'))[:1]; q1, q2, q3, c1 = ids
# T2 the 00:12Z case: A (the refresh) and B (the rider) both load, A saves quake rows, B saves a campus row and adds one
ra = A.load(); rb = B.load()
ra[q1]['unit'] = 'TEST-A1'; ra[q2]['unit'] = 'TEST-A2'; A.save(ra)
rb[c1]['unit'] = 'TEST-B'; rb['zz.test.new'] = dict(rb[c1], id='zz.test.new'); B.save(rb)
f = A._read(); ok('T2 two writers, different rows: both kept', f[q1]['unit'] == 'TEST-A1' and f[q2]['unit'] == 'TEST-A2' and f[c1]['unit'] == 'TEST-B' and 'zz.test.new' in f)
# T3 both change the same row: the second is refused and nothing of its is written
ra = A.load(); rb = B.load(); ra[q3]['unit'] = 'TEST-A3'; A.save(ra); rb[q3]['unit'] = 'TEST-B3'; rb[q1]['unit'] = 'TEST-B1'; h = sha(A.LEDGER)
try: B.save(rb); refused = False
except SystemExit as e: refused = 'REFUSED' in str(e)
ok('T3 same row changed by both: second save refused, file untouched', refused and sha(A.LEDGER) == h and A._read()[q3]['unit'] == 'TEST-A3')
# T4 a writer that saves twice does not undo another writer's change in between
ra = A.load(); ra[q1]['unit'] = 'TEST-A4'; A.save(ra); rb = B.load(); rb[q2]['unit'] = 'TEST-B4'; B.save(rb); ra[q3]['unit'] = 'TEST-A5'; A.save(ra)
f = A._read(); ok('T4 second save by one writer keeps the other writer\'s change', f[q2]['unit'] == 'TEST-B4' and f[q3]['unit'] == 'TEST-A5' and f[q1]['unit'] == 'TEST-A4')
# T5 a deletion and an addition by different writers
ra = A.load(); rb = B.load(); del ra['zz.test.new']; A.save(ra); rb['zz.test.two'] = dict(rb[c1], id='zz.test.two'); B.save(rb)
f = A._read(); ok('T5 one deletes a row, the other adds one: both hold', 'zz.test.new' not in f and 'zz.test.two' in f)
# T9 one writer deletes a row the other has just changed: refused like any conflict (the referee, 21 Nov 02:02Z)
ra = A.load(); rb = B.load(); ra[q1]['unit'] = 'TEST-A9'; A.save(ra); del rb[q1]; h = sha(A.LEDGER)
try: B.save(rb); refused = False
except SystemExit as e: refused = 'REFUSED' in str(e)
ok('T9 one deletes a row the other just changed: refused, file untouched', refused and sha(A.LEDGER) == h and A._read()[q1]['unit'] == 'TEST-A9')
# T6 two real processes, 25 rounds each, each bumping its own row with a pause between load and save
w = '''
import importlib.util, sys, time, random
sp = importlib.util.spec_from_file_location('lc', sys.argv[1] + '/ledger.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
for i in range(25):
    r = m.load(); time.sleep(random.random() * 0.05); r[sys.argv[2]]['value'] = str(int(r[sys.argv[2]].get('value') if str(r[sys.argv[2]].get('value')).isdigit() else 0) + 1); m.save(r)
'''
open(T + '/w.py', 'w').write(w); r = A.load(); r[q1]['value'] = '0'; r[q2]['value'] = '0'; A.save(r)
ps = [subprocess.Popen([sys.executable, T + '/w.py', T, q]) for q in (q1, q2)]; [p.wait(timeout=120) for p in ps]
f = A._read(); ok('T6 two processes, 25 saves each on their own row: none lost', f[q1]['value'] == '25' and f[q2]['value'] == '25', '(%s and %s)' % (f[q1]['value'], f[q2]['value']))
# T7 the same test with the OLD save shows the fault (so the test can fail)
old = open(T + '/ledger_old.py').read(); open(T + '/w_old.py', 'w').write(w.replace("'/ledger.py'", "'/ledger_old.py'"))
r = A.load(); r[q1]['value'] = '0'; r[q2]['value'] = '0'; A.save(r)
ps = [subprocess.Popen([sys.executable, T + '/w_old.py', T, q]) for q in (q1, q2)]; [p.wait(timeout=120) for p in ps]
f = A._read(); ok('T7 the old save under the same test LOSES updates (the test can fail)', not (f[q1]['value'] == '25' and f[q2]['value'] == '25'), '(%s and %s of 25)' % (f[q1]['value'], f[q2]['value']))
# T8 every line of the file is still one JSON row, sorted by id
L = [l for l in open(A.LEDGER) if l.strip()]; idl = [json.loads(l)['id'] for l in L]; ok('T8 file still one row a line, sorted by id', idl == sorted(idl))
print('ALL PASS' if all(res) else 'SOME FAILED'); sys.exit(0 if all(res) else 1)
