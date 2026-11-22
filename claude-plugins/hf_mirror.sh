#!/bin/zsh
# Mirror every public indahl repo to Hugging Face as indahl/<name> (15 Nov 2026, the owner). Only files COMMITTED in each local clone go up (git archive HEAD), never a working folder. The Hub has no code
# repo type, so these are model repos holding the source; each keeps its own README. house-site-source (private) never goes up.
#   hf_mirror.sh            all repos
#   hf_mirror.sh <name>...  just these
set -u
setopt null_glob
PR=~/forge/plugin_repos; PM=~/forge/public_mirror; T=$(mktemp -d)
typeset -A SRC
for d in $PR/*(/); do SRC[${d:t}]=$d; done
SRC[claude-plugins]=$PM/claude-plugins; SRC[indahl.ai]=$PM/indahl.ai
names=(${@:-${(k)SRC}})
for n in $names; do
  s=${SRC[$n]:-}; [ -n "$s" ] && [ -d "$s/.git" ] || { echo "SKIP $n: no clone"; continue; }
  [ "$n" = house-site-source ] && { echo "SKIP $n: private"; continue; }
  [ "$n" = indahl.ai ] && { echo "SKIP $n: synced by hf_stage/hf_site_sync.py on every public push"; continue; }
  [ "$n" = indahl.ai ] && { echo "SKIP $n: synced by hf_stage/hf_site_sync.py on every public push"; continue; }
  GHO=indahl-ai; [ "$n" = claude-plugins ] && GHO=indahl-ai   # 15 Nov: github.com/indahl-ai is the public home; claude-plugins stays until the directory reviews clear
  out=$T/$n; mkdir -p $out; git -C $s archive HEAD | tar -x -C $out
  sha=$(git -C $s rev-parse --short HEAD)
  # HF card header (the Hub warns without one): license read from the repo's LICENSE, tags, and the GitHub source. GitHub copy is untouched.
  lic=other; Ls=($out/LICENSE*); L=${Ls[1]:-}; LN=LICENSE; [ -n "$L" ] && LN=${L:t}; [ -n "$L" ] && head -3 "$L" | grep -qi "MIT License" && lic=mit
  kind=claude-code-plugin; [ "$n" = indahl.ai ] && kind=website-source; [ "$n" = claude-plugins ] && kind=claude-code-plugin-marketplace
  R=$out/README.md; [ -f $R ] || printf '# %s\n\nSource: https://github.com/%s/%s\n' "$n" "$GHO" "$n" > $R
  if ! head -1 $R | grep -q '^---$'; then
    { printf -- '---\nlicense: %s\n' $lic; [ $lic = other ] && printf 'license_name: see-license-file\nlicense_link: https://indahl.ai/downloads' "$n" "$LN"
      printf 'inference: false\ntags:\n- %s\n- indahl\n- heuremen\n- claude-code\n---\n\n' $kind; cat $R
      printf '\n\n---\n\nMirror of https://github.com/%s/%s at %s. Heuremen LLC, https://indahl.ai\n' "$GHO" "$n" "$sha"; } > $R.new && mv $R.new $R
  fi
  hf repos create indahl/$n --type model --public --exist-ok >/dev/null 2>&1 || { echo "FAIL create $n"; continue; }
  if [ $(find $out -type f | wc -l) -gt 2000 ]; then
    hf upload indahl/$n $out . --repo-type model --commit-message "Mirror of github.com/$GHO/$n at $sha" >/dev/null 2>&1 && echo "OK $n (large) from GitHub $sha" || echo "FAIL upload $n"
  else
    hf upload indahl/$n $out . --repo-type model --commit-message "Mirror of github.com/$GHO/$n at $sha" >/dev/null 2>&1 && echo "OK $n from GitHub $sha" || echo "FAIL upload $n"
  fi
  rm -rf $out
done
rm -rf $T
