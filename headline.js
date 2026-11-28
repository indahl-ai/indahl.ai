// Headlines: the page's headline number, and on the home page the strongest ones, from /headlines.json (built from the live feeds).
(function () {
  var path = location.pathname.replace(/\/+$/, '') || '/';
  function esc(s) { var d = document.createElement('div'); d.textContent = String(s == null ? '' : s).replace(/\b(CANNOT|NOTHING|STRADDLES)_(TELL|RETURNED|EDGE)\b/g, '$1 $2'); return d.innerHTML; }   // 16 Nov 2026: outcome words without underscores in reader text
  function table(t) {   // 29 Oct 2026: a headline may carry a small table (QIA: every processor's queue)
    if (!t) return ''; var th = t.cols.map(function (c, i) { return '<th' + (i ? ' class="r"' : '') + '>' + esc(c) + '</th>'; }).join('');
    function row(r, tag) { return '<tr>' + r.map(function (c, i) { return '<' + tag + (i === 1 ? ' class="n"' : i > 1 ? ' class="w"' : '') + '>' + esc(c) + '</' + tag + '>'; }).join('') + '</tr>'; }
    return '<table class="hl-tab"><thead><tr>' + th + '</tr></thead><tbody>' + t.rows.map(function (r) { return row(r, 'td'); }).join('') + '</tbody>' + (t.foot ? '<tfoot>' + row(t.foot, 'td') + '</tfoot>' : '') + '</table>' + (t.note ? '<p class="hl-tnote">' + esc(t.note) + '</p>' : '') + (t.cta ? '<p class="hl-cta"><a href="' + esc(t.cta.href) + '">' + esc(t.cta.text) + '</a>' + esc(t.cta.rest || '') + (t.cta.href2 ? '<a href="' + esc(t.cta.href2) + '">' + esc(t.cta.link2) + '</a>' + esc(t.cta.tail || '') : '') + '</p>' : '');
  }
  // 15 Nov 2026: a page can name where the headline's table goes (#hl-table-here), so inputs sit right under the headline and the table below them
  // 21 Nov 2026 (HS, site/HEADLINE_SPLIT.md, credit the referee): an entry with a short reading draws it under the big figure, the method under that with the
  // time of the reading in UTC, and the long line as the full reading below. An entry without one draws the long line as before. Same markup as build_site.py _hlbody.
  var MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  function when(s) { var m = /^(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2}))?/.exec(s || ''); return m ? ' Last read ' + (+m[3]) + ' ' + MON[+m[2] - 1] + ' ' + m[1] + (m[4] ? ', ' + m[4] + ':' + m[5] + ' UTC' : '') + '.' : ''; }
  function lines(h) { return h.reading ? '<p class="hl-line hl-reading">' + esc(h.reading) + '</p><p class="hl-method">' + esc((h.method || '') + when(h.as_of)) + '</p><details class="hl-full"><summary>Full reading</summary><p>' + esc(/^[a-z]/.test(h.line || '') ? h.big + ' ' + h.line : h.line) + '</p></details>' : '<p class="hl-line">' + esc(h.line) + '</p>'; }
  function block(h) { var dest = document.getElementById('hl-table-here'); if (dest && h.table) { dest.innerHTML = table(h.table); return '<div class="hl-big">' + esc(h.big) + '</div>' + lines(h); } return '<div class="hl-big">' + esc(h.big) + '</div>' + lines(h) + table(h.table); }
  // 29 Oct 2026: the receipt line. Says only that the feed behind the number was hashed onto the tape at an entry (TAPE PLAN Addendum 3).
  function receipt(box, slug) {
    fetch('/tape/live.json', { cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (t) {
      var f = t.feeds && t.feeds[slug]; if (!f || box.querySelector('.hl-receipt')) return;
      var p = document.createElement('p'); p.className = 'hl-receipt'; p.appendChild(document.createTextNode('Receipt: the feed behind this number was hashed onto the tape at entry ' + f.n + ', ' + f.hash.slice(0, 10) + '\u2026 '));
      var a = document.createElement('a'); a.href = '/tape'; a.textContent = 'See the tape'; p.appendChild(a); p.appendChild(document.createTextNode('.')); box.appendChild(p);
    }).catch(function () {});
  }
  function run() {
    // 28 Nov 2026 (owner: the /qia readings flashed and were painted over): a page that ships its own headline block marks it data-hl-fixed,
    // and this script leaves that page alone (no fill, no replace, no inserted headline).
    if (document.querySelector('[data-hl-fixed]')) return;
    fetch('/headlines.json', { cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (d) {
      var pages = d.pages || {}, main = document.querySelector('main.wrap'); if (!main) return;
      var slot = document.getElementById('hl-slot');
      var old = slot ? null : document.querySelector('.hl, .hlgrid'); if (old) old.parentNode.removeChild(old);
      function fill(cls, html) { if (slot) { slot.className = 'hl-slot ' + cls + (slot.className.indexOf('hl-home') > -1 ? ' hl-home' : ''); slot.removeAttribute('aria-hidden'); slot.innerHTML = html; return slot; } var e = document.createElement('section'); e.className = cls; e.innerHTML = html; main.insertBefore(e, main.firstChild); return e; }
      if (path === '/') {
        var list = (d.home || []).filter(function (s) { return pages[s]; }); if (!list.length) return;
        fill('hlgrid', list.map(function (s) { var h = pages[s]; var src = h.reading || h.line; var m = /^(.*?[.!?])(\s+.+)$/.exec(src || ''); var line = m ? esc(m[1]) + '<span class="hl-rest">' + esc(m[2]) + '</span>' : esc(src); return '<a class="hlcard" href="' + esc(h.href) + '"><div class="hl-big">' + esc(h.big) + '</div><p class="hl-line">' + line + '</p><span class="hl-more">' + esc(s.toUpperCase()) + '</span></a>'; }).join(''));
      } else {
        var slug = path.slice(1); if (!pages[slug]) { slug = path.split('/')[1]; if (path.split('/').length > 2) return; } if (path === '/hermes/model') return; var h = pages[slug]; if (!h) return;   // 11 Nov 2026: a headline keyed by a full path (iris/lab) serves that page
        var hs = fill('hl', block(h)); receipt(hs, slug);
      }
    }).catch(function () {});
  }
  run(); setInterval(run, 120000);   // 21 Nov 2026: the STACK picker (/stack/live.json) went with the STACK desk
})();
