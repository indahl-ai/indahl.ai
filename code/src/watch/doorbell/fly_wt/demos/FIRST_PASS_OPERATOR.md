# First pass: The operator (19 Nov 2026), blind to the referee and the designer

Plain English. Numbers come from the bill (indahl-ai/qia_template/QIA-2026-001.json), the QIA Key and the two papers. "To measure" means we don't have the number yet.

## Four tools we bring to any run
1. **Record repair before the run (IBM codes Q2-Q11, Q17, Q19).** The client's tools trust IBM's published record. That includes the layout picker, readout mitigation and the noise models behind ZNE and PEA. On any given day some of that record is wrong or old:
   - readout figures move 16-62% between cycles hours apart (Q9);
   - "zero" readout error isn't zero (Q2);
   - T1/T2 values run up to 97 days old under a fresh stamp (Q3-Q6);
   - zz is listed as 0 on live edges (Q7);
   - init error is missing or stale (Q8).
   We run a short check job first, find the fields that are wrong today, and feed corrected numbers into the client's own tools. Honest limit: fresh readout calibration alone is what M3 already does. What's ours is knowing WHICH record fields mislead and auditing them per run.
2. **The darkwave correction (internal name; in public, the paper's language from "A Readout's Kick Is a Turn") (Q12).** Every mid-circuit readout turns its neighbors' phase by 1.6-2.9 deg. A per-qubit virtual Rz from our table gives back 0.80-0.93 of it, at zero QPU cost. Measuring the table takes about 11 s per chip. It only matters in circuits that read qubits mid-run.
3. **What a readout costs its neighbors (Q13, Q14).**
   - Q13, coherence: fez 0.0070, marrakesh 0.0093 clean-shot loss per readout.
   - Q14, entanglement: kingston +0.006, marrakesh +0.009 to +0.021.
   - We know which neighbors pay, so the run can be scheduled and spaced to avoid it, or corrected after.
4. **The witness/observer separation (internal only).**
   - Split a run's deviation into the part every run shares (drift, the apparatus) and the part that's the actual signal.
   - Q18 says the same circuit moves job to job by more than shot noise, and clients average that in as error.
   - Tonight's check run measured the within-job floor at about 0.0009 (99%, 12 trials), roughly 11x tighter than we planned for.
   - Separating the shared drift from the signal is what shrinks the end-of-run error bar.

## Per industry: my picks

| Industry | Likeliest client run | Our calibrated run | Client today | What they'd see | Why they care |
|---|---|---|---|---|---|
| Dynamic circuits / error correction | Repeated syndrome rounds (repetition or surface-code patch), mid-circuit readout and reset | darkwave table + Q13/Q14 spacing + fresh-table age check, with the witness/observer split on round-to-round drift | IBM defaults (DD, twirling), no phase correction | Logical error per round: lower with ours. The kick give-back is measured (0.80-0.93); the logical-error ratio is to be measured | Fewer rounds lost, so a longer usable memory |
| Chemistry / materials | Iterative phase estimation (ancilla read mid-circuit every round, system register beside it) | darkwave on the system register after each ancilla readout + Q13 + record repair | IBM defaults | Energy error vs exact, ours/theirs (to measure). Each round's kick adds phase error straight into the energy estimate | Chemical accuracy at fewer shots and rounds |
| Finance / economics | Amplitude estimation (option pricing, risk) or sampling-based portfolio runs, all measured at the end | Record repair (Q2, Q9, Q11 readout; Q3-Q6 staleness; Q17 gates) + the witness/observer split across jobs (Q18) | Record-trusting mitigation, results averaged across jobs | Error bar on the price or risk figure at equal shots, ours/theirs (to measure) | Fewer shots for the same confidence = direct cost cut |
| Optimization / logistics | QAOA, end-measured; at larger sizes, QAOA with qubit reuse (mid-circuit reset) | Record repair (Q19 layout, Q1/Q7 coupling at depth) + witness/observer; darkwave when qubit reuse is on | IBM's QAOA tutorial (no readout correction) | Approximation ratio / cut value, ours vs theirs (to measure). Tonight's check run gives the floor | Better answers per run, fewer reruns |
| Simulation / physics | Trotter dynamics with long idles and dynamic-circuit long-range gates | Q16 (idle decay isn't single-exponential) + Q1/Q7 (real neighbor coupling) + darkwave on the measured-gate steps | IBM defaults, record-built noise models (ZNE/PEA) | Observable error vs exact, ours/theirs (to measure) | Deeper simulations stay trustworthy |

## Matching: what each run needs → our best calibration

| Industry run | What it needs to come out right | Best match: OUR SCIENCE | Best match: OUR ACCOUNTED-FOR ERRORS | Pick |
|---|---|---|---|---|
| Error-correction syndrome rounds | Data-qubit phase and coherence kept through every round of mid-circuit readout | darkwave table (Q12), neighbor-cost spacing (Q13, Q14), witness/observer on round-to-round drift | Q9 (readout drift between cycles) for the syndrome readout; Q18 drift | Science-led combo |
| Chemistry: iterative phase estimation | System-register phase kept exact across every ancilla readout | darkwave on the system register (Q12), Q13 | Q2/Q9/Q11 ancilla readout; Q16 idle decay during feed-forward waits | Science-led combo |
| Chemistry: SQD (end-measured) | Correct bitstrings: readout errors decide which configurations survive recovery | witness/observer on shot-to-shot drift | Q2, Q9, Q11 readout repaired pre-run; Q19 layout | Accounted-for errors |
| Finance: amplitude estimation / sampling | Unbiased probabilities, tight error bars per shot | witness/observer: split the shared drift from the signal across jobs (Q18) | Q2, Q9, Q11 readout; Q3-Q6 stale T1/T2 feeding ZNE/PEA noise models; Q17 gates | Accounted-for errors + witness/observer |
| Optimization: QAOA | Good samples; layout on the truly best qubits; crosstalk at depth handled | witness/observer; darkwave when qubit reuse is on | Q19 layout, Q1/Q7 coupling, Q17 gates, Q9 readout | Accounted-for errors (science if qubit reuse) |
| Simulation: Trotter dynamics | Observables stay right through deep circuits with idles and dynamic long-range gates | Q16 idle decay, darkwave on measured-gate steps, Q13/Q14 | Q1/Q7 coupling (crosstalk), Q3-Q6 stale coherence feeding ZNE/PEA | Combo |

## Combinations
- **Error correction:** darkwave + Q13/Q14 spacing + table-age check (all three bite the same circuit).
- **Chemistry:** darkwave + record repair (the ancilla readout figures matter too).
- **Finance:** record repair + witness/observer. There's no mid-circuit readout, so no darkwave.

## My overall top three
1. **Error correction / dynamic circuits.** The strongest data we already hold (both papers, three chips), and the darkwave correction is ours outright.
2. **Chemistry: iterative phase estimation.** Same core asset, the biggest commercial story, and a clean "energy closer to exact" headline.
3. **Finance: record repair + witness/observer.** The biggest market. Every number there still has to be measured, but the cost story (fewer shots for the same error bar) is the one a bank buys.

## What we already have on disk
- Both papers' runs: the_show/runs/2026-10-31-keystone/ and arxiv_one_readout/.
- The bill's per-chip numbers.
- Tonight's Optimization P table and the check-run floor: yo_school/research/closeout/demos/optimization/run/.

## The smallest run that shows each
One P job (calibration table plus kick table, about 11-17 s), then the client's run twice in one job: default vs ours. Error correction and chemistry can each be shown in a few hundred seconds.
