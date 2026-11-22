"""seldon_headline.py: the SELDON headline (big number and line) from the summary as served at /seldon/live.json. Used by build_page.py and by
watch/headlines.py, so the page and the live headline say the same thing. PLAN.md (section 4, headline cell named in advance):
seldon.cbo_range_hit_share, the share of CBO's stated two-thirds ranges, three or more years out, whose outcome fell inside the range, with a
95 percent interval from a bootstrap by report, read against the stated two-thirds (section 5). Standard library only."""
WORD = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell'}
def W(c): return WORD[c['outcome']] + (' (%s)' % c['reason'] if c.get('reason') else '')
def pc(x): return '' if x is None else ('%.1f' % (100 * x))
def headline(S):
    h = S['seldon']['cbo_range_hit_share']
    s = ('Of the two-thirds ranges the Congressional Budget Office printed for the deficit, the debt and average growth three or more years ahead, '
         '%d of %d held the outcome, or %s percent, with a 95%% interval of %s to %s percent. CBO states a two-thirds chance, and the reading is %s.'
         % (h['hits'], h['ranges'], pc(h['value']), pc(h['lo']), pc(h['hi']), W(h)))
    if h['outcome'] == 'ABOVE': s += ' More outcomes fell inside than stated, so the ranges were wider than needed.'
    elif h['outcome'] == 'BELOW': s += ' Fewer outcomes fell inside than stated, so the ranges were too narrow.'
    return '%s%%' % pc(h['value']), s
