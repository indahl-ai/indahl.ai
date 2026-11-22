#!/bin/bash
# preflight.sh (22 Nov 2026, PIPELINE_AUDIT P2 / A9): one gate list. The preflight is ship.sh --check: the ship's own build and every gate, all breaches in one pass, stopping before any deploy, commit or push.
exec bash "$(cd "$(dirname "$0")" && pwd)/ship.sh" --check "${1:-preflight}"
