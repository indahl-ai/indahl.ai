# Mission brief: the demos are a PRODUCT SHOWCASE (the owner, 19 Nov 2026)

To the referee and the designer, from the operator. Read all of this before your first pass.

## Where it went wrong
Four of five demos treated generic readout calibration: stale readout figures, fixed by moving the layout. That's something M3, TREX and any client already do. The plans started from IBM's tutorials, and our findings were only checks bolted on. The redirect to "the kick only" narrowed it to one finding. Both are dead. Do not start from tonight's plans, and do not argue the old designs.

## The mission
This is a product showcase, not research. Industry by industry, show that a run calibrated OUR way ends with significantly lower error than the same run done the way the client does it today. Lower error at the end of every run means saved money, better performance, fewer shots and fewer reruns. The clients care about that. Our job is to show them how. Write it in plain English the owner can read, not our internal shorthand.

## What we have (start here, ALL of it, combinations welcome)

1. **The IBM codes, Q1-Q19, on the QIA Key** (https://indahl.ai/qia/key; source indahl-ai/qia_site.py). Q1-Q16 are the sixteen lines of bill QIA-2026-001 (indahl-ai/qia_template/QIA-2026-001.json). Each is something IBM's record treats as ordinary error, or doesn't cover, and that we can calibrate for BEFORE the run. Never call them "Faults."
   - **Stale record under a fresh stamp:** Q3, Q4, Q5, Q6, Q8 and Q10 (T1, T2 and init values days to months old; IBM flags stale gates but not stale readout or init).
   - **Readout figures:** Q2 (zero stated, not zero), Q9 (readout drifts between cycles hours apart) and Q11 (readout_error isn't the average of its parts).
   - **Coupling:** Q1 (stated zz doesn't predict the neighbor shift) and Q7 (zz = 0 stated on live CZ edges).
   - **What a readout does to neighbors, with no IBM field:** Q12 (phase kick), Q13 (coherence lost next to a readout) and Q14 (entanglement lost next to a readout).
   - **Beyond IBM's noise model:** Q15 (weak-probe offset) and Q16 (idle decay not single-exponential).
   - **From our runs:** Q17 (gate error above stated), Q18 (job-to-job drift) and Q19 (the record doesn't predict the better layout).
2. **The darkwave correction** (INTERNAL name; in public it's the paper's language: "A Readout's Kick Is a Turn", Zenodo 10.5281/zenodo.23843468, runs at ~/forge/the_show/runs/2026-10-31-keystone/). A per-qubit virtual Rz from our table gives back the kick:
   - kingston: 0.92 [0.87, 0.95] from a 10-day-old table and 0.93 from a fresh one;
   - marrakesh: 0.80 [0.67, 0.88] after the kick drifted (-2.39 to -1.68 deg);
   - aging shows in the clock state: 0.76 old vs 1.00 fresh;
   - the correction costs zero QPU time, and the table costs about 11 s per chip.
   - The kick itself is paper 1, "A Readout Is Not an Idle" (Zenodo 10.5281/zenodo.23169755): -1.6 to -2.9 deg per readout on untouched neighbors.
   - Prior art: Krinner et al., Nature 2022. Source of these numbers: yo_school/research/pitch_tables/BRIEF_V2_OUR_FINDINGS_20261117.md; verify against the papers.
3. **The witness/observer separation** (INTERNAL language only; never in client copy). We identify the deviations and separate the actual signal from the noise in a run's output, instead of averaging the deviation away as noise everyone accepts.
4. **Every other calibration we've measured:** fresh per-qubit readout (fez q155: record P(1|0) 0.982, measured 0.013), per-entry record ages, readout near entangled pairs (kingston 0.25 of pair fidelity; echo extra loss 0.010), and the within-job floor from tonight's Optimization check run (99% half-width ~0.0009 over 12 trials, about 11x tighter than planned).
   - Also: THE_BOOK's client rows, qia_leads/THE_BOOK.md C1-C45+.

## Your first pass (separate, blind to each other, no IBM, no code)
For EACH industry (Finance, Optimization/logistics, Chemistry/materials, Simulation/physics, Dynamic circuits/error correction, plus any other industry you think we're strongest in):

1. **The run:** the likeliest client workload in that industry where our calibrations bite hardest. Name the circuit family.
2. **Our calibrated run:** which codes, which correction (darkwave, fresh tables, witness/observer separation), alone or COMBINED, and what's done BEFORE the run vs on the output.
3. **The client's run today:** IBM defaults, the tutorial's settings, and what error they accept at the end.
4. **What the client sees:** the end-of-run error, ours vs theirs, as a ratio. Use our measured numbers where they exist and mark what still has to be measured. Plain English.
5. **Why they care:** money, shots, reruns, accuracy, time to answer. One line.
6. **What we already have on disk** to back it, and the smallest run that would show it.
7. **Your top pick per industry and your overall top three.** Where an industry has no strong case, say so.

Keep all options open: combinations, other industries, other workloads.

The output is a short table per industry plus a plain-English paragraph. The operator collects all three passes and gives the owner them side by side, disagreements marked. Nothing is built or fired until the owner picks.
