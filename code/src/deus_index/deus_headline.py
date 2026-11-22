"""deus_headline.py: the DEUS headline (big figure and line) from the summary as served at /deus/live.json. Used by build_page.py and by
watch/headlines.py, so the page and the live headline say the same thing. PLAN.md (Headline cell, named in advance): deus.stated_above_share, the share
of claims with an independent rerun that read ABOVE, with its model-block bootstrap interval, and the full four-way count beside it. Standard library only."""
WORD = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell'}
def pc(x): return '' if x is None else ('%.0f' % (100 * x) if x in (0, 1) else '%.1f' % (100 * x))
def n(x): return '{:,}'.format(int(x))
def headline(S):
    h = S['headline']; f = h['four']; nr = S['no_rerun']['count']
    big = '%s of %s' % (n(h['n']), n(h['of']))
    s = ('Of %s benchmark scores the labs printed for their own models that have an independent rerun, %s sit above the whole rerun interval with every setup field matched '
         '(share %s percent, 95%% interval %s to %s percent, resampling whole models). Four-way: %s consistent, %s above, %s below, %s cannot tell.'
         % (n(h['of']), n(h['n']), pc(h['share']), pc(h['lo']), pc(h['hi']), n(f['CONSISTENT']), n(f['ABOVE']), n(f['BELOW']), n(f['CANNOT_TELL'])))
    d = h.get('cannot_tell_direction') or {}
    if f['CANNOT_TELL']:
        s += ' Of the cannot tell, %s have the stated score above the rerun interval and %s below it, with a setup field unnamed or different.' % (n(d.get('above', 0)), n(d.get('below', 0)))
    s += ' %s more stated scores in the frame have no independent rerun.' % n(nr)
    s += ' ' + ' '.join(S.get('label') or [])
    return big, s
