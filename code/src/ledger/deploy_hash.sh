#!/bin/bash
# deploy_hash.sh (10 Nov 2026): the ONE hash of everything the indahl.ai worker deploy sends. ship.sh step 5 compares it with the deploy stamp
# (cloudflare-workers/heuremen-door/.last_deploy.sha) to decide whether to deploy, and push_public.sh compares it with the same stamp to decide
# whether the local build is the deployed one. Both call this file, so their lists can never drift apart again (they did on 10 Nov when ship.sh
# gained brand/ and push_public.sh did not, and the public repo got code only for the rest of the day).
# Files: worker.js, wrangler.toml, every indahl-ai/*.js (the worker imports them), every indahl-ai/*.html, style.css, every file under the page
# folders below that exists, and the worker's public folder. Add a page folder here, once, when a build starts writing one.
# 22 Nov 2026 (pagebuilder): the worker folder's desk_*.js modules (desk_template.js) too, so a template-only change deploys.
B="$HOME/forge"; S="$B/indahl-ai"; W="$B/cloudflare-workers/heuremen-door"
# 21 Nov 2026 (control audit #14): the hand list missed sagar/, connect/ and census/, which pages.js imports, so a ship that only edited pages
# there read "worker unchanged" and deployed nothing. Every folder any indahl-ai/*.js or *.mjs imports from (from './<dir>/...) is now added to it.
IMP=$(cat "$S"/*.js "$S"/*.mjs 2>/dev/null | grep -oE "from ['\"]\./[A-Za-z0-9_-]+/" | sed -E "s#from ['\"]\./##; s#/##" | sort -u)
DIRS=(); for d in $(printf '%s\n' oy atlas iris qia hermes darkwave media brand receipts corrections week alerts newsletter security e $IMP | awk '!s[$0]++'); do [ -d "$S/$d" ] && DIRS+=("$S/$d"); done
# 22 Nov 2026: receipts/stamps/ is written by stamps.py release AFTER each deploy (it stamps the deployed build), so it is left out of the hash;
# otherwise every ship changed its own hash and the next ship redeployed for nothing. Those files ride the next real deploy.
{ cat "$W/worker.js" "$W"/desk_*.js "$W/wrangler.toml" "$S"/*.js "$S"/*.mjs "$S"/*.html "$S/style.css"   # 18 Nov 2026: *.mjs too (qia_measured.mjs, connector_tool.mjs are imported by tools_qia.js)
  find "${DIRS[@]}" "$W/public" -type f -not -path "$W/public/receipts/stamps/*" -print0 | sort -z | xargs -0 cat; } | shasum -a 256 | cut -c1-16
