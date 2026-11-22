---
description: Write, fill or verify a Heuremen Standard check block (CHECK.json) for a reading before it is committed
argument-hint: new <folder> "<the reading>" | verify <folder> | staged
---

## Get the script first

The script is not stored in this plugin. Fetch it from the public Heuremen LLC repository at the pinned commit, check its
sha256, and only then run it. If the download or the check fails, stop and tell the user; never run a file that did not pass.
Show the user the commands before running them the first time.

```bash
F="$HOME/.cache/indahl-plugins/readcheck/readcheck-5f4dd3b6d4e8.py"
[ -f "$F" ] || { mkdir -p "$(dirname "$F")" && curl -fsSL "https://raw.githubusercontent.com/indahl-ai/indahl/main/pinned/5f4dd3b6d4e8/claude-plugins/src/readcheck/scripts/readcheck.py" -o "$F.part" && python3 -c "import hashlib,sys; sys.exit(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest() != '5f4dd3b6d4e8dee9faa3ec13b781d6e2c7e5f5863323fa2bc1e8082f89dc96fa')" "$F.part" && mv "$F.part" "$F"; }
```
Source: https://raw.githubusercontent.com/indahl-ai/indahl/main/pinned/5f4dd3b6d4e8/claude-plugins/src/readcheck/scripts/readcheck.py (sha256 5f4dd3b6d4e8dee9faa3ec13b781d6e2c7e5f5863323fa2bc1e8082f89dc96fa).


Run the readcheck tool for: $ARGUMENTS

- `new <folder> "<reading>"`: run `python3 "$HOME/.cache/indahl-plugins/readcheck/readcheck-5f4dd3b6d4e8.py" new <folder> --what "<reading>"`, then fill every
  REQ-01 to REQ-13 answer in the new CHECK.json from what was actually done for this reading (read the code, the data and the run logs;
  never answer from memory). Each answer says what was checked: "holds: <what>", "not applicable: <why>", or what was found and fixed.
  If a requirement was not met, say so in its answer and fix the reading where you can.
- `verify <folder>`: run `python3 "$HOME/.cache/indahl-plugins/readcheck/readcheck-5f4dd3b6d4e8.py" verify <folder>` and report what is missing.
- `staged`: run `python3 "$HOME/.cache/indahl-plugins/readcheck/readcheck-5f4dd3b6d4e8.py" staged` in the repository and report every staged reading without a
  complete block.

The gate hook refuses a `git commit` that stages a reading (files named like *results*, *outcomes*, *readings*, RESULTS*.md) unless a
complete CHECK.json sits in its folder or above. A repository can set its own file patterns in `.readcheck.json` as {"globs": [...]}.
