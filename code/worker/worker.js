// indahl.ai worker (Heuremen LLC). Serves indahl.ai and its MTA-STS host. Built from the private source by kibble/worker-clean/clean_worker.py.
import { PAGES as INDAHL_PAGES, STYLE as INDAHL_CSS, OY_FILES, NDA, PRIVACY, GATE_JS, FEED, BUILT, LASTMOD, LLMS, SITEMAP } from "../../indahl-ai/pages.js";
import * as GATE from "../../indahl-ai/gate.js";
import { handleInquiry } from "../../indahl-ai/inquire.js";
import { handleIndexRequest } from "../../indahl-ai/indexreq.js";
import { handleResponse } from "../../indahl-ai/respondreq.js";
import { handleCorrection } from "../../indahl-ai/correctreq.js";
import { messagePage, formTitle } from "../../indahl-ai/security.js";   // 22 Nov 2026: form answers carry their own title (they read "Inquiry received" on errors)
import { handleApi } from "../../indahl-ai/api.js";
import { handleListRows } from "../../indahl-ai/listrows.js";   // 17 Nov 2026, owner: one public list per desk; no study-list downloads (a copy already downloaded keeps a removed study on).
import { handleWeekly } from "../../indahl-ai/newsletter.js";
import { handleAlerts } from "../../indahl-ai/alerts.js";
import { handleNotify } from "../../indahl-ai/notify.js";
import { handleSecurity, finalize as secFinalize, decorate as secDecorate, mtaSts } from "../../indahl-ai/security.js";
import { render as renderDesk, check as checkDesk } from "./desk_template.js";   // 22 Nov 2026 (pagebuilder step 1): the one desk template, preview route /_edge/<id>/ only
import { DESKS_LIVE } from "../../indahl-ai/desks_live.js";
const DESK_IDS = new Set(DESKS_LIVE.map((d) => d.id));   // written by build_site.py from ledger/desks.json on every build, so a stray KV key cannot make a page
const EDGE_H = { "content-type": "text/html; charset=utf-8", "x-robots-tag": "noindex", "cache-control": "public, max-age=60", "tdm-reservation": "1", "tdm-policy": "https://indahl.ai/terms#ai-training", "x-content-type-options": "nosniff", "referrer-policy": "strict-origin-when-cross-origin", "strict-transport-security": "max-age=31536000", "x-frame-options": "DENY", "permissions-policy": "camera=(), microphone=(), geolocation=()", "content-security-policy": "default-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data:; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'" };
// /_edge/<id>/: the desk/1 doc in KV desk_<id> (cacheTtl 60), check()ed, rendered by desk_template.js, cached by url + hash. On any failure:
// the last good render (stale cache), else a plain 503 page with no numbers. Every fallback writes one log line. noindex, linked from nowhere.
async function edgeDesk(env, id) {
  const cache = caches.default, last = new Request("https://indahl.ai/_edge/" + id + "/?last=1");
  let cause;
  try {
    const doc = await env.IRIS_BENCH.get("desk_" + id, { type: "json", cacheTtl: 60 });
    if (!doc) throw new Error("no desk_" + id + " in KV");
    const bad = checkDesk(doc, id);
    if (bad.length) throw new Error("desk/1 check: " + bad.join("; "));
    const key = new Request("https://indahl.ai/_edge/" + id + "/?h=" + doc.hash), hit = await cache.match(key);
    if (hit) return new Response(hit.body, { headers: EDGE_H });
    const html = renderDesk(doc);
    await cache.put(key, new Response(html, { headers: { ...EDGE_H, "cache-control": "public, s-maxage=300" } }));
    await cache.put(last, new Response(html, { headers: { ...EDGE_H, "cache-control": "public, s-maxage=2592000" } }));
    return new Response(html, { headers: EDGE_H });
  } catch (e) { cause = String((e && e.message) || e).slice(0, 300); }
  console.log(JSON.stringify({ edge_fallback: id, cause }));
  const stale = await cache.match(last).catch(() => null);
  if (stale) return new Response(stale.body, { headers: { ...EDGE_H, "x-edge-fallback": "stale" } });
  return new Response('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>Desk page unavailable | indahl.ai</title><body style="font-family:system-ui;max-width:40rem;margin:4rem auto;padding:0 1rem"><h1>This desk page is unavailable</h1><p>Please try again later. <a href="https://indahl.ai/">indahl.ai</a></p>', { status: 503, headers: { ...EDGE_H, "cache-control": "no-store", "retry-after": "60" } });
}
const FAVICON_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" rx="28" fill="#1a1208"/><polygon points="100,36 176,168 24,168" fill="none" stroke="#c9a84c" stroke-width="14" stroke-linejoin="round"/></svg>';
const PDFS = ["/faults.pdf", "/guards.pdf", "/quantum-idle-audit.pdf"];
const MOVED = { "/las-fallas.pdf": "/faults.pdf", "/las-guardas.pdf": "/guards.pdf", "/qia/study/zenodo-19855345": "/qia/study/zenodo-24287983", "/record": "/qia/list", "/record/": "/qia/list", "/record.json": "/qia/list", "/record.html": "/qia/list" };   // 17 Nov 2026: study listed at its version 2 (zenodo:24287983). 17 Nov 2026: /record retired, a frozen duplicate of the QIA List
const IMMUTABLE = "public, max-age=31536000, immutable";
function cachePolicy(req, r) {
  const u = new URL(req.url);
  if (u.hostname !== "indahl.ai" && u.hostname !== "www.indahl.ai") return r;
  if (r.status !== 200 || req.method !== "GET" && req.method !== "HEAD") return r;
  const p = u.pathname, v = /^[0-9a-f]{8,64}$/.test(u.searchParams.get("v") || "");
  let cc = null;
  if (/\/live\.json$/.test(p)) cc = "public, max-age=60";
  else if (/\.zip$/.test(p)) cc = v ? IMMUTABLE : "public, max-age=3600";
  else if (/^\/og\/[a-z0-9-]+\.png$/.test(p)) cc = v ? IMMUTABLE : "public, max-age=3600";
  else if (/\.(js|css)$/.test(p) && v && p !== "/sw.js") cc = IMMUTABLE;
  if (!cc) return r;
  const h = new Headers(r.headers);
  h.set("cache-control", cc);
  return new Response(r.body, { status: r.status, statusText: r.statusText, headers: h });
}
var cut_default = {
  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    const mr = mtaSts(req, u.hostname, u);
    if (mr) return mr;
    // 23 Nov 2026 (the designer review #7): live.json answers are held at the edge for 60 s (they were a worker run and a KV read per request; the
    // max-age=60 only helped browsers). Security decoration still runs on every answer, hit or miss.
    const lj = req.method === "GET" && (u.hostname === "indahl.ai" || u.hostname === "www.indahl.ai") && /\/live\.json$/.test(u.pathname);
    let r = null;
    const ljKey = lj ? new Request(u.origin + u.pathname) : null;   // 23 Nov 2026 (the designer round 2 #10): one cache entry per feed, whatever the query string
    if (lj) { const hit = await caches.default.match(ljKey).catch(() => null); if (hit) { r = new Response(hit.body, hit); r.headers.set("x-edge-cache", "hit"); } }
    if (!r) {
      r = cachePolicy(req, await handle(req, env));
      if (lj && r.status === 200 && !r.headers.has("set-cookie")) {
        const h = new Headers(r.headers); h.set("cache-control", "public, max-age=60, s-maxage=60");
        const c = r.clone(); const put = caches.default.put(ljKey, new Response(c.body, { status: 200, headers: h })).catch(() => null); if (ctx && ctx.waitUntil) ctx.waitUntil(put); else await put;
      }
    }
    if (u.hostname === "indahl.ai" || u.hostname === "www.indahl.ai" || env.STAGING === "1" && u.hostname === "localhost") r = await secFinalize(req, env, await secDecorate(req, u, r));
    return r;
  }
};
async function handle(req, env) {
  {
    if (env.STAGING === "1" && new URL(req.url).hostname === "localhost") {
      const lu = new URL(req.url);
      lu.protocol = "https:";
      lu.hostname = "indahl.ai";
      lu.port = "";
      req = new Request(lu, req);
    }
    const u = new URL(req.url), host = u.hostname, ip = req.headers.get("CF-Connecting-IP") || "";
    // 17 Nov 2026: quantumidleaudit.com, the Quantum Idle Audit business site (indahl-ai/qia_site.py builds public/_qiasite/)
    if (host === "quantumidleaudit.com" || host === "www.quantumidleaudit.com") {
      if (host === "www.quantumidleaudit.com" || u.protocol === "http:") return Response.redirect("https://quantumidleaudit.com" + u.pathname + u.search, 301);
      const QS = { "/": "/_qiasite/", "/check_run.js": "/_qiasite/check_run.js", "/carry_result.js": "/_qiasite/carry_result.js", "/console.css": "/_qiasite/console.css", "/heuremen-mark-mono-light.svg": "/_qiasite/heuremen-mark-mono-light.svg", "/services": "/_qiasite/services", "/method": "/_qiasite/method", "/listed": "/_qiasite/listed", "/robots.txt": "/_qiasite/robots.txt", "/sitemap.xml": "/_qiasite/sitemap.xml", "/favicon.svg": "/_qiasite/favicon.svg", "/qia-2026-002-cover.jpg": "/_qiasite/qia-2026-002-cover.jpg", "/qia-2026-002.pdf": "/_qiasite/qia-2026-002.pdf" };
      const p = /\.(jpg|svg|txt|xml|pdf)$/.test(u.pathname) ? u.pathname : (u.pathname.replace(/\.html$/, "").replace(/\/+$/, "") || "/");
      // 18 Nov 2026 (owner: "put a key on it"): /plan is the team's working plan; served only with the key (?k= once, then a cookie)
      if (p === "/plan") return new Response("Not found", { status: 404, headers: { "cache-control": "no-store" } });  // 18 Nov 2026: plan is local only
      // 17 Nov 2026 (owner: no manual steps): any page qia_site.py builds is served without a worker edit; unknown paths go home
      if (/^\/qia\/(runcheck\.js|cal\.json|offchain\.json|records\/[A-Za-z0-9._\/-]+|cal\/[A-Za-z0-9._-]+\.json)$/.test(p)) { const q = await env.ASSETS.fetch(new Request(new URL(p, "https://indahl.ai").toString(), req)); if (q.status === 200) { const qh = new Headers(q.headers); qh.set("cache-control", "public, max-age=300"); return new Response(q.body, { status: 200, headers: qh }); } const q2 = await cut_default.fetch(new Request("https://indahl.ai" + p, { method: "GET", headers: req.headers }), env); if (q2.status === 200) { const qh2 = new Headers(q2.headers); qh2.set("cache-control", "public, max-age=300"); return new Response(q2.body, { status: 200, headers: qh2 }); } }   // not a static asset there (served by the indahl.ai side of this worker): ask indahl.ai itself   // 21 Nov 2026: "Check a run" on quantumidleaudit.com reads the same live QIA data as indahl.ai (same assets, no copy)
      if (!QS[p] && /^\/[a-z0-9-]+$/.test(p)) { const g = await env.ASSETS.fetch(new Request(new URL("/_qiasite" + p, "https://quantumidleaudit.com").toString(), req)); if (g.status === 200) return g; }
      if (!QS[p]) return new Response('<!doctype html><meta charset="utf-8"><title>Not found | Quantum Idle Audit</title><meta name="robots" content="noindex"><body style="font-family:system-ui;max-width:40rem;margin:4rem auto;padding:0 1rem"><h1>Page not found</h1><p><a href="https://quantumidleaudit.com/">Quantum Idle Audit home</a></p>', { status: 404, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });   // 18 Nov 2026: a missing page is a 404, not a redirect
      const r = await env.ASSETS.fetch(new Request(new URL(QS[p], "https://quantumidleaudit.com").toString(), req));
      const h = new Headers(r.headers); h.set("cache-control", "public, max-age=300"); h.set("x-robots-tag", "all"); h.set("tdm-reservation", "1"); h.set("tdm-policy", "https://indahl.ai/terms#ai-training");   // 21 Nov 2026: the same AI-training reservation indahl.ai carries
      return new Response(r.body, { status: r.status, headers: h });
    }
    if (u.pathname.startsWith("/_qiasite")) return new Response("Not found", { status: 404 });
    // 17 Nov 2026, owner: one public list per desk; no study-list downloads (a copy already downloaded keeps a removed study on).
    // /_studies/ holds the List data the MCP tools and the /qia/list search read through env.ASSETS; it is never served. The old list files and list packs are gone.
    if (/^\/_studies(\/|$)/.test(u.pathname) || /^\/(qia|iris|sagar)\/list\.(json|csv)$/.test(u.pathname) || /^\/(qia|iris)\/\1-list-pack(\.zip(\.sha256)?|-LICENSE\.txt)$/.test(u.pathname)) return new Response("Not found", { status: 404, headers: { "content-type": "text/plain", "x-robots-tag": "noindex" } });
    if (u.pathname === "/__time") return new Response(JSON.stringify({ t: Date.now() }), { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    if ((host === "indahl.ai" || host === "www.indahl.ai") && (host === "www.indahl.ai" || u.protocol === "http:")) return Response.redirect("https://indahl.ai" + u.pathname + u.search, 301);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && MOVED[u.pathname]) return Response.redirect("https://indahl.ai" + MOVED[u.pathname], 301);
    { const em = host === "indahl.ai" && (req.method === "GET" || req.method === "HEAD") && /^\/_edge\/([a-z0-9-]{1,40})\/?$/.exec(u.pathname); if (em && DESK_IDS.has(em[1]) && env.IRIS_BENCH) return edgeDesk(env, em[1]); }   // 22 Nov 2026: desk pages at the edge, preview only (pagebuilder); public desk routes unchanged
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/list/rows" && env.ASSETS) return handleListRows(req, env, u);   // 17 Nov 2026, owner: one public list per desk; no study-list downloads (a copy already downloaded keeps a removed study on). One page of the List for its search
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/quantum-idle-audit.pdf" && env.ASSETS) return env.ASSETS.fetch(req);
    {
      const bm = (host === "indahl.ai" || host === "www.indahl.ai") && /^\/iris\/bench([2-9]|1[01])?\.json$/.exec(u.pathname);
      if (bm && env.IRIS_BENCH) {
        const v = await env.IRIS_BENCH.get("status" + (bm[1] || ""));
        return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
      }
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/bench-results.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("results");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/bench.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/train.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/lab-live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/yo.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && (u.pathname === "/mcp" || u.pathname.startsWith("/mcp/") || u.pathname.startsWith("/api/") || u.pathname === "/.well-known/mcp.json" || u.pathname === "/.well-known/mcp/server-card.json")) {
      const ar = await handleApi(req, env, u);
      if (ar) return ar;
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/lab/live.json" && env.IRIS_BENCH) {
      return new Response("Gone", { status: 410, headers: { "content-type": "text/plain", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/lab/stan.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/lab/stan.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("stan_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store", "x-content-type-options": "nosniff" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("iris_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/forecast/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/forecast/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("forecast_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/cadence/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/petrol/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("petrol_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/cadence/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("cadence_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/trials/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/trials/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("trials_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/launch/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/launch/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("launch_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/water/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/water/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("water_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && /^\/social\/(summary|dsa|dsa_summary|dsa_automation_monthly|adspend|bluesky)\.json$/.test(u.pathname) && env.ASSETS) return env.ASSETS.fetch(req);
    // 22 Nov 2026: /brand/entities.json and /brand/search.js route removed (brand pages killed 20 Nov, no files behind it).
    if ((host === "indahl.ai" || host === "www.indahl.ai") && /^\/e\/(index\.json|search\.js)$/.test(u.pathname) && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/solar/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("solar_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/deus/live.json" && env.IRIS_BENCH) {   // 22 Nov 2026: DEUS (HERMES)
      const v = await env.IRIS_BENCH.get("deus_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/ares/live.json" && env.IRIS_BENCH) {   // 22 Nov 2026: ARES (HERMES)
      const v = await env.IRIS_BENCH.get("ares_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/argus/live.json" && env.IRIS_BENCH) {   // 22 Nov 2026: ARGUS (HERMES)
      const v = await env.IRIS_BENCH.get("argus_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/zeus/live.json" && env.IRIS_BENCH) {   // 22 Nov 2026: ZEUS (HERMES)
      const v = await env.IRIS_BENCH.get("zeus_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/seldon/live.json" && env.IRIS_BENCH) {   // 22 Nov 2026: SELDON (HERMES)
      const v = await env.IRIS_BENCH.get("seldon_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/tornado/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("tornado_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/cassandra/live.json" && env.IRIS_BENCH) {   // 21 Nov 2026: CASSANDRA (HERMES)
      const v = await env.IRIS_BENCH.get("cassandra_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/prometheus/live.json" && env.IRIS_BENCH) {   // 21 Nov 2026: PROMETHEUS (HERMES)
      const v = await env.IRIS_BENCH.get("prometheus_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/voightkampff/live.json" && env.IRIS_BENCH) {   // 21 Nov 2026: VOIGHT-KAMPFF (HERMES)
      const v = await env.IRIS_BENCH.get("voightkampff_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/credit/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("credit_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/flu/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("flu_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/steo/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("steo_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/seasonal/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("seasonal_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/neo/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("neo_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/census/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("census_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/quake/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("quake_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/cone/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("cone_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/rank/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("rank_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/wiki/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("wiki_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/social/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("social_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/predictions/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("predictions_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && /^\/predictions\/(stamps\.json|fortune\.json|stamps\/log_[0-9a-f]{16}\.jsonl\.ots)$/.test(u.pathname) && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/audit.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/yo.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/yo.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("yo_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/audit.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("qia_audit");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/stability.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/runcheck.js" && env.ASSETS) return env.ASSETS.fetch(req);
    {
      const rm = (host === "indahl.ai" || host === "www.indahl.ai") && /^\/qia\/records\/(index|ibm_[a-z0-9_]+\/(manifest|\d{4}-\d\d-\d\d))\.json$/.exec(u.pathname);
      if (rm && env.IRIS_BENCH) {
        const v = await env.IRIS_BENCH.get("qia_rc" + u.pathname.slice("/qia/records".length));
        return new Response(v || "{}", { status: v ? 200 : 404, headers: { "content-type": "application/json", "cache-control": "public, max-age=300", "x-content-type-options": "nosniff" } });
      }
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/stability.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("qia_stability");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/probe.py" && env.ASSETS) {
      const r = await env.ASSETS.fetch(req);
      return new Response(r.body, { status: r.status, headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "public, max-age=300", "content-disposition": 'inline; filename="probe.py"' } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/queue.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/queue.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("qia_queue");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/t1t2.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/t1t2.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("qia_t1t2");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && (u.pathname === "/qia/cal.js" || u.pathname === "/qia/offchain.js" || u.pathname === "/qia/list.js") && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/cal.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("qia_cal");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && /^\/qia\/cal\/[a-z0-9]{10,40}\.json$/.test(u.pathname) && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("qia_cal_" + u.pathname.slice(9, -5));
      if (v) return new Response(v, { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/offchain-summary.json" && env.IRIS_BENCH) {   // 16 Nov 2026: the page's first read
      const v = await env.IRIS_BENCH.get("qia_offchain_summary");
      if (v) return new Response(v, { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/offchain.json" && env.IRIS_BENCH) {
      // 26 Nov 2026: the full chain is stored in parts under 8 MB (qia_offchain_p<i>) plus a meta key; it reached 20 MB of the 25 MiB value cap as one key.
      const meta = await env.IRIS_BENCH.get("qia_offchain_parts");
      if (meta) {
        const m = JSON.parse(meta); const n = m.parts | 0; delete m.parts;
        const ps = await Promise.all(Array.from({ length: n }, (_, i) => env.IRIS_BENCH.get("qia_offchain_p" + i)));
        if (n > 0 && ps.every(x => x !== null)) {
          const head = JSON.stringify(m).slice(0, -1);
          return new Response(head + ',"entries":[' + ps.join(",") + "]}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
        }
      }
      const v = await env.IRIS_BENCH.get("qia_offchain");
      if (v) return new Response(v, { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/replies.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/now.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/darkwave/clock.json") {
      const v = env.IRIS_BENCH ? await env.IRIS_BENCH.get("dwclock") : null;
      if (v) return new Response(v, { headers: { "content-type": "application/json", "cache-control": "no-store", "x-content-type-options": "nosniff" } });
      if (env.ASSETS) return env.ASSETS.fetch(req);
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/darkwave/tables.js" && env.ASSETS) return env.ASSETS.fetch(req);
    {
      const tm = (host === "indahl.ai" || host === "www.indahl.ai") && /^\/darkwave\/tables\/(?:latest|(ibm_[a-z0-9_]+)\/(index|(\d{4}-\d\d-\d\d)(\.kit)?))\.json$/.exec(u.pathname);
      if (tm && env.IRIS_BENCH) {
        const v = await env.IRIS_BENCH.get("dwt" + u.pathname.slice("/darkwave/tables".length));
        const h = { "content-type": "application/json", "cache-control": !tm[1] || tm[2] === "index" ? "no-store" : "public, max-age=300", "x-content-type-options": "nosniff" };
        if (v && tm[4]) h["content-disposition"] = 'attachment; filename="kick_table_' + tm[1] + "_" + tm[3] + '.json"';
        return new Response(v || "{}", { status: v ? 200 : 404, headers: h });
      }
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/darkwave/fig1.png" && env.ASSETS) {
      const r = await env.ASSETS.fetch(req);
      return new Response(r.body, { status: r.status, headers: { "content-type": "image/png", "cache-control": "public, max-age=86400", "x-content-type-options": "nosniff" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/desks.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && env.ASSETS && ["/manifest.webmanifest", "/sw.js", "/pwa.js", "/live-tags.js", "/headline.js", "/nav.js", "/ares-map.js", "/share.js", "/try.js", "/chronos.js", "/carry_result.js", "/icons/icon-192.png", "/icons/icon-512.png", "/icons/icon-maskable-512.png", "/icons/apple-touch-icon.png"].includes(u.pathname)) {
      const a = await env.ASSETS.fetch(req);
      const h = new Headers(a.headers);
      h.set("cache-control", u.pathname === "/sw.js" || (u.pathname === "/live-tags.js" || u.pathname === "/headline.js") && !u.searchParams.has("v") ? "no-cache" : u.pathname === "/live-tags.js" || u.pathname === "/headline.js" ? "public, max-age=31536000, immutable" : "public, max-age=86400");
      if (u.pathname === "/manifest.webmanifest") h.set("content-type", "application/manifest+json");
      if (u.pathname === "/sw.js") {
        h.set("content-type", "text/javascript");
        h.set("service-worker-allowed", "/");
      }
      return new Response(a.body, { status: a.status, headers: h });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/replies.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("replies_public");
      return new Response(v || '{"replies":[]}', { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/tape/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && /^\/receipts\/stamps\/(live\.js|index\.json|release_[0-9a-f]{12}(-\d{8}T\d{6}Z)?\.json(\.ots)?)$/.test(u.pathname) && env.ASSETS) {
      const r = await env.ASSETS.fetch(req);
      const ty = u.pathname.endsWith(".ots") ? "application/octet-stream" : u.pathname.endsWith(".js") ? "text/javascript; charset=utf-8" : "application/json; charset=utf-8";
      const h = { "content-type": ty, "cache-control": "public, max-age=300", "x-content-type-options": "nosniff", "access-control-allow-origin": "*" };
      if (u.pathname.endsWith(".ots")) h["content-disposition"] = 'attachment; filename="' + u.pathname.split("/").pop() + '"';
      return new Response(r.body, { status: r.status, headers: h });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/tape/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("tape_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/hosts/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/hosts/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("hosts_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/campus/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/campus/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("campus_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/airq/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/airq/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("airq_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/ailuminate/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/ailuminate/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("ailuminate_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/hpt/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/hpt/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("hpt_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/weights/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/weights/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("weights_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/airline/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/airline/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("airline_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/fedsep/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/fedsep/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("fedsep_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/revise/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/revise/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("revise_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/pkginstall/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/pkginstall/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("pkginstall_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/seat/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/seat/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("seat_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/secrecords/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/secrecords/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("secrecords_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/change/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/change/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("change_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/hfsize/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/hfsize/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("hfsize_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/hflicense/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/hflicense/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("hflicense_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/pkglicense/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/pkglicense/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("pkglicense_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/support/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/support/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("support_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/arxivdrift/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/arxivdrift/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("arxivdrift_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/linkrot/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/linkrot/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("linkrot_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/uptime/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/uptime/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("uptime_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/cada/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/cada/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("caca_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/time/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/time/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("time_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/ibm.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/qia/ibm.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("qia_ibm");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && (u.pathname === "/sad" || u.pathname.startsWith("/sad/"))) return Response.redirect("https://" + host + "/hermes/model" + u.pathname.slice(4) + u.search, 301);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/hermes/model/live.js" && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/hermes/model/live.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("model_live");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && (u.pathname === "/vault/tlock.js" || u.pathname === "/vault/app.js") && env.ASSETS) {
      const r = await env.ASSETS.fetch(req);
      return new Response(r.body, { status: r.status, headers: { "content-type": "text/javascript; charset=utf-8", "cache-control": "public, max-age=300", "x-content-type-options": "nosniff" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname.startsWith("/tape/")) {
      const J = (o, st, extra) => new Response(JSON.stringify(o), { status: st || 200, headers: { "content-type": "application/json", "cache-control": "no-store", "x-content-type-options": "nosniff", ...extra || {} } });
      if (u.pathname === "/tape/commit" && env.tape_commits) {
        if (req.method !== "POST") return J({ error: 'POST a JSON body {"h":"<64 hex>"}' }, 405);
        const org = req.headers.get("Origin");
        if (org && org !== "https://indahl.ai" && org !== "https://www.indahl.ai") return J({ error: "origin" }, 403);
        if (!(req.headers.get("content-type") || "").includes("application/json")) return J({ error: "json only" }, 415);
        const raw = await req.text();
        if (raw.length > 200) return J({ error: "too large" }, 413);
        let h = "";
        try {
          h = String(JSON.parse(raw).h || "");
        } catch (e) {
        }
        if (!/^[0-9a-f]{64}$/.test(h)) return J({ error: "h must be 64 lowercase hex characters, the SHA-256 of your file" }, 400);
        const now = Math.floor(Date.now() / 1e3), hr = Math.floor(now / 3600), day = Math.floor(now / 86400);
        const ipk = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(ip + ":" + hr)))).slice(0, 8).map((b) => b.toString(16).padStart(2, "0")).join("");
        const rl = await env.tape_commits.prepare("INSERT INTO rl(k,c,w) VALUES(?,1,?) ON CONFLICT(k) DO UPDATE SET c=c+1 RETURNING c").bind("i" + ipk, hr).first();
        if (rl && rl.c > 20) return J({ error: "too many commits from this address this hour" }, 429);
        const g = await env.tape_commits.prepare("INSERT INTO rl(k,c,w) VALUES(?,1,?) ON CONFLICT(k) DO UPDATE SET c=c+1 RETURNING c").bind("g" + day, day).first();
        if (g && g.c > 3e3) return J({ error: "the daily limit is reached, try tomorrow" }, 503);
        if (Math.random() < 0.01) await env.tape_commits.prepare("DELETE FROM rl WHERE w < ?").bind(hr - 72).run();
        await env.tape_commits.prepare("INSERT OR IGNORE INTO commits(h,t) VALUES(?,?)").bind(h, now).run();
        const r = await env.tape_commits.prepare("SELECT t,n FROM commits WHERE h=?").bind(h).first();
        return J({ h, received: r.t, received_utc: new Date(r.t * 1e3).toISOString().replace(".000Z", "Z"), entry: r.n, status: r.n ? "chained" : "received, chained within the hour" });
      }
      const rcm = /^\/tape\/receipt\/([0-9a-f]{64})$/.exec(u.pathname);
      if (rcm && env.tape_commits) {
        const r = await env.tape_commits.prepare("SELECT t,n FROM commits WHERE h=?").bind(rcm[1]).first();
        return r ? J({ h: rcm[1], received: r.t, received_utc: new Date(r.t * 1e3).toISOString().replace(".000Z", "Z"), entry: r.n, status: r.n ? "chained" : "received, chained within the hour" }) : J({ h: rcm[1], status: "not found" }, 404);
      }
      const dm = /^\/tape\/drand\/52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971\/(info|public\/latest|public\/[0-9]{1,10})$/.exec(u.pathname);
      if (dm && req.method === "GET") {
        const up = await fetch("https://api.drand.sh/52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971/" + dm[1], { cf: { cacheTtl: dm[1] === "public/latest" ? 2 : 86400, cacheEverything: true } });
        return new Response(up.body, { status: up.status, headers: { "content-type": "application/json", "cache-control": dm[1] === "public/latest" ? "public, max-age=2" : "public, max-age=86400" } });
      }
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/headlines.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("headlines");
      return new Response(v || '{"pages":{},"home":[]}', { headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "access-control-allow-origin": "*" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/activity.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("activity");
      return new Response(v || '{"live":{}}', { headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "access-control-allow-origin": "*" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/train.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("train");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && /^\/progress\/[a-z]{2,20}\.json$/.test(u.pathname) && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("progress_" + u.pathname.slice(10, -5));
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && u.pathname === "/iris/yo.json" && env.IRIS_BENCH) {
      const v = await env.IRIS_BENCH.get("yo");
      return new Response(v || "{}", { headers: { "content-type": "application/json", "cache-control": "no-store" } });
    }
    if ((host === "indahl.ai" || host === "www.indahl.ai") && (/^\/(qia|iris)\/runs\/[A-Za-z0-9.\-]+\.zip$/.test(u.pathname) || u.pathname === "/qia/data.json" || u.pathname === "/hermes/datapapers.json" || u.pathname === "/record.json" || /^\/standard\/(STANDARD|CHECKLIST|CROSSWALK)\.md$|^\/standard\/standard_v1(\.schema)?\.json$|^\/standard\/SHA256SUMS\.txt(\.ots)?$/.test(u.pathname) || /^\/(qia|iris|atlas|darkwave|oy|hermes)\/[a-z0-9-]+-(package|kit|pack)\.zip(\.sha256)?$/.test(u.pathname) || /^\/([a-z]+)\/\1-data-pack\.zip(\.sha256)?$/.test(u.pathname) || u.pathname === "/qia/offchain.json" || u.pathname === "/atlas/datacenters.json" || u.pathname === "/atlas/electricity.json" || u.pathname === "/atlas/utilities.json" || u.pathname === "/atlas/plants.json" || u.pathname === "/atlas/carbon.json" || u.pathname === "/atlas/planned.json" || u.pathname === "/atlas/scale.json" || /^\/hermes\/model\/[A-Za-z0-9_.\-]+\.(json|csv|py|txt|jsonl|c|swift|sh)$/.test(u.pathname)) && env.ASSETS) return env.ASSETS.fetch(req);
    if ((host === "indahl.ai" || host === "www.indahl.ai") && PDFS.includes(u.pathname)) return Response.redirect("https://heuremen.org" + u.pathname, 301);
    if (host === "indahl.ai" || host === "www.indahl.ai") {
      const H = { "tdm-reservation": "1", "tdm-policy": "https://indahl.ai/terms#ai-training", "cache-control": "public, max-age=300", "x-content-type-options": "nosniff", "referrer-policy": "strict-origin-when-cross-origin", "strict-transport-security": "max-age=31536000", "x-frame-options": "DENY", "permissions-policy": "camera=(), microphone=(), geolocation=()", "content-security-policy": "default-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data:; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'" };
      {
        const sr = await handleSecurity(req, env, u, { PAGES: INDAHL_PAGES, handle });
        if (sr) return sr;
      }
      if (/^\/r\/[A-Za-z0-9._-]+\.html$/.test(u.pathname)) return Response.redirect(new URL(u.pathname.slice(0, -5), u.origin).toString(), 301);
      if (u.pathname === "/r") return Response.redirect("https://indahl.ai/r/", 301);
      if (u.pathname === "/r/go") {
        const id = (u.searchParams.get("id") || "").trim().slice(0, 120), d = (u.searchParams.get("d") || "").trim();
        const to = id ? "/r/" + id.replace(/flock/g, "house").replace(/[^A-Za-z0-9._~-]/g, (c) => "~" + c.charCodeAt(0).toString(16).toUpperCase().padStart(2, "0")) : /^[a-z0-9-]{1,60}$/.test(d) ? "/r/desk/" + d : "/r/";
        return Response.redirect("https://indahl.ai" + to, 302);
      }
      if (/^\/r\/((desk\/)?[A-Za-z0-9._~-]{1,160})?$/.test(u.pathname) && env.ASSETS) {
        const a = await env.ASSETS.fetch(new Request(new URL(u.pathname === "/r/" ? "/r/index.html" : u.pathname + ".html", u.origin)));
        if (a.status === 200) return new Response(a.body, { headers: { ...H, "content-type": "text/html; charset=utf-8" } });
        return new Response(INDAHL_PAGES["/404"], { status: 404, headers: { ...H, "content-type": "text/html; charset=utf-8" } });
      }
      const oy = OY_FILES[u.pathname.replace(/\.html$/, "")];
      if (oy) return new Response(oy[0], { headers: { ...H, "content-type": oy[1], "content-security-policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'" } });
      if (u.pathname.startsWith("/oy/") && /\.(js|json|stl|png|svg|css|txt)$/.test(u.pathname) && env.ASSETS) {
        const r = await env.ASSETS.fetch(req);
        const h = new Headers(r.headers);
        for (const [k, v] of Object.entries(H)) h.set(k, v);
        h.set("cache-control", "public, max-age=86400");
        return new Response(r.body, { status: r.status, headers: h });
      }
      if (u.pathname === "/robots.txt") return new Response("User-agent: *\nContent-Signal: search=yes, ai-input=yes, ai-train=no\nAllow: /\nDisallow: /agree\nDisallow: /inquiry\nDisallow: /inquire\nDisallow: /correction-request\nDisallow: /request\nDisallow: /respond\n\nUser-agent: GPTBot\nDisallow: /\n\nUser-agent: ClaudeBot\nDisallow: /\n\nUser-agent: anthropic-ai\nDisallow: /\n\nUser-agent: CCBot\nDisallow: /\n\nUser-agent: Google-Extended\nDisallow: /\n\nUser-agent: Applebot-Extended\nDisallow: /\n\nUser-agent: Bytespider\nDisallow: /\n\nUser-agent: Meta-ExternalAgent\nDisallow: /\n\nUser-agent: FacebookBot\nDisallow: /\n\nUser-agent: Amazonbot\nDisallow: /\n\nUser-agent: cohere-ai\nDisallow: /\n\nUser-agent: Diffbot\nDisallow: /\n\nUser-agent: Omgilibot\nDisallow: /\n\nUser-agent: ImagesiftBot\nDisallow: /\n\nSitemap: https://indahl.ai/sitemap.xml\n", { headers: { ...H, "content-type": "text/plain; charset=utf-8" } });
      if (u.pathname === "/7b56a9a7df0179bc520502cd2021efb4.txt") return new Response("7b56a9a7df0179bc520502cd2021efb4", { headers: { ...H, "content-type": "text/plain; charset=utf-8" } });
      if (u.pathname === "/.well-known/openai-apps-challenge") return new Response("7vJW2G4T-37NQjlaCdNkyxTMlMmSGIN5TnxArj2rrBA", { headers: { ...H, "content-type": "text/plain; charset=utf-8" } });   // 14 Nov: OpenAI plugin directory domain verification (public token)
      if (u.pathname === "/.well-known/tdmrep.json") return new Response('[{"location": "/*", "tdm-reservation": 1, "tdm-policy": "https://indahl.ai/terms#ai-training"}]', { headers: { ...H, "content-type": "application/json" } });
      if (/^\/fonts\/[a-z0-9\-]+\.woff2$/.test(u.pathname) && env.ASSETS) {
        const r = await env.ASSETS.fetch(req);
        return new Response(r.body, { status: r.status, headers: { ...H, "content-type": "font/woff2", "cache-control": "public, max-age=31536000, immutable" } });
      }
      if (u.pathname === "/favicon.svg") return new Response(FAVICON_SVG, { headers: { ...H, "content-type": "image/svg+xml", "cache-control": "public, max-age=86400" } });
      if (/^\/og\/[a-z0-9-]+\.png$/.test(u.pathname) && env.ASSETS) {
        const r = await env.ASSETS.fetch(req);
        return new Response(r.body, { status: r.status, headers: { ...H, "content-type": "image/png" } });
      }
      {
        const fm = /^\/[a-z0-9]+\/([a-z0-9_-]+\.csv|[a-z0-9-]+-LICENSE\.txt)$/.exec(u.pathname);
        if (fm && env.ASSETS) {
          const r = await env.ASSETS.fetch(req);
          if (r.status === 200) return new Response(r.body, { headers: { ...H, "content-type": fm[1].endsWith(".csv") ? "text/csv; charset=utf-8" : "text/plain; charset=utf-8", "cache-control": "public, max-age=3600" } });
        }
      }
      {
        const cm = /^\/([a-z0-9]+)\/changes\.xml$/.exec(u.pathname);
        if (cm) {
          const v = env.IRIS_BENCH ? await env.IRIS_BENCH.get("changes_" + cm[1]) : null;
          const r = v ? null : env.ASSETS ? await env.ASSETS.fetch(req) : null;
          if (v || r && r.status === 200) return new Response(v || r.body, { headers: { ...H, "content-type": "application/atom+xml; charset=utf-8", "cache-control": "public, max-age=300" } });
        }
      }
      if ((u.pathname === "/corrections.xml" || u.pathname === "/corrections.csv") && env.ASSETS) {
        const r = await env.ASSETS.fetch(req);
        if (r.status === 200) return new Response(r.body, { headers: { ...H, "content-type": u.pathname.endsWith(".xml") ? "application/atom+xml; charset=utf-8" : "text/csv; charset=utf-8" } });
      }
      if (u.pathname === "/og.png" && env.ASSETS) {
        const r = await env.ASSETS.fetch(req);
        return new Response(r.body, { status: r.status, headers: { ...H, "content-type": "image/png", "cache-control": "public, max-age=86400" } });
      }
      if (u.pathname === "/feed.xml") {
        let rounds = "";
        try {
          const v = env.IRIS_BENCH && await env.IRIS_BENCH.get("results");
          const d = v ? JSON.parse(v) : { rounds: [] };
          const rs = d.rounds || [];
          const MO = { Jan: "01", Feb: "02", Mar: "03", Apr: "04", May: "05", Jun: "06", Jul: "07", Aug: "08", Sep: "09", Oct: "10", Nov: "11", Dec: "12" };
          const roundTime = async (r) => {
            if (r.published) return r.published;
            try {
              const s = JSON.parse(await env.IRIS_BENCH.get("status" + (r.round > 1 ? r.round : "")) || "{}"), m = /^(\d{1,2}) ([A-Za-z]{3}) (\d{2}):(\d{2})/.exec(s.updated || "");
              if (!m || !MO[m[2]]) return null;
              const now = /* @__PURE__ */ new Date();
              let t = new Date(Date.UTC(now.getUTCFullYear(), +MO[m[2]] - 1, +m[1], +m[3], +m[4]));
              if (t > now) t = new Date(Date.UTC(now.getUTCFullYear() - 1, +MO[m[2]] - 1, +m[1], +m[3], +m[4]));
              return t.toISOString().replace(".000Z", "Z");
            } catch (e) {
              return null;
            }
          };
          const ts = await Promise.all(rs.map(roundTime));
          rounds = rs.map((r, i) => `<entry><id>tag:indahl.ai,2026:iris-bench-round-${r.round}</id><title>Faults and Guards bench: round ${r.round} results</title><link href="https://indahl.ai/iris"/><updated>${ts[i] || "2026-10-27T12:00:00Z"}</updated><summary>Rates with intervals for ten open-weight models, bare and with the Fault and Guard wording. Raw replies on Hugging Face.</summary></entry>`).join("");
        } catch (e) {
        }
        const newest = ((rounds + FEED).match(/<updated>[^<]+<\/updated>/g) || []).map((x) => x.slice(9, -10)).sort().pop() || BUILT + "T00:00:00Z";
        return new Response('<?xml version="1.0" encoding="UTF-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom"><id>tag:indahl.ai,2026:feed</id><title>Heuremen LLC: new studies and bench rounds</title><link href="https://indahl.ai/feed.xml" rel="self"/><link href="https://pubsubhubbub.appspot.com/" rel="hub"/><link href="https://indahl.ai/"/><updated>' + newest + "</updated><author><name>Heuremen LLC</name></author>" + rounds + FEED + "</feed>\n", { headers: { ...H, "content-type": "application/atom+xml; charset=utf-8" } });
      }
      if (u.pathname === "/llms.txt") return new Response(LLMS, { headers: { ...H, "content-type": "text/plain; charset=utf-8" } });
      if (u.pathname === "/sitemap.xml") return new Response(SITEMAP, { headers: { ...H, "content-type": "application/xml; charset=utf-8" } });   // 21 Nov 2026 (SEO pass): the sitemap is a build output of build_site.py (one noindex rule, checked by ledger/seo_gate.py); receipts stay out (internal)
      if (u.pathname === "/style.css") return new Response(INDAHL_CSS, { status: 200, headers: { ...H, "content-type": "text/css; charset=utf-8", ...u.searchParams.has("v") ? { "cache-control": "public, max-age=31536000, immutable" } : {} } });
      const html = (body, status) => new Response(body, { status, headers: { ...H, "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
      {
        const nr = await handleNotify(req, env, u, { html, H, PAGES: INDAHL_PAGES, handle, privacy: PRIVACY.version });
        if (nr) return nr;
      }
      if (u.pathname === "/week" || u.pathname.startsWith("/week/") || u.pathname.startsWith("/newsletter")) {
        const wr = await handleWeekly(req, env, u, html, INDAHL_PAGES);
        if (wr) return wr;
      }
      if (u.pathname === "/alerts.js" || u.pathname.startsWith("/alerts/") || u.pathname === "/signup" || u.pathname === "/signup.js" || u.pathname === "/alerts" && u.searchParams.has("e")) {
        const ar = await handleAlerts(req, env, u, html, INDAHL_PAGES);
        if (ar) return ar;
      }
      if (u.pathname === "/index-request") {
        const escI = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
        return handleIndexRequest(req, env, (msg, status) => html(messagePage(INDAHL_PAGES["/inquire-ok"], formTitle("Link", status), `<main class="wrap"><section class="closing"><p>${escI(msg)}</p></section></main>`), status));
      }
      if (u.pathname === "/correction-request") {
        const escC = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
        return handleCorrection(req, env, (msg, status) => html(messagePage(INDAHL_PAGES["/inquire-ok"], formTitle("Correction request", status), `<main class="wrap"><section class="closing"><p>${escC(msg)}</p></section></main>`), status));
      }
      if (u.pathname === "/respond-request") {
        const escR = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
        return handleResponse(req, env, (msg, status) => html(messagePage(INDAHL_PAGES["/inquire-ok"], formTitle("Response", status), `<main class="wrap"><section class="closing"><p>${escR(msg)}</p></section></main>`), status));
      }
      if (u.pathname === "/respond") {
        const uq = (u.searchParams.get("u") || "").toLowerCase();
        const ok = /^(model|oy|qia|iris|atlas|time|cada|uptime|forecast|cadence|trials|launch|linkrot|arxivdrift|support|pkglicense|hflicense|hfsize|change|secrecords|seat|pkginstall|stack|revise|fedsep|airline|weights|hpt|ailuminate|airq|campus|hosts|tape|water|neo|tornado|cassandra|voightkampff|credit|cone|solar|wiki|social|adspend|predictions)-[a-z0-9._-]{1,70}$/.test(uq);
        const escU = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
        return html(INDAHL_PAGES["/respond"].replace("__UNIT__", () => ok ? escU(uq) : ""), 200);
      }
      if (u.pathname === "/inquire") {
        const esc = (t) => t.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
        return handleInquiry(req, env, (msg, status) => msg === null ? html(INDAHL_PAGES["/inquire-ok"], status) : html(INDAHL_PAGES["/inquire-error"].replace("__MSG__", esc(msg)), status));
      }
      const escH = (t) => String(t || "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
      const fail = (msg) => html(INDAHL_PAGES["/inquire-error"].replace("__MSG__", () => escH(msg)), 400);
      if (u.pathname === "/gate-ui.js") return new Response(GATE_JS, { headers: { ...H, "content-type": "text/javascript; charset=utf-8" } });
      if (u.pathname === "/nda" || u.pathname === "/nda.txt") return Response.redirect("https://indahl.ai/contact", 301);
      if (u.pathname === "/auth/start") return await GATE.agreement(req, env) ? GATE.start(req, env) : Response.redirect("https://indahl.ai/contact", 302);
      if (u.pathname === "/auth/callback") return GATE.callback(req, env, fail);
      if (u.pathname === "/auth/out") return GATE.out();
      if (u.pathname === "/agree" && req.method === "POST") return GATE.agree(req, env, { nda: NDA.version, privacy: PRIVACY.version }, fail);
      if (u.pathname === "/inquiry") {
        if (!await GATE.agreement(req, env)) return Response.redirect("https://indahl.ai/contact", 302);
        const s = await GATE.session(req, env);
        const verify = s ? `<p class="meta">Identity verified: <strong>${escH(s.e)}</strong>. <a href="/auth/out">Not you?</a></p>` : '<p class="actions"><a class="btn ghost" id="verify" href="/auth/start">Verify your identity to submit</a></p>';
        return html(INDAHL_PAGES["/inquiry"].replace("__T__", String(Date.now())).replace("__VERIFY__", () => verify).replace("__DISABLED__", s ? "" : " disabled"), 200);
      }
      if (u.pathname === "/request") return Response.redirect("https://indahl.ai/contact", 301);
      let p = u.pathname.replace(/\/index\.html$/, "/").replace(/\.html$/, "");
      if (p.length > 1) p = p.replace(/\/+$/, "");
      const page = p === "/inquire-ok" || p === "/inquire-error" || p === "/inquiry" ? null : INDAHL_PAGES[p];
      return new Response(page || INDAHL_PAGES["/404"], { status: page && p !== "/404" ? 200 : 404, headers: { ...H, "content-type": "text/html; charset=utf-8" } });
    }
    return Response.redirect("https://indahl.ai/", 301);
  }
}
// 23 Nov 2026 (the designer review #9 and #14): one strict counter per key (a visitor's address), used by POST /inquire here and by POST /qubit on
// quantumidleaudit.com (bound across scripts). A Durable Object holds each key in one place, so a burst cannot slip past as it did with
// the KV read-then-write and with the per-location rate-limit binding. GET /?limit=N&win=SECONDS answers 200 (allowed) or 429.
export class Limiter {
  constructor(state) { this.state = state; }
  async fetch(req) {
    const u = new URL(req.url), limit = Math.max(1, Number(u.searchParams.get("limit")) || 20), win = Math.max(1, Number(u.searchParams.get("win")) || 60) * 1000;
    const now = Date.now(); let w = (await this.state.storage.get("w")) || [];
    w = w.filter((t) => now - t < win);
    if (w.length >= limit) { await this.state.storage.put("w", w); return new Response("limited", { status: 429 }); }
    // 23 Nov 2026 (review #3): the record clears itself one window after the last request, so storage does not grow with every visitor.
    await this.state.storage.setAlarm(now + win + 1000);
    w.push(now); await this.state.storage.put("w", w);
    return new Response("ok");
  }
  async alarm() { await this.state.storage.deleteAll(); }
}
export {
  cut_default as default
};
