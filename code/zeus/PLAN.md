# ZEUS: stated thunderstorm forecasts against the lightning that struck

Status: plan, written before any reading of outlooks or lightning. Nothing here has been run. The frame below is fixed now and does not change after the first file is read.

Amendment, 2026-11-22, before any read: a fixed 10-statute-mile secondary radius and the lightning-type carrier, per the operator on PR #8.

Shape note: the ball asks for tornado_index/PLAN.md's shape. That file is not in this repository on any branch, so this plan follows the shape as the ball lists it: Claims read (with quotes and URLs), Questions, Data (public and keyless), Frame fixed before any reading, outcomes four-way, and labels for preliminary data. Fit headings to TORNADO's at build if they differ.

## 1. Claims read

### Stated side: what the thunder line on SPC's Day 1 outlook says

SPC's own product page, https://www.spc.noaa.gov/misc/SPC_probotlk_info.html (read 2026-11-22):

> "The unlabeled (brown) thunderstorm line on the outlook graphic depicts, to the right of the line," ... "a 10% or higher probability of thunderstorms during the valid period."

The NWS directive that governs SPC products, NWSI 10-512 (April 9, 2021), https://www.weather.gov/media/directives/010_pdfs/pd01005012curr.pdf, section 2.3.3, page 10:

> "The Day 1, Day 2, and Day 3 Outlooks also define areas where there is a 10% or greater probability of" / "(general) thunderstorms."

> "The contour for "General Thunder" in the graphical forecast refers to a 10% or greater probability of" / "non-severe convection."

Valid period of the 1300 UTC Day 1 outlook, NWSI 10-512, Table 1, page 10:

> "1300 1300 Day 1 to 1200 Day 2 (23 hour period )"

**The radius.** Neither source names a radius for thunder. The only radius in either is for severe weather. SPC_probotlk_info.html says "For all outlooks, the probability values represent the chance of severe weather occurring within 25 miles of any point". NWSI 10-512 section 3.3.3, page 13, says "These outlooks provide numerical probabilities of severe weather within 25 statute miles of any point". The ball asked for the radius "SPC's definition names". It names none for thunder. The frame in section 4 therefore borrows the 25-statute-mile radius from SPC's severe-probability definition, and labels it as borrowed, not stated. This is the one judgment call in the plan (open question 1).

Pages not read: three other SPC pages (about.html, the outlook index and the FAQ) refused automated reading. A thunder radius there, if any, is unknown. Check them by hand before the first run.

Enhanced Thunderstorm Outlook (context only, not a change to the frame): SPC's page for its separate thunder-probability product was not read from this lane, because SPC's pages refuse automated reading here. An NWS product sheet, https://www.weather.gov/media/cae/SPCProductReferenceSheet.pdf ("Updated: 6/4/2023"), gives only the severe radius ("within 25 miles of a point") and says nothing of a thunder radius or of lightning type. If the Enhanced Thunderstorm Outlook page names a radius for its own thunder probabilities, quote it here by hand before the first read. The frame below stays as fixed either way.

### Stated side: what NOAA says about its own lightning detector

GLM's flash detection efficiency, taken from NOAA's validation documents. These are stated figures: the run does not measure them.

- **Requirement:** "70% total flash detection efficiency (DE)". This is from the GOES-18 GLM full-validation review, slide 8, https://www.noaasis.noaa.gov/pdf/ps-pvr/goes18/GLM/Full/GLM18_FULL_PS-PVR_08Nov2023_augment.pdf. The GOES-16 Product Performance Guide states the same requirement.
- **Measured, GOES-18:** "0.81 DE bulk value across FOV" for January to September 2023, against ground networks (same review, slide 21). Day 0.80 and night 0.84 (slide 13).
- **Edge of view:** "DE vs. ground networks is 79-81% (lower near the limb)" (slide 24), and "Low DE values near limb (large water/ice absorption on long slant path)" (slides 44 and 47).
- **GOES-18 Product Performance Guide, section 3.1,** https://www.noaasis.noaa.gov/pdf/ps-pvr/goes18/GLM/Full/GOES18_GLM_PPG_20231117.pdf: "Detection falls off over CONUS since the instrument minimum detectable energy increases with boresight angle".
- **File cadence, same guide, section 1.1:** "The L2 data files are broadcast every 20 seconds to meet the latency requirement."
- **GOES-19:** no published DE figure was found in the documents read. The run uses GOES-19 for the east and carries this as a gap, not a figure.

## 2. Questions

1. Where SPC drew a thunder area on the 1300 UTC Day 1 outlook, how often did GLM see lightning within the frame radius during the valid period?
2. How much of the lightning GLM saw over CONUS in the valid period fell outside the frame radius of every drawn thunder area?

## 3. Data (all public, no key, no account)

- **Outlooks:** SPC Day 1 Convective Outlook shapefiles, 1300 UTC issuance, category TSTM (general thunder), from the Iowa Environmental Mesonet's SPC outlook archive. This is the same source TORNADO uses. The TSTM polygon contains the higher categories (MRGL and up), so a point inside any of them is inside the thunder area.
- **Lightning:** GOES Geostationary Lightning Mapper Level 2 LCFA (events, groups, flashes) on AWS open data. It's anonymous and needs no key: `s3://noaa-goes19/GLM-L2-LCFA/` (GOES-East) and `s3://noaa-goes18/GLM-L2-LCFA/` (GOES-West), with files at `GLM-L2-LCFA/YYYY/DDD/HH/`. I checked anonymous listing of both buckets from this lane on 2026-11-22. The run uses flash latitude, longitude and time only.
- **Size:** one sample hour, GOES-19, 2026 day 310, 20 UTC, listed 180 files and 88.6 MB. At that rate a 30-day window is about 64 GB per satellite. Volume varies with storm activity, so treat this as one hour's measure, not an estimate the run relies on. Stream each file, keep only the flash points and delete the file.

## 4. Frame (fixed now, before any reading)

- **Outlook:** the 1300 UTC Day 1 issuance only, valid 1300 UTC that day to 1200 UTC the next (23 hours).
- **Window:** the last 30 complete convective days, the outlooks issued 2026-10-22 through 2026-11-20. The last valid period ends 2026-11-21 1200 UTC. The run and every output carry the label "30-day window, late autumn". Late October to November is low lightning season over CONUS, which is a carrier, not a footnote. A years-long version is a later addendum and does not replace this one.
- **Domain:** CONUS land and coastal waters inside the outlook domain.
- **Grid:** points every 0.1 degree of latitude and longitude over the domain. The point set is fixed before reading.
- **Radius:** 25 statute miles (40.2 km) as the primary. This is borrowed from SPC's severe-probability definition, because SPC states no radius for thunder (section 1). It is labeled "borrowed radius" wherever the result appears.
- **Secondary radius:** 10 statute miles (16.1 km), one fixed secondary reading, printed beside the primary with the same outcome rule. Both radii are named now, so neither is chosen after the data.
- **Satellite split:** GOES-19 for points east of 106.2°W, GOES-18 for points west of it. 106.2°W is the midpoint between the two satellites' sub-satellite points (75.2°W and 137.2°W). This keeps each point on the satellite that sees it at the smaller boresight angle.
- **Lightning at a point:** at least one GLM flash within the radius of the point during the valid period. Count only flashes that pass the product's own quality flag.
- **Carriers, stated with every result:** GLM's stated detection efficiency (70% required, 81% measured for GOES-18) and its stated falloff toward the limb. Both make the observed share a floor, not an exact figure. Under "any flash in 23 hours", one missed flash rarely flips a point, so the effect is expected to be small, but the run does not claim to measure it. Also carry the borrowed radius, the season, and the missing GOES-19 DE figure.
- **Carrier, lightning type:** GLM counts all lightning it sees from orbit, in-cloud and cloud-to-ground alike ("total flash detection efficiency", section 1). A thunderstorm forecast is about thunder heard at the ground. A flash GLM records may be one no one on the ground would report as a thunderstorm. This carrier is stated with every result and is not measured.

### Headline cell (named in advance)

`zeus.tstm_hit_share`: the share of thunder-area grid points, summed over the 30 outlooks, that had at least one GLM flash within 25 statute miles during the valid period. Give a 95% interval from a block bootstrap by outlook day, because points on the same day are not independent. The card, the ledger row and the reproduce kit all read this field and no other as the headline.

Secondary reading, printed beside the headline, not the headline: `zeus.tstm_hit_share_10mi`, the same share and interval with the 10-statute-mile radius, read against the same 10% floor with the same outcome rule.

Secondary cell, not the headline: `zeus.flash_outside_share`, the share of GLM flashes over CONUS in the valid periods that fell more than 25 statute miles from every thunder area.

## 5. Outcomes (four-way, relative to what SPC stated)

SPC states a floor: 10% or more. The outcome reads the headline interval against that floor.

- **CONSISTENT:** the whole 95% interval of `zeus.tstm_hit_share` is at or above 10%.
- **BELOW:** the whole interval is under 10%.
- **CANNOT_TELL:** the interval straddles 10%, or any frame item could not be met (for example a missing outlook day or a satellite gap over the window). The reason is named.
- **ABOVE:** not reachable against a one-sided floor. The observed share is reported as measured, and no outcome claims SPC under-forecast.

Nothing returned, refused and held are counted as their own outcomes, as house rules require. A day with no IEM outlook, or a day where a GLM bucket has a gap of more than one hour in the valid period, is held, listed by date, and left out of the headline. It is never filled in.

The secondary cell has no stated figure to compare to, because SPC makes no claim about lightning outside its lines. It is reported as a measurement, with no outcome.

## 6. Labels for preliminary data

- Until the referee's read, every output carries "PRELIMINARY: first run, not refereed".
- If the fetch can't cover all 30 days tonight, the run is labeled "PRELIMINARY: partial window" and lists the days covered. The window is never shortened silently and the headline is not presented as the 30-day figure.
- Every count on the card and in the ledger comes from the run log, never typed in by hand.

## Open questions for the operator

1. **Radius:** settled on PR #8. 25 statute miles primary (borrowed), 10 statute miles secondary, both fixed now.
2. **Satellite split:** 106.2°W is the midpoint between the satellites. Use TORNADO's split instead if it already has one.
3. **Unread SPC pages:** about.html, the outlook index and the FAQ refused automated reading. Read them by hand once in case one names a thunder radius.
