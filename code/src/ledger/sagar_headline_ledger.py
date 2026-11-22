#!/usr/bin/env python3
"""sagar_headline_ledger.py -- 21 Nov 2026. The ledger row for the live SAGAR headline (the designer's design, the referee's three fixes). Same pattern as sagar_set_ledger.py.

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
ROOT = LG.ROOT; SRC = 'sagar/site/sagar_headline.json'; RID = 'sagar.headline.share-checked'
def checks():
    p = os.path.join(ROOT, 'sagar', 'intake_rows', 'CHECKS.md')
    if not os.path.exists(p): return None, 'no sagar/intake_rows/CHECKS.md: the counts are read by the site builder from the feeder\'s counts file and the reader pipeline\'s state; no check block attached'
    try: return LG.checks_ref('sagar/intake_rows/CHECKS.md'), ''
    except SystemExit as e: return None, 'sagar/intake_rows/CHECKS.md last entry incomplete (%s); no check block attached' % e
def main(dry=False):
    c = json.load(open(os.path.join(ROOT, SRC))); rows = LG.load(); old = rows.get(RID)
    snip = norm(c['sentence'])
    claim = ("SAGAR headline: %.1f%% (%.1f%% to %.1f%%, Wilson 95%%) of papers read in full, through the contact gate, whose codes were all batch-checked or that carried none, "
             "print a number or statement their own tables, figures or arithmetic do not support (posted F5 or F6): %d of %d; set aside: awaiting check %d, held %d; a floor, as of %s"
             % (100 * c['share'], 100 * c['lo'], 100 * c['hi'], c['k'], c['n'], c['awaiting'], c['held'], c['at']))
    new = dict(id=RID, claim=claim, value='%.4f' % c['share'], lo='%.4f' % c['lo'], hi='%.4f' % c['hi'], unit='share of papers checked', outcome='RECORD',
               source=dict(file=SRC, grep='"k": %d,' % c['k']), surfaces=[dict(surface='sagar', text=snip)], status='live')
    if old and old.get('status') == 'live' and old.get('surfaces') == new['surfaces'] and old.get('value') == new['value']:
        print('sagar headline ledger: unchanged (%d of %d)' % (c['k'], c['n'])); return 0
    ck, note = checks(); new['checks'] = ck
    if note: new['checks_note'] = note
    hist = list(old.get('history', [])) if old else []
    hist.append({'at': LG.now(), 'change': 'added' if not old else 'refreshed: %s -> %s' % (old.get('value'), new['value']), 'evidence': SRC, 'by': 'ledger/sagar_headline_ledger.py'})
    new['history'] = hist
    print('sagar headline ledger: %s %s | %s' % ('would write' if dry else 'writing', RID, snip))
    if dry: return 0
    rows[RID] = new; n = LG.save(rows); print('sagar headline ledger: rows written %d' % n); return 0
if __name__ == '__main__': sys.exit(main('--dry-run' in sys.argv))
