"""internal_gate.py: refuses a public push that carries internal material (18 Nov 2026 leak fix, the owner: "this can't happen again").

Two rules, both fail-closed:
1. ALLOWLIST: every folder under code/src must be named in ledger/public_src_allowlist.json. A new working folder is private until
   someone adds it to that list on purpose; nothing becomes public just because it exists in ~/bones-forge.
2. MARKERS: no path or file anywhere in the public trees may look like internal notes, plans or IDs (handoffs, the referee/the operator packets,
   the launch plan, the plan page, IBM instance CRNs, the plan key).
Exit 1 with the offending paths; push_public.sh stops the push on a refusal.
"""
import json, os, re, sys
B = os.path.expanduser('~/bones-forge')
TREES = [B + '/public_mirror/indahl.ai', B + '/cloudflare-workers/heuremen-door/public']   # HF WALL 18 Nov 2026: hf_stage is no longer published
if '--tree' in sys.argv: TREES = [sys.argv[sys.argv.index('--tree') + 1]]
if '--site' in sys.argv: TREES = [B + '/cloudflare-workers/heuremen-door/public']   # quickship: the folder about to deploy
ALLOW = set(json.load(open(B + '/ledger/public_src_allowlist.json')))
BAD_PATH = re.compile(r'(^|/)code/src/yo(/|$)|(^|/)(yo_school|launch_copy|private_plan|stan|touring-sage|cuda|disco_\d+|overnight_\d+|notices)(/|$)'
                      r'|(^|/)(HANDOFF|MORNING|NOTE_FROM|BRIEF_FOR|SAGE_|bones_to_sage)[^/]*$'
                      r'|(^|/)sage_[^/]*\.(md|txt|text)$|(?i:fuckup)|(^|/)(internal_gate|scrub_personal|code_sweep|scrub_public|remove|removed_gate)\.py|public_src_allowlist\.json|(^|/)qia_plan[^/]*$|_qiasite/plan\.html$|release_workshop', re.I)
BAD_TEXT = re.compile(r'(?i:\bwayfinder\b)|claude\.ai/code/session_|<kv-namespace-id>|<kv-namespace-id>|<d1-database-id>|<cloudflare-account-id>|<cloudflare-account-id>|\bWayfinder\b|~|\bctrai\b|huggingface\.co/(?:datasets/|spaces/|collections/)?indahl|<ibm-crn>')
TEXT_EXT = ('.md', '.txt', '.text', '.py', '.js', '.json', '.html', '.sh', '.toml', '.yml', '.yaml', '.csv')
hits = []
for t in TREES:
    if not os.path.isdir(t): continue
    src = os.path.join(t, 'code', 'src')
    if os.path.isdir(src):
        for d in os.listdir(src):
            if d not in ALLOW and not d.startswith('.'): hits.append(f'not on the allowlist: {src}/{d}')
    for root, dirs, files in os.walk(t):
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            p = os.path.join(root, f); rel = os.path.relpath(p, t)
            if BAD_PATH.search(rel): hits.append(f'internal path: {p}'); continue
            if f.endswith(TEXT_EXT) and os.path.getsize(p) < 5_000_000:
                try:
                    if BAD_TEXT.search(open(p, errors='ignore').read()): hits.append(f'internal text: {p}')
                except OSError: pass
if hits:
    print('INTERNAL GATE REFUSED: %d item(s)' % len(hits)); [print('  ' + h) for h in hits[:60]]; sys.exit(1)
print('internal gate: clean (%d allowlisted code folders)' % len(ALLOW))
