#!/usr/bin/env python3
"""copy_damage_gate.py (22 Nov 2026): refuse a ship when a served page carries spliced or broken copy.

Why: /chronos shipped "Each calendar<p ...>Type or pick a date ...</p>rsquo;s name links" (a bad splice: a paragraph pasted inside
another, a sentence printed twice, and an entity cut from its &). The owner found it by reading the page. No gate looked at this.

Checks every indahl.ai page in indahl-ai/pages.js and every quantumidleaudit.com page (scripts, styles and code blocks are skipped):
  ENTITY   an entity name with its & cut off ("rsquo;", "ldquo;", "mdash;" ... standing alone in text)
  DOUBLE   a double-escaped entity ("&amp;rsquo;"), which shows the reader "&rsquo;"
  NESTP    a <p> opened inside an open <p> (a splice)
  REPEAT   the same sentence of 40 or more characters twice in a row
Exit 1 on any breach. --all lists every breach (default: the first 40)."""
import glob, html, os, re, sys
B = os.path.expanduser('~/forge')
NAMES = 'rsquo|lsquo|ldquo|rdquo|mdash|ndash|nbsp|middot|hellip|amp|quot|apos|rarr|larr|plusmn|asymp|copy|reg|trade|eacute|uuml|ouml'
BARE = re.compile(r'(?<![&#\w])(' + NAMES + r');')
DBL = re.compile(r'&amp;(' + NAMES + r'|#\d+|#x[0-9a-fA-F]+);')

def pages():
    pj = os.path.join(B, 'indahl-ai', 'pages.js')
    s = open(pj, encoding='utf-8', errors='replace').read(); files = dict(re.findall(r"import (P\d+) from '\./([^']+)'", s))
    paths = {v: k for k, v in re.findall(r'"(/[^"]*)"\s*:\s*(P\d+)', s)}
    for var, rel in files.items():
        f = os.path.join(B, 'indahl-ai', rel)
        if os.path.exists(f) and rel.endswith('.html'): yield 'indahl.ai' + paths.get(var, '/' + rel), f
    for f in glob.glob(os.path.join(B, 'cloudflare-workers', 'heuremen-door', 'public', '_qiasite', '*.html')):
        yield 'quantumidleaudit.com/' + os.path.basename(f)[:-5], f

def strip_code(h):
    return re.sub(r'<(script|style|code|pre|textarea)\b[\s\S]*?</\1>', ' ', h, flags=re.I)

bad = []
for url, f in pages():
    h = strip_code(open(f, encoding='utf-8', errors='replace').read())
    text_parts = re.sub(r'<[^>]+>', '\x00', h)
    for m in BARE.finditer(text_parts): bad.append((url, 'ENTITY', text_parts[max(0, m.start() - 50):m.end() + 20].replace('\x00', ' ')))
    for m in DBL.finditer(h): bad.append((url, 'DOUBLE', h[max(0, m.start() - 40):m.end() + 10]))
    depth = 0
    for m in re.finditer(r'<(/?)p\b[^>]*>', h, re.I):
        if m.group(1): depth = max(0, depth - 1)
        else:
            if depth: bad.append((url, 'NESTP', h[max(0, m.start() - 70):m.start() + 50])); break
            depth = 1
        if re.match(r'</?(div|section|li|td|article|main|footer|header|h\d)\b', h[m.end():m.end() + 12], re.I): pass
    t = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', h)).split())
    sents = re.split(r'(?<=[.!?])\s+', t)
    for a, b in zip(sents, sents[1:]):
        if len(a) >= 40 and a == b: bad.append((url, 'REPEAT', a[:120]))
print('copy damage gate: %d pages read; breaches: %d' % (sum(1 for _ in pages()), len(bad)))
for u, k, c in (bad if '--all' in sys.argv else bad[:40]): print('  BREACH %-6s %s: ...%s...' % (k, u, ' '.join(c.split())[:170]))
sys.exit(1 if bad else 0)
