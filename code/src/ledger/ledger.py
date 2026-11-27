#!/usr/bin/env python3
"""The ledger: one row per public claim or number. The ledger is the state; surfaces follow it.

  ledger.py list [--status live|withdrawn|cannot_tell] [--surface KEY]
  ledger.py show ID
  ledger.py add ID --claim TEXT --value V [--lo L --hi H] [--unit U] --outcome O --source FILE --grep TEXT
                   --on SURFACE "exact snippet" [--on SURFACE "snippet" ...]
  ledger.py set ID --field F --to VALUE --why TEXT --evidence PATH
  ledger.py on ID SURFACE "exact snippet"          (record one more place the claim is printed)
  ledger.py off ID SURFACE --why TEXT              (claim no longer printed on that surface; the row stays)
  ledger.py withdraw ID --why TEXT --evidence PATH --test TEXT
  ledger.py cannot_tell ID --why TEXT
  (10 Nov 2026) kind 'live_headline' rows and their 'live_value' rows are written by ledger/live_headlines.py, not by hand. A superseded value row stays.

Rules the script enforces:
  - a withdrawal needs the evidence that killed the claim (a file that exists) AND the test that was run;
    without both it is refused, and the row can only go to cannot_tell (an untested cut is never a deletion)
  - nothing is deleted: every change appends to the row's history with the time, the change and its evidence
  - outcomes are the four: ABOVE, BELOW, CONSISTENT, CANNOT_TELL (or LEVEL for a value read as a level, COUNT for a count,
    RECORD for what a vendor record shows)
"""
import json, os, sys, argparse, datetime as D

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, 'ledger.jsonl')
OUTCOMES = {'ABOVE', 'BELOW', 'CONSISTENT', 'CANNOT_TELL', 'LEVEL', 'COUNT', 'RECORD'}
SURFACES = {  # surface key -> file (paths relative to ~/forge unless absolute)
    'paper': 'arxiv_one_readout/main.tex',
    'abstract': '~/Desktop/Sink /ARXIV_ABSTRACT_SHORT.txt',
    'bill': 'indahl-ai/qia_template/QIA-2026-001.json',
    'indahl': 'indahl-ai/build_site.py',   # 23 Oct: the indahl.ai pages are generated from this file
    'messages': '~/Desktop/Sink /ENDORSE_MESSAGES_FINAL_DRAFT.txt',
    'zenodo': '~/Desktop/Sink /ZENODO_v6_FORM.txt',   # 30 Oct: the live record is version 6
    'faults': 'ligera/FAULTS.html',
    'guards': 'ligera/GUARDS.html',
    'iris_paper': 'iris_index/pub2/paper/main.tex',   # 25 Oct: Pub #2 (IRIS)
    'oy_matrix': 'indahl-ai/oy.html',
    'qia_cal_js': 'cloudflare-workers/heuremen-door/public/qia/cal.js',   # 30 Oct site pass B-30: the live panels' fixed sentences
    'qia_ibm_js': 'cloudflare-workers/heuremen-door/public/qia/ibm.js',
    'qia_t1t2_js': 'cloudflare-workers/heuremen-door/public/qia/t1t2.js',
    'qia_stability_js': 'cloudflare-workers/heuremen-door/public/qia/stability.js',
    'qia_offchain_js': 'cloudflare-workers/heuremen-door/public/qia/offchain.js',
    'atlas': 'indahl-ai/atlas.html',   # 27 Oct: ATLAS data center map (generated from atlas/)
    'atlas_pn': 'indahl-ai/atlas/planned-plants.html',   # 28 Oct: ATLAS planned power plants (generated from atlas/electricity/planned*)
    'atlas_cb': 'indahl-ai/atlas/carbon.html',   # 28 Oct: ATLAS carbon (generated from atlas/electricity/carbon*)
    'atlas_pl': 'indahl-ai/atlas/power-plants.html',   # 28 Oct: ATLAS power plants (generated from atlas/electricity/plants*)
    'atlas_el': 'indahl-ai/atlas/electricity.html',   # 28 Oct: ATLAS electricity (generated from atlas/electricity/)
    'web': 'indahl-ai/web.html',   # 28 Oct: WEB, pages that returned a wall (generated from oy_index/web_walls.json)
    'sad': 'indahl-ai/model_all.html',   # 28 Oct: the MODEL desk of HERMES (formerly SAD). The surface key stays sad: it is internal to the ledger. Generated from mlperf_index/
    'media_old': 'indahl-ai/media/2026-10-26.html',   # 29 Oct 2026: the 26 Oct release, archived
    'media_oct29': 'indahl-ai/media/2026-10-29.html',   # 27 Nov 2026: the 29 Oct release, archived when the QIA launch release took /media
    'media': 'indahl-ai/media.html',   # 26 Oct 2026: the press release lives on indahl.ai (heuremen.org links to it)
    'qia_matrix': 'indahl-ai/qia.html',
    'qia_process': 'indahl-ai/qia/process.html',
    'qia_corp': 'indahl-ai/qia/studies/corporate.html',   # 15 Nov 2026: calibrated studies moved off /qia
    'qia_research': 'indahl-ai/qia/studies/research.html',   # 15 Nov 2026: how each QIA reading is made, moved off the QIA page by his word   # 25 Oct: Recount Matrix: Quantum Hardware (generated from qia_leads/matrix_page)
    'model_live': 'iris_index/claims_stack/status_model_live.json',   # 30 Oct: MODEL desk claims rounds (S1-S3), the file put in KV model_live
    'darkwave': 'indahl-ai/darkwave.html',   # 20 Nov 2026: the Darkwave page moved to indahl.ai (the owner)   # 16 Nov: moved back to heuremen.org (his word);   # 1 Nov: the Darkwave page (paper + clock)
    'yo': 'indahl-ai/yo.html',   # 9 Nov: the YO desk (his word); every YO number moved here from iris_lab
    'water': 'indahl-ai/water.html',   # 10 Nov: the WATER desk (ATLAS); its headline is built into the page from watch/headlines.json, the live panel reads /water/live.json
    'wiki': 'indahl-ai/wiki.html',   # 10 Nov: the WIKI desk (HERMES); one reading per page, headline built with it, the feed /wiki/live.json reads again weekly
    'social': 'indahl-ai/social.html',   # 10 Nov: the SOCIAL desk (HERMES); built by social_index/build_social.py from the section files, headline built with it
    'downloads': 'indahl-ai/downloads.html',   # 13 Nov: GRAB AND GO, every pack with its size (moved here from the division pages)
    'hermes': 'indahl-ai/hermes.html',   # 10 Nov: the HERMES menu page, which carries the grab-and-go list of HERMES desk packs and their sizes
    'atlas_pack': 'indahl-ai/atlas/data-pack.html',   # 10 Nov (cold read BLOCK 1): the data-pack pages print the built README's counts
    'oy_pack': 'indahl-ai/oy/data-pack.html',
    'model_pack': 'indahl-ai/hermes/model/data-pack.html',
    # 10 Nov 2026 (cold read row 12): the live desks whose headline moves on every read. One 'live_headline' row each (ledger/live_headlines.py)
    # records the page's question heading here, and the feed field, cadence and change rule in the row. Value rows are written on a material change.
    'desk_airq': 'indahl-ai/airq.html',
    'desk_hosts': 'indahl-ai/hosts.html',
    'desk_trials': 'indahl-ai/trials.html',
    'desk_hpt': 'indahl-ai/hpt.html',
    'desk_support': 'indahl-ai/support.html',
    'desk_fedsep': 'indahl-ai/fedsep.html',
    'desk_airline': 'indahl-ai/airline.html',
    'desk_ailuminate': 'indahl-ai/ailuminate.html',
    'desk_weights': 'indahl-ai/weights.html',
    'desk_campus': 'indahl-ai/campus.html',
    'desk_secrecords': 'indahl-ai/secrecords.html',
    'desk_hfsize': 'indahl-ai/hfsize.html',
    'desk_hflicense': 'indahl-ai/hflicense.html',   # 21 Nov 2026: live_headline row for the HFLICENSE card
    'desk_social': 'indahl-ai/social.html',   # 21 Nov 2026: live_headline row for the SOCIAL card
    'desk_pkglicense': 'indahl-ai/pkglicense.html',
    'desk_pkginstall': 'indahl-ai/pkginstall.html',
    'desk_revise': 'indahl-ai/revise.html',
    'desk_change': 'indahl-ai/change.html',
    'desk_cadence': 'indahl-ai/cadence.html',
    'desk_linkrot': 'indahl-ai/linkrot.html',
    'desk_launch': 'indahl-ai/launch.html',
    'desk_tape': 'indahl-ai/tape.html',
    'desk_solar': 'indahl-ai/solar.html',   # 10 Nov 2026: the SOLAR desk (ATLAS); page body from solar_index/solar.html, headline from watch/headlines.json
    'desk_cone': 'indahl-ai/cone.html',   # 10 Nov 2026: the CONE desk (ATLAS); page body from cone_index/cone.html, headline from watch/headlines.json
    'desk_quake': 'indahl-ai/quake.html',   # 10 Nov 2026: the QUAKE desk (ATLAS); page body from quake_index/quake.html, headline from watch/headlines.json
    'desk_credit': 'indahl-ai/credit.html',   # 10 Nov 2026: the CREDIT desk (HERMES); page body from credit_index/credit.html
    'desk_deus': 'indahl-ai/deus.html',   # 22 Nov 2026: the DEUS desk (HERMES); page body from deus_index/deus.html
    'desk_tornado': 'indahl-ai/tornado.html',   # 10 Nov 2026: the TORNADO desk (HERMES); page body from tornado_index/tornado.html
    'desk_argus': 'indahl-ai/argus.html',   # 22 Nov 2026: the ARGUS desk (HERMES); page body from argus_index/argus.html
    'desk_cassandra': 'indahl-ai/cassandra.html',   # 21 Nov 2026: the CASSANDRA desk (HERMES); page body from cassandra_index/cassandra.html
    'desk_ares': 'indahl-ai/ares.html',   # 22 Nov 2026: the ARES desk (HERMES); page body from ares_index/ares.html
    'desk_zeus': 'indahl-ai/zeus.html',   # 22 Nov 2026: the ZEUS desk (HERMES); page body from zeus_index/zeus.html
    'desk_seldon': 'indahl-ai/seldon.html',   # 22 Nov 2026: the SELDON desk (HERMES); page body from seldon_index/seldon.html
    'desk_prometheus': 'indahl-ai/prometheus.html',   # 21 Nov 2026: the PROMETHEUS desk (HERMES); page body from prometheus_index/prometheus.html
    'desk_voightkampff': 'indahl-ai/voightkampff.html',   # 21 Nov 2026: the VOIGHT-KAMPFF desk (HERMES); page body from voightkampff_index/voightkampff.html
    'desk_flu': 'indahl-ai/flu.html',   # 10 Nov 2026: the FLU desk (HERMES); page body from flu_index/flu.html
    'desk_steo': 'indahl-ai/steo.html',   # 10 Nov 2026: the STEO desk (HERMES); page body from steo_index/steo.html
    'desk_seasonal': 'indahl-ai/seasonal.html',   # 10 Nov 2026: the SEASONAL desk (HERMES); page body from seasonal_index/seasonal.html
    'desk_quake': 'indahl-ai/quake.html',   # 10 Nov 2026: the QUAKE desk (ATLAS); page body from quake_index/quake.html, headline from watch/headlines.json
    'desk_now': 'indahl-ai/predictions.html',   # 10 Nov 2026: the NOW desk (HERMES) at /predictions; body and headline from now_index/now.html (frozen reading)
    'desk_rank': 'indahl-ai/rank.html',   # 10 Nov 2026: the RANK desk (OY); page body from rank_index/rank_body.html (rank_index/build_page.py)
    'desk_now': 'indahl-ai/predictions.html',   # 10 Nov 2026: the NOW desk (HERMES) at /predictions; body and headline from now_index/now.html (frozen reading)
    'desk_census': 'indahl-ai/census/revisions.html',   # 11 Nov 2026: the CENSUS desk (division CENSUS); page body from census_index/census_revisions.html, headline from watch/headlines.json
    'desk_fidelity': 'indahl-ai/census/fidelity.html',   # 11 Nov 2026: the CENSUS FIDELITY desk (division CENSUS); page body from fidelity_index/fidelity.html (one-time desk, no feed)
    'desk_censuscov': 'indahl-ai/census/coverage.html',   # 11 Nov 2026: the CENSUS COVERAGE desk (division CENSUS); page body from census_coverage/census_coverage.html (one-time desk, no feed)
    'desk_petrol': 'indahl-ai/petrol.html',   # 12 Nov 2026: the ATLAS PETROL desk; page body from petrol_index/petrol_body.html
    'desk_censusvin': 'indahl-ai/census/vintages.html',   # 11 Nov 2026: the CENSUS VINTAGES desk (division CENSUS); page body from census_index/census_vintages/census_vintages.html (one-time desk, no feed)
    'census': 'indahl-ai/census.html',   # 11 Nov 2026: the CENSUS division page
    'desk_neo': 'indahl-ai/neo.html',   # 10 Nov 2026: the NEO desk (ATLAS); page body from neo_index/neo.html, headline from watch/headlines.json
    'newsletter_0': 'indahl-ai/newsletter/0.html',   # 10 Nov 2026: newsletter Issue 0 on the web (indahl-ai/newsletter_pages.py, text in newsletter/issue_0.md)
    'forecasters': 'indahl-ai/forecasters.html',   # 10 Nov 2026: FORECASTERS, every forecaster desk on one axis (indahl-ai/forecasters.py, members in forecasters/members.json)
    'forecast': 'indahl-ai/forecast.html',   # 10 Nov 2026 (cold read row 9): FORECAST, the NWS event rule beside the original committed rule, with the dated numbers at adoption
    'iris_lab': 'indahl-ai/iris/lab.html',
    'iris_lab_runs': 'indahl-ai/iris/lab/runs.html',   # 15 Nov: earlier LAB runs moved off /iris/lab by his word ("we want people to see how useful YO is")   # 30 Oct: LAB desk under IRIS (Falcon training, finalists, models on Faults and Guards), moved off /iris by his word
    'security_self': 'indahl-ai/security/self.html',   # 10 Nov 2026: SECRECORDS checks on our own domains (indahl-ai/accountability.py)
    'verify_page': 'indahl-ai/verify.html',   # 10 Nov 2026: the published signing key id
    # 17 Nov 2026, the owner: consistency site-wide; removal automated in the page builders. SAGAR rows are written by ledger/sagar_ledger.py
    # (called from sagar/site/make_sagar.py). 'sagar_study' is a folder: check_ledger.py reads every .html in it as one surface.
    'sagar': 'indahl-ai/sagar.html',
    'sagar_study': 'indahl-ai/sagar/study',
    'iris_matrix': 'indahl-ai/iris.html',   # 25 Oct: Recount Matrix: Language Models (generated from iris_index/matrix_page)   # 25 Oct: Recount Matrix: Learning Research (generated from oy_index/matrix_page)
}
ROOT = os.environ.get('FORGE_ROOT') or os.path.expanduser('~/forge')   # 17 Nov 2026, the owner: consistency site-wide; removal automated in the page builders. FORGE_ROOT lets remove.py be tested on a temp copy


def surface_path(key):
    """A surface is a key above, or 'site:<path under heuremen.org>'."""
    if key.startswith('site:'):
        return os.path.join(ROOT, 'heuremen.org', key[5:])
    p = SURFACES[key]
    return os.path.expanduser(p) if p.startswith('~') else os.path.join(ROOT, p)


def now():
    return D.datetime.now().astimezone().isoformat(timespec='seconds')


# 21 Nov 2026: ONE WRITER AT A TIME, AND NO SILENT LOSS. Until today save() wrote whatever this process held, with no lock. Two writers
# under two different locks (a ship's QUAKE refresh under the site lock, the live-headline rider under its own) both loaded, and the
# second save wiped the first: at 00:12:07Z on 21 Nov the refresh printed "23 rows refreshed", the ledger held none of them, and every
# ship after it was refused. Now:
#   - load() remembers what was on disk when this process read it;
#   - save() takes one kernel lock, reads the file as it is NOW, and applies only the rows this process changed. Rows another writer
#     changed or added meanwhile stay as that writer left them;
#   - a row changed by another writer AND by this process is a conflict: nothing is written and the process exits non-zero;
#   - after writing, save() reads the file back and checks that every row it changed is there as written.
# The file's format is unchanged (one row a line, sorted by id), so receipts and hashes of row lines hold.
class Rows(dict):
    """the ledger as this process loaded it, with what was on disk at that moment"""
    __slots__ = ('_base',)


_LAST_BASE = [None]
def _canon(r): return json.dumps(r, ensure_ascii=False, sort_keys=True)
def _read():
    rows = {}
    if os.path.exists(LEDGER):
        for line in open(LEDGER):
            if line.strip():
                r = json.loads(line); rows[r['id']] = r
    return rows


def load():
    rows = Rows(_read()); rows._base = {k: _canon(v) for k, v in rows.items()}; _LAST_BASE[0] = rows._base
    return rows


def save(rows):
    import fcntl
    base = getattr(rows, '_base', None)
    if base is None: base = _LAST_BASE[0]   # a plain dict made from a load in this process
    with open(os.path.join(HERE, '.ledger.flock'), 'a') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        cur = _read(); changed = []
        if base is None: out = dict(rows)   # nothing was loaded in this process: write what was handed over, as before, but under the lock
        else:
            out = dict(cur); conflict = []
            for k in set(base) | set(rows):
                m = _canon(rows[k]) if k in rows else None; b = base.get(k); c = _canon(cur[k]) if k in cur else None
                if m == b: continue                        # not changed by this process: the row on disk stays as it is now
                if c != b and c != m: conflict.append(k); continue
                changed.append(k)
                if m is None: out.pop(k, None)
                else: out[k] = rows[k]
            if conflict:
                sys.exit('ledger.save REFUSED: %d row(s) were changed by another writer since this process loaded the ledger, and by this process too: %s. '
                         'Nothing was written. Load the ledger again and reapply.' % (len(conflict), ', '.join(sorted(conflict)[:8])))
        tmp = LEDGER + '.tmp'
        with open(tmp, 'w') as f:
            for r in sorted(out.values(), key=lambda r: r['id']):
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
        os.replace(tmp, LEDGER)
        back = _read()   # what the file holds now, not what was sent
        lost = [k for k in changed if (_canon(back[k]) if k in back else None) != (_canon(rows[k]) if k in rows else None)]
        if lost: sys.exit('ledger.save: READ BACK FAILED for %d row(s): %s. The ledger does not hold what was written.' % (len(lost), ', '.join(sorted(lost)[:8])))
        if base is not None:
            for k in changed:   # this process's view of what is on disk moves only for the rows it wrote
                if k in rows: base[k] = _canon(rows[k])
                else: base.pop(k, None)
    return len(changed)


def need(rows, cid):
    if cid not in rows:
        sys.exit(f'no claim {cid}')
    return rows[cid]


def checks_ref(path):
    """30 Oct 2026 (the owner's "hit it"): a public number enters or changes only with a complete check block. Returns what the row keeps."""
    import subprocess, hashlib, re
    p = os.path.expanduser(path); p = p if os.path.isabs(p) else os.path.join(ROOT, p)
    if not os.path.exists(p): sys.exit(f'--checks file not found: {p}')
    r = subprocess.run([sys.executable, os.path.expanduser('~/forge/watch/readcheck.py'), 'check', p], capture_output=True, text=True)
    if r.returncode: sys.exit('refused: ' + r.stdout.strip())
    last = re.split(r'(?m)^## (?=\d{4}-\d{2}-\d{2})', open(p).read())[-1]
    return dict(file=path, entry=last.splitlines()[0].strip(), sha256=hashlib.sha256(last.encode()).hexdigest()[:16])
def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('list'); p.add_argument('--status'); p.add_argument('--surface')
    p = sub.add_parser('show'); p.add_argument('id')
    p = sub.add_parser('add'); p.add_argument('id'); p.add_argument('--claim', required=True); p.add_argument('--value', required=True)
    p.add_argument('--lo'); p.add_argument('--hi'); p.add_argument('--unit', default=''); p.add_argument('--outcome', required=True)
    p.add_argument('--source', required=True); p.add_argument('--grep', required=True)
    p.add_argument('--on', nargs=2, action='append', metavar=('SURFACE', 'SNIPPET'), default=[])
    p.add_argument('--checks', required=True, help='CHECKS.md whose last entry is complete (watch/readcheck.py, 30 Oct)')
    p = sub.add_parser('set'); p.add_argument('id'); p.add_argument('--field', required=True); p.add_argument('--to', required=True)
    p.add_argument('--why', required=True); p.add_argument('--evidence', required=True); p.add_argument('--checks')
    p = sub.add_parser('on'); p.add_argument('id'); p.add_argument('surface'); p.add_argument('snippet')
    p = sub.add_parser('off'); p.add_argument('id'); p.add_argument('surface'); p.add_argument('--why', required=True)
    p = sub.add_parser('withdraw'); p.add_argument('id'); p.add_argument('--why', required=True)
    p.add_argument('--evidence'); p.add_argument('--test')
    p = sub.add_parser('cannot_tell'); p.add_argument('id'); p.add_argument('--why', required=True)
    a = ap.parse_args(); rows = load()

    if a.cmd == 'list':
        for r in sorted(rows.values(), key=lambda r: r['id']):
            if a.status and r['status'] != a.status: continue
            if a.surface and not any(s['surface'] == a.surface for s in r['surfaces']): continue
            iv = f" [{r['lo']}, {r['hi']}]" if r.get('lo') is not None else ''
            print(f"{r['id']:<28} {r['status']:<11} {r['outcome']:<11} {r['value']}{iv} {r['unit']}  | {r['claim'][:70]}")
        return
    if a.cmd == 'show':
        print(json.dumps(need(rows, a.id), indent=1, ensure_ascii=False)); return
    if a.cmd == 'add':
        if a.id in rows: sys.exit(f'{a.id} exists; use set/on')
        if a.outcome not in OUTCOMES: sys.exit(f'outcome must be one of {sorted(OUTCOMES)}')
        src = os.path.join(ROOT, a.source) if not a.source.startswith('/') else a.source
        if not os.path.exists(src): sys.exit(f'source file not found: {src}')
        if a.grep not in open(src, errors='ignore').read(): sys.exit(f'source does not contain {a.grep!r}: refused')
        for s, _ in a.on: surface_path(s)
        ck = checks_ref(a.checks)
        rows[a.id] = dict(checks=ck, id=a.id, claim=a.claim, value=a.value, lo=a.lo, hi=a.hi, unit=a.unit, outcome=a.outcome,
                          source=dict(file=a.source, grep=a.grep), surfaces=[dict(surface=s, text=t) for s, t in a.on],
                          status='live', history=[dict(at=now(), change='added', evidence=a.source)])
    elif a.cmd == 'set':
        r = need(rows, a.id)
        if not os.path.exists(os.path.expanduser(a.evidence)) and not os.path.exists(os.path.join(ROOT, a.evidence)):
            sys.exit(f'evidence not found: {a.evidence}')
        if a.field in ('value', 'lo', 'hi', 'outcome'):
            if not a.checks: sys.exit(f'changing {a.field} is a new reading: --checks <CHECKS.md> with a complete entry is required')
            r.setdefault('checks_history', []).append(checks_ref(a.checks))
        if a.field.startswith('surfaces.'):   # 22 Nov 2026: a surface's snippet (surfaces.N.text / surfaces.N.surface) had no way to be edited; a rename left drift
            _, i, k = a.field.split('.', 2); old = r['surfaces'][int(i)].get(k); r['surfaces'][int(i)][k] = a.to
        elif a.field.startswith('source.'):   # source.file / source.grep (23 Oct: a wrong source pointer had no way to be fixed)
            k = a.field.split('.', 1)[1]; old = r['source'].get(k); r['source'][k] = a.to
        else:
            old = r.get(a.field); r[a.field] = a.to
        r['history'].append(dict(at=now(), change=f'{a.field}: {old!r} -> {a.to!r}', why=a.why, evidence=a.evidence))
    elif a.cmd == 'on':
        r = need(rows, a.id); surface_path(a.surface)
        r['surfaces'].append(dict(surface=a.surface, text=a.snippet)); r['history'].append(dict(at=now(), change=f'on {a.surface}'))
    elif a.cmd == 'off':
        r = need(rows, a.id)
        r['surfaces'] = [s for s in r['surfaces'] if s['surface'] != a.surface]
        r['history'].append(dict(at=now(), change=f'off {a.surface}', why=a.why))
    elif a.cmd == 'withdraw':
        r = need(rows, a.id)
        ev_ok = a.evidence and (os.path.exists(os.path.expanduser(a.evidence)) or os.path.exists(os.path.join(ROOT, a.evidence)))
        if not (ev_ok and a.test):
            sys.exit('REFUSED: a withdrawal needs --evidence (a file that exists) AND --test (what was run and what it gave).\n'
                     'An untested cut is not a deletion: use  ledger.py cannot_tell ID --why ...')
        r['status'] = 'withdrawn'
        r['history'].append(dict(at=now(), change='withdrawn', why=a.why, evidence=a.evidence, test=a.test))
    elif a.cmd == 'cannot_tell':
        r = need(rows, a.id); r['status'] = 'cannot_tell'; r['outcome'] = 'CANNOT_TELL'
        r['history'].append(dict(at=now(), change='cannot_tell', why=a.why))
    save(rows); print('ok', a.cmd, getattr(a, 'id', ''))


if __name__ == '__main__':
    main()
