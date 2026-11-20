# Check blocks (watch/readcheck.py). One entry per reading, appended, never edited after commit.

## 2026-11-10 10:30 QUAKE desk first read: USGS aftershock forecasts (every archived oaf version) against ComCat counts in the zone each version states, range cells against the stated 95 percent and probability bins, Wilson and sequence-block bootstrap
packs: P,O
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: PLAN.md committed ae75b55 at 09:25:17 -05:00 (sha256 296dae27, data/plan_seal.json), first comparison 14:58:35Z, plan file unchanged since. Same quantity both sides: the number of ComCat earthquakes at or above the bin magnitude in the stated zone and window. The none is the counter gate: USGS's own observation counts before each forecast against our count for the same zone and span, 604 of 655 Sequence Specific versions agree within the larger of 2 and 20 percent. Drops by reason: 108,372 rows issued after the window opened (4,514 of 14,445 parsed versions, median 6.2 minutes late), 45,742 rows window not closed, 18 rows catalog not read, 788 rows zone not stated, 17 versions deleted, 2 versions whose forecast file does not parse. None of the drop rules reads a count
- II: holds: every range cell prints inside, above the range and below the range apart (M3 every window: 30,761 inside, 749 above, 440 below of 31,950). Probability cells print rows that saw at least one beside the mean stated chance. Repeat floor: the counter gate. No chance figure is compared with a count of misses
- III: holds: misses keep their side and are dated. The row farthest outside its range per event is listed with version date, window, stated chance, range and count
- V: holds: plan ruler is the union of the 95% Wilson interval and the 2,000-resample sequence-block bootstrap (seed 20261110, blocks of mainshocks within 100 km and 365 days, 91 blocks, 83 with scored M3 rows). Second ruler, Wilson alone, is printed. It would read the M3 every-window cell ABOVE (96.07 to 96.48) where the union reads CANNOT_TELL (94.66 to 97.78). The plan ruler decides. Magnitudes rounded to one decimal keep the same range reading in 159,593 of 159,706 rows
- VI: holds: four outcomes kept, both alternatives stated in the plan. Range cells: M3 every window CANNOT_TELL (30,761 of 31,950, 94.7 to 97.8 percent), M3 one day ABOVE (9,627 of 9,736, 98.0 to 99.4), one week ABOVE (9,382 of 9,626, 96.0 to 98.4), one month CANNOT_TELL (8,805 of 9,179, 94.0 to 97.6), one year BELOW (2,947 of 3,409, 79.2 to 94.2). M4 ABOVE (31,386 of 31,830), M5 ABOVE (31,841 of 31,950), M6 ABOVE (31,945 of 31,950), M7 ABOVE (31,949 of 31,950). Probability bins: 0 to 1 percent CONSISTENT (289 of 118,077 against 0.11), 1 to 5 CANNOT_TELL (576 of 17,366 against 2.42), 5 to 10 CONSISTENT (431 of 6,381 against 7.14), 10 to 20 BELOW (593 of 5,635 against 14.36), 20 to 40 BELOW (938 of 4,888 against 28.52), 40 to 60 BELOW (904 of 2,684 against 49.34), 60 to 80 BELOW (789 of 1,854 against 69.52), 80 to 90 BELOW (467 of 746 against 84.93), 90 to 99 BELOW (636 of 816 against 95.19), 99 to 100 BELOW (1,231 of 1,259 against 99.90). As large as the mainshock CONSISTENT (56 of 31,950 against 0.37)
- R: holds: counts read from summary_quake.json and data/quake_rows.json.gz of this run. One count read against ComCat directly: Ridgecrest version 2019-09-14, week window 2019-09-14 04:00 to 09-21 04:00, 60 km circle, M3 and above: the count service gives 0, the desk 0 (stated chance 99.41 percent, range 2 to 11). Reader gate rows in data/known_good_rows.json (three forecast files, raw text equals parsed)
- P1: holds: the USGS sentences in PLAN.md and the page were copied from earthquake.usgs.gov/data/oaf/overview.php, background.php and schedule.php fetched 10 Nov 2026
- P2: holds: page names the product (oaf), the service, every archived version, and its figures live in summary_quake.json, with every row in data/quake_rows.json.gz
- P3: holds: "95% confidence range", "probability" and the window labels as the USGS prints them. "Above the range" and "below the range" are our words, defined in the note
- P4: holds: the page says a count outside the range is a count outside the range and does not say why. The split by network is shown and not scored, with no reason given
- P5: holds: every interval is labelled Wilson or sequence, both 95%
- P6: n/a: first read
- P7: cannot tell: ledger rows, site build and tick-bus rider come with the ship entry below
- P8: holds: quake.html parsed with every tag closed, visible text read in full
- P9: holds: lint_copy.py on quake.html gives 0 hits. One USGS quotation that held the words "due to" was replaced with a plain description of what it says
- P10: holds: additions after the data, display only: the publication-lag figures (late_versions), the row farthest outside its range per event (biggest_misses), and the restriction of the by-magnitude table to the plan's magnitudes 3 to 7 (76 rows also state M8 and stay in the every-magnitude cell). No rule, threshold, cell or outcome definition changed after the plan
- O1: cannot tell: the rider is added at ship
- O2: holds: a failed fetch names its source in sources.stale and the run falls back to the last copy. A failed gate turns every scored outcome into cannot tell and keeps the original
- O3: n/a: no GPU used
- O4: holds: summary carries generated time, plan seal, and data/quake_history.jsonl gets one line per run
- O5: holds: quake_tick.py chdirs to its own folder and every path is under it. Standard library only
- O6: n/a: no GPU job

## Data access and terms (scouted 10 Nov 2026)
- USGS ComCat event service (earthquake.usgs.gov/fdsnws/event/1), keyless. USGS-authored data are in the public domain. User agent heuremen-quake/0.1 (+https://indahl.ai/quake).
- Every archived oaf version: includesuperseded=true on the event query. forecast.json per version at earthquake.usgs.gov/product/oaf/<code>/us/<updateTime>/forecast.json, inline bytes for some 2019 to 2023 versions. Bulk read with at most four connections, 0.25 s between requests per connection. The rider reads new versions one at a time.
- Zone: forecast.json model.parameters regionType circle, regionCenterLat, regionCenterLon, regionRadius (km) from 2022 on. Earlier versions: forecast_data.json parameters.aftershock_search_region with min_depth and max_depth where the version carries that file.
- Catalog: one query per mainshock, from the mainshock time, radius out to the far edge of every stated zone, 0.05 below the lowest stated magnitude, eventtype earthquake, kept gzipped in data/raw/catalog with its fetch time.

## 2026-11-10 11:00 QUAKE ship after the outside referee: referee fixes R1 to R3, R5 and R7 in the page and the headline, ledger rows for the range cells, the probability bins and the display split, page at /quake under ATLAS, feed /quake/live.json, rider publishing on the tick bus
packs: P,O
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the none is unchanged from the first read (counter gate 604 of 655). The referee recount (quake_index_referee/code/recount.py, own reader, zone test, counter, Wilson and bootstrap) reproduces every row of data/quake_rows.json.gz, 0 count, outcome or frame differences in 346,576 rows. Drops by reason are the first read's
- II: holds: inside, above and below printed apart in every range cell. Every magnitude and window together: 157,958 of 159,706 inside, ABOVE
- III: holds: one row per event farthest outside its range, dated, with side
- V: holds: plan ruler unchanged. Referee bootstrap bounds differ from ours by at most 0.15 points on large cells. The one-month M3 cell (8,805 of 9,179) sits on the 97.5 line and flips with the draw (19 of 41 referee seeds CONSISTENT). The sealed seed reads CANNOT_TELL and the page says only cannot tell
- VI: holds: outcomes as in the first read. Display split added at the referee (R1), decides nothing, stated 10 percent or more: every magnitude every window BELOW (5,558 of 17,882 against 41.9), M3 BELOW (3,780 of 12,491 against 44.5), M4 and above CANNOT_TELL (1,778 of 5,391 against 35.6), one day BELOW (336 of 1,410), one week BELOW (863 of 4,106), one month BELOW (1,719 of 7,247), one year CANNOT_TELL (2,640 of 5,119 against 50.7). First version of each forecast, M3: 668 of 719 inside, described
- R: holds: referee spot checks, 8 ComCat count queries, 7 exact and 1 off by one on a 500 km zone edge
- P1: holds: USGS wording unchanged
- P2: holds: page figures from summary_quake.json of the run of 10 Nov
- P3: fixed: "public before the window opened" now reads "stamped in the catalog before the window opened" (referee R7), and the page counts the 985 scored rows from versions indexed after their window opened
- P4: fixed: the national/regional network split is said not to separate US events from events elsewhere, and a split by place (us_place.py, a text rule on the ComCat place and title) is shown, with no reason given for any difference (referee R2)
- P5: fixed: the last column now prints groups of sequences (bootstrap blocks), and the rule line says groups of nearby sequences (referee R3). The range 0 to 0 count is a column for every range cell, and M3 without those rows is described (referee R5)
- P6: fixed: the headline no longer says "Across every magnitude". It gives the pooled 10 percent and up reading and the split by magnitude and window (referee R1)
- P7: holds: ledger rows quake.cover.*, quake.prob.*, quake.prob10.*, quake.first.m3 added before the site edit, surface desk_quake
- P8: holds: quake.html rebuilt, tags closed, visible text read in full
- P9: holds: lint_copy.py 0 hits
- P10: holds: additions after the data at the referee, display only, labelled in summary_quake.json after_data_note and on the page: the split at 10 percent and up, the split by place, cells without 0 to 0 ranges, rows indexed after the window opened
- O1: holds: rider on the tick bus every 60 ticks with --publish (KV quake_live)
- O2: holds: as in the first read
- O3: n/a: no GPU used, network reads and arithmetic on the CPU
- O4: holds: data/quake_history.jsonl one line per run
- O5: holds: own folder, standard library only
- O6: n/a: no GPU job runs in this rider

## 2026-11-11 11:16 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-11T14:23:11Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-11T14:23:11Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-11T14:23:11Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9458, hi 0.9776, unit 30,622 of 31,820, outcome CANNOT_TELL, as printed: M3 and above, every window 31,820 30,622 756 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell 82 12,699
row-record quake.cover.m4: value 0.9857, lo 0.979, hi 0.9941, unit 31,248 of 31,700, outcome ABOVE, as printed: M4 and above 31,700 31,248 446 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,729
row-record quake.cover.m5: value 0.9965, lo 0.9936, hi 0.9987, unit 31,710 of 31,820, outcome ABOVE, as printed: M5 and above 31,820 31,710 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,212
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,815 of 31,820, outcome ABOVE, as printed: M6 and above 31,820 31,815 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,369
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,819 of 31,820, outcome ABOVE, as printed: M7 and above 31,820 31,819 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,706
row-record quake.cover.m3.day: value 0.9888, lo 0.9805, hi 0.9938, unit 9,595 of 9,704, outcome ABOVE, as printed: M3 and above, 1 day 9,704 9,595 51 58 98.9 98.7 to 99.1 98.0 to 99.4 above 82 7,029
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.9839, unit 9,346 of 9,591, outcome ABOVE, as printed: M3 and above, 1 week 9,591 9,346 136 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,700
row-record quake.cover.m3.month: value 0.9585, lo 0.9391, hi 0.9755, unit 8,764 of 9,143, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,143 8,764 230 149 95.9 95.4 to 96.2 93.9 to 97.5 cannot tell 77 1,766
row-record quake.cover.m3.year: value 0.8625, lo 0.7892, hi 0.9408, unit 2,917 of 3,382, outcome BELOW, as printed: M3 and above, 1 year 3,382 2,917 339 126 86.2 85.0 to 87.4 78.9 to 94.1 below 42 204
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,290 of 159,056, outcome ABOVE, as printed: every magnitude, every window 159,056 157,290 1,317 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,775
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 302 of 117,393, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,393 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0334, lo 0.0165, hi 0.0488, unit 579 of 17,360, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,360 579 2.4 3.3 3.1 to 3.6 1.7 to 4.9 cannot tell 82
row-record quake.prob.5_10: value 0.0678, lo 0.0459, hi 0.0913, unit 432 of 6,373, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,373 432 7.1 6.8 6.2 to 7.4 4.6 to 9.1 consistent 80
row-record quake.prob.10_20: value 0.1053, lo 0.0743, hi 0.1363, unit 595 of 5,648, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,648 595 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1923, lo 0.1499, hi 0.2358, unit 943 of 4,904, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,904 943 28.5 19.2 18.1 to 20.4 15.0 to 23.6 below 74
row-record quake.prob.40_60: value 0.3373, lo 0.2638, hi 0.4098, unit 907 of 2,689, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,689 907 49.3 33.7 32.0 to 35.5 26.4 to 41.0 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3042, hi 0.5614, unit 796 of 1,861, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,861 796 69.5 42.8 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.6248, lo 0.4904, hi 0.7564, unit 468 of 749, outcome BELOW, as printed: 80 to 90 percent, not including 90 749 468 84.9 62.5 59.0 to 65.9 49.0 to 75.6 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0044, unit 62 of 31,820, outcome CONSISTENT, as printed: 62 of 31,820 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.311, lo 0.2427, hi 0.3861, unit 5,577 of 17,930, outcome BELOW, as printed: every magnitude, every window 17,930 5,577 41.9 31.1 30.4 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3029, lo 0.2303, hi 0.3833, unit 3,793 of 12,523, outcome BELOW, as printed: M3 and above 12,523 3,793 44.6 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3299, lo 0.2445, hi 0.419, unit 1,784 of 5,407, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,407 1,784 35.6 33.0 31.8 to 34.3 24.4 to 41.9 cannot tell 52
row-record quake.prob10.day: value 0.2381, lo 0.139, hi 0.3388, unit 336 of 1,411, outcome BELOW, as printed: every magnitude, 1 day 1,411 336 36.1 23.8 21.7 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.21, lo 0.1301, hi 0.3094, unit 863 of 4,109, outcome BELOW, as printed: every magnitude, 1 week 4,109 863 36.8 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2371, lo 0.164, hi 0.3265, unit 1,721 of 7,259, outcome BELOW, as printed: every magnitude, 1 month 7,259 1,721 39.6 23.7 22.7 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.5158, lo 0.4214, hi 0.6044, unit 2,657 of 5,151, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,151 2,657 50.7 51.6 50.2 to 52.9 42.1 to 60.4 cannot tell 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-11 11:34 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-11T16:29:29Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-11T16:29:29Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-11T16:29:29Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9458, hi 0.9776, unit 30,630 of 31,828, outcome CANNOT_TELL, as printed: M3 and above, every window 31,828 30,630 756 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell 82 12,703
row-record quake.cover.m4: value 0.9857, lo 0.979, hi 0.9941, unit 31,256 of 31,708, outcome ABOVE, as printed: M4 and above 31,708 31,256 446 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,736
row-record quake.cover.m5: value 0.9965, lo 0.9936, hi 0.9987, unit 31,718 of 31,828, outcome ABOVE, as printed: M5 and above 31,828 31,718 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,220
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,823 of 31,828, outcome ABOVE, as printed: M6 and above 31,828 31,823 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,377
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,827 of 31,828, outcome ABOVE, as printed: M7 and above 31,828 31,827 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,714
row-record quake.cover.m3.day: value 0.9888, lo 0.9805, hi 0.9938, unit 9,597 of 9,706, outcome ABOVE, as printed: M3 and above, 1 day 9,706 9,597 51 58 98.9 98.7 to 99.1 98.0 to 99.4 above 82 7,031
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,350 of 9,595, outcome ABOVE, as printed: M3 and above, 1 week 9,595 9,350 136 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,702
row-record quake.cover.m3.month: value 0.9586, lo 0.9391, hi 0.9755, unit 8,765 of 9,144, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,144 8,765 230 149 95.9 95.4 to 96.2 93.9 to 97.5 cannot tell 77 1,766
row-record quake.cover.m3.year: value 0.8625, lo 0.7893, hi 0.9408, unit 2,918 of 3,383, outcome BELOW, as printed: M3 and above, 1 year 3,383 2,918 339 126 86.2 85.0 to 87.4 78.9 to 94.1 below 42 204
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,330 of 159,096, outcome ABOVE, as printed: every magnitude, every window 159,096 157,330 1,317 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,810
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 302 of 117,428, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,428 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0333, lo 0.0165, hi 0.0487, unit 579 of 17,363, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,363 579 2.4 3.3 3.1 to 3.6 1.7 to 4.9 cannot tell 82
row-record quake.prob.5_10: value 0.0678, lo 0.0459, hi 0.0913, unit 432 of 6,374, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,374 432 7.1 6.8 6.2 to 7.4 4.6 to 9.1 consistent 80
row-record quake.prob.10_20: value 0.1053, lo 0.0743, hi 0.1363, unit 595 of 5,648, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,648 595 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1923, lo 0.1499, hi 0.2358, unit 943 of 4,905, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,905 943 28.5 19.2 18.1 to 20.3 15.0 to 23.6 below 74
row-record quake.prob.40_60: value 0.3373, lo 0.2638, hi 0.4098, unit 907 of 2,689, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,689 907 49.3 33.7 32.0 to 35.5 26.4 to 41.0 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3042, hi 0.5614, unit 796 of 1,861, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,861 796 69.5 42.8 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.6248, lo 0.4904, hi 0.7564, unit 468 of 749, outcome BELOW, as printed: 80 to 90 percent, not including 90 749 468 84.9 62.5 59.0 to 65.9 49.0 to 75.6 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0044, unit 62 of 31,828, outcome CONSISTENT, as printed: 62 of 31,828 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.311, lo 0.2427, hi 0.3861, unit 5,577 of 17,931, outcome BELOW, as printed: every magnitude, every window 17,931 5,577 41.9 31.1 30.4 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3029, lo 0.2303, hi 0.3833, unit 3,793 of 12,524, outcome BELOW, as printed: M3 and above 12,524 3,793 44.6 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3299, lo 0.2445, hi 0.419, unit 1,784 of 5,407, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,407 1,784 35.6 33.0 31.8 to 34.3 24.4 to 41.9 cannot tell 52
row-record quake.prob10.day: value 0.2381, lo 0.139, hi 0.3388, unit 336 of 1,411, outcome BELOW, as printed: every magnitude, 1 day 1,411 336 36.1 23.8 21.7 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.21, lo 0.1301, hi 0.3094, unit 863 of 4,109, outcome BELOW, as printed: every magnitude, 1 week 4,109 863 36.8 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2371, lo 0.164, hi 0.3265, unit 1,721 of 7,259, outcome BELOW, as printed: every magnitude, 1 month 7,259 1,721 39.6 23.7 22.7 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.5157, lo 0.4214, hi 0.6039, unit 2,657 of 5,152, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,152 2,657 50.7 51.6 50.2 to 52.9 42.1 to 60.4 cannot tell 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-11 13:45 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-11T18:42:18Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-11T18:42:18Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-11T18:42:18Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9458, hi 0.9776, unit 30,633 of 31,831, outcome CANNOT_TELL, as printed: M3 and above, every window 31,831 30,633 756 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell 82 12,704
row-record quake.cover.m4: value 0.9857, lo 0.979, hi 0.9941, unit 31,259 of 31,711, outcome ABOVE, as printed: M4 and above 31,711 31,259 446 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,738
row-record quake.cover.m5: value 0.9965, lo 0.9936, hi 0.9987, unit 31,721 of 31,831, outcome ABOVE, as printed: M5 and above 31,831 31,721 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,222
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,826 of 31,831, outcome ABOVE, as printed: M6 and above 31,831 31,826 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,380
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,830 of 31,831, outcome ABOVE, as printed: M7 and above 31,831 31,830 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,717
row-record quake.cover.m3.day: value 0.9888, lo 0.9805, hi 0.9938, unit 9,598 of 9,707, outcome ABOVE, as printed: M3 and above, 1 day 9,707 9,598 51 58 98.9 98.7 to 99.1 98.0 to 99.4 above 82 7,032
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,350 of 9,595, outcome ABOVE, as printed: M3 and above, 1 week 9,595 9,350 136 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,702
row-record quake.cover.m3.month: value 0.9586, lo 0.9391, hi 0.9755, unit 8,766 of 9,145, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,145 8,766 230 149 95.9 95.4 to 96.2 93.9 to 97.5 cannot tell 77 1,766
row-record quake.cover.m3.year: value 0.8626, lo 0.7894, hi 0.9409, unit 2,919 of 3,384, outcome BELOW, as printed: M3 and above, 1 year 3,384 2,919 339 126 86.3 85.1 to 87.4 78.9 to 94.1 below 42 204
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,345 of 159,111, outcome ABOVE, as printed: every magnitude, every window 159,111 157,345 1,317 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,821
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 302 of 117,439, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,439 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0333, lo 0.0165, hi 0.0487, unit 579 of 17,364, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,364 579 2.4 3.3 3.1 to 3.6 1.7 to 4.9 cannot tell 82
row-record quake.prob.5_10: value 0.0678, lo 0.0459, hi 0.0913, unit 432 of 6,375, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,375 432 7.1 6.8 6.2 to 7.4 4.6 to 9.1 consistent 80
row-record quake.prob.10_20: value 0.1053, lo 0.0743, hi 0.1363, unit 595 of 5,648, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,648 595 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1922, lo 0.1499, hi 0.2357, unit 943 of 4,906, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,906 943 28.5 19.2 18.1 to 20.3 15.0 to 23.6 below 74
row-record quake.prob.40_60: value 0.3373, lo 0.2638, hi 0.4098, unit 907 of 2,689, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,689 907 49.3 33.7 32.0 to 35.5 26.4 to 41.0 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3042, hi 0.5614, unit 796 of 1,861, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,861 796 69.5 42.8 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.6253, lo 0.4914, hi 0.7568, unit 469 of 750, outcome BELOW, as printed: 80 to 90 percent, not including 90 750 469 84.9 62.5 59.0 to 65.9 49.1 to 75.7 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0044, unit 62 of 31,831, outcome CONSISTENT, as printed: 62 of 31,831 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.311, lo 0.2427, hi 0.3861, unit 5,578 of 17,933, outcome BELOW, as printed: every magnitude, every window 17,933 5,578 41.9 31.1 30.4 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3029, lo 0.2303, hi 0.3833, unit 3,794 of 12,525, outcome BELOW, as printed: M3 and above 12,525 3,794 44.6 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3299, lo 0.2445, hi 0.419, unit 1,784 of 5,408, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,408 1,784 35.6 33.0 31.8 to 34.2 24.4 to 41.9 cannot tell 52
row-record quake.prob10.day: value 0.2381, lo 0.139, hi 0.3388, unit 336 of 1,411, outcome BELOW, as printed: every magnitude, 1 day 1,411 336 36.1 23.8 21.7 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.21, lo 0.1301, hi 0.3094, unit 863 of 4,109, outcome BELOW, as printed: every magnitude, 1 week 4,109 863 36.8 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2371, lo 0.164, hi 0.3265, unit 1,721 of 7,259, outcome BELOW, as printed: every magnitude, 1 month 7,259 1,721 39.6 23.7 22.7 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.5157, lo 0.4214, hi 0.6039, unit 2,658 of 5,154, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,154 2,658 50.7 51.6 50.2 to 52.9 42.1 to 60.4 cannot tell 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-11 16:15 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-11T20:53:40Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-11T20:53:40Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-11T20:53:40Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9776, unit 30,640 of 31,838, outcome CANNOT_TELL, as printed: M3 and above, every window 31,838 30,640 756 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell 82 12,705
row-record quake.cover.m4: value 0.9857, lo 0.979, hi 0.9941, unit 31,266 of 31,718, outcome ABOVE, as printed: M4 and above 31,718 31,266 446 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,741
row-record quake.cover.m5: value 0.9965, lo 0.9936, hi 0.9987, unit 31,728 of 31,838, outcome ABOVE, as printed: M5 and above 31,838 31,728 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,229
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,833 of 31,838, outcome ABOVE, as printed: M6 and above 31,838 31,833 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,387
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,837 of 31,838, outcome ABOVE, as printed: M7 and above 31,838 31,837 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,724
row-record quake.cover.m3.day: value 0.9888, lo 0.9805, hi 0.9938, unit 9,599 of 9,708, outcome ABOVE, as printed: M3 and above, 1 day 9,708 9,599 51 58 98.9 98.7 to 99.1 98.0 to 99.4 above 82 7,033
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,352 of 9,597, outcome ABOVE, as printed: M3 and above, 1 week 9,597 9,352 136 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,702
row-record quake.cover.m3.month: value 0.9586, lo 0.9391, hi 0.9756, unit 8,768 of 9,147, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,147 8,768 230 149 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell 77 1,766
row-record quake.cover.m3.year: value 0.8627, lo 0.7895, hi 0.9409, unit 2,921 of 3,386, outcome BELOW, as printed: M3 and above, 1 year 3,386 2,921 339 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 204
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,380 of 159,146, outcome ABOVE, as printed: every magnitude, every window 159,146 157,380 1,317 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,846
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 302 of 117,460, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,460 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0333, lo 0.0165, hi 0.0487, unit 579 of 17,370, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,370 579 2.4 3.3 3.1 to 3.6 1.7 to 4.9 cannot tell 82
row-record quake.prob.5_10: value 0.0679, lo 0.046, hi 0.0915, unit 433 of 6,376, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,376 433 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1053, lo 0.0742, hi 0.1362, unit 595 of 5,652, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,652 595 14.4 10.5 9.8 to 11.3 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1924, lo 0.1505, hi 0.2359, unit 944 of 4,907, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,907 944 28.5 19.2 18.2 to 20.4 15.0 to 23.6 below 74
row-record quake.prob.40_60: value 0.3372, lo 0.2637, hi 0.4098, unit 907 of 2,690, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,690 907 49.3 33.7 32.0 to 35.5 26.4 to 41.0 below 58
row-record quake.prob.60_80: value 0.4275, lo 0.304, hi 0.5609, unit 796 of 1,862, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,862 796 69.5 42.8 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.6253, lo 0.4914, hi 0.7568, unit 469 of 750, outcome BELOW, as printed: 80 to 90 percent, not including 90 750 469 84.9 62.5 59.0 to 65.9 49.1 to 75.7 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0044, unit 62 of 31,838, outcome CONSISTENT, as printed: 62 of 31,838 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.311, lo 0.2426, hi 0.3861, unit 5,579 of 17,940, outcome BELOW, as printed: every magnitude, every window 17,940 5,579 41.9 31.1 30.4 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3029, lo 0.2304, hi 0.3833, unit 3,795 of 12,530, outcome BELOW, as printed: M3 and above 12,530 3,795 44.6 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3298, lo 0.2443, hi 0.419, unit 1,784 of 5,410, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,410 1,784 35.6 33.0 31.7 to 34.2 24.4 to 41.9 cannot tell 52
row-record quake.prob10.day: value 0.2381, lo 0.139, hi 0.3388, unit 336 of 1,411, outcome BELOW, as printed: every magnitude, 1 day 1,411 336 36.1 23.8 21.7 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2099, lo 0.13, hi 0.3092, unit 863 of 4,111, outcome BELOW, as printed: every magnitude, 1 week 4,111 863 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.237, lo 0.1639, hi 0.3264, unit 1,721 of 7,263, outcome BELOW, as printed: every magnitude, 1 month 7,263 1,721 39.6 23.7 22.7 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.5158, lo 0.4214, hi 0.6039, unit 2,659 of 5,155, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,155 2,659 50.7 51.6 50.2 to 52.9 42.1 to 60.4 cannot tell 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-11 19:07 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-11T23:02:40Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-11T23:02:40Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-11T23:02:40Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9776, unit 30,650 of 31,848, outcome CANNOT_TELL, as printed: M3 and above, every window 31,848 30,650 756 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell 82 12,710
row-record quake.cover.m4: value 0.9858, lo 0.979, hi 0.9941, unit 31,276 of 31,728, outcome ABOVE, as printed: M4 and above 31,728 31,276 446 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,749
row-record quake.cover.m5: value 0.9965, lo 0.9936, hi 0.9987, unit 31,738 of 31,848, outcome ABOVE, as printed: M5 and above 31,848 31,738 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,239
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,843 of 31,848, outcome ABOVE, as printed: M6 and above 31,848 31,843 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,397
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,847 of 31,848, outcome ABOVE, as printed: M7 and above 31,848 31,847 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,734
row-record quake.cover.m3.day: value 0.9888, lo 0.9805, hi 0.9938, unit 9,603 of 9,712, outcome ABOVE, as printed: M3 and above, 1 day 9,712 9,603 51 58 98.9 98.7 to 99.1 98.0 to 99.4 above 82 7,036
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,354 of 9,599, outcome ABOVE, as printed: M3 and above, 1 week 9,599 9,354 136 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,703
row-record quake.cover.m3.month: value 0.9586, lo 0.9391, hi 0.9756, unit 8,772 of 9,151, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,151 8,772 230 149 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell 77 1,767
row-record quake.cover.m3.year: value 0.8627, lo 0.7895, hi 0.9409, unit 2,921 of 3,386, outcome BELOW, as printed: M3 and above, 1 year 3,386 2,921 339 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 204
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,430 of 159,196, outcome ABOVE, as printed: every magnitude, every window 159,196 157,430 1,317 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,889
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 302 of 117,503, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,503 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0333, lo 0.0165, hi 0.0487, unit 579 of 17,375, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,375 579 2.4 3.3 3.1 to 3.6 1.7 to 4.9 cannot tell 82
row-record quake.prob.5_10: value 0.0679, lo 0.046, hi 0.0915, unit 433 of 6,376, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,376 433 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1053, lo 0.0742, hi 0.1362, unit 595 of 5,652, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,652 595 14.4 10.5 9.8 to 11.3 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1923, lo 0.1505, hi 0.2359, unit 944 of 4,909, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,909 944 28.5 19.2 18.1 to 20.4 15.0 to 23.6 below 74
row-record quake.prob.40_60: value 0.3372, lo 0.2637, hi 0.4098, unit 907 of 2,690, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,690 907 49.3 33.7 32.0 to 35.5 26.4 to 41.0 below 58
row-record quake.prob.60_80: value 0.4275, lo 0.304, hi 0.5609, unit 796 of 1,862, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,862 796 69.5 42.8 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.6253, lo 0.4914, hi 0.7568, unit 469 of 750, outcome BELOW, as printed: 80 to 90 percent, not including 90 750 469 84.9 62.5 59.0 to 65.9 49.1 to 75.7 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0044, unit 62 of 31,848, outcome CONSISTENT, as printed: 62 of 31,848 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3109, lo 0.2425, hi 0.386, unit 5,579 of 17,942, outcome BELOW, as printed: every magnitude, every window 17,942 5,579 41.9 31.1 30.4 to 31.8 24.2 to 38.6 below 77
row-record quake.prob10.m3: value 0.3028, lo 0.2303, hi 0.3832, unit 3,795 of 12,532, outcome BELOW, as printed: M3 and above 12,532 3,795 44.6 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3298, lo 0.2443, hi 0.419, unit 1,784 of 5,410, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,410 1,784 35.6 33.0 31.7 to 34.2 24.4 to 41.9 cannot tell 52
row-record quake.prob10.day: value 0.2381, lo 0.139, hi 0.3388, unit 336 of 1,411, outcome BELOW, as printed: every magnitude, 1 day 1,411 336 36.1 23.8 21.7 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2099, lo 0.13, hi 0.3092, unit 863 of 4,111, outcome BELOW, as printed: every magnitude, 1 week 4,111 863 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2369, lo 0.1638, hi 0.3263, unit 1,721 of 7,265, outcome BELOW, as printed: every magnitude, 1 month 7,265 1,721 39.6 23.7 22.7 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.5158, lo 0.4214, hi 0.6039, unit 2,659 of 5,155, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,155 2,659 50.7 51.6 50.2 to 52.9 42.1 to 60.4 cannot tell 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-11 20:19 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-12T01:17:33Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-12T01:17:33Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-12T01:17:33Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9776, unit 30,655 of 31,853, outcome CANNOT_TELL, as printed: M3 and above, every window 31,853 30,655 756 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell 82 12,713
row-record quake.cover.m4: value 0.9858, lo 0.979, hi 0.9941, unit 31,281 of 31,733, outcome ABOVE, as printed: M4 and above 31,733 31,281 446 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,753
row-record quake.cover.m5: value 0.9965, lo 0.9936, hi 0.9987, unit 31,743 of 31,853, outcome ABOVE, as printed: M5 and above 31,853 31,743 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,244
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,848 of 31,853, outcome ABOVE, as printed: M6 and above 31,853 31,848 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,402
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,852 of 31,853, outcome ABOVE, as printed: M7 and above 31,853 31,852 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,739
row-record quake.cover.m3.day: value 0.9888, lo 0.9805, hi 0.9938, unit 9,606 of 9,715, outcome ABOVE, as printed: M3 and above, 1 day 9,715 9,606 51 58 98.9 98.7 to 99.1 98.0 to 99.4 above 82 7,038
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,354 of 9,599, outcome ABOVE, as printed: M3 and above, 1 week 9,599 9,354 136 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,703
row-record quake.cover.m3.month: value 0.9586, lo 0.9391, hi 0.9756, unit 8,773 of 9,152, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,152 8,773 230 149 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell 77 1,767
row-record quake.cover.m3.year: value 0.8627, lo 0.7897, hi 0.9409, unit 2,922 of 3,387, outcome BELOW, as printed: M3 and above, 1 year 3,387 2,922 339 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 205
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,455 of 159,221, outcome ABOVE, as printed: every magnitude, every window 159,221 157,455 1,317 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,911
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 302 of 117,523, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,523 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0333, lo 0.0165, hi 0.0487, unit 579 of 17,378, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,378 579 2.4 3.3 3.1 to 3.6 1.7 to 4.9 cannot tell 82
row-record quake.prob.5_10: value 0.0679, lo 0.046, hi 0.0915, unit 433 of 6,376, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,376 433 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1053, lo 0.0741, hi 0.1362, unit 595 of 5,653, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,653 595 14.4 10.5 9.8 to 11.3 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1923, lo 0.1504, hi 0.2359, unit 944 of 4,910, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,910 944 28.5 19.2 18.1 to 20.3 15.0 to 23.6 below 74
row-record quake.prob.40_60: value 0.3372, lo 0.2637, hi 0.4098, unit 907 of 2,690, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,690 907 49.3 33.7 32.0 to 35.5 26.4 to 41.0 below 58
row-record quake.prob.60_80: value 0.4275, lo 0.304, hi 0.5609, unit 796 of 1,862, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,862 796 69.5 42.8 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.6253, lo 0.4914, hi 0.7568, unit 469 of 750, outcome BELOW, as printed: 80 to 90 percent, not including 90 750 469 84.9 62.5 59.0 to 65.9 49.1 to 75.7 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0044, unit 62 of 31,853, outcome CONSISTENT, as printed: 62 of 31,853 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3109, lo 0.2425, hi 0.386, unit 5,579 of 17,944, outcome BELOW, as printed: every magnitude, every window 17,944 5,579 41.9 31.1 30.4 to 31.8 24.2 to 38.6 below 77
row-record quake.prob10.m3: value 0.3028, lo 0.2303, hi 0.3831, unit 3,795 of 12,534, outcome BELOW, as printed: M3 and above 12,534 3,795 44.5 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3298, lo 0.2443, hi 0.419, unit 1,784 of 5,410, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,410 1,784 35.6 33.0 31.7 to 34.2 24.4 to 41.9 cannot tell 52
row-record quake.prob10.day: value 0.238, lo 0.1389, hi 0.3388, unit 336 of 1,412, outcome BELOW, as printed: every magnitude, 1 day 1,412 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2099, lo 0.13, hi 0.3092, unit 863 of 4,111, outcome BELOW, as printed: every magnitude, 1 week 4,111 863 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2369, lo 0.1638, hi 0.3263, unit 1,721 of 7,266, outcome BELOW, as printed: every magnitude, 1 month 7,266 1,721 39.6 23.7 22.7 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.5158, lo 0.4214, hi 0.6039, unit 2,659 of 5,155, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,155 2,659 50.7 51.6 50.2 to 52.9 42.1 to 60.4 cannot tell 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-12 01:52 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-12T05:43:09Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-12T05:43:09Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-12T05:43:09Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9775, unit 30,662 of 31,861, outcome CANNOT_TELL, as printed: M3 and above, every window 31,861 30,662 757 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell 82 12,718
row-record quake.cover.m4: value 0.9857, lo 0.9789, hi 0.9939, unit 31,287 of 31,741, outcome ABOVE, as printed: M4 and above 31,741 31,287 448 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,758
row-record quake.cover.m5: value 0.9965, lo 0.9936, hi 0.9987, unit 31,751 of 31,861, outcome ABOVE, as printed: M5 and above 31,861 31,751 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,252
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,856 of 31,861, outcome ABOVE, as printed: M6 and above 31,861 31,856 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,410
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,860 of 31,861, outcome ABOVE, as printed: M7 and above 31,861 31,860 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,747
row-record quake.cover.m3.day: value 0.9887, lo 0.9803, hi 0.9937, unit 9,607 of 9,717, outcome ABOVE, as printed: M3 and above, 1 day 9,717 9,607 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,040
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,355 of 9,600, outcome ABOVE, as printed: M3 and above, 1 week 9,600 9,355 136 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,704
row-record quake.cover.m3.month: value 0.9586, lo 0.9392, hi 0.9756, unit 8,778 of 9,157, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,157 8,778 230 149 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell 77 1,769
row-record quake.cover.m3.year: value 0.8627, lo 0.7897, hi 0.9409, unit 2,922 of 3,387, outcome BELOW, as printed: M3 and above, 1 year 3,387 2,922 339 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 205
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,492 of 159,261, outcome ABOVE, as printed: every magnitude, every window 159,261 157,492 1,320 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,945
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 303 of 117,555, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,555 303 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0336, lo 0.0169, hi 0.0487, unit 584 of 17,381, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,381 584 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell 82
row-record quake.prob.5_10: value 0.0681, lo 0.0463, hi 0.0916, unit 434 of 6,377, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,377 434 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1052, lo 0.0741, hi 0.1362, unit 595 of 5,654, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,654 595 14.4 10.5 9.8 to 11.3 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1928, lo 0.151, hi 0.2364, unit 947 of 4,911, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,911 947 28.5 19.3 18.2 to 20.4 15.1 to 23.6 below 74
row-record quake.prob.40_60: value 0.337, lo 0.2637, hi 0.4095, unit 907 of 2,691, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,691 907 49.3 33.7 31.9 to 35.5 26.4 to 40.9 below 58
row-record quake.prob.60_80: value 0.4273, lo 0.3037, hi 0.5606, unit 796 of 1,863, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,863 796 69.5 42.7 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.6253, lo 0.4914, hi 0.7568, unit 469 of 750, outcome BELOW, as printed: 80 to 90 percent, not including 90 750 469 84.9 62.5 59.0 to 65.9 49.1 to 75.7 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0044, unit 62 of 31,861, outcome CONSISTENT, as printed: 62 of 31,861 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.311, lo 0.2425, hi 0.3861, unit 5,582 of 17,948, outcome BELOW, as printed: every magnitude, every window 17,948 5,582 41.9 31.1 30.4 to 31.8 24.2 to 38.6 below 77
row-record quake.prob10.m3: value 0.3029, lo 0.2302, hi 0.3833, unit 3,798 of 12,537, outcome BELOW, as printed: M3 and above 12,537 3,798 44.5 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3297, lo 0.2443, hi 0.4189, unit 1,784 of 5,411, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,411 1,784 35.6 33.0 31.7 to 34.2 24.4 to 41.9 cannot tell 52
row-record quake.prob10.day: value 0.238, lo 0.1389, hi 0.3388, unit 336 of 1,412, outcome BELOW, as printed: every magnitude, 1 day 1,412 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2099, lo 0.13, hi 0.3092, unit 863 of 4,111, outcome BELOW, as printed: every magnitude, 1 week 4,111 863 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2371, lo 0.1643, hi 0.3265, unit 1,724 of 7,270, outcome BELOW, as printed: every magnitude, 1 month 7,270 1,724 39.6 23.7 22.8 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.5158, lo 0.4214, hi 0.6039, unit 2,659 of 5,155, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,155 2,659 50.7 51.6 50.2 to 52.9 42.1 to 60.4 cannot tell 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-12 05:17 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-12T07:53:55Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-12T07:53:55Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-12T07:53:55Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9775, unit 30,664 of 31,863, outcome CANNOT_TELL, as printed: M3 and above, every window 31,863 30,664 757 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell 82 12,719
row-record quake.cover.m4: value 0.9857, lo 0.9789, hi 0.9939, unit 31,289 of 31,743, outcome ABOVE, as printed: M4 and above 31,743 31,289 448 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,760
row-record quake.cover.m5: value 0.9965, lo 0.9936, hi 0.9987, unit 31,753 of 31,863, outcome ABOVE, as printed: M5 and above 31,863 31,753 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,254
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,858 of 31,863, outcome ABOVE, as printed: M6 and above 31,863 31,858 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,412
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,862 of 31,863, outcome ABOVE, as printed: M7 and above 31,863 31,862 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,749
row-record quake.cover.m3.day: value 0.9887, lo 0.9803, hi 0.9937, unit 9,608 of 9,718, outcome ABOVE, as printed: M3 and above, 1 day 9,718 9,608 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,041
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,356 of 9,601, outcome ABOVE, as printed: M3 and above, 1 week 9,601 9,356 136 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,704
row-record quake.cover.m3.month: value 0.9586, lo 0.9392, hi 0.9756, unit 8,778 of 9,157, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,157 8,778 230 149 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell 77 1,769
row-record quake.cover.m3.year: value 0.8627, lo 0.7897, hi 0.9409, unit 2,922 of 3,387, outcome BELOW, as printed: M3 and above, 1 year 3,387 2,922 339 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 205
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,502 of 159,271, outcome ABOVE, as printed: every magnitude, every window 159,271 157,502 1,320 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,954
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 303 of 117,564, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,564 303 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0336, lo 0.0169, hi 0.0487, unit 584 of 17,381, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,381 584 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell 82
row-record quake.prob.5_10: value 0.068, lo 0.0463, hi 0.0916, unit 434 of 6,378, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,378 434 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1052, lo 0.0741, hi 0.1362, unit 595 of 5,654, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,654 595 14.4 10.5 9.8 to 11.3 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1928, lo 0.151, hi 0.2364, unit 947 of 4,911, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,911 947 28.5 19.3 18.2 to 20.4 15.1 to 23.6 below 74
row-record quake.prob.40_60: value 0.337, lo 0.2637, hi 0.4095, unit 907 of 2,691, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,691 907 49.3 33.7 31.9 to 35.5 26.4 to 40.9 below 58
row-record quake.prob.60_80: value 0.4273, lo 0.3037, hi 0.5606, unit 796 of 1,863, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,863 796 69.5 42.7 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.6253, lo 0.4914, hi 0.7568, unit 469 of 750, outcome BELOW, as printed: 80 to 90 percent, not including 90 750 469 84.9 62.5 59.0 to 65.9 49.1 to 75.7 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0044, unit 62 of 31,863, outcome CONSISTENT, as printed: 62 of 31,863 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.311, lo 0.2425, hi 0.3861, unit 5,582 of 17,948, outcome BELOW, as printed: every magnitude, every window 17,948 5,582 41.9 31.1 30.4 to 31.8 24.2 to 38.6 below 77
row-record quake.prob10.m3: value 0.3029, lo 0.2302, hi 0.3833, unit 3,798 of 12,537, outcome BELOW, as printed: M3 and above 12,537 3,798 44.5 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3297, lo 0.2443, hi 0.4189, unit 1,784 of 5,411, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,411 1,784 35.6 33.0 31.7 to 34.2 24.4 to 41.9 cannot tell 52
row-record quake.prob10.day: value 0.238, lo 0.1389, hi 0.3388, unit 336 of 1,412, outcome BELOW, as printed: every magnitude, 1 day 1,412 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2099, lo 0.13, hi 0.3092, unit 863 of 4,111, outcome BELOW, as printed: every magnitude, 1 week 4,111 863 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2371, lo 0.1643, hi 0.3265, unit 1,724 of 7,270, outcome BELOW, as printed: every magnitude, 1 month 7,270 1,724 39.6 23.7 22.8 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.5158, lo 0.4214, hi 0.6039, unit 2,659 of 5,155, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,155 2,659 50.7 51.6 50.2 to 52.9 42.1 to 60.4 cannot tell 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-12 05:36 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-12T10:24:43Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-12T10:24:43Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-12T10:24:43Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9776, unit 30,673 of 31,872, outcome CANNOT_TELL, as printed: M3 and above, every window 31,872 30,673 757 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell 82 12,725
row-record quake.cover.m4: value 0.9857, lo 0.9789, hi 0.9939, unit 31,298 of 31,752, outcome ABOVE, as printed: M4 and above 31,752 31,298 448 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,766
row-record quake.cover.m5: value 0.9965, lo 0.9936, hi 0.9987, unit 31,762 of 31,872, outcome ABOVE, as printed: M5 and above 31,872 31,762 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,262
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,867 of 31,872, outcome ABOVE, as printed: M6 and above 31,872 31,867 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,421
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,871 of 31,872, outcome ABOVE, as printed: M7 and above 31,872 31,871 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,758
row-record quake.cover.m3.day: value 0.9887, lo 0.9803, hi 0.9937, unit 9,611 of 9,721, outcome ABOVE, as printed: M3 and above, 1 day 9,721 9,611 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,044
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,359 of 9,604, outcome ABOVE, as printed: M3 and above, 1 week 9,604 9,359 136 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,707
row-record quake.cover.m3.month: value 0.9586, lo 0.9392, hi 0.9756, unit 8,780 of 9,159, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,159 8,780 230 149 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell 77 1,769
row-record quake.cover.m3.year: value 0.8628, lo 0.7897, hi 0.9409, unit 2,923 of 3,388, outcome BELOW, as printed: M3 and above, 1 year 3,388 2,923 339 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 205
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,547 of 159,316, outcome ABOVE, as printed: every magnitude, every window 159,316 157,547 1,320 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,992
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 303 of 117,600, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,600 303 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0336, lo 0.017, hi 0.0487, unit 585 of 17,386, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,386 585 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell 82
row-record quake.prob.5_10: value 0.068, lo 0.0463, hi 0.0916, unit 434 of 6,378, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,378 434 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1052, lo 0.0741, hi 0.1362, unit 595 of 5,654, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,654 595 14.4 10.5 9.8 to 11.3 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1929, lo 0.1511, hi 0.2363, unit 948 of 4,914, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,914 948 28.5 19.3 18.2 to 20.4 15.1 to 23.6 below 74
row-record quake.prob.40_60: value 0.337, lo 0.2637, hi 0.4095, unit 907 of 2,691, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,691 907 49.3 33.7 31.9 to 35.5 26.4 to 40.9 below 58
row-record quake.prob.60_80: value 0.4276, lo 0.3048, hi 0.5606, unit 797 of 1,864, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,864 797 69.5 42.8 40.5 to 45.0 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.6253, lo 0.4914, hi 0.7568, unit 469 of 750, outcome BELOW, as printed: 80 to 90 percent, not including 90 750 469 84.9 62.5 59.0 to 65.9 49.1 to 75.7 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,872, outcome CONSISTENT, as printed: 63 of 31,872 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3111, lo 0.2426, hi 0.3861, unit 5,584 of 17,952, outcome BELOW, as printed: every magnitude, every window 17,952 5,584 41.9 31.1 30.4 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.303, lo 0.2303, hi 0.3831, unit 3,799 of 12,540, outcome BELOW, as printed: M3 and above 12,540 3,799 44.5 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3298, lo 0.2444, hi 0.4189, unit 1,785 of 5,412, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,412 1,785 35.6 33.0 31.7 to 34.2 24.4 to 41.9 cannot tell 52
row-record quake.prob10.day: value 0.238, lo 0.1389, hi 0.3388, unit 336 of 1,412, outcome BELOW, as printed: every magnitude, 1 day 1,412 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2099, lo 0.13, hi 0.3092, unit 863 of 4,111, outcome BELOW, as printed: every magnitude, 1 week 4,111 863 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2371, lo 0.1642, hi 0.3264, unit 1,724 of 7,272, outcome BELOW, as printed: every magnitude, 1 month 7,272 1,724 39.6 23.7 22.7 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.516, lo 0.4217, hi 0.604, unit 2,661 of 5,157, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,157 2,661 50.7 51.6 50.2 to 53.0 42.2 to 60.4 cannot tell 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-12 07:54 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-12T12:30:40Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-12T12:30:40Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-12T12:30:40Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9776, unit 30,683 of 31,883, outcome CANNOT_TELL, as printed: M3 and above, every window 31,883 30,683 758 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell 82 12,729
row-record quake.cover.m4: value 0.9857, lo 0.9789, hi 0.9939, unit 31,309 of 31,763, outcome ABOVE, as printed: M4 and above 31,763 31,309 448 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,775
row-record quake.cover.m5: value 0.9965, lo 0.9936, hi 0.9987, unit 31,773 of 31,883, outcome ABOVE, as printed: M5 and above 31,883 31,773 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,273
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,878 of 31,883, outcome ABOVE, as printed: M6 and above 31,883 31,878 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,432
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,882 of 31,883, outcome ABOVE, as printed: M7 and above 31,883 31,882 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,769
row-record quake.cover.m3.day: value 0.9887, lo 0.9803, hi 0.9937, unit 9,611 of 9,721, outcome ABOVE, as printed: M3 and above, 1 day 9,721 9,611 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,044
row-record quake.cover.m3.week: value 0.9745, lo 0.9599, hi 0.984, unit 9,366 of 9,611, outcome ABOVE, as printed: M3 and above, 1 week 9,611 9,366 136 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,709
row-record quake.cover.m3.month: value 0.9586, lo 0.9392, hi 0.9756, unit 8,783 of 9,162, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,162 8,783 230 149 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell 77 1,770
row-record quake.cover.m3.year: value 0.8625, lo 0.7893, hi 0.9409, unit 2,923 of 3,389, outcome BELOW, as printed: M3 and above, 1 year 3,389 2,923 340 126 86.2 85.0 to 87.4 78.9 to 94.1 below 42 206
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,601 of 159,371, outcome ABOVE, as printed: every magnitude, every window 159,371 157,601 1,321 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,038
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 303 of 117,640, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,640 303 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0337, lo 0.017, hi 0.0488, unit 586 of 17,394, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,394 586 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell 82
row-record quake.prob.5_10: value 0.0682, lo 0.0464, hi 0.0916, unit 435 of 6,381, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,381 435 7.1 6.8 6.2 to 7.5 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1054, lo 0.0741, hi 0.1362, unit 596 of 5,656, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,656 596 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1929, lo 0.1511, hi 0.2363, unit 948 of 4,914, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,914 948 28.5 19.3 18.2 to 20.4 15.1 to 23.6 below 74
row-record quake.prob.40_60: value 0.3373, lo 0.2637, hi 0.4098, unit 908 of 2,692, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,692 908 49.3 33.7 32.0 to 35.5 26.4 to 41.0 below 58
row-record quake.prob.60_80: value 0.4279, lo 0.3048, hi 0.5611, unit 798 of 1,865, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,865 798 69.5 42.8 40.6 to 45.1 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.6253, lo 0.4914, hi 0.7568, unit 469 of 750, outcome BELOW, as printed: 80 to 90 percent, not including 90 750 469 84.9 62.5 59.0 to 65.9 49.1 to 75.7 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,883, outcome CONSISTENT, as printed: 63 of 31,883 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3111, lo 0.2426, hi 0.3862, unit 5,587 of 17,956, outcome BELOW, as printed: every magnitude, every window 17,956 5,587 41.9 31.1 30.4 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.303, lo 0.2304, hi 0.3832, unit 3,801 of 12,543, outcome BELOW, as printed: M3 and above 12,543 3,801 44.5 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3299, lo 0.2448, hi 0.4189, unit 1,786 of 5,413, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,413 1,786 35.6 33.0 31.8 to 34.3 24.5 to 41.9 cannot tell 52
row-record quake.prob10.day: value 0.238, lo 0.1389, hi 0.3388, unit 336 of 1,412, outcome BELOW, as printed: every magnitude, 1 day 1,412 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2103, lo 0.1303, hi 0.3092, unit 865 of 4,114, outcome BELOW, as printed: every magnitude, 1 week 4,114 865 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2372, lo 0.1643, hi 0.3265, unit 1,725 of 7,273, outcome BELOW, as printed: every magnitude, 1 month 7,273 1,725 39.6 23.7 22.8 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.516, lo 0.4217, hi 0.604, unit 2,661 of 5,157, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,157 2,661 50.7 51.6 50.2 to 53.0 42.2 to 60.4 cannot tell 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-12 10:21 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-12T15:20:24Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-12T15:20:24Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-12T15:20:24Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9776, unit 30,694 of 31,894, outcome CANNOT_TELL, as printed: M3 and above, every window 31,894 30,694 758 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,735
row-record quake.cover.m4: value 0.9857, lo 0.9789, hi 0.9939, unit 31,319 of 31,774, outcome ABOVE, as printed: M4 and above 31,774 31,319 449 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,783
row-record quake.cover.m5: value 0.9966, lo 0.9936, hi 0.9987, unit 31,784 of 31,894, outcome ABOVE, as printed: M5 and above 31,894 31,784 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,283
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,889 of 31,894, outcome ABOVE, as printed: M6 and above 31,894 31,889 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,443
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,893 of 31,894, outcome ABOVE, as printed: M7 and above 31,894 31,893 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,780
row-record quake.cover.m3.day: value 0.9887, lo 0.9803, hi 0.9937, unit 9,615 of 9,725, outcome ABOVE, as printed: M3 and above, 1 day 9,725 9,615 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,048
row-record quake.cover.m3.week: value 0.9745, lo 0.9599, hi 0.984, unit 9,368 of 9,613, outcome ABOVE, as printed: M3 and above, 1 week 9,613 9,368 136 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,710
row-record quake.cover.m3.month: value 0.9586, lo 0.9392, hi 0.9756, unit 8,785 of 9,164, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,164 8,785 230 149 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,770
row-record quake.cover.m3.year: value 0.8626, lo 0.7895, hi 0.9409, unit 2,926 of 3,392, outcome BELOW, as printed: M3 and above, 1 year 3,392 2,926 340 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 207
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,655 of 159,426, outcome ABOVE, as printed: every magnitude, every window 159,426 157,655 1,322 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,084
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 303 of 117,680, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,680 303 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0337, lo 0.017, hi 0.0488, unit 586 of 17,402, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,402 586 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0683, lo 0.0465, hi 0.0917, unit 436 of 6,382, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,382 436 7.1 6.8 6.2 to 7.5 4.7 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1053, lo 0.0741, hi 0.1362, unit 596 of 5,658, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,658 596 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1928, lo 0.151, hi 0.2363, unit 948 of 4,916, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,916 948 28.5 19.3 18.2 to 20.4 15.1 to 23.6 below 74
row-record quake.prob.40_60: value 0.3375, lo 0.2644, hi 0.4104, unit 909 of 2,693, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,693 909 49.3 33.8 32.0 to 35.6 26.4 to 41.0 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3043, hi 0.5611, unit 798 of 1,866, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,866 798 69.5 42.8 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.6253, lo 0.4914, hi 0.7568, unit 469 of 750, outcome BELOW, as printed: 80 to 90 percent, not including 90 750 469 84.9 62.5 59.0 to 65.9 49.1 to 75.7 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,894, outcome CONSISTENT, as printed: 63 of 31,894 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3111, lo 0.2427, hi 0.3862, unit 5,588 of 17,962, outcome BELOW, as printed: every magnitude, every window 17,962 5,588 41.8 31.1 30.4 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.303, lo 0.2303, hi 0.3833, unit 3,802 of 12,548, outcome BELOW, as printed: M3 and above 12,548 3,802 44.5 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3299, lo 0.2448, hi 0.4189, unit 1,786 of 5,414, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,414 1,786 35.6 33.0 31.8 to 34.2 24.5 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.238, lo 0.1389, hi 0.3388, unit 336 of 1,412, outcome BELOW, as printed: every magnitude, 1 day 1,412 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2102, lo 0.1303, hi 0.3092, unit 865 of 4,115, outcome BELOW, as printed: every magnitude, 1 week 4,115 865 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2373, lo 0.1644, hi 0.3267, unit 1,726 of 7,275, outcome BELOW, as printed: every magnitude, 1 month 7,275 1,726 39.6 23.7 22.8 to 24.7 16.4 to 32.7 below 73
row-record quake.prob10.year: value 0.5157, lo 0.4215, hi 0.6036, unit 2,661 of 5,160, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,160 2,661 50.7 51.6 50.2 to 52.9 42.1 to 60.4 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-12 10:22 Faults and Guards 2.0 migration: reason codes, REQ-13 line, edge convention, addendum
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: n/a: no baseline or null is built by this change, PLAN.md is not edited and its seal in data/plan_seal.json still matches, the addendum is a new file committed as 3ad3ea7 before any reading under it
- II: n/a: no repeated item, every cell keeps its own interval and the Wilson and sequence-group bootstrap intervals are unchanged
- III: holds: ABOVE and BELOW stay separate columns, every non-outcome number of summary_quake.json (value, lo, hi, scored, inside, share, intervals) compared equal in every cell before and after the code change, 0 differences
- V: holds: the rule is named in PLAN_ADDENDUM_std2.md before any reading under it, ABOVE and BELOW against the stated figure, CONSISTENT in the tolerance band with closed edges, no new tolerance invented
- VI: holds: four outcomes kept, every CANNOT_TELL carries one closed reason, the headline cell M3 and above reads CANNOT_TELL STRADDLES_EDGE and no cell changed its outcome, the both-alternatives test is not applied because the plan names no size that matters and the addendum says so
- R: holds: counts and reasons are read from summary_quake.json after re-running quake_tick.py --offline, the rule self-test passed and the kit self-test passed, headline M3 and above 30,694 of 31,894 unchanged, 788 rows NO_INTERVAL_FORMABLE for no zone stated, failed reads 45,904 NOTHING_RETURNED apart
- P1: n/a: no quotation of any source in this change
- P2: n/a: no new figure, every number keeps its source on the page
- P3: n/a: no setting labels of any source are touched by this change
- P4: holds: no cause is named, the added text says only which closed reason a CANNOT_TELL carries and what the edges are
- P5: holds: the page note says the interval is the union of the Wilson and the sequence-group interval and states the closed edges and the minimum of 30 rows and 10 groups as TOO_WIDE_TO_RESOLVE
- P6: holds: the headline line is the same sentence as before plus the reason beside cannot tell and the REQ-13 line read from the summary, no stronger than the reading
- P7: holds: no outcome moved so no ledger outcome changed, refresh_page.py run under the ledger lock refreshed the 24 quake.* rows surface text before any release, the owner ships with ship.sh
- P8: cannot tell: quake.html rebuilt by build_page.py and lint_copy.py reported 0 hits, but the page was not rendered in a browser or served because nothing is deployed from this session
- P9: holds: plain sentences without semicolons in the added page text, no count of our own things in any heading, lint_copy.py 0 hits
- P10: holds: the addendum is dated 12 Nov 2026 and written before any reading under the new rule, no rule set after the data

## 2026-11-12 11:46 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-12T16:41:40Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-12T16:41:40Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-12T16:41:40Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9776, unit 30,707 of 31,907, outcome CANNOT_TELL, as printed: M3 and above, every window 31,907 30,707 758 442 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,742
row-record quake.cover.m4: value 0.9857, lo 0.9789, hi 0.9938, unit 31,331 of 31,787, outcome ABOVE, as printed: M4 and above 31,787 31,331 450 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,791
row-record quake.cover.m5: value 0.9966, lo 0.9936, hi 0.9987, unit 31,797 of 31,907, outcome ABOVE, as printed: M5 and above 31,907 31,797 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,295
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,902 of 31,907, outcome ABOVE, as printed: M6 and above 31,907 31,902 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,456
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,906 of 31,907, outcome ABOVE, as printed: M7 and above 31,907 31,906 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,793
row-record quake.cover.m3.day: value 0.9887, lo 0.9803, hi 0.9937, unit 9,619 of 9,729, outcome ABOVE, as printed: M3 and above, 1 day 9,729 9,619 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,052
row-record quake.cover.m3.week: value 0.9745, lo 0.9599, hi 0.984, unit 9,371 of 9,616, outcome ABOVE, as printed: M3 and above, 1 week 9,616 9,371 136 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,712
row-record quake.cover.m3.month: value 0.9587, lo 0.9392, hi 0.9756, unit 8,788 of 9,167, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,167 8,788 230 149 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,771
row-record quake.cover.m3.year: value 0.8627, lo 0.7897, hi 0.941, unit 2,929 of 3,395, outcome BELOW, as printed: M3 and above, 1 year 3,395 2,929 340 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 207
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,719 of 159,491, outcome ABOVE, as printed: every magnitude, every window 159,491 157,719 1,323 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,137
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 303 of 117,731, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,731 303 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0337, lo 0.0171, hi 0.0488, unit 587 of 17,408, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,408 587 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0683, lo 0.0465, hi 0.0917, unit 436 of 6,383, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,383 436 7.1 6.8 6.2 to 7.5 4.7 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1055, lo 0.0741, hi 0.1363, unit 597 of 5,659, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,659 597 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1929, lo 0.151, hi 0.2366, unit 949 of 4,920, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,920 949 28.5 19.3 18.2 to 20.4 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3378, lo 0.2644, hi 0.4109, unit 910 of 2,694, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,694 910 49.3 33.8 32.0 to 35.6 26.4 to 41.1 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3043, hi 0.5611, unit 798 of 1,866, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,866 798 69.5 42.8 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.6245, lo 0.4903, hi 0.7559, unit 469 of 751, outcome BELOW, as printed: 80 to 90 percent, not including 90 751 469 84.9 62.5 58.9 to 65.8 49.0 to 75.6 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,232 of 1,260, outcome BELOW, as printed: 99 to 100 percent 1,260 1,232 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,907, outcome CONSISTENT, as printed: 63 of 31,907 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3111, lo 0.2427, hi 0.3863, unit 5,591 of 17,969, outcome BELOW, as printed: every magnitude, every window 17,969 5,591 41.8 31.1 30.4 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3031, lo 0.2304, hi 0.3833, unit 3,805 of 12,554, outcome BELOW, as printed: M3 and above 12,554 3,805 44.5 30.3 29.5 to 31.1 23.0 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3298, lo 0.2447, hi 0.4189, unit 1,786 of 5,415, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,415 1,786 35.6 33.0 31.7 to 34.2 24.5 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.238, lo 0.1389, hi 0.3388, unit 336 of 1,412, outcome BELOW, as printed: every magnitude, 1 day 1,412 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2102, lo 0.1303, hi 0.3091, unit 865 of 4,116, outcome BELOW, as printed: every magnitude, 1 week 4,116 865 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2373, lo 0.1645, hi 0.3265, unit 1,727 of 7,278, outcome BELOW, as printed: every magnitude, 1 month 7,278 1,727 39.6 23.7 22.8 to 24.7 16.4 to 32.6 below 73
row-record quake.prob10.year: value 0.5158, lo 0.4215, hi 0.6036, unit 2,663 of 5,163, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,163 2,663 50.7 51.6 50.2 to 52.9 42.1 to 60.4 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-12 17:09 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-12T21:00:57Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-12T21:00:57Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-12T21:00:57Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9623, lo 0.9459, hi 0.9775, unit 30,721 of 31,923, outcome CANNOT_TELL, as printed: M3 and above, every window 31,923 30,721 759 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,746
row-record quake.cover.m4: value 0.9857, lo 0.9789, hi 0.9938, unit 31,347 of 31,803, outcome ABOVE, as printed: M4 and above 31,803 31,347 450 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,802
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,813 of 31,923, outcome ABOVE, as printed: M5 and above 31,923 31,813 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,308
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,918 of 31,923, outcome ABOVE, as printed: M6 and above 31,923 31,918 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,470
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,922 of 31,923, outcome ABOVE, as printed: M7 and above 31,923 31,922 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,809
row-record quake.cover.m3.day: value 0.9887, lo 0.9804, hi 0.9937, unit 9,621 of 9,731, outcome ABOVE, as printed: M3 and above, 1 day 9,731 9,621 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,052
row-record quake.cover.m3.week: value 0.9744, lo 0.9598, hi 0.9839, unit 9,377 of 9,623, outcome ABOVE, as printed: M3 and above, 1 week 9,623 9,377 137 109 97.4 97.1 to 97.7 96.0 to 98.4 above 82 3,715
row-record quake.cover.m3.month: value 0.9586, lo 0.9392, hi 0.9756, unit 8,791 of 9,171, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,171 8,791 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,772
row-record quake.cover.m3.year: value 0.8629, lo 0.7898, hi 0.9411, unit 2,932 of 3,398, outcome BELOW, as printed: M3 and above, 1 year 3,398 2,932 340 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 207
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,797 of 159,571, outcome ABOVE, as printed: every magnitude, every window 159,571 157,797 1,324 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,195
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 304 of 117,786, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,786 304 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0337, lo 0.0171, hi 0.0488, unit 587 of 17,417, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,417 587 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0683, lo 0.0465, hi 0.0917, unit 436 of 6,388, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,388 436 7.1 6.8 6.2 to 7.5 4.7 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1055, lo 0.0741, hi 0.1363, unit 597 of 5,660, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,660 597 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.193, lo 0.1512, hi 0.2366, unit 950 of 4,922, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,922 950 28.5 19.3 18.2 to 20.4 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3379, lo 0.2646, hi 0.4109, unit 911 of 2,696, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,696 911 49.3 33.8 32.0 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.428, lo 0.3045, hi 0.5613, unit 799 of 1,867, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,867 799 69.5 42.8 40.6 to 45.1 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,236 of 1,264, outcome BELOW, as printed: 99 to 100 percent 1,264 1,236 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,923, outcome CONSISTENT, as printed: 63 of 31,923 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3114, lo 0.2429, hi 0.3864, unit 5,599 of 17,980, outcome BELOW, as printed: every magnitude, every window 17,980 5,599 41.9 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3033, lo 0.2306, hi 0.3836, unit 3,809 of 12,559, outcome BELOW, as printed: M3 and above 12,559 3,809 44.6 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3302, lo 0.2447, hi 0.4194, unit 1,790 of 5,421, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,421 1,790 35.6 33.0 31.8 to 34.3 24.5 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.238, lo 0.1389, hi 0.3388, unit 336 of 1,412, outcome BELOW, as printed: every magnitude, 1 day 1,412 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2103, lo 0.1303, hi 0.3091, unit 866 of 4,117, outcome BELOW, as printed: every magnitude, 1 week 4,117 866 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2376, lo 0.1647, hi 0.3268, unit 1,730 of 7,282, outcome BELOW, as printed: every magnitude, 1 month 7,282 1,730 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.516, lo 0.4217, hi 0.6037, unit 2,667 of 5,169, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,169 2,667 50.7 51.6 50.2 to 53.0 42.2 to 60.4 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9287, lo 0.8814, hi 0.9563, unit 664 of 715, outcome CANNOT_TELL, as printed: 664 of 715 inside, 92.9 percent, with a sequence interval of 88.1 to 95.6 percent.

## 2026-11-12 21:19 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-13T01:15:54Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-13T01:15:54Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-13T01:15:54Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,732 of 31,933, outcome CANNOT_TELL, as printed: M3 and above, every window 31,933 30,732 758 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,749
row-record quake.cover.m4: value 0.9857, lo 0.9789, hi 0.9938, unit 31,357 of 31,813, outcome ABOVE, as printed: M4 and above 31,813 31,357 450 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,810
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,823 of 31,933, outcome ABOVE, as printed: M5 and above 31,933 31,823 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,318
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,928 of 31,933, outcome ABOVE, as printed: M6 and above 31,933 31,928 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,480
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,932 of 31,933, outcome ABOVE, as printed: M7 and above 31,933 31,932 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,819
row-record quake.cover.m3.day: value 0.9887, lo 0.9804, hi 0.9937, unit 9,624 of 9,734, outcome ABOVE, as printed: M3 and above, 1 day 9,734 9,624 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,054
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.9841, unit 9,381 of 9,626, outcome ABOVE, as printed: M3 and above, 1 week 9,626 9,381 136 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,716
row-record quake.cover.m3.month: value 0.9586, lo 0.9392, hi 0.9756, unit 8,795 of 9,175, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,175 8,795 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,772
row-record quake.cover.m3.year: value 0.8629, lo 0.7898, hi 0.9411, unit 2,932 of 3,398, outcome BELOW, as printed: M3 and above, 1 year 3,398 2,932 340 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 207
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,848 of 159,621, outcome ABOVE, as printed: every magnitude, every window 159,621 157,848 1,323 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,236
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 304 of 117,825, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,825 304 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0336, lo 0.0169, hi 0.0487, unit 586 of 17,421, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,421 586 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0679, lo 0.0459, hi 0.0914, unit 434 of 6,391, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,391 434 7.1 6.8 6.2 to 7.4 4.6 to 9.1 consistent 80
row-record quake.prob.10_20: value 0.1054, lo 0.0741, hi 0.1363, unit 597 of 5,663, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,663 597 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.193, lo 0.1512, hi 0.2366, unit 950 of 4,922, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,922 950 28.5 19.3 18.2 to 20.4 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3379, lo 0.2646, hi 0.4109, unit 911 of 2,696, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,696 911 49.3 33.8 32.0 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3043, hi 0.5611, unit 799 of 1,868, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,868 799 69.5 42.8 40.6 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,236 of 1,264, outcome BELOW, as printed: 99 to 100 percent 1,264 1,236 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 31,933, outcome CONSISTENT, as printed: 63 of 31,933 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3113, lo 0.2429, hi 0.3864, unit 5,599 of 17,984, outcome BELOW, as printed: every magnitude, every window 17,984 5,599 41.9 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3032, lo 0.2305, hi 0.3835, unit 3,809 of 12,562, outcome BELOW, as printed: M3 and above 12,562 3,809 44.6 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2447, hi 0.4194, unit 1,790 of 5,422, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,422 1,790 35.6 33.0 31.8 to 34.3 24.5 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2378, lo 0.1388, hi 0.3388, unit 336 of 1,413, outcome BELOW, as printed: every magnitude, 1 day 1,413 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2102, lo 0.1302, hi 0.3091, unit 866 of 4,119, outcome BELOW, as printed: every magnitude, 1 week 4,119 866 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2375, lo 0.1647, hi 0.3268, unit 1,730 of 7,283, outcome BELOW, as printed: every magnitude, 1 month 7,283 1,730 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.516, lo 0.4217, hi 0.6037, unit 2,667 of 5,169, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,169 2,667 50.7 51.6 50.2 to 53.0 42.2 to 60.4 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9289, lo 0.8816, hi 0.9565, unit 666 of 717, outcome CANNOT_TELL, as printed: 666 of 717 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-13 00:38 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-13T03:25:42Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-13T03:25:42Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-13T03:25:42Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9776, unit 30,736 of 31,938, outcome CANNOT_TELL, as printed: M3 and above, every window 31,938 30,736 759 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,752
row-record quake.cover.m4: value 0.9856, lo 0.9789, hi 0.9938, unit 31,361 of 31,818, outcome ABOVE, as printed: M4 and above 31,818 31,361 451 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,814
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,828 of 31,938, outcome ABOVE, as printed: M5 and above 31,938 31,828 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,323
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,933 of 31,938, outcome ABOVE, as printed: M6 and above 31,938 31,933 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,485
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,937 of 31,938, outcome ABOVE, as printed: M7 and above 31,938 31,937 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,824
row-record quake.cover.m3.day: value 0.9887, lo 0.9804, hi 0.9937, unit 9,625 of 9,735, outcome ABOVE, as printed: M3 and above, 1 day 9,735 9,625 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,055
row-record quake.cover.m3.week: value 0.9746, lo 0.9598, hi 0.9841, unit 9,382 of 9,627, outcome ABOVE, as printed: M3 and above, 1 week 9,627 9,382 136 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,717
row-record quake.cover.m3.month: value 0.9586, lo 0.9392, hi 0.9756, unit 8,797 of 9,177, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,177 8,797 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,773
row-record quake.cover.m3.year: value 0.8626, lo 0.7894, hi 0.9409, unit 2,932 of 3,399, outcome BELOW, as printed: M3 and above, 1 year 3,399 2,932 341 126 86.3 85.1 to 87.4 78.9 to 94.1 below 42 207
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,871 of 159,646, outcome ABOVE, as printed: every magnitude, every window 159,646 157,871 1,325 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,258
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 304 of 117,846, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,846 304 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0336, lo 0.0169, hi 0.0487, unit 586 of 17,422, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,422 586 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.068, lo 0.0459, hi 0.092, unit 435 of 6,393, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,393 435 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1054, lo 0.0741, hi 0.1363, unit 597 of 5,663, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,663 597 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.193, lo 0.1512, hi 0.2366, unit 950 of 4,922, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,922 950 28.5 19.3 18.2 to 20.4 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3382, lo 0.2649, hi 0.4112, unit 912 of 2,697, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,697 912 49.3 33.8 32.0 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3043, hi 0.5611, unit 799 of 1,868, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,868 799 69.5 42.8 40.6 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,236 of 1,264, outcome BELOW, as printed: 99 to 100 percent 1,264 1,236 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 31,938, outcome CONSISTENT, as printed: 63 of 31,938 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3114, lo 0.2429, hi 0.3864, unit 5,600 of 17,985, outcome BELOW, as printed: every magnitude, every window 17,985 5,600 41.9 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3033, lo 0.2306, hi 0.3835, unit 3,810 of 12,563, outcome BELOW, as printed: M3 and above 12,563 3,810 44.6 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2447, hi 0.4194, unit 1,790 of 5,422, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,422 1,790 35.6 33.0 31.8 to 34.3 24.5 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2378, lo 0.1388, hi 0.3388, unit 336 of 1,413, outcome BELOW, as printed: every magnitude, 1 day 1,413 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2102, lo 0.1302, hi 0.3091, unit 866 of 4,119, outcome BELOW, as printed: every magnitude, 1 week 4,119 866 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2375, lo 0.1647, hi 0.3268, unit 1,730 of 7,283, outcome BELOW, as printed: every magnitude, 1 month 7,283 1,730 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5161, lo 0.4219, hi 0.6038, unit 2,668 of 5,170, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,170 2,668 50.7 51.6 50.2 to 53.0 42.2 to 60.4 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9289, lo 0.8816, hi 0.9565, unit 666 of 717, outcome CANNOT_TELL, as printed: 666 of 717 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-13 03:52 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-13T07:43:44Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-13T07:43:44Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-13T07:43:44Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9459, hi 0.9776, unit 30,747 of 31,949, outcome CANNOT_TELL, as printed: M3 and above, every window 31,949 30,747 759 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,757
row-record quake.cover.m4: value 0.9856, lo 0.979, hi 0.9938, unit 31,372 of 31,829, outcome ABOVE, as printed: M4 and above 31,829 31,372 451 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,822
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,839 of 31,949, outcome ABOVE, as printed: M5 and above 31,949 31,839 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,333
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,944 of 31,949, outcome ABOVE, as printed: M6 and above 31,949 31,944 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,496
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,948 of 31,949, outcome ABOVE, as printed: M7 and above 31,949 31,948 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,835
row-record quake.cover.m3.day: value 0.9887, lo 0.9804, hi 0.9937, unit 9,627 of 9,737, outcome ABOVE, as printed: M3 and above, 1 day 9,737 9,627 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,057
row-record quake.cover.m3.week: value 0.9746, lo 0.9598, hi 0.9841, unit 9,384 of 9,629, outcome ABOVE, as printed: M3 and above, 1 week 9,629 9,384 136 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,718
row-record quake.cover.m3.month: value 0.9586, lo 0.9392, hi 0.9756, unit 8,799 of 9,179, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,179 8,799 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,774
row-record quake.cover.m3.year: value 0.8628, lo 0.7896, hi 0.941, unit 2,937 of 3,404, outcome BELOW, as printed: M3 and above, 1 year 3,404 2,937 341 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 208
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,926 of 159,701, outcome ABOVE, as printed: every magnitude, every window 159,701 157,926 1,325 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,303
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 304 of 117,888, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,888 304 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0336, lo 0.0169, hi 0.0487, unit 586 of 17,427, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,427 586 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.068, lo 0.0459, hi 0.0919, unit 435 of 6,397, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,397 435 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1054, lo 0.0741, hi 0.1363, unit 597 of 5,664, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,664 597 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1932, lo 0.1512, hi 0.2366, unit 951 of 4,923, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,923 951 28.5 19.3 18.2 to 20.4 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.338, lo 0.2649, hi 0.4108, unit 912 of 2,698, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,698 912 49.3 33.8 32.0 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4275, lo 0.3043, hi 0.5608, unit 799 of 1,869, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,869 799 69.5 42.8 40.5 to 45.0 30.4 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7766, lo 0.6691, hi 0.8626, unit 636 of 819, outcome BELOW, as printed: 90 to 99 percent, not including 99 819 636 95.2 77.7 74.7 to 80.4 66.9 to 86.3 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,236 of 1,264, outcome BELOW, as printed: 99 to 100 percent 1,264 1,236 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 31,949, outcome CONSISTENT, as printed: 63 of 31,949 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3114, lo 0.2429, hi 0.3863, unit 5,601 of 17,989, outcome BELOW, as printed: every magnitude, every window 17,989 5,601 41.9 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3033, lo 0.2306, hi 0.3835, unit 3,811 of 12,566, outcome BELOW, as printed: M3 and above 12,566 3,811 44.6 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2446, hi 0.4194, unit 1,790 of 5,423, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,423 1,790 35.6 33.0 31.8 to 34.3 24.5 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2378, lo 0.1388, hi 0.3388, unit 336 of 1,413, outcome BELOW, as printed: every magnitude, 1 day 1,413 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2102, lo 0.1302, hi 0.3091, unit 866 of 4,119, outcome BELOW, as printed: every magnitude, 1 week 4,119 866 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2375, lo 0.1647, hi 0.3268, unit 1,730 of 7,283, outcome BELOW, as printed: every magnitude, 1 month 7,283 1,730 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5158, lo 0.4217, hi 0.6035, unit 2,669 of 5,174, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,174 2,669 50.7 51.6 50.2 to 52.9 42.2 to 60.4 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9289, lo 0.8816, hi 0.9565, unit 666 of 717, outcome CANNOT_TELL, as printed: 666 of 717 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-13 08:11 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-13T11:59:38Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-13T11:59:38Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-13T11:59:38Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,760 of 31,963, outcome CANNOT_TELL, as printed: M3 and above, every window 31,963 30,760 760 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,766
row-record quake.cover.m4: value 0.9856, lo 0.979, hi 0.9938, unit 31,385 of 31,843, outcome ABOVE, as printed: M4 and above 31,843 31,385 452 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,834
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,853 of 31,963, outcome ABOVE, as printed: M5 and above 31,963 31,853 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,345
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,958 of 31,963, outcome ABOVE, as printed: M6 and above 31,963 31,958 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,510
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,962 of 31,963, outcome ABOVE, as printed: M7 and above 31,963 31,962 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,849
row-record quake.cover.m3.day: value 0.9887, lo 0.9804, hi 0.9937, unit 9,634 of 9,744, outcome ABOVE, as printed: M3 and above, 1 day 9,744 9,634 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,064
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,388 of 9,634, outcome ABOVE, as printed: M3 and above, 1 week 9,634 9,388 137 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,720
row-record quake.cover.m3.month: value 0.9586, lo 0.9392, hi 0.9756, unit 8,799 of 9,179, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,179 8,799 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,774
row-record quake.cover.m3.year: value 0.8629, lo 0.7898, hi 0.9411, unit 2,939 of 3,406, outcome BELOW, as printed: M3 and above, 1 year 3,406 2,939 341 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 208
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 157,994 of 159,771, outcome ABOVE, as printed: every magnitude, every window 159,771 157,994 1,327 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,364
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 304 of 117,944, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,944 304 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0337, lo 0.0169, hi 0.0487, unit 587 of 17,434, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,434 587 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.068, lo 0.0459, hi 0.0919, unit 435 of 6,397, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,397 435 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1055, lo 0.0741, hi 0.1363, unit 598 of 5,667, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,667 598 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1931, lo 0.1512, hi 0.2365, unit 951 of 4,924, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,924 951 28.5 19.3 18.2 to 20.4 15.1 to 23.6 below 74
row-record quake.prob.40_60: value 0.338, lo 0.2649, hi 0.4108, unit 912 of 2,698, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,698 912 49.3 33.8 32.0 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.427, lo 0.3043, hi 0.5603, unit 799 of 1,871, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,871 799 69.5 42.7 40.5 to 45.0 30.4 to 56.0 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7756, lo 0.6691, hi 0.8613, unit 636 of 820, outcome BELOW, as printed: 90 to 99 percent, not including 99 820 636 95.2 77.6 74.6 to 80.3 66.9 to 86.1 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,236 of 1,264, outcome BELOW, as printed: 99 to 100 percent 1,264 1,236 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 31,963, outcome CONSISTENT, as printed: 63 of 31,963 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3113, lo 0.2428, hi 0.3863, unit 5,602 of 17,996, outcome BELOW, as printed: every magnitude, every window 17,996 5,602 41.9 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3033, lo 0.2305, hi 0.3836, unit 3,812 of 12,570, outcome BELOW, as printed: M3 and above 12,570 3,812 44.6 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3299, lo 0.2445, hi 0.4192, unit 1,790 of 5,426, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,426 1,790 35.6 33.0 31.8 to 34.2 24.4 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2378, lo 0.1388, hi 0.3388, unit 336 of 1,413, outcome BELOW, as printed: every magnitude, 1 day 1,413 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2104, lo 0.1305, hi 0.3088, unit 867 of 4,121, outcome BELOW, as printed: every magnitude, 1 week 4,121 867 36.7 21.0 19.8 to 22.3 13.1 to 30.9 below 73
row-record quake.prob10.month: value 0.2375, lo 0.1647, hi 0.3268, unit 1,730 of 7,283, outcome BELOW, as printed: every magnitude, 1 month 7,283 1,730 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5154, lo 0.4212, hi 0.603, unit 2,669 of 5,179, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,179 2,669 50.7 51.5 50.2 to 52.9 42.1 to 60.3 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.929, lo 0.882, hi 0.9565, unit 667 of 718, outcome CANNOT_TELL, as printed: 667 of 718 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-13 09:16 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-13T14:14:05Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-13T14:14:05Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-13T14:14:05Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,775 of 31,978, outcome CANNOT_TELL, as printed: M3 and above, every window 31,978 30,775 760 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,771
row-record quake.cover.m4: value 0.9855, lo 0.9789, hi 0.9937, unit 31,397 of 31,858, outcome ABOVE, as printed: M4 and above 31,858 31,397 455 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,847
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,868 of 31,978, outcome ABOVE, as printed: M5 and above 31,978 31,868 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,360
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,973 of 31,978, outcome ABOVE, as printed: M6 and above 31,978 31,973 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,525
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,977 of 31,978, outcome ABOVE, as printed: M7 and above 31,978 31,977 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,864
row-record quake.cover.m3.day: value 0.9887, lo 0.9804, hi 0.9937, unit 9,639 of 9,749, outcome ABOVE, as printed: M3 and above, 1 day 9,749 9,639 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,068
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,390 of 9,636, outcome ABOVE, as printed: M3 and above, 1 week 9,636 9,390 137 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,720
row-record quake.cover.m3.month: value 0.9586, lo 0.9393, hi 0.9756, unit 8,804 of 9,184, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,184 8,804 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,775
row-record quake.cover.m3.year: value 0.863, lo 0.79, hi 0.9411, unit 2,942 of 3,409, outcome BELOW, as printed: M3 and above, 1 year 3,409 2,942 341 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 208
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,066 of 159,846, outcome ABOVE, as printed: every magnitude, every window 159,846 158,066 1,330 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,427
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 305 of 118,001, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,001 305 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.0171, hi 0.0488, unit 589 of 17,444, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,444 589 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0462, hi 0.092, unit 436 of 6,400, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,400 436 7.1 6.8 6.2 to 7.5 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1056, lo 0.0745, hi 0.1363, unit 599 of 5,670, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,670 599 14.4 10.6 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1931, lo 0.1512, hi 0.2365, unit 951 of 4,924, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,924 951 28.5 19.3 18.2 to 20.4 15.1 to 23.6 below 74
row-record quake.prob.40_60: value 0.3381, lo 0.2649, hi 0.411, unit 913 of 2,700, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,700 913 49.3 33.8 32.0 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.427, lo 0.3043, hi 0.5603, unit 799 of 1,871, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,871 799 69.5 42.7 40.5 to 45.0 30.4 to 56.0 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7756, lo 0.6691, hi 0.8613, unit 636 of 820, outcome BELOW, as printed: 90 to 99 percent, not including 99 820 636 95.2 77.6 74.6 to 80.3 66.9 to 86.1 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,236 of 1,264, outcome BELOW, as printed: 99 to 100 percent 1,264 1,236 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 31,978, outcome CONSISTENT, as printed: 63 of 31,978 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3113, lo 0.243, hi 0.3862, unit 5,604 of 18,001, outcome BELOW, as printed: every magnitude, every window 18,001 5,604 41.9 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3033, lo 0.2307, hi 0.3835, unit 3,814 of 12,575, outcome BELOW, as printed: M3 and above 12,575 3,814 44.5 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3299, lo 0.2445, hi 0.4192, unit 1,790 of 5,426, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,426 1,790 35.6 33.0 31.8 to 34.2 24.4 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2376, lo 0.1388, hi 0.3385, unit 336 of 1,414, outcome BELOW, as printed: every magnitude, 1 day 1,414 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2104, lo 0.1305, hi 0.3088, unit 867 of 4,121, outcome BELOW, as printed: every magnitude, 1 week 4,121 867 36.7 21.0 19.8 to 22.3 13.1 to 30.9 below 73
row-record quake.prob10.month: value 0.2377, lo 0.165, hi 0.327, unit 1,732 of 7,285, outcome BELOW, as printed: every magnitude, 1 month 7,285 1,732 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5152, lo 0.4212, hi 0.6025, unit 2,669 of 5,181, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,181 2,669 50.7 51.5 50.1 to 52.9 42.1 to 60.2 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9291, lo 0.8824, hi 0.9566, unit 668 of 719, outcome CANNOT_TELL, as printed: 668 of 719 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-13 11:27 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-13T16:19:23Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-13T16:19:23Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-13T16:19:23Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,783 of 31,986, outcome CANNOT_TELL, as printed: M3 and above, every window 31,986 30,783 760 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,773
row-record quake.cover.m4: value 0.9855, lo 0.9789, hi 0.9937, unit 31,405 of 31,866, outcome ABOVE, as printed: M4 and above 31,866 31,405 455 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,854
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,876 of 31,986, outcome ABOVE, as printed: M5 and above 31,986 31,876 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,368
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,981 of 31,986, outcome ABOVE, as printed: M6 and above 31,986 31,981 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,533
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,985 of 31,986, outcome ABOVE, as printed: M7 and above 31,986 31,985 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,872
row-record quake.cover.m3.day: value 0.9887, lo 0.9804, hi 0.9937, unit 9,641 of 9,751, outcome ABOVE, as printed: M3 and above, 1 day 9,751 9,641 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,069
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,390 of 9,636, outcome ABOVE, as printed: M3 and above, 1 week 9,636 9,390 137 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,720
row-record quake.cover.m3.month: value 0.9586, lo 0.9393, hi 0.9756, unit 8,809 of 9,189, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,189 8,809 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,776
row-record quake.cover.m3.year: value 0.863, lo 0.7901, hi 0.9411, unit 2,943 of 3,410, outcome BELOW, as printed: M3 and above, 1 year 3,410 2,943 341 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 208
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,106 of 159,886, outcome ABOVE, as printed: every magnitude, every window 159,886 158,106 1,330 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,460
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 305 of 118,031, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,031 305 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.0171, hi 0.0488, unit 589 of 17,450, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,450 589 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0462, hi 0.092, unit 436 of 6,401, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,401 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1056, lo 0.0745, hi 0.1363, unit 599 of 5,672, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,672 599 14.4 10.6 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1931, lo 0.1512, hi 0.2365, unit 951 of 4,925, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,925 951 28.5 19.3 18.2 to 20.4 15.1 to 23.6 below 74
row-record quake.prob.40_60: value 0.3381, lo 0.2649, hi 0.411, unit 913 of 2,700, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,700 913 49.3 33.8 32.0 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.427, lo 0.3043, hi 0.5603, unit 799 of 1,871, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,871 799 69.5 42.7 40.5 to 45.0 30.4 to 56.0 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7756, lo 0.6691, hi 0.8613, unit 636 of 820, outcome BELOW, as printed: 90 to 99 percent, not including 99 820 636 95.2 77.6 74.6 to 80.3 66.9 to 86.1 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,236 of 1,264, outcome BELOW, as printed: 99 to 100 percent 1,264 1,236 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 31,986, outcome CONSISTENT, as printed: 63 of 31,986 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3113, lo 0.243, hi 0.3862, unit 5,604 of 18,004, outcome BELOW, as printed: every magnitude, every window 18,004 5,604 41.9 31.1 30.4 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3032, lo 0.2307, hi 0.3835, unit 3,814 of 12,578, outcome BELOW, as printed: M3 and above 12,578 3,814 44.5 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3299, lo 0.2445, hi 0.4192, unit 1,790 of 5,426, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,426 1,790 35.6 33.0 31.8 to 34.2 24.4 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2376, lo 0.1388, hi 0.3385, unit 336 of 1,414, outcome BELOW, as printed: every magnitude, 1 day 1,414 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2104, lo 0.1305, hi 0.3088, unit 867 of 4,121, outcome BELOW, as printed: every magnitude, 1 week 4,121 867 36.7 21.0 19.8 to 22.3 13.1 to 30.9 below 73
row-record quake.prob10.month: value 0.2377, lo 0.165, hi 0.3268, unit 1,732 of 7,287, outcome BELOW, as printed: every magnitude, 1 month 7,287 1,732 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5151, lo 0.4212, hi 0.602, unit 2,669 of 5,182, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,182 2,669 50.7 51.5 50.1 to 52.9 42.1 to 60.2 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9291, lo 0.8824, hi 0.9566, unit 668 of 719, outcome CANNOT_TELL, as printed: 668 of 719 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-13 14:08 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-13T18:29:43Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-13T18:29:43Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-13T18:29:43Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,788 of 31,991, outcome CANNOT_TELL, as printed: M3 and above, every window 31,991 30,788 760 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,776
row-record quake.cover.m4: value 0.9855, lo 0.9789, hi 0.9937, unit 31,410 of 31,871, outcome ABOVE, as printed: M4 and above 31,871 31,410 455 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,857
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,881 of 31,991, outcome ABOVE, as printed: M5 and above 31,991 31,881 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,372
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,986 of 31,991, outcome ABOVE, as printed: M6 and above 31,991 31,986 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,538
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,990 of 31,991, outcome ABOVE, as printed: M7 and above 31,991 31,990 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,877
row-record quake.cover.m3.day: value 0.9887, lo 0.9804, hi 0.9937, unit 9,643 of 9,753, outcome ABOVE, as printed: M3 and above, 1 day 9,753 9,643 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,071
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,391 of 9,637, outcome ABOVE, as printed: M3 and above, 1 week 9,637 9,391 137 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,721
row-record quake.cover.m3.month: value 0.9586, lo 0.9393, hi 0.9756, unit 8,809 of 9,189, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,189 8,809 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,776
row-record quake.cover.m3.year: value 0.8631, lo 0.7902, hi 0.9412, unit 2,945 of 3,412, outcome BELOW, as printed: M3 and above, 1 year 3,412 2,945 341 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 208
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,131 of 159,911, outcome ABOVE, as printed: every magnitude, every window 159,911 158,131 1,330 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,480
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 305 of 118,050, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,050 305 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0337, lo 0.0171, hi 0.0488, unit 589 of 17,452, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,452 589 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0462, hi 0.092, unit 436 of 6,402, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,402 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1056, lo 0.0745, hi 0.1363, unit 599 of 5,672, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,672 599 14.4 10.6 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1931, lo 0.1512, hi 0.2365, unit 951 of 4,926, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,926 951 28.5 19.3 18.2 to 20.4 15.1 to 23.6 below 74
row-record quake.prob.40_60: value 0.3384, lo 0.2649, hi 0.4112, unit 914 of 2,701, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,701 914 49.3 33.8 32.1 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4274, lo 0.3044, hi 0.5605, unit 800 of 1,872, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,872 800 69.5 42.7 40.5 to 45.0 30.4 to 56.0 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7756, lo 0.6691, hi 0.8613, unit 636 of 820, outcome BELOW, as printed: 90 to 99 percent, not including 99 820 636 95.2 77.6 74.6 to 80.3 66.9 to 86.1 below 32
row-record quake.prob.99_100: value 0.9778, lo 0.9589, hi 0.9912, unit 1,236 of 1,264, outcome BELOW, as printed: 99 to 100 percent 1,264 1,236 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 31,991, outcome CONSISTENT, as printed: 63 of 31,991 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3113, lo 0.2431, hi 0.3863, unit 5,606 of 18,007, outcome BELOW, as printed: every magnitude, every window 18,007 5,606 41.9 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3033, lo 0.2308, hi 0.3837, unit 3,816 of 12,580, outcome BELOW, as printed: M3 and above 12,580 3,816 44.5 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3298, lo 0.2443, hi 0.4192, unit 1,790 of 5,427, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,427 1,790 35.6 33.0 31.7 to 34.2 24.4 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2376, lo 0.1388, hi 0.3385, unit 336 of 1,414, outcome BELOW, as printed: every magnitude, 1 day 1,414 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2104, lo 0.1305, hi 0.3088, unit 867 of 4,121, outcome BELOW, as printed: every magnitude, 1 week 4,121 867 36.7 21.0 19.8 to 22.3 13.1 to 30.9 below 73
row-record quake.prob10.month: value 0.2377, lo 0.165, hi 0.3268, unit 1,732 of 7,287, outcome BELOW, as printed: every magnitude, 1 month 7,287 1,732 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5151, lo 0.4216, hi 0.602, unit 2,671 of 5,185, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,185 2,671 50.7 51.5 50.1 to 52.9 42.2 to 60.2 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9291, lo 0.8824, hi 0.9566, unit 668 of 719, outcome CANNOT_TELL, as printed: 668 of 719 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-13 15:58 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-13T20:51:55Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-13T20:51:55Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-13T20:51:55Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,796 of 32,000, outcome CANNOT_TELL, as printed: M3 and above, every window 32,000 30,796 761 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,779
row-record quake.cover.m4: value 0.9855, lo 0.9788, hi 0.9937, unit 31,418 of 31,880, outcome ABOVE, as printed: M4 and above 31,880 31,418 456 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,862
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,890 of 32,000, outcome ABOVE, as printed: M5 and above 32,000 31,890 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,379
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,995 of 32,000, outcome ABOVE, as printed: M6 and above 32,000 31,995 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,547
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,999 of 32,000, outcome ABOVE, as printed: M7 and above 32,000 31,999 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,886
row-record quake.cover.m3.day: value 0.9887, lo 0.9804, hi 0.9937, unit 9,647 of 9,757, outcome ABOVE, as printed: M3 and above, 1 day 9,757 9,647 52 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,074
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,391 of 9,637, outcome ABOVE, as printed: M3 and above, 1 week 9,637 9,391 137 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,721
row-record quake.cover.m3.month: value 0.9586, lo 0.9393, hi 0.9756, unit 8,809 of 9,189, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,189 8,809 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,776
row-record quake.cover.m3.year: value 0.863, lo 0.7901, hi 0.9412, unit 2,949 of 3,417, outcome BELOW, as printed: M3 and above, 1 year 3,417 2,949 342 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 208
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,174 of 159,956, outcome ABOVE, as printed: every magnitude, every window 159,956 158,174 1,332 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,513
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 305 of 118,080, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,080 305 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0337, lo 0.0171, hi 0.0488, unit 589 of 17,456, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,456 589 2.4 3.4 3.1 to 3.6 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0462, hi 0.0919, unit 436 of 6,404, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,404 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1059, lo 0.0748, hi 0.1367, unit 601 of 5,675, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,675 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1934, lo 0.1514, hi 0.2367, unit 953 of 4,928, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,928 953 28.5 19.3 18.3 to 20.5 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3384, lo 0.2649, hi 0.4112, unit 914 of 2,701, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,701 914 49.3 33.8 32.1 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3054, hi 0.5607, unit 802 of 1,875, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,875 802 69.5 42.8 40.6 to 45.0 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7756, lo 0.6691, hi 0.8613, unit 636 of 820, outcome BELOW, as printed: 90 to 99 percent, not including 99 820 636 95.2 77.6 74.6 to 80.3 66.9 to 86.1 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 32,000, outcome CONSISTENT, as printed: 63 of 32,000 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3116, lo 0.2431, hi 0.3866, unit 5,613 of 18,016, outcome BELOW, as printed: every magnitude, every window 18,016 5,613 41.9 31.2 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3035, lo 0.2309, hi 0.3839, unit 3,820 of 12,585, outcome BELOW, as printed: M3 and above 12,585 3,820 44.5 30.3 29.6 to 31.2 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2447, hi 0.4197, unit 1,793 of 5,431, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,431 1,793 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2376, lo 0.1388, hi 0.3385, unit 336 of 1,414, outcome BELOW, as printed: every magnitude, 1 day 1,414 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2104, lo 0.1305, hi 0.3088, unit 867 of 4,121, outcome BELOW, as printed: every magnitude, 1 week 4,121 867 36.7 21.0 19.8 to 22.3 13.1 to 30.9 below 73
row-record quake.prob10.month: value 0.2377, lo 0.165, hi 0.3268, unit 1,732 of 7,287, outcome BELOW, as printed: every magnitude, 1 month 7,287 1,732 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5156, lo 0.4215, hi 0.6031, unit 2,678 of 5,194, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,194 2,678 50.7 51.6 50.2 to 52.9 42.1 to 60.3 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9292, lo 0.8824, hi 0.9566, unit 669 of 720, outcome CANNOT_TELL, as printed: 669 of 720 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-13 18:12 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-13T22:57:04Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-13T22:57:04Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-13T22:57:04Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9623, lo 0.946, hi 0.9776, unit 30,800 of 32,005, outcome CANNOT_TELL, as printed: M3 and above, every window 32,005 30,800 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,780
row-record quake.cover.m4: value 0.9855, lo 0.9787, hi 0.9936, unit 31,422 of 31,885, outcome ABOVE, as printed: M4 and above 31,885 31,422 457 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,865
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,895 of 32,005, outcome ABOVE, as printed: M5 and above 32,005 31,895 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,384
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 32,000 of 32,005, outcome ABOVE, as printed: M6 and above 32,005 32,000 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,552
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 32,004 of 32,005, outcome ABOVE, as printed: M7 and above 32,005 32,004 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,891
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,649 of 9,760, outcome ABOVE, as printed: M3 and above, 1 day 9,760 9,649 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,075
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,391 of 9,637, outcome ABOVE, as printed: M3 and above, 1 week 9,637 9,391 137 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,721
row-record quake.cover.m3.month: value 0.9587, lo 0.9393, hi 0.9756, unit 8,810 of 9,190, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,190 8,810 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,776
row-record quake.cover.m3.year: value 0.8631, lo 0.7901, hi 0.9412, unit 2,950 of 3,418, outcome BELOW, as printed: M3 and above, 1 year 3,418 2,950 342 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 208
row-record quake.cover.all: value 0.9888, lo 0.9848, hi 0.9934, unit 158,197 of 159,981, outcome ABOVE, as printed: every magnitude, every window 159,981 158,197 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,532
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 306 of 118,098, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,098 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.0171, hi 0.0489, unit 590 of 17,460, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,460 590 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0462, hi 0.0919, unit 436 of 6,405, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,405 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1059, lo 0.0748, hi 0.1367, unit 601 of 5,676, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,676 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1933, lo 0.1514, hi 0.2366, unit 953 of 4,929, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,929 953 28.5 19.3 18.3 to 20.5 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3384, lo 0.2649, hi 0.4112, unit 914 of 2,701, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,701 914 49.3 33.8 32.1 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3054, hi 0.5607, unit 802 of 1,875, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,875 802 69.5 42.8 40.6 to 45.0 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7756, lo 0.6691, hi 0.8613, unit 636 of 820, outcome BELOW, as printed: 90 to 99 percent, not including 99 820 636 95.2 77.6 74.6 to 80.3 66.9 to 86.1 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 32,005, outcome CONSISTENT, as printed: 63 of 32,005 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3115, lo 0.2431, hi 0.3866, unit 5,613 of 18,018, outcome BELOW, as printed: every magnitude, every window 18,018 5,613 41.9 31.1 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3035, lo 0.2309, hi 0.3837, unit 3,820 of 12,587, outcome BELOW, as printed: M3 and above 12,587 3,820 44.5 30.3 29.5 to 31.2 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2447, hi 0.4197, unit 1,793 of 5,431, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,431 1,793 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2376, lo 0.1388, hi 0.3385, unit 336 of 1,414, outcome BELOW, as printed: every magnitude, 1 day 1,414 336 36.1 23.8 21.6 to 26.1 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2104, lo 0.1305, hi 0.3088, unit 867 of 4,121, outcome BELOW, as printed: every magnitude, 1 week 4,121 867 36.7 21.0 19.8 to 22.3 13.1 to 30.9 below 73
row-record quake.prob10.month: value 0.2377, lo 0.165, hi 0.3268, unit 1,732 of 7,288, outcome BELOW, as printed: every magnitude, 1 month 7,288 1,732 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5155, lo 0.4215, hi 0.6031, unit 2,678 of 5,195, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,195 2,678 50.7 51.5 50.2 to 52.9 42.1 to 60.3 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9292, lo 0.8824, hi 0.9566, unit 669 of 720, outcome CANNOT_TELL, as printed: 669 of 720 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-13 20:27 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T01:17:56Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T01:17:56Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T01:17:56Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,810 of 32,015, outcome CANNOT_TELL, as printed: M3 and above, every window 32,015 30,810 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,785
row-record quake.cover.m4: value 0.9855, lo 0.9788, hi 0.9936, unit 31,432 of 31,895, outcome ABOVE, as printed: M4 and above 31,895 31,432 457 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,874
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,905 of 32,015, outcome ABOVE, as printed: M5 and above 32,015 31,905 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,394
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 32,010 of 32,015, outcome ABOVE, as printed: M6 and above 32,015 32,010 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,562
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 32,014 of 32,015, outcome ABOVE, as printed: M7 and above 32,015 32,014 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,901
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,651 of 9,762, outcome ABOVE, as printed: M3 and above, 1 day 9,762 9,651 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,076
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,394 of 9,640, outcome ABOVE, as printed: M3 and above, 1 week 9,640 9,394 137 109 97.5 97.1 to 97.7 96.0 to 98.4 above 82 3,723
row-record quake.cover.m3.month: value 0.9587, lo 0.9394, hi 0.9756, unit 8,813 of 9,193, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,193 8,813 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,777
row-record quake.cover.m3.year: value 0.8632, lo 0.7902, hi 0.9413, unit 2,952 of 3,420, outcome BELOW, as printed: M3 and above, 1 year 3,420 2,952 342 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 209
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,247 of 160,031, outcome ABOVE, as printed: every magnitude, every window 160,031 158,247 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,576
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 306 of 118,137, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,137 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.0171, hi 0.0489, unit 590 of 17,466, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,466 590 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0462, hi 0.0919, unit 436 of 6,406, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,406 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1058, lo 0.0748, hi 0.1366, unit 601 of 5,679, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,679 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1933, lo 0.1514, hi 0.2366, unit 953 of 4,929, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,929 953 28.5 19.3 18.3 to 20.5 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3383, lo 0.2647, hi 0.4111, unit 914 of 2,702, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,702 914 49.3 33.8 32.1 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3054, hi 0.5607, unit 802 of 1,875, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,875 802 69.5 42.8 40.6 to 45.0 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7756, lo 0.6691, hi 0.8613, unit 636 of 820, outcome BELOW, as printed: 90 to 99 percent, not including 99 820 636 95.2 77.6 74.6 to 80.3 66.9 to 86.1 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 32,015, outcome CONSISTENT, as printed: 63 of 32,015 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3115, lo 0.2431, hi 0.3866, unit 5,613 of 18,022, outcome BELOW, as printed: every magnitude, every window 18,022 5,613 41.9 31.1 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3034, lo 0.2308, hi 0.3837, unit 3,820 of 12,590, outcome BELOW, as printed: M3 and above 12,590 3,820 44.5 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2446, hi 0.4197, unit 1,793 of 5,432, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,432 1,793 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2375, lo 0.1387, hi 0.3385, unit 336 of 1,415, outcome BELOW, as printed: every magnitude, 1 day 1,415 336 36.1 23.8 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2103, lo 0.1302, hi 0.3088, unit 867 of 4,123, outcome BELOW, as printed: every magnitude, 1 week 4,123 867 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2376, lo 0.1649, hi 0.3268, unit 1,732 of 7,289, outcome BELOW, as printed: every magnitude, 1 month 7,289 1,732 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5155, lo 0.4215, hi 0.6031, unit 2,678 of 5,195, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,195 2,678 50.7 51.5 50.2 to 52.9 42.1 to 60.3 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9292, lo 0.8824, hi 0.9566, unit 669 of 720, outcome CANNOT_TELL, as printed: 669 of 720 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-13 22:34 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T03:19:09Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T03:19:09Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T03:19:09Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,815 of 32,020, outcome CANNOT_TELL, as printed: M3 and above, every window 32,020 30,815 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,789
row-record quake.cover.m4: value 0.9855, lo 0.9788, hi 0.9936, unit 31,437 of 31,900, outcome ABOVE, as printed: M4 and above 31,900 31,437 457 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,878
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,910 of 32,020, outcome ABOVE, as printed: M5 and above 32,020 31,910 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,399
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 32,015 of 32,020, outcome ABOVE, as printed: M6 and above 32,020 32,015 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,567
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 32,019 of 32,020, outcome ABOVE, as printed: M7 and above 32,020 32,019 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,906
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,652 of 9,763, outcome ABOVE, as printed: M3 and above, 1 day 9,763 9,652 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,077
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,396 of 9,642, outcome ABOVE, as printed: M3 and above, 1 week 9,642 9,396 137 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,725
row-record quake.cover.m3.month: value 0.9587, lo 0.9394, hi 0.9757, unit 8,814 of 9,194, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,194 8,814 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,778
row-record quake.cover.m3.year: value 0.8632, lo 0.7903, hi 0.9413, unit 2,953 of 3,421, outcome BELOW, as printed: M3 and above, 1 year 3,421 2,953 342 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 209
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,272 of 160,056, outcome ABOVE, as printed: every magnitude, every window 160,056 158,272 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,599
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 306 of 118,160, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,160 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.0171, hi 0.0489, unit 590 of 17,466, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,466 590 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0462, hi 0.0919, unit 436 of 6,407, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,407 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1058, lo 0.0748, hi 0.1366, unit 601 of 5,679, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,679 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1933, lo 0.1514, hi 0.2366, unit 953 of 4,929, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,929 953 28.5 19.3 18.3 to 20.5 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3385, lo 0.2648, hi 0.4115, unit 915 of 2,703, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,703 915 49.3 33.9 32.1 to 35.7 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3054, hi 0.5607, unit 802 of 1,875, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,875 802 69.5 42.8 40.6 to 45.0 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7756, lo 0.6691, hi 0.8613, unit 636 of 820, outcome BELOW, as printed: 90 to 99 percent, not including 99 820 636 95.2 77.6 74.6 to 80.3 66.9 to 86.1 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 32,020, outcome CONSISTENT, as printed: 63 of 32,020 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3115, lo 0.2431, hi 0.3866, unit 5,614 of 18,023, outcome BELOW, as printed: every magnitude, every window 18,023 5,614 41.9 31.1 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3035, lo 0.231, hi 0.3838, unit 3,821 of 12,591, outcome BELOW, as printed: M3 and above 12,591 3,821 44.5 30.3 29.5 to 31.2 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2446, hi 0.4197, unit 1,793 of 5,432, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,432 1,793 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2375, lo 0.1387, hi 0.3385, unit 336 of 1,415, outcome BELOW, as printed: every magnitude, 1 day 1,415 336 36.1 23.8 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2103, lo 0.1302, hi 0.3088, unit 867 of 4,123, outcome BELOW, as printed: every magnitude, 1 week 4,123 867 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2376, lo 0.1649, hi 0.3268, unit 1,732 of 7,289, outcome BELOW, as printed: every magnitude, 1 month 7,289 1,732 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5156, lo 0.4215, hi 0.6031, unit 2,679 of 5,196, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,196 2,679 50.7 51.6 50.2 to 52.9 42.1 to 60.3 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9292, lo 0.8824, hi 0.9566, unit 669 of 720, outcome CANNOT_TELL, as printed: 669 of 720 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-14 00:28 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T05:20:39Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T05:20:39Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T05:20:39Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,818 of 32,023, outcome CANNOT_TELL, as printed: M3 and above, every window 32,023 30,818 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,790
row-record quake.cover.m4: value 0.9855, lo 0.9788, hi 0.9936, unit 31,440 of 31,903, outcome ABOVE, as printed: M4 and above 31,903 31,440 457 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,881
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,913 of 32,023, outcome ABOVE, as printed: M5 and above 32,023 31,913 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,402
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 32,018 of 32,023, outcome ABOVE, as printed: M6 and above 32,023 32,018 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,570
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 32,022 of 32,023, outcome ABOVE, as printed: M7 and above 32,023 32,022 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,909
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,653 of 9,764, outcome ABOVE, as printed: M3 and above, 1 day 9,764 9,653 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,078
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,397 of 9,643, outcome ABOVE, as printed: M3 and above, 1 week 9,643 9,397 137 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,725
row-record quake.cover.m3.month: value 0.9587, lo 0.9394, hi 0.9757, unit 8,814 of 9,194, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,194 8,814 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,778
row-record quake.cover.m3.year: value 0.8632, lo 0.7904, hi 0.9413, unit 2,954 of 3,422, outcome BELOW, as printed: M3 and above, 1 year 3,422 2,954 342 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 209
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,287 of 160,071, outcome ABOVE, as printed: every magnitude, every window 160,071 158,287 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,612
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 306 of 118,171, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,171 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.0171, hi 0.0489, unit 590 of 17,468, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,468 590 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.068, lo 0.0462, hi 0.0918, unit 436 of 6,408, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,408 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1058, lo 0.0748, hi 0.1366, unit 601 of 5,680, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,680 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1933, lo 0.1514, hi 0.2366, unit 953 of 4,929, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,929 953 28.5 19.3 18.3 to 20.5 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3385, lo 0.2648, hi 0.4115, unit 915 of 2,703, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,703 915 49.3 33.9 32.1 to 35.7 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3054, hi 0.5607, unit 802 of 1,875, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,875 802 69.5 42.8 40.6 to 45.0 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7756, lo 0.6691, hi 0.8613, unit 636 of 820, outcome BELOW, as printed: 90 to 99 percent, not including 99 820 636 95.2 77.6 74.6 to 80.3 66.9 to 86.1 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 32,023, outcome CONSISTENT, as printed: 63 of 32,023 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3115, lo 0.2431, hi 0.3865, unit 5,614 of 18,024, outcome BELOW, as printed: every magnitude, every window 18,024 5,614 41.9 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3034, lo 0.231, hi 0.3837, unit 3,821 of 12,592, outcome BELOW, as printed: M3 and above 12,592 3,821 44.5 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2446, hi 0.4197, unit 1,793 of 5,432, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,432 1,793 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2375, lo 0.1387, hi 0.3385, unit 336 of 1,415, outcome BELOW, as printed: every magnitude, 1 day 1,415 336 36.1 23.8 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2102, lo 0.1302, hi 0.3088, unit 867 of 4,124, outcome BELOW, as printed: every magnitude, 1 week 4,124 867 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2376, lo 0.1649, hi 0.3268, unit 1,732 of 7,289, outcome BELOW, as printed: every magnitude, 1 month 7,289 1,732 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5156, lo 0.4215, hi 0.6031, unit 2,679 of 5,196, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,196 2,679 50.7 51.6 50.2 to 52.9 42.1 to 60.3 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9293, lo 0.8824, hi 0.9567, unit 670 of 721, outcome CANNOT_TELL, as printed: 670 of 721 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-14 03:57 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T07:40:48Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T07:40:48Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T07:40:48Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,821 of 32,026, outcome CANNOT_TELL, as printed: M3 and above, every window 32,026 30,821 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,791
row-record quake.cover.m4: value 0.9855, lo 0.9788, hi 0.9936, unit 31,443 of 31,906, outcome ABOVE, as printed: M4 and above 31,906 31,443 457 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,882
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,916 of 32,026, outcome ABOVE, as printed: M5 and above 32,026 31,916 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,405
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 32,021 of 32,026, outcome ABOVE, as printed: M6 and above 32,026 32,021 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,573
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 32,025 of 32,026, outcome ABOVE, as printed: M7 and above 32,026 32,025 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,912
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,654 of 9,765, outcome ABOVE, as printed: M3 and above, 1 day 9,765 9,654 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,079
row-record quake.cover.m3.week: value 0.9745, lo 0.9598, hi 0.984, unit 9,397 of 9,643, outcome ABOVE, as printed: M3 and above, 1 week 9,643 9,397 137 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,725
row-record quake.cover.m3.month: value 0.9587, lo 0.9394, hi 0.9757, unit 8,815 of 9,195, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,195 8,815 230 150 95.9 95.4 to 96.3 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,778
row-record quake.cover.m3.year: value 0.8633, lo 0.7905, hi 0.9413, unit 2,955 of 3,423, outcome BELOW, as printed: M3 and above, 1 year 3,423 2,955 342 126 86.3 85.1 to 87.4 79.0 to 94.1 below 42 209
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,302 of 160,086, outcome ABOVE, as printed: every magnitude, every window 160,086 158,302 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,623
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 306 of 118,182, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,182 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.0171, hi 0.049, unit 591 of 17,470, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,470 591 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.068, lo 0.0462, hi 0.0918, unit 436 of 6,408, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,408 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1058, lo 0.0748, hi 0.1366, unit 601 of 5,680, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,680 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1935, lo 0.1515, hi 0.2368, unit 954 of 4,931, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,931 954 28.5 19.4 18.3 to 20.5 15.2 to 23.7 below 74
row-record quake.prob.40_60: value 0.3385, lo 0.2648, hi 0.4115, unit 915 of 2,703, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,703 915 49.3 33.9 32.1 to 35.7 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3054, hi 0.5607, unit 802 of 1,875, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,875 802 69.5 42.8 40.6 to 45.0 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7756, lo 0.6691, hi 0.8613, unit 636 of 820, outcome BELOW, as printed: 90 to 99 percent, not including 99 820 636 95.2 77.6 74.6 to 80.3 66.9 to 86.1 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 32,026, outcome CONSISTENT, as printed: 63 of 32,026 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3115, lo 0.2431, hi 0.3866, unit 5,615 of 18,026, outcome BELOW, as printed: every magnitude, every window 18,026 5,615 41.8 31.1 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3035, lo 0.231, hi 0.3837, unit 3,822 of 12,594, outcome BELOW, as printed: M3 and above 12,594 3,822 44.5 30.3 29.5 to 31.2 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2446, hi 0.4197, unit 1,793 of 5,432, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,432 1,793 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2375, lo 0.1387, hi 0.3385, unit 336 of 1,415, outcome BELOW, as printed: every magnitude, 1 day 1,415 336 36.1 23.8 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2102, lo 0.1302, hi 0.3088, unit 867 of 4,124, outcome BELOW, as printed: every magnitude, 1 week 4,124 867 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2376, lo 0.1649, hi 0.3268, unit 1,732 of 7,290, outcome BELOW, as printed: every magnitude, 1 month 7,290 1,732 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5157, lo 0.4215, hi 0.6034, unit 2,680 of 5,197, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,197 2,680 50.7 51.6 50.2 to 52.9 42.1 to 60.3 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9293, lo 0.8824, hi 0.9567, unit 670 of 721, outcome CANNOT_TELL, as printed: 670 of 721 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-14 05:01 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T09:57:17Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T09:57:17Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T09:57:17Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.946, hi 0.9776, unit 30,829 of 32,034, outcome CANNOT_TELL, as printed: M3 and above, every window 32,034 30,829 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,794
row-record quake.cover.m4: value 0.9855, lo 0.9788, hi 0.9936, unit 31,451 of 31,914, outcome ABOVE, as printed: M4 and above 31,914 31,451 457 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,888
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,924 of 32,034, outcome ABOVE, as printed: M5 and above 32,034 31,924 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,412
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 32,029 of 32,034, outcome ABOVE, as printed: M6 and above 32,034 32,029 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,581
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 32,033 of 32,034, outcome ABOVE, as printed: M7 and above 32,034 32,033 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,920
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,655 of 9,766, outcome ABOVE, as printed: M3 and above, 1 day 9,766 9,655 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,080
row-record quake.cover.m3.week: value 0.9745, lo 0.9599, hi 0.984, unit 9,399 of 9,645, outcome ABOVE, as printed: M3 and above, 1 week 9,645 9,399 137 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,725
row-record quake.cover.m3.month: value 0.9587, lo 0.9394, hi 0.9757, unit 8,818 of 9,198, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,198 8,818 230 150 95.9 95.4 to 96.3 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,780
row-record quake.cover.m3.year: value 0.8634, lo 0.7906, hi 0.9414, unit 2,957 of 3,425, outcome BELOW, as printed: M3 and above, 1 year 3,425 2,957 342 126 86.3 85.1 to 87.5 79.1 to 94.1 below 42 209
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,342 of 160,126, outcome ABOVE, as printed: every magnitude, every window 160,126 158,342 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,655
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 306 of 118,212, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,212 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.0171, hi 0.049, unit 591 of 17,472, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,472 591 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.068, lo 0.0461, hi 0.0918, unit 436 of 6,411, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,411 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1058, lo 0.0747, hi 0.1366, unit 601 of 5,682, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,682 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1935, lo 0.1515, hi 0.2368, unit 954 of 4,931, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,931 954 28.5 19.4 18.3 to 20.5 15.2 to 23.7 below 74
row-record quake.prob.40_60: value 0.3383, lo 0.2645, hi 0.4114, unit 915 of 2,705, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,705 915 49.3 33.8 32.1 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4277, lo 0.3054, hi 0.5607, unit 802 of 1,875, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,875 802 69.5 42.8 40.6 to 45.0 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.625, lo 0.4908, hi 0.756, unit 470 of 752, outcome BELOW, as printed: 80 to 90 percent, not including 90 752 470 84.9 62.5 59.0 to 65.9 49.1 to 75.6 below 37
row-record quake.prob.90_99: value 0.7747, lo 0.6691, hi 0.8604, unit 636 of 821, outcome BELOW, as printed: 90 to 99 percent, not including 99 821 636 95.2 77.5 74.5 to 80.2 66.9 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 32,034, outcome CONSISTENT, as printed: 63 of 32,034 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3114, lo 0.2431, hi 0.3866, unit 5,615 of 18,031, outcome BELOW, as printed: every magnitude, every window 18,031 5,615 41.8 31.1 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3034, lo 0.2309, hi 0.3836, unit 3,822 of 12,597, outcome BELOW, as printed: M3 and above 12,597 3,822 44.5 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.33, lo 0.2446, hi 0.4195, unit 1,793 of 5,434, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,434 1,793 35.6 33.0 31.8 to 34.3 24.5 to 41.9 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2375, lo 0.1387, hi 0.3385, unit 336 of 1,415, outcome BELOW, as printed: every magnitude, 1 day 1,415 336 36.1 23.8 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2102, lo 0.1302, hi 0.3088, unit 867 of 4,125, outcome BELOW, as printed: every magnitude, 1 week 4,125 867 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2376, lo 0.1649, hi 0.3267, unit 1,732 of 7,291, outcome BELOW, as printed: every magnitude, 1 month 7,291 1,732 39.6 23.8 22.8 to 24.8 16.5 to 32.7 below 73
row-record quake.prob10.year: value 0.5154, lo 0.4215, hi 0.6034, unit 2,680 of 5,200, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,200 2,680 50.7 51.5 50.2 to 52.9 42.1 to 60.3 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9293, lo 0.8824, hi 0.9567, unit 670 of 721, outcome CANNOT_TELL, as printed: 670 of 721 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-14 07:47 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T12:09:28Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T12:09:28Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T12:09:28Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9461, hi 0.9776, unit 30,849 of 32,054, outcome CANNOT_TELL, as printed: M3 and above, every window 32,054 30,849 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,797
row-record quake.cover.m4: value 0.9855, lo 0.9788, hi 0.9936, unit 31,471 of 31,934, outcome ABOVE, as printed: M4 and above 31,934 31,471 457 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,900
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,944 of 32,054, outcome ABOVE, as printed: M5 and above 32,054 31,944 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,427
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 32,049 of 32,054, outcome ABOVE, as printed: M6 and above 32,054 32,049 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,601
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 32,053 of 32,054, outcome ABOVE, as printed: M7 and above 32,054 32,053 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,940
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,658 of 9,769, outcome ABOVE, as printed: M3 and above, 1 day 9,769 9,658 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,082
row-record quake.cover.m3.week: value 0.9745, lo 0.9599, hi 0.984, unit 9,403 of 9,649, outcome ABOVE, as printed: M3 and above, 1 week 9,649 9,403 137 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,726
row-record quake.cover.m3.month: value 0.9587, lo 0.9394, hi 0.9757, unit 8,825 of 9,205, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,205 8,825 230 150 95.9 95.5 to 96.3 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,780
row-record quake.cover.m3.year: value 0.8636, lo 0.7908, hi 0.9415, unit 2,963 of 3,431, outcome BELOW, as printed: M3 and above, 1 year 3,431 2,963 342 126 86.4 85.2 to 87.5 79.1 to 94.2 below 42 209
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,442 of 160,226, outcome ABOVE, as printed: every magnitude, every window 160,226 158,442 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,725
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 306 of 118,278, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,278 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.0171, hi 0.049, unit 591 of 17,483, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,483 591 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0679, lo 0.0461, hi 0.0917, unit 436 of 6,418, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,418 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1057, lo 0.0747, hi 0.1365, unit 601 of 5,685, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,685 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1942, lo 0.1523, hi 0.2376, unit 959 of 4,938, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,938 959 28.5 19.4 18.3 to 20.5 15.2 to 23.8 below 74
row-record quake.prob.40_60: value 0.3383, lo 0.2645, hi 0.4114, unit 915 of 2,705, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,705 915 49.3 33.8 32.1 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4281, lo 0.3057, hi 0.5606, unit 804 of 1,878, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,878 804 69.5 42.8 40.6 to 45.1 30.6 to 56.1 below 46
row-record quake.prob.80_90: value 0.6252, lo 0.4905, hi 0.7568, unit 472 of 755, outcome BELOW, as printed: 80 to 90 percent, not including 90 755 472 84.9 62.5 59.0 to 65.9 49.0 to 75.7 below 37
row-record quake.prob.90_99: value 0.7747, lo 0.6691, hi 0.8604, unit 636 of 821, outcome BELOW, as printed: 90 to 99 percent, not including 99 821 636 95.2 77.5 74.5 to 80.2 66.9 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 32,054, outcome CONSISTENT, as printed: 63 of 32,054 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3116, lo 0.2432, hi 0.3868, unit 5,624 of 18,047, outcome BELOW, as printed: every magnitude, every window 18,047 5,624 41.9 31.2 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3036, lo 0.231, hi 0.3837, unit 3,827 of 12,607, outcome BELOW, as printed: M3 and above 12,607 3,827 44.5 30.4 29.6 to 31.2 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3303, lo 0.245, hi 0.4198, unit 1,797 of 5,440, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,440 1,797 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2375, lo 0.1387, hi 0.3385, unit 336 of 1,415, outcome BELOW, as printed: every magnitude, 1 day 1,415 336 36.1 23.8 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2101, lo 0.1302, hi 0.3087, unit 867 of 4,126, outcome BELOW, as printed: every magnitude, 1 week 4,126 867 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2377, lo 0.1648, hi 0.3265, unit 1,734 of 7,295, outcome BELOW, as printed: every magnitude, 1 month 7,295 1,734 39.6 23.8 22.8 to 24.8 16.5 to 32.6 below 73
row-record quake.prob10.year: value 0.5156, lo 0.4217, hi 0.6034, unit 2,687 of 5,211, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,211 2,687 50.7 51.6 50.2 to 52.9 42.2 to 60.3 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9293, lo 0.8824, hi 0.9567, unit 670 of 721, outcome CANNOT_TELL, as printed: 670 of 721 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-14 09:40 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T14:27:04Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T14:27:04Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T14:27:04Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9624, lo 0.9461, hi 0.9776, unit 30,855 of 32,060, outcome CANNOT_TELL, as printed: M3 and above, every window 32,060 30,855 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,800
row-record quake.cover.m4: value 0.9855, lo 0.9788, hi 0.9936, unit 31,477 of 31,940, outcome ABOVE, as printed: M4 and above 31,940 31,477 457 6 98.6 98.4 to 98.7 97.9 to 99.4 above 81 22,905
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,950 of 32,060, outcome ABOVE, as printed: M5 and above 32,060 31,950 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,433
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 32,055 of 32,060, outcome ABOVE, as printed: M6 and above 32,060 32,055 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,607
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 32,059 of 32,060, outcome ABOVE, as printed: M7 and above 32,060 32,059 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,946
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,660 of 9,771, outcome ABOVE, as printed: M3 and above, 1 day 9,771 9,660 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,084
row-record quake.cover.m3.week: value 0.9745, lo 0.9599, hi 0.984, unit 9,405 of 9,651, outcome ABOVE, as printed: M3 and above, 1 week 9,651 9,405 137 109 97.5 97.1 to 97.8 96.0 to 98.4 above 82 3,727
row-record quake.cover.m3.month: value 0.9587, lo 0.9395, hi 0.9757, unit 8,826 of 9,206, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,206 8,826 230 150 95.9 95.5 to 96.3 94.0 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,780
row-record quake.cover.m3.year: value 0.8636, lo 0.791, hi 0.9415, unit 2,964 of 3,432, outcome BELOW, as printed: M3 and above, 1 year 3,432 2,964 342 126 86.4 85.2 to 87.5 79.1 to 94.2 below 42 209
row-record quake.cover.all: value 0.9889, lo 0.9849, hi 0.9934, unit 158,472 of 160,256, outcome ABOVE, as printed: every magnitude, every window 160,256 158,472 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,751
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 306 of 118,301, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 118,301 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.0171, hi 0.0489, unit 591 of 17,487, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,487 591 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0679, lo 0.0461, hi 0.0917, unit 436 of 6,419, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,419 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1057, lo 0.0747, hi 0.1365, unit 601 of 5,686, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,686 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1942, lo 0.1523, hi 0.2376, unit 959 of 4,939, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,939 959 28.5 19.4 18.3 to 20.5 15.2 to 23.8 below 74
row-record quake.prob.40_60: value 0.3383, lo 0.2645, hi 0.4114, unit 915 of 2,705, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,705 915 49.3 33.8 32.1 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4281, lo 0.3057, hi 0.5606, unit 804 of 1,878, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,878 804 69.5 42.8 40.6 to 45.1 30.6 to 56.1 below 46
row-record quake.prob.80_90: value 0.6252, lo 0.4905, hi 0.7568, unit 472 of 755, outcome BELOW, as printed: 80 to 90 percent, not including 90 755 472 84.9 62.5 59.0 to 65.9 49.0 to 75.7 below 37
row-record quake.prob.90_99: value 0.7747, lo 0.6691, hi 0.8604, unit 636 of 821, outcome BELOW, as printed: 90 to 99 percent, not including 99 821 636 95.2 77.5 74.5 to 80.2 66.9 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 32,060, outcome CONSISTENT, as printed: 63 of 32,060 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3116, lo 0.2432, hi 0.3867, unit 5,624 of 18,049, outcome BELOW, as printed: every magnitude, every window 18,049 5,624 41.9 31.2 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3035, lo 0.231, hi 0.3837, unit 3,827 of 12,609, outcome BELOW, as printed: M3 and above 12,609 3,827 44.5 30.3 29.5 to 31.2 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3303, lo 0.245, hi 0.4198, unit 1,797 of 5,440, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,440 1,797 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2375, lo 0.1387, hi 0.3385, unit 336 of 1,415, outcome BELOW, as printed: every magnitude, 1 day 1,415 336 36.1 23.8 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2101, lo 0.1302, hi 0.3087, unit 867 of 4,126, outcome BELOW, as printed: every magnitude, 1 week 4,126 867 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2377, lo 0.1648, hi 0.3265, unit 1,734 of 7,296, outcome BELOW, as printed: every magnitude, 1 month 7,296 1,734 39.6 23.8 22.8 to 24.8 16.5 to 32.6 below 73
row-record quake.prob10.year: value 0.5155, lo 0.4217, hi 0.6029, unit 2,687 of 5,212, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,212 2,687 50.7 51.5 50.2 to 52.9 42.2 to 60.3 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9293, lo 0.8824, hi 0.9567, unit 670 of 721, outcome CANNOT_TELL, as printed: 670 of 721 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-14 12:02 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T16:30:02Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T16:30:02Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T16:30:02Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9622, lo 0.9458, hi 0.9776, unit 30,685 of 31,890, outcome CANNOT_TELL, as printed: M3 and above, every window 31,890 30,685 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,645
row-record quake.cover.m4: value 0.9854, lo 0.9785, hi 0.9936, unit 31,307 of 31,770, outcome ABOVE, as printed: M4 and above 31,770 31,307 457 6 98.5 98.4 to 98.7 97.9 to 99.4 above 81 22,734
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,780 of 31,890, outcome ABOVE, as printed: M5 and above 31,890 31,780 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,263
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,885 of 31,890, outcome ABOVE, as printed: M6 and above 31,890 31,885 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,437
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,889 of 31,890, outcome ABOVE, as printed: M7 and above 31,890 31,889 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,776
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,601 of 9,712, outcome ABOVE, as printed: M3 and above, 1 day 9,712 9,601 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,025
row-record quake.cover.m3.week: value 0.9744, lo 0.9599, hi 0.9839, unit 9,347 of 9,593, outcome ABOVE, as printed: M3 and above, 1 week 9,593 9,347 137 109 97.4 97.1 to 97.7 96.0 to 98.4 above 82 3,672
row-record quake.cover.m3.month: value 0.9585, lo 0.9391, hi 0.9757, unit 8,772 of 9,152, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,152 8,772 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,739
row-record quake.cover.m3.year: value 0.8637, lo 0.7912, hi 0.9415, unit 2,965 of 3,433, outcome BELOW, as printed: M3 and above, 1 year 3,433 2,965 342 126 86.4 85.2 to 87.5 79.1 to 94.2 below 42 209
row-record quake.cover.all: value 0.9888, lo 0.9848, hi 0.9934, unit 157,622 of 159,406, outcome ABOVE, as printed: every magnitude, every window 159,406 157,622 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,915
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,482, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,482 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.0171, hi 0.0491, unit 591 of 17,458, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,458 591 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.068, lo 0.0461, hi 0.0918, unit 436 of 6,416, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,416 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1057, lo 0.0747, hi 0.1365, unit 601 of 5,686, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,686 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1941, lo 0.1523, hi 0.2375, unit 959 of 4,940, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,940 959 28.5 19.4 18.3 to 20.5 15.2 to 23.8 below 74
row-record quake.prob.40_60: value 0.3383, lo 0.2645, hi 0.4114, unit 915 of 2,705, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,705 915 49.3 33.8 32.1 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4281, lo 0.3057, hi 0.5606, unit 804 of 1,878, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,878 804 69.5 42.8 40.6 to 45.1 30.6 to 56.1 below 46
row-record quake.prob.80_90: value 0.6252, lo 0.4905, hi 0.7568, unit 472 of 755, outcome BELOW, as printed: 80 to 90 percent, not including 90 755 472 84.9 62.5 59.0 to 65.9 49.0 to 75.7 below 37
row-record quake.prob.90_99: value 0.7747, lo 0.6691, hi 0.8604, unit 636 of 821, outcome BELOW, as printed: 90 to 99 percent, not including 99 821 636 95.2 77.5 74.5 to 80.2 66.9 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,890, outcome CONSISTENT, as printed: 63 of 31,890 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3116, lo 0.2432, hi 0.3867, unit 5,624 of 18,050, outcome BELOW, as printed: every magnitude, every window 18,050 5,624 41.9 31.2 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3035, lo 0.231, hi 0.3837, unit 3,827 of 12,610, outcome BELOW, as printed: M3 and above 12,610 3,827 44.5 30.3 29.5 to 31.2 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3303, lo 0.245, hi 0.4198, unit 1,797 of 5,440, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,440 1,797 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2375, lo 0.1387, hi 0.3385, unit 336 of 1,415, outcome BELOW, as printed: every magnitude, 1 day 1,415 336 36.1 23.8 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2101, lo 0.1302, hi 0.3087, unit 867 of 4,126, outcome BELOW, as printed: every magnitude, 1 week 4,126 867 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2377, lo 0.1648, hi 0.3265, unit 1,734 of 7,296, outcome BELOW, as printed: every magnitude, 1 month 7,296 1,734 39.6 23.8 22.8 to 24.8 16.5 to 32.6 below 73
row-record quake.prob10.year: value 0.5154, lo 0.4217, hi 0.6024, unit 2,687 of 5,213, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,213 2,687 50.7 51.5 50.2 to 52.9 42.2 to 60.2 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.929, lo 0.8822, hi 0.9565, unit 667 of 718, outcome CANNOT_TELL, as printed: 667 of 718 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-14 13:44 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T18:37:56Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T18:37:56Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T18:37:56Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9622, lo 0.9458, hi 0.9776, unit 30,689 of 31,894, outcome CANNOT_TELL, as printed: M3 and above, every window 31,894 30,689 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,645
row-record quake.cover.m4: value 0.9854, lo 0.9785, hi 0.9936, unit 31,311 of 31,774, outcome ABOVE, as printed: M4 and above 31,774 31,311 457 6 98.5 98.4 to 98.7 97.9 to 99.4 above 81 22,737
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,784 of 31,894, outcome ABOVE, as printed: M5 and above 31,894 31,784 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,266
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,889 of 31,894, outcome ABOVE, as printed: M6 and above 31,894 31,889 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,441
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,893 of 31,894, outcome ABOVE, as printed: M7 and above 31,894 31,893 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,780
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,601 of 9,712, outcome ABOVE, as printed: M3 and above, 1 day 9,712 9,601 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,025
row-record quake.cover.m3.week: value 0.9744, lo 0.9599, hi 0.9839, unit 9,347 of 9,593, outcome ABOVE, as printed: M3 and above, 1 week 9,593 9,347 137 109 97.4 97.1 to 97.7 96.0 to 98.4 above 82 3,672
row-record quake.cover.m3.month: value 0.9585, lo 0.9392, hi 0.9757, unit 8,775 of 9,155, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,155 8,775 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 77 1,739
row-record quake.cover.m3.year: value 0.8637, lo 0.7912, hi 0.9416, unit 2,966 of 3,434, outcome BELOW, as printed: M3 and above, 1 year 3,434 2,966 342 126 86.4 85.2 to 87.5 79.1 to 94.2 below 42 209
row-record quake.cover.all: value 0.9888, lo 0.9848, hi 0.9934, unit 157,642 of 159,426, outcome ABOVE, as printed: every magnitude, every window 159,426 157,642 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,929
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,495, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,495 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.0172, hi 0.0491, unit 592 of 17,462, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,462 592 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.068, lo 0.0461, hi 0.0918, unit 436 of 6,416, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,416 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1057, lo 0.0746, hi 0.1365, unit 601 of 5,687, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,687 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1941, lo 0.1523, hi 0.2375, unit 959 of 4,941, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,941 959 28.5 19.4 18.3 to 20.5 15.2 to 23.8 below 74
row-record quake.prob.40_60: value 0.3383, lo 0.2645, hi 0.4114, unit 915 of 2,705, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,705 915 49.3 33.8 32.1 to 35.6 26.5 to 41.1 below 58
row-record quake.prob.60_80: value 0.4284, lo 0.3057, hi 0.5609, unit 805 of 1,879, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,879 805 69.5 42.8 40.6 to 45.1 30.6 to 56.1 below 46
row-record quake.prob.80_90: value 0.6252, lo 0.4905, hi 0.7568, unit 472 of 755, outcome BELOW, as printed: 80 to 90 percent, not including 90 755 472 84.9 62.5 59.0 to 65.9 49.0 to 75.7 below 37
row-record quake.prob.90_99: value 0.7747, lo 0.6691, hi 0.8604, unit 636 of 821, outcome BELOW, as printed: 90 to 99 percent, not including 99 821 636 95.2 77.5 74.5 to 80.2 66.9 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,894, outcome CONSISTENT, as printed: 63 of 31,894 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3116, lo 0.2433, hi 0.3867, unit 5,625 of 18,053, outcome BELOW, as printed: every magnitude, every window 18,053 5,625 41.8 31.2 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3035, lo 0.231, hi 0.3837, unit 3,828 of 12,612, outcome BELOW, as printed: M3 and above 12,612 3,828 44.5 30.3 29.6 to 31.2 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3303, lo 0.245, hi 0.4198, unit 1,797 of 5,441, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,441 1,797 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 52
row-record quake.prob10.day: value 0.2375, lo 0.1387, hi 0.3385, unit 336 of 1,415, outcome BELOW, as printed: every magnitude, 1 day 1,415 336 36.1 23.8 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2101, lo 0.1302, hi 0.3087, unit 867 of 4,126, outcome BELOW, as printed: every magnitude, 1 week 4,126 867 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2376, lo 0.1648, hi 0.3265, unit 1,734 of 7,297, outcome BELOW, as printed: every magnitude, 1 month 7,297 1,734 39.6 23.8 22.8 to 24.8 16.5 to 32.6 below 73
row-record quake.prob10.year: value 0.5154, lo 0.4217, hi 0.6024, unit 2,688 of 5,215, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,215 2,688 50.7 51.5 50.2 to 52.9 42.2 to 60.2 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.929, lo 0.8822, hi 0.9565, unit 667 of 718, outcome CANNOT_TELL, as printed: 667 of 718 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-14 17:53 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T20:52:33Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T20:52:33Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T20:52:33Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9622, lo 0.9458, hi 0.9776, unit 30,697 of 31,902, outcome CANNOT_TELL, as printed: M3 and above, every window 31,902 30,697 762 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,646
row-record quake.cover.m4: value 0.9854, lo 0.9785, hi 0.9936, unit 31,319 of 31,782, outcome ABOVE, as printed: M4 and above 31,782 31,319 457 6 98.5 98.4 to 98.7 97.9 to 99.4 above 81 22,742
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,792 of 31,902, outcome ABOVE, as printed: M5 and above 31,902 31,792 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,274
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,897 of 31,902, outcome ABOVE, as printed: M6 and above 31,902 31,897 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,449
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,901 of 31,902, outcome ABOVE, as printed: M7 and above 31,902 31,901 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,788
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,602 of 9,713, outcome ABOVE, as printed: M3 and above, 1 day 9,713 9,602 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,025
row-record quake.cover.m3.week: value 0.9744, lo 0.9599, hi 0.9839, unit 9,348 of 9,594, outcome ABOVE, as printed: M3 and above, 1 week 9,594 9,348 137 109 97.4 97.1 to 97.7 96.0 to 98.4 above 82 3,672
row-record quake.cover.m3.month: value 0.9585, lo 0.9392, hi 0.9757, unit 8,780 of 9,160, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,160 8,780 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 78 1,740
row-record quake.cover.m3.year: value 0.8638, lo 0.7912, hi 0.9416, unit 2,967 of 3,435, outcome BELOW, as printed: M3 and above, 1 year 3,435 2,967 342 126 86.4 85.2 to 87.5 79.1 to 94.2 below 42 209
row-record quake.cover.all: value 0.9888, lo 0.9848, hi 0.9934, unit 157,682 of 159,466, outcome ABOVE, as printed: every magnitude, every window 159,466 157,682 1,334 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,959
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,521, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,521 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.0172, hi 0.0491, unit 592 of 17,467, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,467 592 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0679, lo 0.046, hi 0.0917, unit 436 of 6,419, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,419 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1056, lo 0.0746, hi 0.1365, unit 601 of 5,690, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,690 601 14.4 10.6 9.8 to 11.4 7.5 to 13.7 below 77
row-record quake.prob.20_40: value 0.1941, lo 0.1523, hi 0.2373, unit 959 of 4,942, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,942 959 28.5 19.4 18.3 to 20.5 15.2 to 23.7 below 74
row-record quake.prob.40_60: value 0.338, lo 0.2643, hi 0.411, unit 915 of 2,707, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,707 915 49.4 33.8 32.0 to 35.6 26.4 to 41.1 below 58
row-record quake.prob.60_80: value 0.4284, lo 0.3057, hi 0.5609, unit 805 of 1,879, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,879 805 69.5 42.8 40.6 to 45.1 30.6 to 56.1 below 46
row-record quake.prob.80_90: value 0.6252, lo 0.4905, hi 0.7568, unit 472 of 755, outcome BELOW, as printed: 80 to 90 percent, not including 90 755 472 84.9 62.5 59.0 to 65.9 49.0 to 75.7 below 37
row-record quake.prob.90_99: value 0.7747, lo 0.6691, hi 0.8604, unit 636 of 821, outcome BELOW, as printed: 90 to 99 percent, not including 99 821 636 95.2 77.5 74.5 to 80.2 66.9 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,902, outcome CONSISTENT, as printed: 63 of 31,902 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3115, lo 0.2431, hi 0.3866, unit 5,625 of 18,059, outcome BELOW, as printed: every magnitude, every window 18,059 5,625 41.8 31.1 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3034, lo 0.2309, hi 0.3835, unit 3,828 of 12,616, outcome BELOW, as printed: M3 and above 12,616 3,828 44.5 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2449, hi 0.4197, unit 1,797 of 5,443, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,443 1,797 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2375, lo 0.1387, hi 0.3385, unit 336 of 1,415, outcome BELOW, as printed: every magnitude, 1 day 1,415 336 36.1 23.8 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2101, lo 0.1302, hi 0.3087, unit 867 of 4,126, outcome BELOW, as printed: every magnitude, 1 week 4,126 867 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2375, lo 0.1646, hi 0.3263, unit 1,734 of 7,302, outcome BELOW, as printed: every magnitude, 1 month 7,302 1,734 39.6 23.8 22.8 to 24.7 16.5 to 32.6 below 74
row-record quake.prob10.year: value 0.5153, lo 0.4216, hi 0.6024, unit 2,688 of 5,216, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,216 2,688 50.7 51.5 50.2 to 52.9 42.2 to 60.2 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9291, lo 0.8824, hi 0.9565, unit 668 of 719, outcome CANNOT_TELL, as printed: 668 of 719 inside, 92.9 percent, with a sequence interval of 88.2 to 95.7 percent.

## 2026-11-14 18:33 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-14T23:12:04Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-14T23:12:04Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-14T23:12:04Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9622, lo 0.9459, hi 0.9775, unit 30,706 of 31,912, outcome CANNOT_TELL, as printed: M3 and above, every window 31,912 30,706 763 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,647
row-record quake.cover.m4: value 0.9854, lo 0.9784, hi 0.9936, unit 31,328 of 31,792, outcome ABOVE, as printed: M4 and above 31,792 31,328 458 6 98.5 98.4 to 98.7 97.8 to 99.4 above 81 22,748
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,802 of 31,912, outcome ABOVE, as printed: M5 and above 31,912 31,802 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,284
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,907 of 31,912, outcome ABOVE, as printed: M6 and above 31,912 31,907 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,459
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,911 of 31,912, outcome ABOVE, as printed: M7 and above 31,912 31,911 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,798
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,604 of 9,715, outcome ABOVE, as printed: M3 and above, 1 day 9,715 9,604 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,026
row-record quake.cover.m3.week: value 0.9743, lo 0.9597, hi 0.9839, unit 9,351 of 9,598, outcome ABOVE, as printed: M3 and above, 1 week 9,598 9,351 138 109 97.4 97.1 to 97.7 96.0 to 98.4 above 82 3,672
row-record quake.cover.m3.month: value 0.9585, lo 0.9393, hi 0.9757, unit 8,784 of 9,164, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,164 8,784 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 78 1,740
row-record quake.cover.m3.year: value 0.8638, lo 0.7912, hi 0.9416, unit 2,967 of 3,435, outcome BELOW, as printed: M3 and above, 1 year 3,435 2,967 342 126 86.4 85.2 to 87.5 79.1 to 94.2 below 42 209
row-record quake.cover.all: value 0.9888, lo 0.9848, hi 0.9934, unit 157,730 of 159,516, outcome ABOVE, as printed: every magnitude, every window 159,516 157,730 1,336 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,996
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,555, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,555 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.0173, hi 0.0492, unit 593 of 17,475, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,475 593 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0679, lo 0.046, hi 0.0917, unit 436 of 6,420, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,420 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1056, lo 0.0746, hi 0.1364, unit 601 of 5,692, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,692 601 14.4 10.6 9.8 to 11.4 7.5 to 13.6 below 77
row-record quake.prob.20_40: value 0.1941, lo 0.1523, hi 0.2375, unit 960 of 4,945, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,945 960 28.5 19.4 18.3 to 20.5 15.2 to 23.8 below 74
row-record quake.prob.40_60: value 0.3379, lo 0.2642, hi 0.4109, unit 915 of 2,708, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,708 915 49.3 33.8 32.0 to 35.6 26.4 to 41.1 below 58
row-record quake.prob.60_80: value 0.4284, lo 0.3057, hi 0.5609, unit 805 of 1,879, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,879 805 69.5 42.8 40.6 to 45.1 30.6 to 56.1 below 46
row-record quake.prob.80_90: value 0.6257, lo 0.4908, hi 0.758, unit 473 of 756, outcome BELOW, as printed: 80 to 90 percent, not including 90 756 473 84.9 62.6 59.1 to 65.9 49.1 to 75.8 below 37
row-record quake.prob.90_99: value 0.7747, lo 0.6691, hi 0.8604, unit 636 of 821, outcome BELOW, as printed: 90 to 99 percent, not including 99 821 636 95.2 77.5 74.5 to 80.2 66.9 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,912, outcome CONSISTENT, as printed: 63 of 31,912 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3115, lo 0.243, hi 0.3865, unit 5,627 of 18,066, outcome BELOW, as printed: every magnitude, every window 18,066 5,627 41.8 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3034, lo 0.2309, hi 0.3835, unit 3,830 of 12,622, outcome BELOW, as printed: M3 and above 12,622 3,830 44.5 30.3 29.5 to 31.1 23.1 to 38.4 below 77
row-record quake.prob10.m4up: value 0.3301, lo 0.2448, hi 0.4197, unit 1,797 of 5,444, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,444 1,797 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2373, lo 0.1386, hi 0.3385, unit 336 of 1,416, outcome BELOW, as printed: every magnitude, 1 day 1,416 336 36.0 23.7 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2103, lo 0.1303, hi 0.3087, unit 868 of 4,128, outcome BELOW, as printed: every magnitude, 1 week 4,128 868 36.7 21.0 19.8 to 22.3 13.0 to 30.9 below 73
row-record quake.prob10.month: value 0.2375, lo 0.1646, hi 0.3263, unit 1,735 of 7,306, outcome BELOW, as printed: every magnitude, 1 month 7,306 1,735 39.6 23.8 22.8 to 24.7 16.5 to 32.6 below 74
row-record quake.prob10.year: value 0.5153, lo 0.4216, hi 0.6024, unit 2,688 of 5,216, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,216 2,688 50.7 51.5 50.2 to 52.9 42.2 to 60.2 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9278, lo 0.88, hi 0.9551, unit 668 of 720, outcome CANNOT_TELL, as printed: 668 of 720 inside, 92.8 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-15 00:02 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-15T03:56:33Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-15T03:56:33Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-15T03:56:33Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9622, lo 0.9459, hi 0.9776, unit 30,715 of 31,921, outcome CANNOT_TELL, as printed: M3 and above, every window 31,921 30,715 763 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,651
row-record quake.cover.m4: value 0.9854, lo 0.9784, hi 0.9936, unit 31,337 of 31,801, outcome ABOVE, as printed: M4 and above 31,801 31,337 458 6 98.5 98.4 to 98.7 97.8 to 99.4 above 81 22,754
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,811 of 31,921, outcome ABOVE, as printed: M5 and above 31,921 31,811 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,293
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,916 of 31,921, outcome ABOVE, as printed: M6 and above 31,921 31,916 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,468
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,920 of 31,921, outcome ABOVE, as printed: M7 and above 31,921 31,920 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,807
row-record quake.cover.m3.day: value 0.9886, lo 0.9802, hi 0.9936, unit 9,608 of 9,719, outcome ABOVE, as printed: M3 and above, 1 day 9,719 9,608 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,029
row-record quake.cover.m3.week: value 0.9743, lo 0.9597, hi 0.9839, unit 9,352 of 9,599, outcome ABOVE, as printed: M3 and above, 1 week 9,599 9,352 138 109 97.4 97.1 to 97.7 96.0 to 98.4 above 82 3,672
row-record quake.cover.m3.month: value 0.9585, lo 0.9393, hi 0.9757, unit 8,786 of 9,166, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,166 8,786 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 78 1,740
row-record quake.cover.m3.year: value 0.8638, lo 0.7914, hi 0.9416, unit 2,969 of 3,437, outcome BELOW, as printed: M3 and above, 1 year 3,437 2,969 342 126 86.4 85.2 to 87.5 79.1 to 94.2 below 42 210
row-record quake.cover.all: value 0.9888, lo 0.9848, hi 0.9934, unit 157,775 of 159,561, outcome ABOVE, as printed: every magnitude, every window 159,561 157,775 1,336 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,033
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,588, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,588 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.0173, hi 0.0492, unit 593 of 17,480, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,480 593 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0679, lo 0.046, hi 0.0917, unit 436 of 6,421, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,421 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1055, lo 0.0745, hi 0.1363, unit 601 of 5,695, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,695 601 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1941, lo 0.1523, hi 0.2375, unit 960 of 4,946, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,946 960 28.5 19.4 18.3 to 20.5 15.2 to 23.8 below 74
row-record quake.prob.40_60: value 0.3376, lo 0.2639, hi 0.4105, unit 915 of 2,710, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,710 915 49.4 33.8 32.0 to 35.6 26.4 to 41.0 below 58
row-record quake.prob.60_80: value 0.4284, lo 0.3057, hi 0.5609, unit 805 of 1,879, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,879 805 69.5 42.8 40.6 to 45.1 30.6 to 56.1 below 46
row-record quake.prob.80_90: value 0.6257, lo 0.4908, hi 0.758, unit 473 of 756, outcome BELOW, as printed: 80 to 90 percent, not including 90 756 473 84.9 62.6 59.1 to 65.9 49.1 to 75.8 below 37
row-record quake.prob.90_99: value 0.7747, lo 0.6691, hi 0.8604, unit 636 of 821, outcome BELOW, as printed: 90 to 99 percent, not including 99 821 636 95.2 77.5 74.5 to 80.2 66.9 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,921, outcome CONSISTENT, as printed: 63 of 31,921 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3114, lo 0.2429, hi 0.3865, unit 5,627 of 18,072, outcome BELOW, as printed: every magnitude, every window 18,072 5,627 41.8 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3033, lo 0.2309, hi 0.3834, unit 3,830 of 12,626, outcome BELOW, as printed: M3 and above 12,626 3,830 44.5 30.3 29.5 to 31.1 23.1 to 38.3 below 77
row-record quake.prob10.m4up: value 0.33, lo 0.2447, hi 0.4196, unit 1,797 of 5,446, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,446 1,797 35.6 33.0 31.8 to 34.3 24.5 to 42.0 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2371, lo 0.1386, hi 0.3385, unit 336 of 1,417, outcome BELOW, as printed: every magnitude, 1 day 1,417 336 36.0 23.7 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2102, lo 0.1301, hi 0.3082, unit 868 of 4,130, outcome BELOW, as printed: every magnitude, 1 week 4,130 868 36.7 21.0 19.8 to 22.3 13.0 to 30.8 below 73
row-record quake.prob10.month: value 0.2374, lo 0.1646, hi 0.3263, unit 1,735 of 7,307, outcome BELOW, as printed: every magnitude, 1 month 7,307 1,735 39.6 23.7 22.8 to 24.7 16.5 to 32.6 below 74
row-record quake.prob10.year: value 0.5151, lo 0.4215, hi 0.6021, unit 2,688 of 5,218, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,218 2,688 50.7 51.5 50.2 to 52.9 42.1 to 60.2 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9278, lo 0.88, hi 0.9551, unit 668 of 720, outcome CANNOT_TELL, as printed: 668 of 720 inside, 92.8 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-15 09:35 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-15T14:21:38Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-15T14:21:38Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-15T14:21:38Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9623, lo 0.9459, hi 0.9776, unit 30,748 of 31,954, outcome CANNOT_TELL, as printed: M3 and above, every window 31,954 30,748 763 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,661
row-record quake.cover.m4: value 0.9854, lo 0.9784, hi 0.9935, unit 31,368 of 31,834, outcome ABOVE, as printed: M4 and above 31,834 31,368 460 6 98.5 98.4 to 98.7 97.8 to 99.4 above 81 22,775
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,844 of 31,954, outcome ABOVE, as printed: M5 and above 31,954 31,844 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,323
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,949 of 31,954, outcome ABOVE, as printed: M6 and above 31,954 31,949 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,501
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,953 of 31,954, outcome ABOVE, as printed: M7 and above 31,954 31,953 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,840
row-record quake.cover.m3.day: value 0.9886, lo 0.9803, hi 0.9936, unit 9,615 of 9,726, outcome ABOVE, as printed: M3 and above, 1 day 9,726 9,615 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,036
row-record quake.cover.m3.week: value 0.9743, lo 0.9597, hi 0.9839, unit 9,359 of 9,606, outcome ABOVE, as printed: M3 and above, 1 week 9,606 9,359 138 109 97.4 97.1 to 97.7 96.0 to 98.4 above 82 3,674
row-record quake.cover.m3.month: value 0.9586, lo 0.9393, hi 0.9757, unit 8,795 of 9,175, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,175 8,795 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 78 1,741
row-record quake.cover.m3.year: value 0.8642, lo 0.7924, hi 0.9417, unit 2,979 of 3,447, outcome BELOW, as printed: M3 and above, 1 year 3,447 2,979 342 126 86.4 85.2 to 87.5 79.2 to 94.2 below 42 210
row-record quake.cover.all: value 0.9888, lo 0.9848, hi 0.9934, unit 157,938 of 159,726, outcome ABOVE, as printed: every magnitude, every window 159,726 157,938 1,338 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,160
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,702, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,702 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.0173, hi 0.0491, unit 593 of 17,502, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,502 593 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0678, lo 0.0458, hi 0.0918, unit 436 of 6,427, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,427 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1056, lo 0.0744, hi 0.1362, unit 602 of 5,703, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,703 602 14.4 10.6 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1939, lo 0.1522, hi 0.2371, unit 960 of 4,951, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,951 960 28.5 19.4 18.3 to 20.5 15.2 to 23.7 below 74
row-record quake.prob.40_60: value 0.3387, lo 0.2644, hi 0.4116, unit 920 of 2,716, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,716 920 49.4 33.9 32.1 to 35.7 26.4 to 41.2 below 58
row-record quake.prob.60_80: value 0.4282, lo 0.3056, hi 0.5606, unit 805 of 1,880, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,880 805 69.5 42.8 40.6 to 45.1 30.6 to 56.1 below 46
row-record quake.prob.80_90: value 0.6248, lo 0.4899, hi 0.758, unit 473 of 757, outcome BELOW, as printed: 80 to 90 percent, not including 90 757 473 84.9 62.5 59.0 to 65.9 49.0 to 75.8 below 37
row-record quake.prob.90_99: value 0.774, lo 0.6684, hi 0.8606, unit 637 of 823, outcome BELOW, as printed: 90 to 99 percent, not including 99 823 637 95.2 77.4 74.4 to 80.1 66.8 to 86.1 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,954, outcome CONSISTENT, as printed: 63 of 31,954 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3114, lo 0.243, hi 0.3866, unit 5,634 of 18,095, outcome BELOW, as printed: every magnitude, every window 18,095 5,634 41.8 31.1 30.5 to 31.8 24.3 to 38.7 below 77
row-record quake.prob10.m3: value 0.3034, lo 0.2307, hi 0.3833, unit 3,836 of 12,642, outcome BELOW, as printed: M3 and above 12,642 3,836 44.5 30.3 29.5 to 31.1 23.1 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3297, lo 0.2446, hi 0.4194, unit 1,798 of 5,453, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,453 1,798 35.5 33.0 31.7 to 34.2 24.5 to 41.9 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2371, lo 0.1386, hi 0.3385, unit 336 of 1,417, outcome BELOW, as printed: every magnitude, 1 day 1,417 336 36.0 23.7 21.6 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.21, lo 0.13, hi 0.3078, unit 868 of 4,133, outcome BELOW, as printed: every magnitude, 1 week 4,133 868 36.7 21.0 19.8 to 22.3 13.0 to 30.8 below 73
row-record quake.prob10.month: value 0.2375, lo 0.1646, hi 0.3259, unit 1,737 of 7,313, outcome BELOW, as printed: every magnitude, 1 month 7,313 1,737 39.6 23.8 22.8 to 24.7 16.5 to 32.6 below 74
row-record quake.prob10.year: value 0.5147, lo 0.4217, hi 0.6016, unit 2,693 of 5,232, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,232 2,693 50.6 51.5 50.1 to 52.8 42.2 to 60.2 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9278, lo 0.88, hi 0.9551, unit 668 of 720, outcome CANNOT_TELL, as printed: 668 of 720 inside, 92.8 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-15 21:16 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-16T01:07:36Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-16T01:07:36Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-16T01:07:36Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9623, lo 0.9459, hi 0.9776, unit 30,774 of 31,981, outcome CANNOT_TELL, as printed: M3 and above, every window 31,981 30,774 764 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,669
row-record quake.cover.m4: value 0.9853, lo 0.9784, hi 0.9935, unit 31,394 of 31,861, outcome ABOVE, as printed: M4 and above 31,861 31,394 461 6 98.5 98.4 to 98.7 97.8 to 99.4 above 81 22,792
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,871 of 31,981, outcome ABOVE, as printed: M5 and above 31,981 31,871 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,349
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,976 of 31,981, outcome ABOVE, as printed: M6 and above 31,981 31,976 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,528
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,980 of 31,981, outcome ABOVE, as printed: M7 and above 31,981 31,980 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,867
row-record quake.cover.m3.day: value 0.9886, lo 0.9803, hi 0.9936, unit 9,622 of 9,733, outcome ABOVE, as printed: M3 and above, 1 day 9,733 9,622 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,039
row-record quake.cover.m3.week: value 0.9742, lo 0.9596, hi 0.9837, unit 9,366 of 9,614, outcome ABOVE, as printed: M3 and above, 1 week 9,614 9,366 139 109 97.4 97.1 to 97.7 96.0 to 98.4 above 82 3,678
row-record quake.cover.m3.month: value 0.9586, lo 0.9394, hi 0.9757, unit 8,802 of 9,182, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,182 8,802 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 78 1,742
row-record quake.cover.m3.year: value 0.8644, lo 0.7926, hi 0.9418, unit 2,984 of 3,452, outcome BELOW, as printed: M3 and above, 1 year 3,452 2,984 342 126 86.4 85.3 to 87.5 79.3 to 94.2 below 42 210
row-record quake.cover.all: value 0.9888, lo 0.9848, hi 0.9933, unit 158,071 of 159,861, outcome ABOVE, as printed: every magnitude, every window 159,861 158,071 1,340 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,265
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,797, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,797 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.0172, hi 0.0492, unit 594 of 17,519, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,519 594 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0678, lo 0.0458, hi 0.0917, unit 436 of 6,431, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,431 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1054, lo 0.0743, hi 0.1361, unit 602 of 5,710, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,710 602 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1941, lo 0.1523, hi 0.2374, unit 962 of 4,956, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,956 962 28.5 19.4 18.3 to 20.5 15.2 to 23.7 below 74
row-record quake.prob.40_60: value 0.3387, lo 0.2642, hi 0.4119, unit 921 of 2,719, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,719 921 49.4 33.9 32.1 to 35.7 26.4 to 41.2 below 58
row-record quake.prob.60_80: value 0.428, lo 0.3052, hi 0.5609, unit 806 of 1,883, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,883 806 69.5 42.8 40.6 to 45.1 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.624, lo 0.4888, hi 0.7568, unit 473 of 758, outcome BELOW, as printed: 80 to 90 percent, not including 90 758 473 84.9 62.4 58.9 to 65.8 48.9 to 75.7 below 37
row-record quake.prob.90_99: value 0.774, lo 0.6684, hi 0.8606, unit 637 of 823, outcome BELOW, as printed: 90 to 99 percent, not including 99 823 637 95.2 77.4 74.4 to 80.1 66.8 to 86.1 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,237 of 1,265, outcome BELOW, as printed: 99 to 100 percent 1,265 1,237 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 31,981, outcome CONSISTENT, as printed: 63 of 31,981 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3113, lo 0.2429, hi 0.3865, unit 5,638 of 18,114, outcome BELOW, as printed: every magnitude, every window 18,114 5,638 41.8 31.1 30.4 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3034, lo 0.2307, hi 0.3832, unit 3,840 of 12,656, outcome BELOW, as printed: M3 and above 12,656 3,840 44.5 30.3 29.5 to 31.1 23.1 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3294, lo 0.2443, hi 0.4193, unit 1,798 of 5,458, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,458 1,798 35.5 32.9 31.7 to 34.2 24.4 to 41.9 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2368, lo 0.1385, hi 0.3385, unit 336 of 1,419, outcome BELOW, as printed: every magnitude, 1 day 1,419 336 36.0 23.7 21.5 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2101, lo 0.1299, hi 0.3077, unit 869 of 4,137, outcome BELOW, as printed: every magnitude, 1 week 4,137 869 36.7 21.0 19.8 to 22.3 13.0 to 30.8 below 73
row-record quake.prob10.month: value 0.2373, lo 0.1645, hi 0.3258, unit 1,737 of 7,319, outcome BELOW, as printed: every magnitude, 1 month 7,319 1,737 39.6 23.7 22.8 to 24.7 16.4 to 32.6 below 74
row-record quake.prob10.year: value 0.5146, lo 0.4212, hi 0.6012, unit 2,696 of 5,239, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,239 2,696 50.6 51.5 50.1 to 52.8 42.1 to 60.1 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9279, lo 0.8802, hi 0.9552, unit 669 of 721, outcome CANNOT_TELL, as printed: 669 of 721 inside, 92.8 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-16 04:42 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-16T03:26:53Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-16T03:26:53Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-16T03:26:53Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9622, lo 0.9458, hi 0.9776, unit 30,778 of 31,986, outcome CANNOT_TELL, as printed: M3 and above, every window 31,986 30,778 765 443 96.2 96.0 to 96.4 94.6 to 97.8 cannot tell (STRADDLES_EDGE) 82 12,672
row-record quake.cover.m4: value 0.9853, lo 0.9784, hi 0.9935, unit 31,399 of 31,866, outcome ABOVE, as printed: M4 and above 31,866 31,399 461 6 98.5 98.4 to 98.7 97.8 to 99.4 above 81 22,795
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,876 of 31,986, outcome ABOVE, as printed: M5 and above 31,986 31,876 109 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,353
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,981 of 31,986, outcome ABOVE, as printed: M6 and above 31,986 31,981 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,533
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,985 of 31,986, outcome ABOVE, as printed: M7 and above 31,986 31,985 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,872
row-record quake.cover.m3.day: value 0.9886, lo 0.9803, hi 0.9936, unit 9,622 of 9,733, outcome ABOVE, as printed: M3 and above, 1 day 9,733 9,622 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,039
row-record quake.cover.m3.week: value 0.9742, lo 0.9596, hi 0.9837, unit 9,367 of 9,615, outcome ABOVE, as printed: M3 and above, 1 week 9,615 9,367 139 109 97.4 97.1 to 97.7 96.0 to 98.4 above 82 3,679
row-record quake.cover.m3.month: value 0.9586, lo 0.9394, hi 0.9757, unit 8,804 of 9,184, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,184 8,804 230 150 95.9 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 78 1,744
row-record quake.cover.m3.year: value 0.8642, lo 0.7922, hi 0.9418, unit 2,985 of 3,454, outcome BELOW, as printed: M3 and above, 1 year 3,454 2,985 343 126 86.4 85.2 to 87.5 79.2 to 94.2 below 42 210
row-record quake.cover.all: value 0.9888, lo 0.9848, hi 0.9933, unit 158,095 of 159,886, outcome ABOVE, as printed: every magnitude, every window 159,886 158,095 1,341 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 128,285
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,815, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,815 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.0172, hi 0.0491, unit 594 of 17,522, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,522 594 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0678, lo 0.0458, hi 0.0917, unit 436 of 6,432, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,432 436 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1054, lo 0.0743, hi 0.1361, unit 602 of 5,710, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,710 602 14.4 10.5 9.8 to 11.4 7.4 to 13.6 below 77
row-record quake.prob.20_40: value 0.1943, lo 0.1523, hi 0.2378, unit 963 of 4,957, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,957 963 28.5 19.4 18.4 to 20.5 15.2 to 23.8 below 74
row-record quake.prob.40_60: value 0.339, lo 0.2646, hi 0.4121, unit 922 of 2,720, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,720 922 49.4 33.9 32.1 to 35.7 26.5 to 41.2 below 58
row-record quake.prob.60_80: value 0.428, lo 0.3052, hi 0.5609, unit 806 of 1,883, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,883 806 69.5 42.8 40.6 to 45.1 30.5 to 56.1 below 46
row-record quake.prob.80_90: value 0.624, lo 0.4888, hi 0.7568, unit 473 of 758, outcome BELOW, as printed: 80 to 90 percent, not including 90 758 473 84.9 62.4 58.9 to 65.8 48.9 to 75.7 below 37
row-record quake.prob.90_99: value 0.774, lo 0.6684, hi 0.8606, unit 637 of 823, outcome BELOW, as printed: 90 to 99 percent, not including 99 823 637 95.2 77.4 74.4 to 80.1 66.8 to 86.1 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,238 of 1,266, outcome BELOW, as printed: 99 to 100 percent 1,266 1,238 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0044, unit 63 of 31,986, outcome CONSISTENT, as printed: 63 of 31,986 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3114, lo 0.2431, hi 0.3865, unit 5,641 of 18,117, outcome BELOW, as printed: every magnitude, every window 18,117 5,641 41.8 31.1 30.5 to 31.8 24.3 to 38.6 below 77
row-record quake.prob10.m3: value 0.3035, lo 0.2307, hi 0.3833, unit 3,842 of 12,658, outcome BELOW, as printed: M3 and above 12,658 3,842 44.5 30.3 29.6 to 31.2 23.1 to 38.3 below 77
row-record quake.prob10.m4up: value 0.3295, lo 0.2444, hi 0.4193, unit 1,799 of 5,459, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,459 1,799 35.5 33.0 31.7 to 34.2 24.4 to 41.9 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2368, lo 0.1385, hi 0.3385, unit 336 of 1,419, outcome BELOW, as printed: every magnitude, 1 day 1,419 336 36.0 23.7 21.5 to 26.0 13.9 to 33.9 below 54
row-record quake.prob10.week: value 0.2101, lo 0.1299, hi 0.3077, unit 869 of 4,137, outcome BELOW, as printed: every magnitude, 1 week 4,137 869 36.7 21.0 19.8 to 22.3 13.0 to 30.8 below 73
row-record quake.prob10.month: value 0.2373, lo 0.1645, hi 0.3258, unit 1,737 of 7,319, outcome BELOW, as printed: every magnitude, 1 month 7,319 1,737 39.6 23.7 22.8 to 24.7 16.4 to 32.6 below 74
row-record quake.prob10.year: value 0.5149, lo 0.4215, hi 0.6017, unit 2,699 of 5,242, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,242 2,699 50.6 51.5 50.1 to 52.8 42.1 to 60.2 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9279, lo 0.8802, hi 0.9552, unit 669 of 721, outcome CANNOT_TELL, as printed: 669 of 721 inside, 92.8 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-16 08:03 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-16T11:57:34Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-16T11:57:34Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-16T11:57:34Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.962, lo 0.9456, hi 0.9774, unit 30,541 of 31,749, outcome CANNOT_TELL, as printed: M3 and above, every window 31,749 30,541 765 443 96.2 96.0 to 96.4 94.6 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,638
row-record quake.cover.m4: value 0.9852, lo 0.9783, hi 0.9935, unit 31,162 of 31,629, outcome ABOVE, as printed: M4 and above 31,629 31,162 461 6 98.5 98.4 to 98.7 97.8 to 99.4 above 81 22,681
row-record quake.cover.m5: value 0.9967, lo 0.9938, hi 0.9989, unit 31,643 of 31,749, outcome ABOVE, as printed: M5 and above 31,749 31,643 105 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,158
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,744 of 31,749, outcome ABOVE, as printed: M6 and above 31,749 31,744 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,296
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,748 of 31,749, outcome ABOVE, as printed: M7 and above 31,749 31,748 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,635
row-record quake.cover.m3.day: value 0.9885, lo 0.9801, hi 0.9935, unit 9,563 of 9,674, outcome ABOVE, as printed: M3 and above, 1 day 9,674 9,563 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,002
row-record quake.cover.m3.week: value 0.974, lo 0.9594, hi 0.9836, unit 9,308 of 9,556, outcome ABOVE, as printed: M3 and above, 1 week 9,556 9,308 139 109 97.4 97.1 to 97.7 95.9 to 98.4 above 82 3,682
row-record quake.cover.m3.month: value 0.9584, lo 0.939, hi 0.9756, unit 8,744 of 9,124, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,124 8,744 230 150 95.8 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 78 1,744
row-record quake.cover.m3.year: value 0.8619, lo 0.7898, hi 0.9396, unit 2,926 of 3,395, outcome BELOW, as printed: M3 and above, 1 year 3,395 2,926 343 126 86.2 85.0 to 87.3 79.0 to 94.0 below 42 210
row-record quake.cover.all: value 0.9887, lo 0.9847, hi 0.9933, unit 156,914 of 158,701, outcome ABOVE, as printed: every magnitude, every window 158,701 156,914 1,337 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,468
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 304 of 117,100, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,100 304 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.017, hi 0.0492, unit 586 of 17,353, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,353 586 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0461, hi 0.0921, unit 434 of 6,372, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,372 434 7.1 6.8 6.2 to 7.5 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1035, lo 0.0715, hi 0.1346, unit 582 of 5,625, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,625 582 14.3 10.3 9.6 to 11.2 7.1 to 13.5 below 77
row-record quake.prob.20_40: value 0.192, lo 0.1491, hi 0.2361, unit 939 of 4,891, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,891 939 28.5 19.2 18.1 to 20.3 14.9 to 23.6 below 74
row-record quake.prob.40_60: value 0.3383, lo 0.2625, hi 0.4116, unit 909 of 2,687, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,687 909 49.3 33.8 32.1 to 35.6 26.2 to 41.2 below 58
row-record quake.prob.60_80: value 0.425, lo 0.3016, hi 0.561, unit 782 of 1,840, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,840 782 69.6 42.5 40.3 to 44.8 30.2 to 56.1 below 46
row-record quake.prob.80_90: value 0.6353, lo 0.4939, hi 0.7727, unit 472 of 743, outcome BELOW, as printed: 80 to 90 percent, not including 90 743 472 85.0 63.5 60.0 to 66.9 49.4 to 77.3 below 37
row-record quake.prob.90_99: value 0.7731, lo 0.6684, hi 0.86, unit 637 of 824, outcome BELOW, as printed: 90 to 99 percent, not including 99 824 637 95.2 77.3 74.3 to 80.0 66.8 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,238 of 1,266, outcome BELOW, as printed: 99 to 100 percent 1,266 1,238 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 63 of 31,749, outcome CONSISTENT, as printed: 63 of 31,749 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.311, lo 0.2425, hi 0.387, unit 5,559 of 17,876, outcome BELOW, as printed: every magnitude, every window 17,876 5,559 41.9 31.1 30.4 to 31.8 24.2 to 38.7 below 77
row-record quake.prob10.m3: value 0.3042, lo 0.2307, hi 0.3852, unit 3,802 of 12,499, outcome BELOW, as printed: M3 and above 12,499 3,802 44.5 30.4 29.6 to 31.2 23.1 to 38.5 below 77
row-record quake.prob10.m4up: value 0.3268, lo 0.2415, hi 0.4171, unit 1,757 of 5,377, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,377 1,757 35.7 32.7 31.4 to 33.9 24.1 to 41.7 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2386, lo 0.14, hi 0.3404, unit 336 of 1,408, outcome BELOW, as printed: every magnitude, 1 day 1,408 336 36.1 23.9 21.7 to 26.2 14.0 to 34.0 below 54
row-record quake.prob10.week: value 0.2116, lo 0.1314, hi 0.3092, unit 869 of 4,106, outcome BELOW, as printed: every magnitude, 1 week 4,106 869 36.8 21.2 19.9 to 22.4 13.1 to 30.9 below 73
row-record quake.prob10.month: value 0.239, lo 0.1654, hi 0.3289, unit 1,730 of 7,240, outcome BELOW, as printed: every magnitude, 1 month 7,240 1,730 39.6 23.9 22.9 to 24.9 16.5 to 32.9 below 74
row-record quake.prob10.year: value 0.5123, lo 0.4177, hi 0.601, unit 2,624 of 5,122, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,122 2,624 50.7 51.2 49.9 to 52.6 41.8 to 60.1 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9275, lo 0.8795, hi 0.9547, unit 665 of 717, outcome CANNOT_TELL, as printed: 665 of 717 inside, 92.8 percent, with a sequence interval of 87.9 to 95.5 percent.

## 2026-11-16 11:57 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-16T14:14:11Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-16T14:14:11Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-16T14:14:11Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9619, lo 0.9456, hi 0.9774, unit 30,549 of 31,758, outcome CANNOT_TELL, as printed: M3 and above, every window 31,758 30,549 766 443 96.2 96.0 to 96.4 94.6 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,640
row-record quake.cover.m4: value 0.9852, lo 0.9782, hi 0.9935, unit 31,170 of 31,638, outcome ABOVE, as printed: M4 and above 31,638 31,170 462 6 98.5 98.4 to 98.7 97.8 to 99.4 above 81 22,690
row-record quake.cover.m5: value 0.9966, lo 0.9938, hi 0.9989, unit 31,651 of 31,758, outcome ABOVE, as printed: M5 and above 31,758 31,651 106 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,167
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,753 of 31,758, outcome ABOVE, as printed: M6 and above 31,758 31,753 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,305
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,757 of 31,758, outcome ABOVE, as printed: M7 and above 31,758 31,757 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,644
row-record quake.cover.m3.day: value 0.9885, lo 0.9801, hi 0.9935, unit 9,564 of 9,675, outcome ABOVE, as printed: M3 and above, 1 day 9,675 9,564 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,003
row-record quake.cover.m3.week: value 0.9741, lo 0.9594, hi 0.9836, unit 9,310 of 9,558, outcome ABOVE, as printed: M3 and above, 1 week 9,558 9,310 139 109 97.4 97.1 to 97.7 95.9 to 98.4 above 82 3,682
row-record quake.cover.m3.month: value 0.9584, lo 0.9391, hi 0.9756, unit 8,747 of 9,127, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,127 8,747 230 150 95.8 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 78 1,744
row-record quake.cover.m3.year: value 0.8617, lo 0.7896, hi 0.9396, unit 2,928 of 3,398, outcome BELOW, as printed: M3 and above, 1 year 3,398 2,928 344 126 86.2 85.0 to 87.3 79.0 to 94.0 below 42 211
row-record quake.cover.all: value 0.9887, lo 0.9847, hi 0.9933, unit 156,956 of 158,746, outcome ABOVE, as printed: every magnitude, every window 158,746 156,956 1,340 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,506
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,134, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,134 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.017, hi 0.0494, unit 587 of 17,360, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,360 587 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0461, hi 0.0921, unit 434 of 6,374, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,374 434 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1036, lo 0.0718, hi 0.1347, unit 583 of 5,627, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,627 583 14.3 10.4 9.6 to 11.2 7.2 to 13.5 below 77
row-record quake.prob.20_40: value 0.192, lo 0.1491, hi 0.2361, unit 939 of 4,891, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,891 939 28.5 19.2 18.1 to 20.3 14.9 to 23.6 below 74
row-record quake.prob.40_60: value 0.3383, lo 0.2625, hi 0.4116, unit 909 of 2,687, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,687 909 49.3 33.8 32.1 to 35.6 26.2 to 41.2 below 58
row-record quake.prob.60_80: value 0.425, lo 0.3016, hi 0.561, unit 782 of 1,840, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,840 782 69.6 42.5 40.3 to 44.8 30.2 to 56.1 below 46
row-record quake.prob.80_90: value 0.6353, lo 0.4939, hi 0.7727, unit 472 of 743, outcome BELOW, as printed: 80 to 90 percent, not including 90 743 472 85.0 63.5 60.0 to 66.9 49.4 to 77.3 below 37
row-record quake.prob.90_99: value 0.7731, lo 0.6684, hi 0.86, unit 637 of 824, outcome BELOW, as printed: 90 to 99 percent, not including 99 824 637 95.2 77.3 74.3 to 80.0 66.8 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,238 of 1,266, outcome BELOW, as printed: 99 to 100 percent 1,266 1,238 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 64 of 31,758, outcome CONSISTENT, as printed: 64 of 31,758 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.311, lo 0.2425, hi 0.387, unit 5,560 of 17,878, outcome BELOW, as printed: every magnitude, every window 17,878 5,560 41.9 31.1 30.4 to 31.8 24.2 to 38.7 below 77
row-record quake.prob10.m3: value 0.3042, lo 0.2308, hi 0.3852, unit 3,803 of 12,501, outcome BELOW, as printed: M3 and above 12,501 3,803 44.5 30.4 29.6 to 31.2 23.1 to 38.5 below 77
row-record quake.prob10.m4up: value 0.3268, lo 0.2415, hi 0.4171, unit 1,757 of 5,377, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,377 1,757 35.7 32.7 31.4 to 33.9 24.1 to 41.7 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2386, lo 0.14, hi 0.3404, unit 336 of 1,408, outcome BELOW, as printed: every magnitude, 1 day 1,408 336 36.1 23.9 21.7 to 26.2 14.0 to 34.0 below 54
row-record quake.prob10.week: value 0.2116, lo 0.1314, hi 0.3092, unit 869 of 4,106, outcome BELOW, as printed: every magnitude, 1 week 4,106 869 36.8 21.2 19.9 to 22.4 13.1 to 30.9 below 73
row-record quake.prob10.month: value 0.239, lo 0.1654, hi 0.3289, unit 1,730 of 7,240, outcome BELOW, as printed: every magnitude, 1 month 7,240 1,730 39.6 23.9 22.9 to 24.9 16.5 to 32.9 below 74
row-record quake.prob10.year: value 0.5123, lo 0.4179, hi 0.6007, unit 2,625 of 5,124, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,124 2,625 50.7 51.2 49.9 to 52.6 41.8 to 60.1 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9275, lo 0.8795, hi 0.9547, unit 665 of 717, outcome CANNOT_TELL, as printed: 665 of 717 inside, 92.8 percent, with a sequence interval of 87.9 to 95.5 percent.

## 2026-11-16 15:25 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-16T19:15:42Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-16T19:15:42Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-16T19:15:42Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9619, lo 0.9456, hi 0.9774, unit 30,557 of 31,766, outcome CANNOT_TELL, as printed: M3 and above, every window 31,766 30,557 766 443 96.2 96.0 to 96.4 94.6 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,642
row-record quake.cover.m4: value 0.9852, lo 0.9782, hi 0.9935, unit 31,178 of 31,646, outcome ABOVE, as printed: M4 and above 31,646 31,178 462 6 98.5 98.4 to 98.7 97.8 to 99.4 above 81 22,694
row-record quake.cover.m5: value 0.9966, lo 0.9938, hi 0.9989, unit 31,659 of 31,766, outcome ABOVE, as printed: M5 and above 31,766 31,659 106 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,174
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,761 of 31,766, outcome ABOVE, as printed: M6 and above 31,766 31,761 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,313
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,765 of 31,766, outcome ABOVE, as printed: M7 and above 31,766 31,765 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,652
row-record quake.cover.m3.day: value 0.9885, lo 0.9801, hi 0.9935, unit 9,565 of 9,676, outcome ABOVE, as printed: M3 and above, 1 day 9,676 9,565 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,003
row-record quake.cover.m3.week: value 0.9741, lo 0.9595, hi 0.9836, unit 9,313 of 9,561, outcome ABOVE, as printed: M3 and above, 1 week 9,561 9,313 139 109 97.4 97.1 to 97.7 96.0 to 98.4 above 82 3,684
row-record quake.cover.m3.month: value 0.9584, lo 0.9391, hi 0.9756, unit 8,748 of 9,128, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,128 8,748 230 150 95.8 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 78 1,744
row-record quake.cover.m3.year: value 0.8618, lo 0.7898, hi 0.9397, unit 2,931 of 3,401, outcome BELOW, as printed: M3 and above, 1 year 3,401 2,931 344 126 86.2 85.0 to 87.3 79.0 to 94.0 below 42 211
row-record quake.cover.all: value 0.9887, lo 0.9847, hi 0.9933, unit 156,996 of 158,786, outcome ABOVE, as printed: every magnitude, every window 158,786 156,996 1,340 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,535
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,159, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,159 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.017, hi 0.0493, unit 587 of 17,368, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,368 587 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0461, hi 0.092, unit 434 of 6,376, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,376 434 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1036, lo 0.0718, hi 0.1347, unit 583 of 5,627, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,627 583 14.3 10.4 9.6 to 11.2 7.2 to 13.5 below 77
row-record quake.prob.20_40: value 0.1919, lo 0.149, hi 0.2361, unit 939 of 4,894, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,894 939 28.5 19.2 18.1 to 20.3 14.9 to 23.6 below 74
row-record quake.prob.40_60: value 0.3382, lo 0.2624, hi 0.4114, unit 909 of 2,688, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,688 909 49.3 33.8 32.0 to 35.6 26.2 to 41.1 below 58
row-record quake.prob.60_80: value 0.4253, lo 0.3018, hi 0.5616, unit 783 of 1,841, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,841 783 69.6 42.5 40.3 to 44.8 30.2 to 56.2 below 46
row-record quake.prob.80_90: value 0.6353, lo 0.4939, hi 0.7727, unit 472 of 743, outcome BELOW, as printed: 80 to 90 percent, not including 90 743 472 85.0 63.5 60.0 to 66.9 49.4 to 77.3 below 37
row-record quake.prob.90_99: value 0.7731, lo 0.6684, hi 0.86, unit 637 of 824, outcome BELOW, as printed: 90 to 99 percent, not including 99 824 637 95.2 77.3 74.3 to 80.0 66.8 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,238 of 1,266, outcome BELOW, as printed: 99 to 100 percent 1,266 1,238 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 64 of 31,766, outcome CONSISTENT, as printed: 64 of 31,766 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.311, lo 0.2424, hi 0.387, unit 5,561 of 17,883, outcome BELOW, as printed: every magnitude, every window 17,883 5,561 41.9 31.1 30.4 to 31.8 24.2 to 38.7 below 77
row-record quake.prob10.m3: value 0.3042, lo 0.2308, hi 0.3851, unit 3,804 of 12,505, outcome BELOW, as printed: M3 and above 12,505 3,804 44.5 30.4 29.6 to 31.2 23.1 to 38.5 below 77
row-record quake.prob10.m4up: value 0.3267, lo 0.2415, hi 0.4171, unit 1,757 of 5,378, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,378 1,757 35.7 32.7 31.4 to 33.9 24.1 to 41.7 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2386, lo 0.14, hi 0.3404, unit 336 of 1,408, outcome BELOW, as printed: every magnitude, 1 day 1,408 336 36.1 23.9 21.7 to 26.2 14.0 to 34.0 below 54
row-record quake.prob10.week: value 0.2116, lo 0.1313, hi 0.3091, unit 869 of 4,107, outcome BELOW, as printed: every magnitude, 1 week 4,107 869 36.8 21.2 19.9 to 22.4 13.1 to 30.9 below 73
row-record quake.prob10.month: value 0.2389, lo 0.1654, hi 0.3289, unit 1,730 of 7,241, outcome BELOW, as printed: every magnitude, 1 month 7,241 1,730 39.6 23.9 22.9 to 24.9 16.5 to 32.9 below 74
row-record quake.prob10.year: value 0.5122, lo 0.4178, hi 0.6003, unit 2,626 of 5,127, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,127 2,626 50.7 51.2 49.9 to 52.6 41.8 to 60.0 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9275, lo 0.8795, hi 0.9547, unit 665 of 717, outcome CANNOT_TELL, as printed: 665 of 717 inside, 92.8 percent, with a sequence interval of 87.9 to 95.5 percent.

## 2026-11-16 18:45 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-16T21:32:09Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-16T21:32:09Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-16T21:32:09Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9619, lo 0.9455, hi 0.9773, unit 30,562 of 31,772, outcome CANNOT_TELL, as printed: M3 and above, every window 31,772 30,562 767 443 96.2 96.0 to 96.4 94.5 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,645
row-record quake.cover.m4: value 0.9852, lo 0.9781, hi 0.9935, unit 31,183 of 31,652, outcome ABOVE, as printed: M4 and above 31,652 31,183 463 6 98.5 98.4 to 98.7 97.8 to 99.4 above 81 22,698
row-record quake.cover.m5: value 0.9966, lo 0.9938, hi 0.9989, unit 31,665 of 31,772, outcome ABOVE, as printed: M5 and above 31,772 31,665 106 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,180
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,767 of 31,772, outcome ABOVE, as printed: M6 and above 31,772 31,767 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,319
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,771 of 31,772, outcome ABOVE, as printed: M7 and above 31,772 31,771 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,658
row-record quake.cover.m3.day: value 0.9885, lo 0.9801, hi 0.9935, unit 9,568 of 9,679, outcome ABOVE, as printed: M3 and above, 1 day 9,679 9,568 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,005
row-record quake.cover.m3.week: value 0.974, lo 0.9592, hi 0.9835, unit 9,314 of 9,563, outcome ABOVE, as printed: M3 and above, 1 week 9,563 9,314 140 109 97.4 97.1 to 97.7 95.9 to 98.4 above 82 3,685
row-record quake.cover.m3.month: value 0.9584, lo 0.9391, hi 0.9756, unit 8,749 of 9,129, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,129 8,749 230 150 95.8 95.4 to 96.2 93.9 to 97.6 cannot tell (STRADDLES_EDGE) 78 1,744
row-record quake.cover.m3.year: value 0.8618, lo 0.7898, hi 0.9397, unit 2,931 of 3,401, outcome BELOW, as printed: M3 and above, 1 year 3,401 2,931 344 126 86.2 85.0 to 87.3 79.0 to 94.0 below 42 211
row-record quake.cover.all: value 0.9887, lo 0.9847, hi 0.9933, unit 157,024 of 158,816, outcome ABOVE, as printed: every magnitude, every window 158,816 157,024 1,342 450 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,560
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 306 of 117,181, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,181 306 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.017, hi 0.0494, unit 588 of 17,372, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,372 588 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0681, lo 0.0461, hi 0.092, unit 434 of 6,376, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,376 434 7.1 6.8 6.2 to 7.4 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1036, lo 0.0718, hi 0.1346, unit 583 of 5,628, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,628 583 14.3 10.4 9.6 to 11.2 7.2 to 13.5 below 77
row-record quake.prob.20_40: value 0.192, lo 0.1495, hi 0.2362, unit 940 of 4,896, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,896 940 28.5 19.2 18.1 to 20.3 14.9 to 23.6 below 74
row-record quake.prob.40_60: value 0.3382, lo 0.2624, hi 0.4114, unit 909 of 2,688, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,688 909 49.3 33.8 32.0 to 35.6 26.2 to 41.1 below 58
row-record quake.prob.60_80: value 0.4253, lo 0.3018, hi 0.5616, unit 783 of 1,841, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,841 783 69.6 42.5 40.3 to 44.8 30.2 to 56.2 below 46
row-record quake.prob.80_90: value 0.6358, lo 0.4945, hi 0.7728, unit 473 of 744, outcome BELOW, as printed: 80 to 90 percent, not including 90 744 473 85.0 63.6 60.1 to 67.0 49.5 to 77.3 below 37
row-record quake.prob.90_99: value 0.7731, lo 0.6684, hi 0.86, unit 637 of 824, outcome BELOW, as printed: 90 to 99 percent, not including 99 824 637 95.2 77.3 74.3 to 80.0 66.8 to 86.0 below 32
row-record quake.prob.99_100: value 0.9779, lo 0.959, hi 0.9912, unit 1,238 of 1,266, outcome BELOW, as printed: 99 to 100 percent 1,266 1,238 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 64 of 31,772, outcome CONSISTENT, as printed: 64 of 31,772 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.311, lo 0.2425, hi 0.387, unit 5,563 of 17,887, outcome BELOW, as printed: every magnitude, every window 17,887 5,563 41.9 31.1 30.4 to 31.8 24.2 to 38.7 below 77
row-record quake.prob10.m3: value 0.3043, lo 0.2308, hi 0.3852, unit 3,806 of 12,508, outcome BELOW, as printed: M3 and above 12,508 3,806 44.5 30.4 29.6 to 31.2 23.1 to 38.5 below 77
row-record quake.prob10.m4up: value 0.3266, lo 0.2415, hi 0.417, unit 1,757 of 5,379, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,379 1,757 35.7 32.7 31.4 to 33.9 24.1 to 41.7 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2385, lo 0.14, hi 0.3404, unit 336 of 1,409, outcome BELOW, as printed: every magnitude, 1 day 1,409 336 36.1 23.8 21.7 to 26.1 14.0 to 34.0 below 54
row-record quake.prob10.week: value 0.2118, lo 0.1315, hi 0.3096, unit 870 of 4,108, outcome BELOW, as printed: every magnitude, 1 week 4,108 870 36.8 21.2 20.0 to 22.4 13.2 to 31.0 below 73
row-record quake.prob10.month: value 0.239, lo 0.1655, hi 0.3289, unit 1,731 of 7,243, outcome BELOW, as printed: every magnitude, 1 month 7,243 1,731 39.7 23.9 22.9 to 24.9 16.6 to 32.9 below 74
row-record quake.prob10.year: value 0.5122, lo 0.4178, hi 0.6003, unit 2,626 of 5,127, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,127 2,626 50.7 51.2 49.9 to 52.6 41.8 to 60.0 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9275, lo 0.8795, hi 0.9547, unit 665 of 717, outcome CANNOT_TELL, as printed: 665 of 717 inside, 92.8 percent, with a sequence interval of 87.9 to 95.5 percent.

## 2026-11-17 08:00 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-17T11:38:05Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-17T11:38:05Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-17T11:38:05Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.962, lo 0.9456, hi 0.9773, unit 30,607 of 31,816, outcome CANNOT_TELL, as printed: M3 and above, every window 31,816 30,607 772 437 96.2 96.0 to 96.4 94.6 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,656
row-record quake.cover.m4: value 0.9852, lo 0.9782, hi 0.9935, unit 31,226 of 31,696, outcome ABOVE, as printed: M4 and above 31,696 31,226 464 6 98.5 98.4 to 98.6 97.8 to 99.4 above 81 22,729
row-record quake.cover.m5: value 0.9966, lo 0.9938, hi 0.9989, unit 31,709 of 31,816, outcome ABOVE, as printed: M5 and above 31,816 31,709 106 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,220
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,811 of 31,816, outcome ABOVE, as printed: M6 and above 31,816 31,811 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,362
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,815 of 31,816, outcome ABOVE, as printed: M7 and above 31,816 31,815 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,701
row-record quake.cover.m3.day: value 0.9885, lo 0.9801, hi 0.9935, unit 9,579 of 9,690, outcome ABOVE, as printed: M3 and above, 1 day 9,690 9,579 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,013
row-record quake.cover.m3.week: value 0.9739, lo 0.9592, hi 0.9834, unit 9,324 of 9,574, outcome ABOVE, as printed: M3 and above, 1 week 9,574 9,324 141 109 97.4 97.0 to 97.7 95.9 to 98.3 above 82 3,688
row-record quake.cover.m3.month: value 0.9579, lo 0.9384, hi 0.9752, unit 8,754 of 9,139, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,139 8,754 234 151 95.8 95.4 to 96.2 93.8 to 97.5 cannot tell (STRADDLES_EDGE) 79 1,744
row-record quake.cover.m3.year: value 0.8643, lo 0.7906, hi 0.9409, unit 2,950 of 3,413, outcome BELOW, as printed: M3 and above, 1 year 3,413 2,950 344 119 86.4 85.2 to 87.5 79.1 to 94.1 below 42 211
row-record quake.cover.all: value 0.9887, lo 0.9847, hi 0.9933, unit 157,245 of 159,037, outcome ABOVE, as printed: every magnitude, every window 159,037 157,245 1,348 444 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,729
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 307 of 117,335, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,335 307 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.017, hi 0.0494, unit 589 of 17,392, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,392 589 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0682, lo 0.0462, hi 0.092, unit 436 of 6,389, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,389 436 7.1 6.8 6.2 to 7.5 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1037, lo 0.072, hi 0.1348, unit 585 of 5,641, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,641 585 14.3 10.4 9.6 to 11.2 7.2 to 13.5 below 77
row-record quake.prob.20_40: value 0.193, lo 0.1499, hi 0.2371, unit 946 of 4,902, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,902 946 28.5 19.3 18.2 to 20.4 15.0 to 23.7 below 74
row-record quake.prob.40_60: value 0.339, lo 0.2627, hi 0.4128, unit 913 of 2,693, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,693 913 49.3 33.9 32.1 to 35.7 26.3 to 41.3 below 58
row-record quake.prob.60_80: value 0.4249, lo 0.3013, hi 0.5613, unit 783 of 1,843, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,843 783 69.6 42.5 40.2 to 44.8 30.1 to 56.1 below 46
row-record quake.prob.80_90: value 0.6367, lo 0.4958, hi 0.7732, unit 475 of 746, outcome BELOW, as printed: 80 to 90 percent, not including 90 746 475 85.0 63.7 60.2 to 67.0 49.6 to 77.3 below 37
row-record quake.prob.90_99: value 0.7733, lo 0.6684, hi 0.861, unit 638 of 825, outcome BELOW, as printed: 90 to 99 percent, not including 99 825 638 95.2 77.3 74.4 to 80.1 66.8 to 86.1 below 32
row-record quake.prob.99_100: value 0.978, lo 0.9591, hi 0.9912, unit 1,243 of 1,271, outcome BELOW, as printed: 99 to 100 percent 1,271 1,243 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 64 of 31,816, outcome CONSISTENT, as printed: 64 of 31,816 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3115, lo 0.2426, hi 0.3878, unit 5,583 of 17,921, outcome BELOW, as printed: every magnitude, every window 17,921 5,583 41.9 31.1 30.5 to 31.8 24.3 to 38.8 below 77
row-record quake.prob10.m3: value 0.3049, lo 0.2312, hi 0.3858, unit 3,821 of 12,531, outcome BELOW, as printed: M3 and above 12,531 3,821 44.5 30.5 29.7 to 31.3 23.1 to 38.6 below 77
row-record quake.prob10.m4up: value 0.3269, lo 0.2419, hi 0.4173, unit 1,762 of 5,390, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,390 1,762 35.8 32.7 31.4 to 34.0 24.2 to 41.7 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2381, lo 0.1394, hi 0.3401, unit 336 of 1,411, outcome BELOW, as printed: every magnitude, 1 day 1,411 336 36.1 23.8 21.7 to 26.1 13.9 to 34.0 below 54
row-record quake.prob10.week: value 0.2122, lo 0.1324, hi 0.3099, unit 873 of 4,114, outcome BELOW, as printed: every magnitude, 1 week 4,114 873 36.7 21.2 20.0 to 22.5 13.2 to 31.0 below 73
row-record quake.prob10.month: value 0.24, lo 0.1666, hi 0.3296, unit 1,741 of 7,254, outcome BELOW, as printed: every magnitude, 1 month 7,254 1,741 39.7 24.0 23.0 to 25.0 16.7 to 33.0 below 75
row-record quake.prob10.year: value 0.5121, lo 0.4177, hi 0.6002, unit 2,633 of 5,142, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,142 2,633 50.7 51.2 49.8 to 52.6 41.8 to 60.0 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9276, lo 0.8782, hi 0.9554, unit 666 of 718, outcome CANNOT_TELL, as printed: 666 of 718 inside, 92.8 percent, with a sequence interval of 87.8 to 95.5 percent.

## 2026-11-17 11:34 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-17T14:16:08Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-17T14:16:08Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-17T14:16:08Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.962, lo 0.9456, hi 0.9774, unit 30,619 of 31,828, outcome CANNOT_TELL, as printed: M3 and above, every window 31,828 30,619 772 437 96.2 96.0 to 96.4 94.6 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,662
row-record quake.cover.m4: value 0.9852, lo 0.9782, hi 0.9935, unit 31,238 of 31,708, outcome ABOVE, as printed: M4 and above 31,708 31,238 464 6 98.5 98.4 to 98.6 97.8 to 99.4 above 81 22,739
row-record quake.cover.m5: value 0.9966, lo 0.9938, hi 0.9989, unit 31,721 of 31,828, outcome ABOVE, as printed: M5 and above 31,828 31,721 106 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,231
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,823 of 31,828, outcome ABOVE, as printed: M6 and above 31,828 31,823 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,374
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,827 of 31,828, outcome ABOVE, as printed: M7 and above 31,828 31,827 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,713
row-record quake.cover.m3.day: value 0.9885, lo 0.9801, hi 0.9935, unit 9,582 of 9,693, outcome ABOVE, as printed: M3 and above, 1 day 9,693 9,582 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,016
row-record quake.cover.m3.week: value 0.9739, lo 0.9593, hi 0.9834, unit 9,329 of 9,579, outcome ABOVE, as printed: M3 and above, 1 week 9,579 9,329 141 109 97.4 97.0 to 97.7 95.9 to 98.3 above 82 3,691
row-record quake.cover.m3.month: value 0.9579, lo 0.9384, hi 0.9752, unit 8,755 of 9,140, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,140 8,755 234 151 95.8 95.4 to 96.2 93.8 to 97.5 cannot tell (STRADDLES_EDGE) 79 1,744
row-record quake.cover.m3.year: value 0.8645, lo 0.7908, hi 0.941, unit 2,953 of 3,416, outcome BELOW, as printed: M3 and above, 1 year 3,416 2,953 344 119 86.5 85.3 to 87.5 79.1 to 94.1 below 42 211
row-record quake.cover.all: value 0.9887, lo 0.9847, hi 0.9933, unit 157,305 of 159,097, outcome ABOVE, as printed: every magnitude, every window 159,097 157,305 1,348 444 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,780
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0044, unit 307 of 117,384, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,384 307 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.017, hi 0.0494, unit 589 of 17,398, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,398 589 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0682, lo 0.0462, hi 0.092, unit 436 of 6,390, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,390 436 7.1 6.8 6.2 to 7.5 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1037, lo 0.072, hi 0.1348, unit 585 of 5,642, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,642 585 14.3 10.4 9.6 to 11.2 7.2 to 13.5 below 77
row-record quake.prob.20_40: value 0.1929, lo 0.1498, hi 0.2369, unit 946 of 4,904, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,904 946 28.5 19.3 18.2 to 20.4 15.0 to 23.7 below 74
row-record quake.prob.40_60: value 0.339, lo 0.2627, hi 0.4128, unit 913 of 2,693, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,693 913 49.3 33.9 32.1 to 35.7 26.3 to 41.3 below 58
row-record quake.prob.60_80: value 0.4249, lo 0.3013, hi 0.5613, unit 783 of 1,843, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,843 783 69.6 42.5 40.2 to 44.8 30.1 to 56.1 below 46
row-record quake.prob.80_90: value 0.6367, lo 0.4958, hi 0.7732, unit 475 of 746, outcome BELOW, as printed: 80 to 90 percent, not including 90 746 475 85.0 63.7 60.2 to 67.0 49.6 to 77.3 below 37
row-record quake.prob.90_99: value 0.7724, lo 0.6675, hi 0.8601, unit 638 of 826, outcome BELOW, as printed: 90 to 99 percent, not including 99 826 638 95.2 77.2 74.3 to 80.0 66.8 to 86.0 below 32
row-record quake.prob.99_100: value 0.978, lo 0.9591, hi 0.9912, unit 1,243 of 1,271, outcome BELOW, as printed: 99 to 100 percent 1,271 1,243 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 64 of 31,828, outcome CONSISTENT, as printed: 64 of 31,828 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3115, lo 0.2426, hi 0.3877, unit 5,583 of 17,925, outcome BELOW, as printed: every magnitude, every window 17,925 5,583 41.9 31.1 30.5 to 31.8 24.3 to 38.8 below 77
row-record quake.prob10.m3: value 0.3049, lo 0.2311, hi 0.3857, unit 3,821 of 12,534, outcome BELOW, as printed: M3 and above 12,534 3,821 44.5 30.5 29.7 to 31.3 23.1 to 38.6 below 77
row-record quake.prob10.m4up: value 0.3268, lo 0.2419, hi 0.4172, unit 1,762 of 5,391, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,391 1,762 35.8 32.7 31.4 to 34.0 24.2 to 41.7 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2381, lo 0.1394, hi 0.3401, unit 336 of 1,411, outcome BELOW, as printed: every magnitude, 1 day 1,411 336 36.1 23.8 21.7 to 26.1 13.9 to 34.0 below 54
row-record quake.prob10.week: value 0.2122, lo 0.1324, hi 0.3099, unit 873 of 4,114, outcome BELOW, as printed: every magnitude, 1 week 4,114 873 36.7 21.2 20.0 to 22.5 13.2 to 31.0 below 73
row-record quake.prob10.month: value 0.24, lo 0.1666, hi 0.3296, unit 1,741 of 7,254, outcome BELOW, as printed: every magnitude, 1 month 7,254 1,741 39.7 24.0 23.0 to 25.0 16.7 to 33.0 below 75
row-record quake.prob10.year: value 0.5117, lo 0.4174, hi 0.5997, unit 2,633 of 5,146, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,146 2,633 50.7 51.2 49.8 to 52.5 41.7 to 60.0 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9276, lo 0.8782, hi 0.9554, unit 666 of 718, outcome CANNOT_TELL, as printed: 666 of 718 inside, 92.8 percent, with a sequence interval of 87.8 to 95.5 percent.

## 2026-11-17 15:03 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-17T16:34:20Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-17T16:34:20Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-17T16:34:20Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9619, lo 0.9455, hi 0.9773, unit 30,624 of 31,836, outcome CANNOT_TELL, as printed: M3 and above, every window 31,836 30,624 774 438 96.2 96.0 to 96.4 94.5 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,664
row-record quake.cover.m4: value 0.9852, lo 0.9782, hi 0.9935, unit 31,246 of 31,716, outcome ABOVE, as printed: M4 and above 31,716 31,246 464 6 98.5 98.4 to 98.7 97.8 to 99.4 above 81 22,743
row-record quake.cover.m5: value 0.9966, lo 0.9938, hi 0.9989, unit 31,729 of 31,836, outcome ABOVE, as printed: M5 and above 31,836 31,729 106 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,238
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,831 of 31,836, outcome ABOVE, as printed: M6 and above 31,836 31,831 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,381
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,835 of 31,836, outcome ABOVE, as printed: M7 and above 31,836 31,835 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,720
row-record quake.cover.m3.day: value 0.9885, lo 0.9801, hi 0.9935, unit 9,583 of 9,694, outcome ABOVE, as printed: M3 and above, 1 day 9,694 9,583 53 58 98.9 98.6 to 99.1 98.0 to 99.4 above 82 7,017
row-record quake.cover.m3.week: value 0.9738, lo 0.9593, hi 0.9833, unit 9,330 of 9,581, outcome ABOVE, as printed: M3 and above, 1 week 9,581 9,330 142 109 97.4 97.0 to 97.7 95.9 to 98.3 above 82 3,692
row-record quake.cover.m3.month: value 0.9577, lo 0.9382, hi 0.9751, unit 8,754 of 9,141, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,141 8,754 235 152 95.8 95.3 to 96.2 93.8 to 97.5 cannot tell (STRADDLES_EDGE) 79 1,744
row-record quake.cover.m3.year: value 0.8646, lo 0.791, hi 0.9411, unit 2,957 of 3,420, outcome BELOW, as printed: M3 and above, 1 year 3,420 2,957 344 119 86.5 85.3 to 87.6 79.1 to 94.1 below 42 211
row-record quake.cover.all: value 0.9887, lo 0.9847, hi 0.9933, unit 157,343 of 159,138, outcome ABOVE, as printed: every magnitude, every window 159,138 157,343 1,350 445 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,808
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0045, unit 309 of 117,410, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,410 309 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0338, lo 0.017, hi 0.0494, unit 589 of 17,402, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,402 589 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0682, lo 0.0462, hi 0.092, unit 436 of 6,392, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,392 436 7.1 6.8 6.2 to 7.5 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1038, lo 0.0723, hi 0.1348, unit 586 of 5,644, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,644 586 14.3 10.4 9.6 to 11.2 7.2 to 13.5 below 77
row-record quake.prob.20_40: value 0.1929, lo 0.1498, hi 0.2369, unit 946 of 4,905, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,905 946 28.5 19.3 18.2 to 20.4 15.0 to 23.7 below 74
row-record quake.prob.40_60: value 0.3391, lo 0.2631, hi 0.4129, unit 914 of 2,695, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,695 914 49.3 33.9 32.1 to 35.7 26.3 to 41.3 below 58
row-record quake.prob.60_80: value 0.4252, lo 0.3018, hi 0.5613, unit 784 of 1,844, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,844 784 69.6 42.5 40.3 to 44.8 30.2 to 56.1 below 46
row-record quake.prob.80_90: value 0.6367, lo 0.4958, hi 0.7732, unit 475 of 746, outcome BELOW, as printed: 80 to 90 percent, not including 90 746 475 85.0 63.7 60.2 to 67.0 49.6 to 77.3 below 37
row-record quake.prob.90_99: value 0.7724, lo 0.6675, hi 0.8601, unit 638 of 826, outcome BELOW, as printed: 90 to 99 percent, not including 99 826 638 95.2 77.2 74.3 to 80.0 66.8 to 86.0 below 32
row-record quake.prob.99_100: value 0.978, lo 0.9592, hi 0.9913, unit 1,246 of 1,274, outcome BELOW, as printed: 99 to 100 percent 1,274 1,246 99.9 97.8 96.8 to 98.5 95.9 to 99.1 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0045, unit 64 of 31,836, outcome CONSISTENT, as printed: 64 of 31,836 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3116, lo 0.2432, hi 0.3877, unit 5,589 of 17,934, outcome BELOW, as printed: every magnitude, every window 17,934 5,589 41.9 31.2 30.5 to 31.9 24.3 to 38.8 below 77
row-record quake.prob10.m3: value 0.3049, lo 0.2312, hi 0.3858, unit 3,823 of 12,538, outcome BELOW, as printed: M3 and above 12,538 3,823 44.5 30.5 29.7 to 31.3 23.1 to 38.6 below 77
row-record quake.prob10.m4up: value 0.3273, lo 0.2426, hi 0.4175, unit 1,766 of 5,396, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,396 1,766 35.8 32.7 31.5 to 34.0 24.3 to 41.8 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2381, lo 0.1394, hi 0.3401, unit 336 of 1,411, outcome BELOW, as printed: every magnitude, 1 day 1,411 336 36.1 23.8 21.7 to 26.1 13.9 to 34.0 below 54
row-record quake.prob10.week: value 0.2122, lo 0.1324, hi 0.3099, unit 873 of 4,114, outcome BELOW, as printed: every magnitude, 1 week 4,114 873 36.7 21.2 20.0 to 22.5 13.2 to 31.0 below 73
row-record quake.prob10.month: value 0.2404, lo 0.1669, hi 0.3303, unit 1,745 of 7,259, outcome BELOW, as printed: every magnitude, 1 month 7,259 1,745 39.7 24.0 23.1 to 25.0 16.7 to 33.0 below 75
row-record quake.prob10.year: value 0.5117, lo 0.4177, hi 0.5996, unit 2,635 of 5,150, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,150 2,635 50.7 51.2 49.8 to 52.5 41.8 to 60.0 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9276, lo 0.8782, hi 0.9554, unit 666 of 718, outcome CANNOT_TELL, as printed: 666 of 718 inside, 92.8 percent, with a sequence interval of 87.8 to 95.5 percent.

## 2026-11-17 20:18 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-17T20:03:48Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-17T20:03:48Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-17T20:03:48Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9619, lo 0.9455, hi 0.9772, unit 30,637 of 31,852, outcome CANNOT_TELL, as printed: M3 and above, every window 31,852 30,637 776 439 96.2 96.0 to 96.4 94.5 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,667
row-record quake.cover.m4: value 0.9852, lo 0.9782, hi 0.9935, unit 31,261 of 31,732, outcome ABOVE, as printed: M4 and above 31,732 31,261 465 6 98.5 98.4 to 98.6 97.8 to 99.4 above 81 22,750
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9989, unit 31,744 of 31,852, outcome ABOVE, as printed: M5 and above 31,852 31,744 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,250
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,847 of 31,852, outcome ABOVE, as printed: M6 and above 31,852 31,847 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,397
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,851 of 31,852, outcome ABOVE, as printed: M7 and above 31,852 31,851 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,736
row-record quake.cover.m3.day: value 0.9885, lo 0.9799, hi 0.9935, unit 9,586 of 9,698, outcome ABOVE, as printed: M3 and above, 1 day 9,698 9,586 53 59 98.9 98.6 to 99.0 98.0 to 99.4 above 82 7,018
row-record quake.cover.m3.week: value 0.9738, lo 0.9593, hi 0.9833, unit 9,332 of 9,583, outcome ABOVE, as printed: M3 and above, 1 week 9,583 9,332 142 109 97.4 97.0 to 97.7 95.9 to 98.3 above 82 3,693
row-record quake.cover.m3.month: value 0.9577, lo 0.9382, hi 0.9751, unit 8,757 of 9,144, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,144 8,757 235 152 95.8 95.3 to 96.2 93.8 to 97.5 cannot tell (STRADDLES_EDGE) 79 1,745
row-record quake.cover.m3.year: value 0.8643, lo 0.7911, hi 0.9409, unit 2,962 of 3,427, outcome BELOW, as printed: M3 and above, 1 year 3,427 2,962 346 119 86.4 85.2 to 87.5 79.1 to 94.1 below 42 211
row-record quake.cover.all: value 0.9887, lo 0.9846, hi 0.9933, unit 157,418 of 159,218, outcome ABOVE, as printed: every magnitude, every window 159,218 157,418 1,354 446 98.9 98.8 to 98.9 98.5 to 99.3 above 82 127,862
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0045, unit 310 of 117,462, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 117,462 310 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0339, lo 0.017, hi 0.0494, unit 590 of 17,413, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,413 590 2.4 3.4 3.1 to 3.7 1.7 to 4.9 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0682, lo 0.0461, hi 0.0919, unit 436 of 6,395, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,395 436 7.1 6.8 6.2 to 7.5 4.6 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1038, lo 0.0723, hi 0.1348, unit 586 of 5,645, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,645 586 14.3 10.4 9.6 to 11.2 7.2 to 13.5 below 77
row-record quake.prob.20_40: value 0.1932, lo 0.1503, hi 0.2371, unit 949 of 4,911, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,911 949 28.5 19.3 18.2 to 20.4 15.0 to 23.7 below 74
row-record quake.prob.40_60: value 0.3388, lo 0.2628, hi 0.4124, unit 914 of 2,698, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,698 914 49.3 33.9 32.1 to 35.7 26.3 to 41.2 below 58
row-record quake.prob.60_80: value 0.4258, lo 0.3026, hi 0.5618, unit 786 of 1,846, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,846 786 69.6 42.6 40.3 to 44.9 30.3 to 56.2 below 46
row-record quake.prob.80_90: value 0.6367, lo 0.4958, hi 0.7732, unit 475 of 746, outcome BELOW, as printed: 80 to 90 percent, not including 90 746 475 85.0 63.7 60.2 to 67.0 49.6 to 77.3 below 37
row-record quake.prob.90_99: value 0.7715, lo 0.6672, hi 0.8601, unit 638 of 827, outcome BELOW, as printed: 90 to 99 percent, not including 99 827 638 95.2 77.1 74.2 to 79.9 66.7 to 86.0 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9586, hi 0.9902, unit 1,246 of 1,275, outcome BELOW, as printed: 99 to 100 percent 1,275 1,246 99.9 97.7 96.8 to 98.4 95.9 to 99.0 below 21
row-record quake.prob.mainshock: value 0.002, lo 0.0, hi 0.0046, unit 65 of 31,852, outcome CONSISTENT, as printed: 65 of 31,852 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3117, lo 0.2433, hi 0.3877, unit 5,594 of 17,948, outcome BELOW, as printed: every magnitude, every window 17,948 5,594 41.9 31.2 30.5 to 31.9 24.3 to 38.8 below 77
row-record quake.prob10.m3: value 0.305, lo 0.2314, hi 0.3858, unit 3,827 of 12,547, outcome BELOW, as printed: M3 and above 12,547 3,827 44.5 30.5 29.7 to 31.3 23.1 to 38.6 below 77
row-record quake.prob10.m4up: value 0.3272, lo 0.2426, hi 0.4173, unit 1,767 of 5,401, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,401 1,767 35.8 32.7 31.5 to 34.0 24.3 to 41.7 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2378, lo 0.1392, hi 0.3401, unit 336 of 1,413, outcome BELOW, as printed: every magnitude, 1 day 1,413 336 36.1 23.8 21.6 to 26.1 13.9 to 34.0 below 54
row-record quake.prob10.week: value 0.2122, lo 0.1324, hi 0.3099, unit 873 of 4,114, outcome BELOW, as printed: every magnitude, 1 week 4,114 873 36.7 21.2 20.0 to 22.5 13.2 to 31.0 below 73
row-record quake.prob10.month: value 0.2403, lo 0.1668, hi 0.3302, unit 1,745 of 7,262, outcome BELOW, as printed: every magnitude, 1 month 7,262 1,745 39.7 24.0 23.1 to 25.0 16.7 to 33.0 below 75
row-record quake.prob10.year: value 0.5117, lo 0.4182, hi 0.5993, unit 2,640 of 5,159, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,159 2,640 50.7 51.2 49.8 to 52.5 41.8 to 59.9 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9276, lo 0.8782, hi 0.9554, unit 666 of 718, outcome CANNOT_TELL, as printed: 666 of 718 inside, 92.8 percent, with a sequence interval of 87.8 to 95.5 percent.

## 2026-11-17 23:43 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-18T02:28:45Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-18T02:28:45Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-18T02:28:45Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9615, lo 0.9452, hi 0.9768, unit 30,275 of 31,488, outcome CANNOT_TELL, as printed: M3 and above, every window 31,488 30,275 773 440 96.2 95.9 to 96.4 94.5 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,493
row-record quake.cover.m4: value 0.9851, lo 0.9783, hi 0.9933, unit 30,901 of 31,368, outcome ABOVE, as printed: M4 and above 31,368 30,901 461 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,488
row-record quake.cover.m5: value 0.9966, lo 0.9936, hi 0.9989, unit 31,380 of 31,488, outcome ABOVE, as printed: M5 and above 31,488 31,380 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 28,904
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,483 of 31,488, outcome ABOVE, as printed: M6 and above 31,488 31,483 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,033
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,487 of 31,488, outcome ABOVE, as printed: M7 and above 31,488 31,487 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,372
row-record quake.cover.m3.day: value 0.9883, lo 0.9797, hi 0.9934, unit 9,484 of 9,596, outcome ABOVE, as printed: M3 and above, 1 day 9,596 9,484 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,932
row-record quake.cover.m3.week: value 0.9734, lo 0.9586, hi 0.9829, unit 9,229 of 9,481, outcome ABOVE, as printed: M3 and above, 1 week 9,481 9,229 143 109 97.3 97.0 to 97.7 95.9 to 98.3 above 82 3,637
row-record quake.cover.m3.month: value 0.9575, lo 0.9381, hi 0.9748, unit 8,661 of 9,045, outcome CONSISTENT, as printed: M3 and above, 1 month 9,045 8,661 231 153 95.8 95.3 to 96.2 93.8 to 97.5 consistent 79 1,712
row-record quake.cover.m3.year: value 0.8619, lo 0.7903, hi 0.939, unit 2,901 of 3,366, outcome BELOW, as printed: M3 and above, 1 year 3,366 2,901 346 119 86.2 85.0 to 87.3 79.0 to 93.9 below 42 212
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9932, unit 155,604 of 157,398, outcome ABOVE, as printed: every magnitude, every window 157,398 155,604 1,347 447 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,352
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 301 of 116,058, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,058 301 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0343, lo 0.0175, hi 0.0499, unit 591 of 17,247, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,247 591 2.4 3.4 3.2 to 3.7 1.8 to 5.0 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0646, lo 0.0416, hi 0.0901, unit 408 of 6,316, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,316 408 7.1 6.5 5.9 to 7.1 4.2 to 9.0 consistent 80
row-record quake.prob.10_20: value 0.1035, lo 0.0705, hi 0.1347, unit 578 of 5,587, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,587 578 14.4 10.3 9.6 to 11.2 7.0 to 13.5 below 77
row-record quake.prob.20_40: value 0.1922, lo 0.1478, hi 0.2369, unit 934 of 4,859, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,859 934 28.5 19.2 18.1 to 20.3 14.8 to 23.7 below 74
row-record quake.prob.40_60: value 0.336, lo 0.2561, hi 0.4122, unit 892 of 2,655, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,655 892 49.3 33.6 31.8 to 35.4 25.6 to 41.2 below 58
row-record quake.prob.60_80: value 0.4308, lo 0.3106, hi 0.5618, unit 787 of 1,827, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,827 787 69.6 43.1 40.8 to 45.4 31.1 to 56.2 below 46
row-record quake.prob.80_90: value 0.6367, lo 0.4958, hi 0.7732, unit 475 of 746, outcome BELOW, as printed: 80 to 90 percent, not including 90 746 475 85.0 63.7 60.2 to 67.0 49.6 to 77.3 below 37
row-record quake.prob.90_99: value 0.7705, lo 0.6662, hi 0.8601, unit 638 of 828, outcome BELOW, as printed: 90 to 99 percent, not including 99 828 638 95.2 77.0 74.1 to 79.8 66.6 to 86.0 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9586, hi 0.9902, unit 1,246 of 1,275, outcome BELOW, as printed: 99 to 100 percent 1,275 1,246 99.9 97.7 96.8 to 98.4 95.9 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0045, unit 60 of 31,488, outcome CONSISTENT, as printed: 60 of 31,488 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3122, lo 0.2431, hi 0.3875, unit 5,550 of 17,777, outcome BELOW, as printed: every magnitude, every window 17,777 5,550 42.0 31.2 30.5 to 31.9 24.3 to 38.8 below 77
row-record quake.prob10.m3: value 0.3053, lo 0.2303, hi 0.3859, unit 3,792 of 12,420, outcome BELOW, as printed: M3 and above 12,420 3,792 44.6 30.5 29.7 to 31.4 23.0 to 38.6 below 77
row-record quake.prob10.m4up: value 0.3282, lo 0.2434, hi 0.418, unit 1,758 of 5,357, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,357 1,758 35.9 32.8 31.6 to 34.1 24.3 to 41.8 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2385, lo 0.1399, hi 0.3401, unit 336 of 1,409, outcome BELOW, as printed: every magnitude, 1 day 1,409 336 36.2 23.8 21.7 to 26.1 14.0 to 34.0 below 54
row-record quake.prob10.week: value 0.2135, lo 0.1335, hi 0.3104, unit 874 of 4,094, outcome BELOW, as printed: every magnitude, 1 week 4,094 874 36.8 21.3 20.1 to 22.6 13.4 to 31.0 below 73
row-record quake.prob10.month: value 0.242, lo 0.1696, hi 0.33, unit 1,745 of 7,211, outcome BELOW, as printed: every magnitude, 1 month 7,211 1,745 39.8 24.2 23.2 to 25.2 17.0 to 33.0 below 75
row-record quake.prob10.year: value 0.5125, lo 0.4158, hi 0.5992, unit 2,595 of 5,063, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,063 2,595 50.9 51.2 49.9 to 52.6 41.6 to 59.9 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9269, lo 0.8776, hi 0.955, unit 659 of 711, outcome CANNOT_TELL, as printed: 659 of 711 inside, 92.7 percent, with a sequence interval of 87.8 to 95.5 percent.

## 2026-11-18 03:02 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-18T06:56:50Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-18T06:56:50Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-18T06:56:50Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9615, lo 0.9452, hi 0.9768, unit 30,288 of 31,502, outcome CANNOT_TELL, as printed: M3 and above, every window 31,502 30,288 773 441 96.2 95.9 to 96.4 94.5 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,498
row-record quake.cover.m4: value 0.9851, lo 0.9784, hi 0.9933, unit 30,915 of 31,382, outcome ABOVE, as printed: M4 and above 31,382 30,915 461 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,495
row-record quake.cover.m5: value 0.9966, lo 0.9936, hi 0.9989, unit 31,394 of 31,502, outcome ABOVE, as printed: M5 and above 31,502 31,394 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 28,914
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,497 of 31,502, outcome ABOVE, as printed: M6 and above 31,502 31,497 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,047
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,501 of 31,502, outcome ABOVE, as printed: M7 and above 31,502 31,501 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,386
row-record quake.cover.m3.day: value 0.9883, lo 0.9797, hi 0.9934, unit 9,487 of 9,599, outcome ABOVE, as printed: M3 and above, 1 day 9,599 9,487 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,935
row-record quake.cover.m3.week: value 0.9734, lo 0.9586, hi 0.9829, unit 9,231 of 9,483, outcome ABOVE, as printed: M3 and above, 1 week 9,483 9,231 143 109 97.3 97.0 to 97.7 95.9 to 98.3 above 82 3,639
row-record quake.cover.m3.month: value 0.9576, lo 0.9382, hi 0.9748, unit 8,664 of 9,048, outcome CONSISTENT, as printed: M3 and above, 1 month 9,048 8,664 231 153 95.8 95.3 to 96.2 93.8 to 97.5 consistent 79 1,712
row-record quake.cover.m3.year: value 0.8618, lo 0.7901, hi 0.9391, unit 2,906 of 3,372, outcome BELOW, as printed: M3 and above, 1 year 3,372 2,906 346 120 86.2 85.0 to 87.3 79.0 to 93.9 below 42 212
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9932, unit 155,673 of 157,468, outcome ABOVE, as printed: every magnitude, every window 157,468 155,673 1,347 448 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,402
row-record quake.prob.0_1: value 0.0026, lo 0.0007, hi 0.0043, unit 301 of 116,101, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,101 301 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0342, lo 0.0175, hi 0.0498, unit 591 of 17,258, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,258 591 2.4 3.4 3.2 to 3.7 1.8 to 5.0 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0646, lo 0.0416, hi 0.0901, unit 408 of 6,316, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,316 408 7.1 6.5 5.9 to 7.1 4.2 to 9.0 consistent 80
row-record quake.prob.10_20: value 0.1034, lo 0.0705, hi 0.1346, unit 578 of 5,592, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,592 578 14.4 10.3 9.6 to 11.2 7.0 to 13.5 below 77
row-record quake.prob.20_40: value 0.1927, lo 0.1484, hi 0.2374, unit 937 of 4,862, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,862 937 28.5 19.3 18.2 to 20.4 14.8 to 23.7 below 74
row-record quake.prob.40_60: value 0.3358, lo 0.256, hi 0.4122, unit 892 of 2,656, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,656 892 49.3 33.6 31.8 to 35.4 25.6 to 41.2 below 58
row-record quake.prob.60_80: value 0.432, lo 0.3123, hi 0.562, unit 791 of 1,831, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,831 791 69.6 43.2 40.9 to 45.5 31.2 to 56.2 below 46
row-record quake.prob.80_90: value 0.6372, lo 0.4965, hi 0.7732, unit 476 of 747, outcome BELOW, as printed: 80 to 90 percent, not including 90 747 476 85.0 63.7 60.2 to 67.1 49.6 to 77.3 below 37
row-record quake.prob.90_99: value 0.7708, lo 0.6667, hi 0.8602, unit 639 of 829, outcome BELOW, as printed: 90 to 99 percent, not including 99 829 639 95.2 77.1 74.1 to 79.8 66.7 to 86.0 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9586, hi 0.9902, unit 1,247 of 1,276, outcome BELOW, as printed: 99 to 100 percent 1,276 1,247 99.9 97.7 96.8 to 98.4 95.9 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0045, unit 60 of 31,502, outcome CONSISTENT, as printed: 60 of 31,502 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3125, lo 0.2434, hi 0.3878, unit 5,560 of 17,793, outcome BELOW, as printed: every magnitude, every window 17,793 5,560 42.0 31.2 30.6 to 31.9 24.3 to 38.8 below 77
row-record quake.prob10.m3: value 0.3056, lo 0.2306, hi 0.386, unit 3,798 of 12,428, outcome BELOW, as printed: M3 and above 12,428 3,798 44.6 30.6 29.8 to 31.4 23.1 to 38.6 below 77
row-record quake.prob10.m4up: value 0.3284, lo 0.2439, hi 0.4182, unit 1,762 of 5,365, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,365 1,762 35.9 32.8 31.6 to 34.1 24.4 to 41.8 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2385, lo 0.1399, hi 0.3401, unit 336 of 1,409, outcome BELOW, as printed: every magnitude, 1 day 1,409 336 36.2 23.8 21.7 to 26.1 14.0 to 34.0 below 54
row-record quake.prob10.week: value 0.2135, lo 0.1335, hi 0.3104, unit 874 of 4,094, outcome BELOW, as printed: every magnitude, 1 week 4,094 874 36.8 21.3 20.1 to 22.6 13.4 to 31.0 below 73
row-record quake.prob10.month: value 0.2421, lo 0.1696, hi 0.3298, unit 1,747 of 7,216, outcome BELOW, as printed: every magnitude, 1 month 7,216 1,747 39.8 24.2 23.2 to 25.2 17.0 to 33.0 below 75
row-record quake.prob10.year: value 0.513, lo 0.4166, hi 0.5993, unit 2,603 of 5,074, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,074 2,603 50.9 51.3 49.9 to 52.7 41.7 to 59.9 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9269, lo 0.8776, hi 0.955, unit 659 of 711, outcome CANNOT_TELL, as printed: 659 of 711 inside, 92.7 percent, with a sequence interval of 87.8 to 95.5 percent.

## 2026-11-18 06:30 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-18T09:12:26Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-18T09:12:26Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-18T09:12:26Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9615, lo 0.9456, hi 0.9771, unit 30,296 of 31,510, outcome CANNOT_TELL, as printed: M3 and above, every window 31,510 30,296 773 441 96.2 95.9 to 96.4 94.6 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,502
row-record quake.cover.m4: value 0.9851, lo 0.9784, hi 0.9934, unit 30,923 of 31,390, outcome ABOVE, as printed: M4 and above 31,390 30,923 461 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,502
row-record quake.cover.m5: value 0.9966, lo 0.9936, hi 0.9989, unit 31,402 of 31,510, outcome ABOVE, as printed: M5 and above 31,510 31,402 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 28,921
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,505 of 31,510, outcome ABOVE, as printed: M6 and above 31,510 31,505 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,055
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,509 of 31,510, outcome ABOVE, as printed: M7 and above 31,510 31,509 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,394
row-record quake.cover.m3.day: value 0.9883, lo 0.9797, hi 0.9934, unit 9,488 of 9,600, outcome ABOVE, as printed: M3 and above, 1 day 9,600 9,488 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,935
row-record quake.cover.m3.week: value 0.9734, lo 0.9591, hi 0.9833, unit 9,234 of 9,486, outcome ABOVE, as printed: M3 and above, 1 week 9,486 9,234 143 109 97.3 97.0 to 97.7 95.9 to 98.3 above 82 3,640
row-record quake.cover.m3.month: value 0.9576, lo 0.9384, hi 0.9752, unit 8,667 of 9,051, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,051 8,667 231 153 95.8 95.3 to 96.2 93.8 to 97.5 cannot tell (STRADDLES_EDGE) 79 1,715
row-record quake.cover.m3.year: value 0.8618, lo 0.7904, hi 0.9395, unit 2,907 of 3,373, outcome BELOW, as printed: M3 and above, 1 year 3,373 2,907 346 120 86.2 85.0 to 87.3 79.0 to 94.0 below 42 212
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9932, unit 155,713 of 157,508, outcome ABOVE, as printed: every magnitude, every window 157,508 155,713 1,347 448 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,436
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 301 of 116,130, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,130 301 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0342, lo 0.0172, hi 0.0498, unit 591 of 17,264, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,264 591 2.4 3.4 3.2 to 3.7 1.7 to 5.0 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0646, lo 0.0405, hi 0.0914, unit 408 of 6,317, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,317 408 7.1 6.5 5.9 to 7.1 4.0 to 9.1 consistent 80
row-record quake.prob.10_20: value 0.1033, lo 0.0703, hi 0.1342, unit 578 of 5,594, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,594 578 14.3 10.3 9.6 to 11.2 7.0 to 13.4 below 77
row-record quake.prob.20_40: value 0.1927, lo 0.1484, hi 0.2392, unit 937 of 4,862, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,862 937 28.5 19.3 18.2 to 20.4 14.8 to 23.9 below 74
row-record quake.prob.40_60: value 0.3357, lo 0.2551, hi 0.4139, unit 892 of 2,657, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,657 892 49.3 33.6 31.8 to 35.4 25.5 to 41.4 below 58
row-record quake.prob.60_80: value 0.432, lo 0.3117, hi 0.564, unit 791 of 1,831, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,831 791 69.6 43.2 40.9 to 45.5 31.2 to 56.4 below 46
row-record quake.prob.80_90: value 0.6372, lo 0.4995, hi 0.7732, unit 476 of 747, outcome BELOW, as printed: 80 to 90 percent, not including 90 747 476 85.0 63.7 60.2 to 67.1 50.0 to 77.3 below 37
row-record quake.prob.90_99: value 0.7699, lo 0.6667, hi 0.8571, unit 639 of 830, outcome BELOW, as printed: 90 to 99 percent, not including 99 830 639 95.2 77.0 74.0 to 79.7 66.7 to 85.7 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9586, hi 0.9902, unit 1,247 of 1,276, outcome BELOW, as printed: 99 to 100 percent 1,276 1,247 99.9 97.7 96.8 to 98.4 95.9 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0045, unit 60 of 31,510, outcome CONSISTENT, as printed: 60 of 31,510 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3124, lo 0.2407, hi 0.3895, unit 5,560 of 17,797, outcome BELOW, as printed: every magnitude, every window 17,797 5,560 42.0 31.2 30.6 to 31.9 24.1 to 39.0 below 77
row-record quake.prob10.m3: value 0.3056, lo 0.2302, hi 0.3858, unit 3,798 of 12,430, outcome BELOW, as printed: M3 and above 12,430 3,798 44.6 30.6 29.8 to 31.4 23.0 to 38.6 below 77
row-record quake.prob10.m4up: value 0.3283, lo 0.2441, hi 0.4198, unit 1,762 of 5,367, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,367 1,762 35.9 32.8 31.6 to 34.1 24.4 to 42.0 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2385, lo 0.1412, hi 0.3416, unit 336 of 1,409, outcome BELOW, as printed: every magnitude, 1 day 1,409 336 36.2 23.8 21.7 to 26.1 14.1 to 34.2 below 54
row-record quake.prob10.week: value 0.2134, lo 0.1345, hi 0.3123, unit 874 of 4,095, outcome BELOW, as printed: every magnitude, 1 week 4,095 874 36.8 21.3 20.1 to 22.6 13.5 to 31.2 below 73
row-record quake.prob10.month: value 0.2421, lo 0.168, hi 0.3298, unit 1,747 of 7,216, outcome BELOW, as printed: every magnitude, 1 month 7,216 1,747 39.8 24.2 23.2 to 25.2 16.8 to 33.0 below 75
row-record quake.prob10.year: value 0.5127, lo 0.4213, hi 0.5961, unit 2,603 of 5,077, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,077 2,603 50.9 51.3 49.9 to 52.6 42.1 to 59.6 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9269, lo 0.8796, hi 0.9551, unit 659 of 711, outcome CANNOT_TELL, as printed: 659 of 711 inside, 92.7 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-18 11:24 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-18T15:53:53Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-18T15:53:53Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-18T15:53:53Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9615, lo 0.9456, hi 0.9771, unit 30,315 of 31,529, outcome CANNOT_TELL, as printed: M3 and above, every window 31,529 30,315 773 441 96.2 95.9 to 96.4 94.6 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,511
row-record quake.cover.m4: value 0.9851, lo 0.9783, hi 0.9934, unit 30,941 of 31,409, outcome ABOVE, as printed: M4 and above 31,409 30,941 462 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,517
row-record quake.cover.m5: value 0.9966, lo 0.9936, hi 0.9989, unit 31,421 of 31,529, outcome ABOVE, as printed: M5 and above 31,529 31,421 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 28,940
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,524 of 31,529, outcome ABOVE, as printed: M6 and above 31,529 31,524 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,074
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,528 of 31,529, outcome ABOVE, as printed: M7 and above 31,529 31,528 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,413
row-record quake.cover.m3.day: value 0.9883, lo 0.9797, hi 0.9934, unit 9,493 of 9,605, outcome ABOVE, as printed: M3 and above, 1 day 9,605 9,493 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,940
row-record quake.cover.m3.week: value 0.9734, lo 0.9591, hi 0.9833, unit 9,239 of 9,491, outcome ABOVE, as printed: M3 and above, 1 week 9,491 9,239 143 109 97.3 97.0 to 97.7 95.9 to 98.3 above 82 3,643
row-record quake.cover.m3.month: value 0.9576, lo 0.9385, hi 0.9752, unit 8,672 of 9,056, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,056 8,672 231 153 95.8 95.3 to 96.2 93.8 to 97.5 cannot tell (STRADDLES_EDGE) 79 1,716
row-record quake.cover.m3.year: value 0.862, lo 0.7908, hi 0.9395, unit 2,911 of 3,377, outcome BELOW, as printed: M3 and above, 1 year 3,377 2,911 346 120 86.2 85.0 to 87.3 79.1 to 94.0 below 42 212
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9932, unit 155,807 of 157,603, outcome ABOVE, as printed: every magnitude, every window 157,603 155,807 1,348 448 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,517
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 302 of 116,204, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,204 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0343, lo 0.0172, hi 0.0498, unit 592 of 17,274, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,274 592 2.4 3.4 3.2 to 3.7 1.7 to 5.0 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0649, lo 0.0408, hi 0.0917, unit 410 of 6,319, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,319 410 7.1 6.5 5.9 to 7.1 4.1 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1032, lo 0.0702, hi 0.1339, unit 578 of 5,599, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,599 578 14.3 10.3 9.6 to 11.2 7.0 to 13.4 below 77
row-record quake.prob.20_40: value 0.193, lo 0.1487, hi 0.2397, unit 939 of 4,865, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,865 939 28.5 19.3 18.2 to 20.4 14.9 to 24.0 below 74
row-record quake.prob.40_60: value 0.3357, lo 0.2551, hi 0.4139, unit 892 of 2,657, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,657 892 49.3 33.6 31.8 to 35.4 25.5 to 41.4 below 58
row-record quake.prob.60_80: value 0.432, lo 0.3117, hi 0.564, unit 791 of 1,831, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,831 791 69.6 43.2 40.9 to 45.5 31.2 to 56.4 below 46
row-record quake.prob.80_90: value 0.6364, lo 0.4982, hi 0.7725, unit 476 of 748, outcome BELOW, as printed: 80 to 90 percent, not including 90 748 476 85.0 63.6 60.1 to 67.0 49.8 to 77.2 below 37
row-record quake.prob.90_99: value 0.7699, lo 0.6667, hi 0.8571, unit 639 of 830, outcome BELOW, as printed: 90 to 99 percent, not including 99 830 639 95.2 77.0 74.0 to 79.7 66.7 to 85.7 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9586, hi 0.9902, unit 1,247 of 1,276, outcome BELOW, as printed: 99 to 100 percent 1,276 1,247 99.9 97.7 96.8 to 98.4 95.9 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0045, unit 60 of 31,529, outcome CONSISTENT, as printed: 60 of 31,529 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3124, lo 0.2407, hi 0.3896, unit 5,562 of 17,806, outcome BELOW, as printed: every magnitude, every window 17,806 5,562 42.0 31.2 30.6 to 31.9 24.1 to 39.0 below 77
row-record quake.prob10.m3: value 0.3055, lo 0.2304, hi 0.3855, unit 3,800 of 12,438, outcome BELOW, as printed: M3 and above 12,438 3,800 44.6 30.6 29.8 to 31.4 23.0 to 38.6 below 77
row-record quake.prob10.m4up: value 0.3282, lo 0.2441, hi 0.4198, unit 1,762 of 5,368, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,368 1,762 35.9 32.8 31.6 to 34.1 24.4 to 42.0 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2385, lo 0.1412, hi 0.3416, unit 336 of 1,409, outcome BELOW, as printed: every magnitude, 1 day 1,409 336 36.2 23.8 21.7 to 26.1 14.1 to 34.2 below 54
row-record quake.prob10.week: value 0.2133, lo 0.1344, hi 0.3123, unit 874 of 4,097, outcome BELOW, as printed: every magnitude, 1 week 4,097 874 36.8 21.3 20.1 to 22.6 13.4 to 31.2 below 73
row-record quake.prob10.month: value 0.2421, lo 0.168, hi 0.3297, unit 1,748 of 7,220, outcome BELOW, as printed: every magnitude, 1 month 7,220 1,748 39.8 24.2 23.2 to 25.2 16.8 to 33.0 below 75
row-record quake.prob10.year: value 0.5126, lo 0.4216, hi 0.5963, unit 2,604 of 5,080, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,080 2,604 50.9 51.3 49.9 to 52.6 42.2 to 59.6 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9269, lo 0.8796, hi 0.9551, unit 659 of 711, outcome CANNOT_TELL, as printed: 659 of 711 inside, 92.7 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-18 16:24 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-18T20:22:51Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-18T20:22:51Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-18T20:22:51Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9615, lo 0.9456, hi 0.9771, unit 30,332 of 31,547, outcome CANNOT_TELL, as printed: M3 and above, every window 31,547 30,332 773 442 96.2 95.9 to 96.4 94.6 to 97.7 cannot tell (STRADDLES_EDGE) 82 12,516
row-record quake.cover.m4: value 0.9851, lo 0.9783, hi 0.9934, unit 30,959 of 31,427, outcome ABOVE, as printed: M4 and above 31,427 30,959 462 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,529
row-record quake.cover.m5: value 0.9966, lo 0.9936, hi 0.9989, unit 31,439 of 31,547, outcome ABOVE, as printed: M5 and above 31,547 31,439 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 28,956
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,542 of 31,547, outcome ABOVE, as printed: M6 and above 31,547 31,542 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,091
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,546 of 31,547, outcome ABOVE, as printed: M7 and above 31,547 31,546 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,430
row-record quake.cover.m3.day: value 0.9883, lo 0.9797, hi 0.9934, unit 9,498 of 9,610, outcome ABOVE, as printed: M3 and above, 1 day 9,610 9,498 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,944
row-record quake.cover.m3.week: value 0.9735, lo 0.9591, hi 0.9833, unit 9,243 of 9,495, outcome ABOVE, as printed: M3 and above, 1 week 9,495 9,243 143 109 97.4 97.0 to 97.7 95.9 to 98.3 above 82 3,644
row-record quake.cover.m3.month: value 0.9575, lo 0.9383, hi 0.975, unit 8,676 of 9,061, outcome CANNOT_TELL, as printed: M3 and above, 1 month 9,061 8,676 231 154 95.8 95.3 to 96.2 93.8 to 97.5 cannot tell (STRADDLES_EDGE) 79 1,716
row-record quake.cover.m3.year: value 0.8622, lo 0.7911, hi 0.9395, unit 2,915 of 3,381, outcome BELOW, as printed: M3 and above, 1 year 3,381 2,915 346 120 86.2 85.0 to 87.3 79.1 to 94.0 below 42 212
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9932, unit 155,897 of 157,694, outcome ABOVE, as printed: every magnitude, every window 157,694 155,897 1,348 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,585
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 302 of 116,268, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,268 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0343, lo 0.0171, hi 0.0498, unit 592 of 17,283, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,283 592 2.4 3.4 3.2 to 3.7 1.7 to 5.0 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.065, lo 0.0409, hi 0.0918, unit 411 of 6,325, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,325 411 7.1 6.5 5.9 to 7.1 4.1 to 9.2 consistent 80
row-record quake.prob.10_20: value 0.1032, lo 0.0702, hi 0.1339, unit 578 of 5,601, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,601 578 14.3 10.3 9.6 to 11.1 7.0 to 13.4 below 77
row-record quake.prob.20_40: value 0.1931, lo 0.1489, hi 0.2397, unit 940 of 4,867, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,867 940 28.5 19.3 18.2 to 20.4 14.9 to 24.0 below 74
row-record quake.prob.40_60: value 0.3361, lo 0.2557, hi 0.4151, unit 894 of 2,660, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,660 894 49.3 33.6 31.8 to 35.4 25.6 to 41.5 below 58
row-record quake.prob.60_80: value 0.4321, lo 0.3114, hi 0.5643, unit 792 of 1,833, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,833 792 69.6 43.2 41.0 to 45.5 31.1 to 56.4 below 46
row-record quake.prob.80_90: value 0.6364, lo 0.4982, hi 0.7725, unit 476 of 748, outcome BELOW, as printed: 80 to 90 percent, not including 90 748 476 85.0 63.6 60.1 to 67.0 49.8 to 77.2 below 37
row-record quake.prob.90_99: value 0.7699, lo 0.6667, hi 0.8571, unit 639 of 830, outcome BELOW, as printed: 90 to 99 percent, not including 99 830 639 95.2 77.0 74.0 to 79.7 66.7 to 85.7 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9588, hi 0.9902, unit 1,250 of 1,279, outcome BELOW, as printed: 99 to 100 percent 1,279 1,250 99.9 97.7 96.8 to 98.4 95.9 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0045, unit 60 of 31,547, outcome CONSISTENT, as printed: 60 of 31,547 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3125, lo 0.2409, hi 0.3897, unit 5,569 of 17,818, outcome BELOW, as printed: every magnitude, every window 17,818 5,569 42.0 31.2 30.6 to 31.9 24.1 to 39.0 below 77
row-record quake.prob10.m3: value 0.3057, lo 0.2304, hi 0.3857, unit 3,804 of 12,445, outcome BELOW, as printed: M3 and above 12,445 3,804 44.6 30.6 29.8 to 31.4 23.0 to 38.6 below 77
row-record quake.prob10.m4up: value 0.3285, lo 0.2443, hi 0.4197, unit 1,765 of 5,373, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,373 1,765 35.9 32.9 31.6 to 34.1 24.4 to 42.0 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2385, lo 0.1412, hi 0.3416, unit 336 of 1,409, outcome BELOW, as printed: every magnitude, 1 day 1,409 336 36.2 23.8 21.7 to 26.1 14.1 to 34.2 below 54
row-record quake.prob10.week: value 0.2133, lo 0.1343, hi 0.3123, unit 874 of 4,098, outcome BELOW, as printed: every magnitude, 1 week 4,098 874 36.8 21.3 20.1 to 22.6 13.4 to 31.2 below 73
row-record quake.prob10.month: value 0.2424, lo 0.169, hi 0.3301, unit 1,752 of 7,227, outcome BELOW, as printed: every magnitude, 1 month 7,227 1,752 39.8 24.2 23.3 to 25.2 16.9 to 33.0 below 75
row-record quake.prob10.year: value 0.5128, lo 0.4219, hi 0.5966, unit 2,607 of 5,084, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,084 2,607 50.9 51.3 49.9 to 52.6 42.2 to 59.7 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.927, lo 0.8796, hi 0.9551, unit 660 of 712, outcome CANNOT_TELL, as printed: 660 of 712 inside, 92.7 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-18 19:54 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-18T22:39:19Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-18T22:39:19Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-18T22:39:19Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9615, lo 0.9459, hi 0.9764, unit 30,337 of 31,553, outcome CANNOT_TELL, as printed: M3 and above, every window 31,553 30,337 774 442 96.2 95.9 to 96.4 94.6 to 97.6 cannot tell (STRADDLES_EDGE) 82 12,518
row-record quake.cover.m4: value 0.9851, lo 0.978, hi 0.993, unit 30,964 of 31,433, outcome ABOVE, as printed: M4 and above 31,433 30,964 463 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,535
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,445 of 31,553, outcome ABOVE, as printed: M5 and above 31,553 31,445 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 28,962
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,548 of 31,553, outcome ABOVE, as printed: M6 and above 31,553 31,548 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,097
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,552 of 31,553, outcome ABOVE, as printed: M7 and above 31,553 31,552 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,436
row-record quake.cover.m3.day: value 0.9883, lo 0.9797, hi 0.9933, unit 9,501 of 9,613, outcome ABOVE, as printed: M3 and above, 1 day 9,613 9,501 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,946
row-record quake.cover.m3.week: value 0.9734, lo 0.9595, hi 0.983, unit 9,243 of 9,496, outcome ABOVE, as printed: M3 and above, 1 week 9,496 9,243 144 109 97.3 97.0 to 97.6 96.0 to 98.3 above 82 3,644
row-record quake.cover.m3.month: value 0.9575, lo 0.9388, hi 0.9738, unit 8,678 of 9,063, outcome CONSISTENT, as printed: M3 and above, 1 month 9,063 8,678 231 154 95.8 95.3 to 96.2 93.9 to 97.4 consistent 79 1,716
row-record quake.cover.m3.year: value 0.8622, lo 0.7939, hi 0.938, unit 2,915 of 3,381, outcome BELOW, as printed: M3 and above, 1 year 3,381 2,915 346 120 86.2 85.0 to 87.3 79.4 to 93.8 below 42 212
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9931, unit 155,925 of 157,724, outcome ABOVE, as printed: every magnitude, every window 157,724 155,925 1,350 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,611
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 302 of 116,291, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,291 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0343, lo 0.0182, hi 0.0505, unit 593 of 17,287, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,287 593 2.4 3.4 3.2 to 3.7 1.8 to 5.1 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.065, lo 0.0409, hi 0.0904, unit 411 of 6,325, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,325 411 7.1 6.5 5.9 to 7.1 4.1 to 9.0 consistent 80
row-record quake.prob.10_20: value 0.1033, lo 0.071, hi 0.1358, unit 579 of 5,604, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,604 579 14.4 10.3 9.6 to 11.2 7.1 to 13.6 below 77
row-record quake.prob.20_40: value 0.1931, lo 0.1505, hi 0.2369, unit 940 of 4,867, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,867 940 28.5 19.3 18.2 to 20.4 15.0 to 23.7 below 74
row-record quake.prob.40_60: value 0.3361, lo 0.2541, hi 0.4186, unit 894 of 2,660, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,660 894 49.3 33.6 31.8 to 35.4 25.4 to 41.9 below 58
row-record quake.prob.60_80: value 0.4321, lo 0.3057, hi 0.5618, unit 792 of 1,833, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,833 792 69.6 43.2 41.0 to 45.5 30.6 to 56.2 below 46
row-record quake.prob.80_90: value 0.6364, lo 0.4941, hi 0.7722, unit 476 of 748, outcome BELOW, as printed: 80 to 90 percent, not including 90 748 476 85.0 63.6 60.1 to 67.0 49.4 to 77.2 below 37
row-record quake.prob.90_99: value 0.7699, lo 0.6658, hi 0.8603, unit 639 of 830, outcome BELOW, as printed: 90 to 99 percent, not including 99 830 639 95.2 77.0 74.0 to 79.7 66.6 to 86.0 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9572, hi 0.9896, unit 1,250 of 1,279, outcome BELOW, as printed: 99 to 100 percent 1,279 1,250 99.9 97.7 96.8 to 98.4 95.7 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0046, unit 60 of 31,553, outcome CONSISTENT, as printed: 60 of 31,553 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3126, lo 0.2432, hi 0.3843, unit 5,570 of 17,821, outcome BELOW, as printed: every magnitude, every window 17,821 5,570 42.0 31.3 30.6 to 31.9 24.3 to 38.4 below 77
row-record quake.prob10.m3: value 0.3057, lo 0.2324, hi 0.3853, unit 3,805 of 12,448, outcome BELOW, as printed: M3 and above 12,448 3,805 44.6 30.6 29.8 to 31.4 23.2 to 38.5 below 77
row-record quake.prob10.m4up: value 0.3285, lo 0.2394, hi 0.4143, unit 1,765 of 5,373, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,373 1,765 35.9 32.9 31.6 to 34.1 23.9 to 41.4 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2383, lo 0.137, hi 0.3388, unit 336 of 1,410, outcome BELOW, as printed: every magnitude, 1 day 1,410 336 36.2 23.8 21.7 to 26.1 13.7 to 33.9 below 54
row-record quake.prob10.week: value 0.2135, lo 0.1319, hi 0.3089, unit 875 of 4,099, outcome BELOW, as printed: every magnitude, 1 week 4,099 875 36.8 21.3 20.1 to 22.6 13.2 to 30.9 below 73
row-record quake.prob10.month: value 0.2424, lo 0.1718, hi 0.3254, unit 1,752 of 7,228, outcome BELOW, as printed: every magnitude, 1 month 7,228 1,752 39.8 24.2 23.3 to 25.2 17.2 to 32.5 below 75
row-record quake.prob10.year: value 0.5128, lo 0.4172, hi 0.5976, unit 2,607 of 5,084, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,084 2,607 50.9 51.3 49.9 to 52.6 41.7 to 59.8 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.927, lo 0.8798, hi 0.9545, unit 660 of 712, outcome CANNOT_TELL, as printed: 660 of 712 inside, 92.7 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-18 23:11 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-19T03:06:43Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-19T03:06:43Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-19T03:06:43Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9615, lo 0.9459, hi 0.9764, unit 30,353 of 31,569, outcome CANNOT_TELL, as printed: M3 and above, every window 31,569 30,353 774 442 96.2 95.9 to 96.4 94.6 to 97.6 cannot tell (STRADDLES_EDGE) 82 12,527
row-record quake.cover.m4: value 0.9851, lo 0.9781, hi 0.993, unit 30,980 of 31,449, outcome ABOVE, as printed: M4 and above 31,449 30,980 463 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,547
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,461 of 31,569, outcome ABOVE, as printed: M5 and above 31,569 31,461 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 28,978
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,564 of 31,569, outcome ABOVE, as printed: M6 and above 31,569 31,564 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,113
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,568 of 31,569, outcome ABOVE, as printed: M7 and above 31,569 31,568 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,452
row-record quake.cover.m3.day: value 0.9884, lo 0.9797, hi 0.9933, unit 9,506 of 9,618, outcome ABOVE, as printed: M3 and above, 1 day 9,618 9,506 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,950
row-record quake.cover.m3.week: value 0.9734, lo 0.9596, hi 0.983, unit 9,247 of 9,500, outcome ABOVE, as printed: M3 and above, 1 week 9,500 9,247 144 109 97.3 97.0 to 97.6 96.0 to 98.3 above 82 3,646
row-record quake.cover.m3.month: value 0.9575, lo 0.9388, hi 0.9738, unit 8,684 of 9,069, outcome CONSISTENT, as printed: M3 and above, 1 month 9,069 8,684 231 154 95.8 95.3 to 96.2 93.9 to 97.4 consistent 79 1,718
row-record quake.cover.m3.year: value 0.8622, lo 0.794, hi 0.938, unit 2,916 of 3,382, outcome BELOW, as printed: M3 and above, 1 year 3,382 2,916 346 120 86.2 85.0 to 87.3 79.4 to 93.8 below 42 213
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9931, unit 156,005 of 157,804, outcome ABOVE, as printed: every magnitude, every window 157,804 156,005 1,350 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,680
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 302 of 116,356, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,356 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0343, lo 0.0182, hi 0.0505, unit 593 of 17,295, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,295 593 2.4 3.4 3.2 to 3.7 1.8 to 5.1 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0649, lo 0.0409, hi 0.0904, unit 411 of 6,328, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,328 411 7.1 6.5 5.9 to 7.1 4.1 to 9.0 consistent 80
row-record quake.prob.10_20: value 0.1033, lo 0.071, hi 0.1358, unit 579 of 5,604, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,604 579 14.4 10.3 9.6 to 11.2 7.1 to 13.6 below 77
row-record quake.prob.20_40: value 0.1931, lo 0.1504, hi 0.2367, unit 940 of 4,869, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,869 940 28.5 19.3 18.2 to 20.4 15.0 to 23.7 below 74
row-record quake.prob.40_60: value 0.3358, lo 0.2538, hi 0.4181, unit 894 of 2,662, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,662 894 49.3 33.6 31.8 to 35.4 25.4 to 41.8 below 58
row-record quake.prob.60_80: value 0.4321, lo 0.3057, hi 0.5618, unit 792 of 1,833, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,833 792 69.6 43.2 41.0 to 45.5 30.6 to 56.2 below 46
row-record quake.prob.80_90: value 0.6364, lo 0.4941, hi 0.7722, unit 476 of 748, outcome BELOW, as printed: 80 to 90 percent, not including 90 748 476 85.0 63.6 60.1 to 67.0 49.4 to 77.2 below 37
row-record quake.prob.90_99: value 0.7699, lo 0.6658, hi 0.8603, unit 639 of 830, outcome BELOW, as printed: 90 to 99 percent, not including 99 830 639 95.2 77.0 74.0 to 79.7 66.6 to 86.0 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9572, hi 0.9896, unit 1,250 of 1,279, outcome BELOW, as printed: 99 to 100 percent 1,279 1,250 99.9 97.7 96.8 to 98.4 95.7 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0046, unit 60 of 31,569, outcome CONSISTENT, as printed: 60 of 31,569 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3125, lo 0.2431, hi 0.3843, unit 5,570 of 17,825, outcome BELOW, as printed: every magnitude, every window 17,825 5,570 42.0 31.2 30.6 to 31.9 24.3 to 38.4 below 77
row-record quake.prob10.m3: value 0.3056, lo 0.2323, hi 0.3852, unit 3,805 of 12,452, outcome BELOW, as printed: M3 and above 12,452 3,805 44.6 30.6 29.8 to 31.4 23.2 to 38.5 below 77
row-record quake.prob10.m4up: value 0.3285, lo 0.2394, hi 0.4143, unit 1,765 of 5,373, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,373 1,765 35.9 32.9 31.6 to 34.1 23.9 to 41.4 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2383, lo 0.137, hi 0.3388, unit 336 of 1,410, outcome BELOW, as printed: every magnitude, 1 day 1,410 336 36.2 23.8 21.7 to 26.1 13.7 to 33.9 below 54
row-record quake.prob10.week: value 0.2134, lo 0.1319, hi 0.3089, unit 875 of 4,100, outcome BELOW, as printed: every magnitude, 1 week 4,100 875 36.8 21.3 20.1 to 22.6 13.2 to 30.9 below 73
row-record quake.prob10.month: value 0.2423, lo 0.1718, hi 0.3251, unit 1,752 of 7,231, outcome BELOW, as printed: every magnitude, 1 month 7,231 1,752 39.8 24.2 23.3 to 25.2 17.2 to 32.5 below 75
row-record quake.prob10.year: value 0.5128, lo 0.4172, hi 0.5976, unit 2,607 of 5,084, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,084 2,607 50.9 51.3 49.9 to 52.6 41.7 to 59.8 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.927, lo 0.8798, hi 0.9545, unit 660 of 712, outcome CANNOT_TELL, as printed: 660 of 712 inside, 92.7 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-19 02:28 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-19T05:16:56Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-19T05:16:56Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-19T05:16:56Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9615, lo 0.946, hi 0.9764, unit 30,357 of 31,573, outcome CANNOT_TELL, as printed: M3 and above, every window 31,573 30,357 774 442 96.2 95.9 to 96.4 94.6 to 97.6 cannot tell (STRADDLES_EDGE) 82 12,529
row-record quake.cover.m4: value 0.9851, lo 0.9781, hi 0.993, unit 30,984 of 31,453, outcome ABOVE, as printed: M4 and above 31,453 30,984 463 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,550
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,465 of 31,573, outcome ABOVE, as printed: M5 and above 31,573 31,465 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 28,982
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,568 of 31,573, outcome ABOVE, as printed: M6 and above 31,573 31,568 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,117
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,572 of 31,573, outcome ABOVE, as printed: M7 and above 31,573 31,572 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,456
row-record quake.cover.m3.day: value 0.9884, lo 0.9797, hi 0.9933, unit 9,506 of 9,618, outcome ABOVE, as printed: M3 and above, 1 day 9,618 9,506 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,950
row-record quake.cover.m3.week: value 0.9734, lo 0.9596, hi 0.983, unit 9,248 of 9,501, outcome ABOVE, as printed: M3 and above, 1 week 9,501 9,248 144 109 97.3 97.0 to 97.6 96.0 to 98.3 above 82 3,647
row-record quake.cover.m3.month: value 0.9576, lo 0.9388, hi 0.9738, unit 8,686 of 9,071, outcome CONSISTENT, as printed: M3 and above, 1 month 9,071 8,686 231 154 95.8 95.3 to 96.2 93.9 to 97.4 consistent 79 1,719
row-record quake.cover.m3.year: value 0.8623, lo 0.7941, hi 0.938, unit 2,917 of 3,383, outcome BELOW, as printed: M3 and above, 1 year 3,383 2,917 346 120 86.2 85.0 to 87.4 79.4 to 93.8 below 42 213
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9931, unit 156,025 of 157,824, outcome ABOVE, as printed: every magnitude, every window 157,824 156,025 1,350 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,697
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 302 of 116,373, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,373 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0343, lo 0.0182, hi 0.0505, unit 594 of 17,297, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,297 594 2.4 3.4 3.2 to 3.7 1.8 to 5.1 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0649, lo 0.0409, hi 0.0904, unit 411 of 6,328, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,328 411 7.1 6.5 5.9 to 7.1 4.1 to 9.0 consistent 80
row-record quake.prob.10_20: value 0.1033, lo 0.071, hi 0.1358, unit 579 of 5,604, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,604 579 14.4 10.3 9.6 to 11.2 7.1 to 13.6 below 77
row-record quake.prob.20_40: value 0.1932, lo 0.1507, hi 0.2368, unit 941 of 4,870, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,870 941 28.5 19.3 18.2 to 20.5 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3358, lo 0.2538, hi 0.4181, unit 894 of 2,662, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,662 894 49.3 33.6 31.8 to 35.4 25.4 to 41.8 below 58
row-record quake.prob.60_80: value 0.4321, lo 0.3057, hi 0.5618, unit 792 of 1,833, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,833 792 69.6 43.2 41.0 to 45.5 30.6 to 56.2 below 46
row-record quake.prob.80_90: value 0.6364, lo 0.4941, hi 0.7722, unit 476 of 748, outcome BELOW, as printed: 80 to 90 percent, not including 90 748 476 85.0 63.6 60.1 to 67.0 49.4 to 77.2 below 37
row-record quake.prob.90_99: value 0.7699, lo 0.6658, hi 0.8603, unit 639 of 830, outcome BELOW, as printed: 90 to 99 percent, not including 99 830 639 95.2 77.0 74.0 to 79.7 66.6 to 86.0 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9572, hi 0.9896, unit 1,250 of 1,279, outcome BELOW, as printed: 99 to 100 percent 1,279 1,250 99.9 97.7 96.8 to 98.4 95.7 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0046, unit 60 of 31,573, outcome CONSISTENT, as printed: 60 of 31,573 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3125, lo 0.2431, hi 0.3843, unit 5,571 of 17,826, outcome BELOW, as printed: every magnitude, every window 17,826 5,571 42.0 31.2 30.6 to 31.9 24.3 to 38.4 below 77
row-record quake.prob10.m3: value 0.3056, lo 0.2324, hi 0.3853, unit 3,806 of 12,453, outcome BELOW, as printed: M3 and above 12,453 3,806 44.6 30.6 29.8 to 31.4 23.2 to 38.5 below 77
row-record quake.prob10.m4up: value 0.3285, lo 0.2394, hi 0.4143, unit 1,765 of 5,373, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,373 1,765 35.9 32.9 31.6 to 34.1 23.9 to 41.4 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2383, lo 0.137, hi 0.3388, unit 336 of 1,410, outcome BELOW, as printed: every magnitude, 1 day 1,410 336 36.2 23.8 21.7 to 26.1 13.7 to 33.9 below 54
row-record quake.prob10.week: value 0.2134, lo 0.1319, hi 0.3089, unit 875 of 4,100, outcome BELOW, as printed: every magnitude, 1 week 4,100 875 36.8 21.3 20.1 to 22.6 13.2 to 30.9 below 73
row-record quake.prob10.month: value 0.2424, lo 0.1719, hi 0.3251, unit 1,753 of 7,232, outcome BELOW, as printed: every magnitude, 1 month 7,232 1,753 39.8 24.2 23.3 to 25.2 17.2 to 32.5 below 75
row-record quake.prob10.year: value 0.5128, lo 0.4172, hi 0.5976, unit 2,607 of 5,084, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,084 2,607 50.9 51.3 49.9 to 52.6 41.7 to 59.8 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.927, lo 0.8798, hi 0.9545, unit 660 of 712, outcome CANNOT_TELL, as printed: 660 of 712 inside, 92.7 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-19 05:39 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-19T09:33:01Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-19T09:33:01Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-19T09:33:01Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9615, lo 0.946, hi 0.9764, unit 30,366 of 31,583, outcome CANNOT_TELL, as printed: M3 and above, every window 31,583 30,366 775 442 96.2 95.9 to 96.4 94.6 to 97.6 cannot tell (STRADDLES_EDGE) 82 12,534
row-record quake.cover.m4: value 0.9851, lo 0.9781, hi 0.993, unit 30,994 of 31,463, outcome ABOVE, as printed: M4 and above 31,463 30,994 463 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,556
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,475 of 31,583, outcome ABOVE, as printed: M5 and above 31,583 31,475 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 28,991
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,578 of 31,583, outcome ABOVE, as printed: M6 and above 31,583 31,578 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,127
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,582 of 31,583, outcome ABOVE, as printed: M7 and above 31,583 31,582 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,466
row-record quake.cover.m3.day: value 0.9884, lo 0.9797, hi 0.9933, unit 9,508 of 9,620, outcome ABOVE, as printed: M3 and above, 1 day 9,620 9,508 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,952
row-record quake.cover.m3.week: value 0.9733, lo 0.9593, hi 0.9828, unit 9,251 of 9,505, outcome ABOVE, as printed: M3 and above, 1 week 9,505 9,251 145 109 97.3 97.0 to 97.6 95.9 to 98.3 above 82 3,650
row-record quake.cover.m3.month: value 0.9576, lo 0.9389, hi 0.9738, unit 8,689 of 9,074, outcome CONSISTENT, as printed: M3 and above, 1 month 9,074 8,689 231 154 95.8 95.3 to 96.2 93.9 to 97.4 consistent 80 1,719
row-record quake.cover.m3.year: value 0.8623, lo 0.7942, hi 0.938, unit 2,918 of 3,384, outcome BELOW, as printed: M3 and above, 1 year 3,384 2,918 346 120 86.2 85.0 to 87.4 79.4 to 93.8 below 42 213
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9931, unit 156,074 of 157,874, outcome ABOVE, as printed: every magnitude, every window 157,874 156,074 1,351 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,737
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 302 of 116,410, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,410 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0344, lo 0.0183, hi 0.0506, unit 595 of 17,303, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,303 595 2.4 3.4 3.2 to 3.7 1.8 to 5.1 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0649, lo 0.0409, hi 0.0904, unit 411 of 6,329, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,329 411 7.1 6.5 5.9 to 7.1 4.1 to 9.0 consistent 80
row-record quake.prob.10_20: value 0.1035, lo 0.0712, hi 0.136, unit 580 of 5,606, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,606 580 14.4 10.3 9.6 to 11.2 7.1 to 13.6 below 78
row-record quake.prob.20_40: value 0.1931, lo 0.1507, hi 0.2368, unit 941 of 4,872, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,872 941 28.5 19.3 18.2 to 20.4 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3357, lo 0.2536, hi 0.418, unit 894 of 2,663, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,663 894 49.4 33.6 31.8 to 35.4 25.4 to 41.8 below 58
row-record quake.prob.60_80: value 0.4321, lo 0.3057, hi 0.5618, unit 792 of 1,833, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,833 792 69.6 43.2 41.0 to 45.5 30.6 to 56.2 below 46
row-record quake.prob.80_90: value 0.6364, lo 0.4941, hi 0.7722, unit 476 of 748, outcome BELOW, as printed: 80 to 90 percent, not including 90 748 476 85.0 63.6 60.1 to 67.0 49.4 to 77.2 below 37
row-record quake.prob.90_99: value 0.769, lo 0.6651, hi 0.8584, unit 639 of 831, outcome BELOW, as printed: 90 to 99 percent, not including 99 831 639 95.2 76.9 73.9 to 79.6 66.5 to 85.8 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9572, hi 0.9896, unit 1,250 of 1,279, outcome BELOW, as printed: 99 to 100 percent 1,279 1,250 99.9 97.7 96.8 to 98.4 95.7 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0046, unit 60 of 31,583, outcome CONSISTENT, as printed: 60 of 31,583 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3125, lo 0.243, hi 0.3842, unit 5,572 of 17,832, outcome BELOW, as printed: every magnitude, every window 17,832 5,572 42.0 31.2 30.6 to 31.9 24.3 to 38.4 below 78
row-record quake.prob10.m3: value 0.3056, lo 0.2322, hi 0.3851, unit 3,807 of 12,457, outcome BELOW, as printed: M3 and above 12,457 3,807 44.6 30.6 29.8 to 31.4 23.2 to 38.5 below 78
row-record quake.prob10.m4up: value 0.3284, lo 0.2394, hi 0.4143, unit 1,765 of 5,375, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,375 1,765 35.9 32.8 31.6 to 34.1 23.9 to 41.4 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2383, lo 0.137, hi 0.3388, unit 336 of 1,410, outcome BELOW, as printed: every magnitude, 1 day 1,410 336 36.2 23.8 21.7 to 26.1 13.7 to 33.9 below 54
row-record quake.prob10.week: value 0.2134, lo 0.1319, hi 0.3089, unit 875 of 4,100, outcome BELOW, as printed: every magnitude, 1 week 4,100 875 36.8 21.3 20.1 to 22.6 13.2 to 30.9 below 73
row-record quake.prob10.month: value 0.2424, lo 0.1719, hi 0.3253, unit 1,754 of 7,235, outcome BELOW, as printed: every magnitude, 1 month 7,235 1,754 39.8 24.2 23.3 to 25.2 17.2 to 32.5 below 76
row-record quake.prob10.year: value 0.5125, lo 0.4172, hi 0.5976, unit 2,607 of 5,087, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,087 2,607 50.9 51.2 49.9 to 52.6 41.7 to 59.8 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9271, lo 0.8803, hi 0.9546, unit 661 of 713, outcome CANNOT_TELL, as printed: 661 of 713 inside, 92.7 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-19 08:56 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-19T11:45:24Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-19T11:45:24Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-19T11:45:24Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9615, lo 0.946, hi 0.9764, unit 30,372 of 31,589, outcome CANNOT_TELL, as printed: M3 and above, every window 31,589 30,372 775 442 96.2 95.9 to 96.4 94.6 to 97.6 cannot tell (STRADDLES_EDGE) 82 12,537
row-record quake.cover.m4: value 0.9851, lo 0.9781, hi 0.993, unit 31,000 of 31,469, outcome ABOVE, as printed: M4 and above 31,469 31,000 463 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,561
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,481 of 31,589, outcome ABOVE, as printed: M5 and above 31,589 31,481 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 28,996
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,584 of 31,589, outcome ABOVE, as printed: M6 and above 31,589 31,584 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,133
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,588 of 31,589, outcome ABOVE, as printed: M7 and above 31,589 31,588 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,472
row-record quake.cover.m3.day: value 0.9884, lo 0.9797, hi 0.9933, unit 9,509 of 9,621, outcome ABOVE, as printed: M3 and above, 1 day 9,621 9,509 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,953
row-record quake.cover.m3.week: value 0.9733, lo 0.9594, hi 0.9828, unit 9,255 of 9,509, outcome ABOVE, as printed: M3 and above, 1 week 9,509 9,255 145 109 97.3 97.0 to 97.6 95.9 to 98.3 above 82 3,652
row-record quake.cover.m3.month: value 0.9576, lo 0.9389, hi 0.9738, unit 8,689 of 9,074, outcome CONSISTENT, as printed: M3 and above, 1 month 9,074 8,689 231 154 95.8 95.3 to 96.2 93.9 to 97.4 consistent 80 1,719
row-record quake.cover.m3.year: value 0.8623, lo 0.7942, hi 0.9381, unit 2,919 of 3,385, outcome BELOW, as printed: M3 and above, 1 year 3,385 2,919 346 120 86.2 85.0 to 87.4 79.4 to 93.8 below 42 213
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9931, unit 156,104 of 157,904, outcome ABOVE, as printed: every magnitude, every window 157,904 156,104 1,351 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,762
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 302 of 116,432, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,432 302 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0344, lo 0.0184, hi 0.0506, unit 596 of 17,307, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,307 596 2.4 3.4 3.2 to 3.7 1.8 to 5.1 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0649, lo 0.0409, hi 0.0904, unit 411 of 6,330, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,330 411 7.1 6.5 5.9 to 7.1 4.1 to 9.0 consistent 80
row-record quake.prob.10_20: value 0.1034, lo 0.0712, hi 0.1359, unit 580 of 5,607, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,607 580 14.3 10.3 9.6 to 11.2 7.1 to 13.6 below 78
row-record quake.prob.20_40: value 0.1933, lo 0.151, hi 0.2369, unit 942 of 4,873, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,873 942 28.5 19.3 18.2 to 20.5 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3357, lo 0.2536, hi 0.418, unit 894 of 2,663, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,663 894 49.4 33.6 31.8 to 35.4 25.4 to 41.8 below 58
row-record quake.prob.60_80: value 0.4324, lo 0.3065, hi 0.5618, unit 793 of 1,834, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,834 793 69.6 43.2 41.0 to 45.5 30.6 to 56.2 below 46
row-record quake.prob.80_90: value 0.6364, lo 0.4941, hi 0.7722, unit 476 of 748, outcome BELOW, as printed: 80 to 90 percent, not including 90 748 476 85.0 63.6 60.1 to 67.0 49.4 to 77.2 below 37
row-record quake.prob.90_99: value 0.769, lo 0.6651, hi 0.8584, unit 639 of 831, outcome BELOW, as printed: 90 to 99 percent, not including 99 831 639 95.2 76.9 73.9 to 79.6 66.5 to 85.8 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9572, hi 0.9896, unit 1,250 of 1,279, outcome BELOW, as printed: 99 to 100 percent 1,279 1,250 99.9 97.7 96.8 to 98.4 95.7 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0046, unit 61 of 31,589, outcome CONSISTENT, as printed: 61 of 31,589 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3125, lo 0.2432, hi 0.3842, unit 5,574 of 17,835, outcome BELOW, as printed: every magnitude, every window 17,835 5,574 42.0 31.2 30.6 to 31.9 24.3 to 38.4 below 78
row-record quake.prob10.m3: value 0.3056, lo 0.2323, hi 0.3851, unit 3,808 of 12,459, outcome BELOW, as printed: M3 and above 12,459 3,808 44.6 30.6 29.8 to 31.4 23.2 to 38.5 below 78
row-record quake.prob10.m4up: value 0.3285, lo 0.2397, hi 0.4143, unit 1,766 of 5,376, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,376 1,766 35.9 32.9 31.6 to 34.1 24.0 to 41.4 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2383, lo 0.137, hi 0.3388, unit 336 of 1,410, outcome BELOW, as printed: every magnitude, 1 day 1,410 336 36.2 23.8 21.7 to 26.1 13.7 to 33.9 below 54
row-record quake.prob10.week: value 0.2134, lo 0.1318, hi 0.3089, unit 875 of 4,101, outcome BELOW, as printed: every magnitude, 1 week 4,101 875 36.8 21.3 20.1 to 22.6 13.2 to 30.9 below 73
row-record quake.prob10.month: value 0.2424, lo 0.1719, hi 0.3253, unit 1,754 of 7,235, outcome BELOW, as printed: every magnitude, 1 month 7,235 1,754 39.8 24.2 23.3 to 25.2 17.2 to 32.5 below 76
row-record quake.prob10.year: value 0.5127, lo 0.4175, hi 0.5978, unit 2,609 of 5,089, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,089 2,609 50.9 51.3 49.9 to 52.6 41.8 to 59.8 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9271, lo 0.8803, hi 0.9546, unit 661 of 713, outcome CANNOT_TELL, as printed: 661 of 713 inside, 92.7 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-19 12:15 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-19T16:12:08Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-19T16:12:08Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-19T16:12:08Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9614, lo 0.946, hi 0.9764, unit 30,395 of 31,614, outcome CANNOT_TELL, as printed: M3 and above, every window 31,614 30,395 777 442 96.1 95.9 to 96.4 94.6 to 97.6 cannot tell (STRADDLES_EDGE) 82 12,552
row-record quake.cover.m4: value 0.9851, lo 0.9781, hi 0.993, unit 31,024 of 31,494, outcome ABOVE, as printed: M4 and above 31,494 31,024 464 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,581
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,506 of 31,614, outcome ABOVE, as printed: M5 and above 31,614 31,506 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,020
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,609 of 31,614, outcome ABOVE, as printed: M6 and above 31,614 31,609 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,158
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,613 of 31,614, outcome ABOVE, as printed: M7 and above 31,614 31,613 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,497
row-record quake.cover.m3.day: value 0.9884, lo 0.9797, hi 0.9933, unit 9,517 of 9,629, outcome ABOVE, as printed: M3 and above, 1 day 9,629 9,517 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,961
row-record quake.cover.m3.week: value 0.9733, lo 0.9594, hi 0.9828, unit 9,262 of 9,516, outcome ABOVE, as printed: M3 and above, 1 week 9,516 9,262 145 109 97.3 97.0 to 97.6 95.9 to 98.3 above 82 3,655
row-record quake.cover.m3.month: value 0.9575, lo 0.9389, hi 0.9738, unit 8,692 of 9,078, outcome CONSISTENT, as printed: M3 and above, 1 month 9,078 8,692 232 154 95.8 95.3 to 96.1 93.9 to 97.4 consistent 80 1,721
row-record quake.cover.m3.year: value 0.8623, lo 0.7942, hi 0.9381, unit 2,924 of 3,391, outcome BELOW, as printed: M3 and above, 1 year 3,391 2,924 347 120 86.2 85.0 to 87.4 79.4 to 93.8 below 42 215
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9931, unit 156,226 of 158,029, outcome ABOVE, as printed: every magnitude, every window 158,029 156,226 1,354 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,871
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 303 of 116,531, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,531 303 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0346, lo 0.0185, hi 0.0509, unit 599 of 17,323, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,323 599 2.4 3.5 3.2 to 3.7 1.8 to 5.1 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0649, lo 0.0409, hi 0.0904, unit 411 of 6,330, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,330 411 7.1 6.5 5.9 to 7.1 4.1 to 9.0 consistent 80
row-record quake.prob.10_20: value 0.1035, lo 0.0715, hi 0.1361, unit 581 of 5,611, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,611 581 14.3 10.3 9.6 to 11.2 7.1 to 13.6 below 78
row-record quake.prob.20_40: value 0.1936, lo 0.151, hi 0.2373, unit 944 of 4,877, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,877 944 28.5 19.4 18.3 to 20.5 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3357, lo 0.2536, hi 0.418, unit 894 of 2,663, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,663 894 49.4 33.6 31.8 to 35.4 25.4 to 41.8 below 58
row-record quake.prob.60_80: value 0.4319, lo 0.306, hi 0.561, unit 793 of 1,836, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,836 793 69.6 43.2 40.9 to 45.5 30.6 to 56.1 below 46
row-record quake.prob.80_90: value 0.6364, lo 0.4941, hi 0.7722, unit 476 of 748, outcome BELOW, as printed: 80 to 90 percent, not including 90 748 476 85.0 63.6 60.1 to 67.0 49.4 to 77.2 below 37
row-record quake.prob.90_99: value 0.769, lo 0.6651, hi 0.8584, unit 639 of 831, outcome BELOW, as printed: 90 to 99 percent, not including 99 831 639 95.2 76.9 73.9 to 79.6 66.5 to 85.8 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9572, hi 0.9896, unit 1,250 of 1,279, outcome BELOW, as printed: 99 to 100 percent 1,279 1,250 99.9 97.7 96.8 to 98.4 95.7 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0046, unit 61 of 31,614, outcome CONSISTENT, as printed: 61 of 31,614 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3125, lo 0.2432, hi 0.3842, unit 5,577 of 17,845, outcome BELOW, as printed: every magnitude, every window 17,845 5,577 42.0 31.2 30.6 to 31.9 24.3 to 38.4 below 78
row-record quake.prob10.m3: value 0.3057, lo 0.2322, hi 0.3852, unit 3,811 of 12,467, outcome BELOW, as printed: M3 and above 12,467 3,811 44.6 30.6 29.8 to 31.4 23.2 to 38.5 below 78
row-record quake.prob10.m4up: value 0.3284, lo 0.2395, hi 0.4142, unit 1,766 of 5,378, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,378 1,766 35.9 32.8 31.6 to 34.1 23.9 to 41.4 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2383, lo 0.137, hi 0.3388, unit 336 of 1,410, outcome BELOW, as printed: every magnitude, 1 day 1,410 336 36.2 23.8 21.7 to 26.1 13.7 to 33.9 below 54
row-record quake.prob10.week: value 0.2132, lo 0.1317, hi 0.3085, unit 875 of 4,105, outcome BELOW, as printed: every magnitude, 1 week 4,105 875 36.8 21.3 20.1 to 22.6 13.2 to 30.9 below 73
row-record quake.prob10.month: value 0.2425, lo 0.172, hi 0.3253, unit 1,755 of 7,236, outcome BELOW, as printed: every magnitude, 1 month 7,236 1,755 39.8 24.2 23.3 to 25.2 17.2 to 32.5 below 76
row-record quake.prob10.year: value 0.5126, lo 0.4173, hi 0.5977, unit 2,611 of 5,094, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,094 2,611 50.9 51.3 49.9 to 52.6 41.7 to 59.8 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9271, lo 0.8803, hi 0.9546, unit 661 of 713, outcome CANNOT_TELL, as printed: 661 of 713 inside, 92.7 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-19 15:47 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-19T18:23:29Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-19T18:23:29Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-19T18:23:29Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9614, lo 0.9459, hi 0.9764, unit 30,398 of 31,618, outcome CANNOT_TELL, as printed: M3 and above, every window 31,618 30,398 778 442 96.1 95.9 to 96.4 94.6 to 97.6 cannot tell (STRADDLES_EDGE) 82 12,553
row-record quake.cover.m4: value 0.9851, lo 0.9781, hi 0.993, unit 31,028 of 31,498, outcome ABOVE, as printed: M4 and above 31,498 31,028 464 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,584
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,510 of 31,618, outcome ABOVE, as printed: M5 and above 31,618 31,510 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,023
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,613 of 31,618, outcome ABOVE, as printed: M6 and above 31,618 31,613 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,162
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,617 of 31,618, outcome ABOVE, as printed: M7 and above 31,618 31,617 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,501
row-record quake.cover.m3.day: value 0.9884, lo 0.9797, hi 0.9933, unit 9,517 of 9,629, outcome ABOVE, as printed: M3 and above, 1 day 9,629 9,517 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,961
row-record quake.cover.m3.week: value 0.9732, lo 0.9593, hi 0.9827, unit 9,263 of 9,518, outcome ABOVE, as printed: M3 and above, 1 week 9,518 9,263 146 109 97.3 97.0 to 97.6 95.9 to 98.3 above 82 3,656
row-record quake.cover.m3.month: value 0.9575, lo 0.9389, hi 0.9738, unit 8,693 of 9,079, outcome CONSISTENT, as printed: M3 and above, 1 month 9,079 8,693 232 154 95.8 95.3 to 96.1 93.9 to 97.4 consistent 80 1,721
row-record quake.cover.m3.year: value 0.8623, lo 0.7942, hi 0.9381, unit 2,925 of 3,392, outcome BELOW, as printed: M3 and above, 1 year 3,392 2,925 347 120 86.2 85.0 to 87.4 79.4 to 93.8 below 42 215
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9931, unit 156,245 of 158,049, outcome ABOVE, as printed: every magnitude, every window 158,049 156,245 1,355 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,886
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 303 of 116,545, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,545 303 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0346, lo 0.0185, hi 0.0509, unit 600 of 17,326, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,326 600 2.4 3.5 3.2 to 3.8 1.8 to 5.1 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.0649, lo 0.0409, hi 0.0904, unit 411 of 6,331, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,331 411 7.1 6.5 5.9 to 7.1 4.1 to 9.0 consistent 80
row-record quake.prob.10_20: value 0.1035, lo 0.0715, hi 0.1361, unit 581 of 5,611, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,611 581 14.3 10.3 9.6 to 11.2 7.1 to 13.6 below 78
row-record quake.prob.20_40: value 0.1935, lo 0.1509, hi 0.2373, unit 944 of 4,878, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,878 944 28.5 19.4 18.3 to 20.5 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3357, lo 0.2536, hi 0.418, unit 894 of 2,663, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,663 894 49.4 33.6 31.8 to 35.4 25.4 to 41.8 below 58
row-record quake.prob.60_80: value 0.4322, lo 0.306, hi 0.5618, unit 794 of 1,837, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,837 794 69.6 43.2 41.0 to 45.5 30.6 to 56.2 below 46
row-record quake.prob.80_90: value 0.6364, lo 0.4941, hi 0.7722, unit 476 of 748, outcome BELOW, as printed: 80 to 90 percent, not including 90 748 476 85.0 63.6 60.1 to 67.0 49.4 to 77.2 below 37
row-record quake.prob.90_99: value 0.769, lo 0.6651, hi 0.8584, unit 639 of 831, outcome BELOW, as printed: 90 to 99 percent, not including 99 831 639 95.2 76.9 73.9 to 79.6 66.5 to 85.8 below 32
row-record quake.prob.99_100: value 0.9773, lo 0.9572, hi 0.9896, unit 1,250 of 1,279, outcome BELOW, as printed: 99 to 100 percent 1,279 1,250 99.9 97.7 96.8 to 98.4 95.7 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0046, unit 61 of 31,618, outcome CONSISTENT, as printed: 61 of 31,618 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3125, lo 0.2432, hi 0.3842, unit 5,578 of 17,847, outcome BELOW, as printed: every magnitude, every window 17,847 5,578 42.0 31.2 30.6 to 31.9 24.3 to 38.4 below 78
row-record quake.prob10.m3: value 0.3057, lo 0.2322, hi 0.3853, unit 3,812 of 12,468, outcome BELOW, as printed: M3 and above 12,468 3,812 44.6 30.6 29.8 to 31.4 23.2 to 38.5 below 78
row-record quake.prob10.m4up: value 0.3283, lo 0.2395, hi 0.4142, unit 1,766 of 5,379, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,379 1,766 35.9 32.8 31.6 to 34.1 23.9 to 41.4 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2383, lo 0.137, hi 0.3388, unit 336 of 1,410, outcome BELOW, as printed: every magnitude, 1 day 1,410 336 36.2 23.8 21.7 to 26.1 13.7 to 33.9 below 54
row-record quake.prob10.week: value 0.2132, lo 0.1317, hi 0.3085, unit 875 of 4,105, outcome BELOW, as printed: every magnitude, 1 week 4,105 875 36.8 21.3 20.1 to 22.6 13.2 to 30.9 below 73
row-record quake.prob10.month: value 0.2425, lo 0.172, hi 0.3253, unit 1,755 of 7,236, outcome BELOW, as printed: every magnitude, 1 month 7,236 1,755 39.8 24.2 23.3 to 25.2 17.2 to 32.5 below 76
row-record quake.prob10.year: value 0.5126, lo 0.4174, hi 0.5977, unit 2,612 of 5,096, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,096 2,612 50.9 51.3 49.9 to 52.6 41.7 to 59.8 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9271, lo 0.8803, hi 0.9546, unit 661 of 713, outcome CANNOT_TELL, as printed: 661 of 713 inside, 92.7 percent, with a sequence interval of 88.0 to 95.5 percent.

## 2026-11-19 19:17 QUAKE desk refresh record: the rows as shipped, recomputed from the run of 2026-11-19T23:05:44Z and the page built from it (durable source for the quake.* ledger rows)
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every line below is read from summary_quake.json of the run at 2026-11-19T23:05:44Z, the same run quake.html prints, and the printed text is found in the rendered page (make_rows.py asserts it)
- II: n/a: no comparison between two runs, numbers copied as printed
- III: holds: above and below the range are separate columns in the cover lines, cannot tell is a reading and never folded into a share
- V: holds: one ruler for the ranges, the stated 95 percent, and the stated chance for the bins, each read on the wider of the Wilson and sequence-group intervals as the plan states
- VI: holds: outcomes as the plan states them, the reading column holds the four outcomes as the plan states them
- R: holds: counts from the summary of 2026-11-19T23:05:44Z, no number typed by hand, display splits keep their label in the claim
- P1: n/a: no quoted text in this record
- P2: holds: each line names the cell and the page names the run date
- P3: holds: labels as the page prints them
- P4: holds: no cause named
- P5: holds: every share has its Wilson and sequence intervals on the page line
- P6: holds: the lines say what the page says and nothing stronger
- P7: holds: ledger rows updated before the page ships, release through ledger/ship.sh
- P8: holds: rows compared with the rendered page text by check_ledger.py at the gate
- P9: holds: plain lines, no semicolons
- P10: n/a: no rule set after the data in this record
row-record quake.cover.m3: value 0.9614, lo 0.9459, hi 0.9763, unit 30,415 of 31,637, outcome CANNOT_TELL, as printed: M3 and above, every window 31,637 30,415 780 442 96.1 95.9 to 96.3 94.6 to 97.6 cannot tell (STRADDLES_EDGE) 82 12,558
row-record quake.cover.m4: value 0.9851, lo 0.9781, hi 0.9929, unit 31,046 of 31,517, outcome ABOVE, as printed: M4 and above 31,517 31,046 465 6 98.5 98.4 to 98.6 97.8 to 99.3 above 81 22,598
row-record quake.cover.m5: value 0.9966, lo 0.9937, hi 0.9987, unit 31,529 of 31,637, outcome ABOVE, as printed: M5 and above 31,637 31,529 107 1 99.7 99.6 to 99.7 99.4 to 99.9 above 82 29,041
row-record quake.cover.m6: value 0.9998, lo 0.9996, hi 1.0, unit 31,632 of 31,637, outcome ABOVE, as printed: M6 and above 31,637 31,632 5 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,180
row-record quake.cover.m7: value 1.0, lo 0.9998, hi 1.0, unit 31,636 of 31,637, outcome ABOVE, as printed: M7 and above 31,637 31,636 1 0 100.0 100.0 to 100.0 100.0 to 100.0 above 82 31,520
row-record quake.cover.m3.day: value 0.9884, lo 0.9798, hi 0.9933, unit 9,523 of 9,635, outcome ABOVE, as printed: M3 and above, 1 day 9,635 9,523 53 59 98.8 98.6 to 99.0 98.0 to 99.3 above 82 6,964
row-record quake.cover.m3.week: value 0.9731, lo 0.9592, hi 0.9825, unit 9,269 of 9,525, outcome ABOVE, as printed: M3 and above, 1 week 9,525 9,269 147 109 97.3 97.0 to 97.6 95.9 to 98.2 above 82 3,658
row-record quake.cover.m3.month: value 0.9574, lo 0.9387, hi 0.9736, unit 8,696 of 9,083, outcome CONSISTENT, as printed: M3 and above, 1 month 9,083 8,696 233 154 95.7 95.3 to 96.1 93.9 to 97.4 consistent 80 1,721
row-record quake.cover.m3.year: value 0.8624, lo 0.7944, hi 0.9382, unit 2,927 of 3,394, outcome BELOW, as printed: M3 and above, 1 year 3,394 2,927 347 120 86.2 85.0 to 87.4 79.4 to 93.8 below 42 215
row-record quake.cover.all: value 0.9886, lo 0.9846, hi 0.9931, unit 156,337 of 158,144, outcome ABOVE, as printed: every magnitude, every window 158,144 156,337 1,358 449 98.9 98.8 to 98.9 98.5 to 99.3 above 82 126,960
row-record quake.prob.0_1: value 0.0026, lo 0.0008, hi 0.0043, unit 303 of 116,613, outcome CONSISTENT, as printed: 0 to 1 percent, not including 1 116,613 303 0.1 0.3 0.2 to 0.3 0.1 to 0.4 consistent 82
row-record quake.prob.1_5: value 0.0347, lo 0.0186, hi 0.0509, unit 601 of 17,338, outcome CANNOT_TELL, as printed: 1 to 5 percent, not including 5 17,338 601 2.4 3.5 3.2 to 3.8 1.9 to 5.1 cannot tell (STRADDLES_EDGE) 82
row-record quake.prob.5_10: value 0.065, lo 0.0409, hi 0.0904, unit 412 of 6,336, outcome CONSISTENT, as printed: 5 to 10 percent, not including 10 6,336 412 7.1 6.5 5.9 to 7.1 4.1 to 9.0 consistent 80
row-record quake.prob.10_20: value 0.1037, lo 0.0717, hi 0.1361, unit 582 of 5,614, outcome BELOW, as printed: 10 to 20 percent, not including 20 5,614 582 14.3 10.4 9.6 to 11.2 7.2 to 13.6 below 78
row-record quake.prob.20_40: value 0.1936, lo 0.1511, hi 0.2373, unit 945 of 4,880, outcome BELOW, as printed: 20 to 40 percent, not including 40 4,880 945 28.5 19.4 18.3 to 20.5 15.1 to 23.7 below 74
row-record quake.prob.40_60: value 0.3361, lo 0.2543, hi 0.4186, unit 896 of 2,666, outcome BELOW, as printed: 40 to 60 percent, not including 60 2,666 896 49.4 33.6 31.8 to 35.4 25.4 to 41.9 below 58
row-record quake.prob.60_80: value 0.4322, lo 0.306, hi 0.5618, unit 794 of 1,837, outcome BELOW, as printed: 60 to 80 percent, not including 80 1,837 794 69.6 43.2 41.0 to 45.5 30.6 to 56.2 below 46
row-record quake.prob.80_90: value 0.6364, lo 0.4941, hi 0.7722, unit 476 of 748, outcome BELOW, as printed: 80 to 90 percent, not including 90 748 476 85.0 63.6 60.1 to 67.0 49.4 to 77.2 below 37
row-record quake.prob.90_99: value 0.769, lo 0.6651, hi 0.8584, unit 639 of 831, outcome BELOW, as printed: 90 to 99 percent, not including 99 831 639 95.2 76.9 73.9 to 79.6 66.5 to 85.8 below 32
row-record quake.prob.99_100: value 0.9774, lo 0.9572, hi 0.9897, unit 1,252 of 1,281, outcome BELOW, as printed: 99 to 100 percent 1,281 1,252 99.9 97.7 96.8 to 98.4 95.7 to 99.0 below 21
row-record quake.prob.mainshock: value 0.0019, lo 0.0, hi 0.0046, unit 61 of 31,637, outcome CONSISTENT, as printed: 61 of 31,637 windows saw one against a mean stated chance of 0.4 percent, and the reading is consistent.
row-record quake.prob10.all: value 0.3127, lo 0.2432, hi 0.3844, unit 5,584 of 17,857, outcome BELOW, as printed: every magnitude, every window 17,857 5,584 42.0 31.3 30.6 to 31.9 24.3 to 38.4 below 78
row-record quake.prob10.m3: value 0.3059, lo 0.2326, hi 0.3855, unit 3,816 of 12,476, outcome BELOW, as printed: M3 and above 12,476 3,816 44.6 30.6 29.8 to 31.4 23.3 to 38.6 below 78
row-record quake.prob10.m4up: value 0.3286, lo 0.2397, hi 0.4146, unit 1,768 of 5,381, outcome CANNOT_TELL, as printed: M4 and above, M5 and above, M6 and above and M7 and above 5,381 1,768 35.9 32.9 31.6 to 34.1 24.0 to 41.5 cannot tell (STRADDLES_EDGE) 53
row-record quake.prob10.day: value 0.2388, lo 0.1368, hi 0.3394, unit 337 of 1,411, outcome BELOW, as printed: every magnitude, 1 day 1,411 337 36.2 23.9 21.7 to 26.2 13.7 to 33.9 below 54
row-record quake.prob10.week: value 0.2132, lo 0.1318, hi 0.3084, unit 876 of 4,108, outcome BELOW, as printed: every magnitude, 1 week 4,108 876 36.7 21.3 20.1 to 22.6 13.2 to 30.8 below 73
row-record quake.prob10.month: value 0.2426, lo 0.172, hi 0.3254, unit 1,756 of 7,238, outcome BELOW, as printed: every magnitude, 1 month 7,238 1,756 39.8 24.3 23.3 to 25.3 17.2 to 32.5 below 76
row-record quake.prob10.year: value 0.5127, lo 0.4176, hi 0.5979, unit 2,615 of 5,100, outcome CANNOT_TELL, as printed: every magnitude, 1 year 5,100 2,615 50.9 51.3 49.9 to 52.6 41.8 to 59.8 cannot tell (STRADDLES_EDGE) 41
row-record quake.first.m3: value 0.9272, lo 0.8808, hi 0.9547, unit 662 of 714, outcome CANNOT_TELL, as printed: 662 of 714 inside, 92.7 percent, with a sequence interval of 88.1 to 95.5 percent.
