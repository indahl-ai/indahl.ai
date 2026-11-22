# AIRQ reproduce kit

Heuremen LLC · https://indahl.ai/airq · https://indahl.ai/reproduce

This kit recomputes the AIRQ headline number and its outcome label with the desk’s own code (its scoring lines, copied as written), from what the kit holds, with its network proxies pointed at a closed port.

## The command

```
python3 run.py --check
```

Needs Python 3.9 or later and nothing else. It prints one line of JSON and checks it against expected.json. The line it must print has sha256 `b75016c019c344ca87609c27552c4a4427926f8b1d52d8f465db81ee6445942a`.

## What it reproduces

The headline as the live feed https://indahl.ai/airq/live.json served it at the feed stamp 22 Nov 15:41 UTC, read by us at 2026-11-22T16:03:07Z. The feed bytes had sha256 `4b2d69b57761f800df7b23683f91cdce734dff7f99f5151e41fe201dd73d25cc`.

- number: 53 of 61
- value: 0.8689
- interval: 0.762 to 0.932
- outcome: ABOVE

The live page can move inside the interval between releases. Each move outside it, or a change of label, gets a new row in the indahl.ai ledger, and a release is refused until this kit reproduces the number that row covers. The headline fields are the ones the ledger reads (`kit.json`, headline).

## Inputs

Not included. Its inputs are the AirNow and PurpleAir daily values the live tick read, and a PurpleAir read needs a PurpleAir key. Each input is named with its sha256, so this kit carries no copy of the source data. MANIFEST.json lists each input file the desk’s scoring read, with its size, its sha256 and the time it was last written. Those exact files are kept and this kit is rerun on them before every release.

The input files are what the desk kept from its reads of the sources, with the time of each read where the desk records it. To check them, read the sources below again and compare. With a copy of the input files, `python3 run.py --check --inputs DIR` reruns the kit on them. A file whose sha256 differs from MANIFEST.json is named and the run stops. Sources change, so a later read can differ from ours.

- AirNow real-time hourly files, https://files.airnowtech.org/airnow/YYYY/YYYYMMDD/HourlyData_YYYYMMDDHH.dat, PM2.5 lines of the panel monitors. data/live_days.json (ref) keeps the daily mean of each monitor, from 18 or more hours.
- PurpleAir daily history of the sensor picked for each monitor, https://api.purpleair.com/v1/sensors/ID/history with average=1440. data/live_days.json (sens) keeps the atm and cf_1 channels and humidity of each day. A PurpleAir read needs a PurpleAir key.
- data/pairs.json is the sensor and monitor pairing of the main read (1 March to 30 June 2026), from which the live panel takes the median-RMSE sensor of each monitor.

## Sources and their terms

As the AIRQ data pack lists them. Credit each source when using its values.

- EPA Air Quality System (AQS) API, https://aqs.epa.gov/aqsweb/documents/data_api.html. U.S. government work, public domain (17 U.S.C. 105).
- EPA AirNow, https://www.airnow.gov/. U.S. government work, public domain (17 U.S.C. 105), preliminary data.
- PurpleAir API, https://www.purpleair.com/policies/terms-of-service. PurpleAir terms of service, no redistribution.

## Input files

| File | Bytes | sha256 |
|---|---|---|
| data/pairs.json | 129,089 | `d6a7d46b4db8c67ec78cacebfac6a25935bebdebe2c2f54233a724fb688fb1e8` |
| data/live_days.json | 673,523 | `06577fa0bc7b27c6686cb6b393afa951c3652829b80a0389deab2cad7c42dbc8` |

## Code

The desk’s tick script reads its sources, scores and publishes in one run, so it never runs in a kit. code/airq_live_score.py is the scoring step of that script and nothing else: airq_live_tick.py, the live panel of PLAN.md Addenda 2 and 3: the sensor pick from data/pairs.json, metrics, meets, corrected, ab_ok and outcome as written, and the rolling evaluation over the last 60 UTC days the tick read, which end on the newest AirNow day it kept. The desk files it follows are under desk/, byte for byte, to read beside it. The scripts that run: code/airq_live_score.py. Before every release the gate checks that this extract prints the number the desk published.

## Files

- kit.json: the steps, the output file and the headline fields.
- run.py: the command.
- expected.json and expected.sha256: the line run.py must print.
- published.json: the headline as the live feed served it when this kit was made.
- MANIFEST.json: every input and code file with its sha256.
- desk/: the desk scripts the extract follows, where the kit runs an extract.
- SHA256SUMS.txt: the sha256 of every file in this folder.
