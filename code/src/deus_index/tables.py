#!/usr/bin/env python3
"""tables.py: DEUS stated side helper. Reads a saved lab page (raw/stated/<host>/<slug>.html, untrusted, parsed as text with the standard
library HTMLParser, nothing executed) and writes <slug>.tables.txt: every <table> as rows of cells separated by ' | ', with its table number.
The reader uses these to find, for the page's own model column, the cell on each frame benchmark row, then quotes that cell word for word.
Usage: python3 -I tables.py <file.html> [...]"""
import sys, re
from html.parser import HTMLParser

class T(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.tables = []; self.stack = []; self.cell = None; self.row = None; self.skip = 0
    def handle_starttag(self, tag, a):
        if tag in ('script', 'style'): self.skip += 1
        elif tag == 'table': self.stack.append([])
        elif tag == 'tr' and self.stack: self.row = []
        elif tag in ('td', 'th') and self.row is not None: self.cell = []
        elif tag in ('br', 'p', 'div', 'sup') and self.cell is not None: self.cell.append(' ')
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip = max(0, self.skip - 1)
        elif tag in ('td', 'th') and self.cell is not None and self.row is not None:
            self.row.append(re.sub(r'\s+', ' ', ''.join(self.cell)).strip()); self.cell = None
        elif tag == 'tr' and self.row is not None and self.stack:
            if self.row: self.stack[-1].append(self.row)
            self.row = None
        elif tag == 'table' and self.stack: self.tables.append(self.stack.pop())
    def handle_data(self, d):
        if not self.skip and self.cell is not None: self.cell.append(d)

def tables(html_text):
    p = T(); p.feed(html_text); return p.tables

if __name__ == '__main__':
    for f in sys.argv[1:]:
        ts = tables(open(f, encoding='utf-8', errors='replace').read())
        with open(f[:-5] + '.tables.txt', 'w', encoding='utf-8') as o:
            for i, t in enumerate(ts):
                o.write('=== table %d (%d rows)\n' % (i + 1, len(t)))
                for r in t: o.write(' | '.join(r) + '\n')
        print(f, len(ts), 'tables')
