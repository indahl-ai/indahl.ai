#!/usr/bin/env python3
"""flywheel_watch.py (22 Nov 2026, the owner's flywheel). Rides the tick (watch/desk_riders.py, 6-tick tier).
Reads flywheel/SLOTS.json on origin/flywheel (calibrations). For each slot:
- DONE  -> ring the operator to review, append the task to flywheel/DONE.jsonl, refill the slot from BACKLOG.json, push (the push wakes the designer on PR #17).
- question set and no answer -> ring the operator once.
- OPEN and not TAKEN for 30 min -> ring once (the designer asleep).
- TAKEN for 6 h with no new commit on its lane branch -> ring once (stuck).
- a free slot and an empty backlog -> ring once.
Works in its own worktree under ~/forge/watch/doorbell/fly_wt; never touches the main calibrations checkout."""
import json, os, subprocess, sys, time
from datetime import datetime, timezone
REPO = os.environ.get('FLY_REPO') or os.path.expanduser('~/forge/calibrations'); WT = os.environ.get('FLY_WT') or os.path.expanduser('~/forge/watch/doorbell/fly_wt')   # env overrides are for dry tests only
H = os.path.dirname(os.path.abspath(__file__)); STATE = os.environ.get('FLY_STATE') or os.path.join(H, 'flywheel_state.json')
PIPE_LOG = os.environ.get('FLY_LOG') or os.path.expanduser('~/forge/sagar/pipeline/pipe.log')
ID = ['-c', 'user.name=Heuremen LLC', '-c', 'user.email=349448817+indahl-ai@users.noreply.github.com']
def g(*a, cwd=WT): return subprocess.run(['git'] + list(a), cwd=cwd, capture_output=True, text=True, timeout=120)
def log(msg):
    with open(PIPE_LOG, 'a') as f: f.write('%s %s\n' % (time.strftime('%Y-%m-%dT%H:%M:%S'), msg.replace('\n', ' ')[:500]))
def ts(s): return datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
now = datetime.now(timezone.utc); nows = now.strftime('%Y-%m-%dT%H:%M:%SZ')
if not os.path.isdir(WT):
    g('fetch', '-q', 'origin', 'flywheel', cwd=REPO)
    r = g('worktree', 'add', '-q', '--detach', WT, 'origin/flywheel', cwd=REPO)
    if r.returncode: log('RING: FLYWHEEL WATCH FAILED: worktree: ' + r.stderr[-200:]); sys.exit(1)
r = g('fetch', '-q', 'origin', 'flywheel')
if r.returncode: log('RING: FLYWHEEL WATCH FAILED: fetch: ' + r.stderr[-200:]); sys.exit(1)
g('checkout', '-q', '--detach', 'origin/flywheel'); g('reset', '-q', '--hard', 'origin/flywheel')
P = lambda n: os.path.join(WT, 'flywheel', n)
slots = json.load(open(P('SLOTS.json'))); backlog = json.load(open(P('BACKLOG.json')))
st = json.load(open(STATE)) if os.path.exists(STATE) else {}
changed, rang = [], []
def once(key, msg):
    if st.get(key): return
    st[key] = nows; log(msg); rang.append(key)
for s in slots:
    k = '%s:%s' % (s['id'], s['status'])
    if s['status'] == 'DONE':
        log('RING: FLYWHEEL DONE S%d %s: %s | commit %s on %s | %s' % (s['slot'], s['id'], s['title'][:80], s.get('done_commit'), s.get('lane'), (s.get('result') or '')[:160]))
        with open(P('DONE.jsonl'), 'a') as f: f.write(json.dumps(dict(s, reviewed_by_operator=None, closed=nows)) + '\n')
        if s.get('question') and not s.get('answer'):   # 22 Nov: a question on a DONE slot was swallowed by the refill (FW-012); ring it
            log('RING: FLYWHEEL QUESTION (on DONE) S%d %s: %s' % (s['slot'], s['id'], s['question'][:300]))
        ready = [i for i, x in enumerate(backlog) if not x.get('blocked')]   # 22 Nov: a blocked task never takes a slot
        if ready:
            n = backlog.pop(ready[0]); num = s['slot']; s.clear()
            s.update(slot=num, id=n['id'], title=n['title'], lane=n['lane'], brief=n['brief'], status='OPEN', opened=nows,
                     question=None, answer=None, done_commit=None, result=None)
            changed.append('refill S%d %s' % (s['slot'], n['id']))
        else:
            s.update(status='FREE', opened=nows); changed.append('S%d free' % s['slot'])
        continue
    if s.get('question') and not s.get('answer'):
        once('q:%s:%s' % (s['id'], hash(s['question']) & 0xffff), 'RING: FLYWHEEL QUESTION S%d %s: %s' % (s['slot'], s['id'], s['question'][:300]))
    if s['status'] == 'OPEN' and (now - ts(s['opened'])).total_seconds() > 1800:
        once('open:%s' % s['id'], 'RING: FLYWHEEL STALL S%d %s: OPEN %d min, not taken (is the designer awake on PR #17?)' % (s['slot'], s['id'], (now - ts(s['opened'])).total_seconds() / 60))
    if s['status'] == 'TAKEN':
        lc = g('log', '-1', '--format=%cI', 'origin/' + s['lane']).stdout.strip()
        try: last = datetime.fromisoformat(lc).astimezone(timezone.utc)
        except Exception: last = ts(s['opened'])
        if (now - max(last, ts(s.get('taken') or s['opened']))).total_seconds() > 6 * 3600:
            once('stuck:%s' % s['id'], 'RING: FLYWHEEL STUCK S%d %s: TAKEN 6 h, no commit on %s' % (s['slot'], s['id'], s['lane']))
    if s['status'] == 'FREE' and not any(not x.get('blocked') for x in backlog):
        once('empty:%s' % nows[:13], 'RING: FLYWHEEL BACKLOG EMPTY: S%d free; the operator, add tasks to flywheel/BACKLOG.json' % s['slot'])
if changed:
    json.dump(slots, open(P('SLOTS.json'), 'w'), indent=1); json.dump(backlog, open(P('BACKLOG.json'), 'w'), indent=1)
    g('add', 'flywheel'); c = g(*ID, 'commit', '-q', '-m', 'FLYWHEEL REFILL: ' + '; '.join(changed))
    p = g('push', '-q', 'origin', 'HEAD:flywheel')
    if p.returncode and ('rejected' in p.stderr or 'expected' in p.stderr or 'fetch first' in p.stderr):
        # 22 Nov 2026: a hand push by the operator landed between this run's fetch and push (07:42 collision). Not a failure: the next tick
        # starts from the new branch tip and redoes the refill. Say so in pipe.log without ringing, and keep no state from this run.
        log('FLYWHEEL: push raced a newer commit; the next tick redoes the refill'); sys.exit(0)
    if p.returncode: log('RING: FLYWHEEL WATCH FAILED: push: ' + p.stderr[-200:]); sys.exit(1)
    log('FLYWHEEL: ' + '; '.join(changed))
    # 22 Nov 2026: a push to the flywheel branch does not wake the designer's worker (only PR comments and CI do; his word), so the
    # refills sat OPEN 30+ min. Every refill now also posts one comment on PR #17. Prefix 'Flywheel wake:' so ack_watch ignores it.
    w = subprocess.run(['/opt/homebrew/bin/gh', 'pr', 'comment', '17', '-R', 'indahl-ai/calibrations', '--body',
                        'Flywheel wake: ' + '; '.join(changed) + '. Slots: ' + ', '.join('S%d %s %s' % (x['slot'], x['id'], x['status']) for x in slots)],
                       capture_output=True, text=True, timeout=60)
    if w.returncode: log('RING: FLYWHEEL WAKE FAILED (refill pushed, the designer not woken): ' + (w.stderr or '')[-200:])
json.dump(st, open(STATE + '.tmp', 'w')); os.replace(STATE + '.tmp', STATE)
print('flywheel_watch: %s | changed: %s | rang: %d' % (' '.join('S%d=%s:%s' % (s['slot'], s['id'], s['status']) for s in slots), changed or 'none', len(rang)))
