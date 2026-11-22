# ARGUS: breed temperament stated in breed standards against open dog genetics and behavior data

Status: plan, written before any behavior or genetic data is read. Nothing here has been run. The frame below is fixed now and does not change after the first data file is read.

Shape: same as zeus_index/PLAN.md. Claims read, Questions, Data, Frame fixed before any reading, outcomes four-way, and labels for preliminary data.

Named for Odysseus's dog, who waited twenty years and knew him.

## 0. Which claim

Two claims were weighed.

- **Consumer dog-DNA tests' stated breed accuracy.** The makers state figures, but none says how it was measured, and no independent validation with released data was found. The only independent study found (Rando et al., JAVMA 2024, DOI 10.2460/javma.23.07.0372) tested 12 purebred dogs, has no data statement or repository, and can't test claims about mixed ancestry. This claim has no delivered side, so it is reported as a count of claims with no independent test (section 4), not as a frame.
- **Breed temperament in breed standards against open behavior and genetic data.** Both sides are public. The behavior and genetic data are released under CC0. This is the frame.

## 1. Claims read

### Stated side: breed standards

Breed standards describe temperament in adjectives, not levels. Two read on 2026-11-22:

- American Kennel Club, Golden Retriever standard (approved 1981), https://images.akc.org/pdf/breeds/standards/GoldenRetriever.pdf: "Friendly, reliable, and trustworthy."
- Royal Kennel Club, Border Collie standard (updated 1 January 2025), https://www.royalkennelclub.com/breed-standards/pastoral/border-collie: "Keen, alert, responsive and intelligent. Neither nervous nor aggressive."

Some phrases state a direction ("Neither nervous nor aggressive" means low on fear and aggression). Others are adjectives with no direction against other breeds. Comparing them with data needs each adjective mapped to a measured trait first. That mapping is the one judgment in this plan, and section 4 fixes it before any data is read.

### Stated side: consumer DNA tests (counted, not framed)

- Embark, https://embarkvet.com/collections/breed-ancestry (no date, footer 2026): "99% breed ancestry accuracy." No method given.
- DNA My Dog, https://dnamydog.com/ (modified 2023-08-30): "We test over 350 breeds with over 99% accuracy". No method given.
- Wisdom Panel, https://www.wisdompanel.com/downloads/wp-breed-detection.pdf (undated): "the global ancestry classifier shows a recall of 0.993". This is leave-one-out cross-validation on the maker's own reference dogs, not a test on new dogs.
- Orivet states no figure on its product page.

### Delivered side: Darwin's Ark

- Morrill et al., "Ancestry-inclusive dog genomics challenges popular breed stereotypes", Science 376:eabk0639 (2022), DOI 10.1126/science.abk0639, read at https://pmc.ncbi.nlm.nih.gov/articles/PMC9675396. Owners answered "12 short surveys (117 questions) on behavioral and physical traits". Breed ancestry comes from supervised ADMIXTURE against "a reference panel of 101 breeds". The paper's own quantity: "Breed offers little predictive value for individuals, explaining just 9% of variation in behavior."
- Data at Dryad, DOI 10.5061/dryad.g4f4qrfr0, and Zenodo, https://zenodo.org/records/6522639 (license field "Creative Commons Zero v1.0 Universal"). Files include DarwinsArk.zip (44.7 MB), GeneticData.zip (about 7 GB) and README.md. Both pages show open download links. The file formats are confirmed at build, because the README didn't render here and the network refused a direct download from this lane.
- The number of behavior factors needs a check. The Results say "eight factors that explain a cumulative 24.3% of variance in behavior". A reading tool reported a different count from the Methods. The run uses the factors as released in the data files and names the count it finds.

## 2. Questions

1. For each breed standard phrase that maps to a measured behavior factor, does the breed's average on that factor sit on the side the standard states, relative to all dogs in the data?
2. For the same phrases, what share of individual dogs of that breed sit on the stated side? This is the paper's point, put to each standard.
3. How many consumer DNA-test accuracy claims have no independent test with released data? Counted.

## 3. Data (all public, no key, no account)

- **Stated:** breed standards from the American Kennel Club's own standard PDFs, quoted from the Temperament section with URL and approval date. A breed with no AKC standard uses the Royal Kennel Club's, named as such.
- **Delivered:** the Darwin's Ark release (Dryad or Zenodo, CC0). Only DarwinsArk.zip (survey answers, factor scores and breed ancestry per dog) is needed. GeneticData.zip is not downloaded unless the per-dog ancestry is missing from DarwinsArk.zip.

## 4. Frame (fixed now, before any data is read)

- **Breed membership:** a dog belongs to a breed when its genetic ancestry is at least 85% from that breed, by the release's own ancestry estimates. Owner-reported breed is a secondary reading, printed beside it.
- **Breeds:** every breed with at least 25 dogs meeting the 85% rule and a published standard. The breed list is built from the ancestry column alone, before any behavior column is opened.
- **Mapping:** before any behavior data is read, a table is committed that maps every phrase in each standard's Temperament section to one behavior factor and one direction (high or low), using the factor names and item wording as released. A phrase that maps to no factor is listed as unmappable and counted, never forced. The referee reads the table before the first run. After that, the table does not change for this run.
- **Comparison point:** the mean factor score across all dogs in the release. A breed's direction is its mean relative to that.
- **Interval:** a 95% interval on the breed's mean minus the all-dog mean, by bootstrap over dogs.
- **Carriers, stated with every result:** behavior is owner-reported, not observed. Dogs in the release are those whose owners joined, which is not a sample of all dogs. A standard describes the breed as its club wants it, which may be read as an ideal rather than a claim about every dog. The run states this and still reads the standard's words as written.

### Headline cell (named in advance)

`argus.direction_outcomes`: across every mapped breed and phrase, the four-way count of the breed's average against the direction its standard states. The card, the ledger row and the reproduce kit read this field and no other as the headline.

Printed beside it, always: `argus.individual_stated_side_share`, for each mapped phrase the share of that breed's individual dogs on the stated side of the all-dog mean, with its interval. A breed can average on the stated side while many of its dogs don't, and the card shows both.

Secondary cells: `argus.unmappable_count` (phrases with no factor) and `argus.dna_test_no_test_count` (consumer DNA claims with no independent test with released data).

## 5. Outcomes (four-way, delivered relative to stated)

- **CONSISTENT:** the whole interval lies on the side the standard states.
- **ABOVE:** the standard states low, and the whole interval is above the all-dog mean.
- **BELOW:** the standard states high, and the whole interval is below the all-dog mean.
- **CANNOT_TELL:** the interval contains zero, or a frame item could not be met. The reason is named.

Nothing returned, refused and held are counted as their own outcomes. An unmappable phrase is nothing returned. A standard that can't be read is refused. A breed under 25 dogs is held and listed.

## 6. Labels for preliminary data

- Until the referee's read, every output carries "PRELIMINARY: first run, not refereed". It stays off the home banner until then.
- Every result carries "owner-reported behavior" beside it.
- Every count on the card and in the ledger comes from the run log, never typed in by hand.

## Open questions for the operator

1. **Mapping table:** it is written and committed before any behavior data is read, and the referee reads it first. Who writes it, this lane or the builder?
2. **Breed threshold:** 85% ancestry and at least 25 dogs are named. Change either before the first read if you want.
3. **Standards source:** AKC first, then the Royal Kennel Club. Keep that order?
