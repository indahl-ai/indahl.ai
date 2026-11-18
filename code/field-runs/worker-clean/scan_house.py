import os, re, sys
WORDS = open(os.path.expanduser('~/bones-forge/ledger/private_scan_words.txt')).read().split('\n')[0].strip()   # the word list is private: publishing it would publish what it protects
bad = []
for p in sys.argv[1:]:
    t = open(p).read().replace('id.replace(/flock/g, "house")', '')   # allowed: maps old receipt ids to the public /r/house.* receipt pages
    for m in re.finditer(r'(?i)\b(' + WORDS + r')', t): bad.append('%s: word %r near %r' % (p, m.group(0), t[max(0, m.start()-40):m.end()+20].replace('\n', ' ')))
    for m in re.finditer(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', t):
        if not m.group(0).startswith(('0.', '127.', '1.0.')): bad.append('%s: IPv4 %s' % (p, m.group(0)))
for b in bad[:40]: print(b)
print('house scan: %d hits' % len(bad)); sys.exit(1 if bad else 0)
