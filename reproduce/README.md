# Reproduce a desk headline

Heuremen LLC · https://indahl.ai/reproduce

Each folder recomputes one desk's headline number and outcome label with the desk's own code, offline. In each folder run `python3 run.py --check`.

reproduce_kits.py is the code that makes the kits and the release gate that reruns every kit before each release.

| Desk | Inputs | Expected output sha256 |
|---|---|---|
| [AILUMINATE](ailuminate/) | fetch and verify | `75252261f72159cfe6fe6ac1235a36d033769a95c57b19d985c4d55f09a5033c` |
| [AIRLINE](airline/) | included | `f32a4e777ddcb767a5d232aacfb62cb2fdaa988637a2dba251a24714e2230e58` |
| [AIRQ](airq/) | fetch and verify | `a105a4e665f0c2eef3ebd8bd394bae4a764c41aefc25cd5db23ad288ac8a3aed` |
| [CADENCE](cadence/) | included | `ef5f789c420e673298c1ff1cde1398ca11280f18262812a72e91a80b00df356e` |
| [CAMPUS](campus/) | fetch and verify | `fe00f96ae1cf9432b5f00c88ce28b57d4137cb116dad88789b416a50c5cf5c3f` |
| [CENSUS](census/) | included | `43f7368f318b9aef23d0af04771a2eb2dcdbc8eb4e81455405b5762fdccc2f1b` |
| [CHANGE](change/) | fetch and verify | `3da1b7f2707fa3cff0dab7ba2eb91494b96fadb45ee93ef03eeadccd7041c4a8` |
| [CONE](cone/) | included | `3a3cc8410a5f9d20204e42be09f230296d0a5d27a7f22182b340590551e02201` |
| [CREDIT](credit/) | included | `c4bbbebe5e465479ebda2c9119dd058d7ef97807e75f5c08009462c3ff5bf5ff` |
| [FEDSEP](fedsep/) | included | `c6978bc2ff30064c0bfe7edb79752a04b912fb7edaf9ed88a8f1bb9571bea7c0` |
| [FLU](flu/) | included | `a2600d5b326d324beacd2bdd7a06419879dafdfe4c5b68bf8a80c01d236c68f8` |
| [HFSIZE](hfsize/) | fetch and verify | `d3a8678dca1b26f272e6e8383330989010b904b2b957f190cb36e29f9b2461c5` |
| [HPT](hpt/) | included | `6703a53c368adddd460f402959758e15a266a0a002b21edfbfb9961b371fe0f1` |
| [LAUNCH](launch/) | fetch and verify | `9b86fccb7e97cdc034297acb756d8ece8d7d2f9d27e607b4c3f513b1a615c2ff` |
| [LINKROT](linkrot/) | included | `be54d807a01527bc4203d4438ae4e6e1ffaf291dda0df72a0cd39e1e80b565c7` |
| [NEO](neo/) | fetch and verify | `f736fda19153f7010fac276eaee4d36571bc6c475daefbfae636257d8c051f9f` |
| [PKGINSTALL](pkginstall/) | fetch and verify | `50cd23a1327ebbdd6bf56db81e4b2200c5bb37460a70de0ef4d75659518d6baa` |
| [PKGLICENSE](pkglicense/) | fetch and verify | `46ab84f4bef32aaa4d529cf50cf780da6697bf1850dab424d7115153b5766933` |
| [QUAKE](quake/) | included | `411e2994288904c8ffa264b151082fdecfb1a323f53605f3cffbf62503e23a13` |
| [SEASONAL](seasonal/) | included | `bc5c500339489235e7034dd1ab3df2971672bbb776d8c74808320075ada0d87f` |
| [SECRECORDS](secrecords/) | fetch and verify | `0a871fcaed515a931910e8d7e73335656d5bae01e1dcdd5227e014dd25aff4d9` |
| [SOLAR](solar/) | fetch and verify | `8ffa5dbef58acd6caa526a66b3d1e133a586d74877cd03304b4ec697e243329e` |
| [STEO](steo/) | included | `62582754f487e4bbb247ecb496530bfe0811c434a8f16222e973664ae554574d` |
| [SUPPORT](support/) | fetch and verify | `b0d76ba21b4a10feb689aa14805965b88cceac5dc2ec974c450a58f1ac7614c4` |
| [TORNADO](tornado/) | fetch and verify | `5ff5d0988b98d09801df2459fa0deb6eb6639eaa2ad0ff222460b5408c325930` |
| [TRIALS](trials/) | included | `024f8a5919f0578fdf39e0aa808df72436378fa75983f78ab9444dd916a178ff` |
| [WATER](water/) | included | `9fa82deee3bf63d3989a180ae7ff29fed0d2d341b59a49bcbe5a37f4640537cf` |
| [WEIGHTS](weights/) | fetch and verify | `c685e05ea6c8a80627dc06e75d4d736aa6d192fd541e3895c6459a5bfdc59820` |

## Desks without a kit

- CADA: The desk asks public DNS resolvers live whether they block fresh abuse listings. A resolver answer cannot be replayed.
- HOSTS: The headline is the count at the newest poll of OpenRouter, a live service whose answers cannot be replayed, and its flag test reads the 24 hours before the poll by the clock. Each poll is kept as parsed rows, not as the service's answers.
- REVISE: The headline compares the first BLS estimate with the most recent value, read from the BLS flat file on each run. The BLS table of first, second and third estimates is kept with its sha256. Until 10 Nov 2026 the flat file was not kept, so the published values cannot be replayed. From the next read on, each version of the flat file is kept by its sha256, and the start of its sha256 is in the feed.
- TAPE: The headline is a clock, the time since the newest entry was chained.
- TIME: The desk measures public time servers live against a GPS-disciplined clock. A time reading cannot be replayed.
- UPTIME: The desk probes vendor services and their status pages live from two networks. A probe answer cannot be replayed.
