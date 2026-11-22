# Indahl Readcheck

`indahl-readcheck`

Refuses a git commit that adds a reading (a results, outcomes or readings file) unless a complete check block, `CHECK.json`, sits beside it. The block has one answer for each Heuremen Standard recount requirement, REQ-01 to REQ-13. Use it in a repository where results files are committed and each should carry a record of what was checked.

## What you get

- A hook that blocks `git commit` when a staged reading has no complete `CHECK.json` in its folder or above.
- A command that writes a blank block, verifies one, or checks every staged reading.
- Per-repository file patterns through `.readcheck.json`.

## How to use

Run `/readcheck` followed by what to check. For example:

```
/readcheck new results/run-12 "Paired accuracy difference on the held-out set"
```

Other forms: `/readcheck verify <folder>` and `/readcheck staged`. The answers in a block are `holds: <what you checked>`, `not applicable: <why>`, or what was found and fixed. A blank answer or one still reading TODO fails.

## Install

```
/plugin marketplace add indahl-ai/indahl.ai
/plugin install indahl-readcheck@heuremen
```

## Requirements

Python 3 (`python3`, or `python` on Windows) and git.

## Services this plugin contacts

None. It runs on your machine and reads your repository.

## Privacy and terms

Privacy: https://indahl.ai/privacy
Terms: https://indahl.ai/terms

Heuremen LLC, https://indahl.ai. Source: https://github.com/indahl-ai/indahl.ai/tree/main/claude-plugins/src/readcheck

## Credits

Refereed before release by the outside referee at Heuremen LLC (13 Nov 2026): every fix from her review was applied before this version shipped.

Windows fix, 14 Nov 2026: The referee asked, the operator found and fixed. The outside referee on our work asked whether `python3` resolves on Windows. The operator ran it on a Windows machine, found it was the Microsoft Store stub that runs nothing (exit 49), so the hook would fail without a word and the check would be silently off, and fixed it in every plugin hook. The hook now falls back to `python`.

## In this copy

The plugin directory accepts command hooks only from Verified organizations, so this copy has the check commands and not the automatic commit gate. The full plugin, gate included, installs from our marketplace: `/plugin marketplace add indahl-ai/indahl.ai` then `/plugin install indahl-readcheck@heuremen`.

## How the scripts arrive

This copy carries no executable file. Its commands fetch each script from the public repository github.com/indahl-ai/indahl.ai at a pinned commit and run it only if its sha256 matches the value written in the command:

- https://raw.githubusercontent.com/indahl-ai/indahl/main/pinned/5f4dd3b6d4e8/claude-plugins/src/readcheck/scripts/readcheck.py
  sha256 5f4dd3b6d4e8dee9faa3ec13b781d6e2c7e5f5863323fa2bc1e8082f89dc96fa

The same scripts are bundled directly in the version in our own marketplace (`/plugin marketplace add indahl-ai/indahl.ai`).
