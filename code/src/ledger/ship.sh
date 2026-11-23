#!/bin/bash
# 10 Nov: a ship always runs under the kernel site lock (ledger/site_lock.py); a ship started outside it waits in line
if [ -z "$SITE_LOCK_HELD" ]; then exec python3 "$(cd "$(dirname "$0")" && pwd)/site_lock.py" run --label "ship.sh: $1" -- bash "$0" "$@"; fi
# ship.sh "what changed" -- ONE command from source to live (23 Oct 2026; his "a system like the big companies, so we stop updating by hand").
# ship.sh --check ["label"] -- the preflight (22 Nov 2026, PIPELINE_AUDIT P2 / A9): the same build and the same gates as a real ship, every
#   breach printed in one pass, then it stops before any deploy, commit or push. ledger/preflight.sh is one line that calls this.
# The big-company pattern on one Mac: single source of truth -> build -> gates -> deploy -> check -> commit -> verify live.
#   1 BUILD   re-render every canonical whose source changed (the paper via tectonic, Faults/Guards via ligera/render.sh, the bill via render_bill.py)
#   2 COPY    copies.py publish: every canonical over all its copies (copies.json)
#   3 GATES   check_ledger.py + copies.py check + site_gate.py (the specbook) and the rest below, plus (22 Nov P2) the cited-file check and
#             internal_gate.py --site, which used to sit in COMMIT/DEPLOY. --check stops here.
#   4 DEPLOY  npx wrangler deploy for indahl.ai if the worker's files changed (deploy token from keychain cloudflare-api-token-ship)
#   4a CHECKS (22 Nov P2 / A10) money_path_check.py + mcp_gate.py against live. If they fail after this ship deployed, `wrangler rollback`
#             puts the version that was live before back, the deploy stamp is not written, and the ship stops before any commit or push.
#             (A preview -> promote flow is not used: version preview URLs are off for heuremen-door, workers_dev = false, and turning them
#             on would publish every old version at a public workers.dev URL, removed studies included.) stats_regression.mjs is a local
#             test and runs in step 3.
#   5 COMMIT  heuremen.org and indahl-ai, if changed; push both (heuremen.org is served from its repo)
#   5b PUBLIC push_public.sh mirrors the deployed build to the public repos
#   6 VERIFY  copies.py live: every public URL byte-identical to its canonical (retries while caches refresh)
#   7 STAMPS  stamps.py release: OpenTimestamps on the release record + Internet Archive captures of what changed (logs, never fails a release)
# Rings (22 Nov P2 / A12): ship.sh never writes RING lines when the ship queue runs it (SHIP_RUNNER set). A refusal writes one FAIL line
# (step and reason) and every non-fatal problem one NOTE line to $SHIP_RESULT; ledger/ship_queue.py reads it and rings once. A ship run by
# hand (no SHIP_RUNNER) rings once itself from the EXIT trap. --check never rings; its caller prints the breaches.
set -euo pipefail
CHECK=0; if [ "${1:-}" = "--check" ]; then CHECK=1; MSG="check: ${2:-preflight}"; else MSG="${1:?usage: ship.sh \"what changed\" | ship.sh --check [label]}"; fi
B="$HOME/forge"; L="$B/ledger"; W="$B/cloudflare-workers/heuremen-door"
if [ $CHECK = 1 ]; then exec > >(tee "$L/.last_check_gates.txt") 2>&1; else exec > >(tee "$L/.last_ship_gates.txt") 2>&1; fi   # 10 Nov: the ship output is kept, so /build.json can carry the gate lines (indahl-ai/accountability.py buildinfo); a --check keeps its own file
AUTHOR=(-c "user.name=Heuremen LLC" -c user.email=349448817+indahl-ai@users.noreply.github.com)   # 15 Nov 2026, the owner: every public commit comes from Heuremen LLC (this line had been the claude-owner identity)
newer() { [ "$1" -nt "$2" ]; }
GT=$(mktemp -d /tmp/ship_gates.XXXXXX)   # 23 Nov 2026 (the designer review #10): each run keeps its own gate output (fixed /tmp paths were shared)
STEP=start; F=0; RES="${SHIP_RESULT:-$L/.ship_result.txt}"; : > "$RES"
one() { printf '%s' "$*" | tr '\n\t' '  ' | cut -c1-300; }
note() { echo "  NOTE: $*"; printf 'NOTE\t%s\t%s\n' "$STEP" "$(one "$*")" >> "$RES"; }   # non-fatal; the runner reports it in its one line
fail() { echo "SHIP REFUSED ($STEP): $*"; printf 'FAIL\t%s\t%s\n' "$STEP" "$(one "$*")" >> "$RES"; exit 1; }
refuse() { if [ $CHECK = 1 ]; then echo "== $(date +%H:%M:%S) REFUSED ($STEP): $*"; printf 'FAIL\t%s\t%s\n' "$STEP" "$(one "$*")" >> "$RES"; F=1; else fail "$@"; fi; }   # a gate: --check records it and runs the rest
trap 'rc=$?; if [ $rc -ne 0 ]; then grep -q "^FAIL" "$RES" 2>/dev/null || printf "FAIL\t%s\t%s\n" "$STEP" "stopped (exit $rc), see ledger/.last_ship_gates.txt" >> "$RES"; if [ $CHECK = 0 ] && [ -z "${SHIP_RUNNER:-}" ]; then printf "%s RING: SHIP FAILED at %s: %s (exit %s): %s\n" "$(date "+%Y-%m-%dT%H:%M:%S")" "$(grep -m1 "^FAIL" "$RES" | cut -f2)" "$(grep -m1 "^FAIL" "$RES" | cut -f3 | cut -c1-200)" "$rc" "$(one "$MSG" | cut -c1-150)" >> "$B/sagar/pipeline/pipe.log" 2>/dev/null; fi; fi; true' EXIT
# gate NAME TAILN cmd...: the whole output is kept in ledger/gates/NAME.txt; on failure the gate and its first lines are printed and refused
gate() { local n="$1" t="$2" rc; shift 2; mkdir -p "$L/gates"; set +e; "$@" > "$L/gates/$n.txt" 2>&1; rc=$?; set -e; tail -"$t" "$L/gates/$n.txt"
  if [ $rc -ne 0 ]; then echo "gate $n (exit $rc), first lines:"; grep -v '^[[:space:]]*$' "$L/gates/$n.txt" | head -15; refuse "gate $n (exit $rc): $(grep -v '^[[:space:]]*$' "$L/gates/$n.txt" | head -1 | cut -c1-200)"; fi; }
export SHIP_RUN=1   # 21 Nov 2026: builders run outside a ship refuse while one runs (a mid-ship local build made the front page differ from what was deployed)
# 23 Nov 2026 (house review: each ship repeated the 6-minute build and gates its preflight had just run). A clean preflight records a
# fingerprint of every source repo (HEAD + uncommitted changes). A real ship that starts within 20 minutes with the SAME fingerprint reuses
# that build and those gates and goes straight to DEPLOY. Any change in between, even one file, means a full build as before. One use only.
# Fingerprint = every source repo's HEAD + its uncommitted CODE files (scripts, templates, styles). Data files the riders rewrite every few
# minutes are left out on purpose: they changed between preflight and ship every time, so the first version never matched (tested 23 Nov:
# this one held steady through two minutes of running jobs). A ship that reuses therefore deploys the data as of its preflight, minutes old.
srcfp() { { for r in "$B/indahl-ai" "$B/calibrations" "$B/heuremen.org" "$L" "$B/faultsguards"; do git -C "$r" rev-parse HEAD 2>/dev/null || true; git -C "$r" status --porcelain 2>/dev/null | grep -E '\.(py|sh|js|mjs|css|toml|tex)$|/[^/]*\.html$' | grep -v -E '(^|/)(data|public|studies|_studies|out|runs|records)/|pages\.js$' || true; done; git --git-dir="$HOME/.house-ops.git" --work-tree="$B" status --porcelain 2>/dev/null | grep -E '\.(py|sh|js|mjs|css|toml)$' || true; } | shasum | cut -c1-16; }
REUSE=0; PF="$L/.preflight_ok"
if [ $CHECK = 0 ] && [ -f "$PF" ]; then read -r pfp pts < "$PF" || true; if [ "${pfp:-x}" = "$(srcfp)" ] && [ $(( $(date +%s) - ${pts:-0} )) -lt 1200 ]; then REUSE=1; echo "== $(date +%H:%M:%S) 1-3 REUSED: the preflight of $(date -r "${pts:-0}" +%H:%M:%S) built and gated these exact sources"; fi; fi
rm -f "$PF"
if [ $REUSE = 0 ]; then
STEP=build; echo "== $(date +%H:%M:%S) 1 BUILD"
for k in FAULTS:faults GUARDS:guards; do src="$B/faultsguards/source/${k%%:*}.html"; out="$B/heuremen.org/${k##*:}.pdf"   # 23 Nov 2026: built from faultsguards/source, the copy the package and the CI PDF check use (ligera held a stale copy with the old byline)
  if newer "$src" "$out"; then "$B/ligera/render.sh" "$src" "$out" || fail "ligera/render.sh ${k##*:} failed"; else echo "  ${k##*:}: up to date"; fi; done
if newer "$B/arxiv_one_readout/main.tex" "$B/heuremen.org/a-readout-is-not-an-idle.pdf"; then
  T=$(mktemp -d); cp -p "$B/arxiv_one_readout/main.tex" "$B/arxiv_one_readout/refs.bib" "$T/"; cp -Rp "$B/arxiv_one_readout/figures" "$T/"
  (cd "$T" && tectonic main.tex >/dev/null 2>&1) || fail "the paper does not compile"
  cp "$T/main.pdf" "$B/heuremen.org/a-readout-is-not-an-idle.pdf"; cp "$T/main.pdf" "$B/arxiv_one_readout/main.pdf"; rm -rf "$T"; echo "  paper: rebuilt"
else echo "  paper: up to date"; fi
# 30 Oct: the public repo builds the paper from its own copy of the source and checks it against the live PDF (paper workflow); keep that
# copy equal to ours on every ship, so the public build never runs on stale source.
PP="$B/public_mirror/heuremen.org/paper"; if [ -d "$PP" ]; then cp "$B/arxiv_one_readout/main.tex" "$B/arxiv_one_readout/refs.bib" "$PP/"
  for f in "$B"/arxiv_one_readout/figures/*.py "$B/arxiv_one_readout/figures/README.md"; do [ -f "$f" ] && cp "$f" "$PP/figures/"; done; echo "  paper source: synced to the public repo"; fi
if newer "$B/indahl-ai/qia_template/QIA-2026-001.json" "$B/indahl-ai/qia_template/QIA-2026-001.pdf"; then
  (cd "$B/indahl-ai/qia_template" && python3 render_bill.py QIA-2026-001.json) || fail "render_bill.py failed"; else echo "  bill: up to date"; fi
python3 "$L/sweep_backups.py" || fail "sweep_backups.py failed"   # 11 Nov: backup-named files and folders are MOVED to archive_private/public_backups before anything is built or gated
python3 "$B/census_index/refresh_page.py" || note "census refresh_page.py FAILED: the last page and rows are kept, check_ledger still guards drift"   # 11 Nov: CENSUS page tables and census.* ledger rows follow the latest desk run (ledger before surface)
python3 "$B/neo_index/refresh_page.py" || note "neo refresh_page.py FAILED: the last page and rows are kept, check_ledger still guards drift"   # 11 Nov: NEO page tables and neo.* ledger rows follow the latest desk run (ledger before surface)
python3 "$B/quake_index/refresh_page.py" || note "quake refresh_page.py FAILED: the last page and rows are kept, check_ledger still guards drift"   # 11 Nov: QUAKE page tables and quake.* ledger rows follow the latest desk run (ledger before surface)
# python3 "$B/ledger/roadmap_sync.py"   # 19 Nov 2026: /changes archived (the owner); sync step off   # 11 Nov: /changes follows the record (every live desk listed, open items recomputed), no hand edits
python3 "$B/qia_leads/matrix_page/render_list.py" || fail "qia_leads/matrix_page/render_list.py failed"   # 11 Nov: the /qia/list table is rendered from list.json (one source for the page and the download)
for b in "$B/sagar/site/make_sagar.py" "$B/iris_index/matrix_page/iris_list.py" "$B/qia_leads/matrix_page/qia_page.py" "$B/atlas/build_atlasmap.py" "$B/iris_index/matrix_page/build_iris_page.py" "$B/oy_index/matrix_page/build_matrix_page.py"; do (cd "$(dirname "$b")" && python3 "$(basename "$b")" >/dev/null 2>&1) || note "page builder FAILED: $b (its last page ships)"; done   # 15 Nov 2026 (the owner): every page is built from its source on every ship
mkdir -p "$L/gates"; HL=0; HEADLINES_RING_LOG="$L/gates/headlines.ring" python3 -I "$B/watch/headlines.py" > "$L/gates/headlines.txt" 2>&1 || HL=$?; grep -E 'skipped|publish FAILED|refused' "$L/gates/headlines.txt" | head -5 || true; [ -s "$L/gates/headlines.ring" ] && { note "headlines: $(tr '\n' ' ' < "$L/gates/headlines.ring" | cut -c1-300)"; : > "$L/gates/headlines.ring"; }; [ $HL = 0 ] || note "headlines refresh FAILED (exit $HL), pages use the last headlines.json: $(tail -1 "$L/gates/headlines.txt" | cut -c1-200)"   # 21 Nov 2026 (control audit #21): output kept in ledger/gates/headlines.txt (headlines.py rings its own skipped/publish FAILED)   # 15 Nov 2026 (the owner): headlines re-read from the live feeds every ship, not only on the bus, so a desk refreshed between ticks never leaves a page headline behind its own pack
python3 "$L/downloads.py" refresh || fail "downloads.py refresh failed"   # 11 Nov: every download is re-made from its source (copies.py publish), the List packs and the QIA Research Package are rebuilt when a file inside differs from its source, pack sizes re-read, all before build_site.py reads them
{ python3 "$B/indahl-ai/reproduce_kits.py" refresh | tail -30; } || true   # 10 Nov: remake the desk reproduce kits the ledger or a live feed has moved past (never fails here, the gate in step 3 decides)
(cd "$B/indahl-ai" && python3 build_site.py) || fail "build_site.py failed"
# 23 Nov 2026 (separate lanes): quantumidleaudit.com is no longer built here; it has its own worker and ship (ledger/ship_qia.sh)
python3 "$L/downloads.py" refresh --post || { [ $? -eq 10 ] && { (cd "$B/indahl-ai" && python3 build_site.py) && python3 "$L/downloads.py" refresh --post; }; } || fail "downloads.py refresh --post failed"   # 11 Nov: packs made from built pages (OY) are rebuilt after the pages; exit 10 = one changed, so the site is built once more with its new size and ledger row, and the pack's input record is re-read against those pages (contents unchanged, so no second pack)
# python3 "$L/receipts.py" build   # 15 Nov 2026: receipts are internal, no public /r/ pages
STEP=copy; echo "== $(date +%H:%M:%S) 2 COPY";  gate copies_publish 1 python3 "$L/copies.py" publish
STEP=gates; echo "== $(date +%H:%M:%S) 3 GATES"; CL=0; python3 "$L/check_ledger.py" > $GT/check_ledger_last.txt || CL=$?; head -1 $GT/check_ledger_last.txt; grep -v LIVESTALE $GT/check_ledger_last.txt | sed -n "2,30p"; [ $CL = 0 ] || refuse "ledger drift (check_ledger.py): $(grep -v LIVESTALE $GT/check_ledger_last.txt | sed -n 2p | cut -c1-200)"   # 15 Nov 2026: print every blocking ledger line, not only the last one
python3 "$L/removed_gate.py" || refuse "a removed id is on a public page (removed_gate.py; ledger/remove.py <id> --why ...)"   # 17 Nov 2026, the owner: consistency site-wide; removal automated in the page builders
gate copies_check 1 python3 "$L/copies.py" check   # restored 15 Nov 2026: the comment above had swallowed it
DG=$(python3 "$L/downloads.py" gate 2>&1) || true; if ! echo "$DG" | grep -q "stale: 0" && ! echo "$DG" | grep "STALE" | grep -vq "its feed moved past the pack"; then echo "downloads: a live feed moved mid-ship, packs rebuilt once and re-checked"; python3 "$L/downloads.py" refresh >/dev/null 2>&1; DG=$(python3 "$L/downloads.py" gate 2>&1) || true; fi; echo "$DG" | tail -1; echo "$DG" | grep -q "stale: 0" || { echo "$DG" | head -20; refuse "a download is stale (downloads.py gate)"; }   # 11 Nov: downloads gate, a stale download or pack stops the ship (runs once)
BG=$(python3 "$L/backup_patterns.py" 2>&1) || true; echo "$BG" | tail -1; echo "$BG" | grep -q "backups gate: 0 in public" || { echo "$BG" | head -20; refuse "a backup file is in the served folder or the public mirror (backup_patterns.py)"; }   # 11 Nov: no backup-named file or folder is served or mirrored
SG=0; python3 "$L/spelling_gate.py" > $GT/spelling_gate_last.txt || SG=$?; tail -12 $GT/spelling_gate_last.txt; [ $SG = 0 ] || refuse "British spelling on our own pages (spelling_gate.py)"   # 21 Nov 2026 (the owner): every built page of ours, American spelling; quotes and study pages are other people's words
NG=0; python3 "$L/name_gate.py" > $GT/name_gate_last.txt || NG=$?; tail -12 $GT/name_gate_last.txt; [ $NG = 0 ] || refuse "plural name of the Heuremen Standard on our own pages (name_gate.py)"   # 21 Nov 2026 (owner: "Heuremen Standard V1.1", never "Standards"): the name lives in faultsguards/CURRENT.json
LG=0; python3 "$L/link_gate.py" > $GT/link_gate_last.txt || LG=$?; tail -25 $GT/link_gate_last.txt; [ $LG = 0 ] || refuse "a dead link on our own pages (link_gate.py)"   # 21 Nov 2026 (site link check): every same-site href/src on the built pages of indahl.ai and quantumidleaudit.com resolves to a built page, a served file or a worker route
python3 "$L/live_headlines.py" seed || refuse "live_headlines seed failed"   # 22 Nov 2026 (cause of the 21:29 refusal): a desk spec with no ledger row refused every bundled request; rows come from the reviewed spec, idempotent
gate one_description 1 python3 "$L/one_desc_gate.py"   # 22 Nov 2026: one description per desk, in seo/seo_copy.json
gate copy_damage 1 python3 "$L/copy_damage_gate.py"   # 22 Nov 2026: spliced or broken copy (the /chronos splice)
gate headline_cover 8 python3 "$L/headline_cover_gate.py"   # 21 Nov 2026: each headline card's number equals its ledger row and the desk kit computes the same field; refuses
DL=0; DESK_GATE_LOG="$L/gates/desk_list.ring" python3 "$L/desk_list_gate.py" --quiet > "$L/gates/desk_list.txt" 2>&1 || DL=$?; tail -3 "$L/gates/desk_list.txt"; : > "$L/gates/desk_list.ring" 2>/dev/null; [ $DL = 0 ] || note "desk list disagrees with ledger/desks.json (ledger/gates/desk_list.txt)"; [ $DL = 0 ] || echo "!! DESK LIST: a file carries its own desk list that disagrees with ledger/desks.json (rung to pipe.log by the gate; warns, never refuses)"   # 21 Nov 2026 HARD row 26
gate site_gate 1 python3 "$B/heuremen-specbook/site_gate.py"   # restored 11 Nov: it had been commented out by the downloads edit
gate house_terms 3 python3 "$L/house_terms.py" served --fix   # 22 Nov 2026 (the owner: no names, no handles anywhere public): every served file (worker public/ and the pages pages.js imports) is scrubbed of house handles, house names and links to deleted accounts (https://indahl.ai/downloads claude-owner), then checked; a hit refuses the ship (ledger/house_terms.py)
bash "$L/runcheck_gate.sh" || refuse "the Check a Run page and the qia-check package disagree (runcheck_gate.sh)"
node "$B/indahl-ai/tests/stats_regression.mjs" > $GT/stats_regression.log 2>&1 || { cat $GT/stats_regression.log; refuse "the statistics checker failed its regression tests (stats_regression.mjs)"; }   # 15 Nov 2026 (the referee): pins the &lt; reader bug, unicode minus, df rounding and the slash rule
gate source_gate 1 python3 "$B/qia_leads/matrix_page/source_gate.py"
python3 "$B/qia_leads/matrix_page/render_list.py" --check || refuse "the /qia/list page and list.json disagree (render_list.py --check)"   # 11 Nov
gate findable 1 python3 "$B/indahl-ai/findable.py" --gate   # 10 Nov: every served page's JSON-LD parses and each Dataset has the fields Google requires
gate entities 1 python3 "$B/indahl-ai/entities.py" --gate   # 10 Nov evening: every entity page traces its rows to a served page or a brand-page row
gate forecasters 1 python3 "$B/indahl-ai/forecasters.py" --gate   # 10 Nov: every /forecasters number traces to a desk feed or a ledger row, labels sit where the drawn intervals sit
gate email_gate 1 python3 "$B/indahl-ai/email_gate.py"   # 10 Nov: no email address in any built site file (newsletter subscribers live only in the private KV)
python3 "$L/no_confessions_gate.py" || refuse "public copy describes our own past errors (no_confessions_gate.py)"   # 15 Nov 2026 (the owner)
gate notify 1 "$B/notify_state/venv/bin/python" "$B/indahl-ai/notify.py" --gate   # 10 Nov: every feed, calendar and OPML file parses (feedparser, icalendar), every calendar event cites its source schedule
gate accountability 1 python3 "$B/indahl-ai/accountability.py" gate   # 10 Nov: the accountability pages exist, keep the public-copy rules, /security/self matches its check file
gate alert_receipts 1 python3 "$B/indahl-ai/alert_receipts.py" gate   # 10 Nov: the alert receipt chain links, and no receipt holds subscriber data
gate reproduce_kits 25 python3 "$B/indahl-ai/reproduce_kits.py" gate   # 10 Nov: every desk reproduce kit, rerun in a clean folder from its own contents, prints the headline the ledger covers and the live feed serves
# every file a live ledger row cites on the site must exist (23 Oct: shot_grid.text was cited, never committed, and the Zenodo build caught it).
# 22 Nov 2026 (P2): the existence check is a gate here; step 5 adds those files to the commit.
python3 - "$B" <<'PY' || refuse "a ledger row cites a site file that does not exist"
import json, os, sys
B = sys.argv[1]; need = set()
for l in open(B + '/ledger/ledger.jsonl'):
    r = json.loads(l); f = r.get('source', {}).get('file', '')
    if r.get('status') == 'live' and f.startswith('heuremen.org/'): need.add(f[len('heuremen.org/'):])
gone = sorted(f for f in need if not os.path.exists(B + '/heuremen.org/' + f))
if gone: print('  missing:', gone); sys.exit(1)
PY
python3 "$B/ledger/internal_gate.py" --site || refuse "internal material in the site (internal_gate.py --site)"   # 22 Nov 2026 (PARTS.md audit): quickship ran this gate, ship.sh did not
fi   # end of the build and gates a fresh preflight lets a ship reuse
if [ $CHECK = 1 ] && [ $F = 0 ]; then echo "$(srcfp) $(date +%s)" > "$PF"; fi
if [ $CHECK = 1 ]; then if [ $F = 0 ]; then echo "preflight: all gates clean (ship.sh --check: the ship's own build and gates; nothing deployed, committed or pushed)"; else echo "preflight: fix the breaches above before ship_request.sh"; fi; exit $F; fi
STEP=deploy; echo "== $(date +%H:%M:%S) 4 DEPLOY"
STAMP="$W/.last_deploy.sha"; NOW=$("$L/deploy_hash.sh"); DEPLOYED=0; PREV=""; CFT=""   # 10 Nov: one hash for ship.sh and push_public.sh (deploy_hash.sh), so the two lists never drift
wr() { ( cd "$W" && if [ -n "$CFT" ]; then CLOUDFLARE_API_TOKEN="$CFT" CLOUDFLARE_ACCOUNT_ID=<cloudflare-account-id> npx wrangler "$@"; else npx wrangler "$@"; fi ) 2>&1; }   # 22 Nov 2026: deploy token from keychain cloudflare-api-token-ship, passed explicitly
if [ "$(cat "$STAMP" 2>/dev/null)" != "$NOW" ]; then
  CFT=$(security find-generic-password -s cloudflare-api-token-ship -w 2>/dev/null) || CFT=""
  [ -n "$CFT" ] || note "keychain cloudflare-api-token-ship missing: wrangler uses its own login"
  # 22 Nov 2026 (P2): the version taking 100% of traffic before this deploy is the rollback target if the checks fail
  PREV=$(wr deployments status --json | python3 -c 'import json,sys; t=sys.stdin.read(); d=json.loads(t[t.index("{"):]); v=sorted(d.get("versions") or [], key=lambda x: -x.get("percentage", 0)); print(v[0]["version_id"] if v else "")' 2>/dev/null) || PREV=""
  [ -n "$PREV" ] && echo "  live before this deploy: version $PREV" || note "could not read the live version (wrangler deployments status): no rollback target for this deploy"
  set +e; WO=$(wr deploy); WR=$?; set -e; echo "$WO" | grep -i -E "deployed|uploaded|version id|error" | grep -v -i token | tail -4 || true
  [ $WR -eq 0 ] || fail "the indahl.ai worker deploy failed (wrangler exit $WR): $(echo "$WO" | grep -i -m1 error | grep -v -i token | cut -c1-200); live is unchanged, the deploy stamp is not written"   # 21 Nov 2026 (control audit #19)
  DEPLOYED=1
else echo "  indahl.ai worker: unchanged"; fi
STEP=checks; echo "== $(date +%H:%M:%S) 4a CHECKS (live after deploy)"; CHK=""
# the two checks write their findings to ledger/gates/*.ring, not pipe.log: the ship's one ring (ship_queue.py) carries them
MP=0; MONEY_PATH_LOG="$L/gates/money_path.ring" python3 "$L/money_path_check.py" --quiet --part inquiry > "$L/gates/money_path.txt" 2>&1 || MP=$?; cat "$L/gates/money_path.txt"; [ $MP = 0 ] && echo "  money path: ok" || CHK="money_path_check: $(grep -m1 '^FAIL' "$L/gates/money_path.txt" | cut -c6-200)"   # what a visitor gets on quantumidleaudit.com (home + Check a run box, demos, /inquiries, every Check a run file, a live runcheck.js run on ibm_fez)
if [ -f "$L/mcp_gate.py" ]; then MG=0; MCP_GATE_LOG="$L/gates/mcp_gate.ring" python3 "$L/mcp_gate.py" --quiet > "$L/gates/mcp_gate.txt" 2>&1 || MG=$?; cat "$L/gates/mcp_gate.txt"; [ $MG = 0 ] && echo "  mcp gate: ok" || CHK="${CHK:+$CHK; }mcp_gate: $(grep -m1 '^FAIL' "$L/gates/mcp_gate.txt" | cut -c6-200)"; fi
POSTFAIL=0
if [ -n "$CHK" ]; then
  if [ $DEPLOYED = 1 ] && [ -n "$PREV" ]; then
    set +e; RB=$(wr rollback "$PREV" -y -m "ship checks failed"); RBR=$?; set -e; echo "$RB" | grep -v -i token | tail -3
    unset CFT
    if [ $RBR -eq 0 ]; then fail "checks failed after deploy, live rolled back to version $PREV (deploy stamp not written, nothing committed or pushed): $CHK"
    else fail "checks failed after deploy and the ROLLBACK FAILED (wrangler exit $RBR): live serves the new version: $CHK"; fi
  elif [ $DEPLOYED = 1 ]; then unset CFT; fail "checks failed after deploy, no rollback target was read, live serves the new version: $CHK"
  else POSTFAIL=1; note "checks failed with the worker unchanged (nothing to roll back): $CHK"; fi
fi
unset CFT
if [ $DEPLOYED = 1 ]; then echo "$NOW" > "$STAMP"; { python3 "$L/stamps.py" manifest || true; }; fi   # the stamp is written only after the checks pass; 10 Nov: the manifest of what this deploy sent (stamps.py)
STEP=commit; echo "== $(date +%H:%M:%S) 5 COMMIT"
python3 - "$B" <<'PY' || fail "could not add the cited site files to the heuremen.org commit"
import json, subprocess, sys
B = sys.argv[1]; need = set()
for l in open(B + '/ledger/ledger.jsonl'):
    r = json.loads(l); f = r.get('source', {}).get('file', '')
    if r.get('status') == 'live' and f.startswith('heuremen.org/'): need.add(f[len('heuremen.org/'):])
subprocess.run(['git', '-C', B + '/heuremen.org', 'add', '--'] + sorted(need), check=True)
PY
for r in heuremen.org indahl-ai; do cd "$B/$r"; git add -u; git add -A -- '*.pdf' 2>/dev/null || true; [ "$r" = indahl-ai ] && git add -A -- oy 2>/dev/null || true
  if git diff --cached --quiet; then echo "  $r: nothing to commit"; else git "${AUTHOR[@]}" commit -q -m "$MSG" || fail "the $r commit was refused (pre-commit hook or git error); nothing pushed"; echo "  $r: $(git log --oneline -1)"; fi; done   # 23 Nov 2026 (outside review #22): a refused commit used to pass silently inside if/else
cd "$B/heuremen.org"; PR=0; PO=$(git push -q origin main 2>&1) || PR=$?; echo "$PO" | tail -2; if [ $PR -eq 0 ]; then echo "  heuremen.org pushed"; else echo "  heuremen.org PUSH FAILED (indahl-ai/heuremen.org refused it; live heuremen.org is NOT updated)"; fi   # 19 Nov 2026 (the owner: full quarantine): heuremen.org is served from indahl-ai/heuremen.org
[ $PR -eq 0 ] || echo "$(date +%Y-%m-%dT%H:%M:%S) RING: HEUREMEN.ORG PUSH FAILED: the site deployed but git push of heuremen.org was refused (live heuremen.org may lag git)" >> "$B/sagar/pipeline/pipe.log"   # 23 Nov 2026 (the designer review #11): its own ring, not only a note
cd "$B/indahl-ai"; set +e; IO=$(git push -q 2>&1); IR=$?; set -e; echo "$IO" | sed -E 's#https://[^@]*@#https://#' | tail -2 || true; [ $IR -eq 0 ] || note "indahl-ai PUSH FAILED (exit $IR)"
# 21 Nov 2026 (control audit #18): both push results are written for watch/alerts_check.py (it was print-only, the indahl-ai one hidden)
python3 -c 'import json,sys,time; pr,ir=int(sys.argv[1]),int(sys.argv[2]); print(json.dumps({"at": time.strftime("%Y-%m-%d %H:%M"), "ok": pr == 0 and ir == 0, "error": ("heuremen.org push exit %d; " % pr if pr else "") + ("indahl-ai push exit %d" % ir if ir else "")}))' "$PR" "$IR" > "$L/ship_push_status.json" || true
[ $PR -eq 0 ] || note "heuremen.org PUSH FAILED (exit $PR): live heuremen.org is NOT updated"
STEP=public; echo "== $(date +%H:%M:%S) 5b PUBLIC REPOS (started in the background: ledger/public_push_after.sh, log ledger/.last_public_push.txt)"
python3 "$B/indahl-ai/accountability.py" buildinfo 2>&1 | tail -1 || true   # 10 Nov: the release record at /build.json (commits, deploy fingerprint, gate lines, pages hash), KV build_json
nohup bash "$L/public_push_after.sh" "$MSG" > "$L/.last_public_push.txt" 2>&1 &   # 23 Nov 2026: off the critical path (it was 5 min 47 s of every ship)
echo "== $(date +%H:%M:%S) 5c INDEXNOW"; python3 "$B/tools/indexnow.py" 2>&1 | tail -1 || true
# 7 STAMPS (10 Nov): outside timestamps after a verified release. release_<commit>.json (commit, ledger hash, manifest of every deployed file)
# stamped with OpenTimestamps, changed public URLs sent to the Internet Archive in the background, paced. Never fails a release.
stamps() { echo "== $(date +%H:%M:%S) 7 STAMPS"; set +e; python3 "$L/stamps.py" release 2>&1 | tail -4; echo "== $(date +%H:%M:%S) 7b WEBSUB"; python3 "$B/indahl-ai/websub_ping.py" ship 2>&1 | tail -1; echo "== $(date +%H:%M:%S) 7c LEDGER BACKUP"; git -C "$L" push -q backup HEAD:main 2>&1 | tail -1 && { rm -f "$L/ledger_backup_status.json"; echo "  ledger pushed to the private backup"; } || { echo "  ledger backup push FAILED"; echo "{\"at\": \"$(date -u +%FT%TZ)\", \"ok\": false}" > "$L/ledger_backup_status.json"; }; echo "== $(date +%H:%M:%S) 7d ARCHIVE BACKUP"; bash "$L/archive_push.sh" 2>&1 | tail -2; echo "== $(date +%H:%M:%S) 7e ZENODO"; python3 "$L/zenodo_sync.py" --publish 2>&1 | tail -20 || echo "  zenodo sync crashed (status file written)"; [ -f "$L/zenodo_status.json" ] || true; set -e; return 0; }   # 11 Nov: 7d pushes archive_private to the private repo, 7e makes a new Zenodo version of each record whose site files changed (24 h guard per record), both after the deploy verified and every gate was 0, neither fails a ship; a failure writes archive_backup_status.json / zenodo_status.json for alerts_check.py   # 10 Nov: 7b tells the WebSub hub which feeds changed (never fails a release, failures alert the operator)
STEP=verify; echo "== $(date +%H:%M:%S) 6 VERIFY"   # 23 Nov 2026 (the referee review S2): stamps (Zenodo, Internet Archive, OpenTimestamps) run only when the live checks passed
for i in 1 2 3 4 5 6; do python3 "$L/copies.py" live > $GT/ship_live.txt 2>&1 && { tail -1 $GT/ship_live.txt; if [ $POSTFAIL = 0 ]; then stamps; echo "SHIP: deployed and verified"; exit 0; fi; STEP=checks; fail "deployed and verified, but the live checks failed with the worker unchanged: $CHK"; }; sleep 20; done
cat $GT/ship_live.txt; fail "live does not match yet (copies.py live): $(grep -m1 'LIVE OFF' $GT/ship_live.txt | cut -c1-200)"
