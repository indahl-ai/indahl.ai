# Heuremen Standard V1.1: publish-time steps (internal)

> DONE 21 Nov 2026: published as Zenodo version 2.1.0, doi 10.5281/zenodo.24430790, files in faultsguards/standard_2_1 (page copier: faultsguards/standard_2_1/web/build_page.py). CURRENT.json points there. The steps below are kept as the pattern for the next version.

The public name "The Heuremen Standard" (no version number in any visible copy, owner 21 Nov 2026) is served from
`faultsguards/CURRENT.json` (name, title, short, nav). Until the V1.1 Zenodo version is published, CURRENT.json points at the published
record (internal: Faults and Guards 2.0.0, doi 10.5281/zenodo.24164794, files in faultsguards/standard_v1). Only the record fields
(version, record_title, doi, files_dir) change at publish; builders never print version or record_title, only the DOI link.

1. Publish V1.1 on Zenodo as a new version of concept DOI 10.5281/zenodo.24164029. Note the new version DOI.
2. Put the V1.1 files in a NEW folder, e.g. `faultsguards/standard_v1_1_released/` (STANDARD.md, standard_v1.json, schema, CHECKLIST.md,
   CROSSWALK.md, LICENSE.txt, SHA256SUMS.txt, .ots). Never edit the stamped files in faultsguards/standard_v1/.
   Its standard_v1.json `standard` block must carry version "1.1", the new doi and the concept doi.
3. Edit `faultsguards/CURRENT.json` only:
   - `"version": "1.1"`
   - `"record_title": "Heuremen Standard 1.1"` (internal)
   - `"doi": "<new version DOI>"`
   - `"files_dir": "faultsguards/standard_v1_1_released"` (and `"json_file"` if the file name changed)
4. If the files folder changed, point `faultsguards/standard_v1/web/build_page.py` at it (it still reads files from its own folder
   `H`) or copy it as `<new folder>/web/build_page.py`, then run it: it copies the files to public/standard/ and writes the DOI line from CURRENT.json.
5. Build and check, under the lock:
   ```bash
   cd ~/forge && python3 ledger/site_lock.py run --label "Heuremen Standard V1.1 record" -- bash -c '
     python3 faultsguards/standard_v1/web/build_page.py &&
     (cd indahl-ai && python3 build_site.py && python3 qia_site.py | tail -1) &&
     python3 ledger/check_ledger.py | head -3 && python3 ledger/spelling_gate.py | tail -2 &&
     python3 ledger/link_gate.py | tail -2 && python3 ledger/name_gate.py | tail -2 &&
     bash ledger/ship_request.sh "Heuremen Standard V1.1: record and DOI"'
   ```
6. Confirm live: `curl -s https://indahl.ai/standard | grep -o 'doi:10.5281/zenodo.[0-9]*'` shows the new DOI (no version label is printed);
   `curl -s https://indahl.ai/llms.txt | grep 'The Heuremen Standard'`; the MCP card (`standards_card`) prints the new DOI
   (it reads indahl-ai/standard_current.js, written from CURRENT.json on every build).
