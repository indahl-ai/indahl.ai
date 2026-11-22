# ARES reproduce kit

Heuremen LLC · https://indahl.ai/ares · https://indahl.ai/reproduce

This kit recomputes the ARES headline number and its outcome label with the desk’s own code, from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later with none (standard library) (PyPI). It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `9a571f396218edaa23e43a66cc94ee236638effeee24d169c434b525372d0ca2`.

## What it reproduces

The headline as the live feed https://indahl.ai/ares/live.json served it at the feed stamp 2026-11-22T16:22:19Z, read by us at 2026-11-22T16:22:35Z. The feed bytes had sha256 `1b7aaf41a091ace97275028b65e978521f5a189289d80493329ae9e0152f2110`.

- number: 518 of 4,145
- value: 0.12496984318455971
- interval: 0.1062891622186122 to 0.14323040380047505
- outcome: none, this headline carries no outcome label

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

Not included. The raw UCDP and GDELT files carry fields ARES never stores, so the fetch keeps only the province-month tables. Every source file is public and named with its hash, and fetch/ rebuilds the tables from them, so this kit carries no copy of the source data. MANIFEST.json lists each input file the desk’s scoring read, with its size, its sha256 and the time it was last written. Those exact files are kept and this kit is rerun on them before every release.

The input files are what the desk kept from its reads of the sources, with the time of each read where the desk records it. To check them, read the sources below again and compare. With a copy of the input files, `python3 run.py --check --inputs DIR` reruns the kit on them. A file whose sha256 differs from MANIFEST.json is named and the run stops. Sources change, so a later read can differ from ours.

- UCDP GED 26.1, https://ucdp.uu.se/downloads/ged/ged261-csv.zip, and UCDP Candidate 26.01.26.09, https://ucdp.uu.se/downloads/candidateged/GEDEvent_v26_01_26_09.csv (CC BY 4.0, sha256 in data/ucdp_pm.json).
- GDELT 2.0 event exports listed in https://data.gdeltproject.org/gdeltv2/masterfilelist.txt, each checked against its MD5 (data/gdelt_files.tsv).
- Natural Earth Admin 1, 1:10m, public domain (sha256 in data/crosswalk.json), used only to group places, never drawn.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/ares_live.json | 1,067,850 | `1b7aaf41a091ace97275028b65e978521f5a189289d80493329ae9e0152f2110` |
| data/ucdp_pm.json | 413,194 | `dcab1ffe5fbf50ace6cce4069b819b460dd97302f86bb3e7bd004a676287f2ad` |
| data/gdelt_pm.json | 439,406 | `702495d47625003863b1ec2768394f1cb654862c13e5dba6d87785432db8dab0` |
| data/gdelt_files.tsv | 2,071,448 | `2033c5a56af8f51aa7b309a809eb91db1b126dad6a4879e0271080475243b8ee` |
| data/crosswalk.json | 304,346 | `4868543b3bde3985d479e43d544773003d13b6dd78ae1998e5544f1e3e218704` |
| data/crosswalk_seal.json | 193 | `5ab9b50b4fe2e1c01d31eca9f2805dd451ced20f91228912b3819067eecd4bbd` |
| data/ne_units.json | 63,165 | `ad7d5a8f18f6a62e32bb09d85e971e7a71f0eebfeb0749abb49792222ba3a6bb` |
| data/ares_kit.csv.gz | 46,722 | `dcf51b086cd287cf67203fec9f79e30d92512c07ec732b7606a1d61604d98d22` |
| PLAN.md | 10,980 | `21e08738bc8c8fb1070ab9345b084378fd09eb78c7427f520dd6cf1b187ac86d` |
| data/plan_seal.json | 499 | `d185ce6416e04041ffba91f87ae70994ff5a1a9155ee6d4079eb2dbc6923001f` |

## Code

code/clock_run.py runs the desk’s own scripts in code/, byte for byte, and changes the clock only. It runs ares_tick.py with --offline and the clock pinned to the time the published run read (the generated field of data/ares_live.json), which sets the window. The same files are in the public repository under code/ares/. Scripts that run: code/clock_run.py ares_tick.py data/ares_live.json --offline.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
