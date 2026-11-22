#!/usr/bin/env python3
"""make_stated_src.py: writes data/stated_src.json, the CBO two-thirds ranges copied by hand from the reports (step 2 of the stated side), on
21 Nov 2026, before any actual was opened. build_stated.py then checks every quoted fragment against its report page. Edit this file, never the JSON."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
R = {  # file: (report, month)
 '51908': ('An Update to the Budget and Economic Outlook: 2016 to 2026', '2016-08'),
 '52370': ('The Budget and Economic Outlook: 2017 to 2027', '2017-01'),
 '53651': ('The Budget and Economic Outlook: 2018 to 2028', '2018-04'),
 '54318': ('An Update to the Economic Outlook: 2018 to 2028', '2018-08'),
 '54918': ('The Budget and Economic Outlook: 2019 to 2029', '2019-01'),
 '55551': ('An Update to the Budget and Economic Outlook: 2019 to 2029', '2019-08'),
 '55234': ('An Evaluation of CBO’s Past Deficit and Debt Projections', '2019-09'),
 '55505': ('CBO’s Economic Forecasting Record: 2019 Update', '2019-10'),
 '56020': ('The Budget and Economic Outlook: 2020 to 2030', '2020-01'),
 '56050': ('The Budget Outlook for 2020 to 2030 in 13 Slides', '2020-01'),
 '56517': ('An Update to the Budget Outlook: 2020 to 2030', '2020-09'),
 '56989': ('Additional Information About the Economic Outlook: 2021 to 2031', '2021-02'),
 '57263': ('Additional Information About the Updated Budget and Economic Outlook: 2021 to 2031', '2021-07'),
 '57579': ('CBO’s Economic Forecasting Record: 2021 Update', '2021-12'),
 '57950': ('The Budget and Economic Outlook: 2022 to 2032', '2022-05'),
 '58848': ('The Budget and Economic Outlook: 2023 to 2033', '2023-02'),
 '59078': ('CBO’s Economic Forecasting Record: 2023 Update', '2023-06'),
 '59096': ('An Update to the Budget Outlook: 2023 to 2033', '2023-05'),
 '59710': ('The Budget and Economic Outlook: 2024 to 2034', '2024-02'),
 '60039': ('An Update to the Budget and Economic Outlook: 2024 to 2034', '2024-06'),
 '60380': ('An Update to the Economic Outlook for 2024 to 2034 in 20 Slides', '2024-06'),
 '60664': ('An Evaluation of CBO’s Projections of Deficits and Debt From 1984 to 2023', '2024-12'),
 '61135': ('Additional Information About the Economic Outlook: 2025 to 2035', '2025-01'),
 '61882': ('The Budget and Economic Outlook: 2026 to 2036', '2026-02'),
 '51129': ('The Budget and Economic Outlook: 2016 to 2026', '2016-01'),
 '53090': ('CBO’s Economic Forecasting Record: 2017 Update', '2017-10'),
}
def q(page, text): return dict(page=page, text=text)
def g(rid, f, measure, target, lo, hi, quotes, note=None):
    rep, mon = R[f]; d = dict(id=rid, file=f, report=rep, report_month=mon, measure=measure, lo=lo, hi=hi, quote=quotes)
    d.update(target)
    if note: d['note'] = note
    return d
FY = lambda y: dict(basis='fiscal year', year=y)
CY = lambda y: dict(basis='calendar year', year=y)
AVG = lambda a, b: dict(basis='calendar years, average annual growth', start=a, end=b)
ranges = [
 g('2016-08.growth.2016-2020', '51908', 'growth', AVG(2016, 2020), 0.7, 3.2, [q(61, 'there is a two-thirds chance that the average growth rate of real GDP will be between 0.7 percent and 3.2 per- cent over the next five years'), q(62, 'real GDP grows at an average annual rate of 2.0 percent over the 2016–2020 period—but there is a two-thirds chance that the growth will be between 0.7 percent and 3.2 percent')]),
 g('2017-01.growth.2017-2020', '52370', 'growth', AVG(2017, 2020), 0.5, 3.3, [q(66, 'there is approximately a two-thirds chance that the average annual growth rate of real GDP'), q(67, 'will be between 0.5 percent and 3.3 percent over the next four years'), q(67, 'over the 2017–2020 period—but there is a roughly two-thirds chance that the growth will be between 0.5 percent and 3.3 percent')]),
 g('2018-04.growth.2018-2022', '53651', 'growth', AVG(2018, 2022), 0.8, 3.5, [q(37, 'there is approximately a two-thirds chance that the average annual growth rate of real GDP will be between 0.8 percent and 3.5 percent over the next five years'), q(39, 'over the 2018–2022 period—but there is a roughly two- thirds chance that the growth would be between 0.8 percent and 3.5 percent')]),
 g('2019-01.deficit.2020', '54918', 'deficit', FY(2020), 3.0, 5.2, [q(24, 'there is approximately a two-thirds chance that the deficit under current law would be between 3.0 percent and 5.2 percent of GDP in 2020')]),
 g('2019-01.deficit.2024', '54918', 'deficit', FY(2024), 2.0, 7.1, [q(24, 'For 2024, the range is larger: CBO estimates that there is approximately a two-thirds chance that the deficit would be between 2.0 percent and 7.1 percent of GDP')]),
 g('2019-01.debt.2024', '54918', 'debt', FY(2024), 76, 96, [q(24, 'federal debt is projected to equal 86 percent of GDP in 2024. Based on the analysis of its past projections, CBO estimates that there is approx imately a two-thirds chance that federal debt under'), q(26, 'current law would be between 76 percent and 96 percent of GDP in that year')]),
 g('2019-01.growth.2019-2023', '54918', 'growth', AVG(2019, 2023), 0.6, 3.2, [q(59, 'there is approximately a two-thirds chance that the average annual growth rate of real GDP will be between 0.6 percent and 3.2 per cent over the next five years'), q(60, 'over the 2019–2023 period, but there is a roughly two-thirds chance that the growth will be between 0.6 percent and 3.2 percent')]),
 g('2019-08.deficit.2020', '55551', 'deficit', FY(2020), 3.5, 5.6, [q(31, 'there is approximately a two-thirds chance that in 2020 the deficit under current law would be between 3.5 percent and 5.6 percent of GDP')]),
 g('2019-08.deficit.2024', '55551', 'deficit', FY(2024), 2.9, 6.7, [q(31, 'The range in 2024 would be larger: CBO estimates that, under current law, there is approximately a two-thirds chance that the deficit would be between 2.9 percent and 6.7 percent of GDP in that year')]),
 g('2019-08.debt.2024', '55551', 'debt', FY(2024), 79, 97, [q(31, 'federal debt held by the public is projected to equal 88 percent of GDP in 2024. After analyzing its past projections, CBO estimates that there is approximately a two-thirds chance that, under current law, federal debt would be between 79 percent and 97 percent of GDP in that year')]),
 g('2019-08.growth.2019-2023', '55551', 'growth', AVG(2019, 2023), 0.7, 3.3, [q(61, 'there is approximately a two-thirds chance that the average annual rate of real GDP growth (on a calendar year basis) will be between 0.7 percent and 3.3 percent over the next five years')],
   note='The report names no years for "the next five years". Its Figure 2-7 runs to 2023, and CBO’s October 2019 forecasting record repeats the range as estimated in August 2019 with the figure ending in 2023, so the period is read as 2019 to 2023 (decided before any actual was opened).'),
 g('2019-09.debt.2020', '55234', 'debt', FY(2020), 79, 82, [q(17, 'there is a two-thirds chance that the debt would be between 79 percent and 82 percent of GDP in 2020 and between 79 percent and 97 percent of GDP in 2024')]),
 g('2020-01.deficit.2021', '56020', 'deficit', FY(2021), 4.3, 5.4, [q(14, 'there is approximately a two-thirds chance that, under current law, the deficit in 2021 would be between 4.'), q(14, '3 percent and 5.4 percent of GDP')],
   note='A footnote is set inside the number on the page, between "4." and "3 percent"; the range reads 4.3 to 5.4 percent.'),
 g('2020-01.deficit.2025', '56020', 'deficit', FY(2025), 3.1, 6.8, [q(14, 'The range in 2025 would be larger: CBO estimates that, under current law, there is approximately a two-thirds chance that the deficit would be between 3.1 percent and 6.8 percent of GDP in that year')]),
 g('2020-01.debt.2025', '56020', 'debt', FY(2025), 80, 98, [q(15, 'federal debt held by the public is projected to equal 89 percent of GDP in 2025. Taking into account the errors in its past projections, CBO estimates that there is approximately a two-thirds chance that, under current law, federal debt would be between 80 percent and 98 percent of GDP in that year')]),
 g('2020-01.growth.2020-2024', '56020', 'growth', AVG(2020, 2024), 0.5, 3.1, [q(54, 'there is approximately a two-thirds chance that the average annual rate of real GDP growth (on a calendar year basis) will be between 0.5 percent and 3.1 percent over the next five years')],
   note='Figure 2-8 takes 2019 as CBO’s estimate and runs the projection to 2024, so the period is read as 2020 to 2024 (decided before any actual was opened).'),
 g('2020-09.deficit.2021', '56517', 'deficit', FY(2021), 7.6, 9.7, [q(29, 'there is approximately a two-thirds chance that, under current law, the deficit in 2021 would be between 7.6 percent and 9.7 percent of GDP')]),
 g('2020-09.deficit.2025', '56517', 'deficit', FY(2025), 2.8, 6.6, [q(29, 'The range in 2025 would be larger: CBO estimates that, under current law, there is approximately a two-thirds chance that the deficit would be between 2.8 percent and 6.6 percent of GDP in that year')]),
 g('2021-02.growth.2021-2025', '56989', 'growth', AVG(2021, 2025), 1.6, 4.1, [q(30, 'there is approximately a two-thirds chance that the average annual rate of real GDP growth (on a calen- dar year basis) will be between 1.6 percent and 4.1 per- cent over the next five years')]),
 g('2021-07.deficit.2022', '57263', 'deficit', FY(2022), 3.8, 5.7, [q(27, 'there is approximately a two-thirds chance that, under current law, the deficit in 2022 would be between 3.8 percent and 5.7 percent of GDP')]),
 g('2021-07.deficit.2026', '57263', 'deficit', FY(2026), 1.4, 6.1, [q(27, 'there is approx- imately a two-thirds chance that the deficit that year would be between 1.4 percent and 6.1 percent of GDP')]),
 g('2021-07.growth.2021', '57263', 'growth', CY(2021), 5.3, 8.1, [q(52, 'there is approximately a two-thirds chance that the rate of real GDP growth (on a calendar year basis) will be between 5.3 percent and 8.1 percent in 2021 and between −1.0 percent and 3.5 percent in 2025')]),
 g('2021-07.growth.2025', '57263', 'growth', CY(2025), -1.0, 3.5, [q(52, 'between 5.3 percent and 8.1 percent in 2021 and between −1.0 percent and 3.5 percent in 2025')]),
 g('2021-07.growth.2021-2025', '57263', 'growth', AVG(2021, 2025), 1.8, 4.4, [q(52, 'there is a two-thirds chance that the average annual rate of real GDP growth will be between 1.8 percent and 4.4 percent over the next five years')]),
 g('2021-12.growth.2021-2025', '57579', 'growth', AVG(2021, 2025), 1.9, 4.3, [q(6, 'there is approximately a two-thirds chance that the rate of real GDP growth over the next five years will be between 1.9 percent and 4.3 percent')],
   note='The report attributes this range to July 2021. It is not the range printed in the July 2021 additional information (1.8 to 4.4 percent), so it is counted here, where it is read.'),
 g('2022-05.deficit.2023', '57950', 'deficit', FY(2023), 2.7, 4.7, [q(23, 'there is approximately a two-thirds chance that the deficit under current law would be between 2.7 percent and 4.7 percent of GDP in 2023')],
   note='The report states this range for the deficit adjusted to exclude the effects of shifts in the timing of certain payments.'),
 g('2022-05.deficit.2027', '57950', 'deficit', FY(2027), 2.2, 7.0, [q(23, 'there is approximately a two- thirds chance that the deficit would be between 2.2 per cent and 7.0 percent of GDP')]),
 g('2022-05.debt.2027', '57950', 'debt', FY(2027), 91, 109, [q(23, 'there is approximately a two-thirds chance that federal debt under current law would be between 91 percent and 109 percent of GDP in that year')]),
 g('2022-05.growth.2022-2026', '57950', 'growth', AVG(2022, 2026), 0.9, 3.5, [q(54, 'between 0.9 percent and 3.5 percent over the next five years')]),
 g('2023-02.deficit.2024', '58848', 'deficit', FY(2024), 5.1, 7.0, [q(37, 'there is an approximately two-thirds chance that, under current law, the deficit in 2024 would be between 5.1 percent and 7.0 percent of GDP')]),
 g('2023-02.deficit.2028', '58848', 'deficit', FY(2028), 3.2, 8.0, [q(37, 'there is a roughly two-thirds chance that the deficit that year would be between 3.2 percent and 8.0 percent of GDP')]),
 g('2023-02.growth.2023', '58848', 'growth', CY(2023), -1.5, 1.7, [q(62, 'between ‒1.5 percent and 1.7 per cent in 2023 and between 0.7 percent and 3.6 percent in 2027')]),
 g('2023-02.growth.2027', '58848', 'growth', CY(2027), 0.7, 3.6, [q(62, 'between 0.7 percent and 3.6 percent in 2027')]),
 g('2023-06.growth.2023-2027', '59078', 'growth', AVG(2023, 2027), 0.6, 3.1, [q(6, 'there is an approximately two-thirds chance that the rate of real GDP growth over the next five years will be between 0.6 percent and 3.1 percent')]),
 g('2024-02.deficit.2025', '59710', 'deficit', FY(2025), 5.0, 7.1, [q(48, 'approximately two-thirds chance that, under current law, the deficit in 2025 would be between 5.0 percent and 7.1 percent of GDP')]),
 g('2024-02.deficit.2029', '59710', 'deficit', FY(2029), 2.9, 7.9, [q(48, 'there is a roughly two-thirds chance that the deficit for that year would be between 2.9 per cent and 7.9 percent of GDP')]),
 g('2024-02.growth.2024', '59710', 'growth', CY(2024), -0.2, 2.9, [q(70, 'between –0.2 percent and 2.9 percent in calendar year 2024 and between zero and 4.1 percent in 2027')]),
 g('2024-02.growth.2027', '59710', 'growth', CY(2027), 0.0, 4.1, [q(70, 'between zero and 4.1 percent in 2027')], note='The figure note on the next page prints 4.0 percent for the upper end; the text is read.'),
 g('2024-06.deficit.2025', '60039', 'deficit', FY(2025), 5.5, 7.6, [q(22, 'there is an approximately two-thirds chance that, under current law, the deficit in 2025 would be between 5.5 percent and 7.6 percent of GDP')]),
 g('2024-06.deficit.2029', '60039', 'deficit', FY(2029), 3.5, 8.5, [q(22, 'there is a roughly two-thirds chance that the deficit for that year would be between 3.5 percent and 8.5 percent of GDP')]),
 g('2024-06.growth.2024', '60380', 'growth', CY(2024), 0.8, 3.2, [q(4, 'between 0.8 percent and 3.2 percent in 2024 and between −0.5 percent and 3.9 percent in 2027')]),
 g('2024-06.growth.2027', '60380', 'growth', CY(2027), -0.5, 3.9, [q(4, 'between −0.5 percent and 3.9 percent in 2027')]),
 g('2024-12.debt.2029', '60664', 'debt', FY(2029), 102, 119, [q(18, 'debt at the end of that year would be between 102 percent and 119 percent of GDP')]),
 g('2025-01.growth.2024-2035', '61135', 'growth', AVG(2024, 2035), 1.5, 2.2, [q(24, 'for an average annual growth rate over the 2024–2035 period of between 1.5 percent and 2.2 percent')]),
 g('2025-01.growth.2024-2025', '61135', 'growth', AVG(2024, 2025), 1.1, 3.1, [q(24, 'the annual rate of real GDP growth since 2023 will be between 1.1 percent and 3.1 percent by the end of 2025')]),
 g('2026-02.deficit.2027', '61882', 'deficit', FY(2027), 4.6, 6.8, [q(29, 'the deficit would be between 4.6 and 6.8 percent of GDP in 2027')]),
 g('2026-02.debt.2031', '61882', 'debt', FY(2031), 101, 118, [q(31, 'federal debt held by the public equals 110 percent of GDP in 2031'), q(31, 'federal debt would be between 101 and 118 percent of GDP in that year')]),
 g('2026-02.growth.2026', '61882', 'growth', CY(2026), 0.5, 3.9, [q(55, 'the annual rate of real GDP growth will be between 0.5 and 3.9 percent')]),
]
def n(f, page, text, why): return dict(file=f, report=R[f][0], report_month=R[f][1], quote=[q(page, text)], why=why)
not_counted = [
 n('51129', 59, 'have a two-thirds chance of being within a range of 1.2 percentage points above or below the actual amount', 'a spread with no endpoints printed: the forecast it is set around is not stated in the sentence'),
 n('53090', 12, 'there is about a two-thirds chance that the actual average growth rate over the next two years will be within 1.3 percentage points of the rate in CBO’s current forecast', 'a spread with no endpoints printed'),
 n('55234', 17, 'there is a two-thirds chance that, if current laws gener ally remained unchanged, the deficit would be between 3.5 percent and 5.6 percent of GDP in 2020', 'the same range was printed first in August 2019 (counted there)'),
 n('55234', 17, 'between 79 percent and 97 percent of GDP in 2024', 'the same range was printed first in August 2019 (counted there)'),
 n('54318', 20, 'between 0.8 percent and 3.5 percent over the next five years', 'the same range was printed first in April 2018 (counted there)'),
 n('55505', 8, 'there is approximately a two-thirds chance that the rate of real GDP growth over the next five years will be between 0.7 percent and 3.3 percent', 'the same range was printed first in August 2019 (counted there)'),
 n('56050', 4, 'would be 1.9 percentage points smaller or larger than the 4.9 percent the agency projects', 'the same 2025 deficit range, printed with endpoints in the January 2020 outlook (counted there)'),
 n('59096', 9, 'there is an approximately two-thirds chance that the deficit would be about 0.5 percent of gross domestic product (or about $140 billion in 2023) larger or smaller than the agency estimates', 'a spread with no endpoints printed'),
 n('60664', 18, 'the deficit in that year would be between 3.5 percent and 8.5 percent of GDP', 'the same 2029 deficit range was printed first in June 2024 (counted there)'),
]
scan = json.load(open('data/stated_scan.json'))
reports_read = [dict(file=o['file'].rsplit('/', 1)[1][:-4], pages=o.get('pages'), two_thirds_passages=len(o.get('hits', [])), error=o.get('error')) for o in scan]
frame_readings = [
 'Only ranges printed as two numbers count. A spread printed as plus or minus some points with no endpoints is listed apart and not counted.',
 'A range counts once, in the report that first printed it. A later report that prints the same numbers for the same year is listed apart.',
 'Growth ranges are real GDP growth on a calendar-year basis: for one year, the annual growth rate in that year; for a span, the average annual growth rate over those years from the year before. Ranges for nominal GDP, inflation, unemployment and interest rates are outside the frame.',
 'Horizon is the target year minus the year of the report (for a span, its last year). Three or more counts toward the headline.',
 'A target year that ends after 30 September 2025 (fiscal year 2025) is held, so calendar 2025 is held.',
 'Old reports (2003 to 2016) state uncertainty as fan charts or spreads and print no two-thirds range with two endpoints for these measures, so the first counted range is from August 2016.',
]
json.dump(dict(_doc=__doc__, copied='2026-11-21, before any actual was opened', frame_readings=frame_readings, ranges=ranges, not_counted=not_counted, reports_read=reports_read), open('data/stated_src.json', 'w'), indent=1, ensure_ascii=False)
print('ranges', len(ranges), 'not counted', len(not_counted), 'reports read', len(reports_read))
