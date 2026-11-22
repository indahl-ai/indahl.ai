// toolkit.js (16 Nov 2026): Heuremen LLC skills turned into read-only MCP tools, gathered for api.js.
// Everything comes from what the caller passes or from public sources (public URLs, Crossref, arXiv, GitHub’s public API, PyPI, npm,
// indahl.ai itself). Nothing a caller sends is written, stored or logged. Spec: TOOLKIT_SPEC.md.
import { TOOLS_QIA } from './tools_qia.js';
import { TOOLS_TEXT } from './tools_text.js';
import { TOOLS_STATS } from './tools_stats.js';
import { TOOLS_OPS } from './tools_ops.js';
export const TOOLKIT = [...TOOLS_QIA, ...TOOLS_TEXT, ...TOOLS_STATS, ...TOOLS_OPS];
const names = a => a.map(t => t.name);
// Focused servers at https://indahl.ai/mcp/<key>. Keys already in api.js GROUPS get these tools added; new keys become new servers.
export const TOOLKIT_GROUPS = {
  quantum: { add: names(TOOLS_QIA) },
  research: { add: [...names(TOOLS_TEXT), 'interval_verdict', 'triangulate_readings'] },
  checks: { title: 'Indahl Checks', note: 'Checks a person brings, run on the server: quotes, figures and citations against their sources, wording that claims more than a comparison shows, intervals read as four outcomes, margins, readings from several sources, controls, two competing explanations, and evaluation setups.',
    tools: ['list_divisions', ...names(TOOLS_TEXT), ...names(TOOLS_STATS)] },
  verify: { title: 'Indahl Verify', note: 'Read an effect back from where it should have landed: a URL, a commit, a release, a published package; whether a plan was pushed before its results; batch manifests and merges; multi-stage job plans; corrections; check blocks; published file hashes.',
    tools: ['list_divisions', ...names(TOOLS_OPS)] },
};
