"""desk/1 contract check, shared by desk_publish.py (before a put) and desk_doctor.py (after).

One definition, so the gate and the checker can't disagree. Stdlib only and 3.9-safe, because
desk_doctor runs inside alerts_check.py on the tick bus (/usr/bin/python3).

    problems = check(doc, want_id)    # [] means the doc is valid
    h = doc_hash(doc)                 # the value doc["hash"] must hold
"""
import hashlib, json, re
from datetime import datetime

OUTCOMES = {'ABOVE', 'BELOW', 'CONSISTENT', 'CANNOT_TELL'}
STATUSES = {'live', 'building', 'plumbing'}
REQUIRED = ('schema', 'id', 'title', 'status', 'updated', 'headline', 'outcome', 'tally', 'sources', 'hash')
SHA256 = re.compile(r'^[0-9a-f]{64}$')
TALLY = ('returned', 'nothing_returned', 'refused', 'held')


def doc_hash(doc):
    body = {k: v for k, v in doc.items() if k != 'hash'}
    raw = json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _str(v):
    return isinstance(v, str) and v.strip() != ''


def _https(v):
    return isinstance(v, str) and v.startswith('https://') and not any(c in v for c in ' "<>\'\n')


def parse_time(v):
    if not isinstance(v, str):
        return None
    try:
        return datetime.fromisoformat(v.replace('Z', '+00:00'))
    except ValueError:
        return None


def check(doc, want_id):
    p = []
    if not isinstance(doc, dict):
        return ['not an object']
    for k in REQUIRED:
        if k not in doc:
            p.append('missing ' + k)
    if p:
        return p
    if doc['schema'] != 'desk/1':
        p.append('schema is not desk/1')
    if doc['id'] != want_id:
        p.append('id does not match key')
    if not _str(doc['title']):
        p.append('title empty')
    if doc['status'] not in STATUSES:
        p.append('status not live/building/plumbing')
    t = parse_time(doc['updated'])
    if t is None or t.tzinfo is None:
        p.append('updated not an ISO time with zone')
    h = doc['headline']
    if not isinstance(h, dict) or not _str(h.get('text')):
        p.append('headline.text empty')
    elif h.get('value') is not None and not _num(h['value']):
        p.append('headline.value not a number')
    if doc['outcome'] not in OUTCOMES:
        p.append('outcome not one of the four')
    ta = doc['tally']
    if not isinstance(ta, dict) or any(not isinstance(ta.get(k), int) or isinstance(ta.get(k), bool) or ta.get(k) < 0 for k in TALLY):
        p.append('tally needs four counts >= 0')
    if not isinstance(doc['sources'], list):
        p.append('sources not a list')
    else:
        ids = set()
        for s in doc['sources']:
            if not isinstance(s, dict) or not _str(s.get('id')) or not _str(s.get('title')) or not _https(s.get('url')):
                p.append('a source lacks id, title or an https url'); break
            ids.add(s['id'])
        c = doc.get('claim')
        if isinstance(c, dict) and c.get('source') not in ids:
            p.append('claim.source not in sources')
    for k in ('measured',):
        m = doc.get(k)
        if m is not None and (not isinstance(m, dict) or (m.get('value') is not None and not _num(m.get('value')))):
            p.append(k + '.value not a number')
    iv = doc.get('interval')
    if iv is not None:
        if not isinstance(iv, dict) or not all(_num(iv.get(k)) for k in ('low', 'high', 'level')):
            p.append('interval low/high/level not numbers')
        elif iv['low'] > iv['high']:
            p.append('interval low > high')
        if isinstance(iv, dict) and iv.get('n') is not None and (not isinstance(iv['n'], int) or isinstance(iv['n'], bool)):
            p.append('interval.n not an integer')
    for k in ('kit', 'plan'):
        v = doc.get(k)
        if v is not None and (not isinstance(v, dict) or not _https(v.get('url')) or not SHA256.match(str(v.get('sha256', '')))):
            p.append(k + ' needs an https url and a sha256')
    for f in doc.get('footnotes') or []:
        if not isinstance(f, dict) or not isinstance(f.get('n'), int) or not _str(f.get('text')):
            p.append('a footnote lacks n or text'); break
    for b in doc.get('blocks') or []:
        if not isinstance(b, dict) or b.get('type') not in ('table', 'note'):
            p.append('a block type is not table or note'); break
        if b['type'] == 'note' and not _str(b.get('text')):
            p.append('a note block has no text'); break
        if b['type'] == 'table':
            head, rows = b.get('head'), b.get('rows')
            if not isinstance(head, list) or not isinstance(rows, list) or any(not isinstance(r, list) or len(r) != len(head) for r in rows):
                p.append('a table block is ragged'); break
    if not SHA256.match(str(doc['hash'])) or doc['hash'] != doc_hash(doc):
        p.append('hash does not match the document')
    return p
