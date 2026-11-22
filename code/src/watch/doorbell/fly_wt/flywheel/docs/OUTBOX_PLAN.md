# OUTBOX_PLAN.md: one mail outbox (P4)

Plan plus code skeleton. The operator's order, 22 Nov 2026, from PIPELINE_AUDIT P4. This has to be in place before the 27 Nov sends resume, so that holds are enforced by code. The operator builds and runs it. **Nothing here sends anything. The skeleton defaults to `live: false`.**

Files on this branch:
- `flywheel/docs/OUTBOX_PLAN.md` (this file)
- `flywheel/docs/outbox.py`, the skeleton. It is stdlib only and 3.9-safe, and it was tested here with a mock transport on these cases:
  - idempotent dedupe
  - second notice refused
  - codes-only refusals
  - reply-time template refused
  - held kind
  - suppression at enqueue and again at send
  - pacing cap
  - missing pace skips the kind
  - crash between sending and sent becomes "unknown", is not resent, and rings
  - history import blocks a second notice

**Not seen from here:** the code of `iris_index/notices/*/send_guarded.py`, `qia/cf_send.py`, `send_wrap.py`, `cf_pacer.py`, `newsletter_send.py` and `alerts_send.py`, and the exact flags of `wrangler email sending`. Every value that should come from them is marked **[confirm]**. None of them is made up. A missing value makes that kind refuse to send.

---

## 1. The shape

```
producer (notice builder, newsletter, subscriber alerts, pitch/corporate drafts)
   └─ outbox.enqueue(kind, to, template, data, dedupe_key [, not_before, hold_reason])
         checks: kind known · template allowed for the kind and free of reply-time promises · address valid
                 · kind rules (codes_only, one_per_paper) · render succeeds · dedupe (repeat = same id back)
         state:  suppressed | held (kind hold or hold_reason) | awaiting_approval | queued
   ▼
outbox.db (sqlite, ~/forge/outbox/, outside every repo)
   ▼
outbox.py drain   (one rider, tier 1; the ONLY code that sends)
   live? · not held · pace allows · re-check suppression · render again · mark "sending"
   └─ transport: lib/cf.py wrangler('email','sending','send', …, role='mail')   keychain cloudflare-api-token-mail
         ok    → "sent" + receipt (provider id)
         error → retry after 10 min, then 1 h, then "failed" + one RING
         crash → "unknown" + one RING, never resent automatically
```

**Entry points:** `enqueue` to put mail in, `drain` to send it. Nothing else calls the mail token.

## 2. States

| State | Means | Leaves by |
|---|---|---|
| `awaiting_approval` | stored, waiting for the owner's word | `outbox.py approve --ids … --note "<whose yes, where, when>"` → queued |
| `held` | the kind is on hold, or the message has a `hold_reason` (an open question on a paper) | `outbox.py release --ids … --note …`, only once the kind's hold is off → awaiting_approval, or queued if the kind needs no approval |
| `queued` | approved and ready, sent when the pace allows | drain |
| `sending` | marked just before the provider call | sent / queued (retry) / failed, or `unknown` if the run died |
| `sent` | provider accepted it. Receipt written | final |
| `failed` | refused at send time (rule, template, no from address) or 3 provider errors. Rung once | final. A fresh enqueue with a new dedupe key is possible |
| `unknown` | crashed between "sending" and "sent". Rung once, never resent | `outbox.py mark <id> sent\|failed --note …` after a person checks the provider log |
| `suppressed` | address or domain on the suppression list, at enqueue or at send | final |
| `imported` | history from the old senders (section 6), so one-per-paper covers past notices | final |

## 3. kinds.json: per-kind policy

`~/forge/outbox/kinds.json`. This is the proposal. Values marked [confirm] are copied from the current senders, never guessed.

```json
{
  "live": false,
  "kinds": {
    "notices": {
      "why": "research notifications to authors; not under the 27 Nov hold (the owner 20 Nov); each send waits for his word, batches ok",
      "hold": false, "needs_approval": true,
      "from": "[confirm: the address send_guarded.py uses]",
      "templates": ["research_notification"],
      "rules": ["codes_only", "one_per_paper"],
      "fields": ["paper_id", "codes", "url", "[confirm: any other field the template uses]"],
      "codes": ["[confirm: the code table in send_guarded.py]"],
      "pace": {"min_gap_s": null, "per_hour": null, "per_day": null}
    },
    "corporate": {
      "why": "the owner: corporate on hold until Fri 27 Nov; lift only on his word",
      "hold": true, "needs_approval": true, "from": "[confirm]", "templates": [],
      "pace": {"min_gap_s": null, "per_hour": null, "per_day": null}
    },
    "pitch": {
      "why": "the owner: pitches on hold until Fri 27 Nov; lift only on his word",
      "hold": true, "needs_approval": true, "from": "[confirm]", "templates": [],
      "pace": {"min_gap_s": null, "per_hour": null, "per_day": null}
    },
    "newsletter": {
      "why": "[confirm with the operator whether the 27 Nov hold covers it; held until then]",
      "hold": true, "needs_approval": true, "from": "[confirm: newsletter_send.py]", "templates": ["newsletter"],
      "pace": {"min_gap_s": null, "per_hour": null, "per_day": null}
    },
    "alerts": {
      "why": "subscriber alerts people signed up for; behaviour as alerts_send.py today",
      "hold": false, "needs_approval": false, "from": "[confirm: alerts_send.py]", "templates": ["[confirm]"],
      "pace": {"min_gap_s": null, "per_hour": null, "per_day": null}
    }
  }
}
```

- **The pace values come from `send_wrap.py` and `cf_pacer.py` [confirm]**: the gap between sends, the hourly cap and the daily cap each sender uses today. Until they are filled in, `drain` prints "pace not set" and skips that kind.
- **Holds have no expiry date on purpose.** 27 Nov is when the owner decides, not a timer. Lifting a hold means setting `"hold": false` and writing whose word it was in `why`. Messages that were held stay held until each is released by id, so a backlog never goes out in one burst because a flag changed.
- **`needs_approval` defaults to true** for any kind that doesn't say otherwise.

## 4. Rules in code

| the owner or specbook rule | In outbox.py |
|---|---|
| Corporate and pitch sends wait until 27 Nov | `hold: true`. enqueue stores them as `held`, and drain skips held kinds. release refuses while the kind is held |
| Each research notice waits for his word (batches ok) | `needs_approval: true` → `awaiting_approval` until `approve --ids … --note` |
| A paper with an open question is held, not raised, and the rest keep shipping (21 Nov) | producer passes `hold_reason="open question"` → `held` for that message only |
| **Codes-only notices** | `codes_only`: data keys must be inside `fields`, and `codes` must be a non-empty list drawn from the code table. Any free-text field is refused at enqueue |
| **No second notice on the same paper** | `one_per_paper`: `rule_key = paper:<paper_id>`. enqueue refuses if any message for that paper is awaiting, held, queued, sending, sent, unknown or imported. A second recipient on the same paper goes in the same message's `to` list, not in a second message |
| **No reply-time promises in any template** | `PROMISE` regex, checked when a template loads and again on the rendered text: "within N hours/days", "24 h", "we will reply/respond/get back", "shortly", "promptly", "as soon as possible", "reply by". A hit refuses the template |
| Plain text only | HTML tags in a template are refused |
| No double sends | `dedupe_key` is UNIQUE, so a repeated enqueue returns the same id. A crash mid-send becomes `unknown` and is never retried automatically |
| Suppression (opt-outs, bounces, authors who asked not to be contacted) | `suppress` table, by address or `@domain`. Checked at enqueue and again just before send |

The research-notification template moves into `templates/research_notification.txt` word for word from the operator's current one. Its first line is `Subject: …`, then a blank line, then the body with `$paper_id`, `$codes` and `$url` placeholders [confirm the field names]. If the template check refuses it, that is the template to fix, not the check.

## 5. Transport

The `transport()` function is the only line that sends: `cf.wrangler('email', 'sending', 'send', '--from', …, '--to', …, '--subject', …, '--text', …, role='mail', timeout=60)`.

**[confirm] the subcommand and flags** with `npx wrangler email sending --help`, and match `transport()` to it. A long body may need a file flag instead of `--text`. The provider message id is read from the output when present and stored in the receipt. Bounce and complaint reads (`cf_deliveries.py` today) can feed `suppress` later, through the same mail role.

`live` stays false until three things are true: the flags are confirmed, the pace values are filled in, and the owner says the first batch goes.

## 6. Cutover

1. Put `outbox.py` in `~/forge/lib/`, so producers import it the same way as `cf`. Make `~/forge/outbox/` with `kinds.json` (`live: false`) and the templates. Keep the folder outside every repo, because it holds addresses.
2. **Import history** so that one-per-paper covers past notices: list every paper the old senders noticed (from their logs or state files [confirm where]), one paper id per line, then run `python3 lib/outbox.py import-sent notices noticed.txt`.
3. **Switch one producer at a time, starting with notices.** In the same commit, the producer calls `enqueue` instead of its sender, and the old sender's rider comes out of desk_riders. The two are never active together.
4. Add the drain rider: `(1, [PY, '-I', '../lib/outbox.py', 'drain'])` (PY from ENV_PLAN, or `/usr/bin/python3` until then, since the code is 3.9-safe).
5. Check with `outbox.py status` and `outbox.py preview <id>`. Preview shows the rendered subject and body and the recipient count, not the addresses.
6. On the owner's word for the first batch: set `"live": true`, then `approve --ids … --note "the owner, main chat, <date>"`.
7. Then the rest, one at a time: alerts, newsletter, and pitch/corporate as drafts that stay held until 27 Nov or his word.

**Retires:** `iris_index/notices/*/send_guarded.py`, `qia/cf_send.py`, `indahl-ai/newsletter_send.py` and `alerts_send.py` as senders (each keeps its building logic as a producer), the pacing in `send_wrap.py`/`cf_pacer.py`/`sagar_pacer_rider.py` (moved into `kinds.json`), and `email_gate` at ship time (now at enqueue). webhooks_send and push_send are not mail and stay as they are.

**Rollback:** `"live": false` stops every send on the next drain, which is one switch. Turning an old sender back on is a last resort, because its history would no longer match the outbox's. If it ever happens, import whatever it sent before switching back.

## 7. Alerts it raises (external or a person's decision only)

| Ring | When |
|---|---|
| `OUTBOX message N refused at send: <rule>` | a template or rule changed between enqueue and send. Nothing went out |
| `OUTBOX message N failed 3 times: <provider reason>` | the provider kept refusing (credential, quota, outage) |
| `OUTBOX message N may or may not have gone out; not resent` | a crash mid-send. A person checks the provider log and marks it |

Nothing watches the outbox from outside it. A held, unapproved or suppressed message is a decision already recorded, not a fault.
