// toolkit_common.js (16 Nov 2026): shared helpers for the toolkit modules (tools_text.js, tools_stats.js, tools_ops.js, tools_qia.js).
// Skills turned into read-only MCP tools. Nothing here writes, stores or logs what a caller sends.
export const TERMS = 'https://indahl.ai/terms', USE = 'Retrieval and answering are permitted. Use as training data is not permitted.';
export const UA = 'indahl.ai checks (https://indahl.ai/contact)';
// Computed answers are read at the moment they are served, so read_at is the serve time unless the data names an earlier read.
export const answer = (source, data, readAt) => { const now = new Date().toISOString(); return { source, read_at: readAt || now, served_at: now, terms: TERMS, use: USE, data }; };
export const clip = (s, n = 20000) => (s == null ? '' : String(s)).slice(0, n);
export async function sha256hex(input) {
  const buf = typeof input === 'string' ? new TextEncoder().encode(input) : input;
  const h = await crypto.subtle.digest('SHA-256', buf); return [...new Uint8Array(h)].map(b => b.toString(16).padStart(2, '0')).join('');
}
// URL guard (16 Nov 2026, the referee MOVES on SSRF). A Cloudflare Worker cannot open connections to private networks, which lowers the stakes;
// the guard still refuses anything that is not a public web address, on the first request and on every redirect hop:
//   http/https only, ports 80 and 443 only, no credentials, at least one dot, no IP literals (the URL parser normalizes decimal, hex and octal
//   IPv4 forms to dotted form first), no local/internal names, and the name must resolve (Cloudflare DNS-over-HTTPS) only to public addresses:
//   loopback, private, link-local (169.254/16), CGNAT (100.64/10), ULA, multicast, documentation and reserved ranges are refused. Redirects are
//   followed by hand, at most 5 hops, each hop re-checked. A Worker cannot pin the resolved address for the connection; that gap is stated.
const PRIVATE_HOST = /(^|\.)(localhost|local|internal|lan|home|corp|intranet|localdomain)$/i;
const FIXED_PUBLIC = /(^|\.)(arxiv\.org|crossref\.org|doi\.org|github\.com|githubusercontent\.com|pypi\.org|npmjs\.org|cloudflare-dns\.com|huggingface\.co|indahl\.ai|wikipedia\.org|nature\.com)$/i;
// Our own zones (the referee round 2): a Worker reaching a hostname on its own Cloudflare account can reach origins the outside internet reaches only
// through Cloudflare (a Tunnel, an origin rule). Every host on these zones is refused except the public site itself (indahl.ai, www.indahl.ai,
// served by this same Worker, so a read returns exactly what anyone sees) and heuremen.org (public GitHub Pages).
const OWN_ZONES = ['indahl.ai', 'heuremen.org'];   // 16 Nov 2026: the other zones on the account are matched by FNV-1a hash, so their names stay out of the public source
const OWN_ZONE_H = new Set(['3fb4ec72', '41fbed5d', '5a96281d', '79346eba', '7d153fd5', '7f9d4549', '82667753', '911c6d00', '9ac046f6', '9d737ac3', '9dac38b0', 'add3c28c', 'b4111d7f', 'c0412abe', 'c8a15826', 'e212a85f', 'fe8415bf']);
function fnv1a(s) { let h = 0x811c9dc5; for (const b of new TextEncoder().encode(s)) { h ^= b; h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16).padStart(8, '0'); }
function ownZone(hl) { if (OWN_ZONES.some(z => hl === z || hl.endsWith('.' + z))) return true; const p = hl.split('.'); for (let i = 0; i < p.length - 1; i++) if (OWN_ZONE_H.has(fnv1a(p.slice(i).join('.')))) return true; return false; }
const OWN_ALLOWED = new Set(['indahl.ai', 'www.indahl.ai', 'heuremen.org', 'www.heuremen.org']);
export function safeUrl(raw) {
  let u; try { u = new URL(String(raw || '').trim()); } catch (e) { return { ok: false, reason: 'not a URL' }; }
  if (!/^https?:$/.test(u.protocol)) return { ok: false, reason: 'only http and https URLs are read' };
  if (u.port && !['80', '443'].includes(u.port)) return { ok: false, reason: 'only ports 80 and 443 are read' };
  const h = u.hostname.replace(/^\[|\]$/g, '').replace(/\.$/, '');
  if (/^[\d.]+$/.test(h) || h.includes(':')) return { ok: false, reason: 'IP-address URLs are not read; use a host name' };
  if (!h.includes('.') || PRIVATE_HOST.test(h)) return { ok: false, reason: 'private, local or single-label host names are not read' };
  if (u.username || u.password) return { ok: false, reason: 'URLs with credentials are not read' };
  const hl = h.toLowerCase(); if (ownZone(hl) && !OWN_ALLOWED.has(hl)) return { ok: false, reason: 'hosts on Heuremen LLC\'s own zones are not read, except the public site indahl.ai' };
  if (OWN_ALLOWED.has(hl) && /^\/(mcp|api)(\/|$)|^\/\.well-known\/mcp/i.test(u.pathname)) return { ok: false, reason: 'the indahl.ai tool endpoints are not read by the tools themselves' };   // the referee round 3: no tool recursion
  return { ok: true, url: u.toString(), host: h };
}
function v4Private(ip) {
  const p = ip.split('.').map(Number); if (p.length !== 4 || p.some(x => !(x >= 0 && x <= 255))) return true;
  const [a, b] = p;
  return a === 0 || a === 10 || a === 127 || (a === 100 && b >= 64 && b <= 127) || (a === 169 && b === 254) || (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168)
    || (a === 192 && b === 0 && (p[2] === 0 || p[2] === 2)) || (a === 198 && (b === 18 || b === 19)) || (a === 198 && b === 51 && p[2] === 100) || (a === 203 && b === 0 && p[2] === 113) || a >= 224;
}
function v6Private(ip) {
  const x = ip.toLowerCase(); if (x === '::' || x === '::1') return true;
  const m = x.match(/^::ffff:(\d+\.\d+\.\d+\.\d+)$/); if (m) return v4Private(m[1]);
  return /^(fc|fd|fe8|fe9|fea|feb|ff)/.test(x) || x.startsWith('64:ff9b:') || x.startsWith('2001:db8') || x.startsWith('100:');
}
const dnsCache = new Map();
let testResolver = null;   // tests with a stubbed fetch set this so the DNS step is not sent to the stub; never set in the worker
export const __setTestResolver = (fn) => { testResolver = fn; dnsCache.clear(); };
async function publicHost(host) {
  if (testResolver) return testResolver(host);   // true when every A/AAAA answer is a public address; fixed public API hosts skip the lookup
  if (FIXED_PUBLIC.test(host)) return { ok: true };
  if (dnsCache.has(host)) return dnsCache.get(host);
  const ask = async (type) => { try { const r = await fetch(`https://cloudflare-dns.com/dns-query?name=${encodeURIComponent(host)}&type=${type}`, { headers: { accept: 'application/dns-json' } }); return r.ok ? r.json() : null; } catch (e) { return null; } };
  const [a, aaaa] = await Promise.all([ask('A'), ask('AAAA')]);
  if (!a && !aaaa) { const v = { ok: false, reason: 'the host name could not be resolved' }; dnsCache.set(host, v); return v; }
  const ips = [...((a && a.Answer) || []).filter(x => x.type === 1), ...((aaaa && aaaa.Answer) || []).filter(x => x.type === 28)].map(x => x.data);
  let v; if (!ips.length) v = { ok: false, reason: 'the host name has no address' };
  else if (ips.some(ip => ip.includes(':') ? v6Private(ip) : v4Private(ip))) v = { ok: false, reason: 'the host name resolves to a private or reserved address' };
  else v = { ok: true };
  dnsCache.set(host, v); return v;
}
export async function fetchText(url, { timeoutMs = 8000, maxBytes = 2_000_000, headers = {}, method = 'GET', bytes = false } = {}) {
  const at = new Date().toISOString(); const ac = new AbortController(); const t = setTimeout(() => ac.abort(), timeoutMs);
  try {
    let cur = url, r = null;
    for (let hop = 0; hop <= 5; hop++) {
      const su = safeUrl(cur); if (!su.ok) return { ok: false, status: 0, url: cur, at, error: 'refused: ' + su.reason, text: '' };
      const ph = await publicHost(su.host); if (!ph.ok) return { ok: false, status: 0, url: cur, at, error: 'refused: ' + ph.reason, text: '' };
      r = await fetch(su.url, { method, redirect: 'manual', signal: ac.signal, headers: { 'user-agent': UA, ...headers } });
      if (r.status >= 300 && r.status < 400 && r.headers.get('location')) { cur = new URL(r.headers.get('location'), su.url).toString(); if (hop === 5) return { ok: false, status: r.status, url: cur, at, error: 'more than 5 redirects', text: '' }; continue; }
      cur = su.url; break;
    }
    let buf = new Uint8Array(0);
    if (method !== 'HEAD' && r.body) {
      const reader = r.body.getReader(); const parts = []; let n = 0;
      while (true) { const { done, value } = await reader.read(); if (done) break; parts.push(value); n += value.length; if (n > maxBytes) { try { await reader.cancel(); } catch (e) {} break; } }
      buf = new Uint8Array(Math.min(n, maxBytes)); let o = 0; for (const p of parts) { const take = Math.min(p.length, buf.length - o); buf.set(p.subarray(0, take), o); o += take; if (o >= buf.length) break; }
    }
    const out = { ok: r.ok, status: r.status, url: cur, contentType: r.headers.get('content-type') || '', at, truncated: buf.length >= maxBytes };
    if (bytes) out.bytes = buf; else out.text = new TextDecoder('utf-8', { fatal: false }).decode(buf);
    return out;
  } catch (e) { return { ok: false, status: 0, url, at, error: e.name === 'AbortError' ? 'timed out' : 'could not connect', text: '' }; }
  finally { clearTimeout(t); }
}
// Visible text of an HTML page (scripts, styles and tags removed, entities decoded, whitespace collapsed).
export function htmlToText(html) {
  return String(html || '').replace(/<(script|style|noscript)[\s\S]*?<\/\1>/gi, ' ').replace(/<br\s*\/?>|<\/(p|div|li|h\d|tr)>/gi, '\n').replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n)).replace(/[ \t\r\f\v]+/g, ' ').replace(/\n\s*/g, '\n').trim();
}
// Read a source the caller names: a DOI, an arXiv id or an http(s) URL. Returns { ok, kind, url, status, text, at, reason }.
export async function readSource(src) {
  const s = String(src || '').trim();
  let m = s.match(/^(?:arxiv:)?(\d{4}\.\d{4,5})(v\d+)?$/i) || s.match(/arxiv\.org\/(?:abs|pdf|html)\/(\d{4}\.\d{4,5})(v\d+)?/i);
  if (m) {
    const id = m[1] + (m[2] || '');
    const h = await fetchText(`https://arxiv.org/html/${id}`); if (h.ok && h.text.length > 2000) return { ok: true, kind: 'arxiv_html', url: h.url, status: h.status, text: htmlToText(h.text), at: h.at };
    const a = await fetchText(`https://arxiv.org/abs/${id}`); if (a.ok) return { ok: true, kind: 'arxiv_abstract', url: a.url, status: a.status, text: htmlToText(a.text), at: a.at, reason: 'full text not available as HTML; abstract page only' };
    return { ok: false, kind: 'arxiv', url: a.url, status: a.status, at: a.at, reason: a.error || `arXiv answered ${a.status}` };
  }
  m = s.match(/^(?:https?:\/\/(?:dx\.)?doi\.org\/|doi:)?(10\.\d{4,9}\/\S+)$/i);
  if (m) {
    const doi = m[1]; const r = await fetchText(`https://doi.org/${doi}`, { headers: { accept: 'text/html' } });
    if (r.ok) return { ok: true, kind: 'doi_landing', url: r.url, status: r.status, text: htmlToText(r.text), at: r.at, reason: 'publisher landing page; full text may be behind a paywall' };
    return { ok: false, kind: 'doi', url: r.url, status: r.status, at: r.at, reason: r.error || `answered ${r.status}` };
  }
  const su = safeUrl(s); if (!su.ok) return { ok: false, kind: 'url', reason: su.reason };
  const r = await fetchText(su.url);
  if (!r.ok) return { ok: false, kind: 'url', url: r.url, status: r.status, at: r.at, reason: r.error || `answered ${r.status}` };
  const isHtml = /html/i.test(r.contentType) || /^\s*</.test(r.text);
  if (/pdf/i.test(r.contentType)) return { ok: false, kind: 'pdf', url: r.url, status: r.status, at: r.at, reason: 'PDF text is not extracted; pass an HTML page or paste the text' };
  return { ok: true, kind: isHtml ? 'html' : 'text', url: r.url, status: r.status, text: isHtml ? htmlToText(r.text) : r.text, at: r.at, truncated: r.truncated };
}
