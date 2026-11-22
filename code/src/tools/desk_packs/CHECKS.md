# Check blocks (watch/readcheck.py). One entry per reading, appended, never edited after commit.

## 2026-11-10 14:10 Desk data packs on every desk page, the Data pack link at the top right of every page with data, and grab-and-go pack lists with zip sizes on the division pages
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: every pack was built from the live feed it describes and checked against a second read of that feed, so the none is the feed itself and a pack that drifts from it is refused
- II: n/a: no comparison between two runs, the packs carry the desks' own results and the sizes are file sizes
- III: n/a: no signed difference is reported, sizes and row counts are levels of one file
- V: holds: two counts side by side for every CSV, the row count read back with csv.DictReader and the count in the live feed, with outcome, n, lo and hi compared row by row
- VI: n/a: no interval outcome is claimed by the pack itself, it carries the desks' outcomes as printed
- R: holds: zip sizes read from the files in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 10 Nov 2026, and the pages print that file
- P1: n/a: no quoted text is added to any page, the list lines reuse the desk lines already in the menu
- P2: holds: every size names its zip, which is linked beside it, and each pack names its feed and as-of time in its README
- P3: holds: pack and desk names as built, file names as served
- P4: holds: no cause named, sizes and links only
- P5: n/a: no intervals on these lines
- P6: holds: each line says what the zip holds and that results-only packs carry no source data, nothing stronger
- P7: holds: ledger rows pack.size.* added before the release, the zips in ledger/copies.json, release through ledger/ship.sh, live fetch and sha256 after
- P8: holds: rendered pages read after build, site gate breaches 0, check_ledger drift 0
- P9: holds: plain sentences, no semicolons, no counts of our things in headings, no AI statements, Heuremen LLC
- P10: n/a: no rule was set after the data, the licence handling per desk was set from the licence notes before the packs were built

## 2026-11-10 14:20 Desk packs of SOCIAL, HERMES and IRIS rebuilt with a Cite section and a doi field in CITATION.cff, for their Zenodo records
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: each pack was rebuilt from the live feed it describes and checked against a second read of that feed by tools/desk_pack.py, every check held on all 22 packs
- II: n/a: no comparison between two runs, the packs carry the desks' own results and the sizes are file sizes
- III: n/a: no signed difference is reported, sizes are levels of one file
- V: holds: the row counts of every CSV were read back and compared with the live feed by the same build, and the zip sizes were read from the files in public/ into tools/desk_packs/pack_sizes.json
- VI: n/a: no interval outcome is claimed by the pack itself, it carries the desks' outcomes as printed
- R: holds: zip sizes read from the files in public/ by tools/desk_pack.py sizes on 10 Nov 2026, five sizes moved by 1 KB with the newer feed reads and the added Cite text
- P1: n/a: no quoted text is added to any page
- P2: holds: every size names its zip, and each pack names its feed, its as-of time and now its Zenodo DOI in its README
- P3: holds: pack and record names as built, file names as served
- P4: holds: no cause named, sizes, links and DOIs only
- P5: n/a: no intervals on these lines
- P6: holds: the Cite section says only where the pack is deposited and that the DOI points to the newest version
- P7: holds: ledger rows pack.size.* set before the release, release through ledger/ship.sh, live sha256 compared before the Zenodo upload
- P8: holds: check_ledger drift read after the rebuild and fixed row by row before the ship
- P9: holds: plain sentences, no semicolons, no counts of our things in headings, no AI statements, Heuremen LLC
- P10: n/a: no rule was set after the data

## 2026-11-10 15:10 Zenodo DOIs on the pages: concept DOI on every pack page, a Zenodo line on each desk page whose pack is deposited, and on the HERMES, IRIS and SOCIAL pack boxes
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: each DOI was read back from the Zenodo API after publishing and the md5 Zenodo stores for every file equals the local file, whose sha256 equals the live zip
- II: n/a: no comparison between two runs
- III: n/a: no signed difference is reported
- V: holds: two records side by side for each DOI, zenodo_packs/dois.json written from the publish response and ledger/zenodo_dois.json, and they agree
- VI: n/a: no interval on these lines
- R: holds: DOIs read from the Zenodo publish response on 10 Nov 2026
- P1: n/a: no quoted text
- P2: holds: every DOI is a link to doi.org and names the record it resolves to
- P3: holds: record names as published on Zenodo
- P4: holds: no cause named, links only
- P5: n/a: no intervals
- P6: holds: the lines say only where the pack is deposited
- P7: holds: ledger rows zenodo.* added before the release, release through ledger/ship.sh
- P8: holds: rendered pages read after build, the DOI lines found on the pages listed in the ledger rows
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-10 20:40 Zenodo second pass: ATLAS 2026-11-10 version published, HERMES Desk Packs 2026-11-10.2 with SEASONAL, STEO, FLU, TORNADO and CREDIT, new records ATLAS Desk Packs (NEO, SOLAR, QUAKE, CONE) and OY Desk Packs (CAMPUS, RANK), DOIs on the pages
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: each DOI was read back from the Zenodo publish response and the API after publishing, the md5 Zenodo stores for every file equals the local file (52 files, all match), and every zip sha256 equals the live .sha256 before upload
- II: n/a: no comparison between two runs
- III: n/a: no signed difference is reported
- V: holds: two records side by side for each DOI, zenodo_packs/dois.json written from the publish response and ledger/zenodo_dois.json, and they agree, and doi.org/10.5281/zenodo.23874305 resolves to record 24110654
- VI: n/a: no interval on these lines
- R: holds: DOIs read from the Zenodo publish response on 10 Nov 2026 evening, ATLAS md5 995351372741192a8a4d04fb224993c5 equals the live zip
- P1: n/a: no quoted text
- P2: holds: every DOI is a link to doi.org and names the record it resolves to, each source licence was read from tools/desk_pack.py DESKS and the packs' own LICENSE files (RANK and NEO results only, SOLAR GFZ Kp CC BY 4.0 credited, FLU FluSight CC BY 4.0 credited, the rest US government work)
- P3: holds: record names as published on Zenodo
- P4: holds: no cause named, links only
- P5: n/a: no intervals
- P6: holds: the lines say only where the pack is deposited, the ATLAS desk lines say the data is inside the ATLAS Data Pack
- P7: holds: ledger rows zenodo.atlas.version, zenodo.atlas_desks.concept and zenodo.oy_desks.concept added before the release, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages read after build, the DOI lines found on the pages listed in the ledger rows
- P9: holds: plain sentences, no semicolons, no AI statements, no counts of our things in titles, creators as in the existing records
- P10: n/a: no rule set after the data

## 2026-11-11 Downloads refreshed from their sources on every ship, QIA List Pack and QIA Research Package rebuilt, zip sizes re-read for the pack.size rows
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the QIA List Pack held two entries removed at an author's request and the QIA Research Package held an older faults.pdf and t1t2 PLAN.md than their sources, ledger/downloads.py gate caught both, so the none is the gate reading each zip against its source
- II: n/a: no comparison between two runs, each zip is read against its own source file
- III: n/a: no signed difference is reported, sizes are levels of one file
- V: holds: two reads side by side, the list.json inside the pack and the published qia/list.json, csv rows and bib entries against the studies count, and every file inside the research package against the file it was copied from
- VI: n/a: no interval on these lines
- R: holds: zip sizes read from the rebuilt files in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 11 Nov 2026, QIA List Pack 881 KB and QIA Research Package 676 KB
- P1: n/a: no quoted text added to any page
- P2: holds: each size names its zip, which is linked beside it
- P3: holds: pack names as built, file names as served
- P4: holds: no cause named, sizes and links only
- P5: n/a: no intervals on these lines
- P6: holds: each line says what the zip holds, nothing stronger
- P7: holds: ledger rows pack.size.* edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages read after build, check_ledger drift 0 required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 AIRQ Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (92788c21dcb75ae7), size 8127 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 10 KB -> 11 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6fdc19aae9f9e210), size 10882 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 CAMPUS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 11 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (544325bf52699a32), size 10954 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 CONE Data Pack rebuilt by ledger/downloads.py: zip size 52 KB -> 55 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (fe0f310c3d793c40), size 56802 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 10 KB -> 11 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (2a95ad1e26a4dec9), size 11135 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 IRIS Research Package rebuilt by ledger/downloads.py: zip size 440 KB -> 441 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (abafce8fce38c9bc), size 451607 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 LINKROT Data Pack rebuilt by ledger/downloads.py: zip size 83 KB -> 85 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d3df7c0b58a5d9aa), size 86944 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 QUAKE Data Pack rebuilt by ledger/downloads.py: zip size 51 KB -> 54 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (cea47d533176ace2), size 55062 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 SECRECORDS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a44b110f9a51f974), size 8725 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 SUPPORT Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (78ea588e75ebb566), size 12776 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:00 TORNADO Data Pack rebuilt by ledger/downloads.py: zip size 27 KB -> 28 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (661dfd433befcd69), size 29108 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:06 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e6dda0907e18151c), size 7562 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:06, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:11 OY Data Pack rebuilt by ledger/downloads.py: zip size 162 KB -> 182 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (cd110f18890137e7), size 186818 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:11, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:33 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7882d8944dfeec2b), size 7819 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:33, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:53 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (584944b591f489b3), size 7577 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:53, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 09:53 QIA List Pack rebuilt by ledger/downloads.py: zip size 881 KB -> 882 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b985099c6c28260f), size 902938 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 09:53, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 10:37 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e9f2add63882da7b), size 7926 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 10:37, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 13:38 SECRECORDS Data Pack rebuilt by ledger/downloads.py: zip size 9 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (37091b7b37f17fa6), size 8605 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 13:38, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 13:38 WATER Data Pack rebuilt by ledger/downloads.py: zip size 766 KB -> 767 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (afda6abf9217424d), size 784919 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 13:38, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 16:15 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f9ae8fe25cbb01aa), size 7513 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 16:15, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 16:27 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d56e914a6684e5eb), size 8350 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 16:27, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 16:42 SECRECORDS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (57e335da99b39149), size 8729 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 16:42, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 17:42 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d103a67953fc407d), size 7561 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 17:42, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 19:08 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (904d67006eb7a006), size 7881 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 19:08, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 19:08 SECRECORDS Data Pack rebuilt by ledger/downloads.py: zip size 9 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b02250a250d4fdee), size 8605 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 19:08, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 20:35 WATER Data Pack rebuilt by ledger/downloads.py: zip size 767 KB -> 766 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (efe98910785a3405), size 784854 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 20:35, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 21:22 ARXIVDRIFT Data Pack rebuilt by ledger/downloads.py: zip size 126 KB -> 127 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (404121e5b4c859d9), size 130068 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 21:22, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 21:22 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1aad59e80b8bfaf7), size 7816 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 21:22, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-11 22:32 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (67ad372f36c4fb1b), size 7670 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-11 22:32, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 01:53 SECRECORDS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (fd5de59856a4f07e), size 8709 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 01:53, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 05:20 SECRECORDS Data Pack rebuilt by ledger/downloads.py: zip size 9 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f4894434b9ff1154), size 8598 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 05:20, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 05:36 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ee36d59578d42e11), size 7926 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 05:36, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 06:30 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (19ab1d66c0d43643), size 7652 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 06:30, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 06:30 SECRECORDS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (02296807474c1da7), size 8709 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 06:30, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 07:54 QIA List Pack rebuilt by ledger/downloads.py: zip size 882 KB -> 876 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f11e27602f74cf4d), size 896665 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 07:54, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 07:54 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d14e202d1a4968a8), size 7675 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 07:54, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 07:54 WEIGHTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b6c72e1055b2d678), size 8738 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 07:54, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 08:44 SECRECORDS Data Pack rebuilt by ledger/downloads.py: zip size 9 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (382921699e1dc0a4), size 8599 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 08:44, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 08:58 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (588ce0c5d7c3a44d), size 7822 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 08:58, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 08:58 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (61b5a05093b44c6e), size 7687 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 08:58, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:04 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 10 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (fe0ab66f3ec3ce56), size 13706 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:04, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:04 CADA Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7a062655d250616c), size 7980 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:04, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 11 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1fee03c10dbac853), size 13737 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 FEDSEP Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ac5e6ec3ab13b359), size 13808 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 11 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3687cb9ed0e0d54c), size 12753 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 MODEL Data Pack rebuilt by ledger/downloads.py: zip size 267 KB -> 272 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4f4af44de6aa849b), size 278019 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (bbd26c153cf6b7e1), size 7621 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 LINKROT Data Pack rebuilt by ledger/downloads.py: zip size 85 KB -> 86 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (41c4433d99c9747c), size 88045 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 REVISE Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8f9f731b2ffd9f4f), size 8405 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 SECRECORDS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8a3e6474cf0e87be), size 8718 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 SOCIAL Data Pack rebuilt by ledger/downloads.py: zip size 126 KB -> 128 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (042e7e9833146795), size 131572 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 STACK Data Pack rebuilt by ledger/downloads.py: zip size 18 KB -> 19 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a4a911ebead6d2f9), size 19914 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 SUPPORT Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ce61530c18d9c88b), size 13253 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 TIME Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (510b9dff30ec95b4), size 16671 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 TRIALS Data Pack rebuilt by ledger/downloads.py: zip size 35 KB -> 37 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ec715a934eb93697), size 37602 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 UPTIME Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (2abcc57e62eeda72), size 7682 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:05 WATER Data Pack rebuilt by ledger/downloads.py: zip size 766 KB -> 781 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (12b56bacc102b161), size 799437 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:08 OY Data Pack rebuilt by ledger/downloads.py: zip size 182 KB -> 183 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e6e1d6ef7ac49735), size 187235 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:08, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:12 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3eda33350de0e517), size 7989 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:12, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:12 UPTIME Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (75c50aa8960ebfb2), size 7678 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:12, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:15 UPTIME Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (9ed736262fd86810), size 7681 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:15, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:38 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8cf498559aa5496b), size 12843 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:38, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:46 CONE Data Pack rebuilt by ledger/downloads.py: zip size 55 KB -> 59 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (37f05a8cfc3c7959), size 60370 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:46, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:46 FEDSEP Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (357a4984be8d9f1e), size 13930 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:46, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:46 NEO Data Pack rebuilt by ledger/downloads.py: zip size 10 KB -> 11 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f4d46b79e08f6a77), size 11663 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:46, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 11:46 QUAKE Data Pack rebuilt by ledger/downloads.py: zip size 54 KB -> 57 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (0286947315dc8c0e), size 58141 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 11:46, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 12:03 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e07c800a3bdcdc42), size 13873 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 12:03, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 12:03 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (cdc31101be4adf66), size 12795 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 12:03, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 17:25 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6c3ee35e795ed940), size 7592 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 17:25, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 17:25 TORNADO Data Pack rebuilt by ledger/downloads.py: zip size 28 KB -> 31 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f7babeda4ced0871), size 31334 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 17:25, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 21:20 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (0373a019a4606907), size 13826 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 21:20, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 21:20 CHANGE Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6fa038beda7fb055), size 9019 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 21:20, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-12 21:20 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (2324b3ceef0d3fab), size 12875 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-12 21:20, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 00:39 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a9265ba841b0c58e), size 13432 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 00:39, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 00:39 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8881963eb23f736f), size 13813 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 00:39, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 00:39 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4db85a13fecacfdd), size 12778 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 00:39, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 03:53 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1cff8d3358cc33ec), size 8059 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 03:53, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 08:12 CREDIT Data Pack rebuilt by ledger/downloads.py: zip size 55 KB -> 58 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (406cc95c65885d86), size 58975 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 08:12, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 08:12 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (0c0cfc3e00ce02ff), size 12976 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 08:12, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 10:37 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b609631b0f11ae5d), size 13849 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 10:37, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 11:27 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (367537adb680774d), size 13801 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 11:27, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 12:17 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a5aa784549a487fe), size 12761 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 12:17, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 12:17 QIA Research Package rebuilt by ledger/downloads.py: zip size 676 KB -> 677 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4dadd78631d0da99), size 692768 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 12:17, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 12:30 QIA Research Package rebuilt by ledger/downloads.py: zip size 677 KB -> 676 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (611d6bfddde80b7c), size 692281 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 12:30, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 14:08 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ad9c434958c6874a), size 13879 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 14:08, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 14:44 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3a18474d23802351), size 13815 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 14:44, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 14:44 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (55d6a4e755391bb3), size 7623 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 14:44, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 14:44 QIA Research Package rebuilt by ledger/downloads.py: zip size 676 KB -> 680 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a9bc83c579d04f41), size 696695 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 14:44, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 14:58 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b9f6cdff8cad86f8), size 7808 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 14:58, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 15:34 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c32da6f1bba25828), size 7566 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 15:34, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 15:59 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (bfc307321a0ebe10), size 13980 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 15:59, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 16:09 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1b5a66d4e78cbfe0), size 7742 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 16:09, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 16:28 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c5ed3b54cb3d79e8), size 13824 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 16:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 16:28 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (830c0b2a55bcfe3e), size 7470 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 16:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 16:34 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e6d999393e27f5c5), size 13820 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 16:34, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 17:01 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (fdf54abf487baadd), size 13666 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 17:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 17:01 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (9b63ca7a106f8dd4), size 13826 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 17:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 17:01 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e3fea98cd4f994c6), size 7735 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 17:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 17:14 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (512b404914521b9b), size 14046 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 17:14, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 17:14 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8eb26b4cfc5cfb16), size 13822 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 17:14, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 17:34 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (51fb83c6f7c21326), size 7524 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 17:34, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 18:13 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (79dd6c4f9b1f1816), size 13769 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 18:13, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 18:21 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5c9ca7a5fa3c4958), size 13963 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 18:21, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 18:31 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (919bdae38fe12fdd), size 13811 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 18:31, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 18:31 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5b0be48773c14094), size 7701 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 18:31, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 18:37 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (0cfa7c76272f3aaa), size 13976 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 18:37, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 18:43 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (28940e94ff45b537), size 13824 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 18:43, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 18:43 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4742aa8e199725d9), size 7591 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 18:43, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 19:04 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (cb94636fc5560328), size 12855 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 19:04, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 19:33 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6dcd8c9f5e1e5ba9), size 7746 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 19:33, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 19:48 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8c293983c0893e3b), size 7313 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 19:48, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 20:27 QIA Research Package rebuilt by ledger/downloads.py: zip size 680 KB -> 681 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (eefa6efda245e95a), size 697059 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 20:27, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 21:10 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d68063005c1260d5), size 7825 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 21:10, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 21:16 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5146f9960e3af534), size 7647 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 21:16, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 21:28 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8ed2c7a10bf89f1d), size 13819 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 21:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 21:28 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (23822779ad7ca73b), size 7806 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 21:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 21:37 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6203111df7987a8b), size 13827 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 21:37, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 21:43 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c07e4c8b0601a19b), size 7597 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 21:43, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 21:57 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8514a2427c1f0814), size 13823 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 21:57, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 22:11 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d770173485e650ae), size 13827 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 22:11, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 22:44 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4c52f5d90e7fcbc4), size 13823 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 22:44, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 22:58 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (65e959ed9cd02859), size 13828 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 22:58, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-13 23:04 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (af9738b13d880831), size 13799 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-13 23:04, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 00:29 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d422a2369b3fec2c), size 13823 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 00:29, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 00:29 SOCIAL Data Pack rebuilt by ledger/downloads.py: zip size 128 KB -> 129 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4db1d48e5d0216fa), size 131988 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 00:29, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 00:29 WIKI Data Pack rebuilt by ledger/downloads.py: zip size 150 KB -> 151 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6ba1d77aad344340), size 154220 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 00:29, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 01:32 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (bc339a250a358895), size 13825 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 01:32, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 04:03 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (53e0ba6d2d1b53b1), size 13822 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 04:03, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 04:32 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 42 KB -> 43 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4ce23ad189900bcb), size 43567 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 04:32, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 04:48 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 43 KB -> 44 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (dd26e3c71fbdd0ef), size 45277 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 04:48, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 05:02 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ee1a7c7a83c9edc1), size 13829 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 05:02, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 05:02 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 44 KB -> 45 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (65f2644bb071f600), size 45585 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 05:02, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 05:35 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (313d7c641cfc86b9), size 13823 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 05:35, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 05:35 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 45 KB -> 47 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d3ee9289db436aab), size 47913 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 05:35, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 05:45 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (15f1ec17f9b95322), size 13824 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 05:45, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 06:00 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 47 KB -> 48 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (22fb17ccfe8244c2), size 48958 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 06:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 06:05 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ff5ce1561a9e73c4), size 13821 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 06:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 06:13 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7d28ed39a4c331eb), size 13826 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 06:13, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 06:30 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 48 KB -> 49 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ff82ce0948b3ed4b), size 50104 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 06:30, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 06:53 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (056b94e364577d37), size 13822 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 06:53, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 07:01 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (0207b0f785894c3b), size 13826 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 07:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 07:01 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 49 KB -> 50 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6c3bbdcca90d2c43), size 51060 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 07:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 07:01 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c97d88ad845fd732), size 16905 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 07:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 07:06 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (de5027edefaedf9b), size 16814 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 07:06, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 07:47 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 50 KB -> 51 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c3e33e551d31cb6a), size 52314 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 07:47, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 07:53 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 51 KB -> 52 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f7de49fd55dbc319), size 52767 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 07:53, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 07:58 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (30e4005d12e12f2b), size 13823 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 07:58, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 08:03 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (734661319a7d9101), size 13824 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 08:03, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 08:20 WEIGHTS Data Pack rebuilt by ledger/downloads.py: zip size 9 KB -> 10 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (088ed484f388e399), size 9747 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 08:20, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 08:34 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (9744ba847703a3f8), size 13823 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 08:34, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 08:34 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 52 KB -> 53 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a736f9d195094e5e), size 53955 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 08:34, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 08:46 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c3e0761faba10b76), size 13825 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 08:46, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 08:46 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4434f2384a8e7aa9), size 7767 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 08:46, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 09:01 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (92b64f7159dc34d3), size 7423 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 09:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 09:20 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 53 KB -> 54 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e56b5bef7e9c3715), size 55140 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 09:20, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 09:26 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (9a12d6beca0d871d), size 13821 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 09:26, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 09:41 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (89ddfc03e3773ff3), size 13826 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 09:41, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 09:55 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3e79fdb9324d2629), size 13823 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 09:55, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 09:55 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 54 KB -> 55 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5d802861b25edbbb), size 55850 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 09:55, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 10:27 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3f4280f266761f4d), size 13824 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 10:27, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 10:27 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (9605dd48a963e878), size 7710 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 10:27, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 10:38 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ecf0e0ac91a7afa3), size 7579 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 10:38, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 12:02 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 55 KB -> 56 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8c7d3046d1efb785), size 57216 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 12:02, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 13:31 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f92024c30cf83b52), size 13823 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 13:31, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 13:31 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 56 KB -> 57 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1c0893ecb1eb9ca9), size 58181 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 13:31, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 13:34 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (80a398c07ce5afc2), size 13828 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 13:34, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 17:54 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (97eeaf8a28e566d2), size 13815 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 17:54, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 17:54 HPT Data Pack rebuilt by ledger/downloads.py: zip size 85 KB -> 84 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (284d8955d9fff00c), size 86135 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 17:54, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 17:54 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 57 KB -> 58 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (eb7a5278cc48339f), size 59857 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 17:54, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 17:56 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7f0042180e3a2fa0), size 13825 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 17:56, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 18:00 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 58 KB -> 59 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (15f69c10878d66e6), size 59936 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 18:00, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 18:04 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (099a2acdb321c00a), size 13818 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 18:04, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 20:34 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5f7d35ff1ce78101), size 13828 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 20:34, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 20:34 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4e7efee40680111b), size 7725 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 20:34, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-14 20:34 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 59 KB -> 60 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3901bc7baf332282), size 61192 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-14 20:34, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 00:02 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7fd9cd3406264964), size 7195 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 00:02, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 00:02 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 60 KB -> 61 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (dabe28f3ec0488f8), size 62188 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 00:02, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 10:58 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (69360af6374c9bdb), size 7820 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 10:58, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 13:45 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (2d8375cc51f9bc95), size 14030 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 13:45, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 13:45 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a6c20f76c0b9d22d), size 7524 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 13:45, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 14:28 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7480194a5ab1df5f), size 8185 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 14:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 14:28 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 61 KB -> 62 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8f1562efb88b4cce), size 63082 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 14:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 16:38 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (160b37aee7c18e14), size 7576 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 16:38, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 16:46 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b3808c9b002053b3), size 7683 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 16:46, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 16:51 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f0bd31f04295659a), size 7426 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 16:51, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 18:16 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3e05778bec2adc44), size 13749 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 18:16, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 18:16 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b142a98c9b1ebb18), size 13821 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 18:16, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 21:17 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (fb0aba673e001130), size 13841 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 21:17, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 21:17 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3526b7e8b800f5c8), size 7828 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 21:17, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-15 21:17 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 62 KB -> 63 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b7af02f0755e35b2), size 64102 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-15 21:17, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 04:43 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (746dd60d732fe498), size 13819 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 04:43, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 04:43 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6ef448e0fbd5859c), size 12762 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 04:43, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 04:43 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d2c6d955c3fd780a), size 7592 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 04:43, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 08:04 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (07f765f022d57697), size 12859 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 08:04, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 08:04 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f858d48e39b7a38e), size 7861 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 08:04, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 08:04 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 63 KB -> 64 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (18aa6fc17d9c8018), size 65512 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 08:04, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 15:25 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (43dcf0015cde98db), size 12748 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 15:25, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 15:25 QIA List Pack rebuilt by ledger/downloads.py: zip size 876 KB -> 875 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (222a554731f7571a), size 895984 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 15:25, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 15:25 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 64 KB -> 65 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4dfb3cad63446ae8), size 66107 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 15:25, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 18:46 QIA List Pack rebuilt by ledger/downloads.py: zip size 875 KB -> 876 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (cbae95af292e1d3a), size 896995 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 18:46, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 19:28 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (68482f751e1f7c26), size 12830 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 19:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-16 20:33 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (01e2a014a55b7841), size 13824 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-16 20:33, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-17 04:22 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5200c5f5cb5d6428), size 12799 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-17 04:22, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-17 08:01 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6a2d80796870616e), size 12883 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-17 08:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-17 08:01 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4ad6877eac9ddb10), size 7569 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-17 08:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-17 08:01 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 65 KB -> 66 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ae42f20c6e98b63f), size 67371 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-17 08:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-17 11:35 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (13a454f8d9bef8ea), size 7875 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-17 11:35, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-17 20:19 WIKI Data Pack rebuilt by ledger/downloads.py: zip size 151 KB -> 147 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3f6138aa87220742), size 150392 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-17 20:19, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-17 23:43 QUAKE Data Pack rebuilt by ledger/downloads.py: zip size 57 KB -> 56 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c4041a754c2da56b), size 57707 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-17 23:43, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-17 23:43 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a342bfb4e40380cc), size 16915 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-17 23:43, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 03:03 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 66 KB -> 67 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6665f000498f24f8), size 68201 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 03:03, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 03:03 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b00490240a12dbfb), size 16648 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 03:03, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 03:03 WEIGHTS Data Pack rebuilt by ledger/downloads.py: zip size 10 KB -> 11 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c3e9eb0d7070b364), size 10768 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 03:03, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 06:30 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c9c35066646812fe), size 7633 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 06:30, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 11:25 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c94fe2ae28a9e8e8), size 7949 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 11:25, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 13:12 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (84c95bdd5fc4466e), size 7673 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 13:12, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 13:14 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1ca9e65db952cf7a), size 16954 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 13:14, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 16:23 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (4487034564e0f1b9), size 7883 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 16:23, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 16:23 QUAKE Data Pack rebuilt by ledger/downloads.py: zip size 56 KB -> 57 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a7b4bc83c7b192ae), size 57859 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 16:23, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 16:23 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a3da54bec65b3b43), size 16849 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 16:23, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 16:23 WATER Data Pack rebuilt by ledger/downloads.py: zip size 781 KB -> 783 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3db5f9c15be54bed), size 801366 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 16:23, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-18 23:12 ARXIVDRIFT Data Pack rebuilt by ledger/downloads.py: zip size 127 KB -> 128 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d7c2096d69e00baa), size 130734 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-18 23:12, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 02:28 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (80b3f12f5b21718b), size 12799 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 02:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 02:28 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (05886abdc0e05486), size 7446 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 02:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 05:40 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ca808a1b838be263), size 7834 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 05:40, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 08:57 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (498eb8e60ed50f57), size 12900 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 08:57, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 08:57 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5ff5badebf34a3d2), size 7609 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 08:57, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 08:57 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 67 KB -> 68 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6f5022e3ef4a53fb), size 69336 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 08:57, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 12:16 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (57719f194285a788), size 12795 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 12:16, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 12:16 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ca522197be0a5b41), size 8276 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 12:16, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 19:18 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1da0e51224dc1eb6), size 12900 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 19:18, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 19:18 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d660671acb916130), size 8898 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 19:18, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 19:18 WATER Data Pack rebuilt by ledger/downloads.py: zip size 783 KB -> 782 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f28061890d87f194), size 801103 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 19:18, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 19:57 MODEL Data Pack rebuilt by ledger/downloads.py: zip size 272 KB -> 271 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (0a239ab604861e08), size 278008 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 19:57, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 19:57 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 9 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (57f5ce7800aedc4c), size 8556 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 19:57, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 19:57 WATER Data Pack rebuilt by ledger/downloads.py: zip size 782 KB -> 783 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f66018c58a89b475), size 801408 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 19:57, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 19:59 QIA Research Package rebuilt by ledger/downloads.py: zip size 681 KB -> 677 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b831b8ba29411e9c), size 693310 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 19:59, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-19 22:42 QIA Research Package rebuilt by ledger/downloads.py: zip size 677 KB -> 678 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f139055fb4d9ee45), size 694779 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-19 22:42, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 05:41 PKGINSTALL Data Pack rebuilt by ledger/downloads.py: zip size 6 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (a178cdd3a2ab6cbc), size 6774 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 05:41, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 05:41 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 68 KB -> 69 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3e9a4a0bfbb12402), size 70471 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 05:41, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 05:41 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (0aa7a907b426e401), size 16911 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 05:41, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 05:42 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e880c08bfbeb8a62), size 16893 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 05:42, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 09:02 PKGINSTALL Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 6 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7741e70be0015616), size 6448 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 09:02, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 09:02 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (74147d65bd13d519), size 16928 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 09:02, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 09:02 WEIGHTS Data Pack rebuilt by ledger/downloads.py: zip size 11 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e6542a1bdafcdb8d), size 11783 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 09:02, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 11:53 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (75e8fea10dcdb0c7), size 16696 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 11:53, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 12:05 Zenodo sync: ATLAS Data Pack new version, version DOI doi:10.5281/zenodo.24110654 -> doi:10.5281/zenodo.24403684
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the record was versioned because the md5 of a file on the site differed from the md5 of the same file in its latest Zenodo version, so the none is the record against the site
- II: n/a: no comparison between two runs
- III: n/a: no signed difference is reported
- V: holds: two records side by side, the DOI in the Zenodo publish response and the DOI written to ledger/zenodo_dois.json and zenodo_packs/dois.json, and the md5 of each uploaded file read back from the new version
- VI: n/a: no interval outcome is claimed
- R: holds: the DOI read from the Zenodo publish response on 2026-11-20 12:05
- P1: n/a: no quoted text is added to any page
- P2: holds: the DOI links to doi.org
- P3: holds: record and file names as published
- P4: holds: no cause named
- P5: n/a: no intervals on this line
- P6: holds: the line says which version holds the pack, nothing stronger
- P7: holds: ledger rows edited before the page, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 12:24 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (0f8790ea5fe348f7), size 8840 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 12:24, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 12:30 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f39805b1d01aa27b), size 7621 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 12:30, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 12:30 WATER Data Pack rebuilt by ledger/downloads.py: zip size 783 KB -> 782 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (025382a07b71b4aa), size 801093 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 12:30, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 15:42 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (2b805e9003ed7743), size 7821 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 15:42, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 15:42 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 9 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8b52b93310356595), size 8641 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 15:42, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 15:42 WATER Data Pack rebuilt by ledger/downloads.py: zip size 782 KB -> 783 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7be0edfc2868976d), size 801405 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 15:42, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 19:13 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (6b8b3be479586d9c), size 7497 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 19:13, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 20:28 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (25d7f45a9a00ff2d), size 7791 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 20:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 20:32 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (0815f1b4d7cf813d), size 7650 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 20:32, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-20 22:31 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 69 KB -> 70 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3de234ec90cb7d97), size 71276 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-20 22:31, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 02:05 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (352630510327fc2c), size 13803 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 02:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 02:05 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 70 KB -> 69 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (faa884924d0340e8), size 71065 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 02:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 02:05 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (443c434500cbf2f1), size 16901 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 02:05, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 05:19 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c39f7e3b73536c45), size 16786 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 05:19, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 07:35 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 69 KB -> 70 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ed143a0502cc1ca4), size 71275 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 07:35, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 10:01 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5c574af85fa3b206), size 13859 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 10:01, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 10:28 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ccfb3c03fd425053), size 13785 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 10:28, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 10:48 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ae7664cfee0f0d5e), size 16966 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 10:48, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 10:59 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (2a51cd503e888e9a), size 13831 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 10:59, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 10:59 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (fe66e4169f969d8c), size 16874 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 10:59, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 11:46 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3c4097ddc1f5271a), size 13818 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 11:46, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 11:56 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (077dcf20dd22b7b8), size 13886 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 11:56, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 11:56 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (71806c0e082bfb45), size 16905 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 11:56, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 12:06 Zenodo sync: ATLAS Data Pack new version, version DOI doi:10.5281/zenodo.24403684 -> doi:10.5281/zenodo.24423534
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the record was versioned because the md5 of a file on the site differed from the md5 of the same file in its latest Zenodo version, so the none is the record against the site
- II: n/a: no comparison between two runs
- III: n/a: no signed difference is reported
- V: holds: two records side by side, the DOI in the Zenodo publish response and the DOI written to ledger/zenodo_dois.json and zenodo_packs/dois.json, and the md5 of each uploaded file read back from the new version
- VI: n/a: no interval outcome is claimed
- R: holds: the DOI read from the Zenodo publish response on 2026-11-21 12:06
- P1: n/a: no quoted text is added to any page
- P2: holds: the DOI links to doi.org
- P3: holds: record and file names as published
- P4: holds: no cause named
- P5: n/a: no intervals on this line
- P6: holds: the line says which version holds the pack, nothing stronger
- P7: holds: ledger rows edited before the page, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 12:09 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (91016dfba6c5a096), size 12793 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 12:09, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 12:09 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ca2ef446606b104d), size 16782 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 12:09, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 12:37 WATER Data Pack rebuilt by ledger/downloads.py: zip size 783 KB -> 782 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c95302264438a0de), size 801101 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 12:37, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 12:49 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (2525d80d095d320f), size 13816 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 12:49, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 13:10 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1d658824fb720345), size 16946 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 13:10, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 13:22 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (53b457a72c7e3d7c), size 16878 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 13:22, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 13:33 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5f49509a1cbf01b1), size 16899 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 13:33, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 13:33 WATER Data Pack rebuilt by ledger/downloads.py: zip size 782 KB -> 783 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (88cd273475672a70), size 801414 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 13:33, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 13:45 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c57124b91b6c4d8b), size 13882 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 13:45, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 13:45 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5de588a5f6ed3e7f), size 16695 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 13:45, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 14:39 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7ed17acd3b0c534d), size 13759 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 14:39, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 15:48 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (9f18cd3e9f08a53f), size 16940 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 15:48, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 16:03 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (bf8a298b3da2f1b0), size 16880 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 16:03, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 16:30 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e27017cff79a220c), size 16962 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 16:30, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 16:46 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (902d5216164f3caf), size 16840 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 16:46, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 17:14 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1908adbf8e9bcbd0), size 16958 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 17:14, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 17:25 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c829882f6c6a928c), size 16812 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 17:25, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 17:35 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (9a027f4fca9bee74), size 8851 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 17:35, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 17:57 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 9 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c869b30d149bfba2), size 8428 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 17:57, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 18:08 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7d6b000e34e77b4e), size 13824 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 18:08, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 18:08 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (9843dd39d86362ee), size 16904 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 18:08, the page prints that file
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 18:24 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (38bc1818649c00e7), size 13820 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 18:24, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 18:24 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (d1bc6c9a83678241), size 16856 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 18:24, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 18:25 QIA Research Package rebuilt by ledger/downloads.py: zip size 678 KB -> 679 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (320d07df21ed6d70), size 695089 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 18:25, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 18:40 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e7892d900fac3abd), size 16986 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 18:40, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 19:05 FORECAST Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (2ae63ebcd5f8d2e1), size 12905 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 19:05, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 19:26 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (225b3074b48d9ce4), size 16883 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 19:26, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 19:49 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (e3734513cbf7e60b), size 16952 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 19:49, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 20:22 NEO Data Pack rebuilt by ledger/downloads.py: zip size 11 KB -> 12 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (8a09b70e7e9883aa), size 11778 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 20:22, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 20:22 QUAKE Data Pack rebuilt by ledger/downloads.py: zip size 57 KB -> 56 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3c8438e34a8df7fd), size 57801 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 20:22, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 20:22 TAPE Data Pack rebuilt by ledger/downloads.py: zip size 70 KB -> 71 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7c837550b12b7251), size 72221 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 20:22, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 21:14 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1cade33787731db0), size 13824 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 21:14, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 21:14 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (13bc4badbc908151), size 16834 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 21:14, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 21:20 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (af3c0b78d0107d63), size 13820 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 21:20, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 21:24 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (7af4edffc9d72ee4), size 8113 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 21:24, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 21:24 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (c5d537b348a116a7), size 16975 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 21:24, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 21:35 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (68b4b741eabd8108), size 16849 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 21:35, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 21:38 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (77f299db8840c31e), size 13836 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 21:38, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 21:38 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (ff25e1bd84a9ac30), size 7610 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 21:38, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-21 22:16 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3f4aac2fbb398bb5), size 16901 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-21 22:16, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 01:41 NEO Data Pack rebuilt by ledger/downloads.py: zip size 12 KB -> 11 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (bf9ab4a5a0c36d47), size 11761 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 01:41, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 01:41 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 9 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (aabce9c7efd09954), size 9136 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 01:41, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 01:41 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (06dbe7bcaf034bc3), size 16876 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 01:41, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 05:03 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (fbcd7b6308b95b17), size 13823 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 05:03, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 05:03 SEAT Data Pack rebuilt by ledger/downloads.py: zip size 9 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (30b8893f15ee8964), size 8448 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 05:03, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 05:03 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f3cca3a3c6ed64fc), size 16897 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 05:03, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 06:47 CADENCE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (f2c7017725891953), size 13829 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 06:47, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 06:47 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (b35cbe6d2a3ba0ab), size 16808 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 06:47, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 07:28 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 7 KB -> 8 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (31b83cd4194af70a), size 7821 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 07:28, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 09:48 HOSTS Data Pack rebuilt by ledger/downloads.py: zip size 8 KB -> 7 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (5d655b5d53a5c26d), size 7178 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 09:48, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 11:27 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (3be98ed4aaec93df), size 13833 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 11:27, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 11:47 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 14 KB -> 13 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (59dd774a180b9d61), size 13822 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 11:47, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 11:47 TIME Data Pack rebuilt by ledger/downloads.py: zip size 16 KB -> 17 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (194e5277610fdb83), size 16912 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 11:47, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 12:11 AIRLINE Data Pack rebuilt by ledger/downloads.py: zip size 13 KB -> 14 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (34b0e608ae98f138), size 13868 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 12:11, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data

## 2026-11-22 12:21 TIME Data Pack rebuilt by ledger/downloads.py: zip size 17 KB -> 16 KB
packs: P
(answer each line: holds:/fixed:/caught:/n/a:/cannot tell: followed by what was checked)
- I: holds: the pack was rebuilt because a hash of its inputs differed from the hash recorded when it was last made (ledger/pack_inputs.json), and its contents differ from the zip it replaces, so the none is the pack against its own inputs
- II: n/a: no comparison between two runs, one file size read before and after
- III: n/a: no signed difference is reported, a size is a level of one file
- V: holds: two counts side by side, the zip was opened again and its sha256 sidecar read back (1cfd3c58e31301dc), size 16818 bytes
- VI: n/a: no interval outcome is claimed
- R: holds: size read from the file in public/ by tools/desk_pack.py sizes into tools/desk_packs/pack_sizes.json on 2026-11-22 12:21, the page prints that file
- X: holds: no earlier reading corrected, a rebuilt pack replaces a zip whose inputs changed, the old size was right for the old zip
- P1: n/a: no quoted text is added to any page
- P2: holds: the size names its zip, linked beside it
- P3: holds: pack name as built, file name as served
- P4: holds: no cause named, a size and a link only
- P5: n/a: no intervals on this line
- P6: holds: the line says what the zip holds, nothing stronger
- P7: holds: the pack.size row is edited before the surface, release through ledger/ship.sh under site_lock
- P8: holds: rendered pages are read after build, check_ledger drift 0 is required before the ship completes
- P9: holds: plain sentences, no semicolons, no AI statements, Heuremen LLC
- P10: n/a: no rule set after the data
