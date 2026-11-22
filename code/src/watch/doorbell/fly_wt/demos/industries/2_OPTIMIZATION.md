# Industry 2 of 5: Optimization / logistics (one industry at a time, the owner 19 Nov)

## The client's run
QAOA for MaxCut-type scheduling and routing problems, run IBM's tutorial way: Sampler, level-3 transpile, layout from the record, no readout correction (IBM's QAOA tutorial uses none). The client reads the cut value / approximation ratio. Tonight we ran exactly this circuit on kingston: 100 nodes, 111 edges, p = 1.

## The operator's plan: specific calibrations that land on THIS run
1. **The 5 qubits the record says are fine but aren't (Q19 + Q2/Q9/Q11), corrected in place instead of moved.**
   - Tonight's P job flagged q58, 76, 77, 90 and 99 in the client's own layout as reading out worse than the record says (measured, job dbv4lnf82tmc73dudf0g).
   - Moving off them costs 458 vs 222 two-qubit gates, so we DON'T move. We keep the client's layout and correct those qubits' readout with today's table.
   - The tutorial corrects nothing, so every edge touching those qubits carries a wrong ZZ.
   - Number: COMPUTABLE FROM DISK with zero QPU. Tonight's raw check-run data is B, the client's exact circuit. Re-read it with the record's readout vs P's readout and give the cut value both ways.
2. **Coupling IBM lists as zero on live edges (Q1/Q7), compensated in the circuit.**
   - QAOA is layers of RZZ on native edges with idles in between. IBM lists zz = 0 on edges whose CZ the same record calibrates, while delivered is 2.9-15.4 kHz (bill line 7), and stated zz doesn't predict delivered (bill line 1).
   - Unseen coherent ZZ adds a phase to every edge every layer, at about 0.02-0.1 rad per microsecond of idle (computed from 2.9-15.4 kHz).
   - Ours: a virtual RZZ / phase compensation from the measured zz, at zero QPU cost.
   - Number: to compute from tonight's scheduled circuit durations + bill line 7.
3. **True gate error picks the depth (Q17).** Real CZ error is 1.24-1.37x stated. Clients pick depth p (and the number of layers they trust) from the stated figure. From the true figure, the best p is lower and the cut is higher. Number: to compute from the light-cone model on disk with the true vs stated error.
4. **One job, with the ruler measured on the client's own circuit (Q18 + witness/observer, internal).**
   - Tonight's check run was ON THIS QAOA circuit: B against itself, -0.0000 [-0.0009, +0.0008], 99%, n 12.
   - So on this run, any ours-vs-theirs difference bigger than about 0.001 is real. That's the one place our floor is measured on the client's own circuit.
5. **Qubit-reuse QAOA (measure and reset to fit a bigger problem) gets the darkwave correction.** Niche, but when a logistics client uses reuse to go past the chip's size, every reset readout kicks its neighbors 1.6-2.9 deg, and our table gives back 0.80-0.93.

## What the client sees
- Cut value / approximation ratio, ours vs the tutorial, on their own layout and in the same job.
- #1 can be computed TONIGHT from the data already on disk.
- #2 and #3 are offline computations.
- A run only if they show a gap: about 115 s main, as already built.

## Ratings of the other two plans (the operator)
- **The referee (round 2 §7, "optimization: the health check is the product"):**
  - Right that moving the layout costs more than it saves.
  - But she stopped there. She missed correcting in place (#1), the zz-zero coupling (#2) and the true-error depth (#3), all of which land on the QAOA run.
  - Scores: A 2, B 3, C 3, D 5, E 4, F 3, G 4.
- **The designer (round 2, "Optimization: health check"):**
  - The same stop as the referee. His BALL says simulation, optimization and chemistry got the same codes fix as Finance; to be read when he files his section here.
  - Scores pending his revised section.

## Top pick for Optimization
The client's own QAOA layout, kept as is, with today's readout table on the 5 qubits the record got wrong and zz compensation on the edges IBM lists as zero. Scored as cut value vs the tutorial in the same job, with tonight's on-circuit floor (0.0009) as the ruler.
