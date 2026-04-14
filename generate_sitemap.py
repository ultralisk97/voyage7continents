#!/usr/bin/env python3
"""Génère sitemap.xml et robots.txt à partir de tous les .html du repo."""
import os
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://voyage7continents.fr"
TODAY = date.today().isoformat()

SKIP_FILES = {"mentions-legales.html", "politique-confidentialite.html"}

# Priorités et changefreq par type de page
def meta_for(rel_path):
    if rel_path == "":
        return ("1.0", "weekly")
    parts = rel_path.split("/")
    if parts[-1] == "index.html" and len(parts) == 2:
        return ("0.9", "weekly")  # page catégorie
    if rel_path in {"mentions-legales.html", "politique-confidentialite.html"}:
        return ("0.2", "yearly")
    return ("0.7", "monthly")  # article

urls = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    # Skip .git, node_modules, etc.
    dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in {"img", "css", "js"}]
    for fn in sorted(filenames):
        if not fn.endswith(".html"):
            continue
        abs_path = os.path.join(dirpath, fn)
        rel = os.path.relpath(abs_path, ROOT).replace(os.sep, "/")
        if rel == "index.html":
            url = BASE + "/"
            key = ""
        elif rel.endswith("/index.html"):
            url = BASE + "/" + rel[:-len("index.html")]
            key = rel
        else:
            url = BASE + "/" + rel
            key = rel
        prio, freq = meta_for(key)
        urls.append((url, prio, freq))

# Ordre : racine, catégories, articles, pages légales
def sort_key(u):
    url = u[0]
    if url == BASE + "/":
        return (0, url)
    if url.endswith("/"):
        return (1, url)
    if "mentions-legales" in url or "politique-confidentialite" in url:
        return (3, url)
    return (2, url)

urls.sort(key=sort_key)

out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url, prio, freq in urls:
    out.append("  <url>")
    out.append(f"    <loc>{url}</loc>")
    out.append(f"    <lastmod>{TODAY}</lastmod>")
    out.append(f"    <changefreq>{freq}</changefreq>")
    out.append(f"    <priority>{prio}</priority>")
    out.append("  </url>")
out.append("</urlset>")
out.append("")

with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"wrote sitemap.xml  ({len(urls)} URLs)")

robots = f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
"""
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots)
print("wrote robots.txt")
