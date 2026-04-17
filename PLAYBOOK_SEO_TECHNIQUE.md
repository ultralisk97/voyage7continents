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
- [ ] `<link rel="canonical" href="https://exemple.fr/categorie/slug">` **sans `.html`** (cf. §6.3)
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
- [ ] **Bloc `article-meta` visible** en haut d'article (sous le sommaire ou juste avant l'image hero) : photo auteur + lien vers `/a-propos`, **`<time datetime="...">Publié le ...</time>`** et `<time>Mis à jour le ...</time>`. La date doit être visible pour le lecteur **et** correspondre au `datePublished` du JSON-LD
- [ ] **Introduction** (lead) d'une phrase répondant directement à la requête
- [ ] Au moins **2 liens externes d'autorité** par article (sources officielles, avec `target="_blank" rel="noopener nofollow"`)
- [ ] Au moins **1 lien interne** vers la page pilier de la catégorie
- [ ] Au moins **4-5 images** avec attributs `alt` descriptifs (français, mots-clés), `loading="lazy"`, `width` et `height` explicites
- [ ] Mots-clés en `<strong>` dans le corps (parcimonieux, pas de bourrage)
- [ ] Bloc **« Le conseil d'expert »** en fin d'article (info-box) — signal E-E-A-T
- [ ] Bloc **« À retenir »** en milieu d'article (info-box)
- [ ] **Fiche auteur** (`<aside class="author-card">`) en bas d'article, avant le bloc related : photo, nom, rôle, bio courte, lien vers `/a-propos` — signal E-E-A-T majeur

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
- **Page `/a-propos`** (fichier `a-propos.html` — on link sans l'extension, cf. §6.3) ou `/auteurs/<slug>` pour chaque auteur, avec :
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

### 6.3 URLs sans `.html` — RÈGLE CRITIQUE SEO
Cloudflare Pages sert les fichiers `.html` aux **deux URLs** `/page.html` et `/page`, mais **redirige** `/page.html` → `/page` en **307**. Conséquence : si les canonicals, liens internes et sitemap contiennent `.html`, Screaming Frog remonte :
- **Canonicals: Non-Indexable Canonical** (le canonical pointe vers une URL qui redirige)
- **Canonicals: Canonicalised** (la page crawlée a un canonical vers une autre URL)
- **Response Codes: Internal Redirection (3xx)** (tous les liens internes redirigent)

**Règle absolue** : les **fichiers** sur disque gardent `.html`, mais **toute URL écrite dans le HTML ou le sitemap** doit être sans `.html`.

| Contexte | ❌ Mauvais | ✅ Bon |
|---|---|---|
| Canonical | `href="https://site.fr/afrique/safari.html"` | `href="https://site.fr/afrique/safari"` |
| Lien interne | `<a href="/asie/japon.html">` | `<a href="/asie/japon">` |
| Sitemap `<loc>` | `.../japon.html` | `.../japon` |
| `og:url` / breadcrumb schema | `.../safari.html` | `.../safari` |
| Page pilier catégorie | `/afrique/` (garder le slash final) | `/afrique/` ✅ |
| Homepage | `/` | `/` ✅ |

**À faire dans chaque template** : pas d'`.html` dans `<link rel="canonical">`, `og:url`, `twitter:url`, schemas JSON-LD, `<a href="/...">`, ni dans `sitemap.xml`. Le script `generate_sitemap.py` (§5) doit produire les `<loc>` **sans** extension.

**Vérification post-déploiement** :
- `curl -I https://<site>/page` doit retourner **200** directement (c'est l'URL qui doit être partout)
- `curl -I https://<site>/page.html` retourne **307** vers `/page` (normal : c'est justement pour ça qu'il faut éviter `.html` dans les URLs)
- `grep -rE 'href="[^"]*\.html"' *.html` doit ne rien retourner (hors liens externes)
- `grep '\.html' sitemap.xml` doit ne rien retourner

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

## 8bis. Responsive mobile — OBLIGATOIRE

Le site doit être parfaitement utilisable sur mobile **dès la mise en ligne**. Google utilise l'indexation mobile-first : une page qui déborde horizontalement ou dont le texte est coupé à droite est *immédiatement* déclassée. Aucun site ne doit être mis en prod sans être testé à 320, 375 et 768 px.

### 8bis.1 Règles CSS obligatoires (à mettre dans `style.css`)

```css
/* Safety net anti-débordement horizontal */
html, body { max-width: 100%; overflow-x: hidden; }
body { overflow-wrap: break-word; -webkit-text-size-adjust: 100%; }
h1, h2, h3, h4, h5, h6, p, a, li {
  overflow-wrap: break-word;
  hyphens: auto;
}
img, video, iframe, table { max-width: 100%; height: auto; }

/* PIÈGE CSS GRID : toujours utiliser minmax(0, 1fr), JAMAIS 1fr seul.
   Sans ça, une <img width="600"> dans une card force la grille à 600px
   même sur un viewport de 375px → tout le texte est poussé à droite. */
.ma-grille {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;  /* ✅ */
  /* grid-template-columns: 1fr 280px;            ❌ piège min-content */
}
/* Ceinture-bretelles : forcer min-width 0 sur les enfants de grid */
.ma-grille > * { min-width: 0; }
```

### 8bis.2 Breakpoints standards

- **≤ 968 px** : désactiver la sidebar sticky, passer le contenu principal en 1 colonne.
- **≤ 768 px** : activer le hamburger menu, réduire les paddings, empiler les grilles, tap targets `min-height: 44px` sur les liens/boutons.
- **≤ 480 px** : réduire `html { font-size }` à ~14.5 px, resserrer encore les paddings.

### 8bis.3 Tests automatisés (Playwright)

Avant chaque mise en prod, lancer un test qui :
1. Spin up `python3 -m http.server`
2. Ouvre les pages clés (homepage, 1 page pilier, 1 article, 1 page simple) à 320/375/768 px de viewport
3. Vérifie que `document.documentElement.scrollWidth <= clientWidth + 1` (pas de scroll horizontal)
4. Vérifie qu'aucun élément n'a `getBoundingClientRect().right > clientWidth`

Installation une fois : `pip3 install playwright && python3 -m playwright install chromium`

Script de référence (à copier dans `test_responsive.py`) : utiliser le snippet Playwright de `voyage7continents.fr` — il teste 5 URLs × 3 viewports et échoue si un élément déborde.

### 8bis.4 Erreurs classiques à vérifier

- [ ] `<img width="xxx" height="yyy">` obligatoire (bon pour le CLS) → mais **dans une grille**, provoque le débordement si la grille n'utilise pas `minmax(0, 1fr)`
- [ ] Longues URLs en lien (`https://...`) sans `word-break: break-word` → débordent sur mobile
- [ ] `<table>` sans wrapper scrollable → débordent systématiquement, prévoir `overflow-x: auto` sur un wrapper parent
- [ ] Inline styles `style="max-width: 900px"` sur `.pillar-content` → OK si `box-sizing: border-box` global, mais à bannir quand même
- [ ] `position: fixed` du menu mobile sans `max-height: calc(100vh - 64px); overflow-y: auto` → menu qui sort de l'écran si liste longue
- [ ] Boutons sans `min-height: 44px` → tap targets trop petits pour iOS

### 8bis.5 Checklist avant chaque déploiement

- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1.0">` sur TOUTES les pages
- [ ] Test Playwright à 320/375/768 px passe sans débordement
- [ ] Hamburger menu fonctionne et se ferme au tap en dehors
- [ ] Hero h1 lisible sur 320 px (pas de troncature, pas de débordement)
- [ ] Cards d'articles et cards de continents empilées en 1 colonne sur mobile
- [ ] Footer en 1 colonne sur mobile
- [ ] Lecture confortable d'un article : paragraphes, images, info-box, TOC, related articles, author-card — tout s'affiche sans scroll horizontal
- [ ] Test réel sur un smartphone en fin de cycle (mode navigation privée pour éviter le cache CDN)

---

## 9. Accessibilité (bonus SEO)

- [ ] `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` sémantiques
- [ ] `aria-label` sur `<nav>` et boutons de menu
- [ ] Contraste texte/fond ≥ AA
- [ ] Tous les liens visibles au focus clavier
- [ ] Ordre logique du DOM (pas de `tabindex` > 0)
- [ ] `alt` descriptif sur chaque image (ou `alt=""` si décorative)

---

## 11. Méthode de rédaction IA — pipeline 4 agents

**Origine :** workflow n8n *Article SEO V3* (validé sur plusieurs sites WordPress). Adapté ici pour un site statique HTML. Toutes les méthodes ci-dessous sont **obligatoires** dès qu'on rédige un article via IA — même si la rédaction est faite en une seule conversation Claude et non via n8n.

### 11.1 Principe

Ne jamais écrire un article en "one-shot" direct. Toujours enchaîner 4 phases :

1. **Recherche documentaire** — sources, faits, stats, citations, angles uniques
2. **Analyse SERP Top 10** — mesurer les concurrents, fixer les cibles
3. **Rédaction HTML** — utiliser les inputs des phases 1 et 2
4. **Métadonnées SEO** — générer ensuite, basé sur l'article écrit

Chaque phase produit un JSON (ou HTML pour la phase 3) qui alimente la suivante.

### 11.2 Phase 1 — Agent Recherche

**Mission** : trouver des infos fiables, récentes et uniques sur le sujet. Sources officielles prioritaires. Données chiffrées datées.

**Outil** : recherche web (Perplexity `sonar` / Tavily / WebSearch). Filtrer sur le dernier mois si actualité.

**Output JSON attendu :**
```json
{
  "sources": [{"title": "", "url": "", "key_info": ""}],
  "key_facts": ["..."],
  "statistics": ["... avec source et date"],
  "expert_quotes": ["..."],
  "unique_angles": ["ce que les concurrents ne traitent pas"]
}
```

**Règles :**
- Minimum 5 sources différentes
- Minimum 3 statistiques chiffrées avec année
- Toujours identifier au moins 2 angles uniques (gaps concurrents)
- Jamais deviner un chiffre — si doute, re-chercher

### 11.3 Phase 2 — Agent SERP Top 10

**Mission** : analyser les 10 premiers résultats Google de la requête cible, calculer les moyennes, repérer les gaps.

**Output JSON attendu :**
```json
{
  "target_word_count": 2500,
  "target_h2_count": 8,
  "target_h3_count": 12,
  "target_h4_count": 4,
  "target_image_count": 5,
  "main_topics": ["..."],
  "subtopics": ["..."],
  "content_depth": "superficial|moderate|in-depth|expert",
  "key_keywords": ["..."],
  "secondary_keywords": ["..."],
  "recommended_sections": ["..."],
  "search_intent": "informational|transactional|navigational|commercial",
  "competitors_analysis": [
    {"url": "", "word_count": 0, "h2_count": 0, "strengths": "", "gaps": ""}
  ]
}
```

**Règles :**
- Mots cible = moyenne top 10 × 1.1 (viser au-dessus, pas en-dessous)
- `main_topics` = sujets présents chez au moins 5/10
- `gaps` = sujets manquants ou mal traités → c'est là qu'on apporte de la valeur

### 11.4 Phase 3 — Agent Rédaction

**System message (à coller dans le prompt système) :**
> Tu es un rédacteur web SEO de niveau expert. Tu rédiges des articles longs, approfondis, factuels et optimisés pour le référencement naturel. Tu as accès à un outil de recherche web que tu peux utiliser à tout moment pour vérifier un fait, trouver une statistique récente, ou approfondir un sujet. Tu ne devines JAMAIS une donnée chiffrée — tu la vérifies. Ton output final est TOUJOURS du HTML pur sans aucun wrapper markdown.

**Structure imposée :**
- **Introduction** : 60-80 mots, accroche sur la problématique lecteur
- **N chapitres H2** (= `target_h2_count` de la phase 2), issus de `recommended_sections` + exploitation des `gaps`
- **M sous-sections H3** (= `target_h3_count`) pour la profondeur
- **Conclusion** : 60-80 mots, résumé + CTA (PAS de heading "Conclusion")

**Volume minimum par bloc :**
- Article entier : minimum `target_word_count × 0.85`
- Chaque H2 : 250-350 mots
- Chaque H3 : 150-200 mots

**Règles de contenu :**
- Intègre OBLIGATOIREMENT les `key_facts` et `statistics` de la phase 1
- Exploite les `gaps` concurrents pour apporter de la valeur unique
- **UN SEUL tableau comparatif HTML** pertinent et actionable
- **Maximum UNE liste à puces** dans tout l'article
- Explique POURQUOI et COMMENT, pas juste le QUOI
- Exemples concrets, cas pratiques, données chiffrées
- Si un fait semble douteux : re-chercher avant d'écrire

**Format HTML (balises autorisées, rien d'autre) :**
`<h2>`, `<h3>`, `<h4>`, `<p>`, `<strong>`, `<em>`, `<ul>`, `<li>`, `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`

- **Zéro `<h1>`** dans le corps (le H1 vient du template `article-meta` de la page)
- `<strong>` stratégique sur les mots-clés (pas de bourrage)
- Titres H2 **descriptifs** (PAS "Chapitre 1", PAS "Introduction", PAS "Conclusion")

**Ton :**
- Professionnel, accessible, conversationnel
- **Tutoiement**
- Voix active
- Empathique et utile

**Output :** HTML pur. Pas de markdown, pas de ```html, pas de préambule. Commence directement par la première balise HTML (typiquement `<p>` de l'intro).

### 11.5 Phase 4 — Agent SEO Metadata

**Mission** : générer les 13 champs SEO à partir de l'article écrit.

**Champs à produire :**

| Champ | Contrainte | Notes |
|---|---|---|
| `article_title` | H1, max **70** chars | Accrocheur, émotionnel/créatif |
| `seo_title` | max **60** chars | **DIFFÉRENT** de `article_title`, mot-clé en début |
| `slug` | 3-5 mots, lowercase, tirets | Contient le mot-clé principal |
| `meta_description` | max **155** chars | Mot-clé + CTA + **un emoji pertinent** |
| `focus_keyword` | 1-4 mots | Exact, pour Yoast / SEO |
| `og_title` | max **60** chars | Engageant |
| `og_description` | max **200** chars | Incite au clic |
| `twitter_title` | max **55** chars | Percutant |
| `twitter_description` | max **200** chars | |
| `excerpt` | 2-3 phrases, max **300** chars | Résumé |
| `schema_type` | `Article` / `BlogPosting` / `HowTo` / `FAQPage` | Adapté au contenu |
| `tags` | 5-8 tags | Pertinents |
| `canonical_path` | `/slug-ici/` | |

**Règles fortes :**
- `seo_title` doit **toujours** différer de `article_title` (sinon Google affiche le H1 à sa place = titre non optimisé perdu)
- `meta_description` contient **toujours** un emoji + un CTA ("Découvre", "Teste", "Évite", "Prépare", etc.)
- `slug` = mots-clé principal, pas de "et", "le", "la", "de" sauf nécessaire

### 11.6 Adaptation site statique (voyage7continents.fr)

Le workflow n8n publie dans WordPress+Yoast. Ici, site statique HTML : les champs ci-dessus sont injectés **directement dans le `<head>` HTML** via le template du `generate_<categorie>.py`.

| Champ n8n (Yoast) | Équivalent site statique |
|---|---|
| `article_title` | `<h1>` dans le `<body>` + `<title>` dans le `<head>` |
| `seo_title` | `<title>` + `og:title` si différent |
| `meta_description` | `<meta name="description">` + `og:description` + `twitter:description` |
| `focus_keyword` | pas de balise dédiée — présent naturellement dans H1, intro, 2-3 H2 |
| `canonical_url` | `<link rel="canonical">` |
| `og_title` / `og_description` / `og_image_url` | `<meta property="og:*">` |
| `twitter_title/description/image` | `<meta name="twitter:*">` |
| `schema_type` | `@type` du JSON-LD `Article` |
| `tags` | pas de taxonomie côté statique — noter dans le commit / repo interne |
| `article_html` | corps du `<article>` entre hero et bloc "related" |
| `excerpt` | `<meta name="description">` + lead visible en haut d'article |
| `featured_media` | `/img/articles/<slug>-1.jpg` référencé dans `og:image` et JSON-LD `image` |

**Sources de vérité (pas de Google Sheet)** : liste de sujets directement dans le script `generate_<categorie>.py` ou fournie en input de la conversation Claude.

### 11.7 Génération d'images (Imagen 4, Nano Banana, Replicate…)

Sur ce site on utilise Wikimedia par défaut (§4), sinon Google Imagen 4 via `generate_images.py` (clé API en env var, jamais commitée).

**Règle n°1 — pas de rendu "IA".** Les images doivent ressembler à de vraies photos terrain. Un rendu trop lisse, trop parfait, trop cinématographique casse l'EEAT et déclenche la méfiance du lecteur.

**Techniques anti-IA obligatoires dans chaque prompt :**

| À faire | À éviter |
|---|---|
| `iPhone 15 Pro photo` / `shot on Fuji X100V` / `Google Pixel camera` | `professional editorial photography` |
| `candid travel snapshot`, `unposed tourist photo`, `Flickr style` | `editorial`, `cinematic`, `dramatic`, `pristine` |
| `handheld, slight motion blur, subtle film grain, ISO 800` | `sharp focus everywhere`, `8k`, `hyperreal` |
| `10 AM overcast`, `light drizzle`, `tourists walking past` | `perfect golden hour`, `studio lighting` |
| `documentary photojournalism` | `photorealistic` (paradoxalement trahit l'IA) |

**Structure des prompts (1 cover + 3-4 inline) :**

- **1 cover** (aspect `16:9`) : `iPhone 15 Pro travel snapshot: <sujet_article>. Candid handheld shot, 10 AM overcast, subtle motion blur, natural uneven light, documentary style, slightly overexposed sky, NO TEXT`
- **Inline** (aspect `4:3`) :
  1. *Vue d'ensemble* : `Fuji X100V travel photo: <topic_1>. Handheld candid, mid-afternoon soft light, slight film grain, backpacker perspective, Flickr travel blog style, NO TEXT`
  2. *Scène détaillée* : `Google Pixel snapshot: <topic_2>. Unposed, natural light through window/trees, ISO 800, slight depth of field, documentary feel, NO TEXT`
  3. *Action / pratique* : `Travel photojournalism: <topic_3>. Tourists walking past, locals in background, candid moment, ambient light, slight shadow, NO TEXT`
  4. *Contexte informatif* : `Smartphone travel snapshot: <topic_4>. Everyday angle, handheld, imperfect framing, natural midday overcast light, NO TEXT`

**Ne jamais utiliser** : `professional`, `editorial`, `perfect composition`, `clean`, `cinematic`, `dramatic lighting`, `8k`, `hyperreal`, `sharp focus`, `sigma 85mm f/1.4`, `high quality`, `photorealistic`.

**Alts images** (SEO + accessibilité) :
- Cover : `<focus_keyword> - <article_title>`
- Inline i : `<main_topics[i]> - <focus_keyword>` (fallback : `<keyword> - vue d'ensemble / détail pratique / conseils / guide complet`)

**Compression** : passer chaque image par Tinify (ou équivalent) avant upload → viser < 200 ko.

**Placement dans l'article** : répartir les 4 images uniformément sur les H2 (pas toutes en haut). Cover = hero, pas insérée inline.

### 11.8 Checklist qualité finale d'un article

À vérifier avant commit :

- [ ] Mots ≥ `target_word_count × 0.85` (phase 2)
- [ ] Nombre de H2 = cible phase 2 (±1)
- [ ] Chaque H2 ≥ 250 mots, chaque H3 ≥ 150 mots
- [ ] Intro 60-80 mots, répond directement à la requête
- [ ] Pas de heading "Introduction" ni "Conclusion" visible
- [ ] `focus_keyword` présent dans : H1, intro (1ère phrase), 2-3 H2, méta description
- [ ] Au moins 3 statistiques chiffrées avec source et année
- [ ] Au moins 2 angles uniques issus des `gaps` concurrents
- [ ] 1 tableau comparatif, max 1 liste à puces
- [ ] Tutoiement partout, voix active
- [ ] 2 liens externes d'autorité (`target="_blank" rel="noopener nofollow"`)
- [ ] 1 lien interne vers la page pilier
- [ ] `seo_title` ≠ `article_title`
- [ ] `meta_description` : ≤ 155 chars, emoji, CTA
- [ ] Tous les alts d'images remplis

---

## 12. Checklist "je lance un nouveau site"

1. [ ] Cloner ce playbook dans le nouveau repo
2. [ ] Créer l'arborescence (§1.1)
3. [ ] Copier/adapter les scripts utilitaires (§5)
4. [ ] Créer `.assetsignore` (§3.3)
5. [ ] Créer `favicon.svg` + `img/logo.svg` (§3.4)
6. [ ] Créer `robots.txt` + `generate_sitemap.py` (§3.1, §3.2)
7. [ ] Créer `mentions-legales.html` + `politique-confidentialite.html`
8. [ ] Créer **au moins un auteur** : `img/authors/<slug>.svg|jpg` + fichier `a-propos.html` (lié partout comme `/a-propos`, cf. §6.3) avec schema `Person`/`AboutPage` (§2.7)
9. [ ] Ajouter sur la homepage : schemas `Organization` + `WebSite` (§2.6)
10. [ ] Connecter le repo à Cloudflare Pages
11. [ ] Vérifier le domaine dans Google Search Console
12. [ ] Soumettre `sitemap.xml`
13. [ ] **Tester le responsive mobile** (§8bis) — Playwright à 320/375/768 px, hard refresh sur smartphone réel
14. [ ] Premier batch d'articles → respecter la checklist §2 pour chaque article (y compris `article-meta` + `author-card`)
15. [ ] Pour chaque nouvel article : suivre la **méthode 4 agents (§11)** — Recherche → SERP → Rédaction → SEO, sans raccourci
