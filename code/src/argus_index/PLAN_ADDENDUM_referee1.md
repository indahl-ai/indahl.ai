# ARGUS plan addendum: The referee's read of the mapping table, applied before the first run

Written 22 Nov 2026 UTC, after the ancestry column, the breed columns, the factor definitions and the question wording were read, and before any behavior column (factor scores, survey answers) was opened. PLAN.md section 4 asks the referee to read the mapping table before the first run. Her read is in referee/mapping_read_1.txt and the table it read is referee/mapping_ask_1.md (mapping.json at commit f56ec71, sha256 eaf54bd4).

Her changes, as applied in mapping.json at the commit that carries this file:

1. Golden Retriever "an unwarranted show of timidity or nervousness" moves from Human Sociability high to unmappable. The standard does not say toward people.
2. Labrador Retriever "non-aggressive towards ... animal" moves from Dog Sociability high to unmappable. Animals is wider than the dog-only items.
3. Labrador Retriever "Aggressiveness towards ... other animals" moves to unmappable, the same reason.
4. Each Agonistic Threshold row is checked against the item wording. Its high-loading items are all aggression on provocation or threat, so the three rows stay mapped to the diffident end, and the deciding items are printed beside each row.
5. Phrases that carry no trait (Golden Retriever "Such actions should be penalized according to their significance", Labrador Retriever "True Labrador Retriever temperament is as much a hallmark of the breed as the otter tail") are left out of every count.
6. Headline unit. `argus.direction_outcomes` counts each distinct breed, factor and direction once, and the phrase rows print beside it. This replaces "across every mapped breed and phrase" in PLAN.md section 4.
7. Comparison point. A breed's mean is read against the mean of all other dogs in the release, not all dogs. This replaces "the mean factor score across all dogs in the release" in PLAN.md section 4. The individual share is read against the same other-dogs mean. The bootstrap still resamples the whole release jointly, 2,000 draws, fixed seed.
8. The American Pit Bull Terrier prints as a coded row: not comparable, no standard reachable (American Kennel Club standard PDF 403 and breed page 404, Royal Kennel Club 404, checked 22 Nov 2026 UTC).
9. Recount before the first run: 9 mapped phrase rows, 10 unmappable trait phrases, 2 phrases with no trait left out, 6 distinct breed, factor and direction triples (Golden Retriever: Human Sociability high, Dog Sociability high, Agonistic Threshold high. Labrador Retriever: Human Sociability high, Biddability low, Agonistic Threshold high).

Stands as planned: the 85 percent ancestry rule, the 25-dog floor, the direction coding, the raw score column, Wilson intervals on the individual share, and the Biddability low rows for tractable and eager to please.
