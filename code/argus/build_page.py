#!/usr/bin/env python3
"""build_page.py: writes argus.html, the desk's page draft, from summary_argus.json. Reads no network. The live page is built by the site build, which
takes the body from this file."""
import json, os, sys, html
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
from argus_headline import headline
S = json.load(open('summary_argus.json'))
e = html.escape
WORD = {'ABOVE': 'above', 'BELOW': 'below', 'CONSISTENT': 'consistent', 'CANNOT_TELL': 'cannot tell', None: ''}
def Wd(c): return WORD[c['outcome']] + (' (%s)' % c['reason'] if c.get('reason') else '')
def f3(x): return '' if x is None else '%+.3f' % x
def pc(x): return '' if x is None else '%.0f' % (100 * x)
def num(x): return '{:,}'.format(int(x))
A = S['argus']; B = S['breeds']; G = S['gates']; F = S['frame']; SRC = S['source']; M = json.load(open('mapping.json'))
HL_BIG, HL_LINE = headline(S)
hl = '<section id="hl-slot" class="hl-slot hl"><div class="hl-big">%s</div><p class="hl-line">%s</p></section>' % (e(HL_BIG), e(HL_LINE))
def std_block(b):
    sd = M['breeds'][b]
    q = ' '.join('<span class="quote">&ldquo;%s&rdquo;</span>' % e(x) for x in sd['temperament'].split('; '))   # quoted in pieces at each semicolon of the source, words unchanged
    return '<p><b>%s</b>, %s (<a href="%s">standard</a>): %s</p>' % (e(b.title()), e(sd['standard']), e(sd['url']), q)
def phrase_table():
    out = []
    for b in B['read']:
        for ph in M['breeds'][b]['phrases']:
            if ph.get('no_trait'): where = 'no trait stated, left out of every count'
            elif not ph['factor']: where = 'no measured factor'
            else:
                fn = M['factors'][ph['factor']]; where = '%s, %s end' % (fn['name'], fn[ph['direction']])
            out.append('<tr><td>%s</td><td>%s</td><td><span class="quote">&ldquo;%s&rdquo;</span></td><td>%s</td></tr>' % (e(b.title()), e(ph['id']), e(ph['phrase']), e(where)))   # the standard's own words, quoted
    return ('<div class="tw"><table class="bench"><thead><tr><th>Breed</th><th>Row</th><th>Phrase</th><th>Mapped to</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>')
def triple_table():
    out = []
    for x in S['triples']:
        g = x['genetic']; o = x['owner_reported']
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s to %s</td><td>%s</td><td>%s</td><td>%s</td><td>%s to %s</td><td>%s</td></tr>' % (
            e(x['breed'].title()), e(x['factor_name']), e(x['stated_side']), e(', '.join(x['phrases'])), num(g['n']), f3(g['diff']), f3(g['lo']), f3(g['hi']), Wd(g),
            num(o['n']), f3(o['diff']), f3(o['lo']), f3(o['hi']), Wd(o)))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Breed</th><th>Factor</th><th>Stated side</th><th>Phrases</th><th>Dogs, ancestry 85 percent or more</th>'
            '<th>Breed mean minus other dogs</th><th>95% interval</th><th>Reading</th><th>Dogs, owner-reported breed</th><th>Breed mean minus other dogs</th><th>95% interval</th><th>Reading, shown only</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>')
def share_table():
    out = []
    for x in A['individual_stated_side_share']:
        out.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%d of %d</td><td>%s</td><td>%s to %s</td></tr>' % (
            e(x['breed'].title()), e(x['factor_name']), e(x['stated_side']), x['k'], x['n'], pc(x['share']), pc(x['lo']), pc(x['hi'])))
    return ('<div class="tw"><table class="bench"><thead><tr><th>Breed</th><th>Factor</th><th>Stated side</th><th>Dogs on the stated side</th><th>Percent</th><th>95% interval, percent</th></tr></thead><tbody>' + ''.join(out) + '</tbody></table></div>')
def gate_table():
    rows = ''.join('<tr><td>%s</td><td><span class="quote">&ldquo;%s&rdquo;</span></td><td>%+.2f</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
        e(M['factors'][x['factor']]['name']), e(x['text']), x['pattern'], num(x['n']), '' if x['r'] is None else '%+.3f' % x['r'], 'yes' if x['agrees'] else 'no') for x in G['direction'])
    return ('<div class="tw"><table class="bench"><thead><tr><th>Factor</th><th>Item with the largest loading</th><th>Loading</th><th>Dogs</th><th>Correlation of score with the answer</th><th>Same sign</th></tr></thead><tbody>' + rows + '</tbody></table></div>')
um = A['unmappable_count']; nt = A['no_trait_left_out']
unm = ', '.join('%s <span class="quote">&ldquo;%s&rdquo;</span>' % (e(u['id']), e(u['phrase'])) for u in S['unmappable'])
ntl = ', '.join('%s <span class="quote">&ldquo;%s&rdquo;</span>' % (e(u['id']), e(u['phrase'])) for u in S['no_trait'])
held = B['held']; held_top = ', '.join('%s %d' % (h['breed'], h['dogs']) for h in held[:12])
ref = '. '.join('%s: %s' % (e(b.title()), e(t)) for b, t in B['refused'].items())
dna = S['dna_claims']['claims']
dna_rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
    ('<a href="%s">%s</a>' % (e(c['url']), e(c['url'].split('/')[2])) if c.get('url') else 'product page'), ('&ldquo;%s&rdquo;' % e(c['quote'])) if c.get('quote') else 'no figure stated',
    'yes, ' + e(c['method_note']) if c.get('method_stated') and c.get('method_note') else ('no' if c.get('figure') else ''), 'none found' if c.get('figure') else '') for c in dna)
gate_line = 'All known-good checks passed on this run.' if G['passed'] else 'A known-good check did not pass on this run, so every reading shows cannot tell.'
body = hl + '''<p class="meta crumb">Division: <a href="/hermes">HERMES</a></p>
<p class="meta"><b>%s</b> Every result here is owner-reported behavior.</p>
<h2>Do dogs of a breed behave the way its standard says?</h2>
<p>A breed standard describes the temperament a breed club wants. The words are adjectives, not levels, and some of them state a direction, such as friendly or not aggressive. This page reads those words against the open Darwin&rsquo;s Ark release behind Morrill and colleagues, &ldquo;Ancestry-inclusive dog genomics challenges popular breed stereotypes&rdquo;, Science 2022. In that study owners answered short surveys on their dogs&rsquo; behavior, and the authors reduced the answers to behavior factors and estimated each dog&rsquo;s breed ancestry from its genome. The paper&rsquo;s own summary is that &ldquo;Breed offers little predictive value for individuals, explaining just 9%% of variation in behavior.&rdquo;</p>
<p>A dog counts as a member of a breed when at least 85 percent of its genetic ancestry comes from that breed, by the release&rsquo;s own estimates. A breed is read when at least 25 dogs meet that rule and its standard can be read. Each phrase of the standard&rsquo;s Temperament section was mapped to one of the %d scored behavior factors and a direction before any behavior data was opened. A phrase with no matching factor is counted apart and never forced. The mapping was read before the first run, and its changes are dated in the plan addendum. For each mapped statement the breed&rsquo;s mean factor score is set against the mean of all other dogs in the release, with a 95 percent interval from %s bootstrap draws over dogs. Each breed, factor and direction is counted once in the headline, and restated phrases are listed beside it. %s</p>
<h2>The breed standards as read</h2>
%s
%s
<h2>Breed averages against all other dogs</h2>
<p>A positive difference means the breed sits higher on the factor score than the other dogs in the release. The stated side is the end of the factor that the standard&rsquo;s words point to. Breed membership by genetic ancestry decides the reading. Membership by the breed the owner reported is printed beside it and decides nothing.</p>
%s
<p class="bench-note">Reading: consistent if the whole 95%% interval lies on the side the standard states. Above if the standard states the low end and the whole interval is above zero. Below if the standard states the high end and the whole interval is under zero. Otherwise cannot tell, with the reason STRADDLES_EDGE when the interval holds zero. The plan names no size that matters, so the both-alternatives test is not applied. Beside the headline: %s</p>
<h2>Individual dogs on the stated side</h2>
<p>A breed can average on the stated side while many of its own dogs do not. This is the share of each breed&rsquo;s dogs whose own score sits on the stated side of the other dogs&rsquo; mean, with a Wilson 95 percent interval.</p>
%s
<h2>Phrases with no measured factor</h2>
<p>Counted apart as nothing returned and never read: %s. State no trait and left out of every count: %s.</p>
<h2>Breeds not read</h2>
<p>Refused. %s</p>
<p>Held, fewer than %d dogs at 85 percent ancestry or more: %s breeds, the largest %s.</p>
<h2>Consumer DNA test accuracy claims</h2>
<p>Several makers of consumer dog DNA tests state a breed accuracy figure. None of the figures read comes with an independent test on released data, so this claim has no delivered side and is counted, not read. Claims with a figure and no independent test with released data: %d. The one independent study found, Rando and colleagues, JAVMA 2024 (DOI 10.2460/javma.23.07.0372), tested 12 purebred dogs, gives no data statement or repository, and cannot test claims about mixed ancestry.</p>
<div class="tw"><table class="bench"><thead><tr><th>Source</th><th>Stated</th><th>Method stated</th><th>Independent test with released data</th></tr></thead><tbody>%s</tbody></table></div>
<h2>Known-good checks</h2>
<p>The files match the checksums the archive gives. Every dog placed in a breed by the 85 percent rule carries the same breed in the release&rsquo;s own breed column (%s of %s). Each standard&rsquo;s Temperament text quoted here was found in the standard as fetched. The survey codes agree as the lowest answer and disagree as the highest, and for each factor the score moves with its largest item in the direction of the loading, which fixes which end of each score is which:</p>
%s
<h2>What this page holds and what it leaves out</h2>
<p>Behavior is owner-reported, not observed. Dogs in the release are those whose owners joined, which is not a sample of all dogs. A standard describes the breed as its club wants it, which may be read as an ideal rather than a claim about every dog, and this page still reads the words as written. Only breeds with at least 25 dogs at 85 percent ancestry or more are read, so most standards are not. The interval covers sampling of the dogs in the release and not how they came to join. A reading says where a breed&rsquo;s average sits. It does not say why.</p>
<p class="meta">Sources: Morrill et al., Science 376:eabk0639 (2022), DOI 10.1126/science.abk0639. Darwin&rsquo;s Ark data, Zenodo record 6522639, DOI 10.5281/zenodo.6522639, released under Creative Commons Zero v1.0 Universal, data freeze 15 November 2019. Breed standards as published by the breed registry named with each standard. All read without a key, one request at a time. Generated %s. Heuremen LLC.</p>
<p class="meta">The newest run is always in <a href="/argus/live.json">/argus/live.json</a>.</p>
<p class="meta">Plan and code for this page are public: <a href="https://github.com/indahl-ai/indahl.ai/tree/main/code/argus">argus</a>. The plan was fixed before the comparison it describes.</p>
<p class="meta">Data read from: <a href="https://zenodo.org/records/6522639">Darwin&rsquo;s Ark release on Zenodo</a> &middot; <a href="https://doi.org/10.5061/dryad.g4f4qrfr0">the same release on Dryad</a> &middot; <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC9675396">Morrill et al. 2022</a>.</p>
<p class="meta">Named here and want to answer a row? <a href="/respond?u=argus-all">Respond</a></p>
<section id="replies" data-prefix="argus"></section><script src="/replies.js" defer></script>''' % (
    e(S['label']), SRC['factors_scored'], num(F['bootstrap']['draws']), gate_line,
    ''.join(std_block(b) for b in B['read']), phrase_table(), triple_table(), e(S['req13']['line']), share_table(),
    unm, ntl, ref, F['min_dogs'], num(len(held)), e(held_top), A['dna_test_no_test_count'], dna_rows,
    num(G['membership_agree']), num(G['membership_of']), gate_table(), e(S['generated'][:10]))
TITLE = 'ARGUS | Breed standard temperament against open dog genetics | Heuremen LLC'
DESC = 'ARGUS: the temperament words in breed standards, mapped in advance to behavior factors, read against the open Darwin’s Ark genetic and owner survey data, with bootstrap intervals and the share of each breed’s own dogs on the stated side.'
page = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="https://indahl.ai/argus">
<meta name="author" content="Heuremen LLC">
<link rel="stylesheet" href="/style.css">
<style>.tw{overflow-x:auto}table.bench{border-collapse:collapse;font-size:.86rem}table.bench th,table.bench td{padding:.3rem .55rem;border-bottom:1px solid #ccc;text-align:left;white-space:nowrap}</style>
</head>
<body>
<header class="top"><div class="wrap bar"><a class="brand" href="/"><span>Heuremen LLC</span></a></div></header>
<section class="hero slim"><div class="wrap"><h1><b class="ac">ARGUS</b> &middot; Breed standard temperament against open dog genetics</h1></div></section>
<main class="wrap">%s</main>
</body>
</html>
''' % (e(TITLE), e(DESC), body)
open('argus.html', 'w').write(page); print('argus.html', len(page))
