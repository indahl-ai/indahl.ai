#!/bin/bash
# save_source.sh "what changed" (22 Nov 2026): commit and push every house SOURCE repo before a ship, so no site edit can exist only on
# this Mac. The owner found his QIA site edits living only as working-tree files: ship.sh step 5 commits indahl-ai with `git commit -q ...
# && echo`, so a refused commit (the indahl-ai pre-commit hook) passed silently and the ship went on. This runs first in ship_qia.sh and
# in ship_request.sh (before ship.sh), and exits nonzero if any repo cannot be saved.
#   repo          work tree                                git dir                remote/branch
#   indahl-ai     ~/forge/indahl-ai                  .git                   origin main      (indahl-ai/house-site-source, private)
#   ledger        ~/forge/ledger                     .git                   backup main      (indahl-ai/ledger-private, private)
#   calibrations  ~/forge/calibrations               .git                   origin lane      (indahl-ai/calibrations, private)
#   house-ops     ~/forge (only heuremen-door, qia-site, heuremen-specbook, lib, watch; whitelist in the git dir's info/exclude)
#                                                          ~/.house-ops.git       origin main      (indahl-ai/house-ops, private)
#     house-ops keeps its git dir OUTSIDE forge, so no script in forge ever finds a repo by walking up. To use it by hand:
#     git --git-dir=$HOME/.house-ops.git --work-tree=$HOME/forge status
# Each repo: git add -A (the repo's .gitignore keeps out generated pages, studies, state, logs, keys, backups), then
# ledger/source_scan.py on the staged files (secrets: keychain values, key shapes, key files; studies: study paths, notice bodies, PDFs not
# on ledger/source_pdf_allow.txt; files over 5 MB). A hit unstages everything and fails. Then commit as Heuremen LLC with
# "ship: <what changed>" (--no-verify: the indahl-ai pre-commit hook is a publishing gate on the ledger and copies, and saving source must
# never wait on it; ship.sh still runs every gate before a deploy) and push. A repo still ahead of its remote after the push fails.
# Never pushes to a public repo: the remotes above are fixed here and each is checked PRIVATE once a day (ledger/.save_source_private).
# Exit 0 = every repo saved; 1 = a scan hit, a commit or a push failed (one line per problem on stdout).
set -uo pipefail
MSG="${1:?usage: save_source.sh \"what changed\"}"
B="$HOME/forge"; L="$B/ledger"; HG="$HOME/.house-ops.git"
cd "$B"   # 23 Nov 2026: house-ops adds the pathspec "." against its work tree, which git reads from the current folder; run from ledger/ it named only ledger/ (ignored there) and refused every ship request made from that folder
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
# 23 Nov 2026 (separate lanes): SAVE_SCOPE=qia saves only the qia.com source paths, under its own lock, so a qia.com ship never waits on
# (or commits) another lane's half-done work. Unset = every source repo, as before.
SCOPE="${SAVE_SCOPE:-all}"; LOCKF="$L/.save_source.flock"; [ "$SCOPE" = qia ] && LOCKF="$L/.save_source_qia.flock"
if [ -z "${SAVE_SOURCE_LOCKED:-}" ]; then export SAVE_SOURCE_LOCKED=1; exec /usr/bin/lockf -k -t 600 "$LOCKF" bash "$0" "$@"; fi
AUTHOR=(-c "user.name=Heuremen LLC" -c "user.email=349448817+indahl-ai@users.noreply.github.com")
SUBJ="ship: $(printf '%s' "$MSG" | tr '\n\t' '  ' | cut -c1-180)"
BAD=0; OUT=()

# house-ops whitelist (rewritten every run so a lost info/exclude can never widen what is versioned)
mkdir -p "$HG/info" 2>/dev/null && cat > "$HG/info/exclude" <<'EOF'
# house-ops: the work tree is ~/forge, but only these folders are versioned here (save_source.sh rewrites this file).
/*
!/lib/
!/watch/
!/heuremen-specbook/
!/cloudflare-workers/
/cloudflare-workers/*
!/cloudflare-workers/heuremen-door/
!/cloudflare-workers/qia-site/
# 23 Nov 2026: tools/ holds the off-site backup and log rotation scripts, which were in no repo and not in the backup itself.
# Scripts only: the ESP toolchains, built packs, caches, logs and backups stay out.
!/tools/
/tools/esptool-venv/
/tools/openocd-esp32/
/tools/desk_packs/dist/
/tools/**/__pycache__/
/tools/*.log
/tools/*.bak-*
EOF

# once a day: every remote must be a PRIVATE indahl-ai repo, or nothing is pushed
STAMP="$L/.save_source_private"
if [ ! -f "$STAMP" ] || [ $(( $(date +%s) - $(stat -f %m "$STAMP") )) -gt 86400 ]; then
  PV=ok; for r in house-site-source ledger-private calibrations house-ops; do
    v=$(gh repo view "indahl-ai/$r" --json visibility -q .visibility 2>/dev/null); [ "$v" = PRIVATE ] || { PV="indahl-ai/$r is ${v:-unreadable}, not PRIVATE"; break; }; done
  if [ "$PV" = ok ]; then touch "$STAMP"; else echo "save_source: REFUSED: $PV (nothing committed or pushed)"; exit 1; fi
fi

# 23 Nov 2026 (the designer review #18): the qia and all scopes keep separate locks (qia.com never waits on an indahl.ai ship), so two saves can
# meet in one repo. git's own index.lock is the guard; a step that loses that race waits and tries again instead of failing the save.
gtry() { local o i; for i in 1 2 3 4 5; do o=$("$@" 2>&1) && { printf '%s' "$o"; return 0; }; case "$o" in *index.lock*) sleep 3;; *) printf '%s' "$o"; return 1;; esac; done; printf '%s' "$o"; return 1; }
save() {   # save NAME REMOTE BRANCH git-args...   (env PATHS: only these paths, for SAVE_SCOPE=qia)
  local name="$1" remote="$2" branch="$3"; shift 3; local g=(git "$@") i r out n ahead; local pa=(); [ -n "${PATHS:-}" ] && read -r -a pa <<< "$PATHS"
  for i in $(seq 1 30); do   # a ship's own commit may hold the index for a moment
    [ -e "$("${g[@]}" rev-parse --absolute-git-dir)/index.lock" ] || break; sleep 2; done
  out=$(gtry "${g[@]}" add -A -- "${pa[@]:-.}") || { OUT+=("$name: git add failed: $(echo "$out" | head -1)"); BAD=1; return; }
  if ! "${g[@]}" diff --cached --quiet; then
    n=$("${g[@]}" diff --cached --name-only | wc -l | tr -d ' ')
    if [ "$name" = house-ops ]; then out=$(python3 "$L/source_scan.py" --git-dir "$HG" --work-tree "$B" 2>&1); r=$?
    else out=$(python3 "$L/source_scan.py" "$("${g[@]}" rev-parse --show-toplevel)" 2>&1); r=$?; fi
    if [ $r -ne 0 ]; then "${g[@]}" reset -q; echo "$out" | sed "s/^/  /"
      OUT+=("$name: SCAN REFUSED ($(echo "$out" | grep -c '^  HIT') hits, first: $(echo "$out" | grep -m1 '^  HIT' | sed 's/^  HIT //' | cut -c1-140)); nothing committed"); BAD=1; return; fi
    out=$(gtry "${g[@]}" "${AUTHOR[@]}" commit -q --no-verify -m "$SUBJ" -- "${pa[@]:-.}") || { OUT+=("$name: COMMIT FAILED: $(echo "$out" | grep -v '^\s*$' | head -1 | cut -c1-160)"); BAD=1; return; }
    OUT+=("$name: committed $n files ($("${g[@]}" log -1 --format=%h))")
  else OUT+=("$name: nothing to commit"); fi
  out=$("${g[@]}" push -q "$remote" "HEAD:$branch" 2>&1); r=$?
  ahead=$("${g[@]}" rev-list --count "$remote/$branch..HEAD" 2>/dev/null || echo "?")
  if [ $r -ne 0 ] || [ "$ahead" != 0 ]; then OUT+=("$name: PUSH FAILED to $remote/$branch (exit $r, $ahead commits ahead): $(echo "$out" | sed -E 's#https://[^@]*@#https://#' | grep -v '^\s*$' | head -1 | cut -c1-160)"); BAD=1
  else OUT[${#OUT[@]}-1]="${OUT[${#OUT[@]}-1]}, pushed"; fi
}

if [ "$SCOPE" = qia ]; then   # the qia.com lane: its own source files only
  PATHS="qia_site.py standard_md.py" save indahl-ai origin main -C "$B/indahl-ai"
  PATHS="site/console" save calibrations origin lane -C "$B/calibrations"
  PATHS="cloudflare-workers/qia-site" save house-ops origin main --git-dir="$HG" --work-tree="$B"
else
  save indahl-ai    origin main -C "$B/indahl-ai"
  save ledger       backup main -C "$L"
  save calibrations origin lane -C "$B/calibrations"
  save house-ops    origin main --git-dir="$HG" --work-tree="$B"
fi

for o in "${OUT[@]}"; do echo "  save_source $o"; done
[ $BAD = 0 ] && echo "save_source: every source repo saved" || echo "save_source: FAILED (see the lines above)"
exit $BAD
