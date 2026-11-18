# CADENCE reproduce kit

Heuremen LLC · https://indahl.ai/cadence · https://indahl.ai/reproduce

This kit recomputes the CADENCE headline number and its outcome label with the desk's own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `ef5f789c420e673298c1ff1cde1398ca11280f18262812a72e91a80b00df356e`.

## What it reproduces

The headline as the live feed https://indahl.ai/cadence/live.json served it at the feed stamp 15 Nov 21:36, read by us at 2026-11-15T21:41:33Z. The feed bytes had sha256 `e65bdefb90eced79d5643ecba306ea6f6c6d7a498137d6705c0ec742d9895ab5`.

- number: 15.8 years (5,787 days)
- value: 5787
- outcome: none, this headline carries no outcome label

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk's scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Sources and their terms

As the CADENCE data pack lists them. Credit each source when using its values.

- Federal agency data.json catalogues (DCAT-US), https://resources.data.gov/resources/dcat-us/. U.S. government work, public domain (17 U.S.C. 105).

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/portal_bls.json | 828 | `c1b32fbce7915286745961ea133f2a9803315e6c48566e0b0e45dddf723c818c` |
| data/portal_cdc.json | 120,471 | `93673a0d83cb3d41313eef0a6396c5ca7a4b57b7e11daec3c04ba4ce12dff789` |
| data/portal_cms.json | 2,271,491 | `ca3d1f8715797558c7315aa6a87b14d052bd7eaa0834033a266d025a0bc46f56` |
| data/portal_energy.json | 98,897 | `3d3d482c53990b9bc5abbb2798406bd6f25aaec58eeecdf879894d2d849784a9` |
| data/portal_healthcare_gov.json | 39,052 | `5979e53659e67d098cda899d191c8b04a6f0ce8cfdab3429a188c297aba1b6f6` |
| data/portal_healthdata_gov.json | 444,375 | `ad0f86cb8b0c860a306596853a9506a644a63c4ef93213458718ef3cf2b6be66` |
| data/portal_labor.json | 98,683 | `a6f781bc79ab08ce561509038c0b9eabedac4d073f80199c9b7479d33460a440` |
| data/portal_veterans_affairs.json | 205,199 | `33baeb1d3ad3e71623b41ef7d515298f18583d14d74e5000d6a6877502e90617` |

## Code

The desk's tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/cadence_score.py is the scoring step of that script and nothing else: cadence_tick.py lines 8 to 32 and 70 to 95, the interval and date readers and the series and overdue loop. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/cadence_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
