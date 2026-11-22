"""zeus_headline.py: the ZEUS headline (big number and line) from the summary as served at /zeus/live.json. Used by build_page.py and by
watch/headlines.py, so the page and the live headline say the same thing. PLAN.md (section 4, headline cell named in advance): zeus.tstm_hit_share,
the share of thunder-area grid points over the window's outlooks with at least one GLM flash within 25 statute miles in the valid period, with a
day block bootstrap 95 percent interval read against SPC's stated floor of 10 percent. Standard library only."""
import time
WORD = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell'}
def W(c): return WORD[c['outcome']] + (' (%s)' % c['reason'] if c.get('reason') else '')
def pc(x): return '' if x is None else ('%.1f' % (100 * x))
def day(d): return time.strftime('%d %B %Y', time.strptime(d, '%Y%m%d')).lstrip('0')
def headline(S):
    h = S['zeus']['tstm_hit_share']; t = S['zeus']['tstm_hit_share_10mi']; w0, w1 = S['frame']['window']
    s = ('Where the Storm Prediction Center drew its general thunder area on the 1300 UTC Day 1 outlook from %s to %s, the GOES Lightning Mapper saw at least one flash '
         'within 25 statute miles, a radius borrowed from the SPC severe definition, at %s percent of the points, with a 95%% interval of %s to %s percent. '
         'SPC states a 10 percent or higher chance of thunderstorms, and the reading is %s.' % (day(w0), day(w1), pc(h['value']), pc(h['lo']), pc(h['hi']), W(h)))
    s += ' Within 10 statute miles the share is %s percent, from %s to %s percent.' % (pc(t['value']), pc(t['lo']), pc(t['hi']))
    if S.get('partial'): s += ' Partial window: %d of %d days read.' % (S['days_read'], S['frame']['frame_days'])
    return '%s%%' % pc(h['value']), s
