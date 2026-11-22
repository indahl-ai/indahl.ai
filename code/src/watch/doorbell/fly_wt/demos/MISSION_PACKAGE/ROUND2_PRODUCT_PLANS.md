# Round 2: actual product plans, then hot potato (the owner, 19 Nov 2026)

the owner scanned round 1: "you're on the right track." What he wants now is PRODUCT PLANS with real numbers. Not reasons it won't work.

## Step 1: each of us writes a product plan (PRODUCT_PLAN_<NAME>.md in the parent folder)
For each industry, take the client's run and lay out:
- our calibrated run, matched to what that run needs (our science, our accounted-for errors, or both);
- the end-of-run result the client's way vs our way, AS A NUMBER;
- where the number comes from.

Use data ALREADY ON DISK first (no new IBM time). Work out the client-default result and the calibrated result from runs we already have, and label each number measured / computed from disk / estimate. Where a field has no data, name the one small run that gets it. That run doesn't fire without the owner.

We don't have to show everything for every industry. Find the deviations we can account for that give the BIG results.

Examples already in our record (verify each against its source before using it):
- **Readout next to entangled pairs (Q14), plus a symmetric echo.** Readouts cost Bell pairs 0.25 of fidelity on kingston and 0.06 on fez. With the echo the loss drops to about 0.01 on both chips. That's about +0.24 fidelity back on kingston. Source: Phase 2 re-analysis, commit 1e7a051. Each arm is compared with its own idle; post-hoc.
- **Darkwave correction (internal; in public, paper 2's language).**
  - marrakesh untouched qubits: 0.24 given back from a ten-day table, 0.80 [0.67, 0.88] from a fresh table.
  - marrakesh Bell-pair phase: 0.40 old vs 0.92 fresh.
  - kingston clock state: 0.76 old vs 1.00 fresh.
  - marrakesh clock: -0.51 old (worse than no correction) vs 0.77 fresh (copies disagree).
  - echo: 0.91-1.00, with no table, at the cost of two X gates per untouched qubit.
  - Source: paper 2, 31 Oct run, 99% bootstrap bands.
- **Fresh-data layout:** +0.029 (fez), +0.049 (marrakesh); did not repeat on kingston (the referee's round 1).
- **Pre-run health check:** our hourly runs caught fez q155's bad readout 1-3 hours before IBM's own refresh did (the referee's round 1). Record: P(1|0) 0.982, measured 0.013.
- **Tonight's within-job floor:** 0.0009 (99%, 12 trials), about 11x tighter than planned.

## THE RULE (the owner, 19 Nov): bigger is better, by lots, but ONLY if it applies to that industry's run
Pick each industry's demo by the BIGGEST improvement that actually lands on that industry's run. A huge number measured on a circuit that industry never runs counts for nothing there. A big number is only worth something where it applies. So for each industry, first ask: does this deviation happen in this industry's run? Then rank the ones that do by size, biggest first.

## Step 2: hot potato triangulation
Once all three plans are in, each of us rates the OTHER TWO plans, industry by industry, on these metrics. Score each 0-5 with one line of why.

| Metric | What scores high |
|---|---|
| A. Size of the win, where it applies | The biggest end-of-run improvement THAT LANDS ON THIS INDUSTRY'S RUN, ours vs the client's real default. A big number that doesn't apply to this industry scores 0 here. The client's default includes the mitigation they'd already switch on |
| B. Backed by our data | The number comes from our own runs on disk, not an estimate |
| C. Ours, not generic | The treatment is our science or our accounted-for errors (IBM codes), not something M3/TREX/PEA already does |
| D. The client really runs it | The likeliest workload in that industry |
| E. Cheap to show | Few QPU seconds, and data already on disk |
| F. Plain to sell | One clean number a buyer understands (fidelity, energy error, error bar, shots saved) |
| G. Holds up | States its comparison and what it rules out; four outcomes; post-hoc labelled |

Each rater returns a table (plan x industry x metric) plus their top three across all plans. The operator collects everything and gives the owner one sheet: the scores side by side, where the raters agree, and where they split.
