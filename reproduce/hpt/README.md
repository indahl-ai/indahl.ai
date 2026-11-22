# HPT reproduce kit

Heuremen LLC · https://indahl.ai/hpt · https://indahl.ai/reproduce

This kit recomputes the HPT headline number and its outcome label with the desk’s own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `1e7d500a04013231e66f04bb25966d5dc381cfe6b3c2a8e22cf239f18c985082`.

## What it reproduces

The headline as the live feed https://indahl.ai/hpt/live.json served it at the feed stamp 21 Nov 13:49, read by us at 2026-11-22T16:02:17Z. The feed bytes had sha256 `5265f22c263958631f72dfac0ba7972fc930f5992f3c7ba44a5756503de25502`.

- number: 474 of 985
- value: 0.4812
- interval: 0.4501 to 0.5124
- outcome: CANNOT_TELL

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

The exact files the desk’s scoring read, stored gzip-compressed under inputs/. run.py checks the sha256 of each one before it runs.

## Sources and their terms

As the HPT data pack lists them. Credit each source when using its values.

- Hospital cms-hpt.txt files under the CMS price transparency rule, https://www.cms.gov/priorities/key-initiatives/hospital-price-transparency. Public files published under a federal rule, presence and header facts only.
- Wikidata (US hospitals with official websites), https://query.wikidata.org/. CC0 1.0.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/domains.json | 445,118 | `7805e095cec597ccf5c230f22f2c9c908e65a2182e58e150323285d10fe52d19` |
| summary_hpt.json | 6,350 | `5265f22c263958631f72dfac0ba7972fc930f5992f3c7ba44a5756503de25502` |

## Code

The desk’s tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/hpt_score.py is the scoring step of that script and nothing else: hpt_tick.py lines 121 to 124 and 128, the grp function and the comparison block. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/hpt_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.

## Note

The outcome needs the desk’s own live gate to have passed on the run. That gate cannot be replayed, so the kit reads its result from summary_hpt.json, the summary that run wrote.
