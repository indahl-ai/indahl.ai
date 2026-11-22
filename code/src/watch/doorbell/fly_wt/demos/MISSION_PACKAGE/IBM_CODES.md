# IBM codes (Q codes), verbatim from the live QIA Key, https://indahl.ai/qia/key (read 19 Nov 2026)

| Code | Name | Definition | Bill QIA-2026-001 line |
|---|---|---|---|
| Q1 | Coupling not predicted | The stated zz coupling does not predict the measured shift of an idle qubit when a neighbour changes state. | 1 |
| Q2 | Readout zero stated | IBM states P(1|0) = 0. The delivered value is above what a zero allows. | 2 |
| Q3 | T1 older than a fresh record | A record stamped the same day carries T1 values measured days or weeks earlier. | 3 |
| Q4 | Value carried for months | A single T1 or T2 value stays in the record for weeks to months without re-measurement. | 4 |
| Q5 | Old values across consecutive records | Records stamped on consecutive days keep the same old T1 and T2 values. | 5 |
| Q6 | Stamp without re-measurement | The record’s calibration stamp moves while T1 and T2 keep their old values and dates. | 6 |
| Q7 | Coupling stated zero on live edges | zz = 0 is stated on edges whose CZ the same record calibrates. | 7 |
| Q8 | Initialisation error missing or stale | init_error is absent or more than seven days old. | 8 |
| Q9 | Readout drift between cycles | Stated readout error moves between calibration cycles hours apart. | 9 |
| Q10 | Stale flags incomplete | IBM flags stale gate errors but not stale readout or initialisation values. | 10 |
| Q11 | Readout error not the average of its parts | readout_error differs from the average of prob_meas0_prep1 and prob_meas1_prep0. | 11 |
| Q12 | Phase kick per readout | A mid-circuit readout turns the phase of untouched neighbouring qubits. No IBM field covers it. | 12 |
| Q13 | Coherence lost next to a readout | Untouched qubits next to a measured one lose coherence per readout. | 13 |
| Q14 | Entanglement lost next to a readout | Untouched Bell pairs lose entanglement per readout. | 14 |
| Q15 | Probe offset | Weak-measurement probe values sit above what the calibration-built noise model predicts. | 15 |
| Q16 | Idle decay not single-exponential | Idle decay departs from a single exponential set by T1. | 16 |
| Q17 | Gate error above stated | Delivered single-qubit (sx) or two-qubit (CZ) error is higher than the error IBM states for the same gate in the record in force. | gate table |
| Q18 | Job-to-job drift | The same circuit, run in jobs minutes apart, returns values that differ by more than shot noise. | indahl.ai runs |
| Q19 | Layout not predicted by the record | The record’s per-qubit figures do not predict which layout delivers the better result. | indahl.ai runs |
| Q20 | Readout below stated (Amazon Braket) | Delivered readout assignment fidelity is below the figure in the Braket device properties. | B1 |
| Q21 | T2 below stated (Amazon Braket) | Delivered T2 is below the figure in the Braket device properties. | B2 |
| Q22 | Fit floor stored as a fidelity (Amazon Braket) | Single-qubit RB fidelity is stored at exactly 0.5, the fully depolarised floor of the fit. | B3 |
| Q23 | Simultaneous above isolated (Amazon Braket) | Simultaneous RB fidelity is stated above isolated RB fidelity on the same qubit. | B4 |
