// connector_tool.mjs -- qia_measured as a separate read-only tool in the Indahl Quantum connector, beside qia_calibration_check, and the
// Test Drive row that shows the same answer text. The operator's ball on PR #1 (comment 6969497405, 18 Nov). Staged here because the connector source
// (indahl-ai/tools_qia.js, tests indahl-ai/tests/test_qia.mjs) and indahl-ai/try.html are in a repository this session cannot open; this file is
// written to be imported by tools_qia.js unchanged. No dependencies.
//   QIA_MEASURED_TOOL            the tool definition: name, title, description, inputSchema, outputSchema, annotations
//   makeQiaMeasuredHandler(deps) the handler: (args) -> { content: [{type:'text', text}], structuredContent }
//     deps.fetchJson(url)        the worker's own fetch-and-parse (for indahl.ai/qia/cal.json and /qia/cal/<job>.json)
//     deps.calibrationCheck(args) qia_calibration_check's existing data function, called as is; its output is read, never changed
//     deps.now(), deps.floors, deps.historyN (optional)
//   answerText(result)           the one text both the tool and the Test Drive row show
//   locateRuns(index, processor) the ONE place that knows cal.json's index shape (assumed; the operator to confirm)
// Heuremen LLC.
import { qiaMeasured, TOOL, TRY_ENTRY, CAL_BASE, HISTORY_N, CAVEAT } from './qia_measured.mjs';

export const CAL_INDEX = 'https://indahl.ai/qia/cal.json';
export const MAX_HISTORY = 48;   // a cap on job files fetched per call, whatever historyN asks

const str = { type: 'string' }, num = { type: 'number' }, nul = t => ({ type: [t, 'null'] });
const fieldSchema = { type: 'object', properties: {
  stated: nul('number'), stated_measured: nul('string'), measured: nul('number'), interval: { type: 'array', items: nul('number') },
  outcome: nul('string'), reads: str, stated_age_h_at_answer: nul('number'), absent: { type: 'array', items: str } } };
export const QIA_MEASURED_TOOL = {
  name: TOOL.name,
  title: 'Measured against stated, per IBM qubit',
  description: TOOL.description,
  inputSchema: TOOL.inputSchema,
  outputSchema: { type: 'object', required: ['processor', 'lines', 'caveat'], properties: {
    processor: str, headline: nul('string'), source: str, recent_run_limit_h: num,
    lines: { type: 'array', items: str }, history_lines: { type: 'array', items: str },
    qubits: { type: 'array', items: { type: 'object', required: ['qubit'], properties: {
      qubit: num, measured: { type: 'object', properties: {
        job: nul('string'), job_url: nul('string'), current: { type: 'boolean' }, measurement_age_h: nul('number'), note: str,
        fields: { type: 'object', additionalProperties: fieldSchema } } } } } },
    t1_median_measured_over_stated: { type: ['object', 'null'] }, caveat: str,
    runs_fetched: { type: 'object', properties: { asked: num, loaded: num, failed: { type: 'array', items: str } } } } },
  // MCP annotation names; the operator's ball: readOnly true, openWorld false, destructive false
  annotations: { readOnlyHint: true, openWorldHint: false, destructiveHint: false, idempotentHint: true },
};

// cal.json's index shape is not visible from here. Accepted forms (first match wins), newest job last in `recent`:
//   { ibm_fez: { job_id|job|latest, recent|runs|jobs: [id | {job_id}] } }   { processors: { ibm_fez: {...same} } }
//   { runs: [{ job_id|job, backend|processor, window_utc|end }] }          a single run object (latest only)
const idOf = r => typeof r === 'string' ? r : (r && (r.job_id || r.job)) || null;
export function locateRuns(index, processor) {
  if (!index) return { latest: null, recent: [] };
  const p = (index.processors && index.processors[processor]) || index[processor];
  if (p) {
    const recent = (p.recent || p.runs || p.jobs || []).map(idOf).filter(Boolean);
    const latest = idOf(p.job_id || p.job || p.latest) || recent[recent.length - 1] || null;
    if (latest && recent[recent.length - 1] !== latest) recent.push(latest);
    return { latest, recent };
  }
  if (Array.isArray(index.runs)) {
    const mine = index.runs.filter(r => (r.backend || r.processor) === processor)
      .sort((a, b) => String((a.window_utc || [])[1] || a.end || '').localeCompare(String((b.window_utc || [])[1] || b.end || '')));
    const recent = mine.map(idOf).filter(Boolean); return { latest: recent[recent.length - 1] || null, recent };
  }
  if ((index.backend || index.processor) === processor && idOf(index)) return { latest: idOf(index), recent: [idOf(index)] };
  return { latest: null, recent: [] };
}

export function answerText(r) {
  return [r.headline ? `Record: ${r.headline}` : null, ...r.lines, ...(r.history_lines || []),
          r.runs_fetched && r.runs_fetched.failed.length ? `${r.runs_fetched.failed.length} of ${r.runs_fetched.asked} hourly job files did not load: ` + r.runs_fetched.failed.join(', ') + '.' : null,
          `Source: ${r.source}.`, r.caveat].filter(Boolean).join('\n');
}

export function makeQiaMeasuredHandler(deps) {
  const now = deps.now || (() => new Date().toISOString());
  return async function qia_measured(args = {}) {
    const processor = String(args.processor || '').trim();
    if (!/^ibm_[a-z0-9_]+$/.test(processor)) {
      const text = `Give an IBM processor name such as ibm_fez (got "${processor}").`;
      return { content: [{ type: 'text', text }], structuredContent: { processor, lines: [text], caveat: CAVEAT }, isError: true };
    }
    const n = Math.min(Number(deps.historyN) || HISTORY_N, MAX_HISTORY);
    let index = null, failed = [];
    try { index = await deps.fetchJson(CAL_INDEX); } catch (e) { failed.push('cal.json'); }
    const { latest, recent } = locateRuns(index, processor);
    const ids = recent.slice(-n); if (latest && !ids.includes(latest)) ids.push(latest);
    const loaded = await Promise.all(ids.map(async id => {
      try { return await deps.fetchJson(CAL_BASE + id + '.json'); } catch (e) { failed.push(id); return null; } }));
    const byId = Object.fromEntries(ids.map((id, i) => [id, loaded[i]]));
    const latestRun = latest ? byId[latest] : null;
    const check = await deps.calibrationCheck({ processor, qubits: args.qubits });   // read only; qiaMeasured works on a copy
    const r = qiaMeasured(check, latestRun, { now: now(), floors: deps.floors, history: loaded.filter(Boolean), historyN: n });
    r.runs_fetched = { asked: ids.length, loaded: loaded.filter(Boolean).length, failed };
    return { content: [{ type: 'text', text: answerText(r) }], structuredContent: r };
  };
}

// Test Drive row for indahl-ai/try.html: the menu entry (from qia_measured.mjs) and what the page shows, which is the tool's own text.
export const TRY_ROW = TRY_ENTRY;
export async function tryAnswer(handler, args) { const out = await handler(args); return out.content[0].text; }
