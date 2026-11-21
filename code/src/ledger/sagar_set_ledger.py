#!/usr/bin/env python3
"""sagar_set_ledger.py -- 21 Nov 2026. The ledger row for the moving counts of SAGAR's third set, "arXiv 2025, text on hand".

The set's paragraph on /sagar prints how many papers have been read and how many were set aside unread. Those counts move with every
batch the readers finish, and a public number goes to the ledger before the page. sagar/site/make_sagar.py writes the numbers it printed
(and the exact sentence that carries them) to sagar/site/arm2_counts.json, then calls this, the way it calls sagar_ledger.py for the rows.

One row, id sagarset.arxiv-2025-text-on-hand, outcome RECORD:
  source   sagar/site/arm2_counts.json, with a grep anchor on the read count
  surface  sagar: the sentence "<T> papers are in the set so far; <N> have been read; <M> were set aside unread; the rest wait in that order",
           normalised with check_ledger.norm, so what is written is what the drift gate compares
It is added the first time, and refreshed (with a history entry naming the old and new counts) whenever the sentence changes.
Written through ledger.save (one lock, merge, refuse a conflict). Check block: sagar/intake_rows/CHECKS.md if its last entry is complete
(watch/readcheck.py); otherwise the row records checks: null and says so in checks_note.

  python3 sagar_set_ledger.py [--dry-run]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ledger as LG
from check_ledger import norm
ROOT = LG.ROOT; SRC = 'sagar/site/arm2_counts.json'; RID = 'sagarset.arxiv-2025-text-on-hand'
def checks():
    p = os.path.join(ROOT, 'sagar', 'intake_rows', 'CHECKS.md')
    if not os.path.exists(p): return None, 'no sagar/intake_rows/CHECKS.md: the counts are read by the site builder from the feeder\'s counts file and the reader pipeline\'s state; no check block attached'
    try: return LG.checks_ref('sagar/intake_rows/CHECKS.md'), ''
    except SystemExit as e: return None, 'sagar/intake_rows/CHECKS.md last entry incomplete (%s); no check block attached' % e
def main(dry=False):
    c = json.load(open(os.path.join(ROOT, SRC))); rows = LG.load(); old = rows.get(RID)
    snip = norm(c['sentence']); claim = ("SAGAR's set \"arXiv 2025, text on hand\": %d papers in the set so far; %d read by a first reader and then a second reader, in an order fixed before reading; %d set aside unread "
                                          "(%d because they name Gaia or a third data release, %d by a rule fixed on each paper's identifier), as of %s" % (c['in_set'], c['read'], c['set_aside'], c['gaia_or_third_release'], c['by_identifier_rule'], c['at']))
    new = dict(id=RID, claim=claim, value=str(c['read']), lo=None, hi=None, unit='papers read (%d set aside unread)' % c['set_aside'], outcome='RECORD',
               source=dict(file=SRC, grep='"read": %d,' % c['read']), surfaces=[dict(surface='sagar', text=snip)], status='live')
    if old and old.get('status') == 'live' and old.get('surfaces') == new['surfaces'] and old.get('claim', '').split(', as of ')[0] == claim.split(', as of ')[0]:
        print('sagar set ledger: unchanged (%d read, %d set aside)' % (c['read'], c['set_aside'])); return 0
    ck, note = checks(); new['checks'] = ck
    if note: new['checks_note'] = note
    hist = list(old.get('history', [])) if old else []
    hist.append({'at': LG.now(), 'change': 'added' if not old else 'refreshed: %s -> %s read, unit was "%s"' % (old.get('value'), new['value'], old.get('unit')), 'evidence': SRC, 'by': 'ledger/sagar_set_ledger.py'})
    new['history'] = hist
    print('sagar set ledger: %s %s | %s' % ('would write' if dry else 'writing', RID, snip))
    if dry: return 0
    rows[RID] = new; n = LG.save(rows); print('sagar set ledger: rows written %d' % n); return 0
if __name__ == '__main__': sys.exit(main('--dry-run' in sys.argv))
