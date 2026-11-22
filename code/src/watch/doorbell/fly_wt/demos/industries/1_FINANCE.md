# Industry 1 of 5: Finance (one industry at a time, the owner 19 Nov)

## The client's run
Option pricing and risk (VaR / CVaR) by quantum amplitude estimation: the iterative or maximum-likelihood kind, run on Sampler. A ladder of circuits with 0, 1, 2 ... k Grover steps. The answer is a probability read off ONE objective qubit, fitted across the ladder. The client checks the price against Black-Scholes.

## The operator's plan: specific calibrations that land on THIS run
1. **True gate error sets the ladder (Q17).** Real two-qubit error is 1.30x stated on kingston and 1.24-1.27x on fez (our RB, 23-24 Oct, measured). The client sizes the ladder from the stated figures, so their deepest rungs are mostly noise and the fit gets dragged by them. We pick the ladder's top rung from the TRUE error and drop the dead rungs.
   - From disk: at a planned fidelity of 0.5, the chip delivers 0.41-0.42.
   - Shots for the same precision scale as 1/F², so the client spends 1.42-1.52x the shots they budgeted (computed by the referee from our measured ratio).
   - Ours: the budget matches the chip, so that 1.42-1.52x comes back.
2. **The noise term inside the fit uses our measured decay (Q16 + Q17).** Maximum-likelihood amplitude estimation models how the signal fades with depth. IBM's figures assume single-exponential decay at the stated rate. Ours: 62-85% of points sit below the single exponential (Q16, measured), at 1.3x the stated gate error.
   - A wrong fade model biases the PRICE itself, not just its error bar.
   - Ours puts the measured fade in the fit, and the price bias shrinks. Size: to measure, by simulating from our decay data on disk.
3. **The objective qubit sits on readout that isn't lying today (Q2, Q9, Q11 + health check).**
   - The answer is P(1) on one qubit, so a readout error on that qubit IS a price error.
   - Our hourly runs caught fez q155: the record said P(1|0) 0.982, we measured 0.013, and IBM's own refresh came 1-3 h later.
   - Q9: readout moves 16-62% between cycles hours apart.
   - Ours: the pre-run check (about 11 s) puts the objective qubit on verified-good readout, and the run is corrected with today's measured readout, not the record's.
   - (Sampler users don't get TREX; that's Estimator only.)
4. **The ladder in one job, drift split from signal (Q18 + witness/observer, internal).** Clients run the rungs in separate jobs. Q18 says jobs drift by more than shot noise, and the fit reads that drift as signal.
   - Ours: all rungs interleaved in one job, with our seat measuring the shared drift (tonight's within-job floor, 0.0009) and taking it out.
   - Size: to measure.

## What the client sees
The price error vs Black-Scholes at equal shots, ours / theirs, plus shots to reach a target error, ours / theirs.
- From disk: 1.42-1.52x fewer shots, from #1 alone.
- #2 to #4: to measure.
- Smallest run: one P/health-check job (~11-30 s, including a fresh RB pair), then a 3-qubit option-pricing ladder, both arms interleaved in one job.

## Evaluation of the other two plans (the operator rating)
- **The referee (§5, "the price of depth"):**
  - Strong and specific, with a real multiplier from our own RB (1.42-1.52x shots).
  - But she calls it "a cost forecast, not lower error." That undersells it: the same true-error knowledge sets the ladder and the fit, so it lowers the price error too. She left out #2, #3 and #4.
  - Scores: A 4, B 4, C 5, D 4, E 5, F 5, G 4.
- **The designer (§6):**
  - The right list of codes (readout, staleness, Q17, witness/observer).
  - But he defers the whole industry until witness/observer has a number, and misses the depth-budget win the referee found.
  - Scores: A 2, B 1, C 3, D 4, E 3, F 3, G 4.

## Top pick for Finance
Amplitude-estimation option pricing with the TRUE-error ladder (Q17 measured) and the health-checked objective qubit, against the client's stated-error ladder. Headline: the same price accuracy for about two-thirds of the shots, with a smaller price bias still to measure.

## The referee's round (verbatim, 19 Nov)
## (a) Finance, refined

**The client's run:** option pricing or VaR by maximum-likelihood amplitude estimation on Sampler. It's a ladder of Grover depths, and the answer is P(1) on one qubit. Measurement happens only at the end, so **the kick doesn't apply, and the page says so.**

**Correcting myself, and the operator on one point.** Knowing the true gate error doesn't make the chip any better. The 1.42–1.52x is **the client's budget miss**: what they lose by trusting the stated figures. It isn't shots we give back. What our knowledge actually changes is threefold:

| What we do | Applies how | Number |
|---|---|---|
| **1. A fresh RB pair sets the fade model (Q17).** | Default MLAE fits the ladder as if it had no noise. Noise pulls each rung's P(1) toward ½, and that **biases the price itself.** With a measured fade rate in the fit, that bias shrinks. | **To compute, zero QPU:** an offline simulation from our measured 1.24–1.30x, running now (BUILD below). |
| **2. We drop the dead rungs and reallocate shots.** | Information per s

hot falls as F². At true error 1.3x stated, a rung planned at F=0.5 delivers 0.41, and a rung planned at 0.3 delivers 0.21. | **[D]** Those rungs cost **1.5x (planned 0.5) to 2.1x (planned 0.3)** the shots they were budgeted on kingston, and 1.4–1.8x on fez. How much reallocation recovers is part of the same simulation. |
| **3. The objective qubit goes on readout checked today (Q2, Q9, Q11).** | Sampler has no TREX. A 1% readout error on that one qubit is about a 1% probability error, straight into the price. | **[M]** One case: fez q155, where the record and reality disagreed by 0.97, with our hourly read 1–3 h ahead of IBM's refresh. A client using M3 already corrects the mean, so ours is only the **qubit choice**. It's small. |

What I'm leaving out:
- **Q16:** it's idle decay, and AE is gate-bound.
- **The kick:** there's no mid-circuit readout here.
- **Witness/observer:** there's no definition yet.
- **The operator's #4:** the 0.0009 floor came from a different circuit and an observable that isn't a price.

**What the client sees:** price error against Black-Scholes at equal shots, ours vs theirs. The number comes from the simulation first, then from one small run: a fresh RB pair (about 30 s), then a 3-qubit pricing ladder with both arms interleaved in one job.

## (b) Ratings

**The operator**

| | Score | Why |
|---|---|---|
| A | 3 | The headline 1.52x is the client's miss, not our win. The real win, the price bias, is unmeasured. |
| B | 3 | Q17 is measured but nearly a month old. Items #2–#4 are still to measure. |
| C | 4 | Q17 and the fade model are ours. The readout part partly overlaps M3. |
| D | 5 | Amplitude-estimation pricing is the finance run. |
| E | 4 | An offline simulation plus about 30 s plus a small ladder. |
| F | 4 | Price error against Black-Scholes is clean. |
| G | 2 | "Shots come back" points the wrong way. It uses Q16 (idle) as a gate fade. #4 bo

rrows a floor from another circuit. |

**The designer**

| | Score | Why |
|---|---|---|
| A | 1 | No number anywhere. |
| B | 1 | Nothing on disk. |
| C | 2 | He's right that readout is M3's job. His one "ours" item is undefined. |
| D | 4 | The right run. |
| E | 2 | Gated on a method with no measured run. |
| F | 3 | The error bar is clear enough. |
| G | 4 | He's honest that nothing mid-circuit bites. But he misses that a noiseless fit plus true error gives us a real lever. |

## (c) Top pick

Amplitude-estimation option pricing, with a fresh RB pair setting both the ladder's depth and a fade term in the fit, scored as price error against Black-Scholes at equal shots. The number comes offline first, and the QPU only touches it if the simulation shows a gap worth buying.

BUILD: Offline MLAE bias simulation, numpy/scipy only, no qiskit, no network. Model: European-call amplitude a=sin²θ with θ swept over [0.2, 1.2] rad. Rung k gives p_k = 1/2 + F_k·(sin²((2k+1)θ) − 1/2), with F_k = (1−e)^(g·(2k+1)), g = 2-qubit gates per Grover step swept over {20, 40, 80}, e_stated swept over {0.002, 0.003, 0.005}, and e_true = r·e_stated with r ∈ {1.24, 1.30}. Ladder k = 0..K, with K chosen where the planned F (using e_stated) stays ≥ 0.3. Arms at equal total shots (sweep 2k, 8k, 32k): (T) the client's default, standard MLAE likelihood with no fade term, ladder from e_stated; (O) ours, MLAE likelihood with the fade term at e_true and top rung re-chosen at true F ≥ 0.3, plus (O2) the same with shots per rung proportional to (2k+1)²F_k². Report the bias and RMSE of the estimated a (and of θ) over 2,000 seeded draws per cell, the ratio RMSE_T/RMSE_O, and shots for O to match T's RMSE. Also run a control cell with r=1.0 where O must not beat T beyond noise. Write the results table and code to the drafts folder, with seeds printed. Stop at the cap and report what's done.


## The designer's round (19 Nov). My earlier Finance call ("codes only, not a lead demo") is withdrawn.

The codes ARE the product, and Finance is where they show most plainly. Every number the client gets is P(1) on one qubit, read at the end, fitted across a ladder the client sized from IBM's record. So each record figure the run leans on is a place the price can go wrong. The demo shows each code clearing its deviation on the page, and the price each arm gives against Black-Scholes.

### (a) The codes that clear deviations on THIS run, before the run

| Code | Deviation on this run | What we do before the run | Number now (label) |
|---|---|---|---|
| **Q2 / Q9 / Q10 / Q11: objective-qubit readout** | The price IS P(1) on one qubit. A correction built from the record carries the record's error straight into the price. Sampler has no TREX. | An 11 s check puts the objective qubit on readout measured today, and corrects with today's numbers. | **Computed from disk** (P2 kingston readout table, 17 Nov; record-built correction vs today's): <br>- kingston q15 (stated P(1\|0) 0.0020, delivered 0.0643): **price bias +0.054 at a true probability of 0.10** (a deep out-of-the-money option priced 54 % high), +0.035 at 0.30 → about 0 with today's numbers. <br>- kingston q1: −0.005 to −0.015. <br>- fez q155 (record 0.982, delivered 0.012): a record-built correction **returns −145 for a true 0.10**. The price is destroyed by one stale record line (P2 CHECKS QC; stated P(0\|1) 0.012 is read off the record's readout_error 0.497). |
| **Q17: gate error above stated** | The client sizes the ladder and assumes no fade from the stated figures. Real CZ error is 1.24-1.37x stated (RB 23-24 Oct, measured; weeks old). | A fresh RB pair (about 30 s) sets the top rung and puts the measured fade term in the likelihood. | Rungs planned at F 0.5 and 0.3 deliver 0.41 and 0.21: **1.5x-2.1x the shots budgeted** (kingston), 1.4-1.8x (fez) (computed, the referee). The price-bias size is in the referee's offline sim, running now. |
| **Q1 / Q7: coupling on the oracle's edges** | zz is stated 0 on live CZ edges, while delivered is 2.9-15.4 kHz (bill line 7), and stated zz doesn't predict delivered (kingston slope ≤ 0.38, bill line 1). Coherent ZZ turns θ itself, so it moves the price rather than fading it toward ½. | We place the oracle on edges whose zz we measured, or put the measured zz in the fade model. | Size: add a coherent-phase term to the referee's sim (zero QPU). |
| **Q3-Q6 / Q8: stale T1, T2, init** | Any noise model or layout from the record leans on entries up to 97 days old under a fresh stamp (bill lines 3-6), and init up to 84 days old with no flag (bill lines 8, 10). | We picked from today's values. | Carried in the health check; a client-visible line on the ledger. |
| **Q18: job-to-job drift** | Clients run rungs in separate jobs, so the fit reads drift as signal. | All rungs interleaved in one job, with the seat run ON THE LADDER itself (the referee is right that tonight's 0.0009 was another circuit). | Seat on the ladder: measured in the same small run. |

### What the client sees
A ledger and a price:
- **The ledger:** per code, the record's figure on the qubits and edges this price runs on, today's figure, and cleared or not.
- **The price:** three arms in one job:
  1. the client's (record ladder, record readout, no fade);
  2. + our readout and layout codes;
  3. + the Q17 ladder and fade.
- **The scores:** price error vs Black-Scholes at equal shots, and shots to a target error, for each arm. The codes' shares show one by one.

**From disk now:** a readout bias of up to 0.054 on the price from one mislabelled qubit, and a stale line that destroys a record-built price outright.

**From the offline sim (no QPU):** the fade and coupling bias.

**Smallest run:** an 11 s check + a 30 s RB pair + a 3-qubit pricing ladder with the arms interleaved and the seat. Doesn't fire without the owner.

### (b) Ratings

**The operator**

| | Score | Why |
|---|---|---|
| A | 4 | Four codes land on this exact run. The price bias is the real win, and it's coming. |
| B | 3 | Q17 is measured but weeks old. The readout cases are on disk (q155, and the P2 kingston table). |
| C | 5 | The ladder from true error, the fade term and the health-checked objective qubit are all codes, not M3. |
| D | 5 | MLAE pricing on Sampler is the finance run. |
| E | 4 | One small job after a check and an RB pair. |
| F | 5 | Price vs Black-Scholes and shots to target: a banker reads both in a second. |
| G | 3 | the referee's three points stand: show 1.42-1.52x as arm vs arm, use a gate fade (not Q16 idle), and run the seat on the ladder. All are fixable in the plan. |

**The referee**

| | Score | Why |
|---|---|---|
| A | 4 | The fade term in the likelihood is a real price lever, and the dead-rung shot cost is computed. |
| B | 3 | Q17 is measured but weeks old. The sim is running. |
| C | 4 | Q17 and the fade are ours. |
| D | 5 | The right run. |
| E | 5 | Offline first, zero QPU until there's a gap worth buying. |
| F | 4 | Price vs Black-Scholes. |
| G | 5 | It has an r = 1.0 control cell where ours must not win. |
| Take | | "Readout is small, only qubit choice" undersells it. On the P2 kingston table, one qubit's record readout puts +0.054 on a 0.10 price, and q155's record line returns −145. The choice is the price. |

### (c) Top pick for Finance
MLAE option pricing with three codes cleared on the page before the run:
- Q2/Q9/Q10/Q11: the objective qubit on today's readout;
- Q17: a true-error ladder plus a fade term;
- Q1/Q7: the oracle on measured-coupling edges.

The arms are interleaved in one job, with the seat on the ladder. The headline is the price error vs Black-Scholes, each code's share shown. It leads my codes-side demos.
