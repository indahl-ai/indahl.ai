# CASSANDRA: build notes, written before any warning is set beside a report

PLAN.md is the frozen plan from indahl-ai/calibrations, branch lane-research, commit f2e35ca, copied here unchanged and sealed in data/plan_seal.json. This file fixes the details PLAN.md leaves to the build. It was written after reading only the field names of a one-day warning sample and the file listings of the sources, and before any warning was paired with any report. Nothing here picks a case. Every rule below applies to every warning and every report in the window the same way.

## Sources as read
- Warnings: the IEM watch and warning shapefile service named in PLAN.md section 3, https://mesonet.agron.iastate.edu/cgi-bin/request/gis/watchwarn.py, one file per calendar year, storm-based polygons only (limit1), phenomenon FF, significance W (limitps). Fields read: WFO, ISSUED, EXPIRED, INIT_EXP, ETN, VTEC_YR, STATUS, GTYPE, PROD_ID.
- Reports, primary: NCEI Storm Events bulk files, https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/, StormEvents_details-ftp_v1.0_dYYYY files, keyless. Confirmed keyless on 21 Nov 2026 as PLAN.md asks. Rows with EVENT_TYPE "Flash Flood".
- Reports, secondary: IEM Local Storm Reports, https://mesonet.agron.iastate.edu/cgi-bin/request/gis/lsr.py, CSV, one file per calendar year, rows whose type text is FLASH FLOOD.
- Requests one at a time, 2 seconds apart, user agent heuremen-cassandra/0.1 (+https://indahl.ai/cassandra). Downloads go to data/raw and are read as data only.

## The warning
- One warning is one VTEC event: the key WFO, VTEC year and event number (ETN). If the file holds more than one NEW storm-based row for a key, the earliest issued is the warning and the count of extra rows is printed.
- Issue time: ISSUED. End: EXPIRED, which IEM sets to the event's final expiry after any extension that keeps the event number. INIT_EXP, the first stated expiry, is printed beside it and decides nothing.
- Polygon: the issuance polygon, held from issue to final expiry. Follow-up statements that redraw the polygon are not read. Rings are read by even-odd parity, so a hole is outside.
- In the window: issued from 2008-01-01 00:00 UTC up to 2026-01-01 00:00 UTC, any office, any state or territory in the file.
- A warning whose polygon has fewer than three points or no readable time is held and listed.

## The report
- Storm Events: report time is the begin time (BEGIN_YEARMONTH, BEGIN_DAY, BEGIN_TIME) in the row's CZ_TIMEZONE, turned into UTC. "CST-6" and the like read as the stated offset. A bare zone name reads as its standard offset (EST 5, CST 6, MST 7, PST 8, AKST 9, HST 10, AST 4, SST 11, GST minus 10). Any other zone is held and counted. Report place is BEGIN_LAT, BEGIN_LON. A row with no begin position is held and counted.
- LSR: report time VALID (UTC), place LAT, LON. LSR rows with the same time, place and office are one report (the archive keeps a report again when its remark is corrected). Storm Events rows are one report per EVENT_ID.
- Report files read: the years 2008 to 2025 and, for warnings issued on 31 December 2025 that run into 2026, the 2026 file for times before the last expiry in the window. A 2026 file that is not there leaves those few warnings to the 2025 file alone, and the count is printed.

## The pairing (PLAN.md section 4)
- Hit: at least one report of the source with issue time at or before the report time, report time at or before the final expiry, and the report place inside the polygon.
- Storm Events and LSR are paired separately and never merged.
- Flood warned share: of the reports in the window that have a time and a place, the share inside the polygon of a warning in force at the report time (issue at or before, final expiry at or after). Reports held for time or place are outside both parts of this share and are listed.

## Interval
- Block bootstrap with the block the forecast office and the calendar year of issue (for reports, the office in the row, WFO, and the calendar year of the report time). 2,000 resamples of the blocks with replacement, fixed seed 20261122, 95 percent percentile interval of the ratio of summed hits over summed warnings.

## Outcome (PLAN.md section 5), in the kit's terms
- The run's reading of "likely" is the band [0.5, 1], closed at both ends. heuremen_kit.read with band (0.5, 1.0) and edge closed gives CONSISTENT when the whole interval is at or above 0.5, BELOW when the whole interval is under 0.5, CANNOT_TELL with STRADDLES_EDGE otherwise. ABOVE cannot occur. No size that matters is named, so the both-alternatives test is not applied.
- The secondary cells and the per-year table are read by the same rule and are display only. The headline is cassandra.ffw_hit_share and nothing else.

## Held years (PLAN.md section 5, a gap in either archive)
- Fixed now, on counts that do not depend on any pairing: a year is held from a cell if the warning file or that cell's report file for the year cannot be fetched or read, or if either file holds no record at all for some calendar month of that year. A held year is left out of the cell and listed. It is never filled in.

## Known-good gates
- Format: the fields above are present in every file read.
- Rule selftest: the outcome rule, the pairing and the time zone parse on made-up cases with known answers.
- Raw row: one Storm Events row and one warning are printed raw with the times the run read from them, in CHECKS.md.
- A failed gate turns every outcome into CANNOT_TELL with reason NO_INTERVAL_FORMABLE and keeps the original beside it.

## Labels
- Every output carries "PRELIMINARY: first run, not refereed" and "floods reported, not floods" beside the share, until the referee reads the first run.
