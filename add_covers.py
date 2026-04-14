#!/usr/bin/env python3
"""Add cover images to article-cards in all category index pages."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

CATS = ["europe", "asie", "afrique", "amerique-nord", "amerique-sud", "oceanie", "antarctique"]

# Build map: article_href -> hero image src by reading each article's first article-hero
hero_map = {}
for cat in CATS:
    for fn in os.listdir(cat):
        if fn == "index.html" or not fn.endswith(".html"):
            continue
        path = os.path.join(cat, fn)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # First try hero figure, then any img in main
        m = re.search(r'<figure class="article-hero"[^>]*>\s*<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', content)
        if not m:
            m = re.search(r'<img[^>]+class="article-img"[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', content)
        if not m:
            m = re.search(r'<img[^>]+src="(/img/articles/[^"]+)"[^>]*alt="([^"]*)"', content)
        if m:
            href = f"/{cat}/{fn}"
            hero_map[href] = (m.group(1), m.group(2))

print(f"mapped {len(hero_map)} hero images")

# Now process each category index page
card_rx = re.compile(
    r'(<div class="article-card">)\s*(<div class="article-card-body">\s*<span class="tag">[^<]*</span>\s*<h3><a href="([^"]+)">)',
    re.DOTALL,
)

for cat in CATS:
    path = os.path.join(cat, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    def repl(match):
        div_open = match.group(1)
        rest = match.group(2)
        href = match.group(3)
        img = hero_map.get(href)
        if not img:
            return match.group(0)
        src, alt = img
        # Avoid duplicating if already has image
        return (
            f'{div_open}\n'
            f'          <a class="article-card-image" href="{href}">\n'
            f'            <img src="{src}" alt="{alt}" loading="lazy" width="600" height="360">\n'
            f'          </a>\n'
            f'          {rest}'
        )

    # Remove any previously-added image blocks first to allow re-running
    content = re.sub(
        r'\s*<a class="article-card-image"[^>]*>\s*<img[^>]+>\s*</a>\s*',
        "\n          ",
        content,
    )
    content = card_rx.sub(repl, content)

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"updated {path}")
print("done")
