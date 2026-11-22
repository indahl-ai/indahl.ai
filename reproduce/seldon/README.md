# SELDON reproduce kit

Heuremen LLC · https://indahl.ai/seldon · https://indahl.ai/reproduce

This kit recomputes the SELDON headline number and its outcome label with the desk’s own code, from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later with none (standard library) (PyPI). It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `6006080a590859c19528a680d7f34591b20c0faa6d28346e0015bb7d9fbdabc0`.

## What it reproduces

The headline as the live feed https://indahl.ai/seldon/live.json served it at the feed stamp 2026-11-22T22:25:55Z, read by us at 2026-11-22T22:30:07Z. The feed bytes had sha256 `38cf6ed97ada221a233bfce1ac6d0ceef808e8e90190805e5a1c6e74b623859a`.

- number: 84.6%
- value: 0.8462
- interval: 0.7333 to 1.0
- outcome: ABOVE

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk’s scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/seldon_live.json | 40,202 | `38cf6ed97ada221a233bfce1ac6d0ceef808e8e90190805e5a1c6e74b623859a` |
| PLAN.md | 8,631 | `0800f1522c9e7125de3c9443407bc60de57ee5a201d25cebfa2e1b7c362b93bd` |
| data/plan_seal.json | 580 | `9ce3245ffa8f65f4b9055f7ba820d639706000d07d25b369bf2791558ca4e253` |
| data/stated_ranges.json | 58,202 | `1af69d3e0a9c262e393b051f19040c94c35445c7a07c35cf419b03441014933a` |
| data/imf_events.json | 15,445 | `60ad5ffafae9e557c7f6e81d2ebb56b2fd149c48c5d89d849042324cbdcfee24` |
| data/raw/cbo_actuals/actual_GDP.csv | 632 | `eb90d2eb38d8f7d5f3af27c9600bf52d4dcc8903e8e196191ba562f5800c10b4` |
| data/raw/cbo_actuals/actuals.csv | 38,624 | `810e101e0691d9f1d734e8de2578bf69d6343396151ffa5eea7a4e4c3a2bf996` |
| data/raw/cbo_actuals/debt_actuals_pct_GDP.csv | 1,839 | `b21ef4456d15044268a0a95d4f6c36c1071b0a1b290a1ca30355121e43fb4de9` |
| data/raw/cbo_actuals/deficit_actuals_pct_GDP.csv | 1,953 | `40926316f6b562e057cf13c5c26aff21874d8f760c044171518cbb2691976ee6` |
| data/raw/cbo_actuals/eval_projections_commit.txt | 62 | `b3c70f9c44a36dc2c35022c2c186834f7b2ddb3bc9d5b138b49bd611161ba7eb` |
| data/raw/cbo_data/cbo_data_commit.txt | 62 | `48bc2b86ca01ff73cf9c20fca60b1f3886b63643043d47bb129c9b1cec5c0865` |
| data/raw/cbo_data/economic_projections_calendar_2024-02.csv | 80,365 | `8802a8ccd17ac3583d6103ef3f072c760131fa377503bb7ef35fdac89d42ee3e` |
| data/raw/cbo_data/economic_projections_calendar_2024-06.csv | 69,308 | `4e8c9b5f6600a68d477a8d5767240d7f04af2a98071471ec878de1d6c806a970` |
| data/raw/cbo_data/economic_projections_calendar_2025-01.csv | 82,652 | `dfe6699335b84dfaaca1ae92ee2671b4e1ed766cf0e7eedfc780897c1ee653e4` |
| data/raw/cbo_data/economic_projections_calendar_2025-09.csv | 11,269 | `43fc2e319349a4a8e9007f5f79ae2d1f72aebb189ca6c44794657623ca262f66` |
| data/raw/cbo_data/economic_projections_calendar_2026-02.csv | 88,093 | `6b54df40058d206247e78fadfe5ebd11e02ae29efd2f0e1a4a86b6767c9ca559` |
| data/raw/cbo_data/economic_projections_quarterly_2025-09.csv | 46,908 | `31c2986c194dd83ea188399961dfc87c6c694adbde13e6a102c934bef439591c` |
| data/raw/cbo_data/historical_economic_annual_cy_2026-02.csv | 235,221 | `b7a11ad35e5b1d9dc90f029ef21eca1eafe7834cf3ca92ac6b84d865076fb284` |
| data/raw/cbo_data/historical_economic_quarterly_2022-05.csv | 841,182 | `ed06d49482379829658b29fbd4032ca73ad6d0737b04cb3818c789bc56a7257c` |
| data/raw/cbo_data/historical_economic_quarterly_2023-02.csv | 851,993 | `c75df7240be757e70a6bceb39fcbc6f7002abf72d4bbbcfe19c56a9a3dca6803` |
| data/raw/cbo_data/historical_economic_quarterly_2023-07.csv | 767,052 | `109210126f0808ba6150625d868321daf5af26cbbec21b6e121a78e31cea36f5` |
| data/raw/cbo_data/historical_economic_quarterly_2024-02.csv | 866,526 | `0df6ffb5e38afed00b1a65a12ebc98ae3b142c410afe97854ccd89d8e860fef0` |
| data/raw/cbo_data/historical_economic_quarterly_2024-06.csv | 867,707 | `f65a56ec08297fa1a9190133e8631d88649d2a8ae8b55e68770e4098ed98328d` |
| data/raw/cbo_data/historical_economic_quarterly_2025-01.csv | 860,669 | `14df2a1dda723a85d4b55d920c8eebf3c747f72130456bba57dc5741dbd269de` |
| data/raw/cbo_data/historical_economic_quarterly_2026-02.csv | 1,013,425 | `e51170462dab40316574a38f691f302794aaa7500f7f89b97d79d4dfa4193934` |

## Code

code/clock_run.py runs the desk’s own scripts in code/, byte for byte, and changes the clock only. It runs seldon_tick.py with the clock pinned to the time the published run read (the generated field of data/seldon_live.json). The tick reads no network and the clock only stamps the run. The same files are in the public repository under code/seldon/. Scripts that run: code/clock_run.py seldon_tick.py data/seldon_live.json.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.

## Note

data/stated_ranges.json holds every CBO two-thirds range the desk counts, each with the words that print it and the report page, checked against the report text by build_stated.py before any actual was opened. data/raw/cbo_actuals holds actuals.csv, actual_GDP.csv and CBO percent-of-GDP files from US-CBO/eval-projections, and data/raw/cbo_data the economic vintages from US-CBO/cbo-data (works of the US government). data/imf_events.json holds the WEO probability statements with their quotes and the World Output figures read from the next October WEO. The CBO report PDFs and WEO chapters stay with the desk, listed with sha256 in data/stated_ranges.json and data/imf_events.json.
