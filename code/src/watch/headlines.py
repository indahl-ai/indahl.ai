#!/usr/bin/env python3
"""headlines.py: tick-bus rider. Builds one headline per page from the live feeds (number first, plain words) and publishes headlines.json to the KV key 'headlines'.
The pages’ headline.js reads /headlines.json. A page whose feed cannot be read gets no headline this round."""
import os, re, json, time, subprocess, urllib.request, hashlib
import os as _pg_os, sys as _pg_sys, subprocess as _pg_sp   # 10 Nov 2026 (publish guard): the site KV is written only by a run the tick bus or the house clock started
_PUBLISH = '--publish' in _pg_sys.argv or _pg_os.environ.get('HEUREMEN_PUBLISH') == '1'   # (they export HEUREMEN_PUBLISH=1) or a run given --publish. A copy run for a reproduce kit or a test never publishes
if _PUBLISH: _pg_os.environ['HEUREMEN_PUBLISH'] = '1'   # passed on to the scripts this one starts, and kept across a detach or re-exec
try:   # 22 Nov 2026: one shared upload part (lib/cf.py: kv token, rings on failure); this file's own guard stays as the fallback for kits
    _pg_sys.path.insert(0, _pg_os.path.expanduser('~/forge/lib')); from cf import guarded_put as _kv_put
except Exception:
    def _kv_put(cmd, **kw):
        if _PUBLISH: return _pg_sp.run(cmd, **kw)
        print('publish guard: %s not put to the site KV (run with --publish, or from the tick bus)' % cmd[5], file=_pg_sys.stderr)
        return _pg_sp.CompletedProcess(cmd, 0, '' if kw.get('text') or kw.get('universal_newlines') else b'', '' if kw.get('text') or kw.get('universal_newlines') else b'')
B = os.path.expanduser('~/forge'); W = B + '/cloudflare-workers/heuremen-door'; NS = '<kv-namespace-id>'
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u + ('&' if '?' in u else '?') + 'x=%d' % time.time(), headers={'User-Agent': 'heuremen-headlines/0.1'}), timeout=30).read()
# 10 Nov 2026 (cold read row 5): the riders run in parallel on the bus, and a KV write takes up to a minute to reach the edge, so a headline read
# from the public feed could carry the read before the one the page body shows. A desk that keeps its feed file here is read from that file,
# the same bytes its tick puts to KV, and the HOSTS and QIA queue ticks start this script again right after they publish.
LOCAL = {'hosts': B + '/hosts_index/summary_hosts.json', 'voightkampff': B + '/voightkampff_index/data/voightkampff_live.json', 'neo': B + '/neo_index/data/neo_live.json', 'quake': B + '/quake_index/data/quake_live.json', 'census': B + '/census_index/data/census_live.json', 'solar': B + '/solar_index/data/solar_live.json', 'cone': B + '/cone_index/data/cone_live.json', 'tornado': B + '/tornado_index/data/tornado_live.json', 'prometheus': B + '/prometheus_index/data/prometheus_live.json', 'ares': B + '/ares_index/data/ares_live.json', 'deus': B + '/deus_index/data/deus_live.json', 'argus': B + '/argus_index/data/argus_live.json', 'credit': B + '/credit_index/data/credit_live.json'}   # 10 Nov 2026: NEO’s feed file is the bytes its tick puts to KV neo_live
def feed(s):
    if s in LOCAL and os.path.exists(LOCAL[s]): return json.load(open(LOCAL[s]))
    return json.loads(get('https://indahl.ai/%s/live.json' % s))
import fcntl as _fc
_lk = open(B + '/watch/.headlines.lock', 'w'); _fc.flock(_lk, _fc.LOCK_EX)   # one build at a time; a second start waits and then builds from the newer files
def ordn(n): n = int(n); return '%d%s' % (n, 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th'))
def pct(x, d=0): return ('%.' + str(d) + 'f%%') % (100 * x)
def f(n): return '{:,}'.format(int(n))
H = {}
def add(slug, big, line, href=None):
    H[slug] = dict(big=big, line=line, href=href or '/' + slug)
_SKIPPED = {}   # 21 Nov 2026 (control audit #21): a desk headline that throws was dropped silently; now rung once to sagar/pipeline/pipe.log
def _ring(m):
    try: open(B + '/sagar/pipeline/pipe.log', 'a').write(time.strftime('%Y-%m-%dT%H:%M:%S ') + 'RING: HEADLINES ' + m + '\n')
    except Exception as e: print('headlines: could not ring pipe.log:', type(e).__name__)
def safe(slug, fn):
    try: fn()
    except Exception as e: print('headlines: skipped', slug, type(e).__name__, str(e)[:60]); _SKIPPED[slug] = '%s %s' % (type(e).__name__, str(e)[:80])
def airq():
    d = feed('airq'); c = d['comparison']; a = c['Map reading (atm channels, raw)']; r = c['cf_1 corrected for humidity (Barkjohn 2021)']
    # 10 Nov 2026 (AIRQ Addendum 5): the plan names no headline reading, so the map reading and the corrected reading lead together, with the other tie
    tie = lambda c: (' (%d under the other tie)' % c['n_other_tie']) if c.get('n_other_tie') is not None and c['n_other_tie'] != c['n'] else ''
    # 11 Nov (his "poorly worded ... is there a better, shorter one"): both readings as one range, neither named the headline (Addendum 5); ties and 2025 stay on /airq
    lo, hi = sorted((r['n'], a['n']))
    add('airq', '%d to %d' % (lo, hi), 'of %d EPA monitors had a nearby PurpleAir sensor that missed the EPA accuracy target, %s: %d with the humidity correction, %d on the raw map reading.' % (a['of'], d.get('window') or '1 June to 29 September 2025', r['n'], a['n']))
def hosts():
    d = feed('hosts'); add('hosts', f(d['problems_now']), 'open-weight model endpoints were flagged by OpenRouter or showed 5-minute uptime below 100 percent at the read of %s UTC, out of %s endpoints on %d hosts serving %d models.' % (d['updated'][-5:], f(d['endpoints']), d['hosts'], d['models']))
def airline():
    d = feed('airline'); rows = [(k, v) for k, v in d['now_vs_2025'].items() if v.get('outcome') == 'ABOVE']; rows.sort(key=lambda kv: -kv[1]['change'])
    top = ', '.join('%s +%d min' % (k.split(' (')[0], round(v['change'])) for k, v in rows[:3])
    _fa = d.get('faa', {}); faa = _fa.get('airports_listed', _fa.get('airports_now')); prog = _fa.get('airports_now'); tail = (' Right now the FAA lists a delay or closure notice at %d airport%s, %d with a delay program.' % (faa, '' if faa == 1 else 's', prog or 0)) if faa is not None else ''   # 30 Oct 2026 (site pass I-4): the count includes closures until nas_tick.py counts programs only
    add('airline', '%d of %d' % (len(rows), d['headline']['of']), 'airlines widened the gap between scheduled and flown time on their median route, %s 2026 against 2025: %s.%s' % (d.get('months') or 'January to August', top, tail) + ((' Airlines read: ' + d['headline']['req13']['line']) if (d['headline'].get('req13') or {}).get('line') else ''))   # 12 Nov 2026 (Faults and Guards 2.0, REQ-13)   # 9 Nov 2026 (site pass M2): a median over routes, not each route
def weights():
    d = feed('weights'); h = d['headline']; e = d.get('ever') or h   # 30 Oct site pass I-3: changes on any pass, not netted to the latest pair
    add('weights', '%d of %s' % (e['n'], f(e['of'])), 'popular Hugging Face models changed their weight files on at least one read, %d between the last two. Last read %s UTC.' % (h['n'], d['updated'][-5:]))
def ailuminate():
    d = feed('ailuminate'); h = d['headline']   # 16 Nov 2026 (teardown #8): the desk’s own reading, with its ruler, not the spread of scores
    oc = {'CANNOT_TELL': 'cannot tell', 'CONSISTENT': 'consistent', 'ABOVE': 'above the band'}.get(h['outcome'], h['outcome'].lower())
    add('ailuminate', '%d of %d' % (h['n'], h['of']), 'systems on the MLCommons AILuminate results page disagree with their own detailed reports (95%% interval %s to %s): %s against the 5%% that would matter.' % (pct(h['share_lo']), pct(h['share_hi'], 1), oc))
def campus():
    d = feed('campus'); s = d['state_now']; add('campus', '%d of %d' % (s['Opens (HTTP 200)'], d['sources']), 'sources behind the OY page open today. %d are not found and %d refuse automated reads.' % (s['Not found (404, 410)'], s['Blocked (401, 403, 429)']))
def hpt():
    d = feed('hpt'); c = d['comparison']; k2 = [v for k, v in c.items() if k.startswith('2')][0]
    add('hpt', '%d of %d' % (k2['n'], k2['of']), 'hospital price files linked from hospital websites do not open as data. %s hospital websites were read for the file the federal rule asks for.' % f(d['domains']))
def secrecords():
    d = feed('secrecords'); c = d['comparison']; a = c['HSTS preload header']; b = c['SPF lookup limit']
    add('secrecords', pct(a['share']), 'of top sites that send an HSTS preload header miss the preload list’s own requirements (%d of %d). %d of %d SPF records break the 10-lookup limit.' % (a['n'], a['of'], b['n'], b['of']) + (' HSTS: ' + a['req13_line'] if a.get('req13_line') else '') + (' SPF: ' + b['req13_line'] if b.get('req13_line') else ''))   # 12 Nov 2026 (Faults and Guards 2.0, REQ-13): the counts beside each headline share
def hfsize():
    d = feed('hfsize'); c = d['comparison']; add('hfsize', '%d of %d' % (c['n'], c['of']), 'popular Hugging Face models weigh outside the size in their name.' + (' ' + c['req13_line'] if c.get('req13_line') else ''))   # 12 Nov 2026 (Faults and Guards 2.0, REQ-13)
def pkglicense():
    # 30 Oct 2026 (site pass I-21): say what the disagreements are. Our hand notes show some are a classifier that differs from the license field, or a package in a subfolder of a repository with another root license.
    d = feed('pkglicense'); c = d['classes']; n = c['DISAGREE']['n']; of = c['AGREE']['n'] + n
    soft = sum(1 for r in d.get('disagree_list', []) if 'classifier' in r.get('reason', '') or 'subfolder' in r.get('reason', ''))
    add('pkglicense', '%d of %d' % (n, of), 'PyPI projects state a license that differs from the license GitHub reports for their repository.' + ((' Each is read in full. %d of them are a classifier that differs from the license field, or a package in a subfolder of a repository with another root license.' % soft) if soft else '') + (' ' + d['disagree']['req13_line'] if d.get('disagree', {}).get('req13_line') else ''))   # 12 Nov 2026 (Faults and Guards 2.0, REQ-13)
def support():
    d = feed('support'); a = d['all']; add('support', pct(a['share']), 'of release cycles stated as supported had no release in more than a year (%d of %d).' % (a['unreleased'], a['tested']))
def trials():
    # 10 Nov 2026 (TRIALS Addendum 5): records 13 to 15 months past completion are the plan’s lag zone and are not scored
    d = feed('trials'); a = d['all']; add('trials', pct(a['share_no_results'], 1), 'of ClinicalTrials.gov trials of FDA-regulated drugs and devices that reached primary completion at least 15 months ago have no results on the record (%s of %s).' % (f(a['no_results']), f(a['n'])) + ((' Records 13 to 15 months past completion are shown apart and not scored (%s).' % f(d['lag_zone']['n'])) if d.get('lag_zone') else ''))
def revise():
    d = feed('revise'); c = d['counts']; k = [v for kk, v in c.items() if kk.startswith('Most recent')][0]; t = [v for kk, v in c.items() if kk.startswith('Third')][0]
    OC = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell'}   # 10 Nov 2026 (newsletter audit): both intervals, and which one the plan names
    RW = lambda o, r: OC.get(o, o) + ((' (%s)' % r) if o == 'CANNOT_TELL' and r else '')   # 12 Nov 2026 (Faults and Guards 2.0): the reason stands beside every cannot tell
    add('revise', '%d of %d' % (k['exceed'], k['months']), 'monthly jobs numbers moved by more than the BLS’s stated margin once benchmarked. %d of %d moved that far by the third release. On the interval over months, which the plan names, the benchmarked count reads %s. On the interval over calendar years it reads %s.' % (t['exceed'], t['months'], RW(k['outcome'], k.get('reason')), RW(k.get('outcome_y'), k.get('reason_y'))) + ((' Beside the benchmarked count: ' + k['req13']['line']) if (k.get('req13') or {}).get('line') else ''))
def fedsep():
    d = feed('fedsep'); p = d['pooled']; n = [v for k, v in p.items() if k.startswith('Next')][0]; t = [v for k, v in p.items() if k.startswith('This')][0]
    add('fedsep', '%d of %d' % (n['outside'], n['triples']), 'next-year Fed projections landed outside the 70 percent range the Fed states. This year, %d of %d.' % (t['outside'], t['triples']) + ((' Read against 0.30 with no tolerance, next year reads cannot tell (%s). %s' % (n.get('reason'), n['req13']['line'])) if (n.get('req13') or {}).get('line') and n.get('outcome') == 'CANNOT_TELL' else ((' ' + n['req13']['line']) if (n.get('req13') or {}).get('line') else '')))   # 12 Nov 2026 (Faults and Guards 2.0, REQ-13)
def change():
    d = feed('change'); L = d['lifespan']; g = L.get('Google, names with preview') or L['Google']; o = L.get('Google, other names')   # 30 Oct site pass I-2: all of the short-lived ones are previews
    add('change', '%d of %d' % (g['under180'], g['n']), 'Google preview models with a shutdown date ran under six months. Their median is %s days.%s' % (('%g' % g['median']), (' Of %d other Google models, %d did (median %s days).' % (o['n'], o['under180'], '%g' % o['median'])) if o else ''))
def cadence():
    # 10 Nov 2026 (newsletter audit): never round an age up to a whole year. 5,782 days is 15.8 years, printed as nearly 16 years.
    d = feed('cadence'); m = d['most_overdue'][0]; y = m['age_days'] / 365.25; n = round(y)
    add('cadence', ('nearly %d years' if n > y else 'over %d years') % n, 'since a US government dataset that states a daily update was last modified (%.1f years): %s, %s.' % (y, m['title'], m['portal']) + ((' Across all series read: ' + d['req13']['line']) if (d.get('req13') or {}).get('line') else ''))   # 12 Nov 2026 (Faults and Guards 2.0, REQ-13)
def linkrot():
    d = feed('linkrot'); a = d['all']; add('linkrot', pct(a['rot_share'], 1), 'of code and data links in arXiv papers are gone (%d of %s).' % (a['gone'], f(a['links'])))
def _watched_flown():
    # launches that flew after we first read them: some snapshot of the launch was taken before it flew. Launches already flown at our first read cannot be scored.
    f = B + '/launch_index/data/snapshots.jsonl'
    if not os.path.exists(f): return None
    hist = {}
    for l in open(f):
        try: s = json.loads(l)
        except Exception: continue
        hist.setdefault(s['id'], []).append(s)
    FL = {'Success', 'Failure', 'Partial Failure'}; n = 0
    for hs in hist.values():
        if hs[-1]['status'] in FL and any(h['status'] not in FL for h in hs): n += 1
    return n
def launch():
    # 30 Oct 2026 (site pass H-4): the first reads already held 100 flown launches, which were never watched before they flew and cannot be scored.
    d = feed('launch'); w = _watched_flown()
    if w is None: add('launch', '%d' % d['waiting'], 'tracked launches are waiting to fly. Each stated launch time is scored against the actual one once the launch has flown.'); return
    add('launch', '%d' % w, 'launches have flown since reading began. %d more are waiting to fly. The other %d flown launches were already in the record at the first read and are not scored. Each stated launch time is scored against the actual one.' % (d['waiting'], d['flown'] - w))
def pkginstall():
    d = feed('pkginstall'); c = d['comparison']; add('pkginstall', '%d of %d' % (c['of'] - c['n'], c['of']), 'install commands in popular Python packages resolve on a clean install. Only the %d of %s projects with a comparable command are counted.' % (c['of'], f(d.get('projects', 1000))) + (' ' + c['req13_line'] if c.get('req13_line') else ''))   # 12 Nov 2026 (Faults and Guards 2.0, REQ-13)
def oy():
    # 10 Nov 2026 (newsletter audit): the headline is built with the page by oy_index/matrix_page/build_matrix_page.py from the rows (two readings,
    # the rule written before the read first, the rule set after 41 schools beside it). Read from that file, never scraped or typed here.
    h = json.load(open(B + '/oy_index/matrix_page/oy_headline.json', encoding='utf-8')); add('oy', h['big'], h['line'])
def tape():
    # 30 Oct 2026 (site pass I-28): lead on the age of the newest entry, not on a count of our own entries
    d = feed('tape'); h = d['head']; b = d['beacon']
    import calendar; age = max(0, time.time() - calendar.timegm(time.strptime(h['t'][:19], '%Y-%m-%dT%H:%M:%S')))
    add('tape', _dur(age), 'since the newest entry was chained to the tape, at %s UTC. Each entry is hashed onto the one before, and the beacon now begins %s.' % (h['t'][11:16], b['value'][:8]))
def atlas():
    # 30 Oct 2026 (site pass A-16): ATLAS has its own headline, from its own map data, and no longer borrows the SECRECORDS reading
    # 30 Oct 2026 (his "the data headline is the cost to scale"): once /atlas/scale.json is live the headline is the cost to scale, arithmetic on Epoch AI’s stated power and EIA-861 state prices. Until then the count line below stands.
    try:
        t = json.loads(get('https://indahl.ai/atlas/scale.json'))['totals']
        add('atlas', '$%s billion' % t['total_busd'], 'for one year of electricity at the full stated power of the %d AI data centers in Epoch AI’s dataset that state a power and sit in a state, at each state’s average 2024 industrial price from EIA-861. It is arithmetic on published figures, not a forecast and not any site’s bill.' % t['counted'], '/atlas')
        return
    except Exception: pass
    d = json.loads(get('https://indahl.ai/atlas/datacenters.json'))
    add('atlas', f(len(d['osm'])), 'features tagged as data centers in OpenStreetMap in the United States, and %d AI data centers in Epoch AI’s dataset, pulled %s. This is what these two sources hold, not a count of every data center.' % (len(d['epoch']), d['pulled']), '/atlas')
def _dur(x):
    x = float(x); return '%d s' % round(x) if x < 90 else ('%d min' % round(x / 60) if x < 5400 else '%.1f h' % (x / 3600))
def _open_rates():
    # 30 Oct 2026 (his "labs should check QIA for the fez wait time"): Open plan probes pair the jobs in front at sending with the measured wait
    rows = [json.loads(l) for l in open(B + '/qia_queue/data/probes_open.jsonl')] if os.path.exists(B + '/qia_queue/data/probes_open.jsonl') else []
    out = {}
    for r in rows:
        if r.get('wait_s') is None: continue
        out.setdefault(r['backend'], []).append((r.get('front_at_send') or 0, r['wait_s']))
    return out
def _probes(name):
    f = B + '/qia_queue/data/' + name
    return [json.loads(l) for l in open(f)] if os.path.exists(f) else []
def qia():
    # 30 Oct 2026 (his "labs should check QIA for the fez wait time ... every us east and europe plan"): jobs in front from IBM (free), the wait our
    # latest one-shot probe saw on each processor (paid plans, every hour), and the Open plan approximation from its own probes.
    d = json.load(open(B + '/qia_queue/summary.json')); ps = [dict(backend=p['backend'], pending=p['pending']) for p in d['processors'] if p.get('pending') is not None]
    eu = _probes('probes_eu.jsonl')
    if eu and eu[-1].get('front_at_send') is not None and not any(p['backend'] == eu[-1]['backend'] for p in ps): ps.append(dict(backend=eu[-1]['backend'], pending=eu[-1]['front_at_send']))
    ps.sort(key=lambda p: -p['pending']); b = ps[0]; avg = sum(p['pending'] for p in ps) / len(ps); now = time.time()
    latest = {}
    for r in _probes('probes.jsonl') + eu:
        if r.get('state') != 'NOT_FOUND': latest[r['backend']] = r   # files are in send order, so the last row per processor is the newest (11 Nov: a job IBM cannot find carries no wait)
    def wait_now(n):
        r = latest.get(n)
        if not r: return 'first probe pending'
        if r.get('wait_s') is not None: return _dur(r['wait_s'])
        import calendar; t = calendar.timegm(time.strptime(r['sent'], '%Y-%m-%dT%H:%M:%SZ'))   # the stamp is UTC
        return 'waiting ' + _dur(max(0, now - t)) + ' so far'
    OPENP = ('ibm_fez', 'ibm_kingston', 'ibm_marrakesh'); rates = _open_rates()
    def approx(p):
        if p['backend'] not in OPENP: return '\u2014'
        v = rates.get(p['backend'], [])
        if not v: return 'pending'
        rs = sorted(w / f for f, w in v if f > 0)
        if not rs: return _dur(max(w for f, w in v))
        return 'about ' + _dur(p['pending'] * rs[len(rs) // 2])
    add('qia', f(b['pending']), 'jobs in front at %s, the longest IBM queue. Last read %s.' % (b['backend'], d['updated']))
    # 11 Nov 2026 (his "make qubit 85 a data headline on QIA"): the lead is boston qubit 85 from its newest joint T1/T2 run, while IBM’s T2 reads ABOVE
    # the 2 x T1 ceiling; the queue keeps its table below. Read from t1t2_check/summary_t1t2.json, the bytes publish_results.py puts to KV qia_t1t2.
    try:
        tt = json.load(open(B + '/t1t2_check/summary_t1t2.json'))
        runs = sorted([(p['ran'], q) for p in tt['processors'] if p['backend'] == 'ibm_boston' and p.get('state') == 'ran' for q in p['qubits'] if q['qubit'] == 85])
        if runs and runs[-1][1].get('ibm_t2_vs_now') == 'ABOVE':
            ran, q = runs[-1]; day = time.strftime('%-d %b', time.strptime(ran[:10], '%Y-%m-%d'))
            line = ('is the T2 IBM publishes for qubit 85 on ibm_boston. The indahl.ai run on %s measured its T1 at %.1f \u00b5s (95%% interval %.1f to %.1f), so no T2 on that qubit could be above %.1f \u00b5s.'
                    % (day, q['t1'], q['t1_ci'][0], q['t1_ci'][1], q['t2_max_now']))
            # 11 Nov (his "put both in the headline"): the other qubit in the same job, when IBM’s T1 for it reads ABOVE or BELOW our measured interval
            same = [p for p in tt['processors'] if p['backend'] == 'ibm_boston' and p.get('ran') == ran]
            for c in (same[0]['qubits'] if same else []):
                if c['qubit'] != 85 and c.get('ibm_t1_vs_now') in ('ABOVE', 'BELOW'):
                    line += (' In the same job, the T1 IBM publishes for qubit %d (%.0f \u00b5s) is %s what was measured, %.0f \u00b5s (95%% interval %.0f to %.0f).'
                             % (c['qubit'], c['pub_t1'], 'below' if c['ibm_t1_vs_now'] == 'BELOW' else 'above', c['t1'], c['t1_ci'][0], c['t1_ci'][1]))
            add('qia', '%.1f \u00b5s' % q['pub_t2'], line, href='/qia#t1t2-live')
    except Exception as e: print('headlines: qia qubit 85 lead skipped', type(e).__name__, str(e)[:60])
    # 11 Nov (his "we never have wait times for the open plan"): the Open plan column shows only while its probes have a wait from the last 7 days
    _op = [r for r in _probes('probes_open.jsonl') if r.get('wait_s') is not None and r.get('sent', '') >= time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(now - 7 * 86400))]
    # 15 Nov 2026 (the owner’s QIA reorganisation): one queue table. The 24-hour change and the median wait of finished indahl.ai jobs come from
    # qia_queue/summary.json (the bytes queue_tick.py puts to KV qia_queue), so the second table under it is retired. Same pending counts checked first:
    # both feeds read 15 Nov ~21:36 UTC agreed on all seven shared processors.
    try: _qs = {r['backend']: r for r in json.load(open(B + '/qia_queue/summary.json'))['processors']}
    except Exception as e: _qs = {}; print('headlines: qia queue summary unreadable', type(e).__name__)
    def _chg(b):
        v = _qs.get(b, {}).get('change_24h'); return '\u2014' if v is None else ('%+d' % v if v else '0')
    def _med(b):
        r = _qs.get(b, {}); return r.get('our_median_wait') or '\u2014'
    _cols = ['Processor', 'Jobs in front', 'Change, 24 h', 'Latest paid job'] + (['Open plan estimate'] if _op else []) + ['Median wait, finished jobs']
    H['qia']['table'] = dict(cols=_cols, rows=[[p['backend'], f(p['pending']), _chg(p['backend']), wait_now(p['backend'])] + ([approx(p)] if _op else []) + [_med(p['backend'])] for p in ps],
                             foot=['Average', f(round(avg)), '', ''] + ([''] if _op else []) + [''],
                             note='Jobs in front: the count IBM reports. Change, 24 h: against the earliest reading in the last 24 hours. Latest paid job: the newest indahl.ai calibration job on a paid plan, from sending to running, or how long it has waited so far; a job is not sent to every processor every hour.' + (' Open plan estimate: jobs in front now times the seconds per job in front measured by indahl.ai probes on the Open plan, the free line most labs use (\u2014 where there are no probes).' if _op else '') + ' Median wait: finished indahl.ai jobs, shown from three. IBM publishes no wait estimate.')
    H['qia']['table']['cta'] = dict(text='Check a wait: probe.py', href='/qia/probe.py', rest=' One Python file and an IBM key. Jobs in front are free, a timed probe costs 2 s of the plan. Source also on ', link2='GitHub', href2='https://github.com/indahl-ai/indahl.ai/blob/main/code/qia/probe.py', tail=', needs qiskit-ibm-runtime (PyPI).')
def lab():
    # 11 Nov 2026 (his "ANY training we do is live on the lab page ... every page should have a live something at top and a data headline"): the newest
    # paired test of a referee V seat, and every seat’s stage now, from referee_library/council/live_export.json (the allow-listed bytes live_export.py puts to KV council_live).
    if os.path.exists(B + '/referee_library/council/PAUSE') and os.path.exists(B + '/stan/results/baseline_dev.json'):
        # 12 Nov 2026 (his "close it out on the lab too and make sure Stan is live"): The referee V is paused for STANYO, so the lab leads with STANYO. Every number is computed from
        # stan/results/baseline_dev.json: the untrained base’s pooled agreement with the answer key (development half), and the pooled majority-class rate
        # (n-weighted mean of the per-code rates). Ledger rows stan.baseline.base and stan.baseline.majority.
        # 12 Nov 2026 (the referee break 1): the agreement headline counted CANNOT_TELL as agreeing with an unflagged recount, so it measured abstention.
        # The lab now leads with the decided share (calls a model commits to), from stan/results/decided_summary.json. Ledger rows stan.v1.decided, stan.base.decided.
        # 15 Nov 2026 (his "why is our failure a data headline ... STANYO or YO training, those are the two shippable ones"): the LAB headline is YO at
        # work, from yo/live_reads.jsonl (v7 reads only): the share of new IBM records where YO’s flags matched the answer code computes from the same record.
        rd = [json.loads(l) for l in open(B + '/yo/live_reads.jsonl')] if os.path.exists(B + '/yo/live_reads.jsonl') else []
        v7 = [r for r in rd if r.get('model') == 'v7']
        if v7:
            ex = sum(r['score'] == 1.0 for r in v7)
            add('iris/lab', '%d%%' % round(100 * ex / len(v7)),
                'of the new IBM calibration records YO v7 has read, its flags matched the answer code computes from the same record exactly: %s of %s since %s. YO reads each new record as IBM publishes it.'
                % (f(ex), f(len(v7)), time.strftime('%-d %b', time.strptime(min(r['read'] for r in v7)[:10], '%Y-%m-%d'))), href='/yo')
            rows = [[r['backend'], r['stamp'], 'matched' if r['score'] == 1.0 else 'score %.2f' % r['score']] for r in v7[-6:][::-1]]
            H['iris/lab']['table'] = dict(cols=['Processor', 'Record', 'YO against the code'], rows=rows,
                                          note='The newest reads by YO v7. A read matches when YO flags exactly the qubits the code flags (stale T1 or T2, and error values of exactly zero).',
                                          cta=dict(text='Watch YO read live', href='/yo', rest=' Training data and every read: ', link2='Hugging Face', href2='https://indahl.ai/downloads', tail='.'))
        return
    d = json.load(open(B + '/referee_library/council/live_export.json'))
    pr = sorted([x for x in d.get('paired') or [] if x.get('grounded') and len(x['grounded']) == 4 and None not in x['grounded']], key=lambda x: x['ts'])
    ev = sorted(d.get('events') or [], key=lambda x: x['ts'])
    def outcome(seat, ts):
        for e in ev:
            if e['seat'] == seat and e['ts'] >= ts and e['event'] in ('went live', 'rolled back after the paired eval', 'rolled back', 'champion kept'):
                return {'went live': 'The new adapter went live.', 'champion kept': 'The adapter already serving was kept over it.',
                        'rolled back': 'The new adapter was rolled back.', 'rolled back after the paired eval': 'The new adapter was rolled back on its test.'}[e['event']]
        return 'Its release is being decided.'
    def ago(ts):
        m = int((time.time() - time.mktime(time.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')) + time.timezone) // 60)
        return '%d min ago' % m if m < 120 else '%d h ago' % (m // 60)
    if pr:
        x = pr[-1]; g = x['grounded']
        add('iris/lab', '%d%%' % round(100 * g[1]),
            "of %s's claims carried a quote the code found in the passage it was shown, with this turn’s adapter, against %d%% for the base model, on %d held-out prompts (difference %d to %d points, 95%% interval). %s Tested %s."
            % (x['seat'], round(100 * g[0]), x['n'], round(100 * g[2]), round(100 * g[3]), outcome(x['seat'], x['ts']), ago(x['ts'])), href='/iris/lab/live')
    else:
        return
    def short(seat, ts):
        o = outcome(seat, ts)
        return {'The new adapter went live.': 'went live', 'The adapter already serving was kept over it.': 'kept the serving adapter', 'The new adapter was rolled back.': 'rolled back',
                'The new adapter was rolled back on its test.': 'rolled back on its test'}.get(o, 'deciding')
    NOW = {'harvest': 'collecting examples', 'SFT': 'training', 'DPO': 'preference training', 'paired eval': 'testing', 'idle': 'idle'}
    SERV = {'released': 'its own adapter', 'serving, not released': 'adapter on trial', 'base model': 'base model', 'paused': 'paused'}
    last = {}
    for y in pr: last[y['seat']] = y
    rows = []
    for st in d.get('seats') or []:
        y = last.get(st['seat'])
        rows.append([st['seat'], ('%d%% to %d%%' % (round(100 * y['grounded'][0]), round(100 * y['grounded'][1]))) if y else '\u2014',
                     (short(st['seat'], y['ts']) + ', ' + ago(y['ts'])) if y else 'no test yet',
                     NOW.get(st.get('stage'), st.get('stage') or ''), SERV.get(st.get('status'), st.get('status') or '')])
    H['iris/lab']['table'] = dict(cols=['Seat', 'Quoted claims, base to adapter', 'Last test', 'Now', 'Serving'], rows=rows,
                                  note='Cycle %d of the council. Every turn collects examples, trains a LoRA adapter, then tests it against its own base model on held-out prompts. Updated %s UTC. Every result is also in the public repository.' % (d.get('cycle') or 0, d['updated'][11:16]),
                                  cta=dict(text='Watch every turn live', href='/iris/lab/live', rest=' Results as data: ', link2='GitHub', href2='https://github.com/Heuremen-LLC/council/tree/main/results', tail='.'))
def iris():
    d = feed('hosts'); add('iris', f(d['endpoints']), 'host endpoints serve %d open-weight models. %d were flagged by OpenRouter or showed 5-minute uptime below 100 percent at the last read, %s UTC.' % (d['models'], d['problems_now'], d['updated'][-5:]))
def water():
    # 10 Nov 2026: WATER (ATLAS). The six-month band cells against the 80 percent Reclamation states in its Minimum and Maximum reports, with the plan’s
    # intervals, the Most Probable cells read against a median (our reading), and the ruler note where an after-data ruler gives another outcome.
    d = feed('water'); h = d['headline_lead6']; m, p = h['mead'], h['powell']; OC = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell'}
    def dep(b): return any(v.get(k) and v[k] != b['outcome'] for v in (b.get('checks_after_data') or {}).values() for k in ('outcome', 'outcome_unrounded'))
    em, ep = round(0.8 * m['band']['n']), round(0.8 * p['band']['n'])
    seg = lambda b, nm: '%d to %d percent for %s' % (round(100 * b['lo']), round(100 * b['hi']), nm) + (', whose reading depends on the ruler' if dep(b) else '')
    sm, sp = seg(m['band'], 'Lake Mead'), seg(p['band'], 'Lake Powell')
    mo, po = m['mp']['outcome'], p['mp']['outcome']
    tell = lambda o, r=None: ('cannot tell' + (' (%s)' % r if r else '')) if o == 'CANNOT_TELL' else 'read ' + OC.get(o, o.lower())   # 12 Nov 2026: the closed reason beside cannot tell
    rm, rp = m['mp'].get('reason'), p['mp'].get('reason')
    rq = ''.join(' %s %s' % (nm, x['req13']['line']) for nm, x in (('Lake Mead band at six months:', m['band']), ('Lake Powell band at six months:', p['band'])) if x.get('req13'))   # REQ-13 beside the headline cells
    add('water', '%d of %d' % (m['band']['inside'], m['band']['n']),
        'Lake Mead end-of-month levels measured six months after a 24-Month Study fell inside the range between its Probable Minimum and Probable Maximum projections. Lake Powell: %d of %d. '
        'Reclamation’s reports say \u201cThere is approximately an 80%% probability that a future elevation will fall inside the range of the minimum and maximum inflow scenarios.\u201d '
        'At that rate about %s would have. Counted on water years, the 95%% intervals are %s%s%s. '
        'Six months ahead the lake ended above the Most Probable projection in %d of %d Lake Mead and %d of %d Lake Powell projections. Read against a median, which is an indahl.ai reading, %s.%s'
        % (p['band']['inside'], p['band']['n'], ('%d of each' % em) if em == ep else ('%d and %d' % (em, ep)), sm, ', and ' if dep(m['band']) else ' and ', sp,
           m['mp']['above'], m['mp']['n'], p['mp']['above'], p['mp']['n'], ('both ' + tell(mo, rm)) if (mo, rm) == (po, rp) else ('Lake Mead %s and Lake Powell %s' % (tell(mo, rm), tell(po, rp))), (' Rows behind the band cells,' + rq) if rq else ''))
def solar():
    # 10 Nov 2026: SOLAR (ATLAS). The line comes from solar_index/solar_headline.py, the same function that writes the page (PLAN headline row: M-class flares, day one).
    import sys as _s; _s.path.insert(0, B + '/solar_index'); from solar_headline import headline
    big, line = headline(feed('solar')); add('solar', big, line)
def tornado():
    # 10 Nov 2026: TORNADO (HERMES). The line comes from tornado_index/tornado_headline.py, the same function that writes the page.
    import sys as _s; _s.path.insert(0, B + '/tornado_index'); from tornado_headline import headline as _h
    big, line = _h(feed('tornado')); add('tornado', big, line)
def deus():
    # 22 Nov 2026: DEUS (HERMES). The line comes from deus_index/deus_headline.py, the same function that writes the page.
    import sys as _s; _s.path.insert(0, B + '/deus_index'); from deus_headline import headline as _h
    big, line = _h(feed('deus')); add('deus', big, line)
def prometheus():
    # 21 Nov 2026: PROMETHEUS (HERMES). The line comes from prometheus_index/prometheus_headline.py, the same function that writes the page.
    import sys as _s; _s.path.insert(0, B + '/prometheus_index'); from prometheus_headline import headline as _h
    big, line = _h(feed('prometheus')); add('prometheus', big, line)
def ares():
    # 22 Nov 2026: ARES (HERMES). The line comes from ares_index/ares_headline.py, the same function that writes the page. Off the home banner until the referee reads the first run.
    import sys as _s; _s.path.insert(0, B + '/ares_index'); from ares_headline import headline as _h
    big, line = _h(feed('ares')); add('ares', big, line)
def voightkampff():
    # 21 Nov 2026: VOIGHT-KAMPFF (HERMES). The line comes from voightkampff_index/vk_headline.py, the same function that writes the page. Off the home banner.
    import sys as _s; _s.path.insert(0, B + '/voightkampff_index'); from vk_headline import headline as _h
    big, line = _h(feed('voightkampff')); add('voightkampff', big, line)
def argus():
    # 22 Nov 2026: ARGUS (HERMES). The line comes from argus_index/argus_headline.py, the same function that writes the page. Off the home banner until the referee reads the first run.
    import sys as _s; _s.path.insert(0, B + '/argus_index'); from argus_headline import headline as _h
    big, line = _h(feed('argus')); add('argus', big, line)
def credit():
    # 10 Nov 2026: CREDIT (HERMES). The line comes from credit_index/credit_headline.py, the same function that writes the page.
    import sys as _s; _s.path.insert(0, B + '/credit_index'); from credit_headline import headline as _h
    big, line = _h(feed('credit')); add('credit', big, line)
def flu():
    # 10 Nov 2026: FLU (HERMES). The line comes from flu_index/flu_headline.py, the same function that writes the page.
    import sys as _s; _s.path.insert(0, B + '/flu_index'); from flu_headline import headline as _h
    big, line = _h(feed('flu')); add('flu', big, line)
def steo():
    # 10 Nov 2026: STEO (HERMES). The line comes from steo_index/steo_headline.py, the same function that writes the page.
    import sys as _s; _s.path.insert(0, B + '/steo_index'); from steo_headline import headline as _h
    big, line = _h(feed('steo')); add('steo', big, line)
def seasonal():
    # 10 Nov 2026: SEASONAL (HERMES). The line comes from seasonal_index/seasonal_headline.py, the same function that writes the page.
    import sys as _s; _s.path.insert(0, B + '/seasonal_index'); from seasonal_headline import headline as _h
    big, line = _h(feed('seasonal')); add('seasonal', big, line)
def neo():
    # 10 Nov 2026: NEO (ATLAS). The line comes from neo_index/neo_headline.py, the same function that writes the page, so the page and this headline
    # say the same thing: the plan’s all-leads cell, the split by lead, and the dependence on one archived copy (referee R4, neo_index_referee/REFEREE.md).
    import sys as _s; _s.path.insert(0, B + '/neo_index'); from neo_headline import headline
    big, line = headline(feed('neo')); add('neo', big, line)
def cone():
    # 10 Nov 2026: CONE (ATLAS). The line comes from cone_index/cone_headline.py, the same function that writes the page. Headline cell fixed in cone_index/PLAN.md.
    import importlib.util as _u
    sp = _u.spec_from_file_location('cone_headline', B + '/cone_index/cone_headline.py'); m = _u.module_from_spec(sp); sp.loader.exec_module(m)
    big, line = m.headline(feed('cone')); add('cone', big, line)
def census():
    # 11 Nov 2026: CENSUS. The line comes from census_index/census_headline.py, the same function that writes the desk page.
    import sys as _s; _s.path.insert(0, B + '/census_index'); from census_headline import headline
    big, line = headline(feed('census')); add('census', big, line)
def quake():
    # 10 Nov 2026: QUAKE (ATLAS). The line comes from quake_index/quake_headline.py, the same function that writes the page.
    import sys as _s; _s.path.insert(0, B + '/quake_index'); from quake_headline import headline
    big, line = headline(feed('quake')); add('quake', big, line)
def petrol():
    # 21 Nov 2026 (division pages read every desk from headlines.json): PETROL's own headline from its feed (petrol_index, KV petrol_live)
    d = feed('petrol'); add('petrol', d['headline']['big'], d['headline']['line'])
def rank():
    d = feed('rank'); add('rank', d['headline']['big'], d['headline']['line'])
def social():
    d = feed('social'); add('social', d['headline']['big'], d['headline']['line'])
def hflicense():
    d = feed('hflicense'); m = d['comparison']['Models']; ds = d['comparison']['Datasets']
    add('hflicense', '%d of %d' % (m['n'], m['of']), 'popular Hugging Face models with a license tag and a license file of the same comparable family carry a file that names another license. Datasets: %d of %d.' % (ds['n'], ds['of']))
for n, fn in list(globals().items()):
    if callable(fn) and n in ('airq', 'hosts', 'airline', 'weights', 'ailuminate', 'campus', 'hpt', 'secrecords', 'hfsize', 'pkglicense', 'tape', 'support', 'trials', 'revise', 'fedsep', 'change', 'cadence', 'linkrot', 'launch', 'pkginstall', 'oy', 'qia', 'iris', 'atlas', 'water', 'neo', 'quake', 'census', 'solar', 'cone', 'tornado', 'voightkampff', 'prometheus', 'ares', 'deus', 'argus', 'credit', 'flu', 'steo', 'seasonal', 'lab', 'petrol', 'rank', 'social', 'hflicense'): safe(n, fn)
# 21 Nov 2026 (HS, site/HEADLINE_SPLIT.md on lane-pod, design by the designer, credit the referee): on the 11 pages whose top is one long live line, the entry also
# carries a short reading (one sentence, 120 characters or fewer, the number and what it measures), the method (source, window, scoring rule),
# the figure (the big number) and as_of (the feed stamp, ISO UTC). The long line stays in 'line', and headline.js and build_site.py draw it under
# the method as the full reading, so every number it carries stays on the page. Every number here comes from the same feed fields the desk's own
# headline function reads. An entry that fails a writer check gets no reading, and the page draws the long line as before.
import importlib.util as _hs_u
def _hs_mod(name):
    sp = _hs_u.spec_from_file_location(name, B + '/heuremen-specbook/%s.py' % name); m = _hs_u.module_from_spec(sp); sp.loader.exec_module(m); return m
HS_MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
HS_OC = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell'}
def _hs_rw(c): return HS_OC.get(c['outcome'], c['outcome'].lower()) + ((' (%s)' % c['reason']) if c['outcome'] == 'CANNOT_TELL' and c.get('reason') else '')
def _hs_pc(x): return '%.1f' % (100 * x)
def _hs_day(iso): y, m, dd = iso[:10].split('-'); return '%d %s %s' % (int(dd), HS_MON[int(m) - 1], y)
def _hs_month(ym): return '%s %s' % (HS_MON[int(ym[5:7]) - 1], ym[:4])
# 21 Nov 2026 (BT, site/HEADLINES_PICK.md on lane-site, picks by the designer): every desk with a pick carries reading/figure/method/as_of. A pick that
# changes the headline cell sets big to the new figure; the old big is kept in front of a line that continued it, so the full reading still reads.
_HS_SMON = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
def _hs_iso(v):
    """Feed stamps: '2026-11-21T20:38:08Z', '2026-11-21 20:38', '2026-11-21 21:35 UTC', '21 Nov 21:42' (UTC, year from the clock as in ledger/live_headlines.py stamp_epoch)."""
    v = str(v or '').strip()
    if re.match(r'^\d{4}-\d{2}-\d{2}$', v): return v
    m = re.match(r'^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})(:\d{2})?', v)
    if m: return '%sT%s%sZ' % (m.group(1), m.group(2), m.group(3) or ':00')
    m = re.match(r'^(\d{1,2}) ([A-Za-z]{3}) (\d{2}):(\d{2})', v)
    if m and m.group(2).lower() in _HS_SMON:
        import calendar; now = time.time(); y = time.gmtime(now).tm_year
        t = calendar.timegm((y, _HS_SMON.index(m.group(2).lower()) + 1, int(m.group(1)), int(m.group(3)), int(m.group(4)), 0))
        if t > now + 3600: y -= 1
        return '%d-%02d-%02dT%s:%s:00Z' % (y, _HS_SMON.index(m.group(2).lower()) + 1, int(m.group(1)), m.group(3), m.group(4))
    return None
def _hs_dm(v):   # '07 Nov 00:11 UTC' or '20261029T1808' or an ISO date, as '7 November 2026'
    i = _hs_iso(v) or (('%s-%s-%s' % (v[:4], v[4:6], v[6:8])) if re.match(r'^\d{8}', str(v)) else None)
    return _hs_day(i) if i else None
def _hs_n(x): return '{:,}'.format(int(x))
def _hs_p0(x): return '%d%%' % round(100 * x)
def _hs_solar(d):
    import sys as _s; _s.path.insert(0, B + '/solar_index'); import solar_headline as sh
    c = sh.cell(d, 'M', 1); bs = sh.counted(c, d['frame']['min_n']); ab = [b for b in bs if b['outcome'] == 'ABOVE']
    meth = ('NOAA SWPC’s daily report as first published since %s, set beside the flares that followed, bin by bin of the stated chance, with at least %d days in a bin; a bin reads cannot tell when the interval on its share of flare days holds the stated chance, a point figure with no tolerance.'
            % (_hs_day(d['frame']['first_issue']), d['frame']['min_n']))
    if ab:
        fig = '%d of %d' % (len(ab), len(bs)); b = ab[0]
        return dict(fig=fig, big=True, method=meth, reading='In %s bins of NOAA’s next-day M-class flare odds, flares came more often than forecast, %s%% of days at %s%%.' % (fig, sh.pc(b['observed']), sh.pc(b['mean_stated'], 0)))
    ct = [b for b in bs if b['outcome'] in ('CANNOT_TELL', 'CONSISTENT')]; fig = '%d of %d' % (len(ct), len(bs))
    return dict(fig=fig, method=meth, reading='NOAA SWPC’s next-day M-class flare odds read cannot tell in %s bins.' % fig)
def _hs_cone(d):
    import importlib.util as _u
    sp = _u.spec_from_file_location('cone_headline', B + '/cone_index/cone_headline.py'); m = _u.module_from_spec(sp); sp.loader.exec_module(m)
    al = d['cells'][0]; fig = '{:,} of {:,}'.format(al['inside'], al['scored']); bd = d['claim']['whole_path_band']
    return dict(fig=fig, reading='NHC states %d to %d percent; the storm center stayed inside the Atlantic cone all five days in %s cases.' % (round(100 * bd[0]), round(100 * bd[1]), fig),
                method='National Hurricane Center official Atlantic track forecasts, seasons %s, set beside the post-season best track, with a 95 percent interval resampled by storm; against the %d to %d percent NHC states, the share, %s percent, reads %s.'
                % (m.seasons_phrase(d), round(100 * bd[0]), round(100 * bd[1]), _hs_pc(al['share']), _hs_rw(al)))
def _hs_census(d):
    import sys as _s; _s.path.insert(0, B + '/census_index'); import census_headline as ch
    c = ch.cell(d, 'SALES', 'S1'); fig = '%d of %d' % (c['inside'], c['scored'])
    return dict(fig=fig, reading='At the second print, new home sales sat inside the first print’s 90 percent interval in %s months.' % fig,
                method='Census Bureau first prints of new home sales, housing starts, housing completions and advance retail sales, each set beside the value after one revision, two, and today, and read against the 90 percent figure with no tolerance; new home sales, %s to %s, reads %s.'
                % (_hs_month(c['first_month']), _hs_month(c['last_month']), ch.reading(c).replace('a share ', '', 1)))
def _hs_neo(d):
    near = d['cells'][1]; fig = '%d of %d' % (near['inside'], near['scored'])
    return dict(fig=fig, reading='JPL’s latest orbit solution put %s near-Earth passes inside the 3-sigma range JPL gave 0 to 7 days ahead.' % fig,
                method='NASA/JPL close-approach ranges for approaches since %s, copied at the time by the Internet Archive and by this desk, set beside the distance from the latest orbit solution, with a 95 percent interval on the share inside; the 0 to 7 day cell reads %s.'
                % (_hs_day(d['frame']['approach_from']), _hs_rw(near)))
def _hs_quake(d):
    A = d['described']['stated_10_percent_or_more_all']; fig = '%s%%' % _hs_pc(A['share'])
    return dict(fig=fig, big=True, reading='Where USGS gave at least a 10 percent chance of a later quake, one came in %s of windows, against %s%% stated.' % (fig, _hs_pc(A['stated_mean'])),
                method='USGS Operational Aftershock Forecasts for sequences since %s, each closed window where the stated chance of at least one was 10 percent or more set beside the USGS catalog, %s of %s windows, with a 95 percent interval that resamples whole groups of sequences; against a mean stated %s percent it reads %s.'
                % (_hs_month(d['sources']['first_event'][:7]), _hs_n(A['occurred']), _hs_n(A['scored']), _hs_pc(A['stated_mean']), _hs_rw(A)))
def _hs_flu(d):
    import sys as _s; _s.path.insert(0, B + '/flu_index'); import flu_headline as fh
    a = fh.cell(d, 'all horizons', '95'); fig = '%s%%' % _hs_pc(a['share'])
    return dict(fig=fig, big=True, reading='Weekly flu hospital admits fell inside CDC FluSight’s 95%% range %s of the time; %s%% ran above it, %s%% below.' % (fig, _hs_pc(a['share_above']), _hs_pc(a['share_below'])),
                method='CDC FluSight ensemble 95 percent quantile ranges, 0 to 3 weeks ahead, reference dates %s to %s, set beside the latest NHSN weekly count, %s of %s, with a %d-week block bootstrap 95 percent interval; the share reads %s.'
                % (_hs_day(d['sources']['first_reference_date']), _hs_day(d['sources']['last_reference_date']), fh.f(a['inside']), fh.f(a['scored']), d['frame']['block_weeks'], _hs_rw(a)))
def _hs_seasonal(d):
    import sys as _s; _s.path.insert(0, B + '/seasonal_index'); import seasonal_headline as sh
    t = sh.cell(d, 'temperature, leaning'); fig = '%s%%' % _hs_pc(t['observed'])
    return dict(fig=fig, reading='Where CPC gave a temperature category 40 percent or more, averaging %s percent, it came in %s of grid cells.' % (_hs_pc(t['mean_stated']), fig),
                method='NOAA Climate Prediction Center 3-month outlooks at 0.5-month lead, %s to %s, on its 2 by 2 degree grid, set beside CPC’s verification archive, with a %d-season block bootstrap 95 percent interval; the share reads %s.'
                % (d['sources']['first_season'], d['sources']['last_season'], d['frame']['block_seasons'], _hs_rw(t)))
def _hs_water(d):
    h = d['headline_lead6']; m, p = h['mead'], h['powell']; fig = '%d of %d' % (m['band']['inside'], m['band']['n'])
    return dict(fig=fig, reading='Reclamation states about 80 percent; six months on, Lake Mead sat inside its range in %s cases, Lake Powell %d.' % (fig, p['band']['inside']),
                method='Reclamation 24-Month Study projections since %s, each set beside the end-of-month elevation six months later and read against the 80 percent its reports state, with 95 percent intervals counted on water years of %d to %d percent for Lake Mead and %d to %d percent for Lake Powell.'
                % (d['coverage']['first_issue'][:4], round(100 * m['band']['lo']), round(100 * m['band']['hi']), round(100 * p['band']['lo']), round(100 * p['band']['hi'])))
def _hs_steo(d):
    import sys as _s; _s.path.insert(0, B + '/steo_index'); import steo_headline as sh
    w = sh.cell(d['cells'], 'WTI', 'all leads'); fig = '%s of %s' % (sh.f(w['inside']), sh.f(w['scored']))
    iss = lambda x: '%s 20%s' % (x[:1].upper() + x[1:3], x[3:5])
    return dict(fig=fig, reading='WTI’s monthly price landed inside EIA’s 95 percent range in %s months, %s.' % (fig, 'and never above it' if not w['above'] else 'above it in %s percent' % _hs_pc(w['share_above'])),
                method='EIA Short-Term Energy Outlook 95 percent NYMEX futures price ranges, from the %s issue to the %s issue, set beside EIA’s monthly average WTI Cushing spot price, with a %d-month block bootstrap 95 percent interval; the share, %s percent, reads %s.'
                % (iss(d['sources']['first_issue']), iss(d['sources']['last_issue']), d['frame']['block_months'], _hs_pc(w['share']), _hs_rw(w)))
def _hs_oy(d):
    c = d['counts']; fig = '%d of %d' % (c['original_rule'], c['read']); m = re.search(r'We read each school on (\d{1,2} [A-Z][a-z]+ \d{4})', d['line'])
    pol = re.search(r'which counts only a policy, guidance or a tool a central office provides, (.+?) of %d had' % c['read'], d['line'])
    return dict(fig=fig, as_of=None, reading='%s listed colleges and universities had published a measured grade or outcome of their own AI policy or tool.' % fig,
                method='Each listed school’s public pages, read on %s, for a measured grade or outcome of its own AI policy, guidance, tool or pilot, by the rule written before any school was read; by a narrower rule set after the first 41 schools, %s of %d had.'
                % (m.group(1), pol.group(1), c['read']))
def _hs_airq(d):
    L = d['live']; c = L['comparison']; r = c['Map reading (atm channels, raw)']; k = c['cf_1 corrected for humidity (Barkjohn 2021)']; fig = '%d of %d' % (r['n'], r['of'])
    return dict(fig=fig, big=True, as_of=_hs_iso(L['updated']),
                reading='%s EPA monitors had a nearby PurpleAir sensor miss the EPA target on the raw map reading; %d of %d when corrected.' % (fig, k['n'], k['of']),
                method='PurpleAir sensors near the %d EPA monitors with at least 30 kept days in %s, read through %s, each set beside the monitor’s preliminary AirNow values and read against the EPA accuracy targets with a 95 percent Wilson interval; the raw map reading reads %s and the humidity-corrected reading %s.'
                % (r['of'], L['window'], _hs_day(L['sensor_days_through']), _hs_rw(r), _hs_rw(k)))
def _hs_hosts(d):
    one = d['models_by_hosts']['1 host']; fig = '%d of %d' % (one, d['models'])
    return dict(fig=fig, big=True, reading='%s open-weight models on OpenRouter are served by only one host.' % fig,
                method='OpenRouter’s endpoint list, polled since %s, each model counted by the hosts serving it at the latest read; at that read %d of %s endpoints were flagged by OpenRouter or below 100 percent five-minute uptime.'
                % (_hs_dm(d['first_poll']), d['problems_now'], _hs_n(d['endpoints'])))
def _hs_iris(d):
    return dict(fig=_hs_n(d['endpoints']), reading='%s host endpoints serve %d open-weight models; %d of those models have only one host.' % (_hs_n(d['endpoints']), d['models'], d['models_by_hosts']['1 host']),
                method='OpenRouter’s endpoint list, polled since %s; at the latest read %d endpoints were flagged by OpenRouter or showed five-minute uptime below 100 percent.' % (_hs_dm(d['first_poll']), d['problems_now']))
def _hs_trials(d):
    a = d['all']; dv = d['by_kind']['device_only']; fig = '%s%%' % _hs_pc(a['share_no_results'])
    return dict(fig=fig, as_of=_hs_iso(d['read']), reading='%s of FDA-regulated trials 15 months past completion post no results; device-only, %s of %s.' % (fig, _hs_n(dv['no_results']), _hs_n(dv['n'])),
                method='ClinicalTrials.gov records of FDA-regulated drug and device trials with primary completion on or before %s, %s of %s read with no results posted, with a 95 percent interval; records 13 to 15 months past completion are shown apart and not scored, and the share reads %s.'
                % (_hs_day(d['cutoff']), _hs_n(a['no_results']), _hs_n(a['n']), _hs_rw(a)))
def _hs_hpt(d):
    k = '1 A cms-hpt.txt at the root of the domain'; c = d['comparison'][k]; fig = '%d of %d' % (c['n'], c['of'])
    return dict(fig=fig, big=True, reading='%s reachable hospital domains have no cms-hpt.txt at their root, the file the federal rule asks for.' % fig,
                method='Hospital websites on the list of %s, each reachable domain read for cms-hpt.txt at its root; %d that are a page on a shared site are left out, because a root file cannot apply to them, and with no figure stated to read the share against it reads %s.'
                % (_hs_day(d['listdate']), d['not_comparable_reasons']['website is a page on a shared site']['n'], _hs_rw(c)))
def _hs_support(d):
    a = d['all']; fig = _hs_p0(a['share'])
    return dict(fig=fig, reading='%s of release cycles listed as supported had no release in more than a year, %d of %d.' % (fig, a['unreleased'], a['tested']),
                method='endoflife.date, read every pass, each cycle it lists as supported set beside the date of its newest release, with a 95 percent interval over products; the share reads %s.' % _hs_rw(a))
def _hs_fedsep(d):
    P = d['pooled']; t = [v for k, v in P.items() if k.startswith('This')][0]; n = [v for k, v in P.items() if k.startswith('Next')][0]; fig = '%d of %d' % (t['outside'], t['triples'])
    return dict(fig=fig, big=True, reading='The Fed’s September projections for the current year landed outside its own 70 percent range %s times.' % fig,
                method='Federal Reserve September Summaries of Economic Projections with outcomes in hand, each set beside the outcome and its stated 70 percent range, with a 95 percent interval over years; against the 30 percent the range leaves outside, the share reads %s, and next year, %d of %d, reads %s.'
                % (_hs_rw(t), n['outside'], n['triples'], _hs_rw(n)))
def _hs_ailuminate(d):
    h = d['headline']; fig = '%d of %d' % (h['n'], h['of'])
    return dict(fig=fig, reading='%s systems on MLCommons AILuminate’s results page disagree with their own detailed reports.' % fig,
                method='The results page and each system’s detailed report, read %s times, with a 95 percent interval of %s to %s percent; against the 5 percent that would matter it reads %s.'
                % (_hs_n(d['reads']), ('%g' % round(100 * h['share_lo'], 1)), ('%g' % round(100 * h['share_hi'], 1)), _hs_rw(h)))
def _hs_weights(d):
    e = d['ever']; h = d['headline']; fig = '%d of %s' % (e['n'], _hs_n(e['of']))
    return dict(fig=fig, reading='%s popular Hugging Face models changed their weight files on at least one read.' % fig,
                method='Each model’s weight files on Hugging Face, read every pass (pass %d), each set beside the read before; %d of %s changed between the last two passes.' % (d['pass_number'], h['n'], _hs_n(h['of'])))
def _hs_campus(d):
    s = d['state_now']; fig = '%d of %d' % (s['Opens (HTTP 200)'], d['sources'])
    return dict(fig=fig, reading='%s sources behind the OY page open today.' % fig,
                method='Each source the OY page cites, read every pass (pass %d); %d are not found and %d refuse automated reads.' % (d['pass_number'], s['Not found (404, 410)'], s['Blocked (401, 403, 429)']))
def _hs_secrecords(d):
    a = d['comparison']['HSTS preload header']; fig = _hs_p0(a['share'])
    return dict(fig=fig, reading='%s of top sites that send an HSTS preload header miss the preload list’s own requirements, %d of %d.' % (fig, a['n'], a['of']),
                method='The top %s domains on the list of %s, each HTTPS response read for its HSTS header and set beside the preload list’s stated requirements, with a 95 percent interval; the share reads %s.' % (_hs_n(d['domains']), _hs_day(d['listdate']), _hs_rw(a)))
def _hs_hfsize(d):
    c = d['comparison']; fig = '%d of %d' % (c['n'], c['of'])
    return dict(fig=fig, reading='%s popular Hugging Face models weigh outside the size in their name.' % fig,
                method='Models whose name states a size, each set beside the parameter count in its weight files, with a 95 percent interval; the share, %d percent, reads %s.' % (round(100 * c['share']), _hs_rw(c)))
def _hs_pkglicense(d):
    c = d['disagree']; fig = '%d of %d' % (c['n'], c['of'])
    return dict(fig=fig, reading='%s PyPI projects state a license that differs from the one GitHub reports for their repository.' % fig,
                method='Popular PyPI projects with a GitHub repository, each license read in full on both, with a 95 percent interval; %d of %s are not comparable, and the share, %d percent, reads %s.'
                % (d['classes']['NOT_COMPARABLE']['n'], _hs_n(d['read']), round(100 * c['share']), _hs_rw(c)))
def _hs_pkginstall(d):
    c = d['comparison']; tot = sum(v['n'] for v in d['classes'].values()); fig = '%d of %d' % (c['of'] - c['n'], c['of'])
    return dict(fig=fig, reading='%s install commands in popular Python packages work on a clean install.' % fig,
                method='The pip install line in each project’s description, run in a clean environment with pip %s; %d of %s projects have no such line and are not counted.'
                % (d['pip'], d['not_comparable_reasons']['no pip install line in the description']['n'], _hs_n(tot)))
def _hs_revise(d):
    k = [v for kk, v in d['counts'].items() if kk.startswith('Most recent')][0]; fig = '%d of %d' % (k['exceed'], k['months'])
    ym = lambda s: '%s %s' % (HS_MON[int(s[5:7]) - 1], s[:4])
    return dict(fig=fig, reading='%s monthly payroll numbers moved by more than the BLS’s stated margin once benchmarked.' % fig,
                method='BLS first prints of the monthly payroll change, %s to %s, set beside the benchmarked figure, with a 95 percent interval over months; against the BLS’s stated margin it reads %s.' % (ym(k['first']), ym(k['last']), _hs_rw(k)))
def _hs_change(d):
    L = d['lifespan']; g = L['Google, names with preview']; o = L['Google, other names']; fig = '%d of %d' % (g['under180'], g['n'])
    return dict(fig=fig, reading='%s Google preview models with a shutdown date ran under six months; %d of %d other Google models did.' % (fig, o['under180'], o['n']),
                method='Google’s published model shutdown dates, read since %s, each model’s release set beside its stated shutdown date; the median is %g days for previews and %g for the rest.' % (_hs_day(d['first_snapshot']), g['median'], o['median']))
def _hs_cadence(d):
    t = d['totals']; m = d['most_overdue'][0]; fig = '%s of %s' % (_hs_n(t['below']), _hs_n(t['readable']))
    return dict(fig=fig, big=True, reading='%s readable US government data series are behind the update schedule they state.' % fig,
                method='US government data series that state an update frequency, each last-modified date set beside its stated cadence, behind when its age is more than twice that interval; the most overdue%s was last modified %.1f years ago.'
                % (', stated daily,' if m.get('cadence') == 'R/P1D' else '', m['age_days'] / 365.25))
def _hs_linkrot(d):
    a = d['all']; fig = '%s%%' % _hs_pc(a['rot_share'])
    return dict(fig=fig, reading='%s of code and data links in arXiv papers are gone, %d of %s.' % (fig, a['gone'], _hs_n(a['links'])),
                method='Each code or data link in the arXiv papers read, opened, with a 95 percent interval; %s are live, %s of %s papers carry a link, and the share reads %s.'
                % (_hs_n(a['live']), _hs_n(d['papers_with_a_link']), _hs_n(d['papers']), _hs_rw(a)))
def _hs_launch(d):
    c1 = next(c for c in d['cells'] if c['who'] == 'All providers' and c['lead'] == '1 day'); c7 = next(c for c in d['cells'] if c['who'] == 'All providers' and c['lead'] == '7 days')
    fig = '%d of %d' % (c1['n'] - c1['over_24h'], c1['n']); same = _hs_rw(c1) == _hs_rw(c7)
    return dict(fig=fig, big=True, reading='Stated a day ahead, %s launches flew within 24 hours; stated a week ahead, %d of %d slipped more than a day.' % (fig, c7['over_24h'], c7['n']),
                method='Each launch’s stated time, read as it stood one and seven days before, set beside the time it flew, for launches first read before they flew (%d so far); a week out the median slip was %g hours, and %s.'
                % (d['flown_watched'], c7['median_abs_slip_h'], ('both cells read ' + _hs_rw(c1)) if same else ('the one-day cell reads %s and the seven-day cell %s' % (_hs_rw(c1), _hs_rw(c7)))))
def _hs_tape(d):
    h = d['head']; b = d['beacon']; fig = H['tape']['big']
    return dict(fig=fig, as_of=_hs_iso(h['t']), reading='%s since the newest entry was chained to the tape.' % fig,
                method='Each entry is hashed onto the one before, and the beacon now begins %s.' % b['value'][:8])
def _hs_lab(d):
    v7 = [r for r in d if r.get('model') == 'v7']; ex = sum(r['score'] == 1.0 for r in v7); fig = '%d%%' % round(100 * ex / len(v7))
    return dict(fig=fig, as_of=_hs_iso(max(r['read'] for r in v7)), reading='YO v7’s flags matched the code’s answer on %s of new IBM calibration records since %s, %s of %s.' % (fig, _hs_dm(min(r['read'] for r in v7)).rsplit(' ', 1)[0], _hs_n(ex), _hs_n(len(v7))),
                method='Each new IBM calibration record as IBM publishes it, read by YO v7 and by code, a match when both flag exactly the same qubits.')
def _hs_tornado(d):
    p = d['warnings']['pooled']; pod = p['pod']; ld = p['lead_min']; fig = '%s%%' % _hs_pc(pod['value']); lab = p['label'].replace('FY', '')
    return dict(fig=fig, big=True, reading='NWS warnings were in force for %s of touchdowns, fiscal %s, against a %d percent goal.' % (fig, lab, round(100 * pod['goal'])),
                method='NWS warning verification, %s, each tornado set beside the warnings in force, with a 95 percent interval; detection reads %s against the %d percent goal, and mean lead time, %g minutes against a %g-minute goal, reads %s.'
                % (p['label'], _hs_rw(pod), round(100 * pod['goal']), ld['value'], ld['goal'], _hs_rw(ld)))
def _hs_credit(d):
    r = next(x for x in d['ruler1'] if x['year'] == 2025); fig = H['credit']['big']
    tail = 'too close to tell apart' if r['outcome'] == 'CANNOT_TELL' else 'which reads ' + _hs_rw(r)
    return dict(fig=fig, reading='The CFPB printed %s of 2025 complaints answered on time; its own database shows %s, %s.' % (r['printed'], fig, tail),
                method='The CFPB public database, cases received in 2025, timely share set beside the %s the CFPB printed, with a company-month block bootstrap 95 percent interval; against the band the printed figure allows it reads %s.' % (r['printed'], _hs_rw(r)))
def _hs_petrol(d):
    o = d['opec']; c = o['counts']; fig = '%d below' % c['BELOW']
    return dict(fig=fig, big=True, reading='OPEC+ output for %s: %s the required level by more than OPEC’s revision width, %d above, %d inside.' % (_hs_month(o['month']), fig, c['ABOVE'], c['CONSISTENT']),
                method='OPEC’s secondary-source production figure for each of the %d OPEC+ members, set beside the required production level OPEC+ states and read against OPEC’s own revision width; %d could not be read.' % (o['members'], c['CANNOT_TELL']))
def _hs_rank(d):
    h = d['headline']; fig = h['big']
    return dict(fig=fig, reading='%s US News figures differ from the public record after rounding, among those compared for the same year.' % fig,
                method='US News education ranking figures set beside state report cards, federal school and college data and schools’ own reports for the same year; %s more read cannot tell.' % _hs_n(h['req13']['cannot_tell']))
def _hs_social(d):
    fig = d['headline']['big']
    return dict(fig=fig, as_of=_hs_iso(d['checked']), reading='%s matched committees and cycles read above, below or consistent on Google ad spend against FEC filings.' % fig,
                method='Google’s stated election ad spend for each political committee and cycle, set beside the committee’s FEC filings, counted where the outcome holds under both timing bands and rests on an FEC ID match alone.')
def _hs_hflicense(d):
    m = d['comparison']['Models']; ds = d['comparison']['Datasets']; fig = '%d of %d' % (m['n'], m['of'])
    return dict(fig=fig, reading='%s popular Hugging Face models carry a license file that names another license than their license tag.' % fig,
                method='The most downloaded Hugging Face models and datasets, the license tag set beside the license file where both name a comparable family, with a 95 percent Wilson interval; models read %s, and datasets, %d of %d, read %s.' % (_hs_rw(m), ds['n'], ds['of'], _hs_rw(ds)))
def _hs_check(slug, fig, reading, method, h1):
    ts = _hs_mod('tone_scan'); cs = _hs_mod('count_scan'); bad = []
    for nm, t in (('reading', reading), ('method', method)):
        for a in ts.ARGUE:
            if re.search(a, t, re.I): bad.append('%s argues: %s' % (nm, a))
        if '\'' in t or '"' in t: bad.append('%s has a straight quote' % nm)
        if not t.endswith('.') or len(re.findall(r'[.!?](?=\s|$)', t)) != 1: bad.append('%s is not one sentence ending in a period' % nm)
        if re.search(r'\d %', t): bad.append('%s has a space before %%' % nm)
    if len(reading) > 120: bad.append('reading is %d characters' % len(reading))
    if cs.COUNT.search(cs.clean(reading)): bad.append('reading counts our own things: %s' % cs.COUNT.search(cs.clean(reading)).group(0))
    if reading.count(fig) != 1: bad.append('figure %r is not in the reading once' % fig)
    stems = {w.lower()[:6] for w in re.findall(r'[A-Za-z]{6,}', h1 or '') if w.lower() not in ts.STOP}
    rep = sorted({w for w in re.findall(r'[A-Za-z]{6,}', reading) if w.lower() not in ts.STOP and w.lower()[:6] in stems})
    if rep: print('headlines: %s reading shares a word with the h1 (outside the hero, so not a header repeat; noted only): %s' % (slug, ', '.join(rep)))   # 21 Nov 2026 (BT): The designer's picks use the desk's own words; the header repeat rule reads the hero alone
    return bad
def _hs_h1(slug):
    p = B + '/indahl-ai/%s.html' % slug
    try: m = re.search(r'<section class="hero[^"]*">.*?<h1>(.*?)</h1>', open(p, encoding='utf-8').read(), re.S); return re.sub(r'<[^>]+>', ' ', m.group(1)) if m else ''
    except Exception: return ''
HS = {'solar': _hs_solar, 'cone': _hs_cone, 'census': _hs_census, 'neo': _hs_neo, 'quake': _hs_quake, 'flu': _hs_flu, 'seasonal': _hs_seasonal, 'water': _hs_water, 'steo': _hs_steo, 'oy': _hs_oy,
      'airq': _hs_airq, 'hosts': _hs_hosts, 'iris': _hs_iris, 'trials': _hs_trials, 'hpt': _hs_hpt, 'support': _hs_support, 'fedsep': _hs_fedsep, 'ailuminate': _hs_ailuminate, 'weights': _hs_weights,
      'campus': _hs_campus, 'secrecords': _hs_secrecords, 'hfsize': _hs_hfsize, 'pkglicense': _hs_pkglicense, 'pkginstall': _hs_pkginstall, 'revise': _hs_revise, 'change': _hs_change,
      'cadence': _hs_cadence, 'linkrot': _hs_linkrot, 'launch': _hs_launch, 'tape': _hs_tape, 'iris/lab': _hs_lab, 'tornado': _hs_tornado, 'credit': _hs_credit, 'petrol': _hs_petrol, 'rank': _hs_rank, 'social': _hs_social, 'hflicense': _hs_hflicense}
HS_H1 = {'census': ('census', 'census/revisions')}   # the CENSUS entry also draws /census/revisions, so its reading is read against both h1 lines
def _hs_load(s):
    if s == 'oy': return json.load(open(B + '/oy_index/matrix_page/oy_headline.json', encoding='utf-8'))
    if s == 'iris/lab': return [json.loads(l) for l in open(B + '/yo/live_reads.jsonl')]
    return feed('hosts' if s == 'iris' else s)
for _s, _fn in HS.items():
    if _s not in H: continue
    if _s == 'iris/lab' and H[_s].get('href') != '/yo': continue   # the YO lead only; the referee V seat headline keeps its long line
    try:
        _d = _hs_load(_s); _r = _fn(_d)
        _bad = [b for p in HS_H1.get(_s, (_s,)) for b in _hs_check(_s, _r['fig'], _r['reading'], _r['method'], _hs_h1(p))]
        if _bad: print('headlines: %s reading refused, the long line stands:' % _s, '; '.join(_bad)); continue
        if _r.get('big') and _r['fig'] != H[_s]['big']:
            if H[_s]['line'][:1].islower(): H[_s]['line'] = H[_s]['big'] + ' ' + H[_s]['line']   # the old figure stays in front of the line it began
            H[_s]['big'] = _r['fig']
        H[_s].update(reading=_r['reading'], figure=_r['fig'], method=_r['method'], as_of=_r['as_of'] if 'as_of' in _r else _hs_iso(_d.get('updated') if isinstance(_d, dict) else None))
    except Exception as e: print('headlines: %s reading skipped' % _s, type(e).__name__, str(e)[:80])
# division pages reuse the strongest desk beneath them
for dv, src in (('hermes', 'trials'),):
    if src in H: H[dv] = dict(H[src], href='/' + dv)
# 21 Nov 2026 (HARD row 26): the home banner desks and their order come from ledger/desks.json (on_home, home_order). If it cannot be read,
# the last published home list stays (watch/headlines.json), never an empty banner.
try: HOME = [d['id'] for d in sorted((d for d in json.load(open(B + '/ledger/desks.json'))['desks'] if d.get('on_home')), key=lambda d: d['home_order'])]
except Exception:
    try: HOME = json.load(open(B + '/watch/headlines.json')).get('home', [])
    except Exception: HOME = []
HOME = [s for s in HOME if s in H]
try: _HELD = set(json.load(open(os.path.expanduser('~/forge/reproduce_kits/held.json'))).get('held', []))   # 21 Nov 2026: a desk whose reproduce kit breaches leaves the home banner until it passes again (the gate no longer stops the whole site)
except Exception: _HELD = set()
try: _HELD |= set(json.load(open(os.path.expanduser('~/forge/ledger/live_held.json'))).get('held', []))   # 21 Nov 2026 (control audit #1): a desk whose live feed or field check_ledger could not read leaves the home banner
except Exception: pass
HOME = [s for s in HOME if s not in _HELD]
out = dict(updated=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), pages=H, home=HOME)
p = B + '/watch/headlines.json'; json.dump(out, open(p, 'w'), indent=1)
fp = hashlib.sha256(json.dumps(out['pages'], sort_keys=True).encode()).hexdigest()[:16]; st = B + '/watch/headlines_state.json'; prev = json.load(open(st)) if os.path.exists(st) else {}
if prev.get('fp') != fp or time.time() - prev.get('t', 0) > 3000:
    env = dict(os.environ, CLOUDFLARE_ACCOUNT_ID='<cloudflare-account-id>', PATH='/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin')
    r = _kv_put(['/opt/homebrew/bin/npx', 'wrangler', 'kv', 'key', 'put', 'headlines', '--path', p, '--namespace-id', NS, '--remote'], cwd=W, env=env, capture_output=True, text=True)
    if r.returncode == 0 and _PUBLISH: json.dump(dict(fp=fp, t=time.time()), open(st, 'w'))
    print('headlines:', len(H), 'pages', 'published' if r.returncode == 0 else 'publish FAILED')
    _pubfail = r.returncode != 0
else: print('headlines:', len(H), 'pages unchanged'); _pubfail = None
# rings on change only, so a standing fault rings once, not every tick (state in watch/.headlines_rung.json)
try:
    _rf = B + '/watch/.headlines_rung.json'; _was = json.load(open(_rf)) if os.path.exists(_rf) else {}
    _new = sorted(set(_SKIPPED) - set(_was.get('skipped', [])))
    if _new: _ring('skipped (desk headline threw, dropped from its page and the banner): ' + '; '.join('%s %s' % (k, _SKIPPED[k]) for k in _new))
    if _pubfail and not _was.get('pubfail'): _ring('publish FAILED (wrangler kv put headlines, exit %s)' % r.returncode)
    json.dump(dict(skipped=sorted(_SKIPPED), pubfail=_pubfail if _pubfail is not None else _was.get('pubfail', False)), open(_rf + '.tmp', 'w')); os.replace(_rf + '.tmp', _rf)
except Exception as e: print('headlines: ring state failed:', type(e).__name__)
