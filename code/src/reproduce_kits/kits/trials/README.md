# TRIALS reproduce kit

Heuremen LLC · https://indahl.ai/trials · https://indahl.ai/reproduce

This kit recomputes the TRIALS headline number and its outcome label with the desk's own code, from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `024f8a5919f0578fdf39e0aa808df72436378fa75983f78ab9444dd916a178ff`.

## What it reproduces

The headline as the live feed https://indahl.ai/trials/live.json served it at the feed stamp 2026-11-15 19:18 UTC, read by us at 2026-11-15T21:43:33Z. The feed bytes had sha256 `550910db3fa22dec289de228fd62cf62387ceb527111ff3b90c928b23a2bf018`.

- number: 21.5%
- value: 0.2153
- interval: 0.21 to 0.2208
- outcome: ABOVE

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk's scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Sources and their terms

As the TRIALS data pack lists them. Credit each source when using its values.

- ClinicalTrials.gov API v2, https://clinicaltrials.gov/data-api/api. U.S. National Library of Medicine, public data, cite ClinicalTrials.gov.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/records.jsonl | 7,089,284 | `768a93bf97205627839c3af3c5b06aec82f314a39913fca1e1057a1d9758564e` |
| data/read_at.txt | 55 | `d3e6cba32d26f6671afd6ba3375a60076d5962fef0278ad0b8969ef8b0bdef91` |

## Code

The desk's own scripts, byte for byte, under code/. They run in this order: code/trials_summary.py. The same files are in the public repository under code/trials/.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
