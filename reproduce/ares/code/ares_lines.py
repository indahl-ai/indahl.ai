"""ares_lines.py: the hard lines of ARES (PLAN.md section 0), in code. Every fetch, the tick and the page builder import this, and each one fails
(AssertionError, exit non-zero) if a line is crossed.

  1. No casualties: no death, injury or fatality field is read past the filter, stored, printed or used for dot size.
  2. No sides: no actor, side, dyad or party name field is read past the filter, stored or printed.
  3. No flags, no country fills, no borders drawn. One footnote, exactly FOOTNOTE.
  4. Province at the finest. Never coordinates or towns in a stored table, the feed or the kit.
  5. Dot size is active_days. Displacement is left out.
Standard library only."""
import re

FOOTNOTE = 'This page takes no position on any border, name or claim.'

# Columns a source reader may look at. Nothing else in a row is ever copied out of the reader.
UCDP_READ = ('code_status', 'type_of_violence', 'where_prec', 'adm_1', 'country', 'date_prec', 'date_start', 'date_end')
# GDELT 2.0 event table, 61 tab-separated columns (GDELT-Event_Codebook-V2.0.pdf). Only these indices are read. Actor columns 5 to 24 and 35 to 50,
# the coordinates 56 and 57, the feature id 58 and the source URL 60 are never read.
GDELT_COLS = 61
GDELT_READ = {'SQLDATE': 1, 'IsRootEvent': 25, 'EventRootCode': 28, 'QuadClass': 29, 'NumSources': 32,
              'ActionGeo_Type': 51, 'ActionGeo_FullName': 52, 'ActionGeo_CountryCode': 53, 'ActionGeo_ADM1Code': 54}

# Key fragments that must never appear as a key in anything ARES stores, publishes or puts in the kit.
FORBIDDEN_KEY = re.compile(r'(death|injur|fatal|casualt|kill|wound|victim|best_est|^best$|^high$|^low$|actor|side_a|side_b|^side|dyad|party|parties|'
                           r'conflict_name|belligerent|perpetrat|target|latitude|longitude|^lat$|^lon$|^long$|^lng$|geom|coord|priogrid|adm_2|'
                           r'where_desc|town|city|village|displac|refugee|sourceurl|source_article|headline_src)', re.I)

for _k in list(UCDP_READ) + list(GDELT_READ):
    assert not FORBIDDEN_KEY.search(_k.replace('ActionGeo_', '')), 'ares_lines: a read column crosses a hard line: %s' % _k


def assert_clean(obj, where, path=''):
    """Fail if any dict key anywhere in obj matches FORBIDDEN_KEY. Used on every file ARES writes."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            assert not FORBIDDEN_KEY.search(str(k)), 'ares_lines: %s carries a forbidden field %r at %s' % (where, k, path or '/')
            assert_clean(v, where, path + '/' + str(k))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj[:200000]):
            assert_clean(v, where, '%s[%d]' % (path, i))


# Page and copy checks (build_page.py and lint_copy.py).
NUM_NEAR_HARM = re.compile(r'(\d[\d,.]*\s+(\w+\s+){0,3}(dead|deaths?|killed|fatalit\w*|casualt\w*|injur\w*|wounded|displaced|refugees?|lives))|'
                           r'((dead|deaths?|killed|fatalit\w*|casualt\w*|injur\w*|wounded|displaced|refugees?)\s+(\w+\s+){0,3}\d)', re.I)


def assert_page(html_text, visible_text):
    """The page lines: no number beside a harm word, the footnote exactly once, no drawn region (only circles in the map), no flag, no fills by country."""
    assert visible_text.count(FOOTNOTE) == 1, 'ares_lines: the no-position footnote must appear exactly once'
    m = NUM_NEAR_HARM.search(visible_text)
    assert not m, 'ares_lines: a number beside a harm word on the page: %r' % m.group(0)
    svg = re.findall(r'(?is)<svg.*?</svg>', html_text)
    for s in svg:
        for tag in re.findall(r'<\s*([a-zA-Z]+)', s):
            assert tag.lower() in ('svg', 'circle', 'title', 'g', 'rect', 'text', 'desc'), 'ares_lines: map holds a <%s>, only dots may be drawn' % tag
        assert s.count('<rect') <= 1, 'ares_lines: the map may hold one frame rect only, no region shapes'
    assert not re.search(r'[\U0001F1E6-\U0001F1FF]', html_text), 'ares_lines: flag emoji on the page'
    main = html_text.split('<main', 1)[-1]
    assert not re.search(r'(?i)<img|background-image|<iframe', main), 'ares_lines: images on the page (flags or drawn maps) are not allowed'
    assert not re.search(r'(?i)\bkilled\b|\bfatalit|\bcasualt|\binjur|\bwounded\b', visible_text), 'ares_lines: harm wording on the page'
