# SECRECORDS reproduce kit

Heuremen LLC · https://indahl.ai/secrecords · https://indahl.ai/reproduce

This kit recomputes the SECRECORDS headline number and its outcome label with the desk's own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `0a871fcaed515a931910e8d7e73335656d5bae01e1dcdd5227e014dd25aff4d9`.

## What it reproduces

The headline as the live feed https://indahl.ai/secrecords/live.json served it at the feed stamp 15 Nov 17:41, read by us at 2026-11-15T21:41:23Z. The feed bytes had sha256 `23cd62dae0210f2fd6dd5912dc56234b4b8c35e7464d42f7b732bcbd21c2ffaf`.

- number: 14%
- value: 0.1448
- interval: 0.0967 to 0.2113
- outcome: ABOVE

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

Not included. The Tranco list draws on a non-commercial input and a share-alike input, so this kit carries no copy of the source data. MANIFEST.json lists each input file the desk's scoring read, with its size, its sha256 and the time it was last written. Those exact files are kept and this kit is rerun on them before every release.

The input files are what the desk kept from its reads of the sources, with the time of each read where the desk records it. To check them, read the sources below again and compare. With a copy of the input files, `python3 run.py --check --inputs DIR` reruns the kit on them. A file whose sha256 differs from MANIFEST.json is named and the run stops. Sources change, so a later read can differ from ours.

- The domain list: the top 1,000 rows of the Tranco list of the date in data/listdate.txt of the desk, https://tranco-list.eu/
- For each domain, the first HTTPS response of https://DOMAIN/ (no redirect followed) and its SPF record read through DNS over HTTPS, as secrecords_tick.py does. Each row of data/domains.json carries the time it was read in its read field.

## Sources and their terms

As the SECRECORDS data pack lists them. Credit each source when using its values.

- Tranco list, https://tranco-list.eu/. Tranco terms, built from inputs that include CC BY-NC and share-alike data.
- HTTPS headers and DNS records of each domain, https://indahl.ai/secrecords. Public protocol facts, our own reads.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/domains.json | 368,948 | `c0613790bf50be5788ff34f3847920914b7d8429e706d784901d5f1e2a0f38fd` |
| summary_secrecords.json | 15,911 | `23cd62dae0210f2fd6dd5912dc56234b4b8c35e7464d42f7b732bcbd21c2ffaf` |

## Code

The desk's tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/secrecords_score.py is the scoring step of that script and nothing else: secrecords_tick.py lines 150 to 162, read_share, the grp function and the comparison block. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/secrecords_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
