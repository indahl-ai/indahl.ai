# The ledger: one writer at a time, and no silent loss (21 Nov 2026)

This folder is not under git, so this file is the record of the change.

## What happened
- **21 Nov 2026, 00:12:07Z.** A ship's QUAKE refresh (`quake_index/make_rows.py --update`, under the site lock) and the live-headline rider (`ledger/live_headlines.py run`, on the tick bus, under its own lock) both saved `ledger.jsonl` in the same seconds.
- The refresh printed "23 rows refreshed". The ledger held none of them: no `quake.*` row carries a change stamped between 00:10Z and 00:16Z, while `live.campus.v20261121T001204Z` is stamped 00:12:07Z. The rider had loaded before the refresh wrote, and its save wiped the refresh's rows.
- The QUAKE page was then one desk run ahead of its ledger rows, and every ship from 00:14Z was refused at the ledger gate. Nothing wrong was published. The fault was a success line that was not true.
- Found 21 Nov 01:58Z by reading the code and the ledger's own history stamps. Cleared at 01:26Z by running `quake_index/refresh_page.py` (25 rows refreshed).

## The cause
`ledger.py`'s `save()` took no lock: it wrote whatever the process held and swapped the file in. Two different locks guarded one file.

## The fix (ledger.py only)
| File | sha256 |
|---|---|
| ledger.py (now) | e25eb076831ce84d0ffa07090bbdfc681191242e7baf56409ef1e487caa267a2 |
| ledger.py.bak-20261121-onewriter (before) | fea239d150fb9e74b30588cb0e64220fe5c2613fd9c18d6ee26412b2d399d4ec |
| test_two_writers.py | 47312a6f75041e8f87f5d81764456a6de3797c5df92577c442b4652175e95703 |

- `load()` remembers what was on disk when the process read it.
- `save()` takes one kernel lock on `.ledger.flock`, a file of its own that is never swapped, reads the ledger as it is now, and applies only the rows this process changed. Rows another writer changed or added stay as that writer left them.
- A row changed (or deleted) by this process that another writer also changed is a conflict: nothing is written and the process exits non-zero.
- After writing, `save()` reads the file back and checks every row it changed is there as written, or exits non-zero.
- The file's format is unchanged: one row a line, sorted by id.
- The callers are untouched. Every program that writes the ledger goes through `save()`: checked across the house on 21 Nov (live_headlines, zenodo_sync, sagar_ledger, the quake, census and neo row makers, linkrot's ship_samples, and the ledger.py command line). Files named `look_ledger.jsonl` and `flywheel_ledger.jsonl` are other files.

## The test
`python3 test_two_writers.py` copies everything into a temporary folder and never touches the live ledger. Nine cases, passing under the shell's Python and under the tick bus's `/usr/bin/python3` 3.9.6. Case T7 runs the old save under the same two-process load and must lose updates; it does on every run.

## Referee
The referee, 21 Nov 2026 02:02Z (outside_referee 2026-11-21T02-02-25), STANDS on three conditions: the lock sits on a fixed file of its own (it does); nothing writes the ledger outside `save()` (checked, above); a deletion against another writer's change is refused (case T9).

## Correction, 21 Nov 2026 02:20Z: one direct writer was found and fixed
The line above, "Every program that writes the ledger goes through `save()`", was wrong by one when it was written. The referee asked for the exact search and its hit list (02:16Z). The first search only looked at lines where the file name sat beside a write call, so it missed a program that binds the path to a name and writes through the name.

- **Found:** `ledger/reword.py` (15 Nov) opened the ledger itself and rewrote it: no lock, no merge, rows in file order. It is a tool run by hand, not on the tick bus, and it did not run during tonight's lost update.
- **Fixed:** it now loads with `ledger.load()` and writes with `ledger.save()`. Tested on a temporary copy: a dry run leaves the file byte-identical; a real run changed 4 rows through save, the file stayed sorted by id with the same row count.
- **The search, kept so the claim carries its own evidence:** `python3 ledger/find_direct_writers.py` (exit 1 if any direct writer). It walks the house for .py and .sh files naming `ledger.jsonl` exactly, finds every name bound to that path, and reports any line that opens, replaces, copies onto or redirects into it. Run against the old reword.py in a copy, it finds line 28.

| File | sha256 |
|---|---|
| find_direct_writers.py | 0becb9a778aad99b6cb51d8c011f3581ac7c8c12c27125563f7b8a3f2942bcfd |
| reword.py (now) | e28de5616d2a486594cd742cf4ce0ee56ae7b31790c464bb7735f2a563c1665c |
| reword.py.bak-20261121-onewriter (before) | fab7f03a032e8b596d6fb766c8ca49dc4d7d398a8e0b04f6764fd9d4dda6dd6a |

Its output on the house, 21 Nov 2026 02:21Z:
```
programs that name ledger.jsonl: 38 | lines that write a file of that name: 2 | allowed, each with its reason: 2 | direct writers: 0
  allowed ledger/ledger.py line 191 (its save() is the one writer)
  allowed gridsong/wire_clocked.py line 376 (read 21 Nov 2026: its self-test binds LOG to a file named ledger.jsonl inside its own temporary folder (tmp), not the house ledger)
```
Not searched: files in other languages (none in the house writes the ledger that I know of), and the folders the script's SKIP list names (backups, archives, mirrors, vendored code).
