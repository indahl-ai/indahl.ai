#!/bin/bash
# start.sh: run once when the container starts (RunPod template start command). Makes sure Python 3.11 or newer is available, installs the
# four libraries into ./.venv, and prints how to begin. Nothing here sends anything anywhere except package downloads.
set -e
cd "$(dirname "$0")"
export PATH="/usr/local/bin:$HOME/.local/bin:$PATH"
if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
  python3 -m venv .venv
  .venv/bin/python -m pip install --quiet --no-cache-dir -r requirements.txt
else
  python3 -m pip install --quiet --no-cache-dir uv      # uv fetches its own Python 3.12; the image's older Python is left alone
  uv venv --python 3.12 .venv
  uv pip install --quiet --python .venv/bin/python -r requirements.txt
fi
echo
echo "Quantum Idle Audit finance demonstration is ready. First:  source .venv/bin/activate"
echo "  1. No key needed:      python sandbox.py replay"
echo "  2. Your own IBM time:  export IBM_QUANTUM_TOKEN=<your key>; python sandbox.py check"
echo "Everything stays in this container. Read README.md first."
