# ARGUS reproduce kit

Heuremen LLC · https://indahl.ai/argus · https://indahl.ai/reproduce

This kit recomputes the ARGUS headline number and its outcome label with the desk’s own code, from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later with numpy and pypdf (PyPI). It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `a3f1012ded4bad73f008cca85340107e4bae889deadf585c0cb3f2fab3ffe442`.

## What it reproduces

The headline as the live feed https://indahl.ai/argus/live.json served it at the feed stamp 2026-11-22T10:13:31Z, read by us at 2026-11-22T15:53:18Z. The feed bytes had sha256 `9ee90a8fdbb20888ab90986716159751d6021865e0ae9eeedc91119a34ed142c`.

- number: 4 of 6
- value: 4
- outcome: none, this headline carries no outcome label

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

Not included. Its inputs are the Darwin’s Ark archive (DarwinsArk.zip, 45 MB, and about 115 MB of files read from it), more than a public kit carries. Every source is public, the archive is CC0, and each file is named with its sha256, so this kit carries no copy of the source data. MANIFEST.json lists each input file the desk’s scoring read, with its size, its sha256 and the time it was last written. Those exact files are kept and this kit is rerun on them before every release.

The input files are what the desk kept from its reads of the sources, with the time of each read where the desk records it. To check them, read the sources below again and compare. With a copy of the input files, `python3 run.py --check --inputs DIR` reruns the kit on them. A file whose sha256 differs from MANIFEST.json is named and the run stops. Sources change, so a later read can differ from ours.

- Darwin’s Ark release, Zenodo record 6522639, https://zenodo.org/records/6522639 (data/raw/zenodo: record_6522639.json, README.md, DarwinsArk.zip, CC0, checked against the md5 the record gives), with the six files argus_tick.py reads from the zip in data/raw/darwinsark.
- The American Kennel Club breed standard PDFs named in mapping.json, https://images.akc.org/pdf/breeds/standards/GoldenRetriever.pdf and https://images.akc.org/pdf/breeds/standards/LabradorRetriever.pdf (data/raw/standards).

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/argus_live.json | 28,119 | `9ee90a8fdbb20888ab90986716159751d6021865e0ae9eeedc91119a34ed142c` |
| data/raw/darwinsark/DarwinsArk_20191115_answers.csv | 104,537,423 | `af26b5858dd8e5d6527b3d7ff12fca32ddd417905f0bc938aa7deaa157abb72f` |
| data/raw/darwinsark/DarwinsArk_20191115_breedcalls.csv | 793,747 | `57ef4fba71e7da49f0fe4357f6c47c0eba5a1c5143cc773036a9662e95723fb2` |
| data/raw/darwinsark/DarwinsArk_20191115_dogs.csv | 4,139,906 | `5902b3f29eaf8e70818f98b6f9e7405172f412096657a5313dfe3cb6b2aa13bd` |
| data/raw/darwinsark/DarwinsArk_20191115_factor_scores.csv | 5,088,455 | `7e25602a6604ae36b434b26af37298970dd9d1a9ee5805a1bd3a4aa23beb91e1` |
| data/raw/darwinsark/DarwinsArk_20191115_factors.csv | 26,353 | `218cd3205a8cc4dcebc4749945e6c2d0ca83bf99367c6fcc8af4a41955408090` |
| data/raw/darwinsark/DarwinsArk_20191115_questions.csv | 30,648 | `a9392e8120a1955d9dcdce838c1558d26a21c6ea6bebd83cadfd1b56cb3e1168` |
| data/raw/standards/AmericanPitBullTerrier_akc_response.xml | 263 | `abb5ea2c99c769090363c86b5fe90f469a54c54cc6c7ab60b518eba5a8f398f4` |
| data/raw/standards/GoldenRetriever.pdf | 229,296 | `aa0be1bd97c9df51766f4dc586d44597bf5366b6d1cea9ebe8bbc0699451edf6` |
| data/raw/standards/LabradorRetriever.pdf | 189,315 | `cc37e4b63d60e70a5ba80c81a4cd223dfbd4ae9beb7fc290155dec33dcb8cef5` |
| data/raw/zenodo/DarwinsArk.zip | 44,707,720 | `560fc0243b34a0454a967ea01f428bc7cc6355db6bf498161f1511470d90e27f` |
| data/raw/zenodo/README.md | 12,800 | `ad5264e5dcbf4438ca9ecca778780d92d8e1f5e394ce2f38a4f27e7543b9d0b2` |
| data/raw/zenodo/record_6522639.json | 9,271 | `f7a594b0af79f0a29cc492babf9f2e81fb267a4a8aadf5555e146559346e3212` |
| PLAN.md | 8,378 | `e63f757281dd52089289b5c9b7a4c3442e01a1c2db465939307208bdb0d4303a` |
| PLAN_ADDENDUM_referee1.md | 2,813 | `87e10fd54b72e76bc4ea6ff6e7bec7f616d40e475feadb7f70aed0ab779a5dc7` |
| mapping.json | 11,789 | `c78d067fd3cd29ac81a249b34bf68008b7cb609baa2ec2d6fd74d4fd8ac2fcba` |
| dna_claims.json | 1,535 | `b52656d3550155f833e4a935d3d38dc56fee7ad9c735e52586cbe56ff367de7b` |
| data/referee_mapping_read.json | 569 | `d6d66f654803f1a188c7ea916aa8fe15f09d44bb6740856f2ef378d25f0fa7d6` |
| data/plan_seal.json | 1,121 | `d9a25f8e98258a8001c78d82960e3069bb741782b9632a34f3886a5b61cca0c7` |

## Code

code/clock_run.py runs the desk’s own scripts in code/, byte for byte, and changes the clock only. It runs argus_tick.py with --offline and the clock pinned to the time the published run read (the generated field of data/argus_live.json). The same files are in the public repository under code/argus/. Scripts that run: code/clock_run.py argus_tick.py data/argus_live.json --offline.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
