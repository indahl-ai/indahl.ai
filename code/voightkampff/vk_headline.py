"""vk_headline.py: the VOIGHT-KAMPFF headline (big figure and line) from the summary as served at /voightkampff/live.json. Used by build_page.py and by
watch/headlines.py, so the page and the live headline say the same thing. PLAN.md (Headline cell, named in advance): voightkampff.fpr_outcomes, the four-way
count of the false positive rate on known-human text against the maker's stated rate, with the no-test pairings counted beside it. Standard library only."""
def headline(S):
    f = S['voightkampff']['fpr_outcomes']; c = f['counts']; n = f['pairings']
    big = '%d of %d' % (c['CANNOT_TELL'], n)
    reasons = ', '.join('%d %s' % (v, k) for k, v in sorted(f['cannot_tell_by_reason'].items())) or 'none'
    s = ('Detector and test pairings with released output on known-human text, set beside the false positive rate the maker states: %d above, %d below, %d consistent and %d cannot tell (%s). '
         % (c['ABOVE'], c['BELOW'], c['CONSISTENT'], c['CANNOT_TELL'], reasons))
    s += ('%d more pairings returned no per-item output, and %d detectors have no independent test with released data. ' % (f['nothing_returned'], f['no_test']))
    if S.get('req13', {}).get('line'): s += 'Beside the pairings: ' + S['req13']['line'] + ' '
    s += S['label'] + '.'
    return big, s
