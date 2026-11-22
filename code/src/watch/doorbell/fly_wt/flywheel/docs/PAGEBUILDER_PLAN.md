# PAGEBUILDER_PLAN.md: one page builder, at the edge

Plan only. The owner's order, 22 Nov 2026, via the operator: slim down, one page builder in Cloudflare, rebuild the plane while it flies. Read against `PARTS.md` and `cf.py` (820f9bf). The operator builds.

Not seen from here: the heuremen-door worker source, any `summary_*.json`, `desks.json`, `build_site.py` and the live desk pages. None of them are in this repo. Every place this plan leans on their shape is marked **[confirm]**. Step 0 below turns those into facts before any code.

---

## The idea in one paragraph
A desk page today is data → `build_page.py` or a `build_site.py` section → HTML → `auto_ship.py` → `ship.sh` (27 gates, two git pushes, a worker deploy). After this, a desk page is data → `desk_<id>` in KV, and heuremen-door renders it on request from one template that ships with the worker. A data change is one gated `cf.kv_put`. `ship.sh` runs only when the template or worker code changes.

---

## 1. Edge rendering in heuremen-door

**Route.** heuremen-door already serves indahl.ai. It gains one handler for desk page paths **[confirm the current desk URL pattern, e.g. `/<id>/`]**:

```
GET /<id>/  (id in DESK_IDS, a list compiled into the worker at ship time)
  1. cache hit (Cache API, key = url + desk hash)           -> serve
  2. doc = KV.get("desk_" + id, {type: "json", cacheTtl: 60})
  3. check(doc)            schema "desk/1", id matches, outcome in the four values, every url https
  4. html = renderDesk(doc)   ONE template module, every field HTML-escaped
  5. put in cache, serve with the same headers the static page has today (noindex where it is noindex now)
  on any failure in 2-4    -> fallback chain (section 5)
```

- **One template.** `desk_template.js`, plain template literals and one `esc()` function, no library. It holds the shared head, nav, footer (the exact specbook footer block site_gate checks), the desk layout and the kit and plan links. Desk-specific shapes go through a short list of typed blocks (section 2), never per-desk HTML.
- **Escaping is the security line.** Quoted claims, source titles and footnotes are third-party text. `esc()` runs on every string, and links pass only as `https://` URLs. A doc with any other scheme fails `check()` and falls back.
- **The live feeds stay.** `<id>_live` → `/<id>/live.json` is untouched. Ticks keep writing it. Other readers use it.
- **Unknown ids** are not looked up in KV. `DESK_IDS` comes from `desks.json` at ship time, so a stray key can't create a page.

## 2. The desk JSON (`desk/1`)

One document per desk, key `desk_<id>`, namespace ecb59d96… (`cf.NS_DEFAULT`).

```json
{
  "schema": "desk/1",
  "id": "prometheus",
  "title": "…",
  "status": "live | building | plumbing",
  "updated": "2026-11-22T15:00:00Z",
  "headline": { "text": "…", "value": 0.0, "unit": "…", "as_of": "…" },
  "claim":    { "quote": "…", "by": "…", "source": "s1", "date": "…" },
  "outcome":  "ABOVE | BELOW | CONSISTENT | CANNOT_TELL",
  "measured": { "value": 0.0, "unit": "…" },
  "interval": { "low": 0.0, "high": 0.0, "level": 0.99, "method": "…", "n": 0 },
  "tally":    { "returned": 0, "nothing_returned": 0, "refused": 0, "held": 0 },
  "sources":  [ { "id": "s1", "title": "…", "url": "https://…", "retrieved": "…" } ],
  "kit":      { "url": "https://…", "sha256": "…", "version": "…" },
  "plan":     { "url": "https://…", "sha256": "…", "frozen": "…" },
  "footnotes": [ { "n": 1, "text": "…" } ],
  "blocks":   [ { "type": "table", "caption": "…", "head": ["…"], "rows": [["…"]] },
                { "type": "note", "text": "…" } ],
  "source_summary": { "file": "summary_prometheus.json", "sha256": "…" },
  "hash": "sha256 of this document without this field"
}
```

- `outcome` uses the four values the MCP servers already use. `tally` carries "nothing returned, refused and held are counted as their own outcomes".
- `claim.quote` is the stated value, quoted, with its source id. It is never paraphrased.
- `blocks` are for what varies by desk (tables, notes). v1 has two types. A new type is a template change and a ship, on purpose.
- `hash` lets the Mac skip a put when nothing changed, and gives the edge a cache key.

**Mapping from `summary_*.json`.** These files aren't visible from here, so the mapping is a contract plus one adapter per desk family:

| desk/1 field | Full-template desks (17, PCTHBLKD) | Older 29 Oct desks (24, built in build_site.py) |
|---|---|---|
| headline | the desk's own `*_headline.py` output, called as a module | the headline logic in that desk's build_site.py section **[confirm]** |
| claim, outcome, measured, interval | summary fields the current `build_page.py` reads **[confirm per desk]** | the summary fields the build_site.py section reads **[confirm]** |
| sources, footnotes | what build_page.py prints today | what the section prints |
| kit | heuremen_kit.py download (52 copies, all md5 5d280380) | same |
| plan | PLAN.md, its published URL and hash | same |
| blocks | the tables build_page.py draws | the tables the section draws |

Each adapter is `desk_json/<id>.py`, about 30 lines: read summary, call the headline module, return a dict. The fields come out of the existing builder line by line, so the adapter is a port of the builder's reads, not a rewrite of the page.

## 3. Migration order

**Step 0, facts (the operator, about an hour).** Paste the heuremen-door route table, one `summary_prometheus.json`, one `summary_argus.json`, deus's summary, and the `desks.json` entries for the three. Every [confirm] here closes on those.

**Step 1, worker in preview.** Ship the template and handler, serving only `/_edge/<id>/` (noindex, not linked). The public routes stay as they are. This is the only ship needed to start.

**Step 2, the three pilots.**
- **prometheus**: full template, has a rider. The reference case.
- **argus**: full template, a second shape.
- **deus**: no `*_tick` (deus_read.py) and no rider (PARTS #16). It proves the contract works for an odd desk, and it gets a rider or a `static` mark as part of the move.

For each pilot: adapter → `desk_publish.py <id>` (section 4) → `/_edge/<id>/` → `meaning_diff.py` against the live static page. The diff extracts visible text, every number, every link target and the footer, normalizes whitespace, and must match except the timestamp lines. When it matches for a full day of ticks, the desk joins the live list (`EDGE_DESKS` in the worker). That flip is a one-line worker config change and a ship. The old static page stays in place as the fallback asset.

**Step 3, the other 14 full-template desks.** Same steps, a few at a time. They share a builder shape, so their adapters are near copies.

**Step 4, the 24 older desks.** Their adapters are ported from build_site.py sections. Each port removes a section from build_site.py.

**Step 5, the rest.** petrol, rank, wiki, fidelity, now/predictions, seat, tape, time, uptime. Five stubs and shells (dryad, earthdata, qdata, datapaper, oy) get no page until they have data.

**Kept until each desk passes:** the old build path for that desk. Nothing is removed for a desk until its edge page has matched for a day and served live for a day.

## 4. What retires, and where the gates go

**Retires on the Mac once its desks are on the edge:**
- the 22 per-desk `build_page.py`, and the desk sections of `build_site.py` (most of its 3,595 lines are desks **[confirm]**)
- `lint_copy.py` per desk, folded into the one publish gate below
- `auto_ship.py` for data. A summary change no longer needs a ship. It stays only to queue template ships, or goes.
- `quickship.sh` for desk data. It keeps the copy fast path or is retired outright, since its deploy uses the second credential (PARTS #8).
- the 5 stale site-tree copies (public_mirror ×3, hf_stage ×2), archived outside ~/forge after one grep (PARTS #25)

**Stays:** `ship.sh` for the template, worker code, QIA static and the rest of indahl.ai. The `*_tick.py` riders, `<id>_live`, heuremen_kit.py and PLAN.md all stay.

**The one publish gate, `desk_publish.py <id>` (Mac, before any put):**
1. Build the doc with the adapter.
2. Check `desk/1`: fields, the four outcomes, https-only links, numbers are numbers.
3. **Render with the same template:** `node render_check.mjs <doc>` imports `desk_template.js` from the worker folder, so there is no second template.
4. Run the copy gates on that rendered HTML. That means site_gate.py (forbid rules, footer, count_scan 0b.5, tone_scan), spelling, name and headline_cover. site_gate.py gains a `--file <path>` mode (about 5 lines) so it can check one rendered page instead of globbing the tree.
5. If `hash` equals the last put, stop (no write).
6. `cf.kv_put('desk_<id>', path, who='desk_publish')`. A failure rings through cf.py's RING line, as for any other put.

Any gate failure means no put and a RING. The edge keeps serving the last good doc. Ticks call `desk_publish.py` where they call `auto_ship` today.

## 5. Caching and fallback

- **KV reads** use `cacheTtl: 60`. A put shows within about a minute, which is KV's normal spread.
- **Rendered pages** go in the Cache API, keyed by URL plus `hash`, with `s-maxage=300` and a long stale window. A new hash is a new key, so a fresh put never serves an old render past the KV minute.
- **Fallback chain when KV is unreadable or the doc fails `check()`:**
  1. the stale cached render (the last good page)
  2. the static fallback asset for that desk, kept in the worker's assets. During migration it is the current static page. After retirement, each template ship renders every desk's current doc into the assets folder, so the fallback is as fresh as the last ship and no extra build exists.
  3. a plain 503 page that says the desk page is unavailable and shows no numbers. It never shows made-up or empty values as data.
- Every fallback serve writes one log line (`console.log` with the desk id and the cause). cf_log_watch.py (the new 10:32 rider) can turn a run of them into a RING.

## 6. QIA

quantumidleaudit.com stays static, built by `site/console/build.py` and shipped from the operator's seat. No QIA data change before 27 Nov. Nothing in this plan touches QIA pages, `qia_*` KV keys or the QIA riders.

---

## My call on PARTS.md HARD 22, 23, 24 and 26

- **#22, one pinned interpreter: yes, first.** Use one project venv on Python 3.12, the version qvenv, yo, revise and mirror_check already run (3.12.13). Avoid brew's 3.14, because brew upgrades move it under the venv. Avoid CLT 3.9, which is past end of life and caused the fromisoformat and bq_publish failures. qvenv stays as the one allowed second interpreter, for the heavy QIA stack. The tick-bus plist points at the venv, and `desk_riders.py` gets one `PY` constant in place of `sys.executable` and bare paths. That gives two interpreters instead of 13, and the shared venv also ends the campus/ailuminate borrowing of revise's venv (#19).
- **#23, independent watchdog: yes, in /bin/sh, not Python.** It should share nothing with what it watches: its own launchd agent with StartInterval 120, about 20 lines of shell checking the ages of ticks.log, desk_bus_state.json, alerts/last_check and poll.out.log. It writes a RING line to pipe.log and also to `watch/WATCHDOG.txt`, which mission_hook.py reads directly. That way a dead doorbell (PARTS failure 3) still shows on the next prompt. Shell means a broken venv can't take the watchdog down with the buses.
- **#24, desk checker: yes, but against the JSON contract, not the folder template.** Once pages come from `desk/1`, a desk is healthy if it produces a valid doc, has a rider or a `static` mark, and its `desk_<id>` is fresh against its tier. Folder layout no longer matters. So `desk_doctor.py` checks desks.json id ↔ folder ↔ rider ↔ `desk_<id>` freshness ↔ `<id>_live` freshness. Migrating the 24 older folders to PCTHBLKD then isn't needed: their adapters are the migration. It also catches social, mlperf, voightkampff, deus, fidelity and zeus (#15, #16).
- **#26, one PATH and env: yes, with #22, in the same change.** Add EnvironmentVariables (PATH with /opt/homebrew/bin first, HEUREMEN_PUBLISH) to the tick-bus plist, and have desk_bus pass one env dict. The 65 scripts that patch PATH become harmless and can be cleaned when touched. This also ends the `No such file: 'gh'` ring from ack_watch.

**Order:** 22 + 26 together, then 23, then the page builder, with 24 built as part of the page builder's publish gate.

**A note on cf.py:** in the 820f9bf copy, `kv_get` already passes `stdout_only=True`, so PARTS #12 (stderr in the value) looks fixed in that file. Worth checking that the Mac copy matches.
