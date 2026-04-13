#!/usr/bin/env python3
"""Migrate flat URL structure to /category/article.html layout."""
import os
import re
import shutil
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

CATEGORIES = ["europe", "asie", "afrique", "amerique-nord", "amerique-sud", "oceanie", "antarctique"]

# Build file move map: old_path -> new_path
moves = {}

# Category pages: europe.html -> europe/index.html
for cat in CATEGORIES:
    if os.path.exists(f"{cat}.html"):
        moves[f"{cat}.html"] = f"{cat}/index.html"

# Article pages: europe-xxx.html -> europe/xxx.html
for fname in sorted(os.listdir(".")):
    if not fname.endswith(".html"):
        continue
    for cat in CATEGORIES:
        prefix = cat + "-"
        if fname.startswith(prefix):
            new = f"{cat}/{fname[len(prefix):]}"
            moves[fname] = new
            break

# Create dirs
for cat in CATEGORIES:
    os.makedirs(cat, exist_ok=True)

# Move files with git mv
for old, new in moves.items():
    if os.path.exists(old):
        print(f"git mv {old} {new}")
        subprocess.run(["git", "mv", old, new], check=True)

# Now build URL replacement rules
# href/src patterns to replace
replacements = []

# 1. Absolute paths for static assets (from any depth)
replacements.append((r'(href|src)="css/', r'\1="/css/'))
replacements.append((r'(href|src)="js/', r'\1="/js/'))
replacements.append((r'(href|src)="img/', r'\1="/img/'))
replacements.append((r"url\('img/", r"url('/img/"))
replacements.append((r'url\("img/', r'url("/img/'))

# 2. index.html -> /
replacements.append((r'href="index\.html"', r'href="/"'))

# 3. Legal pages stay at root
# (nothing — already resolve by absolute below)
replacements.append((r'href="mentions-legales\.html"', r'href="/mentions-legales.html"'))
replacements.append((r'href="politique-confidentialite\.html"', r'href="/politique-confidentialite.html"'))

# 4. Category pages: europe.html -> /europe/
for cat in CATEGORIES:
    replacements.append((rf'href="{cat}\.html"', f'href="/{cat}/"'))

# 5. Article pages: europe-xxx.html -> /europe/xxx.html
for cat in CATEGORIES:
    pattern = rf'href="{cat}-([a-z0-9\-]+)\.html"'
    repl = rf'href="/{cat}/\1.html"'
    replacements.append((pattern, repl))

# 6. Canonical / og:url absolute URLs
replacements.append((r'https://voyage7continents\.fr/index\.html', r'https://voyage7continents.fr/'))
for cat in CATEGORIES:
    replacements.append((rf'https://voyage7continents\.fr/{cat}\.html', f'https://voyage7continents.fr/{cat}/'))
    replacements.append((rf'https://voyage7continents\.fr/{cat}-([a-z0-9\-]+)\.html', rf'https://voyage7continents.fr/{cat}/\1.html'))

# Walk all HTML files in repo
html_files = []
for dirpath, dirnames, filenames in os.walk("."):
    # skip .git
    if ".git" in dirpath.split(os.sep):
        continue
    for fn in filenames:
        if fn.endswith(".html"):
            html_files.append(os.path.join(dirpath, fn))

for path in html_files:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for pat, repl in replacements:
        content = re.sub(pat, repl, content)
    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"updated {path}")

print("done")
