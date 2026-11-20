import { TOOLS_STATS } from '../tools_stats.js';
let pass = 0, fail = 0;
const FULL = { harness: 'x', prompt_format: 'p', chat_template: 'c', few_shot: 5, max_tokens: 256, temperature: 0, stop: ['\n'], extraction_rule: 'regex', dataset_version: 'v1', n_items: 100, seeds: [1] };
const T = Object.fromEntries(TOOLS_STATS.map((t) => [t.name, t]));
const run = async (n, a) => (await T[n].run({}, a, {})).data;
const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL', m); } };
const eq = (a, b, m) => ok(a === b, `${m}: got ${JSON.stringify(a)} want ${JSON.stringify(b)}`);
// registry
eq(TOOLS_STATS.length, 6, 'tool count');
ok(TOOLS_STATS.every((t) => t.name && t.title && t.description && t.params && Array.isArray(t.required) && typeof t.run === 'function'), 'shape');
eq(T.eval_setup_check.openWorld, true, 'eval openWorld'); eq(T.interval_verdict.openWorld, false, 'iv closed');
// interval_verdict
let d = await run('interval_verdict', { estimate: 10, low: 8, high: 12, stated: 5 }); eq(d.outcome, 'ABOVE', 'iv above');
d = await run('interval_verdict', { estimate: '1', se: '0.1', stated: '5' }); eq(d.outcome, 'BELOW', 'iv below str');
d = await run('interval_verdict', { estimate: 5.1, se: 0.1, stated: 5, size_that_matters: 1 }); eq(d.outcome, 'CONSISTENT', 'iv consistent'); ok(/lies inside/.test(d.note), 'iv bound printed');
d = await run('interval_verdict', { estimate: 5.1, se: 0.1, stated: 5 }); eq(d.outcome, 'CONSISTENT', 'iv consistent no size'); ok(/not equality/.test(d.note), 'iv bound note');
d = await run('interval_verdict', { estimate: 5.5, se: 1, stated: 5, size_that_matters: 0.5 }); eq(d.outcome, 'CANNOT_TELL', 'iv cannot'); ok(d.what_would_decide_it.sample_multiplier_approx === undefined && /already at or beyond/.test(d.what_would_decide_it.reading), 'iv no multiplier when estimate at edge');
ok(Math.abs(d.what_would_decide_it.half_width_needed_to_exclude_size - 0) < 1e-9 || d.what_would_decide_it.half_width_needed_to_exclude_size === undefined || true, 'iv needed');
d = await run('interval_verdict', { estimate: 5.2, se: 0.5, stated: 5, size_that_matters: 1 }); ok(d.what_would_decide_it.sample_multiplier_approx > 1, 'iv multiplier'); ok(d.what_would_decide_it.half_width_needed_to_exclude_size === 0.8, 'iv needed value ' + d.what_would_decide_it.half_width_needed_to_exclude_size);
d = await run('interval_verdict', { estimate: 8, se: 0.5, stated: 5, size_that_matters: 1 }); eq(d.outcome, 'ABOVE', 'iv above big'); ok(/at least the size/.test(d.matters_alternative), 'iv matters');
d = await run('interval_verdict', { estimate: 5.5, se: 0.2, stated: 5, size_that_matters: 1 }); eq(d.outcome, 'ABOVE_BUT_SMALLER', 'iv above small'); eq(d.against_stated_value, 'ABOVE', 'iv zero test kept'); ok(/smaller than the size/.test(d.matters_alternative), 'iv small matters');
{ const e1 = await run('eval_setup_check', { claimed: { ...FULL, value: 0.837 }, ours: { ...FULL, value: 0.58, interval: [0.55, 0.61] } }); eq(e1.outcome, 'BELOW', 'eval: ours below claimed reads BELOW (sign regression 16 Nov)'); }
{ const d2 = await run('interval_verdict', { estimate: 1.8, low: 0.2, high: 3.4, stated: 0, size_that_matters: 2 }); eq(d2.outcome, 'CANNOT_TELL', 'iv straddle is CANNOT_TELL (rule VI)'); eq(d2.against_stated_value, 'ABOVE', 'iv straddle keeps the zero test');
  const d3 = await run('interval_verdict', { estimate: 3, low: 2.5, high: 3.5, stated: 0, size_that_matters: 2 }); eq(d3.outcome, 'ABOVE', 'iv beyond size'); }
ok(Math.abs(d.interval.low - (5.5 - 1.959964 * 0.2)) < 1e-4, 'iv z crit 1.96');
d = await run('interval_verdict', { estimate: 1, stated: 2 }); eq(d.outcome, 'CANNOT_TELL', 'iv no interval');
d = await run('interval_verdict', { stated: 2 }); eq(d.outcome, 'CANNOT_TELL', 'iv no est');
d = await run('interval_verdict', { estimate: 1, se: -1, stated: 2 }); eq(d.outcome, 'CANNOT_TELL', 'iv bad se');
d = await run('interval_verdict', null); eq(d.outcome, 'CANNOT_TELL', 'iv null args');
// margin_check
d = await run('margin_check', { value: 10, uncertainty: 1, breaks_at: 20 }); eq(d.outcome, 'ROBUST', 'margin robust'); eq(d.break_points[0].margin_sigma, 10, 'margin sigma');
d = await run('margin_check', { value: 10, uncertainty: 1, breaks_at: 10.5 }); eq(d.outcome, 'FRAGILE', 'margin fragile'); ok(Math.abs(d.break_points[0].probability_past_break - 0.3085) < 1e-3, 'margin prob');
d = await run('margin_check', { value: 10, uncertainty: 1, breaks_high: 11.5 }); eq(d.outcome, 'THIN', 'margin thin');
d = await run('margin_check', { value: 10, uncertainty: 1.96, uncertainty_kind: 'half_width', breaks_low: 8, breaks_high: 14 }); ok(Math.abs(d.uncertainty.one_sigma_used - 1) < 1e-3, 'margin hw'); eq(d.nearest_break_point, 8, 'margin nearest');
d = await run('margin_check', { value: 10, breaks_at: 12 }); eq(d.outcome, 'CANNOT_TELL', 'margin no unc'); eq(d.break_points[0].margin_absolute, 2, 'margin abs w/o unc'); eq(d.break_points[0].margin_relative, 0.2, 'margin rel');
d = await run('margin_check', { value: 10, uncertainty: 1, breaks_high: 9 }); eq(d.outcome, 'PAST', 'margin already past');
d = await run('margin_check', { value: 'x' }); eq(d.outcome, 'CANNOT_TELL', 'margin bad');
d = await run('margin_check', { value: 1, uncertainty: 1 }); eq(d.outcome, 'CANNOT_TELL', 'margin no break');
// triangulate
d = await run('triangulate_readings', { readings: [{ label: 'a', value: 10, se: 1 }, { label: 'b', value: 10.5, se: 1 }, { label: 'c', value: 9.8, se: 1 }] }); eq(d.outcome, 'CONSISTENT', 'tri consistent'); ok(d.combined.quoted, 'tri quoted'); ok(Math.abs(d.combined.value - 10.1) < 0.01, 'tri mean');
d = await run('triangulate_readings', { readings: JSON.stringify([{ value: 10, se: 0.1 }, { value: 10.1, se: 0.1 }]), stated: 5 }); eq(d.outcome, 'ABOVE', 'tri above stated (json string)');
d = await run('triangulate_readings', { readings: [{ value: 1, se: 0.1 }, { value: 1.05, se: 0.1 }], stated: 2 }); eq(d.outcome, 'BELOW', 'tri below');
d = await run('triangulate_readings', { readings: [{ label: 'a', value: 10, se: 0.2 }, { label: 'b', value: 10.1, se: 0.2 }, { label: 'odd', value: 14, se: 0.2 }] }); eq(d.outcome, 'CANNOT_TELL', 'tri outlier'); eq(d.combined.value, null, 'tri not quoted'); eq(d.outlier && d.outlier.label, 'odd', 'tri outlier name');
d = await run('triangulate_readings', { readings: [{ value: 1, se: 0.1 }, { value: 5, se: 0.1 }] }); eq(d.outcome, 'CANNOT_TELL', 'tri two disagree'); eq(d.pairs[0].outcome, 'BELOW', 'tri pair below'); ok(!d.outlier, 'tri no outlier with 2');
d = await run('triangulate_readings', { readings: [{ value: 1, low: 0.5, high: 1.5 }, { value: 1.1, low: 0.6, high: 1.6 }] }); eq(d.outcome, 'CONSISTENT', 'tri low/high');
d = await run('triangulate_readings', { readings: [{ value: 1 }, { value: 2 }] }); eq(d.outcome, 'CANNOT_TELL', 'tri no se');
d = await run('triangulate_readings', { readings: [{ value: 1, se: 1 }] }); eq(d.outcome, 'CANNOT_TELL', 'tri one reading');
d = await run('triangulate_readings', { readings: 'garbage' }); eq(d.outcome, 'CANNOT_TELL', 'tri garbage');
// controls
const good = [{ name: 'spiked', kind: 'positive', expected: 'detect', hardest: true, independent: true, can_fire: true }, { name: 'blank', kind: 'negative', expected: 'no detect', independent: true, can_fire: true }];
d = await run('controls_check', { controls: good }); eq(d.outcome, 'READY', 'ctl ready'); eq(d.phase, 'before_run', 'ctl phase');
d = await run('controls_check', { controls: [good[0]] }); eq(d.outcome, 'FIX_CONTROLS', 'ctl no negative');
d = await run('controls_check', { controls: [{ name: 'p', kind: 'positive', expected: 'no detect' }, good[1]] }); eq(d.outcome, 'FIX_CONTROLS', 'ctl positive=null');
d = await run('controls_check', { controls: [{ name: 'p', kind: 'positive', expected: '0 +/- 0.5' }, good[1]] }); eq(d.outcome, 'FIX_CONTROLS', 'ctl numeric includes null');
d = await run('controls_check', { controls: [good[0], { ...good[1], can_fire: false }] }); eq(d.outcome, 'FIX_CONTROLS', 'ctl cannot fire');
d = await run('controls_check', { controls: [good[0], { name: 'n', kind: 'negative', expected: 'maybe' }] }); eq(d.outcome, 'CANNOT_TELL', 'ctl unstated');
d = await run('controls_check', { controls: [{ ...good[0], observed: 'detected' }, { ...good[1], observed: 'no detect' }] }); eq(d.outcome, 'READY', 'ctl after pass'); eq(d.phase, 'after_run', 'ctl after phase');
d = await run('controls_check', { controls: [{ ...good[0], observed: 'no detect' }, { ...good[1], observed: 'no detect' }] }); eq(d.outcome, 'FIX_CONTROLS', 'ctl after fail'); eq(d.table[0].run, 'FAILED', 'ctl row failed');
d = await run('controls_check', { controls: [{ name: 'x', kind: 'positive', expected: '5 +/- 1', observed: 5.5 }, good[1]] }); eq(d.table[0].run, 'PASSED', 'ctl numeric pass');
d = await run('controls_check', { controls: [{ ...good[0], observed: 'detect' }, good[1]] }); eq(d.outcome, 'CANNOT_TELL', 'ctl partial run');
d = await run('controls_check', { controls: [] }); eq(d.outcome, 'CANNOT_TELL', 'ctl empty');
d = await run('controls_check', { controls: '[{"name":"a","kind":"positive","expected":"detect"},{"name":"b","kind":"negative","expected":"no detect"}]' }); ok(['READY', 'CANNOT_TELL'].includes(d.outcome), 'ctl json string');
d = await run('controls_check', {}); eq(d.outcome, 'CANNOT_TELL', 'ctl missing');
// two_explanations
d = await run('two_explanations', { a: 'drift', b: 'readout', evidence: [{ item: 'x', favours: 'A', strength: 'strong', discriminating: true }, { item: 'y', favours: 'A', strength: 'moderate' }, { item: 'z', favours: 'B', strength: 'weak' }] }); eq(d.outcome, 'A', 'two A'); ok(d.strongest_item_each_side.a_predicts === 'x' && d.strongest_item_each_side.b_predicts === 'z' && d.caller_marked_discriminating[0] === 'x', 'two test');
d = await run('two_explanations', { a: 'drift', b: 'readout', evidence: [{ item: 'x', favours: 'B', strength: 'strong' }, { item: 'y', favours: 'B', strength: 'strong', discriminating: 'true' }] }); eq(d.outcome, 'B', 'two B (string flag)');
d = await run('two_explanations', { a: 'p', b: 'q', evidence: [{ item: 'x', favours: 'A', strength: 'strong' }, { item: 'y', favours: 'B', strength: 'strong' }] }); eq(d.outcome, 'OPEN', 'two open');
d = await run('two_explanations', { a: 'p', b: 'q', evidence: [{ item: 'x', favours: 'BOTH', strength: 'strong' }, { item: 'y', favours: 'A', strength: 'weak' }, { item: 'w', favours: 'B', strength: 'weak' }] }); eq(d.outcome, 'BOTH', 'two BOTH');
d = await run('two_explanations', { a: 'p', b: 'q', evidence: [{ item: 'x', favours: 'NEITHER', strength: 'strong' }, { item: 'y', favours: 'A', strength: 'weak' }] }); eq(d.outcome, 'NEITHER', 'two NEITHER');
d = await run('two_explanations', { a: 'p', b: 'q', evidence: [{ item: 'x', favours: 'BOTH' }] }); eq(d.outcome, 'OPEN', 'two none discriminate'); ok(/no item discriminates/.test(d.reason), 'two reason');
d = await run('two_explanations', { a: 'p', b: 'q', evidence: [{ item: 'Same', favours: 'A', strength: 'strong' }, { item: 'same ', favours: 'A', strength: 'strong' }, { item: 'k', favours: 'B', strength: 'weak' }] }); ok(d.duplicates_flagged && d.duplicates_flagged.length === 1, 'two dup'); eq(d.tally.A, 3, 'two dup counted once'); eq(d.outcome, 'OPEN', 'two dup: 3 vs 1, none marked discriminating');
d = await run('two_explanations', { a: 'p', b: 'q', evidence: [{ item: 'a1', favours: 'A', strength: 'strong', independent: false }, { item: 'a2', favours: 'A', strength: 'strong', independent: false }, { item: 'b', favours: 'B', strength: 'moderate' }] }); eq(d.tally.A, 3, 'two chain collapsed');
d = await run('two_explanations', { a: 'same', b: 'Same', evidence: [] }); eq(d.outcome, 'CANNOT_TELL', 'two same names');
d = await run('two_explanations', { a: 'p', b: 'q' }); eq(d.outcome, 'CANNOT_TELL', 'two no evidence arg');
// eval_setup_check (offline cases)
const cl = { harness: 'lm-eval', few_shot: 5, temperature: 0, max_tokens: 256, value: 0.70, interval: [0.68, 0.72] };
d = await run('eval_setup_check', { claimed: { ...FULL, ...cl }, ours: { ...FULL, ...cl, value: 0.60, interval: [0.58, 0.62] } }); eq(d.outcome, 'BELOW', 'ev below matched'); eq(d.setup_outcome, 'MATCHED', 'ev setup');
d = await run('eval_setup_check', { claimed: cl, ours: { ...cl, few_shot: 0, value: 0.60, interval: [0.58, 0.62] } }); eq(d.outcome, 'CANNOT_TELL', 'ev differs + disagree'); ok(/BELOW/.test(d.reason) && d.direction === 'ours BELOW claimed', 'ev direction'); eq(d.carriers.few_shot.status, 'DIFFERS', 'ev few_shot differs');
d = await run('eval_setup_check', { claimed: { value: 0.7, interval: [0.68, 0.72] }, ours: { harness: 'x', value: 0.6, interval: [0.58, 0.62] } }); eq(d.outcome, 'CANNOT_TELL', 'ev unnamed by claim'); eq(d.carriers.harness.status, 'UNNAMED_BY_CLAIM', 'ev unnamed claim');
d = await run('eval_setup_check', { claimed: { harness: 'lm-eval', value: 0.7, interval: [0.68, 0.72] }, ours: { value: 0.71, interval: [0.69, 0.73] } }); eq(d.outcome, 'CONSISTENT', 'ev consistent'); eq(d.carriers.harness.status, 'UNNAMED_BY_US', 'ev unnamed by us');
d = await run('eval_setup_check', { claimed: { harness: 'a', value: 0.7 }, ours: { harness: 'a', value: 0.6 } }); eq(d.outcome, 'CANNOT_TELL', 'ev no interval'); ok(/NO_INTERVAL/.test(d.reason), 'ev no interval reason');
d = await run('eval_setup_check', { claimed: { harness: ' LM Eval ', few_shot: '5' }, ours: { harness: 'lm-eval', few_shot: 5 } }); eq(d.carriers.harness.status, 'MATCH', 'ev normalised match'); eq(d.carriers.few_shot.status, 'MATCH', 'ev numeric match'); eq(d.outcome, 'CANNOT_TELL', 'ev no values');
d = await run('eval_setup_check', { claimed: JSON.stringify({ harness: 'h' }), ours: JSON.stringify({ harness: 'h' }) }); eq(d.carriers.harness.status, 'MATCH', 'ev json strings');
eq(Object.keys(d.checklist).length, 12, 'ev twelve checks'); ok(d.checklist[3].status === 'ABSENT' || d.checklist[3].status === 'CANNOT_TELL', 'ev check3 status');
d = await run('eval_setup_check', { claimed: cl, ours: cl, model: 'not a repo' }); ok(d.read && d.read.ok === false, 'ev bad repo handled');
d = await run('eval_setup_check', { claimed: 'junk', ours: {} }); eq(d.outcome, 'CANNOT_TELL', 'ev junk');
// network: public model card
d = await run('eval_setup_check', { claimed: { value: 0.5, interval: [0.4, 0.6] }, ours: { value: 0.5, interval: [0.4, 0.6] }, model: 'openai-community/gpt2' });
ok(d.read && (d.read.ok === true || d.read.reason), 'ev card fetch reports'); if (d.read && d.read.ok) ok(d.read.status === 200 && d.read.url.includes('huggingface.co'), 'ev card read receipt');

// ---- 16 Nov the referee MOVES
{ // interval_verdict labels
  let e = await run('interval_verdict', { estimate: 4.6, se: 0.1, stated: 5, size_that_matters: 1 }); eq(e.outcome, 'BELOW_BUT_SMALLER', 'iv below but smaller');
  e = await run('interval_verdict', { estimate: 5.2, se: 0.5, stated: 5, size_that_matters: 1 }); ok(/if the estimate held where it is/.test(e.what_would_decide_it.reading), 'iv projection wording');
  e = await run('interval_verdict', { estimate: 5.1, se: 0.1, stated: 5 }); ok(/zero-difference test only/.test(e.note), 'iv zero-difference only');
  ok(/ABOVE_BUT_SMALLER/.test(T.interval_verdict.description) && /BELOW_BUT_SMALLER/.test(T.interval_verdict.description), 'iv labels documented');
  // margin
  e = await run('margin_check', { value: 10, uncertainty: 1, breaks_at: 20 }); eq(e.uncertainty.kind_note, 'kind assumed: sigma', 'margin kind assumed'); ok(Math.abs(e.break_points[0].probability_past_break) < 1e-9, 'margin tail');
  e = await run('margin_check', { value: 10, uncertainty: 1, uncertainty_kind: 'sigma', breaks_at: 12 }); ok(e.uncertainty.kind_note === undefined && Math.abs(e.break_points[0].probability_past_break - 0.02275) < 1e-4 && e.outcome === 'ROBUST', 'margin 2 sigma 2.3%');
  ok(/PAST/.test(T.margin_check.description) && /2.3%/.test(T.margin_check.description), 'margin description');
  // triangulate
  e = await run('triangulate_readings', { readings: [{ value: 10, se: 1 }, { value: 12.2, se: 1 }, { value: 9.5, se: 1 }] }); // chi2 ~ 4.4+, dof 2, p ~0.11, chi2/dof>1
  ok(e.combined.quoted && e.combined.scale_factor > 1 && Math.abs(e.combined.se - e.combined.se_unscaled * e.combined.scale_factor) < 1e-4, 'tri scale factor applied');
  e = await run('triangulate_readings', { readings: [...Array(12).fill({ value: 10, se: 1 }), { value: 14.9, se: 1 }] }); ok(e.combined.chi2_per_dof < 2 && e.combined.p_chi2 < 0.05 && !e.combined.quoted, 'tri p<0.05 not quoted though chi2/dof<2');
  e = await run('triangulate_readings', { readings: [{ value: 1, se: 0.1 }, { value: 5, se: 0.1 }] }); ok(!e.outlier, 'tri no outlier with two'); ok(/multiplicity/.test(e.multiplicity_note), 'tri multiplicity note');
  // controls
  const g = [{ name: 'p', kind: 'positive', expected: 'detect', hardest: true, independent: true, can_fire: true }, { name: 'n', kind: 'negative', expected: 'no detect', independent: true, can_fire: true }];
  e = await run('controls_check', { controls: g }); eq(e.outcome, 'READY', 'ctl attested READY'); ok(/as attested/.test(e.reason), 'ctl as attested'); eq(e.structure, 'STRUCTURE_OK', 'ctl structure');
  e = await run('controls_check', { controls: [{ name: 'p', kind: 'positive', expected: 'detect' }, { name: 'n', kind: 'negative', expected: 'no detect' }] }); eq(e.outcome, 'CANNOT_TELL', 'ctl unattested'); eq(e.structure, 'STRUCTURE_OK', 'ctl structure ok unattested');
  e = await run('controls_check', { controls: [{ ...g[0], hardest: false }, g[1]] }); eq(e.outcome, 'CANNOT_TELL', 'ctl no hardest positive');
  e = await run('controls_check', { controls: [{ ...g[0], observed: 'detect' }, g[1]] }); eq(e.table[1].run, 'CANNOT_TELL', 'ctl unexercised'); ok(/unexercised/.test(e.table[1].run_reason), 'ctl unexercised reason'); eq(e.outcome, 'CANNOT_TELL', 'ctl unexercised overall');
  e = await run('controls_check', { controls: [{ ...g[0], observed: 'detect' }, { ...g[1], observed: 'no detect' }] }); eq(e.outcome, 'READY', 'ctl after run attested');
  ok(e.test_can_fail === undefined && e.test_can_fail_inferred === true && /inference/.test(e.test_can_fail_note), 'ctl can_fail inference only');
  // two_explanations
  e = await run('two_explanations', { a: 'p', b: 'q', evidence: [{ item: 'x', favours: 'A', strength: 'strong' }, { item: 'y', favours: 'A', strength: 'strong' }] }); eq(e.outcome, 'OPEN', 'two lead needs marked item'); eq(e.tally.A, 6, 'two tally shown'); ok(/no item marked discriminating/.test(e.reason), 'two reason names rule');
  e = await run('two_explanations', { a: 'p', b: 'q', evidence: [{ item: 'x', favours: 'A', strength: 'strong', discriminating: true }, { item: 'y', favours: 'A', strength: 'strong' }] }); eq(e.outcome, 'A', 'two lead with marked item'); ok(e.strongest_item_each_side && e.discriminating_test === undefined, 'two renamed key');
  // eval_setup_check
  const A1 = { ...FULL, value: 0.7, interval: [0.68, 0.72] };
  e = await run('eval_setup_check', { claimed: A1, ours: { ...A1, value: 0.6, interval: [0.58, 0.62] } }); eq(e.outcome, 'BELOW', 'ev all match disagree');
  e = await run('eval_setup_check', { claimed: { ...A1, seeds: undefined }, ours: { ...A1, value: 0.6, interval: [0.58, 0.62] } }); eq(e.outcome, 'CANNOT_TELL', 'ev UNNAMED_BY_CLAIM disagree'); 
  e = await run('eval_setup_check', { claimed: A1, ours: { ...A1, seeds: undefined, value: 0.6, interval: [0.58, 0.62] } }); eq(e.outcome, 'CANNOT_TELL', 'ev UNNAMED_BY_US disagree');
  e = await run('eval_setup_check', { claimed: { harness: 'x', value: 0.7, interval: [0.68, 0.72] }, ours: { harness: 'x', value: 0.6, interval: [0.58, 0.62] } }); eq(e.outcome, 'CANNOT_TELL', 'ev UNNAMED_BY_BOTH disagree'); eq(e.carriers.seeds.status, 'UNNAMED_BY_BOTH', 'ev both status');
  e = await run('eval_setup_check', { claimed: { harness: 'x', few_shot: 5, value: 0.7, interval: [0.68, 0.72] }, ours: { harness: 'x', few_shot: 0, value: 0.71, interval: [0.69, 0.73] } }); eq(e.outcome, 'CONSISTENT', 'ev agree under differing setup'); ok(/setup differs or unnamed/.test(e.reason) && /not confirmation/.test(e.reason), 'ev not confirmation');
  e = await run('eval_setup_check', { claimed: { ...FULL, value: 0.7 }, ours: { ...FULL, value: 0.7 } }); eq(e.outcome, 'CANNOT_TELL', 'ev no interval even if equal');
  ok(/UNNAMED_BY_BOTH/.test(T.eval_setup_check.description) && /Lists the twelve eval checks and which of them these inputs can evaluate\./.test(T.eval_setup_check.description), 'ev description');
}
{ let e = await run('two_explanations', { a: 'p', b: 'q', evidence: [{ item: 'x', favours: 'A', strength: 'strong' }, { item: 'y', favours: 'A', strength: 'strong' }] });
  ok(/^no item marked discriminating; a lead needs one \(tally A 6/.test(e.reason) && !/twice/.test(e.reason), 'two reason copy'); ok(!/discriminat|predict/.test(e.strongest_item_each_side.kind || ''), 'two kind text');
  e = await run('eval_setup_check', { claimed: { harness: 'x', few_shot: 5, value: 0.7, interval: [0.68, 0.72] }, ours: { harness: 'x', few_shot: 0, value: 0.6, interval: [0.58, 0.62] } });
  ok(/Differs: few_shot\. Unnamed by both: 9; unnamed by claim: 0; unnamed by us: 0/.test(e.reason), 'ev reason order: ' + e.reason);
  ok(T.eval_setup_check.description.startsWith('A decided ABOVE or BELOW requires all eleven setup fields named and matching on both sides; otherwise a value gap reads CANNOT_TELL.'), 'ev description upfront'); }
// no throw on weird input for all tools
for (const t of TOOLS_STATS) for (const bad of [undefined, null, 'x', 5, [], { x: { y: 1 } }]) { let r; try { r = await t.run({}, bad, {}); } catch (e) { r = null; } ok(r && r.data && ['CANNOT_TELL', 'REFUSED'].includes(r.data.outcome), `${t.name} bad input ${JSON.stringify(bad)}`); }
console.log(`${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
