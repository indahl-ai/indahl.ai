#!/bin/bash
# firewall_on.sh (25 Nov 2026, owner: "you handle security"): turn on the macOS application firewall without cutting off house services.
# Run once with: sudo bash ~/forge/ledger/firewall_on.sh
# Keeps working: The referee's library (:8790, referee_library/serve.py) and GridSong query (:8097), which other machines reach over the tailnet,
# by allowing the two Python apps they run under. Apple-signed services (Remote Management, AirPlay) stay allowed by the signed-software rule.
# Stealth mode: the Mac stops answering pings and probes on closed ports. watch/alerts_check.py rings if the firewall goes off again or a
# house service's Python app falls off the allow list (a Homebrew Python upgrade changes the app path).
set -e
[ "$(id -u)" = 0 ] || { echo "run with sudo"; exit 1; }
F=/usr/libexec/ApplicationFirewall/socketfilterfw
for pid in $(lsof -tiTCP:8790 -sTCP:LISTEN) $(lsof -tiTCP:8097 -sTCP:LISTEN); do
  exe=$(ps -o comm= -p "$pid"); app="${exe%%/Contents/MacOS/*}"
  echo "allowing $app"; $F --add "$app" >/dev/null; $F --unblockapp "$app" >/dev/null
done
$F --setallowsigned on >/dev/null; $F --setallowsignedapp on >/dev/null
$F --setglobalstate on; $F --setstealthmode on
$F --getglobalstate; $F --getstealthmode
