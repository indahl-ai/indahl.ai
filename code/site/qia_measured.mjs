// qia_measured.mjs -- the latest hourly measurement beside IBM's stated figure, per qubit (the operator's ball on PR #1, comment 6968487487).
// Wiring only: qia_cal/cal.py already measures every qubit's P(1|0), P(0|1) and T1 each hour and publishes indahl.ai/qia/cal.json and
// /qia/cal/<job>.json. This module joins one such run to the figures qia_calibration_check already returns, so one answer carries the stated
// value, the measured value with its interval, the job id, the window, the outcome, the job file URL, the record's age, and the drift caveat.
// No dependencies; plain ES module, so it drops into the MCP server and the Test Drive page alike.
//   qiaMeasured(checkData, calRun, opts) the payload of the separate read-only tool qia_measured(processor, qubits) (TOOL below); works on a
//                                       copy, so qia_calibration_check's own output stays exactly as published (the referee's ship read, 18 Nov 04:06Z)
//   attach(checkData, calRun, opts)     the join qiaMeasured uses; it writes into the object it is given, so call it only on a copy
//   normalizeCal(raw, processor)        the adapter: ONE place that knows cal.json's field names (FIELD below, to confirm against a real file)
// Outcomes are cal.py's own words (qia_cal/callib.py: ABOVE = IBM's stated figure above our interval, BELOW = below it), never recomputed here;
// each is translated into one fixed plain sentence per quantity (DIRECTION). Fields the run or the record lack are said out loud.
// Heuremen LLC.

export const VERSION = '0.2.0';
export const CAL_BASE = 'https://indahl.ai/qia/cal/';
// Age limit on OUR latest run, from its window end to the answer. Hourly runs: 3 h allows one missed run plus slack (the designer's pick; the referee/the operator
// may set it). Past it the answer reads "no recent run" with the last run's time and presents no measured value as current.
export const RECENT_RUN_H = 3;
export const HISTORY_N = 24;   // last-N hourly runs summarised per qubit (median, range, cal.py's own outcome counts); no threshold of ours

export const CAVEAT =
  'A record days old disagrees with today\'s hardware by drift too: IBM\'s own entries move against their own later refresh ' +
  '(the IBM-vs-IBM floor). A measured-vs-stated gap names a gap, not a cause. The T1 column most of all: read it beside the record\'s age ' +
  'and the floor. A readout figure held by an unchanged record while the measurement sits far from it is the case the floor does not explain. ' +
  'One run is one look; some qubits are intermittent.';

// cal.py's word -> one fixed sentence per quantity. A word not in this table is printed as given and marked untranslated, never guessed.
export const DIRECTION = {
  readout: { ABOVE: "IBM's stated error is higher than measured", BELOW: "IBM's stated error is lower than measured",
             CONSISTENT: "IBM's stated error is inside the measured interval", CANNOT_TELL: "the measurement cannot place IBM's stated error" },
  t1:      { ABOVE: "IBM's stated T1 is longer than measured", BELOW: "IBM's stated T1 is shorter than measured",
             CONSISTENT: "IBM's stated T1 is inside the measured interval", CANNOT_TELL: "the measurement cannot place IBM's stated T1" },
};
export function direction(p, word) {
  if (word === undefined || word === null || word === '') return 'no outcome word in the run';
  const s = DIRECTION[p === 't1' ? 't1' : 'readout'][word];
  return s || `outcome word "${word}" as given by cal.py (not translated)`;
}
export const NO_FLOOR = 'no floor supplied';
export const T1_METHOD = "T1 method: ours is cal.py's fit to this run (see the job file); IBM's is its own single-exponential fit, method otherwise unstated by IBM";

// ---- the adapter: cal.json field names, assumed until checked against one /qia/cal/<job>.json -------------------------------------------
// Edit FIELD only; everything below reads the normalized shape.
export const FIELD = {
  job: ['job_id', 'job'],
  processor: ['backend', 'processor', 'chip'],
  start: ['window_start', 'started_utc', 'start'],
  end: ['window_end', 'finished_utc', 'end'],
  qubits: ['qubits', 'per_qubit', 'results'],
  qubit: ['qubit', 'q'],
  params: { p10: ['p10', 'prob_meas1_prep0'], p01: ['p01', 'prob_meas0_prep1'], t1: ['t1', 'T1', 't1_us'] },
  value: ['value', 'measured', 'est'],
  lo: ['lo', 'ci_lo', 'low'],
  hi: ['hi', 'ci_hi', 'high'],
  k: ['k'], n: ['n', 'shots'],
  conf: ['conf', 'level'],
  outcome: ['outcome', 'call', 'verdict'],
  stated: ['ibm', 'stated', 'record'],
  statedDate: ['statedDate', 'ibm_date', 'stated_date', 'record_date'],
};
const pick = (o, keys) => { if (!o) return undefined; for (const k of keys) if (o[k] !== undefined && o[k] !== null) return o[k]; return undefined; };

// 18 Nov (the referee): every printed time carries a zone. IBM's stamps are US Eastern (-04:00 / -05:00 with daylight time); cal.py
// files before 18 Nov kept them with the zone cut off. A stamp with Z or an offset is read as given; a bare one is read as US Eastern and
// printed in UTC, and the answer says it was converted.
export function utcStamp(s) {
  if (s == null || s === '') return { utc: null, converted: false };
  const str = String(s).trim().replace(' ', 'T');
  if (/(Z|[+-]\d\d:?\d\d)$/.test(str)) { const d = new Date(str); return { utc: isNaN(d) ? String(s) : d.toISOString().slice(0, 16) + 'Z', converted: false }; }
  const m = str.match(/^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d)/); if (!m) return { utc: String(s), converted: false, unparsed: true };
  const asUtc = Date.UTC(+m[1], +m[2] - 1, +m[3], +m[4], +m[5]);
  const off = d => { const p = new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
    .formatToParts(new Date(d)).reduce((a, x) => (a[x.type] = x.value, a), {});
    return Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute) - d; };
  let t = asUtc - off(asUtc); t = asUtc - off(t);
  // fall-back hour: the same bare Eastern time happens twice (-04:00 then -05:00); say so rather than pick silently
  const a = asUtc + 4 * 3600e3, b = asUtc + 5 * 3600e3, back = d => d + off(d) === asUtc;
  const ambiguous = back(a) && back(b);
  // spring-forward gap (the referee 18 Nov): a bare Eastern time that never existed on the clock is said, never mapped silently
  const gap = !back(a) && !back(b);
  return { utc: new Date(t).toISOString().slice(0, 16) + 'Z', converted: true, ...(ambiguous ? { ambiguous: true } : {}), ...(gap ? { gap: true } : {}) };
}
// Run windows are UTC by definition (window_utc). A window stamp that arrives without a zone is read as UTC and given its Z here, so the age
// check never depends on the machine's local zone and never gets the US Eastern conversion meant for IBM's stamps (the referee, 18 Nov).
export function windowUtc(s) {
  if (s == null || s === '') return s ?? null;
  const str = String(s).trim().replace(' ', 'T');
  if (/(Z|[+-]\d\d:?\d\d)$/.test(str)) { const d = new Date(str); return isNaN(d) ? String(s) : d.toISOString().replace('.000Z', 'Z'); }
  return /^\d{4}-\d\d-\d\dT\d\d:\d\d(:\d\d)?$/.test(str) ? (str.length === 16 ? str + ':00' : str) + 'Z' : String(s);
}
// Interval levels: read from the run when it carries them (cal.py from 18 Nov), else from cal.py's published rule (qia_cal/callib.py).
const RULE_LEVELS = { p10: 0.999, p01: 0.999, t1: 0.9999 };
export function normalizeCal(raw, processor) {
  if (!raw) return null;
  // cal.json may hold the latest run per processor: {ibm_fez: {...}, ...} or {runs: [...]}; a /qia/cal/<job>.json is one run
  let run = raw;
  if (raw[processor]) run = raw[processor];
  else if (!pick(raw, FIELD.job) && Object.keys(raw).some(k => /^ibm_/.test(k))) return null;   // a per-processor map without this processor
  else if (Array.isArray(raw.runs)) run = raw.runs.filter(r => pick(r, FIELD.processor) === processor).slice(-1)[0];
  if (!run || (pick(run, FIELD.processor) && pick(run, FIELD.processor) !== processor)) return null;
  const job = pick(run, FIELD.job);
  const win = Array.isArray(run.window_utc) ? run.window_utc : [];
  const out = { job, processor, start: windowUtc(pick(run, FIELD.start) ?? win[0]), end: windowUtc(pick(run, FIELD.end) ?? win[1]), url: job ? CAL_BASE + job + '.json' : null, qubits: {} };
  let qs = pick(run, FIELD.qubits) || [];
  if (!Array.isArray(qs)) qs = Object.entries(qs).map(([q, v]) => ({ qubit: Number(q), ...v }));
  for (const row of qs) {
    const q = Number(pick(row, FIELD.qubit)); if (!Number.isFinite(q)) continue;
    const m = {};
    for (const [p, keys] of Object.entries(FIELD.params)) {
      let r = pick(row, keys); if (r === undefined) continue;
      if (typeof r === 'number') {   // the real /qia/cal/<job>.json shape (checked 18 Nov on dbuha7larooc73fjuc10): flat fields per qubit
        const ci = row[p + '_ci'] || [];
        const lv = run.interval_levels ? (p === 't1' ? run.interval_levels.t1 : run.interval_levels.readout) : undefined;
        const fromRule = lv === undefined && /qia_cal PLAN\.md/.test(String(run.rule || ''));
        r = { value: r, lo: ci[0], hi: ci[1], outcome: row[p + '_outcome'], stated: row['ibm_' + p], statedDate: row['ibm_' + p + '_date'],
              conf: lv ?? (fromRule ? RULE_LEVELS[p] : undefined), conf_source: lv !== undefined ? 'run' : (fromRule ? "cal.py's published rule (not stored in this run's file)" : undefined) };
      }
      const k = pick(r, FIELD.k), n = pick(r, FIELD.n);
      m[p] = { value: pick(r, FIELD.value) ?? (k !== undefined && n ? k / n : undefined), lo: pick(r, FIELD.lo), hi: pick(r, FIELD.hi),
               k, n, conf: pick(r, FIELD.conf), conf_source: r.conf_source, outcome: pick(r, FIELD.outcome) ?? null, stated: pick(r, FIELD.stated), statedDate: pick(r, FIELD.statedDate) };
    }
    out.qubits[q] = m;
  }
  return out;
}

// ---- the join ---------------------------------------------------------------------------------------------------------------------------
const STATED = { p10: ['prob_meas1_prep0', 'prob_meas1_prep0_measured'], p01: ['prob_meas0_prep1', 'prob_meas0_prep1_measured'], t1: ['t1_us', 't1_measured'] };
const LABEL = { p10: 'P(1|0)', p01: 'P(0|1)', t1: 'T1 (us)' };
const hoursBetween = (a, b) => (new Date(b) - new Date(a)) / 3.6e6;
const fmt = (x, p = 4) => (x === undefined || x === null || !Number.isFinite(Number(x))) ? 'n/a' : (Math.abs(x) >= 10 ? Number(x).toFixed(1) : p === 1 ? Number(x).toFixed(1) : Number(Number(x).toPrecision(3)).toString());

const absent = (v, say) => (v === undefined || v === null || v === '' || (typeof v === 'number' && !Number.isFinite(v))) ? say : null;

export function rowFor(fig, cal, now, floors) {
  const q = fig.qubit; const m = cal && cal.qubits[q];
  const ageCal = cal && cal.end ? hoursBetween(cal.end, now) : null;
  const block = { qubit: q, job: cal ? cal.job : null, job_url: cal ? cal.url : null, window: cal ? { start: cal.start, end: cal.end } : null,
                  measurement_age_h: ageCal === null ? null : +ageCal.toFixed(1), current: false, fields: {}, absent: [] };
  if (!cal) { block.note = 'no hourly measurement of this processor in the published calibration'; return block; }
  if (ageCal === null) { block.note = `no recent run: the last hourly run (job ${cal.job}) gives no window end, so its age cannot be checked`; return block; }
  if (ageCal > RECENT_RUN_H) {
    block.note = `no recent run: the last hourly run (job ${cal.job}) ended ${cal.end}, ${ageCal.toFixed(1)} h before this answer (limit ${RECENT_RUN_H} h)`;
    return block;   // nothing from it is presented as current
  }
  if (!m) { block.note = `not measured in the latest hourly run (job ${cal.job})`; return block; }
  block.current = true;
  for (const p of ['p10', 'p01', 't1']) {
    const x = m[p]; if (!x) { block.absent.push(`${LABEL[p]}: not in the run`); continue; }
    const stated = fig[STATED[p][0]] ?? x.stated;
    const sdRaw = (STATED[p][1] && fig[STATED[p][1]]) || x.statedDate || null, sdz = utcStamp(sdRaw), sd = sdz.utc;
    const f = { stated: stated ?? null, stated_measured: sd, measured: x.value ?? null, interval: [x.lo ?? null, x.hi ?? null], conf: x.conf ?? null, conf_source: x.conf_source ?? null, stated_measured_note: sdz.converted ? (sdz.gap ? "IBM's bare stamp names a time that does not exist on the US Eastern clock (the spring-forward hour); the UTC shown is not a real reading of it" : sdz.ambiguous ? "IBM's US Eastern stamp in the repeated fall-back hour; read as daylight time, could be one hour later" : "IBM's US Eastern stamp, converted to UTC") : null,
                k: x.k ?? null, n: x.n ?? null, outcome: x.outcome, reads: direction(p, x.outcome),
                stated_age_h_at_answer: sd ? +hoursBetween(sd, now).toFixed(1) : null, absent: [] };
    for (const s of [absent(stated, 'IBM states no figure'), absent(sd, "IBM's entry date not given"), absent(x.value, 'no measured value in the run'),
                     (x.lo == null || x.hi == null) ? 'no interval in the run' : null, absent(x.conf, 'interval level not given in the run')]) if (s) f.absent.push(s);
    if (p === 't1') {
      f.ratio_measured_over_stated = (Number(stated) > 0 && Number.isFinite(Number(x.value))) ? +(x.value / stated).toFixed(3) : null;
      f.floor = (floors && floors[cal.processor] && floors[cal.processor].t1) || NO_FLOOR;
      f.method = T1_METHOD;
    }
    block.fields[LABEL[p]] = f;
  }
  return block;
}

// last-N history for one qubit over the hourly runs given (newest last): per field, how many runs measured it, median and range of the
// measured value, and counts of cal.py's own outcome words. No episode threshold of our own.
export function history(runsRaw, processor, qubit, n = HISTORY_N) {
  let list = Array.isArray(runsRaw) ? runsRaw : (runsRaw && Array.isArray(runsRaw.runs) ? runsRaw.runs : []);
  // the referee 18 Nov: only runs that passed cal.py's own known-good enter the history, so an apparatus fault is never counted as a qubit episode.
  const kgOk = r => r && (r.known_good === 'passed' || r.known_good === 'PASSED' || r.known_good === true);
  const mine = list.filter(r => r && (!pick(r, FIELD.processor) || pick(r, FIELD.processor) === processor));
  const failedKg = mine.filter(r => r.known_good !== undefined && !kgOk(r)).length, noKg = mine.filter(r => r.known_good === undefined).length;
  const runs = mine.filter(kgOk).map(r => normalizeCal(r, processor)).filter(Boolean)
    .sort((a, b) => String(a.end || '').localeCompare(String(b.end || ''))).slice(-n);
  const out = { runs_looked_at: runs.length, asked_for: n, first_end: runs.length ? runs[0].end : null, last_end: runs.length ? runs[runs.length - 1].end : null,
                runs_without_qubit: runs.filter(r => !r.qubits[qubit]).length, left_out_failed_known_good: failedKg, left_out_no_known_good: noKg, fields: {} };
  for (const p of ['p10', 'p01', 't1']) {
    const xs = runs.map(r => r.qubits[qubit] && r.qubits[qubit][p]).filter(Boolean);
    const v = xs.map(x => Number(x.value)).filter(Number.isFinite).sort((a, b) => a - b);
    const counts = {}; for (const x of xs) { const w = x.outcome || 'no outcome word'; counts[w] = (counts[w] || 0) + 1; }
    const h = v.length >> 1;
    out.fields[LABEL[p]] = { runs: xs.length, median: v.length ? +(v.length % 2 ? v[h] : (v[h - 1] + v[h]) / 2).toPrecision(4) : null,
                             range: v.length ? [v[0], v[v.length - 1]] : null, outcome_counts: counts };
  }
  return out;
}

export function historyLine(processor, qubit, hst) {
  if (!hst) return `${processor} q${qubit}, history: no earlier hourly runs supplied.`;
  if (!hst.runs_looked_at) {   // runs were given but none passed known-good: say that, not "none supplied"
    const left = (hst.left_out_failed_known_good || 0) + (hst.left_out_no_known_good || 0);
    if (!left) return `${processor} q${qubit}, history: no earlier hourly runs supplied.`;
    return `${processor} q${qubit}, history: no run counted; ${left} supplied, none passed known-good` +
      (hst.left_out_failed_known_good ? ` (${hst.left_out_failed_known_good} failed` : ' (') +
      (hst.left_out_no_known_good ? `${hst.left_out_failed_known_good ? ', ' : ''}${hst.left_out_no_known_good} without a known-good result` : '') + ').';
  }
  const parts = Object.entries(hst.fields).filter(([, f]) => f.runs).map(([k, f]) =>
    `${k} median ${fmt(f.median)} [range ${fmt(f.range[0])}-${fmt(f.range[1])}] over ${f.runs} runs; cal.py's words: ` +
    Object.entries(f.outcome_counts).map(([w, c]) => `${w} ${c}`).join(', '));
  return `${processor} q${qubit}, last ${hst.runs_looked_at} hourly runs (asked for ${hst.asked_for}; ${hst.first_end} to ${hst.last_end}` +
    (hst.runs_without_qubit ? `; ${hst.runs_without_qubit} without this qubit` : '') +
    `; only runs that passed known-good counted` + (hst.left_out_failed_known_good ? `, ${hst.left_out_failed_known_good} failed and left out` : '') +
    (hst.left_out_no_known_good ? `, ${hst.left_out_no_known_good} without a known-good result left out` : '') + '): ' + (parts.join('; ') || 'not measured in any of them') + '.';
}

export function line(processor, b) {
  if (!b.current) return `${processor} q${b.qubit}: ${b.note}.`;
  const parts = Object.entries(b.fields).map(([k, f]) => {
    const iv = (f.interval[0] == null || f.interval[1] == null) ? '(no interval in the run)' : `[${fmt(f.interval[0])}, ${fmt(f.interval[1])}]`;
    return `${k}: IBM states ${f.stated == null ? 'no figure' : fmt(f.stated)}` +
      (f.stated_measured ? ` (its entry ${f.stated_measured}${f.stated_measured_note ? ', ' + f.stated_measured_note : ''}, ${fmt(f.stated_age_h_at_answer, 1)} h old` + (b.record_stamp ? `; the record IBM's API returned is stamped ${b.record_stamp}, ${fmt(b.record_stamp_age_h, 1)} h old` : '') + ')' : " (IBM's entry date not given)" + (b.record_stamp ? ` (the record IBM's API returned is stamped ${b.record_stamp}, ${fmt(b.record_stamp_age_h, 1)} h old)` : ''))
      + `; measured ${fmt(f.measured)} ${iv}` + (f.conf ? ` at ${f.conf}` + (f.conf_source && f.conf_source !== 'run' ? ` (level from ${f.conf_source})` : '') : ' (interval level not given in the run)')
      + ` -> ${f.outcome ?? 'no outcome word'}: ${f.reads}`
      + (k.startsWith('T1') ? (f.ratio_measured_over_stated ? ` (measured/stated ${f.ratio_measured_over_stated})` : '')
          + `; IBM-vs-IBM T1 floor: ${typeof f.floor === 'string' ? f.floor : `${f.floor.fraction_below_1 !== undefined ? 'fraction below 1 ' + f.floor.fraction_below_1 : 'supplied'}${f.floor.lag_d ? ' at lag ' + f.floor.lag_d + ' d' : ''}`}; ${f.method}` : '');
  });
  const miss = b.absent.length ? ` Not in the run: ${b.absent.map(s => s.split(':')[0]).join(', ')}.` : '';
  return `${processor} q${b.qubit}, hourly run ${b.job} (window ${b.window.start} to ${b.window.end}, ended ${b.measurement_age_h} h before this answer; ${b.job_url}): `
    + parts.join('; ') + '.' + miss;
}

export function t1Median(cal, figures) {
  const r = figures.map(f => { const m = cal && cal.qubits[f.qubit] && cal.qubits[f.qubit].t1; return m && f.t1_us > 0 ? m.value / f.t1_us : NaN; })
    .filter(Number.isFinite).sort((a, b) => a - b);
  if (!r.length) return null;
  const h = r.length >> 1; return { median: +(r.length % 2 ? r[h] : (r[h - 1] + r[h]) / 2).toFixed(3), n: r.length };
}

// option A: inside qia_calibration_check's data (figures rows gain `measured`; data gains measured_note with the caveat and the record age)
export function attach(data, calRaw, opts = {}) {
  const now = opts.now || new Date().toISOString(); const cal = normalizeCal(calRaw, data.processor);
  // the readout entries' own dates are not in the figures rows; qia_calibration_check prints them in its flags ("measured YYYY-MM-DD HH:MM UTC")
  for (const f of ((data.flags || {}).error_figures || [])) {
    const d = /measured (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC/.exec(f.detail || ''); const fig = (data.figures || []).find(x => x.qubit === f.qubit);
    if (d && fig && /^prob_meas/.test(f.field)) fig[f.field + '_measured'] = d[1].replace(' ', 'T') + ':00Z';
  }
  for (const fig of data.figures || []) {
    fig.measured = rowFor(fig, cal, now, opts.floors);
    // the referee 18 Nov: the record's stamp age always beside each field's own entry age, no threshold (a new stamp is not new measurements)
    const rs = data.record && data.record.stamp ? utcStamp(data.record.stamp).utc : null;
    if (rs) { fig.measured.record_stamp = rs; fig.measured.record_stamp_age_h = +hoursBetween(rs, now).toFixed(1); }
    if (opts.history) fig.measured.history = history(opts.history, data.processor, fig.qubit, opts.historyN || HISTORY_N);
  }
  data.measured_note = {
    source: cal ? cal.url : 'no published hourly run for this processor',
    record_age_h: data.record ? data.record.age_hours_at_check : null,
    lines: (data.figures || []).map(f => line(data.processor, f.measured)),
    history_lines: opts.history ? (data.figures || []).map(f => historyLine(data.processor, f.qubit, f.measured.history)) : ['no earlier hourly runs supplied'],
    recent_run_limit_h: RECENT_RUN_H,
    t1_median_measured_over_stated: (cal && cal.end && hoursBetween(cal.end, now) <= RECENT_RUN_H) ? t1Median(cal, data.figures || []) : null,
    caveat: CAVEAT,
    method: 'qia_cal hourly: in-session P(1|0), P(0|1) with exact intervals and T1 with a profile interval against the record in force; outcome words are cal.py\'s (ABOVE = IBM\'s figure above our interval), translated, not recomputed. ' + T1_METHOD + '. ' +
            'Measured on the indahl.ai account; reproduce from the job file.',
  };
  return data;
}

// option B: a new read-only tool. checkData is qia_calibration_check's data for the same processor and qubits (the record-age line and the
// stated figures come from there, so the two tools never disagree on what IBM states).
export const TOOL = {
  name: 'qia_measured',
  description: 'The latest hourly measurement of IBM qubits beside the figure IBM publishes for them: for each qubit, IBM\'s stated P(1|0), ' +
    'P(0|1) and T1 with their measurement dates and the record\'s age, our measured value with its interval from the newest hourly run, the job id, ' +
    'its window, cal.py\'s outcome word with a plain sentence of which way it points, the job file URL to reproduce it, and the qubit\'s last hourly ' +
    'runs (median, range, outcome counts). A run older than ' + RECENT_RUN_H + ' h is reported as no recent run. Read-only; no QPU time is spent by asking. ' +
    'A record days old disagrees with today\'s hardware by drift too, so a gap names a gap, not a cause; one run is one look.',
  inputSchema: { type: 'object', properties: {
    processor: { type: 'string', description: 'IBM processor, for example ibm_fez.' },
    qubits: { type: 'string', description: 'Qubits: "155" or "0,1,5" or "0-5". Empty lists every measured qubit.' } }, required: ['processor'] },
};
export function qiaMeasured(checkData, calRaw, opts = {}) {
  const d = attach(JSON.parse(JSON.stringify(checkData)), calRaw, opts);
  return { processor: d.processor, headline: d.headline, record: d.record,
           qubits: (d.figures || []).map(f => ({ qubit: f.qubit, measured: f.measured })), lines: d.measured_note.lines,
           history_lines: d.measured_note.history_lines, recent_run_limit_h: RECENT_RUN_H,
           t1_median_measured_over_stated: d.measured_note.t1_median_measured_over_stated, caveat: CAVEAT, source: d.measured_note.source,
           reproduce: { job_file: d.measured_note.source, stated: (d.reproduce || {}).records } };
}

// Test Drive (indahl.ai/try): one more menu entry, calling the same tool, no key, signed receipt as the paper check does.
export const TRY_ENTRY = { id: 'ibm-qubit', label: 'A qubit on an IBM processor', tool: 'qia_measured',
  fields: [{ name: 'processor', label: 'Processor', placeholder: 'ibm_fez' }, { name: 'qubits', label: 'Qubit(s)', placeholder: '155' }],
  example: { processor: 'ibm_fez', qubits: '155' }, receipt: true, caveat: CAVEAT };
