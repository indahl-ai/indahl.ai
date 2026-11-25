# CADENCE reproduce kit

Heuremen LLC · https://indahl.ai/cadence · https://indahl.ai/reproduce

This kit recomputes the CADENCE headline number and its outcome label with the desk’s own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `7933c886d1748f0ad7e5f37935dc478a35e9b3f2690469f8c5649601781b0aa3`.

## What it reproduces

The headline as the live feed https://indahl.ai/cadence/live.json served it at the feed stamp 25 Nov 06:47, read by us at 2026-11-25T06:48:55Z. The feed bytes had sha256 `a15075ad8caa0b81454ab55da6fcb5a6753cf2224c21e63d97b69656e8d282e6`.

- number: 638 of 1,243
- value: 638
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
| data/portal_bls.json | 828 | `e49be497741859dd80ca11f7fb9ccac3ae5301202d37014a99010d87777df389` |
| data/portal_cdc.json | 125,724 | `55f67d441b46b0b9c7d35475b101f8da89356b6d76a1858bd13874a1345e24d8` |
| data/portal_cms.json | 2,284,005 | `cd8369b0ca3c6b9510b43b02463b8d5de1bef8087f40fe37549a55e4aab383e4` |
| data/portal_energy.json | 98,897 | `88388965e53a84f874e440a65b24d71a8fde1837b1e575faeeef1eec3795211a` |
| data/portal_healthcare_gov.json | 39,052 | `ed795dbf58a40854ccbf52a2a769b21c03ad97a075ccd60aca380d8c5784c298` |
| data/portal_healthdata_gov.json | 449,075 | `968ae8ad5d52a2050da6327474e9668ae1f17efb0fe7c29d4e7eb1e94598f9c2` |
| data/portal_labor.json | 98,681 | `6b7598eea824084998bea7a61244c0277b331067f18099bf198a9a2f90f6c690` |
| data/portal_veterans_affairs.json | 205,198 | `9b0e96f6eaad4810d6a3bb7cb072dcd969ab1bd2969e7ed34899e48e8652f27c` |

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
