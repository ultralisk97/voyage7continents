#!/usr/bin/env python3
"""Fetch article images with multi-source fallback: Unsplash -> Pexels -> Wikimedia.

Usage:
    python3 fetch_images.py <slug> [slug2 ...]       # batch from SPEC
    python3 fetch_images.py --only-hero <slug>       # only index 1 (hero)
    python3 fetch_images.py --force <slug>           # overwrite existing files

Reads keys from ~/.image_api_keys (UNSPLASH_KEY, PEXELS_KEY).
Falls back to fetch_wikimedia.py SPEC dict for queries (shared source of truth).
Writes to img/articles/<slug>-<n>.jpg (n in 1..5).
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "img", "articles")
os.makedirs(OUT, exist_ok=True)

# --- Load keys ---
KEYS_PATH = os.path.expanduser("~/.image_api_keys")
KEYS = {}
if os.path.exists(KEYS_PATH):
    with open(KEYS_PATH) as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                KEYS[k] = v
UNSPLASH_KEY = KEYS.get("UNSPLASH_KEY", "")
PEXELS_KEY = KEYS.get("PEXELS_KEY", "")

UA = "voyage7continents/1.0 (contact@voyage7continents.fr)"

# --- Import query SPEC from fetch_wikimedia.py ---
sys.path.insert(0, ROOT)
from fetch_wikimedia import SPEC as WIKI_SPEC  # noqa: E402

# --- HTTP helpers ---
def http_get_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def http_download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)

# --- Source: Unsplash ---
def search_unsplash(query, used_ids=None):
    if not UNSPLASH_KEY:
        return None
    used_ids = used_ids or set()
    url = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode({
        "query": query,
        "per_page": 10,
        "orientation": "landscape",
        "content_filter": "high",
    })
    try:
        data = http_get_json(url, headers={
            "Authorization": f"Client-ID {UNSPLASH_KEY}",
            "Accept-Version": "v1",
            "User-Agent": UA,
        })
    except urllib.error.HTTPError as e:
        print(f"   unsplash HTTP {e.code}", flush=True)
        return None
    except Exception as e:
        print(f"   unsplash err {e}", flush=True)
        return None
    for p in data.get("results", []):
        if p["id"] in used_ids:
            continue
        if p.get("width", 0) < 1200:
            continue
        return {
            "source": "unsplash",
            "id": p["id"],
            "download": p["urls"]["raw"] + "&w=1600&q=80&fm=jpg&fit=max",
        }
    return None

# --- Source: Pexels ---
def search_pexels(query, used_ids=None):
    if not PEXELS_KEY:
        return None
    used_ids = used_ids or set()
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode({
        "query": query,
        "per_page": 10,
        "orientation": "landscape",
        "size": "large",
    })
    try:
        data = http_get_json(url, headers={
            "Authorization": PEXELS_KEY,
            "User-Agent": UA,
        })
    except urllib.error.HTTPError as e:
        print(f"   pexels HTTP {e.code}", flush=True)
        return None
    except Exception as e:
        print(f"   pexels err {e}", flush=True)
        return None
    for p in data.get("photos", []):
        if p["id"] in used_ids:
            continue
        if p.get("width", 0) < 1200:
            continue
        return {
            "source": "pexels",
            "id": p["id"],
            "download": p["src"]["large2x"],
        }
    return None

# --- Source: Wikimedia (fallback) ---
WIKI_SKIP_RE = re.compile(
    r"\.(svg|tif|tiff)$"
    r"|flag|coat.of.arms|map of|location map|logo|seal of"
    r"|diagram|chart|graph|blank|silhouette",
    re.IGNORECASE,
)

def search_wikimedia(query, used_ids=None):
    used_ids = used_ids or set()
    api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": "6",
        "gsrlimit": "10",
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "iiurlwidth": "1600",
    })
    try:
        data = http_get_json(api, headers={"User-Agent": UA})
    except Exception as e:
        print(f"   wiki err {e}", flush=True)
        return None
    pages = data.get("query", {}).get("pages", {}) or {}
    for _, p in pages.items():
        title = p.get("title", "")
        if WIKI_SKIP_RE.search(title):
            continue
        if title in used_ids:
            continue
        ii = (p.get("imageinfo") or [{}])[0]
        thumb = ii.get("thumburl")
        if not thumb:
            continue
        if ii.get("width", 0) < 800:
            continue
        return {"source": "wikimedia", "id": title, "download": thumb}
    return None

# --- Orchestration ---
def fetch_one(slug, n, query, used_ids, force=False):
    dest = os.path.join(OUT, f"{slug}-{n}.jpg")
    if os.path.exists(dest) and os.path.getsize(dest) > 20000 and not force:
        print(f"SKIP {slug}-{n}  (exists)", flush=True)
        return True
    for fn, label in ((search_unsplash, "unsplash"),
                      (search_pexels, "pexels"),
                      (search_wikimedia, "wikimedia")):
        res = fn(query, used_ids.get(label, set()))
        if res:
            try:
                size = http_download(res["download"], dest)
            except Exception as e:
                print(f"   dl err from {label}: {e}", flush=True)
                continue
            used_ids.setdefault(label, set()).add(res["id"])
            print(f"OK   {slug}-{n:1d}  [{label:9s}]  {size:>8} bytes  {query[:60]}", flush=True)
            return True
        time.sleep(0.3)
    print(f"MISS {slug}-{n}  (all sources failed)  query={query}", flush=True)
    return False

def fetch_slug(slug, force=False, only_hero=False):
    queries = WIKI_SPEC.get(slug)
    if not queries:
        print(f"!! no SPEC for slug '{slug}' — add it to fetch_wikimedia.py first")
        return
    used = {}
    indices = [1] if only_hero else list(range(1, len(queries) + 1))
    for idx in indices:
        q = queries[idx - 1]
        fetch_one(slug, idx, q, used, force=force)
        time.sleep(0.4)

def main(argv):
    args = list(argv[1:])
    force = False
    only_hero = False
    if "--force" in args:
        force = True
        args.remove("--force")
    if "--only-hero" in args:
        only_hero = True
        args.remove("--only-hero")
    if not args:
        print(__doc__)
        sys.exit(1)
    for slug in args:
        print(f"=== {slug} ===", flush=True)
        fetch_slug(slug, force=force, only_hero=only_hero)

if __name__ == "__main__":
    main(sys.argv)
