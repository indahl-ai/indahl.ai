#!/bin/sh
# Independent watchdog (22 Nov 2026, PARTS.md HARD #23, the designer's call: plain sh, shares nothing with what it watches).
# Its own launchd agent (com.heuremen.watchdog, every 120 s). Checks the ages of the three heartbeats the buses write.
# A dead heartbeat writes one RING to pipe.log and one macOS notification, once per outage (state file), and again when it recovers.
B="$HOME/forge"; PIPE="$B/sagar/pipeline/pipe.log"; ST="$B/watch/.watchdog_state"
now=$(date +%s); dead=""
check() {   # file limit_seconds name
  if [ -f "$1" ]; then a=$((now - $(stat -f %m "$1"))); else a=999999; fi
  [ "$a" -gt "$2" ] && dead="$dead $3($((a / 60))m)"
}
check "$B/watch/ticks.log" 1200 tick-bus
check "$B/watch/desk_bus_state.json" 1800 desk-bus
check "$B/alerts/last_check" 3600 alerts-check
prev=$(cat "$ST" 2>/dev/null)
if [ -n "$dead" ] && [ "$dead" != "$prev" ]; then
  printf '%s RING: WATCHDOG DEAD MACHINERY:%s (restart: launchctl kickstart -k gui/%s/com.heuremen.tick-bus)\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$dead" "$(id -u)" >> "$PIPE"
  osascript -e "display notification \"Dead:$dead\" with title \"Heuremen watchdog\"" >/dev/null 2>&1
elif [ -z "$dead" ] && [ -n "$prev" ]; then
  printf '%s WATCHDOG RECOVERED (was:%s)\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$prev" >> "$PIPE"
fi
printf '%s' "$dead" > "$ST"
