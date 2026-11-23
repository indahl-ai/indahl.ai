#!/usr/bin/env python3
"""Builds the ChatGPT plugin directory packages (OpenAI) from the same directory copies the Anthropic directory gets (13 Nov 2026,
The owner). One package per plugin in plugins/ (the parts and
the indahl bundle): openai/<name>/ with .codex-plugin/plugin.json (interface block for the listing), skills, commands, .mcp.json where the
part has the indahl.ai connector, assets/logo.png and assets/icon.png, and openai/<name>.zip ready to upload. Plugins with the connector also
get openai/<name>.chatgpt-app-submission.json (every tool's hints and justifications, five positive and three negative tests).
Never edit openai/ by hand.   python3 build_openai.py"""
import json, os, re, shutil, urllib.request, zipfile
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, 'plugins'); O = os.path.join(H, 'openai')
DEMO_URL = os.environ.get('INDAHL_DEMO_URL', '')   # reviewer-accessible walkthrough video, required for MCP review
ICONS = os.path.expanduser('~/forge/cloudflare-workers/heuremen-door/public/icons')
# 23 Nov 2026 (owner: ): eli5, relay, rubicon, spend-cap, ccr, fsck and
# silent-failure-guard are off the listing (agent operations and plain-language tools, not research method).
ORDER = ['indahl', 'indahl-data', 'standards', 'eval-check', 'reproduce', 'qia-calibration', 'darkwave-correction', 'prereg', 'readcheck', 'triangulate', 'batch', 'cannot-tell', 'both', 'outside-ruler', 'number-check', 'quote-check', 'source-check', 'controls', 'margin', 'correct', 'clause']
SUB = {   # subtitle (30 characters or fewer) and three starter prompts per listing
 'indahl': ('Stated vs. delivered, measured', ["Check IBM's calibration for qubits 0-4 on ibm_kingston.", 'Has this paper been retracted? (DOI)', 'Is this quote accurate? (quote and source)']),
 'indahl-data': ('Check claims against the data', ['List the indahl.ai divisions.', 'Does this Hugging Face model match its license file?', 'Has this paper been corrected or withdrawn? (DOI or arXiv id)']),
 'standards': ('Check papers vs. the Standards', ['Check this paper against the Heuremen Standard.', 'Which claim codes apply to this abstract?', 'Give me a recount card for this result.']),
 'eval-check': ('Check an LLM eval claim', ['Check this benchmark claim.', 'Is this eval run comparable to the vendor number?', 'Run the twelve eval checks on this result.']),
 'reproduce': ('Rerun an indahl.ai desk kit', ['List the desks with reproduce kits.', 'Reproduce the FLU desk.', 'Show what the TIME kit would run.']),
 'qia-calibration': ('Check an IBM Quantum run', ['Check this calibration record before my run.', 'Which records were in force during my run?', 'Run the same-job T1/T2 check.']),
 'darkwave-correction': ('Correct IBM Quantum readout', ['Check my backend for the Darkwave kit.', 'What would the Darkwave measurement cost?', 'Correct these counts with the kit.']),
 'prereg': ('Was the plan pushed first?', ['Was my plan pushed before the first run?', 'List what ran that the plan did not cover.', 'Check this repository for a pre-registration.']),
 'triangulate': ('Three blind reads, one verdict', ['Triangulate: is this claim right?', 'Get three independent reads on this decision.', 'Check this number against three seats.']),
 'batch': ('Big audits, batched', ['Audit every page of this site in batches.', 'Apply batch to this.', 'Show batch on an example.']),
 'cannot-tell': ("Say can't-tell, usefully", ["Is this claim right, or can't we tell yet?", 'Apply cannot tell to this.', 'Show cannot tell on an example.']),
 'both': ('Keep two explanations alive', ['Hold both explanations and tell me what separates them.', 'Apply both to this.', 'Show both on an example.']),
 'outside-ruler': ('Referee it before it ships', ['Referee this draft before I publish it.', 'Apply outside ruler to this.', 'Show outside ruler on an example.']),
 'number-check': ('Trace every figure', ['Check every number in this report against its source.', 'Run number check on this.', 'Show number check on an example.']),
 'quote-check': ('Every quote, verbatim', ['Check every quote in this draft against its source.', 'Run quote check on this.', 'Show quote check on an example.']),
 'source-check': ('Do the citations say it?', ['Check that every citation in this exists and says what is claimed.', 'Run source check on this.', 'Show source check on an example.']),
 'controls': ('Can your test actually fail?', ['Audit the controls of this study before we run it.', 'Run controls on this.', 'Show controls on an example.']),
 'eli5': ('Explain it plainly', ['Explain this paper like I am new to the field.', 'What does this error message mean, in plain words?', 'ELI5 this result, and keep how sure anyone is.']),
 'relay': ('Run a multi-stage job', ['Set up a relay chain for this pipeline.', 'Show the status of my relay chain.', 'Add a decide stage that picks the next run.']),
 'silent-failure-guard': ('Did it really work?', ['Verify what this push actually did.', 'Run silent-failure-guard on this pipeline.', 'Scan this script for hidden failures.']),
 'margin': ('How far before it breaks?', ['How much margin does this prediction have?', 'Run margin on this.', 'Show margin on an example.']),
 'correct': ('Fix it beside, not over', ['Log this correction properly.', 'Run correct on this.', 'Show correct on an example.']),
 'clause': ('The sentence reviewers catch', ['Check the claims in this results paragraph.', 'Run clause on this.', 'Show clause on an example.']),
 'readcheck': ('Check blocks for readings', ['Make a check block for this reading.', 'Verify the check block in this folder.', 'List staged readings without a check block.']),
}
CAT = 'Education & Research'

CHATGPT_DESC = {
    'indahl': ("Check published claims against the data behind them. Check the calibration IBM publishes for the qubits a quantum circuit will use, "
               "before a run or for a run already done; look up a paper by DOI or arXiv id for retractions, corrections, its current version and broken "
               "links; recompute reported statistics; check quotations, figures and citations against their sources; read an interval as one of four "
               "outcomes; and check a PyPI package or Hugging Face model live. Every answer names its source and when it was read, and "
               "outcomes are ABOVE, BELOW, CONSISTENT or CANNOT_TELL relative to what was stated. Read-only: nothing is written or sent."),
    'indahl-data': ("Measurements of published claims against the data behind them, from indahl.ai: the calibration IBM publishes for its quantum "
                    "processors checked against our own runs, and checks on the papers, statistics, quotations, citations, packages and models a person brings. Every answer names its source and when it was read, with the outcome "
                    "ABOVE, BELOW, CONSISTENT or CANNOT_TELL relative to what was stated. Read-only."),
}
def listing_name(p):
    return 'Indahl' if p == 'indahl' else ('Indahl ' + {'indahl-data': 'Data', 'qia-calibration': 'QIA Calibration', 'darkwave-correction': 'Darkwave', 'eval-check': 'Eval Check', 'cannot-tell': 'Cannot Tell', 'outside-ruler': 'Outside Ruler', 'number-check': 'Number Check', 'quote-check': 'Quote Check', 'source-check': 'Source Check'}.get(p, p.replace('-', ' ').title()))

def build(p):
    src = os.path.join(P, p); m = json.load(open(os.path.join(src, '.claude-plugin', 'plugin.json')))
    name = 'indahl' if p == 'indahl' else ('indahl-' + p if not p.startswith('indahl') else p)
    name = {'indahl-darkwave-correction': 'indahl-darkwave'}.get(name, name)
    dst = os.path.join(O, name); shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('.claude-plugin', '__pycache__', '*.pyc', '*.bak*', '*.pre-*'))
    for _d, _, _fs in os.walk(dst):   # 16 Nov 2026: ChatGPT/Codex copies speak of the host, not Claude Code
        for _f in _fs:
            if _f.endswith('.md'):
                _p = os.path.join(_d, _f); _t = open(_p, encoding='utf-8').read(); _o = _t
                for _a, _b in (("Claude Code's Task/Agent tool", "the host's subagent tool"), ('Claude Code connects', 'the host connects'), ('Claude Code to write', 'the assistant to write'), ("Claude Code's", "the host's"), ('inside Claude Code', 'in the assistant'), ('Claude Code', 'the assistant')):
                    _t = _t.replace(_a, _b)
                if _t != _o: open(_p, 'w', encoding='utf-8').write(_t)
    os.makedirs(os.path.join(dst, '.codex-plugin'), exist_ok=True); os.makedirs(os.path.join(dst, 'assets'), exist_ok=True)
    shutil.copy(os.path.join(ICONS, 'icon-512.png'), os.path.join(dst, 'assets', 'logo.png')); shutil.copy(os.path.join(ICONS, 'icon-192.png'), os.path.join(dst, 'assets', 'icon.png'))
    sub, prompts = SUB[p]; assert len(sub) <= 30, sub
    desc = m['description'].replace(' inside Claude Code', '').replace('inside Claude Code', 'with the indahl.ai connector'); has_mcp = os.path.exists(os.path.join(dst, '.mcp.json'))
    if name in CHATGPT_DESC: desc = CHATGPT_DESC[name]   # 16 Nov 2026: ChatGPT listings describe what a person can ask, not Claude Code packaging (OpenAI flagged the marketplace wording)
    man = {'name': name, 'version': m.get('version', '1.0.0'), 'description': desc, 'author': {'name': 'Heuremen LLC', 'url': 'https://indahl.ai'},
           'homepage': 'https://indahl.ai/plugins', 'repository': 'https://github.com/indahl-ai/indahl.ai', 'license': m.get('license', 'SEE LICENSE'),
           'keywords': m.get('keywords', []), 'skills': './skills/',
           'interface': {'displayName': listing_name(p), 'shortDescription': sub, 'longDescription': desc, 'developerName': 'Heuremen LLC', 'category': CAT,
                         'capabilities': [], 'websiteURL': 'https://indahl.ai', 'supportURL': 'https://indahl.ai/contact',
                         'privacyPolicyURL': 'https://indahl.ai/privacy', 'termsOfServiceURL': 'https://indahl.ai/terms', 'defaultPrompt': prompts,
                         'brandColor': '#111111', 'composerIcon': './assets/icon.png', 'logo': './assets/logo.png'}}
    if has_mcp:
        man['mcpServers'] = './.mcp.json'
    if has_mcp and name in ('indahl', 'indahl-data'):   # 16 Nov 2026: review test cases only for the bundles that are submitted (the full server)
        # 14 Nov 2026: OpenAI imports review test cases from the package (extensions.com.openai.review), not the dashboard.
        submission(name, desc); s = json.load(open(os.path.join(O, name + '.chatgpt-app-submission.json')))
        rv = {'test_cases': {'positive': [{'description': c['description'], 'prompt': c['user_prompt'], 'tools_triggered': c['tools_triggered'], 'expected_behavior': c['expected_output']} for c in s['test_cases']],
                             'negative': [{'description': c['description'], 'prompt': c['user_prompt'], 'expected_behavior': c['expected_output']} for c in s['negative_test_cases']]}}
        if DEMO_URL: rv['demo_recording_url'] = DEMO_URL
        man['extensions'] = {'com.openai': {'review': rv, 'publication': {'release_notes': 'First directory submission: %s %s.' % (listing_name(p), man['version'])}}}
    json.dump(man, open(os.path.join(dst, '.codex-plugin', 'plugin.json'), 'w'), indent=2)
    z = os.path.join(O, name + '.zip')
    files = sorted(os.path.relpath(os.path.join(d, f), dst) for d, _, fs in os.walk(dst) for f in fs if f != '.DS_Store')
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:   # 14 Nov: deterministic (fixed time, sorted, fixed mode), so an unchanged plugin makes a byte-identical zip and no new commit
        for rel in files:
            zi = zipfile.ZipInfo(rel, date_time=(2026, 1, 1, 0, 0, 0)); zi.external_attr = 0o644 << 16; zi.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(zi, open(os.path.join(dst, rel), 'rb').read())
    return name, has_mcp, desc

TOOLKIT_COMPUTE = None   # 16 Nov 2026: tools that compute on supplied input (the toolkit), read from the live server card's groups
def submission(name, desc):
    global TOOLKIT_COMPUTE
    if TOOLKIT_COMPUTE is None:
        card = json.load(urllib.request.urlopen(urllib.request.Request('https://indahl.ai/.well-known/mcp.json', headers={'user-agent': 'indahl-openai-build'}), timeout=60))
        # 21 Nov 2026: the card now lists one server (indahl.ai at /mcp), so the old 'indahl-checks'/'indahl-verify' lookup came back empty and every check
        # got the "retrieves our own measurements" wording. Everything on the server except the QIA reads and list_divisions works on what the person supplies.
        TOOLKIT_COMPUTE = {n for sv in card.get('servers', []) for n in sv['tools'] if not n.startswith('qia_')} - {'list_divisions'}
        assert TOOLKIT_COMPUTE, 'server card lists no compute tools'
    r = urllib.request.urlopen(urllib.request.Request('https://indahl.ai/mcp', data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'}).encode(),
                               headers={'content-type': 'application/json', 'user-agent': 'indahl-openai-build'}), timeout=60)
    tools = json.load(r)['result']['tools']; names = {t['name'] for t in tools}; T = {}
    for t in tools:
        a = t['annotations']; assert a.get('readOnlyHint') is True and a.get('destructiveHint') is False, t['name']   # 14 Nov: paper_check, package_check and model_check read the open web, so openWorld is taken from the tool
        ow = a.get('openWorldHint') is True
        computes = t['name'] in TOOLKIT_COMPUTE
        T[t['name']] = {'annotations': {'readOnlyHint': True, 'openWorldHint': ow, 'destructiveHint': False},
                        'justifications': {'read_only_justification': ("Computes its result from the text or numbers the person supplies (and any public page they name) and returns it; nothing is created, changed or stored." if computes else "Only retrieves indahl.ai's own published measurements for this desk and returns them; nothing is created, changed or stored."),
                                           'open_world_justification': ("Reads public records at the source the person names (Crossref, arXiv, PyPI, GitHub or Hugging Face) to answer, and never writes to the internet or to any third-party system." if ow else "Reads only indahl.ai's own public data and never writes to the internet or to any third-party system."),
                                           'destructive_justification': 'Cannot delete, overwrite, send or revoke anything; repeated calls return the same published data.'}}
    pos = [('Check IBM Quantum calibration before a run.', 'I am about to run a circuit on ibm_kingston using qubits 0, 1, 2, 3 and 4. Is IBM\'s published calibration for those qubits fit to rely on, and which qubits look better?', 'qia_calibration_check', 'Reads the newest calibration record IBM published for ibm_kingston, applies the QIA package rules to qubits 0 to 4 (stale figures, T2 above twice T1, T1 and T2 measured far apart, zero error figures), states the record\'s age, and lists unflagged qubits with the lowest readout error.'),
           ('Check one paper for retractions and corrections.', 'Has this paper been retracted or corrected? 10.1016/S0140-6736(97)11096-0', 'paper_check', 'Reads the Crossref record and finds the 2004 correction and the 2010 retraction notices with their DOIs and dates.'),
           ('Recompute reported statistics from their own numbers.', 'Check the statistics in this passage: "Participants in the treatment group scored higher, t(28) = 2.20, p = .01, and the effect held at follow-up, F(1, 40) = 4.10, p = .049."', 'check_reported_statistics', 'Recomputes both tests: t(28) = 2.20 gives p of about .036, so the stated p = .01 reads BELOW; F(1, 40) = 4.10 gives p of about .0496, CONSISTENT with .049.'),
           ('Check a quotation against its source.', 'Is this quote accurate? "deep learning allows computational models that are composed of multiple processing layers to learn representations of data" Source: https://www.nature.com/articles/nature14539', 'quote_check', 'Reads the named page and marks the quotation VERBATIM, ALTERED (with the source\'s exact words and the differences), NOT_FOUND or CANNOT_TELL; here VERBATIM, with where it sits in the page.'),
           ('Read an interval as one of four outcomes.', 'Our trial found a difference of 1.8 points, 95% interval 0.2 to 3.4. The smallest difference that matters clinically is 2 points. Can we say the treatment works?', 'interval_verdict', 'Tests both alternatives: the interval excludes zero but still reaches 2 points and beyond, so the answer on the question that matters is CANNOT_TELL, with the width needed to decide.')]
    for x in pos: assert x[2] in names, x[2]
    neg = [('Do not trigger for general coding help.', 'Write a Python function that sorts a list of dictionaries by date.'),
           ('Do not trigger for personal scheduling.', 'What meetings do I have tomorrow, and can you move the 3pm?'),
           ('Do not trigger for stock trading advice.', 'Should I buy IBM stock this week?')]
    s = {'$schema': 'https://developers.openai.com/apps-sdk/schemas/chatgpt-app-submission.v1.json', 'schema_version': 1,
         'app_info': {'display_name': listing_name(name if name != 'indahl-data' else 'indahl-data'), 'subtitle': SUB['indahl' if name == 'indahl' else 'indahl-data'][0],
                      'description': desc, 'category': 'EDUCATION'},
         'tools': T,
         'test_cases': [{'description': d, 'user_prompt': u, 'file_attachment_urls': None, 'tools_triggered': tn, 'expected_output': e, 'expected_output_url': None} for d, u, tn, e in pos],
         'negative_test_cases': [{'description': d, 'user_prompt': u, 'file_attachment_urls': None, 'tools_triggered': None,
                                  'expected_output': "The app should not be invoked because the request is outside indahl.ai's published measurements.", 'expected_output_url': None} for d, u in neg]}
    json.dump(s, open(os.path.join(O, name + '.chatgpt-app-submission.json'), 'w'), indent=2)
    return len(T)

if __name__ == '__main__':
    shutil.rmtree(O, ignore_errors=True); os.makedirs(O)
    for p in ORDER:
        name, mcp, desc = build(p)
        extra = f', submission JSON for {submission(name, desc)} tools' if mcp and name in ('indahl', 'indahl-data') else (' (connects its indahl.ai server; listed through the main Indahl app)' if mcp else '')   # 16 Nov 2026: one OpenAI submission for the full server; per-plugin bundles connect focused servers
        print(f'  openai: {name}.zip ({listing_name(p)}){extra}')
