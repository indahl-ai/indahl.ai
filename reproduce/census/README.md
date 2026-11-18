# CENSUS reproduce kit

Heuremen LLC · https://indahl.ai/census · https://indahl.ai/reproduce

This kit recomputes the CENSUS headline number and its outcome label with the desk's own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `43f7368f318b9aef23d0af04771a2eb2dcdbc8eb4e81455405b5762fdccc2f1b`.

## What it reproduces

The headline as the live feed https://indahl.ai/census/live.json served it at the feed stamp 2026-11-15T02:03:00Z, read by us at 2026-11-15T21:41:44Z. The feed bytes had sha256 `d7875a646a0e3920eef403796354d3d8e9b55515b62d90c6843e16143b286beb`.

- number: 117 of 117
- value: 1.0
- interval: 0.9682096231761248 to 1.0
- outcome: ABOVE

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk's scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Sources and their terms

As the CENSUS data pack lists them. Credit each source when using its values.

- U.S. Census Bureau Economic Indicators Time Series API (new residential sales, new residential construction, monthly retail trade), https://www.census.gov/data/developers/data-sets/eits.html. U.S. government work, public domain (17 U.S.C. 105). This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.
- Federal Reserve Bank of St. Louis ALFRED archival series HSN1F, HOUST, PERMIT, COMPUTSA, RSAFS, https://alfred.stlouisfed.org/. Census Bureau and HUD data, public domain, citation requested.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/census.json | 1,934,936 | `c1cd20d37deaf3cc4b48876b4fe77c8750dc5a624a40f5ba0b3aef2e2b6dbe40` |
| summary_census.json | 66,488 | `3523705b24855e62cd3e7da9658c29a80c5f097534d3eeca28d52e1779eb28f6` |

## Code

The desk's tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/census_score.py is the scoring step of that script and nothing else: census_tick.py cells() and the outcome rule against 90 percent, for the national total cells. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/census_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.

## Note

data/census.json holds every row the run scored, first print, later value and stated width, from the ALFRED vintages and dated Census API copies. The gate result comes from summary_census.json, the summary of the same run.
