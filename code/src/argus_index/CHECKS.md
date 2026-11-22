# Check blocks (watch/readcheck.py). One entry per reading, appended, never edited after commit.

## Data access and terms (scouted 22 Nov 2026)
- Darwin's Ark release, Zenodo record 6522639: license field "Creative Commons Zero v1.0 Universal" (cc-zero). Cited on the page with the paper DOI and the record DOI. Only README.md and DarwinsArk.zip fetched (GeneticData.zip, about 7 GB, not needed: per-dog ancestry is in DarwinsArk.zip). Stored as data only in data/raw, files read with python -I.
- American Kennel Club standard PDFs: read and quoted as short temperament passages with URL and approval date.
- Requests one at a time, 2 s apart, user agent heuremen-argus/0.1 (+https://indahl.ai/argus), no key.

## 2026-11-21 21:11 ARGUS first read and ship: AKC breed standard temperament phrases mapped in advance to Darwin's Ark behavior factors (mapping read by the referee), genetic breed averages against all other dogs, owner-reported breed beside, DNA-test accuracy claims counted
packs: P,O
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: PLAN.md copied from indahl-ai/calibrations lane-research c680778 and committed a8a0421 (21:00:11 -05:00, sha256 e63f7572) before any data column was read. Breed list built from the ancestry column alone: 2,155 dogs with ancestry, 584 at 85 percent or more, 3 breeds with 25 or more (American pit bull terrier 42, golden retriever 31, labrador retriever 26), 85 held. Mapping committed f56ec71 before any behavior column was opened, the referee read it, her nine changes applied in c045c18 (PLAN_ADDENDUM_referee1.md), first comparison 02:06:25Z. Like for like: breed mean minus the mean of all other dogs on the same factor score
- II: holds: every triple prints dogs, difference, interval and reading apart, cannot tell never folded. Headline argus.direction_outcomes on 6 distinct breed, factor and direction triples: 4 CONSISTENT, 2 CANNOT_TELL, 0 ABOVE, 0 BELOW. Phrase rows (9): 7 consistent, 2 cannot tell, printed beside. 10 unmappable phrases counted as nothing returned, 2 no-trait phrases left out
- III: holds: the four consistent triples keep their sides and sizes: golden Agonistic Threshold +0.273 (0.018 to 0.516), labrador Human Sociability +0.407 (0.064 to 0.686), labrador Biddability -0.415 (-0.710 to -0.060), labrador Agonistic Threshold +0.564 (0.308 to 0.798). The two cannot tell: golden Human Sociability +0.325 (-0.050 to 0.647), golden Dog Sociability +0.194 (-0.143 to 0.530). Every point estimate is on the stated side
- V: holds: plan ruler is genetic membership (85 percent ancestry) with a 2,000-draw joint bootstrap over dogs, seed 20261122. Second ruler side by side, display only: owner-reported breed (n 261 to 764). It reads golden Human Sociability consistent (+0.452, 0.367 to 0.530) where the genetic ruler cannot tell, and golden Dog Sociability cannot tell on both. Individual share beside the headline: 68 to 92 percent of each breed's own dogs on the stated side (Wilson)
- VI: holds: four outcomes kept with a reason on every cannot tell (2 STRADDLES_EDGE). Both-alternatives test not applied because the plan names no size that matters, said on the page. Nothing returned (10 unmappable), refused (American pit bull terrier, no AKC or Royal Kennel Club standard reachable: AKC PDF 403, page 404, RKC 404) and held (85 breeds) counted apart
- R: holds: counts read from summary_argus.json of the run at 02:06Z (data/run1.log) and the publish run (data/run2.log), identical readings. DarwinsArk.zip md5 e9dc33d2 matches the Zenodo record. Factor ids in the scores file are 1 to 8, as the Results say (eight factors). Gate 2: 584 of 584 dogs at 85 percent carry the same breed in the release's regseq_breed. Gate 3: for each of the 8 factors the score correlates with its largest-loading item in the sign of the loading (abs r 0.56 to 0.87, n 12,229 to 14,270), which fixes high = the released positive label
- X: holds: no earlier reading
- P1: holds: temperament text copied from the fetched AKC PDFs and checked in the run (gate standards_text). Labrador text quoted in pieces at its semicolons, words unchanged. Paper quote from PMC9675396 as given in the plan. DNA claim quotes from PLAN.md section 1, read by the plan lane on 22 Nov 2026
- P2: holds: page figures come from summary_argus.json through build_page.py and argus_headline.py, the feed /argus/live.json is the same summary, ledger rows argus.* cite it
- P3: holds: factor names and their low and high labels as released in DarwinsArk_20191115_factors.csv
- P4: holds: no cause named. The page says a reading says where a breed average sits and not why
- P5: holds: breed intervals labelled 95 percent bootstrap over dogs, shares labelled Wilson 95 percent
- P6: holds: headline says 4 of 6, names the 2 cannot tell, and prints the individual share beside it, owner-reported and PRELIMINARY labels on the line
- P7: holds: ledger rows written through ledger/live_headlines.py before the ship, release through ledger/ship_request.sh only
- P8: cannot tell: checked after the ship on the live page
- P9: holds: lint_copy.py 0 hits. No semicolons, no digits or company names in headings, American spelling, Heuremen LLC named
- P10: holds: the headline unit (distinct triples), the other-dogs baseline and the mapping changes come from the referee's read before any behavior column was opened, dated in PLAN_ADDENDUM_referee1.md. No label added after the data
- O1: holds: rider on the tick bus every 264 ticks (about daily) with --publish putting argus_live in the site KV, served at /argus/live.json by the worker route
- O2: holds: a failed fetch names its file in sources_stale and the run falls back to the last copy. A failed gate turns every outcome into cannot tell and keeps the original. Without the referee's recorded read of the current mapping hash the run refuses (exit 4) and forms no reading
- O3: n/a: no GPU, CPU arithmetic only (numpy)
- O4: holds: the feed carries generated and updated, data/argus_history.jsonl gets one line per run
- O5: holds: argus_tick.py chdirs to its own folder, wrangler called by absolute path with PATH set as TORNADO does
- O6: n/a: no GPU job runs in this rider
