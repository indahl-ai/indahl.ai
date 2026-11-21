# BRANDS desk rules (12 Nov 2026)
Papers with at least one author at a named company (Google, Microsoft, NVIDIA, Meta, IBM, Amazon, DeepMind, Apple), 2026, with an arXiv
version, and only those whose authors we can reach. Same errata check as SAGAR: places where a paper disagrees with itself.
Errata framing: "a classification for indexing, not an assessment of the study or its authors", never a ranking of companies, quote only,
no adjectives. Emails follow the corporate rule: all at once, the same way.

Paper types: E (empirical result: experiments, benchmarks, measurements), M (method, with a benchmark), T (theory, survey or position).

Codes shown on pages: F2 (single best value headlined, spread not beside it; benchmark "state of the art" claims with one number count
only when the paper's own tables show the spread), F3 (a claim with no significance, interval or variance across seeds or runs behind it),
F5 (a printed number that does not follow from the paper's own printed numbers), F6 (text against the paper's own table, caption,
appendix or released file). F1 and F4 are drafted but kept off pages, as on SAGAR. Prose against prose is CANNOT_TELL.
Severity tiers, the same as SAGAR: T1 arithmetic or typo, T2 contradiction, T3 sits in or sets a headline number.
Every finding needs two readers: the draft agent and a blind second-reader agent.


## 21 Nov 2026 (2026-11-21T04:21:32Z): what the second reader is given
Dated line, ordered by the referee (OTHER DESKS: SAME CHANGE, 21 Nov 04:12Z) after her check of SAGAR's second reads.
- Until now this desk's second reader was handed, with each item, the passage the first reader had paired with it, the first reader's tier and the first reader's quote. It judged them without seeing the first reader's verdict or working, but it did not find the place itself. No record made before this line may be called blind or independent.
- All 192 existing records (verified and review) now carry `second_reader_saw: "pairing and tier"`, and their method label no longer says blind.
- From the next second read launched, the second reader is given the printed passage and a neutral task only. The full item is kept in `work/<batch>_items_full.json` for the merge. Agreement needs matching verdicts at the same place; a matching verdict at a different place is logged as "agree, different place" and goes to review; a recompute with no paired place is counted on its own.
- Backups of the pipeline, the prompts and the record files end in `.bak-20261121-secondinput`.
