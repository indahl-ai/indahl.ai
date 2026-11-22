# Mission package: match each industry's run to our best calibration (the owner, 19 Nov 2026)

For the operator, the referee and the designer. Each of us works separately and blind. No IBM, no code. Plain English.

## The task
For each industry, take the run that industry actually needs. Ask what it needs to come out right: phase kept through mid-circuit readouts, accurate readout, fresh coherence figures, stable results job to job, correct coupling, and so on. Then match it to the BEST calibration we have. That's either:
- **OUR SCIENCE:**
  - the darkwave correction (internal name; in public use the paper's language, "A Readout's Kick Is a Turn");
  - the kick itself (Q12);
  - what a readout costs its neighbors (Q13 coherence, Q14 entanglement);
  - the probe offset (Q15) and non-single-exponential idle decay (Q16);
  - the witness/observer separation (internal only): splitting the shared drift from the actual signal.

  Or:
- **OUR ACCOUNTED-FOR ERRORS:** the IBM codes, which are errors IBM's record misstates, carries stale or doesn't cover, and which we correct for BEFORE the run:
  - Q1-Q11: coupling, readout, staleness and init;
  - Q17-Q19: gates above stated, job-to-job drift, layout not predicted.

Combinations are expected. The goal: the client's end-of-run error comes out significantly lower than with what they accept today, shown as a ratio, ours vs theirs. That ratio is what saves them money and improves performance.

## What's in here
- **MISSION_BRIEF.md:** the full brief (what went wrong, the mission, everything we have, the questions per industry).
- **IBM_CODES.md:** all 23 Q codes, verbatim from the live QIA Key, with their bill lines.
- **BILL_QIA-2026-001.json:** the bill, with every measured number, chip, date and IBM doc quote for Q1-Q16.
- **DARKWAVE_AND_KICK_NUMBERS.md:** both papers' numbers (kick sizes per chip; give-back 0.80-0.93; table aging; cost), with sources.
- **Elsewhere on disk:**
  - qia_leads/THE_BOOK.md (client rows C1-C45+);
  - the_show/runs/2026-10-31-keystone/ (paper 2 runs);
  - optimization/run/ (tonight's P table and check run, within-job floor ~0.0009).

## What each of us returns
A file in the parent folder, FIRST_PASS_<NAME>.md. For each industry:
1. the run;
2. what it needs;
3. our best calibration match (science, accounted-for errors or both), split into before the run vs on the output;
4. the client's run today;
5. the end-of-run error ratio, measured or "to measure";
6. why they care;
7. what's on disk, and the smallest run that shows it.

Then a top pick per industry and an overall top three. The operator lays the three passes side by side for the owner.
