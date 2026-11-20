// entry_ages.mjs -- one added sentence for qia_calibration_check: for the qubits asked, the oldest and newest entry dates and ages per field
// (readout, T1, T2), worded as what IBM's API returned. The operator's ball on PR #1 (comment 6969825451), the referee's 18 Nov ruling (b).
// Why: the headline says "the newest record ... is stamped X, 0.6 h before now; every figure in it is at least that old". When IBM restamps
// without new measurements (ibm_marrakesh since 18 Nov 03:51Z: readout entries still 13 Nov 03:47Z, T1 13 Nov 01:17Z) that reads as fresh.
// The existing sentence is kept byte for byte; this adds a sentence beside it and changes nothing else.
// Staged here because the source (indahl.ai: tools_qia.js; qia_engine.js generated from public/qia/runcheck.js) is in a repo this session can't
// open. Python twin for the pip package qia-check: entry_ages.py (same sentence; parity tested). No dependencies. Heuremen LLC.
// the referee's read (18 Nov, comment 6970023834), all five moves: readout subfields printed apart when their dates differ, so a fresh one never vouches
// for a stale one; dates in T-form (2026-11-13T03:47Z); a bare Eastern stamp inside the spring-forward gap is said and left out, never mapped;
// a planted fresh control and a chicago-shaped mixed case in the test; the package difference stated in the tool description.
//   entryAges(record, qubits, now)  -> { qubits_asked, fields: {readout|T1|T2: {entries, oldest, newest, oldest_age_h, newest_age_h, converted,
//                                         ambiguous, gap}; readout also {split, subfields}}, sentence }
//   withEntryAges(data, record, qubits, now) -> a COPY of the check's data with `entry_ages` added; headline untouched
//   headlineText(data)               the check's answer text: its headline, byte for byte, then the added sentence
import { utcStamp } from './qia_measured.mjs';

export const ENTRY_AGES_VERSION = '1.1.0';
export const CHANGELOG_LINE = 'qia_calibration_check: adds one sentence after the headline giving, for the qubits asked, the oldest and newest ' +
  'entry dates and ages per field (readout, T1, T2; readout\'s three entries apart whenever their dates differ) as IBM\'s API returned them; ' +
  'the headline itself is unchanged (the referee 18 Nov, ruling b).';
// Added to qia_calibration_check's tool description, so nobody reads the package as printing it (the referee 18 Nov, move 5).
export const TOOL_DESCRIPTION_ADD = 'The answer adds one sentence after the headline giving, for the qubits asked, the oldest and newest entry dates ' +
  'and ages per field as IBM\'s API returned them. The qia-check package does not print this sentence yet.';
// IBM properties names per field. readout_length is a duration, not a measurement, so it is left out.
export const FIELDS = { readout: ['readout_error', 'prob_meas0_prep1', 'prob_meas1_prep0'], T1: ['T1'], T2: ['T2'] };

const qubitList = rec => { const p = rec && (rec.properties || rec); return (p && p.qubits) || []; };
const hours = (a, b) => (Date.parse(b) - Date.parse(a)) / 3.6e6;
const age = h => h.toFixed(1);

export function parseQubits(spec, n) {
  if (spec == null || String(spec).trim() === '') return null;   // null = all qubits
  const out = new Set();
  for (const part of String(spec).split(',')) {
    const m = part.trim().match(/^(\d+)(?:-(\d+))?$/); if (!m) continue;
    const a = +m[1], b = m[2] === undefined ? a : +m[2]; for (let q = Math.min(a, b); q <= Math.max(a, b); q++) if (q < n) out.add(q);
  }
  return [...out].sort((x, y) => x - y);
}

// stamps for one set of IBM names over the qubits asked: [{q, name, utc, converted, ambiguous, gap}]
function stamps(all, qs, names) {
  const out = [];
  for (const q of qs) for (const e of all[q] || []) if (names.includes(e.name) && e.date) {
    const u = utcStamp(e.date); if (u.utc && !u.unparsed) out.push({ q, name: e.name, ...u });
  }
  return out;
}
// range over stamps; a spring-forward-gap stamp names a time that never existed, so it is counted and left out of the range, never mapped
function stats(ds, now) {
  const real = ds.filter(d => !d.gap), gap = ds.length - real.length;
  if (!real.length) return { entries: 0, gap };
  const sorted = real.map(d => d.utc).sort(), oldest = sorted[0], newest = sorted[sorted.length - 1];
  return { entries: real.length, oldest, newest, oldest_age_h: +age(hours(oldest, now)), newest_age_h: +age(hours(newest, now)),
           converted: real.some(d => d.converted), ambiguous: real.filter(d => d.ambiguous).length, gap };
}
// readout's three entries share a date when, on every qubit asked, every readout entry IBM returned carries the same stamp; only then one range
function readoutShared(ds) {
  const byQ = new Map(); for (const d of ds) { if (!byQ.has(d.q)) byQ.set(d.q, new Set()); byQ.get(d.q).add(d.gap ? 'gap:' + d.utc : d.utc); }
  const names = new Set(ds.map(d => d.name)), perQ = new Map();
  for (const d of ds) { if (!perQ.has(d.q)) perQ.set(d.q, new Set()); perQ.get(d.q).add(d.name); }
  return [...byQ.values()].every(s => s.size === 1) && [...perQ.values()].every(s => s.size === names.size);
}
function span(label, x) {
  const gapNote = x.gap ? `${x.gap} stamp${x.gap === 1 ? ' names' : 's name'} a US Eastern time that never existed, in the spring-forward hour, left out` : '';
  if (!x.entries) return x.gap ? `no ${label} entry with a real time, ${gapNote}` : `no ${label} entry`;
  const s = x.oldest === x.newest ? `${label} entries all dated ${x.oldest} (${age(x.oldest_age_h)} h old)`
    : `${label} entries dated ${x.oldest} to ${x.newest} (${age(x.oldest_age_h)} to ${age(x.newest_age_h)} h old)`;
  return s + (x.ambiguous ? `, ${x.ambiguous} in the fall-back hour, read as the earlier` : '') + (x.gap ? `, ${gapNote}` : '');
}

export function entryAges(record, qubits, now) {
  const all = qubitList(record); const asked = Array.isArray(qubits) ? qubits : parseQubits(qubits, all.length);
  const qs = asked === null ? all.map((_, i) => i) : asked.filter(q => q < all.length);
  const fields = {}, parts = [];
  for (const [f, names] of Object.entries(FIELDS)) {
    const ds = stamps(all, qs, names); fields[f] = stats(ds, now);
    if (f !== 'readout') { parts.push(span(f, fields[f])); continue; }
    const subfields = {}; for (const n of names) subfields[n] = stats(ds.filter(d => d.name === n), now);
    const split = ds.length > 0 && !readoutShared(ds);
    fields[f] = { ...fields[f], split, subfields };
    if (split) for (const n of names) parts.push(span(n, subfields[n])); else parts.push(span(f, fields[f]));
  }
  const conv = Object.values(fields).some(x => x.converted);
  const who = asked === null ? `all ${qs.length} qubits` : qs.length === 1 ? `qubit ${qs[0]}` : `qubits ${qs.join(', ')}`;
  const sentence = qs.length ? `For ${who}, IBM's API returned ${parts.join('; ')}` + (conv ? ' (stamps without a zone read as US Eastern, given in UTC).' : '.')
    : 'No qubit asked is on this processor, so no entry ages are given.';
  return { qubits_asked: asked === null ? 'all' : qs, fields, sentence };
}

export function withEntryAges(data, record, qubits, now) {
  const copy = JSON.parse(JSON.stringify(data)); copy.entry_ages = entryAges(record, qubits, now); return copy;
}
export function headlineText(data) { return data.entry_ages ? `${data.headline} ${data.entry_ages.sentence}` : data.headline; }
