"""cassandra_headline.py: the CASSANDRA headline (big number and line) from the summary as served at /cassandra/live.json. Used by build_page.py and by
watch/headlines.py, so the page and the live headline say the same thing. PLAN.md (Headline cell, named in advance): cassandra.ffw_hit_share, the share of
Flash Flood Warnings followed by a flash flood report in NCEI Storm Events inside the polygon before expiry, with its 95 percent interval. Standard library only."""
WORD = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell'}
def W(c): return WORD[c['outcome']] + (' (%s)' % c['reason'] if c.get('reason') else '')
def pc(x): return '' if x is None else ('%.1f' % (100 * x))
def num(x): return '{:,}'.format(int(x))
def headline(S):
    c = S['cassandra']['ffw_hit_share']; y0, y1 = S['frame']['window']
    s = ('Of %s flash flood warnings issued from %d to %d, %s percent were followed by a flash flood report in the NCEI Storm Events record inside the warning polygon before it expired, '
         'with a 95%% interval of %s to %s percent. Read against “likely” taken as more often than not, the share reads %s. Floods reported, not floods. '
         'PRELIMINARY: first run, not refereed.' % (num(c['warnings']), y0, y1, pc(c['value']), pc(c['lo']), pc(c['hi']), W(c)))
    r13 = S.get('req13') or {}
    if r13.get('line'): s += ' Beside the reading: ' + r13['line']
    return '%s%%' % pc(c['value']), s
