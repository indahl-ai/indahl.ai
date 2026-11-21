#!/usr/bin/env python3
"""Per-prompt context, slim (the owner 19 Nov: the long injected blocks crowded out the goal). Prints the live MISSION file.
The full laws / six questions / rulers remain in /tp and ligera/; the gates enforce in code."""
import json, os
m = open(os.path.expanduser('~/bones-forge/MISSION.md')).read().strip()
# 21 Nov 2026 (the owner: The designer's rings must never be overlooked again): unread "Ball to the operator" rings, from watch/doorbell/inbox.jsonl
try:
    _ib = os.path.expanduser('~/bones-forge/watch/doorbell/inbox.jsonl')
    _u = [json.loads(l) for l in open(_ib) if l.strip() and not json.loads(l)['read']] if os.path.exists(_ib) else []
    if _u: m += '\n\nUNREAD BALLS FROM THE DESIGNER (%d): act on them first; mark read with python3 ~/bones-forge/watch/doorbell/read.py\n' % len(_u) + '\n'.join('- PR #%d %s: %s' % (r['pr'], r['at'][11:16] + 'Z', r['first'][:200]) for r in _u[-8:])
except Exception: pass
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": m}}))
