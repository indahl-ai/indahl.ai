#!/usr/bin/env python3
"""build_crosswalk.py: ARES crosswalk (PLAN.md section 3). Maps UCDP's adm_1 names and GDELT's FIPS 10-4 first-order codes to one public first-level
boundary file, Natural Earth 1:10m Admin 1 (public domain), used only to group places into provinces and never drawn.

Reads place fields only (country, adm_1, FIPS code), never an event count. Append-only: an entry once written is never changed, so the crosswalk a
reading used is the one sealed before it (data/crosswalk_seal.json, written here, checked by ares_tick.py).

Rules, fixed here before any province-month is counted:
  Unit   a province is the set of Natural Earth rows that share one FIPS 10-4 code (a row with none is its own unit).
  GDELT  code equal to a unit's FIPS code, else to fips_alt of one unit only. Else held, listed by GDELT's code and spelling.
  UCDP   within the UCDP country's Natural Earth country: the adm_1 name, accents, punctuation and the unit word (state, province, oblast, ...) removed,
         equal to one province's name, name_alt, name_en, gn_name, woe_name, gns_name or name_local treated the same way (method exact).
         Where more than one row matches: name or name_en before other names, then the unit word against the file's type (oblast to Region).
         Else one unit within edit distance 2 of the name (six letters or more) and no other unit within distance 3 (method near_spelling, listed).
         Else one exact name match across the whole file, for a place the file lists under its own country name (method exact_elsewhere_in_file).
         Else held, listed by UCDP's spelling. Never guessed beyond these rules.
Standard library only."""
import hashlib, json, os, re, sys, time, unicodedata
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0, H)
import ares_lines as L

NE = json.load(open('data/ne_admin1_props.json'))
UNIT = r'(autonomous republic of|autonomous region|autonomous community|capital district|federal district|federal capital territory|special region|' \
       r'governorate|province|provincia de|provincia del|departamento de|departamento del|department|state of|state|oblast|kray|krai|region de|region|' \
       r'prefecture|district|county|municipality|division|territory|wilayah|wilaya|muhafazat|estado de|estado|republic of|republic|city of|' \
       r'parish|emirate|canton|zone|ostan|velayat|okrug|respublika|sharqiya|ili|il|mintaqat|dist\.)'
CTY = {'DR Congo (Zaire)': 'Democratic Republic of the Congo', 'Russia (Soviet Union)': 'Russia', 'Yemen (North Yemen)': 'Yemen', 'Myanmar (Burma)': 'Myanmar',
       'Cambodia (Kampuchea)': 'Cambodia', 'Tanzania': 'United Republic of Tanzania', 'Serbia (Yugoslavia)': 'Republic of Serbia', 'Congo': 'Republic of the Congo',
       'Ivory Coast': 'Ivory Coast', 'Bosnia-Herzegovina': 'Bosnia and Herzegovina', 'Macedonia, FYR': 'North Macedonia', 'Zimbabwe (Rhodesia)': 'Zimbabwe',
       'Madagascar (Malagasy)': 'Madagascar', 'Vietnam (North Vietnam)': 'Vietnam', 'Germany (Prussia)': 'Germany', 'Kingdom of eSwatini (Swaziland)': 'eSwatini',
       'Burkina Faso (Upper Volta)': 'Burkina Faso', 'Bahamas': 'The Bahamas', 'Guinea-Bissau': 'Guinea Bissau', 'East Timor': 'East Timor',
       'Israel': 'Israel', 'Palestine': 'Palestine', 'South Sudan': 'S. Sudan', 'Serbia': 'Republic of Serbia'}


def norm(s, unit=True):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    s = re.sub(r"[`'’ʼ]", '', s)
    if unit: s = re.sub(r'\b%s\b' % UNIT, ' ', s)
    return re.sub(r'[^a-z0-9]', '', s)


def lev(a, b):
    if abs(len(a) - len(b)) > 3: return 9
    p = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        c = [i]
        for j, cb in enumerate(b, 1): c.append(min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (ca != cb)))
        p = c
    return p[-1]


def names_of(r):
    out = set()
    for k in ('name', 'name_en', 'gn_name', 'woe_name', 'gns_name', 'name_local', 'name_alt'):
        for v in (r.get(k) or '').split('|'):
            for f in (norm(v), norm(v, unit=False)):
                if len(f) >= 3: out.add(f)
    return out


def unit_of(r):
    """The province unit: Natural Earth rows that share one FIPS 10-4 code are one unit (FIPS is GDELT's key, and some FIPS codes cover two Natural
    Earth rows, such as a city and the province around it). A row with no FIPS code is a unit of its own."""
    return 'F:' + r['fips'] if r.get('fips') else 'N:' + r['adm1_code']


BY_ADMIN, UNITS = {}, {}
for r in NE['rows']:
    BY_ADMIN.setdefault(r['admin'], []).append(r); UNITS.setdefault(unit_of(r), []).append(r)
NAMES = {r['adm1_code']: names_of(r) for r in NE['rows']}
MAIN = {r['adm1_code']: {f for k in ('name', 'name_en') for f in (norm(r.get(k)), norm(r.get(k), unit=False)) if f} for r in NE['rows']}
BY_FIPS_ALT = {}
for r in NE['rows']:
    for f in (r.get('fips_alt') or '').split('|'):
        if f: BY_FIPS_ALT.setdefault(f, []).append(r)
TYPES = {'oblast': {'region'}, 'state': {'state'}, 'province': {'province'}, 'governorate': {'governorate', 'province'}, 'region': {'region'},
         'department': {'department'}, 'county': {'county'}, 'prefecture': {'prefecture'}, 'district': {'district'}, 'division': {'division'},
         'city': {'municipality', 'city', 'capital city', 'metropolitan city', 'independent city', 'independent component city', 'highly urbanized city'}}


def ne_country(c):
    c2 = CTY.get(c, re.sub(r'\s*\(.*\)$', '', c))
    return c2 if c2 in BY_ADMIN else None


def pick(rows, adm):
    """One unit from candidate rows: name or name_en first, then the unit word against the boundary file's type. None if still more than one."""
    if not rows: return None
    a_n, a_f = norm(adm), norm(adm, unit=False)
    t1 = [r for r in rows if a_n in MAIN[r['adm1_code']] or a_f in MAIN[r['adm1_code']]]
    rows = t1 or rows
    if len({unit_of(r) for r in rows}) == 1: return rows[0]
    w = (adm.lower().split() or [''])[-1]
    ok = [r for r in rows if (r.get('type_en') or '').lower() in TYPES.get(w, set())]
    if len({unit_of(r) for r in ok}) == 1: return ok[0]
    if w not in ('city',):
        nc = [r for r in rows if 'city' not in (r.get('type_en') or '').lower() and 'municipal' not in (r.get('type_en') or '').lower()]
        if len({unit_of(r) for r in nc}) == 1: return nc[0]
    return None


def match_ucdp(country, adm):
    adm_n, adm_f = norm(adm), norm(adm, unit=False)
    if not adm.strip(): return None, 'blank name'
    cands = BY_ADMIN.get(ne_country(country) or '', [])
    ex = [r for r in cands if adm_n in NAMES[r['adm1_code']] or adm_f in NAMES[r['adm1_code']]]
    if ex:
        m = pick(ex, adm)
        return (m, 'exact') if m else (None, 'more than one province matches')
    if cands:
        d = sorted((min([lev(adm_n, n) for n in NAMES[r['adm1_code']]] or [9]), r['adm1_code']) for r in cands)
        near = [x for x in d if x[0] <= 2]
        if near and len(adm_n) >= 6 and len({unit_of(next(r for r in cands if r['adm1_code'] == c)) for _, c in near}) == 1 and \
                all(x[0] > 3 for x in d if unit_of(next(r for r in cands if r['adm1_code'] == x[1])) != unit_of(next(r for r in cands if r['adm1_code'] == near[0][1]))):
            return next(r for r in cands if r['adm1_code'] == near[0][1]), 'near_spelling'
    # the boundary file may file the place under another country name (for example a territory the boundary file lists on its own): one exact
    # match across the whole file, never a near spelling
    g = [r for r in NE['rows'] if adm_f in MAIN[r['adm1_code']] or norm(r['admin'], unit=False) == adm_f]
    if len({unit_of(r) for r in g}) == 1: return g[0], 'exact_elsewhere_in_file'
    return None, 'country not found in the boundary file' if not cands else 'no province matches'


def main():
    P = 'data/crosswalk.json'
    X = json.load(open(P)) if os.path.exists(P) else dict(boundary=dict(source=NE['source'], url=NE['url'], sha256=NE['sha256']), ucdp={}, gdelt={})
    assert X['boundary']['sha256'] == NE['sha256'], 'crosswalk: the boundary file changed, a new crosswalk needs a new seal'
    U = json.load(open('data/ucdp_pm.json')); G = json.load(open('data/gdelt_pm.json'))
    new = 0
    for r in U['rows']:
        k = r['country'] + '|' + r['adm_1']
        if k in X['ucdp']: continue
        m, how = match_ucdp(r['country'], r['adm_1'])
        X['ucdp'][k] = dict(country=r['country'], adm_1=r['adm_1'], province_key=unit_of(m) if m else None, method=how if m else 'held',
                            why=None if m else how, boundary_row=m['adm1_code'] if m else None); new += 1
    for r in G['rows']:
        k = r['adm1_code']
        if k in X['gdelt']: continue
        c, how = UNITS.get('F:' + k) or [], 'fips'
        if not c:
            c2 = BY_FIPS_ALT.get(k) or []
            if len({unit_of(r) for r in c2}) == 1: c, how = c2, 'fips_alt'
        m = c[0] if c else None
        X['gdelt'][k] = dict(adm1_code=k, country=r['country'], province=r['province'], province_key=unit_of(m) if m else None,
                             method=how if m else 'held', why=None if m else 'code not in the boundary file',
                             boundary_row=m['adm1_code'] if m else None); new += 1
    X['rules'] = __doc__.split('Rules, fixed here before any province-month is counted:')[1].split('Standard library only.')[0].strip()
    L.assert_clean(dict(X, ucdp=list(X['ucdp'].values()), gdelt=list(X['gdelt'].values())), P)   # name-keyed maps: the keys are place names, the fields are checked
    json.dump(X, open(P + '.tmp', 'w'), indent=1, ensure_ascii=False); os.replace(P + '.tmp', P)
    units = {u: rs[0]['adm0_a3'] for u, rs in UNITS.items()}   # the tick's only need from the boundary file: a block id per unit, no coordinates
    json.dump(dict(boundary_sha256=NE['sha256'], unit_country=units), open('data/ne_units.json', 'w'), separators=(',', ':'))
    sha = hashlib.sha256(open(P, 'rb').read()).hexdigest()
    json.dump(dict(crosswalk_sha256=sha, sealed=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), new_entries=new,
                   ucdp_entries=len(X['ucdp']), gdelt_entries=len(X['gdelt'])), open('data/crosswalk_seal.json', 'w'), indent=1)
    from collections import Counter
    print('crosswalk: new', new, 'ucdp', Counter(v['method'] for v in X['ucdp'].values()), 'gdelt', Counter(v['method'] for v in X['gdelt'].values()))


if __name__ == '__main__':
    main()
