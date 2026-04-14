# Playbook SEO & Technique — Site éditorial statique

Checklist réutilisable des décisions techniques et SEO validées sur **voyage7continents.fr**.
À copier dans n'importe quel nouveau projet de site éditorial statique (blog, guide, magazine).
Ne contient **aucun contenu rédactionnel** — uniquement l'infrastructure, le SEO et le tooling.

---

## 1. Architecture du site

### 1.1 Arborescence
```
/                          ← racine
├── index.html             ← page d'accueil
├── mentions-legales.html
├── politique-confidentialite.html
├── robots.txt
├── sitemap.xml
├── .assetsignore          ← OBLIGATOIRE pour Cloudflare Pages
├── css/style.css
├── js/main.js
├── img/
│   ├── hero-*.jpg         ← covers de catégorie
│   └── articles/
│       └── <slug>-1.jpg à <slug>-5.jpg
└── <categorie>/           ← 1 dossier par catégorie / pilier
    ├── index.html         ← page pilier (pillar page)
    └── <slug>.html        ← articles (cluster content)
```

### 1.2 Modèle "pillar + cluster"
- **1 page pilier** par catégorie : gros contenu long, sommaire, cartes des articles.
- **N articles** courts/moyens qui traitent d'une question précise et **renvoient vers la page pilier**.
- Chaque article se maille aux autres articles de la même catégorie via le bloc « Ça pourrait vous intéresser ».

---

## 2. SEO on-page — checklist par article

Chaque article doit impérativement contenir :

### 2.1 `<head>`
- [ ] `<html lang="fr">`
- [ ] `<meta charset="UTF-8">`
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- [ ] `<title>` unique, ≤ 60 caractères, avec nom du site à la fin (`| Nom du Site`)
- [ ] `<meta name="description">` unique, 140-160 caractères, avec appel à l'action ou chiffre
- [ ] `<meta name="robots" content="index, follow">`
- [ ] `<link rel="canonical" href="https://exemple.fr/categorie/slug.html">`
- [ ] `<link rel="icon" type="image/svg+xml" href="/favicon.svg">` + `<link rel="apple-touch-icon" href="/favicon.svg">`
- [ ] **Open Graph complet** : `og:title`, `og:description`, `og:type="article"`, `og:url`, **`og:image`** (absolue)
- [ ] **Twitter Cards** : `twitter:card="summary_large_image"`, `twitter:title`, `twitter:description`, `twitter:image`
- [ ] `<link rel="stylesheet" href="/css/style.css">`
- [ ] **JSON-LD `Article`** avec `headline`, `image`, `mainEntityOfPage`, `description`, `author` (type `Person`, avec `url` vers la page auteur), `publisher` (avec `logo.url`), `datePublished`, `dateModified`
- [ ] **JSON-LD `BreadcrumbList`** en bloc séparé (3 items : Accueil → Catégorie → Article)

### 2.2 Hiérarchie sémantique
- [ ] **Un seul `<h1>`** par page, formulé comme la requête cible
- [ ] Structure `H1 → H2 → H3 → H4` respectée, sans saut de niveau
- [ ] Minimum 4 `<h2>` par article (correspondant aux sections du sommaire)

### 2.3 Contenu
- [ ] **Bloc `article-meta` visible** en haut d'article (sous le sommaire ou juste avant l'image hero) : photo auteur + lien vers `/a-propos.html`, **`<time datetime="...">Publié le ...</time>`** et `<time>Mis à jour le ...</time>`. La date doit être visible pour le lecteur **et** correspondre au `datePublished` du JSON-LD
- [ ] **Introduction** (lead) d'une phrase répondant directement à la requête
- [ ] Au moins **2 liens externes d'autorité** par article (sources officielles, avec `target="_blank" rel="noopener nofollow"`)
- [ ] Au moins **1 lien interne** vers la page pilier de la catégorie
- [ ] Au moins **4-5 images** avec attributs `alt` descriptifs (français, mots-clés), `loading="lazy"`, `width` et `height` explicites
- [ ] Mots-clés en `<strong>` dans le corps (parcimonieux, pas de bourrage)
- [ ] Bloc **« Le conseil d'expert »** en fin d'article (info-box) — signal E-E-A-T
- [ ] Bloc **« À retenir »** en milieu d'article (info-box)
- [ ] **Fiche auteur** (`<aside class="author-card">`) en bas d'article, avant le bloc related : photo, nom, rôle, bio courte, lien vers `/a-propos.html` — signal E-E-A-T majeur

### 2.4 Navigation intra-article
- [ ] **Fil d'Ariane** (breadcrumb) en haut : `Accueil › Catégorie › Article`
- [ ] **Sommaire (TOC)** avec ancres vers chaque `<h2>` (id unique par section)
- [ ] **Sidebar TOC** sticky sur desktop (version raccourcie)

### 2.5 Maillage interne
- [ ] Bloc **« Ça pourrait vous intéresser »** en fin d'article, avec 3-4 articles de la même catégorie (généré automatiquement — voir §5)
- [ ] Phrase de transition vers la page pilier de la catégorie juste avant le bloc

---

### 2.6 Schemas globaux (hors article)

| Page | Schemas à injecter |
|---|---|
| **Accueil (`index.html`)** | `Organization` (nom, url, logo, description, founder, foundingDate, sameAs) + `WebSite` (name, url, inLanguage) |
| **Page À propos** | `AboutPage` avec `mainEntity: Person` (nom, jobTitle, description, image, knowsAbout, worksFor) + `BreadcrumbList` |
| **Page catégorie / pilier** | `BreadcrumbList` (Accueil → Catégorie) |
| **Article** | `Article` + `BreadcrumbList` (Accueil → Catégorie → Article) |
| **Pages légales** | Aucun schema particulier, juste `noindex, nofollow` |

Règle d'or : **un schema `Organization` existe une seule fois sur le site**, sur la page d'accueil. Partout ailleurs, `publisher` dans `Article` suffit.

### 2.7 Fiche auteur et E-E-A-T

Les sites éditoriaux doivent afficher des auteurs identifiés pour être pris au sérieux par Google (Helpful Content) et par les acheteurs de liens.

- **1 auteur minimum par site**, avec nom réel ou fictif mais crédible
- **Page `/a-propos.html`** (ou `/auteurs/<slug>.html`) pour chaque auteur, avec :
  - Photo (portrait, ≥ 400×400 px, format rond en front)
  - Nom complet, rôle, bio longue (parcours, spécialités, formations)
  - Schema `Person` dans un JSON-LD `AboutPage`
- **Signature sur chaque article** :
  - `article-meta` en haut (photo mini + nom + date publication)
  - `author-card` en bas (photo, nom, rôle, bio courte, lien page auteur)
  - `author` du JSON-LD `Article` au type `Person` avec `url` vers la page auteur
- **Nom de l'auteur dans `<meta name="author">`** du `<head>` (optionnel mais recommandé)
- Si plusieurs auteurs : créer un répertoire `/auteurs/` avec une page par auteur

---

## 3. Fichiers techniques à la racine

### 3.1 `robots.txt`
```
User-agent: *
Allow: /

Sitemap: https://exemple.fr/sitemap.xml
```

### 3.2 `sitemap.xml`
- **Généré automatiquement** par `generate_sitemap.py` (voir §5)
- 1 `<url>` par page HTML publiée
- `lastmod` à la date du jour au moment de la génération
- `priority` :
  - `1.0` pour l'accueil
  - `0.9` pour les pages catégories
  - `0.7` pour les articles
  - `0.2` pour les pages légales
- `changefreq` : `weekly` pour accueil/catégories, `monthly` pour articles, `yearly` pour pages légales
- **À régénérer à chaque ajout/suppression/renommage de page HTML**, dans le même commit que les nouvelles pages

### 3.3 `.assetsignore` (Cloudflare Pages — obligatoire)
Si déploiement via **`npx wrangler deploy` avec `directory: "."`** (racine du repo), ce fichier est **indispensable** sinon le build échoue (le pack Git > 25 MiB dépasse la limite Workers).

Contenu minimum :
```
.git
.git/**
*.py
*.log
*.md
.gitignore
.assetsignore
wrangler.jsonc
wrangler.toml
```

Ajouter à `.assetsignore` tout nouveau type de fichier non publiable (`*.zip`, datasets, dumps…).
**Vérifier en premier** ce fichier si un build échoue avec « Asset too large ».

### 3.4 Favicon + logo (SVG)

- **`/favicon.svg`** à la racine — supporté par Chrome/Firefox/Safari modernes, scalable, léger
- **`/img/logo.svg`** — utilisé dans le header, dans le schema `Organization.logo` et sur les pages auteur
- Référencé via `<link rel="icon" type="image/svg+xml" href="/favicon.svg">` + `<link rel="apple-touch-icon" href="/favicon.svg">` dans **chaque** page HTML
- Si besoin de compatibilité iOS < 17 stricte, ajouter un PNG 180×180 généré depuis le SVG

### 3.5 Pages légales
- [ ] `mentions-legales.html` (nom de l'éditeur, hébergeur, contact, directeur de publication)
- [ ] `politique-confidentialite.html` (cookies, RGPD, droits, contact DPO)
- [ ] Liens `rel="nofollow"` dans le footer

---

## 4. Images

- **Source recommandée** : Wikimedia Commons (licences claires, gratuit, pas de tracking)
- **Téléchargement automatisé** : script `fetch_wikimedia.py` qui interroge l'API Commons avec 5 requêtes par slug et télécharge les thumbs 1024 px
- **Format** : JPG 1024 px de large (compromis qualité/poids)
- **Taille max** : 25 MiB par fichier (limite Cloudflare Workers) — en pratique, viser < 2 MiB
- **Nommage** : `<slug>-1.jpg` à `<slug>-5.jpg` (image 1 = hero, 2-5 = inline)
- **Attributs HTML** : `alt` descriptif FR, `loading="lazy"`, `width="800" height="500"` (ou équivalent) pour éviter le CLS
- **Skip automatique** : filtrer les SVG, cartes, armoiries, logos, diagrammes (regex de blacklist)

---

## 5. Scripts utilitaires (réutilisables)

À copier dans le nouveau projet et adapter le `SPEC`/les slugs.

| Script | Rôle |
|---|---|
| `generate_<categorie>.py` | Génère N articles d'une catégorie depuis un template Python (head + sections + body + expert tip) |
| `fetch_wikimedia.py` | Télécharge 5 images Wikimedia par slug via l'API Commons, avec blacklist et retry |
| `add_related.py` | Ajoute/régénère le bloc « Ça pourrait vous intéresser » en fin d'article avec N articles de la même catégorie |
| `add_covers.py` | Met à jour les images hero des cartes d'articles sur la page pilier de chaque catégorie |
| `generate_sitemap.py` | Génère `sitemap.xml` + `robots.txt` à partir de tous les `.html` du repo |
| `update_seo_schemas.py` | Injecte en une passe sur toutes les pages : favicon, Twitter Cards, og:image/og:url, JSON-LD BreadcrumbList, Organization/WebSite (homepage), author `Person`, bloc `article-meta` (date visible) et `author-card` |

**Workflow type pour un nouveau batch d'articles :**
```bash
python3 generate_<categorie>.py      # 1. créer les HTML (template déjà enrichi : author, dates, schemas)
python3 fetch_wikimedia.py <slugs>   # 2. télécharger les images
# 3. ajouter à la main les cards à <categorie>/index.html
python3 add_related.py               # 4. régénérer les blocs related
python3 add_covers.py                # 5. mettre à jour les covers catégorie
python3 update_seo_schemas.py        # 6. uniquement si on touche d'anciennes pages sans schemas
python3 generate_sitemap.py          # 7. régénérer sitemap.xml
git add -A && git commit -m "..." && git push
```

---

## 6. Déploiement — Cloudflare Pages

### 6.1 Config
- Connecter le repo GitHub à Cloudflare Pages
- Build command : `npx wrangler deploy`
- Output directory : `.` (racine)
- `wrangler.jsonc` généré automatiquement par wrangler au premier build :
  ```jsonc
  {
    "name": "<nom-projet>",
    "compatibility_date": "2026-xx-xx",
    "assets": { "directory": "." },
    "compatibility_flags": ["nodejs_compat"]
  }
  ```

### 6.2 Points de vigilance
- `.assetsignore` **obligatoire** (cf. §3.3)
- Limite **25 MiB par asset** (Workers)
- Auto-déploiement à chaque `git push` sur `main`
- Logs de build accessibles dans le dashboard Cloudflare (`<project>.production.<id>.build.log`)

---

## 7. Google Search Console (GSC)

### 7.1 Vérification de propriété
Trois options, par ordre de préférence :

1. **Type "Domaine"** (recommandé) → enregistrement DNS TXT chez le registrar
2. **Type "Préfixe d'URL"** → fichier `googleXXXXXXXX.html` à la racine du repo (commit + push, Cloudflare redéploie, valider dans GSC)
3. **Balise `<meta>`** dans le `<head>` de `index.html`

### 7.2 Soumission du sitemap
Après vérification : GSC → **Sitemaps** → soumettre `sitemap.xml`.
Google recrawle automatiquement ensuite, pas besoin de re-soumettre après chaque push.

### 7.3 Suivi recommandé
- **Couverture** : vérifier chaque semaine les pages indexées vs découvertes
- **Performances** : requêtes qui rapportent des impressions mais peu de clics → retravailler le `<title>` et la `<meta description>`
- **Core Web Vitals** : LCP, INP, CLS — surveillés aussi dans Cloudflare Analytics

---

## 8. Performance & Core Web Vitals

- [ ] **Images** : `loading="lazy"` partout sauf hero (ou `fetchpriority="high"` sur le hero)
- [ ] **Dimensions explicites** `width`/`height` sur chaque `<img>` → évite le CLS
- [ ] **CSS** dans un seul fichier `/css/style.css` avec `<link rel="stylesheet">` (pas de styles inline sauf hero background)
- [ ] **JS minimal** dans `/js/main.js`, chargé en fin de `<body>`, non-bloquant
- [ ] **Pas de webfont** externe bloquante (utiliser `font-display: swap` si webfont nécessaire)
- [ ] **Pas de tracker** lourd (GA4 en option via `defer`, pas de Tag Manager par défaut)
- [ ] Cache CDN géré par Cloudflare Pages (aucune config manuelle nécessaire)

---

## 9. Accessibilité (bonus SEO)

- [ ] `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` sémantiques
- [ ] `aria-label` sur `<nav>` et boutons de menu
- [ ] Contraste texte/fond ≥ AA
- [ ] Tous les liens visibles au focus clavier
- [ ] Ordre logique du DOM (pas de `tabindex` > 0)
- [ ] `alt` descriptif sur chaque image (ou `alt=""` si décorative)

---

## 10. Checklist "je lance un nouveau site"

1. [ ] Cloner ce playbook dans le nouveau repo
2. [ ] Créer l'arborescence (§1.1)
3. [ ] Copier/adapter les scripts utilitaires (§5)
4. [ ] Créer `.assetsignore` (§3.3)
5. [ ] Créer `favicon.svg` + `img/logo.svg` (§3.4)
6. [ ] Créer `robots.txt` + `generate_sitemap.py` (§3.1, §3.2)
7. [ ] Créer `mentions-legales.html` + `politique-confidentialite.html`
8. [ ] Créer **au moins un auteur** : `img/authors/<slug>.svg|jpg` + `a-propos.html` avec schema `Person`/`AboutPage` (§2.7)
9. [ ] Ajouter sur la homepage : schemas `Organization` + `WebSite` (§2.6)
10. [ ] Connecter le repo à Cloudflare Pages
11. [ ] Vérifier le domaine dans Google Search Console
12. [ ] Soumettre `sitemap.xml`
13. [ ] Premier batch d'articles → respecter la checklist §2 pour chaque article (y compris `article-meta` + `author-card`)
