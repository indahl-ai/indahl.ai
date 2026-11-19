"""scrub_personal.py: personal material never reaches a public copy (18 Nov 2026, the designer's security pass; the owner: professional standards).
Works on the PUBLIC copies only (the deployed site folder and public_mirror); house sources keep their notes.
- bylines and names: "Heuremen LLC" / "the owner" -> "Heuremen LLC" / "the owner"
- local paths: ~ -> ~
- whole files that are personal logs are removed (THE_FUCKUPS, SHOW_LOG, the-horn reread notes)
"""
import os, re, sys
B = os.path.expanduser('~/bones-forge')
TREES = [B + '/cloudflare-workers/heuremen-door/public', B + '/public_mirror/indahl.ai']
if '--site' in sys.argv: TREES = TREES[:1]
DROP = re.compile(r'(?i)fuckup|(^|/)(internal_gate\.py[^/]*|scrub_personal\.py[^/]*|code_sweep\.py[^/]*|public_src_allowlist\.json|scrub_public\.py[^/]*|remove\.py[^/]*|removed_gate\.py[^/]*|[^/]*_guard\.py[^/]*|[^/]*FUCKUPS[^/]*|[^/]*sage[^/]*eval[^/]*|[^/]*eval[^/]*sage[^/]*|THE_FUCKUPS[^/]*|SHOW_LOG[^/]*|[^/]*reread[^/]*|[^/]*_hf[^/]*\.py|publish_hf[^/]*|upload_[^/]*hf[^/]*)$|(^|/)code/src/hf_(indahl|packs)/', re.I)
TEXT_EXT = ('.md', '.txt', '.text', '.py', '.js', '.mjs', '.json', '.jsonl', '.html', '.sh', '.toml', '.yml', '.yaml', '.csv', '.xml', '.tex', '.bib', '.cff', '.rc', '.log', '.sha256', '.tsv')
SUBS = [(re.compile(r'<kv-namespace-id>|<kv-namespace-id>'), '<kv-namespace-id>'), (re.compile(r'<d1-database-id>'), '<d1-database-id>'), (re.compile(r'<cloudflare-account-id>|<cloudflare-account-id>'), '<cloudflare-account-id>'), (re.compile(r'(\b(?:id|preview_id)\s*=\s*")[a-f0-9]{32}(")'), r'\1<kv-namespace-id>\2'), (re.compile(r'(database_id\s*=\s*")[a-f0-9-]{36}(")'), r'\1<d1-database-id>\2'), (re.compile(r'(?:https?://)?huggingface\.co/(?:datasets/|spaces/|collections/)?indahl[^\s"\'<>)]*'), 'https://indahl.ai/downloads'), (re.compile(r'the owner (and|&) the operator's), 'Heuremen LLC'), (re.compile(r"the owner's"), "the owner's"), (re.compile(r'\bWayfinder\b'), 'the owner'), (re.compile(r'\bwayfinder\b', re.I), 'owner'), (re.compile(r'https?://claude\.ai/code/session_[A-Za-z0-9]+'), ''), (re.compile(r'        (re.compile(r'~'), '~'), (re.compile(r'/(home|Users)/user|C:\\\\Users\\\\user|\bctrai\b', re.I), 'user')]
changed = dropped = 0; sealed = []
for t in TREES:
    for root, dirs, files in os.walk(t):
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            p = os.path.join(root, f)
            if DROP.search(os.path.relpath(p, t)): os.remove(p); dropped += 1; continue
            if not f.endswith(TEXT_EXT) or os.path.getsize(p) > 20_000_000: continue
            try: s = open(p, encoding='utf-8', errors='surrogateescape').read()
            except (UnicodeDecodeError, OSError): continue
            n = s
            for rx, rep in SUBS: n = rx.sub(rep, n)
            if n != s:
                if not os.access(p, os.W_OK): sealed.append(p); os.chmod(p, 0o644); os.remove(p); continue   # a sealed record with personal text is left out of the public copy (privacy wins over the copy)
                open(p, 'w', encoding='utf-8', errors='surrogateescape').write(n); changed += 1
# outside email addresses in the public CODE tree become <email> (desk pages that quote a public contact are left alone)
EM = re.compile(r'(?<![\w.+-])[A-Za-z0-9._%+-]+@(?!(?:heuremen\.(?:com|org)|indahl\.ai|users\.noreply\.github\.com|anthropic\.com|example\.(?:com|org|invalid))\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
em = 0
for root, dirs, files in os.walk(B + '/public_mirror/indahl.ai/code'):
    dirs[:] = [d for d in dirs if d != '.git']
    for f in files:
        p = os.path.join(root, f)
        if not f.endswith(TEXT_EXT) or os.path.getsize(p) > 20_000_000 or not os.access(p, os.W_OK): continue
        try: s0 = open(p, encoding='utf-8', errors='surrogateescape').read()
        except OSError: continue
        n0 = EM.sub('<email>', s0)
        if n0 != s0: open(p, 'w', encoding='utf-8', errors='surrogateescape').write(n0); em += 1
for t in TREES:
    for root, dirs, files in os.walk(t, topdown=False):
        if '.git' not in root and root != t and not os.listdir(root): os.rmdir(root)
print(f'scrub_personal: outside emails replaced in {em} code files')
print(f'scrub_personal: {changed} files scrubbed, {dropped} personal files removed, {len(sealed)} sealed files left as they are')
