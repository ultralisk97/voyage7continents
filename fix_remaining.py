#!/usr/bin/env python3
"""Fix the 7 remaining images via Commons API with browser UA and delays."""
import json, os, time, urllib.parse, urllib.request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "articles")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

TARGETS = [
    ("valise-usa-4.jpg",     "hiker backpack mountain"),
    ("shopping-usa-4.jpg",   "Manhattan Fifth Avenue shopping"),
    ("castiglione-4.jpg",    "Castiglione della Pescaia porto"),
    ("plage-canella-4.jpg",  "Santa Giulia Porto Vecchio"),
    ("morro-sao-paulo-5.jpg","Ilha Tinhare Bahia"),
]

BAD = ["map", "coat of arms", "logo", "flag", "diagram", "drawing", "poster", ".svg", "engraving", "cartoon", "illustration"]

def req(url):
    r = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return resp.read()

def api(params):
    params = {**params, "format": "json"}
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    return json.loads(req(url).decode("utf-8"))

def search(query):
    d = api({"action": "query", "list": "search",
             "srsearch": query + " filetype:bitmap",
             "srnamespace": 6, "srlimit": 15})
    for h in d.get("query", {}).get("search", []):
        t = h["title"].lower()
        if any(b in t for b in BAD):
            continue
        return h["title"]
    return None

def thumb(title, w=1024):
    d = api({"action": "query", "titles": title, "prop": "imageinfo",
             "iiprop": "url|mime", "iiurlwidth": w})
    for _, p in d.get("query", {}).get("pages", {}).items():
        info = p.get("imageinfo", [])
        if info and info[0].get("mime") in ("image/jpeg", "image/png"):
            return info[0].get("thumburl") or info[0].get("url")
    return None

for fname, query in TARGETS:
    try:
        title = search(query)
        if not title:
            print(f"MISS search {fname}")
            continue
        url = thumb(title)
        if not url:
            print(f"MISS thumb {fname} {title}")
            continue
        data = req(url)
        dest = os.path.join(OUT, fname)
        with open(dest, "wb") as f:
            f.write(data)
        print(f"OK {fname}  {len(data)}  {title}")
        time.sleep(1.5)
    except Exception as e:
        print(f"ERR {fname}: {e}")
        time.sleep(3)
print("done")
