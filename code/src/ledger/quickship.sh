#!/bin/bash
# quickship.sh -- copy and layout changes live in about a minute (15 Nov 2026, the owner). Builds every page from source, runs the gates that protect page text (ledger, copies,
# statistics regression), deploys the worker, then pushes the public repo in the background. Data refreshes, packs, Zenodo and stamps stay in
# ship.sh, which the automatic ship still runs on schedule.
#   ledger/quickship.sh "what changed"
if [ -z "$SITE_LOCK_HELD" ]; then exec python3 "$(cd "$(dirname "$0")" && pwd)/site_lock.py" run --label "quickship.sh: $1" -- bash "$0" "$@"; fi
set -eo pipefail   # 21 Nov 2026 (control audit #6): without pipefail, `gate | tail -1` never refused
B=~/forge; L=$B/ledger; W=$B/cloudflare-workers/heuremen-door; MSG="${1:-Copy update}"; T0=$(date +%s)
_RUNG=0; ring() { _RUNG=1; echo "  $*"; printf '%s RING: QUICKSHIP %s\n' "$(date '+%Y-%m-%dT%H:%M:%S')" "$*" >> "$B/sagar/pipeline/pipe.log" 2>/dev/null || true; }
trap 'rc=$?; if [ $rc -ne 0 ] && [ $_RUNG -eq 0 ]; then ring "REFUSED or failed (exit $rc)"; fi' EXIT   # 22 Nov 2026 (PARTS.md audit): most refusals exited without a ring
echo "== BUILD"
python3 -I "$B/watch/headlines.py" >/dev/null 2>&1 || echo "  headlines: refresh failed, last headlines.json used"
for b in "$B/sagar/site/make_sagar.py" "$B/iris_index/matrix_page/iris_list.py" "$B/qia_leads/matrix_page/render_list.py" "$B/qia_leads/matrix_page/qia_page.py" "$B/atlas/build_atlasmap.py" "$B/iris_index/matrix_page/build_iris_page.py" "$B/oy_index/matrix_page/build_matrix_page.py"; do [ -f "$b" ] && (cd "$(dirname "$b")" && python3 "$(basename "$b")" >/dev/null 2>&1) || ring "builder FAILED: $b (its last page ships)"; done   # control audit #20
(cd "$B/indahl-ai" && set -o pipefail && python3 build_site.py | tail -1) || { echo "QUICKSHIP REFUSED: build_site.py failed, nothing deployed"; exit 1; }   # 18 Nov 2026: a failed page build used to deploy the old pages silently
(cd "$B/indahl-ai" && python3 qia_site.py | tail -1) || { echo "QUICKSHIP REFUSED: quantumidleaudit.com build failed"; exit 1; }   # 17 Nov 2026: the QIA business site rebuilds on every ship (was a hand step)   # 17 Nov 2026, the owner: consistency site-wide; removal automated in the page builders. The builder loop above now runs make_sagar.py (which writes the SAGAR ledger rows), iris_list.py and render_list.py; each drops ids in indahl-ai/removed_by_author.json
echo "== GATES"
CL=0; python3 "$L/check_ledger.py" > /tmp/check_ledger_last.txt || CL=$?; head -1 /tmp/check_ledger_last.txt; grep -v LIVESTALE /tmp/check_ledger_last.txt | sed -n "2,30p"
[ $CL = 0 ] || { echo "QUICKSHIP REFUSED: ledger drift (lines above)"; exit 1; }
python3 "$L/removed_gate.py" || { echo "QUICKSHIP REFUSED: a removed id is on a public page (lines above; ledger/remove.py <id> --why ...)"; exit 1; }   # 17 Nov 2026, the owner: consistency site-wide; removal automated in the page builders.
python3 "$L/copies.py" publish | tail -1 || { echo "QUICKSHIP REFUSED: copies.py publish failed"; ring "REFUSED: copies.py publish"; exit 1; }; python3 "$L/copies.py" check | tail -1 || { echo "QUICKSHIP REFUSED: copies.py check (a copy differs or is missing)"; ring "REFUSED: copies.py check"; exit 1; }
node "$B/indahl-ai/tests/stats_regression.mjs" > /tmp/stats_regression.log 2>&1 || { cat /tmp/stats_regression.log; echo "QUICKSHIP REFUSED: statistics regression"; exit 1; }
python3 "$B/indahl-ai/email_gate.py" | tail -1 || { echo "QUICKSHIP REFUSED: an email address in a built site file (email_gate.py)"; ring "REFUSED: email_gate.py"; exit 1; }
python3 "$L/no_confessions_gate.py" || { echo "QUICKSHIP REFUSED: public copy describes our own past errors (lines above)"; exit 1; }   # 15 Nov 2026 (the owner)
echo "== DEPLOY"
python3 "$B/ledger/scrub_personal.py" --site >/dev/null
python3 "$B/ledger/internal_gate.py" --site || { echo "QUICKSHIP REFUSED: internal material or a Hugging Face link in the site (ledger/internal_gate.py)"; exit 1; }   # 18 Nov 2026
set +e; CFT=$(security find-generic-password -s cloudflare-api-token-ship -w 2>/dev/null); WO=$(cd "$W" && if [ -n "$CFT" ]; then CLOUDFLARE_API_TOKEN="$CFT" CLOUDFLARE_ACCOUNT_ID=<cloudflare-account-id> npx wrangler deploy 2>&1; else npx wrangler deploy 2>&1; fi); WR=$?; unset CFT; set -e; echo "$WO" | grep -i -E "deployed|uploaded|error" | grep -v -i token | tail -3 || true   # 22 Nov 2026: deploy token from keychain cloudflare-api-token-ship (WR read right after the deploy)
[ $WR -eq 0 ] || { echo "QUICKSHIP REFUSED: wrangler deploy failed (exit $WR); deploy stamp not written"; ring "REFUSED: wrangler deploy failed (exit $WR)"; exit 1; }   # control audit #6: the stamp was written even after a failed deploy
NEWSTAMP=$("$L/deploy_hash.sh") && echo "$NEWSTAMP" > "$W/.last_deploy.sha" || true
echo "  live in $(( $(date +%s) - T0 )) s"
echo "== PUBLIC REPO (background)"
nohup bash -c "SHIP_DEPLOYED=1 '$L/push_public.sh' '$MSG' > /tmp/quickship_public.log 2>&1" >/dev/null 2>&1 &
echo "  pushing in the background, log /tmp/quickship_public.log"
