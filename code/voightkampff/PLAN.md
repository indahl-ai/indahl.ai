# VOIGHT-KAMPFF: stated accuracy of AI-text detectors against independent tests

Status: plan, written before any test result is read. Nothing here has been run. The frame below is fixed now and does not change after the first test file is read.

Shape: same as zeus_index/PLAN.md. Claims read, Questions, Data, Frame fixed before any reading, outcomes four-way, and labels for preliminary data.

This is a measurement of what detector makers state against what independent tests with released data show. It is not a ranking of detectors, and no output orders them.

## 1. Claims read

### Stated side: what each maker says about its own detector

Read 2026-11-22 from each maker's own page. The run quotes the figure in force at each test's date (section 4), so these are the current figures, not the ones a test is read against.

- **GPTZero,** https://gptzero.me/technology (no date shown): "We keep GPTZero's false positive rate at no more than 1% when evaluating AI versus human text." Also "with a 96.5% accuracy rate", for mixed documents. Operating point: "the average error rate is less than 1% for the 'high' confidence predictions".
- **Turnitin,** https://turnitin.com/integrity-matters/integrity-matters-detail_14472 (no date shown): the document false positive rate "is less than 1% for documents with 20% or more AI writing", and "Our sentence-level false positive rate is around 4%."
- **Originality.ai,** https://originality.ai/blog/ai-content-detection-accuracy (dated Nov 7, 2026): "Originality.ai 5.0 has 99%+ accuracy". Earlier models carry their own rates, for example Turbo 3.0.2, "Even lower false positive rate of 1.5%." Operating point: "AI Allowance is 99%+ Accurate at 15% AI Allowed".
- **Copyleaks,** https://copyleaks.com/ai-content-detector/testing-methodology (published Sept 28, 2026): true positive rate "0.989", true negative rate "0.999", and false positive rates by setting, with Balanced (default) at "0.30%".
- **Pangram,** https://www.pangram.com/blog/technical-report-february-2024 (Feb 21, 2024): "Our model demonstrates 99.85% accuracy with 0.19% false positive rate".
- **Winston AI,** https://gowinston.ai/ai-content-detector/ (modified 2026-11-16): "99.87% Accurate". No numeric false positive rate, only "Tuned to eliminate false positives".

### Delivered side: independent tests that release their data

Setup only. No result from any test was read.

- **RAID** (Dugan et al., ACL 2024), https://arxiv.org/abs/2405.07940, data at https://huggingface.co/datasets/liamdugan/raid (MIT). It tested GPTZero (v2 API, queried Jan 24, 2024), Originality (v1 API, Jan 24 to 25, 2024), Winston (v1 API, date not stated) and ZeroGPT. Eleven domains, eleven generators, greedy and sampled decoding, and adversarial attacks. Its threshold is set per detector to give a 5% false positive rate on human text, so RAID's own false positive figure is fixed by design and is never read as a measured rate. Only raw per-item detector scores, read at the maker's own operating point, count here.
- **Liang et al. 2023,** "GPT detectors are biased against non-native English writers", https://arxiv.org/html/2304.02819v3, data at https://github.com/Weixin-Liang/ChatGPT-Detector-Bias/ and Zenodo 10.5281/zenodo.7893958 (MIT badge, no license file). Seven detectors accessed Mar 15, 2023, including Originality.AI, GPTZero and ZeroGPT. Human text includes TOEFL essays by non-native writers and essays by US students. The repository says each folder holds per-detector result files. Threshold not stated.
- **Jabarian and Imas 2025,** NBER working paper 34223, https://www.nber.org/system/files/working_papers/w34223/w34223.pdf, repository https://github.com/brianjabarian/DetectionAI (MIT). It tested Pangram (API v2025-05), GPTZero (API v2) and Originality (Turbo) on 1,992 pre-2020 human passages and machine text. The paper says the raw texts are partly placeholders, so per-item use is unconfirmed.
- **Weber-Wulff et al. 2023,** https://arxiv.org/abs/2306.15666v2, tested Turnitin and others. No data release was confirmed, so it does not enter unless one is found before the first read.

Gaps found: no independent test with released data covers Turnitin or Copyleaks. Their claims count as no independent test.

## 2. Questions

1. For each detector and each independent test with released per-item output, is the false positive rate on known-human text ABOVE, BELOW, CONSISTENT with, or CANNOT_TELL against the rate the maker stated?
2. The same for stated accuracy against the test's measured accuracy, as a secondary reading.
3. How many stated figures in the frame have no independent test with released data? Counted and listed by detector.

## 3. Data (all public, no key, no account)

- **Stated:** the makers' own pages, read in full and quoted word for word with URL, page date and date read. The figure in force at a test's query date is read from the maker's own page as captured by the Internet Archive on or before that date, quoted with the snapshot URL. An archive is used only to date a page that is readable live, never to get past a page that refuses reading.
- **Delivered:** the three test datasets above, downloaded from their public homes (Hugging Face, GitHub, Zenodo), keyless, credited under their licenses. RAID's full set is 16.7 GB, so the run streams only the human-text rows and the detector score columns.

## 4. Frame (fixed now, before any test result is read)

- **Detectors:** GPTZero, Turnitin, Originality.ai, Copyleaks, Pangram and Winston AI. ZeroGPT appears in the tests but states no figure that was read, so it has no stated side and is left out.
- **Tests:** RAID, Liang et al. 2023 and Jabarian and Imas 2025. A test enters for a detector only if it releases that detector's per-item output (a score or a label for each text). Without it, the pairing is nothing returned.
- **Human text:** only texts each test labels as written by people. Each test's human set is a carrier and is printed with the result: its domains, its writers (for example non-native writers in Liang et al.), its dates and its length.
- **Operating point:** the maker's own default decision, as the maker states it at the test date. A text counts as a false positive when the detector's output marks it as machine-written at that operating point. Where the test kept only a score and the maker states no numeric cut-off, the pairing reads CANNOT_TELL (NO_OPERATING_POINT). The run never picks a threshold of its own.
- **Version and date match (PACK L):** a stated figure is read against a test only when the stated figure was in force at the test's query date. Version is a carrier. Where the maker names a model version and the test names another, or either names none, a measured rate outside the stated figure reads CANNOT_TELL with the direction beside it.
- **Stated figure form:** "no more than", "less than" or "around" is a ceiling or a point, read as written. A ceiling can be met or exceeded, so BELOW is not reachable against a ceiling. Turnitin's figure holds only "for documents with 20% or more AI writing", which describes machine text, so its human-text rate is read only where the test matches that condition, and otherwise CANNOT_TELL.
- **Interval:** a Wilson 95% interval on the count of human texts in each test and each human subset. Texts from one source or writer may not be independent. Each test's own grouping is a carrier.
- **Accuracy (secondary):** accuracy is read only where the test's mix of human and machine text matches the mix the maker's figure describes. Otherwise CANNOT_TELL (MIX_DIFFERS).

### Headline cell (named in advance)

`voightkampff.fpr_outcomes`: across every detector and test pairing in the frame, the four-way count of the false positive rate on known-human text against the maker's stated rate, with no-test pairings counted beside it. Each pairing's measured rate and Wilson interval are printed under it. This is the number that hurts real people, because a false positive accuses a person who wrote their own words. The card, the ledger row and the reproduce kit read this field and no other as the headline.

Secondary cells: `voightkampff.accuracy_outcomes` (the same count for accuracy) and `voightkampff.no_test_count`.

## 5. Outcomes (four-way, delivered relative to stated)

- **ABOVE:** the whole interval of the measured false positive rate is above the stated rate or ceiling, with version and date matched.
- **BELOW:** the whole interval is below a stated point rate, with version and date matched. Not reachable against a ceiling.
- **CONSISTENT:** the interval contains the stated point, or lies at or under the stated ceiling.
- **CANNOT_TELL:** the interval straddles the stated figure, or version, date, operating point or text mix differs or is unnamed. The direction is written beside it and the reason named.

Nothing returned, refused and held are counted as their own outcomes. A detector with no released per-item output in any test is nothing returned. A maker's page that refuses reading is refused. A dataset that can't be fully read (for example placeholder texts) is held, listed, and left out of the headline.

## 6. Labels for preliminary data

- Until the referee's read, every output carries "PRELIMINARY: first run, not refereed". It stays off the home banner until then.
- Every result prints the test's date and the detector version it ran. Detectors change often, so a 2023 or 2024 test describes that version and no later one.
- Every count on the card and in the ledger comes from the run log, never typed in by hand.

## Open questions for the operator

1. **Archived maker pages:** the run reads the stated figure in force at each test date from the Internet Archive's capture of the maker's own page. Keep this, or read only today's figures and mark every pairing with a date gap as CANNOT_TELL?
2. **Turnitin and Copyleaks:** no independent test with released data was found. They enter as no test. Name another test before the first read if you know one.
3. **Direction words:** this plan reads delivered relative to stated, as ZEUS does. DEUS reads the stated score relative to the rerun, as its ball worded it. Pick one convention for the family before the cards go up.
