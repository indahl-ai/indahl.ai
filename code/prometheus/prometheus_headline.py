"""prometheus_headline.py: the PROMETHEUS headline (big figure and line) from the summary as served at /prometheus/live.json. Used by build_page.py and by
watch/headlines.py, so the page and the live headline say the same thing. PLAN.md (section 4, headline cell named in advance): prometheus.above_exceed_share,
of PSA-months rated above normal in the first month of each outlook, the share whose large-fire count exceeded that PSA's usual count for that month,
with its 95 percent interval, read against 0.5. Standard library only."""
WORD = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell'}
def W(c): return WORD[c['outcome']] + (' (%s)' % c['reason'] if c.get('reason') else '')
def pc(x): return '' if x is None else ('%.1f' % (100 * x))
def headline(S):
    h = S['prometheus']['above_exceed_share']; n = S['counts']; i0, i1 = S['frame']['issues']
    if h['value'] is None:
        s = ('The NIFC wildfire outlook says where significant fire activity is expected above normal. For the %d issues from %s to %s, the NIFC archive holds '
             'maps and PDFs and no Predictive Services Area polygons, so no rated area-month could be set beside the large fires that followed. '
             'The headline share reads %s. Held: %d issues. Nothing returned: %d.' % (n['frame_issues'], i0, i1, W(h), n['held'], n['nothing_returned']))
    else:
        s = ('Where the NIFC wildfire outlook rated a Predictive Services Area above normal for its first month, from %s to %s, the area had more large fires '
             'than its usual count in %s percent of %d area-months, with a 95%% interval of %s to %s percent. Read against more than half, it is %s.'
             % (i0, i1, pc(h['value']), h['psa_months'], pc(h['lo']), pc(h['hi']), W(h)))
    s += ' ' + ' '.join(S['labels']) if S.get('labels') else ''
    return h['display'], s
