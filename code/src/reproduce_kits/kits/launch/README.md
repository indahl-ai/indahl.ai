# LAUNCH reproduce kit

Heuremen LLC · https://indahl.ai/launch · https://indahl.ai/reproduce

This kit recomputes the LAUNCH headline number and its outcome label with the desk's own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `9b86fccb7e97cdc034297acb756d8ece8d7d2f9d27e607b4c3f513b1a615c2ff`.

## What it reproduces

The headline as the live feed https://indahl.ai/launch/live.json served it at the feed stamp 15 Nov 21:27, read by us at 2026-11-15T21:41:28Z. The feed bytes had sha256 `7f4529c43f06d0304ad600fb4d6c74bf9af96c060a8bc9c33b0b1d3e4c2e5624`.

- number: 15
- value: 15
- outcome: CANNOT_TELL

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

Not included. The Space Devs state no data licence for Launch Library 2, so this kit carries no copy of the source data. MANIFEST.json lists each input file the desk's scoring read, with its size, its sha256 and the time it was last written. Those exact files are kept and this kit is rerun on them before every release.

The input files are what the desk kept from its reads of the sources, with the time of each read where the desk records it. To check them, read the sources below again and compare. With a copy of the input files, `python3 run.py --check --inputs DIR` reruns the kit on them. A file whose sha256 differs from MANIFEST.json is named and the run stops. Sources change, so a later read can differ from ours.

- Launch Library 2, https://ll.thespacedevs.com/2.3.0/launches/upcoming/?limit=100&mode=normal and .../previous/?limit=100&mode=normal, read every 6 ticks. Each row of data/snapshots.jsonl is one launch as read, with the read time in its read field.

## Sources and their terms

As the LAUNCH data pack lists them. Credit each source when using its values.

- Launch Library 2, https://thespacedevs.com/llapi. The Space Devs terms, no data licence stated.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/snapshots.jsonl | 2,996,330 | `af16150b27bfbade8e16ce188766b89451bf84d96aa0190d5062fdc07371313d` |

## Code

The desk's tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/launch_score.py is the scoring step of that script and nothing else: launch_tick.py lines 28 to 58, flown_watched and the cells, without the count still waiting. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/launch_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
