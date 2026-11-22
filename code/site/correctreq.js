// correctreq.js -- the correction or removal door (30 Oct 2026, the owner: "go for correction or removal option").
// Open to anyone: no agreement, no sign-in, no work email. A person or organisation named on a page, or anyone who finds an error, can ask for a
// correction or a removal. Nothing here is posted. We read every request in full and answer by email, and we may write back to confirm that a
// removal request comes from the person or organisation named. Stored: the fields below and the time, kept 24 months as the privacy notice states.
// A truncated one-way hash of the address is kept 1 hour for the rate limit (never the address itself).
import { EmailMessage } from 'cloudflare:email';
const OK = 'Thank you. Your request has been received. We read it in full and answer by email, usually within a few days. Nothing you sent is posted.';
const KINDS = { correct: 'Correct a number, a quote or a claim', name: 'Remove my name', page: 'Remove a page or a study row', privacy: 'Another privacy request' };
const FIELDS = { name: 120, email: 160, link: 500, kind: 20, details: 3000 };
const EMAIL = /^[^\s@<>"]{1,64}@[^\s@<>"]{1,180}\.[A-Za-z]{2,24}$/;
async function sha(s) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }
export async function handleCorrection(req, env, page) {
  if (req.method !== 'POST') return page('Use the form on the correction page.', 405);
  const f = await req.formData();
  if (String(f.get('website') || '')) return page(OK, 200);                          // honeypot: bots get the same answer, nothing stored
  const rec = {};
  for (const [k, n] of Object.entries(FIELDS)) { const v = String(f.get(k) || '').trim(); if (v.length > n) return page('One of the fields is longer than the form allows.', 400); rec[k] = v; }
  if (!rec.name || !rec.email || !rec.details || !rec.kind) return page('Please complete every required field.', 400);
  if (!EMAIL.test(rec.email)) return page('Please give an email address we can answer.', 400);
  if (!KINDS[rec.kind]) return page('Please choose what you would like us to do.', 400);
  if (rec.link && !/^https:\/\/(www\.)?(indahl\.ai|heuremen\.org)(\/[^\s]*)?$/i.test(rec.link)) return page('The link should be a page on indahl.ai or heuremen.org, or leave it empty and describe the page.', 400);
  const ip = req.headers.get('cf-connecting-ip') || ''; const rk = 'corrrl:' + (await sha('corr|' + ip)).slice(0, 32);
  const n = parseInt((await env.INDAHL_INQUIRIES.get(rk)) || '0', 10);
  if (n >= 5) return page('Several requests have arrived from you this hour. Please try again later.', 429);
  rec.received = new Date().toISOString(); rec.country = req.headers.get('cf-ipcountry') || null;
  const key = `corr:${rec.received}:${crypto.randomUUID().slice(0, 8)}`;
  await env.INDAHL_INQUIRIES.put(key, JSON.stringify(rec), { expirationTtl: 63072000 });   // 24 months, as the privacy notice states
  await env.INDAHL_INQUIRIES.put(rk, String(n + 1), { expirationTtl: 3600 });
  try { await notify(env, rec, key); } catch (e) { await env.INDAHL_INQUIRIES.put('notify-failed:' + key, String(e && e.message || e)); }
  return page(OK, 200);
}
async function notify(env, rec, key) {
  if (!env.INQUIRY_MAIL || !env.INQUIRY_TO || !env.INQUIRY_FROM) return;
  const h = v => String(v || '').replace(/[\r\n]+/g, ' ').slice(0, 200);
  const body = [`Correction or removal request (${rec.received}, ${rec.country || 'country unknown'})`, '', `Name: ${rec.name}`, `Email: ${rec.email}`,
    `What: ${KINDS[rec.kind]}`, `Page: ${rec.link || 'not given'}`, '', 'In their words:', rec.details, '', `Stored as ${key}. Read all with: python3 ~/forge/indahl-ai/inquiries.py`].join('\r\n');
  const raw = [`From: Indahl inquiries <${env.INQUIRY_FROM}>`, `To: <${env.INQUIRY_TO}>`, `Reply-To: ${h(rec.email)}`,
    `Subject: CORRECTION OR REMOVAL: ${h(KINDS[rec.kind])} (${h(rec.name)})`, `Date: ${new Date().toUTCString()}`, `Message-ID: <${crypto.randomUUID()}@indahl.ai>`,
    'MIME-Version: 1.0', 'Content-Type: text/plain; charset=utf-8', 'Content-Transfer-Encoding: 8bit', '', body].join('\r\n');
  await env.INQUIRY_MAIL.send(new EmailMessage(env.INQUIRY_FROM, env.INQUIRY_TO, raw));
}
