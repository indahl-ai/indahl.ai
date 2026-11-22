# Ship gates inventory, 22 Nov 2026

Read-only inventory of `ledger/ship.sh` (133 lines) as it stands on the night of 21 to 22 Nov 2026. Nothing was run that writes. Line numbers are ship.sh lines unless a file is named. Timings come from the mtimes of `ledger/gates/*.txt` from the 21:39 run and from the scripts' own printed times. "Stops" means the ship exits before deploy. "set -e" means the step has no SHIP REFUSED message but a nonzero exit still kills the ship (the EXIT trap at line 23 rings pipe.log).

The script has 61 distinct steps. 38 of them can stop the ship before the deploy (34 with an explicit refusal or a `gate` wrapper, 4 more only through set -e). 13 run after the deploy and cannot undo it.

## Step table

Columns: # | step | command | reads | refuses on | writes | duplicated sources it depends on | time | breach scope

| # | step | command (line) | reads | refuses on | writes | dup sources | time | scope |
|---|---|---|---|---|---|---|---|---|
| 0 | site lock | `ledger/site_lock.py run` (3) | lock file | never, waits in line | lock state | none | waits | whole |
| 1 | FAULTS/GUARDS PDFs | `ligera/render.sh` (29-30) | `ligera/FAULTS.html`, `GUARDS.html` | set -e on render failure | `heuremen.org/faults.pdf`, `guards.pdf` | none | seconds, only when newer | whole |
| 2 | paper | `tectonic main.tex` (31-35) | `arxiv_one_readout/` | "the paper does not compile" | `heuremen.org/a-readout-is-not-an-idle.pdf`, `arxiv_one_readout/main.pdf` | none | only when newer | whole |
| 3 | paper source sync | `cp` (38-39) | `arxiv_one_readout/` | set -e on cp failure | `public_mirror/heuremen.org/paper/` (working tree of a public repo, pushed in step 51) | none | instant | whole |
| 4 | bill | `qia_template/render_bill.py` (40-41) | `QIA-2026-001.json` | set -e | `QIA-2026-001.pdf` | none | only when newer | whole |
| 5 | sweep backups | `ledger/sweep_backups.py` (42) | worker `public/`, `public_mirror/indahl.ai` | set -e | moves files to `archive_private/public_backups/` | `backup_patterns.py` PAT | seconds | whole |
| 6 | CENSUS refresh | `census_index/refresh_page.py` (43) | desk summary | never, rings | census page tables, `census.*` ledger rows | ledger rows | seconds | per-desk |
| 7 | NEO refresh | `neo_index/refresh_page.py` (44) | desk summary | never, rings | neo page, `neo.*` ledger rows | ledger rows | seconds | per-desk |
| 8 | QUAKE refresh | `quake_index/refresh_page.py` (45) | desk summary | never, rings | quake page, `quake.*` ledger rows | ledger rows | seconds | per-desk |
| 9 | QIA list render | `qia_leads/matrix_page/render_list.py` (47) | `list.json` | set -e | `/qia/list` table | none | seconds | whole |
| 10 | page builder loop | 6 builders: `make_sagar.py`, `iris_list.py`, `qia_page.py`, `build_atlasmap.py`, `build_iris_page.py`, `build_matrix_page.py` (48) | their sources | never, rings per builder | their pages | none | tens of seconds | per-builder |
| 11 | headlines | `watch/headlines.py` (49) | live feeds (network), `LOCAL` files, `desks.json` on_home | never, rings | `watch/headlines.json`, `headlines_state.json`, KV `headlines` only if `HEUREMEN_PUBLISH=1` is in the environment | `headlines.py` per-desk functions (41), `LOCAL` (line 18), desks.json | about 1 min | per-desk (skips) |
| 12 | downloads refresh | `ledger/downloads.py refresh` (50) | `copies.json`, packs, `pack_inputs.json` | set -e | runs `copies.py publish` up to 3 times, List packs, QIA package, desk packs (desk builders), `pack.size.*` ledger rows | `copies.json` | tens of seconds | whole |
| 13 | kits refresh | `indahl-ai/reproduce_kits.py refresh` (51) | live feeds, ledger, `SPECS` | never (`|| true`) | remade kits under `reproduce_kits/kits/`, `index.json`, pipe.log rings | SPECS, LH.DESKS | up to minutes when kits remake | per-desk |
| 14 | indahl.ai build | `indahl-ai/build_site.py` (52) | `desks.json`, `seo/seo_copy.json`, every `<desk>.html`, ledger, packs, `forecasters/members.json` | set -e, BUILD REFUSED when more than 3 desk pages fail (build_site.py 2927) | every `indahl-ai/*.html`, `pages.js`, `desks_live.js`, og PNGs, change feeds, `.desk_build_state.json` | PAGES, _FEED, NAV, HOME, seo_copy, desks.json, build_page DESC (via html) | about 30 s | per-desk up to 3, then whole |
| 15 | QIA site build | `indahl-ai/qia_site.py` (53) | QIA sources | "quantumidleaudit.com build failed" | `public/_qiasite/*.html` | none | seconds | whole |
| 16 | post-build packs | `downloads.py refresh --post` (54) | built OY pages | set -e on any exit but 0 or 10 | packs, and a second `build_site.py` run on exit 10 | `copies.json` | up to another build | whole |
| 17 | COPY | `gate copies_publish` -> `copies.py publish` (56) | `copies.json` | any MISSING, STALE or DIFFERS set | every copy in `copies.json` | `copies.json` | ~2 s | whole |
| 18 | ledger | `check_ledger.py` (57) | `ledger.jsonl`, every surface, live feeds (network) | MISSING, ZOMBIE, SOURCE on any row, or more than 3 LIVEFEED/LIVEFIELD desks | `ledger/live_held.json`, `/tmp/check_ledger_last.txt`, pipe.log | LH.H2 (stored as row surface text), LH.DESKS fields | ~10 s with step 19 | whole, except live feeds (per-desk up to 3) |
| 19 | removed ids | `removed_gate.py` (58) | `removed_by_author.json`, `indahl-ai/`, worker `public/`, `public_mirror/indahl.ai` | any removed id on a page | nothing | none | ~3 s | whole |
| 20 | copies check | `gate copies_check` (59) | `copies.json` | any drift | gate log | `copies.json` | <1 s | whole |
| 21 | downloads gate | `downloads.py gate` (60), with one inline `refresh` retry | packs, `removed_at_request.json` | any stale download after one retry | the retry runs refresh (writes as step 12) | `copies.json` | seconds, doubles on retry | whole |
| 22 | backups gate | `backup_patterns.py` (61) | `public/`, mirror | any backup-named file | nothing | PAT | <1 s | whole |
| 23 | spelling | `spelling_gate.py` (62) | built pages | any British spelling | a new-data report file, `/tmp/spelling_gate_last.txt` | none | ~1 s | whole |
| 24 | name | `name_gate.py` (63) | built pages, `faultsguards/CURRENT.json` | "Standards" plural | `/tmp/name_gate_last.txt` | none | <1 s | whole |
| 25 | links | `link_gate.py` (64) | built pages, `public/`, `worker.js` routes, handler modules | any dead same-site link, any backup file served | `/tmp/link_gate_last.txt` | worker routes, desk paths | ~2 s | whole |
| 26 | headline seed | `live_headlines.py seed` (65) | `LH.DESKS`, `LH.H2`, `CHECKS.md` | any exception (missing CHECKS entry, a missing H2, a missing surface) | adds `live.<slug>.headline` rows to `ledger.jsonl` | LH.DESKS, LH.H2 | ~1 s | whole |
| 27 | headline cover | `gate headline_cover` (66) | `headlines.json`, ledger, LH.DESKS, kit.json files, live feeds | COVER, ROW, KIT, NOROW breach on any one card | gate log | LH.DESKS, kit specs, `headlines.py` LOCAL, NOROW (gate line 20) | ~2 s | whole |
| 28 | desk list | `desk_list_gate.py --quiet` (67) | desks.json and 10 lists | never (warn only) | `.desk_list_gate_state.json`, pipe.log | all desk lists | <1 s | none |
| 29 | specbook | `gate site_gate` (68) | `site_rules.json`, every page | any forbidden pattern | gate log | none | ~1 s | whole |
| 30 | Check a Run | `runcheck_gate.sh` (69) | qia_check package, two `runcheck.js` copies, tests | any mismatch | `.runcheck_gate_pass` | two runcheck.js copies | instant, about 5 min when inputs changed | whole |
| 31 | stats regression | `node tests/stats_regression.mjs` (70) | stats checker | any failed test | `/tmp/stats_regression.log` | none | ~1 s | whole |
| 32 | QIA sources | `gate source_gate` (71) | `book_calibrated.json`, cited files | any QIA row without its number in a cited file | gate log | none | <1 s | whole |
| 33 | QIA list check | `render_list.py --check` (72) | `list.json`, page | set -e on mismatch | nothing | none | <1 s | whole |
| 34 | findable | `gate findable` (74) | built pages, desks.json feeds, `STATIC_FEED` | any JSON-LD that does not parse or a Dataset missing fields | gate log | desks.json feed, findable `STATIC_FEED` (line 24) | <1 s | whole |
| 35 | entities | `gate entities` (77) | `entities_index.json`, `brands/rows.json`, built pages | any entity row not traced | gate log | none | <1 s | whole |
| 36 | forecasters | `gate forecasters` (78) | `forecasters/rows.json`, `members.json`, feeds | any number not traced | gate log | `forecasters/members.json` (13 desks) | <1 s | whole |
| 37 | email | `gate email_gate` (79) | every built and served text file | any non-house email address | gate log | none | ~9 s | whole |
| 38 | confessions | `no_confessions_gate.py` (80) | built pages | any listed phrase | nothing | none | <1 s | whole |
| 39 | notify | `gate notify` (81) | built feeds, calendars, OPML | any that does not parse | gate log | none | <1 s | whole |
| 40 | accountability | `gate accountability` (82) | 7 accountability pages, `/security/self` check file | semicolon, house word, missing page | gate log | none | <1 s | whole |
| 41 | alert receipts | `gate alert_receipts` (83) | receipt chain | chain break, subscriber data | gate log | none | <1 s | whole |
| 42 | reproduce kits | `gate reproduce_kits` (84) | kits, ledger, LH.DESKS, desks.json, live feeds | more than 3 desks breaching at once | `reproduce_kits/held.json`, `index.json` verified stamps, pipe.log | SPECS, NOKIT, LH.DESKS, desks.json | 70 s | per-desk up to 3, then whole |
| 43 | cited files | inline python (88-97) | `ledger.jsonl` live rows | a live row cites a missing `heuremen.org/` file | `git add` in heuremen.org | ledger | instant | whole |
| 44 | commit | `git commit` in heuremen.org and indahl-ai (98-99) | working trees | set -e on a pre-commit hook failure. heuremen.org runs `readcheck_hook.sh`. indahl-ai reruns `check_ledger.py`, `site_gate.py`, `copies.py check` | two local commits | same as 18, 20, 29 | ~15 s (repeats gates) | whole |
| 45 | push heuremen.org | `git push origin main` (101) | commit | never, rings | GitHub `indahl-ai/heuremen.org` | none | seconds | whole |
| 46 | push indahl-ai | `git push` (102) | commit | never, rings | GitHub indahl-ai private source repo | none | seconds | whole |
| 47 | push status | inline python (104) | push exit codes | never | `ledger/ship_push_status.json` | none | instant | none |
| 48 | worker deploy | `deploy_hash.sh`, `npx wrangler deploy`, `stamps.py manifest` (106-109) | worker.js, `indahl-ai/*.js/html`, page folders, `public/` | wrangler failure ("worker deploy failed") | live indahl.ai and quantumidleaudit.com, `.last_deploy.sha`, `ledger/stamps/deployed_manifest.json` | deploy_hash folder list | ~30 s to 1 min | whole |
| 49 | money path | `money_path_check.py --quiet` (112) | live quantumidleaudit.com and indahl.ai, `demos.json` | post-deploy, exit 1 at end only | its state file, pipe.log, a dry POST to `/inquire`, runs `inquiry_bell.py` | `demos.json` | tens of seconds | whole |
| 50 | MCP gate | `mcp_gate.py --quiet` (113) | live MCP endpoints, built `api.js` | post-deploy, exit 1 at end only | state file, pipe.log | `api.js` MAIN_TOOLS | tens of seconds | whole |
| 51 | public repos | `push_public.sh` (116-120) | worker `public/`, code dirs, push_public `DESKS` (line 83) | never stops the ship (exit 3, 4, 5 recorded) | public GitHub repos indahl.ai, heuremen.org, claude-plugins, `public_push_status.json`, `alerts/ALERTS_OPEN.txt` | push_public DESKS | ~1 min | whole |
| 52 | build record | `accountability.py buildinfo` (121) | `.last_ship_gates.txt`, push status, deploy hash | never | `ledger/builds/build_<commit>.json`, KV `build_json` (public `/build.json`) | none | seconds | none |
| 53 | privacy gate | `public_privacy_gate.py` (123) | public mirror git files | alert only | `alerts/ALERTS_OPEN.txt`, pipe.log | none | seconds | whole |
| 54 | served gate | `served_public_gate.py` (124-125) | `public/`, mirror git | alert only | `public_gates_status.json`, `ALERTS_OPEN.txt` | none | seconds | whole |
| 55 | IndexNow | `tools/indexnow.py` (127) | built pages, `indexnow_state.json` | never | IndexNow API pings, state file | none | seconds | none |
| 56 | VERIFY | `copies.py live` (131-133), 6 tries 20 s apart | live URLs in `copies.json` | exit 1 if live never matches (after deploy) | `/tmp/ship_live.txt` | `copies.json` | up to 2 min | whole |
| 57 | release stamp | `stamps.py release` (130) | manifest, ledger hash | never | `ledger/stamps/release_*.json`, Wayback Save Page Now requests | none | seconds, Wayback in background | none |
| 58 | WebSub | `websub_ping.py ship` (130) | built feeds | never | pings to pubsubhubbub.appspot.com, state | none | seconds | none |
| 59 | ledger backup | `git -C ledger push backup` (130) | ledger repo | never | private backup repo, `ledger_backup_status.json` | none | seconds | none |
| 60 | archive backup | `archive_push.sh` (130) | `archive_private/` | never | commit and push to private repo backup-private | none | varies | none |
| 61 | Zenodo | `zenodo_sync.py --publish` (130) | `ZENODO_MAP.json`, served files | never | new Zenodo versions (public DOIs), `ZENODO_MAP.json`, `zenodo_dois.json`, `zenodo_packs/dois.json`, ledger rows and page sources that print a DOI | ledger | minutes when a record changes | per-record |

Steps 57 to 61 run only when VERIFY passes. Steps 49, 50, 53 and 54 never stop the public push. The first nonzero refusal in steps 1 to 44 stops everything that follows, including every later gate, so one run shows one refusal at a time.

## 1. Duplicated sources

Nine fact classes have more than one hand-kept copy. Counts compare literal values in source files (parsed with ast, nothing imported that writes).

### 1a. Desk list (which desks exist)

Copies:
- `ledger/desks.json` `desks` (64 entries, 62 desks and 2 division rows). Meant to be the one list.
- `indahl-ai/build_site.py` line 18 `NAV`, a hand list of 27 paths (`/cada`, `/uptime`, `/time` and others). `desk_list_gate.py` does not read it.
- `indahl-ai/build_site.py` line 16 `HOME` (breadcrumbs, checked by desk_list_gate), line 178 `_PARENT` (not checked), and lines like 1765 `HOME['/prometheus'] = '/hermes'` set inside desk blocks.
- `indahl-ai/build_site.py` `PAGES['/<desk>']` blocks, one per desk (61 of 62 desks have a literal block, forecasters is built by `forecasters.py`).
- `indahl-ai/build_site.py` `_FEED.append` lines (70 literal lines, 1010 to 1830). Five desks have no literal feed line: lab, forecasters, vault, oy, chronos.
- `ledger/live_headlines.py` line 30 `DESKS` literal (35) plus item assignments at lines 202, 205, 208, 211 (petrol, rank, social, hflicense) for 39 total.
- `indahl-ai/reproduce_kits.py` line 44 `SPECS` (32) and line 161 `NOKIT` (10).
- `watch/headlines.py` one function per desk (41 desk functions, 44 `add()` slugs including atlas, iris, iris/lab, qia) and `LOCAL` at line 18 (12 desks).
- `ledger/headline_cover_gate.py` line 20 `NOROW` (6 card slugs).
- `ledger/push_public.sh` line 83 `DESKS`, `ledger/receipts.py` line 296 `CODE_DIRS`, `cloudflare-workers/heuremen-door/worker.js` `/<desk>/live.json` routes.
- `forecasters/members.json` (13 desks).
- `indahl-ai/findable.py` line 24 `STATIC_FEED`.

Differences found:
- desks.json `live_headline` true on 35 desks, `LH.DESKS` holds 39. The 4 extra (hflicense, petrol, rank, social) are added by item assignment after the literal. `desk_list_gate.py` reads only the literal (`_assign`), so it reports "every list agrees" while 4 desks differ.
- SPECS equals desks.json `has_kit` (32). NOKIT equals `nokit` (10). 0 differ.
- 22 desks have neither a kit nor a NOKIT entry (arxivdrift, cassandra, fidelity, forecast, wiki, seat, the census and atlas subpages and others). The reproduce gate only demands one of the two for desks in LH.DESKS, so this is allowed today.
- `NAV` (27 paths) has no check at all.

### 1b. Title

Copies: desks.json `title` (short nav label) and `what`, the second argument of each `PAGES` call, each `<desk>_index/build_page.py` `TITLE` (16 desks), `seo/seo_copy.json` `title` (overrides when not null, set on 1 desk), `LH.DESKS[slug]['name']`, the `_FEED` title, the `hero_slim()` text in each PAGES call.
Differences: build_page TITLE equals the PAGES title on all 16. `LH.DESKS['census'].name` is CENSUS while desks.json title is REVISIONS. The desks.json `what` line is not found inside the `_FEED` title on 42 of 59 desks (for example census: "Stated Census intervals against the revisions that followed" against "CENSUS: Stated uncertainty against later revisions").

### 1c. Description (meta description)

Copies: third argument of each `PAGES` call in build_site.py, `build_page.py` `DESC` (16 desks, used in the standalone `<desk>.html` head, which build_site.py discards when it cuts the body), and `indahl-ai/seo/seo_copy.json` `description`, which `page()` (build_site.py 185-188) puts in place of the PAGES text whenever the path is listed.
Differences:
- PAGES description against build_page DESC: 6 of 16 differ. neo (build_site 1631, build_page 14), seasonal (1646, 57), tornado (1744, 125), prometheus (1774, 53), cassandra (1789, 81), voightkampff (1819, 117).
- seo_copy lists 42 desks. Its description differs from the PAGES text on 41 of them, so for those 41 the PAGES description is dead text that still has to be kept.
- 10 desks carry three descriptions at once (seo_copy, PAGES, build_page): neo, solar, quake, cone, seasonal, steo, flu, tornado, credit, wiki.

### 1d. Feed line (the site feed entry)

Copies: `_FEED.append((path, title, desc))` lines in build_site.py, written by hand next to each desk block, plus the feed URL in desks.json `feed`, LH `feed_url(slug)`, findable `STATIC_FEED`, `watch/headlines.py` `LOCAL`, and worker.js routes.
Differences: feed URLs agree between desks.json and LH for all 39. Feed titles and descriptions have no check. They differ from desks.json `what` on 42 of 59.

### 1e. Headline spec

Copies: `LH.DESKS` field, n, of, lo, hi, outcome, show, stamp (line 30 and the `.update()` calls at 180 to 211), `LH.H2` and `H2_ADD` (lines 215 to 225), the ledger row `live.<slug>.headline` (written by `seed`, which also copies `H2[slug]` in as surface text), each kit's `kit.json` headline, and the hand-written card function in `watch/headlines.py`.
Differences: H2 text differs from desks.json `what` on 38 of 39 desks. The H2 copied into each ledger row must also stay on the built page or `check_ledger.py` reports MISSING. `headline_cover_gate.py` exists only to keep the card, the ledger row and the kit in step.

### 1f. Kit spec

Copies: `reproduce_kits.py` `SPECS` entry (mode, sources, ref files, python), the `has_kit`/`nokit` flags in desks.json, and `kit.json` inside each kit, whose headline block must equal LH.DESKS.
Differences: membership agrees (0 differ). Field agreement is checked twice, by `headline_cover_gate` KIT and by the reproduce gate.

### 1g. Page path

Copies: desks.json `path`, the `PAGES` key, the `page()` first argument (written twice on every PAGES line), the `_FEED` path, `HOME` and `NAV` entries, worker.js routes, link_gate's route reading, `deploy_hash.sh` folder list.
Differences: 12 desks have a path that is not `/<id>` (census subpages, atlas subpages, `/iris/lab`, `/hermes/model`, `/hermes/datapapers`, `/census`). No mismatch found between desks.json and PAGES keys.

### 1h. Division and nav placement

Copies: desks.json `division`, `nav`, `home_division`, build_site.py `HOME` (line 16), `_PARENT` (line 178), `NAV` (line 18), in-block `HOME[...] =` lines, and the hardcoded crumb string `Division: <a href="/hermes">HERMES</a>` that each build_page.py writes and build_site.py asserts and strips (for example lines 1741, 1757).

### 1i. File copies

`ledger/copies.json` itself is a copy registry. `copies.py publish` runs at step 12 (up to three times inside `downloads.py refresh`), again at step 17, and is checked at step 20, step 44 (pre-commit) and step 56.

## 2. Steps that stop the whole ship for one desk's problem

- 18 `check_ledger.py`: one MISSING, ZOMBIE or SOURCE row from any desk refuses everything. Only live feed failures are scoped (up to 3).
- 26 `live_headlines.py seed`: one desk spec with no H2 or no surface raises and refuses (the 21:29 refusal).
- 27 `headline_cover_gate`: any one card breach refuses. It has no per-desk hold.
- 25 `link_gate`: one dead link on one desk page refuses.
- 23, 24, 38 spelling, name, confessions: one hit on one desk page refuses.
- 29 `site_gate`, 34 `findable`, 37 `email_gate`: one page refuses.
- 21 downloads gate: one stale desk pack refuses.
- 17 and 20 copies: one desk's stale or missing copy refuses.
- 36 forecasters: one untraced number from one of its 13 member desks refuses.
- 14 build_site and 42 reproduce kits are scoped per desk, but only up to 3 desks. Tonight's run had 5 kit breaches (cadence, argus, prometheus, voightkampff, deus), 4 of them "no live ledger value row" for first-ship desks, so the whole ship refused.
- 44 commit: the indahl-ai pre-commit hook reruns check_ledger, site_gate and copies check without any scoping.

## 3. Steps with no dry-run or no-deploy mode

ship.sh itself has no dry-run or no-deploy flag. Running it always ends in commit, push and deploy if gates pass.

Steps whose script has no read-only mode as called: 1, 2, 3, 4 (renders write in place), 6 to 10 (page builders write their pages), 12 and 16 `downloads.py refresh` (writes packs, ledger size rows), 13 `reproduce_kits.py refresh`, 14 `build_site.py`, 15 `qia_site.py`, 17 `copies.py publish`, 26 `live_headlines.py seed` (its `run` has `--dry`, `seed` does not), 43 and 44 (git add and commit), 45 and 46 (git push), 48 (`wrangler deploy` is called without `--dry-run`), 51 `push_public.sh`, 52 `accountability.py buildinfo` (KV write), 59 and 60 (git push).

Gates that are read-only or have a report mode: 19, 20, 22, 24 (`--report`), 25 (`--report`), 23 (`--report`, otherwise writes a report file), 27, 29, 31, 32 (`--report`), 33, 35, 36, 38, 39, 40, 41. Gates that are checks but still write state: 18 (`live_held.json`, pipe.log), 28 (state file, pipe.log), 30 (pass hash), 42 (`held.json`, `index.json`). `sweep_backups.py --dry`, `websub_ping.py --dry`, `indexnow.py --init`, `alert_receipts --dry`, `forecasters --dry` and `zenodo_sync.py` (dry by default) exist but ship.sh never uses them. `watch/headlines.py` skips its KV write unless `HEUREMEN_PUBLISH=1` is set, but it still rewrites `watch/headlines.json`, which the pages read.

## 4. Writes to public surfaces, in order

1. Step 3 copies the paper source into `public_mirror/heuremen.org/paper/` (local working tree of a public repo, published at step 51).
2. Step 11 can put KV key `headlines` on the indahl.ai KV namespace when the environment carries `HEUREMEN_PUBLISH=1` (the tick bus exports it, a hand ship does not).
3. Step 45 pushes heuremen.org to GitHub `indahl-ai/heuremen.org`, which serves heuremen.org.
4. Step 46 pushes the indahl-ai source repo.
5. Step 48 deploys the heuremen-door worker with `npx wrangler deploy` (live indahl.ai and quantumidleaudit.com).
6. Step 49 sends a non-storing POST to `https://indahl.ai/inquire`.
7. Step 51 `push_public.sh` commits and pushes the public GitHub repos indahl.ai, heuremen.org and claude-plugins.
8. Step 52 writes KV key `build_json` (served as `/build.json`).
9. Step 55 sends changed URLs to IndexNow.
10. Step 57 sends changed URLs to Internet Archive Save Page Now.
11. Step 58 pings the WebSub hub.
12. Step 59 pushes the ledger to its private backup repo, and step 60 pushes `archive_private` to a private repo (private, listed for completeness).
13. Step 61 publishes new Zenodo versions with new public DOIs, then edits ledger rows and page sources that print a DOI. Those edits ship only on the next run.

Steps 1 to 44 write only local files, but several of them write into folders the deploy and the public push serve (`indahl-ai/*.html`, worker `public/`, `public_mirror/`), so a refused ship leaves a half-built local tree in place until the next run.
