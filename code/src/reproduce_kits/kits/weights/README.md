# WEIGHTS reproduce kit

Heuremen LLC · https://indahl.ai/weights · https://indahl.ai/reproduce

This kit recomputes the WEIGHTS headline number and its outcome label with the desk’s own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `696dd1f22c805d59a3b3ee9aa658614583d85b0c890575e8c24e0f6d1647bab8`.

## What it reproduces

The headline as the live feed https://indahl.ai/weights/live.json served it at the feed stamp 22 Nov 14:38, read by us at 2026-11-22T16:02:30Z. The feed bytes had sha256 `2a0a7861c222af30a3a1be06f2d1bbd723f43208479a1c04da59f3566c92ccfd`.

- number: 28 of 1,115
- value: 0.0251
- interval: 0.0174 to 0.0361
- outcome: CONSISTENT

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

Not included. The Hugging Face API is under its terms of service and not an open licence, so this kit carries no copy of the source data. MANIFEST.json lists each input file the desk’s scoring read, with its size, its sha256 and the time it was last written. Those exact files are kept and this kit is rerun on them before every release.

The input files are what the desk kept from its reads of the sources, with the time of each read where the desk records it. To check them, read the sources below again and compare. With a copy of the input files, `python3 run.py --check --inputs DIR` reruns the kit on them. A file whose sha256 differs from MANIFEST.json is named and the run stops. Sources change, so a later read can differ from ours.

- For each model, https://huggingface.co/api/models/MODEL/tree/main on each pass. data/repos.json holds the sha256 of every weight file Hugging Face reported on each pass, with the pass times, so a reader can compare them with the files as served now.

## Sources and their terms

As the WEIGHTS data pack lists them. Credit each source when using its values.

- Hugging Face Hub API, https://huggingface.co/docs/hub/api. Hugging Face terms of service, https://huggingface.co/terms-of-service.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/repos.json | 2,988,939 | `3b7d77ade1aa6199f536c6e2ec6c19bdfe6bd70196dd19dd02f6f127bc6b34c7` |

## Code

The desk’s tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/weights_score.py is the scoring step of that script and nothing else: weights_tick.py lines 70 to 76 and 84 to 86, the latest pair, the any-pass count and their intervals. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/weights_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
