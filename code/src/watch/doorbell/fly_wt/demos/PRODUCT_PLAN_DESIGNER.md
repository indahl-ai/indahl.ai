# Product plan: The designer (19 Nov 2026), round 2

I wrote this before reading PRODUCT_PLAN_REFEREE.md (it landed while I worked; unread when this was written).

**The rule (the owner):** the biggest improvement counts only where it lands on that industry's run. Every number was read today from the file named beside it. No new IBM time.

**Labels:**
- **measured:** a reading fixed before fire, from our own job.
- **computed from disk:** arithmetic on measured readings, done here.
- **defined after the data:** a reading chosen after the job came back.
- **estimate:** not on disk.

**Sources:**
- **K1** = research/kick_today/code/analyze_k1_ibm_<chip>.log. Fired 17 Nov on three chips, 2,000 shots, 117 untouched qubits, 8 readouts of 39 neighbors, 99 % intervals. Arms:
  - M = the client's run, no correction;
  - MC = our 27-day-old kick table;
  - MF = our fresh kick table, measured minutes before;
  - ME = a symmetric echo.
- **P2** = research/closeout/phase2/results_p2_ibm_<chip>.text and CHECKS.md. Fired 17-18 Nov on 48 Bell pairs with 4 neighbor readouts and 2,500 shots; 99 % bootstrap over pairs × trials.
- **Seat** = optimization/run/seat_optimization.text (tonight).

## The two biggest numbers we hold, and where they land

### A. Entangled pairs next to a readout lose fidelity, and our table gives it back (Q14 + darkwave)
| Chip | Pair fidelity lost to the readouts, client's run | Lost with our table | Ours / theirs | Pre-set claim |
|---|---|---|---|---|
| kingston | 0.243 (record placement), 0.208 (fresh placement) | 0.0091, 0.0045 | **0.04, 0.02 (about 27x and 46x less)** | Table vs none: **+0.219 [+0.120, +0.318] ABOVE** |
| fez | 0.053, 0.070 | 0.0014, 0.0118 | **0.03, 0.17** | **+0.055 [+0.033, +0.079] ABOVE** |

Sources:
- The "+" column is P2-K, measured (predicted ABOVE in PLAN 7).
- The loss columns are P2's given-back lines (each arm vs its own idle), defined after the data. The ratios are computed from disk.
- Cost: P2 main jobs 212 s (kingston) and 208 s (fez) charged (CHECKS.md R).

### B. A qubit that should come back to 0 doesn't, after 8 neighbor readouts, and our fresh table fixes it (Q12 + darkwave)
| Chip | Wrong-answer rate, client's run (M) | With our fresh table (MF) | Ours / theirs | 27-day table (MC) |
|---|---|---|---|---|
| fez | 0.0407 [0.0127, 0.0570] | 0.0013 [−0.0040, 0.0047] | **0.03 (31x less)** | 0.0047, fine |
| kingston | 0.0552 [0.0285, 0.0890] | 0.0013 [−0.0013, 0.0058] | **0.02 (42x less)** | 0.0020, fine |
| marrakesh | 0.0230 [0.0080, 0.0508] | 0.0010 [−0.0013, 0.0055] | **0.04 (23x less)** | phase overshoots, +0.94 [+0.61, +1.46] deg per readout |

Sources:
- K1 reading S3, measured: the P(1) excess on a qubit that should read 0, from the committed keystone analysis. Ratios are computed from disk.
- The fresh-table arms are consistent with zero, so the honest form is "down to what we can't tell from zero".
- Cost: 75 s (fez), 165 s (kingston) and 171 s (marrakesh) charged, including the 11 s table job (fire_ibm_<chip>.log).
- The marrakesh 27-day row is why a fresh table is a service and not a one-off: the kick moved, and the old table turns the phase the other way (K1 S5, BELOW).

**What neither number covers:** coherence lost next to a readout (Q13). K1 S4 is about −0.006 in every arm. The table turns phase back; it does not return coherence. Said on the page.

**The one open question that decides both:** do the client's default settings already do what our echo does? On disk, the echo ties our table:
- K1 ME residuals are consistent with zero.
- P2 "table on top of echo" is +0.0001 [−0.0039, +0.0039], CONSISTENT.

If IBM's default dynamical decoupling acts as that echo, the client already gets most of this, and our table's edge is cost and reach:
- zero gates against two X per qubit per window;
- it works on qubits busy with gates, where an echo can't go.

If the default doesn't act as that echo, the numbers above stand as ours vs theirs.

The smallest run that settles it: one job, the client's DD on vs our table, after an 11 s table. Under 100 s, by K1's fez cost. Doesn't fire without the owner.

## Per industry: biggest improvement that lands

| Industry | Does A or B happen in their run? | Our calibrated run | Client's way vs ours | Number from | Smallest run to get their own number |
|---|---|---|---|---|---|
| **Long-range entanglement / networking** (GHZ and teleported gates by measure and feed-forward) | **A, directly.** The circuit holds Bell pairs while neighbors are measured, which is exactly what P2 measured. | Fresh table + pairs placed off the heaviest readouts (Q14) + fresh readout (Q2, Q9) | Pair fidelity lost: **0.24 → 0.005-0.009 (kingston); 0.05-0.07 → 0.001-0.012 (fez)** | P2, measured / defined after the data | 8-12 qubit GHZ by feed-forward, our table vs the client's DD, one job |
| **Error correction** (repeated syndrome rounds) | **B, directly.** Data qubits sit through repeated neighbor readouts and must keep their state; that is K1's setup. | Fresh table every session (11 s), syndrome readout re-measured (Q9), data qubits off the costliest readouts (Q13) | Per-qubit wrong-answer rate after 8 readouts: **0.023-0.055 → about 0.001** (23-42x less) | K1, measured | 3-5 data-qubit code, 10 rounds, our table vs the client's DD |
| **Chemistry** (iterative phase estimation) | **B, as a bias.** The system register's phase is the answer, and each ancilla readout turns it. | Fresh table on the system register after each ancilla readout | Phase bias per readout: **1.75-2.51° → ≤ 0.10-0.21° (99 % upper end; point 0.004-0.10°)**, so at most 5-12 % of today's bias | K1 S1 MF vs KG kick, computed from disk | H2 minimal basis, 4-6 rounds, energy vs exact, our table vs none |
| **Chemistry** (SQD, end-measured) | Codes clear the readout deviations directly; SQD usually runs without readout correction, so a bad qubit's flips feed recovery. | Q2/Q9/Q10/Q11 readout from today, Q19 layout, Q17 depth | Ledger of cleared codes on the qubits used, plus valid-bitstring yield, ours vs theirs; readout cases on disk (q15, q155) | P2 readout table, measured | Health check + SQD sample, arms interleaved in one job |
| **Simulation** (Trotter + ZNE/PEA) | Codes clear the noise-model deviations: Q3-Q6 stale T1/T2 (up to 97 days), Q16 decay shape, Q1/Q7 zz stated 0 on live edges (delivered 2.9-15.4 kHz) | Repaired noise model and measured-zz placement before the run | Observable vs exact, record-built vs repaired; the ledger shows each code cleared | bill lines 1, 3-7, 16, measured | 1D Ising, 4-6 qubits, both arms in one job |
| **Optimization** (QAOA) | Codes clear deviations already caught tonight: P flagged 6 qubits worse than their record (58 76 77 90 99 113) | Q9/Q19 flags, Q1/Q7 coupling, Q17 gates, before the run; seat proves the ruler | Cut value, ours vs theirs; ruler 0.0009 (seat, tonight, measured) | P + seat, measured | Main as planned, after the referee's hold is resolved |
| **Finance** (MLAE option pricing) | **Yes: the price is P(1) on one qubit, sized and corrected from the record.** Full plan in industries/1_FINANCE.md, the designer's round | Q2/Q9/Q10/Q11 objective-qubit readout, Q17 ladder + fade, Q1/Q7 oracle edges, Q18 seat on the ladder | Readout bias on the price: +0.054 at 0.10 (kingston q15) → about 0; fez q155 record correction returns −145 | P2 readout table + CHECKS, computed from disk | 11 s check + 30 s RB + 3-qubit ladder, arms interleaved |

**Withdrawn (19 Nov): my earlier Finance row ("codes only, no big number, not a lead demo") and the same "not a lead demo / to measure" calls on SQD, Simulation and Optimization. A demo where the codes visibly clear the deviations is the product; the rows above replace them.**

## The codes half: big numbers from the record, measured on disk

These clear deviations before the run, on every industry's demo, and each shows on that demo's ledger.

- **fez q155 (Q10, record not flagged):** the record says P(1|0) 0.982; the same job measured 0.010-0.014 over 5 trials (P2 CHECKS QC).
  - Arithmetic that trusts the record divides by 0.007, and pair (139,155) read "fidelity" 26 and 72 (P2-S +4.66).
  - Without that pair it reads +0.169.
  - One stale line in the record turned a working qubit's answer into nonsense.
- **kingston q15 (Q2/Q9):** stated P(1|0) 0.0020, delivered 0.0643 [0.0588, 0.0702]. That's 32x the record, on 17 Nov (P2 kingston readout table, measured).
- **kingston, stated-zero P(1|0) (Q2):** the record says 0 on qubits 5, 6, 21, 61, 68, 105 and 106; delivered 0.0006 to 0.0059 on all seven (P2, measured).

## My top three, by the rule
1. **Long-range entanglement: A.** The biggest measured number (0.24 of pair fidelity back on kingston, 27-46x less loss) lands on exactly the circuit this field runs.
2. **Error correction: B.** It's 23-42x on three chips, measured, and it lands on every syndrome round.
3. **Chemistry IPE: B as a bias.** Shots can't remove a bias. We cut it to at most 5-12 %.

Codes as the pre-run check on all three, with q155 as the one-line story.

Before any of the three becomes a client claim: one sub-100 s job, the client's default DD vs our table.

## Addendum after reading the referee's plan (same night)
The referee is right about dose. The kick scales with how many qubits are read at once:
- 39 of 156 read: −1.62° on fez;
- 10 of 39 read: −0.17° [−0.32, −0.07] (bill line 12, fez 22 Oct repeat, measured).

**Chemistry IPE reads one ancilla per round, so B lands on it weakly. It drops out of my three.** Teleportation (few readouts) drops with it.

A and B stand where the readout is dense:
- syndrome rounds read about half the register;
- measurement-built GHZ reads the middle qubits;
- both K1 and P2 read 39 neighbors.

My three are now: error correction (B), measurement-built GHZ / dense long-range entanglement (A), and the pre-run health check (codes; the referee's #3, with q155).

## Top three, revised 19 Nov (supersedes both lists above)
Ranked by codes and findings visibly clearing deviations on the run the industry actually does, not by headline size alone:
1. **Error correction syndrome rounds:** findings (fresh kick table, 23-42x on K1) plus codes (syndrome readout Q9, init Q8, neighbor cost Q13) on one ledger.
2. **Finance, MLAE option pricing:** codes clear four deviations the price leans on (objective-qubit readout, true-error ladder and fade, oracle coupling, job drift). On disk: +0.054 price bias from one mislabelled qubit, and a stale line that returns −145.
3. **Dense long-range entanglement:** P2-K +0.219 measured, plus the Q14 placement and Q1/Q7 coupling codes.

The pre-run health check is the first line of every demo's ledger, not a separate pick.
