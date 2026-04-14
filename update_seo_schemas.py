#!/usr/bin/env python3
"""Mise à jour SEO one-shot sur toutes les pages HTML :
- favicon + apple-touch-icon
- Twitter Cards + og:image + og:url
- JSON-LD BreadcrumbList
- JSON-LD Organization (homepage uniquement)
- JSON-LD Article: auteur = Person (Claire Moreau)
- bloc .article-meta (date de publication visible) au début du main
- bloc .author-card inséré avant le bloc related-articles
"""
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://voyage7continents.fr"
TODAY = date.today().isoformat()
TODAY_FR = date.today().strftime("%-d %B %Y").replace(
    "January", "janvier").replace("February", "février").replace("March", "mars").replace(
    "April", "avril").replace("May", "mai").replace("June", "juin").replace(
    "July", "juillet").replace("August", "août").replace("September", "septembre").replace(
    "October", "octobre").replace("November", "novembre").replace("December", "décembre")

AUTHOR = {
    "name": "Claire Moreau",
    "role": "Fondatrice & rédactrice en chef",
    "photo": "/img/authors/claire-moreau.svg",
    "url": "/a-propos.html",
    "bio_short": "Journaliste voyage depuis 2014, Claire a visité 68 pays sur les 7 continents. Elle fonde Voyage 7 Continents en 2022 pour partager des guides pratiques vérifiés sur le terrain.",
    "bio_meta": "Journaliste voyage · 68 pays · 7 continents",
}

CATEGORIES = ["europe", "asie", "afrique", "amerique-nord", "amerique-sud", "oceanie", "antarctique"]
CAT_LABEL = {
    "europe": "Europe", "asie": "Asie", "afrique": "Afrique",
    "amerique-nord": "Amérique du Nord", "amerique-sud": "Amérique du Sud",
    "oceanie": "Océanie", "antarctique": "Antarctique",
}

# Bloc HTML de la fiche auteur à insérer en fin d'article
AUTHOR_CARD_HTML = f"""      <!-- author-card -->
      <aside class="author-card" aria-label="À propos de l'auteur">
        <div class="author-card-photo">
          <img src="{AUTHOR['photo']}" alt="Portrait de {AUTHOR['name']}, rédactrice voyage" width="110" height="110" loading="lazy">
        </div>
        <div class="author-card-body">
          <span class="author-card-label">À propos de l'auteur</span>
          <h3><a href="{AUTHOR['url']}">{AUTHOR['name']}</a></h3>
          <p class="author-card-role">{AUTHOR['role']}</p>
          <p class="author-card-bio">{AUTHOR['bio_short']}</p>
          <a class="author-card-link" href="{AUTHOR['url']}">Lire la biographie complète &rsaquo;</a>
        </div>
      </aside>
"""


def extract_between(content, start_re, end_re):
    m = re.search(start_re, content)
    if not m:
        return None, None, None
    start = m.start()
    tail = content[m.end():]
    m2 = re.search(end_re, tail)
    if not m2:
        return None, None, None
    end = m.end() + m2.end()
    return start, end, content[start:end]


def get_meta(content, name, prop=False):
    attr = "property" if prop else "name"
    m = re.search(rf'<meta\s+{attr}="{re.escape(name)}"\s+content="([^"]*)"', content)
    return m.group(1) if m else None


def get_canonical(content):
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', content)
    return m.group(1) if m else None


def get_title(content):
    m = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
    return m.group(1).strip() if m else ""


def get_h1(content):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.DOTALL)
    if not m:
        return ""
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()


def build_article_img(slug, category):
    """Return the og:image URL (absolute) for a given slug."""
    candidate = f"/img/articles/{slug}-1.jpg"
    if os.path.exists(os.path.join(ROOT, candidate.lstrip("/"))):
        return BASE + candidate
    # Category hero as fallback
    hero = f"/img/hero-{category}.jpg"
    if os.path.exists(os.path.join(ROOT, hero.lstrip("/"))):
        return BASE + hero
    return BASE + "/favicon.svg"


def ensure_favicon(head_block):
    if 'rel="icon"' in head_block:
        return head_block
    injection = (
        '  <link rel="icon" type="image/svg+xml" href="/favicon.svg">\n'
        '  <link rel="apple-touch-icon" href="/favicon.svg">\n'
    )
    return head_block.replace('<link rel="stylesheet"', injection + '  <link rel="stylesheet"', 1)


def ensure_twitter_og_image(head_block, canonical, og_title, og_desc, og_image):
    """Ensure og:url, og:image and twitter cards are present."""
    # Remove existing twitter & og:image/og:url to replace cleanly
    head_block = re.sub(r'\s*<meta\s+property="og:url"[^>]*>', '', head_block)
    head_block = re.sub(r'\s*<meta\s+property="og:image"[^>]*>', '', head_block)
    head_block = re.sub(r'\s*<meta\s+name="twitter:[^"]+"[^>]*>', '', head_block)

    og_title = (og_title or "").replace('"', "&quot;")
    og_desc = (og_desc or "").replace('"', "&quot;")
    addition = (
        f'  <meta property="og:url" content="{canonical}">\n'
        f'  <meta property="og:image" content="{og_image}">\n'
        f'  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{og_title}">\n'
        f'  <meta name="twitter:description" content="{og_desc}">\n'
        f'  <meta name="twitter:image" content="{og_image}">\n'
    )
    # Insert right after the last og: meta
    m = list(re.finditer(r'<meta\s+property="og:[^"]+"[^>]*>\n', head_block))
    if m:
        last = m[-1]
        head_block = head_block[:last.end()] + addition + head_block[last.end():]
    else:
        head_block = head_block.replace('<link rel="stylesheet"', addition + '  <link rel="stylesheet"', 1)
    return head_block


def update_article_jsonld(head_block, canonical, og_image):
    """Update the existing Article JSON-LD block to use Person author and full publisher."""
    def replacer(m):
        block = m.group(0)
        # Replace author
        block = re.sub(
            r'"author"\s*:\s*\{[^}]*\}',
            '"author": {{"@type": "Person", "name": "{n}", "url": "{u}{p}"}}'.format(
                n=AUTHOR["name"], u=BASE, p=AUTHOR["url"]),
            block,
        )
        # Upgrade publisher to include logo
        block = re.sub(
            r'"publisher"\s*:\s*\{[^}]*\}',
            '"publisher": {"@type": "Organization", "name": "Voyage 7 Continents", '
            '"logo": {"@type": "ImageObject", "url": "' + BASE + '/img/logo.svg"}}',
            block,
        )
        # Ensure image + mainEntityOfPage
        if '"image"' not in block:
            block = block.replace(
                '"description"',
                f'"image": "{og_image}",\n    "mainEntityOfPage": "{canonical}",\n    "description"',
                1,
            )
        return block
    return re.sub(
        r'<script type="application/ld\+json">\s*\{[^<]*"@type":\s*"Article"[^<]*\}\s*</script>',
        replacer,
        head_block,
        count=1,
        flags=re.DOTALL,
    )


def inject_breadcrumb_jsonld(head_block, canonical, category, slug_title):
    if "BreadcrumbList" in head_block:
        # Already there, replace
        head_block = re.sub(
            r'<script type="application/ld\+json">\s*\{[^<]*"BreadcrumbList"[^<]*\}\s*</script>\s*',
            '', head_block, flags=re.DOTALL,
        )
    cat_label = CAT_LABEL.get(category, category.title())
    cat_url = f"{BASE}/{category}/"
    items = [
        {"pos": 1, "name": "Accueil", "item": f"{BASE}/"},
        {"pos": 2, "name": cat_label, "item": cat_url},
    ]
    if slug_title:
        items.append({"pos": 3, "name": slug_title.replace('"', "&quot;"), "item": canonical})
    items_json = ",\n      ".join(
        f'{{"@type": "ListItem", "position": {i["pos"]}, "name": "{i["name"]}", "item": "{i["item"]}"}}' for i in items
    )
    block = (
        '  <script type="application/ld+json">\n'
        '  {\n'
        '    "@context": "https://schema.org",\n'
        '    "@type": "BreadcrumbList",\n'
        '    "itemListElement": [\n'
        f'      {items_json}\n'
        '    ]\n'
        '  }\n'
        '  </script>\n'
    )
    # head_block is the content BEFORE </head>, so just append.
    return head_block + block


def inject_article_meta(body, title):
    """Insert visible publication date + author block just before the first <figure class='article-hero'>."""
    if 'class="article-meta"' in body:
        return body
    meta_html = (
        f'      <div class="article-meta">\n'
        f'        <span class="meta-author"><img src="{AUTHOR["photo"]}" alt="{AUTHOR["name"]}" width="32" height="32" loading="lazy"> <a href="{AUTHOR["url"]}">Par {AUTHOR["name"]}</a></span>\n'
        f'        <time datetime="{TODAY}">Publié le {TODAY_FR}</time>\n'
        f'        <time class="meta-updated" datetime="{TODAY}">Mis à jour le {TODAY_FR}</time>\n'
        f'      </div>\n'
    )
    # Insert before first <figure class="article-hero">
    if '<figure class="article-hero"' in body:
        return body.replace('<figure class="article-hero"', meta_html + '      <figure class="article-hero"', 1)
    # Fallback: insert after <nav class="toc">...</nav>
    m = re.search(r'</nav>\s*\n', body)
    if m:
        return body[:m.end()] + "\n" + meta_html + body[m.end():]
    return body


def inject_author_card(body):
    if "author-card" in body:
        return body
    # Insert just before <!-- related-articles -->
    if "<!-- related-articles -->" in body:
        return body.replace("<!-- related-articles -->", AUTHOR_CARD_HTML + "\n      <!-- related-articles -->", 1)
    # Fallback: before </main>
    if "</main>" in body:
        return body.replace("</main>", AUTHOR_CARD_HTML + "\n    </main>", 1)
    return body


def process_article(path, category):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    orig = content

    # Split head / body
    m = re.search(r"</head>", content)
    if not m:
        return False
    head = content[: m.start()]
    rest = content[m.start():]

    canonical = get_canonical(content) or f"{BASE}/{category}/{os.path.basename(path)}"
    slug = os.path.splitext(os.path.basename(path))[0]
    og_image = build_article_img(slug, category)
    og_title = get_meta(content, "og:title", prop=True) or get_title(content)
    og_desc = get_meta(content, "description") or ""

    head = ensure_favicon(head)
    head = ensure_twitter_og_image(head, canonical, og_title, og_desc, og_image)
    head = update_article_jsonld(head, canonical, og_image)
    head = inject_breadcrumb_jsonld(head, canonical, category, get_h1(content))

    content = head + rest
    content = inject_article_meta(content, og_title)
    content = inject_author_card(content)

    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def process_category_index(path, category):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    orig = content
    m = re.search(r"</head>", content)
    if not m:
        return False
    head = content[: m.start()]
    rest = content[m.start():]

    canonical = get_canonical(content) or f"{BASE}/{category}/"
    og_image = BASE + f"/img/hero-{category}.jpg"
    og_title = get_meta(content, "og:title", prop=True) or get_title(content)
    og_desc = get_meta(content, "description") or ""

    head = ensure_favicon(head)
    head = ensure_twitter_og_image(head, canonical, og_title, og_desc, og_image)
    head = inject_breadcrumb_jsonld(head, canonical, category, None)

    content = head + rest
    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def process_home(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    orig = content
    m = re.search(r"</head>", content)
    if not m:
        return False
    head = content[: m.start()]
    rest = content[m.start():]

    canonical = get_canonical(content) or f"{BASE}/"
    og_image = BASE + "/img/hero-home.jpg"
    og_title = get_meta(content, "og:title", prop=True) or get_title(content)
    og_desc = get_meta(content, "description") or ""

    head = ensure_favicon(head)
    head = ensure_twitter_og_image(head, canonical, og_title, og_desc, og_image)

    # Organization JSON-LD
    if '"@type": "Organization"' not in head or '"@type":"Organization"' not in head:
        if '"Organization"' not in head:
            org = (
                '  <script type="application/ld+json">\n'
                '  {\n'
                '    "@context": "https://schema.org",\n'
                '    "@type": "Organization",\n'
                f'    "name": "Voyage 7 Continents",\n'
                f'    "url": "{BASE}/",\n'
                f'    "logo": "{BASE}/img/logo.svg",\n'
                '    "description": "Guide de voyage indépendant couvrant les 7 continents : conseils pratiques, itinéraires et retours de terrain.",\n'
                '    "founder": {"@type": "Person", "name": "Claire Moreau"},\n'
                '    "foundingDate": "2022",\n'
                '    "sameAs": []\n'
                '  }\n'
                '  </script>\n'
            )
            head += org

    # WebSite JSON-LD with SearchAction
    if '"WebSite"' not in head:
        ws = (
            '  <script type="application/ld+json">\n'
            '  {\n'
            '    "@context": "https://schema.org",\n'
            '    "@type": "WebSite",\n'
            '    "name": "Voyage 7 Continents",\n'
            f'    "url": "{BASE}/",\n'
            '    "inLanguage": "fr-FR"\n'
            '  }\n'
            '  </script>\n'
        )
        head += ws

    content = head + rest
    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def process_simple(path):
    """Just favicon + twitter cards, for a-propos / mentions / politique."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    orig = content
    m = re.search(r"</head>", content)
    if not m:
        return False
    head = content[: m.start()]
    rest = content[m.start():]

    canonical = get_canonical(content)
    if canonical:
        og_title = get_meta(content, "og:title", prop=True) or get_title(content)
        og_desc = get_meta(content, "description") or ""
        og_image = BASE + "/img/logo.svg"
        head = ensure_twitter_og_image(head, canonical, og_title, og_desc, og_image)
    head = ensure_favicon(head)

    content = head + rest
    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    count = 0
    # Homepage
    home = os.path.join(ROOT, "index.html")
    if os.path.exists(home) and process_home(home):
        count += 1
        print(f"updated index.html")
    # Simple pages
    for fn in ("a-propos.html", "mentions-legales.html", "politique-confidentialite.html"):
        p = os.path.join(ROOT, fn)
        if os.path.exists(p) and process_simple(p):
            count += 1
            print(f"updated {fn}")
    # Categories
    for cat in CATEGORIES:
        cat_dir = os.path.join(ROOT, cat)
        if not os.path.isdir(cat_dir):
            continue
        idx = os.path.join(cat_dir, "index.html")
        if os.path.exists(idx) and process_category_index(idx, cat):
            count += 1
            print(f"updated {cat}/index.html")
        for fn in sorted(os.listdir(cat_dir)):
            if fn == "index.html" or not fn.endswith(".html"):
                continue
            p = os.path.join(cat_dir, fn)
            if process_article(p, cat):
                count += 1
                print(f"updated {cat}/{fn}")
    print(f"\ndone — {count} files updated")


if __name__ == "__main__":
    main()
