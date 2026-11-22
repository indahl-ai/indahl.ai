# VOIGHT-KAMPFF reproduce kit

Heuremen LLC · https://indahl.ai/voightkampff · https://indahl.ai/reproduce

This kit recomputes the VOIGHT-KAMPFF headline number and its outcome label with the desk’s own code, from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later with none (standard library) (PyPI). It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `7fb742f42ea2e38282e4bce76f5dd947cf1bbeae5443a10d659ac0c1e9e7268b`.

## What it reproduces

The headline as the live feed https://indahl.ai/voightkampff/live.json served it at the feed stamp 2026-11-22T02:10:37Z, read by us at 2026-11-22T15:57:30Z. The feed bytes had sha256 `91e6e4418b47387a1dd1b26e35530b0db6c11acabc55593c7749c4f72b54f899`.

- number: 5 of 5
- value: 5
- outcome: none, this headline carries no outcome label

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

Not included. The stated side is the text of the detector makers' own pages, which this house does not pass on. The test files are public under the MIT license and are named with their sha256 and source, so this kit carries no copy of the source data. MANIFEST.json lists each input file the desk’s scoring read, with its size, its sha256 and the time it was last written. Those exact files are kept and this kit is rerun on them before every release.

The input files are what the desk kept from its reads of the sources, with the time of each read where the desk records it. To check them, read the sources below again and compare. With a copy of the input files, `python3 run.py --check --inputs DIR` reruns the kit on them. A file whose sha256 differs from MANIFEST.json is named and the run stops. Sources change, so a later read can differ from ours.

- The makers' pages named in PLAN.md section 1, each fetched by vk_fetch.py stated, with the Internet Archive capture list for the same address (data/raw/stated/<maker>/).
- Liang and others 2023, https://github.com/Weixin-Liang/ChatGPT-Detector-Bias, Data_and_Results/Human_Data (MIT badge).
- Jabarian and Imas 2025, https://github.com/brianjabarian/DetectionAI, all_json/different_threshold_json_files/merged_corpus_withDetectors_defaultProb.json (MIT).
- RAID, https://huggingface.co/datasets/liamdugan/raid (README) and https://github.com/liamdugan/raid leaderboard/submissions/*/metadata.json (MIT).

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/raw/stated/copyleaks/live.html.meta.json | 147 | `ede00f6b4a2fb61f032dc27629e0680c48e3c28df291a5d4cb5271f56a565e5a` |
| data/raw/stated/gptzero/live.html.meta.json | 390 | `bb8f50a55740565a7e78634c153d18fe7566f907d2b9889d557e70d9a8e6ec26` |
| data/raw/stated/originality/live.html.meta.json | 436 | `189235ad17815f74f4460190739d778c8e0d830d3b2b3ebd8e56a1566782e61c` |
| data/raw/stated/pangram/live.html.meta.json | 450 | `bc2b9db15b8be3ddd49b5183b65ffc308c20fd7b922bb563306df1acf61a7ec7` |
| data/raw/stated/turnitin/live.html.meta.json | 155 | `0dcbb9493ba0c87a65462b676c8d3665e077094ccf2712673d77e3a77de07eeb` |
| data/raw/stated/winston/live.html.meta.json | 414 | `05b35be26ef24693c4c8d537e9e690b04b556847efdfb3ef00212b48a1fa1816` |
| data/raw/stated/gptzero/live.html.text.txt | 12,521 | `d27279dd00538b044bab308849ff42f235698baa7cc61c2c05178acde5b28dad` |
| data/raw/stated/originality/live.html.text.txt | 30,202 | `ffa0d5a810b04bf0af6041e2e21bf354d711db82203a667faaa6ca6c79e2a015` |
| data/raw/stated/pangram/live.html.text.txt | 16,983 | `36ff1451914bab23b19321192dfd2fcb96869e964699202320cd7bcb37e69ec5` |
| data/raw/stated/winston/live.html.text.txt | 13,224 | `bffb07dcc725feb2a69f54b9f9a68491c6c33fcb4d5c275db1305c9f0ae79b78` |
| data/raw/stated/copyleaks/cdx.json | 5,049 | `ab2d4df2704742aca5d0a5e20b2349b1b54d1c6e885db04ca4140ec6299a36ed` |
| data/raw/stated/gptzero/cdx.json | 7,028 | `85b5b71ffa6fdde73c04c580b2801bece267b56b257c1a05bad157a8028dd440` |
| data/raw/stated/originality/cdx.json | 11,181 | `097cca79dd0567b9c38a496619c1f5d12f048aa62094cb4fa52fce35ed0a27c0` |
| data/raw/stated/pangram/cdx.json | 4,354 | `f50263abb157e5f3adfba6e73a4ae5926b8150022edd2c86434dd9f04a4e8394` |
| data/raw/stated/turnitin/cdx.json | 186 | `c589ee015a1dd6efae61bd040313910a9f9816a996511ee0f692e1ad4d19d801` |
| data/raw/stated/winston/cdx.json | 3,409 | `206473451aba7ba874e754cbd858621a5396182dd27173f167eb983a5b494633` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CS224N_real_145/GPTZero.json | 205,936 | `87463f526cda0ef610e7073f23f4ac3990c695d1f0f92bd10536a94fccd35ce3` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CS224N_real_145/GPTZero.json.meta.json | 586 | `457c77935d61d21253270143ea7ab232851758d4d98d1899409f635552c43c5d` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CS224N_real_145/OriginalityAI.json | 687,743 | `a294a02729eec5f0932e51b3a97bfebbb657f0217980789d68d2ed8ee0dd31d8` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CS224N_real_145/OriginalityAI.json.meta.json | 604 | `e7175c3ec3bac7ce04e0e5a6038471f95555b68dd2c662de3de52a68470280a8` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CS224N_real_145/data.json | 178,308 | `fa62fd0355b7121283feb3ee4468bd0db23ba7847806a04d4a754f77b723a31d` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CS224N_real_145/data.json.meta.json | 577 | `7d0f4d4833c6041cd9221c8986c8596c9bdf04f88f509d666a6124fd504555b1` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CS224N_real_145/name.json | 66 | `f3a57ee64aaf918c53f6315f3dc0238f2105bedf49c1b4b9e9cec04e1f3022a0` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CS224N_real_145/name.json.meta.json | 573 | `fceb82f23acbfd9b1ac16c5ccce9be2a51d9ecd1f212114d6226da19dd8a4588` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CollegeEssay_real_70/GPTZero.json | 267,382 | `9dbcc99ee00ba0bc10643f8b875bf130651c45043071db5d2510244257594e75` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CollegeEssay_real_70/GPTZero.json.meta.json | 601 | `900c54dc15be50464f46e2006f40fe468211f3c1c83039e2c80eca041118117d` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CollegeEssay_real_70/OriginalityAI.json | 863,000 | `080ab9faf3fd876be2a94660e100bad03a3bc091666a8c05f3c05c8374b0ada8` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CollegeEssay_real_70/OriginalityAI.json.meta.json | 619 | `e07a2914fe38af52cbb8d5f09201aa041a69728102a55c46131cad62643024fc` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CollegeEssay_real_70/data.json | 250,505 | `37534035e5ad8bbb7a362433644b38c6b8d45ad9c444836cc89a7013eb0d9917` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CollegeEssay_real_70/data.json.meta.json | 592 | `948e9b9a0cc46dc09412e3d76547503b89c28616fef8937299f7495c2c1fc2ef` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CollegeEssay_real_70/name.json | 74 | `69b4797da887ee2dfea23c0e954aacd472ca6d76571a3981c2fc712b4da58ae7` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/CollegeEssay_real_70/name.json.meta.json | 588 | `6c8c00d1c67a4545ee83791517172a6b48206d8e148d067e262549067f96203e` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/HewlettStudentEssay_real_88/GPTZero.json | 208,128 | `f08aa8d89a0d1fd3cf84ea5080beca6d4d18f33907c6032ac9f663cae54f20bb` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/HewlettStudentEssay_real_88/GPTZero.json.meta.json | 622 | `ead09fd5f3ba0aed775355ecf409bde56e650e3fc6f4df56017da4ad08c6cc83` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/HewlettStudentEssay_real_88/OriginalityAI.json | 651,790 | `924b814cfa61a911cbc2fedb93191a90f308e4e2e16a5bc7a6649a07d3972403` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/HewlettStudentEssay_real_88/OriginalityAI.json.meta.json | 640 | `10371eb13190b699eba366a2ef84dc48e4e435d09769037cba04ce9e4c9c8046` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/HewlettStudentEssay_real_88/data.json | 187,850 | `6145e4e8bf36b780624626b31a783d7ca97696e1e14ae6d13c083b79da2f042d` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/HewlettStudentEssay_real_88/data.json.meta.json | 613 | `94a51c23be56e140e8c83449bd4c581d4633baef71b3fcee0237c8f2b36f7c82` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/HewlettStudentEssay_real_88/name.json | 73 | `283d08094b0573d9563b5e7918c207c8ef329b024ded208a87be8d5c77dccb5a` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/HewlettStudentEssay_real_88/name.json.meta.json | 609 | `3945791907592301a38f9923a045eebe1d753188025385ca8982c5fb6cc01511` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/TOEFL_real_91/GPTZero.json | 76,327 | `0f3d39d382b3d7146db19535b269dc3e7f4c5ce0a6ca704972d71e585d8f3f37` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/TOEFL_real_91/GPTZero.json.meta.json | 579 | `c38f8f4d839c6d1e35de26962421cca60b69b4300ea62e9efc17c1f49f159d6f` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/TOEFL_real_91/OriginalityAI.json | 316,046 | `3df006dc648bce0b0cab94bb9d7110872e5fc6f8f93baf554992261922f50395` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/TOEFL_real_91/OriginalityAI.json.meta.json | 598 | `da8f41da3d88ad3d110fb062459eb28b08e5f937d0c83a690aead4220c5a7ef3` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/TOEFL_real_91/data.json | 56,146 | `d5e2bf0bd4831262d60aa936b2ac8e532bd3859067411288b6c22ed16867666b` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/TOEFL_real_91/data.json.meta.json | 570 | `159948273e92488b1293dd4d2d1ffc577a311e05e7a3779d6d7638a4389ef9fc` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/TOEFL_real_91/name.json | 65 | `e94ab2e2e8a9d5fefc4baac388e1576a9e5a81a5bf96d8f3ac680e30a556c4e8` |
| data/raw/tests/liang2023/Data_and_Results/Human_Data/TOEFL_real_91/name.json.meta.json | 567 | `b1036248a4ac71a9f0c2a0181ce262210dbfeb2e1573fb5be4f9c23bf42b57f9` |
| data/raw/tests/jabarian2025/all_json/different_threshold_json_files/merged_corpus_withDetectors_defaultProb.json | 16,645,240 | `660941bd29da0087bb30a3ece10315739f5939843096c7e20afc8bfffc319d2c` |
| data/raw/tests/raid/leaderboard/submissions/gptzero/metadata.json | 227 | `d70a22ffbf74bab908920828b49744adefc2ea86071150d9620dd8c8695eb9fe` |
| data/raw/tests/raid/leaderboard/submissions/winston-ai/metadata.json | 209 | `49695a9ddd43da31718d36f081737107bd3db7b8e4fbe23be7d1cd2eeedeb1ca` |
| data/raw/tests/raid/hf_README.md | 3,664 | `54df4f236108b360e8ad4b4e527b3764c4068fb77c95cbce1e9bac78af64d35c` |
| sources.json | 9,050 | `03d55cd43a7725e0756bc0ea98fc1b7d6371d34cf95b337e485d28986484d0da` |
| PLAN.md | 10,213 | `f05422739d134c2ae59f4ad79c522c0ca92e163119b76e3b9f0ddced062d8d87` |
| data/plan_seal.json | 300 | `a319c5e14ece08dc7890098f5b117c16a1d414858dd8b16ca3a2e9114f8a2347` |
| data/plan_answers.json | 1,800 | `4fbcb625ed8204a7733e9921f11dd8d0e9e0f636da68fad162164cdb83ef5bf9` |

## Code

The desk’s own scripts, byte for byte, under code/. They run in this order: code/vk_tick.py. The same files are in the public repository under code/voightkampff/.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
