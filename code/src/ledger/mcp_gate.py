#!/usr/bin/env python3
"""mcp_gate.py (21 Nov 2026, owner: "fix the cause and the problem"): every MCP endpoint we publish answers, and every tool answers from a live source.

Why: five connectors (Astrophysics, Atlas, Campus, Models, Public Data) 404'd for two days after their servers were removed on 19-20 Nov,
because /connect kept listing them (it parsed the GROUPS source text, not what the worker serves) and no ship check ever called an MCP
endpoint. This gate calls them all, against the deployed worker, right after each deploy.

What it reads from the BUILT code (node imports indahl-ai/api.js): MCP_URL and MAIN_TOOLS (the one published server, in order),
LEGACY_SERVERS (still served, not listed) and RETIRED_SERVERS (must answer a JSON-RPC error naming MCP_URL, never a 404).
What it reads from the site: /.well-known/mcp.json and every indahl.ai/mcp address printed in the built pages (indahl-ai/pages.js).

Checks:
  - every published address: initialize and tools/list answer; a retired address printed on a page fails
  - /mcp: tools/list and the server card list exactly MAIN_TOOLS, in order
  - every tool on every live server, called once with the sample below: fails on HTTP 404, a JSON-RPC error (other than an expected
    "not found" for the sample), isError, or a data source that returned nothing (data null or empty, data.error, or a CANNOT_TELL whose
    reason says the source could not be read)
  - retired tools (find_study, astrophysics_find_study, all_tests_side_by_side, qia_audit, eval_setup_check) are on no server
  - every retired server answers JSON-RPC error -32001 naming MCP_URL, with an HTTP status other than 404

  python3 ledger/mcp_gate.py                       against https://indahl.ai (run right after deploy)
  python3 ledger/mcp_gate.py --base http://127.0.0.1:8787 --host indahl.ai   against a local `npx wrangler dev`
  python3 ledger/mcp_gate.py --quiet               one summary line plus failures

Any failure prints and appends `MCP GATE FAILED: <endpoint/tool>: <why>` to sagar/pipeline/pipe.log (watch/doorbell/poll.py rings it),
once per new set of failures (state in ledger/.mcp_gate_state.json), and exits 1. Standard library only.
"""
import concurrent.futures as cf, datetime as dt, json, os, re, subprocess, sys, time, urllib.error, urllib.request

B = os.path.expanduser('~/forge'); S = os.path.join(B, 'indahl-ai')
PIPE_LOG = os.environ.get('MCP_GATE_LOG') or os.path.join(B, 'sagar', 'pipeline', 'pipe.log')   # the env override: dry tests, and ship.sh step 4a (22 Nov 2026 P2: the ship's one ring, from ship_queue.py, carries the failure)
STATE = os.environ.get('MCP_GATE_STATE') or os.path.join(B, 'ledger', '.mcp_gate_state.json')
NODE = next((p for p in ('/opt/homebrew/bin/node', '/usr/local/bin/node') if os.path.exists(p)), 'node')
ARGS = sys.argv[1:]
def opt(name, default=None):
    return ARGS[ARGS.index(name) + 1] if name in ARGS and ARGS.index(name) + 1 < len(ARGS) else default
BASE = opt('--base', 'https://indahl.ai').rstrip('/'); HOST = opt('--host'); QUIET = '--quiet' in ARGS
UA = 'indahl-mcp-gate/1.0'
RETIRED_TOOLS = ['find_study', 'astrophysics_find_study', 'all_tests_side_by_side',
                 'qia_audit', 'eval_setup_check']   # 22 Nov 2026 (owner: kill what does nothing useful): CANNOT_TELL on every qubit; MATCHED with nothing compared
# A JSON-RPC error that is the right answer to the sample input. None today: every sample names something that exists.
EXPECT_NOT_FOUND = set()
fails, oks = [], []


def fail(where, why): fails.append('%s: %s' % (where, why))


def ring(msg):
    line = '%s %s' % (time.strftime('%Y-%m-%dT%H:%M:%S'), msg.replace('\n', ' ')[:600])
    try:
        with open(PIPE_LOG, 'a') as f: f.write(line + '\n')
    except Exception as e: sys.stderr.write('mcp_gate: could not write the pipeline log (%s)\n' % e)


def built():
    """MCP_URL, MAIN_TOOLS, LEGACY_SERVERS, RETIRED_SERVERS from the built api.js"""
    js = ("const m = await import(%s); console.log(JSON.stringify({ url: m.MCP_URL, main: m.MAIN_TOOLS, legacy: m.LEGACY_SERVERS, retired: m.RETIRED_SERVERS }));"
          % json.dumps('file://' + os.path.join(S, 'api.js')))
    r = subprocess.run([NODE, '--input-type=module', '-e', js], capture_output=True, text=True, timeout=90, cwd=S)
    if r.returncode != 0: raise SystemExit('mcp_gate: could not import indahl-ai/api.js: ' + r.stderr[-400:])
    return json.loads(r.stdout.strip().splitlines()[-1])


def path_of(url): return re.sub(r'^https?://(www\.)?indahl\.ai', '', url) or '/'


def http(method, path, body=None, timeout=90):
    """-> (status, parsed JSON or None, raw text)"""
    data = json.dumps(body).encode() if body is not None else None
    h = {'user-agent': UA, 'content-type': 'application/json', 'accept': 'application/json, text/event-stream'}
    if HOST: h['host'] = HOST
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r: raw = r.read().decode('utf-8', 'replace'); st = r.status
    except urllib.error.HTTPError as e: st = e.code; raw = e.read().decode('utf-8', 'replace') if e.fp else ''
    except Exception as e: return 0, None, '%s: %s' % (type(e).__name__, str(e)[:160])
    try: return st, json.loads(raw), raw
    except Exception: return st, None, raw[:300]


def rpc(path, method, params=None, rid=1, timeout=90):
    return http('POST', path, {'jsonrpc': '2.0', 'id': rid, 'method': method, 'params': params or {}}, timeout)


def samples(proc):
    hour_ago = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    return {
        'qia_calibration_check': {'processor': proc, 'qubits': '0,1'},
        'qia_run_check': {'processor': proc, 'start': hour_ago, 'qubits': '0,1'},
        'qia_qubit_history': {'processor': proc, 'qubit': 0, 'days': 3},
        'qia_measured': {'processor': proc, 'qubits': '0,1'},
        'paper_check': {'id': '1706.03762'},
        'paper_statistics': {'id': '1706.03762'},
        'check_reported_statistics': {'text': 't(28) = 2.20, p = .036'},
        'number_check': {'text': 'The model has 7 billion parameters.', 'source_text': 'The model has 7 billion parameters.'},
        'interval_verdict': {'estimate': 0.5, 'low': 0.4, 'high': 0.6, 'stated': 0.45},
        'triangulate_readings': {'readings': [{'label': 'a', 'value': 1.0, 'se': 0.1}, {'label': 'b', 'value': 1.1, 'se': 0.1}]},
        'claim_wording_check': {'text': 'Our method is the first to beat the baseline.'},
        'package_check': {'name': 'requests'},
        'model_check': {'repo': 'Qwen/Qwen2.5-7B-Instruct'},
        'link_rot': {'urls': 'https://indahl.ai/ https://arxiv.org/'},
        'arxiv_version_drift': {'id': '1706.03762', 'version_read': '1'},
        'source_check': {'refs': ['10.48550/arXiv.1706.03762']},
        'quote_check': {'text': '"Attention Is All You Need"', 'source_text': 'Attention Is All You Need'},
        'list_divisions': {},
        # legacy servers (served, not listed)
        'what_changed': {},
        'standards_card': {'id': '1706.03762'},
        'margin_check': {'value': 1.0, 'uncertainty': 0.1, 'breaks_at': 0.5},
        'controls_check': {'controls': [{'name': 'pos', 'kind': 'positive', 'expected': 'fires', 'observed': 'fires'}, {'name': 'neg', 'kind': 'negative', 'expected': 'silent', 'observed': 'silent'}]},
        'two_explanations': {'a': 'The drift is thermal.', 'b': 'The drift is a firmware change.', 'evidence': [{'item': 'drift tracks room temperature', 'favours': 'A'}]},
        'verify_landed': {'kind': 'url', 'target': 'https://indahl.ai/'},
        'prereg_check': {'repo': 'indahl-ai/indahl.ai', 'plan_path': 'README.md'},
        'batch_plan': {'items': ['a', 'b', 'c']},
        'batch_merge_check': {'manifest_items': ['a', 'b'], 'results': ['a', 'b']},
        'relay_plan_check': {'stages': [{'name': 's1', 'lane': 'cpu'}]},
        'correction_check': {'original': 'x is 5', 'corrected': 'x is 6'},
        'check_block_validate': {'block': 'REQ-01: holds: sample'},
        'reproduce_check': {'desk': 'airline'},
    }


UNREAD = re.compile(r'could not be read|did not answer|no store|not available|missing |no record was saved|source could not', re.I)


def judge(where, st, j, raw, tool):
    if st == 404: return fail(where, 'HTTP 404')
    if st == 0: return fail(where, 'no answer (%s)' % raw)
    if not isinstance(j, dict): return fail(where, 'HTTP %s, not JSON-RPC (%s)' % (st, raw[:120]))
    if 'error' in j:
        msg = str((j['error'] or {}).get('message', ''))
        if tool in EXPECT_NOT_FOUND and re.search(r'not found|no record', msg, re.I): return oks.append(where + ' (expected not found)')
        return fail(where, 'JSON-RPC error %s %s' % ((j['error'] or {}).get('code'), msg[:160]))
    res = j.get('result') or {}
    if res.get('isError'): return fail(where, 'isError: ' + ''.join(c.get('text', '') for c in res.get('content', []))[:160])
    sc = res.get('structuredContent')
    if not isinstance(sc, dict): return fail(where, 'no structuredContent')
    d = sc.get('data')
    if d is None or d == {} or d == []: return fail(where, 'data source returned nothing (%s)' % sc.get('source'))
    if isinstance(d, dict):
        if d.get('error') and d.get('outcome') not in ('REFUSED',): return fail(where, 'data.error: %s' % str(d['error'])[:160])
        if d.get('outcome') == 'CANNOT_TELL' and UNREAD.search(str(d.get('reason') or d.get('note') or '')): return fail(where, 'source unreadable: %s' % str(d.get('reason') or d.get('note'))[:160])
    oks.append(where)


def main():
    b = built(); main_url, MAIN = b['url'], b['main']; main_path = path_of(main_url)
    legacy = ['/mcp/' + k for k in b['legacy']]; retired = {'/mcp/' + k: v for k, v in b['retired'].items()}
    # published addresses: the server card and every indahl.ai/mcp address printed on a built page
    st, card, raw = http('GET', '/.well-known/mcp.json')
    published = {main_path}
    if st != 200 or not isinstance(card, dict): fail('/.well-known/mcp.json', 'HTTP %s' % st)
    else:
        for sv in card.get('servers', []): published.add(path_of(sv.get('url', '')))
        if [t.get('name') for t in card.get('tools', [])] != MAIN: fail('/.well-known/mcp.json', 'tools differ from MAIN_TOOLS')
    try:   # pages.js imports one HTML file per page; read pages.js (it carries llms.txt) and every file it imports
        pj = open(os.path.join(S, 'pages.js'), encoding='utf-8', errors='replace').read(); parts = [pj]
        for f in set(re.findall(r"^import \w+ from '\./([^']+\.(?:html|txt))';?$", pj, re.M)):
            try: parts.append(open(os.path.join(S, f), encoding='utf-8', errors='replace').read())
            except Exception: fail('indahl-ai/' + f, 'imported by pages.js but not readable')
        pages = '\n'.join(parts)
    except Exception: pages = ''; fail('indahl-ai/pages.js', 'not readable')
    for u in set(re.findall(r'https?://indahl\.ai(/mcp(?:/[a-z]+)?)\b', pages)) | set('/mcp' + x for x in re.findall(r'<code>/mcp(/[a-z]+)?</code>', pages)):
        published.add(u)
    for p in sorted(published):
        if p in retired: fail(p, 'retired server is still printed on a page or the server card')
    live = sorted(published - set(retired)) + [p for p in legacy if p not in published]
    # initialize + tools/list on every live server
    tools_on = {}
    for p in live:
        st, j, raw = rpc(p, 'initialize', {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': UA, 'version': '1'}})
        if st != 200 or not isinstance(j, dict) or 'result' not in j: fail(p, 'initialize: HTTP %s %s' % (st, (raw or '')[:120])); continue
        st, j, raw = rpc(p, 'tools/list', rid=2)
        if st != 200 or not isinstance(j, dict) or 'result' not in j: fail(p, 'tools/list: HTTP %s %s' % (st, (raw or '')[:120])); continue
        names = [t['name'] for t in j['result'].get('tools', [])]
        if not names: fail(p, 'tools/list is empty'); continue
        tools_on[p] = j['result']['tools']; oks.append(p + ' initialize, tools/list (%d tools)' % len(names))
        if p == main_path and names != MAIN: fail(p, 'tools/list differs from MAIN_TOOLS: %s' % ', '.join(n for n in names if n not in MAIN) or 'order')
        for n in RETIRED_TOOLS:
            if n in names: fail(p + '/' + n, 'retired tool still served')
    # pick a processor the QIA mirror holds
    proc = 'ibm_fez'
    if main_path in tools_on:
        st, j, raw = rpc(main_path, 'tools/call', {'name': 'qia_calibration_check', 'arguments': {}}, rid=3)
        try:
            ps = j['result']['structuredContent']['data'].get('processors') or []
            if ps: proc = 'ibm_fez' if 'ibm_fez' in ps else ps[0]
            else: fail(main_path + '/qia_calibration_check', 'lists no processors (QIA mirror empty)')
        except Exception: pass
    SAM = samples(proc)
    # each tool once, on the published server first
    todo, seen = [], set()
    for p in [x for x in live if x in tools_on]:
        for t in tools_on[p]:
            n = t['name']
            if n in seen: continue
            seen.add(n)
            req = t.get('inputSchema', {}).get('required', [])
            a = SAM.get(n)
            if a is None or any(k not in a for k in req): fail(p + '/' + n, 'no sample input in mcp_gate.py for its required %s' % (req or 'inputs')); continue
            todo.append((p, n, a))
    def call(x):
        p, n, a = x; st, j, raw = rpc(p, 'tools/call', {'name': n, 'arguments': a}, rid=4, timeout=120); return p, n, st, j, raw
    with cf.ThreadPoolExecutor(8) as ex:
        for p, n, st, j, raw in ex.map(call, todo): judge(p + '/' + n, st, j, raw, n)
    # retired servers: a JSON-RPC error naming the live server, never a 404
    for p, title in sorted(retired.items()):
        st, j, raw = rpc(p, 'initialize', {'protocolVersion': '2025-06-18'})
        if st == 404: fail(p, 'retired server answers HTTP 404'); continue
        e = (j or {}).get('error') if isinstance(j, dict) else None
        if not e or e.get('code') != -32001 or main_url not in str(e.get('message', '')): fail(p, 'retired server does not answer the JSON-RPC error naming %s (HTTP %s %s)' % (main_url, st, (raw or '')[:120])); continue
        oks.append(p + ' retired: JSON-RPC error names ' + main_url)
    for n in RETIRED_TOOLS:   # 22 Nov 2026: a retired tool is gone from the JSON API too, not only from the MCP servers
        st, j, raw = http('GET', '/api/v1/' + n)
        if st != 404: fail('/api/v1/' + n, 'retired tool still answers on the API (HTTP %s)' % st)
        else: oks.append('/api/v1/' + n + ' retired: 404')
    if not QUIET:
        for o in oks: print('ok   ' + o)
    for f in fails: print('FAIL ' + f)
    key = sorted(re.sub(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', 'T', f) for f in fails)
    try: last = json.load(open(STATE)).get('fails', [])
    except Exception: last = None
    if key != last:
        for f in fails: ring('MCP GATE FAILED: ' + f)
        if not fails and last: ring('mcp gate: cleared, every published MCP endpoint and tool answers')
        try: tmp = STATE + '.tmp'; json.dump({'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'base': BASE, 'fails': key}, open(tmp, 'w'), indent=1); os.replace(tmp, STATE)
        except Exception: pass
    print('mcp gate: %d checks ok, %d failed (%s; published %s; legacy %s; retired %d)' % (len(oks), len(fails), BASE, ', '.join(sorted(published - set(retired))), ', '.join(legacy), len(retired)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
