// test_qia.mjs: the QIA tools on the local copy of the public record index (qia_runcheck/public/qia/records), through a mock KV.
// the referee 16 Nov rules: coverage before flags; STALE_AT_STAMP apart from record age; PERSISTENT only past 2.5; distinct stamps.
import fs from 'fs'; import crypto from 'crypto';
import { TOOLS_QIA } from '../tools_qia.js'; import { ENGINE_SHA256 } from '../qia_engine.js';
const R = new URL('../../qia_runcheck/public/qia/records/', import.meta.url).pathname;
const mk = (patch) => ({ IRIS_BENCH: { get: async k => { const p = R + k.replace(/^qia_rc\//, ''); if (!fs.existsSync(p)) return null; let s = fs.readFileSync(p, 'utf8'); if (patch && k.endsWith('index.json')) { const j = JSON.parse(s); patch(j); s = JSON.stringify(j); } return s; } } });
const env = mk(), T = n => TOOLS_QIA.find(t => t.name === n); let pass = 0, fail = 0;
const ok = (c, m, x) => { if (c) pass++; else { fail++; console.log('FAIL', m, x !== undefined ? JSON.stringify(x).slice(0, 300) : ''); } };
const page = fs.readFileSync(new URL('../../cloudflare-workers/heuremen-door/public/qia/runcheck.js', import.meta.url), 'utf8');
ok(crypto.createHash('sha256').update(page).digest('hex') === ENGINE_SHA256, 'qia_engine.js is stale: rerun gen_qia_engine.py');
const fresh = mk(j => j.processors.forEach(p => { p.last_read = new Date(Date.now() - 600e3).toISOString(); }));   // a read 10 minutes ago
const stale = mk(j => j.processors.forEach(p => { p.last_read = new Date(Date.now() - 30 * 3.6e6).toISOString(); }));
let r = await T('qia_calibration_check').run(env, {}); ok(r.data.outcome === 'REFUSED' && r.data.processors.length >= 7, 'no processor lists processors');
r = await T('qia_calibration_check').run(env, { processor: 'ibm_nowhere' }); ok(r.data.outcome === 'REFUSED', 'unknown processor');
r = await T('qia_calibration_check').run(env, { processor: 'ibm_kingston', qubits: 'x,y' }); ok(r.data.outcome === 'REFUSED', 'bad qubits');
// coverage: an old last read is CANNOT_TELL RECORD_OUT_OF_DATE, never FLAGGED, and lists no qubits
r = await T('qia_calibration_check').run(stale, { processor: 'ibm_kingston', qubits: '0-4' });
ok(r.data.outcome === 'CANNOT_TELL' && /RECORD_OUT_OF_DATE/.test(r.data.reason) && r.data.lowest_readout_unflagged.length === 0, 'stale index -> CANNOT_TELL', r.data);
// fresh read: flags are against IBM's own stamp; record age is the headline, not a flag
r = await T('qia_calibration_check').run(fresh, { processor: 'ibm_kingston', qubits: '0-4' });
ok(['CLEAR', 'FLAGGED', 'CANNOT_TELL'].includes(r.data.outcome) && r.data.figures.length === 5, 'kingston now shape', r.data);
ok((r.data.flags.counts.STALE_AT_RUN || 0) > 0 && !('STALE' in r.data.flags.counts), 'now mode: run time is now, STALE_AT_RUN fires (the referee round 2)', r.data.flags.counts);
ok(/IBM's API returned to our account/.test(r.data.headline) && !/IBM has not/.test(r.data.headline), 'headline names what the API returned', r.data.headline);
console.log('kingston now:', r.data.outcome, '|', r.data.reason, '|', JSON.stringify(r.data.flags.counts), '|', r.data.headline);
// run time inside coverage: STALE_AT_RUN appears when the run is > 24 h after measurement
r = await T('qia_calibration_check').run(env, { processor: 'ibm_kingston', at: '2026-11-15T20:00:00Z', qubits: '0-4' });
ok(r.data.record && r.data.record.mode.startsWith('record in force') && (r.data.flags.counts.STALE_AT_RUN || 0) > 0, 'at mode: STALE_AT_RUN', r.data);
r = await T('qia_calibration_check').run(env, { processor: 'ibm_kingston', at: '2099-01-01T00:00:00Z' }); ok(r.data.outcome === 'CANNOT_TELL' && /after the index/.test(r.data.reason), 'run after last read -> CANNOT_TELL');
r = await T('qia_calibration_check').run(env, { processor: 'ibm_fez', at: '2026-11-16T06:30:00Z' }); ok(r.data.outcome === 'CANNOT_TELL' && /no successful read/.test(r.data.reason), 'run in a read gap -> CANNOT_TELL', r.data.reason);
r = await T('qia_calibration_check').run(env, { processor: 'ibm_kingston', at: '2020-01-01' }); ok(r.data.outcome === 'CANNOT_TELL', 'before the window');
// 18 Nov 2026 (the referee): written against a fixture where aachen had not been read since 13 Nov; the live fixture now reads aachen again, so the
// case plants that state instead of depending on the fixture's date.
{ const unread = mk(j => j.processors.forEach(p => { if ((p.backend || p.name) === 'ibm_aachen') p.last_read = '2026-11-13T00:00:00Z'; }));
  r = await T('qia_calibration_check').run(unread, { processor: 'ibm_aachen', qubits: '0' }); ok(r.data.outcome === 'CANNOT_TELL', 'aachen (planted: not read since 13 Nov) -> CANNOT_TELL', r.data.reason); }
r = await T('qia_calibration_check').run(fresh, { processor: 'ibm_pittsburgh', alternatives: 0 });
console.log('pittsburgh all (fresh):', r.data.outcome, JSON.stringify(r.data.flags.counts));
// run check
r = await T('qia_run_check').run(env, { processor: 'ibm_fez', start: '2026-11-12T00:00:00Z', end: '2026-11-12T03:00:00Z', qubits: '0-9' });
console.log('fez run 12 Nov:', r.data.outcome, '|', r.data.reason);
ok(['NO_CHANGE', 'CHANGED_DURING_RUN', 'FLAGGED', 'CANNOT_TELL'].includes(r.data.outcome), 'fez run shape');
// 18 Nov 2026 (the referee): the run is placed one hour after the fixture's own last read of fez, not on a hard-coded date the fixture has since passed.
{ const ix = JSON.parse(fs.readFileSync(R + 'index.json', 'utf8')), lr = Date.parse(ix.processors.find(p => (p.backend || p.name) === 'ibm_fez').last_read);
  r = await T('qia_run_check').run(env, { processor: 'ibm_fez', start: new Date(lr + 3.6e6).toISOString(), end: new Date(lr + 7.2e6).toISOString() }); ok(r.data.outcome === 'CANNOT_TELL' && /after the index/.test(r.data.reason), 'run past last read -> CANNOT_TELL (the referee)', r.data.reason); }
r = await T('qia_run_check').run(env, { processor: 'ibm_fez', start: '2026-11-15T12:00:00Z', end: '2026-11-15T13:00:00Z' }); ok(r.data.outcome === 'CANNOT_TELL' && r.data.read_gaps, 'window across a read gap -> CANNOT_TELL', r.data.reason);
r = await T('qia_run_check').run(env, { processor: 'ibm_fez', start: 'yesterday' }); ok(r.data.outcome === 'REFUSED', 'bad start');
r = await T('qia_run_check').run(env, { processor: 'ibm_fez', start: '2026-11-11', end: '2026-11-10' }); ok(r.data.outcome === 'REFUSED', 'end before start');
// history: q36 sits at the bound (past 2 often, never 2.5) -> CANNOT_TELL NEAR_BOUND, never PERSISTENT
r = await T('qia_qubit_history').run(env, { processor: 'ibm_pittsburgh', qubit: 36 });
console.log('pittsburgh q36:', r.data.outcome, '|', r.data.reason, '|', JSON.stringify(r.data.ratio_summary), JSON.stringify(r.data.remeasurement.stamps_without_new_measurement_of_this_qubit), 'loose', r.data.t2_without_same_pass_t1.length);
ok(r.data.outcome !== 'PERSISTENT' || r.data.ratio_summary.past_2_5 * 2 >= r.data.ratio_summary.pairs, 'PERSISTENT only past 2.5');
const t1s = r.data.same_pass_pairs.map(x => x.t1_measured); ok(new Set(t1s).size === t1s.length, 'each T1 used once');
ok(r.data.remeasurement.stamps_without_new_measurement_of_this_qubit < r.data.window.distinct_stamps, 'counts distinct stamps');
r = await T('qia_qubit_history').run(env, { processor: 'ibm_pittsburgh', qubit: 9999 }); ok(r.data.outcome === 'REFUSED', 'qubit not in record');
r = await T('qia_qubit_history').run(env, { processor: 'ibm_pittsburgh', qubit: 'a' }); ok(r.data.outcome === 'REFUSED', 'bad qubit');
console.log(`qia tests: ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
