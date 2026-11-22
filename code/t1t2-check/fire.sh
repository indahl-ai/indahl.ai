#!/bin/bash
# 29 Oct, his word "fire away": one job per flagged processor, sequential. Key and instance from local files, never printed.
cd ~/forge/t1t2_check
export IBM_QUANTUM_TOKEN="[...]" IBM_QUANTUM_INSTANCE="[...]"
for b in ibm_boston ibm_kingston ibm_fez; do
  ~/forge/qvenv/bin/python -I run_check.py --backend $b --flagged --yes --out runs/results_$b.json 2>&1 | grep -v WARNING | sed "s/$IBM_QUANTUM_TOKEN/<KEY>/g" > runs/log_$b.txt
done
echo done > runs/DONE
