
## 2026-11-17 14:18 qia.corp.ibm_qaoa_tutorial outcome corrected CONSISTENT -> BELOW: hardware 0.2860 [0.2772, 0.2950] vs forecast 0.3301
packs: Q,P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: comparison is the committed 23 Oct forecast from IBM's record for the same job vs that job's hardware count; nothing re-built today
- II: holds: single figure (P optimal cut), no netting; the interval is the binomial width of one run, stated as one run
- III: holds: signed, hardware 0.286 below forecast 0.330; one cell, no fold
- V: holds: ruler is the 95% binomial interval on hardware vs the Aer forecast (+-0.0021); both printed in the results file
- VI: fixed: interval [0.2772, 0.2950] excludes 0.3301 -> BELOW; the CONSISTENT label had no basis in the file; BELOW is the only outcome the file supports
- R: holds: numbers read from arxiv_one_readout/industry_run/results_tqaoa_ibm_kingston.text line 'hardware 0.2860 [0.2772, 0.2950] vs forecast 0.3301'; no new data
- QA: holds: forecast is IBM's own tutorial path (Aer from the backend record); record unchanged during the run per the results file
- QB: n/a: no idle arm in this reading; it is a forecast-vs-hardware comparison
- QC: n/a: label correction only; no new instrument; the run's own checks stand as committed 23 Oct
- QD: holds: four-outcome rule applied to one interval; one chip, one run, said so
- QE: holds: no mechanism named; the Q17 calibration text already says forecast with delivered error, not a cause
- QF: holds: run date 23 Oct from the job record in industry_run; correction dated 17 Nov
- QG: holds: caught by a neutral comparison of two independent inventories (COMPARISON.md) against the raw file
- P1: n/a: no quotes changed
- P2: holds: figure lives in results_tqaoa_ibm_kingston.text; public table already prints 0.330 and 0.286 [0.277, 0.295]
- P3: holds: no setting label changed
- P4: holds: no cause named
- P5: holds: public text says 95% binomial interval
- P6: holds: the public table shows numbers only, no outcome word; this fixes the internal ledger field only
- P7: holds: ledger edited first via ledger.py set; no surface text changes, so no ship needed
- P8: holds: rendered corporate.html and the study page read 17 Nov 19:18Z: numbers only, no CONSISTENT shown
- P9: holds: no copy written
- P10: n/a: not post hoc; the hardware reading was planned 23 Oct
