// quantumidleaudit.com "Check a run" (21 Nov 2026): the indahl.ai/qia check on the home page, in the Console look.
// The checks are the tested engine /qia/runcheck.js (window.QIARunCheck, the qia_check.py rules); this file is the form and the result.
// It reads only same-origin static files: /qia/records/, /qia/cal.json and /qia/cal/<job>.json, /qia/offchain.json.
// Nothing typed here is sent or uploaded. The IBM job ID field never asks for, accepts or keeps an API token.
// The Inquire link under a result carries processor, window, qubits and a one-line summary to /inquiries (carry_result.js).
(function () {
  'use strict';
  var box = document.getElementById('cr-live'); if (!box) return;
  var INQ = box.getAttribute('data-inquire') || '/inquiries';
  var Q = window.QIARunCheck;
  var form = document.getElementById('cr-form'), out = document.getElementById('cr-out'), jobNote = document.getElementById('cr-job-note');
  var fJob = document.getElementById('cr-job'), fProc = document.getElementById('cr-proc'), fStart = document.getElementById('cr-start'),
    fEnd = document.getElementById('cr-end'), fQ = document.getElementById('cr-q');
  if (!Q || !form) { if (out) out.textContent = 'The check could not start in this browser.'; return; }

  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function iso(ms) { return new Date(ms).toISOString().replace(/\.\d{3}Z$/, 'Z'); }
  function p2(n) { return (n < 10 ? '0' : '') + n; }
  function sec(ms) { var d = new Date(ms); return Q.minute(ms) + ':' + p2(d.getUTCSeconds()); }
  function cap(m) { return el('p', 'qia-cap', m); }
  function h3(m) { return el('h3', 'qia-cr__h', m); }
  var WORD = { ABOVE: 'above', BELOW: 'below', CONSISTENT: 'consistent', CANNOT_TELL: 'cannot' };
  function cell(v, cls) {
    var td = el('td', cls || null);
    var w = WORD[v]; if (w) { td.appendChild(el('span', 'qia-word qia-word--' + w, String(v).replace('_', ' '))); return td; }
    td.textContent = v == null ? '' : String(v); return td;
  }
  function table(caption, cols, rows) {
    var wrap = el('div', 'qia-tablewrap'), t = el('table', 'qia-table'), hd = el('tr'), th = el('thead'), b = el('tbody');
    t.appendChild(el('caption', 'qia-cr__cap', caption));
    cols.forEach(function (c) { var h = el('th', null, c[0]); h.setAttribute('scope', 'col'); hd.appendChild(h); });
    th.appendChild(hd); t.appendChild(th);
    rows.forEach(function (r) { var tr = el('tr'); cols.forEach(function (c) { tr.appendChild(cell(r[c[1]], c[2])); }); b.appendChild(tr); });
    t.appendChild(b); wrap.appendChild(t); return wrap;
  }
  var cache = {};
  function getJson(u) {
    if (!cache[u]) cache[u] = fetch(u, { credentials: 'omit' }).then(function (r) { if (!r.ok) throw new Error(u + ' ' + r.status); return r.json(); });
    return cache[u];
  }

  // ---- processors: the live list of what the mirror holds ----
  var procs = [];
  getJson('/qia/records/index.json').then(function (ix) {
    fProc.textContent = '';
    ix.processors.forEach(function (p) { procs.push(p.backend); var o = el('option', null, p.backend); o.value = p.backend; fProc.appendChild(o); });
  }).catch(function () { out.textContent = 'The list of processors could not be read just now.'; });

  // ---- the IBM job ID field: a job ID, or a pasted line from the visitor's own job record. Never a token. ----
  var JOBID = /\b([a-z0-9]{20})\b/;
  var ISOANY = /(\d{4}-\d\d-\d\d[T ]\d\d:\d\d(?::\d\d(?:\.\d+)?)?\s*(?:Z|[+-]\d\d(?::?\d\d)?)?)/ig;
  function looksLikeKey(s) {
    if (/\b(api[_ -]?key|apikey|token|bearer|password|secret)\b/i.test(s)) return true;
    return s.split(/[\s"',:{}()=]+/).some(function (w) { return w.length >= 40 || (w.length >= 32 && /[A-Z_-]/.test(w) && /\d/.test(w)); });
  }
  function keyedTime(s, names) {   // "running": "2026-...Z", running=..., running: ...
    var re = new RegExp('[\'"]?(?:' + names + ')[\'"]?\\s*[:=]\\s*(?:datetime\\.datetime\\()?[\'"]?(\\d{4}-\\d\\d-\\d\\d[T ]\\d\\d:\\d\\d(?::\\d\\d(?:\\.\\d+)?)?\\s*(?:Z|[+-]\\d\\d(?::?\\d\\d)?)?)', 'i');
    var m = re.exec(s); return m ? m[1] : null;
  }
  var lastJob = '';
  function readJobField() {
    var s = fJob.value; jobNote.textContent = ''; lastJob = '';
    if (!s.trim()) return;
    if (looksLikeKey(s)) {
      fJob.value = '';
      jobNote.appendChild(el('p', 'qia-cr__warn', 'That looks like an API key or token, so it was cleared from the field. Nothing was read, kept or sent. This check never needs one.'));
      return;
    }
    var m = JOBID.exec(s), job = m ? m[1] : '';
    lastJob = job;
    var filled = [], missing = [];
    var b = /\b(ibm_[a-z]+)\b/.exec(s);
    if (b) {
      if (procs.indexOf(b[1]) > -1) { fProc.value = b[1]; filled.push('processor ' + b[1]); }
      else missing.push(b[1] + ' is not a processor in our mirror');
    }
    var st = keyedTime(s, 'running|started|start|run_start'), en = keyedTime(s, 'finished|completed|ended|end|run_end'), from = 'the keys';
    if (!st && !en) {   // two bare times and nothing else: the first is the start, the second the end
      var all = s.match(ISOANY) || [];
      if (all.length === 2 && !/created|queued|submitted/i.test(s)) { st = all[0]; en = all[1]; from = 'order'; }
    }
    [[st, fStart, 'start'], [en, fEnd, 'end']].forEach(function (x) {
      if (!x[0]) return; var t = Q.parseWhen(x[0]);
      if (isNaN(t)) { missing.push('the ' + x[2] + ' time could not be read'); return; }
      x[1].value = sec(t); filled.push(x[2] + ' ' + sec(t) + ' UTC');
    });
    if (filled.length) {
      jobNote.appendChild(el('p', 'qia-cap', 'Filled from what you pasted: ' + filled.join(', ') + '.' +
        (from === 'order' ? ' The first time was read as the start and the second as the end.' : '') + ' Check them before you press Check.'));
    }
    if (missing.length) jobNote.appendChild(el('p', 'qia-cap', 'Not filled: ' + missing.join('; ') + '.'));
    if (!filled.length) {
      jobNote.appendChild(el('p', 'qia-cap', (job ? 'Job ' + job + ': we' : 'We') + ' can’t look up a job from here. Reading a job takes your IBM token, and we never ask for one.'));
      jobNote.appendChild(el('p', 'qia-cap', 'Read three things from your own job record and enter them below: the backend, when the job started running and when it finished. In Qiskit they are job.backend().name and the “running” and “finished” times in job.metrics()["timestamps"]. Paste that timestamps line here and the form fills in.'));
    }
  }
  fJob.addEventListener('change', readJobField);
  fJob.addEventListener('paste', function () { setTimeout(readJobField, 0); });

  // ---- the check ----
  form.addEventListener('submit', function (ev) {
    ev.preventDefault(); out.textContent = '';
    var s = Q.parseWhen(fStart.value), e = Q.parseWhen(fEnd.value), q = Q.parseQubits(fQ.value), b = fProc.value;
    function say(m) { out.appendChild(cap(m)); }
    if (isNaN(s) || isNaN(e)) return say('Give the start and the end as UTC times like 2026-11-01 12:00. A time with Z or an offset, for example 2026-11-01T12:00:00-05:00, is converted to UTC.');
    if (e < s) return say('The end is earlier than the start.');
    if (q.error) return say(q.error);
    if (!b) return say('Pick a processor.');
    say('Reading the records.');
    Q.load(getJson, b, s, e, q).then(function (r) { render(r, b, s, e, q); }).catch(function () { out.textContent = ''; say('The records could not be read just now.'); });
  });

  function render(r, b, s, e, q) {
    out.textContent = '';
    var m = r.manifest, panel = el('div', 'qia-panel qia-cr__res'), head = el('div', 'qia-panel__head'), body = el('div', 'qia-cr__body');
    head.appendChild(el('span', null, 'Run window, UTC: ' + Q.minute(s) + ' to ' + Q.minute(e)));
    head.appendChild(el('span', null, b + (lastJob ? ' · job ' + lastJob : '')));
    panel.appendChild(head); panel.appendChild(body); out.appendChild(panel);
    function add(x) { body.appendChild(x); }
    if (!r.under) {
      add(el('p', null, 'No record in the indahl.ai mirror is stamped at or before the run start, so the record in force at the start is not here. Our mirror of ' + b + ' begins at ' + (m.first ? sec(Q.parseWhen(m.first)) : '') + ' UTC.'));
    } else {
      var age = (s - r.under.stamp) / 3600000;
      add(cap('What this checks: the record in force at the start, for the qubits in that record. Records stamped during the run are listed and their changes shown, but their own flags are not checked here. The qia-check package checks each of them (qia-check after).'));
      add(h3('The record in force at the start'));
      add(el('p', null, 'The latest record in the indahl.ai mirror stamped at or before the start was stamped ' + sec(r.under.stamp) + ' UTC, ' + Q.fmtFixed(age, 1) + ' hours before the start. File: ' + r.under.file + '. If IBM recalibrated after it and before the run, the record in force is not in the indahl.ai mirror.'));
      if (r.inForce.length > 1) add(cap('The indahl.ai mirror holds ' + r.inForce.length + ' files with that stamp. ' + (r.conflict ? 'Their figures differ, so which one was in force is not known. The flags below are for the first file.' : 'Their figures are the same.')));
      if (m.newest && Q.parseWhen(m.newest) < e) add(cap('The newest indahl.ai record for ' + b + ' is stamped ' + sec(Q.parseWhen(m.newest)) + ' UTC, earlier than the end of the run, so later records may exist that are not here yet.'));
      if (r.missing.length) add(cap('Not in this record, so not checked: qubits ' + r.missing.join(', ') + '.'));
      add(h3('Flags in that record, for ' + (q.all ? 'every qubit' : 'qubits in the run')));
      if (!r.flags.length) add(el('p', null, 'Nothing flagged in the figures this check reads.'));
      else {
        var nu = r.flags.filter(function (x) { return x.check === 'UNKNOWN'; }).length;
        if (nu) add(cap(nu + ' UNKNOWN row' + (nu === 1 ? '' : 's') + ': something could not be read. UNKNOWN is not a pass.'));
        add(table('Flags in the record in force at the start', [['Qubit', 'qubit'], ['Check', 'check'], ['Figure', 'field'], ['Detail', 'detail'], ['Outcome', 'outcome']],
          r.flags.map(function (x) { return { qubit: x.qubit, check: x.check, field: x.field, detail: String(x.detail).replace(/; /g, ', '), outcome: x.outcome }; })));
      }
      add(h3('Records IBM stamped during the run'));
      if (!r.during.length) add(el('p', null, (m.newest && Q.parseWhen(m.newest) < e) ? 'None in the indahl.ai mirror so far. The indahl.ai records stop before the end of the run, so a later record may still appear.' : 'None. No record in the indahl.ai mirror was stamped between the start and the end of the run.'));
      else {
        var ul = el('ul', 'qia-cr__list'); r.during.forEach(function (x) { ul.appendChild(el('li', null, sec(x.stamp) + ' UTC, ' + x.file)); }); add(ul);
        if (!r.changes.length) add(el('p', null, 'The T1, T2 and error figures on these qubits did not change in those records.'));
        else {
          add(el('p', null, 'T1, T2 or error figures on these qubits changed during the run. Each record is set against the one before it.'));
          var U = { T1: ' (µs)', T2: ' (µs)' };
          function utc(x) { if (!x) return ''; var t = Q.parseWhen(x); return isNaN(t) ? String(x) : sec(t); }
          add(table('Figures that changed during the run', [['Record, UTC', 'record'], ['Qubit', 'qubit'], ['Figure', 'fl'], ['Before', 'before'], ['After', 'after'], ['Measured before, UTC', 'db'], ['Measured after, UTC', 'da']],
            r.changes.map(function (c) { return { record: c.record, qubit: c.qubit, fl: c.field + (U[c.field] || ''), before: c.before, after: c.after, db: utc(c.date_before), da: utc(c.date_after) }; })));
        }
      }
      add(cap('These checks read IBM’s published figures only and make no claim about your results. Compare your results against the record in force.'));
    }
    var want = q.all ? [] : q.list, meas = el('div'), chain = el('div');
    add(meas); add(chain);
    measured(b, want, s, meas);
    offChain(b, want, s, chain);
    var cta = el('p', 'qia-cr__cta'); cta.appendChild(document.createTextNode('Want this for every run? '));
    var a = el('a', 'qia-link', 'Inquire'); a.href = INQ; cta.appendChild(a); out.appendChild(cta);
    // CI (21 Nov): the Inquire link carries this result to /inquiries in the URL fragment, never to a server (carry_result.js).
    var C = window.QIACarry;
    if (C) {
      var carry = { processor: b, start: iso(s), end: iso(e), qubits: q.all ? [] : q.list, summary: C.summarize(r, { start: s }) };
      a.href = C.inquiryHref(carry, { base: INQ });
      C.storeOnClick(a, carry);   // FW-007: the same-tab copy is kept only when Inquire is clicked
    }
  }

  // ---- our measurement of those qubits: the newest indahl.ai calibration job on the processor (as indahl.ai/qia shows it) ----
  function measured(b, want, s, box2) {
    box2.appendChild(h3('Measured by indahl.ai on ' + b + ', newest run'));
    var st = cap('Reading our newest run.'); box2.appendChild(st);
    getJson('/qia/cal.json').then(function (d) {
      var p = (d.processors || {})[b];
      if (!p) { st.textContent = 'We have no measurement run on ' + b + ' yet.'; return null; }
      return getJson('/qia/cal/' + p.job_id + '.json').then(function (run) {
        var t0 = Q.parseWhen(String((p.window_utc || [''])[0])), hrs = isNaN(t0) ? null : (t0 - s) / 3600000;
        st.textContent = 'Our newest job on ' + b + ' ran ' + (isNaN(t0) ? '' : Q.minute(t0) + ' UTC, ') + (hrs == null ? '' : Q.fmtFixed(Math.abs(hrs), 1) + ' hours ' + (hrs >= 0 ? 'after' : 'before') + ' the start of your run, ') + 'job ' + p.job_id + '. Intervals: 99.9% for readout, 99.99% for T1. IBM’s dates are in US Eastern time.';
        var rows = (run.qubits || []).filter(function (x) { return !want.length || want.indexOf(x.qubit) > -1; });
        if (!rows.length) { box2.appendChild(cap('None of these qubits is in that run.')); return; }
        function rd(v, dt) { return v == null ? '' : (+v).toFixed(4) + (dt ? ', ' + dt : ''); }
        function ci(v, c) { return v == null ? '' : v + (c ? ' [' + c.join(', ') + ']' : ''); }
        box2.appendChild(table('Our measurement against IBM’s record in force when our job ran',
          [['Qubit', 'q'], ['P(1|0) ours', 'a'], ['IBM, date', 'b'], ['', 'c'], ['P(0|1) ours', 'd'], ['IBM, date', 'e'], ['', 'f'], ['T1 ours, µs', 'g'], ['IBM, date', 'h'], ['', 'i']],
          rows.map(function (x) { return { q: x.qubit, a: ci(x.p10, x.p10_ci), b: rd(x.ibm_p10, x.ibm_p10_date), c: x.p10_outcome, d: ci(x.p01, x.p01_ci), e: rd(x.ibm_p01, x.ibm_p01_date), f: x.p01_outcome,
            g: ci(x.t1, x.t1_ci), h: (x.ibm_t1 == null ? '' : (+x.ibm_t1).toFixed(1)) + (x.ibm_t1_date ? ', ' + x.ibm_t1_date : ''), i: x.t1_outcome }; })));
      });
    }).catch(function () { st.textContent = 'Our measurement could not be read just now.'; });
  }

  // ---- the off-record chain: every time one of our jobs found IBM's figure outside what the qubit delivered, nearest the run first ----
  function offChain(b, want, s, box2) {
    box2.appendChild(h3('When IBM’s calibration was off, near this run'));
    var st = cap('Loading the chain.'); box2.appendChild(st);
    getJson('/qia/offchain.json').then(function (c) {
      var raw = c.entries || [], sup = {}, es = [];
      raw.forEach(function (x) { if (x.corrects != null) sup[x.corrects] = x.n; });
      function n(v, u) { return v == null ? '' : (u === 'us' ? Number(v).toFixed(1) : Number(v).toPrecision(3)); }
      raw.forEach(function (x) {
        if (sup[x.n] != null || !x.window_utc || (x.type !== 'calibration run' && !x.qubits)) return;
        if (x.type === 'calibration run') (x.off || []).forEach(function (o) {
          es.push({ n: x.n, processor: x.processor, qubits: [o.qubit], quantity: o.quantity, ibm: n(o.ibm, o.unit) + (o.unit ? ' ' + o.unit : '') + (o.ibm_date ? ', ' + o.ibm_date : ''),
            meas: n(o.measured, o.unit) + (o.interval ? ' [' + n(o.interval[0], o.unit) + ', ' + n(o.interval[1], o.unit) + ']' : ''), outcome: o.outcome, w: x.window_utc, job: x.job_id });
        });
        else es.push({ n: x.n, processor: x.processor, qubits: x.qubits, quantity: x.quantity, ibm: (x.ibm_stated == null ? '' : x.ibm_stated + (x.unit ? ' ' + x.unit : '') + ', ') + (x.ibm_date || ''),
          meas: x.measured ? (x.measured.interval ? x.measured.value + ' [' + x.measured.interval.join(', ') + ']' : (x.measured.bound != null ? 'at most ' + x.measured.bound : String(x.measured.value))) : '', outcome: x.outcome, w: x.window_utc, job: x.job_id });
      });
      var rows = es.filter(function (x) { return x.processor === b && (!want.length || (x.qubits || []).some(function (q) { return want.indexOf(q) > -1; })); });
      if (!rows.length) { st.textContent = 'No entry on ' + b + (want.length ? ' for qubits ' + want.join(', ') : '') + '. No entry means none of our readings of it was off.'; return; }
      rows.forEach(function (x) { x.h = (Q.parseWhen(x.w[0]) - s) / 3600000; });
      rows.sort(function (a, z) { return Math.abs(a.h) - Math.abs(z.h); });
      var shown = rows.slice(0, 12);
      st.textContent = rows.length + (rows.length === 1 ? ' entry' : ' entries') + ' on ' + b + (want.length ? ' for these qubits' : '') + (rows.length > shown.length ? '. The ' + shown.length + ' nearest your run are shown.' : '.') + ' Each is hashed into the chain, append only.';
      box2.appendChild(table('Readings where IBM’s figure was outside what the qubit delivered, nearest your run first',
        [['#', 'n'], ['Qubits', 'qs'], ['Quantity', 'quantity'], ['IBM published, date (US Eastern)', 'ibm'], ['Measured by our job', 'meas'], ['Reading', 'outcome'], ['Our job ran, UTC', 'when'], ['From your run', 'from'], ['Job ID', 'job']],
        shown.map(function (x) { return { n: x.n, qs: (x.qubits || []).join(', '), quantity: x.quantity, ibm: x.ibm, meas: x.meas, outcome: x.outcome,
          when: String(x.w[0]).replace('T', ' ').slice(0, 16), from: (function (v) { return v === '-0.0' || v === '0.0' ? '0.0 h' : (x.h > 0 ? '+' : '') + v + ' h'; })(Q.fmtFixed(x.h, 1)), job: x.job || '' }; })));
    }).catch(function () { st.textContent = 'The chain could not be read just now.'; });
  }
})();
