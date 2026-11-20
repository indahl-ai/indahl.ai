// tools_stats.js (16 Nov 2026): the stats-method skills as deterministic, read-only MCP tools.
// interval_verdict (cannot-tell), margin_check (margin), triangulate_readings (triangulate), controls_check (controls),
// two_explanations (both), eval_setup_check (eval-check). Pure arithmetic and rule-based text matching, no model. Nothing is stored or logged.
// Only eval_setup_check may fetch (a public Hugging Face model card named by the caller).
import { answer, fetchText, safeUrl, clip } from './toolkit_common.js';

const SRC = 'https://indahl.ai/tools';

// ---------- numerics (own copies: regularized upper incomplete gamma gives normal and chi-square tails) ----------
function lgamma(x) {
  const c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
  let y = x, t = x + 5.5; t -= (x + 0.5) * Math.log(t); let s = 1.000000000190015;
  for (const k of c) s += k / ++y;
  return -t + Math.log(2.5066282746310005 * s / x);
}
function gammaQ(a, x) {
  if (x <= 0) return 1;
  if (x < a + 1) { let ap = a, sum = 1 / a, del = sum; for (let n = 0; n < 500; n++) { ap++; del *= x / ap; sum += del; if (Math.abs(del) < Math.abs(sum) * 3e-14) break; }
    return 1 - sum * Math.exp(-x + a * Math.log(x) - lgamma(a)); }
  let b = x + 1 - a, c = 1e300, d = 1 / b, h = d;
  for (let i = 1; i < 500; i++) { const an = -i * (i - a); b += 2; d = an * d + b; if (Math.abs(d) < 1e-300) d = 1e-300; c = b + an / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; const del = d * c; h *= del; if (Math.abs(del - 1) < 3e-14) break; }
  return Math.exp(-x + a * Math.log(x) - lgamma(a)) * h;
}
const erfcAbs = (x) => gammaQ(0.5, x * x);                                // erfc(|x|)
const Phi = (z) => (z >= 0 ? 1 - 0.5 * erfcAbs(z / Math.SQRT2) : 0.5 * erfcAbs(z / Math.SQRT2));
const pTwo = (z) => erfcAbs(Math.abs(z) / Math.SQRT2);
const pChi2 = (x, df) => gammaQ(df / 2, x / 2);
function zcrit(level) { let lo = 0, hi = 12; for (let i = 0; i < 100; i++) { const m = (lo + hi) / 2; (pTwo(m) > 1 - level ? lo = m : hi = m); } return (lo + hi) / 2; }

// ---------- input parsing ----------
const num = (x) => { if (x == null || typeof x === 'boolean') return null; if (typeof x === 'number') return Number.isFinite(x) ? x : null; if (typeof x === 'string' && x.trim() !== '') { const n = Number(x.trim()); return Number.isFinite(n) ? n : null; } return null; };
const jparse = (x) => { if (typeof x !== 'string') return x; try { return JSON.parse(x); } catch (e) { return undefined; } };
const arr = (x) => { const v = jparse(x); return Array.isArray(v) ? v : null; };
const obj = (x) => { const v = jparse(x); return v && typeof v === 'object' && !Array.isArray(v) ? v : null; };
const r6 = (x) => (x == null || !Number.isFinite(x) ? x : Number(x.toPrecision(6)));
const bool = (x) => (x === true || x === 'true' ? true : x === false || x === 'false' ? false : null);
function level(x) { if (x == null || x === '') return { level: 0.95 }; let n = num(x); if (n != null && n > 1 && n < 100) n /= 100; if (n == null || !(n > 0 && n < 1)) return { err: 'level must be between 0 and 1 (or a percent such as 95)' }; return { level: n }; }
const cannot = (reason, extra = {}) => answer(SRC, { outcome: 'CANNOT_TELL', reason, ...extra });
const refused = (reason, extra = {}) => answer(SRC, { outcome: 'REFUSED', reason, ...extra });
const guard = (fn) => async (env, args, req) => { try { return await fn(args && typeof args === 'object' ? args : {}, env, req); } catch (e) { return refused('The input could not be processed.'); } };

// ---------- 1. interval_verdict ----------
function intervalVerdict(a) {
  const est = num(a.estimate), stated = num(a.stated), size = a.size_that_matters == null || a.size_that_matters === '' ? null : num(a.size_that_matters);
  const lv = level(a.level); if (lv.err) return cannot(lv.err);
  if (est == null) return cannot('estimate is missing or not a number');
  if (stated == null) return cannot('stated (the claimed value or threshold) is missing or not a number');
  if (a.size_that_matters != null && a.size_that_matters !== '' && (size == null || size <= 0)) return cannot('size_that_matters must be a positive number');
  const z = zcrit(lv.level); let low = num(a.low), high = num(a.high), se = num(a.se);
  if (low != null && high != null) {
    if (low > high) return cannot('low is greater than high');
    if (est < low - 1e-12 || est > high + 1e-12) return cannot('estimate lies outside the stated interval');
    se = (high - low) / (2 * z);
  } else if (se != null) {
    if (se <= 0) return cannot('se must be positive'); low = est - z * se; high = est + z * se;
  } else return cannot('no interval: give low and high, or se');
  const half = (high - low) / 2, zz = se > 0 ? (est - stated) / se : null;
  const alt = { zero_difference: { tests: 'estimate against the stated value', interval_excludes_stated: stated < low || stated > high, z: zz == null ? null : r6(zz), p_two_sided: zz == null ? null : r6(pTwo(zz)) } };
  if (size != null) {
    const up = stated + size, dn = stated - size;
    alt.size_that_matters = { size, zone: [r6(dn), r6(up)], interval_reaches_upper_edge: high >= up, interval_reaches_lower_edge: low <= dn, interval_inside_zone: low >= dn && high <= up };
  }
  let outcome, note, matters, decide;
  const against_zero = low > stated ? 'ABOVE' : high < stated ? 'BELOW' : 'CONSISTENT';
  if (low > stated) outcome = 'ABOVE'; else if (high < stated) outcome = 'BELOW';
  else if (size == null) { outcome = 'CONSISTENT'; note = `The interval contains the stated value; it is a bound, not equality. The size that would matter was not given, so this is the zero-difference test only.`; }
  else if (low >= stated - size && high <= stated + size) { outcome = 'CONSISTENT'; note = `The interval contains the stated value and lies inside stated +/- ${size} (${r6(stated - size)} to ${r6(stated + size)}): a difference of that size is excluded.`; }
  else {
    outcome = 'CANNOT_TELL'; note = `The interval contains the stated value and also reaches a difference of at least the size that matters (${size}).`;
    const need = size - Math.abs(est - stated);
    decide = { possible_range: { low: r6(low), high: r6(high), difference_from_stated: [r6(low - stated), r6(high - stated)] }, current_half_width: r6(half) };
    if (need > 0) { decide.half_width_needed_to_exclude_size = r6(need); decide.sample_multiplier_approx = r6((half / need) ** 2); decide.reading = 'A projection: if the estimate held where it is, and the interval narrowed with the square root of n. A narrower interval can settle as CONSISTENT (inside the zone) or, if the estimate stays this far from stated, as ABOVE or BELOW.'; }
    else decide.reading = 'The point estimate is already at or beyond stated +/- size, so narrowing alone cannot place the interval inside the zone; it can only settle ABOVE or BELOW. That needs more data on the same quantity, or a different measurement.';
  }
  if (size != null && (outcome === 'ABOVE' || outcome === 'BELOW')) {
    const edge = outcome === 'ABOVE' ? low > stated + size : high < stated - size;
    const inside = outcome === 'ABOVE' ? high <= stated + size : low >= stated - size;
    matters = edge ? `The whole interval is beyond stated +/- ${size}: the difference is at least the size that matters.` : inside ? `The whole interval lies inside stated +/- ${size}: a difference exists and is smaller than the size that matters.` : `The interval excludes the stated value but straddles stated ${outcome === 'ABOVE' ? '+' : '-'} ${size}: whether the difference reaches the size that matters is CANNOT_TELL.`;
    if (inside) { outcome = outcome + '_BUT_SMALLER'; note = `Against the stated value the interval reads ${outcome.replace('_BUT_SMALLER', '')}, and the whole interval lies inside stated +/- ${size}: a difference exists and is smaller than the size that matters.`; }
    if (!edge && !inside) {   // 16 Nov 2026 (the operator, house rule VI): an interval that reaches both live alternatives is CANNOT_TELL on the question that matters, whatever the zero test says
      note = `Against the stated value alone the interval reads ${outcome}; it also reaches inside stated +/- ${size}, so on the question that matters the outcome is CANNOT_TELL.`;
      const need = Math.abs(est - stated) - size;
      decide = { possible_range: { low: r6(low), high: r6(high), difference_from_stated: [r6(low - stated), r6(high - stated)] }, current_half_width: r6(half) };
      if (need > 0) { decide.half_width_needed_to_clear_size = r6(need); decide.sample_multiplier_approx = r6((half / need) ** 2); decide.reading = 'A projection: if the estimate held where it is, and the interval narrowed with the square root of n, it would clear the size that matters.'; }
      else decide.reading = `The point estimate sits inside stated +/- ${size}, so narrowing at this estimate would settle it as CONSISTENT with a difference smaller than the size that matters, not as a difference that matters.`;
      outcome = 'CANNOT_TELL';
    }
  }
  return answer(SRC, { outcome, against_stated_value: against_zero, ...(note ? { note } : {}), ...(matters ? { matters_alternative: matters } : {}), estimate: est, stated, interval: { low: r6(low), high: r6(high), level: lv.level, half_width: r6(half) }, alternatives_tested: alt, ...(decide ? { what_would_decide_it: decide } : {}), method: 'Interval against the stated value, and against stated +/- the size that matters when given (without it: zero-difference test only). A normal interval is assumed when only se is given; when only low and high are given, p and z use a symmetric normal se derived from the width. Rule-based; no model.' });
}

// ---------- 2. margin_check ----------
function marginCheck(a) {
  const value = num(a.value); if (value == null) return cannot('value is missing or not a number');
  const lv = level(a.level); if (lv.err) return cannot(lv.err);
  const kind = String(a.uncertainty_kind || 'sigma').toLowerCase().replace(/[- ]/g, '_');
  if (!['sigma', 'half_width'].includes(kind)) return cannot('uncertainty_kind must be sigma or half_width');
  const pts = []; const at = num(a.breaks_at), lo = num(a.breaks_low), hi = num(a.breaks_high);
  if (at != null) pts.push({ given: 'breaks_at', bp: at, side: at >= value ? 'high' : 'low' });
  if (lo != null) pts.push({ given: 'breaks_low', bp: lo, side: 'low' });
  if (hi != null) pts.push({ given: 'breaks_high', bp: hi, side: 'high' });
  if (!pts.length) return cannot('no break point: give breaks_at, or breaks_low and/or breaks_high');
  let u = num(a.uncertainty); if (u != null && u <= 0) u = null;
  const sigma = u == null ? null : kind === 'sigma' ? u : u / zcrit(lv.level);
  const rows = pts.map((p) => {
    const d = p.side === 'high' ? p.bp - value : value - p.bp; const already = d <= 0;
    const row = { break_point: p.bp, given_as: p.given, direction: p.side === 'high' ? 'above value' : 'below value', margin_absolute: r6(d), margin_relative: value === 0 ? null : r6(d / Math.abs(value)), already_past_at_nominal: already };
    if (sigma != null) { row.margin_sigma = r6(d / sigma); row.probability_past_break = r6(Phi(-d / sigma)); row.margin_vs_stated_uncertainty = r6(d / u); row.label = already ? 'PAST' : d < u ? 'FRAGILE' : d >= 2 * u ? 'ROBUST' : 'THIN'; }
    else row.label = 'CANNOT_TELL';
    return row;
  });
  const order = { PAST: 4, FRAGILE: 3, THIN: 2, ROBUST: 1, CANNOT_TELL: 0 };
  const nearest = rows.reduce((m, r) => (r.margin_absolute < m.margin_absolute ? r : m));
  const outcome = sigma == null ? 'CANNOT_TELL' : rows.reduce((m, r) => (order[r.label] > order[m] ? r.label : m), 'ROBUST');
  const d = { outcome, value, uncertainty: sigma == null ? null : { stated: u, kind, level: kind === 'half_width' ? lv.level : null, one_sigma_used: r6(sigma), ...(a.uncertainty_kind == null || a.uncertainty_kind === '' ? { kind_note: 'kind assumed: sigma' } : {}) }, break_points: rows, nearest_break_point: nearest.break_point,
    method: 'Margin = distance from the stated value to each break point. Probability past the break point assumes the parameter is normally distributed about the stated value with the stated 1-sigma (a half-width is converted at its level); one tail. Labels: PAST when the value is already past the break point (the conclusion fails at the nominal value), FRAGILE when the margin is smaller than the stated uncertainty, ROBUST when at least two stated uncertainties, THIN in between (house addition: not smaller than the uncertainty, not clearly larger). Pairs of parameters moving together are not computed.' };
  if (sigma == null) d.reason = 'uncertainty is not stated (or not positive); margins are given but cannot be compared with it';
  return answer(SRC, d);
}

// ---------- 3. triangulate_readings ----------
function triangulate(a) {
  const rs = arr(a.readings); if (!rs) return cannot('readings must be an array of {label, value, se or low/high}');
  if (rs.length < 2) return cannot('two or more readings are needed');
  if (rs.length > 50) return refused('at most 50 readings');
  const lv = level(a.level); if (lv.err) return cannot(lv.err); const z = zcrit(lv.level);
  const stated = a.stated == null || a.stated === '' ? null : num(a.stated); if (a.stated != null && a.stated !== '' && stated == null) return cannot('stated is not a number');
  const rd = rs.map((x, i) => {
    x = x && typeof x === 'object' ? x : {}; const v = num(x.value), lo = num(x.low), hi = num(x.high); let se = num(x.se), why = null;
    if (v == null) why = 'value missing';
    else if (se != null && se > 0) { /* ok */ } else if (lo != null && hi != null && hi > lo) se = (hi - lo) / (2 * z); else { se = null; why = 'no uncertainty (se or low/high)'; }
    return { label: String(x.label || `reading ${i + 1}`).slice(0, 80), value: v, se, why };
  });
  const usable = rd.filter((x) => x.value != null && x.se != null);
  const readings = rd.map((x) => ({ label: x.label, value: x.value, se: x.se == null ? null : r6(x.se), interval: x.se == null ? null : [r6(x.value - z * x.se), r6(x.value + z * x.se)], ...(x.why ? { excluded_from_combination: x.why } : {}) }));
  const pairs = [];
  for (let i = 0; i < rd.length; i++) for (let j = i + 1; j < rd.length; j++) {
    const A = rd[i], B = rd[j]; const p = { a: A.label, b: B.label };
    if (A.value == null || B.value == null || A.se == null || B.se == null) { pairs.push({ ...p, outcome: 'CANNOT_TELL', reason: 'a reading lacks a value or uncertainty' }); continue; }
    const gap = A.value - B.value, s = Math.hypot(A.se, B.se), zz = gap / s, h = z * s;
    pairs.push({ ...p, gap: r6(gap), gap_interval: [r6(gap - h), r6(gap + h)], z: r6(zz), p_two_sided: r6(pTwo(zz)), outcome: gap - h > 0 ? 'ABOVE' : gap + h < 0 ? 'BELOW' : 'CONSISTENT', meaning: 'outcome describes a relative to b' });
  }
  const base = { readings, pairs, level: lv.level };
  if (usable.length < 2) return answer(SRC, { outcome: 'CANNOT_TELL', reason: 'fewer than two readings carry both a value and an uncertainty', ...base });
  const comb = (set) => { const w = set.map((x) => 1 / (x.se * x.se)), W = w.reduce((s, y) => s + y, 0), m = set.reduce((s, x, i) => s + w[i] * x.value, 0) / W; return { m, se: 1 / Math.sqrt(W), chi2: set.reduce((s, x, i) => s + w[i] * (x.value - m) ** 2, 0), dof: set.length - 1 }; };
  const c = comb(usable), red = c.dof > 0 ? c.chi2 / c.dof : 0, pchi = c.dof > 0 ? pChi2(c.chi2, c.dof) : 1, quoted = pchi >= 0.05, scale = red > 1 ? Math.sqrt(red) : 1, seq = c.se * scale;
  const combined = { value: quoted ? r6(c.m) : null, se: quoted ? r6(seq) : null, se_unscaled: r6(c.se), scale_factor: r6(scale), interval: quoted ? [r6(c.m - z * seq), r6(c.m + z * seq)] : null, chi2: r6(c.chi2), dof: c.dof, chi2_per_dof: r6(red), p_chi2: r6(pchi), quoted, ...(scale > 1 ? { scale_note: `se inflated by sqrt(chi2/dof) = ${r6(scale)} (PDG scale factor)` } : {}) };
  let outlier = null;
  if (usable.length >= 3) {
    let best = null;
    usable.forEach((x, i) => { const rest = usable.filter((_, k) => k !== i), o = comb(rest), zi = (x.value - o.m) / Math.hypot(x.se, o.se), restOk = rest.length < 2 || pChi2(o.chi2, o.dof) >= 0.05;
      if (Math.abs(zi) > z && restOk && (!best || Math.abs(zi) > Math.abs(best.z))) best = { label: x.label, z: r6(zi), direction: zi > 0 ? 'above the others' : 'below the others' }; });
    outlier = best;
  }
  let outcome, note;
  if (!quoted) {
    outcome = 'CANNOT_TELL'; combined.note = 'The readings disagree beyond their stated uncertainties (chi-square p < 0.05), so a combined value is not quoted.';
    note = outlier ? `Readings disagree; ${outlier.label} is the outlier (${outlier.direction}).` : usable.length === 2 ? 'The two readings disagree; with two readings, which one is off cannot be told.' : 'The readings disagree and no single reading accounts for it.';
  } else if (stated != null) {
    const lo = c.m - z * seq, hi = c.m + z * seq; outcome = lo > stated ? 'ABOVE' : hi < stated ? 'BELOW' : 'CONSISTENT';
    note = outcome === 'CONSISTENT' ? `Combined interval ${r6(lo)} to ${r6(hi)} contains the stated value ${stated}; a bound, not equality.` : `Combined interval ${r6(lo)} to ${r6(hi)} is wholly ${outcome.toLowerCase()} the stated value ${stated}.`;
  } else { outcome = 'CONSISTENT'; note = 'The readings agree within their stated uncertainties; no stated value was given to compare with.'; }
  return answer(SRC, { outcome, note, multiplicity_note: 'Pairwise comparisons are not corrected for multiplicity.', combined, ...(outlier ? { outlier } : {}), ...(stated != null ? { stated } : {}), ...base,
    method: 'Pairwise gaps use the quadrature sum of the two uncertainties (normal). Combined value is the inverse-variance weighted mean with se 1/sqrt(sum of weights); chi2 = sum of weighted squared deviations, dof = readings - 1. The combined value is quoted only if the chi-square survival probability at dof is at least 0.05; when chi2/dof > 1 the combined se is multiplied by sqrt(chi2/dof) and the factor is printed. Pairwise comparisons are not corrected for multiplicity. The outlier is the reading furthest from the combination of the others, named only when it exceeds the interval level and the rest agree. Outliers are never named with only two readings. Readings are assumed independent; shared sources are not detected.' });
}

// ---------- 4. controls_check ----------
const NONE_RE = /\b(no[ -]?(detect\w*|signal|effect|hit|fire|firing|difference|change)|not[ -]?(detect\w*|fire\w*|trigger\w*|flag\w*)|none|silent|silence|null|negative|zero|absent|stays? silent|nothing)\b/i;
const HIT_RE = /\b(detect\w*|fires?|fired|firing|positive|hit|flag\w*|trigger\w*|present|found|yes|pass\w*|significant|signal)\b/i;
function classify(v) {
  if (v == null || v === '') return { type: 'unstated' };
  if (typeof v === 'boolean') return { type: v ? 'detect' : 'no_detect' };
  if (typeof v === 'object') { const x = num(v.value), t = num(v.tolerance); return x == null ? { type: 'unstated' } : { type: 'numeric', value: x, tol: t == null || t < 0 ? 0 : t }; }
  const s = String(v).trim(); const n = num(s); if (n != null) return { type: 'numeric', value: n, tol: 0, no_tolerance: true };
  const m = s.match(/^(-?\d*\.?\d+)\s*(?:\+\/-|\+-|±)\s*(\d*\.?\d+)$/); if (m) return { type: 'numeric', value: Number(m[1]), tol: Number(m[2]) };
  if (NONE_RE.test(s)) return { type: 'no_detect' }; if (HIT_RE.test(s)) return { type: 'detect' };
  return { type: 'unstated' };
}
function controlsCheck(a) {
  const cs = arr(a.controls); if (!cs) return cannot('controls must be an array of {name, kind, expected, observed}');
  if (!cs.length) return cannot('no controls given: a test needs at least one positive and one negative control', { table: [] });
  if (cs.length > 100) return refused('at most 100 controls');
  const nullv = num(a.null_value) ?? 0; const issues = []; const rows = [];
  cs.forEach((c0, i) => {
    const c = c0 && typeof c0 === 'object' ? c0 : {}; const name = String(c.name || `control ${i + 1}`).slice(0, 80); const kind = String(c.kind || '').toLowerCase();
    const row = { name, kind: kind === 'positive' || kind === 'negative' ? kind : 'unknown', checks: [], needs_reading: [] }; const bad = [];
    const ex = classify(c.expected), ob = classify(c.observed);
    if (row.kind === 'unknown') bad.push('kind must be positive or negative');
    if (ex.type === 'unstated') row.checks.push('expected outcome is not stated or not readable'); // CANNOT_TELL
    else {
      row.expected_read = ex.type === 'numeric' ? `${ex.value} +/- ${ex.tol}` : ex.type;
      if (row.kind === 'positive') {
        if (ex.type === 'no_detect') bad.push('positive control expects the null outcome (no detection), so it cannot separate the test from the null');
        if (ex.type === 'numeric' && Math.abs(ex.value - nullv) <= ex.tol) bad.push(`expected value ${ex.value} +/- ${ex.tol} includes the null value ${nullv}`);
      } else if (row.kind === 'negative') {
        if (ex.type === 'detect') bad.push('negative control expects a detection');
        if (ex.type === 'numeric' && Math.abs(ex.value - nullv) > ex.tol) bad.push(`expected value ${ex.value} is not the null value ${nullv}`);
      }
    }
    const ind = bool(c.independent), cf = bool(c.can_fire), hd = bool(c.hardest);
    if (ind === false) bad.push('chosen by the value the rule reads, not independently'); else if (ind == null) row.needs_reading.push('independence of choice from the value the rule reads');
    if (cf === false) bad.push('the rule cannot fire on this control under its own minimums'); else if (cf == null) row.needs_reading.push('whether the rule can fire on it (resolution, n, minimums)');
    if (hd === false && row.kind === 'positive') row.needs_reading.push('not marked as the hardest known positive');
    row.hardest = hd === true;
    row.problems = bad; bad.forEach((b) => issues.push(`${name}: ${b}`));
    row.pre_run = bad.length ? 'FIX_CONTROLS' : ex.type === 'unstated' ? 'CANNOT_TELL' : 'STRUCTURE_OK';
    row.attested = ind === true && cf === true;
    if (c.observed != null && c.observed !== '') {
      let st, why;
      if (ex.type === 'unstated' || row.kind === 'unknown') { st = 'CANNOT_TELL'; why = 'expected outcome or kind unreadable'; }
      else if (ex.type === 'numeric') { if (ob.type !== 'numeric') { st = 'CANNOT_TELL'; why = 'observed is not a number'; } else { st = Math.abs(ob.value - ex.value) <= ex.tol ? 'PASSED' : 'FAILED'; why = `observed ${ob.value}, expected ${ex.value} +/- ${ex.tol}`; } }
      else if (ob.type === 'unstated' || ob.type === 'numeric') { st = 'CANNOT_TELL'; why = 'observed outcome unreadable as detect / no detect'; }
      else { const want = row.kind === 'positive' ? 'detect' : 'no_detect'; st = ob.type === want ? 'PASSED' : 'FAILED'; why = `observed ${ob.type}, a ${row.kind} control should give ${want}`; }
      row.observed_read = ob.type === 'numeric' ? ob.value : ob.type; row.run = st; row.run_reason = why;
    } else row.run = 'NOT_RUN';
    rows.push(row);
  });
  const pos = rows.filter((r) => r.kind === 'positive').length, neg = rows.filter((r) => r.kind === 'negative').length;
  if (!pos) issues.push('no positive control: a silent result cannot be told from a test that cannot fire');
  if (!neg) issues.push('no negative control: a hit cannot be told from a test that always fires');
  const anyObs = rows.some((r) => r.run !== 'NOT_RUN'); const failed = rows.filter((r) => r.run === 'FAILED'); const cannotRows = rows.filter((r) => r.pre_run === 'CANNOT_TELL' || r.run === 'CANNOT_TELL' || (anyObs && r.run === 'NOT_RUN'));
  rows.forEach((r) => { if (anyObs && r.run === 'NOT_RUN') { r.run = 'CANNOT_TELL'; r.run_reason = 'unexercised: no observed value for this control'; } });
  const can_fail_inferred = pos > 0 && neg > 0;
  const hardestPos = rows.some((r) => r.kind === 'positive' && r.hardest);
  const attested = rows.every((r) => r.attested) && hardestPos;
  let outcome, reason;
  if (issues.length || failed.length) { outcome = 'FIX_CONTROLS'; reason = 'structure problems or failed controls'; }
  else if (cannotRows.length) { outcome = 'CANNOT_TELL'; reason = 'a control is unreadable or unexercised'; }
  else if (!attested) { outcome = 'CANNOT_TELL'; reason = `${anyObs ? 'All controls passed, but' : `Structure is ${'STRUCTURE_OK'}, but`} the caller has not attested, per control, independent: true and can_fire: true, plus a reachable hardest positive (hardest: true on a positive)`; }
  else { outcome = 'READY'; reason = anyObs ? 'every control passed, as attested' : 'structure OK and the independence, can-fire and hardest-positive attestations are given, as attested'; }
  const structure = issues.length ? 'FIX_CONTROLS' : rows.some((r) => r.pre_run === 'CANNOT_TELL') ? 'CANNOT_TELL' : 'STRUCTURE_OK';
  const desc = a.test_description ? clip(String(a.test_description), 2000) : null;
  const hasHardest = rows.some((r) => r.hardest);
  return answer(SRC, { outcome, reason, structure, attested_as_given: attested, phase: anyObs ? 'after_run' : 'before_run', test_can_fail_inferred: can_fail_inferred, test_can_fail_note: 'An inference only: it is true when a positive and a negative control exist with different expected words; it does not show the rule can fire.', positive_controls: pos, negative_controls: neg, hardest_positive_marked: hasHardest, problems: issues, failed_controls: failed.map((r) => r.name),
    ...(cannotRows.length ? { cannot_tell_controls: cannotRows.map((r) => r.name) } : {}), table: rows, ...(desc ? { test_description: desc } : {}),
    needs_reading: 'Three questions per control (chosen independently of the value the rule reads; the rule can fire on it; the hardest known positive is reachable under the rule limits) are computed only from the flags independent, can_fire and hardest when supplied; otherwise they need a person to read the design. Write this before the run; a control redefined after results is labelled so.',
    method: 'Rule-based. Expected and observed outcomes are read by keyword (detect / no detect) or as a number with a tolerance; STRUCTURE_OK means the structure passes these rules, not that the design is sound; READY is given only on the attestations the caller gives. Before a run: at least one positive and one negative control, each expected outcome differs from the null. After a run: each control PASSED, FAILED or CANNOT_TELL (a control with no observed value is CANNOT_TELL, unexercised); READY only if every control passed and the attestations are given.' });
}

// ---------- 5. two_explanations ----------
const W = { weak: 1, moderate: 2, strong: 3 };
function twoExplanations(a) {
  const A = String(a.a || '').trim().slice(0, 200), B = String(a.b || '').trim().slice(0, 200);
  if (!A || !B) return cannot('both explanations a and b must be named');
  if (A.toLowerCase() === B.toLowerCase()) return cannot('a and b are the same reading; the skill requires two readings that predict different things');
  const ev = arr(a.evidence); if (!ev) return cannot('evidence must be an array of {item, favours, strength, independent}');
  if (ev.length > 200) return refused('at most 200 evidence items');
  const seen = new Map(); const rows = []; const dup = [];
  ev.forEach((e0, i) => {
    const e = e0 && typeof e0 === 'object' ? e0 : {}; const item = String(e.item || `item ${i + 1}`).slice(0, 300); const f = String(e.favours || '').toUpperCase();
    const fav = ['A', 'B', 'BOTH', 'NEITHER'].includes(f) ? f : null; const st = String(e.strength || '').toLowerCase(); const strength = W[st] ? st : null; const ind = bool(e.independent), dsc = bool(e.discriminating);
    const key = item.toLowerCase().replace(/\s+/g, ' ').trim();
    const row = { item, favours: fav || 'INVALID', strength: strength || 'weak (not stated, counted weak)', independent: ind !== false, discriminating: dsc === true, weight: W[strength] || 1 };
    if (!fav) { row.counted = false; row.note = 'favours must be A, B, BOTH or NEITHER'; }
    else if (seen.has(key)) { row.counted = false; row.note = `duplicate of item ${seen.get(key) + 1}`; dup.push(item); }
    else { seen.set(key, i); row.counted = true; }
    rows.push(row);
  });
  const tally = { A: 0, B: 0, BOTH: 0, NEITHER: 0 }; const chain = {};
  rows.filter((r) => r.counted).forEach((r) => { if (r.independent) tally[r.favours] += r.weight; else chain[r.favours] = Math.max(chain[r.favours] || 0, r.weight); });
  Object.entries(chain).forEach(([k, w]) => { tally[k] += w; });
  const dependent = rows.filter((r) => r.counted && !r.independent).map((r) => r.item);
  const counted = rows.filter((r) => r.counted && r.favours !== 'INVALID');
  const marked = counted.filter((r) => r.discriminating && (r.favours === 'A' || r.favours === 'B')); const disc = counted.filter((r) => r.favours === 'A' || r.favours === 'B'); const strongest = (f) => disc.filter((r) => r.favours === f).sort((x, y) => y.weight - x.weight)[0];
  let state, why;
  const m = Math.max(tally.A, tally.B, tally.BOTH, tally.NEITHER);
  if (!counted.length) { state = 'OPEN'; why = 'no usable evidence'; }
  else if (!disc.length) { state = 'OPEN'; why = 'no item discriminates between the two readings (none is marked A or B)'; }
  else if (tally.BOTH > 0 && tally.BOTH >= m) { state = 'BOTH'; why = 'evidence for each part together outweighs evidence for either alone'; }
  else if (tally.NEITHER > 0 && tally.NEITHER > Math.max(tally.A, tally.B, tally.BOTH)) { state = 'NEITHER'; why = 'evidence against both readings outweighs evidence for either'; }
  else if (!marked.length && ((tally.A >= 2 * tally.B && tally.A - tally.B >= 2 && tally.A >= tally.NEITHER) || (tally.B >= 2 * tally.A && tally.B - tally.A >= 2 && tally.B >= tally.NEITHER))) { state = 'OPEN'; why = `no item marked discriminating; a lead needs one (tally A ${tally.A}, B ${tally.B}, BOTH ${tally.BOTH}, NEITHER ${tally.NEITHER})`; }
  else if (tally.A >= 2 * tally.B && tally.A - tally.B >= 2 && tally.A >= tally.NEITHER) { state = 'A'; why = 'A weight is at least twice B and ahead by 2 or more'; }
  else if (tally.B >= 2 * tally.A && tally.B - tally.A >= 2 && tally.B >= tally.NEITHER) { state = 'B'; why = 'B weight is at least twice A and ahead by 2 or more'; }
  else { state = 'OPEN'; why = (marked.length ? 'neither reading leads by the rule (a caller-marked discriminating item, and twice the other and ahead by 2); both stay live' : 'no item marked discriminating; a lead needs one') + ` (tally A ${tally.A}, B ${tally.B}, BOTH ${tally.BOTH}, NEITHER ${tally.NEITHER})`; }
  let test;
  if (!disc.length) test = 'None derivable: no item discriminates. The question cannot currently be split from the items given.';
  else {
    const sa = strongest('A'), sb = strongest('B');
    test = sa && sb ? { kind: 'The strongest item (by stated weight) for each side; nothing more is implied.', a_predicts: sa.item, b_predicts: sb.item, note: 'Items are named as given; this is not a discriminating test and the tool does not infer one.' }
      : { kind: 'Only one side has an item marked A or B; the strongest item for that side is shown, nothing more.', only_side: sa ? 'A' : 'B', item: (sa || sb).item };
  }
  return answer(SRC, { outcome: state, state, reason: why, a: A, b: B, tally, evidence: rows, ...(dup.length ? { duplicates_flagged: dup } : {}), ...(dependent.length ? { non_independent_items_collapsed: dependent } : {}), strongest_item_each_side: test, caller_marked_discriminating: marked.map((r) => r.item),
    method: 'Rule-based, no model. Weights weak 1, moderate 2, strong 3 (unstated counts as weak). Items marked independent: false are one evidence chain: per side only the strongest counts. Duplicate item text counts once. State: BOTH if its tally is the largest and above zero; NEITHER if it exceeds A, B and BOTH; A or B if leading by twice the other and by 2 or more and at least one item is marked discriminating: true; otherwise OPEN. The tool counts what the caller marked; it does not judge the evidence itself.' });
}

// ---------- 6. eval_setup_check ----------
const FIELDS = ['harness', 'prompt_format', 'chat_template', 'few_shot', 'max_tokens', 'temperature', 'stop', 'extraction_rule', 'dataset_version', 'n_items', 'seeds'];
const CARD_PATTERNS = {
  harness: /\b(lm[-_ ]?eval(?:uation)?[-_ ]?harness|lm[-_]eval|lighteval|evalplus|opencompass|simple[-_]evals?|helm|inspect[-_]ai|evalscope|deepeval)\b/i,
  few_shot: /\b(\d+)[- ]?shots?\b|\b(zero|one|two|three|four|five)[- ]shot\b/i,
  temperature: /\btemperature\b\s*(?:of|=|:|is)?\s*(\d*\.?\d+)/i,
  max_tokens: /\bmax[_ -]?(?:new[_ -]?)?(?:tokens|length|gen[_ -]?len)\b\s*(?:of|=|:|is)?\s*(\d+)/i,
  chat_template: /\bchat[_ -]?template\b/i,
  prompt_format: /\bprompt (?:format|template)\b/i,
  extraction_rule: /\b(?:answer extraction|extract(?:ed|ion)?|regex|exact[ -]match)\b/i,
  stop: /\bstop (?:sequences?|tokens?|strings?)\b/i,
  dataset_version: /\b(?:version|v)\s?\d+(?:\.\d+)*\b/i,
  seeds: /\bseeds?\b\s*(?:=|:|of)?\s*\d*/i,
};
const normV = (f, v) => {
  if (v == null || v === '') return null; if (typeof v === 'boolean') return String(v);
  if (Array.isArray(v)) return JSON.stringify(v.map((x) => normV(f, x)).sort());
  if (typeof v === 'object') return JSON.stringify(v);
  const n = num(v); if (n != null) return String(n);
  return String(v).toLowerCase().replace(/[\s_-]+/g, ' ').trim();
};
function ivOf(side) {
  let v = num(side.value); if (v == null) return null; let iv = side.interval; iv = typeof iv === 'string' ? jparse(iv) : iv; let lo = null, hi = null;
  if (Array.isArray(iv) && iv.length === 2) { lo = num(iv[0]); hi = num(iv[1]); } else if (iv && typeof iv === 'object') { lo = num(iv.low ?? iv.lo); hi = num(iv.high ?? iv.hi); }
  return { v, lo: lo != null && hi != null && lo <= hi ? lo : null, hi: lo != null && hi != null && lo <= hi ? hi : null };
}
function readingOutcome(c, o) {
  const z = zcrit(0.95);
  if (c.lo != null && o.lo != null) {
    const sc = (c.hi - c.lo) / (2 * z), so = (o.hi - o.lo) / (2 * z), s = Math.hypot(sc, so), gap = o.v - c.v, h = z * s;
    if (s === 0) return { outcome: gap === 0 ? 'CONSISTENT' : gap > 0 ? 'ABOVE' : 'BELOW', basis: 'both intervals have zero width' };
    return { outcome: gap - h > 0 ? 'ABOVE' : gap + h < 0 ? 'BELOW' : 'CONSISTENT', gap: r6(gap), gap_interval_95: [r6(gap - h), r6(gap + h)], basis: 'difference of the two values with the quadrature sum of the two interval half-widths, read as 95% normal intervals (level not stated by the caller)' };
  }
  if (o.lo != null) return { outcome: c.v < o.lo ? 'ABOVE' : c.v > o.hi ? 'BELOW' : 'CONSISTENT', basis: 'our interval against the claimed point value; the direction is ours relative to the claim (ABOVE means ours is above claimed)', flip: true };
  if (c.lo != null) return { outcome: o.v < c.lo ? 'BELOW' : o.v > c.hi ? 'ABOVE' : 'CONSISTENT', basis: 'our point value against the claimed interval' };
  return { outcome: 'CANNOT_TELL', reason: 'NO_INTERVAL_FORMABLE', basis: 'neither side carries an interval, so the values cannot be compared' };
}
async function evalSetup(a) {
  const claimed = obj(a.claimed), ours = obj(a.ours);
  if (!claimed || !ours) return cannot('claimed and ours must each be an object of setup fields');
  const cd = { ...claimed }; const eff = {}; let read = null; const cardHits = {};
  const repo = a.model == null ? '' : String(a.model).trim();
  if (repo) {
    if (!/^[A-Za-z0-9][\w.-]*\/[\w.-]+$/.test(repo)) read = { ok: false, reason: 'model must be a Hugging Face repo id such as org/name' };
    else {
      const url = `https://huggingface.co/${repo}/raw/main/README.md`; const su = safeUrl(url);
      if (!su.ok) read = { ok: false, reason: su.reason };
      else {
        const r = await fetchText(su.url, { maxBytes: 1_000_000 });
        read = { url: r.url, status: r.status, at: r.at, ok: !!r.ok, ...(r.ok ? {} : { reason: r.error || `answered ${r.status}` }) };
        if (r.ok) {
          const txt = clip(r.text, 400000); read.characters = txt.length;
          for (const f of Object.keys(CARD_PATTERNS)) { const m = txt.match(CARD_PATTERNS[f]); if (m) { const s = Math.max(0, m.index - 60); cardHits[f] = txt.slice(s, m.index + m[0].length + 60).replace(/\s+/g, ' ').trim(); } }
          const wordN = { zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5 };
          const h = txt.match(CARD_PATTERNS.harness); if (h) eff.harness = h[1]; const sh = txt.match(CARD_PATTERNS.few_shot);
          if (sh) eff.few_shot = sh[1] != null ? Number(sh[1]) : wordN[sh[2].toLowerCase()];
          const t = txt.match(CARD_PATTERNS.temperature); if (t) eff.temperature = Number(t[1]); const mt = txt.match(CARD_PATTERNS.max_tokens); if (mt) eff.max_tokens = Number(mt[1]);
        }
      }
    }
  }
  const rows = {};
  for (const f of FIELDS) {
    const cv = normV(f, cd[f]), ov = normV(f, ours[f]); let fromCard = false, cvEff = cv;
    if (cv == null && eff[f] != null) { cvEff = normV(f, eff[f]); fromCard = true; }
    let st; if (cvEff == null) st = ov == null ? 'UNNAMED_BY_BOTH' : 'UNNAMED_BY_CLAIM'; else if (ov == null) st = 'UNNAMED_BY_US'; else st = cvEff === ov ? 'MATCH' : 'DIFFERS';
    rows[f] = { status: st, claimed: cd[f] ?? (fromCard ? eff[f] : null), claimed_source: cv != null ? 'caller' : fromCard ? 'model card (keyword match, read it to confirm)' : null, ours: ours[f] ?? null,
      ...(st === 'UNNAMED_BY_BOTH' ? { note: 'named by neither side; not compared (house label set extended for this case)' } : {}), ...(cardHits[f] && cv == null ? { card_text: cardHits[f] } : {}) };
  }
  const fl = Object.entries(rows); const differs = fl.filter(([, r]) => r.status === 'DIFFERS').map(([k]) => k), unC = fl.filter(([, r]) => r.status === 'UNNAMED_BY_CLAIM').map(([k]) => k), unU = fl.filter(([, r]) => r.status === 'UNNAMED_BY_US').map(([k]) => k);
  const setup_outcome = differs.length ? 'DIFFERS' : unC.length ? 'CANNOT_TELL' : 'MATCHED';
  const c = ivOf(claimed), o = ivOf(ours); let reading = null, outcome, reason;
  if (c && o) reading = readingOutcome(c, o);
  const nonMatch = fl.filter(([, r]) => r.status !== 'MATCH').map(([k, r]) => `${k} ${r.status}`); const carrierIssue = nonMatch.length > 0;
  let direction = null;
  if (reading) direction = reading.outcome === 'CONSISTENT' || reading.outcome === 'CANNOT_TELL' ? null : (reading.flip || reading.outcome ? `ours ${reading.outcome} claimed` : null);
  if (!reading) { outcome = 'CANNOT_TELL'; reason = 'values for both sides were not given (value on claimed and ours), so no reading comparison was made'; }
  else if (reading.outcome === 'CANNOT_TELL') { outcome = 'CANNOT_TELL'; reason = `${reading.reason}: ${reading.basis}`; }
  else if (reading.outcome !== 'CONSISTENT' && carrierIssue) { outcome = 'CANNOT_TELL'; const ubo = fl.filter(([, r]) => r.status === 'UNNAMED_BY_BOTH').length; reason = `The values disagree (${direction}). ${differs.length ? 'Differs: ' + differs.join(', ') + '. ' : ''}Unnamed by both: ${ubo}; unnamed by claim: ${unC.length ? unC.join(', ') : 0}; unnamed by us: ${unU.length ? unU.join(', ') : 0}. The gap is not read as a difference between models.`; }
  else if (reading.outcome === 'CONSISTENT') { outcome = 'CONSISTENT'; reason = 'The values agree within the intervals given (a bound, not equality)' + (carrierIssue ? ' (setup differs or unnamed: ' + nonMatch.join('; ') + '); this is not confirmation.' : '.'); }
  else { outcome = reading.outcome; reason = 'Every setup field is a MATCH; direction is ours relative to claimed.'; }
  const st3 = differs.length ? 'PRESENT' : unC.length ? 'CANNOT_TELL' : 'ABSENT';
  const nt = (needs) => ({ status: 'NOT_EVALUATED', needs });
  const dv = rows.dataset_version.status;
  const checklist = {
    1: nt('raw replies read next to the scorer output (about 10 per task family, two models)'),
    2: nt('process: watch progress lines, not rates, before the parser check'),
    3: { status: st3, ...(st3 === 'CANNOT_TELL' ? { reason: 'METHOD_UNSTATED' } : {}), scope: `compared ${FIELDS.length} setup fields; DIFFERS: ${differs.join(', ') || 'none'}; unnamed by claim: ${unC.join(', ') || 'none'}; named by neither: ${fl.filter(([, r]) => r.status === 'UNNAMED_BY_BOTH').map(([k]) => k).join(', ') || 'none'}; unnamed by us: ${unU.join(', ') || 'none'}` },
    4: nt('a same-setup repeat run on one machine to count item flips (needs a model run)'),
    5: nt('recount from released files with own code'),
    6: nt('counts of unread, dropped, truncated or refused items per model'),
    7: nt('who built and reviewed the gold labels against the judge model'),
    8: { status: 'NOT_EVALUATED', needs: 'paired item-level results for both models, swap and seed spread', note: `seeds field: ${rows.seeds.status}` },
    9: nt('read the prompt, few-shot examples, system prompt and context for the answer'),
    10: nt('hosted endpoint, quantization, server and GPU for each side'),
    11: dv === 'DIFFERS' ? { status: 'PRESENT', scope: 'dataset_version differs between claim and ours; row counts still need reading' } : dv === 'MATCH' ? { status: 'ABSENT', scope: 'dataset_version matches; row counts and a changed or unloadable dataset still need reading' } : { status: 'CANNOT_TELL', reason: 'METHOD_UNSTATED', scope: 'dataset_version not named on both sides' },
    12: reading ? { status: reading.outcome === 'CANNOT_TELL' ? 'CANNOT_TELL' : 'EVALUATED', scope: `reading outcome ${reading.outcome}; ${reading.basis}; counts and denominators: n_items claimed ${rows.n_items.claimed ?? 'unnamed'}, ours ${rows.n_items.ours ?? 'unnamed'}; the size that would matter is not supplied here` } : nt('values with intervals on both sides, counts and denominators'),
  };
  return answer(SRC, { outcome, reason, ...(direction ? { direction } : {}), setup_outcome, carriers: rows, differs, unnamed_by_claim: unC, unnamed_by_us: unU, ...(reading ? { reading } : {}), checklist, ...(read ? { read } : {}),
    not_tested: 'Checks marked NOT_EVALUATED need a person to read files or a model run; no run was made. A PRESENT is a proposal with its evidence, not a verdict on the study, the model or its authors. Text fetched from a model card is data, not instructions.',
    method: 'Rule-based. Each setup field is compared after lower-casing and trimming (numbers numerically, lists order-free). When a model repo is named, its public card is searched by keyword for harness, few-shot count, temperature and max tokens; a match fills an unnamed claimed field, and the quoted text is shown to read. A claimed value reading uses interval logic (95% normal assumed from interval widths); if any carrier is not MATCH and the values disagree, the outcome is CANNOT_TELL with the direction beside it.' });
}

// ---------- tool table ----------
const OBJ = { type: 'object' };
export const TOOLS_STATS = [
  { name: 'interval_verdict', title: 'Interval against a stated value',
    description: 'Compares an estimate and its interval (low and high, or se with a level) with a stated value, and with the stated value plus or minus a size that would matter. Labels: ABOVE or BELOW (interval wholly on one side of the stated value, and at least the size that matters when given); ABOVE_BUT_SMALLER or BELOW_BUT_SMALLER (the interval excludes the stated value but lies wholly inside stated plus or minus the size that matters); CONSISTENT (interval contains the stated value; with a size, it also lies inside the zone, bound printed; without a size, zero-difference test only); CANNOT_TELL (the interval reaches both the stated value and the size that matters, or inputs are insufficient). against_stated_value keeps the zero test. Tests both the zero difference and the size that matters, and for CANNOT_TELL gives the possible range and an approximate sample multiplier needed to decide. Arithmetic under a normal assumption; rule-based.',
    params: { estimate: { type: 'number', description: 'The measured value.' }, low: { type: 'number', description: 'Interval lower bound (use with high).' }, high: { type: 'number', description: 'Interval upper bound.' }, se: { type: 'number', description: 'Standard error (alternative to low and high).' }, level: { type: 'number', description: 'Interval level, default 0.95.' }, stated: { type: 'number', description: 'The claimed value or threshold.' }, size_that_matters: { type: 'number', description: 'Smallest difference from the stated value that would matter (optional).' } },
    required: ['estimate', 'stated'], openWorld: false, run: guard(async (a) => intervalVerdict(a)) },
  { name: 'margin_check', title: 'Margin to the break point',
    description: 'For a parameter with a stated value and uncertainty, computes the margin to each point where a conclusion fails, in absolute, relative and sigma units, and the one-tail probability the parameter lies past it under a normal assumption. Labels: ROBUST = at least 2 stated uncertainties of margin (the tail probability is printed, 2.3% at 2 sigma); THIN = between 1 and 2; FRAGILE = under 1; PAST = the value is already past the break point; CANNOT_TELL = uncertainty not stated. Kind is assumed sigma when unstated, and printed. Single-parameter only; pairs of parameters are not computed.',
    params: { value: { type: 'number', description: 'Stated value of the parameter.' }, uncertainty: { type: 'number', description: 'Stated 1-sigma, or interval half-width if uncertainty_kind is half_width.' }, uncertainty_kind: { type: 'string', description: 'sigma (default) or half_width.', enum: ['sigma', 'half_width'] }, level: { type: 'number', description: 'Level of a half-width, default 0.95.' }, breaks_at: { type: 'number', description: 'Value at which the conclusion fails.' }, breaks_low: { type: 'number', description: 'Lower failure point.' }, breaks_high: { type: 'number', description: 'Upper failure point.' } },
    required: ['value'], openWorld: false, run: guard(async (a) => marginCheck(a)) },
  { name: 'triangulate_readings', title: 'Combine independent readings',
    description: 'Takes two or more readings (value with se or low/high). Returns pairwise gaps with z and ABOVE / BELOW / CONSISTENT per pair, an inverse-variance combined value with chi2 per dof (quoted only if the chi-square p is at least 0.05; se inflated by sqrt(chi2/dof) when above 1, factor printed), an outlier (three or more readings only) when one reading accounts for a disagreement, pairwise comparisons not corrected for multiplicity, and an overall outcome against an optional stated value. Assumes the readings are independent and normal; shared sources are not detected.',
    params: { readings: { type: 'array', items: OBJ, description: 'Objects {label, value, se} or {label, value, low, high}.' }, stated: { type: 'number', description: 'Optional claimed value to compare the combined reading with.' }, level: { type: 'number', description: 'Interval level, default 0.95.' } },
    required: ['readings'], openWorld: false, run: guard(async (a) => triangulate(a)) },
  { name: 'controls_check', title: 'Positive and negative controls',
    description: 'Checks a list of controls before a run (at least one positive and one negative, each expected outcome different from the null, hardest positive and independence flags when supplied) and after a run (each control PASSED, FAILED or CANNOT_TELL against its expected outcome). Returns FIX_CONTROLS, CANNOT_TELL or READY with a table; structure alone is reported as STRUCTURE_OK, and READY needs the caller to attest independent: true and can_fire: true per control and a hardest: true positive. A control with no observed value after a run is CANNOT_TELL (unexercised). Rule-based on keywords and numbers; design questions that need reading are listed, not judged.',
    params: { controls: { type: 'array', items: OBJ, description: 'Objects {name, kind: positive|negative, expected, observed?, independent?, can_fire?, hardest?}. expected is e.g. "detect", "no detect", or "5 +/- 1".' }, test_description: { type: 'string', description: 'Optional plain description of the test.' }, null_value: { type: 'number', description: 'Value under the null for numeric expectations, default 0.' } },
    required: ['controls'], openWorld: false, run: guard(async (a) => controlsCheck(a)) },
  { name: 'two_explanations', title: 'Two explanations ledger',
    description: 'Tallies an evidence ledger for two named explanations. Items are weighted by stated strength, duplicates are flagged and counted once, and items marked not independent count as one chain. Returns A, B, BOTH, NEITHER or OPEN by a stated rule; A or B needs at least one item the caller marks discriminating: true. Lists the strongest item on each side and the caller-marked discriminating items. Counts what the caller marked; it does not judge the evidence.',
    params: { a: { type: 'string', description: 'Explanation A as a plain claim.' }, b: { type: 'string', description: 'Explanation B as a plain claim.' }, evidence: { type: 'array', items: OBJ, description: 'Objects {item, favours: A|B|BOTH|NEITHER, strength?: weak|moderate|strong, independent?: boolean, discriminating?: boolean}.' } },
    required: ['a', 'b', 'evidence'], openWorld: false, run: guard(async (a) => twoExplanations(a)) },
  { name: 'eval_setup_check', title: 'Evaluation setup comparison',
    description: 'A decided ABOVE or BELOW requires all eleven setup fields named and matching on both sides; otherwise a value gap reads CANNOT_TELL. Compares a claimed evaluation setup with ours field by field (harness, prompt format, chat template, few-shot, max tokens, temperature, stop, extraction rule, dataset version, items, seeds): MATCH, DIFFERS, UNNAMED_BY_CLAIM, UNNAMED_BY_US or UNNAMED_BY_BOTH (named by neither side; not compared, but it still keeps the outcome from reading as a clean match). With values and intervals, compares the readings; if setup differs or is unnamed by the claim and the values disagree the outcome is CANNOT_TELL with the direction. Optionally reads a public Hugging Face model card for stated setup words. Lists the twelve eval checks and which of them these inputs can evaluate.',
    params: { claimed: { type: 'object', description: 'Claimed setup fields and optional value and interval.' }, ours: { type: 'object', description: 'Our setup fields and optional value and interval.' }, model: { type: 'string', description: 'Optional Hugging Face repo id (org/name) whose public model card is read for setup words.' } },
    required: ['claimed', 'ours'], openWorld: true, run: guard(async (a) => evalSetup(a)) },
];
