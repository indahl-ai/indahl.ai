# Field run: the indahl.ai worker, cleaned for public release

**Job.** The worker that serves indahl.ai also carried routing for sites retired in an earlier lockdown, with a private address and private names in it, so it could not be published. Cloudflare's own API showed those hosts already redirect elsewhere, so that code could never run. The job: remove it, prove nothing a visitor sees changed, deploy, and publish the worker.

**Tools used.** indahl-rubicon (criteria frozen before the work), indahl-relay (the deploy as a chain of stages), indahl-ccr (approval bound to the exact bytes, compared at release).

## What happened

| step | result |
|---|---|
| Criteria frozen (`.rubicon/frozen.json`) | 4 criteria, each with a planted wrong answer, sha256 e59470173d75 |
| Parity, old worker against cleaned worker, locally | 5,363 URLs including MCP calls, 0 mismatches. Control (old against old): 0. Planted break on /contact: caught |
| Privacy scan | 0 hits on the cleaned worker. A planted copy with a private address: caught |
| Chain (`chain.json`, `chain.relay/`) | 9 stages: 7 done, 2 failed (below) |
| CCR release | SAME for worker.js and wrangler.toml: the approved bytes are the shipped bytes |
| Public worker | `code/worker/` in this repo, identical to the deployed file (sha256 9a78f315…) |

## The two failed stages

- **compare: 107 URLs differed after the deploy, beyond the floor stated before it.** None changed status, redirect or type, only body bytes. The cause was our test design: the floor was measured with no release between snapshots, but the deploy goes through the release pipeline, which also rebuilds the pages. Decided by running the old and new worker on the same current pages: 5,363 URLs, 0 mismatches (`parity_oldsrc_vs_deployed_samepages.json`). The worker change altered nothing a visitor sees, and the 107 differences were the rebuild.
- **gate: one release receipt missing from the public repo.** The pipeline writes that receipt after its own public push, so the check, run later, found the newest one missing. The gate now names such a receipt and leaves it for the next release.

## Files

`CRITERIA_public.md` (redacted copy of the frozen criteria), `scan_house.py` (its word list is private), and `clean_worker.py` is not published because its cut points quote the private source. Also, `parity.py`, `snap.py`, `compare_floor.py`, `chain.json` with each stage's log, and every parity and snapshot result as JSON.
