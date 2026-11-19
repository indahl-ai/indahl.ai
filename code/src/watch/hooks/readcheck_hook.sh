#!/bin/sh
# pre-commit line: a reading goes in with its check block (watch/hooks/readcheck_hook.py)
python3 "$HOME/bones-forge/watch/hooks/sim_headline_guard.py" || exit 1
exec python3 "$HOME/bones-forge/watch/hooks/readcheck_hook.py"
