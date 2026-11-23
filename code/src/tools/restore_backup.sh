#!/bin/bash
# restore_backup.sh <release-tag> [out-dir]  (23 Nov 2026, the designer round 2 #11): download an off-site backup release, check its HMAC BEFORE
# decrypting, then decrypt and unpack. Key: ACCOUNTS/offsite-backup-key (never printed). Releases before 20261123-1900 used the raw key for
# the HMAC; this script accepts either and says which.
set -euo pipefail
TAG="${1:?release tag, e.g. backup-20261123-1653}"; OUT="${2:-$HOME/restore_$TAG}"; K=~/Documents/"Heuremen LLC"/ACCOUNTS/offsite-backup-key
mkdir -p "$OUT"; cd "$OUT"
gh release download "$TAG" --repo indahl-ai/backup-private --clobber
D=${TAG#backup-}; cat bk_$D.tar.gz.enc.part* > bk_$D.tar.gz.enc
if [ -f bk_$D.tar.gz.enc.hmac ]; then
  python3 - "$K" bk_$D.tar.gz.enc bk_$D.tar.gz.enc.hmac <<'PY'
import hmac, hashlib, sys
raw = open(sys.argv[1], 'rb').read().strip(); want = open(sys.argv[3]).read().strip()
def mac(k):
    h = hmac.new(k, digestmod=hashlib.sha256); f = open(sys.argv[2], 'rb')
    for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
derived = hmac.new(raw, b'backup-mac', hashlib.sha256).digest()
if hmac.compare_digest(mac(derived), want): print('HMAC ok (derived key)')
elif hmac.compare_digest(mac(raw), want): print('HMAC ok (raw key, older release)')
else: sys.exit('HMAC MISMATCH: the archive is not the one that was uploaded; not decrypting')
PY
else echo "no HMAC file (release before 23 Nov 2026 evening); decrypting without an integrity check"; fi
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -pass file:"$K" -in bk_$D.tar.gz.enc | tar -xzf -
rm -f bk_$D.tar.gz.enc bk_$D.tar.gz.enc.part*
echo "restored into $OUT: $(ls "$OUT/bk" | wc -l | tr -d ' ') items in bk/"
