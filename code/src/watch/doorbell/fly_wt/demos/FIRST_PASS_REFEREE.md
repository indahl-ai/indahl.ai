# First pass: The referee (19 Nov 2026), blind to the operator and the designer (verbatim from her reply)

the owner, here's my blind first pass. First, the one rule I scored by: **"the client's run today" includes whatever error-fixing they'd already switch on** (TREX, M3, PEA). If we only beat a raw run, we're selling them their own free tools. So our real wins come from three places:
1. **Things IBM has no field for.** Mainly the readout kick (Q12–Q14), which only matters when something is measured *mid-run* while its neighbours keep working.
2. **Picking qubits from fresh data before the run** (Q19, Q9, the stale entries Q3–Q10). Every IBM tool picks from the record.
3. **Knowing the true gate error** (Q17) when you choose a circuit's depth.

Every ratio below is marked **measured** or **estimate**. Where the honest answer is "small," I say so.

---

## Dynamic circuits / error correction: our strongest ground

| | |
|---|---|
| **The run** | Repeated parity checks: a small error-correcting code, or the simplest phase-sensitive repetition code, run for 5–20 rounds. Every round, helper qubits are read out while the data qubits beside them wait. |
| **Ours** | **Before:** the kick table from an 11 s calibration job; qubits picked from fresh readout plus our intermittent-qubit watch (Q9). **During:** a free vir

tual turn on each data qubit after each readout (darkwave), costing zero QPU time. |
| **Client today** | IBM defaults plus the tutorial's dynamical decoupling. Nothing in IBM's stack knows about the kick, so it lands as unexplained "noise" every round. |
| **End-of-run error** | **Measured:** the correction gives back 0.92 [0.87, 0.95] of the kick on kingston, and 0.80 on marrakesh after the kick drifted. **Estimate:** about 2° per neighbour readout, 2 neighbours, 10 rounds is a ~40° drift, which costs about 23% on a phase-sensitive result. Correct 92% of it and roughly 2% is left. **Not measured:** whether IBM's default decoupling already cancels part of the kick, and whether two neighbour kicks simply add. Both decide whether this is "10x" or "nothing." |
| **Why they care** | The kick piles up every round, so it limits how long their code can run. That's the whole game in error correction. |
| **On disk** | Both papers and the keystone runs. **Smallest run:** a 3–5 data-qubit code, 10 rounds, table on vs off, both with the client's decoupling, plus one tiny job checking the kick survives decoupling. |
| **Pick** | **Yes, top pick.** |

**Plain English:** this is the one place where we fix something nobody else even names. The risk is equally plain: if IBM's default decoupling already eats the kick, we learn that from a 10-second job before spending anything else, and it becomes a published "default already handles it."

## "Other": long-range entanglement by measure-and-feed-forward (my surprise pick)

| | |
|---|---|
| **The run** | IBM's own flagship dynamic-circuit trick: building GHZ states or long-range CNOTs in constant depth by measuring middle qubits and correcting on the fly. Also teleportation. |
| **Ours** | The darkwave table on the qubits holding the entanglement, plus Q14 (entanglement lost next to a readout) used to choose which qubits sit beside th

e readouts. |
| **Client today** | The tutorial as written. |
| **End-of-run error** | **Measured:** readout next to an entangled pair cost 0.25 of pair fidelity on kingston (I need to recheck exactly what that 0.25 is against). **Not measured:** in this circuit. |
| **Why they care** | It's a single clean number (GHZ fidelity) on IBM's own showcase. The kick lands exactly on the qubits that carry the answer. |
| **Smallest run** | 5–9 qubit GHZ via mid-circuit measurement, table on vs off. |
| **Pick** | **Yes.** It may beat QEC as the *first* demo, because it's shorter, cheaper and easier to explain. |

## Chemistry / materials

| | |
|---|---|
| **The run** | Today's mainstream IBM chemistry is **sample-based diagonalization (SQD)**, which measures only at the end. The darkwave-friendly one is **iterative phase estimation**, which reads a helper qubit every round while the molecule register waits. |
| **Ours** | **SQD:** pick qubits from fresh readout and today's real gate error, and drop anything on the intermittent watch (Q9, Q17, Q19, stale entries). SQD often runs *without* readout correction, because flipped bits feed its recovery step, so fresh qubit choice matters more there than for a TREX user. **Phase estimation:** darkwave on the system register every round. |
| **Client today** | SQD tutorial defaults, with layout picked from the record. |
| **End-of-run error** | **Measured, nearby:** fresh-data layout beat the record's choice by +0.029 (fez) and +0.049 (marrakesh) on our own test. **It did not repeat on kingston,** and the gain shifted day to day. **Not measured:** on a chemistry energy. |
| **Why they care** | Fewer bad bitstrings means fewer samples to reach chemical accuracy. That's shots and money. |
| **Pick** | SQD with fresh qubit choice for **reach** (it's what clients actually run). Phase estimation as the **future-facing** darkwave demo. Med

ium strength. |

## Optimization / logistics

| | |
|---|---|
| **The run** | QAOA. |
| **Ours** | Fresh qubit choice (Q19, Q9); darkwave only if they use qubit reuse (measure, reset, reuse to fit a bigger problem). |
| **Client today** | Tutorial QAOA, layout from the record. |
| **End-of-run error** | **Measured tonight:** fresh data flagged 5 qubits the record missed. But on a problem graph shaped like the chip, moving off them cost 458 two-qubit gates against 222. **The fix can be worse than the disease.** Gains are only plausible on non-native graphs that need routing anyway. |
| **Pick** | **Weak.** A useful "your record is wrong about 5 of your qubits" health report, not a lower-error headline. Qubit-reuse QAOA is the only darkwave angle, and it's niche. |

## Simulation / physics

| | |
|---|---|
| **The run** | **Mainstream:** Trotter dynamics with Estimator plus ZNE/PEA. **Research niche:** monitored circuits (measurement-induced phase transitions), where mid-circuit readouts happen everywhere. |
| **Ours** | **Mainstream:** fresh qubit choice; maybe Q16 (idle decay isn't one exponential), which could bend ZNE's extrapolation. That's speculative and unmeasured. **Monitored circuits:** darkwave, heavily. |
| **Client today** | PEA learns layer noise in session, so stale readout figures hardly hurt them. Twirled layer models don't capture a kick from a mid-circuit readout. |
| **Pick** | **Weak for mainstream** (their tools already absorb most of what we'd fix). **Strong but small market for monitored circuits.** Academic buyers, a great paper, not a big invoice. |

## Finance

| | |
|---|---|
| **The run** | Amplitude estimation (pricing, risk) and portfolio QAOA. Both measure at the end. |
| **Ours** | Fresh qubit choice, plus Q17: true gate error decides how deep an amplitude-estimation circuit can go before the answer is noise. |
| **Client today** | Estim

ator with TREX. |
| **Pick** | **No strong case. I'd say so on the page.** The kick doesn't apply, and readout mean errors are already handled. The only honest pitch is "we tell you the real depth budget before you burn shots," and that needs a measured Q17 gap on their circuit first. |

## Across every industry: a pre-run health check

This isn't per industry, but it might be the easiest thing to sell. **Measured:** our hourly runs caught fez q155's bad-readout episode **1–3 hours before IBM's own refresh did**, and marrakesh's too. Records carry entries days to weeks old under a fresh stamp (Q3–Q10). A "before you submit, here's which qubits are lying today" check applies to every workload, costs about 11 s, and needs no demo circuit at all.

---

## My overall top three

1. **Long-range entanglement via dynamic circuits (GHZ / teleportation) with darkwave.** It's IBM's own showcase, the kick hits the qubits that hold the answer, and it gives one clean number.
2. **Error-correction rounds with darkwave.** It's the biggest payoff because the kick compounds, and the longest-lived market.
3. **The fresh-calibration pre-run check, shown on chemistry SQD.** Broadest reach, smaller per-run gain, honestly mixed across chips.

**What I'd say plainly to the owner:**
- **Witness/observer separation:** I can't attach a number to it yet. Until it has a written definition of what it does to a run's output and one measured run, it stays out of every ratio.
- **The kick's survival under default decoupling** is the single question that decides picks 1 and 2. It's the first thing I'd measure, at about 11 seconds.

