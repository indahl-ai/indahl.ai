"""argus_headline.py: the ARGUS headline (big number and line) from the summary as served at /argus/live.json. Used by build_page.py and by
watch/headlines.py, so the page and the live headline say the same thing. PLAN.md section 4 names argus.direction_outcomes as the headline cell, counted
on distinct breed, factor and direction triples (PLAN_ADDENDUM_referee1.md item 6), with argus.individual_stated_side_share printed beside it. Standard library only."""
WORD = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell'}
def pc(x): return '' if x is None else '%.0f' % (100 * x)
def headline(S):
    A = S['argus']; o = A['direction_outcomes']; n = A['triples']; sh = A['individual_stated_side_share']
    parts = ['%d %s' % (o[k], WORD[k]) for k in ('CONSISTENT', 'CANNOT_TELL', 'ABOVE', 'BELOW')]
    br = S['breeds']['read']
    names = ['the ' + b.title() for b in br]
    s = ('Of %d temperament statements in the breed standards of %s that map to a measured behavior factor, the genetic breed average set against all other dogs reads %s. '
         % (n, ' and '.join(names) if len(names) <= 2 else ', '.join(names[:-1]) + ' and ' + names[-1], ', '.join(parts[:-1]) + ' and ' + parts[-1]))
    lo = min(x['share'] for x in sh if x['share'] is not None); hi = max(x['share'] for x in sh if x['share'] is not None)
    s += 'Beside it, the share of each breed’s own dogs on the stated side runs from %s to %s percent%s. ' % (pc(lo), pc(hi), ', so in every statement some dogs of the breed sit on the other side' if hi < 1 else '')
    s += '%d statements map to no factor and are counted apart. Owner-reported behavior. %s' % (A['unmappable_count'], S['label'])
    return '%d of %d' % (o['CONSISTENT'], n), s
