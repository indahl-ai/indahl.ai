// inquire.js -- the indahl.ai inquiry gate (23 Oct 2026).
// POST /inquire from the form on /contact. 24 Oct 2026: engagement inquiries need the signed WorkOS session from gate.js and an
// accepted NDA (the version and SHA-256 served at /nda.txt); without both, nothing is stored. Privacy requests and security reports
// now use the same form and the same checks. Filters: organizational email only (personal mail
// domains refused), a honeypot field, a minimum fill time, field length limits, and a per-visitor rate limit. Accepted inquiries are
// stored in the private KV namespace INDAHL_INQUIRIES (key inq:<ISO time>:<random>); only the country is kept, never the raw IP.
// Read them with the inquiries reader (internal).

import { EmailMessage } from 'cloudflare:email';
import { session, agreement, FREEMAIL, viaQia, clientIp, clientCountry } from './gate.js';

// 22 Nov 2026 (FW-019, the designer; wired by the operator): carry fields from the Check a run on quantumidleaudit.com, read-only on /inquiry.
// Optional. A value that fails its shape is dropped (stored empty), never cut or rewritten. They go only in KV and the notice email, never a URL.
const CARRY_MAX = { carry_processor: 40, carry_window: 60, carry_finding: 280 };
const ISO = '\\d{4}-\\d{2}-\\d{2}(?:[T ]\\d{2}:\\d{2}(?::\\d{2}(?:\\.\\d{1,6})?)?(?:Z|[+-]\\d{2}:?\\d{2})?)?';
const ISO_RE = new RegExp('^' + ISO + '(?: to ' + ISO + ')?$');
const ISO_G = new RegExp(ISO, 'g');
const PHONE = /\+?\d(?:[\s().\/\-]{0,2}\d){6,}/;
const KEYLIKE = [/\b(?:api[_-]?key|apikey|token|secret|bearer|password|passwd|authorization)\b/i, /\bcrn:/i, /[A-Za-z0-9_\-+/=]{32,}/];
function carryClean(name, v) {
  if (typeof v !== 'string') return '';
  const s = v.replace(/[\u0000-\u001f\u007f]/g, ' ').replace(/\s+/g, ' ').trim();
  if (!s || s.length > CARRY_MAX[name] || /[<>@＠]/.test(s)) return '';
  if (KEYLIKE.some((re) => re.test(s)) || PHONE.test(s.replace(ISO_G, ' '))) return '';
  if (name === 'carry_processor') return /^[A-Za-z0-9][A-Za-z0-9_.\-]*$/.test(s) ? s : '';
  if (name === 'carry_window') return ISO_RE.test(s) ? s : '';
  return s;
}
const SUBJECTS = ['Quick check ($50 to $100)', 'Full audit ($500)', '30-day pilot ($2,500)', 'Monitoring subscription ($2,500 a month)', 'Other'];   // 22 Nov (the owner): ONE form for both sites (quantumidleaudit.com/inquiries hands off here); every paid offer on either site, no audience split
const FIELDS = { reason: 300, name: 120, email: 160, organisation: 160, role: 120, scope: 3000, timeline: 40, referral: 300 };
// 19 Nov 2026: the reason is free text now; the subject line still flags privacy and security requests by keyword.

async function sha(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].slice(0, 12).map(x => x.toString(16).padStart(2, '0')).join('');
}

export async function handleInquiry(req, env, render) {
  const reject = (msg, status = 400) => render(msg, status);
  if (req.method !== 'POST') return reject('Please use the inquiry form on the contact page.', 405);
  if (!env.INDAHL_INQUIRIES) return reject('Inquiries are temporarily unavailable. Please try again later.', 503);
  const len = Number(req.headers.get('content-length') || 0);
  if (len > 20000) return reject('That submission is too long.', 413);
  // 23 Nov 2026 (the designer review #14): content-length can be left out (a chunked body), so the body is read with a real byte cap first.
  let f, raw;
  try { raw = await req.arrayBuffer(); } catch (e) { return reject('That submission could not be read.'); }
  if (raw.byteLength > 20000) return reject('That submission is too long.', 413);
  try { f = await new Request('https://form.local/', { method: 'POST', headers: { 'content-type': req.headers.get('content-type') || '' }, body: raw }).formData(); } catch (e) { return reject('That submission could not be read.'); }
  if ((f.get('website') || '').trim()) return render(null, 200);                 // honeypot: look accepted, store nothing
  const started = Number(f.get('t') || 0);
  if (!started || Date.now() - started < 3000) return reject('That went through too quickly. Please wait a moment and submit again.');
  const rec = {};
  for (const [k, max] of Object.entries(FIELDS)) {
    const v = String(f.get(k) || '').trim();
    if (v.length > max) return reject(`The ${k} field is too long.`);
    rec[k] = v;
  }
  for (const k of Object.keys(CARRY_MAX)) rec[k] = carryClean(k, f.get(k));
  // 22 Nov 2026 (the owner): the subject is one of three; no budget is asked. Privacy and security requests come under Other, flagged by keyword in the scope.
  if (!SUBJECTS.includes(rec.reason)) return reject('Please choose a subject.');
  const kind = /privacy/i.test(rec.scope || '') ? 'privacy' : /security|vulnerab/i.test(rec.scope || '') ? 'security' : 'engagement';
  const engagement = true;   // 26 Oct 2026: one inquiry form for everything; every reason goes through the agreements and the identity check
  let who = null, ag = null;
  if (engagement) {
    ag = await agreement(req, env);
    if (!ag) return reject('The agreements have not been accepted in this browser, or have expired. Please start again from the contact page.', 401);
    who = await session(req, env);
    if (!who) return reject('Please verify your identity before submitting.', 401);
    rec.email = who.e;                                                                     // the verified address, never the form's
  }
  // 23 Oct full pass: privacy requests and security reports must be possible from any address and without NDA authority.
  for (const k of (engagement ? ['name', 'email', 'organisation', 'role', 'scope'] : ['name', 'email', 'scope'])) if (!rec[k]) return reject('Please complete every required field.');
  if (!engagement && f.get('privacy') !== 'yes') return reject('Please confirm you have read the privacy notice.');
  const m = rec.email.toLowerCase().match(/^[^\s@]+@([a-z0-9.-]+\.[a-z]{2,})$/);
  if (!m) return reject('Please give a valid email address.');
  if (engagement && FREEMAIL.has(m[1])) return reject('Please write from your organization’s email address. Inquiries from personal email services are not reviewed.');
  const ip = clientIp(req, env);   // 23 Nov 2026: the visitor's IP on a quantumidleaudit.com forward (gate.js viaQia), else cf-connecting-ip
  // 23 Nov 2026 (the designer review #14): 3 an hour per visitor, held strictly by the Limiter Durable Object (the KV read-then-write let a burst
  // through). Without the binding it falls back to the old KV counter.
  if (env.LIMITER) {
    const lr = await env.LIMITER.get(env.LIMITER.idFromName('inq:' + await sha(ip))).fetch('https://limiter/?limit=3&win=3600');
    if (lr.status === 429) return reject('We have received several inquiries from you recently. Please wait before sending another.', 429);
  } else {
    const rk = 'rate:' + await sha(ip + '|' + new Date().toISOString().slice(0, 13));
    const n = Number(await env.INDAHL_INQUIRIES.get(rk) || 0);
    if (n >= 3) return reject('We have received several inquiries from you recently. Please wait before sending another.', 429);
    await env.INDAHL_INQUIRIES.put(rk, String(n + 1), { expirationTtl: 3600 });
  }
  rec.received = new Date().toISOString();
  rec.country = clientCountry(req, env);
  rec.site = viaQia(req, env) ? 'quantumidleaudit.com' : 'indahl.ai';   // which site's form it came from; same store, same inbox
  rec.domain = m[1];
  const key = `inq:${rec.received}:${crypto.randomUUID().slice(0, 8)}`;
  rec.nda_confirmed = engagement;
  if (engagement) {
    rec.identity = { verified_email: who.e, domain: who.d, method: who.m, workos_user: who.u, workos_org: who.o || null, verified_at: new Date(who.iat * 1000).toISOString() };
    const at = new Date(ag.at * 1000).toISOString();
    rec.agreements = { nda: { version: ag.nda, accepted_at: at, accepted_by: rec.name, title: rec.role, organisation: rec.organisation, authority_confirmed: true },
      privacy: { version: ag.privacy, agreed_at: at }, terms: { version: ag.terms || null, agreed_at: at }, both_read_to_end: ag.read === true };   // 30 Oct site pass: the Terms version accepted is kept too
  }
  await env.INDAHL_INQUIRIES.put(key, JSON.stringify(rec), { expirationTtl: 63072000 });   // 24 months, as the privacy notice states
  // 21 Nov 2026 (money-path check): notify() read `kind` from this function's scope, so since the 19 Nov free-text change every notice email
  // threw a ReferenceError and the inquiry sat in KV with no mail. kind is passed now; a failure still leaves notify-failed:<key>, which
  // ledger/inquiry_bell.py rings into sagar/pipeline/pipe.log (the doorbell) with every new inquiry.
  try { await notify(env, rec, key, kind); } catch (e) { await env.INDAHL_INQUIRIES.put('notify-failed:' + key, String(e && e.message || e)); }
  return render(null, 200);
}

// Email notice of an accepted inquiry. The destination lives only in the worker's private config (send_email binding + vars);
// it never appears on a page or in this source. Header values are stripped of line breaks so form text cannot inject headers.
async function notify(env, rec, key, kind) {
  if (!env.INQUIRY_MAIL || !env.INQUIRY_TO || !env.INQUIRY_FROM) throw new Error('mail binding or address missing');   // 21 Nov 2026: was a silent return (no mail, no record)
  const h = v => String(v || '').replace(/[\r\n]+/g, ' ').slice(0, 200);
  const body = [
    `New engagement inquiry (${rec.received}, ${rec.country || 'country unknown'})`, '',
    `Name: ${rec.name}`, `Role: ${rec.role}`, `Organisation: ${rec.organisation} (${rec.domain})`, `Email: ${rec.email}`,
    `Subject: ${rec.reason}`, `Referred by: ${rec.referral || '-'}`, `Sent from: ${rec.site || 'indahl.ai'}`, (rec.agreements ? `AGREEMENTS: NDA v${rec.agreements.nda.version} and Privacy Notice ${rec.agreements.privacy.version} read to the end (Terms ${rec.agreements.terms.version}) and checked at ${rec.agreements.nda.accepted_at} by ${rec.agreements.nda.accepted_by}, ${rec.agreements.nda.title}, for ${rec.agreements.nda.organisation} (authority confirmed). Identity verified: ${rec.identity.verified_email} via ${rec.identity.method}.` : 'Agreements: not required for this reason'), '',
    'Scope, in their words:', rec.scope, '',
    ...((rec.carry_processor || rec.carry_window || rec.carry_finding) ? ['From the Check a run (generated on quantumidleaudit.com, read-only on the form):', `Processor: ${rec.carry_processor || '-'}`, `Run window, UTC: ${rec.carry_window || '-'}`, `Finding: ${rec.carry_finding || '-'}`, ''] : []),
    `Timeline: ${rec.timeline || 'not stated'}`, '',
    `Stored as ${key}. Read all with the inquiries reader.`,
  ].join('\r\n');
  const raw = [
    `From: Indahl inquiries <${env.INQUIRY_FROM}>`, `To: <${env.INQUIRY_TO}>`, `Reply-To: ${h(rec.email)}`,
    `Subject: ${kind === 'engagement' ? 'Inquiry' : kind === 'privacy' ? 'PRIVACY REQUEST' : 'SECURITY REPORT'}: ${h(rec.organisation || rec.name)} (${h(rec.domain)})`, `Date: ${new Date().toUTCString()}`,
    `Message-ID: <${crypto.randomUUID()}@indahl.ai>`, 'MIME-Version: 1.0', 'Content-Type: text/plain; charset=utf-8',
    'Content-Transfer-Encoding: 8bit', '', body,
  ].join('\r\n');
  await env.INQUIRY_MAIL.send(new EmailMessage(env.INQUIRY_FROM, env.INQUIRY_TO, raw));
}
