# CREDIT reproduce kit

Heuremen LLC · https://indahl.ai/credit · https://indahl.ai/reproduce

This kit recomputes the CREDIT headline number and its outcome label with the desk’s own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later with numpy (PyPI). It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `dc9d388c81bcafc7493de59f6cfe10c450157f909962f7ccc1aed57fda392eb3`.

## What it reproduces

The headline as the live feed https://indahl.ai/credit/live.json served it at the feed stamp 2026-11-20T12:53:49Z, read by us at 2026-11-22T16:02:50Z. The feed bytes had sha256 `290c02837d22a1ffd4da5dfd98d07c2234a0bdb458515c3717149fed747508f5`.

- number: 99.55%
- value: 0.995497
- interval: 0.993501 to 0.996794
- outcome: CANNOT_TELL

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk’s scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Sources and their terms

As the CREDIT data pack lists them. Credit each source when using its values.

- CFPB Consumer Complaint Database (company-level counts only, no complaint text or ZIP code), https://www.consumerfinance.gov/data-research/consumer-complaints/. CC0 as the CFPB search service states, U.S. government work.
- CFPB Consumer Response Annual Reports 2021 to 2025, https://www.consumerfinance.gov/data-research/research-reports/. U.S. government work, public domain (17 U.S.C. 105).
- CFPB Terms of Credit Card Plans survey, https://www.consumerfinance.gov/data-research/credit-card-data/terms-credit-card-plans-survey/. U.S. government work, public domain (17 U.S.C. 105).
- Federal Reserve G.19 Consumer Credit, terms of credit, https://www.federalreserve.gov/releases/g19/. Federal Reserve Board data, public.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/cache/agg_a2516688944feb17.json | 22,572,830 | `a003b4a16065b1999b37a9d873789ad1cf87585b72788de6c2b586215e2c2d12` |

## Code

The desk’s tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/credit_score.py is the scoring step of that script and nothing else: credit_tick.py lines 23, 39, 128 to 150 and 195 to 200, the printed band, the company-month block bootstrap and ruler one for 2025. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/credit_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.

## Note

The aggregate file holds company, month, product family, complaints and complaints not answered in time, counted by credit_tick.py from the CFPB complaint database download (about 365 MB, no complaint text kept). Its name carries the first 16 characters of the sha256 of the download it was counted from.
