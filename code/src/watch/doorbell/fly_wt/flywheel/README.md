# FLYWHEEL: one queue, three slots, one PR (the owner's design, 22 Nov 2026)

Replaces waking channels one by one. **the designer's main chat** is the only worker that needs waking, and it watches **one PR: #17 (branch `flywheel`)**.
Every refill is a push to this branch, and a push on PR #17 wakes the main chat. Lane branches stay for the code; the talking happens here.

## The loop
1. `flywheel/SLOTS.json` holds **three slots**. Each slot holds one task: id, title, lane branch, brief, status.
2. The designer (main chat) takes an OPEN slot: sets `status: TAKEN`, commits `FLYWHEEL TAKE S<n> <id>`, pushes. Work happens on the task's lane branch (or from any channel the designer chooses).
3. Done: set `status: DONE`, `done_commit: <sha on the lane branch>`, one line in `result`, commit `FLYWHEEL DONE S<n> <id>`, push. The designer moves straight on to the next OPEN slot.
4. The operator's rider (`watch/doorbell/flywheel_watch.py`, every tick) sees the DONE, rings the operator to review the work, moves the task to `flywheel/DONE.jsonl`, and **refills the slot from `flywheel/BACKLOG.json` on its own** with a push, which wakes the designer again.
5. The operator keeps BACKLOG.json ordered: money path first, then IDEAS.md order. The designer can add to it too (`"from": "designer"`).

## Rings to the operator
- a slot DONE (review it)
- a slot OPEN and not TAKEN within 30 min (the designer asleep)
- a slot TAKEN for more than 6 h with no commit on its lane branch (stuck)
- BACKLOG empty while a slot is free

## Rules kept
Plans before builds; nothing public without the gates; the referee referees what she referees; codes only in notices; the owner sends mail.
A question for the operator goes in the slot's `question` field (pushed); the rider rings the operator, and he answers in `answer` with a push.
The operator cannot read Duet. Everything goes through this branch.
