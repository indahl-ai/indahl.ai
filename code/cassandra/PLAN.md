# CASSANDRA: flash flood warnings against the floods reported

Status: plan, written before any outcome is read. Nothing here has been run. The frame below is fixed now and does not change after the first file is read.

Shape: same as zeus_index/PLAN.md. Claims read, Questions, Data, Frame fixed before any reading, outcomes four-way, and labels for preliminary data.

## 0. Why this frame

The ball asks for warnings that came true, without picking cases after the fact. Six warning types were weighed on three tests: every warning archived, a public outcome record, and a stated meaning.

- **Volcano alert levels** fail on meaning. WATCH says "timeframe uncertain", and WARNING includes "underway", so many warnings follow the eruption they warn of. https://www.usgs.gov/programs/VHP/volcanic-alert-levels-characterize-conditions-us-volcanoes
- **Tsunami warnings** fail on outcome. The warning is for "widespread inundation", which is not a field in the outcome database. https://www.tsunami.gov/?page=message_definitions
- **Avalanche danger ratings** fail on archive and outcome. There is no single keyless archive, and observations are volunteered.
- **Recalls** have no outcome record.
- **Geomagnetic storm watches** pass all three tests but overlap SOLAR, which already reads space weather. Not used.
- **Flash flood warnings** pass with two weaknesses stated up front. "Likely" carries no number, and the outcome record is floods reported, not floods.

Flash flood warnings are the most honest frame with public data. Every warning in the window is counted, hits and misses alike.

## 1. Claims read

What a flash flood warning states, NWSI 10-922, https://www.weather.gov/media/directives/010_pdfs/pd01009022curr.pdf: "Flash flood warnings are issued when flooding is imminent or likely."

Each warning also carries its own polygon and its own expiry time. That gives a stated place and a stated window for every warning, which is what lets hits be counted without choosing cases.

"Likely" is not given a number in the directive. SELDON-style coverage against a stated share is therefore not possible. The run reads the share of warnings followed by a reported flood and states it as a measurement, with a reading against "likely" only under the rule in section 5.

## 2. Questions

1. Of all flash flood warnings issued in the window, what share had a flash flood report inside the warning polygon between issue and expiry?
2. Of all flash flood reports in the window, what share fell inside a warning in force at the time? This is a secondary reading, for floods that came without a warning.

## 3. Data (all public, no key, no account)

- **Warnings:** the Iowa Environmental Mesonet's archive of every VTEC-coded warning, shapefile or KML, https://mesonet.agron.iastate.edu/request/gis/watchwarn.phtml. Caveats from https://mesonet.agron.iastate.edu/info/datasets/vtec.html: records before 2005 are reconstructed, and polygons before October 2007 were experimental. TORNADO and ZEUS read the same archive for other products.
- **Reports, primary:** NCEI Storm Events, the official record, flash flood events with begin and end times and locations. Its URL, format and keyless access are confirmed before the first run. If it can't be read keyless, the run uses the next item as primary and says so.
- **Reports, secondary:** IEM Local Storm Reports, FLASH FLOOD type, CSV or shapefile, https://mesonet.agron.iastate.edu/request/gis/lsrs.phtml. IEM labels this archive "not complete or official".
- IEM's own warning verification tool pairs warnings with reports and calls itself "unofficial". The run does its own pairing and does not read that tool's results.

## 4. Frame (fixed now, before any outcome is read)

- **Warnings:** every Flash Flood Warning (VTEC phenomenon FF, significance W) issued from 2008-01-01 through 2025-12-31 over the US. This starts after the experimental polygon period and ends before the latest year, which Storm Events may not yet have finished. Every warning in the window is counted. None is chosen.
- **Hit:** at least one flash flood report whose location lies inside the warning polygon, with a report time between the warning's issue and its expiry. Extensions that keep the same event number count as the same warning, ending at the final expiry.
- **Interval:** a 95% interval on the hit share from a block bootstrap by forecast office and year, because warnings from one office in one event are not independent.
- **Carriers, stated with every result:** the outcome is a report, not a flood. A flood in an empty place may go unreported and reads as a miss. Reporting effort may rise when a warning is out, which can raise hits. Neither effect is measured. The two report sources are read separately and never merged.

### Headline cell (named in advance)

`cassandra.ffw_hit_share`: the share of Flash Flood Warnings in the window followed by a flash flood report inside the polygon before expiry, read against NCEI Storm Events, with its 95% interval. The card, the ledger row and the reproduce kit read this field and no other as the headline.

Secondary cells: `cassandra.ffw_hit_share_lsr` (the same against IEM reports) and `cassandra.flood_warned_share` (the share of flash flood reports that fell inside a warning in force).

## 5. Outcomes (four-way, delivered relative to stated)

The directive says flooding is "imminent or likely" and gives no number. The run reads "likely" at its weakest plain meaning, more often than not, a share of 0.5. This reading is named now, before any data, and is printed with the outcome as the run's reading, not NWS's.

- **CONSISTENT:** the whole 95% interval of the hit share is at or above 0.5.
- **BELOW:** the whole interval is below 0.5.
- **CANNOT_TELL:** the interval straddles 0.5, or a frame item could not be met. The reason is named.
- **ABOVE:** not reachable against a floor.

Nothing returned, refused and held are counted as their own outcomes. A warning whose polygon can't be read is held and listed. A year with a gap in either archive is held and left out of the headline, never filled in.

## 6. Labels for preliminary data

- Until the referee's read, every output carries "PRELIMINARY: first run, not refereed". It stays off the home banner until then.
- Every result carries "floods reported, not floods" beside the share.
- Every count on the card and in the ledger comes from the run log, never typed in by hand.

## Open questions for the operator

1. **Reading "likely" as 0.5:** this is the one judgment call. Keep it, or report the share with no outcome at all?
2. **Window:** 2008 through 2025 is named. Shorten it before the first read if the build is too large.
3. **Geomagnetic watches:** they pass all three tests but sit next to SOLAR. If SOLAR doesn't already read watches, they could be a later addendum there.
