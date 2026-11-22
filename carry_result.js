/* site/console/carry_result.js -- CI (the operator's ball, 21 Nov 2026): "Check a run" carries its result into the inquiry.
 *
 * The home page check builds the "Want this for every run? Inquire" link with inquiryHref(result). The link opens
 * /inquiries with the processor, the window, the qubits and a one-line summary in the URL fragment. A fragment is never
 * sent to the server, so nothing leaves the browser until the visitor presses send. A sessionStorage copy covers a
 * fragment lost to a redirect.
 *
 * On /inquiries this file runs by itself when the page has #carry-group: it reads the carried fields, writes them
 * into editable fields, shows one line saying where they came from, and clears the fragment and the stored copy.
 * The Continue link (data-carry-continue) then carries the fields as edited, again in a fragment, to the NDA-gated
 * form, which reads them with the same readCarried(). Nothing is submitted from /inquiries.
 *
 * Only the four named fields travel. Each value is checked against a strict shape and anything key-like is dropped,
 * so a token can never ride along even if a caller passes one. Works in the browser (window.QIACarry) and in Node
 * (require) for the tests.
 *
 * FW-007 (22 Nov 2026, privacy first: no personal data in any URL):
 *  - Any value holding an @ or a phone-shaped run of digits is dropped (dates and times in the check's own shape are not
 *    phone numbers and survive).
 *  - Continue carries only what the home page generated: each field as it arrived or not at all (qubits: the carried
 *    ones kept). Anything the visitor typed stays on /inquiries.
 *  - Continue carries nothing at all unless its link has data-carry-reads, which says the target page reads the fragment
 *    and clears it (fillInquiry + clearCarried). indahl.ai/contact does not yet, so the link stays bare.
 *  - The sessionStorage copy is written when Inquire is clicked (storeOnClick), not when the result renders.
 *
 * FW-014 (22 Nov 2026, money path): the carry lands on indahl.ai/contact. That form had no field for it, so the page
 * gets a "From your check" group (id="contact-carry", hidden until filled) with three read-only fields named
 * carry_processor, carry_window and carry_finding, and a Remove button (data-carry-remove). On load, fillContact reads
 * the fragment (or the same-tab copy), writes the three fields as text, and clears both. Qubits do not go on. On submit,
 * a carry field goes only as it was filled; anything else in it is blanked. /inquiries' Continue now has
 * data-carry-reads. See site/console/CONTACT_CARRY_SNIPPET.html.
 *
 * FW-019 (22 Nov 2026, the real flow): indahl.ai/contact is the agreements gate, not the form. The form is /inquiry,
 * reached after the agreements and the identity check, so a carry read and cleared at /contact would be lost. Now:
 *  - /contact (page marked data-carry-gate): holdAtGate reads the fragment, clears it, and keeps the carry in
 *    indahl.ai's sessionStorage (same tab only) under qia-carry-hold with the time it was held. An optional
 *    #carry-held line shows that a check is held, with its own Remove.
 *  - /inquiry (page with the "From your check" group, id="contact-carry"): fillContact fills the three read-only
 *    fields from the hold (or from a fragment, if one arrives there). The hold stays until the form is submitted or
 *    Remove is pressed, and it is dropped after 30 minutes from the moment it was held.
 *  - Server side: the three fields go into inquire.js FIELDS with the same shape checks, into the notify() email
 *    body, and never into any URL. Patch for the operator: site/console/INQUIRE_CARRY_PATCH.md.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) { module.exports = factory(); return; }
  var api = root.QIACarry = factory();
  if (typeof document !== 'undefined' && document.getElementById('carry-group')) {   // /inquiries (loaded with defer)
    api.fillInquiry(document, window); api.wireContinue(document);
  } else if (typeof document !== 'undefined' && document.getElementById('contact-carry')) {   // indahl.ai/inquiry (FW-019)
    api.fillContact(document, window); api.wireContact(document, window);
  } else if (typeof document !== 'undefined' && document.querySelector('[data-carry-gate]')) {   // indahl.ai/contact gate (FW-019)
    api.holdAtGate(document, window); api.wireGate(document, window);
  }
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var PREFIX = 'qia-carry=';
  var STORE_KEY = 'qia-carry';
  var HOLD_KEY = 'qia-carry-hold';          // FW-019: indahl.ai same-tab hold between the /contact gate and /inquiry
  var HOLD_MS = 30 * 60 * 1000;             // dropped 30 minutes after it was held
  var MAX = { processor: 40, time: 40, qubits: 200, summary: 280 };

  // Anything that looks like a credential: named like one, or a long unbroken run of key characters.
  var KEYLIKE = [
    /\b(?:api[_-]?key|apikey|token|secret|bearer|password|passwd|authorization)\b/i,
    /\bcrn:/i,
    /[A-Za-z0-9_\-+/=]{32,}/,
  ];

  function keyLike(s) {
    for (var i = 0; i < KEYLIKE.length; i++) if (KEYLIKE[i].test(s)) return true;
    return false;
  }

  // Personal data never rides in a URL: any @ (an email address), or a phone-shaped run of 7 or more digits joined only
  // by spaces, dots, dashes, slashes or brackets. Dates and times in the check's own ISO shape are taken out first.
  var ISO_DT = /\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d{1,6})?)?(?:Z|[+-]\d{2}:?\d{2})?)?/g;
  var PHONE = /\+?\d(?:[\s().\/\-]{0,2}\d){6,}/;
  function personal(s) {
    if (s.indexOf('@') !== -1 || s.indexOf('\uff20') !== -1) return true;
    return PHONE.test(s.replace(ISO_DT, ' '));
  }

  function cleanText(v, max) {
    if (typeof v !== 'string' && typeof v !== 'number') return '';
    var s = String(v).replace(/[\u0000-\u001f\u007f<>]/g, ' ').replace(/\s+/g, ' ').trim();
    if (!s || s.length > max || keyLike(s) || personal(s)) return '';
    return s;
  }

  function cleanProcessor(v) {
    var s = cleanText(v, MAX.processor);
    return /^[A-Za-z0-9][A-Za-z0-9_.\-]*$/.test(s) ? s : '';
  }

  // ISO 8601 date-time (or date) only, as the check reports its window.
  function cleanTime(v) {
    var s = cleanText(v, MAX.time);
    return /^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d{1,6})?)?(?:Z|[+-]\d{2}:?\d{2})?)?$/.test(s) ? s : '';
  }

  function cleanQubits(v) {
    var list = Array.isArray(v) ? v : (typeof v === 'string' ? v.split(/[\s,]+/) : []);
    var out = [];
    for (var i = 0; i < list.length && out.length < MAX.qubits; i++) {
      var t = String(list[i]).trim();
      if (!/^\d{1,4}$/.test(t)) continue;
      var n = parseInt(t, 10);
      if (out.indexOf(n) === -1) out.push(n);
    }
    return out;
  }

  // The only shape that travels: {processor, start, end, qubits, summary}. Unknown fields are dropped.
  function pick(result) {
    result = result || {};
    var w = result.window || {};
    return {
      processor: cleanProcessor(result.processor),
      start: cleanTime(result.start != null ? result.start : w.start),
      end: cleanTime(result.end != null ? result.end : w.end),
      qubits: cleanQubits(result.qubits),
      summary: cleanText(result.summary, MAX.summary),
    };
  }

  function isEmpty(c) {
    return !c.processor && !c.start && !c.end && !c.qubits.length && !c.summary;
  }

  function encode(c) {
    var p = [];
    if (c.processor) p.push('p=' + encodeURIComponent(c.processor));
    if (c.start) p.push('s=' + encodeURIComponent(c.start));
    if (c.end) p.push('e=' + encodeURIComponent(c.end));
    if (c.qubits.length) p.push('q=' + encodeURIComponent(c.qubits.join(',')));
    if (c.summary) p.push('m=' + encodeURIComponent(c.summary));
    return p.join('&');
  }

  function decode(s) {
    var raw = {};
    String(s || '').split('&').forEach(function (kv) {
      var i = kv.indexOf('=');
      if (i < 1) return;
      try { raw[kv.slice(0, i)] = decodeURIComponent(kv.slice(i + 1).replace(/\+/g, ' ')); } catch (e) { /* bad escape: skip */ }
    });
    return pick({ processor: raw.p, start: raw.s, end: raw.e, qubits: raw.q, summary: raw.m });
  }

  // Home page: the href for the Inquire link under a result. Writes nothing; storeOnClick keeps the same-tab copy.
  function inquiryHref(result, opts) {
    opts = opts || {};
    var base = opts.base || '/inquiries';
    var c = pick(result);
    if (isEmpty(c)) return base;
    return base + '#' + PREFIX + encode(c);
  }

  // Keep the same-tab copy (for a fragment lost to a redirect) only when the visitor clicks Inquire, so a run that was
  // only looked at never turns up later on /inquiries.
  function remember(result, store) {
    var c = pick(result);
    if (!store || isEmpty(c)) return false;
    try { store.setItem(STORE_KEY, encode(c)); return true; } catch (e) { return false; }
  }
  function storeOnClick(a, result, opts) {
    opts = opts || {};
    if (!a || !a.addEventListener) return;
    a.addEventListener('click', function () { remember(result, opts.storage !== undefined ? opts.storage : safeSession()); });
  }

  // Inquiries page: read the carried fields from the fragment, else the stored copy. Returns null when none.
  function readCarried(loc, store) {
    var hash = (loc && loc.hash) || '';
    var payload = '';
    if (hash.indexOf('#' + PREFIX) === 0) payload = hash.slice(1 + PREFIX.length);
    else if (store) { try { payload = store.getItem(STORE_KEY) || ''; } catch (e) { payload = ''; } }
    if (!payload) return null;
    var c = decode(payload);
    return isEmpty(c) ? null : c;
  }

  function clearCarried(loc, hist, store) {
    if (store) { try { store.removeItem(STORE_KEY); } catch (e) { /* ignore */ } }
    if (loc && hist && hist.replaceState && (loc.hash || '').indexOf('#' + PREFIX) === 0) {
      hist.replaceState(null, '', (loc.pathname || '') + (loc.search || ''));
    }
  }

  // Text for each form field, as the visitor will see and edit it.
  function fieldText(c) {
    return {
      processor: c.processor,
      window: c.start && c.end ? c.start + ' to ' + c.end : (c.start || c.end || ''),
      qubits: c.qubits.join(', '),
      summary: c.summary,
    };
  }

  var NOTE = 'Filled in from the run checked on the home page. Continue takes these lines to the inquiry form as checked. A line changed here stays on this page.';
  var NOTE_STAYS = 'Filled in from the run checked on the home page. Nothing here is sent: copy what you need into the inquiry form on the next page.';
  var carried = null;   // what arrived from the home page, so Continue can tell an edited summary from the generated one

  function continueReads(doc) {
    var a = doc && doc.querySelector ? doc.querySelector('a[data-carry-continue]') : null;
    return !!(a && a.hasAttribute && a.hasAttribute('data-carry-reads'));
  }

  // Inquiries page entry point. Fields are found by name="carry_<field>" inside the form; the note goes in
  // the element with id="carry-note". Values are written as text (.value / .textContent), never as HTML.
  function fillInquiry(doc, win) {
    win = win || (typeof window !== 'undefined' ? window : null);
    if (!doc || !win) return null;
    var store = safeSession(win);
    var c = readCarried(win.location, store);
    clearCarried(win.location, win.history, store);
    if (!c) return null;
    carried = c;
    var t = fieldText(c);
    var filled = 0;
    Object.keys(t).forEach(function (k) {
      if (!t[k]) return;
      var el = doc.querySelector('[name="carry_' + k + '"]');
      if (el) { el.value = t[k]; filled++; }
    });
    var group = doc.getElementById('carry-group');
    if (group && filled) group.hidden = false;
    var note = doc.getElementById('carry-note');
    if (note && filled) { note.textContent = continueReads(doc) ? NOTE : NOTE_STAYS; note.hidden = false; }
    return t;
  }

  function utcMin(ms) {
    var d = new Date(ms);
    return isNaN(d.getTime()) ? '' : d.toISOString().slice(0, 16).replace('T', ' ') + ' UTC';
  }

  // One line on what the check found, from check_run.js's result object (record in force, flags, records during the run).
  function summarize(r, opts) {
    opts = opts || {};
    if (!r || !r.under) return 'No record in the mirror was in force at the run start.';
    var parts = [], start = opts.start;
    var age = start != null && r.under.stamp != null ? (start - r.under.stamp) / 3600000 : null;
    parts.push('Record in force stamped ' + utcMin(r.under.stamp) + (age != null && isFinite(age) ? ', ' + age.toFixed(1) + ' h before the start' : ''));
    var flags = r.flags || [], by = {}, order = [];
    flags.forEach(function (f) { var k = String(f.outcome || f.check || 'flag').replace('_', ' '); if (!by[k]) { by[k] = 0; order.push(k); } by[k]++; });
    parts.push(flags.length ? flags.length + ' flag' + (flags.length === 1 ? '' : 's') + ' (' + order.map(function (k) { return by[k] + ' ' + k; }).join(', ') + ')' : 'no flags');
    var dur = (r.during || []).length, ch = (r.changes || []).length;
    parts.push(dur ? dur + ' record' + (dur === 1 ? '' : 's') + ' stamped during the run, ' + ch + ' figure' + (ch === 1 ? '' : 's') + ' changed' : 'no record stamped during the run');
    var line = parts.join('; ') + '.';
    return line.length <= MAX.summary ? line : line.slice(0, MAX.summary - 1).replace(/[;,]?\s*\S*$/, '') + '.';
  }

  // The fields as the visitor left them on /inquiries, in the shape that travels. Only what the home page generated may
  // travel: each field goes on as it arrived or not at all (qubits: the carried ones the visitor kept). Anything the
  // visitor typed, even in a strict-shaped field, could be a name or a number, and it never goes into a URL.
  function readFields(doc, from) {
    from = from === undefined ? carried : from;
    if (!from) return pick({});
    function v(n) { var el = doc.querySelector('[name="carry_' + n + '"]'); return el ? String(el.value).replace(/\s+/g, ' ').trim() : ''; }
    var w = v('window').split(/\s+to\s+/);
    var kept = cleanQubits(v('qubits')).filter(function (n) { return from.qubits.indexOf(n) !== -1; });
    return pick({
      processor: v('processor') === from.processor ? from.processor : '',
      start: w[0] === from.start ? from.start : '',
      end: (w[1] || '') === from.end ? from.end : '',
      qubits: kept,
      summary: v('summary') === from.summary ? from.summary : '',
    });
  }

  // Continue carries nothing unless the link says its target reads and clears the fragment (data-carry-reads).
  function wireContinue(doc) {
    var a = doc.querySelector('a[data-carry-continue]');
    if (!a) return;
    var base = a.getAttribute('href').split('#')[0];
    var reads = a.hasAttribute ? a.hasAttribute('data-carry-reads') : false;
    a.setAttribute('href', base);
    if (!reads) return;
    a.addEventListener('click', function () {
      var c = readFields(doc);
      a.setAttribute('href', isEmpty(c) ? base : base + '#' + PREFIX + encode(c));
    });
  }

  // ---------- indahl.ai: /contact gate holds, /inquiry fills (FW-014, reworked FW-019) ----------
  var CONTACT_FIELDS = ['processor', 'window', 'finding'];
  var contactCarried = null;   // what was filled, so submit can tell a filled value from anything else

  function contactText(c) {
    var t = fieldText(c);
    return { processor: t.processor, window: t.window, finding: t.summary };
  }
  function contactEl(doc, k) { return doc.querySelector('[name="carry_' + k + '"]'); }
  function nowMs(now) { return typeof now === 'number' ? now : Date.now(); }

  // The hold: {"v": <encoded carry>, "t": <ms held>}. Anything stale, unreadable or empty is removed and reads as none.
  function readHeld(store, now) {
    if (!store) return null;
    var raw = null;
    try { raw = store.getItem(HOLD_KEY); } catch (e) { return null; }
    if (!raw) return null;
    var h = null;
    try { h = JSON.parse(raw); } catch (e) { h = null; }
    var t = h && typeof h.t === 'number' ? h.t : NaN;
    var age = nowMs(now) - t;
    var c = h && typeof h.v === 'string' && isFinite(age) && age >= 0 && age <= HOLD_MS ? decode(h.v) : null;
    if (!c || isEmpty(c)) { dropHeld(store); return null; }
    return c;
  }
  function dropHeld(store) {
    if (store) { try { store.removeItem(HOLD_KEY); } catch (e) { /* ignore */ } }
  }
  function fragmentCarry(loc) {
    var hash = (loc && loc.hash) || '';
    if (hash.indexOf('#' + PREFIX) !== 0) return null;
    var c = decode(hash.slice(1 + PREFIX.length));
    return isEmpty(c) ? null : c;
  }

  // /contact gate entry point: take the fragment, clear it from the address bar, and hold it for /inquiry in this tab.
  // With no fragment, an earlier hold is kept (the visitor may come back to the gate) unless it has gone stale.
  function holdAtGate(doc, win, now) {
    win = win || (typeof window !== 'undefined' ? window : null);
    if (!win) return null;
    var store = safeSession(win);
    var c = fragmentCarry(win.location);
    clearCarried(win.location, win.history, null);
    if (c && store) {
      try { store.setItem(HOLD_KEY, JSON.stringify({ v: encode(c), t: nowMs(now) })); } catch (e) { /* storage blocked: nothing held */ }
    }
    var held = readHeld(store, now);
    var line = doc && doc.getElementById ? doc.getElementById('carry-held') : null;
    if (line) line.hidden = !held;
    return held;
  }

  // Remove on the gate: drop the hold and hide the line.
  function wireGate(doc, win) {
    var line = doc && doc.getElementById ? doc.getElementById('carry-held') : null;
    var b = line && line.querySelector ? line.querySelector('[data-carry-remove]') : null;
    if (b && b.addEventListener) b.addEventListener('click', function (ev) {
      if (ev && ev.preventDefault) ev.preventDefault();
      dropHeld(safeSession(win)); line.hidden = true;
    });
  }

  // /inquiry entry point: fill the three read-only fields from a fragment (cleared) or else the hold (kept until submit,
  // Remove, or 30 minutes). The FW-007 same-tab copy is cleared too.
  function fillContact(doc, win, now) {
    win = win || (typeof window !== 'undefined' ? window : null);
    if (!doc || !win) return null;
    var store = safeSession(win);
    var c = fragmentCarry(win.location);
    clearCarried(win.location, win.history, store);
    if (c && store) { try { store.setItem(HOLD_KEY, JSON.stringify({ v: encode(c), t: nowMs(now) })); } catch (e) { /* ignore */ } }
    if (!c) c = readHeld(store, now);
    contactCarried = null;
    if (!c) return null;
    var t = contactText(c), filled = 0;
    CONTACT_FIELDS.forEach(function (k) {
      var el = contactEl(doc, k);
      if (!el) return;
      el.value = t[k] || '';
      if (el.setAttribute) el.setAttribute('readonly', '');
      if (t[k]) filled++;
    });
    if (!filled) return null;
    contactCarried = t;
    var group = doc.getElementById('contact-carry');
    if (group) group.hidden = false;
    return t;
  }

  // Remove: empty the three fields, hide the group and drop the hold, so nothing from the check is sent.
  function removeContact(doc, win) {
    CONTACT_FIELDS.forEach(function (k) { var el = contactEl(doc, k); if (el) el.value = ''; });
    contactCarried = null;
    var group = doc.getElementById('contact-carry');
    if (group) group.hidden = true;
    dropHeld(safeSession(win));
  }

  // Submit: each carry field goes only exactly as it was filled; anything else in it is blanked. Returns what goes.
  function guardContact(doc, from) {
    from = from === undefined ? contactCarried : from;
    var out = {};
    CONTACT_FIELDS.forEach(function (k) {
      var el = contactEl(doc, k);
      if (!el) return;
      if (!from || el.value !== from[k]) el.value = '';
      out[k] = el.value;
    });
    return out;
  }

  function wireContact(doc, win) {
    var b = doc.querySelector('[data-carry-remove]');
    if (b && b.addEventListener) b.addEventListener('click', function (ev) { if (ev && ev.preventDefault) ev.preventDefault(); removeContact(doc, win); });
    var group = doc.getElementById('contact-carry');
    var form = group && group.closest ? group.closest('form') : null;
    if (form && form.addEventListener) form.addEventListener('submit', function () { guardContact(doc); dropHeld(safeSession(win)); });
  }

  function safeSession(win) {
    win = win || (typeof window !== 'undefined' ? window : null);
    try { return win && win.sessionStorage ? win.sessionStorage : null; } catch (e) { return null; }
  }

  return {
    pick: pick, encode: encode, decode: decode, keyLike: keyLike, personal: personal,
    inquiryHref: inquiryHref, remember: remember, storeOnClick: storeOnClick, readCarried: readCarried, clearCarried: clearCarried,
    fieldText: fieldText, fillInquiry: fillInquiry, NOTE: NOTE, NOTE_STAYS: NOTE_STAYS, PREFIX: PREFIX, STORE_KEY: STORE_KEY,
    summarize: summarize, readFields: readFields, wireContinue: wireContinue,
    fillContact: fillContact, removeContact: removeContact, guardContact: guardContact, wireContact: wireContact,
    CONTACT_FIELDS: CONTACT_FIELDS,
    holdAtGate: holdAtGate, wireGate: wireGate, readHeld: readHeld, dropHeld: dropHeld, HOLD_KEY: HOLD_KEY, HOLD_MS: HOLD_MS,
  };
}));
