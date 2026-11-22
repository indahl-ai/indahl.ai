# First pass: The designer (19 Nov 2026)

**Not blind.** I read FIRST_PASS_OPERATOR.md before writing this, because it landed in the same pull as the package. Where I agree with the operator I say so in a line. Where I differ, the difference is marked **[differs]** so it shows when the passes sit side by side.

Plain English. Every number carries its source:
- **bill:** indahl-ai/qia_template/QIA-2026-001.json (copy in MISSION_PACKAGE/);
- **P1:** "A Readout Is Not an Idle", Zenodo 10.5281/zenodo.23169755, preprint;
- **P2:** "A Readout's Kick Is a Turn", Zenodo 10.5281/zenodo.23843468, preprint;
- **tonight:** optimization/run/seat_optimization.text.

"To measure" means we don't hold the number. "Modelled" means the arithmetic below, from measured inputs, has not been run on a chip.

## The product, in one paragraph

The client hands us the run they already do. We do two things they can't.
- **Before the run:** we clear the deviations IBM's record misstates, carries stale or doesn't cover (the IBM codes). That gives the client a layout, a readout map and a noise model built from numbers that are true today.
- **In the circuit and on the output:** we apply our science. The darkwave correction gives back the phase every mid-circuit readout steals. Neighbor-cost spacing keeps data qubits away from the readouts that bleed them. The witness/observer split takes the shared drift out of the result instead of averaging it in.

The client sees one number: their end-of-run error, ours over theirs.

## One demo format for every industry [differs: The operator has "default vs ours"; I add a middle arm and the ruler]

There is one job and one chip. The arms are interleaved, so drift hits all of them alike.
1. **Client today:** IBM defaults or the tutorial's settings, record as published.
2. **Client + our codes:** the same circuit, with the record repaired before the run.
3. **Client + our codes + our science:** the darkwave correction, spacing and the witness/observer split, wherever the run has something for them to act on.
4. **Seat:** arm 1 run against a copy of itself. This proves the ruler before we claim a ratio.
   - Tonight's seat read −0.0000 [−0.0009, +0.0008] (99 % t-interval, n 12, CONSISTENT; tonight).
   - Any ours/theirs difference bigger than about 0.001 in the same job is real.

Arm 2 against arm 1 shows what the codes are worth. Arm 3 against arm 2 shows what the science adds on top. A client asking "isn't that just M3?" gets the answer in the table.

## Per industry

### 1. Dynamic circuits / error correction: repeated syndrome rounds
| | |
|---|---|
| Run | Repetition code or small surface-code patch, 5 to 20 rounds of mid-circuit syndrome readout, reset and feed-forward. |
| What it needs | Data-qubit phase and coherence kept through every round; a syndrome readout that is accurate today. |
| Before the run | Kick table, fresh, about 11 s per chip (P2, job C logs). Q9/Q2/Q11 syndrome-readout figures re-measured. Q13/Q14 neighbor-cost map, so data qubits don't sit beside the heaviest readouts. Q8 init checked, since every round resets. |
| On the output / in circuit | A virtual Rz per data qubit per round, from the table (zero QPU time). The witness/observer split on round-to-round drift (Q18). |
| Client today | IBM defaults (dynamical decoupling, twirling). No phase correction for the kick. The record has no field for it (bill line 12). |
| Ratio | **Measured, the kick part only:** the residual after correction is 0.07 of the kick on kingston (fresh table gives back 0.93; P2) and 0.20 on marrakesh (0.80 [0.67, 0.88]; P2). **Modelled, after N rounds:** the uncorrected kick piles up, about 2.86° × N on kingston (P1), which is 29° after 10 rounds. Phase error on a superposition grows with the angle squared, so 0.07 of the angle leaves about 0.07² ≈ 0.005 of the error. **The logical error per round, ours/theirs, is to measure.** |
| Why they care | More usable rounds before the memory fails means longer computations from the same hardware. |
| On disk | Both papers' runs (the_show/runs/2026-10-31-keystone/, arxiv_one_readout/); bill lines 12 to 14 on three chips. |
| Smallest run | Kick table plus arms 1 and 3 at 10 rounds on one chip. About 170 s, from the keystone's per-chip cost (C 11 s + two arms about 80 s each; P2 logs). |

Agree with the operator: this is #1.

### 2. Chemistry / materials: iterative phase estimation
| | |
|---|---|
| Run | Iterative phase estimation. The ancilla is read mid-circuit every round, and the system register sits beside it holding the state whose energy we want. |
| What it needs | System-register phase kept exact across every ancilla readout. The phase IS the answer here. |
| Before the run | Kick table; Q2/Q9/Q11 ancilla readout; Q16 idle decay for the feed-forward waits; Q3 to Q6 if the client builds a noise model. |
| On the output / in circuit | Darkwave Rz on the system register after each ancilla readout. Q13 spacing. |
| Client today | IBM defaults. Each round's kick (1.6 to 2.9° per readout, P1) goes straight into the phase estimate as a systematic shift that more shots do not remove. |
| Ratio | **Energy error vs exact, ours/theirs: to measure.** Bias from the kick, modelled: the uncorrected shift is N × kick; corrected leaves 0.07 to 0.20 of it (P2). That is a bias, so it shows even at infinite shots. |
| Why they care | Chemical accuracy needs the bias gone. You can't buy your way out of a bias with shots. |
| On disk | Same as above. No chemistry run yet. |
| Smallest run | A 2-qubit Hamiltonian with a known exact energy (for example H2 in a minimal basis), 4 to 6 IPE rounds, arms 1 and 3. A few hundred seconds, to size. |

Agree with the operator: #2. The "bias, not noise" line is the pitch: shots can't fix it, we can.

### 3. Long-range entanglement / networking: GHZ and teleported gates by measurement and feed-forward [differs: The operator files this under Simulation; I'd make it its own showcase]
| | |
|---|---|
| Run | Constant-depth GHZ prep or a teleported long-range CNOT, done with mid-circuit measurement and feed-forward (IBM's own dynamic-circuit showcase family). |
| What it needs | Bell pairs that keep their entanglement while their neighbors are measured; phase kept on the surviving qubits; correct coupling on the edges used. |
| Before the run | **Q14** (Bell pairs lose entanglement next to a readout): fez 0.0070, marrakesh 0.0093 clean-shot loss per 4 readouts (bill line 14). This is exactly the resource these circuits spend. Q1/Q7 coupling (zz stated 0 on live edges, delivered 2.9 to 15.4 kHz; bill lines 1, 7). Kick table. |
| On the output / in circuit | Darkwave Rz on the kept qubits after the measured layer. Pairs placed away from the heaviest readouts. |
| Client today | IBM's dynamic-circuit tutorial settings on the record's layout. No knowledge of which pairs pay for which readouts. |
| Ratio | **GHZ fidelity error, ours/theirs: to measure.** All three inputs (kick, Q14 loss, coupling) are measured per chip. |
| Why they care | Long-range gates without long SWAP chains is the reason dynamic circuits exist. If the measurement step eats the entanglement, the shortcut costs more than it saves. |
| On disk | Bill lines 1, 7, 12, 14; P1's Bell-pair arms. The H0r GHZ jobs (17 Nov, three chips, raw saved, results not opened) are end-measured GHZ, not feed-forward, so they back the layout half only. |
| Smallest run | 8- to 12-qubit GHZ by measurement and feed-forward on one chip, arms 1 to 3. To size. |

### 4. Simulation / physics: Trotter dynamics with idles
| | |
|---|---|
| Run | Trotter time evolution, deep, with idle stretches; ZNE/PEA mitigation built from the record. |
| What it needs | A true noise model (the mitigation extrapolates from it) and true neighbor coupling at depth. |
| Before the run | Q3 to Q6 (T1/T2 up to 97 days old under a fresh stamp; bill lines 3 to 6) and Q16 (idle decay isn't single-exponential: 62 to 85 % below the line vs 49 to 54 %; bill line 16) fed into the noise model. Q1/Q7 coupling. Q17 gates (Book Part 0 only, weeks old: re-measure). |
| On the output | Witness/observer split across Trotter steps. |
| Client today | ZNE/PEA on a record-built model. |
| Ratio | **Observable error vs exact, ours/theirs: to measure.** |
| Why they care | Mitigation built on a wrong model extrapolates to a wrong answer, confidently. |
| On disk | Bill lines 1, 3 to 7, 16. |
| Smallest run | 1D Ising, 4 to 6 qubits, exact answer known, arms 1 and 2. To size. |

Codes-led. A fair demo, not a top three.

### 5. Optimization / logistics: QAOA at depth
| | |
|---|---|
| Run | QAOA, end-measured, depth 2 to 4. |
| What it needs | Two-qubit gates on edges whose real coupling and error are known; samples free of job-to-job drift. |
| Before the run | Q1/Q7 (crosstalk-aware placement from measured zz, which M3 and TREX don't touch), Q17 gates, Q19. Readout repair alone is the dead pattern and stays out of the pitch. |
| On the output | Witness/observer split (Q18). |
| Client today | IBM's QAOA tutorial. |
| Ratio | **Approximation ratio, ours/theirs: to measure.** The ruler is on disk tonight (floor ~0.0009). |
| Why they care | Better cut per run, fewer reruns. |
| On disk | optimization/run/ (P table, seat CONSISTENT; main never fired, held by the referee). P flagged qubits 58 76 77 90 99 113 as worse than their record (tonight). |
| Smallest run | Seat plus arms 1 and 2 at depth 2, sized off tonight's 112 s per arm (PLAN_EST_S). |

### 6. Finance: amplitude estimation / sampling [differs: The operator has it #3]
| | |
|---|---|
| Run | Amplitude estimation for pricing or risk, end-measured. |
| Before the run | Q2/Q9/Q11 readout, Q3 to Q6 for any noise model, Q17. |
| On the output | Witness/observer split across jobs (Q18). |
| Client today | Record-trusting mitigation, jobs averaged. |
| Ratio | Error bar at equal shots, ours/theirs: **to measure, every cell.** |
| Why they care | Fewer shots for the same confidence. |
| Honest take | No mid-circuit readout, so none of our science bites except the witness/observer split. The readout half overlaps what M3 and TREX already sell. The best market and our weakest edge. I'd show it only after the witness/observer split has its own measured number. |

## Top pick per industry
| Industry | Top pick | Led by |
|---|---|---|
| Error correction | Syndrome rounds, darkwave + Q13/Q14 spacing + fresh table | Science |
| Chemistry | Iterative phase estimation, "bias not noise" | Science |
| Long-range entanglement | GHZ by measurement and feed-forward, Q14 + darkwave + Q1/Q7 | Science + codes |
| Simulation | Trotter with a repaired noise model (Q3 to Q6, Q16) | Codes |
| Optimization | QAOA with crosstalk-aware placement (Q1/Q7, Q17) | Codes |
| Finance | Amplitude estimation + witness/observer | Codes; weakest case |

## My overall top three
1. **Error correction: syndrome rounds.** Our strongest data, the correction is ours outright, and the measured kick residual (0.07 to 0.20) is already a ratio. (Same as the operator.)
2. **Chemistry: iterative phase estimation.** The same asset with a headline a buyer gets in one line: the kick is a bias, shots can't remove it, we do. (Same as the operator.)
3. **Long-range entanglement: GHZ by feed-forward.** [differs] It is the one workload where Q12, Q14 and Q1/Q7 all bite the same circuit. It's IBM's own showcase family. And it shows codes and science together in one table, which is the product.

Finance drops out of my three. It's the biggest market, but our edge there is thinnest until the witness/observer split carries a measured number of its own.

## What a demo has to show before it's a claim
- Arms interleaved in one job, with the seat read first. Tonight's code already does both (opt_demo.py).
- A fresh kick table, age-capped. Marrakesh shows why: the 10-day table overshoots once the kick drifts from −2.39° to −1.68° (P2).
- The middle arm, so the codes' share and the science's share are each on the page.
- Every ratio labelled measured, modelled or to measure. Nothing fires until the owner picks and the referee clears the plan.
