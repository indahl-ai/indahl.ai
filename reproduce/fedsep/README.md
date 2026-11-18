# FEDSEP reproduce kit

Heuremen LLC · https://indahl.ai/fedsep · https://indahl.ai/reproduce

This kit recomputes the FEDSEP headline number and its outcome label with the desk's own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `c6978bc2ff30064c0bfe7edb79752a04b912fb7edaf9ed88a8f1bb9571bea7c0`.

## What it reproduces

The headline as the live feed https://indahl.ai/fedsep/live.json served it at the feed stamp 15 Nov 19:17, read by us at 2026-11-15T21:41:32Z. The feed bytes had sha256 `11639752ce0ba1b83624e8f28e855df10ece85681fc07a980cf381b1817aedbb`.

- number: 10 of 37
- value: 0.2703
- interval: 0.0811 to 0.4872
- outcome: CANNOT_TELL

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk's scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Sources and their terms

As the FEDSEP data pack lists them. Credit each source when using its values.

- FOMC Summary of Economic Projections, https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm. U.S. government work, public domain (17 U.S.C. 105).
- BEA NIPA tables, https://www.bea.gov/. U.S. government work, public domain (17 U.S.C. 105).
- BLS unemployment rate LNS14000000, https://www.bls.gov/. U.S. government work, public domain (17 U.S.C. 105).
- Federal Reserve H.15, https://www.federalreserve.gov/releases/h15/. U.S. government work, public domain (17 U.S.C. 105).

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/projections.json | 4,223 | `389aa46dd55e746079d0426e73bf4de42b087088ec596c0fd7cc821e6b031c3b` |
| data/outcomes_day.json | 2,431 | `e61890e9d5bf2da3750f3392f04992a6d91c9b915b23807e2931220c1893199f` |

## Code

The desk's tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/fedsep_score.py is the scoring step of that script and nothing else: fedsep_tick.py lines 24 and 49 to 69, the inside test, the triples and the pooled bootstrap. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/fedsep_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
