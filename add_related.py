#!/usr/bin/env python3
"""Add a 'Ça pourrait vous intéresser' block at the end of each article."""
import os, re, random

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

CATEGORIES = ["europe", "asie", "afrique", "amerique-nord", "amerique-sud", "oceanie", "antarctique"]

CAT_LABEL = {
    "europe": "Europe",
    "asie": "Asie",
    "afrique": "Afrique",
    "amerique-nord": "Amérique du Nord",
    "amerique-sud": "Amérique du Sud",
    "oceanie": "Océanie",
    "antarctique": "Antarctique",
}

def extract_h1(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
    if not m:
        return None
    h1 = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return h1

def short_title(h1):
    # Remove trailing tagline after first ":" for a punchier card title
    if ":" in h1:
        return h1.split(":", 1)[0].strip()
    return h1

# Build: cat -> list of (slug, full_h1, short_title)
articles_by_cat = {}
for cat in CATEGORIES:
    items = []
    for fn in sorted(os.listdir(cat)):
        if fn == "index.html" or not fn.endswith(".html"):
            continue
        h1 = extract_h1(os.path.join(cat, fn))
        if h1:
            items.append((fn, h1, short_title(h1)))
    articles_by_cat[cat] = items

# Build related block for each article
BLOCK_MARKER = "<!-- related-articles -->"

def build_block(cat, current_slug):
    pool = [x for x in articles_by_cat[cat] if x[0] != current_slug]
    # Show up to 4
    picks = pool[:3]
    if not picks:
        return ""
    cards = []
    for slug, h1, short in picks:
        cards.append(
            f'        <a class="related-card" href="/{cat}/{slug}">\n'
            f'          <span class="related-tag">{CAT_LABEL[cat]}</span>\n'
            f'          <h3>{short}</h3>\n'
            f'        </a>'
        )
    return (
        f'      {BLOCK_MARKER}\n'
        f'      <section class="related-articles" aria-labelledby="related-title">\n'
        f'        <h2 id="related-title">Ça pourrait vous intéresser</h2>\n'
        f'        <div class="related-grid">\n'
        + "\n".join(cards) + "\n"
        f'        </div>\n'
        f'      </section>\n'
    )

for cat in CATEGORIES:
    for slug, h1, short in articles_by_cat[cat]:
        path = os.path.join(cat, slug)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Remove old block if present
        content = re.sub(
            r"\s*<!-- related-articles -->.*?</section>\s*",
            "\n",
            content,
            flags=re.DOTALL,
        )
        block = build_block(cat, slug)
        if not block:
            continue
        # Insert before closing </main>
        new_content, n = re.subn(
            r"(\s*)</main>",
            "\n\n" + block + r"\1</main>",
            content,
            count=1,
        )
        if n == 0:
            print(f"WARN no </main> in {path}")
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"updated {path}")

print("done")
