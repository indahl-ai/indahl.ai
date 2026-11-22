#!/usr/bin/env python3
"""fetch_outlooks.py: pull the NIFC monthly outlook archive ZIPs named on the outlooks page.

Untrusted downloads land in data/raw/outlooks/ as data only. Nothing in them is executed.
One request at a time, 1.5 s apart, public and keyless. Files already on disk are kept.
Writes data/outlook_manifest.json: issue, url, bytes, sha256, member list, whether any PSA polygon file is inside.
"""
import hashlib, json, os, re, sys, time, urllib.parse, urllib.request, zipfile

H = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(H, "data", "raw", "outlooks")
PAGE = os.path.join(H, "data", "raw", "nifc", "outlooks_page.html")
UA = "heuremen-prometheus/0.1 (+https://indahl.ai/prometheus)"
BASE = "https://www.nifc.gov"
MON = {"JFMA": 1, "FMAM": 2, "MAMJ": 3, "AMJJ": 4, "MJJA": 5, "MJJA_": 5, "JJAS": 6, "JASO": 7, "ASON": 8, "SOND": 9, "ONDJ": 10, "NDJF": 11, "DJFM": 12}
POLY = (".shp", ".kml", ".kmz", ".geojson", ".gdb", ".gpkg")   # the same list as prometheus_tick.py


def get(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest + ".part", "wb") as f:
        while True:
            b = r.read(1 << 16)
            if not b:
                break
            f.write(b)
    os.replace(dest + ".part", dest)


def main():
    os.makedirs(RAW, exist_ok=True)
    if not os.path.exists(PAGE) or "--refresh" in sys.argv:
        os.makedirs(os.path.dirname(PAGE), exist_ok=True)
        get(BASE + "/nicc/predictive-services/outlooks", PAGE)
    html = open(PAGE, encoding="utf-8", errors="replace").read()
    hrefs = sorted(set(re.findall(r'href="(/sites/default/files/NICC/2-Predictive%20Services/Outlooks/NSWF%20-%20Potential%20Outlook%20-%20Archive/[^"]+\.zip)"', html)))
    rows = []
    for h in hrefs:
        name = urllib.parse.unquote(h.rsplit("/", 1)[1])
        year = int(re.search(r"Archive/(\d{4})/", h).group(1))
        code = re.search(r"(JFMA|FMAM|MAMJ|AMJJ|MJJA|JJAS|JASO|ASON|SOND|ONDJ|NDJF|DJFM)", name).group(1)
        issue = "%04d-%02d" % (year, MON[code])
        dest = os.path.join(RAW, "%s_%s.zip" % (issue, code))
        row = {"issue": issue, "code": code, "url": BASE + h, "file": os.path.relpath(dest, H)}
        if not os.path.exists(dest):
            try:
                get(BASE + h, dest)
                time.sleep(1.5)
            except Exception as e:  # nothing returned is its own outcome
                row["error"] = "%s" % (e,)
                rows.append(row)
                continue
        b = open(dest, "rb").read()
        row["bytes"] = len(b)
        row["sha256"] = hashlib.sha256(b).hexdigest()
        try:
            with zipfile.ZipFile(dest) as z:
                names = z.namelist()
        except zipfile.BadZipFile:
            names, row["error"] = [], "unreadable zip"
        row["members"] = names
        row["has_psa_polygons"] = any(n.lower().endswith(POLY) for n in names)
        rows.append(row)
    rows.sort(key=lambda r: r["issue"])
    json.dump({"fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "issues": rows},
              open(os.path.join(H, "data", "outlook_manifest.json"), "w"), indent=1)
    for r in rows:
        print(r["issue"], r.get("bytes"), "polygons" if r.get("has_psa_polygons") else "no polygons", r.get("error", ""))


if __name__ == "__main__":
    main()
