// qubit.js (23 Nov 2026: "check a qubit live" on the QIA overview). The qubit half of the indahl.ai Test Drive:
// IBM's stated figure for a qubit beside our latest hourly hardware measurement of it, with the run's job ID and time.
// It calls the same qia_measured tool as indahl.ai/try, through this site's /qubit route (worker.js forwards only that tool).
(function () {
  var f = document.getElementById('qubit-form'); if (!f) return;
  var inp = document.getElementById('qubit-in'), o = document.getElementById('qubit-out');
  var HOWTO = 'Type a processor and qubits, for example: ibm_fez 5, ibm_fez q5 or ibm_kingston 0-3.';
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
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
  function linkify(s) { return esc(s).replace(/https:\/\/indahl\.ai\/qia\/cal\/[A-Za-z0-9]+\.json/g, function (u) { return '<a href="' + u + '">' + u + '</a>'; }); }
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var pq = parseQubit(inp.value);
    if (!pq.processor || !pq.qubits) { o.innerHTML = '<p>' + esc(!pq.processor && pq.qubits ? 'Name the processor too. ' + HOWTO : HOWTO) + '</p>'; return; }
    o.innerHTML = '<p>Reading ' + esc(pq.processor) + ' qubit ' + esc(pq.qubits) + '...</p>';
    fetch('/qubit', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ processor: pq.processor, qubits: pq.qubits }) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var c = (j.result && j.result.content) || [], ans = null;
        try { ans = JSON.parse(c[0].text); } catch (err) { ans = null; }
        var d = ans && ans.data ? ans.data : ans;
        if (!d || d.error) { o.innerHTML = '<p>' + esc((d && d.error) || 'Nothing returned.') + ' ' + HOWTO + '</p>'; return; }
        if (!(d.lines || []).length) {
          var noRun = /no published hourly run/i.test(d.text || '');
          o.innerHTML = '<p>' + esc(noRun ? 'No hourly runs are published for ' + pq.processor + '. ' + HOWTO : 'No hourly measurement of qubit ' + pq.qubits + ' on ' + pq.processor + ' is published. ' + HOWTO) + '</p>';
          return;
        }
        o.innerHTML = '<div class="qia-qubit-text">' + String(d.text || '').split('\n').map(function (l) { return '<p>' + linkify(l) + '</p>'; }).join('') + '</div>';
      })
      .catch(function (err) { o.innerHTML = '<p>Could not reach the server: ' + esc(err.message || err) + '</p>'; });
  });
})();
