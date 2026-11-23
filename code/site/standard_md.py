"""standard_md.py (23 Nov 2026): renders the Heuremen Standard's STANDARD.md into HTML for indahl.ai/standard and quantumidleaudit.com/standard.
One source: the STANDARD.md in the files folder that faultsguards/CURRENT.json names (the same file indahl.ai serves at /standard/STANDARD.md).
Nothing is retyped: every heading, paragraph, list item and link is the file's own text, escaped. The H1 is left to the page hero.
Anchors: one per section (#scope, #terms, #how-to-read, #codes, #faults, #outcomes, #guards, #requirements, #versioning, #citation,
#provenance, #changes), one per subsection (#family-i, #part-i, #s6-1) and one per entry id (#QIA-F1, #FLT-01, #GRD-01, #REQ-01).
No inline script and no style attributes: each site passes its own class names.
  render(cls) -> (toc_html, body_html, n_sections)"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
FORGE = os.path.dirname(HERE)
CUR = json.load(open(os.path.join(FORGE, 'faultsguards', 'CURRENT.json'), encoding='utf-8'))
SRC = os.path.join(FORGE, CUR['files_dir'], 'STANDARD.md')
SEC_IDS = {'1': 'scope', '2': 'terms', '3': 'how-to-read', '4': 'codes', '5': 'faults', '6': 'outcomes', '7': 'guards',
           '8': 'requirements', '9': 'versioning', '10': 'citation', '11': 'provenance', 'Changes': 'changes'}
URL = re.compile(r'https?://[^\s<>()]+[^\s<>().,:]')
ENTRY = re.compile(r'^\*\*((?:FLT|GRD|REQ)-\d+)\b')


def _inline(s, cls):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return URL.sub(lambda m: '<a%s href="%s">%s</a>' % (_attr(cls.get('a', '')), m.group(0), m.group(0)), s)


def _attr(c):
    return ' class="%s"' % c if c else ''


def _sub_id(title):
    m = re.match(r'(QIA-F\d+)\b', title)
    if m: return m.group(1)
    m = re.match(r'(Family|Part) ([IVX]+)\.', title)
    if m: return '%s-%s' % (m.group(1).lower(), m.group(2).lower())
    m = re.match(r'(\d+)\.(\d+)\b', title)
    if m: return 's%s-%s' % (m.group(1), m.group(2))
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:40]


def render(cls=None, src=SRC):
    """cls: optional class names, keys h2 h3 p ul ol li a toc entry"""
    cls = cls or {}
    lines = open(src, encoding='utf-8').read().split('\n')
    out, toc, para, lst, ids = [], [], [], None, set()

    def flush_para():
        if not para: return
        txt = ' '.join(para); para.clear()
        m = ENTRY.match(txt); pid = m.group(1) if m else None
        if pid:
            assert pid not in ids, 'duplicate anchor ' + pid
            ids.add(pid)
        out.append('<p%s%s>%s</p>' % (' id="%s"' % pid if pid else '', _attr(cls.get('entry' if pid else 'p', '')), _inline(txt, cls)))

    def flush_list():
        nonlocal lst
        if lst is None: return
        tag, items = lst; lst = None
        out.append('<%s%s>%s</%s>' % (tag, _attr(cls.get(tag, '')), ''.join('<li%s>%s</li>' % (_attr(cls.get('li', '')), _inline(i, cls)) for i in items), tag))

    for ln in lines:
        if ln.startswith('# '):
            flush_para(); flush_list(); continue   # the title: the page hero carries it
        m = re.match(r'^(#{2,3}) (.+)$', ln)
        if m:
            flush_para(); flush_list()
            title = m.group(2).strip()
            if m.group(1) == '##':
                k = re.match(r'(\d+)\.', title); k = k.group(1) if k else title
                sid = SEC_IDS[k]; toc.append((sid, title))
                out.append('<h2 id="%s"%s>%s</h2>' % (sid, _attr(cls.get('h2', '')), _inline(title, cls)))
            else:
                sid = _sub_id(title)
                assert sid not in ids, 'duplicate anchor ' + sid
                out.append('<h3 id="%s"%s>%s</h3>' % (sid, _attr(cls.get('h3', '')), _inline(title, cls)))
            ids.add(sid); continue
        m = re.match(r'^(- |\d+\. )(.*)$', ln)
        if m:
            flush_para(); tag = 'ul' if m.group(1) == '- ' else 'ol'
            if lst is None or lst[0] != tag: flush_list(); lst = (tag, [])
            lst[1].append(m.group(2)); continue
        if not ln.strip():
            flush_para(); flush_list(); continue
        flush_list(); para.append(ln.strip())
    flush_para(); flush_list()
    assert len(toc) == len(SEC_IDS), 'STANDARD.md sections changed: %r' % [t for _, t in toc]
    toc_html = '<ol%s>%s</ol>' % (_attr(cls.get('toc', '')), ''.join('<li><a href="#%s">%s</a></li>' % (i, html.escape(re.sub(r'^\d+\.\s*', '', t))) for i, t in toc))
    return toc_html, '\n'.join(out), len(toc)


if __name__ == '__main__':
    t, b, n = render()
    print('%d sections, %d characters of HTML from %s' % (n, len(b), os.path.relpath(SRC, FORGE)))
