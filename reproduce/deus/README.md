# DEUS reproduce kit

Heuremen LLC · https://indahl.ai/deus · https://indahl.ai/reproduce

This kit recomputes the DEUS headline number and its outcome label with the desk’s own code, from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later with none (standard library) (PyPI). It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `d26495860af734cb101ece06a25f8eeca7d53487561fbef1715ad2d40c4061d0`.

## What it reproduces

The headline as the live feed https://indahl.ai/deus/live.json served it at the feed stamp 2026-11-22T02:17:38Z, read by us at 2026-11-22T17:10:09Z. The feed bytes had sha256 `23acac122676fb7eceed73bdca95a2f46a1959c33ad0325e0d362a46550fd8db`.

- number: 0 of 40
- value: 0.0
- outcome: none, this headline carries no outcome label

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

Not included. The stated side is the text of the labs' own pages, which are not ours to pass on. Every page is listed in MANIFEST.json with its URL, read time and sha256, and the Epoch AI file is CC BY 4.0 from https://epoch.ai/data/benchmark_data.zip, so this kit carries no copy of the source data. MANIFEST.json lists each input file the desk’s scoring read, with its size, its sha256 and the time it was last written. Those exact files are kept and this kit is rerun on them before every release.

The input files are what the desk kept from its reads of the sources, with the time of each read where the desk records it. To check them, read the sources below again and compare. With a copy of the input files, `python3 run.py --check --inputs DIR` reruns the kit on them. A file whose sha256 differs from MANIFEST.json is named and the run stops. Sources change, so a later read can differ from ours.

- Epoch AI Benchmarking Hub download, https://epoch.ai/data/benchmark_data.zip (CC BY 4.0), linked from https://epoch.ai/benchmarks/use-this-data (raw/epoch/DATE/, with manifest.json).
- The labs' own launch posts and model cards named in stated_sources.json, each saved as text with its URL, read time and sha256 in raw/stated/fetch_log.jsonl.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| summary_deus.json | 52,101 | `c719b86e409e444f760e4a8d67f206641e732cf16c4c0d90ed776a54abd1c4e8` |
| PLAN.md | 14,976 | `b80c1d882dfb98dba239b4a6221e545c4bd5b6ac958ec27413322e93e0354cf0` |
| data/plan_seal.json | 326 | `90c667ac466c27c6df0eb388a60afc94c1df1bfca0aec57cf00a68900fb10672` |
| claims_text.json | 4,801 | `09c0cd8fc8c0aac713532fc733deea96d79059718e55537978690e516c9da00b` |
| claims_image.json | 17,602 | `e22aeefb278a6635d47460716e9bef651bcf3e4695a1ca32fe823ee67073a72e` |
| stated_sources.json | 44,287 | `5fa5363f82cbb4de188bfb20b488ce12a96f986ffe95eb16e97385fa4c562fd3` |
| raw/stated/fetch_log.jsonl | 114,026 | `f6b65e29e1154c45459077dd4d55dc36a0043dfbc2f6ce5127b3854146b744d6` |
| raw/stated/ai-meta-com/meta-muse-spark-1-1.text.txt | 8,253 | `d949f51e2bbd351fb26f69e8af870d732d3e56472348da9e9715c4c8004b2fd6` |
| raw/stated/ai-meta-com/meta-muse-spark.text.txt | 9,041 | `d2668f16ecb7eaea85ee93fba1c7cf1b3e9703329f7bfee20c82ab83fb9804f9` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4-1-flash-1017.text.txt | 3,292 | `af7e701d063b6bf876ceb51c56e92701b4ad0270c9eea7d8d71c3285a50d23ee` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4-1-flash.text.txt | 4,174 | `2f3182db792bc2b9478242bd3028eff9d16b55e8ffe5c82990e406e237edf62a` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4-pro-ga.text.txt | 4,058 | `a13cf0be16d43be2250b932323aabeefabde35ce87fa088f5be82474a6c41dae` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4.text.txt | 4,046 | `c395cbef2731a855528fc3464c6051c8c90d9e9ef9c80d189e707bcb43037534` |
| raw/stated/deepmind-google/google-gemini-3-1-flash-lite.text.txt | 14,449 | `03a84e5ff4cab932ff2d8b1d92807a1c43acf64a3e174070accacc1757d4afad` |
| raw/stated/deepmind-google/google-gemini-3-1-pro.text.txt | 18,417 | `a8027928472efb38818231713ca48858ef5795e51e83bf48ca0fbb8d82c21954` |
| raw/stated/deepmind-google/google-gemini-3-5-flash-lite.text.txt | 14,304 | `7563b956ea01ca33baded05e9527431ea027021b7a953352dac5b5811a77fd8f` |
| raw/stated/deepmind-google/google-gemini-3-5-flash.text.txt | 14,193 | `2694a3ccb948fe86be1f063709da6366b9d49a1c9b1b507a712fe2b6936ef8e9` |
| raw/stated/deepmind-google/google-gemini-3-6-flash.text.txt | 14,915 | `77b1e6e8101e9e6179a18783bce6fd726798a0423f17a3a03b255f5d5e12988e` |
| raw/stated/deepmind-google/google-gemini-3-7-flash.text.txt | 17,284 | `16b787fa79dc2b0c131715d5be9ee87059dac01eac42b1a2a914f52a94c17b6b` |
| raw/stated/deepmind-google/google-gemini-3-8-flash.text.txt | 14,920 | `9040325dffc69bc1312667d1e59fcedf3d95c98f480346edfc7990a2eeba96ce` |
| raw/stated/deepmind-google/google-gemini-3-deep-think.text.txt | 18,879 | `00be7fd96a7ca25ecc55a5599578e0f49d70538526fab201cc45d0d82c3cb1aa` |
| raw/stated/deepmind-google/google-gemini-4-argon.text.txt | 23,642 | `fc505795c8e01846fd4df94969926bfc06f470ba0994c2157370d32bc2d96eda` |
| raw/stated/deepmind-google/google-gemma-4.text.txt | 8,181 | `94ff33f9d25cf4cee41289e5d79e660f1d09864be2534f9fc8af26e472f82659` |
| raw/stated/huggingface-co/alibaba-qwen3-5-0-8b-card.text.txt | 145,707 | `c42ce959c315b36f8b9fd74827740b6ae7162064035a2cccb5bc8a5a6806aece` |
| raw/stated/huggingface-co/alibaba-qwen3-5-122b-a10b-card.text.txt | 142,747 | `bd09542f3cdf4ad2f5825f4e16713fd70c76e48967af14b940415ccc62bdb94b` |
| raw/stated/huggingface-co/alibaba-qwen3-5-27b-card.text.txt | 151,043 | `8b1bcfe7c58fa4b0b80cfc1a19c6fe956d69497e921a3e7994d494d7acc99e2a` |
| raw/stated/huggingface-co/alibaba-qwen3-5-2b-card.text.txt | 147,508 | `9bfe2a46cc674c088160f80b244106f80511fd006f6b2eb6e89f252e20137eb7` |
| raw/stated/huggingface-co/alibaba-qwen3-5-35b-a3b-card.text.txt | 163,476 | `af337ba8854c358a0c88902782a82d962980bfaa87dc75d8fa0a9cd9640cd96c` |
| raw/stated/huggingface-co/alibaba-qwen3-5-397b-a17b-card.text.txt | 222,495 | `380ef333c53b07082964bfa84fce09ae63af136a8ee2bdada903a007c6af96ae` |
| raw/stated/huggingface-co/alibaba-qwen3-5-4b-card.text.txt | 174,756 | `04db07b4e87d51d8c3e8ae64f5f89eddf2886c7bb77250bc4f27000e0879bcfd` |
| raw/stated/huggingface-co/alibaba-qwen3-5-9b-card.text.txt | 221,947 | `7c5184ff826786ebbb16c0dd84a2764d10492067278479c9148c8c0bc4a99c13` |
| raw/stated/huggingface-co/alibaba-qwen3-6-27b-card.text.txt | 245,343 | `84df825913e86a002e4b76c96f1af1c21cb318809b40880f0bea3dcecb1becd4` |
| raw/stated/huggingface-co/alibaba-qwen3-6-35b-a3b-card.text.txt | 254,772 | `1df17e2733730d5487d9e371c2a413bed32be1bf6f04747ca265bc5e89d90aff` |
| raw/stated/huggingface-co/alibaba-qwen3-8-27b-card.text.txt | 430,556 | `adf91c5ecd843d4c14d4d773b5d4091afdbd31b1680545986a47848006e421a7` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-1-flash-1017-card.text.txt | 136,643 | `2b3104d3fadf28c3c14700de7e8e5a6d643d63a481d587dc4deacb1ce5f4b96b` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-1-flash-card.text.txt | 165,791 | `0aee1dd54056377724c621907f9e587b0097abde7b41bf4aab50eeb3e5732487` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-flash-0731-card.text.txt | 50,900 | `2e95e8f504e7cefd7f5df5c4b9dd7bc0d4b4238673c3864733ef954259509075` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-flash-card.text.txt | 68,438 | `0d7efda4920c10f3a806eeb09e757f55fb5f5cc64973fd0ae9f0e72e46272cbc` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-pro-0813-card.text.txt | 47,490 | `67f752ccb0a37a81e118de96f7f3cbc9914cc80352ef06577310b2660e16936c` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-pro-card.text.txt | 126,829 | `03e8a13098533fa2b57db013b0c1f5b00b255a8626c71a98ccbb89cfe9fd40cc` |
| raw/stated/huggingface-co/meta-muse-glimmer-card.text.txt | 307,350 | `26265f79954bf49cc40c3a551a4e17e885fd91a59f87f681c46f042919fee385` |
| raw/stated/openai-com/openai-gpt-5-3-codex.text.txt | 17,766 | `40a099385a6e9f724d7e97dd1eaf8d292a0f62f466fdd0fb9fc0ba1e136cbc02` |
| raw/stated/openai-com/openai-gpt-5-4-mini-and-nano.text.txt | 9,153 | `a0eecc2f998638ca7081803ca7a4e4686a3ff09409a6d0bf658a37c31f7c7c93` |
| raw/stated/openai-com/openai-gpt-5-4.text.txt | 28,695 | `32dd0f984082ef4d97a1ea58442787e69208cba2ef6a14dba99dffed0f55f7a9` |
| raw/stated/openai-com/openai-gpt-5-5-instant.text.txt | 16,486 | `365c251cef52f7579824c54f657e41b8738a6f5fa9b913a20e7c8cb7dbb6b727` |
| raw/stated/openai-com/openai-gpt-5-5.text.txt | 30,594 | `d149ce66f3bfa3706f1229ca0bae8680480c50627c92c7023396a8259f161a9b` |
| raw/stated/openai-com/openai-gpt-5-6.text.txt | 36,111 | `2fe68c34fb2701e0e0aee4097367fe6f4c35fb189443ecb21667084b3a04d60a` |
| raw/stated/openai-com/openai-gpt-6-1-sol.text.txt | 9,438 | `9f499a2ac2688d7268ff8524a0eb8b38f90d1df71711b8fc1ee373e14cb11c61` |
| raw/stated/openai-com/openai-gpt-6-1-terra.text.txt | 6,517 | `38deeb0237d4f7efdebf36be6d0ff0592e67be3996324de63138653ffe641f2d` |
| raw/stated/openai-com/openai-gpt-6-astra.text.txt | 33,270 | `2d719173b948b4da1197e9757b1045a441dd702ce23ec65342189c94a256d221` |
| raw/stated/openai-com/openai-gpt-6-sol-and-luna.text.txt | 14,693 | `37edc12f219444d8d9ec93e781f502f0d38b35189d6a69d8f29b92f244eb8f1f` |
| raw/stated/research-meta-ai/meta-muse-glimmer.text.txt | 9,252 | `86cbf1214c2656a74bf5a2e12b34f1f148cc8fb413d642013a2da797ff7858c6` |
| raw/stated/research-meta-ai/meta-muse-spark-1-2.text.txt | 6,091 | `054e8ea14fdf5905838e294fe9963a25b8ecb6731587102d9d920779d776ca5b` |
| raw/stated/research-meta-ai/meta-muse-spark-1-3.text.txt | 11,112 | `8fc89ececf298d879db14970bbc15eddc99cd24a7cccb7e13732d955b844bdf7` |
| raw/stated/research-meta-ai/meta-muse-spark-open.text.txt | 4,673 | `94ef4d2e3e74d6be634724d3a613ba27ae38479d5ddb978a330ef49a1fc05bad` |
| raw/stated/research-meta-ai/meta-muse-wonder.text.txt | 9,214 | `fe6ee6c0f8576bbf35cdaa32a1c7e64292149fff57b54e0271e445ef106373c3` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-5.text.txt | 19,410 | `3bed2cd77b71bc2231f785ac59ef951e31c995588ace3277356537733e4e43fb` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-6-max-preview.text.txt | 7,535 | `c58c0065345fb3d44f1b3cbc4756e9eaec952dc1c5a79fee663531654e676ebd` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-6-plus.text.txt | 18,699 | `fc4fe59db837ce6c3ba9c025a4f117073b7ac16ac676d312bdc30957056189e1` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-7-max.text.txt | 21,946 | `29eca19bab6b0e8c416e1164782ae782e341e21993a574f237639d859ac8aef7` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-7-plus.text.txt | 22,710 | `392d78112b364740ba3759d0b95b94866011184c5a4b3e93dec38ac868de56b4` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-8-flash.text.txt | 21,078 | `2f070a8ea40a3671ef63f27863e4bdb45a3a078df5b111d284354beb2b1a7b3b` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-8-max.text.txt | 38,141 | `c7f0252476dbb076d2afc1c59550be86748b7660691fcb9fd9e562434c1d4c14` |
| raw/stated/www-anthropic-com/anthropic-claude-fable-5-1.text.txt | 35,792 | `beb7cdaac0362ef03ed66329adfcf65f3ee5ed0b016087d4f696d0886d6ca2e1` |
| raw/stated/www-anthropic-com/anthropic-claude-fable-5.text.txt | 26,400 | `874554ee47a156918e01da024790d5348dc4d54b486dcce300a1d892cd244d16` |
| raw/stated/www-anthropic-com/anthropic-claude-haiku-5-5.text.txt | 11,291 | `d67e14fe589415d0501500fad5ceb9079040b7b796ecf7dfd8b8d1c3f1e501cf` |
| raw/stated/www-anthropic-com/anthropic-claude-mythos-preview.text.txt | 91,379 | `9eb9080dfa423d89c840b503a403ba9a7b96288a660b4b91b20a6c39aed63a75` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-4-6.text.txt | 20,830 | `90a8c3500726bb8c3bf1ff8251139854dcfeb812983e9328e5c5bef7faeee709` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-4-7.text.txt | 20,866 | `e88158e59b57dfef5db287695dc5229307aced0bc6153e2183a9ac33d6bdfebc` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-4-8.text.txt | 10,991 | `7a5b4f4f0c9f12a25d54968e19e0888315c8ecb246c08a609ec6bcc4042ebf3f` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-5-5.text.txt | 39,214 | `27d361761356d4a4e0fdfbdf647f3f1b5d1445cd801a8afaaaa6757436ca0e60` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-5.text.txt | 18,357 | `48502c7ba062ec790088ff4fad57ed3afa37750b8db6488ac26140d388bdbdcd` |
| raw/stated/www-anthropic-com/anthropic-claude-sonnet-4-6.text.txt | 15,026 | `baaa33c8b742be3c8aa90fc02df8c33c41ce625eb25257dfc02a1122039df11e` |
| raw/stated/www-anthropic-com/anthropic-claude-sonnet-5-5.text.txt | 18,885 | `81dadfa17a022344681082288c194810bf1fe0ed41c0d17264277e7b0704b845` |
| raw/stated/www-anthropic-com/anthropic-claude-sonnet-5.text.txt | 14,275 | `b21e44d00942db1d68bc6fe0da063f7ecb7296f897709e4c054adec66773170f` |
| raw/stated/www-anthropic-com/anthropic-system-cards-index.text.txt | 1,695 | `0b44f05aa1f746402cfd153875ccd160c6d86893057994e36167f42781cd47ef` |
| raw/stated/x-ai/xai-grok-4-5.text.txt | 7,429 | `1db08cb32b343cfc8f0a29796917d6ada9b194b06f0125f4d5f37aa0834f684e` |
| raw/stated/x-ai/xai-grok-4-6.text.txt | 5,811 | `7c67850b43b9106ff06e83cbd65253a28756656b8450af10b57af8f5644278cd` |
| raw/stated/x-ai/xai-grok-4-7.text.txt | 4,614 | `f3c5d4aa10e7e0037ba7551edaba00a0992ae5efa7b4693f87e8099af13df82d` |
| raw/stated/x-ai/xai-grok-build-0-1.text.txt | 2,013 | `a089eb045598755ba1f4b9e283ae340b5eba5dcaa59f058ece2b78d68652a4a4` |
| raw/stated/ai-meta-com/meta-muse-spark-1-1.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/ai-meta-com/meta-muse-spark.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4-1-flash-1017.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4-1-flash.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/deepmind-google/google-gemini-3-1-flash-lite.tables.txt | 2,189 | `07c467253ed58b060fa19a1c16ae3d7b91e49690a09305d2f7e0c9912a6a586e` |
| raw/stated/deepmind-google/google-gemini-3-1-pro.tables.txt | 5,339 | `fd4719a058cb6d20c5ca749ef8677388435c8666e01b7f369e77f27da904e232` |
| raw/stated/deepmind-google/google-gemini-3-5-flash-lite.tables.txt | 1,626 | `a2520500b6862baa3534a1b3e42b544149a8e91801414d7ea1d9fb39d2494fd1` |
| raw/stated/deepmind-google/google-gemini-3-5-flash.tables.txt | 2,209 | `a2ac53b8796c99746f736f891476815710c5859a2947a24476f6357ddea1080b` |
| raw/stated/deepmind-google/google-gemini-3-6-flash.tables.txt | 1,940 | `94ae991cc802008309a19fb75ce93df9653b67e69a8419156ab763b4262078e3` |
| raw/stated/deepmind-google/google-gemini-3-7-flash.tables.txt | 5,093 | `3a132926bb459ff65b8e3707e51d3a692a82228645976511a0f1fbd586eba9ba` |
| raw/stated/deepmind-google/google-gemini-3-8-flash.tables.txt | 2,429 | `c8df4971275c819cd693e9f2fc8d9a134b06e01fe8a11d72e65ffc2591458151` |
| raw/stated/deepmind-google/google-gemini-3-deep-think.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/deepmind-google/google-gemini-4-argon.tables.txt | 5,936 | `2ae037d617b486d5cf9c2c571f5e37fa8cc59d6f532276c4cd0f352f2cb94c33` |
| raw/stated/deepmind-google/google-gemma-4.tables.txt | 692 | `a4942af6c167e8b8c93061f33d1c1bfd22635319a3844526f504f31d5cd5bcef` |
| raw/stated/huggingface-co/alibaba-qwen3-5-0-8b-card.tables.txt | 3,324 | `2a40dbc6774df74447bcb974166d69b97747a0178e9595c729ee2791f8edcbf0` |
| raw/stated/huggingface-co/alibaba-qwen3-5-122b-a10b-card.tables.txt | 4,863 | `ab491ab7ae6364b57bdbb471120dd164afd07e71d051bca9402e2d9d04c48590` |
| raw/stated/huggingface-co/alibaba-qwen3-5-27b-card.tables.txt | 4,863 | `ab491ab7ae6364b57bdbb471120dd164afd07e71d051bca9402e2d9d04c48590` |
| raw/stated/huggingface-co/alibaba-qwen3-5-2b-card.tables.txt | 3,327 | `1a939fc6a6cacc65be2d6f5631c8d47ac5da7cff9ba0ff3d0f7d8ec61ac7ff48` |
| raw/stated/huggingface-co/alibaba-qwen3-5-35b-a3b-card.tables.txt | 4,863 | `ab491ab7ae6364b57bdbb471120dd164afd07e71d051bca9402e2d9d04c48590` |
| raw/stated/huggingface-co/alibaba-qwen3-5-397b-a17b-card.tables.txt | 4,881 | `f44faad26220cf4a0f063622d94c49ed353a7baa8437ce62c760efc93d1b5a31` |
| raw/stated/huggingface-co/alibaba-qwen3-5-4b-card.tables.txt | 3,856 | `c7e7a7ab61154d5aa118128958cf977f3b56e1e248839992c3b48e7a495d4797` |
| raw/stated/huggingface-co/alibaba-qwen3-5-9b-card.tables.txt | 3,856 | `c7e7a7ab61154d5aa118128958cf977f3b56e1e248839992c3b48e7a495d4797` |
| raw/stated/huggingface-co/alibaba-qwen3-6-27b-card.tables.txt | 2,755 | `953ecd7b225eed6fe2b8d9516f369e7fe7faf86521d818bda5b9640a0e76d685` |
| raw/stated/huggingface-co/alibaba-qwen3-6-35b-a3b-card.tables.txt | 2,904 | `6b40f4dbf021563177d3a3602e9aa556cdb93786d50332993eeb39d90f206a65` |
| raw/stated/huggingface-co/alibaba-qwen3-8-27b-card.tables.txt | 2,312 | `30069cc6e4923bf86a1a2308ef148f24dbd3a797f52ba753c607994e230e93ad` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-1-flash-1017-card.tables.txt | 909 | `3e88dbb0d1f6afa94591fce2dd9b2902dfaa4df9bb32b20e5046997446e5ddd7` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-1-flash-card.tables.txt | 3,272 | `708f16210f632666e1b3e817817a545cf8c9bf1e36ee58c00374431b5f738b97` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-flash-0731-card.tables.txt | 591 | `5c326d0ae4e25973028986b19e399a4aed6af7031cc9cf23f5025ed981132e97` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-flash-card.tables.txt | 5,485 | `ba691393e546f8cb6372af526a78cba1df4cd5f430a254e24dcd2f41416ab8d9` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-pro-0813-card.tables.txt | 961 | `e743df0abd88020033abacbe27885a871b752e8f3a5e78b5396551d7f10d1e8e` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-pro-card.tables.txt | 5,485 | `ba691393e546f8cb6372af526a78cba1df4cd5f430a254e24dcd2f41416ab8d9` |
| raw/stated/huggingface-co/meta-muse-glimmer-card.tables.txt | 3,823 | `09bd26aaceff47bc2e6fe4be7435c3840fe4f06c65ae41c9d92d09c4fdb002fd` |
| raw/stated/openai-com/openai-gpt-5-3-codex.tables.txt | 390 | `c1f401c33ee0bc17163b0c2b8217d14e8e4af06408ee436ffe6cdf80693be692` |
| raw/stated/openai-com/openai-gpt-5-4-mini-and-nano.tables.txt | 1,756 | `1a891c46822ce26f466e3b9d7e23118b04e35bcc4947a6ff02b02f5e1a3dda59` |
| raw/stated/openai-com/openai-gpt-5-4.tables.txt | 3,472 | `fa14bc3aff22971e93691675ddb265f9753cf57bcd6b5b2a05fac465f1096b02` |
| raw/stated/openai-com/openai-gpt-5-5-instant.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/openai-com/openai-gpt-5-5.tables.txt | 3,913 | `8e02a8304c0a1a5cd1f26bd3ce83442397ebec87253287430cf4ecc36e969e86` |
| raw/stated/openai-com/openai-gpt-5-6.tables.txt | 5,049 | `f177231ceea1927f4055ec81803cddd0fa0c47d50b159a3c63a7dd90e51322cf` |
| raw/stated/openai-com/openai-gpt-6-1-sol.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/openai-com/openai-gpt-6-1-terra.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/openai-com/openai-gpt-6-astra.tables.txt | 3,908 | `06646dd70a4ee36a58d216dfa44507a3c0696b54fba081a6dc58380771ac18da` |
| raw/stated/openai-com/openai-gpt-6-sol-and-luna.tables.txt | 508 | `8f13d9e322679b4461dd047dd4704001b5b837a9d5a90916389946b5343dfdc1` |
| raw/stated/research-meta-ai/meta-muse-glimmer.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/research-meta-ai/meta-muse-spark-1-2.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/research-meta-ai/meta-muse-spark-1-3.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/research-meta-ai/meta-muse-spark-open.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/research-meta-ai/meta-muse-wonder.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-5.tables.txt | 5,912 | `a8e97a28e87400ca0d5435f5369e02b41246841baa71aee7fcb49778a2b4903a` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-6-max-preview.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-6-plus.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-7-max.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-7-plus.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-8-flash.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-8-max.tables.txt | 398 | `c5f0f8c3a9d07fc0ca877bf4d2cac780c04761c9730cb65a328a1fde15fd2569` |
| raw/stated/www-anthropic-com/anthropic-claude-fable-5-1.tables.txt | 1,045 | `4d5075e243805eb1023cb2f6ae82932fbe6ae98ee830cdc3c7c7993dbee4dad2` |
| raw/stated/www-anthropic-com/anthropic-claude-fable-5.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-anthropic-com/anthropic-claude-haiku-5-5.tables.txt | 987 | `73629e99674c3d3e80cc5af0040fa3479ae70e8796affb68a03402652c09eac8` |
| raw/stated/www-anthropic-com/anthropic-claude-mythos-preview.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-4-6.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-4-7.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-4-8.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-5-5.tables.txt | 1,212 | `b6eac7c018579399e0ad700207905268f13163846424b32983a9879301df8e5c` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-5.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-anthropic-com/anthropic-claude-sonnet-4-6.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-anthropic-com/anthropic-claude-sonnet-5-5.tables.txt | 998 | `c974c65a913703288f1e030dca012e5517bf9f1b8505e41586ca4d3d6a39d0c7` |
| raw/stated/www-anthropic-com/anthropic-claude-sonnet-5.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/www-anthropic-com/anthropic-system-cards-index.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/x-ai/xai-grok-4-5.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/x-ai/xai-grok-4-6.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/x-ai/xai-grok-4-7.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/x-ai/xai-grok-build-0-1.tables.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| raw/stated/ai-meta-com/meta-muse-spark-1-1.meta.json | 5,400 | `76cba49edc345442aa7ffe8e6fc439974ff7f91104f76e11f74eb25c28c5ed84` |
| raw/stated/ai-meta-com/meta-muse-spark.meta.json | 6,396 | `0a0308c4834cff9043867b1a2129ef9327b69c443c4c0d901fafe8eb4ceeb911` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4-1-flash-1017.meta.json | 2,556 | `24ad69472c25463badcc1c762ed8f0257279a2dcd84d8e6b5c6544da55cf17f2` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4-1-flash.meta.json | 1,883 | `93a36cb045461355ed439e35e9a29adf62b303f7bc703fecc2c5d36c8af3ead3` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4-pro-ga.meta.json | 622 | `af76ae5b7db83d5e4939772c1cdae8864c533f02a17fece2ea3bb81722f30481` |
| raw/stated/api-docs-deepseek-com/deepseek-deepseek-v4.meta.json | 2,366 | `45eb96270a90342e25c5e1292a36606372e0d0fc19a0c89e30bdfcfb42f60454` |
| raw/stated/deepmind-google/google-gemini-3-1-flash-lite.meta.json | 657 | `ea73e994cca0c20585c6567047c003f587956ed1cb94b9f32dac5dfba0823905` |
| raw/stated/deepmind-google/google-gemini-3-1-pro.meta.json | 615 | `29fb616041a45d35cc9ff09159c9326d2bb2c19d68521d88be228c26118c9986` |
| raw/stated/deepmind-google/google-gemini-3-5-flash-lite.meta.json | 657 | `02b2693907114f667db47d62d8e99516bf7fbada796f8603e0ea6e15dad1fba0` |
| raw/stated/deepmind-google/google-gemini-3-5-flash.meta.json | 627 | `d265c86d799bf91b5533d5253906b34bafbe6a9a06cf3f23557977de925fbd7e` |
| raw/stated/deepmind-google/google-gemini-3-6-flash.meta.json | 627 | `a04b82ca9641963942601d9056a905db5e4a3546c32ae4cc73e9413247580cf1` |
| raw/stated/deepmind-google/google-gemini-3-7-flash.meta.json | 627 | `3288636f9a20cc4175e032f168a8848d741c58c0f908eafa588bae0b877dca3b` |
| raw/stated/deepmind-google/google-gemini-3-8-flash.meta.json | 627 | `6c6a13b53f1b0768d4feef611555f73a7d27942d1c59e79d105d5e7f189b0882` |
| raw/stated/deepmind-google/google-gemini-3-deep-think.meta.json | 726 | `b5101f0e7b460d358fe5f75babd324f56d9bf373ca032d02ea55c7813d75107c` |
| raw/stated/deepmind-google/google-gemini-4-argon.meta.json | 615 | `6259daba37e6923c8d9f51ccb0645cf321164092dfc0570e025a630d2de440e3` |
| raw/stated/deepmind-google/google-gemma-4.meta.json | 560 | `4fbf7229c1ced2cad636dad936264b36363e9f5b38a22825c6864c71c9d57bda` |
| raw/stated/huggingface-co/alibaba-qwen3-5-0-8b-card.meta.json | 1,449 | `3304cdb747e7033e83a22aea093cbdc07cfdd3ef3b29bdae4094a854dfce1ee7` |
| raw/stated/huggingface-co/alibaba-qwen3-5-122b-a10b-card.meta.json | 1,660 | `d3a0c8049fa10a87c71b04326be4e5e165652104dc20cb407fc3958cbd37169c` |
| raw/stated/huggingface-co/alibaba-qwen3-5-27b-card.meta.json | 1,612 | `ab662cc4a753cdf19cd20ea5ba205a96b5b78827f8864eeb567f0b59df687d8a` |
| raw/stated/huggingface-co/alibaba-qwen3-5-2b-card.meta.json | 1,433 | `60d3ca35cfa8a631122213712e9153a1d1ecfebeb1429a404b429e420c43cf64` |
| raw/stated/huggingface-co/alibaba-qwen3-5-35b-a3b-card.meta.json | 1,653 | `68a1de361bf672363927af91d2bdd48e173e77d33b2cc38a4460f4748404914c` |
| raw/stated/huggingface-co/alibaba-qwen3-5-397b-a17b-card.meta.json | 1,649 | `9816a97431e054fd7d6ac9c72809e2fc9548c78d285b2f518bcd22cc67919cfd` |
| raw/stated/huggingface-co/alibaba-qwen3-5-4b-card.meta.json | 1,621 | `4433ebb95381eeb692a88ac43b6f04a175a14c74c2aad040f759e71357d36150` |
| raw/stated/huggingface-co/alibaba-qwen3-5-9b-card.meta.json | 1,603 | `7899088847ac35eba71b3429dfb070cf555f563dc38b5c889fae22a8df02ae52` |
| raw/stated/huggingface-co/alibaba-qwen3-6-27b-card.meta.json | 1,260 | `c09e7abcdbab237e2e230bfb1a1f343af89f00f7528b33a32dfe3fb2ab8a475b` |
| raw/stated/huggingface-co/alibaba-qwen3-6-35b-a3b-card.meta.json | 1,649 | `a836dbd05bdbe381ea014e71b8f70938148c983a3b03464b6a4073cda0147655` |
| raw/stated/huggingface-co/alibaba-qwen3-8-27b-card.meta.json | 1,307 | `6ac901bc2bcd08bf63a5ea3f51cbd0d16ef4aa798ba2165a2904ad5a4aef93fb` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-1-flash-1017-card.meta.json | 1,787 | `870d57dcd60913a7301ac68ac0390a396f7ea66fd19d67fc1b9c6d867f09e474` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-1-flash-card.meta.json | 1,789 | `075715b3f7d212c34ea52cf353cb155e163794db06f5ac1618290433d07454d7` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-flash-0731-card.meta.json | 1,041 | `421172ffa1416b83de44faadf8d72f027e8aecf3b0d27908e37490b45582b36f` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-flash-card.meta.json | 1,702 | `c39fb7cb5f411dfbf131947a24173f5158f15db8804cba4d2d2d8e2cbcd52817` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-pro-0813-card.meta.json | 1,027 | `9fa99afa1448ed09e0244093a41386c038630fbd4e102621de03f452afec929e` |
| raw/stated/huggingface-co/deepseek-deepseek-v4-pro-card.meta.json | 1,690 | `888cb1933ab7e7468f14a2e1da84a03146ef79c92b5714a521a4a9239aac1a13` |
| raw/stated/huggingface-co/meta-muse-glimmer-card.meta.json | 960 | `8a589959a4705f70fc298e7a9c5a2d04c48e005e6b172b229933fba47d10d2c8` |
| raw/stated/openai-com/openai-gpt-5-3-codex.meta.json | 594 | `4e0d1df2ddeb673bddf9e65ecf0603bad0d529c3db8fc0d085a9b7d00cb1e802` |
| raw/stated/openai-com/openai-gpt-5-4-mini-and-nano.meta.json | 641 | `ba95fbf45d8c5c3316be67c719fd0554e737d54ecc8242dfa873803dea6cf506` |
| raw/stated/openai-com/openai-gpt-5-4.meta.json | 1,008 | `40b501b45f1c74b10afd1e003b52c3fa9d12a13b58f0b1c8e00a38b74e82ab85` |
| raw/stated/openai-com/openai-gpt-5-5-instant.meta.json | 1,040 | `1ceb54c95e1e7b171642027e3f0d12da6efd71702d5d5abff86e114cbce18bb7` |
| raw/stated/openai-com/openai-gpt-5-5.meta.json | 1,008 | `b581f25202bb0cfc764b29f4b73128d0736631cdb89bdcf4a30c8076c4be75ce` |
| raw/stated/openai-com/openai-gpt-5-6.meta.json | 985 | `a5a14d506a90911fb827f734f25d8161edfba27780254b82eb27e48faaa45194` |
| raw/stated/openai-com/openai-gpt-6-1-sol.meta.json | 581 | `c10c98b447782fee7ae4f6ed8d692c5489863475dc60552507d78da9fb27a3bf` |
| raw/stated/openai-com/openai-gpt-6-1-terra.meta.json | 593 | `1e5354d7b7c890a1a4b3e500b61ea1d239b894227773fac671a8ce32c55f1e10` |
| raw/stated/openai-com/openai-gpt-6-astra.meta.json | 1,037 | `4f185b3fe2b69ece9f725ae5c29f140d53ea7884a6fb445ee217c8e88ff3ce7c` |
| raw/stated/openai-com/openai-gpt-6-sol-and-luna.meta.json | 1,085 | `539b1ea2c676b88f968d99a50bc2d0859ab8862e58a6e1e49f2a6a1fa29014c7` |
| raw/stated/research-meta-ai/meta-muse-glimmer.meta.json | 2,172 | `17b9fb8fa58784e74dba6a4a4f126761cb4eb05e8f82aecfdb68e29bbc5a5724` |
| raw/stated/research-meta-ai/meta-muse-spark-1-2.meta.json | 3,413 | `9e12028b3dfc3dae0dab9f9a0bef7b38c14d2a19eeaa2549a6120a63040991a6` |
| raw/stated/research-meta-ai/meta-muse-spark-1-3.meta.json | 2,397 | `3a849823ab721b491bc4f58dd691309f321f0701cbd22fe75c9eacd8e527659b` |
| raw/stated/research-meta-ai/meta-muse-spark-open.meta.json | 1,236 | `37b1f35e99fd3927c4f964090d65d818b370aa374ac2f370007c44f980b0281a` |
| raw/stated/research-meta-ai/meta-muse-wonder.meta.json | 1,204 | `e25c09b7a6d60bc8afa73c4cf495da2e6eb97ecdefd51fecdba40d9ceb73c4e3` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-5.meta.json | 2,232 | `6db24f5a6d2ce8cdbfb78690a2e3cbab491c4e3e69fa3576d3a96be0ab8a8811` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-6-max-preview.meta.json | 2,359 | `dfdae5e40268665805d0e31ba53ae57ac77ca79391230afb074a33f7b36153ef` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-6-plus.meta.json | 2,271 | `af65ff4b830b3627d6a6b3c27e285b5c1813fd0e2cc158a4b02bade751e74654` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-7-max.meta.json | 2,575 | `5fe3b8c78160d219a70e1ed3d1bdd4257f732d11def5068906f1bbea742cfb73` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-7-plus.meta.json | 2,953 | `07903edb7b16960b59cef17629b5e0846b02646b77e9d43af4352a739ba0e723` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-8-flash.meta.json | 3,357 | `6961f0712cd0783669034e09d5a88f65d9d2d17d7bd6d0d99234d0e964a0827a` |
| raw/stated/www-alibabacloud-com/alibaba-qwen3-8-max.meta.json | 2,954 | `2a8b335054f1aeb090dd75354818d314c51e02b386f0c43d342355b5af2deb28` |
| raw/stated/www-anthropic-com/anthropic-claude-fable-5-1.meta.json | 636 | `3b8583bf381a6299c29c47ee9e1434d9fc19bc4e9a233c88222154a5eee19cb0` |
| raw/stated/www-anthropic-com/anthropic-claude-fable-5.meta.json | 1,058 | `cc247fe6acc060bab9563a2a7675c72dbfecffd4de80471e9c2da2d66bb75d0e` |
| raw/stated/www-anthropic-com/anthropic-claude-haiku-5-5.meta.json | 614 | `b41f93474d5363eda1cecc511647782cf5cc992edd72a4f3ebd81172c65c0cfa` |
| raw/stated/www-anthropic-com/anthropic-claude-mythos-preview.meta.json | 1,002 | `cd371f9d1cdfe342b4c6e84757adbe22a8823f75683adbf95af0722ca4f2cd4b` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-4-6.meta.json | 2,678 | `a3677569869124a7907f0c2553822b8dbff669b9071768faf08335e58f89edc5` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-4-7.meta.json | 4,091 | `da10fdb60f986726658960d43ccc44c6cfd0cdedd702dba210043009f0e55608` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-4-8.meta.json | 1,313 | `29f1fcc4ef77332c8bce66fd931a1803cfb3ecabcbd0d4cb15e8465c72e41bbb` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-5-5.meta.json | 608 | `e41ae623835d1beb5429f8e91e1d78b2103aeb81f3d213d700474a5c8f3af19a` |
| raw/stated/www-anthropic-com/anthropic-claude-opus-5.meta.json | 4,754 | `6a9cc463d23b4707ad802623e87a51f5e6231d19bc4e2a43118cf84487920325` |
| raw/stated/www-anthropic-com/anthropic-claude-sonnet-4-6.meta.json | 1,499 | `21719c39fb407b72c3ec29e426c94090bc218c7e89aca9588d4a283e707a3f1d` |
| raw/stated/www-anthropic-com/anthropic-claude-sonnet-5-5.meta.json | 620 | `f84dae6cdaee0d7695ba2e75fd638581dc0199831a0ffc0155c9ff561ce66a8d` |
| raw/stated/www-anthropic-com/anthropic-claude-sonnet-5.meta.json | 1,691 | `50a47dafc2799d02cb5efca38c9d88da3310e22fbd98ca5eae5774d2a4f096c9` |
| raw/stated/www-anthropic-com/anthropic-system-cards-index.meta.json | 607 | `1389c8fb9bb84ccffc07256bc20beb256d89a2af4743cfdf39f6611a48912ef7` |
| raw/stated/x-ai/xai-grok-4-5.meta.json | 499 | `bdefd08c01fcb249c24b51710be5605e0d81bbd9c6254dc5aefb5fd4a211a977` |
| raw/stated/x-ai/xai-grok-4-6.meta.json | 499 | `92cd4b6d93542292552fb62334d8853669b0926be4d1803226bef5a64be28752` |
| raw/stated/x-ai/xai-grok-4-7.meta.json | 499 | `d670b1e64eb5dae77e9b2bced1ced2ade4ee06048b065d582b4899f035a677fc` |
| raw/stated/x-ai/xai-grok-build-0-1.meta.json | 535 | `95e3870facf1fcb4ce97f190287e9f3acf00abc9a9f6293692cd13de9507b54d` |
| raw/epoch/20261122/manifest.json | 19,436 | `b160ab7b94658265d336ac7b1e1b8852109e68bc702ccfbbcd5218bfaae44f3f` |
| raw/epoch/20261122/csv/adversarial_nli_external.csv | 7,856 | `d4ff30fc512c5568f8910b22d53218ae6c91ccc01d4efa266f5199886774cebf` |
| raw/epoch/20261122/csv/aider_polyglot_external.csv | 27,739 | `65e7eeea3b35435d5c7bc1ab55fa440b58b8dc0c311c54c140b93fbf01806f92` |
| raw/epoch/20261122/csv/ale_bench_external.csv | 30,357 | `52df9cb362344b26f0d0e1c72876720835bbb7091f2fa674196d71911172cdc1` |
| raw/epoch/20261122/csv/algotune_external.csv | 3,887 | `8e255a1ddc34bf49781f75d235c1d474b8be5c7a10757ce714805c973f95d8c9` |
| raw/epoch/20261122/csv/apex_agents_external.csv | 13,554 | `de7e61c4cdd3541eda9be310e7f79bb78a9f441910214cb947c31c60b8e07a98` |
| raw/epoch/20261122/csv/arc_agi_2_external.csv | 58,663 | `1f870613f7e319c04a73a38d4965b90669d8e686be31927d7e326a5d0d6ac2ee` |
| raw/epoch/20261122/csv/arc_agi_external.csv | 71,504 | `9eb652fbb57ed9d985751e9658f5d954f0aeab433a0e42d4709c7bd6f2f182e0` |
| raw/epoch/20261122/csv/arc_ai2_external.csv | 47,496 | `cd7d28c3bd17b03fd2fcfdb9e220831932a5ab1669096e8b9d115feb043b4eea` |
| raw/epoch/20261122/csv/balrog_external.csv | 19,160 | `c6a775c92abd194973cd01355879b7b3e474913d931fc4bd5dbe82907050eba4` |
| raw/epoch/20261122/csv/bbh_external.csv | 27,620 | `fa536f0eb125ce6574ad3b3ab7e2e2535f2a70eb14581d5c4c6e915b0c4a8c41` |
| raw/epoch/20261122/csv/benchmark_metadata.csv | 6,392 | `f6ee439ef0eb0f68722e2280703912f9f67053f7e71817511ed2080d5ee4607c` |
| raw/epoch/20261122/csv/blueprint_bench_2_external.csv | 7,678 | `4b7a14b2739bb3a61e0b184636ececf3c2c9d3c28b8211ae459dcd03201756ef` |
| raw/epoch/20261122/csv/bool_q_external.csv | 57,081 | `36802c8082e551d93fd5c4ba02d104938ee4ede29963b0406df6e2c67899de9e` |
| raw/epoch/20261122/csv/btf3_external.csv | 3,541 | `4f8b3678c840770d904c0a6284d853a23a44f96318a2eb49d72e56f330a293b5` |
| raw/epoch/20261122/csv/cad_eval_external.csv | 5,518 | `bbdb9610edb3a9dddf3aac4a3fc5b182986519e24fdc04de0605f59938d27496` |
| raw/epoch/20261122/csv/chess_puzzles.csv | 75,833 | `0ce4f79dab0a02ebddf4b2b4bacae195598a0b4ec1f0bcc8c8d416d8e56b6fc0` |
| raw/epoch/20261122/csv/cl_bench_external.csv | 6,892 | `d05a8ad3fad268c407c9c44aa648f74781f375a19f784eecc29724e93f04ba7e` |
| raw/epoch/20261122/csv/cl_bench_life_external.csv | 4,875 | `a89c7e55d87cb0861df86660deefaadfd06f9deef12634213de58f24ab676584` |
| raw/epoch/20261122/csv/common_sense_qa_2_external.csv | 3,537 | `19373551d52c9b68eaa760521573247206c0da3aadacc4bb8e71656c1d680f0a` |
| raw/epoch/20261122/csv/critpt_external.csv | 54,031 | `bbb5ca1deafc46fc0aee6e65622068249f198cac584c803d14f3918f62aa4820` |
| raw/epoch/20261122/csv/cursorbench_external.csv | 8,204 | `0f7bfff887de1fe27dd8e0fdedb438c7109768d9fe1d1b11ae07a6f573e68628` |
| raw/epoch/20261122/csv/cybench_external.csv | 10,969 | `58a64c603ee77d89228ce4aa605188c0bc4055aa3572d2325b37c74bb25a055c` |
| raw/epoch/20261122/csv/deepresearchbench_external.csv | 8,408 | `8a1e4f5d083f76b69aafe63f5519f750c42e3b359459785ce8bab1913f68a535` |
| raw/epoch/20261122/csv/deepswe_external.csv | 20,634 | `1cf010b60a9ab513cee9330ad2315b0f766b2854399cd310e7ccb0e52f60f048` |
| raw/epoch/20261122/csv/dtbench_external.csv | 56,994 | `f35ded7eee36b54afbfc014e79b290aa0a1903c6a67a64569e183789e3232422` |
| raw/epoch/20261122/csv/ebr_bench.csv | 7,883 | `eafc02264dc28a525d62ce42563bb9d2cd1c27e8925945147cdb7946888e05f6` |
| raw/epoch/20261122/csv/eci_scores.csv | 31,805 | `98c83f75bec8174c9b5753ce8d31ff8bb0ced0423a8418cca376dadb43030955` |
| raw/epoch/20261122/csv/edi_scores.csv | 4,001 | `6b7fd185c9a70bb25315ca05e489e229a5e0ca9165e9b22cb424a9c6884e9a05` |
| raw/epoch/20261122/csv/enigma_eval_external.csv | 15,403 | `4dd784ed5fc2349b1070e63cf2080e4f0f496efcfd388e00135780cfb6aaef27` |
| raw/epoch/20261122/csv/exploitbench_external.csv | 3,123 | `f9c9556febdd8975d997636da196fb94b7558f462f7ffdf8470840539353abd9` |
| raw/epoch/20261122/csv/fictionlivebench_external.csv | 26,068 | `89dbd70094a544ed83c5e823427a14cf56193e558ffe08743a3d79324030c693` |
| raw/epoch/20261122/csv/forecastbench_external.csv | 30,295 | `a0834884762b4226c356fde0408f5795fe311e036985e8fcec2f07c819896223` |
| raw/epoch/20261122/csv/frontiercode_external.csv | 10,829 | `72bc2d10ceb47004d9052217e7d6095cc7ceb36e409e2655030c1bd77284996f` |
| raw/epoch/20261122/csv/frontiermath.csv | 36,580 | `f5c92f0f0b9103abb02308fd428c0806e7c21b91e8a14d43edb8af77ce941598` |
| raw/epoch/20261122/csv/frontiermath_erdos.csv | 3,590 | `4b6110d65675cf93b6d168f1a94ed870c94b76af1434e7443066d25748df41be` |
| raw/epoch/20261122/csv/frontiermath_tier_4.csv | 21,777 | `c928e5adccd6e0995d50ede183fb99728d6c5be01951434a3077429ffb5802b2` |
| raw/epoch/20261122/csv/frontiermath_tier_4_v2.csv | 31,638 | `654ec804e0a2b560aefa03aae43711a39288a2395455aa596538924fb0e5a3e1` |
| raw/epoch/20261122/csv/frontiermath_tiers_1_3_v2.csv | 51,687 | `14f8767d6cabd84077372aa41adce78326ab8bb1de6fc63afe5bfacda0867714` |
| raw/epoch/20261122/csv/frontierswe_external.csv | 7,366 | `09703bc9fae3f8acc3e2d4e2686f64bcbbb965819b91cc47c090ff7d90c9b32c` |
| raw/epoch/20261122/csv/furniture_assembly.csv | 10,615 | `efa6812c5280b40d6daa3319eec0631581cbb16884df81347d49953513082d8a` |
| raw/epoch/20261122/csv/gbaeval_external.csv | 10,939 | `cfb1094b212f44e7ee44c11f5ff3a945d850020888a22ac6d98a8233ee66fa54` |
| raw/epoch/20261122/csv/gdp_pdf_external.csv | 7,759 | `717263a8bc7cbd9849613a42c41f21611f77a259147a55e4bb9aa8b1be080111` |
| raw/epoch/20261122/csv/gdpval_external.csv | 2,806 | `0421e702386009e334aa5608c970400f1a795d36c19126f715ae8bfcac71de4c` |
| raw/epoch/20261122/csv/geobench_external.csv | 15,298 | `8bdc256807e54b1f870d50666eaae18e65de404ba8835bdbf2a4844d820b8248` |
| raw/epoch/20261122/csv/gpqa_diamond.csv | 175,402 | `1a989df9aecce5da9d5c3ddb7834a3a867c0d2177a0466eae71c5e8ac9420d99` |
| raw/epoch/20261122/csv/gsm8k_external.csv | 61,569 | `beeb35978c1c8fd82788c8406d82a6610d82b8880e1e1221d3160eb640b9304f` |
| raw/epoch/20261122/csv/gso_external.csv | 10,502 | `1d0a25874d72ab1b3e62ab50ea4eed244350c907a87c8eba4f7af9e4dfec4cb7` |
| raw/epoch/20261122/csv/hella_swag_external.csv | 43,332 | `be11d87b05df3741471d2af809f7bb344cdc26f19d1f2d353d0f23440add7ebf` |
| raw/epoch/20261122/csv/hle_external.csv | 14,159 | `c1c5d974c5f3fc5f13b2d18228151591fca40bd0d0964b5b7c6db50b6cfbb372` |
| raw/epoch/20261122/csv/lambada_external.csv | 20,880 | `f178e797a392e20755a1f314aa6bc6c0308f080c76009c1009cbb86dcb7f51f2` |
| raw/epoch/20261122/csv/lech_mazur_writing_external.csv | 27,283 | `591ff9b605f7130924d5fe69c29c849a942262e680b253e31c1043e1552374fd` |
| raw/epoch/20261122/csv/live_bench_external.csv | 21,283 | `c743a6af489cf5c8052a22928924059fc3ab68eac2b2df92da40b687171039dc` |
| raw/epoch/20261122/csv/lmca_external.csv | 41,139 | `88bcd9fe0180e1080a9f4d51e3ffe9a2595e58e0bf13260d2bb14b3e0c1b46d8` |
| raw/epoch/20261122/csv/math_level_5.csv | 49,104 | `a22829149dd32f11bf475e410067a787b7687cf95e09aaac13f5d57f448ff5a2` |
| raw/epoch/20261122/csv/metr_time_horizons_external.csv | 18,705 | `71702e086a4d18927927ec824717aec9728cc00bb19c8265148f4b6881dff15c` |
| raw/epoch/20261122/csv/mindcube_external.csv | 1,124 | `c21d9a3d5ed20d584aa82d1b46402c5763eee9c34999126f5d499a2f22d55fc0` |
| raw/epoch/20261122/csv/mirrorcode.csv | 17,349 | `50793e25b73996df20138dd36e15345c2e891f02837fed758bf1ecca0ff20bf8` |
| raw/epoch/20261122/csv/mmlu_external.csv | 79,823 | `e4752463b5520b42e95cac34cc94b1b6e69cb41d4833c4c677f0350f963802cb` |
| raw/epoch/20261122/csv/model_metadata.csv | 135,230 | `f590339b81743ff78b9cbbbce9048d695e104669ffbf2d2a4fef695e038c3c8b` |
| raw/epoch/20261122/csv/mystery_game_puzzles.csv | 39,738 | `c51c84a1ef40f249c6e8ad3d2b945311aab3e37acaad7eed8c02589e84fefc83` |
| raw/epoch/20261122/csv/open_book_qa_external.csv | 27,871 | `a631f2dd7e6344f8a3c0f7b86cc11f135239f0d252a4419d6265e2318af4dc4f` |
| raw/epoch/20261122/csv/os_world_external.csv | 9,434 | `ba86a536e49028f75def7fb65151767173057c5b8903f4c86c5d11bf35d09657` |
| raw/epoch/20261122/csv/osworld_2_external.csv | 2,870 | `c032d6754876e28792bf654ba9cb3a7cf02b2dadd7b2b9fd0c9e476a37d1a115` |
| raw/epoch/20261122/csv/otis_mock_aime_2024_2025.csv | 161,689 | `1a1c3bbbfd33e143848e2b989fcba0a6fb5485b9bc72f814c4246be44766d70b` |
| raw/epoch/20261122/csv/piqa_external.csv | 44,827 | `372c170454897f5221eb1eea69b5f3e1c018ba74506f6a1d670f275698db15c9` |
| raw/epoch/20261122/csv/posttrainbench_external.csv | 4,301 | `295fc209a4227d1016ea15477a6d9700d850a5e21e92b462b02bcf98ab1a92a0` |
| raw/epoch/20261122/csv/processed_data_for_eci.csv | 369,818 | `27a85846e9e60be111e6e1bdb3364b9e26e4bdce0350072d90bff49038a586a5` |
| raw/epoch/20261122/csv/proofbench_external.csv | 29,844 | `5afb8587cfe9dc98f47142a090e60d85dcfac146e4649f8ce865b8d796971ee9` |
| raw/epoch/20261122/csv/rli_external.csv | 3,441 | `240ee7189939369ededaf443ab151ee7fbd4f5a6fd8dd6d0547c2b2913bc11c7` |
| raw/epoch/20261122/csv/scicode_external.csv | 61,675 | `164ef38d1bf8f40537ee990092db8add64bbace1e357af258f986fadc5b224e6` |
| raw/epoch/20261122/csv/science_qa_external.csv | 16,537 | `7829478ee0ebdfb42013ccb84bb91e4c86d3417abfb1a3b6f2975dedb1423862` |
| raw/epoch/20261122/csv/simplebench_external.csv | 30,948 | `591f7ca462a972f37015266b78423927820f332893406dd2eca2c3e9637bd125` |
| raw/epoch/20261122/csv/simpleqa_verified.csv | 46,256 | `cd6bd38badd60b6c02f698da30e7ebec4702492dac904903eb1922015eba0063` |
| raw/epoch/20261122/csv/spatialviz_bench_external.csv | 3,740 | `709ff308ee856feaf8a7842b5f39f67d332d381d87ba5de13f7e9edc934533c3` |
| raw/epoch/20261122/csv/spireclimb.csv | 3,705 | `7a227039dd65eba9eb9da9c9dd01bec2643df97e23c9bb52bee0869045ac67d3` |
| raw/epoch/20261122/csv/spireclimb_sts1_a20_heart.csv | 3,063 | `36fbb91dfd1a76ec32fe230e4bfa177b04017de8dc116b92ae87dcea03624774` |
| raw/epoch/20261122/csv/spireclimb_sts2_a10.csv | 3,243 | `a840c485ca380fc9b2d8830b0dc954268b46e7b99b5ec0bc0750fd094011862d` |
| raw/epoch/20261122/csv/superglue_external.csv | 3,281 | `cc8024909446cbbbcfaa727dea2753a2401616eb9eec560d47bc56519dd89143` |
| raw/epoch/20261122/csv/surface_evolver_bench_external.csv | 8,417 | `cd702ba924ec0a799d39f088a297daa0e6c575b27061b55fcfb3cf3c32de6aef` |
| raw/epoch/20261122/csv/swe_bench_verified.csv | 16,671 | `6480176a5d9b1573676fcacc5df5e8c58f9e5fce34025600a19b3bf60617561c` |
| raw/epoch/20261122/csv/terminalbench_external.csv | 65,747 | `2ddde74508edf86412d288942c9eae6d2157080f623eda6f5a7c6d9997fa2f74` |
| raw/epoch/20261122/csv/the_agent_company_external.csv | 9,425 | `fdc459c051a06ba8a4b316f11d291532e18aaa9c9a49b0bd6ff716a0bc83ba20` |
| raw/epoch/20261122/csv/trivia_qa_external.csv | 42,584 | `39f98187506371e7e4c24392acb523a28b0a6c8e7fcace4bc704da344224de3d` |
| raw/epoch/20261122/csv/vending_bench_2_external.csv | 11,721 | `42f4dcd976edd90a8e4466722432072a4b4c51c2f4c5deb8c8a2899a6e255da2` |
| raw/epoch/20261122/csv/video_mme_external.csv | 12,967 | `16aa52df486b8e0c877da47710e81ea4b93a49bf04bc50c9a38e8156f53fa1d2` |
| raw/epoch/20261122/csv/vpct_external.csv | 9,136 | `02d50564b13f06ff6e499acddcdb1dea2b18c4e699c8ab9385e2cbbaafdc4c43` |
| raw/epoch/20261122/csv/webdev_arena_external.csv | 31,519 | `8360125f19d518462541c16d1a64e4e220fb7b2c48e3b82e04b51274f955382c` |
| raw/epoch/20261122/csv/weirdml_external.csv | 51,512 | `ffbb171209b196ef7441570b2df602ac0d552930c54f44d89a098cbb3f3ce324` |
| raw/epoch/20261122/csv/weirdml_v3_external.csv | 11,173 | `a775f29c04efa997923d1404a474f07f51a1d9140e3412e48832a1ca3842accb` |
| raw/epoch/20261122/csv/wino_grande_external.csv | 53,104 | `22ec3c23bb019996b409f6add2694cf6eb226594e5fdbfd6e41282d737db3136` |

## Code

code/deus_read.py runs the desk’s own scripts in code/, byte for byte, and changes the whole reader as the desk runs it. It reads only the saved files and touches no network. The same files are in the public repository under code/deus/. Scripts that run: code/deus_read.py.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
