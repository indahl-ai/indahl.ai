# CADENCE reproduce kit

Heuremen LLC · https://indahl.ai/cadence · https://indahl.ai/reproduce

This kit recomputes the CADENCE headline number and its outcome label with the desk’s own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `b13b6b4cbc08a6f0570d7806529bb733d58ddaf4f70c99e2c6c4a95c1f49ac8c`.

## What it reproduces

The headline as the live feed https://indahl.ai/cadence/live.json served it at the feed stamp 23 Nov 07:40, read by us at 2026-11-23T08:17:31Z. The feed bytes had sha256 `d0fdce27227b4c2cdf526320350042be618046dbf25da1c3af45d7dd5b3f9e56`.

- number: 640 of 1,243
- value: 640
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
| data/portal_bls.json | 828 | `617c4b3cb75777fdc26a115251d21f61c4f12c4e526e168a7884dea7463bf4f9` |
| data/portal_cdc.json | 125,372 | `6b9cb884dc297059db1df237ba47f3e69e139f802b3f11c708ff56532de1b3ac` |
| data/portal_cms.json | 2,277,889 | `b88d38352ca1581f6be33a2f0dbcd8f5bcfe87b2cd6b9c5afc1224e16d2cd3f7` |
| data/portal_energy.json | 98,897 | `6be3b38ca51e15c4e0f1eab216c98fdab558f52c7ea48835dcd77fb18329a6c4` |
| data/portal_healthcare_gov.json | 39,053 | `2d386712625cf69afc094caba8695021ef9d721d2a372132d3769764fd23c8f7` |
| data/portal_healthdata_gov.json | 449,074 | `0aad92e708dc3aeafac6b992a0b21200938d4474fff08ee66584ac7f899bca29` |
| data/portal_labor.json | 98,682 | `47ed42bc0e645e36df6156f0f340d4ecc8209ddc169b2b04d520ff88f774a325` |
| data/portal_veterans_affairs.json | 205,199 | `42a371ce07cc3a4b0313439979c3355e87e3ee5dabec8e2440155541208fddab` |

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
