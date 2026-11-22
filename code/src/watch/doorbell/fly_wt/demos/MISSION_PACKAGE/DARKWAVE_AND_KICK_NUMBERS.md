# Brief v2: the pitch tables rest on OUR findings (the owner, 17 Nov). Supersedes the framing of BRIEF_PITCH_TABLES_20261117.md.

The owner: "Our calibrations are not just for the stale qubits, you need to use our findings. THAT is the big deviation." Brief v1 and DESIGN.md
draft 1 were built on IBM's refresh tutorial alone (H0/H0r). That stays as ONE row family. The headline is what our own work measured and what
IBM's calibration record has no field for. We don't publish anything new in the pitch: it shows outcomes with math that can't be argued with;
the method, the correction tables and their values stay ours.

## What we have, from the record (read these, raw, before designing)
1. THE KICK (paper 1, "A Readout Is Not an Idle", Zenodo 10.5281/zenodo.23169755; the_show/runs/ and arxiv_one_readout/): a mid-circuit readout
   of 39 of 156 qubits turns the phase of the 117 untouched qubits by -1.6 to -2.9 deg per readout (signed; fez -1.62 [-2.08,-1.18], kingston -2.86
   [-3.55,-2.09], marrakesh -2.39 [-3.00,-1.72]), plus a coherence loss (kingston +0.006, marrakesh +0.009 to +0.021; fez cannot tell or consistent with zero) and a Bell-pair
   entanglement loss (fez 0.005-0.007, marrakesh 0.009; kingston cannot tell on clean shots under the committed rule, above zero on all shots). IBM's calibration record has NO FIELD for any of these (bill QIA-2026-001, "effects" section).
2. THE CORRECTION AND HOW LONG IT LASTS (paper 2, "A Readout's Kick Is a Turn", Zenodo 10.5281/zenodo.23843468; ~/forge/the_show/runs/
   2026-10-31-keystone/): a per-qubit virtual Rz from our table gives back, on kingston, 0.92 [0.87,0.95] of the kick from a 10-day-old table
   and 0.93 from a fresh one (nearly equal on the kick; the aging shows in the clock state, 0.76 [0.73,0.78] old vs 1.00 fresh, 99% bootstrap bands); on marrakesh the kick drifted (-2.39 -> -1.68 deg) and the 10-day table overshoots it and only the fresh table gives
   back 0.80 [0.67,0.88], and the marrakesh clock keeps a 0.07-0.08 fidelity deficit in every corrected and echoed arm. Virtual Rz costs no QPU time;
   measuring the table costs ~11 s per chip (job C, 31 Oct logs). Prior art stated honestly: Krinner et al. (Nature 2022) proposed the correction; we
   measured it on IBM Heron and measured how fast the table ages, per chip. The table aging chip by chip IS the reason for a service.
3. THE RECORD ITSELF (bill QIA-2026-001, indahl-ai/qia_template/QIA-2026-001.json): stated zz = 0 on live coupled edges (delivered 2.9 to
   15.4 kHz); stated zz does not predict delivered coupling on kingston (slope <= 0.38; fez 1.00 as a known-good); prob_meas1_prep0 stated 0 on
   14 marrakesh qubits, delivered above what zero allows on 9 to 11; "last calibration" stamp moves while 4,204 of 4,204 T1/T2 entries keep their
   values and dates; entries up to 158 days old with no stale flag; readout_error not the average of its parts on 153 measurements; idle decay
   not single-exponential (62 to 85% below the line vs 49 to 54%). NOT on the bill, Book Part 0 only and weeks old: RB delivered/stated
   kingston sx 1.31-1.37x, CZ 1.30-1.31x (24 Oct), fez CZ 1.24-1.27x (23 Oct); a row only if re-measured today under a plan.
4. PLACEMENT (H0 17 Nov morning, H0r tonight): IBM's own refresh method, marrakesh +0.0509 [+0.0467,+0.0551], fez +0.0046 [+0.0030,+0.0067].

## Rebuttal IBM gets to make (assume they know more)
IBM's researchers have measured readout crosstalk themselves; never imply they don't know. The claim is only that the calibration record users receive has no field for it, and that its size and drift per chip are measured by us, today.

## The tables, redesigned
Table 1, "What the published record leaves out, measured today": one row per finding per processor: IBM's stated figure (or "no field"),
delivered today with interval, outcome (ABOVE/BELOW/CONSISTENT/CANNOT_TELL), job id. The kick row and the correction row lead.
Table 2, "Who is affected, and the offset": rows by workload class, from THE_BOOK's client rows (qia_leads/THE_BOOK.md C1-C45+): mid-circuit
measurement and feed-forward (error-correction syndrome rounds, IBM's own spacetime error detection C27/C28, dynamic-circuit algorithms C43,
teleportation, repeat-until-success); entanglement-carrying protocols (Bell pairs, sampling); anything built on a noise model from the record
(C19 noise-model validation); every placed circuit (transpiler reads the record). Columns: which finding touches it, MEASURED / MODELLED /
UNKNOWN, the offset (correction table at zero QPU time; fresh placement; delivered-vs-stated factors), and its measured give-back.
The referee's bar (BRIEF v1 last section) still governs every cell. Krinner credited where the correction is named.

## TODAY'S FIRE ("so they know we're current")
Repeat the keystone run unchanged on fez, kingston and marrakesh on the comped open instance (key_3 CRN in research/h0r_repeat_test/PLAN.md):
- table A = the committed 21 Oct kicks (now 27 days old); table B = fresh (job C minutes before). Cost from the 31 Oct logs: ~170 s per chip
  (C 11 s + A 77-80 s + B 77-80 s), ~510 s for three; ~10,500 s free. fez was not in the 31 Oct run: it gets fresh-table arms plus its own
  committed 21 Oct table.
- Readings fixed before fire: kick today vs 21 Oct per chip (the record still has no field); give-back of the 27-day table and of the fresh
  table; the four-outcome table and the over-correction case (residual crosses zero) stated before data.
The designer: write research/kick_today/PLAN.md from the_show/runs/2026-10-31-keystone/PLAN_KEYSTONE.md.text and its code, changes listed line by line.
The referee referees the plan BEFORE fire (Q32: no fire while the referee is out). The operator runs CPU tests, fires, analyzes.
Then the designer redrafts DESIGN.md (draft 2) to these two tables, pushed before any of today's results are opened.

## The referee's ruling on v2 (REFEREE_REPLY_V2.md, MOVES) — build to this
Framing holds. Rows: each kick/correction row cites its Zenodo paper labelled preprint, not peer reviewed (procedure public, table values ours);
prior art named in the row; "no field" is a dated claim about the published backend properties, never "IBM doesn't account for it"; every row
carries its own measurement date (October numbers never under "measured today"); every interval names its type. Marrakesh 10-day row states
plainly: the kick drifted (-2.39 -> -1.68) and the old table overshoots. QIA record rows: "carries no age flag", with read date, source and
delivered method each.
kick_today/PLAN.md must contain: unchanged circuits and code with line-by-line changes and hashes; Table A cited by its pre-31 Oct commit;
an uncorrected reference in every job; a coded, tested cap on fresh-table age; job timing and A/B order; give-back, over-correction and
kick-change rules and numeric predictions, all before fire; a known-good reproduction of paper 2 from the 31 Oct raw data; planted kick,
over-correction and zero; the comp disclosed, push witness, job times after the push; no aging-rate claim; DESIGN draft 2 pushed before any
result is opened. No fire before the plan is ruled.
