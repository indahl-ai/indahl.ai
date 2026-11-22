# PROMETHEUS reproduce kit

Heuremen LLC · https://indahl.ai/prometheus · https://indahl.ai/reproduce

This kit recomputes the PROMETHEUS headline number and its outcome label with the desk’s own code, from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later with none (standard library) (PyPI). It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `75765f774094ce3738a5bbbf8bf3da76344397a2caf3b9d277b437b3944f8961`.

## What it reproduces

The headline as the live feed https://indahl.ai/prometheus/live.json served it at the feed stamp 2026-11-22T10:13:30Z, read by us at 2026-11-22T15:55:45Z. The feed bytes had sha256 `5112e14663fc53334d2562c4cd80d766e3390be07186a35a52f44009eeb382d4`.

- number: cannot tell
- value: "cannot tell"
- outcome: CANNOT_TELL

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

Not included. Its inputs are the NIFC monthly outlook archive ZIPs, about 270 MB of maps and PDFs, more than a public kit carries. Every source is public and listed below, and each file is named in MANIFEST.json with its sha256, so this kit carries no copy of the source data. MANIFEST.json lists each input file the desk’s scoring read, with its size, its sha256 and the time it was last written. Those exact files are kept and this kit is rerun on them before every release.

The input files are what the desk kept from its reads of the sources, with the time of each read where the desk records it. To check them, read the sources below again and compare. With a copy of the input files, `python3 run.py --check --inputs DIR` reruns the kit on them. A file whose sha256 differs from MANIFEST.json is named and the run stops. Sources change, so a later read can differ from ours.

- NIFC Significant Wildland Fire Potential Outlook monthly archive, one ZIP per issue, linked from https://www.nifc.gov/nicc/predictive-services/outlooks (data/raw/outlooks/YYYY-MM_CODE.zip, listed with sha256 in data/outlook_manifest.json).

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/prometheus_live.json | 36,108 | `5112e14663fc53334d2562c4cd80d766e3390be07186a35a52f44009eeb382d4` |
| data/outlook_manifest.json | 28,476 | `919aefe33c66f98ce22d7277b372e3a34c0254d58b69d0e34ae8bc14db6c7299` |
| data/raw/outlooks/2023-01_JFMA.zip | 2,059,381 | `eb1aea48023e5c5cb36194bd8644b973c203c3c1a52448bf0bdd1c8e959b39e7` |
| data/raw/outlooks/2023-02_FMAM.zip | 2,117,263 | `2f128f5a625e47bb9b77c62334f500bbc89c76b6afd4bcd8cc54d2ec5af9eca5` |
| data/raw/outlooks/2023-03_MAMJ.zip | 2,120,680 | `273b00ad1b5dd68697dd47673ff02eaaf7956b6056e591ebe679ce921ca76004` |
| data/raw/outlooks/2023-04_AMJJ.zip | 2,461,648 | `30bcc8f7ce185905af9728d28d9b9e0ea3eecde9b5e26a37204004c9cbcf9bcb` |
| data/raw/outlooks/2023-05_MJJA.zip | 2,177,854 | `a31919f480232291c6d7c177bcebfa6e7b30d0b2aeb132277431677d534dbd10` |
| data/raw/outlooks/2023-06_JJAS.zip | 2,278,754 | `da9c79cd412f94df8c3db53a29ce4f1b8f5a8e6474291501d48fe537cb50e77a` |
| data/raw/outlooks/2023-07_JASO.zip | 2,274,664 | `b2e57136706bff0ca76daf721240eae56cbf5debf909652cae3dcfb2d65900e9` |
| data/raw/outlooks/2023-08_ASON.zip | 2,438,227 | `7d5111cffcfffefcf322df9a0e39fcde67a6196394763ac952494df6f829db27` |
| data/raw/outlooks/2023-09_SOND.zip | 2,410,676 | `eae4859f99e8cc360a478f89292ce7b4c2134f9c0af74bb9ad25a3a3b05c77cb` |
| data/raw/outlooks/2023-10_ONDJ.zip | 2,607,597 | `f9d9135f0ac61db73f53166fbd54d4d5029f66d0ea93307e2957aeb8835545e1` |
| data/raw/outlooks/2023-11_NDJF.zip | 2,164,613 | `061572aaa1b3fc41fadf927439b500b3b36ac1cfbf9b90c5af1542131dc7dd40` |
| data/raw/outlooks/2023-12_DJFM.zip | 2,384,478 | `9e9c492e000b82934e177201650718cacaec2e685d86e3f5529ed0edba870e94` |
| data/raw/outlooks/2024-01_JFMA.zip | 2,391,740 | `ccbb8dde3d38681bec27386bd4a903d879faeb572923348afd07cfba9af47fd5` |
| data/raw/outlooks/2024-02_FMAM.zip | 2,296,256 | `0a4014c55b4db42634cc05bf8f7dd4b33441218e2dc403449627ab940a421fb1` |
| data/raw/outlooks/2024-03_MAMJ.zip | 5,063,094 | `59aaddb7d3fae4ba6463cdfac75c0b99d07487e3334fde3fec900b9320da905b` |
| data/raw/outlooks/2024-04_AMJJ.zip | 4,916,005 | `00af1ffa5fa3a7fd818988a8bc081b17960e93a9d4499dd28c11bb94d76f667d` |
| data/raw/outlooks/2024-05_MJJA.zip | 5,681,367 | `52ffa567cea8bbc6e86c647a718c0e24d529be10cd0ed037818c17c45cddf0f3` |
| data/raw/outlooks/2024-06_JJAS.zip | 6,254,175 | `f925e1114f38aa8f3dcc3d3c2f6e814299173e65ce55a4bafb772010060fc56a` |
| data/raw/outlooks/2024-07_JASO.zip | 6,315,715 | `841a467fa7f600d2258611e272cbe4711a769079e869ef87bca737d022bcf454` |
| data/raw/outlooks/2024-08_ASON.zip | 6,277,033 | `4fe0a79719896298d43ab800cf121c3273d2bcd83c7d45b5fd9d85fd8187d6fe` |
| data/raw/outlooks/2024-09_SOND.zip | 6,461,678 | `6c13c29cef7f3504b748aa5508e35adc168b18c06d86ebe5aee7fc0ca2b3f9eb` |
| data/raw/outlooks/2024-10_ONDJ.zip | 6,182,881 | `9c6ba8c6fbfd91d9ead4aa59220620afb1bc85ebe9e3734225323123d4ca77b8` |
| data/raw/outlooks/2024-11_NDJF.zip | 5,961,768 | `72abc1189f91970a2fca37a2edfdda5570287ab596b6b6ff5a82a302762df02d` |
| data/raw/outlooks/2024-12_DJFM.zip | 6,152,954 | `6a1b2276574f47937934a7d888b1dafff7942a6202a4c5d997023be658c2ad93` |
| data/raw/outlooks/2025-01_JFMA.zip | 6,042,792 | `96b84f1145b089d69f02231a9fb4982b4b195e10a78e961ec592004cfb12b689` |
| data/raw/outlooks/2025-02_FMAM.zip | 6,178,232 | `8da9403df123ce7ced07e7cc97f6cbd2e477c3e34fb1f1b97facb947f081bf9d` |
| data/raw/outlooks/2025-03_MAMJ.zip | 6,216,568 | `5cf1ed9f7730dca167b82b2cbc6c3ad7f0a7ea1c566fef967aa6614cd3e292f6` |
| data/raw/outlooks/2025-04_AMJJ.zip | 6,144,278 | `457a05de272f34bb2ccd48e5866dbd53dac12599969ef05cf76ee849f22d7c61` |
| data/raw/outlooks/2025-05_MJJA.zip | 6,849,414 | `9b08f04728af98c7e0231308ca26f9545cf71349fa7767121a70c3753cddeaaa` |
| data/raw/outlooks/2025-06_JJAS.zip | 6,740,741 | `c6525733c5365311d6977ea27bb24dffe1999938b3c727783ba84da783c9c412` |
| data/raw/outlooks/2025-07_JASO.zip | 6,410,558 | `6d2e136c9fa6b678fd0b9139ceaa62ab430c3ed3fc5d24bccb002ad52f4f09ac` |
| data/raw/outlooks/2025-08_ASON.zip | 6,487,352 | `33ab57cb1bd74b6f7822fcc055a9fca1beb765f0778b6b1ee4959cd4e6bd22f1` |
| data/raw/outlooks/2025-09_SOND.zip | 6,441,337 | `c77263dcf9b7e8ced562f05e4e41a0070eae10fa6821d26f91003bf7151f1af8` |
| data/raw/outlooks/2025-10_ONDJ.zip | 6,134,525 | `24d9ddf0e0a32c49502108b24f21754fcb9b8c33d07bbec38702330fd24b7111` |
| data/raw/outlooks/2025-11_NDJF.zip | 6,071,068 | `e03da0031743a5dd6c556e3272601dc000d12572fc0410bd5bf01c889a601539` |
| data/raw/outlooks/2025-12_DJFM.zip | 6,111,213 | `ddaf56a63f96e89f3c0cf1e00f863a17155e810b1271c1142ee50c23fecf4624` |
| data/raw/outlooks/2026-01_JFMA.zip | 6,373,751 | `bab0b229fc4a450b877b2777f3a1a2b8cb240f3762ba5012b8fc4df70a26c7a3` |
| data/raw/outlooks/2026-02_FMAM.zip | 6,071,816 | `1b1fdefc8b5ce62341e32082b5677d90efdf67288ec2ab8594f2073013184ef4` |
| data/raw/outlooks/2026-03_MAMJ.zip | 6,137,085 | `a7f7b9d99cccfbb0909699a03f2082cb1a2a3db78072d6fe037ac7f0bcbb674f` |
| data/raw/outlooks/2026-04_AMJJ.zip | 6,337,435 | `8faec37be6dee34319b0ff7575a16132a0fca7d537b4c39419114bba1779a654` |
| data/raw/outlooks/2026-05_MJJA.zip | 6,331,635 | `bd1804296d0f87b1d3d0839ad56999a84e68afb50a273463efb242f52364c9b0` |
| data/raw/outlooks/2026-06_JJAS.zip | 6,493,382 | `8e24ba2bd48145e1f11fba5ff6ec90c4898d3ed8a31e6f11d6f50ea6bb0b9d7f` |
| data/raw/outlooks/2026-07_JASO.zip | 6,602,699 | `006c087c33d849fc4da08590185582a1ceb8e112700c4155645a8350f4fb829a` |
| data/raw/outlooks/2026-08_ASON.zip | 6,682,044 | `87c0ace26336ff95943d09701fa08bc5cdb51d7e67a3cc653a1cd0e6a8858ef1` |
| data/raw/outlooks/2026-09_SOND.zip | 6,533,933 | `a8c9996620c3a042797c2df529dec571d98777b508e0e9b7a26d14ea9dedce71` |
| PLAN.md | 8,115 | `22a872afbff435c7a158f6fa8ba886ddde21f20d406e16e981976cba63260ae8` |
| data/plan_seal.json | 300 | `69ebe2223c416a215160b382230534df4e76bc5448512bf5cc9b22100181154b` |

## Code

code/clock_run.py runs the desk’s own scripts in code/, byte for byte, and changes the clock only. It runs prometheus_tick.py with --offline and the clock pinned to the time the published run read (the generated field of data/prometheus_live.json). The same files are in the public repository under code/prometheus/. Scripts that run: code/clock_run.py prometheus_tick.py data/prometheus_live.json --offline.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
