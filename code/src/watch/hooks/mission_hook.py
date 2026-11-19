#!/usr/bin/env python3
"""Per-prompt context, slim (the owner 19 Nov: the long injected blocks crowded out the goal). Prints the live MISSION file.
The full laws / six questions / rulers remain in /tp and ligera/; the gates enforce in code."""
import json, os
m = open(os.path.expanduser('~/bones-forge/MISSION.md')).read().strip()
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": m}}))
