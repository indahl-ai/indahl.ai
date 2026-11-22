// research.js (14 Nov 2026): checks a person brings to us, for the indahl.ai research connector (/mcp/research).
// paper_check: one paper by DOI or arXiv id. Retraction, correction and concern notices registered in Crossref (from publishers, and entries
// Refereed before release by the outside referee on our work, over three passes (14 Nov 2026). She caught the .05 decision flag missing
// "p < .05" errors, typo’d DOIs reading clean, unreadable lists reading NOT_INDEXED, receipts that did not bind the request, and overclaiming outcome words.
//   Crossref attributes to Retraction Watch), the current arXiv version, whether a page answers at each code and data link the paper states,
//   and whether QIA or IRIS indexed it.
// check_reported_statistics: reported test statistics and percentages in pasted text, recomputed (the method of statcheck, Nuijten et al.
//   2016, and of percentage recomputation). Deterministic arithmetic, no model.
// Nothing here writes or stores what a person sends (14 Nov: the worker has no observability or Logpush set, and no console.log here). Upstream
// fetches carry the DOI or arXiv id to Crossref and arXiv and are cached by URL for an hour. Every result says what was read, from where, and what could not be read.
const UA = 'indahl.ai research checks (https://indahl.ai/contact)';

// ---------- numerics: regularized incomplete beta and gamma (Numerical Recipes forms) ----------
function lgamma(x) {
  const c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
  let y = x, t = x + 5.5; t -= (x + 0.5) * Math.log(t); let s = 1.000000000190015;
  for (const k of c) s += k / ++y;
  return -t + Math.log(2.5066282746310005 * s / x);
}
function betacf(a, b, x) {
  const FPMIN = 1e-300; let qab = a + b, qap = a + 1, qam = a - 1, c = 1, d = 1 - qab * x / qap;
  if (Math.abs(d) < FPMIN) d = FPMIN; d = 1 / d; let h = d;
  for (let m = 1; m <= 300; m++) {
    const m2 = 2 * m; let aa = m * (b - m) * x / ((qam + m2) * (a + m2));
    d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN; c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN; d = 1 / d; h *= d * c;
    aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
    d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN; c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN; d = 1 / d;
    const del = d * c; h *= del; if (Math.abs(del - 1) < 3e-14) break;
  }
  return h;
}
function ibeta(a, b, x) {
  if (x <= 0) return 0; if (x >= 1) return 1;
  const bt = Math.exp(lgamma(a + b) - lgamma(a) - lgamma(b) + a * Math.log(x) + b * Math.log(1 - x));
  return x < (a + 1) / (a + b + 2) ? bt * betacf(a, b, x) / a : 1 - bt * betacf(b, a, 1 - x) / b;
}
function gammaQ(a, x) {   // upper regularized gamma Q(a, x)
  if (x <= 0) return 1;
  if (x < a + 1) { let ap = a, sum = 1 / a, del = sum; for (let n = 0; n < 500; n++) { ap++; del *= x / ap; sum += del; if (Math.abs(del) < Math.abs(sum) * 3e-14) break; }
    return 1 - sum * Math.exp(-x + a * Math.log(x) - lgamma(a)); }
  let b = x + 1 - a, c = 1e300, d = 1 / b, h = d;
  for (let i = 1; i < 500; i++) { const an = -i * (i - a); b += 2; d = an * d + b; if (Math.abs(d) < 1e-300) d = 1e-300; c = b + an / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; const del = d * c; h *= del; if (Math.abs(del - 1) < 3e-14) break; }
  return Math.exp(-x + a * Math.log(x) - lgamma(a)) * h;
}
const pT = (t, df) => ibeta(df / 2, 0.5, df / (df + t * t));                      // two-tailed
const pF = (f, d1, d2) => f <= 0 ? 1 : ibeta(d2 / 2, d1 / 2, d2 / (d2 + d1 * f));
const pChi = (x, df) => gammaQ(df / 2, x / 2);
const pZ = (z) => gammaQ(0.5, z * z / 2);                                           // two-tailed, erfc(|z|/sqrt2)
const pR = (r, df) => Math.abs(r) >= 1 ? 0 : pT(r * Math.sqrt(df / (1 - r * r)), df);
export const _stats = { pT, pF, pChi, pZ, pR };

// ---------- check_reported_statistics ----------
const NUM = '(-?\\d*\\.?\\d+)';
const half = (s) => { const d = (String(s).split('.')[1] || '').length; return 0.5 * Math.pow(10, -d); };
const TESTS = [
  { kind: 't', re: new RegExp('\\bt\\s*\\(\\s*(\\d+(?:\\.\\d+)?)\\s*\\)\\s*=\\s*' + NUM, 'gi'), p: (v, a) => pT(Math.abs(v), a[0]) },
  { kind: 'F', re: new RegExp('\\bF\\s*\\(\\s*(\\d+(?:\\.\\d+)?)\\s*,\\s*(\\d+(?:\\.\\d+)?)\\s*\\)\\s*=\\s*' + NUM, 'gi'), p: (v, a) => pF(v, a[0], a[1]) },
  { kind: 'chi2', re: new RegExp('(?:χ2|χ²|chi2|chi-square|chi²|X2)\\s*\\(\\s*(\\d+)(?:\\s*,\\s*N\\s*=\\s*\\d+)?\\s*\\)\\s*=\\s*' + NUM, 'gi'), p: (v, a) => pChi(v, a[0]) },
  { kind: 'r', re: new RegExp('\\br\\s*\\(\\s*(\\d+)\\s*\\)\\s*=\\s*' + NUM, 'gi'), p: (v, a) => pR(v, a[0]) },
  { kind: 'z', re: new RegExp('\\bz\\s*=\\s*' + NUM, 'gi'), p: (v) => pZ(Math.abs(v)) },
];
const PV = /^\s*,?\s*(?:ns,\s*)?p\s*(=|<|>|≤|≥|<=|>=)\s*(\d*\.?\d+)/i;
function judgeP(test, statStr, args, op, pStr, argStrs) {
  const v = parseFloat(statStr), h = half(statStr), lo = Math.abs(v) - h, hi = Math.abs(v) + h;
  const sgn = v < 0 ? -1 : 1;   // the p of a two-sided statistic depends on |v| only
  // 15 Nov 2026: a fractional df (Welch, Satterthwaite) is rounded too; "t(2.4) = 2.84, p = .086" sits inside df 2.35-2.45 and read ABOVE
  // when only the statistic’s rounding was allowed. Every corner of the statistic and df rounding ranges is tried.
  let variants = [args];
  (argStrs || []).forEach((a, i) => { if (/\./.test(String(a))) { const d = half(String(a)); variants = variants.flatMap(v0 => [-d, d].map(e => v0.map((x, j) => j === i ? Math.max(x + e, 0.01) : x))); } });
  const ps = variants.flatMap(ar => [test.p(sgn * Math.max(lo, 0), ar), test.p(sgn * hi, ar)]);
  const pmin = Math.min(...ps), pmax = Math.max(...ps), p0 = test.p(v, args), sp = parseFloat(pStr);
  let outcome;
  if (op === '=') { const ph = half(pStr); outcome = (sp + ph >= pmin && sp - ph <= pmax) ? 'CONSISTENT' : (sp > pmax ? 'ABOVE' : 'BELOW'); if (sp === 0) outcome = pmin < half(pStr) ? 'CONSISTENT' : 'BELOW'; }
  else if (op === '<') outcome = pmin < sp ? 'CONSISTENT' : 'BELOW';     // stated bound sits below every p the statistic allows
  else if (op === '≤' || op === '<=') outcome = pmin <= sp ? 'CONSISTENT' : 'BELOW';
  else outcome = pmax > sp ? 'CONSISTENT' : 'ABOVE';
  // 14 Nov (the referee MOVES 1): what the paper states about .05, against what the statistic allows (the whole rounding range, not one point)
  const statedSig = ((op === '<' || op === '≤' || op === '<=') && sp <= 0.05) || (op === '=' && sp < 0.05);
  const statedNon = ((op === '>' || op === '≥' || op === '>=') && sp >= 0.05) || (op === '=' && sp >= 0.05);
  const recSig = pmax < 0.05 ? true : pmin >= 0.05 ? false : null;
  const atEdge = op === '=' && sp === 0.05;   // 14 Nov (the referee): authors use "p = .05" both ways
  const decision = outcome === 'CONSISTENT' ? false : atEdge ? 'CANNOT_TELL' : recSig === null || (!statedSig && !statedNon) ? 'CANNOT_TELL' : (statedSig && !recSig) || (statedNon && recSig);
  return { recomputed_p: +p0.toPrecision(3), recomputed_range: [+pmin.toPrecision(3), +pmax.toPrecision(3)], outcome, changes_05_decision: decision };
}
const ONE_TAILED = /\b(one[- ]tailed|one[- ]sided|directional (?:test|hypothes))/i, CORRECTED = /\b(bonferroni|holm|fdr|benjamini|corrected|adjusted p|p[- ]?adj(?:usted)?|p_adj)\b/i;   // 14 Nov (the referee): bare "adjusted" (for age and sex) changes the model, not the p
function sentenceAt(src, i) { const a = Math.max(src.lastIndexOf('. ', i), src.lastIndexOf('\n', i)) + 1, b = src.indexOf('. ', i); return src.slice(a, b < 0 ? src.length : b); }
export function checkReportedStatistics(text) {
  const full = String(text || ''), LIM = 20000, src = full.slice(0, LIM).replace(/[−–]/g, '-'), rows = []; let capped = false, nearCut = 0;
  const oneTailedText = ONE_TAILED.test(src);
  for (const T of TESTS) {
    T.re.lastIndex = 0; let m;
    while ((m = T.re.exec(src))) { if (rows.length >= 200) { capped = true; break; }
      if (full.length > LIM && T.re.lastIndex > LIM - 40) { nearCut++; continue; }   // 14 Nov (the referee): the cut can split a number
      const statStr = m[m.length - 1], args = m.slice(1, -1).map(Number), after = src.slice(T.re.lastIndex, T.re.lastIndex + 40), pm = PV.exec(after);
      const quote = src.slice(m.index, T.re.lastIndex + (pm ? pm[0].length : 0)).replace(/\s+/g, ' ').trim();
      if (!pm) { rows.push({ kind: 'test', test: T.kind, quoted: quote, outcome: 'CANNOT_TELL', note: 'no p value directly after the statistic' }); continue; }
      const row = { kind: 'test', test: T.kind, quoted: quote, stated_p: pm[1] + pm[2], ...judgeP(T, statStr, args, pm[1], pm[2], m.slice(1, -1)),
        note: 'two-tailed p recomputed from the statistic and its degrees of freedom, allowing for the rounding of both' };
      if (row.outcome !== 'CONSISTENT') {   // 14 Nov (the referee, question b): wording that can explain the difference reads CANNOT_TELL, not ABOVE or BELOW
        const halfT = { ...T, p: (v, a) => T.p(v, a) / 2 }, j1 = (T.kind === 't' || T.kind === 'z' || T.kind === 'r') ? judgeP(halfT, statStr, args, pm[1], pm[2], m.slice(1, -1)) : null;
        if (oneTailedText && j1 && j1.outcome === 'CONSISTENT') Object.assign(row, { outcome: 'CANNOT_TELL', reason: 'ONE_TAILED_POSSIBLE', changes_05_decision: 'CANNOT_TELL', note: 'The text mentions a one-tailed or directional test and the stated p matches half the two-tailed p.' });
        else { const cw = sentenceAt(src, m.index).match(CORRECTED); if (cw) Object.assign(row, { outcome: 'CANNOT_TELL', reason: 'CORRECTED_POSSIBLE', trigger: cw[0], changes_05_decision: 'CANNOT_TELL', note: 'The same sentence mentions a correction ("' + cw[0] + '"), so the stated p may be adjusted.' }); }
      }
      if (row.outcome === 'ABOVE' || row.outcome === 'BELOW') { const dfs = m.slice(1, -1).filter(Boolean); if (dfs.length && dfs.every(d => !/\./.test(d))) row.df_policy = 'integer degrees of freedom read as exact'; }
      rows.push(row);
    }
  }
  const PC = /(\d+)\s*(?:of|\/|out of)\s*(\d+)\s*(?:participants|patients|subjects|cases|people|respondents)?\s*\(\s*(\d+(?:\.\d+)?)\s*%\s*\)/gi; let m;
  while ((m = PC.exec(src))) { if (rows.length >= 400) { capped = true; break; }
    const x = +m[1], n = +m[2], p = m[3]; if (!n) continue;
    const r = 100 * x / n, h = half(p) + 1e-9, sp = parseFloat(p);
    const okp = Math.abs(r - sp) <= h, slash = /^\d+\s*\/\s*\d+/.test(m[0]) && (n <= 20 || x > n);   // the referee 15 Nov: a large denominator is a count, x > y cannot be one
    // 15 Nov 2026: "1/5 (33.9%)" was a 1-to-5 rating with its share, not a count over a total. A mismatch in the slash form reads CANNOT_TELL
    // (a slash also writes ratings and ratios); "x of y (z%)" and "x out of y (z%)" keep ABOVE and BELOW. Only ever more cautious.
    rows.push({ kind: 'percentage', quoted: m[0].replace(/\s+/g, ' '), stated: p + '%', recomputed: +r.toFixed(3) + '%',
      outcome: okp ? 'CONSISTENT' : slash ? 'CANNOT_TELL' : (sp > r ? 'ABOVE' : 'BELOW'), ...(!okp && slash ? { reason: 'SLASH_MAY_BE_A_SCALE' } : {}),
      note: !okp && slash ? 'Written as x/y, which can be a rating or a ratio rather than a count over a total, so the difference is not read as an error.' : 'count divided by total, allowing for the rounding of the stated percentage' });
  }
  const tally = { CONSISTENT: 0, ABOVE: 0, BELOW: 0, CANNOT_TELL: 0 }; for (const r of rows) tally[r.outcome]++;
  const truncated = full.length > LIM || capped;
  const slashAside = rows.filter(r => r.reason === 'SLASH_MAY_BE_A_SCALE').length;
  return { found: rows.length, outcomes: tally, set_aside_as_possible_scales: slashAside, truncated, dropped_near_cut: nearCut, characters_read: Math.min(full.length, LIM), characters_sent: full.length,
    reading: (truncated ? 'Only part of the text was read (' + Math.min(full.length, LIM) + ' of ' + full.length + ' characters' + (capped ? ', row limit reached' : '') + (nearCut ? ', ' + nearCut + ' statistic(s) at the cut dropped' : '') + '). ' : '') + (rows.length ? 'Each reported value against the value its own statistic or counts give. ABOVE and BELOW say the stated value sits above or below what the numbers allow. Rows where the text mentions one-tailed tests or a correction read CANNOT_TELL with the reason. Typesetting errors can also explain a difference: read the quoted text before concluding anything.' : 'No reported test statistics (t, F, chi-square, r, z with a p value) or count-and-percentage pairs were found in the text.'),
    method: 'Two-tailed p from the reported statistic and degrees of freedom (as in statcheck, Nuijten et al. 2016), and percentages from their counts. Rounding of every reported number is allowed for. Measured against scipy, relative error under 2e-10. Known limit: sentence splitting breaks on abbreviations such as "et al." and "e.g.", so a correction word one clause back can be missed.',
    rows };
}

// ---------- paper_check ----------
const getJSON = async (url) => { try { const r = await fetch(url, { headers: { 'user-agent': UA, accept: 'application/json' }, cf: { cacheTtl: 3600 } }); return r.ok ? await r.json() : { _status: r.status }; } catch (e) { return { _error: String(e && e.name || e) }; } };
const getText = async (url) => { try { const r = await fetch(url, { headers: { 'user-agent': UA }, cf: { cacheTtl: 3600 } }); return r.ok ? await r.text() : null; } catch (e) { return null; } };
async function linkState(url) {
  const tryOne = async (method) => { const c = new AbortController(), t = setTimeout(() => c.abort(), 8000);
    try { const r = await fetch(url, { method, redirect: 'follow', headers: { 'user-agent': UA }, signal: c.signal }); return r.status; } catch (e) { return null; } finally { clearTimeout(t); } };
  let s = await tryOne('HEAD'); if (s === null || s === 405 || s === 403) s = await tryOne('GET');
  return { url, http_status: s, state: s === null ? 'CANNOT_TELL (no answer)' : s < 400 ? 'answers' : (s === 404 || s === 410) ? 'gone' : (s === 401 || s === 403 || s === 429) ? 'CANNOT_TELL (refused automated reads)' : 'error ' + s };
}
function parseId(raw) {
  const s = String(raw || '').trim().replace(/^https?:\/\/(dx\.)?doi\.org\//i, '').replace(/^doi:\s*/i, '');
  let m = s.match(/arxiv\.org\/(?:abs|pdf)\/([^\s?#]+?)(?:\.pdf)?$/i) || s.match(/^arxiv:\s*(\S+)$/i) || s.match(/^(\d{4}\.\d{4,5}(?:v\d+)?)$/) || s.match(/^([a-z\-]+(?:\.[A-Z]{2})?\/\d{7}(?:v\d+)?)$/i)
    || s.match(/^10\.48550\/arxiv\.(\S+)$/i);
  if (m) return { arxiv: m[1].replace(/v\d+$/, '') };
  if (/^10\.\d{4,9}\/\S+$/.test(s)) return { doi: s };
  return null;
}
async function arxivMeta(id) {
  const x = await getText(`https://export.arxiv.org/api/query?id_list=${encodeURIComponent(id)}&max_results=1`); if (!x) return null;
  const e = (x.split('<entry>')[1] || ''); if (!e) return null;
  const tag = (t) => { const m = e.match(new RegExp(`<${t}[^>]*>([\\s\\S]*?)</${t}>`)); return m ? m[1].replace(/\s+/g, ' ').trim() : null; };
  const idUrl = tag('id') || ''; const v = (idUrl.match(/v(\d+)$/) || [])[1];
  const doi = (e.match(/<arxiv:doi[^>]*>([^<]+)</) || [])[1] || null, comment = (e.match(/<arxiv:comment[^>]*>([\s\S]*?)</) || [])[1] || '';
  const summary = tag('summary') || '';
  const dec = (t) => t.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");
  const links = [...new Set(((dec(summary) + ' ' + dec(comment)).match(/https?:\/\/[^\s<>"')\]]+/g) || []).map(u => u.replace(/[.,;:]+$/, '')))].slice(0, 6);
  return { comment: comment.replace(/\s+/g, ' ').trim(), title: tag('title'), current_version: v ? +v : null, published: tag('published'), updated: tag('updated'), journal_doi: doi, links, url: idUrl.replace(/v\d+$/, '') };
}
async function crossrefRecord(doi) {   // 14 Nov (the referee MOVES 2): "no such record" (404) is not "did not answer"
  try { const r = await fetch(`https://api.crossref.org/works/${encodeURIComponent(doi)}`, { headers: { 'user-agent': UA, accept: 'application/json' }, cf: { cacheTtl: 3600 } });
    if (r.status === 404) return { state: 'NO_RECORD' }; if (!r.ok) return { state: 'NO_ANSWER', why: 'HTTP ' + r.status };
    return { state: 'READ', m: (await r.json()).message }; } catch (e) { return { state: 'NO_ANSWER', why: String(e && e.name || e) }; }
}
async function notices(doi, rec) {   // the union of updated-by on the record and the updates: filter (the referee: read both)
  const out = [], seen = new Set(), add = (o) => { const k = (o.notice_doi || '').toLowerCase() + '|' + o.type; if (!seen.has(k)) { seen.add(k); out.push(o); } };
  for (const u of (rec && rec['updated-by']) || []) add({ type: u.type, notice_doi: u.DOI, notice_link: 'https://doi.org/' + u.DOI, date: (u.updated && u.updated['date-time'] || '').slice(0, 10) || null, recorded_by: u.source || 'publisher', ...(u['record-id'] ? { record_id: u['record-id'] } : {}) });
  const d = await getJSON(`https://api.crossref.org/works?filter=updates:${encodeURIComponent(doi)}&rows=20`);
  if (!d || !d.message) return { read: !!rec, notices: out, filter_read: false };
  for (const it of d.message.items || []) for (const u of it['update-to'] || []) if (String(u.DOI || '').toLowerCase() === doi.toLowerCase())
    add({ type: u.type, notice_doi: it.DOI, notice_link: 'https://doi.org/' + it.DOI, date: (it.created && it.created['date-time'] || '').slice(0, 10) || null, recorded_by: u.source || 'publisher' });
  return { read: true, notices: out, filter_read: true };
}
const WITHDRAWN = /(?:^\s*|\bthis\s+)(?:paper|article|submission|manuscript|work)\s+(?:has\s+been\s+|is\s+|was\s+)?withdrawn\b|^\s*withdrawn\b|\b(?:paper|article|submission)\s+(?:is\s+|was\s+|has\s+been\s+)?withdrawn\s+by\s+the\s+authors?\b/i;   // 14 Nov (the referee): anchored to the start or to "this"
const esc = (x) => x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
export async function paperCheck(env, req, args) {
  const id = parseId(args.id); if (!id) return { error: 'Give a DOI (10.xxxx/...) or an arXiv id (2401.01234, arXiv:2401.01234 or an arxiv.org link).' };
  const out = { asked: String(args.id).slice(0, 200), checks: [] };
  let ax = null, doi = id.doi || null, recordExists = null;
  if (id.arxiv) {
    ax = await arxivMeta(id.arxiv); out.arxiv_id = id.arxiv;
    out.checks.push(ax ? { check: 'arXiv record', outcome: 'read', title: ax.title, current_version: ax.current_version, first_posted: ax.published, last_updated: ax.updated, link: ax.url,
      note: ax.current_version > 1 ? `Version ${ax.current_version} is current. Numbers quoted from an earlier version may have changed.` : 'Only one version posted.' } : { check: 'arXiv record', outcome: 'CANNOT_TELL', note: 'arXiv did not answer or has no record with this id.' });
    if (ax) { const w = (ax.comment || '').match(WITHDRAWN);   // 14 Nov (the referee MOVES 4): read on every arXiv record, its own check, a strict phrase
      out.checks.push({ check: 'arXiv comment on withdrawal', outcome: w ? 'MENTIONS_WITHDRAWAL' : 'NO_MENTION', ...(w ? { quoted: ax.comment.slice(0, 300) } : {}), note: w ? 'The arXiv comment says the paper was withdrawn. Read it.' : 'The arXiv comment does not say the paper was withdrawn.' }); }
    doi = (ax && ax.journal_doi) || null;
  }
  let rec = null;
  if (doi) {
    const r = await crossrefRecord(doi); recordExists = r.state === 'READ' ? true : r.state === 'NO_RECORD' ? false : null; rec = r.m || null;
    if (rec) { out.title = (rec.title || [])[0] || null; out.doi = doi; out.checks.push({ check: 'Crossref record', outcome: 'read', title: out.title, publisher: rec.publisher || null, journal: (rec['container-title'] || [])[0] || null, link: 'https://doi.org/' + doi }); }
    else out.checks.push({ check: 'Crossref record', outcome: r.state === 'NO_RECORD' ? 'NO_RECORD' : 'CANNOT_TELL', note: r.state === 'NO_RECORD' ? 'Crossref has no record for this DOI. Check the DOI for a typo.' : 'Crossref did not answer (' + r.why + ').' });
  }
  const nd = doi || (ax ? '10.48550/arXiv.' + id.arxiv : null);
  if (!nd || (doi && recordExists !== true) || (!doi && !ax)) {
    out.checks.push({ check: 'Retraction, correction and concern notices', outcome: 'CANNOT_TELL', note: 'No record was found at the source, so there is nothing to look notices up against.' });
  } else {
    const n = await notices(nd, rec);
    if (!n.read) out.checks.push({ check: 'Retraction, correction and concern notices', outcome: 'CANNOT_TELL', note: 'Crossref could not be read.' });
    else out.checks.push({ check: 'Retraction, correction and concern notices', outcome: n.notices.length ? 'FOUND' : 'NONE_FOUND', looked_up_under: nd, notices: n.notices,
      note: (n.notices.length ? 'Read each notice: a correction can be minor, a retraction withdraws the paper. ' : 'No notice is registered in Crossref for this DOI. A notice not yet registered would not show here. ')
        + 'Crossref lists notices from publishers and entries it attributes to Retraction Watch (recorded_by: retraction-watch).' + (doi ? '' : ' Preprints are rarely corrected through Crossref, so NONE_FOUND here says little.') + (n.filter_read ? '' : ' Only the record itself was read, the notice search did not answer.') });
  }
  if (!out.title && ax) out.title = ax.title;
  const links = ax ? ax.links : [];
  if (links.length) { const st = await Promise.all(links.map(linkState)); out.checks.push({ check: 'Code and data links stated in the abstract and comments', outcome: st.every(s => s.state === 'answers') ? 'ALL_ANSWER' : st.some(s => s.state === 'gone') ? 'SOME_GONE' : 'SOME_CANNOT_TELL', links: st, note: 'A page answered at each link marked answers. Whether it holds the stated code or data was not read.' }); }
  else out.checks.push({ check: 'Code and data links stated in the abstract and comments', outcome: ax ? 'NONE_STATED' : 'CANNOT_TELL', note: ax ? 'The arXiv abstract and comments state no links.' : 'Only arXiv records are read for links.' });
  // 21 Nov 2026 (owner: retire every tool that reads our study index): paper_check reads live sources only, no lookup into the QIA or IRIS List.
  out.reading = 'Each check says what was read and from where. NONE_FOUND means nothing was registered at the source when read, not that the paper is sound.';
  return out;
}

// ---------- link_rot and arxiv_version_drift on one paper (21 Nov 2026, owner: one server, checks a person brings) ----------
// Both read live sources only (arXiv and the links themselves). Neither reads the indahl.ai study index.
export async function linkRotCheck(args) {
  const raw = String(args.id || '').trim(), given = String(args.urls || '').split(/[\s,]+/).filter(u => /^https?:\/\/\S+$/i.test(u)).slice(0, 10);
  if (!raw && !given.length) return { outcome: 'CANNOT_TELL', reason: 'Give an arXiv id or up to 10 URLs.' };
  let links = given, read = null;
  if (raw) { const id = parseId(raw); if (!id || !id.arxiv) return { outcome: 'CANNOT_TELL', reason: 'The id is not an arXiv id. Pass the links as urls instead.' };
    const ax = await arxivMeta(id.arxiv); if (!ax) return { arxiv_id: id.arxiv, outcome: 'CANNOT_TELL', reason: 'arXiv did not answer or has no record with this id.' };
    read = { arxiv_id: id.arxiv, title: ax.title, current_version: ax.current_version, link: ax.url }; links = [...new Set([...ax.links, ...given])].slice(0, 10); }
  if (!links.length) return { ...(read || {}), outcome: 'NONE_STATED', links: [], note: 'The arXiv abstract and comments state no links.' };
  const st = await Promise.all(links.map(linkState)), gone = st.filter(s => s.state === 'gone').length, ans = st.filter(s => s.state === 'answers').length;
  return { ...(read || {}), outcome: gone ? 'SOME_GONE' : ans === st.length ? 'ALL_ANSWER' : 'SOME_CANNOT_TELL', links_read: st.length, answer: ans, gone, cannot_tell: st.length - ans - gone, links: st,
    note: 'A page answered at each link marked answers. Whether it holds the stated code or data was not read. Links that refuse automated reads are CANNOT_TELL, not gone.' };
}
const absNums = (t) => (String(t || '').match(/\d+(?:\.\d+)?%?/g) || []).sort();
export async function arxivVersionCheck(args) {
  const raw = String(args.id || '').trim(), id = parseId(raw); if (!id || !id.arxiv) return { outcome: 'CANNOT_TELL', reason: 'Give an arXiv id (2401.01234, arXiv:2401.01234 or an arxiv.org link).' };
  const cur = await arxivMeta(id.arxiv); if (!cur) return { arxiv_id: id.arxiv, outcome: 'CANNOT_TELL', reason: 'arXiv did not answer or has no record with this id.' };
  const vm = String(args.version_read || (raw.match(/v(\d+)\s*$/) || [])[1] || '').replace(/^v/i, ''), vr = /^\d{1,3}$/.test(vm) ? +vm : null;
  const w = (cur.comment || '').match(WITHDRAWN);
  const out = { arxiv_id: id.arxiv, title: cur.title, current_version: cur.current_version, first_posted: cur.published, last_updated: cur.updated, link: cur.url, journal_doi: cur.journal_doi,
    withdrawal_in_comment: w ? cur.comment.slice(0, 300) : null };
  if (vr === null) return { ...out, outcome: cur.current_version > 1 ? 'LATER_VERSIONS_EXIST' : 'ONE_VERSION', note: 'Pass version_read (the version you read, for example 1) to compare its title and abstract numbers with the current version.' };
  if (vr >= cur.current_version) return { ...out, version_read: vr, outcome: 'READ_IS_CURRENT', note: 'The version read is the current version.' };
  const old = await arxivMeta(id.arxiv + 'v' + vr); if (!old) return { ...out, version_read: vr, outcome: 'CANNOT_TELL', reason: 'arXiv did not return version ' + vr + '.' };
  const curX = await getText(`https://export.arxiv.org/api/query?id_list=${encodeURIComponent(id.arxiv)}&max_results=1`), oldX = await getText(`https://export.arxiv.org/api/query?id_list=${encodeURIComponent(id.arxiv + 'v' + vr)}&max_results=1`);
  const summ = (x) => { const e = (String(x || '').split('<entry>')[1] || ''); const m = e.match(/<summary[^>]*>([\s\S]*?)<\/summary>/); return m ? m[1].replace(/\s+/g, ' ').trim() : ''; };
  const a = absNums(summ(oldX)), b = absNums(summ(curX)), numsChanged = a.join('|') !== b.join('|'), titleChanged = (old.title || '') !== (cur.title || '');
  return { ...out, version_read: vr, outcome: numsChanged ? 'ABSTRACT_NUMBERS_CHANGED' : titleChanged ? 'TITLE_CHANGED' : 'NUMBERS_SAME',
    title_read: old.title, abstract_numbers_read: a, abstract_numbers_current: b,
    note: 'Compares the title and the numbers stated in the abstract of the version read with the current version. A change in the body of the paper would not show here.' };
}

// ---------- paper_statistics (15 Nov 2026, the owner) ----------
// The full text of one arXiv paper, read from arXiv’s own HTML rendering (LaTeXML), with every reported test statistic and percentage
// recomputed by checkReportedStatistics. Math is read from LaTeXML’s alttext (the LaTeX the authors typed). The references section is cut.
// Text is read in chunks that end on paragraph breaks, so no number is split. Sends only the arXiv id to arxiv.org.
export function htmlToText(h) {
  const dec = (s) => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&nbsp;/g, ' ').replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n)).replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16))).replace(/&amp;/g, '&');
  h = h.replace(/<(script|style|nav|header|footer)\b[\s\S]*?<\/\1>/gi, ' ');
  h = h.replace(/<math\b[^>]*?alttext="([^"]*)"[\s\S]*?<\/math>/gi, (_, a) => ' ' + a.replace(/\\mathrm\{([^}]*)\}|\\text\{([^}]*)\}/g, '$1$2').replace(/\\(?:left|right|,|;|!|quad)/g, '').replace(/[{}]/g, '') + ' ');
  h = h.replace(/<\/(p|div|section|h[1-6]|li|tr|table|figure|caption)>/gi, '\n\n').replace(/<br\s*\/?>/gi, '\n');
  return dec(h.replace(/<[^>]+>/g, ' ')).replace(/[ \t]+/g, ' ').replace(/\n\s*\n\s*(\n\s*)+/g, '\n\n').trim();
}
export async function paperStatistics(args) {
  const id = parseId(args.id);
  if (!id || !id.arxiv) return { error: 'Give an arXiv id (2401.01234, arXiv:2401.01234 or an arxiv.org link). The full text is read from arXiv, so DOIs of journal papers are not covered here.' };
  const url = 'https://arxiv.org/html/' + id.arxiv, html = await getText(url);
  if (!html) return { arxiv_id: id.arxiv, outcome: 'CANNOT_TELL', reason: 'NO_HTML', note: 'arXiv has no HTML version of this paper (some papers are posted as PDF only, or failed to convert), so its text could not be read here.', source: url };
  // the referee 15 Nov: cut only the bibliography block (appendices often hold the full statistics); count LaTeXML conversion errors; record the version
  const version = (html.match(new RegExp('arXiv:' + id.arxiv.replace('.', '\\.') + '(v\\d+)')) || [])[1] || null;
  const convErrors = (html.match(/class="[^"]*\bltx_ERROR\b/g) || []).length;
  const bib = html.match(/<section[^>]*class="[^"]*\bltx_bibliography\b[\s\S]*?<\/section>/);
  const cut = bib ? bib[0].length : 0;
  let text = htmlToText(bib ? html.replace(bib[0], ' ') : html);
  const chunks = []; let cur = '';
  for (const para of text.split(/\n\n/)) { if (cur.length + para.length + 2 > 19000 && cur) { chunks.push(cur); cur = ''; } cur += (cur ? '\n\n' : '') + para.slice(0, 19000); }
  if (cur) chunks.push(cur);
  const rows = [], tally = { CONSISTENT: 0, ABOVE: 0, BELOW: 0, CANNOT_TELL: 0 }; let method = '';
  for (const c of chunks.slice(0, 20)) { const r = checkReportedStatistics(c); method = r.method; for (const x of r.rows) { rows.push(x); tally[x.outcome]++; } }
  const flagged = rows.filter(r => r.outcome !== 'CONSISTENT');
  const read = chunks.slice(0, 20).reduce((s, c) => s + c.length, 0), nread = Math.min(chunks.length, 20);
  const aside = rows.filter(r => r.reason === 'SLASH_MAY_BE_A_SCALE').length;
  const scope = `Read: ${nread} chunk(s), ${read} characters, arXiv version ${version || 'not stated on the page'}; conversion errors on the page: ${convErrors}. Not checked: tables, figures, supplementary files, the bibliography, and any part the arXiv HTML failed to convert.`;
  return { arxiv_id: id.arxiv, version, source: url, characters_read: read, bibliography_cut: !!bib, conversion_errors: convErrors, chunks_read: nread, chunks_total: chunks.length,
    found: rows.length, outcomes: tally, set_aside_as_possible_scales: aside,
    reading: rows.length ? `${rows.length} reported statistic(s) and percentage(s) found; ${tally.CONSISTENT} consistent with their own numbers, ${tally.ABOVE + tally.BELOW} not, ${tally.CANNOT_TELL} cannot be told from the text${aside ? ' (' + aside + ' written as x/y and set aside as possible scales)' : ''}. ` + scope
      : 'No checkable test statistics found in the text we read. This does not mean the paper’s statistics are correct, or that it has none. ' + scope,
    method, rows: flagged.concat(rows.filter(r => r.outcome === 'CONSISTENT')).slice(0, 200) };
}
