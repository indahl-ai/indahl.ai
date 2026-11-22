#!/usr/bin/env python3
"""One watcher for every Cloudflare call on this Mac (22 Nov 2026, the owner: "interchangeable parts").

Wrangler writes a log for every run, from any script, with an "errored" event naming the command and the
error type. This rider reads the logs written since its last pass and rings once per (command, error) with
a count and the folder it ran from. No script has to remember to check its own return code.
Rides the tick bus (watch/desk_riders.py, tier 1). State: watch/cf_log_watch.state.
"""
import os, re, glob, json, time, collections

LOGS = os.path.expanduser('~/Library/Preferences/.wrangler/logs')
STATE = os.path.expanduser('~/forge/watch/cf_log_watch.state')
PIPE = os.path.expanduser('~/forge/sagar/pipeline/pipe.log')
ERR = re.compile(r'"event":"wrangler command errored".*?"sanitizedCommand":"([^"]*)".*?"errorType":"([^"]*)"')
WHERE = re.compile(r'\.env file not found at "([^"]+)/\.env"')


def main():
    try: last = float(open(STATE).read().strip())
    except Exception: last = time.time() - 600
    now = time.time()
    hits = collections.Counter(); where = {}
    for f in glob.glob(os.path.join(LOGS, 'wrangler-*.log')):
        try:
            if os.path.getmtime(f) <= last: continue
            t = open(f, errors='replace').read()
        except OSError: continue
        w = WHERE.search(t); folder = w.group(1).replace(os.path.expanduser('~'), '~') if w else '?'
        for cmd, et in set(ERR.findall(t)):
            k = (cmd, et); hits[k] += 1; where.setdefault(k, set()).add(folder)
    if hits:
        with open(PIPE, 'a') as p:
            for (cmd, et), n in hits.most_common():
                p.write('%s RING: CLOUDFLARE CALL FAILED x%d: wrangler %s -> %s (from %s)\n' % (
                    time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), n, cmd, et, ', '.join(sorted(where[(cmd, et)]))[:200]))
        print('cf_log_watch: %d failure kinds rung' % len(hits))
    else:
        print('cf_log_watch: no Cloudflare failures since last pass')
    open(STATE, 'w').write(str(now))


if __name__ == '__main__':
    main()
