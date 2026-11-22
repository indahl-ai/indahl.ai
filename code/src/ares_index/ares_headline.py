"""ares_headline.py: the ARES headline (big figure and line) from the summary as served at /ares/live.json. Used by build_page.py and by
watch/headlines.py, so the page and the live headline say the same thing. PLAN.md section 4, headline cell named in advance: ares.agree_share, of all
province-months in the window where either tracker recorded organized armed violence, the share where both did, with a 95 percent block bootstrap
interval by country and month. Wording from PLAN.md: "In N of M province-months with recorded armed violence, both public trackers agree".
Standard library only."""
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def mname(m): return '%s %s' % (MONTHS[int(m[5:7]) - 1], m[:4])


def pc(x): return '' if x is None else '%.1f' % (100 * x)


def headline(S):
    h = S['ares']['agree_share']; c = S['counts']; w0, w1 = S['frame']['window']
    if h['value'] is None:
        s = ('No province-month in the window from %s to %s has a recorded event from either public tracker on this run, so no share is formed.' % (mname(w0), mname(w1)))
    else:
        s = ('In %s of %s province-months with recorded armed violence, both public trackers agree. %s to %s, every month at least 30 days old. '
             'Share %s percent, 95 percent interval %s to %s percent. One tracker only: UCDP %s, GDELT %s.'
             % ('{:,}'.format(h['n']), '{:,}'.format(h['of']), mname(w0), mname(w1), pc(h['value']), pc(h['lo']), pc(h['hi']),
                '{:,}'.format(c['ucdp_only']), '{:,}'.format(c['gdelt_only'])))
    s += ' ' + S['labels'][0] + '.' if S.get('labels') else ''
    big = '%s of %s' % ('{:,}'.format(h['n']), '{:,}'.format(h['of'])) if h['value'] is not None else 'none'   # the ledger row reads n of of (live_headlines show n_of)
    return big, s
