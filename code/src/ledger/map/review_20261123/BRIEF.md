# House review: efficiency, security, ability to scale (23 Nov 2026)

You are reviewing how Heuremen LLC's operation actually runs: two public sites (indahl.ai and quantumidleaudit.com on Cloudflare Workers), a research index (SAGAR) with codes-only notice emails, live data desks, a QIA quantum calibration mirror, and the machinery that ships, schedules and alarms all of it, mostly from one Mac.

The owner's question: is this efficient, is it secure, and could it scale fast if business took off tomorrow (assume 10x inquiries, 10x papers and desks, and three more people shipping changes)?

## Read these (raw material; nothing here is a conclusion)
- `ledger/map/workflows.json`: every workflow, its trigger, steps, files, outputs and alarm.
- `ledger/map/map.json`: machines, every scheduled job, launch agents, workers, repos, folders, secrets by NAME only.
- `RUNBOOK.md` and `OPERATING_RULES.md`: how the work is supposed to be done.
- The code each workflow names. Check the code, not the documents: where a document and the code disagree, the code is what runs.
  Start with: `ledger/ship.sh`, `ledger/ship_queue.py`, `ledger/ship_qia.sh`, `ledger/save_source.sh`, `watch/desk_bus.py`, `watch/desk_riders.py`,
  `watch/rider_wrap`, `watch/tock.sh`, `lib/outbox.py`, `lib/cf.py`, `sagar/pipeline/sagar_pipe.py`, `indahl-ai/gate.js`, `indahl-ai/inquire.js`,
  `cloudflare-workers/qia-site/worker.js`, `cloudflare-workers/heuremen-door/worker.js`, `tools/offsite_backup.sh`.

## What to return
Up to 25 findings, most severe first, each as:
- **Area:** efficiency / security / scale
- **Finding:** one sentence
- **Where:** file and line
- **Evidence:** what in the code or data shows it; say VERIFIED (you read it) or INFERRED (you reason it)
- **Severity:** high / medium / low, and what breaks or leaks if it is left
- **Fix:** the smallest change that solves it, and how to check the fix worked

Then three short lists: what is already done well (keep it), the three changes that matter most before a launch this Friday, and what to build before growing past one person and one Mac.

Rules: never print a secret value (keychain entries and secret files are named, not opened). Read only; change nothing. Say CANNOT_TELL where the code does not settle a question.
