# Reproduce a desk headline

Heuremen LLC · https://indahl.ai/reproduce

Each folder recomputes one desk’s headline number and outcome label with the desk’s own code, offline. In each folder run `python3 run.py --check`.

reproduce_kits.py is the code that makes the kits and the release gate that reruns every kit before each release.

| Desk | Inputs | Expected output sha256 |
|---|---|---|
| [AILUMINATE](ailuminate/) | fetch and verify | `a983d694c8576fc498dc37b7ff7c49e52fe910c6e328375a6233bdd073c8f0f3` |
| [AIRLINE](airline/) | included | `f32a4e777ddcb767a5d232aacfb62cb2fdaa988637a2dba251a24714e2230e58` |
| [AIRQ](airq/) | fetch and verify | `b75016c019c344ca87609c27552c4a4427926f8b1d52d8f465db81ee6445942a` |
| [ARES](ares/) | fetch and verify | `9a571f396218edaa23e43a66cc94ee236638effeee24d169c434b525372d0ca2` |
| [ARGUS](argus/) | fetch and verify | `a3f1012ded4bad73f008cca85340107e4bae889deadf585c0cb3f2fab3ffe442` |
| [CADENCE](cadence/) | included | `637417e5057146729ce3e8589ea3633475c948b4acaaccfe8bed3f7cf4d15b0d` |
| [CAMPUS](campus/) | fetch and verify | `975e05958a91b4d456f879d871322bb9f9474b09d22abd58595490103ad9d20b` |
| [CENSUS](census/) | included | `43f7368f318b9aef23d0af04771a2eb2dcdbc8eb4e81455405b5762fdccc2f1b` |
| [CHANGE](change/) | fetch and verify | `3da1b7f2707fa3cff0dab7ba2eb91494b96fadb45ee93ef03eeadccd7041c4a8` |
| [CONE](cone/) | included | `3a3cc8410a5f9d20204e42be09f230296d0a5d27a7f22182b340590551e02201` |
| [CREDIT](credit/) | included | `dc9d388c81bcafc7493de59f6cfe10c450157f909962f7ccc1aed57fda392eb3` |
| [DEUS](deus/) | fetch and verify | `d26495860af734cb101ece06a25f8eeca7d53487561fbef1715ad2d40c4061d0` |
| [FEDSEP](fedsep/) | included | `0d992fb204e98127560358a234492afc70b2d5c279c040963dc62e86937fd975` |
| [FLU](flu/) | included | `70f134448e6c3f2a7285cfaf31417c87974d33c7ed61d39d0c0736a8baf3e013` |
| [HFSIZE](hfsize/) | fetch and verify | `7b24ec3fe82039a323e3e6855f9ca3f725825a792e52e6384a26d288e5a52ba7` |
| [HPT](hpt/) | included | `1e7d500a04013231e66f04bb25966d5dc381cfe6b3c2a8e22cf239f18c985082` |
| [LAUNCH](launch/) | fetch and verify | `27411d642ca138921f14ad8b58829bf84e61fc19c522577ea8c96eade81501e4` |
| [LETHE](linkrot/) | included | `301f97cf489129761a35a170d88462950cf5031aa6802d687099656974967a60` |
| [NEO](neo/) | fetch and verify | `b62d2bfc2f939c7d3818b1055004b755ae1417b21c4a08edce93d7d9860b7cd9` |
| [PKGINSTALL](pkginstall/) | fetch and verify | `51b66bc97927f8161690c7c6aeb3e86f18081af65ab3768f31e5ed84488ed08f` |
| [PKGLICENSE](pkglicense/) | fetch and verify | `46ab84f4bef32aaa4d529cf50cf780da6697bf1850dab424d7115153b5766933` |
| [PROMETHEUS](prometheus/) | fetch and verify | `75765f774094ce3738a5bbbf8bf3da76344397a2caf3b9d277b437b3944f8961` |
| [QUAKE](quake/) | included | `026cc97e8c5e51a5906ae1d2edb2a209a7aaa5e48a145d66b83f27ea504b7dc1` |
| [SEASONAL](seasonal/) | included | `1cba88ef5719653d4062694b26db6777fd39a1f8c715816ce344494fbbc44b3b` |
| [SECRECORDS](secrecords/) | fetch and verify | `4740ccce5fbdedd5a133cbcb06f8f5119b14ad81f7108c16f8d6098fcd218cb1` |
| [SELDON](seldon/) | included | `6006080a590859c19528a680d7f34591b20c0faa6d28346e0015bb7d9fbdabc0` |
| [SOLAR](solar/) | fetch and verify | `2d116169c1de5e8599bf3e4a1bf513aff2a41e8f836a36472e1564d17d098c19` |
| [STEO](steo/) | included | `62582754f487e4bbb247ecb496530bfe0811c434a8f16222e973664ae554574d` |
| [SUPPORT](support/) | fetch and verify | `9378e1e83aa28ab04128e4a2e5d34065cb9f8df38764de1fde8949ce23353f87` |
| [TORNADO](tornado/) | fetch and verify | `81fe3c588bfc98918871070d6b762f3b513b5dc6b840b6ef1b186d73a7b34383` |
| [TRIALS](trials/) | included | `c0198e3bcf6f733e76fda3767f5eb6d23187cc889a1194cc25803da53363736b` |
| [VOIGHT-KAMPFF](voightkampff/) | fetch and verify | `7fb742f42ea2e38282e4bce76f5dd947cf1bbeae5443a10d659ac0c1e9e7268b` |
| [WATER](water/) | included | `9fa82deee3bf63d3989a180ae7ff29fed0d2d341b59a49bcbe5a37f4640537cf` |
| [WEIGHTS](weights/) | fetch and verify | `696dd1f22c805d59a3b3ee9aa658614583d85b0c890575e8c24e0f6d1647bab8` |
| [ZEUS](zeus/) | included | `a5bdac732f9a5db530dfe954c0db51980b8b3980c652506c8e2284bc585399f6` |

## Desks without a kit

- CADA: The desk asks public DNS resolvers live whether they block fresh abuse listings. A resolver answer cannot be replayed.
- HFLICENSE: The card is read from the Hugging Face API listing and each repository’s license file on the day of the read. Repositories change their files and the API answers with the current state.
- HOSTS: The headline is the count at the newest poll of OpenRouter, a live service whose answers cannot be replayed, and its flag test reads the 24 hours before the poll by the clock. Each poll is kept as parsed rows, not as the service’s answers.
- PETROL: The card is a count of outcome words for the newest OPEC month, read from the OPEC Monthly Oil Market Report tables and the EIA weekly files as each was published. A later report replaces the month it covers.
- RANK: Each US News figure is set beside a public record read one by one from state report cards, federal school and college data and schools’ own reports, sources that change on their own schedules.
- REVISE: The headline compares the first BLS estimate with the most recent value, read from the BLS flat file on each run. The BLS table of first, second and third estimates is kept with its sha256. Until 10 Nov 2026 the flat file was not kept, so the published values cannot be replayed. From the next read on, each version of the flat file is kept by its sha256, and the start of its sha256 is in the feed.
- SOCIAL: The ad-spend reading matches Google’s political ads library to FEC filings, both read as they stood on the read date. Neither source keeps the earlier answer.
- TAPE: The headline is a clock, the time since the newest entry was chained.
- TIME: The desk measures public time servers live against a GPS-disciplined clock. A time reading cannot be replayed.
- UPTIME: The desk probes vendor services and their status pages live from two networks. A probe answer cannot be replayed.
