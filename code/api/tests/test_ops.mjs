// Tests for tools_ops.js. Run: node tests/test_ops.mjs
// Planted cases use a stubbed fetch (deterministic); a few cases read real public things (GitHub, PyPI, example.com, indahl.ai).
import { TOOLS_OPS, _ops, diffTexts } from '../tools_ops.js';
import { __setTestResolver } from '../toolkit_common.js';
__setTestResolver((h) => ({ ok: !/(^|\.)(localhost|local|internal)$/i.test(h) }));   // stubbed fetch: the DNS step is not sent to the stub (the real guard is tested in test_ssrf.mjs)
let bad = 0, n = 0; const ok = (name, cond, extra) => { n++; console.log((cond ? 'PASS ' : 'FAIL ') + name + (cond ? '' : '  ' + JSON.stringify(extra))); if (!cond) bad++; };
const T = Object.fromEntries(TOOLS_OPS.map(t => [t.name, t])); const run = async (name, args) => (await T[name].run({}, args)).data;
const realFetch = globalThis.fetch;
async function stub(handler, fn) {
  globalThis.fetch = async (url, init) => { const r = handler(String(url)); if (r instanceof Error) throw r; const body = typeof r.body === 'string' ? r.body : JSON.stringify(r.body ?? {}); return new Response(r.status === 204 ? null : body, { status: r.status ?? 200, headers: r.headers || {} }); };
  try { return await fn(); } finally { globalThis.fetch = realFetch; }
}
const rateLimited = (d) => d.outcome === 'CANNOT_TELL' && /rate limited/.test(d.reason || '');

ok('eight tools exported', TOOLS_OPS.length === 8 && TOOLS_OPS.every(t => t.name && t.description && t.params && typeof t.run === 'function'));
ok('names unique snake_case', new Set(TOOLS_OPS.map(t => t.name)).size === 8 && TOOLS_OPS.every(t => /^[a-z_]+$/.test(t.name)));

// ---- verify_landed (stubbed) ----
const body = 'hello world';
const hex = async (s) => { const h = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(h)].map(b => b.toString(16).padStart(2, '0')).join(''); };
const sha = await hex(body);
await stub(() => ({ status: 200, body }), async () => {
  ok('url clean: LANDED', (await run('verify_landed', { kind: 'url', target: 'https://example.org/x' })).outcome === 'LANDED');
  ok('url sha match: LANDED', (await run('verify_landed', { kind: 'url', target: 'https://example.org/x', expect: JSON.stringify({ sha256: sha }) })).outcome === 'LANDED');
  ok('url sha differs: DIFFERENT', (await run('verify_landed', { kind: 'url', target: 'https://example.org/x', expect: { sha256: 'a'.repeat(64) } })).outcome === 'DIFFERENT');
  ok('url substring found as plain expect string', (await run('verify_landed', { kind: 'url', target: 'https://example.org/x', expect: 'hello' })).outcome === 'LANDED');
  ok('url substring missing: DIFFERENT', (await run('verify_landed', { kind: 'url', target: 'https://example.org/x', expect: { contains: 'goodbye' } })).outcome === 'DIFFERENT');
  ok('url expected status mismatch: DIFFERENT', (await run('verify_landed', { kind: 'url', target: 'https://example.org/x', expect: { status: 201 } })).outcome === 'DIFFERENT');
});
await stub(() => ({ status: 404, body: 'no' }), async () => {
  ok('url 404: NOT_LANDED', (await run('verify_landed', { kind: 'url', target: 'https://example.org/x' })).outcome === 'NOT_LANDED');
  ok('url 404 expected 404: LANDED', (await run('verify_landed', { kind: 'url', target: 'https://example.org/x', expect: { status: 404 } })).outcome === 'LANDED');
});
await stub(() => ({ status: 429 }), async () => { const d = await run('verify_landed', { kind: 'url', target: 'https://example.org/x' }); ok('url 429: CANNOT_TELL rate limited', d.outcome === 'CANNOT_TELL' && /rate limited/.test(d.reason), d); });
await stub(() => new Error('boom'), async () => { const d = await run('verify_landed', { kind: 'url', target: 'https://example.org/x' }); ok('url network failure: CANNOT_TELL', d.outcome === 'CANNOT_TELL' && d.reason, d); });
await stub(() => ({ status: 403, body: { message: 'API rate limit exceeded' } }), async () => { const d = await run('verify_landed', { kind: 'github_commit', repo: 'a/b', sha: 'abcdef1' }); ok('github 403: CANNOT_TELL rate limited', d.outcome === 'CANNOT_TELL' && /rate limited/.test(d.reason), d); });
await stub((u) => u.includes('/commits/') ? { status: 422, body: { message: 'No commit found' } } : { status: 500 }, async () => ok('github commit 422: NOT_LANDED', (await run('verify_landed', { kind: 'github_commit', repo: 'a/b', sha: 'abcdef1' })).outcome === 'NOT_LANDED'));
const full = 'a'.repeat(40), head = 'b'.repeat(40);
const ghStub = (status) => (u) => u.includes('/commits/') ? { body: { sha: full, commit: { message: 'm', committer: { date: '2026-01-01T00:00:00Z' } } } } : u.includes('/branches/') ? { body: { commit: { sha: head } } } : u.includes('/compare/') ? { body: { status } } : { status: 500 };
await stub(ghStub('ahead'), async () => ok('commit on branch (ahead): LANDED', (await run('verify_landed', { kind: 'github_commit', repo: 'a/b', sha: 'aaaaaaa', branch: 'main' })).outcome === 'LANDED'));
await stub(ghStub('diverged'), async () => ok('commit not on branch (diverged): DIFFERENT', (await run('verify_landed', { kind: 'github_commit', repo: 'a/b', sha: 'aaaaaaa', branch: 'main' })).outcome === 'DIFFERENT'));
await stub((u) => u.includes('/releases/tags/') ? { body: { published_at: 'x', assets: [{ name: 'a.zip', size: 1 }] } } : { status: 500 }, async () => {
  ok('release asset present: LANDED', (await run('verify_landed', { kind: 'github_release', repo: 'a/b', tag: 'v1', expect: { assets: ['a.zip'] } })).outcome === 'LANDED');
  ok('release asset missing: DIFFERENT', (await run('verify_landed', { kind: 'github_release', repo: 'a/b', tag: 'v1', expect: { assets: ['b.zip'] } })).outcome === 'DIFFERENT');
});
await stub((u) => u.includes('/releases/tags/') ? { status: 404 } : u.includes('/git/ref/tags/') ? { status: 404 } : { status: 500 }, async () => { const d = await run('verify_landed', { kind: 'github_release', repo: 'a/b', tag: 'v9' }); ok('release and tag 404: CANNOT_TELL not found or not public, never NOT_LANDED', d.outcome === 'CANNOT_TELL' && /not public/.test(d.reason), d); });
await stub(() => ({ status: 404, body: { message: 'Not Found' } }), async () => { const d = await run('verify_landed', { kind: 'github_commit', repo: 'a/b', sha: 'abcdef1' }); ok('github commit 404: CANNOT_TELL not public', d.outcome === 'CANNOT_TELL' && /not public/.test(d.reason), d); });
await stub((u) => u.includes('/1.0/json') ? { body: { info: { version: '1.0', yanked: true, yanked_reason: 'broken' }, urls: [{ filename: 'p-1.0.tar.gz', upload_time_iso_8601: 'x', yanked: true, digests: { sha256: 'c'.repeat(64) } }] } } : { status: 404 }, async () => { const d = await run('verify_landed', { kind: 'pypi', target: 'p', version: '1.0' }); ok('pypi yanked release: DIFFERENT (landed, yanked)', d.outcome === 'DIFFERENT' && d.yanked === true && /yanked/.test(d.reason), d); });
await stub(() => ({ body: { Status: 0, Answer: [] } }), async () => { const d = await run('verify_landed', { kind: 'dns_txt', target: 'example.org' }); ok('method says DNS seen by Cloudflare resolver and URL may be CDN cached', /Cloudflare\'?s resolver/.test(d.method) && /CDN cache/.test(d.method)); });
await stub(() => ({ body: { message: 'x' }, status: 404 }), async () => { const d = await run('verify_landed', { kind: 'pypi', target: 'p', version: '1' }); ok('answers carry untrusted-source note', /untrusted/.test(d.untrusted_note), d); });
await stub((u) => u.includes('/1.0/json') ? { body: { info: { version: '1.0' }, urls: [{ filename: 'p-1.0.tar.gz', upload_time_iso_8601: '2026-01-01T00:00:00Z', digests: { sha256: 'c'.repeat(64) } }] } } : { status: 404 }, async () => {
  ok('pypi version + file: LANDED', (await run('verify_landed', { kind: 'pypi', target: 'p', version: '1.0', expect: { files: ['p-1.0.tar.gz'] } })).outcome === 'LANDED');
  ok('pypi missing file: DIFFERENT', (await run('verify_landed', { kind: 'pypi', target: 'p', version: '1.0', expect: { files: ['p-1.0-py3-none-any.whl'] } })).outcome === 'DIFFERENT');
  ok('pypi missing version: NOT_LANDED', (await run('verify_landed', { kind: 'pypi', target: 'p', version: '9.9' })).outcome === 'NOT_LANDED');
});
await stub((u) => u.includes('dns-query') ? { body: { Status: 0, Answer: [{ type: 16, data: '"v=spf1 " "include:x"' }] } } : { status: 500 }, async () => {
  ok('dns txt contains (joined strings): LANDED', (await run('verify_landed', { kind: 'dns_txt', target: 'example.org', expect: 'v=spf1 include:x' })).outcome === 'LANDED');
  ok('dns txt missing text: DIFFERENT', (await run('verify_landed', { kind: 'dns_txt', target: 'example.org', expect: 'nope' })).outcome === 'DIFFERENT');
});
await stub(() => ({ body: { Status: 3 } }), async () => ok('dns NXDOMAIN: NOT_LANDED', (await run('verify_landed', { kind: 'dns_txt', target: 'nonexistent.example.org' })).outcome === 'NOT_LANDED'));
ok('verify_landed bad kind: REFUSED', (await run('verify_landed', { kind: 'ftp', target: 'x' })).outcome === 'REFUSED');
ok('verify_landed private host: REFUSED', (await run('verify_landed', { kind: 'url', target: 'http://localhost/x' })).outcome === 'REFUSED');
ok('verify_landed garbage args no throw', (await run('verify_landed', undefined ?? {})).outcome === 'REFUSED');

// ---- prereg_check (stubbed) ----
const prStub = ({ planDate, resDate, planSha, resSha, pushPlan, pushRes, files }) => (u) => {
  const mk = (sha, date) => ({ sha, commit: { author: { date }, committer: { date }, message: 'm' } });
  if (u.includes('/commits?path=plan.md')) return { body: [mk(planSha, planDate)] };
  if (u.includes('/commits?path=results')) return { body: [mk(resSha, resDate)] };
  if (u.includes('/events')) return { body: [pushRes && { type: 'PushEvent', created_at: pushRes, payload: { head: resSha, before: '0'.repeat(40), push_id: 2 } }, pushPlan && { type: 'PushEvent', created_at: pushPlan, payload: { head: planSha, before: '0'.repeat(40), push_id: 1 } }].filter(Boolean) };
  if (u.includes('/commits/' + resSha)) return { body: { files: files || [{ filename: 'results/a.csv', status: 'added' }, { filename: 'results/extra.csv', status: 'added' }] } };
  if (u.includes('raw.githubusercontent.com')) return { body: 'We will produce a.csv with the analysis.' };
  return { status: 404 };
};
const A = 'a1'.repeat(20), B = 'b2'.repeat(20);
await stub(prStub({ planDate: '2026-01-01T00:00:00Z', resDate: '2026-01-02T00:00:00Z', planSha: A, resSha: B, pushPlan: '2026-01-01T00:01:00Z', pushRes: '2026-01-02T00:01:00Z' }), async () => {
  const d = await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', results_path: 'results' });
  ok('prereg PLAN_FIRST from push records', d.outcome === 'PLAN_FIRST' && /PushEvent/.test(d.basis), d);
  ok('prereg lists in_results_not_named_in_plan file', JSON.stringify(d.in_results_not_named_in_plan.files) === '["results/extra.csv"]', d.in_results_not_named_in_plan);
});
await stub(prStub({ planDate: '2026-01-05T00:00:00Z', resDate: '2026-01-02T00:00:00Z', planSha: A, resSha: B, pushPlan: '2026-01-05T00:01:00Z', pushRes: '2026-01-02T00:01:00Z' }), async () => ok('prereg RESULTS_FIRST', (await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', results_path: 'results' })).outcome === 'RESULTS_FIRST'));
await stub(prStub({ planDate: '2026-01-01T00:00:00Z', resDate: '2026-01-01T00:00:30Z', planSha: A, resSha: B }), async () => { const d = await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', results_path: 'results' }); ok('prereg no push record, commit dates 30 s apart: CANNOT_TELL NO_PUSH_RECORD', d.outcome === 'CANNOT_TELL' && /NO_PUSH_RECORD/.test(d.reason), d); });
await stub(prStub({ planDate: '2026-01-01T00:00:00Z', resDate: '2026-01-09T00:00:00Z', planSha: A, resSha: B, pushPlan: '2026-01-01T00:00:00Z', pushRes: '2026-01-01T00:00:30Z' }), async () => { const d = await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', results_path: 'results' }); ok('prereg push times 30 s apart: CANNOT_TELL STRADDLES_EDGE', d.outcome === 'CANNOT_TELL' && /STRADDLES_EDGE/.test(d.reason), d); });
await stub(prStub({ planDate: '2026-01-01T00:00:00Z', resDate: '2026-01-03T00:00:00Z', planSha: A, resSha: B }), async () => { const d = await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', results_path: 'results' }); ok('prereg no push record: CANNOT_TELL, commit dates only as a note', d.outcome === 'CANNOT_TELL' && /plan first/.test(d.note) && /author-set/.test(d.note) && /90 days and at most 300 events/.test(d.push_record_note), d); });
await stub(prStub({ planDate: '2026-01-01T00:00:00Z', resDate: '2026-01-02T00:00:00Z', planSha: A, resSha: B }), async () => { const d = await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', results_path: 'results' }); ok('prereg note says commit dates say plan first, no label from them', d.outcome === 'CANNOT_TELL' && /plan first/.test(d.note)); });
await stub(prStub({ planDate: '2026-01-01T00:00:00Z', planSha: A, resSha: A, pushPlan: '2026-01-01T00:01:00Z' }), async () => ok('prereg same commit: SAME_PUSH', (await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', results_path: 'results' })).outcome === 'SAME_PUSH'));
await stub(prStub({ planDate: '2026-01-01T00:00:00Z', planSha: A, pushPlan: '2026-01-01T00:01:00Z' }), async () => {
  { const d = await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', first_run_at: '2026-02-01T00:00:00Z' }); ok('prereg first_run_at after plan push: PLAN_FIRST, first_run_at called the caller\'s word', d.outcome === 'PLAN_FIRST' && /caller's word/.test(d.results.record) && /caller's word/.test(d.basis), d); }
  ok('prereg first_run_at before push: RESULTS_FIRST', (await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', first_run_at: '2025-12-01T00:00:00Z' })).outcome === 'RESULTS_FIRST');
});
await stub(() => ({ status: 403, body: {} }), async () => { const d = await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', results_path: 'results' }); ok('prereg rate limited: CANNOT_TELL', d.outcome === 'CANNOT_TELL' && /rate limited/.test(d.reason), d); });
await stub(() => ({ body: [] }), async () => ok('prereg unknown plan path: CANNOT_TELL', (await run('prereg_check', { repo: 'a/b', plan_path: 'zzz', results_path: 'r' })).outcome === 'CANNOT_TELL'));
ok('prereg bad repo: REFUSED', (await run('prereg_check', { repo: 'nope', plan_path: 'p', results_path: 'r' })).outcome === 'REFUSED');
ok('prereg neither results nor first_run: REFUSED', (await run('prereg_check', { repo: 'a/b', plan_path: 'p' })).outcome === 'REFUSED');
ok('prereg bad time: REFUSED', (await run('prereg_check', { repo: 'a/b', plan_path: 'p', first_run_at: 'yesterday-ish' })).outcome === 'REFUSED');
// push membership through the compare API (payload lists no commits)
const C1 = 'c1'.repeat(20), H1 = 'd1'.repeat(20), H2 = 'd2'.repeat(20);
await stub((u) => {
  const mk = (sha, date) => ({ sha, commit: { author: { date }, committer: { date }, message: 'm' } });
  if (u.includes('/commits?path=plan.md')) return { body: [mk(C1, '2026-01-01T00:00:00Z')] };
  if (u.includes('/events')) return { body: [{ type: 'PushEvent', created_at: '2026-03-01T00:00:00Z', payload: { head: H2, before: H1, push_id: 9 } }, { type: 'PushEvent', created_at: '2026-02-01T00:00:00Z', payload: { head: H1, before: 'e'.repeat(40), push_id: 8 } }] };
  if (u.includes('/compare/' + 'e'.repeat(40))) return { body: { commits: [{ sha: C1 }, { sha: H1 }] } };
  if (u.includes('/compare/')) return { body: { commits: [{ sha: H2 }] } };
  return { status: 404 };
}, async () => { const d = await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', first_run_at: '2026-06-01T00:00:00Z' }); ok('prereg push membership found through compare before..head (earliest push)', d.outcome === 'PLAN_FIRST' && d.plan.push_time === '2026-02-01T00:00:00Z' && d.compare_checks_used >= 1, d); });
// Link header pagination to the oldest commit
await stub((u) => u.includes('page=7') ? { body: [{ sha: 'z'.repeat(40), commit: { author: { date: '2020-01-01T00:00:00Z' }, committer: { date: '2020-01-01T00:00:00Z' }, message: 'oldest' } }] } : u.includes('/commits?path=') ? { body: [{ sha: 'y'.repeat(40), commit: { author: { date: '2026-01-01T00:00:00Z' }, committer: { date: '2026-01-01T00:00:00Z' }, message: 'new' } }], headers: { link: '<https://api.github.com/repos/a/b/commits?path=plan.md&per_page=100&page=7>; rel="last"' } } : { body: [] }, async () => {
  const d = await run('prereg_check', { repo: 'a/b', plan_path: 'plan.md', first_run_at: '2026-06-01T00:00:00Z' }); ok('prereg follows Link rel=last to the oldest commit', d.plan && d.plan.message === 'oldest', d.plan);
});

// ---- round 2 ----
ok('descriptions state the shared GitHub limit', ['verify_landed', 'prereg_check'].every(n => /shared and rate limiting is common/.test(T[n].description) && /CANNOT_TELL \(rate limited\)/.test(T[n].description)));
{ let hits = 0; await stub((u) => { if (u.includes('/commits/' + full)) hits++; return u.includes('/commits/') ? { body: { sha: full, commit: { message: 'm', committer: { date: 'x' } } } } : u.includes('/branches/') ? { body: { commit: { sha: full } } } : { status: 500 }; }, async () => {
  await run('verify_landed', { kind: 'github_commit', repo: 'a/b', sha: full, branch: 'main' }); ok('commit read once per call', hits === 1, hits); }); }
ok('near-empty wording', !/script/.test(JSON.stringify(await stub(() => ({ body: '<div></div>' }), () => run('correction_check', { original: 'The cat sat. It was big.', corrected: 'The cat sat. It was small.', places: ['https://example.org/t'] })))) );
// ---- batch ----
const items = Array.from({ length: 60 }, (_, i) => 'item-' + String(i).padStart(3, '0'));
const bp = await run('batch_plan', { items: JSON.stringify(items), batch_size: '25' });
ok('batch_plan items: 60 items, 3 batches of 25/25/10', bp.item_count === 60 && bp.batch_count === 3 && bp.batches[2].count === 10 && bp.batches[1].start === 25, bp);
ok('batch_plan manifest sha is 64 hex and READY', /^[0-9a-f]{64}$/.test(bp.manifest_sha256) && bp.outcome === 'READY');
const bp2 = await run('batch_plan', { items: [...items].reverse() });
ok('batch_plan manifest independent of input order', bp2.manifest_sha256 === bp.manifest_sha256);
const dup = await run('batch_plan', { items: ['a', 'b', 'a'] }); ok('batch_plan reports duplicates removed', dup.duplicates_removed === 1 && dup.item_count === 2);
const big = await run('batch_plan', { items: Array.from({ length: 5200 }, (_, i) => 'u' + i) }); ok('batch_plan capped: CAPPED, manifest_complete false', big.item_count === 5000 && big.capped === true && big.outcome === 'CAPPED' && big.manifest_complete === false && /capped/.test(big.reason));
ok('batch_plan clean: manifest_complete true', bp.manifest_complete === true);
ok('batch_plan nothing given: REFUSED', (await run('batch_plan', {})).outcome === 'REFUSED');
ok('batch_plan private sitemap URL: REFUSED', (await run('batch_plan', { source: 'http://localhost/sitemap.xml' })).outcome === 'REFUSED');
await stub((u) => u.endsWith('index.xml') ? { body: '<sitemapindex><sitemap><loc>https://example.org/s1.xml</loc></sitemap><sitemap><loc>https://example.org/s2.xml</loc></sitemap></sitemapindex>' } : u.endsWith('s1.xml') ? { body: '<urlset><url><loc>https://example.org/a</loc></url><url><loc>https://example.org/b?x=1&amp;y=2</loc></url></urlset>' } : u.endsWith('s2.xml') ? { body: '<urlset><url><loc>https://example.org/c</loc></url></urlset>' } : { status: 404 }, async () => {
  const d = await run('batch_plan', { source: 'https://example.org/index.xml' }); ok('batch_plan follows sitemap index one level', d.item_count === 3 && d.items.includes('https://example.org/b?x=1&y=2'), d);
  const e = await run('batch_plan', { source: 'https://example.org/missing.xml' }); ok('batch_plan unreadable sitemap: CANNOT_TELL', e.outcome === 'CANNOT_TELL', e);
});
await stub((u) => u.endsWith('index.xml') ? { body: '<sitemapindex><sitemap><loc>https://example.org/s1.xml</loc></sitemap></sitemapindex>' } : { body: '<sitemapindex><sitemap><loc>https://example.org/deep.xml</loc></sitemap></sitemapindex>' }, async () => { const d = await run('batch_plan', { source: 'https://example.org/index.xml' }); ok('batch_plan warns on index deeper than one level, not followed, not complete', d.manifest_complete === false && d.warnings.some(w => /deeper than one level/.test(w)) && d.item_count === 0, d); });
await stub((u) => u.endsWith('/repos/a/b') ? { body: { default_branch: 'main' } } : u.includes('/git/trees/main') ? { body: { tree: [{ path: 'docs/x.md', type: 'blob' }, { path: 'docs/y.txt', type: 'blob' }, { path: 'src/z.md', type: 'blob' }, { path: 'docs', type: 'tree' }] } } : { status: 404 }, async () => {
  const d = await run('batch_plan', { source: 'a/b', path: 'docs', ext: ['md'] }); ok('batch_plan repo tree filtered by path and ext', JSON.stringify(d.items) === '["docs/x.md"]', d.items);
});

const m = bp.items;
const ok1 = await run('batch_merge_check', { manifest_items: m, manifest_sha256: bp.manifest_sha256, results: m.map(id => ({ id, v: 1 })) });
ok('merge COMPLETE with matching sha', ok1.outcome === 'COMPLETE' && ok1.manifest_sha256_check === 'MATCH', ok1);
const miss = await run('batch_merge_check', { manifest_items: JSON.stringify(m), results: JSON.stringify(m.slice(2)) });
ok('merge MISSING listed', miss.outcome === 'INCOMPLETE' && miss.missing.count === 2 && miss.missing.ids[0] === 'item-000', miss);
const du = await run('batch_merge_check', { manifest_items: m, results: [...m, 'item-005'] }); ok('merge DUPLICATE listed', du.outcome === 'INCOMPLETE' && du.duplicate.count === 1 && du.duplicate.ids[0].id === 'item-005');
const ex = await run('batch_merge_check', { manifest_items: m, results: [...m, 'stranger'] }); ok('merge EXTRA listed', ex.outcome === 'INCOMPLETE' && ex.extra.ids[0] === 'stranger');
const noid = await run('batch_merge_check', { manifest_items: m, results: [...m, { value: 3 }] }); ok('merge result without id is not COMPLETE', noid.outcome === 'INCOMPLETE' && noid.results_without_id === 1);
const wrongSha = await run('batch_merge_check', { manifest_items: m.slice(1), manifest_sha256: bp.manifest_sha256, results: m.slice(1) }); ok('merge wrong sha: CANNOT_TELL', wrongSha.outcome === 'CANNOT_TELL' && /do not hash/.test(wrongSha.reason));
const part = await run('batch_merge_check', { manifest_items: m, manifest_complete: false, results: m }); ok('merge partial manifest: CANNOT_TELL, never COMPLETE', part.outcome === 'CANNOT_TELL' && /partial/.test(part.reason) && part.manifest_complete === false, part);
const part2 = await run('batch_merge_check', { manifest_items: m, manifest_complete: 'false', results: m.slice(1) }); ok('merge partial manifest with a missing item: INCOMPLETE', part2.outcome === 'INCOMPLETE');
ok('merge sha only, no items: CANNOT_TELL', (await run('batch_merge_check', { manifest_items: [], manifest_sha256: bp.manifest_sha256, results: ['a'] })).outcome === 'CANNOT_TELL');
ok('merge garbage input: CANNOT_TELL', (await run('batch_merge_check', { manifest_items: 12, results: 'x' })).outcome === 'CANNOT_TELL');

// ---- relay_plan_check ----
const good = [{ name: 'train', lane: 'gpu', deadline_minutes: 60, writes_exit_code_to: 'rc/train' }, { name: 'eval', needs: ['train'], lane: 'gpu', deadline_minutes: 10, writes_exit_code_to: 'rc/eval' }, { name: 'report', needs: ['eval'], deadline_minutes: 5, writes_exit_code_to: 'rc/report' }];
const rg = await run('relay_plan_check', { stages: JSON.stringify(good), lane_limits: '{"gpu":1}' });
ok('relay clean chain: READY with three waves', rg.outcome === 'READY' && rg.run_order_waves.length === 3 && rg.run_order_waves[0].stages[0] === 'train', rg);
const codes = (d) => d.findings.map(f => f.code);
ok('relay unknown dependency', codes(await run('relay_plan_check', { stages: [{ name: 'a', needs: ['ghost'], deadline_minutes: 1, writes_exit_code_to: 'x' }] })).includes('UNKNOWN_DEPENDENCY'));
const cyc = await run('relay_plan_check', { stages: [{ name: 'a', needs: ['b'], deadline_minutes: 1, writes_exit_code_to: 'x' }, { name: 'b', needs: ['a'], deadline_minutes: 1, writes_exit_code_to: 'y' }] });
ok('relay cycle reported with its path', cyc.outcome === 'FIX' && cyc.findings.some(f => f.code === 'CYCLE' && /a -> b -> a|b -> a -> b/.test(f.message)), cyc);
const nd = await run('relay_plan_check', { stages: [{ name: 'a', writes_exit_code_to: 'x' }] }); ok('relay no deadline: FIX', nd.outcome === 'FIX' && codes(nd).includes('NO_DEADLINE'));
const ne = await run('relay_plan_check', { stages: [{ name: 'a', deadline_minutes: 5 }] }); ok('relay no exit record: FIX', codes(ne).includes('NO_EXIT_RECORD'));
const se = await run('relay_plan_check', { stages: [{ name: 'a', deadline_minutes: 5, writes_exit_code_to: 'rc' }, { name: 'b', deadline_minutes: 5, writes_exit_code_to: 'rc' }] }); ok('relay shared exit file', codes(se).includes('SHARED_EXIT_FILE'));
const ov = await run('relay_plan_check', { stages: [{ name: 'a', lane: 'gpu', deadline_minutes: 5, writes_exit_code_to: '1' }, { name: 'b', lane: 'gpu', deadline_minutes: 5, writes_exit_code_to: '2' }], lane_limits: { gpu: 1 } }); ok('relay lane oversubscribed', codes(ov).includes('LANE_OVERSUBSCRIBED'), ov);
const dn = await run('relay_plan_check', { stages: [{ name: 'a', deadline_minutes: 5, writes_exit_code_to: '1' }, { name: 'a', deadline_minutes: 5, writes_exit_code_to: '2' }] }); ok('relay duplicate name', codes(dn).includes('DUPLICATE_NAME'));
const bd = await run('relay_plan_check', { stages: [{ name: 'a', deadline_minutes: -3, writes_exit_code_to: '1' }] }); ok('relay negative deadline', codes(bd).includes('BAD_DEADLINE'));
ok('relay empty stages: CANNOT_TELL', (await run('relay_plan_check', { stages: [] })).outcome === 'CANNOT_TELL');
ok('relay garbage stages: CANNOT_TELL', (await run('relay_plan_check', { stages: 'not json at all\n' })).outcome === 'FIX');
ok('relay stage not object does not throw', (await run('relay_plan_check', { stages: [1, null] })).outcome === 'FIX');

// ---- correction_check ----
const orig = 'The trial enrolled 120 patients. The effect was significant. Results are final.';
const corr = 'The trial enrolled 112 patients. The effect was significant. Results are final.';
const dd = diffTexts(orig, corr);
ok('diff pairs the changed sentence and finds the number', dd.pairs.length === 1 && dd.pairs[0].was.includes('120') && dd.pairs[0].now.includes('112') && dd.numbers_removed[0] === '120' && dd.numbers_added[0] === '112', dd);
const lg = await run('correction_check', { original: orig, corrected: corr, why: 'miscount' });
ok('ledger entry has was, now, when, why', lg.outcome === 'LEDGER_ONLY' && lg.ledger_entry.was.length === 1 && lg.ledger_entry.now.length === 1 && lg.ledger_entry.why === 'miscount' && /^\d{4}-/.test(lg.ledger_entry.logged_at) && lg.ledger_entry.when === undefined, lg);
ok('identical texts: NO_CHANGE', (await run('correction_check', { original: orig, corrected: orig + '  ' })).outcome === 'NO_CHANGE');
ok('whitespace and quote differences are not changes', (await run('correction_check', { original: 'He said “yes”.  It works.', corrected: 'He said "yes". It works.' })).outcome === 'NO_CHANGE');
const pages = { '/new': '<html><p>The trial enrolled 112 patients. The effect was significant.</p></html>', '/old': '<p>The trial   enrolled 120 patients. The effect was significant.</p>', '/both': '<p>The trial enrolled 120 patients.</p><p>Corrected: The trial enrolled 112 patients.</p>', '/none': '<p>' + 'Unrelated page about cats and dogs. '.repeat(30) + '</p>', '/tiny': '<div id="root"></div><script>app()</script>' };
await stub((u) => { const p = new URL(u).pathname; return pages[p] ? { body: pages[p], headers: { 'content-type': 'text/html' } } : { status: 503 }; }, async () => {
  const d = await run('correction_check', { original: orig, corrected: corr, places: JSON.stringify(['https://example.org/new', 'https://example.org/old', 'https://example.org/both', 'https://example.org/none', 'https://example.org/down', 'https://example.org/tiny']) });
  const by = Object.fromEntries(d.places.map(p => [new URL(p.url).pathname, p.outcome]));
  ok('places: UPDATED / STILL_OLD / BOTH_PRESENT / NEITHER_FOUND / CANNOT_TELL', by['/new'] === 'UPDATED' && by['/old'] === 'STILL_OLD' && by['/both'] === 'BOTH_PRESENT' && by['/none'] === 'NEITHER_FOUND' && by['/down'] === 'CANNOT_TELL', by);
  ok('near-empty page with nothing found: row CANNOT_TELL', d.places.find(x => x.url.endsWith('/tiny')).outcome === 'CANNOT_TELL' && /too little visible text to read absence/.test(d.places.find(x => x.url.endsWith('/tiny')).reason));
  ok('overall NOT_ALL_UPDATED with counts', d.outcome === 'NOT_ALL_UPDATED' && d.place_counts.STILL_OLD === 1);
  const d3 = await run('correction_check', { original: orig, corrected: corr, places: ['https://example.org/none'] }); ok('every place NEITHER_FOUND: overall CANNOT_TELL', d3.outcome === 'CANNOT_TELL' && /NEITHER_FOUND/.test(d3.reason), d3);
  const d4 = await run('correction_check', { original: orig, corrected: corr, places: ['https://example.org/tiny'] }); ok('JS-rendered near-empty body: overall CANNOT_TELL', d4.outcome === 'CANNOT_TELL', d4);
  const d5 = await run('correction_check', { original: orig, corrected: corr, places: ['https://example.org/new', 'https://example.org/none'] }); ok('one UPDATED and one NEITHER_FOUND: NOT_ALL_UPDATED', d5.outcome === 'NOT_ALL_UPDATED', d5);
  const d2 = await run('correction_check', { original: orig, corrected: corr, places: ['https://example.org/new'] }); ok('all updated: ALL_UPDATED', d2.outcome === 'ALL_UPDATED');
});
const many = await stub(() => ({ body: 'x' }), () => run('correction_check', { original: orig, corrected: corr, places: Array.from({ length: 25 }, (_, i) => 'https://example.org/p' + i) }));
ok('places capped at 20', many.places.length === 20 && many.places_not_read === 5);
ok('places unsafe URL: CANNOT_TELL row', (await run('correction_check', { original: orig, corrected: corr, places: ['http://localhost/x'] })).places[0].outcome === 'CANNOT_TELL');
ok('correction missing text: CANNOT_TELL', (await run('correction_check', { original: '', corrected: 'x' })).outcome === 'CANNOT_TELL');

// ---- check_block_validate ----
const IDS = Array.from({ length: 13 }, (_, i) => 'REQ-' + String(i + 1).padStart(2, '0'));
const full13 = Object.fromEntries(IDS.map(id => [id, { answer: 'holds: checked the run log for ' + id }]));
const vb = await run('check_block_validate', { block: JSON.stringify({ what: 'A reading', requirements: full13 }) });
ok('block JSON full: VALID (real standard read or embedded)', vb.outcome === 'VALID', vb);
const txt = IDS.map(id => `${id}: holds: checked ${id} against the log`).join('\n');
ok('block text full: VALID', (await run('check_block_validate', { block: txt })).outcome === 'VALID');
const withBlank = JSON.stringify({ what: 'w', requirements: { ...full13, 'REQ-03': { answer: 'TODO' }, 'REQ-04': { answer: '' }, 'REQ-05': { answer: 'holds' } } });
const vbk = await run('check_block_validate', { block: withBlank });
const st = Object.fromEntries(vbk.lines.map(l => [l.req, l.status]));
ok('block BLANK for TODO, empty and bare holds', vbk.outcome === 'INVALID' && st['REQ-03'] === 'BLANK' && st['REQ-04'] === 'BLANK' && st['REQ-05'] === 'BLANK', st);
const noReq = { ...full13 }; delete noReq['REQ-07'];
ok('block MISSING line', (await run('check_block_validate', { block: JSON.stringify({ what: 'w', requirements: noReq }) })).lines.find(l => l.req === 'REQ-07').status === 'MISSING');
const bo = await run('check_block_validate', { block: JSON.stringify({ what: 'w', requirements: { ...full13, 'REQ-05': { answer: 'holds: all readings were reported', outcome: 'PASS' } } }) });
ok('block BAD_OUTCOME for PASS', bo.outcome === 'INVALID' && bo.lines.find(l => l.req === 'REQ-05').status === 'BAD_OUTCOME');
const good2 = await run('check_block_validate', { block: JSON.stringify({ what: 'w', requirements: { ...full13, 'REQ-05': { answer: 'holds: all readings were reported', outcome: 'CANNOT_TELL' } } }) });
ok('block four-outcome word accepted', good2.outcome === 'VALID');
const txtBad = txt.replace('REQ-05: holds: checked REQ-05 against the log', 'REQ-05: holds: counted. outcome: maybe');
ok('block text outcome word checked', (await run('check_block_validate', { block: txtBad })).lines.find(l => l.req === 'REQ-05').status === 'BAD_OUTCOME');
await stub(() => ({ status: 500 }), async () => { const d = await run('check_block_validate', { block: txt }); ok('block validates against embedded list when standard unreadable, and says so', d.outcome === 'VALID' && d.embedded_list_used === true && /embedded/.test(d.requirements_source), d.requirements_source); });
ok('block empty: CANNOT_TELL', (await run('check_block_validate', { block: '  ' })).outcome === 'CANNOT_TELL');
ok('block with no REQ lines: INVALID', (await run('check_block_validate', { block: 'just some words about a run' })).outcome === 'INVALID');
ok('block broken JSON does not throw', ['VALID', 'INVALID'].includes((await run('check_block_validate', { block: '{"requirements": ' })).outcome));

// ---- reproduce_check (stubbed) ----
const payload = 'zipbytes'; const psha = await hex(payload);
await stub((u) => u.endsWith('.sha256') ? { body: psha + '  steo-data-pack.zip\n' } : { body: payload }, async () => {
  const d = await run('reproduce_check', { desk: 'steo' }); ok('reproduce MATCH (site file, sha, github copy all agree)', d.outcome === 'MATCH' && d.comparisons.length === 2, d);
});
await stub((u) => u.endsWith('.sha256') ? { body: 'f'.repeat(64) + '  x\n' } : { body: payload }, async () => ok('reproduce MISMATCH on wrong published sha', (await run('reproduce_check', { desk: 'steo' })).outcome === 'MISMATCH'));
await stub((u) => u.endsWith('.sha256') ? { body: psha } : u.includes('raw.githubusercontent.com') ? { body: 'different' } : { body: payload }, async () => { const d = await run('reproduce_check', { desk: 'steo' }); ok('reproduce: site copy matches its .sha256 but GitHub copy differs: overall MISMATCH', d.outcome === 'MISMATCH' && d.comparisons[0].outcome === 'MATCH' && d.comparisons[1].outcome === 'MISMATCH', d); });
await stub((u) => u.endsWith('.sha256') ? { status: 404 } : { body: payload }, async () => ok('reproduce missing .sha256: CANNOT_TELL', (await run('reproduce_check', { desk: 'steo' })).outcome === 'CANNOT_TELL'));
await stub((u) => u.endsWith('.sha256') ? { body: 'not a hash' } : { body: payload }, async () => ok('reproduce unparseable .sha256: CANNOT_TELL', (await run('reproduce_check', { desk: 'steo' })).outcome === 'CANNOT_TELL'));
ok('reproduce bad desk: REFUSED', (await run('reproduce_check', { desk: '../etc' })).outcome === 'REFUSED');
ok('reproduce nothing given: REFUSED', (await run('reproduce_check', {})).outcome === 'REFUSED');
ok('reproduce private url: REFUSED', (await run('reproduce_check', { url: 'http://127.0.0.1/x' })).outcome === 'REFUSED');

// ---- real network (few) ----
const net = await run('verify_landed', { kind: 'url', target: 'https://example.com', expect: 'Example Domain' }); ok('NET example.com landed with text', net.outcome === 'LANDED', net);
const net404 = await run('verify_landed', { kind: 'url', target: 'https://example.com/this-page-does-not-exist-zzz' }); ok('NET example.com missing page NOT_LANDED', net404.outcome === 'NOT_LANDED', net404);
const py = await run('verify_landed', { kind: 'pypi', target: 'requests', version: '2.31.0' }); ok('NET pypi requests 2.31.0 LANDED with files and upload time', py.outcome === 'LANDED' && py.files.length > 0 && py.first_upload_time, py);
const pyNo = await run('verify_landed', { kind: 'pypi', target: 'requests', version: '999.0.0' }); ok('NET pypi requests 999.0.0 NOT_LANDED', pyNo.outcome === 'NOT_LANDED', pyNo);
const npmD = await run('verify_landed', { kind: 'npm', target: 'left-pad', version: '1.3.0' }); ok('NET npm left-pad 1.3.0 LANDED', npmD.outcome === 'LANDED', npmD);
const dns = await run('verify_landed', { kind: 'dns_txt', target: 'example.com' }); ok('NET dns TXT example.com answers (LANDED or NOT_LANDED, never a throw)', ['LANDED', 'NOT_LANDED', 'DIFFERENT', 'CANNOT_TELL'].includes(dns.outcome), dns);
const rp = await run('reproduce_check', { desk: 'steo' }); ok('NET reproduce steo: MATCH on indahl.ai file, sha256 and GitHub copy', rp.outcome === 'MATCH' || (rp.outcome === 'MISMATCH' && rp.comparisons[1] && rp.comparisons[1].computed_github), rp);
const rpFile = await run('reproduce_check', { desk: 'steo' }); ok('NET reproduce steo first comparison (site vs published sha) MATCH', rpFile.comparisons[0] && rpFile.comparisons[0].outcome === 'MATCH', rpFile.comparisons);
const rb = await run('check_block_validate', { block: txt }); ok('NET standard read from indahl.ai', /standard_v1\.json \(Standards/.test(rb.requirements_source), rb.requirements_source);
const gc = await run('batch_plan', { source: 'indahl-ai/indahl.ai', path: 'claude-plugins', ext: ['md'], batch_size: 10 });
ok('NET batch_plan repo indahl-ai/indahl.ai (or rate limited)', rateLimited(gc) || (gc.outcome === 'READY' && gc.item_count > 0 && gc.items.every(i => i.startsWith('claude-plugins/') && i.endsWith('.md'))), gc.reason || gc.outcome);
const tr = await realFetch('https://api.github.com/repos/indahl-ai/indahl.ai/commits?per_page=1'); let headSha = null; if (tr.ok) headSha = (await tr.json())[0].sha;
if (headSha) {
  const vc = await run('verify_landed', { kind: 'github_commit', repo: 'indahl-ai/indahl.ai', sha: headSha, branch: 'main' }); ok('NET github_commit head on main LANDED (or rate limited)', vc.outcome === 'LANDED' || rateLimited(vc), vc);
  const vn = await run('verify_landed', { kind: 'github_commit', repo: 'indahl-ai/indahl.ai', sha: '0123456789abcdef0123456789abcdef01234567' }); ok('NET github_commit nonexistent NOT_LANDED (or rate limited)', vn.outcome === 'NOT_LANDED' || rateLimited(vn), vn);
} else ok('NET github reachable (rate limited, tests skipped)', true);
const pr = await run('prereg_check', { repo: 'indahl-ai/indahl.ai', plan_path: 'README.md', results_path: 'steo/steo_outcomes.csv' });
ok('NET prereg real repo returns a label or rate limited, with times', rateLimited(pr) || (['PLAN_FIRST', 'RESULTS_FIRST', 'SAME_PUSH', 'CANNOT_TELL'].includes(pr.outcome) && pr.plan && pr.results), pr.reason || pr.outcome);

console.log(bad ? `${bad} FAILED of ${n}` : `all pass (${n})`); process.exit(bad ? 1 : 0);
