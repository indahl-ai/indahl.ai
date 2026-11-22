// Division pages: fills each desk's current reading from /headlines.json (watch/headlines.py, the same live feed headline.js reads).
// 21 Nov 2026: was /stack/live.json, gone with the STACK desk. A desk is keyed by its link's path (/water -> water, /iris/lab -> iris/lab);
// a desk with no headline entry stays empty.
(function () {
  var slots = document.querySelectorAll('.deskread'); if (!slots.length) return;
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function plain(s) { return String(s || '').replace(/\b(CANNOT|NOTHING|STRADDLES)_(TELL|RETURNED|EDGE)\b/g, '$1 $2'); }
  function when(s) { var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s || ''); return m ? ' Read ' + (+m[3]) + ' ' + MON[+m[2] - 1] + ' ' + m[1] + '.' : ''; }
  function first(s) { var m = /^(.*?[.!?])(\s|$)/.exec(s || ''); return m ? m[1] : (s || ''); }
  fetch('/headlines.json', { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
    var pages = (d && d.pages) || {};
    slots.forEach(function (el) {
      var a = el.parentNode && el.parentNode.querySelector('a[href]'), key = a ? a.getAttribute('href').replace(/^https?:\/\/(www\.)?indahl\.ai/, '').replace(/^\/+|\/+$/g, '') : '';
      var h = key && pages[key]; if (!h) { el.textContent = ''; return; }
      var t = h.reading ? h.reading : (h.big ? h.big + ' ' + first(h.line) : first(h.line));
      el.textContent = t ? plain(t) + when(h.as_of) : '';
    });
  }).catch(function () {});
})();
