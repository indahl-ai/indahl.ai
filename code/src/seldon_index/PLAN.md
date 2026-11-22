# SELDON: stated ranges of long-range official forecasts against outcomes

Status: plan, written before any outcome is read. Nothing here has been run. The frame below is fixed now and does not change after the first outcome file is read.

Shape: same as zeus_index/PLAN.md. Claims read, Questions, Data, Frame fixed before any reading, outcomes four-way, and labels for preliminary data.

What is new here is the horizon. FEDSEP reads the Fed's ranges and STEO reads energy price intervals, both over a year or two. SELDON reads stated ranges for budget and growth five or more years out. It reads neither of those desks' sources.

Quotes below came through an automated reading step. Each is checked word for word against its page before the first run, and any that differs is corrected or dropped.

## 1. Claims read

### Stated side: the Congressional Budget Office

- How CBO builds its ranges, https://www.cbo.gov/system/files/2024-12/60664-Deficits-Debt.pdf: "the agency typically presents a range of deficit and debt projections based on historical errors in its baseline projections."
- A stated range, same report (June 2024 baseline, fiscal year 2029): "There is roughly a two-thirds chance that, under current law, the deficit in that year would be" ... "between 3.5 percent and 8.5 percent of GDP". For debt at the end of 2029: "between 102 percent and 119 percent of GDP". Landing page https://www.cbo.gov/publication/61067, which also says "CBO's projections of debt are more uncertain than the agency's projections of deficits."
- For growth, https://www.cbo.gov/system/files/2023-06/59078-Economic-Forecasting-Record.pdf: "CBO relies on the root mean square error of its historical forecasts to quantify the uncertainty", and "there is an approximately two-thirds chance that economic growth will average between 0.6 percent and 3.1 percent" (five-year average real GDP growth).
- CBO's latest yearly accuracy report, https://www.cbo.gov/system/files/2026-01/61916-budget-accuracy.pdf (Jan 2026), states no interval and is not a stated range.

The claim SELDON reads is CBO's own: roughly two-thirds of outcomes should fall inside its stated two-thirds ranges.

### Stated side: the IMF World Economic Outlook

- April 2025 WEO, chapter 1, https://www.imf.org/-/media/files/publications/weo/2025/april/english/ch1.pdf.md: "The probability that global growth in 2025 will fall below 2 percent is assessed at close to 30 percent." The bands are "G20 model-derived confidence bands around the WEO reference forecast using historical shock resampling".
- No 50, 70 or 90 percent band printed as numbers was found in that chapter. Whether other WEO issues print numeric bands or probabilities is read before the first run, as part of listing the stated side.

### Existing evaluations (context, not the frame)

- CBO's own evaluations: budget errors by projection year 1 to 11 from 1984, and growth over two and five years, scored against the latest revised data (59078 above).
- Celasun, Lee, Mrkaic and Timmermann, IMF WP/21/216, https://imf.org/-/media/Files/Publications/WP/2021/English/wpiea2021216-print-pdf.ashx: the outturn is "the actual value for a given year (t) as reported in the following year's (t + 1) Fall issue of the WEO." These authors are mostly IMF staff, so the paper is not independent.

## 2. Questions

1. Of CBO's stated two-thirds ranges whose target year has passed, what share held the outcome, and is that share ABOVE, BELOW, CONSISTENT with, or CANNOT_TELL against two-thirds?
2. For each probability the WEO states for a defined event (for example global growth below a threshold in a named year), what happened? This is a secondary reading.

## 3. Data (all public, no key, no account)

- **CBO projections and actuals:** https://github.com/US-CBO/eval-projections (CSV: `baselines.csv`, `actuals.csv`, `actual_gdp.csv`), https://github.com/US-CBO/cbo-data (versioned CSV, one file per vintage), and https://www.cbo.gov/data/budget-economic-data (XLSX, vintages from 2000 to Feb 2026).
- **CBO stated ranges:** the reports themselves and their supplemental data, for example www.cbo.gov/publication/60664#data and www.cbo.gov/publication/59078#data. Each range is quoted with its report, page and target year.
- **IMF:** the Historical WEO Forecasts Database, https://www.imf.org/-/media/files/publications/weo/weo-database/2025/april/weohistorical.xlsx, with forecasts from April 1990 for key indicators, and the archived vintages at https://www.imf.org/en/publications/sprolls/world-economic-outlook-databases. Use the newest edition of the historical file at build.

## 4. Frame (fixed now, before any outcome is read)

- **CBO claims:** every two-thirds range CBO printed for deficits as a share of GDP, debt held by the public as a share of GDP, or average real GDP growth, in any report, whose target year ends on or before fiscal year 2025 (the last year with actuals in the Jan 2026 accuracy report). The list of ranges is built from the reports first, before any actual is opened, and committed. A range counts once, in the report that first printed it.
- **Horizon:** each range carries its horizon in years from the report date to the target year. Only ranges at least three years out count toward the headline. Shorter ones are printed apart.
- **Outturn vintage (CBO):** for deficits and debt, the actual as CBO records it in `actuals.csv`, since budget actuals change little. For growth, the first figure CBO published for the full period, read from the cbo-data vintage after the period ended. The latest revised figure is printed beside it as a secondary reading, because CBO's own evaluation uses it.
- **Outturn vintage (IMF):** the value in the following year's October WEO, as the IMF's own evaluation does.
- **Hit:** the outcome falls inside the stated range, endpoints included. The range is read at its printed rounding.
- **Interval:** a 95% interval on the hit share from a block bootstrap by report, because ranges from one report share one baseline and are not independent.
- **Carriers, stated with every result:** CBO projects under current law, so later changes in law move outcomes away from a projection without the projection being wrong about current law. CBO's ranges come from its own past errors, so a share near two-thirds is partly built in over the years those errors cover. The number of reports with ranges is expected to be small, which widens the interval.

### Headline cell (named in advance)

`seldon.cbo_range_hit_share`: the share of CBO's stated two-thirds ranges, three or more years out, whose outcome fell inside the range, with its 95% interval. The card, the ledger row and the reproduce kit read this field and no other as the headline.

Secondary cells: `seldon.cbo_range_hit_share_revised` (growth against revised data), `seldon.cbo_short_horizon_hit_share` (under three years) and `seldon.imf_probability_events`, a list of each stated WEO probability with its event and what happened. The IMF list is a measurement with no outcome unless at least 20 such statements exist, because fewer can't test a stated probability.

## 5. Outcomes (four-way, delivered relative to stated)

CBO states a share: roughly two-thirds, read as 0.667.

- **CONSISTENT:** the 95% interval of the hit share contains 0.667.
- **ABOVE:** the whole interval is above 0.667. More outcomes fell inside than stated, so the ranges were wider than needed.
- **BELOW:** the whole interval is below 0.667. Fewer outcomes fell inside than stated, so the ranges were too narrow.
- **CANNOT_TELL:** too few ranges to form an interval (fewer than 10), or a frame item could not be met. The reason is named.

Nothing returned, refused and held are counted as their own outcomes. A range whose target year has no actual yet is held and listed. A report that can't be read is refused. No range is inferred from a chart when the report prints no numbers.

## 6. Labels for preliminary data

- Until the referee's read, every output carries "PRELIMINARY: first run, not refereed". It stays off the home banner until then.
- Every count on the card and in the ledger comes from the run log, never typed in by hand.

## Open questions for the operator

1. **Headline threshold:** three years or more is named as the long horizon. Change it before the first read if you want five.
2. **Growth outturn:** first-published is primary and revised is secondary. Swap them if you'd rather match CBO's own evaluation.
3. **IMF:** the WEO prints few probabilities as numbers. The plan keeps the IMF as a list unless 20 or more exist. Say if you want the IMF dropped or given its own desk.
