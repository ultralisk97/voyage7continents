#!/usr/bin/env python3
"""Second pass: replace bad Wikimedia picks with hand-curated File:... titles."""
import json, os, urllib.parse, urllib.request, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "img", "articles")
UA = "voyage7continents-bot/1.0"

# Hand-picked replacements: (output filename, Wikimedia File:title)
FIXES = [
    ("vermont-1.jpg",       "File:Fall Foliage, East Haven, Vermont.jpg"),
    ("maine-5.jpg",         "File:Pemaquid Point Light, Maine.jpg"),
    ("preparer-usa-2.jpg",  "File:United States Passport.jpg"),
    ("preparer-usa-4.jpg",  "File:Boeing 777-200ER American Airlines (AAL) N751AN - MSN 30012 233 (9528311773).jpg"),
    ("preparer-usa-5.jpg",  "File:Statue of Liberty 7.jpg"),
    ("valise-usa-2.jpg",    "File:Suitcase clothes packed travel.jpg"),
    ("valise-usa-4.jpg",    "File:Backpack and passport travel.jpg"),
    ("shopping-usa-4.jpg",  "File:Times Square, New York City (HDR).jpg"),
    ("castiglione-4.jpg",   "File:Castiglione della Pescaia-vista.jpg"),
    ("plage-canella-3.jpg", "File:Plage de Palombaggia Corse.jpg"),
    ("plage-canella-4.jpg", "File:Palombaggia beach Corsica.jpg"),
    ("morro-sao-paulo-3.jpg","File:Farol de Morro de Sao Paulo.jpg"),
    ("morro-sao-paulo-5.jpg","File:Morro de Sao Paulo sunset.jpg"),
]

def api_get(params):
    params = {**params, "format": "json"}
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def find_file(query):
    """Search and return best bitmap File:title."""
    data = api_get({
        "action": "query", "list": "search",
        "srsearch": query + " filetype:bitmap",
        "srnamespace": 6, "srlimit": 10,
    })
    for hit in data.get("query", {}).get("search", []):
        t = hit["title"]
        low = t.lower()
        if any(b in low for b in ["map", "coat of arms", "logo", "flag", "diagram", "drawing", "poster", ".svg", "engraving"]):
            continue
        return t
    return None

def get_thumb(title, width=1024):
    data = api_get({
        "action": "query", "titles": title,
        "prop": "imageinfo", "iiprop": "url|mime|size",
        "iiurlwidth": width,
    })
    for _, page in data.get("query", {}).get("pages", {}).items():
        info = page.get("imageinfo", [])
        if info and info[0].get("mime") in ("image/jpeg", "image/png"):
            return info[0].get("thumburl") or info[0].get("url")
    return None

def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)

# Fallback search queries per filename (when hand-picked title doesn't exist)
FALLBACK = {
    "vermont-1.jpg":       "Vermont fall foliage photograph",
    "maine-5.jpg":         "Pemaquid Point Light",
    "preparer-usa-2.jpg":  "United States passport book",
    "preparer-usa-4.jpg":  "American Airlines Boeing airport",
    "preparer-usa-5.jpg":  "Statue of Liberty New York photo",
    "valise-usa-2.jpg":    "packed suitcase luggage clothes",
    "valise-usa-4.jpg":    "backpacker traveler airport",
    "shopping-usa-4.jpg":  "Times Square New York night",
    "castiglione-4.jpg":   "Castiglione della Pescaia harbor",
    "plage-canella-3.jpg": "Palombaggia Corsica beach",
    "plage-canella-4.jpg": "Santa Giulia beach Corsica",
    "morro-sao-paulo-3.jpg":"Morro de Sao Paulo Farol",
    "morro-sao-paulo-5.jpg":"Morro de Sao Paulo village",
}

for fname, title in FIXES:
    dest = os.path.join(OUT, fname)
    # Try the hand-picked title, then fallback to search
    url = get_thumb(title, 1024)
    if not url:
        q = FALLBACK.get(fname, title.replace("File:", "").replace(".jpg", ""))
        t2 = find_file(q)
        if t2:
            print(f"  fallback {fname} -> {t2}")
            url = get_thumb(t2, 1024)
    if not url:
        print(f"MISS {fname}")
        continue
    try:
        sz = download(url, dest)
        print(f"OK {fname}  {sz}")
    except Exception as e:
        print(f"ERR {fname} {e}")
print("done")
