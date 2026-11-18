import { safeUrl, fetchText } from '../toolkit_common.js';
const bad = ['http://127.0.0.1/', 'http://2130706433/', 'http://0x7f.0.0.1/', 'http://[::1]/', 'http://[::ffff:127.0.0.1]/', 'http://metadata/', 'http://localhost/', 'https://example.com:8080/', 'http://user:pw@example.com/', 'file:///etc/passwd', 'http://printer.local/', 'https://net.indahl.ai/', 'https://leapfrog.indahl.ai/x', 'https://api.indahl.ai/', 'https://heuremen.com/', 'https://indahl.ai/mcp', 'https://indahl.ai/mcp/checks', 'https://indahl.ai/api/v1/quote_check?x=1', 'https://www.indahl.ai/.well-known/mcp.json'];
for (const u of ['https://indahl.ai/standard/standard_v1.json', 'https://www.indahl.ai/', 'https://heuremen.org/']) { if (!safeUrl(u).ok) { fails++; console.log('WRONGLY REFUSED', u); } }
let fails = 0; for (const u of bad) { const r = safeUrl(u); if (r.ok) { fails++; console.log('LET THROUGH', u); } }
for (const u of ['http://127.0.0.1.nip.io/', 'http://10.0.0.1.nip.io/', 'http://169.254.169.254.nip.io/latest/meta-data/']) { const r = await fetchText(u); if (!/refused/.test(r.error || '')) { fails++; console.log('DNS LET THROUGH', u, r.status, r.error); } else console.log('refused', u, '-', r.error); }
const ok = await fetchText('https://example.com/'); console.log('example.com', ok.status, ok.ok);
const red = await fetchText('http://github.com/indahl-ai'); console.log('redirect followed', red.status, red.url);
console.log(fails ? `SSRF: ${fails} FAILED` : "SSRF: all refused"); process.exit(fails ? 1 : 0);
