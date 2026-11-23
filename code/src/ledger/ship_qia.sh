#!/bin/bash
# ship_qia.sh "what changed"  (22 Nov 2026, QIA split): the short ship path for quantumidleaudit.com. It never waits on the indahl.ai site lock
# and never touches heuremen-door: it takes its own kernel lock (ledger/.qia_site.flock), builds the QIA pages, gates them, deploys only the
# qia-site worker (cloudflare-workers/qia-site), checks live, and rolls the worker back on a failed check.
#   1 BUILD   wipe cloudflare-workers/qia-site/public/ (so a page removed from the builders cannot stay live), copy qia-site/static/
#             (the sample report PDF and cover), run indahl-ai/qia_site.py (which runs calibrations/site/console/build.py) into public/_qiasite
#   2 GATES   site_gate.py --qia (the specbook wording rules on every QIA page and script), house_terms.py check (no house handles or names),
#             internal_gate.py --tree (no internal material, keys or ids), the private-names scan (ledger/private_names.txt, home address)
#   3 DEPLOY  wrangler deploy of qia-site only (keychain cloudflare-api-token-ship, never printed); the version live before is the rollback target
#   4 CHECKS  only when the zone routes point at qia-site (ledger/qia_route.py): every built page and file byte-identical live, /method 404,
#             money_path_check.py. A failed check runs `wrangler rollback <previous version>` and the ship fails.
#   0 SAVE    (22 Nov) ledger/save_source.sh commits and pushes every source repo first; a scan hit or failed push refuses the ship
# A failure writes ONE line to sagar/pipeline/pipe.log: `<time> RING: QIA SHIP FAILED at <step>: <reason> (<what changed>)`.
# Rollback of the cutover itself (send quantumidleaudit.com back to heuremen-door): python3 ~/forge/ledger/qia_route.py door
B="$HOME/forge"; L="$B/ledger"
if [ -z "${QIA_LOCK_HELD:-}" ]; then
  exec python3 -c 'import fcntl, os, sys
f = open(sys.argv[1], "a+"); os.set_inheritable(f.fileno(), True)
try: fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError: print("ship_qia: another QIA ship holds ledger/.qia_site.flock, waiting in line"); sys.stdout.flush(); fcntl.flock(f, fcntl.LOCK_EX)
f.truncate(0); f.write("%d %s\n" % (os.getpid(), " ".join(sys.argv[3:]))); f.flush()
os.environ["QIA_LOCK_HELD"] = "1"; os.execvp("bash", ["bash"] + sys.argv[2:])' "$L/.qia_site.flock" "$0" "$@"
fi
set -uo pipefail
MSG="${1:?usage: ship_qia.sh \"what changed\"}"
Q="$B/cloudflare-workers/qia-site"; OUT="$Q/public/_qiasite"; PIPE="$B/sagar/pipeline/pipe.log"; LOG="$L/.last_ship_qia.txt"
exec > >(tee "$LOG") 2>&1
T0=$(date +%s); STEP=start; PREV=""; DEPLOYED=0; CFT=""
one() { printf '%s' "$*" | tr '\n\t' '  ' | cut -c1-200; }
fail() { echo "QIA SHIP REFUSED ($STEP): $*"; printf '%s RING: QIA SHIP FAILED at %s: %s (%s)\n' "$(date '+%Y-%m-%dT%H:%M:%S')" "$STEP" "$(one "$*")" "$(one "$MSG" | cut -c1-120)" >> "$PIPE"; echo "ship_qia: $(( $(date +%s) - T0 )) s"; exit 1; }
wr() { ( cd "$Q" && env -u CLOUDFLARE_API_TOKEN CLOUDFLARE_API_TOKEN="$CFT" CLOUDFLARE_ACCOUNT_ID=<cloudflare-account-id> /opt/homebrew/bin/npx wrangler "$@" ) 2>&1 | { grep -v -i token || true; }; }

STEP=save_source; echo "== 0 SAVE SOURCE (every source repo committed and pushed before anything is built; ledger/save_source.sh)"
SO=$(SAVE_SCOPE=qia bash "$L/save_source.sh" "$MSG" 2>&1); SR=$?; echo "$SO" | tail -8   # 23 Nov 2026: qia.com files only, own lock
[ $SR -eq 0 ] || fail "save_source: $(echo "$SO" | grep -m1 -E 'REFUSED|FAILED' | sed 's/^ *//')"
STEP=build; echo "== 1 BUILD ($MSG)"
rm -rf "$Q/public"; mkdir -p "$OUT" || fail "could not make $OUT"
cp -p "$Q/static/"* "$OUT/" || fail "could not copy qia-site/static"
BO=$(cd "$B/indahl-ai" && QIA_SITE_OUT="$OUT" python3 qia_site.py 2>&1) || fail "qia_site.py failed: $(echo "$BO" | tail -1)"
echo "$BO" | tail -3
[ -e "$OUT/method.html" ] && fail "method.html was built (the Method page is removed)"
[ -s "$OUT/index.html" ] && [ -s "$OUT/robots.txt" ] && [ -s "$OUT/sitemap.xml" ] || fail "the build is missing index.html, robots.txt or sitemap.xml"
echo "  built: $(cd "$OUT" && ls | tr '\n' ' ')"

STEP=gates; echo "== 2 GATES"
G=$(python3 "$B/heuremen-specbook/site_gate.py" --qia "$OUT" 2>&1) || fail "site_gate --qia: $(echo "$G" | grep -m1 BREACH)"; echo "  $(echo "$G" | tail -1)"
G=$(python3 "$L/house_terms.py" check "$Q/public" 2>&1) || fail "house_terms: $(echo "$G" | head -1)"; echo "  $(echo "$G" | tail -1)"
G=$(python3 "$L/internal_gate.py" --tree "$Q/public" 2>&1) || fail "internal_gate: $(echo "$G" | grep -v '^\s*$' | head -1)"; echo "  internal gate: clean"
G=$(python3 - "$Q/public" "$L" <<'PY'
import os, re, sys
top, L = sys.argv[1], sys.argv[2]
names = re.compile(open(L + '/private_names.txt').read().split('\n')[0].strip(), re.I)
home = open(L + '/private_scan_words.txt').read().split('\n')[1].strip()
hits = []
for d, _, fs in os.walk(top):
    for f in fs:
        if not re.search(r'\.(html|txt|xml|js|css|json|svg)$', f): continue
        t = open(os.path.join(d, f), encoding='utf-8', errors='ignore').read()
        if names.search(t): hits.append(f + ': private name')
        if home and home in t: hits.append(f + ': home address')
print('private names: %s' % ('; '.join(hits) if hits else 'clean')); sys.exit(1 if hits else 0)
PY
) || fail "$G"; echo "  $G"

STEP=deploy; echo "== 3 DEPLOY (qia-site only)"
CFT=$(security find-generic-password -s cloudflare-api-token-ship -w 2>/dev/null) || CFT=""
[ -n "$CFT" ] || fail "keychain cloudflare-api-token-ship missing"
PREV=$(wr deployments status --json | python3 -c 'import json,sys; t=sys.stdin.read(); d=json.loads(t[t.index("{"):]); v=sorted(d.get("versions") or [], key=lambda x: -x.get("percentage", 0)); print(v[0]["version_id"] if v else "")' 2>/dev/null) || PREV=""
[ -n "$PREV" ] && echo "  live before this deploy: version $PREV" || echo "  no earlier qia-site version (first deploy): no rollback target"
WO=$(wr deploy); WR=$?
echo "$WO" | grep -i -E "uploaded|deployed|version id|error" | tail -4
[ $WR -eq 0 ] && ! echo "$WO" | grep -q -i "✘\|\[ERROR\]" || fail "wrangler deploy failed: $(echo "$WO" | grep -i -m1 error | cut -c1-200)"
DEPLOYED=1

STEP=checks; echo "== 4 CHECKS"
ROUTES=$(python3 "$L/qia_route.py" 2>&1)
if ! echo "$ROUTES" | grep -q -- "-> qia-site"; then
  echo "  routes still on heuremen-door: live checks skipped (cutover: python3 $L/qia_route.py qia)"; unset CFT
  echo "QIA SHIP: deployed (not serving yet); $(( $(date +%s) - T0 )) s"; exit 0
fi
CHK=$(python3 - "$OUT" <<'PY'
import os, re, sys, time, urllib.request, urllib.error
out = sys.argv[1]; S = 'https://quantumidleaudit.com'
BEACON = re.compile(rb'<script[^>]*cloudflareinsights[^>]*>(</script>)?\n?')   # the zone injects its Web Analytics beacon into HTML
def get(p):
    try:
        r = urllib.request.urlopen(urllib.request.Request(S + p + ('&' if '?' in p else '?') + 'qs=%d' % time.time(), headers={'User-Agent': 'research-client'}), timeout=30)
        return r.status, BEACON.sub(b'', r.read())
    except urllib.error.HTTPError as e: return e.code, e.read()
    except Exception: return 0, b''
want = {}
for f in sorted(os.listdir(out)):
    if f.startswith('_'): continue   # 23 Nov 2026: _inquiry-*.html are templates the worker fills (/inquiry and the handler's answers), not pages
    p = '/' if f == 'index.html' else '/' + (f[:-5] if f.endswith('.html') else f)
    want[p] = open(os.path.join(out, f), 'rb').read()
for attempt in range(4):
    bad = []
    for p, b in want.items():
        st, body = get(p)
        same = body.endswith(b) if p == '/robots.txt' else body == b   # Cloudflare prepends its managed robots block on the zone
        if st != 200 or not same: bad.append('%s (%s%s)' % (p, st, '' if st != 200 else ', differs from the build'))
    st, _ = get('/method')
    if st != 404: bad.append('/method answers %s, not 404' % st)
    if not bad: break
    time.sleep(15)
print('live pages: %d match the build' % len(want) if not bad else 'live differs: ' + ', '.join(bad)); sys.exit(1 if bad else 0)
PY
); CR=$?; echo "  $CHK"
MP=0; MPO=$(MONEY_PATH_LOG="$L/gates/money_path_qia.ring" python3 "$L/money_path_check.py" --quiet 2>&1) || MP=$?; echo "$MPO" | tail -3 | sed 's/^/  /'
if [ $CR -ne 0 ] || [ $MP -ne 0 ]; then
  WHY="$([ $CR -ne 0 ] && echo "$CHK") $([ $MP -ne 0 ] && echo "money path: $(echo "$MPO" | grep -m1 '^FAIL' | cut -c6-160)")"
  if [ -n "$PREV" ]; then RB=$(wr rollback "$PREV" -y -m "ship_qia checks failed"); RBR=$?; echo "$RB" | tail -2
    [ $RBR -eq 0 ] && fail "checks failed, qia-site rolled back to $PREV: $WHY" || fail "checks failed and the ROLLBACK FAILED (live serves the new version): $WHY"
  else fail "checks failed, no earlier version to roll back to (python3 $L/qia_route.py door sends the site back to heuremen-door): $WHY"; fi
fi
unset CFT
echo "QIA SHIP: deployed and verified; $(( $(date +%s) - T0 )) s"
