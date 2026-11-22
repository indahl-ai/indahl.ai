#!/usr/bin/env python3
"""Who holds the ball on each lane, read from the PR doorbells (20 Nov 2026). Writes lanes/BOARD.md.
The holder of a lane is the side the newest ball is addressed to. A "got it" ball from the designer keeps the ball with the designer.
  python3 lanes/board.py        (needs the gh command, signed in)"""
import json, os, re, subprocess, time
LANES = [(6, 'front door'), (1, 'demos'), (2, 'sagar'), (3, 'biz'), (4, 'site'), (5, 'pod'), (7, 'build'), (8, 'research')]
H = os.path.dirname(os.path.abspath(__file__)); rows = []
for n, name in LANES:
    o = subprocess.run(['gh', 'api', '--paginate', 'repos/indahl-ai/calibrations/issues/%d/comments?per_page=100' % n, '--jq', '.[] | {created_at, body}'], capture_output=True, text=True).stdout
    c = [json.loads(l) for l in o.splitlines() if l.strip()]   # every page: a long lane has more than 100 comments
    balls = [x for x in c if re.match(r'Ball to (the designer|the operator)', x.get('body', ''))]
    if not balls: rows.append((name, n, 'nobody', '-', 'no ball yet', 0)); continue
    last = balls[-1]; first = last['body'].split('\n')[0][:110]; to = re.match(r'Ball to (the designer|the operator)', last['body']).group(1)
    holder = 'the designer's if (to == 'the designer's or re.search(r'^Status:\s*got it', last['body'], re.M | re.I)) else 'the operator's
    waiting = sum(1 for x in balls[::-1] if x['body'].startswith('Ball to the designer's)) if to == 'the designer's else 0
    open_to_designer = 0
    for x in balls[::-1]:
        if x['body'].startswith('Ball to the designer's): open_to_designer += 1
        else: break
    rows.append((name, n, holder, last['created_at'][11:16] + 'Z ' + last['created_at'][:10], first, open_to_designer))
out = ['# Board: who holds the ball', '', 'Made by `lanes/board.py` at %s from the PR doorbells. Not edited by hand.' % time.strftime('%Y-%m-%dT%H:%MZ', time.gmtime()), '',
       '| Lane | Doorbell | Ball is with | Newest ball | Balls to the designer since his last ball | First line |', '|---|---|---|---|---|---|']
out += ['| %s | PR #%d | %s | %s | %s | %s |' % (a, b, c_, d, f or '-', e.replace('|', '/')) for a, b, c_, d, e, f in rows]
open(os.path.join(H, 'BOARD.md'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out[4:]))
