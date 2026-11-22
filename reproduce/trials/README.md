# TRIALS reproduce kit

Heuremen LLC · https://indahl.ai/trials · https://indahl.ai/reproduce

This kit recomputes the TRIALS headline number and its outcome label with the desk’s own code, from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `c0198e3bcf6f733e76fda3767f5eb6d23187cc889a1194cc25803da53363736b`.

## What it reproduces

The headline as the live feed https://indahl.ai/trials/live.json served it at the feed stamp 2026-11-21 23:14 UTC, read by us at 2026-11-22T00:03:15Z. The feed bytes had sha256 `eb8a36b3794d84e7d3cd7c53eb7435efd4e39bd563bc56938ee580259f61f3ba`.

- number: 21.5%
- value: 0.2151
- interval: 0.2098 to 0.2205
- outcome: ABOVE

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk’s scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Sources and their terms

As the TRIALS data pack lists them. Credit each source when using its values.

- ClinicalTrials.gov API v2, https://clinicaltrials.gov/data-api/api. U.S. National Library of Medicine, public data, cite ClinicalTrials.gov.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/records.jsonl | 7,095,810 | `6c1067c4a505e9f9e34bb01e759f27ac083ac8cdea62a3eb81ba211d3344f15d` |
| data/read_at.txt | 55 | `fac23cf96c2a1a75c0ef751861eac247d4a20cdbe71fea244c6e9071e5c2eecb` |

## Code

The desk’s own scripts, byte for byte, under code/. They run in this order: code/trials_summary.py. The same files are in the public repository under code/trials/.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
