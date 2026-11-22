# Indahl Data

`indahl-data`

Brings the read-only indahl.ai MCP server (https://indahl.ai/mcp) into Claude Code. Each answer holds a stated claim against the data behind it and is quoted with its count, interval, outcome and receipt. Use it to check the calibration IBM publishes for an IBM Quantum processor against our own runs (QIA, the Quantum Idle Audit), or to check what you bring: a paper by DOI or arXiv id, reported statistics, the numbers, quotations and citations in a draft, an interval against a stated value, an LLM evaluation setup, a PyPI package or a Hugging Face model.

## What you get

- The server's tools, which Claude calls for you. It needs no key.
- Each figure with its count and denominator, its interval and level, its outcome (ABOVE, BELOW, CONSISTENT or CANNOT_TELL), the source link and the time it was read.
- Nothing returned, refused and held counted as their own outcomes, never folded into a pass or a fail.

## How to use

Run `/indahl` followed by what to check. For example:

```
/indahl Is IBM's published calibration for qubits 0 to 4 on ibm_kingston fit to rely on?
```

Retrieval and answering are permitted. Saving responses to train, fine-tune or build a model is not permitted (see the terms).

## Install

```
/plugin marketplace add indahl-ai/indahl.ai
/plugin install indahl-data@heuremen
```

## Requirements

Claude Code with network access to indahl.ai.

## Services this plugin contacts

- indahl.ai (https://indahl.ai/mcp), the read-only MCP server. Tool calls send the question's parameters to indahl.ai. Our server code stores no queries, and Cloudflare, which serves the site, keeps its standard request records. Do not put private data in a query.

Nothing else is contacted. The tool list and responses are treated as data, not instructions.

## Privacy and terms

Privacy: https://indahl.ai/privacy
Terms: https://indahl.ai/terms

Heuremen LLC, https://indahl.ai. Source: https://github.com/indahl-ai/indahl.ai/tree/main/claude-plugins/src/indahl-data

## Credits

Refereed before release by the outside referee at Heuremen LLC (13 Nov 2026): every fix from her review was applied before this version shipped.
