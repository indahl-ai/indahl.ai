# How the operator and the designer work together (indahl-ai/calibrations, private)

Written 20 Nov 2026 on the owner's order ("we really gotta nail down communications"). This file is the path. If it and a chat message disagree, the owner's latest word wins and this file gets fixed the same day.

## Who does what
- **the owner** decides. Anything sent to anyone, anything shipped, any spend and any new account is his word.
- **The operator** runs things: machines, runs, the record, the site pipeline, the referee. The operator answers a ball before starting anything else.
- **The designer** designs and writes: tools, pages, copy, research. The designer builds; the operator runs what the designer builds.
- **The referee** referees. The operator carries questions to the referee and brings rulings back as balls.

## The lanes
One lane is one branch plus one PR. The PR is the doorbell.

| Channel | Branch | Doorbell | What it is for | State |
|---|---|---|---|---|
| front door | `lane-door` | PR #6 | New lanes, anything urgent, anything with no lane, a blocked channel | open |
| demos | `lane` | PR #1 | Industry demo runs and results | open |
| sagar | `lane-sagar` | PR #2 | SAGAR indexing, the one-pass tool, the Gaia lane | open |
| biz | `lane-biz` | PR #3 | Decks, leads, the 27 Nov pitch pack (Card #1 = LTM) | open, LIVE (the owner restarted it 22 Nov) |
| site | `lane-site` | PR #4 | Site pages, style, SEO copy (indahl.ai and quantumidleaudit.com) | open, LIVE |
| pod | `lane-pod` | PR #5 | POD desk: tools, research, page | open, LIVE |
| build | `lane-build` | PR #7 | Standing lane: any tool or code job with no lane of its own | open, spare |
| research | `lane-research` | PR #8 | Standing lane: any reading-only job with no lane of its own | open, spare |

**LIVE** means machines are rented or a deadline is running on that lane. The operator sets and clears it here.
Who holds the ball on each lane right now: `lanes/BOARD.md` (the operator regenerates it from the PRs with `lanes/board.py`).

## A ball
A ball is one PR comment. One topic per ball. Its first line starts with the words below, exactly, so both sides can find it.

**The operator to the designer**
```
Ball to the designer: <the job in one line>
Priority: URGENT | today | when free
Job: what to make or find out
Files: where it goes (branch and paths)
Done means: how both of us will know it is finished
Ring me when: the first useful point, not only the end
```

**The designer to the operator**
```
Ball to the operator: <what happened in one line>
Status: got it | done | blocked | question
Commit: the commit, if there is one
What I need: nothing, or the one thing that unblocks me
```

## Acknowledge every ball
- **The designer answers every ball with a "got it" ball** (Status: got it, the channel, a rough time) the first time he sees it. Silence is not a yes.
- **The operator answers every ball** before starting anything else, even if the answer is "seen, running it at <time>".
- A ball that is finished gets a "done" ball with the commit. Work that is pushed but not rung is not delivered.

## How fast
| Who | Watches | How often |
|---|---|---|
| the operator | every doorbell in the table | every minute while a session is up; at the start of every session otherwise |
| the designer, a lane's own channel | its own PR | as it works |
| the designer, main chat | PR #6, the front door | every 15 minutes while any lane is LIVE; every hour otherwise |

- **URGENT** means one of: money is burning on rented machines, something public is wrong, a channel is blocked, or work is waiting on one answer. The operator uses it sparingly.
- **Overnight:** the designer still makes channels and works. He pings the owner only for a ball marked URGENT.
- **No acknowledgement:** if a ball to the designer has no "got it" after 20 minutes on a LIVE lane (75 minutes otherwise), the operator rings the front door with an URGENT ball naming it, and tells the owner in his next message. If a ball to the operator has no answer after 10 minutes while the operator is up, the designer rings the front door.

## New work, without waiting for anyone
1. If the work fits an open lane, the operator rings that lane.
2. If it does not, the operator rings **build** (tools, code) or **research** (reading). Those two channels exist so that new work never waits for a new channel or a click.
3. If the work is big enough for its own lane, the operator opens the branch and PR, adds the row above, and rings the front door: "Ball to the designer: new lane", with the branch, the PR and the first job. The designer's main chat makes the channel and tells the owner in one line.
4. **The repository.** A new channel may not be able to reach this repository until the owner attaches it with push access (repository `indahl-ai/calibrations`, the lane's branch). Until he has, the designer does that lane's work from **build** or **research**, which already have it, and rings "Ball to the operator: channel blocked" on the front door once. Nobody waits.

## Handing work back and forth
- **The designer builds on the lane's branch and pushes.** the operator pulls, runs it, and reports the result as a ball on the same lane, with the numbers and the commit he ran.
- **Frozen files are never edited** (plans, addenda, code tables, hashed tools). A change is a new dated file, and the operator takes it to the referee.
- **The referee's rulings reach the designer as a ball** that says what changes for his tools, not as the ruling pasted whole.
- **The operator does not rewrite the designer's work and the designer does not rewrite the operator's.** Each reviews the other's and rings with what is wrong. If one has to build the other's piece because of time (as with the POD harness on 20 Nov), he says so in a ball and the owner reviews it first thing.

## Rules on every lane
- Nothing is sent to anyone and nothing ships without the owner's word.
- No sign-ups, accounts, keys or spend from a lane. Research is reading.
- Quotes are whole sentences, word for word, with the page and the date read.
- No predicted numbers in a plan, a page or a tool.
- American spelling. No count of our own things in a title or heading.
- **The specbook is the standard for anything a stranger sees** (pages, footers, mail, bills, the mark): `specbook/` on `lane-door`, start with `specbook/README_FOR_DESIGNER.md`. The book wins. Only the owner amends it.

## Pace (the owner, 21 Nov 2026)
- **New desk ideas go on one list,** `~/forge/IDEAS.md`, in order. At most two desks build at once. The ship rebuild holds both slots until it lands, then SELDON, then ARES. Nothing builds from a chat message alone.
- **Ships are bundled once an hour** (`ledger/ship_queue.py`). A request whose label starts with `MONEY:` or `URGENT:` ships at once. Money-path work never waits on the idea list.

## Acks are watched (22 Nov 2026, the owner: "Hard Lockdown Full Comms")
- `watch/doorbell/ack_watch.py` rides the tick on the operator's seat. A "Ball to the designer" with no "Ball to the operator" on the **same PR** within 30 minutes rings the operator.
- Every channel (front door, main chat, demos, sagar, biz, site, pod, build, research) must be subscribed to its own PR so a new ball wakes it. Build was not on 22 Nov and slept through three balls.
- The operator cannot read or write Duet chats (blocked for him). Anything a channel needs from the operator goes on its PR as a ball, never only in a Duet chat.
