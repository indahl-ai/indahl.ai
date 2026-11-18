// Regression tests for check_reported_statistics and the arXiv HTML reader (the referee, 15 Nov 2026). Run: node tests/stats_regression.mjs
const r = await import('../research.js');
let bad = 0; const ok = (name, cond) => { console.log((cond ? 'PASS ' : 'FAIL ') + name); if (!cond) bad++; };
const one = (t) => r.checkReportedStatistics(t).rows[0] || {};
const html = (s) => r.htmlToText('<p>' + s + '</p>');
ok('&lt; inside math alttext survives the tag stripper', /p<\.001/.test(html('t(18)=7.20 , <math alttext="p&lt;.001"><mi>p</mi></math> )')));
ok('&gt; inside math alttext survives', /p>\.05/.test(html('<math alttext="p&gt;.05"><mi>p</mi></math>')));
ok('p<.001 without spaces is read', one('t(18) = 7.20, p<.001').outcome === 'CONSISTENT');
ok('p < .001 with spaces is read', one('t(18) = 7.20, p < .001').outcome === 'CONSISTENT');
ok('unicode minus in a statistic', one('t(12) = −2.10, p = .057').outcome === 'CONSISTENT');
ok('≤ is read as an upper bound', ['CONSISTENT'].includes(one('t(18) = 7.20, p ≤ .001').outcome));
ok('fractional df rounding allowed: t(2.4) = 2.84, p = .086', one('t(2.4) = 2.84, p = .086').outcome === 'CONSISTENT');
ok('integer df exact and labelled: t(14) = 2.40, p = .030', one('t(14) = 2.40, p = .030').outcome === 'BELOW' && one('t(14) = 2.40, p = .030').df_policy === 'integer degrees of freedom read as exact');
ok('slash with small denominator set aside: 1/5 (33.9%)', one('levels 1/5 (33.9%)').reason === 'SLASH_MAY_BE_A_SCALE');
ok('slash with large denominator is a count: 12/40 (45%)', one('12/40 (45%)').outcome === 'ABOVE');
ok('"of" form keeps its verdict: 1 of 5 (33.9%)', one('1 of 5 (33.9%)').outcome === 'ABOVE');
ok('set-aside count reported', r.checkReportedStatistics('1/5 (33.9%) and 2/5 (18.6%)').set_aside_as_possible_scales === 2);
ok('participant count, small denominator, mismatch: 3 of 8 participants (40%)', one('3 of 8 participants (40%)').outcome === 'ABOVE');   // the referee 15 Nov: 37.5% recomputed
ok('participant count, small denominator, exact: 3 of 8 participants (37.5%)', one('3 of 8 participants (37.5%)').outcome === 'CONSISTENT');
ok('participant count, rounding allowed: 3 out of 8 patients (38%)', one('3 out of 8 patients (38%)').outcome === 'CONSISTENT');
console.log(bad ? bad + ' FAILED' : 'all pass'); process.exit(bad ? 1 : 0);
