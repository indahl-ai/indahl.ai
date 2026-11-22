#!/usr/bin/env python3
"""Per-prompt context, slim (the owner 19 Nov: the long injected blocks crowded out the goal). Prints the live MISSION file.
The full laws / six questions / rulers remain in /tp and ligera/; the gates enforce in code."""
import json, os
m = open(os.path.expanduser('~/forge/MISSION.md')).read().strip()
# 21 Nov 2026 (the owner: The designer's rings must never be overlooked again): unread "Ball to the operator" rings, from watch/doorbell/inbox.jsonl
try:
    _ib = os.path.expanduser('~/forge/watch/doorbell/inbox.jsonl')
    _u = [json.loads(l) for l in open(_ib) if l.strip() and not json.loads(l)['read']] if os.path.exists(_ib) else []
    if _u: m += '\n\nUNREAD BALLS FROM THE DESIGNER AND PIPELINE ALERTS (%d): act on them first; mark read with python3 ~/forge/watch/doorbell/read.py\n' % len(_u) + '\n'.join(('- PR #%d %s: %s' % (r['pr'], r['at'][11:16] + 'Z', r['first'][:200]) if r['pr'] else '- %s %s' % (r['at'][11:16] + 'Z', r['first'][:200])) for r in _u[-8:])
except Exception: pass
# 21 Nov 2026 (control audit, the owner "now"): open alerts printed only at session start, so a refused automatic ship sat unseen for hours. Print them every prompt.
try:
    _al = open(os.path.expanduser('~/forge/alerts/ALERTS_OPEN.txt')).read().strip()
    if _al: m += '\n\nOPEN ALERTS (fix first): ' + _al[:1500]
    try:   # 22 Nov 2026 (PARTS.md audit): if the tick bus dies, every check that rides it dies too; these three ages are read here on every prompt
        import os as _o, time as _t; _B = _o.path.expanduser('~/forge'); _now = _t.time(); _dead = []
        for _f, _lim, _what in ((_B + '/watch/ticks.log', 1200, 'tick bus'), (_B + '/watch/desk_bus_state.json', 1800, 'desk bus'), (_B + '/alerts/last_check', 3600, 'alerts_check')):
            _a = _now - _o.path.getmtime(_f) if _o.path.exists(_f) else 1e9
            if _a > _lim: _dead.append('%s silent %d min (%s)' % (_what, _a // 60, _f.replace(_B, '~/forge')))
        if _dead: m += '\n\nDEAD MACHINERY (fix before anything else): ' + '; '.join(_dead) + '. Restart: launchctl kickstart -k gui/$(id -u)/com.heuremen.tick-bus'
    except Exception: pass
except Exception: pass
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": m}}))
