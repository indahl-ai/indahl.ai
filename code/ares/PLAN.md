# ARES: where public conflict trackers agree that armed violence happened

Status: plan only. Nothing here has been run. The build waits until the seven new desks have their first the referee reads and November 27 has passed. The referee reads this plan once before any data is opened. The frame below is fixed now and does not change after the first file is read.

Shape: same as zeus_index/PLAN.md. Claims read, Questions, Data, Frame fixed before any reading, outcomes, and labels for preliminary data.

## 0. Lines that hold everywhere

These come first and every later section obeys them.

1. **No casualties.** No death or injury count appears anywhere: not on the map, not in dot sizes, not in the headline, not in the kit. Death and injury fields are dropped when a file is read and never stored.
2. **Dot size comes from a measure other than casualties** (section 4).
3. **No sides.** Who did what is never coded. Actor, side and dyad name fields are dropped when a file is read. No named parties on the map.
4. **Neutral surfaces.** No flags, no country fills, no borders drawn. Place names are the source's own, quoted. One footnote: "This page takes no position on any border, name or claim."
5. **Delay.** Only months that ended at least 30 days before the run. Never near-live.
6. **Detail.** Province (first-level administrative unit) at the finest. Never coordinates or towns on the page or in the kit.

## 1. Claims read

### UCDP (Uppsala Conflict Data Program)

- Downloads, https://ucdp.uu.se/downloads/: "All datasets are free of charge and licensed under CC BY 4.0", free to redistribute "provided you cite the relevant publications listed with each dataset". The Georeferenced Event Dataset (GED 26.1, https://ucdp.uu.se/downloads/ged/ged261-csv.zip) "covers the world between 1989-01-01 and 2025-12-31". The Candidate Events Dataset is "published at a monthly release cycle" with "not more than a month's lag globally" (latest seen: October 2026, https://ucdp.uu.se/downloads/candidateged/GEDEvent_v26_0_10.csv). UCDP asks: "Always include the Version number in analyses using the dataset".
- Citations, carried on the page: Sundberg and Melander 2013, Journal of Peace Research 50(4), for GED, and Hegre, Croicu, Eck and Högbladh 2020, Research and Politics, doi:10.1177/2053168020935257, for Candidate events.
- An event, GED codebook (ged251.pdf, ged261.pdf): "An incident where armed force was used by an organized actor against another organized actor, or against civilians", resulting "in at least 1 direct death at a specific location and a specific date".
- Place fields: `adm_1` is the "Name of the first order (largest) administrative division where the event took place", a name with no code. `where_prec` 1 to 4 means the event is placed at least to its province, and 4 means "only the first order administrative division where an event happened is known".

### GDELT 2.0 Event Database

- Terms, https://gdeltproject.org/about.html#termsofuse: "available for unlimited and unrestricted use", and "You may redistribute, rehost, republish, and mirror any of the GDELT datasets in any form", with a citation to the GDELT Project and a link to https://www.gdeltproject.org/.
- Access: raw files listed at https://data.gdeltproject.org/gdeltv2/masterfilelist.txt, keyless, from February 19, 2015.
- Fields, https://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf: `QuadClass` "4=Material Conflict", `EventRootCode`, and `ActionGeo_Type`, where 4 is a world city and 5 is a match "to an Administrative Division 1 outside the US". A country-level match gets "the centroid of that country or state". Hammond and Weidmann 2014 (doi:10.1177/2053168014539924): "at the local level major issues of geographic bias exist in how events are reported."

### ACLED: left out

ACLED's license (https://acleddata.com/eula, effective 1 Nov 2026) grants publishing "for non-commercial purposes", says "Commercial entities may not access or use the Content and/or Platforms without first obtaining a corporate license", and requires published work to be "transformative, such that they cannot be reverse engineered to recreate the Licensed Content". Counts by province and month may be read as only "reorganized", which the license says is not enough. Access also needs an account. Heuremen LLC is a company, accounts are outside this lane's rules, and the terms do not clearly allow this map. ACLED is left out. It comes in only with ACLED's written permission and a license that fits.

## 2. Questions

1. For each province and month in the window, do the trackers agree that organized armed violence happened there?
2. Where they disagree, which tracker recorded it? This is counted, not explained.

## 3. Data (all public, no key, no account)

- **UCDP Candidate Events,** monthly, for the window months. **UCDP GED 26.1** for any window month it covers, with GED preferred over Candidate where both exist, because GED is the checked release.
- **GDELT 2.0 events,** raw files, keeping only rows with QuadClass 4 and root codes 18, 19 and 20. These are Assault, Fight and Unconventional mass violence in CAMEO. The labels are checked in the CAMEO manual at build. No article text and no mention tables are read.
- **Province layer:** one public first-level boundary file, used only to group points into provinces. It is never drawn. The file and its license are named at build. A crosswalk from UCDP's `adm_1` names and GDELT's FIPS 10-4 province codes to that file is committed before any event is counted.
- **Kit:** one table, one row per province and month: country and province as each source spells them, month, `ucdp_any`, `gdelt_any` and `active_days`. No coordinates, no actors, no death or injury fields. The fetch is streamed and filtered, so only that table is kept.

## 4. Frame (fixed now, before any data is opened)

- **Window:** the trailing 12 complete calendar months that ended at least 30 days before the run. On a run in early December 2026, that is October 2025 through September 2026, read from the Candidate release dated after each month.
- **What counts as organized armed violence in a province-month:**
  - UCDP: at least one event of any of UCDP's three types (state-based, non-state, one-sided), with `where_prec` 1 to 4, and in Candidate data a status of "Clear". Types are pooled and never printed separately.
  - GDELT: at least one root event (`IsRootEvent` 1) with QuadClass 4 and root code 18, 19 or 20, `ActionGeo_Type` 4 or 5, and at least two sources (`NumSources` 2 or more). Country-level matches are dropped because they sit on a centroid.
- **What counts as a conflict:** the ball asks whether UCDP's dyad list can be used without printing deaths. It can, but ARES doesn't need it. The unit is the province-month, not the conflict. UCDP's Candidate events "include all events that meet the definition of an event regardless of the annual threshold", so the 25-death yearly line never decides what appears. One line still remains: UCDP records an event only if at least one death is registered. ARES uses that as a yes or no and never reads or stores the number. This is stated on the page as a carrier: UCDP's line is drawn by deaths, and GDELT's is drawn by news reports.
- **Dot size, named now:** `active_days`, the number of distinct days in the month with at least one UCDP event placed in the province and dated to the exact day (`date_prec` 1). Why this one:
  - It isn't a human-cost number.
  - It runs from 0 to 31 on every map, so dots compare month to month.
  - One long day of reporting counts as one day, so it is less driven by how much a place is covered by news than an event count is.
  - Provinces touched and months active describe a whole conflict, not a province, and would need conflicts named. A composite would be harder to read and to check.
  - GDELT days are not used for size, because duplicate stories inflate them. Days from UCDP events dated only to a range are not counted.
- **Displacement:** left out, as you ruled. It is a human-cost figure, contested in the same way deaths are.
- **Map:** a dot at each province's label point for every province-month where either tracker recorded violence. Dot area follows `active_days`, in one neutral color. A solid dot means both trackers agree. A hollow dot means one tracker only. The tooltip shows only the province name as the source spells it, the month, "both trackers", "UCDP only" or "GDELT only", and the active days. No borders and no country fills.

### Headline cell (named in advance)

`ares.agree_share`: of all province-months in the window where either tracker recorded organized armed violence, the share where both did, with a 95% interval from a block bootstrap by country and month. This is also the field for live_headlines.py. Headline wording: "In N of M province-months with recorded armed violence, both public trackers agree", with N and M from the run log.

Secondary cells: `ares.ucdp_only_count` and `ares.gdelt_only_count`.

## 5. Outcomes (in plain words)

There is no stated claim to be above or below, so ARES uses two of the four words, per province-month:

- **CONSISTENT:** both trackers recorded organized armed violence there that month. Plain words on the page: "both trackers agree".
- **CANNOT_TELL:** one tracker did and the other didn't. Plain words: "one tracker only", with which one.
- ABOVE and BELOW are not used, and the page says why.

Nothing returned, refused and held are counted as their own outcomes. A month whose Candidate release is missing is held and listed. A province name that can't be matched in the crosswalk is held, listed by its source spelling and never guessed. GDELT rows with a blank place are nothing returned.

## 6. Labels for preliminary data

- Until the referee's read, every output carries "PRELIMINARY: first run, not refereed". It stays off the home banner until then.
- Every page carries the delay ("at least 30 days old"), both citations with version numbers, the GDELT citation and link, and the no-position footnote.
- Every count comes from the run log, never typed in by hand.

## 7. Cadence and kit

- **Cadence:** monthly, after each UCDP Candidate release, reading only months that meet the 30-day delay.
- **Kit:** the province-month table above (12 months, compressed), the crosswalk, the filter code and a hash of each source file read. The size of a GDELT year after filtering is measured at the first build and printed, not estimated here.

## Open questions for the operator

1. **GDELT filter:** two or more sources and root events only, named now to cut duplicates. Loosen or tighten it before the first read?
2. **Boundary file:** one public first-level file, used only to group points and never drawn. Name a preferred one, or I'll name one with its license before the build.
3. **ACLED:** left out on its terms and its account requirement. It comes in only with written permission, which would be an outside contact.
