// indahl.ai test drive (15 Nov 2026): one arXiv id or DOI, checked live by the indahl.ai MCP server, the same server assistants use.
// Runs paper_check, and paper_statistics for arXiv ids, then shows each result in plain rows with its signed receipt underneath.
(function () {
  var f = document.getElementById('tryf'); if (!f) return;
  var o = document.getElementById('tryout'), m = document.getElementById('trymode'), inp = document.getElementById('tryin');
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function mode() { return m ? m.value : 'paper'; }
  function show() {
    var md = mode(), p = md !== 'stats';
    inp.placeholder = md === 'qubit' ? 'A processor and qubits, for example: ibm_fez q5   or   ibm_kingston 0-5' : (md === 'paper' ? 'An arXiv id (2401.01234) or a DOI (10.xxxx/...)' : 'Paste a passage with reported statistics, for example: t(28) = 2.20, p = .036');
    inp.rows = p ? 1 : 5;
  }
  if (m) m.addEventListener('change', show); show();
  function call(name, args) {
    return fetch('/mcp', { method: 'POST', headers: { 'content-type': 'application/json', 'accept': 'application/json, text/event-stream' },
      body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name: name, arguments: args } }) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j.error) throw new Error(j.error.message || 'refused');
        var c = (j.result && j.result.content) || [], ans = null, rec = null;
        try { ans = JSON.parse(c[0].text); } catch (e) { ans = { raw: c[0] && c[0].text }; }
        if (c[1]) { try { rec = JSON.parse(c[1].text); } catch (e) { rec = c[1].text; } }
        return { ans: ans, rec: rec };
      });
  }
  var BADGE = { CONSISTENT: 'ok', NONE_FOUND: 'ok', NO_MENTION: 'ok', answers: 'ok', read: 'ok', ABOVE: 'bad', BELOW: 'bad', MENTIONS_WITHDRAWAL: 'bad', FOUND: 'bad', gone: 'bad' };
  function badge(s) { s = String(s || ''); var k = BADGE[s] || (/^CANNOT_TELL/.test(s) ? 'ct' : (/notice/i.test(s) ? 'bad' : 'n')); return '<span class="tb tb-' + k + '">' + esc(s) + '</span>'; }
  function receipt(rec) {
    return rec ? '<details class="trec"><summary>Signed receipt</summary><pre class="tryjson">' + esc(typeof rec === 'string' ? rec : JSON.stringify(rec, null, 1)) + '</pre></details>' : '';
  }
  function renderCheck(r) {
    var d = r.ans && r.ans.data ? r.ans.data : r.ans, h = '<h3>The paper&rsquo;s record</h3>';
    if (!d || d.error) return h + '<p>' + esc(d && d.error || 'Nothing returned.') + '</p>' + receipt(r.rec);
    h += '<table class="mtx trt"><tbody>';
    (d.checks || []).forEach(function (c) {
      var extra = c.title || c.note || (c.links ? c.links.length + ' link(s) read' : '') || '';
      h += '<tr><td>' + esc(c.check) + '</td><td>' + badge(c.outcome) + '</td><td>' + esc(extra).slice(0, 400) + (c.link ? ' <a href="' + esc(c.link) + '" rel="noopener">source</a>' : '') + '</td></tr>';
      (c.links || []).slice(0, 8).forEach(function (l) { h += '<tr><td class="trsub">' + esc(l.url) + '</td><td>' + badge(l.state) + '</td><td></td></tr>'; });
    });
    return h + '</tbody></table>' + receipt(r.rec);
  }
  function renderStats(r) {
    var d = r.ans && r.ans.data ? r.ans.data : r.ans, h = '<h3>Every reported statistic, recomputed</h3>';
    if (!d || d.error) return h + '<p>' + esc(d && d.error || 'Nothing returned.') + '</p>' + receipt(r.rec);
    if (d.outcome === 'CANNOT_TELL') return h + '<p>' + badge('CANNOT_TELL') + ' ' + esc(d.note) + '</p>' + receipt(r.rec);
    h += '<p>' + esc(d.reading) + (d.characters_read ? ' Read ' + Number(d.characters_read).toLocaleString() + ' characters of the paper' + (d.references_cut_characters ? ', references left out' : '') + '.' : '') + '</p>';
    var rows = (d.rows || []);
    if (rows.length) {
      h += '<table class="mtx trt"><thead><tr><th>Quoted</th><th>Stated</th><th>Recomputed</th><th>Outcome</th></tr></thead><tbody>';
      rows.slice(0, 60).forEach(function (x) {
        h += '<tr><td>' + esc(x.quoted) + '</td><td>' + esc(x.stated_p || x.stated || '') + '</td><td>' + esc(x.recomputed_p != null ? x.recomputed_p : (x.recomputed || '')) + '</td><td>' + badge(x.outcome) + (x.reason ? ' <span class="trsub">' + esc(x.reason) + '</span>' : '') + '</td></tr>';
      });
      h += '</tbody></table>' + (rows.length > 60 ? '<p class="trsub">First 60 of ' + rows.length + ' rows shown; rows that are not CONSISTENT come first.</p>' : '');
    }
    return h + receipt(r.rec);
  }
  // 22 Nov 2026: "ibm_fez qubit 5", "ibm_fez q5", "fez q5", "q0, q1 on ibm_kingston", "ibm_kingston 0-3" -> { processor, qubits }.
  // A bare name (fez) becomes ibm_fez. Any word left over that is not a processor, a qubit or a joining word means the input did not parse.
  function parseQubit(v) {
    var t = String(v).toLowerCase().replace(/[;:]/g, ' ').replace(/\s*-\s*/g, '-').trim(), proc = null, qs = [], bad = false;
    t.split(/[\s,]+/).forEach(function (w) {
      if (!w) return;
      var m;
      if (/^ibm_[a-z0-9_]+$/.test(w)) { if (proc) bad = true; proc = w; return; }
      if (/^(qubits?|qs?|on|of|and|the|processor|ibm)$/.test(w)) return;
      if ((m = w.match(/^q?(\d{1,4})(?:-q?(\d{1,4}))?$/))) { qs.push(m[2] != null ? m[1] + '-' + m[2] : m[1]); return; }
      if (/^[a-z]{3,20}$/.test(w) && !proc) { proc = 'ibm_' + w; return; }
      bad = true;
    });
    return bad ? {} : { processor: proc, qubits: qs.join(',') };
  }
  f.addEventListener('submit', function (e) {
    e.preventDefault(); var v = inp.value.trim(); if (!v) return;
    o.hidden = false; o.innerHTML = '<p>Reading&hellip;</p>';
    if (mode() === 'qubit') {   // 18 Nov 2026: qia_measured, IBM's stated figure beside our latest hourly measurement; the page shows the tool's own text
      // 22 Nov 2026: natural wordings ("ibm_fez qubit 5", "ibm_fez q5", "fez q5", "qubits 0-3 on ibm_kingston"). Anything that does not parse,
      // and any answer with no measured line, gets one plain line saying what to type. The tool is never called with no qubits.
      var HOWTO = 'Type a processor and qubits, for example: ibm_fez 5, ibm_fez q5 or ibm_kingston 0-3.';
      var pq = parseQubit(v);
      if (!pq.processor || !pq.qubits) { o.innerHTML = '<p>' + esc(!pq.processor && pq.qubits ? 'Name the processor too. ' + HOWTO : HOWTO) + '</p>'; return; }
      call('qia_measured', { processor: pq.processor, qubits: pq.qubits }).then(function (r) {
        var d = r.ans && r.ans.data ? r.ans.data : r.ans;
        if (!d || d.error) { o.innerHTML = '<p>' + esc((d && d.error) || 'Nothing returned.') + ' ' + HOWTO + '</p>'; return; }
        if (!(d.lines || []).length) {
          var noRun = /no published hourly run/i.test(d.text || '');
          o.innerHTML = '<p>' + esc(noRun ? 'No hourly runs are published for ' + pq.processor + '. ' + HOWTO : 'No hourly measurement of qubit ' + pq.qubits + ' on ' + pq.processor + ' is published. ' + HOWTO) + '</p>' + receipt(r.rec);
          return;
        }
        o.innerHTML = '<h3>Stated against measured</h3><pre class="tryjson">' + esc(d.text || '') + '</pre>' + receipt(r.rec);
      }).catch(function (err) { o.innerHTML = '<p>Could not reach the server: ' + esc(err.message || err) + '</p>'; });
      return;
    }
    if (mode() !== 'paper') {
      call('check_reported_statistics', { text: v }).then(function (r) { o.innerHTML = renderStats(r); }).catch(function (err) { o.innerHTML = '<p>Could not reach the server: ' + esc(err.message || err) + '</p>'; });
      return;
    }
    var isArxiv = /(^|arxiv[:/.\s]|abs\/)\d{4}\.\d{4,5}/i.test(v) || /^\d{4}\.\d{4,5}(v\d+)?$/.test(v);
    var jobs = [call('paper_check', { id: v }).then(renderCheck)];
    if (isArxiv) jobs.push(call('paper_statistics', { id: v }).then(renderStats));
    Promise.all(jobs.map(function (p) { return p.catch(function (err) { return '<p>Could not reach the server: ' + esc(err.message || err) + '</p>'; }); }))
      .then(function (parts) { o.innerHTML = parts.join('') + (isArxiv ? '' : '<p class="trsub">The whole-paper statistics check reads arXiv&rsquo;s full text, so it runs on arXiv ids.</p>'); });
  });
})();
