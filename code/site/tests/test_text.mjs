// Tests for tools_text.js (16 Nov 2026). Run: node tests/test_text.mjs
import { TOOLS_TEXT } from '../tools_text.js';
import { __setTestResolver } from '../toolkit_common.js';
__setTestResolver((h) => ({ ok: !/(^|\.)(localhost|local|internal)$/i.test(h) }));   // stubbed fetch: the DNS step is not sent to the stub (the real guard is tested in test_ssrf.mjs)
const T = Object.fromEntries(TOOLS_TEXT.map(t => [t.name, t]));
let bad = 0, n = 0; const ok = (name, cond, extra) => { n++; console.log((cond ? 'PASS ' : 'FAIL ') + name); if (!cond) { bad++; if (extra !== undefined) console.log('   ', JSON.stringify(extra).slice(0, 700)); } };
const run = async (name, args) => { const r = await T[name].run({}, args, {}); return r.data; };
const net = await fetch('https://example.com', { method: 'HEAD' }).then(r => r.ok).catch(() => false);
console.log('network:', net);

// ---- shape
ok('five tools, unique names, snake_case', TOOLS_TEXT.length === 5 && new Set(TOOLS_TEXT.map(t => t.name)).size === 5 && TOOLS_TEXT.every(t => /^[a-z_]+$/.test(t.name) && typeof t.run === 'function' && t.params && Array.isArray(t.required)));

// ---- quote_check
const SRC = 'Results. The model reached 91.2 percent accuracy on the held-out set, which the authors describe as a modest gain over the baseline. In the discussion they write that "adaptive sampling reduces variance in the estimate without changing its expected value" and caution that further work is needed. Smith said the committee "never saw the final draft" before the vote.';
let q = await run('quote_check', { text: 'The authors say “adaptive sampling reduces variance in the estimate without changing its expected value”.', source_text: SRC });
ok('quote VERBATIM (curly quotes)', q.quotes[0].label === 'VERBATIM' && q.outcome === 'VERBATIM', q);
q = await run('quote_check', { text: 'They write "Adaptive   Sampling reduces variance in the estimate — without changing its expected value".', source_text: SRC.replace('estimate without', 'estimate - without') });
ok('quote VERBATIM across case, whitespace and dash variants', q.quotes[0].label === 'VERBATIM', q);
q = await run('quote_check', { text: 'They write "adaptive sampling greatly reduces variance in the estimate without altering its expected value".', source_text: SRC });
ok('quote ALTERED with source words and diff', q.quotes[0].label === 'ALTERED' && /expected value/.test(q.quotes[0].source_words) && /greatly/.test(q.quotes[0].diff_text) && /changing/.test(q.quotes[0].diff_text) && q.quotes[0].similarity >= 0.7, q);
q = await run('quote_check', { text: 'He claimed "the vaccine was approved in under a week by every regulator".', source_text: SRC });
ok('quote NOT_FOUND', q.quotes[0].label === 'NOT_FOUND', q);
q = await run('quote_check', { text: 'The paper says "sampling that adapts reduces the variance of the estimate while its expected value is unchanged".', source_text: SRC });
ok('quote PARAPHRASE_IN_QUOTES (content-word overlap)', q.quotes[0].label === 'PARAPHRASE_IN_QUOTES' && q.quotes[0].content_word_overlap >= 0.7, q);
q = await run('quote_check', { text: 'They write "adaptive sampling reduces variance ... without changing its expected value".', source_text: SRC });
ok('quote ellipsis gap: VERBATIM_WITH_GAPS with omitted words printed', q.quotes[0].label === 'VERBATIM_WITH_GAPS' && q.quotes[0].omitted_source_words.length === 1 && /in the estimate/.test(q.quotes[0].omitted_source_words[0]), q);
q = await run('quote_check', { text: 'He said "the plan will ... work as intended".', source_text: 'He said the plan will not work as intended, and left.' });
ok('ellipsis that drops "not" prints it', q.quotes[0].label === 'VERBATIM_WITH_GAPS' && /not/.test(q.quotes[0].omitted_source_words[0]), q);
q = await run('quote_check', { text: 'He said "a sentence that cannot be anywhere in this short page".', source_text: 'tiny' });
ok('pasted short source still NOT_FOUND (user supplied full text)', q.quotes[0].label === 'NOT_FOUND', q);
ok('source_text_note on fetched-text tools', typeof q.source_text_note === 'string' && /untrusted/i.test(q.source_text_note));

q = await run('quote_check', { text: 'They write "without changing its expected value ... adaptive sampling reduces variance".', source_text: SRC });
ok('quote ellipsis out of order is not VERBATIM', q.quotes[0].label !== 'VERBATIM', q);
q = await run('quote_check', { text: 'Smith said the committee "never saw the final draft" before the vote.', source_text: SRC, attributed_to: 'Jane Smith' });
ok('attribution name reported near match, not a label', q.quotes[0].label === 'VERBATIM' && q.quotes[0].attribution_name_near_quote === true && !JSON.stringify(q).includes('"MISATTRIBUTED"') , q);
q = await run('quote_check', { text: '> adaptive sampling reduces variance in the estimate without changing its expected value\n\nOther text.', source_text: SRC });
ok('block quote read', q.quotes[0].label === 'VERBATIM' && q.quotes[0].form === 'block quote', q);
q = await run('quote_check', { text: 'plain sentence with no marks at all but quite long enough to be taken as one quote when the draft is short.', source_text: SRC });
ok('single unmarked text taken as one quote', q.quotes.length === 1 && q.quotes[0].form.startsWith('whole text'), q);
q = await run('quote_check', { text: 'He said "no way".', source_text: SRC });
ok('short span (<3 words) skipped, error-free CANNOT_TELL', q.outcome === 'CANNOT_TELL' && q.short_spans_skipped === 1, q);
q = await run('quote_check', { text: 'She said "something quite specific here".' });
ok('no source: CANNOT_TELL, no throw', q.outcome === 'CANNOT_TELL' && q.quotes[0].label === 'CANNOT_TELL', q);
{ const of = globalThis.fetch; globalThis.fetch = async (u, o) => /stub-short\.example\.net/.test(String(u)) ? new Response('<html><body>Please accept cookies to continue reading this article.</body></html>', { status: 200, headers: { 'content-type': 'text/html' } }) : of(u, o);
  q = await run('quote_check', { text: 'The article says "a sentence from the body that the wall hides".', source: 'https://stub-short.example.net/a' });
  globalThis.fetch = of; ok('cookie wall / body under 3000 chars -> CANNOT_TELL with scope named', q.quotes[0].label === 'CANNOT_TELL' && /characters of visible text/.test(q.quotes[0].read_scope), q); }
q = await run('quote_check', { text: 'x "a b c d" y', source: 'http://localhost/secret' });
ok('private URL refused as CANNOT_TELL', q.outcome === 'CANNOT_TELL' && /private|local/.test(q.reason), q);
q = await run('quote_check', {});
ok('quote_check empty args', q.outcome === 'CANNOT_TELL');
if (net) {
  q = await run('quote_check', { text: 'The page says "This domain is for use in documentation examples without requiring any permission".', source: 'https://example.com' });
  ok('network: example.com read, planted alteration found', q.read.http_status === 200 && q.quotes[0].label === 'ALTERED', q);
  q = await run('quote_check', { text: 'It says "this domain is for use in documentation examples without needing permission".', source: 'https://example.com' });
  ok('network: example.com VERBATIM', q.quotes[0].label === 'VERBATIM', q);
  q = await run('quote_check', { text: 'It says "a sentence that is surely not on this page at all".', source: '10.1038/nature14539' });
  ok('network: DOI resolving to landing page only + body quote -> CANNOT_TELL with scope', q.quotes[0].label === 'CANNOT_TELL' && /landing page|characters of visible text/.test(q.quotes[0].read_scope || ''), q);
}

// ---- number_check
const NSRC = 'Annual report. Revenue was $4.2 billion in 2023, up 12.34% from the prior year. Operating margin reached 18.5% for the full year. The company employed 12,400 people at year end. Net debt stood at $1.1 billion.';
let nn = await run('number_check', { text: 'Revenue was $4.2 billion in 2023, up 12.3% from the prior year. The company employed 12,400 people at year end.', source_text: NSRC });
const by = (d, f) => d.figures.find(x => x.figure === f);
ok('number HELD exact with source line', by(nn, '12,400').status === 'HELD' && /12,400 people/.test(by(nn, '12,400').source_line), nn);
ok('number HELD rounded: 12.3% vs 12.34%', by(nn, '12.3%').status === 'HELD' && /rounded/.test(by(nn, '12.3%').note), by(nn, '12.3%'));
ok('number HELD with $ and billion', by(nn, '$4.2 billion').status === 'HELD', by(nn, '$4.2 billion'));
nn = await run('number_check', { text: 'Operating margin reached 21.5% for the full year. Net debt stood at 3 trillion yen across 450 subsidiaries.', source_text: NSRC });
ok('number MOVED shows both values', by(nn, '21.5%').status === 'MOVED' && by(nn, '21.5%').source_candidates[0].figure === '18.5%', nn);
ok('number NO_SOURCE', nn.figures.some(f => f.figure === '450' && f.status === 'NO_SOURCE'), nn);
ok('MOVED ranks before HELD in outcome', nn.outcome === 'MOVED' && nn.figures[0].status === 'MOVED');
nn = await run('number_check', { text: 'The firm has 12400 staff? Revenue of $4.2B beat plans. Margin was 18.5 %.', source_text: NSRC });
ok('suffix B and spaced % read as same values', by(nn, '$4.2B').status === 'HELD' && nn.figures.find(f => f.figure.startsWith('18.5')).status === 'HELD', nn);
nn = await run('number_check', { text: 'Revenue of 4.2 billion.' });
ok('number_check no source -> CANNOT_TELL', nn.outcome === 'CANNOT_TELL' && nn.figures[0].status === 'CANNOT_TELL', nn);
nn = await run('number_check', { text: 'No digits here at all.', source_text: NSRC });
ok('number_check no numbers -> CANNOT_TELL', nn.outcome === 'CANNOT_TELL', nn);
nn = await run('number_check', { source_text: NSRC });
ok('number_check missing text no throw', nn.outcome === 'CANNOT_TELL');

nn = await run('number_check', { text: 'We report 94.1% accuracy on 1,200 test items, up from 91.0%.', source_text: 'The new model scored 94.1% accuracy; the previous version scored 90.2%.' });
ok('the referee sample: 94.1 HELD, 91.0 MOVED to 90.2 not 94.1', by(nn, '94.1%').status === 'HELD' && by(nn, '91.0%').status === 'MOVED' && by(nn, '91.0%').source_candidates[0].figure === '90.2%' && by(nn, '91.0%').source_candidates.every(c => c.figure !== '94.1%'), nn);
ok('1,200 with no plain figure in source -> NO_SOURCE', by(nn, '1,200').status === 'NO_SOURCE', nn);
nn = await run('number_check', { text: 'Accuracy was 55.0% on the sample.', source_text: 'Other results were reported. Noise was 12 units on the sample here.' });
ok('no shared context -> NO_SOURCE not MOVED', nn.figures[0].status === 'NO_SOURCE', nn);
nn = await run('number_check', { text: 'The model reached 94.1% accuracy on the held-out set.', source_text: 'The model reached 94% accuracy on the held-out set.' });
ok('PRECISION_ADDED when report is more precise than source', nn.figures[0].status === 'PRECISION_ADDED' && nn.outcome === 'PRECISION_ADDED', nn);
nn = await run('number_check', { text: 'The model reached 94% accuracy on the held-out set.', source_text: 'The model reached 94.1% accuracy on the held-out set.' });
ok('less precise report stays HELD with rounded note', nn.figures[0].status === 'HELD' && /rounded/.test(nn.figures[0].note), nn);
nn = await run('number_check', { text: 'Revenue of 4.2 billion.', source_text: 'Revenue was $4.2 billion.' });
ok('kind must match: plain vs currency is not HELD', nn.figures[0].status !== 'HELD', nn);

nn = await run('number_check', { text: 'Previous version: 55.0% apples.', source_text: 'Previous version: 12.0% oranges.' });
ok('only shared context words are stopwords -> NO_SOURCE', nn.figures[0].status === 'NO_SOURCE', nn);
nn = await run('number_check', { text: 'Operating margin reached 21.5% for the full year. Employees numbered 12,400 at year end.', source_text: NSRC });
ok('MOVED and HELD rows list shared_context_words, none a stopword', Array.isArray(by(nn, '21.5%').source_candidates[0].shared_context_words) && by(nn, '21.5%').source_candidates[0].shared_context_words.length >= 1 && Array.isArray(by(nn, '12,400').shared_context_words) && !by(nn, '21.5%').source_candidates[0].shared_context_words.some(w => ['the', 'for', 'was', 'up', 'previous'].includes(w)), nn);

// ---- claim_wording_check
let cw = await run('claim_wording_check', { text: 'Our results prove that the drug causes recovery. The effect was clearly significant. We are the first to show this works in all models. The difference was not significant (p = .21), so there is no difference between arms. Accuracy was 91% in the held-out set.' });
const rule = (r, id) => r.hits && r.hits.some(h => h.rule === id);
const rows = cw.sentences;
ok('proof language REVIEW with phrase-level suggestion', rule(rows.find(r => /prove/.test(r.sentence)), 'proof_language') && rows.find(r => /prove/.test(r.sentence)).hits[0].suggested_phrase === 'is consistent with', rows);
ok('cause from association', rule(rows.find(r => /prove/.test(r.sentence)), 'cause_from_association') && rows.find(r => /prove/.test(r.sentence)).hits.some(h => h.suggested_phrase === 'is associated with'));
ok('clearly removed and significant-without-test', (() => { const r = rows.find(r => /clearly/.test(r.sentence)); return rule(r, 'intensifier') && rule(r, 'significant_without_test'); })(), rows);
ok('first/novel and universal', (() => { const r = rows.find(r => /first to/.test(r.sentence)); return rule(r, 'priority_or_novelty') && rule(r, 'universal_wording'); })());
ok('no difference from non-significance', (() => { const r = rows.find(r => /not significant/.test(r.sentence)); return rule(r, 'no_effect_from_nonsignificance') && r.hits.some(h => h.suggested_phrase === 'no statistically significant difference'); })(), rows);
ok('plain result sentence KEEP', rows.find(r => /91%/.test(r.sentence)).status === 'KEEP');
ok('REVIEW listed first; REWORD not used; no replacement_sentence anywhere', rows[0].status === 'REVIEW' && cw.outcome === 'REVIEW' && !JSON.stringify(cw).includes('REWORD') && !JSON.stringify(cw).includes('replacement_sentence'));
cw = await run('claim_wording_check', { text: 'Our results prove that the intervention causes better outcomes.' });
ok('the referee sample hits BOTH proof_language and the causal rule', rule(cw.sentences[0], 'proof_language') && rule(cw.sentences[0], 'cause_from_association'), cw);
cw = await run('claim_wording_check', { text: 'In a randomized trial the treatment caused a 4 point drop (95% CI 2 to 6, p = .001).' });
ok('causal verb kept when a randomized design is in the sentence; test present', cw.sentences[0].status === 'KEEP', cw);
cw = await run('claim_wording_check', { text: 'Model A is significantly better than model B (p < .01).' });
ok('significant with p value present is not flagged', !cw.sentences[0].hits || !rule(cw.sentences[0], 'significant_without_test'), cw);
ok('method says rule-based', /Rule-based/.test(cw.method));
cw = await run('claim_wording_check', { text: '' });
ok('claim_wording empty -> CANNOT_TELL', cw.outcome === 'CANNOT_TELL');
cw = await run('claim_wording_check', { text: 'Thanks for reading this note. See you soon.' });
ok('no result sentence -> CANNOT_TELL', cw.outcome === 'CANNOT_TELL', cw);

// ---- source_check
let sc = await run('source_check', {});
ok('source_check empty -> CANNOT_TELL', sc.outcome === 'CANNOT_TELL');
sc = await run('source_check', { refs: ['Smith J. A paper about things. 2020.'] });
ok('unparsed reference -> CANNOT_TELL', sc.references[0].resolution === 'CANNOT_TELL', sc);
sc = await run('source_check', { text: 'See http://127.0.0.1/x and http://localhost/y.' });
ok('private hosts refused as CANNOT_TELL', sc.references.every(r => r.resolution === 'CANNOT_TELL'), sc);
{ const many = Array.from({ length: 18 }, (_, i) => `http://127.0.0.${i + 1}/x`).concat([]); sc = await run('source_check', { refs: many });
  ok('cap 15, rest NOT_CHECKED', sc.not_checked === 3 && sc.references.filter(r => r.resolution === 'NOT_CHECKED').length === 3, sc.not_checked); }
if (net) {
  sc = await run('source_check', { text: 'Deep learning is reviewed in Nature (https://doi.org/10.1038/nature14539). The page at https://example.com/ is a reserved example. A bad one: 10.9999/definitely.not.real.12345 and https://example.com/no-such-page-xyz. Attention is in arXiv:1706.03762.' });
  const g = (k) => sc.references.find(r => r.reference.includes(k));
  ok('network: DOI RESOLVES with Crossref title', g('nature14539').resolution === 'RESOLVES' && /deep learning/i.test(g('nature14539').title), g('nature14539'));
  ok('network: made-up DOI BROKEN (or CANNOT_TELL if Crossref rate-limits)', g('definitely.not.real').resolution === 'BROKEN' || (g('definitely.not.real').http_status === 429 && g('definitely.not.real').resolution === 'CANNOT_TELL'), g('definitely.not.real'));
  ok('network: 404 URL BROKEN', g('no-such-page').resolution === 'BROKEN', g('no-such-page'));
  ok('network: arXiv RESOLVES with current version', g('1706.03762').resolution === 'RESOLVES' && g('1706.03762').current_version >= 1, g('1706.03762'));
  ok('network: broken sorts before resolving; outcome BROKEN (or rate-limited)', (sc.outcome === 'BROKEN' && sc.references[0].resolution === 'BROKEN') || sc.references.some(r => r.http_status === 429), sc.references.map(r => r.resolution));
  sc = await run('source_check', { refs: [{ ref: 'https://example.com', claim: 'This domain is for use in illustrative examples in documents' }, { ref: 'https://example.com/', claim: 'Quantum chromodynamics predicts hadron masses on a lattice with fermion determinants' }] });
  ok('network: claim PASSAGE_FOUND', sc.references.some(r => r.claim_support && r.claim_support.label === 'PASSAGE_FOUND' && r.claim_support.content_word_overlap >= 0.5), sc);
  ok('claim support never labelled SUPPORTS', !JSON.stringify(sc).includes('"SUPPORTS"'));
}

{ const of = globalThis.fetch; const stub = (map) => async (u, o) => { const k = Object.keys(map).find(x => String(u).includes(x)); if (!k) return of(u, o); const [st] = map[k]; if (st === 'throw') { const e = new Error('t'); e.name = 'AbortError'; throw e; } return new Response('', { status: st }); };
  globalThis.fetch = stub({ 'a403.example.net': [403], 'a429.example.net': [429], 'a404.example.net': [404], 'a410.example.net': [410], 'atime.example.net': ['throw'] });
  sc = await run('source_check', { refs: ['https://a403.example.net/x', 'https://a429.example.net/x', 'https://a404.example.net/x', 'https://a410.example.net/x', 'https://atime.example.net/x'] });
  globalThis.fetch = of; const g = (k) => sc.references.find(r => r.reference.includes(k));
  ok('401/403/429/timeout are CANNOT_TELL, never BROKEN', g('a403').resolution === 'CANNOT_TELL' && g('a429').resolution === 'CANNOT_TELL' && g('atime').resolution === 'CANNOT_TELL', sc.references);
  ok('404 and 410 are BROKEN', g('a404').resolution === 'BROKEN' && g('a410').resolution === 'BROKEN'); }
{ const of = globalThis.fetch; globalThis.fetch = async (u, o) => /ok\.example\.net/.test(String(u)) ? new Response('', { status: 200 }) : of(u, o);
  sc = await run('source_check', { refs: Array.from({ length: 16 }, (_, i) => `https://ok.example.net/${i}`) }); globalThis.fetch = of;
  ok('NOT_CHECKED present: outcome CANNOT_TELL with unchecked count, not RESOLVES', sc.outcome === 'CANNOT_TELL' && sc.not_checked === 1 && /1 reference/.test(sc.unchecked_reason) && sc.counts.RESOLVES === 15, sc); }
ok('source_check carries source_text_note', typeof sc.source_text_note === 'string');
if (net) { sc = await run('source_check', { refs: ['arXiv:1706.03762v1'] });
  ok('network: version drift is RESOLVES with note and fields', sc.references[0].resolution === 'RESOLVES' && sc.references[0].version_cited === 1 && sc.references[0].version_drift === true && /version moved, cited v1, current v\d+/.test(sc.references[0].note), sc.references[0]);
  sc = await run('source_check', { refs: [{ ref: 'https://doi.org/10.1038/nature14539', claim: 'Deep learning discovers intricate structure in large data sets using backpropagation' }] });
  ok('network: abstract/landing-only scope never NO_MATCHING_PASSAGE', !sc.references[0].claim_support || sc.references[0].claim_support.label !== 'NO_MATCHING_PASSAGE', sc.references[0]); }

{ const of = globalThis.fetch; globalThis.fetch = async (u, o) => /fewwords\.example\.net/.test(String(u)) ? new Response('', { status: 200 }) : of(u, o);
  sc = await run('source_check', { text: 'Retracted work is cited here (https://fewwords.example.net/p).' }); globalThis.fetch = of;
  ok('citing sentence with < 3 content words -> CANNOT_TELL "no claim to match", never NO_MATCHING_PASSAGE', sc.references[0].claim_support && sc.references[0].claim_support.label === 'CANNOT_TELL' && sc.references[0].claim_support.reason === 'no claim to match' && sc.references[0].claim_support.label !== 'NO_MATCHING_PASSAGE', sc.references[0]); }

// ---- standards_card
const PAPER = 'Abstract\nWe report a best-case accuracy of 91.0% on 50 items. Data availability: the data are available at https://zenodo.org/records/1.\nResults\nIn a paired test, t(18) = 7.20, p < .001. A second test gave t(14) = 2.40, p = .030. In total 12 of 40 patients (45%) improved. Figure 2 shows the effect.';
let st = await run('standards_card', { text: PAPER });
ok('standards F5 scope names read scope', /read scope: pasted text/.test(st.card.codes.F5.scope), st.card.codes.F5.scope);
ok('standards F5 PRESENT with quote, location, arithmetic', st.card.codes.F5.status === 'PRESENT' && st.card.codes.F5.quotes.length >= 1 && st.card.codes.F5.quotes.every(x => x.text && x.where && x.arithmetic), st.card.codes.F5);
ok('standards F5 catches the percent (12 of 40 = 30%)', st.card.codes.F5.quotes.some(x => /12 of 40/.test(x.text)), st.card.codes.F5.quotes);
ok('standards needs-reading codes are CANNOT_TELL, none ABSENT', ['F1', 'F2', 'F3', 'F4', 'F6'].every(c => st.card.codes[c].status === 'CANNOT_TELL' && st.card.codes[c].reason === 'needs reading') && !JSON.stringify(st).includes('"ABSENT"'), st.card.codes);
ok('standards F4 finds availability statement; F7 in not_tested not codes', st.card.codes.F4.availability_statement_found === true && !('F7' in st.card.codes) && /F7/.test(st.not_tested), st.card.codes.F4);
ok('standards F2 cue found in abstract', st.card.codes.F2.cues.length >= 1, st.card.codes.F2);
st = await run('standards_card', { text: 'The sample was 20 patients. Of these 10 of 20 patients (50%) responded; t(20) = 2.09, p = .049.' });
ok('standards clean text: F5 CANNOT_TELL (needs reading), outcome CANNOT_TELL', st.card.codes.F5.status === 'CANNOT_TELL' && st.outcome === 'CANNOT_TELL', st);
st = await run('standards_card', {});
ok('standards empty -> CANNOT_TELL', st.outcome === 'CANNOT_TELL');
st = await run('standards_card', { id: 'not an id' });
ok('standards bad id -> CANNOT_TELL', st.outcome === 'CANNOT_TELL' && /DOI or arXiv/.test(st.reason), st);
if (net) {
  st = await run('standards_card', { id: '1706.03762' });
  ok('network: arXiv id card has work.id, notices, version, read', st.card.work.id === '1706.03762' && st.notices && st.version && st.read.http_status === 200, { notices: st.notices, version: st.version, read: st.read });
  ok('network: arXiv card codes present, F7 not in codes', ['F1', 'F2', 'F3', 'F4', 'F5', 'F6'].every(c => st.card.codes[c]) && !('F7' in st.card.codes), Object.keys(st.card.codes));
  st = await run('standards_card', { id: '10.1038/nature14539' });
  ok('network: DOI landing page gives CANNOT_TELL UNREADABLE codes, not ABSENT', st.outcome === 'CANNOT_TELL' && st.card.codes.F5.reason === 'UNREADABLE' && st.card.codes.F5.status === 'CANNOT_TELL', st);
}
if (net) { const w = await run('source_check', { text: 'Cited (https://doi.org/10.1016/S0140-6736(97)11096-0) here.' });
  ok('network: parenthesised Lancet DOI kept whole and RETRACTED (regression 16 Nov)', w.references[0].reference === '10.1016/S0140-6736(97)11096-0' && w.references[0].resolution === 'RETRACTED', w.references[0]); }
console.log(bad ? `${bad} FAILED of ${n}` : `all ${n} pass`); process.exit(bad ? 1 : 0);
