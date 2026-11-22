#!/bin/bash
# fly_wake.sh "<what changed>": The operator's hand edits to the flywheel (answers, backlog, manual refills) wake the designer's worker with a PR #17 comment.
/opt/homebrew/bin/gh pr comment 17 -R indahl-ai/calibrations --body "Flywheel wake: $1" | tail -1
