#!/usr/bin/env python3
"""no_confessions_gate.py (15 Nov 2026, the owner and
"nobody does that"). Public copy states what a thing is now. A fix is made, never announced; the version history holds the past.
Refuses a release when a built public page carries one of these phrases about indahl.ai's own past errors. Legal pages are exempt.
  python3 no_confessions_gate.py     exit 1 and print every hit"""
import glob, html, os, re, sys
B = os.path.expanduser('~/forge'); SITE = os.path.join(B, 'indahl-ai')
PHRASES = [r'\bour corrections\b', r'\bcorrections? log\b', r'corrected after (it|they) went out', r'\bwe fixed (the|a|our|it)\b',
           r'\bour (own )?mistakes?\b', r'\bour (own )?errors?\b', r'\bthe fix made our\b', r'\bwe were wrong\b', r'\bwhen we get something wrong\b',
           r'\buntil \d{1,2} (january|february|march|april|may|june|july|august|september|october|november|december) 20\d\d,? the (weights|files|page|card|adapter)\b',
           r'\bwas wrong (here|on this page)\b', r'\bwe (had )?misstated\b']
PAT = re.compile('|'.join(PHRASES), re.I)
EXEMPT = re.compile(r'^(privacy|terms|agree|contact|consent|unsubscribe|correction|security/policy)\.html$')
hits = []
for f in sorted(glob.glob(SITE + '/*.html') + glob.glob(SITE + '/*/*.html') + glob.glob(SITE + '/*/*/*.html')):
    rel = os.path.relpath(f, SITE)
    if '.bak' in rel or rel.startswith(('e/', 'model_all')) or EXEMPT.match(rel): continue
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', open(f, encoding='utf-8', errors='ignore').read(), flags=re.S)
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))
    for m in PAT.finditer(t): hits.append((rel, t[max(0, m.start() - 70):m.end() + 50]))
print('no-confessions gate: %d hit(s)' % len(hits))
for rel, ctx in hits[:40]: print('  %s: ...%s...' % (rel, ctx))
sys.exit(1 if hits else 0)
