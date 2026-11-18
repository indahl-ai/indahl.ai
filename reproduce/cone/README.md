# CONE reproduce kit

Heuremen LLC · https://indahl.ai/cone · https://indahl.ai/reproduce

This kit recomputes the CONE headline number and its outcome label with the desk's own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `3a3cc8410a5f9d20204e42be09f230296d0a5d27a7f22182b340590551e02201`.

## What it reproduces

The headline as the live feed https://indahl.ai/cone/live.json served it at the feed stamp 2026-11-15T14:21:38Z, read by us at 2026-11-15T21:41:35Z. The feed bytes had sha256 `caa9f65a0bb2ebb9a6f5a2e95f1fe0a12776da2085976fb57a133b918e2e6985`.

- number: 697 of 1,315
- value: 0.53
- interval: 0.4515 to 0.6041
- outcome: CANNOT_TELL

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk's scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Sources and their terms

As the CONE data pack lists them. Credit each source when using its values.

- NOAA NHC ATCF a-decks (official forecasts) and b-decks, https://ftp.nhc.noaa.gov/atcf/. U.S. government work, public domain (17 U.S.C. 105).
- NOAA NHC HURDAT2 best track, https://www.nhc.noaa.gov/data/hurdat/. U.S. government work, public domain (17 U.S.C. 105).
- NOAA NHC cone definition and verification tables, https://www.nhc.noaa.gov/aboutcone.shtml. U.S. government work, public domain (17 U.S.C. 105).
- Internet Archive Wayback Machine copies of the NHC cone page, https://web.archive.org/. Internet Archive terms of use, https://archive.org/about/terms.php.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/cone.json | 19,796,944 | `f6cc44d0a803a778d3952a055c75588dacf9b4420b322c9858402ae3712b5a63` |

## Code

The desk's tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/cone_score.py is the scoring step of that script and nothing else: cone_tick.py lines 18 to 25, 200 to 222 and 398 to 401, the storm-level bootstrap and the whole-path cells. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/cone_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.

## Note

data/cone.json holds every forecast path the run scored, inside or outside the cone, from the NHC a-decks and HURDAT2 (about 300 MB of NHC files). This kit starts from those scored paths.
