#!/bin/bash
# Encrypted off-site copy: git bundles of every repo + ledger, book, notes, memory -> private release on indahl-ai/backup-private. Key: ACCOUNTS/offsite-backup-key (never printed).
set -e; export PATH=/opt/homebrew/bin:/usr/bin:/bin; T=$(mktemp -d); D=$(date +%Y%m%d-%H%M);   # 23 Nov 2026: minutes in the name (a second run that day was refused: tag already existed)
trap 'rm -rf "$T"' EXIT   # 23 Nov 2026 (the designer review #19): the plaintext archive never outlives the run, failed or not
 cd ~/forge; mkdir $T/bk
# 23 Nov 2026: repos with a GitHub remote are already off-site there; bundle only the repos that live nowhere else (yo_school and sagar
# history alone is 11 GB and pushed the upload past what GitHub takes).
for g in $(ls -d */.git | sed 's#/.git##'); do [ -n "$(git -C $g remote 2>/dev/null)" ] && continue; git -C $g bundle create $T/bk/$g.bundle --all >/dev/null 2>&1 || echo "$(date +%Y-%m-%dT%H:%M:%S) RING: BACKUP: git bundle of $g failed; that repo is not in this backup" >> ~/forge/sagar/pipeline/pipe.log; done
find ledger qia_leads ligera watch outbox rolodex notify_state sagar/intake_rows -type f -size -100M ! -name '*.log' ! -name '*.log.*' ! -name '*.gz' ! -path '*/node_modules/*' ! -path '*/contact_stage_*' ! -name '*.tmp' ! -name '*.lock' ! -name '*.flock' ! -name '*-wal' ! -name '*-shm' ! -name '*-journal' > $T/list.txt 2>/dev/null   # 23 Nov 2026: no logs, no file over 100 MB
# 23 Nov 2026 (the designer review #2): uncommitted files exist only on the Mac (git bundles and GitHub carry commits only). Add every repo's
# changed and untracked files under 100 MB, except yo_school and iris_index (training data and downloaded paper data, about 20 GB,
# rebuilt from their sources). qia_cal's hardware runs and archive are the irreplaceable part.
for g in $(find . -maxdepth 3 -name .git -type d -not -path "./node_modules/*" -not -path "./.lanes/*" -not -path "./public_mirror/*" 2>/dev/null | sed 's#^\./##; s#/.git$##'); do case "$g" in yo_school|iris_index) continue;; esac   # 23 Nov 2026 (the designer round 2 #2): nested repos too; public_mirror is rebuilt from sources and lives on GitHub
  git -C "$g" ls-files -m -o --exclude-standard 2>/dev/null | while IFS= read -r f; do p="$g/$f"; [ -f "$p" ] || continue
    case "$p" in *.log|*.log.*|*-wal|*-shm|*-journal|*.tmp|*.lock|*/node_modules/*|*/__pycache__/*) continue;; esac
    [ "$(stat -f %z "$p")" -lt 100000000 ] && echo "$p" || true; done; done >> $T/list.txt   # || true: under set -e a big last file must not end the run (review #4)
sort -u -o $T/list.txt $T/list.txt
# 23 Nov 2026: live SQLite files change and their -wal/-shm files come and go mid-pack (the 12:55 run failed on outbox.db-shm). Each
# database is packed from a consistent snapshot (sqlite3 .backup), never from the live file.
mkdir -p $T/dbsnap; grep '\.db$' $T/list.txt | while read -r f; do mkdir -p "$T/dbsnap/$(dirname "$f")"; sqlite3 "$f" ".backup '$T/dbsnap/$f'" || exit 1; done
grep -v '\.db$' $T/list.txt > $T/list2.txt; mv $T/list2.txt $T/list.txt
tar -czf $T/bk/dbsnap_$D.tar.gz -C $T/dbsnap .
tar -czf $T/bk/internal_$D.tar.gz -T $T/list.txt   # 23 Nov 2026: a failed tar fails the backup (it used to upload a partial one)
tar -czf $T/bk/memory_$D.tar.gz -C ~/.claude/projects/-Users-heuremen memory
K=~/Documents/"Heuremen LLC"/ACCOUNTS/offsite-backup-key; cd $T; tar -czf bk.tar.gz bk
openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt -pass file:"$K" -in bk.tar.gz -out bk_$D.tar.gz.enc
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -pass file:"$K" -in bk_$D.tar.gz.enc | gzip -t
rm -rf bk bk.tar.gz   # 23 Nov 2026 (review #4): plaintext gone the moment the encrypted copy checks out, not only at exit
# 23 Nov 2026: GitHub refuses release files of 2 GiB or more, and the backup passed that after 29 Oct, so every run failed silently for 25 days.
# The encrypted file is cut into 1900 MiB parts. Restore: cat bk_$D.tar.gz.enc.part* > bk_$D.tar.gz.enc, then decrypt with the key.
# 23 Nov 2026 (the designer review #19): CBC carries no integrity check; an HMAC-SHA256 of the encrypted file (same offline key, read by python, never
# on a command line) is uploaded beside it; the MAC key is derived from it (HMAC(key, "backup-mac"), the designer round 2 #11). Restore with tools/restore_backup.sh, which checks it first.
python3 -c "import hmac,hashlib,sys;k=hmac.new(open(sys.argv[1],'rb').read().strip(),b'backup-mac',hashlib.sha256).digest();h=hmac.new(k,digestmod=hashlib.sha256);f=open(sys.argv[2],'rb')
for b in iter(lambda:f.read(1<<20),b''): h.update(b)
print(h.hexdigest())" "$K" bk_$D.tar.gz.enc > bk_$D.tar.gz.enc.hmac
echo "offsite: encrypted size $(du -h bk_$D.tar.gz.enc | cut -f1)"
split -b 1900m bk_$D.tar.gz.enc bk_$D.tar.gz.enc.part
gh release create backup-$D bk_$D.tar.gz.enc.part* bk_$D.tar.gz.enc.hmac --repo indahl-ai/backup-private --title "Encrypted backup $D" --notes "AES-256, key held offline. Parts: cat bk_$D.tar.gz.enc.part* > bk_$D.tar.gz.enc" >/dev/null
# keep the newest 4 releases
[ "$(gh release view backup-$D --repo indahl-ai/backup-private --json assets --jq '.assets|length')" -eq "$(ls bk_$D.tar.gz.enc.part* bk_$D.tar.gz.enc.hmac | wc -l | tr -d ' ')" ] || { echo "offsite: backup-$D incomplete on GitHub; older releases kept" >&2; exit 1; }   # review #4: never prune after a partial upload
gh release list --repo indahl-ai/backup-private --limit 20 --json tagName --jq '.[].tagName' | tail -n +5 | while read t; do gh release delete "$t" --repo indahl-ai/backup-private --cleanup-tag -y >/dev/null; done
echo "offsite: backup-$D uploaded"
