# PROMETHEUS: stated wildfire outlooks against the large fires that followed

Status: plan, written before any outlook or fire record is read. Nothing here has been run. The frame below is fixed now and does not change after the first file is read.

Shape: same as zeus_index/PLAN.md. Claims read, Questions, Data, Frame fixed before any reading, outcomes four-way, and labels for preliminary data.

## 1. Claims read

### Stated side: the Significant Wildland Fire Potential Outlook

- What the outlook says it does, National Interagency Mobilization Guide 2026, chapter 60, https://www.nifc.gov/sites/default/files/NICC/3-Logistics/Reference%20Documents/Mob%20Guide/2026/2026%20Chapter%2060.pdf: "The Outlook identifies areas where significant wildland fire activity is expected to be above or below normal levels."
- Its period, same source: "The Outlook covers a four-month period, divided into four one-month sections."
- Its schedule, National Interagency Predictive Services Handbook 2023, https://www.nifc.Gov/sites/default/files/NICC/2-Predictive%20Services/National%20Interagency%20Predictive%20Services%20Handbook%202023.pdf: issued "on the first day of each month at 1200 Mountain Time". The outlooks page, https://www.nifc.gov/nicc/predictive-services/outlooks, adds: "only issued when Geographic Areas are in fire season and Predictive Services staff are on duty."
- Its unit: the Predictive Services Area (PSA). The mapping service, https://fsapps.nwcg.gov/psp/rest/services/npsg/Outlooks_Monthly_Extended/MapServer, describes a "Forecast of significant fire potential by predictive service area (PSA)".
- A baseline the outlook itself uses, June 2023 outlook, https://www.nifc.gov/sites/default/files/document-media/monthly_seasonal_outlook.pdf: "Historically during June, between one to two large fires occur per Predictive Services Area (PSA)."

**No numeric definition of "above normal" was found.** The mobilization guide, the handbook, the outlooks page and the current outlook give no probability or frequency. A wording on NIFC's social media, "a greater than usual likelihood that significant wildland fires will occur", was seen only as a search-result title and could not be read, so it is not quoted as a claim. The ball asked for the outlook's own definition. It states a direction and no number. Section 5 says how the run reads that direction.

### What counts as a large fire

- National Interagency Coordination Center, Mobilization Guide chapter 60 (above): "100 acres or larger in timber or slash fuel models" and "300 acres or larger in grass or brush fuel models", or a fire with a Complex, Type 1 or Type 2 team assigned.
- The 7-Day product, https://www.nifc.gov/sites/default/files/document-media/7-Day_Product_Description.pdf, uses another definition, "the top 5% of historic "daily largest fires"" per PSA. It is a different product and is not used here.

## 2. Questions

1. Where the outlook rated a PSA's month above normal, did that PSA have more large fires that month than its own usual count for that month?
2. Where it rated below normal, did it have fewer? Where it rated normal, how did the count compare? These are secondary readings.

## 3. Data (all public, no key, no account)

- **Outlooks:** NIFC's monthly archive, one ZIP per issue from January 2023 to September 2026, listed on the outlooks page. Whether each ZIP holds PSA polygons or only maps and PDFs is not yet known, because nifc.gov refuses connections from this lane. The current-issue files at https://fsapps.nwcg.gov/psp/npsg/data/dynamic/monthly_extended_outlook.zip and the NCEI copies are overwritten each month and are not an archive. PSA boundaries: https://fsapps.nwcg.gov/psp/npsg/forecast/home/downloads ("updated 15 January 2025").
- **Fires, outcome years:** NIFC Open Data, Wildland Fire Locations Full History (WFIGS, from IRWIN), https://data-nifc.opendata.arcgis.com/, GeoJSON or shapefile. NWCG says it "may be incomplete". Years covered and field names are confirmed at build.
- **Fires, baseline years:** Fire Program Analysis fire-occurrence database, 6th edition (Short 2022), https://www.fs.usda.gov/rds/archive/products/RDS-2013-0009.6/_metadata_RDS-2013-0009.6.html, "2.3 million geo-referenced wildfire records", 1992 to 2020, with FIRE_SIZE and DISCOVERY_DATE.

## 4. Frame (fixed now, before any outlook or fire record is read)

- **Outlooks:** every issue from January 2023 through December 2025, first month only (the month the outlook is issued for first). Months two to four are a secondary reading. 2026 is left out because the archive ends at September 2026 and later fire records are still being entered.
- **Unit:** the PSA and calendar month. Each PSA-month carries one rating: above normal, normal or below normal.
- **Large fire:** a fire of 100 acres or more by final reported size, discovered in that PSA in that month. This is the lower NICC threshold, applied to all fuels, because fuel type is not reliably in the records. A secondary reading uses 300 acres. Fuel type is a carrier.
- **Usual count:** for each PSA and calendar month, the median count of large fires over 2001 to 2020 in the baseline database, using the PSA boundaries above.
- **Exceed:** a PSA-month's large-fire count is above its usual count.
- **Interval:** a 95% interval on each share from a block bootstrap by outlook issue, because PSAs in one issue share one weather pattern and are not independent.
- **Carriers, stated with every result:** the baseline comes from one database and the outcome years from another. The run counts both in 2020, if WFIGS covers it, and prints the difference. "Above normal" has no stated number. The large-fire threshold ignores fuel type. Fire records may be incomplete.

### Headline cell (named in advance)

`prometheus.above_exceed_share`: of PSA-months rated above normal in the first month of each outlook, the share whose large-fire count exceeded that PSA's usual count for that month, with its 95% interval. The card, the ledger row and the reproduce kit read this field and no other as the headline.

Secondary cells: `prometheus.below_under_share` (below normal, count under usual), `prometheus.normal_exceed_share` (normal, count above usual, printed for comparison), and the same three at 300 acres and for months two to four.

## 5. Outcomes (four-way, delivered relative to stated)

The outlook states a direction: activity above normal levels. "Normal" here is the PSA's usual count, its median, so a PSA-month above its median happens about half the time without any outlook. The run reads "above normal" as a claim that exceeding happens more than half the time. This reading is named now, before any data, and printed with the outcome as the run's reading, not NIFC's.

- **CONSISTENT:** the whole 95% interval of `prometheus.above_exceed_share` is above 0.5.
- **BELOW:** the whole interval is at or below 0.5.
- **CANNOT_TELL:** the interval straddles 0.5, or a frame item could not be met (for example archive ZIPs with no PSA polygons). The reason is named.
- **ABOVE:** not reachable against a direction claim.

Nothing returned, refused and held are counted as their own outcomes. An issue whose archive holds no PSA polygons is held and listed, never redrawn from a map image. A month with no outlook because staff were off duty is not counted and is listed.

## 6. Labels for preliminary data

- Until the referee's read, every output carries "PRELIMINARY: first run, not refereed". It stays off the home banner until then.
- Every result carries "above normal has no stated number. The run reads it as more than half."
- Every count on the card and in the ledger comes from the run log, never typed in by hand.

## Open questions for the operator

1. **Archive contents:** nifc.gov is refused from this lane. Open one archive ZIP from your seat. If they hold no PSA polygons, the frame can't be met and this plan reads CANNOT_TELL until one is found.
2. **Reading "above normal" as more than half:** keep it, or report the shares with no outcome?
3. **Large fire:** 100 acres for all fuels is primary and 300 secondary. Swap them?
