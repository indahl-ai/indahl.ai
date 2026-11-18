// QIA List: search, filters and pages (16 Nov 2026, teardown #6). The page ships its first 50 rows; this script takes over the table.
// 17 Nov 2026, the owner: one public list per desk; no study-list downloads. The script no longer fetches the whole List: it asks the
// worker for one page at a time, GET /qia/list/rows?q=&code=&month=&page=&anchor= (indahl-ai/listrows.js). A link to #<anchor> opens the
// page that holds that row.
(function () {
  var tb = document.querySelector('table.mtx.list tbody'), ctl = document.getElementById('ql-ctl');
  if (!tb || !ctl || !window.fetch) return;
  // 17 Nov 2026: paging state lives in load() below (the server returns one page)
  function el(t, c, x) { var e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function link(href, text) { var a = el('a', null, text); a.href = href; return a; }
  function codeA(c) { var a = link('/qia/key#' + c, c); a.className = 'code'; return a; }
  function row(s) {
    var tr = el('tr'); tr.id = s.anchor;
    var t1 = el('td'); t1.appendChild(link(s.link, s.study)); tr.appendChild(t1);
    var t2 = el('td'); if (s.codes && s.codes.length) s.codes.forEach(function (c, i) { if (i) t2.appendChild(document.createTextNode(' ')); t2.appendChild(codeA(c)); }); else t2.textContent = '—'; tr.appendChild(t2);
    tr.appendChild(el('td', null, s.indexed || ''));
    var t4 = el('td'), d = el('details'), sm = el('summary', null, 'receipt'), ul = el('ul');
    d.appendChild(sm);
    ul.appendChild(el('li', null, 'Read: ' + (s.read || '') + (s.version ? ', version ' + s.version : '') + ', indexed ' + (s.indexed_note || s.indexed || '')));
    Object.keys(s.basis || {}).forEach(function (c) { (s.basis[c] || []).forEach(function (b) { var li = el('li'); li.appendChild(codeA(c)); li.appendChild(document.createTextNode(' ' + b)); ul.appendChild(li); }); });
    if (s.calibrated) ul.appendChild(el('li', null, 'Calibrated: see the QIA page'));
    d.appendChild(ul); t4.appendChild(d); tr.appendChild(t4); return tr;
  }
  var q = el('input'); q.type = 'search'; q.placeholder = 'Search titles and notes'; q.setAttribute('aria-label', 'Search the List');
  var code = el('select'); code.setAttribute('aria-label', 'Filter by code');
  var year = el('select'); year.setAttribute('aria-label', 'Filter by indexed month');
  var info = el('p', 'meta'), nav = el('p', 'ql-nav');
  var prev = el('button', 'btn ghost', 'Previous'), next = el('button', 'btn ghost', 'Next'); prev.type = next.type = 'button';
  nav.appendChild(prev); nav.appendChild(document.createTextNode(' ')); nav.appendChild(next);
  ctl.textContent = ''; [q, code, year].forEach(function (x) { ctl.appendChild(x); ctl.appendChild(document.createTextNode(' ')); }); ctl.appendChild(info);
  var tbl = tb.closest('table'); tbl.parentNode.parentNode.insertBefore(nav, tbl.parentNode.nextSibling);
  var cur = null, seq = 0, timer = null;
  function show(d) {
    cur = d; tb.textContent = ''; d.rows.forEach(function (s) { tb.appendChild(row(s)); });
    var a = d.page * d.per, b = a + d.rows.length;
    info.textContent = d.matched ? 'Rows ' + (a + 1) + ' to ' + b + ' of ' + d.matched + (d.matched !== d.total ? ' (filtered from ' + d.total + ')' : '') + '.' : 'No row matches.';
    prev.disabled = d.page === 0; next.disabled = b >= d.matched;
  }
  function options(d) {
    if (code.options.length) return;
    code.appendChild(new Option('All codes', '')); d.codes.forEach(function (c) { code.appendChild(new Option(c, c)); }); code.appendChild(new Option('— (no code)', '—'));
    year.appendChild(new Option('Any indexed month', '')); d.months.forEach(function (m) { year.appendChild(new Option(m, m)); });
  }
  function load(pg, anchor, then) {
    var n = ++seq, p = new URLSearchParams({ q: q.value.trim(), code: code.value, month: year.value, page: String(pg || 0) });
    if (anchor) p.set('anchor', anchor);
    fetch('/qia/list/rows?' + p.toString()).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (d) {
      if (n !== seq) return;
      options(d); if (d.reset) { q.value = ''; code.value = ''; year.value = ''; }
      show(d); if (then) then();
    }).catch(function () { if (n === seq) info.textContent = 'Search is not available just now; the first rows are shown.'; });
  }
  function soon() { clearTimeout(timer); timer = setTimeout(function () { load(0); }, 250); }
  q.addEventListener('input', soon); code.addEventListener('change', function () { load(0); }); year.addEventListener('change', function () { load(0); });
  prev.onclick = function () { if (cur && cur.page > 0) load(cur.page - 1, null, function () { tbl.scrollIntoView(); }); };
  next.onclick = function () { if (cur && (cur.page + 1) * cur.per < cur.matched) load(cur.page + 1, null, function () { tbl.scrollIntoView(); }); };
  function jump() {
    var h = decodeURIComponent((location.hash || '').slice(1)); if (!h) return;
    load(0, h, function () { var r = document.getElementById(h); if (r) { r.scrollIntoView(); r.classList.add('ql-hit'); } });
  }
  if (location.hash) jump(); else load(0);
  window.addEventListener('hashchange', jump);
})();
