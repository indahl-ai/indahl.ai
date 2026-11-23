"""Title and description templates for indahl.ai pages built from data (SEO job, 22 Nov 2026).

Each function takes the page's own fields and returns a string inside the limits:
titles 60 characters or fewer, descriptions 155 or fewer. See site/SEO_COPY.md.
Copied 21 Nov 2026 from indahl-ai/calibrations lane-site 57bb751 (the designer) so the build does not read the calibrations checkout.
One change on copy (the operator): sagar_lookup_cat_desc said each passage and the data it differs from, which a lookup page does not show
(it lists each study with its codes), so it now says what the page shows."""
def cut(s, room):
    """Fit s into room characters at a word boundary; add … only if cut."""
    if len(s) <= room: return s
    s = s[:room-1]; s = s[:s.rfind(' ')] if ' ' in s else s
    STOP={'of','the','and','in','for','on','with','a','an','at','to','from'}
    w=s.rstrip(' ,:;-').split(' ')
    while len(w)>1 and w[-1].lower() in STOP: w.pop()
    return ' '.join(w).rstrip(' ,:;-') + '…'
def lc1(s): return s[:1].lower()+s[1:] if s and not s[:2].isupper() else s
def sagar(id_, version, labels, codes, page, title):
    head = f"Errata in arXiv {id_} {version}: {lc1(' and '.join(l.rstrip('.') for l in labels))} ({', '.join(codes)}{', page '+str(page) if page else ''}). "
    return head + '“' + cut(title, 155-len(head)-2) + '”'
def qia(id_, title, published, code, action):
    head = f"arXiv {id_} recount. Published: {lc1(published)}. QIA {code}: {lc1(action)} "
    return head + '“' + cut(title, 155-len(head)-2) + '”'
def iris(id_, title, codes, shows):
    first = shows.split('. ')[0].rstrip('.') + '.'
    head = f"arXiv {id_} recount, IRIS {', '.join(codes)}: "
    return cut(head + first, 155)
def oy_title(name):
    for t in (f"{name} | OY | indahl.ai", f"{name} | indahl.ai"):
        if len(t) <= 60: return t
    return cut(name, 60-len(" | indahl.ai")).rstrip('…') + " | indahl.ai"
def oy_desc(name, state):
    return cut(f"{name}, {state}: sentences naming AI on its public pages and AI course titles, found by script.", 155)
def hermes_title(name, middle=" | MODEL"):
    for t in (f"{name}{middle} | indahl.ai", f"{name} | indahl.ai"):
        if len(t) <= 60: return t
    return cut(name, 60-len(" | indahl.ai")).rstrip('…') + " | indahl.ai"
def hermes_desc(name):
    tail = ": each stated figure set against the published files, with the quote, entry and outcome."
    return cut(name, 155-len(tail)) + tail if len(name)+len(tail) > 155 else name + tail
def week_desc(date_words):
    # date_words: "Tuesday 17 November 2026", as the page already prints it
    return f"What changed on indahl.ai in the week from {date_words}: headline changes, first values and new desks, each with its time and link."
def sagar_lookup_cat_title(cat):
    return f"{cat} errata | SAGAR | indahl.ai"
def sagar_lookup_cat_desc(cat, cat_name):
    return cut(f"SAGAR errata in arXiv {cat} papers ({cat_name}): each study with its codes and a link to its page.", 155)
def entity_desc(kind_words, name):
    # kind_words: "the quantum backend", "the model family", "the package"
    return cut(f"Every row the Heuremen LLC desks publish about {kind_words} {name}, grouped by division, with a link to each page.", 155)
