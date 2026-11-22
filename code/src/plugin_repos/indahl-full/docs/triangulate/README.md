# Indahl Triangulate

`indahl-triangulate`

Puts one question to three independent seats run blind, then reads where they agree and where they split. Use it when a decision, a claim, a number or a judgment matters enough that one reading is not enough.

## What you get

- One outcome: ABOVE, BELOW, CONSISTENT or CANNOT_TELL, or HOLDS, FAILS, SPLIT or CANNOT_TELL for a yes or no question.
- What would decide it.
- A `RECEIPT.md` holding every seat's answer verbatim.

## How to use

Run `/triangulate` followed by what to check. For example:

```
/triangulate Does the vendor's stated 99.9 percent uptime hold for the last quarter?
```

## Install

```
/plugin marketplace add indahl-ai/indahl.ai
/plugin install indahl-triangulate@heuremen
```

## Requirements

None. Runs inside Claude Code.

## Services this plugin contacts

The seats run inside your session. The plugin also connects the read-only indahl.ai server (https://indahl.ai/mcp, no key); when a seat calls one of its tools, that call's parameters go to indahl.ai.

## Privacy and terms

Privacy: https://indahl.ai/privacy
Terms: https://indahl.ai/terms

Heuremen LLC, https://indahl.ai. Source: https://github.com/indahl-ai/indahl.ai/tree/main/claude-plugins/src/triangulate

## Credits

The outside referee on our work found on 14 Nov 2026 (her item #25) that this skill asked each seat for evidence but never checked it, and counted seats instead of evidence. The grounding rules (UNGROUNDED, SHARED_SOURCE, two grounded seats on independent evidence chains) are hers, applied at the lines she named. Reading the rebuild with her own tools, she found the next gap: a citation counted as grounding without anyone opening it. The skill now opens each seat's evidence with the source-check procedure before counting it.
