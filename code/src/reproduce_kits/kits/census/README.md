# CENSUS reproduce kit

Heuremen LLC · https://indahl.ai/census · https://indahl.ai/reproduce

This kit recomputes the CENSUS headline number and its outcome label with the desk’s own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `1a4440bf8f730442337be269ab734863c1b8b6a7b993e40ae7ff2769468fc98d`.

## What it reproduces

The headline as the live feed https://indahl.ai/census/live.json served it at the feed stamp 2026-11-26T21:57:10Z, read by us at 2026-11-27T01:36:05Z. The feed bytes had sha256 `d26be6b190ad841504752aae636e480775b0cdedae560b7e9dfbeb5b5c0c475e`.

- number: 118 of 118
- value: 1.0
- interval: 0.9684705387979147 to 1.0
- outcome: ABOVE

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk’s scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Sources and their terms

As the CENSUS data pack lists them. Credit each source when using its values.

- U.S. Census Bureau Economic Indicators Time Series API (new residential sales, new residential construction, monthly retail trade), https://www.census.gov/data/developers/data-sets/eits.html. U.S. government work, public domain (17 U.S.C. 105). This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.
- Federal Reserve Bank of St. Louis ALFRED archival series HSN1F, HOUST, PERMIT, COMPUTSA, RSAFS, https://alfred.stlouisfed.org/. Census Bureau and HUD data, public domain, citation requested.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/census.json | 1,949,851 | `db9b7035a2a48384c4f8bf840e61b5df403096545a41c846b72fba5d2f4673fe` |
| summary_census.json | 96,302 | `de5a1eec9bb3ac2bac375b0662ef911776bb4adfbdc1e1ec527d46806dcbb60d` |

## Code

The desk’s tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/census_score.py is the scoring step of that script and nothing else: census_tick.py cells() and the outcome rule against 90 percent, for the national total cells. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/census_score.py. Before every release the gate checks that this extract prints the number the desk published.

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
