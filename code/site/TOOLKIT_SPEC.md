# indahl.ai toolkit: skills turned into MCP tools (16 Nov 2026)

Goal: every Heuremen LLC skill that can do real work on a server becomes a read-only MCP tool on https://indahl.ai/mcp, so anyone
can add it to Claude, ChatGPT or any MCP client from the website. Everything comes from what the caller passes in or from PUBLIC
sources (public URLs, Crossref, arXiv, GitHub public API, PyPI, indahl.ai itself). Never from Heuremen's private machines or files.

## Where the code goes
- One ES module per group in `~/bones-forge/indahl-ai/`: `tools_text.js`, `tools_stats.js`, `tools_ops.js` (QIA: `tools_qia.js`, the operator).
- Each module: `import { answer, fetchText, sha256hex, safeUrl, clip } from './toolkit_common.js';` and
  `export const TOOLS_<GROUP> = [ ... ];`
- Do NOT edit api.js, research.js, checks.js or anything else. The operator wires the arrays into api.js.
- Tool object shape (the same as api.js TOOLS_ALL):
  `{ name, title, description, params: { argName: { type, description, enum? } }, required: [...], openWorld: bool, run: async (env, args, req) => answer(source, data) }`
  - `name`: snake_case, unique, not already used in api.js (check: `grep -n "name: '" indahl-ai/api.js`).
  - `openWorld: true` only when the tool fetches a URL or service the caller names (the same convention as paper_check). Pure arithmetic/text tools: false.
  - Param types: string, integer, number, boolean, array (items: {type: string}), object. Arguments may arrive as strings over REST
    (`GET /api/v1/<tool>?x=...`), so parse numbers with Number() and accept JSON strings for arrays/objects.
- Return ALWAYS via `answer(source, data)`. `source` = the public page or service read (or 'https://indahl.ai/tools' for pure computation).
  `data` must include: `outcome` (overall), per-item rows with their own outcome, `method` (one or two plain sentences on what was
  computed and its limits), and `read` (what was fetched, with URL, HTTP status and when) for anything fetched.

## Outcome words
House rule: four outcomes ABOVE / BELOW / CONSISTENT / CANNOT_TELL, never folded, and NOTHING_RETURNED / REFUSED as their own facts.
Tool-specific labels from the skill are fine (VERBATIM, HELD, READY...) but CANNOT_TELL must exist in every label set, and anything that
could not be read is CANNOT_TELL or NOTHING_RETURNED with the reason, never a pass.

## Runtime limits (Cloudflare Workers)
- Only `fetch`, `crypto.subtle`, `TextEncoder`, `URL`, standard JS. No Node modules, no npm packages, no eval.
- At most ~40 outbound fetches per call; use `fetchText` (8 s timeout, 2 MB cap, follows redirects, returns {ok,status,url,text,error,at}).
- User-named URLs go through `safeUrl` first (http/https only, no IP literals, no localhost/private names). Refuse otherwise.
- Pasted text args: clip to 20000 characters with `clip`. The request body cap is 64 KB.
- Nothing is written, stored or logged. No console.log. No KV writes.
- Deterministic: same input and same fetched content give the same output.

## Copy rules (OpenAI rejected "promises the functionality does not support")
- Descriptions say exactly what is computed and its limits. No "guarantees", "nothing dropped", "ensures", "proves", "every" unless literally true.
- Rule-based checks say they are rule-based. A tool never claims to judge meaning it cannot compute.
- Corporate, third person, plain. No "we/you" marketing, no counts of our things.

## Tests
- Each module gets `~/bones-forge/indahl-ai/tests/test_<group>.mjs`, runnable with `node tests/test_<group>.mjs` (Node 26 has fetch and crypto.subtle).
- Cover: a clean case, a planted failure for each label, a CANNOT_TELL case, bad input (missing/garbage args return an error-free CANNOT_TELL or REFUSED, never a throw).
- Network cases may hit real public URLs (arXiv, Crossref, GitHub, example.com); keep them few.
- All tests must pass before you report.

## Report back
Tool names, one line each on what it computes, test results (counts), and anything you could not do honestly.
