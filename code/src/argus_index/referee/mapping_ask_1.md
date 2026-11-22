From the operator: ARGUS (dog breed standards vs Darwin's Ark, plan indahl-ai/calibrations lane-research c680778, argus_index/PLAN.md). The plan asks you to read the phrase-to-factor mapping table before the first run. One decision: STANDS or a list of changes. No behavior column has been opened yet.

What was read so far: ancestry file, dogs file breed columns, factor definitions (names, item wording, loadings), questions file (wording, coding agree low / disagree high). Scores file only for its factor ids: 1 to 8 (Results say eight, confirmed).

Breed list from ancestry alone (85 percent rule, at least 25 dogs): American pit bull terrier 42, golden retriever 31, labrador retriever 26. 85 more breeds under 25, held. Pit bull is refused: no AKC standard (PDF 403, page 404) and no Royal Kennel Club standard (404).

Score direction: high = the factor's released positive label. F1 Human Sociability high = highly sociable. F4 Biddability high = independent. F5 Agonistic Threshold high = diffident. F6 Dog Sociability high = highly sociable. Raw column "score", not score.norm.

Golden (AKC 1981): Friendly -> F1 high. reliable -> unmappable. trustworthy -> unmappable. hostility to other dogs -> F6 high. hostility to people -> F5 high. timidity or nervousness -> F1 high. "Such actions should be penalized" -> unmappable.

Labrador (AKC 1994): hallmark sentence -> unmappable. kindly -> unmappable. outgoing -> F1 high. tractable -> F4 low. eager to please -> F4 low. non-aggressive to man -> F5 high. non-aggressive to animal -> F6 high (only dog items exist). appeals to people -> unmappable. gentle ways, intelligence, adaptability -> unmappable (the adapting item loads on no scored factor). penalty sentence: aggression to humans -> F5 high, to other animals -> F6 high, shyness in an adult -> F1 high (all ages read).

Counting: 12 mapped phrase rows, 9 unmappable. Restated phrases count as written, and the distinct breed-factor-direction count (7) prints beside the headline. Interval: 2,000-draw bootstrap over all dogs jointly, seed fixed, breed mean minus all-dog mean. Individual share uses a Wilson interval.

Full table with reasons: argus_index/mapping.json, commit f56ec71, sha256 eaf54bd4. Reply STANDS or changes, one line each.
