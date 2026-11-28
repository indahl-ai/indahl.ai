# CADENCE reproduce kit

Heuremen LLC · https://indahl.ai/cadence · https://indahl.ai/reproduce

This kit recomputes the CADENCE headline number and its outcome label with the desk’s own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `ee1adc9c3a4a165bd6c9f038853295b4484f563b67f6b0d6ab6b78a16cab30b0`.

## What it reproduces

The headline as the live feed https://indahl.ai/cadence/live.json served it at the feed stamp 28 Nov 10:47, read by us at 2026-11-28T10:48:48Z. The feed bytes had sha256 `c9fabf1734353a18c39f0fb0839dd30628a5fa2d21992909ab0ead843efaf401`.

- number: 639 of 1,243
- value: 639
- outcome: none, this headline carries no outcome label

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk’s scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Sources and their terms

As the CADENCE data pack lists them. Credit each source when using its values.

- Federal agency data.json catalogues (DCAT-US), https://resources.data.gov/resources/dcat-us/. U.S. government work, public domain (17 U.S.C. 105).

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/portal_bls.json | 828 | `857eec71a865e4a3f9299c58dfaf241524c506353a5e01225eb5b458b00f0bbf` |
| data/portal_cdc.json | 125,724 | `d0e2de02939982cc7213664be91de8b3b51b40385ab5043596f365ecfc2a0f52` |
| data/portal_cms.json | 2,287,301 | `835e026b7a69d7191d4ebeedfec152413a084e2ff61d9176a5c4dcd826253a65` |
| data/portal_energy.json | 98,897 | `0cbfbf77e697814dc26b1af2b37b718c5247b250d01c8f9f84b76fc04abbd1e2` |
| data/portal_healthcare_gov.json | 39,053 | `d619177eea11337d99df3843be765344f3c08e23218e0e008c38c304f8c9ac43` |
| data/portal_healthdata_gov.json | 449,464 | `da59f2ff11bf34350aab8a5eef529ba8781aab1b1b18a388636686c3646477c2` |
| data/portal_labor.json | 98,682 | `654b4d1f5f4b2c1e1a221d2f7e897b2a8bd00e83ae1f75d554ad3b911c0781bf` |
| data/portal_veterans_affairs.json | 205,198 | `40ad68bee5afa42ee0e1425d08cb2c82a4450713dbc65481bb134815e7539d35` |

## Code

The desk’s tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/cadence_score.py is the scoring step of that script and nothing else: cadence_tick.py lines 8 to 32 and 70 to 95, the interval and date readers and the series and overdue loop. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/cadence_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
