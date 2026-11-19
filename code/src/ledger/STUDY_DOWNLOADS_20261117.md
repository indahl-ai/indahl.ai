# Study-list downloads: inventory, 17 Nov 2026

17 Nov 2026, the owner: one public list per desk (the web list page, built from the ledger-backed rows); no official downloadable copy of a
study list, so a removal is honoured everywhere automatically. Non-study grab-and-go data packs on /downloads stay.
Written before any change (assess first). Status column says what was done after (see the end).

## A. Files served on indahl.ai (cloudflare-workers/heuremen-door/public/)

| Surface | Made by | Advertised at | Read by |
|---|---|---|---|
| /qia/list.json | ledger/copies.json `qia-list-json` copies the hand-kept qia_leads/matrix_page/list.json | /qia, /qia/list (noscript "download"), JSON-LD Dataset on /qia (build_site.py page() `dd`), llms.txt / llms-full ("Machine-readable at"), tools/desk_pack.py source cite | **/qia/list page script public/qia/list.js (fetches the whole file for search/filters/pages)**; **MCP api.js `studies()` (find_study, qia tools) through env.ASSETS** |
| /iris/list.json | iris_index/matrix_page/iris_list.py writes iris_list.json and copies it; copies.json `iris-list-json` | /iris ("download" link, build_site.py ~1877), JSON-LD on /iris, llms.txt | MCP api.js `studies()` (find_study division iris) |
| /sagar/list.json | build_site.py copies sagar/site/list.json (make_sagar.py) | not linked; worker serves it with headers (worker.js ~478) | MCP api.js `studies()` (find_study sagar, astrophysics_find_study) |
| /qia/qia-list-pack.zip (+ .sha256, -LICENSE.txt) | list_packs/build_packs.py via ledger/downloads.py refresh; copies.json `qia-list-pack` | pkgbox on /qia/list, "Also:" line on /qia, Data pack link on /qia/list and every /qia/study/* page (`_dpk_for`), /downloads grab-and-go (QIA LIST line, desk_pack.py OTHER), llms.txt, findable.py Dataset distribution | nothing (download only) |
| /iris/iris-list-pack.zip (+ .sha256, -LICENSE.txt) | same | same pattern on /iris/list, /iris, /iris/study/*, /downloads | nothing |
| tools/desk_packs/pack_sizes.json keys qia/qia-list-pack.zip, iris/iris-list-pack.zip | tools/desk_pack.py OTHER | /downloads sizes | ledger rows pack.size.qia-list-pack, pack.size.iris-list-pack (surface downloads) |

Not study lists (stay): QIA / IRIS Research Packages (checkers; no list.json or list.csv inside, checked), desk data packs (*-data-pack.zip),
/qia/data.json (raw measurement files index), /hermes/datapapers.json (data papers index). Operator decision: arxivdrift and linkrot data packs
carry arXiv ids (papers revised / dead links); they are desk measurements, kept as grab-and-go.

## B. Ledger rows
- pack.size.qia-list-pack, pack.size.iris-list-pack (live, surface `downloads`, source tools/desk_packs/pack_sizes.json).

## C. Hugging Face
- Datasets indahl/qia-list, indahl/iris-list, indahl/qia-calibrated-studies: set PRIVATE by the main session 17 Nov (not deleted).
  No script in the repo creates or uploads them (hand-made); ledger/hf_packs.py only uploads `*-data-pack.zip` from the public mirror.
  Linked from build_site.py `_HF` map (/qia, /qia/list, /qia/package, /iris, /iris/list, /iris/package).
- indahl/indahl.ai (model repo) = hf_stage/hf_site_sync.py mirror of public_mirror/indahl.ai git HEAD: carries qia/list.json, iris/list.json,
  sagar/list.json, both list packs, code/list-packs, code/repos/sagar/index + data. It deletes on HF whatever leaves the mirror.
- hf_stage/indahl.ai and hf_stage/indahl.ai-code (local staging copies) hold the same files plus stale sagar.html / feed-entries.html.
- Collections ("indahl.ai studies, runs and models") were made by hand; no collection definition in the repo. Dropping the three datasets
  from that collection is an operator step on huggingface.co.
- claude-plugins/hf_mirror.sh: code model repos only; no list data.

## D. Zenodo
- ZENODO_MAP.json records "QIA List Pack" (concept 10.5281/zenodo.23874312, latest 24295081) and "IRIS List Pack" (concept
  10.5281/zenodo.23874314, latest 24311491). ledger/zenodo_sync.py makes a new version when the site file changes (ship.sh 7e).
  Published Zenodo versions cannot be deleted by us: operator decision (Zenodo support can hide a record).

## E. Public code mirror (public_mirror/indahl.ai, pushed by ledger/push_public.sh; rsync without --delete)
- Root copies: qia/list.json, iris/list.json, sagar/list.json, qia|iris -list-pack.zip/.sha256/-LICENSE.txt.
- code/list-packs (build_packs.py + src), from push_public.sh's package-source loop.
- code/repos/sagar/index (verified.jsonl, batch_*.json, *_draft.jsonl, tiers.json, queue_reachable.json, ...) and code/repos/sagar/data/index_seed.json:
  the SAGAR desk record exported at the pinned commit in ledger/public_code_repos.tsv. These are the study list in raw form.
- code/tape/leaves: hash-chained record; listed, never edited.
- code/site/pages.js: the built page bundle inside the code mirror (carries /qia/list etc. as pages, which is the web list itself).

## F. Text that points at list files
- build_site.py llms.txt / llms-full: "Machine-readable at https://indahl.ai/qia/list.json", "QIA List (JSON)", "IRIS List (JSON)", "QIA List Pack ... IRIS List Pack".
- build_site.py page(): JSON-LD Dataset with distribution /qia/list.json, /iris/list.json on /qia and /iris.
- indahl-ai/findable.py: Dataset distribution for the list packs.
- tools/desk_pack.py line 36: source cite "QIA List and IRIS List, https://indahl.ai/qia/list.json".
- Feed entries carry study pages (one entry per study page), not list rows: they are the web pages, kept.

## Plan (what changes)
1. Worker-only data: build_site.py writes public/_studies/{qia,iris,sagar}.json (filtered by indahl-ai/_by_author.json).
   worker.js answers 404 to any public request for /_studies/*, the three list.json paths and the list packs. api.js `studies()` reads
   /_studies/<division>.json through env.ASSETS (internal, not routed through the public handler). push_public.sh excludes _studies.
2. The /qia/list search: list.js no longer downloads the List. It asks the worker for one page at a time,
   GET /qia/list/rows?q=&code=&month=&page=&anchor= (50 rows and the filter options), computed server side from _studies/qia.json.
3. Builders stop making and advertising list files: copies.json entries removed; downloads.py stops rebuilding/checking list packs;
   build_site.py drops the pkgbox, Also lines, list-pack Data pack links, grab-and-go lines, llms lines, JSON-LD list distributions, the IRIS
   "download" link, the noscript download text and the three HF dataset names; iris_list.py stops copying list.json to public/;
   desk_pack.py OTHER drops the two packs; findable.py drops the list-pack distribution; zenodo_sync.py skips the List Pack records;
   push_public.sh deletes the list files, code/list-packs and code/repos/sagar/{index,data} from the mirror; hf_packs.py refuses the three HF names.
4. Ledger: pack.size.qia-list-pack and pack.size.iris-list-pack withdrawn through ledger.py.
5. removed_gate.py refuses any study-list file on a served root (list.json under qia/iris/sagar, *-list-pack*, studies files outside _studies).

## Done (17 Nov 2026, local only; nothing deployed, pushed or uploaded)
- What the MCP path reads now: indahl-ai/api.js `studies()` reads `/_studies/<qia|iris|sagar>.json` through `env.ASSETS` (internal binding,
  never routed through the public handler). build_site.py writes those three files on every build from qia_leads/matrix_page/list.json,
  iris_index/matrix_page/iris_list.json and sagar/site/list.json, each filtered by indahl-ai/_by_author.json.
- worker.js answers 404 (all hosts) to /_studies/*, /(qia|iris|sagar)/list.(json|csv) and the list packs; /record.json now redirects to /qia/list.
- /qia/list search: public/qia/list.js calls GET /qia/list/rows (indahl-ai/listrows.js, 50 rows a page plus the code and month options,
  same search and #anchor rules), so the browser never holds the whole List. Unit-tested in node on the real 2,585 rows.
- build_site.py deletes the old list files from public/ on every build and no longer prints any list link, JSON-LD download, llms line or
  the three private HF dataset names. Ledger rows pack.size.qia-list-pack and pack.size.iris-list-pack withdrawn (evidence: this file).
- removed_gate.py refuses a study-list file on a served root; copies in the public mirror and HF stage are reported until push_public.sh
  (which now deletes them, code/list-packs and code/repos/sagar/{index,data}) and the HF sync remove them.
- zenodo_sync.py skips the two List Pack records; hf_packs.py refuses the three study-list HF names and any list pack.

## Operator decisions
- Zenodo: the QIA and IRIS List Pack records (concept DOIs 10.5281/zenodo.23874312 and 23874314) stay published; hiding them needs Zenodo support.
- Hugging Face: indahl/qia-list, indahl/iris-list, indahl/qia-calibrated-studies are private, not deleted; remove them from the "indahl.ai
  studies, runs and models" collection on huggingface.co (no collection definition exists in the repo). indahl/indahl.ai keeps old list files
  in its git history after the next sync deletes them; squashing that history is a separate step.
- Data packs that carry study lists inside: OY Data Pack (json/oy_list.json, csv/oy_list.csv, 148 policy studies) and ARXIVDRIFT Data Pack
  (studies from the QIA and IRIS Lists that were revised). Kept as grab-and-go per "data packs still good".
- Scripts that read the retired /qia/list.json and will fail after deploy (private desk tools, not changed): iris_index/notices/qia/build_*_notices*.py
  (fetch https://indahl.ai/qia/list.json), qia_leads/recheck_published/fetch.py (reads public/qia/list.json); several one-off qia_leads add_*/fix_* scripts
  copy list.json into public/qia/ (build_site.py deletes it again and removed_gate.py refuses it).
- Stale page indahl-ai/qia/study/zenodo-19855345.html (study moved to zenodo-24287983 and redirected by the worker) still carries a QIA List Pack link.
