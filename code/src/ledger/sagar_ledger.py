#!/usr/bin/env python3
"""sagar_ledger.py -- 17 Nov 2026, the owner: consistency site-wide; removal automated in the page builders.
The SAGAR desk writes its own ledger rows, the way the automated desks do (linkrot_index/early/ship_samples.py). make_sagar.py calls this
after it writes sagar_rows.json, so the ledger moves with the record and before the surface (build_site.py) does.

  python3 sagar_ledger.py            sync: add a row for every listed SAGAR row, refresh a row whose printed text changed, withdraw a row
                                     no longer listed (through ledger.py withdraw, with evidence and test; nothing is deleted)
  python3 sagar_ledger.py --dry-run  print what a sync would do, write nothing

One row per listed paper: id sagar.<arxiv>.<codes joined by ->, outcome RECORD (what the paper prints against what it shows elsewhere,
classified for indexing), source sagar/site/sagar_rows.json with a grep anchor that holds the paper's arXiv id and its codes, and two surfaces:
  sagar        the list row on indahl-ai/sagar.html: "<title> Study page <codes> <tier>"
  sagar_study  the Work line on its study page:      "<title> arXiv <id>, published <month year>"
Snippets are normalised with check_ledger.norm, so what is written is what the drift gate compares.
Check block: if sagar/CHECKS.md exists and its last entry is complete (watch/readcheck.py), each new row carries it; otherwise the row
records checks: null and says so in checks_note (a check block is attested by whoever ran the reading, never written by this script)."""
import html, json, os, re, shutil, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ledger as LG
from check_ledger import norm
from removed_ids import load as load_removed

ROOT = LG.ROOT
SRC = 'sagar/site/sagar_rows.json'
REMOVED_FILE = 'indahl-ai/removed_by_author.json'
E = html.escape


def rid(r): return 'sagar.%s.%s' % (r['arxiv'], r['code'].replace(' ', '-'))
def grep(r): return '"arxiv": "%s",\n  "code": "%s",' % (r['arxiv'], r['code'])
def _stored(t):   # check_ledger normalises the stored text again; a title that prints a literal tag (raw MathML) is kept escaped so it survives that
    return t if norm(t) == t else E(t, quote=False)
def list_snip(r):   # the row as build_site.py prints it on /sagar (title cell + its Study page link, the code links, the tier link)
    return _stored(norm('<a>%s</a><br><span class="by"><a>Study page</a></span></td><td>%s<a>%s</a></td>' % (E(r['title']), ''.join('<a>%s</a> ' % c for c in r['code'].split()), r['tier'])))
def study_snip(r):   # the first cell of the study page (make_sagar.py c1)
    return _stored(norm('<a>%s</a><br><span class="by">arXiv %s, %s %s</span>' % (E(r['title']), r['arxiv'], r.get('pubword', 'published'), E(r['pub']))))   # 21 Nov 2026: rows of the arXiv 2025 set say "posted" (an arXiv listing date is not publication); every other row keeps "published"
def claim(r):
    return 'SAGAR lists arXiv %s (%s) with claim codes %s, tier %s: where the paper prints one thing and shows another, classified for indexing' % (r['arxiv'], r['title'][:120], r['code'], r['tier'])


def checks():
    p = os.path.join(ROOT, 'sagar', 'CHECKS.md')
    if not os.path.exists(p): return None, 'no sagar/CHECKS.md: the reading is the SAGAR record (two readers, verified.jsonl, second_reader.jsonl); no check block attached'
    try: return LG.checks_ref('sagar/CHECKS.md'), ''
    except SystemExit as e: return None, 'sagar/CHECKS.md last entry incomplete (%s); no check block attached' % e


def sync(dry=False):
    listed = json.load(open(os.path.join(ROOT, SRC), encoding='utf-8'))
    src_text = open(os.path.join(ROOT, SRC), encoding='utf-8').read()
    removed = set(load_removed())
    rows = LG.load(); now = LG.now()
    want = {rid(r): r for r in listed}
    have = {k: v for k, v in rows.items() if k.startswith('sagar.')}
    listed_ids = {r['arxiv'] for r in listed}
    add, upd, relist, out = [], [], [], []
    ck, ck_note = checks()
    for k, r in want.items():
        assert src_text.count(grep(r)) == 1, 'grep anchor not unique in %s: %s' % (SRC, k)
        surf = [dict(surface='sagar', text=list_snip(r)), dict(surface='sagar_study', text=study_snip(r))]
        if k not in have:
            add.append(k)
            rows[k] = dict(checks=ck, id=k, claim=claim(r), value=r['code'], lo=None, hi=None, unit='claim codes (tier %s)' % r['tier'], outcome='RECORD',
                           source=dict(file=SRC, grep=grep(r)), surfaces=surf, status='live', kind='sagar_row', desk='sagar', tier=r['tier'],
                           history=[dict(at=now, change='added', evidence=SRC, by='ledger/sagar_ledger.py')])
            if ck_note: rows[k]['checks_note'] = ck_note
            continue
        x = rows[k]
        if x['status'] != 'live':   # listed again after a withdrawal (a removal reversed, or codes back as before)
            relist.append(k); x['status'] = 'live'
            x['history'].append(dict(at=now, change='listed again: back in %s' % SRC, evidence=SRC, by='ledger/sagar_ledger.py'))
        ch = []
        if x['surfaces'] != surf: ch.append('surface text'); x['surfaces'] = surf
        if x.get('tier') != r['tier']: ch.append('tier %s -> %s' % (x.get('tier'), r['tier'])); x['tier'] = r['tier']; x['unit'] = 'claim codes (tier %s)' % r['tier']
        if x['claim'] != claim(r): ch.append('claim'); x['claim'] = claim(r)
        if x['source'] != dict(file=SRC, grep=grep(r)): ch.append('source'); x['source'] = dict(file=SRC, grep=grep(r))
        if ch:
            upd.append(k); x['history'].append(dict(at=now, change='refreshed from %s: %s' % (SRC, ', '.join(ch)), evidence=SRC, by='ledger/sagar_ledger.py'))
    for k, x in have.items():
        if k in want or x['status'] in ('withdrawn', 'superseded'): continue
        out.append(k)
    print('sagar_ledger: %d listed, %d rows in the ledger; add %d, refresh %d, listed again %d, withdraw %d%s'
          % (len(want), len(have), len(add), len(upd), len(relist), len(out), ' (dry run, nothing written)' if dry else ''))
    for tag, ks in (('add', add), ('refresh', upd), ('relist', relist), ('withdraw', out)):
        for k in ks[:12]: print('  %-8s %s' % (tag, k))
        if len(ks) > 12: print('  %-8s ... %d more' % (tag, len(ks) - 12))
    if dry or not (add or upd or relist or out): return 0
    bak = os.path.join(HERE, 'ledger.jsonl.bak-%s-sagarledger' % time.strftime('%Y%m%d'))
    if not os.path.exists(bak): shutil.copy2(LG.LEDGER, bak)
    if add or upd or relist: LG.save(rows)
    env = dict(os.environ, FORGE_ROOT=ROOT)
    for k in out:   # through ledger.py's own withdraw path: evidence that exists and the test that was run
        a = k.split('.', 1)[1].rsplit('.', 1)[0]; codes = k.rsplit('.', 1)[1].replace('-', ' ')
        if a in removed:
            why, ev, test = 'removed from SAGAR at the author\'s request (%s)' % REMOVED_FILE, REMOVED_FILE, 'removed_gate passes after rebuild'
        elif a in listed_ids:
            why, ev, test = 'arXiv %s is listed with different codes now; this row\'s codes (%s) are no longer listed' % (a, codes), SRC, 'make_sagar.py rebuilt %s; arXiv %s is listed without codes %s' % (SRC, a, codes)
            # the paper is still listed, so its study page still prints the Work line: take that surface off before the withdrawal (no false ZOMBIE)
            subprocess.run([sys.executable, os.path.join(HERE, 'ledger.py'), 'off', k, 'sagar_study', '--why', 'the paper is still listed under a new row'], check=True, env=env, stdout=subprocess.DEVNULL)
        else:
            why, ev, test = 'arXiv %s is no longer listed in %s' % (a, SRC), SRC, 'make_sagar.py rebuilt %s; arXiv %s is not in it' % (SRC, a)
        subprocess.run([sys.executable, os.path.join(HERE, 'ledger.py'), 'withdraw', k, '--why', why, '--evidence', ev, '--test', test], check=True, env=env, stdout=subprocess.DEVNULL)
    stale = [a for a in {k.split('.', 1)[1].rsplit('.', 1)[0] for k in out} if a not in listed_ids and os.path.exists(os.path.join(ROOT, 'indahl-ai', 'sagar', 'study', a + '.html'))]
    if stale: print('  note: study pages left behind for papers no longer listed (build_site.py does not delete them; ledger/remove.py does): ' + ', '.join(sorted(stale)))
    return 0


if __name__ == '__main__':
    sys.exit(sync('--dry-run' in sys.argv))
