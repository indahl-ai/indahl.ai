#!/bin/bash
# lane.sh (23 Nov 2026, separate lanes): edit site code in a private git worktree, never in the live working copy the ships build from.
# A SAGAR batch ship was refused on 23 Nov because an agent was halfway through editing indahl-ai/build_site.py in the live copy.
#   lane.sh start <repo> <name>   make ~/forge/.lanes/<name>, a worktree of <repo> (indahl-ai | calibrations | ledger) on branch wt/<name>
#   lane.sh land <name>           compile-check the changed .py/.sh files, then merge wt/<name> into the live copy (fast, one step) and remove the worktree
#   lane.sh list                  open lanes
# The live copy only ever changes in the one merge step, so a ship never builds a half-edited file. Data (studies, feeds, notices) is not code
# and keeps shipping on its own.
set -euo pipefail
B="$HOME/forge"; LN="$B/.lanes"; mkdir -p "$LN"
repo_dir() { case "$1" in indahl-ai) echo "$B/indahl-ai";; calibrations) echo "$B/calibrations";; ledger) echo "$B/ledger";; *) echo "unknown repo $1 (indahl-ai, calibrations, ledger)" >&2; exit 2;; esac; }
case "${1:-}" in
  start)
    R=$(repo_dir "${2:?repo}"); N="${3:?name}"; W="$LN/$N"
    [ -e "$W" ] && { echo "lane $N already open at $W"; exit 1; }
    git -C "$R" worktree add -q -b "wt/$N" "$W" HEAD
    echo "$2" > "$W/.lane_repo"; echo "lane $N open: edit in $W, then: lane.sh land $N" ;;
  land)
    N="${2:?name}"; W="$LN/$N"; [ -d "$W" ] || { echo "no lane $N"; exit 1; }
    R=$(repo_dir "$(cat "$W/.lane_repo")"); rm -f "$W/.lane_repo"
    BR=$(git -C "$R" rev-parse --abbrev-ref HEAD)
    git -C "$W" add -A; git -C "$W" -c user.name="Heuremen LLC" -c user.email=349448817+indahl-ai@users.noreply.github.com commit -q --no-verify -m "lane $N" || true
    for f in $(git -C "$W" diff --name-only "$BR"...HEAD); do
      case "$f" in *.py) python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$W/$f" || { echo "lane $N: $f does not parse; not landed"; exit 1; };;
                   *.sh) bash -n "$W/$f" || { echo "lane $N: $f has a syntax error; not landed"; exit 1; };; esac
    done
    git -C "$R" -c user.name="Heuremen LLC" -c user.email=349448817+indahl-ai@users.noreply.github.com merge -q --no-edit "wt/$N" || { echo "lane $N: merge conflict in the live copy; resolve by hand"; exit 1; }
    git -C "$R" worktree remove --force "$W"; git -C "$R" branch -q -d "wt/$N" 2>/dev/null || true
    case "$(basename "$R")" in ledger) RM=backup;; *) RM=origin;; esac   # 23 Nov 2026: a landed lane is pushed at once (the unsaved-source alert caught one that was not)
    git -C "$R" push -q "$RM" "HEAD:$BR" || { echo "lane $N landed but the push to $RM/$BR failed; push by hand"; exit 1; }
    echo "lane $N landed in $R ($BR) and pushed" ;;
  list) for d in "$LN"/*/; do [ -d "$d" ] && echo "$(basename "$d") ($(cat "$d/.lane_repo" 2>/dev/null))"; done; true ;;
  *) sed -n 2,8p "$0"; exit 2 ;;
esac
