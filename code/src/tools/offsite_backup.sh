#!/bin/bash
# Encrypted off-site copy: git bundles of every repo + ledger, book, notes, memory -> private release on indahl-ai/backup-private. Key: ACCOUNTS/offsite-backup-key (never printed).
set -e; export PATH=/opt/homebrew/bin:/usr/bin:/bin; T=$(mktemp -d); D=$(date +%Y%m%d); cd ~/forge; mkdir $T/bk
# 23 Nov 2026: repos with a GitHub remote are already off-site there; bundle only the repos that live nowhere else (yo_school and sagar
# history alone is 11 GB and pushed the upload past what GitHub takes).
for g in $(ls -d */.git | sed 's#/.git##'); do [ -n "$(git -C $g remote 2>/dev/null)" ] && continue; git -C $g bundle create $T/bk/$g.bundle --all >/dev/null 2>&1 || true; done
find ledger qia_leads ligera watch outbox rolodex notify_state sagar/intake_rows -type f -size -100M ! -name '*.log' ! -name '*.log.*' ! -name '*.gz' ! -path '*/node_modules/*' ! -path '*/contact_stage_*' ! -name '*.tmp' ! -name '*.lock' ! -name '*.flock' > $T/list.txt 2>/dev/null   # 23 Nov 2026: no logs, no file over 100 MB
tar -czf $T/bk/internal_$D.tar.gz -T $T/list.txt   # 23 Nov 2026: a failed tar fails the backup (it used to upload a partial one)
tar -czf $T/bk/memory_$D.tar.gz -C ~/.claude/projects/-Users-heuremen memory
K=~/Documents/"Heuremen LLC"/ACCOUNTS/offsite-backup-key; cd $T; tar -czf bk.tar.gz bk
openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt -pass file:"$K" -in bk.tar.gz -out bk_$D.tar.gz.enc
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -pass file:"$K" -in bk_$D.tar.gz.enc | gzip -t
# 23 Nov 2026: GitHub refuses release files of 2 GiB or more, and the backup passed that after 29 Oct, so every run failed silently for 25 days.
# The encrypted file is cut into 1900 MiB parts. Restore: cat bk_$D.tar.gz.enc.part* > bk_$D.tar.gz.enc, then decrypt with the key.
echo "offsite: encrypted size $(du -h bk_$D.tar.gz.enc | cut -f1)"
split -b 1900m bk_$D.tar.gz.enc bk_$D.tar.gz.enc.part
gh release create backup-$D bk_$D.tar.gz.enc.part* --repo indahl-ai/backup-private --title "Encrypted backup $D" --notes "AES-256, key held offline. Parts: cat bk_$D.tar.gz.enc.part* > bk_$D.tar.gz.enc" >/dev/null
# keep the newest 4 releases
gh release list --repo indahl-ai/backup-private --limit 20 --json tagName --jq '.[].tagName' | tail -n +5 | while read t; do gh release delete "$t" --repo indahl-ai/backup-private --cleanup-tag -y >/dev/null; done
echo "offsite: backup-$D uploaded"; rm -rf $T
