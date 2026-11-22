# Ledger coverage of indahl.ai top-level pages, 17 Nov 2026

17 Nov 2026, the owner: consistency site-wide; removal automated in the page builders. Generated from ledger/ledger.py SURFACES and ledger/ledger.jsonl
by a one-off script (ledger state after the SAGAR rows were added). Listed only; nothing migrated.

A page is **ledger-backed** when a SURFACES key points at its built file and live rows are checked against it by check_ledger.py.
Pages without their own key may still be checked in part through the `indahl` surface (build_site.py source text, 2 live rows); that
checks the generator source, not the built page, so it is noted, not counted as coverage.

Top-level pages: 96. Ledger-backed: 47. Key but no live rows: 3. Not ledger-backed: 46.

## Ledger-backed (SURFACES key and live rows)

| Page | Surface key(s) | Live rows |
|---|---|---|
| ailuminate.html | desk_ailuminate | 1 |
| airline.html | desk_airline | 1 |
| airq.html | desk_airq | 1 |
| atlas.html | atlas | 108 |
| cadence.html | desk_cadence | 1 |
| campus.html | desk_campus | 1 |
| change.html | desk_change | 1 |
| cone.html | desk_cone | 23 |
| credit.html | desk_credit | 14 |
| downloads.html | downloads | 43 |
| fedsep.html | desk_fedsep | 1 |
| flu.html | desk_flu | 11 |
| forecast.html | forecast | 5 |
| forecasters.html | forecasters | 3 |
| hermes.html | hermes | 1 |
| hfsize.html | desk_hfsize | 1 |
| hosts.html | desk_hosts | 1 |
| hpt.html | desk_hpt | 1 |
| iris.html | iris_matrix | 50 |
| launch.html | desk_launch | 1 |
| linkrot.html | desk_linkrot | 340 |
| media.html | media | 10 |
| model_all.html | sad | 777 |
| neo.html | desk_neo | 14 |
| oy.html | oy_matrix | 46 |
| pkginstall.html | desk_pkginstall | 1 |
| pkglicense.html | desk_pkglicense | 1 |
| predictions.html | desk_now | 9 |
| qia.html | qia_matrix | 132 |
| quake.html | desk_quake | 30 |
| rank.html | desk_rank | 38 |
| revise.html | desk_revise | 1 |
| sagar.html | sagar | 162 |
| seasonal.html | desk_seasonal | 10 |
| secrecords.html | desk_secrecords | 1 |
| social.html | social | 15 |
| solar.html | desk_solar | 12 |
| steo.html | desk_steo | 13 |
| support.html | desk_support | 1 |
| tape.html | desk_tape | 1 |
| tornado.html | desk_tornado | 11 |
| trials.html | desk_trials | 2 |
| verify.html | verify_page | 1 |
| water.html | water | 11 |
| weights.html | desk_weights | 1 |
| wiki.html | wiki | 18 |
| yo.html | yo | 22 |

## Has a SURFACES key but no live rows

| Page | Surface key(s) | Rows (any status) |
|---|---|---|
| census.html | census | 0 |
| petrol.html | desk_petrol | 0 |
| web.html | web | 0 |

## Not ledger-backed (no SURFACES key)

404.html, agree.html, alerts.html, api.html, arxivdrift.html, brand.html, caca.html, cada.html, changelog.html, changes.html, coin.html, community.html, conflict-of-interest.html, connect.html, contact.html, correction.html, darkwave.html, developers.html, feed-entries.html, follow.html, hflicense.html, how.html, index.html, inquire-error.html, inquire-ok.html, inquiry.html, mydata.html, newsletter.html, now.html, plugins.html, privacy.html, reproduce.html, respond.html, seat.html, security.html, services.html, stack.html, standard.html, terms.html, time.html, transparency.html, try.html, uptime.html, vault.html, webhooks.html, week.html

## Also covered, not top-level

- indahl-ai/sagar/study/*.html: surface `sagar_study` (folder surface, 162 live rows), added 17 Nov 2026.
- Sub-pages with their own keys: atlas/*, qia/process.html, qia/studies/*, iris/lab*.html, census/*, newsletter/0.html, security/self.html, hermes/model/data-pack.html, oy/data-pack.html, media/2026-10-26.html, model_all.html (SAD).

## Notes

- QIA and IRIS study pages (indahl-ai/qia/study, indahl-ai/iris/study) have no surface key. They are built from the same table cells as qia.html / iris.html rows, and removed_gate.py covers removals, but their text is not ledger-checked.
- Many unbacked pages are legal, process, form or navigation pages with no numbers (terms, contact, correction, agree, 404). Desk pages among them that print numbers are the migration candidates: arxivdrift, hflicense, seat, stack, time, uptime, cada, now, week, coin, darkwave (its key `darkwave` points at heuremen.org/darkwave.html since 16 Nov, so the indahl-ai copy is unchecked), standard, transparency, index (home).
- census.html, petrol.html and web.html have keys but zero live rows: the key is there, but nothing on those pages is checked.
