// listrows.js -- 17 Nov 2026, the owner: one public list per desk; no study-list downloads (a copy already downloaded keeps a removed
// study on). The /qia/list page no longer downloads the whole List: its script (public/qia/list.js) asks GET /qia/list/rows for one page
// at a time, with the same search, code filter, month filter and #anchor jump it had. The rows come from public/_studies/qia.json, read
// through the ASSETS binding (worker.js refuses any public request for /_studies/). build_site.py writes that file from the List record,
// filtered by indahl-ai/removed_by_author.json.
export const PER = 50;
const byCode = (a, b) => a.localeCompare(b, undefined, { numeric: true });

// Pure: rows (the List studies) and params -> one page. Same rules as the 16 Nov list.js filter.
export function pageRows(rows, p) {
  const w = String(p.q || '').trim().toLowerCase().slice(0, 200), c = String(p.code || ''), y = String(p.month || '');
  const match = s => {
    if (c === '—' ? (s.codes && s.codes.length) : (c && (s.codes || []).indexOf(c) < 0)) return false;
    if (y && String(s.indexed || '').slice(0, 7) !== y) return false;
    if (!w) return true;
    return (s.study + ' ' + JSON.stringify(s.basis || {}) + ' ' + (s.version || '')).toLowerCase().indexOf(w) > -1;
  };
  let view = rows.filter(match), reset = false, page = Math.max(0, parseInt(p.page, 10) || 0);
  if (p.anchor) {   // a link to #<anchor> opens the page that holds that row; if the filters hide it, they are cleared
    let i = view.findIndex(s => s.anchor === p.anchor);
    if (i < 0) { i = rows.findIndex(s => s.anchor === p.anchor); if (i > -1) { view = rows; reset = true; } }
    if (i > -1) page = Math.floor(i / PER);
  }
  const last = Math.max(0, Math.ceil(view.length / PER) - 1); page = Math.min(page, last);
  const codes = {}, months = {};
  rows.forEach(s => { (s.codes || []).forEach(x => { codes[x] = 1; }); const m = String(s.indexed || '').slice(0, 7); if (m) months[m] = 1; });
  return { total: rows.length, matched: view.length, page, per: PER, reset, rows: view.slice(page * PER, page * PER + PER),
           codes: Object.keys(codes).sort(byCode), months: Object.keys(months).sort() };
}

let cache = null, cacheAt = 0;
export async function handleListRows(req, env, u) {
  if (req.method !== 'GET') return new Response('Method not allowed', { status: 405 });
  if (!cache || Date.now() - cacheAt > 300000) {
    const r = await env.ASSETS.fetch(new Request(new URL('/_studies/qia.json', req.url)));
    if (!r.ok) return new Response(JSON.stringify({ error: 'list unavailable' }), { status: 503, headers: { 'content-type': 'application/json' } });
    cache = ((await r.json()).studies) || []; cacheAt = Date.now();
  }
  const q = u.searchParams, out = pageRows(cache, { q: q.get('q'), code: q.get('code'), month: q.get('month'), page: q.get('page'), anchor: q.get('anchor') });
  return new Response(JSON.stringify(out), { headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'public, max-age=300', 'x-robots-tag': 'noindex' } });
}
