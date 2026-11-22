# ZEUS reproduce kit

Heuremen LLC · https://indahl.ai/zeus · https://indahl.ai/reproduce

This kit recomputes the ZEUS headline number and its outcome label with the desk’s own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later with numpy (PyPI). It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `a5bdac732f9a5db530dfe954c0db51980b8b3980c652506c8e2284bc585399f6`.

## What it reproduces

The headline as the live feed https://indahl.ai/zeus/live.json served it at the feed stamp 2026-11-22T21:40:47Z, read by us at 2026-11-22T21:41:39Z. The feed bytes had sha256 `abfe3c6ada739d76388d3e060ba02b4658d0a77b0d6b77e52a5d46c8bddf4df6`.

- number: 48.6%
- value: 0.4861
- interval: 0.4376 to 0.5341
- outcome: CONSISTENT

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk’s scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/zeus_rows.json | 3,797 | `34f38bb7d21fea6c0bcde7cc0c5c44b3bd9ae25cc8e5087daca43989c5fb7f8b` |

## Code

The desk’s tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/zeus_score.py is the scoring step of that script and nothing else: zeus_tick.py lines 24 to 28, 76 to 84 and 239 to 253: FLOOR, SEED and NBOOT, floor_outcome(), the day block bootstrap boot_ratio() and the headline cells. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/zeus_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.

## Note

data/zeus_rows.json holds, for each outlook day the run read, the thunder-area grid points and how many had a GLM flash with the good quality flag within 25 and within 10 statute miles in the valid period, counted by zeus_tick.py from the SPC Day 1 outlooks (Iowa Environmental Mesonet archive) and the GOES-19 and GOES-18 GLM flash files (NOAA open data on AWS, public domain). The flash files kept by the desk are about 48 MB. This kit starts from the counts.
