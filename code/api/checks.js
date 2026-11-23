// checks.js (14 Nov 2026): the PKGLICENSE, PKGINSTALL, HFLICENSE and HFSIZE desk rules, run on one package or model a person names.
// Refereed before release by the outside referee on our work (14 Nov 2026). She asked for the row-by-row parity run against the desks
// (ALL IDENTICAL on 3,082 rows) and caught "files pip can install" overclaiming when a release carries only platform wheels.
// The desks read the 1,000 most downloaded. These tools read any name, live, with the same family rules and the same three classes:
// AGREE, DISAGREE, NOT_COMPARABLE (with the reason). Rules ported from pkglicense_tick.py, hflicense_tick.py and hfsize_tick.py, planted
// pairs included (CHECKS_SELFTEST below runs them).
const UA = 'indahl.ai on-demand checks (https://indahl.ai/contact)';
const j = async (url) => { try { const r = await fetch(url, { headers: { 'user-agent': UA, accept: 'application/json' }, cf: { cacheTtl: 900 } }); return { status: r.status, body: r.ok ? await r.json() : null }; } catch (e) { return { status: null, body: null }; } };
const t = async (url) => { try { const r = await fetch(url, { headers: { 'user-agent': UA }, cf: { cacheTtl: 900 } }); return r.ok ? await r.text() : null; } catch (e) { return null; } };

// ---- package license family (pkglicense_tick.py fam/compare) ----
export function famPkg(s) {
  const x = String(s || '').toLowerCase().trim(); if (!x) return null;
  if (/\bagpl|affero/.test(x)) return 'AGPL';
  if (/\blgpl|lesser general/.test(x)) return 'LGPL';
  if (/\bgpl|general public license/.test(x)) { if (/(-|v|version\s*|\s)3(\.0)?\b|v3/.test(x)) return 'GPL-3.0'; if (/(-|v|version\s*|\s)2(\.0)?\b|v2/.test(x)) return 'GPL-2.0'; return 'GPL'; }
  if (/\b0?bsd|berkeley/.test(x)) return 'BSD';
  if (/\bapache/.test(x)) return 'Apache-2.0';
  if (/\bmit\b/.test(x)) return 'MIT';
  if (/\bisc\b/.test(x)) return 'ISC';
  if (/\bmpl|mozilla/.test(x)) return 'MPL-2.0';
  if (/\bpsf|python software foundation/.test(x)) return 'PSF';
  if (/unlicense/.test(x)) return 'Unlicense';
  if (/\bcc0|creative commons zero/.test(x)) return 'CC0';
  return 'OTHER';
}
const famset = (parts) => new Set(parts.map(famPkg).filter(Boolean));
const gplEq = (a, b) => a === b || (a === 'GPL' && (b === 'GPL-2.0' || b === 'GPL-3.0')) || (b === 'GPL' && (a === 'GPL-2.0' || a === 'GPL-3.0'));
export function comparePkg(stated, repo) {
  const S = [...stated].filter(f => f !== 'OTHER'), R = [...repo].filter(f => f !== 'OTHER');
  if (!S.length || !R.length) return 'NOT_COMPARABLE';
  return S.some(a => R.some(b => gplEq(a, b))) ? 'AGREE' : 'DISAGREE';
}
// ---- license text family (hflicense_tick.py fam_text), used on a repository’s license file ----
export function famText(txt) {
  const x = String(txt || '').toLowerCase().replace(/\s+/g, ' '), hd6 = x.slice(0, 600);
  if (/^\s*(attribution|cc0|creative commons)/.test(hd6) || hd6.includes('creative commons') || /attribution[\w\- ]*\s\d\.\d|\bcc by\b|\bcc-by\b/.test(hd6)) {
    if (hd6.includes('cc0') || (hd6.includes('zero') && hd6.includes('universal'))) return 'CC0';
    if (hd6.includes('attribution')) { const u = hd6.replace(/[- ]/g, ''); return 'CC-BY' + (u.includes('noncommercial') ? '-NC' : '') + (u.includes('sharealike') ? '-SA' : '') + (u.includes('noderivatives') ? '-ND' : ''); }
  }
  if (x.includes('apache license') && x.includes('version 2.0')) return 'Apache-2.0';
  if (x.includes('mozilla public license')) return 'MPL-2.0';
  const hd = x.slice(0, 400);
  if (hd.includes('gnu affero')) return 'AGPL';
  if (hd.includes('gnu lesser general public')) return 'LGPL';
  if (hd.includes('gnu general public license')) return hd.includes('version 3') ? 'GPL-3.0' : hd.includes('version 2') ? 'GPL-2.0' : 'GPL';
  if (x.includes('permission is hereby granted, free of charge')) return 'MIT';
  if (x.includes('redistribution and use in source and binary forms')) return 'BSD';
  if (x.includes('permission to use, copy, modify, and/or distribute this software for any purpose with or without fee')) return 'ISC';
  if (x.includes('this is free and unencumbered software')) return 'Unlicense';
  return 'OTHER';
}
// ---- model card license tag family (hflicense_tick.py fam_tag/compare) ----
export function famTag(tag) {
  const x = String(tag || '').toLowerCase().trim();
  if (!x || ['other', 'unknown', 'none'].includes(x) || /openrail|llama|gemma|bigscience|creativeml|falcon|deepseek|qwen|license|agreement/.test(x)) return 'OTHER';
  if (x.startsWith('cc0')) return 'CC0';
  if (x.startsWith('cc-by')) return 'CC-BY' + (x.includes('-nc') ? '-NC' : '') + (x.includes('-sa') ? '-SA' : '') + (x.includes('-nd') ? '-ND' : '');
  if (x.startsWith('agpl')) return 'AGPL'; if (x.startsWith('lgpl')) return 'LGPL';
  if (x.startsWith('gpl')) return x.includes('3') ? 'GPL-3.0' : x.includes('2') ? 'GPL-2.0' : 'GPL';
  if (x.startsWith('apache')) return 'Apache-2.0'; if (x.startsWith('bsd') || x === '0bsd') return 'BSD';
  if (x === 'mit') return 'MIT'; if (x === 'isc') return 'ISC'; if (x.startsWith('mpl')) return 'MPL-2.0'; if (x === 'unlicense') return 'Unlicense';
  return 'OTHER';
}
const compareFam = (s, f) => (!s || !f || s === 'OTHER' || f === 'OTHER') ? 'NOT_COMPARABLE' : gplEq(s, f) ? 'AGREE' : 'DISAGREE';
// ---- model size (hfsize_tick.py stated/compare) ----
const PACKED = /awq|gptq|gguf|bnb|[1-8]bit|int4|int8|fp8|fp4|nvfp4|mxfp4|w4a16|w8a8|quantized/i;
const TOK = /(?<![A-Za-z0-9.])(\d+(?:\.\d+)?)([BMbm])(?![A-Za-z])/g;
export function statedSize(name) {
  if (/\d+x\d+(?:\.\d+)?[Bb]/.test(name) || /(?<![A-Za-z0-9])A\d+(?:\.\d+)?B/.test(name)) return [null, 'mixture-of-experts name'];
  const toks = new Set([...name.matchAll(TOK)].map(m => parseFloat(m[1]) * (m[2].toLowerCase() === 'b' ? 1e9 : 1e6)));
  if (!toks.size) return [null, 'no size in the name']; if (toks.size > 1) return [null, 'more than one size in the name'];
  return [[...toks][0], null];
}
export const compareSize = (s, a) => (s == null || a == null) ? 'NOT_COMPARABLE' : (a / s >= 0.70 && a / s <= 1.35 ? 'AGREE' : 'DISAGREE');
const fmt = (x) => x >= 1e9 ? (x / 1e9).toFixed(2) + ' B' : (x / 1e6).toFixed(0) + ' M';
const LICENSE_FILE = (f) => { if (!/^(license|licence|copying)([-_.][\w.-]*)?$/i.test(f)) return false; const tail = f.includes('.') ? f.split('.').pop().toLowerCase() : ''; return ['', 'md', 'txt', 'rst'].includes(tail) || /^\d+$/.test(tail) || !f.includes('.'); };

export async function packageCheck(args) {
  const name = String(args.name || '').trim().replace(/^pip install\s+/i, '').split(/[\s=<>!~\[;]/)[0];
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$/.test(name)) return { error: 'Give a PyPI project name, for example requests.' };
  const r = await j(`https://pypi.org/pypi/${encodeURIComponent(name)}/json`);
  if (r.status === 404) return { name, checks: [{ check: 'PyPI project', outcome: 'NO_RECORD', note: 'PyPI has no project with this name. Check the spelling: a near-miss name that does exist can be someone else’s package.' }] };
  if (!r.body) return { name, checks: [{ check: 'PyPI project', outcome: 'CANNOT_TELL', note: 'PyPI did not answer.' }] };
  const i = r.body.info, out = { name: i.name, version: i.version, pypi: `https://pypi.org/project/${i.name}/`, checks: [] };
  // install: does the newest release carry files, is it yanked, what Python it asks for
  const files = r.body.urls || [], wheels = files.filter(f => f.packagetype === 'bdist_wheel').length, sdists = files.filter(f => f.packagetype === 'sdist').length;
  // 14 Nov (the referee, third pass): files existing is not the same as installable everywhere. An sdist or a py3-none-any wheel installs on any
  // platform. Without one, the release is limited to the platforms its wheels name. No files means pip skips the release.
  const universal = files.some(f => f.packagetype === 'sdist' || /-none-any\.whl$/.test(f.filename || ''));
  const plats = [...new Set(files.filter(f => f.packagetype === 'bdist_wheel').map(f => (String(f.filename).match(/-([^-]+)\.whl$/) || [])[1]).filter(Boolean))].slice(0, 30);
  out.checks.push({ check: 'Newest release carries files', outcome: !files.length ? 'NO_FILES' : i.yanked ? 'YANKED' : universal ? 'AGREE' : 'PLATFORM_LIMITED',
    latest: i.version, wheels, sdists, yanked: !!i.yanked, requires_python: i.requires_python || null, ...(universal || !files.length ? {} : { platforms: plats }),
    note: (!files.length ? 'The newest release has no files, so pip will skip this release.' : i.yanked ? 'The newest release is yanked: ' + (i.yanked_reason || 'no reason given') + '. pip skips it unless pinned.' : universal ? 'The newest release has an sdist or a universal wheel, so pip can install it on any platform.' + (wheels ? '' : ' No wheel, so pip builds from source.') : 'The newest release has wheels only for the platforms listed and no sdist.') + ' requires_python is shown but not checked against any Python version.' });
  // license: stated (expression, classifiers or license field) against the repository’s license
  let parts = [];
  if (i.license_expression) parts = i.license_expression.split(/\s+(?:OR|AND|WITH)\s+|[()]/).filter(x => x.trim());
  else if ((i.classifiers || []).some(c => c.startsWith('License ::'))) parts = i.classifiers.filter(c => c.startsWith('License ::'));
  else if (i.license && i.license.length <= 100) parts = [i.license];
  const urls = i.project_urls || {}, cand = [];
  for (const k of ['Source', 'Repository', 'Code', 'Homepage', 'Source Code', 'GitHub', 'Home']) for (const [kk, v] of Object.entries(urls)) if (kk.toLowerCase() === k.toLowerCase()) cand.push(v);
  cand.push(i.home_page || ''); let repo = null;
  for (const u of cand) { const m = String(u).match(/^https?:\/\/(?:www\.)?github\.com\/([A-Za-z0-9_.-]+)\/([A-Za-z0-9_.-]+?)(?:\.git)?(?:[/#?].*)?$/); if (m) { repo = [m[1], m[2]]; break; } }
  let repoFam = null, why = null, file = null;
  if (!parts.length) why = 'no stated license';
  else if (!repo) why = 'no GitHub repository linked';
  else {
    const api = await j(`https://api.github.com/repos/${repo[0]}/${repo[1]}/license`);
    if (api.body && api.body.license && api.body.license.spdx_id && api.body.license.spdx_id !== 'NOASSERTION') { repoFam = api.body.license.spdx_id; file = api.body.path; }
    else if (api.status === 404) why = 'repository license not detected (or repository not found)';
    else { for (const f of ['LICENSE', 'LICENSE.md', 'LICENSE.txt', 'COPYING', 'LICENSE.rst']) { const tx = await t(`https://raw.githubusercontent.com/${repo[0]}/${repo[1]}/HEAD/${f}`); if (tx) { repoFam = famText(tx); file = f; break; } }
      if (!repoFam) why = 'GitHub did not answer and no license file was found'; }
  }
  if (!why && famPkg(repoFam) === 'OTHER') why = 'the repository license (' + repoFam + ') is not one of the recognized families';
  if (!why && [...famset(parts)].every(f => f === 'OTHER')) why = 'the stated license is not one of the recognized families';
  const cls = why ? 'NOT_COMPARABLE' : comparePkg(famset(parts), famset([repoFam]));
  out.checks.push({ check: 'Stated license against the repository license', outcome: cls, stated: parts, repository: repo ? `https://github.com/${repo[0]}/${repo[1]}` : null, repository_license: repoFam, license_file: file,
    ...(why ? { reason: why } : {}), note: 'Licenses are compared by family (MIT, Apache-2.0, BSD, GPL versions and so on), the rules of the PKGLICENSE desk. The repository license comes from the GitHub API. When GitHub reports no assertion or refuses (it allows 60 unauthenticated requests an hour, shared across many callers), the license file at the default branch is read instead. A repository with several license files can read DISAGREE when the package states one of them.' });
  out.reading = 'AGREE and DISAGREE compare two published statements. NOT_COMPARABLE gives the reason. Neither says whether the license fits your use.';
  return out;
}

export async function modelCheck(args) {
  const raw = String(args.repo || '').trim().replace(/^https?:\/\/huggingface\.co\//i, '').replace(/\/(tree|blob|resolve)\/.*$/, '');
  if (!/^[A-Za-z0-9][\w.-]*\/[\w.-]+$/.test(raw)) return { error: 'Give a Hugging Face model id, for example Qwen/Qwen2.5-7B-Instruct.' };
  const r = await j(`https://huggingface.co/api/models/${raw}?expand[]=safetensors&expand[]=tags&expand[]=siblings&expand[]=cardData`);
  if (r.status === 404 || r.status === 401) return { repo: raw, checks: [{ check: 'Hugging Face model', outcome: r.status === 404 ? 'NO_RECORD' : 'CANNOT_TELL', note: r.status === 404 ? 'Hugging Face has no public model with this id.' : 'Hugging Face answered 401: the model is gated, private or does not exist. It cannot be told apart without signing in.' }] };
  if (!r.body) return { repo: raw, checks: [{ check: 'Hugging Face model', outcome: 'CANNOT_TELL', note: 'Hugging Face did not answer.' }] };
  const m = r.body, out = { repo: m.id || raw, page: `https://huggingface.co/${m.id || raw}`, checks: [] }, name = (m.id || raw).split('/').pop(), tags = (m.tags || []).join(' ');
  // size: the size in the name against the safetensors total
  const st = m.safetensors || {}, tot = st.total || null, psum = Object.values(st.parameters || {}).reduce((a, b) => a + b, 0) || null;
  let cls, why = null, s = null;
  if (PACKED.test(name + ' ' + tags)) { cls = 'NOT_COMPARABLE'; why = 'packed or quantized weights'; }
  else { [s, why] = statedSize(name); if (s == null) cls = 'NOT_COMPARABLE'; else if (!tot) { cls = 'NOT_COMPARABLE'; why = 'no safetensors total'; } else if (psum && tot !== psum) { cls = 'NOT_COMPARABLE'; why = 'Hugging Face total does not match its own breakdown'; } else { cls = compareSize(s, tot); why = null; } }
  out.checks.push({ check: 'Size in the name against the weights', outcome: cls, stated: s ? fmt(s) : null, weights: tot ? fmt(tot) : null, ratio: s && tot ? +(tot / s).toFixed(3) : null, ...(why ? { reason: why } : {}),
    note: 'AGREE when the weights hold 0.70 to 1.35 times the size in the name, the rule of the HFSIZE desk. Embeddings, vision or audio towers can explain a DISAGREE. The size rule matches the desk row for row. Packed and quantized detection reads the model tags and was not compared against the desk, which does not store tags.' });
  // license: the card’s license tag against the license file in the repository root, read at the revision the API returns (14 Nov, the referee: not main)
  const tag = ((m.tags || []).find(x => x.startsWith('license:')) || '').split(':')[1] || (m.cardData && m.cardData.license) || null, tagFam = famTag(tag);
  const lf = (m.siblings || []).map(x => x.rfilename).filter(f => !f.includes('/')).find(LICENSE_FILE) || null;
  let fileFam = null, lwhy = null;
  if (!tag) lwhy = 'no license on the card';
  else if (tagFam === 'OTHER') lwhy = 'the card names a custom or unrecognized license (' + tag + ')';
  else if (!lf) lwhy = 'no license file in the repository root';
  else { const tx = await t(`https://huggingface.co/${m.id || raw}/resolve/${m.sha || 'main'}/${lf}`); if (!tx) lwhy = 'license file not readable'; else { fileFam = famText(tx); if (fileFam === 'OTHER') lwhy = 'the license file is not one of the recognized families'; } }
  out.checks.push({ check: 'Card license against the license file', outcome: lwhy ? 'NOT_COMPARABLE' : compareFam(tagFam, fileFam), card_license: tag, card_family: tagFam, license_file: lf, file_family: fileFam, ...(lwhy ? { reason: lwhy } : {}),
    note: 'Compared by family, the rules of the HFLICENSE desk.' });
  out.reading = 'AGREE and DISAGREE compare two published statements about the same model. NOT_COMPARABLE gives the reason.';
  return out;
}

export function CHECKS_SELFTEST() {   // the desks’ planted pairs, run against the ports
  const P = [[['MIT'], ['MIT'], 'AGREE'], [['License :: OSI Approved :: Apache Software License'], ['Apache-2.0'], 'AGREE'], [['BSD-3-Clause'], ['BSD-2-Clause'], 'AGREE'],
    [['License :: OSI Approved :: GNU General Public License v3 (GPLv3)'], ['GPL-3.0'], 'AGREE'], [['MIT'], ['Apache-2.0'], 'DISAGREE'], [['Custom proprietary terms'], ['MIT'], 'NOT_COMPARABLE'],
    [['MIT', 'Apache-2.0'], ['Apache-2.0'], 'AGREE'], [['GPL'], ['GPL-3.0'], 'AGREE'], [['GPL-2.0'], ['GPL-3.0'], 'DISAGREE']];
  const SZ = [[7e9, 7.24e9, 'AGREE'], [7e9, 7e10, 'DISAGREE'], [7e9, 7e8, 'DISAGREE'], [135e6, 1.345e8, 'AGREE'], [7e9, 4.9e9, 'AGREE'], [7e9, 9.45e9, 'AGREE'], [7e9, 9.5e9, 'DISAGREE'], [null, 5e9, 'NOT_COMPARABLE'], [7e9, null, 'NOT_COMPARABLE']];
  const NM = [['Qwen2.5-7B-Instruct', 7e9], ['all-MiniLM-L6-v2', null], ['bge-m3', null], ['SmolLM2-135M', 1.35e8], ['gpt2-medium', null], ['Mixtral-8x7B-v0.1', null], ['Qwen3-30B-A3B', null], ['distil-7B-to-1B', null], ['Llama-3.2-1B', 1e9]];
  const fails = [];
  for (const [a, b, w] of P) if (comparePkg(famset(a), famset(b)) !== w) fails.push('pkg ' + a + ' ' + b);
  for (const [s, a, w] of SZ) if (compareSize(s, a) !== w) fails.push('size ' + s + ' ' + a);
  for (const [n, w] of NM) if (statedSize(n)[0] !== w) fails.push('name ' + n);
  return { cases: P.length + SZ.length + NM.length, fails };
}
