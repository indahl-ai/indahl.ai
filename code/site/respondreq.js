// respondreq.js -- the response door (28 Oct 2026, the owner): any company, school or author named on a page may add a PDF response to that page's unit.
// One field. The PDF stays on the sender's own host; the host name is what we show. Stores the unit code, the link, the host and the time (no name, no email, no IP).
// A truncated one-way hash of the address is kept 1 hour for the rate limit. Nothing is posted until we have read the file and recounted anything it disputes.
const OK = 'Thank you. The response has been received. We read it and recount anything it disputes before it is posted. It is posted as received, dated, with the host it came from.';
const UNIT = /^(model|oy|qia|iris|atlas|time|coin|cada|uptime|forecast|cadence|trials|launch|linkrot|arxivdrift|support|pkglicense|hflicense|hfsize|change|secrecords|seat|pkginstall|stack|revise|fedsep|airline|weights|hpt|ailuminate|airq|campus|hosts|tape|water|wiki|social|adspend)-[a-z0-9._-]{1,70}$/;
const isPdfUrl = s => /^https:\/\/[^\s]+\.pdf([?#][^\s]*)?$/i.test(s);
async function sha(s) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }
export async function handleResponse(req, env, page) {
  if (req.method !== 'POST') return page('Use the form on the response page.', 405);
  const f = await req.formData(); const url = String(f.get('url') || '').trim(); const unit = String(f.get('unit') || '').trim().toLowerCase();
  if (String(f.get('website') || '')) return page(OK, 200);                       // honeypot: bots get the same answer, nothing stored
  if (!UNIT.test(unit)) return page('That reference is not one of ours. Please use the Respond link on the page you are answering.', 400);
  if (url.length > 2000 || !isPdfUrl(url)) return page('Please paste a direct https link to a PDF.', 400);
  const ip = req.headers.get('cf-connecting-ip') || ''; const rk = 'resprl:' + (await sha('qia-resp|' + ip)).slice(0, 32);
  const n = parseInt((await env.INDAHL_INQUIRIES.get(rk)) || '0', 10);
  if (n >= 5) return page('Several responses have arrived from you this hour. Please try again later.', 429);
  let isPdf = false;                                                              // the link must really serve a PDF
  try {
    const r = await fetch(url, { method: 'GET', headers: { Range: 'bytes=0-7' }, redirect: 'follow', cf: { cacheTtl: 0 } });
    const ct = (r.headers.get('content-type') || '').toLowerCase(); const head = new Uint8Array(await r.arrayBuffer()).slice(0, 5);
    isPdf = ct.includes('application/pdf') || String.fromCharCode(...head) === '%PDF-';
  } catch (e) { isPdf = false; }
  if (!isPdf) return page('That link did not return a PDF. Please paste a direct link to the PDF file.', 400);
  const ts = new Date().toISOString(); const host = new URL(url).hostname.toLowerCase();
  await env.INDAHL_INQUIRIES.put(`resp:${ts}:${crypto.randomUUID().slice(0, 8)}`, JSON.stringify({ unit, url, host, received: ts }));
  await env.INDAHL_INQUIRIES.put(rk, String(n + 1), { expirationTtl: 3600 });
  return page(OK, 200);
}
