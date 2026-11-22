#!/bin/bash
# seal_plan.sh <commit>: copy zeus_index/PLAN.md from indahl-ai/calibrations at <commit> (branch lane-research) and write data/plan_seal.json.
# zeus_tick.py refuses to read without the seal and refuses if PLAN.md differs from it.
set -euo pipefail; H="$(cd "$(dirname "$0")" && pwd)"; C="${1:?commit}"
gh api "repos/indahl-ai/calibrations/contents/zeus_index/PLAN.md?ref=$C" --jq .content | base64 -d > "$H/PLAN.md"
T=$(gh api "repos/indahl-ai/calibrations/commits/$C" --jq .commit.committer.date); FULL=$(gh api "repos/indahl-ai/calibrations/commits/$C" --jq .sha)
S=$(shasum -a 256 "$H/PLAN.md" | cut -d' ' -f1)
printf '{\n "plan_repo": "indahl-ai/calibrations",\n "plan_branch": "lane-research",\n "plan_commit": "%s",\n "plan_commit_time": "%s",\n "plan_sha256": "%s",\n "sealed": "%s"\n}\n' "$FULL" "$T" "$S" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$H/data/plan_seal.json"
cat "$H/data/plan_seal.json"
