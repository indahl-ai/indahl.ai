# Quant desk rules (12 Nov 2026), errata lane
Empirical quantitative-finance papers on arXiv (q-fin, 2025 to 2026: backtests, Sharpe ratios, out-of-sample tests, returns, portfolios),
only those whose authors we can reach. The check is the one academic replicators don't run: places where a paper disagrees with itself.
Errata framing: "a classification for indexing, not an assessment of the study or its authors". Quote only, no adjectives, never
investment advice, never a judgement on a strategy's merit.

Paper types: E (empirical: backtest, estimation, measurement), M (method with an empirical test), T (theory, survey or simulation only).

Codes shown on pages: F2 (a single best value headlined, such as the best strategy, best window or best asset, with the spread across the
tested set not beside it), F3 (a claim of outperformance or significance with no interval, standard error, t-statistic or test behind it;
a Sharpe ratio printed without a standard error does NOT fire alone, only a claim built on it), F5 (a printed number that does not follow
from the paper's own printed numbers: annualisation, cumulative return against period returns, Sharpe against mean and volatility,
percentages, sums), F6 (text against the paper's own table, figure caption or appendix). F1 and F4 are drafted, kept off pages.
Prose against prose is CANNOT_TELL. Severity tiers, the same as SAGAR: T1 arithmetic or typo, T2 contradiction, T3 sits in or sets a
headline number. Every finding needs two readers: the draft agent and a blind second-reader agent.


## 21 Nov 2026 (2026-11-21T04:21:32Z): what the second reader is given
Dated line, ordered by the referee (OTHER DESKS: SAME CHANGE, 21 Nov 04:12Z) after her check of SAGAR's second reads.
- Until now this desk's second reader was handed, with each item, the passage the first reader had paired with it, the first reader's tier and the first reader's quote. It judged them without seeing the first reader's verdict or working, but it did not find the place itself. No record made before this line may be called blind or independent.
- All 748 existing records (verified and review) now carry `second_reader_saw: "pairing and tier"`, and their method label no longer says blind.
- From the next second read launched, the second reader is given the printed passage and a neutral task only. The full item is kept in `work/<batch>_items_full.json` for the merge. Agreement needs matching verdicts at the same place; a matching verdict at a different place is logged as "agree, different place" and goes to review; a recompute with no paired place is counted on its own.
- Backups of the pipeline, the prompts and the record files end in `.bak-20261121-secondinput`.
