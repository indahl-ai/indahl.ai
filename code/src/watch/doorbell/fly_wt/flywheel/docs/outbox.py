#!/usr/bin/env python3
"""The one mail outbox (P4 in PIPELINE_AUDIT.md). Plan skeleton: see OUTBOX_PLAN.md.

Producers never send. They call:
    import outbox
    outbox.enqueue(kind, to, template, data, dedupe_key)      # -> (id, state)

One rider drains it:
    outbox.py drain               # the only code path that sends

Fail closed everywhere: an unknown kind, a missing pace, a template that promises a reply
time, a held kind, a suppressed address, a second notice on a paper, or `live: false`
all mean nothing is sent. A message caught between "sending" and "sent" by a crash is
marked "unknown" and rung, never sent again automatically: a lost mail is recoverable,
a double mail is not.

Stdlib only, 3.9-safe. State lives in $OUTBOX_DIR (default ~/forge/outbox):
    outbox.db       messages, suppressions, receipts (sqlite, WAL)
    kinds.json      per-kind policy: hold, needs_approval, pace, from, templates, rules
    templates/      <name>.txt: "Subject: ..." line, blank line, plain-text body ($vars)
"""
import argparse, fcntl, json, os, re, sqlite3, string, sys, time

DIR = os.path.expanduser(os.environ.get('OUTBOX_DIR', '~/forge/outbox'))
PIPE = os.path.expanduser('~/forge/sagar/pipeline/pipe.log')
MAX_ATTEMPTS = 3
BACKOFF_S = (600, 3600)
STUCK_S = 600
ADDR = re.compile(r'^[^@\s<>,;"]+@[^@\s<>,;"]+\.[A-Za-z]{2,}$')
# No reply-time promises anywhere (site_gate 0b.13, the owner 22 Nov). Checked on every template, at load and at render.
# A time phrase counts only next to a reply word, so data-age wording ("more than 24 h earlier") passes.
_TIME = (r'(within\s+\d+\s*(business\s+|working\s+)?(hours?|days?|weeks?)|\b\d+\s*(h|hrs?|hours?|days?|weeks?)\b'
         r'|\bshortly\b|\bpromptly\b|as\s+soon\s+as\s+possible|\bsame[-\s]day\b|next\s+(business\s+|working\s+)?day)')
_REPLY = (r'(\brepl(y|ies|ied)\b|\brespon(d|ds|se|ses)\b|get\s+back|hear\s+(back|from\s+us)|\banswer|\backnowledg\w*'
          r'|turnaround|be\s+in\s+touch|contact\s+you)')
PROMISE = re.compile(r'(' + _REPLY + r'[^.!?\n]{0,60}' + _TIME + r'|' + _TIME + r'[^.!?\n]{0,60}' + _REPLY +
                     r"|\bwe\s*(will|'ll)\s+(reply|respond|get\s+back|be\s+in\s+touch)|\b(reply|respond)\s+by\b)", re.I)
STATES = ('awaiting_approval', 'held', 'queued', 'sending', 'sent', 'failed', 'unknown', 'suppressed', 'imported')
LIVE_STATES = ('awaiting_approval', 'held', 'queued', 'sending', 'sent', 'unknown', 'imported')   # count for dedupe and one-per-paper


class Refused(Exception):
    """enqueue refused the message. str(e) says why. Nothing was stored."""


def _ring(what):
    try:
        with open(PIPE, 'a') as f:
            f.write(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + ' RING: OUTBOX ' + what.replace('\n', ' ')[:300] + '\n')
    except OSError:
        pass


def db():
    os.makedirs(DIR, exist_ok=True)
    c = sqlite3.connect(os.path.join(DIR, 'outbox.db'), timeout=30, isolation_level=None)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA journal_mode=WAL')
    c.executescript('''
    CREATE TABLE IF NOT EXISTS msg (
      id INTEGER PRIMARY KEY, kind TEXT NOT NULL, to_json TEXT NOT NULL, template TEXT NOT NULL,
      data_json TEXT NOT NULL, dedupe_key TEXT NOT NULL UNIQUE, rule_key TEXT, state TEXT NOT NULL,
      hold_reason TEXT, approved_note TEXT, created REAL NOT NULL, not_before REAL NOT NULL,
      attempts INTEGER NOT NULL DEFAULT 0, last_error TEXT, sent_at REAL);
    CREATE INDEX IF NOT EXISTS msg_rule ON msg(rule_key);
    CREATE INDEX IF NOT EXISTS msg_state ON msg(kind, state, not_before);
    CREATE TABLE IF NOT EXISTS suppress (addr TEXT PRIMARY KEY, reason TEXT NOT NULL, added REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS receipt (msg_id INTEGER NOT NULL, at REAL NOT NULL, result TEXT NOT NULL, provider_id TEXT, detail TEXT);
    ''')
    return c


def kinds():
    with open(os.path.join(DIR, 'kinds.json'), encoding='utf-8') as f:
        return json.load(f)


def policy(kind):
    k = kinds().get('kinds', {}).get(kind)
    if not k:
        raise Refused('unknown kind %r' % kind)
    return k


def load_template(name):
    path = os.path.join(DIR, 'templates', name + '.txt')
    if not re.match(r'^[a-z0-9_]+$', name) or not os.path.isfile(path):
        raise Refused('no template %r' % name)
    text = open(path, encoding='utf-8').read()
    first, _, body = text.partition('\n')
    if not first.startswith('Subject: ') or not body.startswith('\n'):
        raise Refused('template %r must start with a "Subject: " line and a blank line' % name)
    check_text(name, first + body)
    return first[len('Subject: '):].strip(), body[1:]


def check_text(where, text):
    m = PROMISE.search(text)
    if m:
        raise Refused('%s promises a reply time (%r)' % (where, m.group(0)))
    if re.search(r'<\s*(html|body|a|div|p|br)\b', text, re.I):
        raise Refused('%s is not plain text' % where)


def _norm_to(to):
    lst = [to] if isinstance(to, str) else list(to)
    out = []
    for a in lst:
        a = str(a).strip()
        if not ADDR.match(a):
            raise Refused('bad address')
        out.append(a.lower())
    if not out:
        raise Refused('no recipient')
    return sorted(set(out))


def _suppressed(c, addrs):
    for a in addrs:
        if c.execute('SELECT 1 FROM suppress WHERE addr=? OR addr=?', (a, '@' + a.split('@', 1)[1])).fetchone():
            return True
    return False


def _apply_rules(pol, data):
    """Kind rules from kinds.json. Returns rule_key (for one-per-*) or None."""
    rules = pol.get('rules', [])
    rule_key = None
    if 'codes_only' in rules:
        allowed = set(pol.get('fields', []))
        extra = sorted(set(data) - allowed)
        if extra:
            raise Refused('codes_only: fields not allowed: %s' % ','.join(extra))
        codes = data.get('codes')
        table = set(pol.get('codes', []))
        if not table:
            raise Refused('codes_only: no code table in kinds.json')
        if not isinstance(codes, list) or not codes or any(x not in table for x in codes):
            raise Refused('codes_only: codes must be a non-empty list from the code table')
    if 'one_per_paper' in rules:
        pid = str(data.get('paper_id', '')).strip()
        if not pid:
            raise Refused('one_per_paper: paper_id missing')
        rule_key = 'paper:' + pid
    return rule_key


def render(template, data):
    subject, body = load_template(template)
    vals = {k: ('\n'.join(map(str, v)) if isinstance(v, list) else str(v)) for k, v in data.items()}
    try:
        subject = string.Template(subject).substitute(vals)
        body = string.Template(body).substitute(vals)
    except (KeyError, ValueError) as e:
        raise Refused('template %r: missing or bad value %s' % (template, e))
    check_text('rendered ' + template, subject + '\n' + body)
    return subject, body


def enqueue(kind, to, template, data, dedupe_key, not_before=None, hold_reason=None):
    """Store one message. Idempotent on dedupe_key: a repeat returns the existing (id, state).
    Raises Refused (nothing stored) when a rule says no."""
    pol = policy(kind)
    if template not in pol.get('templates', []):
        raise Refused('template %r not allowed for %s' % (template, kind))
    if not isinstance(data, dict) or not dedupe_key:
        raise Refused('data must be a dict and dedupe_key non-empty')
    addrs = _norm_to(to)
    rule_key = _apply_rules(pol, data)
    render(template, data)                      # validate now; rendered again at send time
    c = db()
    c.execute('BEGIN IMMEDIATE')
    try:
        row = c.execute('SELECT id, state FROM msg WHERE dedupe_key=?', (dedupe_key,)).fetchone()
        if row:
            c.execute('COMMIT'); return row['id'], row['state']
        if rule_key and c.execute('SELECT 1 FROM msg WHERE kind=? AND rule_key=? AND state IN (%s)' % ','.join('?' * len(LIVE_STATES)),
                                  (kind, rule_key) + LIVE_STATES).fetchone():
            raise Refused('one_per_paper: %s already has a notice' % rule_key)
        if _suppressed(c, addrs):
            state = 'suppressed'
        elif hold_reason or pol.get('hold'):
            state = 'held'
        elif pol.get('needs_approval', True):
            state = 'awaiting_approval'
        else:
            state = 'queued'
        now = time.time()
        cur = c.execute('INSERT INTO msg (kind,to_json,template,data_json,dedupe_key,rule_key,state,hold_reason,created,not_before) '
                        'VALUES (?,?,?,?,?,?,?,?,?,?)',
                        (kind, json.dumps(addrs), template, json.dumps(data, sort_keys=True), dedupe_key, rule_key, state,
                         hold_reason, now, float(not_before or now)))
        c.execute('COMMIT')
        return cur.lastrowid, state
    except BaseException:
        c.execute('ROLLBACK'); raise


def _pace_ok(c, kind, pace, now):
    if any(pace.get(k) is None for k in ('min_gap_s', 'per_hour', 'per_day')):
        return False, 'pace not set'
    last = c.execute("SELECT MAX(sent_at) FROM msg WHERE kind=? AND state='sent'", (kind,)).fetchone()[0] or 0
    if now - last < pace['min_gap_s']:
        return False, 'min gap'
    hour = c.execute("SELECT COUNT(*) FROM msg WHERE kind=? AND state='sent' AND sent_at>?", (kind, now - 3600)).fetchone()[0]
    day = c.execute("SELECT COUNT(*) FROM msg WHERE kind=? AND state='sent' AND sent_at>?", (kind, now - 86400)).fetchone()[0]
    if hour >= pace['per_hour'] or day >= pace['per_day']:
        return False, 'rate'
    return True, ''


def transport(frm, to, subject, body):
    """Send one mail through the mail token. Returns (ok, provider_id, detail). [confirm the flags with
    `npx wrangler email sending --help` on the Mac before going live; this is the only line that sends.]"""
    sys.path.insert(0, os.path.expanduser('~/forge/lib'))
    import cf
    args = ['email', 'sending', 'send', '--from', frm, '--subject', subject, '--text', body]
    for a in to:
        args += ['--to', a]
    rc, out = cf.wrangler(*args, role='mail', timeout=60)
    m = re.search(r'\b(id|message[_ ]id)\W+([A-Za-z0-9._-]{6,})', out)
    return rc == 0, (m.group(2) if m else None), ('' if rc == 0 else cf._why(out))


def drain(max_per_run=20):
    conf = kinds()
    if not conf.get('live'):
        print('outbox not live (kinds.json "live": false); nothing sent'); return 0
    lock = open(os.path.join(DIR, 'outbox.lock'), 'w')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return 0                                # another drain is running
    c, now, sent = db(), time.time(), 0
    for r in c.execute("SELECT id FROM msg WHERE state='sending' AND not_before<?", (now - STUCK_S,)).fetchall():
        c.execute("UPDATE msg SET state='unknown', last_error='crashed between sending and sent' WHERE id=?", (r['id'],))
        c.execute('INSERT INTO receipt VALUES (?,?,?,?,?)', (r['id'], now, 'unknown', None, 'not resent'))
        _ring('message %d may or may not have gone out; not resent. Check the provider log, then mark it.' % r['id'])
    for kind, pol in conf.get('kinds', {}).items():
        if pol.get('hold'):
            continue
        while sent < max_per_run:
            now = time.time()
            ok, why = _pace_ok(c, kind, pol.get('pace', {}), now)
            if not ok:
                if why == 'pace not set':
                    print('%s: pace not set in kinds.json, skipped' % kind)
                break
            m = c.execute("SELECT * FROM msg WHERE kind=? AND state='queued' AND not_before<=? ORDER BY id LIMIT 1", (kind, now)).fetchone()
            if not m:
                break
            to, data = json.loads(m['to_json']), json.loads(m['data_json'])
            try:
                if _suppressed(c, to):
                    c.execute("UPDATE msg SET state='suppressed' WHERE id=?", (m['id'],)); continue
                subject, body = render(m['template'], data)
                frm = pol.get('from')
                if not frm or not ADDR.match(frm):
                    raise Refused('no valid from address for %s' % kind)
            except Refused as e:
                c.execute("UPDATE msg SET state='failed', last_error=? WHERE id=?", (str(e), m['id']))
                _ring('message %d (%s) refused at send: %s' % (m['id'], kind, e)); continue
            if c.execute("UPDATE msg SET state='sending', not_before=? WHERE id=? AND state='queued'", (now, m['id'])).rowcount != 1:
                continue
            good, pid, detail = transport(frm, to, subject, body)
            t = time.time()
            if good:
                c.execute("UPDATE msg SET state='sent', sent_at=?, attempts=attempts+1 WHERE id=?", (t, m['id']))
                c.execute('INSERT INTO receipt VALUES (?,?,?,?,?)', (m['id'], t, 'sent', pid, ''))
                sent += 1
            else:
                n = m['attempts'] + 1
                c.execute('INSERT INTO receipt VALUES (?,?,?,?,?)', (m['id'], t, 'error', None, detail[:200]))
                if n >= MAX_ATTEMPTS:
                    c.execute("UPDATE msg SET state='failed', attempts=?, last_error=? WHERE id=?", (n, detail[:200], m['id']))
                    _ring('message %d (%s) failed %d times: %s' % (m['id'], kind, n, detail[:120]))
                else:
                    c.execute("UPDATE msg SET state='queued', attempts=?, last_error=?, not_before=? WHERE id=?",
                              (n, detail[:200], t + BACKOFF_S[n - 1], m['id']))
                break                           # a provider error pauses this kind until the next run
    return sent


def _cli():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('drain')
    st = sp.add_parser('status'); st.add_argument('--kind')
    pv = sp.add_parser('preview'); pv.add_argument('id', type=int)
    apv = sp.add_parser('approve'); apv.add_argument('--ids', required=True); apv.add_argument('--note', required=True)
    rel = sp.add_parser('release'); rel.add_argument('--ids', required=True); rel.add_argument('--note', required=True)
    sup = sp.add_parser('suppress'); sup.add_argument('addr'); sup.add_argument('--reason', required=True)
    im = sp.add_parser('import-sent', help='cutover: record notices the old senders already sent, so one_per_paper covers them')
    im.add_argument('kind'); im.add_argument('file', help='one paper_id per line')
    mk = sp.add_parser('mark'); mk.add_argument('id', type=int); mk.add_argument('state', choices=('sent', 'failed')); mk.add_argument('--note', required=True)
    a = ap.parse_args()
    c = db()
    if a.cmd == 'drain':
        print('sent %d' % drain())
    elif a.cmd == 'status':
        q = 'SELECT kind, state, COUNT(*) n FROM msg %s GROUP BY kind, state ORDER BY kind, state' % ('WHERE kind=?' if a.kind else '')
        for r in c.execute(q, (a.kind,) if a.kind else ()):
            print('%-12s %-18s %d' % (r['kind'], r['state'], r['n']))
    elif a.cmd == 'preview':
        m = c.execute('SELECT * FROM msg WHERE id=?', (a.id,)).fetchone()
        s, b = render(m['template'], json.loads(m['data_json']))
        print('Kind: %s  State: %s  To: %d recipient(s)\nSubject: %s\n\n%s' % (m['kind'], m['state'], len(json.loads(m['to_json'])), s, b))
    elif a.cmd in ('approve', 'release'):
        # approve: awaiting_approval -> queued, on the owner's word (the note says whose word and where).
        # release: held -> awaiting_approval (or queued if the kind needs no approval); the kind's hold must already be off.
        ids = [int(x) for x in a.ids.split(',') if x.strip()]
        src = 'awaiting_approval' if a.cmd == 'approve' else 'held'
        done = 0
        for i in ids:
            m = c.execute('SELECT kind, state FROM msg WHERE id=?', (i,)).fetchone()
            if not m or m['state'] != src:
                print('%d: not %s, skipped' % (i, src)); continue
            pol = policy(m['kind'])
            if pol.get('hold'):
                print('%d: kind %s is on hold, skipped' % (i, m['kind'])); continue
            dst = 'queued' if (a.cmd == 'approve' or not pol.get('needs_approval', True)) else 'awaiting_approval'
            c.execute('UPDATE msg SET state=?, approved_note=COALESCE(approved_note || ' | ', '') || ? WHERE id=? AND state=?',
                      (dst, '%s %s: %s' % (a.cmd, time.strftime('%Y-%m-%d'), a.note), i, src))
            done += 1
        print('%s %d' % (a.cmd, done))
    elif a.cmd == 'suppress':
        c.execute('INSERT OR REPLACE INTO suppress VALUES (?,?,?)', (a.addr.strip().lower(), a.reason, time.time()))
        print('suppressed')
    elif a.cmd == 'import-sent':
        n, now = 0, time.time()
        for line in open(a.file, encoding='utf-8'):
            pid = line.strip()
            if pid:
                n += c.execute("INSERT OR IGNORE INTO msg (kind,to_json,template,data_json,dedupe_key,rule_key,state,created,not_before) "
                               "VALUES (?,'[]','imported','{}',?,?,'imported',?,?)",
                               (a.kind, 'import:%s:%s' % (a.kind, pid), 'paper:' + pid, now, now)).rowcount
        print('imported %d' % n)
    elif a.cmd == 'mark':
        # For "unknown" messages only, after a person has checked the provider log.
        n = c.execute("UPDATE msg SET state=?, last_error=? WHERE id=? AND state='unknown'", (a.state, a.note, a.id)).rowcount
        print('marked %d' % n)


if __name__ == '__main__':
    _cli()
