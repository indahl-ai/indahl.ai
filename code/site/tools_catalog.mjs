// 15 Nov 2026 (the owner): prints every MCP tool, read from api.js itself (the server card and the OpenAPI
// document), so the /connect/tools pages built by build_site.py never drift from what tools/list serves.
const m = await import('./api.js');
const get = async (p) => (await m.handleApi(new Request('https://indahl.ai' + p), {}, new URL('https://indahl.ai' + p))).json();
const card = await get('/.well-known/mcp.json'), oa = await get('/api/openapi.json');
const tools = card.tools.map(t => { const op = oa.paths['/api/v1/' + t.name] || {}; const g = op.get || op.post || {};
  return { ...t, description: g.description || g.summary || '', params: (g.parameters || []).map(p => ({ name: p.name, required: !!p.required, description: p.description || '' })) }; });
console.log(JSON.stringify({ tools, servers: card.servers }));
