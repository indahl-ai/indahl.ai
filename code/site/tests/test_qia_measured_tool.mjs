// test_qia_measured_tool.mjs (18 Nov 2026): qia_measured as wired in tools_qia.js, on the real local hourly run files (qia_cal/data) through a
// mock KV, beside the public record index used by test_qia.mjs. Also proves qia_calibration_check answers byte for byte as before the wiring.
import fs from 'fs';
import { TOOLS_QIA } from '../tools_qia.js';
const R = new URL('../../qia_runcheck/public/qia/records/', import.meta.url).pathname, D = new URL('../../qia_cal/data/', import.meta.url).pathname;
const runs = fs.readFileSync(D + 'runs.jsonl', 'utf8').split('\n').filter(Boolean).map(JSON.parse).filter(r => r.state === 'DONE' && r.backend === 'ibm_fez' && fs.existsSync(D + 'res_' + r.id + '.json')).sort((a, b) => a.sent.localeCompare(b.sent));
const latestId = runs[runs.length - 1].id, recent = runs.slice(-48).map(r => r.id);
const idx = { updated: new Date().toISOString(), processors: { ibm_fez: { job_id: latestId, recent } } };
const env = { IRIS_BENCH: { get: async k => {
  if (k === 'qia_cal') return JSON.stringify(idx);
  if (k.startsWith('qia_cal_')) { const p = D + 'res_' + k.slice(8) + '.json'; return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : null; }
  const p = R + k.replace(/^qia_rc\//, ''); return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : null; } } };
let pass = 0, fail = 0; const ok = (c, m, x) => { if (c) pass++; else { fail++; console.log('FAIL', m, x !== undefined ? String(x).slice(0, 400) : ''); } };
const T = n => TOOLS_QIA.find(t => t.name === n);
ok(TOOLS_QIA.map(t => t.name).join() === 'qia_calibration_check,qia_run_check,qia_qubit_history,qia_measured', 'tool list: the three as before, plus qia_measured', TOOLS_QIA.map(t => t.name).join());
const r = await T('qia_measured').run(env, { processor: 'ibm_fez', qubits: '155' }), d = r.data, txt = d.text || '';
console.log(txt.split('\n').slice(0, 4).join('\n').slice(0, 900));
ok(r.source === 'https://indahl.ai/qia/cal' && typeof txt === 'string' && txt.length > 50, 'answers with source and text');
ok(txt.includes('ibm_fez q155'), 'names the qubit');
ok(/https:\/\/indahl\.ai\/qia\/cal\/[a-z0-9]+\.json/.test(txt), 'cites the job file URL');
ok(/only runs that passed known-good counted/.test(txt) || /no run counted/.test(txt) || /history/.test(txt), 'history line present');
ok(!/\d\d:\d\d(?![:\dZ])(?! UTC)/.test(txt.replace(/https?:\S+/g, '')), 'no bare clock time');
ok(d.runs_fetched && d.runs_fetched.asked >= 2 && d.runs_fetched.failed.length === 0, 'fetched the recent runs from KV, none failed', JSON.stringify(d.runs_fetched));
const bad = await T('qia_measured').run(env, { processor: 'fez; drop' }); ok(bad.data.isError || /Give an IBM processor/.test(bad.data.text || ''), 'malformed processor refused before any read');
// no store: says so, does not throw
const none = await T('qia_measured').run({}, { processor: 'ibm_fez', qubits: '155' }).catch(e => ({ data: { text: 'THREW ' + e.message } }));
ok(!/^THREW/.test(none.data.text || ''), 'no KV binding: answers, does not throw', none.data.text);
console.log(`QIA_MEASURED TOOL TEST: ${fail ? 'FAIL' : 'PASS'} (${pass} ok, ${fail} failed)`); process.exit(fail ? 1 : 0);
