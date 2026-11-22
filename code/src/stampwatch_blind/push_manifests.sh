#!/bin/bash
# push_manifests.sh (13 Nov 2026): stampwatch blind-feed manifests (file, sha256, read time, counts only) and collector hashes placed in
# claude-plugins/plans/stampwatch/manifests, so the series is outside-witnessed as it grows (plan v3). No snapshot content leaves this machine:
# only manifest.jsonl rows (file, read_at, sha256_raw, n, nothing_returned), the frozen sample frames and the collector sha256 are copied.
# 21 Nov 2026 (witness fix): this used to `git push` claude-plugins to Heuremen-LLC/claude-plugins, a frozen mirror (GitHub public home is
# indahl-ai only). Local main diverged from that remote after its 15 Nov rewrite, so every push since then failed unseen. Now it commits
# locally only, never pushes. The public witness is ledger/push_public.sh, which rsyncs ~/forge/claude-plugins/ into
# public_mirror/indahl.ai/claude-plugins/ and pushes indahl-ai/indahl.ai on every ship (internal_gate.py and scrub_public.py run first).
# Exit 0 when nothing changed or the local commit lands; nonzero only on a real failure (copy, hash or commit).
set -euo pipefail
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
S=~/forge/stampwatch_blind; R=~/forge/claude-plugins; M=$R/plans/stampwatch/manifests
mkdir -p "$M"
cp "$S/manifest.jsonl" "$M/hf_manifest.jsonl"; [ -f "$S/manifest_ckan.jsonl" ] && cp "$S/manifest_ckan.jsonl" "$M/ckan_manifest.jsonl"
cp "$S/models.json" "$M/hf_models.json"; cp "$S/ckan_datasets.json" "$M/ckan_datasets.json"; [ -f "$S/ckan_frame.json" ] && cp "$S/ckan_frame.json" "$M/ckan_frame.json"
( cd "$S" && shasum -a 256 snap_hf.py snap_ckan.py push_manifests.sh ) > "$M/collector_sha256.txt"
cd "$R"
git add plans/stampwatch/manifests
if git diff --cached --quiet -- plans/stampwatch/manifests; then echo "push_manifests: no new manifest rows, nothing to commit"; exit 0; fi
git -c user.name="Heuremen LLC" -c user.email="noreply@indahl.ai" commit -q -m "stampwatch: blind-feed manifests $(date -u +%Y-%m-%dT%H:%MZ)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -- plans/stampwatch/manifests
echo "push_manifests: committed locally ($(git rev-parse --short HEAD)); publish rides the next ship (push_public.sh -> indahl-ai/indahl.ai claude-plugins/plans/stampwatch/manifests)"
