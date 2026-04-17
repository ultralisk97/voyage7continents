#!/usr/bin/env python3
"""Generate 10 Oceania articles — template SEO enrichi (auteur, dates, schemas)."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "oceanie")
os.makedirs(OUT, exist_ok=True)

HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://voyage7continents.fr/oceanie/{slug}.html">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="apple-touch-icon" href="/favicon.svg">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://voyage7continents.fr/oceanie/{slug}.html">
  <meta property="og:image" content="https://voyage7continents.fr/img/articles/{slug}-1.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{og_title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://voyage7continents.fr/img/articles/{slug}-1.jpg">
  <link rel="stylesheet" href="/css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{og_title}",
    "image": "https://voyage7continents.fr/img/articles/{slug}-1.jpg",
    "mainEntityOfPage": "https://voyage7continents.fr/oceanie/{slug}.html",
    "description": "{desc}",
    "author": {{"@type": "Person", "name": "Claire Moreau", "url": "https://voyage7continents.fr/a-propos.html"}},
    "publisher": {{"@type": "Organization", "name": "Voyage 7 Continents", "logo": {{"@type": "ImageObject", "url": "https://voyage7continents.fr/img/logo.svg"}}}},
    "datePublished": "2026-04-15",
    "dateModified": "2026-04-15"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://voyage7continents.fr/"}},
      {{"@type": "ListItem", "position": 2, "name": "Océanie", "item": "https://voyage7continents.fr/oceanie/"}},
      {{"@type": "ListItem", "position": 3, "name": "{crumb}", "item": "https://voyage7continents.fr/oceanie/{slug}.html"}}
    ]
  }}
  </script>
</head>
<body>

  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="logo">Voyage<span>7Continents</span></a>
      <nav class="main-nav" aria-label="Navigation principale">
        <ul>
          <li><a href="/europe/">Europe</a></li>
          <li><a href="/asie/">Asie</a></li>
          <li><a href="/afrique/">Afrique</a></li>
          <li><a href="/amerique-nord/">Amérique du Nord</a></li>
          <li><a href="/amerique-sud/">Amérique du Sud</a></li>
          <li><a href="/oceanie/" class="active">Océanie</a></li>
          <li><a href="/antarctique/">Antarctique</a></li>
        </ul>
      </nav>
      <button class="menu-toggle" aria-label="Ouvrir le menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <section class="hero hero-pillar" style="background: linear-gradient(rgba(14,47,68,0.75), rgba(26,82,118,0.7)), url('/img/hero-oceanie.jpg') center/cover no-repeat;">
    <div class="hero-content">
      <div class="breadcrumb">
        <a href="/">Voyage 7 Continents</a> &rsaquo; <a href="/oceanie/">Océanie</a> &rsaquo; <strong>{crumb}</strong>
      </div>
      <h1>{h1}</h1>
      <p>{lead}</p>
    </div>
  </section>

  <div class="content-with-sidebar">
    <main class="pillar-content">

      <nav class="toc">
        <h3>Sommaire</h3>
        <ol>
{toc_items}
        </ol>
      </nav>

      <div class="article-meta">
        <span class="meta-author"><img src="/img/authors/claire-moreau.svg" alt="Claire Moreau" width="32" height="32" loading="lazy"> <a href="/a-propos.html">Par Claire Moreau</a></span>
        <time datetime="2026-04-15">Publié le 15 avril 2026</time>
        <time class="meta-updated" datetime="2026-04-15">Mis à jour le 15 avril 2026</time>
      </div>

      <figure class="article-hero"><img src="/img/articles/{slug}-1.jpg" alt="{alt1}" loading="lazy" width="800" height="500"><figcaption>{caption1}</figcaption></figure>

{body}

      <div class="info-box tip">
        <strong>Le conseil d'expert</strong>
        <p>{expert_tip}</p>
      </div>

      <p>Pour préparer votre voyage, retrouvez notre <a href="/oceanie/">guide complet Océanie</a> et nos autres articles de la catégorie.</p>

      <!-- author-card -->
      <aside class="author-card" aria-label="À propos de l'auteur">
        <div class="author-card-photo">
          <img src="/img/authors/claire-moreau.svg" alt="Portrait de Claire Moreau, rédactrice voyage" width="110" height="110" loading="lazy">
        </div>
        <div class="author-card-body">
          <span class="author-card-label">À propos de l'auteur</span>
          <h3><a href="/a-propos.html">Claire Moreau</a></h3>
          <p class="author-card-role">Fondatrice &amp; rédactrice en chef</p>
          <p class="author-card-bio">Journaliste voyage depuis 2014, Claire a visité 68 pays sur les 7 continents. Elle fonde Voyage 7 Continents en 2022 pour partager des guides pratiques vérifiés sur le terrain.</p>
          <a class="author-card-link" href="/a-propos.html">Lire la biographie complète &rsaquo;</a>
        </div>
      </aside>

    </main>

    <aside class="sidebar-toc">
      <h4>Navigation rapide</h4>
      <ol>
{sidebar_items}
      </ol>
    </aside>
  </div>

  <footer class="site-footer">
    <div class="footer-grid">
      <div class="footer-col">
        <h4>Voyage 7 Continents</h4>
        <p>Votre guide de référence pour voyager sur les 7 continents.</p>
      </div>
      <div class="footer-col">
        <h4>Continents</h4>
        <ul>
          <li><a href="/europe/">Europe</a></li>
          <li><a href="/asie/">Asie</a></li>
          <li><a href="/afrique/">Afrique</a></li>
          <li><a href="/amerique-nord/">Amérique du Nord</a></li>
          <li><a href="/amerique-sud/">Amérique du Sud</a></li>
          <li><a href="/oceanie/">Océanie</a></li>
          <li><a href="/antarctique/">Antarctique</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Informations</h4>
        <ul>
          <li><a href="/a-propos.html">À propos</a></li>
          <li><a href="/mentions-legales.html" rel="nofollow">Mentions légales</a></li>
          <li><a href="/politique-confidentialite.html" rel="nofollow">Politique de confidentialité</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 Voyage 7 Continents. Tous droits réservés.</p>
    </div>
  </footer>

  <script src="/js/main.js"></script>
</body>
</html>
"""

def build_body(sections, slug):
    out = []
    for sec in sections:
        out.append(f'      <h2 id="{sec["id"]}">{sec["h2"]}</h2>')
        for block in sec["blocks"]:
            kind = block[0]
            if kind == "p":
                out.append(f'      <p>{block[1]}</p>')
            elif kind == "h3":
                out.append(f'      <h3>{block[1]}</h3>')
            elif kind == "h4":
                out.append(f'      <h4>{block[1]}</h4>')
            elif kind == "img":
                n, alt = block[1], block[2]
                out.append(f'      <img class="article-img" src="/img/articles/{slug}-{n}.jpg" alt="{alt}" loading="lazy" width="800" height="500">')
            elif kind == "box":
                out.append(f'      <div class="info-box tip">\n        <strong>À retenir</strong>\n        <p>{block[1]}</p>\n      </div>')
        out.append("")
    return "\n".join(out)

def render(a):
    toc_items = "\n".join(f'          <li><a href="#{s["id"]}">{s["toc"]}</a></li>' for s in a["sections"])
    sidebar_items = "\n".join(f'        <li><a href="#{s["id"]}">{s.get("short", s["toc"])}</a></li>' for s in a["sections"])
    body = build_body(a["sections"], a["slug"])
    return HEAD.format(
        title=a["title"], desc=a["desc"], og_title=a["og_title"], slug=a["slug"],
        crumb=a["crumb"], h1=a["h1"], lead=a["lead"], alt1=a["alt1"], caption1=a["caption1"],
        toc_items=toc_items, sidebar_items=sidebar_items, body=body, expert_tip=a["expert_tip"],
    )

ARTICLES = []

# 1. Décalage horaire France-Fidji
ARTICLES.append({
    "slug": "decalage-horaire-fidji",
    "title": "Décalage Horaire France-Fidji : +10h ou +11h en 2026 ? | Voyage 7 Continents",
    "og_title": "Décalage Horaire France-Fidji : Guide Complet 2026",
    "desc": "Les Fidji sont à UTC+12 toute l'année : +10h en été et +11h en hiver par rapport à la France. Horaires, jet lag, conseils pratiques pour voyageurs.",
    "crumb": "Décalage Fidji",
    "h1": "Décalage Horaire France-Fidji",
    "lead": "Les îles Fidji sont à UTC+12 : +10 heures par rapport à la France en été, +11 heures en hiver. Guide pratique pour gérer le jet lag et planifier ses appels.",
    "alt1": "Plage de sable blanc et cocotiers aux îles Fidji avec eau turquoise",
    "caption1": "Les Fidji, à 16 000 km de la France, sont parmi les premiers pays à voir le soleil se lever chaque jour.",
    "sections": [
        {"id":"decalage-actuel","toc":"Décalage en temps réel","short":"Décalage","h2":"Quel Décalage Horaire Aujourd'hui ?",
         "blocks":[
            ("p","Les <strong>îles Fidji</strong> sont sur le fuseau horaire <strong>UTC+12</strong> (Fiji Time, FJT) toute l'année. La France, elle, alterne entre <strong>UTC+1 en hiver</strong> (heure d'hiver) et <strong>UTC+2 en été</strong> (heure d'été). Le décalage varie donc selon la saison française :"),
            ("h3","Période heure d'été française (fin mars à fin octobre)"),
            ("p","Quand il est midi à Paris, il est <strong>22 heures à Suva</strong> (capitale des Fidji). Soit <strong>+10 heures</strong>. Cette période correspond à l'hiver austral aux Fidji — saison sèche et la meilleure pour visiter."),
            ("h3","Période heure d'hiver française (fin octobre à fin mars)"),
            ("p","Quand il est midi à Paris, il est <strong>23 heures à Suva</strong>. Soit <strong>+11 heures</strong>. Cette période correspond à l'été austral, saison des pluies et des cyclones (décembre à avril)."),
            ("img",2,"Horloge mondiale affichant l'heure de Paris et de Suva"),
            ("h4","Pas de changement d'heure aux Fidji"),
            ("p","Depuis 2021, les Fidji ont <strong>abandonné le passage à l'heure d'été</strong> qu'elles pratiquaient auparavant (source : <a href=\"https://www.timeanddate.com/time/zone/fiji\" target=\"_blank\" rel=\"noopener nofollow\">timeanddate.com</a>). Le pays reste donc sur UTC+12 en permanence, ce qui simplifie les calculs pour les voyageurs."),
         ]},
        {"id":"vol-jetlag","toc":"Vol et jet lag","short":"Jet lag","h2":"Vol Paris-Fidji et Jet Lag",
         "blocks":[
            ("p","Il n'existe <strong>aucun vol direct Paris-Nadi</strong> (l'aéroport international des Fidji). Toutes les connexions passent par une escale, le plus souvent en Asie (Singapour, Séoul, Hong Kong) ou en Océanie (Sydney, Auckland). Compter au minimum <strong>28 à 32 heures</strong> de trajet total, escales comprises."),
            ("h3","Itinéraires classiques"),
            ("p","<strong>Via Séoul avec Korean Air</strong> puis Fiji Airways : souvent le meilleur tarif (1 400-1 800 €). <strong>Via Sydney avec Qantas/Emirates + Fiji Airways</strong> : plus long mais une seule escale principale. <strong>Via Los Angeles avec Fiji Airways</strong> : possible depuis Londres, rare depuis Paris."),
            ("img",3,"Avion Fiji Airways sur le tarmac de l'aéroport international de Nadi"),
            ("h3","Gérer le jet lag"),
            ("p","Traverser <strong>10 à 11 fuseaux horaires</strong> dans le même sens (vers l'Est) provoque un jet lag sévère. Le corps met en moyenne <strong>1 jour par fuseau traversé</strong> pour se resynchroniser, soit <strong>10 jours complets</strong>. Les premiers 3-4 jours sont généralement les plus difficiles."),
            ("h4","Astuces qui marchent"),
            ("p","<strong>S'exposer à la lumière naturelle</strong> en matinée une fois sur place (effet sur la mélatonine), éviter les siestes de plus de 20 minutes les 2 premiers jours, manger aux horaires locaux immédiatement, s'hydrater en vol (2 L d'eau minimum), éviter l'alcool. La mélatonine 1 mg le soir aide à caler le sommeil les 3-4 premiers jours."),
         ]},
        {"id":"appels-famille","toc":"Appels et famille","short":"Appels","h2":"Appeler la France depuis les Fidji",
         "blocks":[
            ("p","Avec <strong>10 à 11 heures de décalage</strong>, les créneaux pour téléphoner à la famille sont restreints. Voici les meilleures fenêtres pour ne réveiller personne."),
            ("h3","Meilleures heures pour appeler la France"),
            ("p","<strong>Depuis les Fidji le matin (7h-10h)</strong>, il est 20h-23h en France heure d'été, ou 21h-00h en heure d'hiver. C'est le créneau idéal : vous êtes réveillé(e) et vos proches sont disponibles le soir."),
            ("p","<strong>Depuis les Fidji en fin de journée (19h-22h)</strong>, il est 8h-11h du matin en France (été) ou 9h-12h (hiver). Bon créneau pour attraper quelqu'un au bureau ou au réveil."),
            ("img",4,"Personne en visioconférence avec vue sur un lagon des Fidji"),
            ("h3","Éviter"),
            ("p","Appeler <strong>au milieu de votre journée aux Fidji (midi-17h)</strong> revient à téléphoner à 1h-6h du matin en France. À réserver aux urgences uniquement."),
            ("h4","WhatsApp et WiFi"),
            ("p","La plupart des resorts fidjiens offrent un WiFi correct (parfois payant, 5-10 FJD/jour). WhatsApp et FaceTime fonctionnent bien. Pour appeler en 4G, une eSIM locale (Vodafone Fiji) à environ 15 € pour 10 Go couvre largement un séjour de 15 jours."),
         ]},
        {"id":"retour-france","toc":"Retour et jet lag inverse","short":"Retour","h2":"Retour en France : Jet Lag Inverse",
         "blocks":[
            ("p","Le retour Fidji → France est <strong>plus difficile</strong> que l'aller pour la majorité des voyageurs. Voler vers l'Ouest (l'Europe) en traversant les fuseaux dans le sens inverse raccourcit la journée au lieu de l'allonger : le corps doit avancer son rythme circadien, ce qui est contre-intuitif."),
            ("p","Prévoyez <strong>2 à 3 jours de récupération</strong> à la maison avant de reprendre le travail. Ne planifiez pas de réunion importante le lendemain du retour."),
            ("img",5,"Voyageur fatigué à l'aéroport Roissy CDG après un vol long-courrier"),
            ("h4","Le piège de la ligne de changement de date"),
            ("p","Les Fidji sont situées <strong>juste à l'ouest de la ligne internationale de changement de date</strong>. Au retour, vous « récupérez » une journée : si vous décollez un lundi soir, vous arrivez en France un mardi matin du même jour civil, malgré 30h de voyage. Vérifiez bien les dates sur votre billet pour ne pas vous tromper le jour du départ."),
         ]},
    ],
    "expert_tip":"Pour minimiser le jet lag à l'aller, <strong>commencez à décaler vos heures de coucher 3 jours avant le départ</strong> (couchez-vous 1h plus tôt chaque soir). À l'arrivée aux Fidji, forcez-vous à rester éveillé(e) jusqu'à 21h-22h locale même si vous tombez de fatigue — une sieste tardive peut ruiner votre première nuit. Et emportez un masque de sommeil et des bouchons d'oreilles : les resorts sont calmes, mais les chants d'oiseaux dès 5h du matin peuvent surprendre.",
})

# 2. Monnaie Papouasie
ARTICLES.append({
    "slug": "monnaie-papouasie",
    "title": "Quelle est la Monnaie de la Papouasie-Nouvelle-Guinée ? Kina 2026 | Voyage 7 Continents",
    "og_title": "Monnaie Papouasie-Nouvelle-Guinée : Le Kina (PGK) 2026",
    "desc": "La monnaie de la Papouasie-Nouvelle-Guinée est le kina (PGK) : taux de change, billets, retraits, cash, cartes bancaires et astuces pratiques pour voyageurs.",
    "crumb": "Monnaie Papouasie",
    "h1": "Quelle est la Monnaie de la Papouasie-Nouvelle-Guinée ?",
    "lead": "La Papouasie-Nouvelle-Guinée utilise le kina (PGK), divisé en 100 toea. Taux de change, retraits ATM, cartes bancaires et cash : le guide complet pour votre voyage.",
    "alt1": "Billets et pièces de kina, monnaie officielle de la Papouasie-Nouvelle-Guinée",
    "caption1": "Le kina de Papouasie-Nouvelle-Guinée, dont le nom vient d'un coquillage traditionnellement utilisé comme monnaie.",
    "sections": [
        {"id":"kina-base","toc":"Le kina","short":"Kina","h2":"Le Kina (PGK) en Bref",
         "blocks":[
            ("p","La <strong>monnaie officielle</strong> de la Papouasie-Nouvelle-Guinée est le <strong>kina</strong> (code ISO : <strong>PGK</strong>, symbole : K). Son nom vient d'un coquillage nacré (<em>Pinctada maxima</em>) qui servait traditionnellement de moyen d'échange dans de nombreuses sociétés mélanésiennes avant la colonisation. Le kina a remplacé le dollar australien le 19 avril 1975, quelques mois avant l'indépendance du pays."),
            ("p","Un kina se divise en <strong>100 toea</strong>. Les billets en circulation sont de <strong>2, 5, 10, 20, 50 et 100 kina</strong>, et les pièces de <strong>5, 10, 20, 50 toea et 1 kina</strong>. Les billets récents sont en polymère (plastique), plus résistants à l'humidité tropicale."),
            ("img",2,"Banque de Papouasie-Nouvelle-Guinée à Port Moresby"),
            ("h3","Banque centrale"),
            ("p","L'émission du kina est gérée par la <a href=\"https://www.bankpng.gov.pg/\" target=\"_blank\" rel=\"noopener nofollow\">Bank of Papua New Guinea</a>, la banque centrale du pays. Elle publie les taux de change officiels et supervise les banques commerciales (BSP, ANZ, Westpac, Kina Bank)."),
         ]},
        {"id":"taux-change","toc":"Taux de change","short":"Taux","h2":"Taux de Change Euro-Kina",
         "blocks":[
            ("p","Le taux de change <strong>EUR / PGK</strong> fluctue autour de <strong>1 € = 4,1 à 4,4 kina</strong> en 2026 (à vérifier en temps réel avant le départ). Le kina est une monnaie peu liquide sur les marchés internationaux, ce qui signifie qu'il est <strong>difficile à obtenir en France avant le départ</strong>."),
            ("h3","Ordres de grandeur"),
            ("p","<strong>10 € ≈ 42 PGK</strong> : un déjeuner dans un marché local. <strong>50 € ≈ 210 PGK</strong> : une nuit en auberge simple à Port Moresby. <strong>200 € ≈ 840 PGK</strong> : une nuit dans un lodge de trekking en vallée du Wahgi. <strong>1 000 € ≈ 4 200 PGK</strong> : une semaine complète en lodge tout compris en zone rurale."),
            ("img",3,"Marché local à Mount Hagen avec vendeurs et produits locaux en kina"),
            ("h3","Où s'informer du taux"),
            ("p","Consultez <a href=\"https://www.xe.com/currencyconverter/convert/?From=EUR&To=PGK\" target=\"_blank\" rel=\"noopener nofollow\">XE.com</a> ou <a href=\"https://wise.com/fr/currency-converter/pgk-to-eur-rate\" target=\"_blank\" rel=\"noopener nofollow\">Wise</a> pour le taux interbancaire en temps réel. Les bureaux de change pratiquent une marge de <strong>3 à 6 %</strong> au-dessus de ce taux."),
         ]},
        {"id":"retraits","toc":"Retraits et cartes","short":"Retraits","h2":"Retraits et Cartes Bancaires",
         "blocks":[
            ("p","La Papouasie-Nouvelle-Guinée est un pays où le <strong>cash reste roi</strong>. Les cartes bancaires internationales (Visa, Mastercard) ne sont acceptées que dans une minorité d'établissements : hôtels haut de gamme de Port Moresby, quelques supermarchés de la capitale, agences de voyages formelles. En dehors de la capitale, prévoyez <strong>uniquement du cash</strong>."),
            ("h3","Retirer sur place"),
            ("p","Les distributeurs automatiques (ATM) sont présents à <strong>Port Moresby, Lae, Mount Hagen, Madang</strong>, principalement dans les agences BSP, ANZ et Westpac. Plafond de retrait par transaction : <strong>1 000 à 2 000 PGK</strong> selon la banque. Frais de retrait internationaux : <strong>15 à 30 PGK</strong> côté banque locale, plus la commission de votre banque française (souvent 2-3 % + 2-4 €)."),
            ("img",4,"Distributeur automatique BSP (Bank South Pacific) en Papouasie-Nouvelle-Guinée"),
            ("h3","Recommandations"),
            ("p","<strong>Prévoyez une carte Visa et une carte Mastercard</strong> en backup (certains ATM n'acceptent qu'un réseau). <strong>Prévenez votre banque</strong> de votre voyage avant le départ pour éviter un blocage sécurité. <strong>Emportez 200-300 € en liquide</strong> (USD ou AUD) comme fonds de secours — plus faciles à changer que l'euro dans les bureaux de change locaux."),
            ("h4","Traveler's cheques"),
            ("p","Les <strong>chèques de voyage</strong> (traveler's cheques) sont quasiment inacceptés aujourd'hui et ne sont plus recommandés. Privilégiez cash + carte bancaire."),
         ]},
        {"id":"conseils","toc":"Conseils pratiques","short":"Conseils","h2":"Conseils Pratiques pour Votre Voyage",
         "blocks":[
            ("p","La Papouasie-Nouvelle-Guinée est un pays avec un <strong>taux de criminalité élevé</strong> à Port Moresby et Lae (<a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/papouasie-nouvelle-guinee/\" target=\"_blank\" rel=\"noopener nofollow\">Source : France Diplomatie</a>). Les conseils suivants sont basés sur les recommandations des ambassades occidentales."),
            ("h3","Sécurité du cash"),
            ("p","Ne retirez jamais de grosses sommes en une seule fois en ville. Évitez de sortir votre portefeuille en public. Répartissez votre cash dans plusieurs poches et un petit coffre caché. Préférez les ATM situés <strong>dans l'enceinte sécurisée</strong> d'un hôtel ou d'un centre commercial."),
            ("img",5,"Hôtel sécurisé à Port Moresby avec gardiennage à l'entrée"),
            ("box","Pour les trekkings en zones rurales (Kokoda Track, Mount Wilhelm, Sepik), <strong>prévoyez tout le cash nécessaire avant de partir</strong> : aucun ATM fonctionnel au-delà des villes principales. Les guides et porteurs sont payés en kina uniquement."),
            ("h4","Pourboires"),
            ("p","Le pourboire n'est <strong>pas une tradition</strong> en PNG, mais il est apprécié dans le tourisme : 5-10 % dans les restaurants haut de gamme, quelques kinas au porteur, un petit extra aux guides de trek en fin de circuit (environ 100 PGK par jour et par client)."),
         ]},
    ],
    "expert_tip":"Changez <strong>200-300 € en kina</strong> dès l'atterrissage à l'aéroport Jackson de Port Moresby (bureaux BSP et Travelex dans le hall des arrivées, taux correct). Ne comptez pas sur les changes en ville : ils ferment tôt et les files sont longues. Et gardez toujours une <strong>petite réserve en USD ou AUD</strong> dans un endroit séparé : en cas de vol ou de carte bloquée, ces devises se changent plus facilement que l'euro dans les zones reculées.",
})

# 3. Température Nouvelle-Zélande juillet
ARTICLES.append({
    "slug": "temperature-nouvelle-zelande-juillet",
    "title": "Température Moyenne Nouvelle-Zélande en Juillet : Hiver Austral 2026 | Voyage 7 Continents",
    "og_title": "Température Nouvelle-Zélande Juillet : 5 à 15°C selon la Région",
    "desc": "Juillet est le cœur de l'hiver austral en Nouvelle-Zélande : 5 à 15°C selon la région, neige dans les Alpes, climat doux au nord. Le guide complet par ville.",
    "crumb": "Température NZ juillet",
    "h1": "Température Moyenne en Nouvelle-Zélande en Juillet",
    "lead": "Juillet est le cœur de l'hiver austral néo-zélandais : 5 à 15°C selon la latitude, neige dans les Alpes du Sud, pluie à Wellington, doux climat à Auckland.",
    "alt1": "Paysage enneigé du mont Cook en Nouvelle-Zélande avec ciel clair d'hiver",
    "caption1": "Le mont Cook (Aoraki), 3 724 m, sous la neige en juillet : c'est le plein hiver austral sur l'île du Sud.",
    "sections": [
        {"id":"hiver-austral","toc":"Hiver austral","short":"Hiver","h2":"Juillet : Cœur de l'Hiver Austral",
         "blocks":[
            ("p","La Nouvelle-Zélande est située dans <strong>l'hémisphère sud</strong>, ce qui inverse les saisons par rapport à la France. Juillet y correspond au <strong>cœur de l'hiver austral</strong> (équivalent janvier en France). Les journées sont courtes (9-10 h de jour), les températures basses, la pluviométrie variable selon les régions."),
            ("p","Contrairement à ce qu'on imagine, l'hiver néo-zélandais <strong>n'est pas glacial</strong> grâce à l'influence océanique : les températures restent positives la journée partout au niveau de la mer. Mais la montagne, les plateaux intérieurs et l'île du Sud peuvent être très froids."),
            ("img",2,"Vignoble enneigé dans la région de Central Otago en juillet"),
            ("h3","Jours et nuits"),
            ("p","Le <strong>solstice d'hiver</strong> a lieu le 21 juin : en juillet, les jours commencent tout juste à rallonger. À Auckland, le soleil se lève vers 7h30 et se couche vers 17h15. À Queenstown, lever 8h15, coucher 17h10. Prévoir les activités outdoor le matin : le froid s'intensifie après 16h."),
         ]},
        {"id":"temperatures-villes","toc":"Températures par ville","short":"Villes","h2":"Températures Moyennes par Ville en Juillet",
         "blocks":[
            ("p","Les écarts entre le nord et le sud du pays sont importants : plus de <strong>2 200 km séparent Kaitaia (extrême nord) de Bluff (extrême sud)</strong>, soit l'équivalent de Paris-Lisbonne en latitude. Les données qui suivent proviennent de <a href=\"https://niwa.co.nz/climate\" target=\"_blank\" rel=\"noopener nofollow\">NIWA (National Institute of Water and Atmospheric Research)</a>."),
            ("h3","Auckland (île du Nord)"),
            ("p","Climat subtropical océanique : <strong>minimale moyenne 8°C, maximale moyenne 15°C</strong>. Pluviométrie élevée (environ 140 mm sur le mois, 15 jours de pluie). C'est la ville la plus douce du pays. Auckland reçoit rarement la neige (le dernier épisode en ville date de 2011)."),
            ("h3","Wellington (île du Nord, sud)"),
            ("p","<strong>Minimale 6°C, maximale 12°C</strong>. Plus fraîche qu'Auckland, très venteuse (surnom local : « Windy Welly »). Les rafales dépassent fréquemment 60 km/h, ce qui donne un ressenti très froid. Prévoir veste coupe-vent."),
            ("img",3,"Rue piétonne de Wellington sous la pluie en juillet avec passants en manteaux"),
            ("h3","Christchurch (île du Sud, est)"),
            ("p","<strong>Minimale 2°C, maximale 12°C</strong>. Climat plus continental : gelées matinales fréquentes (jusqu'à -3°C), après-midi douces quand le soleil perce. Peu de pluie (environ 60 mm) mais neige possible 1-2 jours par mois en moyenne."),
            ("h3","Queenstown (île du Sud, Alpes)"),
            ("p","<strong>Minimale -1°C, maximale 8°C</strong>. Station de ski la plus connue du pays. Neige fréquente, pistes ouvertes à Coronet Peak, The Remarkables, Cardrona. C'est la région la plus froide accessible en voiture."),
            ("h3","Milford Sound (fjords)"),
            ("p","<strong>Minimale 2°C, maximale 9°C</strong>. Pluies abondantes toute l'année (plus de 400 mm en juillet !) — c'est l'une des zones les plus arrosées du monde. Les cascades sont alors à leur maximum, les fjords spectaculaires sous les nuages."),
         ]},
        {"id":"equipement","toc":"Que mettre dans sa valise","short":"Équipement","h2":"Équipement pour Juillet en Nouvelle-Zélande",
         "blocks":[
            ("p","L'hiver néo-zélandais demande un équipement adapté mais pas extrême. Le <strong>système 3 couches</strong> classique (base thermique, polaire, coupe-vent/imperméable) convient à 90 % des situations. Seule la haute montagne (ski, treks d'altitude) demande plus."),
            ("h3","Vêtements indispensables"),
            ("p","<strong>Imperméable respirant</strong> (type Gore-Tex), <strong>polaire 200-300 g</strong>, <strong>pantalon chaud</strong> qui sèche vite, <strong>1-2 sous-pulls mérinos</strong>, <strong>bonnet et gants légers</strong>, <strong>chaussures de randonnée imperméables</strong>. Les Néo-Zélandais portent rarement le manteau lourd : on privilégie les couches superposables."),
            ("img",4,"Randonneur en tenue 3 couches au Tongariro National Park en juillet"),
            ("h3","Pour les activités outdoor"),
            ("p","<strong>Ski</strong> : lunettes de soleil catégorie 3, crème solaire 50 (le soleil sur la neige est redoutable malgré le froid), pantalon de ski imperméable, gants de ski. <strong>Trek</strong> : bâtons de marche, crampons légers (microspikes) pour les zones givrées, lampe frontale (nuit à 17h)."),
            ("h4","Ce dont on n'a pas besoin"),
            ("p","Une grosse doudoune type Antarctique, une combinaison de ski professionnelle, des bottes polaires : la météo ne justifie pas cet équipement au niveau de la mer. Réservez-le à la haute montagne."),
         ]},
        {"id":"avantages-inconvenients","toc":"Pour / contre","short":"Pour/contre","h2":"Avantages et Inconvénients de Juillet",
         "blocks":[
            ("p","Voyager en Nouvelle-Zélande en juillet a des qualités et des défauts qu'il faut bien peser avant de réserver."),
            ("h3","Les plus"),
            ("p","<strong>Ski et snowboard</strong> dans un décor unique (2 grandes régions : Queenstown/Wanaka et Ruapehu). <strong>Peu de touristes</strong> — hors stations de ski, les sites majeurs (Milford, Rotorua, Tongariro) sont quasi vides. <strong>Prix bas</strong> : billets d'avion, locations de voiture et hébergements sont 30-50 % moins chers qu'en été. <strong>Paysages grandioses</strong> avec neige sur les sommets."),
            ("h3","Les moins"),
            ("p","<strong>Certaines routes fermées</strong> : Milford Road (SH94) peut être bloquée par avalanches, Crown Range par la neige. <strong>Jours courts</strong> : difficile de faire des longues randonnées après 15h. <strong>Plages interdites</strong> à la baignade (trop froid, courants, méduses parfois)."),
            ("img",5,"Route de montagne néo-zélandaise fermée par la neige en hiver avec panneau"),
            ("h4","Ce qui est possible"),
            ("p","Road trips bien planifiés en 4x4 ou camping-car équipé, observation des baleines à Kaikoura (présentes toute l'année), sources chaudes de Rotorua (géothermie, eau à 40°C même en hiver !), Tongariro Alpine Crossing accessible en raquettes avec guide."),
         ]},
    ],
    "expert_tip":"Si vous venez pour le ski, <strong>basez-vous à Queenstown</strong> plutôt qu'à Wanaka : les pistes sont plus variées, les options « hors-ski » (bains chauds, bars, jet-boat) plus nombreuses, et les transferts aux stations sont organisés. Réservez votre logement <strong>au moins 2 mois à l'avance</strong> pour les semaines de vacances scolaires australiennes et néo-zélandaises (début juillet en général) : les prix montent de 40-60 % et les bons adresses sont prises.",
})

# 4. Vaccins Vanuatu
ARTICLES.append({
    "slug": "vaccins-vanuatu",
    "title": "Vaccins Obligatoires pour le Vanuatu en 2026 : Guide Officiel | Voyage 7 Continents",
    "og_title": "Vaccins Vanuatu 2026 : Obligatoires et Recommandés",
    "desc": "Aucun vaccin n'est strictement obligatoire pour le Vanuatu (sauf fièvre jaune si transit), mais plusieurs sont fortement recommandés : hépatite A, typhoïde, DTP. Guide officiel.",
    "crumb": "Vaccins Vanuatu",
    "h1": "Vaccins Obligatoires pour le Vanuatu",
    "lead": "Aucun vaccin n'est strictement obligatoire à l'entrée du Vanuatu pour les voyageurs venant de France, mais plusieurs sont fortement recommandés selon les sources officielles. Le guide complet 2026.",
    "alt1": "Carnet de vaccination international avec seringue et passeport",
    "caption1": "Préparer sa trousse médicale de voyage et vérifier ses vaccins est essentiel avant un séjour au Vanuatu.",
    "sections": [
        {"id":"obligatoires","toc":"Vaccins obligatoires","short":"Obligatoires","h2":"Vaccins Strictement Obligatoires",
         "blocks":[
            ("p","Pour un voyage direct depuis la France métropolitaine vers le Vanuatu, <strong>aucun vaccin n'est obligatoire</strong> à l'entrée du territoire. Le Vanuatu ne figure pas dans la liste des pays à risque de fièvre jaune et ne l'exige donc pas des ressortissants français."),
            ("h3","Exception : transit par un pays à risque"),
            ("p","<strong>Seule exception</strong> : si vous <strong>transitez par un pays où la fièvre jaune circule</strong> (Amérique du Sud tropicale, Afrique subsaharienne), le certificat de vaccination contre la fièvre jaune devient obligatoire. L'<a href=\"https://www.pasteur.fr/fr/centre-medical/fiches-maladies/fievre-jaune\" target=\"_blank\" rel=\"noopener nofollow\">Institut Pasteur</a> liste précisément les pays concernés."),
            ("img",2,"Centre de vaccinations internationales avec affiches d'information"),
            ("h3","Base officielle"),
            ("p","La référence en France est la rubrique <a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/vanuatu/\" target=\"_blank\" rel=\"noopener nofollow\">Conseils aux voyageurs - Vanuatu</a> de France Diplomatie, mise à jour régulièrement. En cas de doute, consultez <strong>un centre de vaccinations internationales</strong> (Pasteur, Air France, Hôtel-Dieu) 4 à 6 semaines avant le départ."),
         ]},
        {"id":"recommandes","toc":"Vaccins recommandés","short":"Recommandés","h2":"Vaccins Fortement Recommandés",
         "blocks":[
            ("p","Même s'ils ne sont pas exigés à la frontière, plusieurs vaccins sont <strong>fortement conseillés</strong> par l'Institut Pasteur, l'OMS et les centres spécialisés pour un séjour au Vanuatu. Ils couvrent les risques réels sur place."),
            ("h3","Vaccinations universelles à jour"),
            ("p","<strong>Diphtérie-Tétanos-Poliomyélite (DTP)</strong> : rappel si > 10 ans. <strong>Rougeole-Oreillons-Rubéole (ROR)</strong> pour les jeunes adultes nés après 1980. <strong>Hépatite B</strong> : séjours longs ou contacts sanguins possibles (soins médicaux, piercing, tatouage)."),
            ("h3","Vaccins spécifiques au voyage"),
            ("p","<strong>Hépatite A</strong> : vivement recommandée — transmission par l'eau et l'alimentation, facile à attraper au Vanuatu même dans un bon hôtel. Protection à vie en 2 doses (6-12 mois entre les deux, mais 1 seule dose suffit pour démarrer)."),
            ("p","<strong>Typhoïde</strong> : recommandée pour les séjours > 2 semaines ou les conditions d'hygiène moyennes. Efficacité environ 70 %, rappel tous les 3 ans."),
            ("img",3,"Échantillons de vaccins contre l'hépatite A et la typhoïde"),
            ("h3","Cas particuliers"),
            ("p","<strong>Rage</strong> : à envisager pour les séjours > 1 mois, les trekkings isolés, les voyageurs qui travaillent avec les animaux. <strong>Encéphalite japonaise</strong> : non recommandée car la maladie n'est pas présente au Vanuatu."),
         ]},
        {"id":"paludisme","toc":"Paludisme et moustiques","short":"Paludisme","h2":"Paludisme et Maladies des Moustiques",
         "blocks":[
            ("p","Le Vanuatu est classé <strong>zone de transmission du paludisme</strong> (zone 3 selon l'OMS) sur toutes les îles, y compris les zones touristiques. Le risque est modéré mais réel, surtout en saison des pluies (décembre à avril)."),
            ("h3","Prophylaxie antipaludique"),
            ("p","Le traitement préventif recommandé varie selon la durée du séjour : <strong>Atovaquone-Proguanil (Malarone)</strong> pour les séjours courts (1-3 semaines, bien toléré, prise quotidienne) ou <strong>Doxycycline</strong> (moins cher, à éviter si soleil fort et grossesse). Consultation médicale obligatoire pour la prescription — ce ne sont pas des médicaments en vente libre."),
            ("p","La molécule <strong>Méfloquine (Lariam)</strong>, ancien standard, est aujourd'hui moins prescrite à cause de ses effets secondaires psychiatriques."),
            ("img",4,"Moustiquaire imprégnée installée au-dessus d'un lit dans un bungalow tropical"),
            ("h3","Dengue, chikungunya, Zika"),
            ("p","Présents aussi au Vanuatu, ces virus transmis par le moustique <em>Aedes aegypti</em> n'ont <strong>pas de vaccin disponible</strong> en voyage touristique. Seule la prévention anti-moustiques protège : <strong>répulsif DEET 30-50 %</strong>, vêtements longs au coucher du soleil, moustiquaire imprégnée, climatisation. L'<a href=\"https://www.who.int/fr/health-topics/dengue-and-severe-dengue\" target=\"_blank\" rel=\"noopener nofollow\">OMS</a> documente une hausse régulière des cas dans le Pacifique Sud."),
            ("h4","Éviter les piqûres"),
            ("p","Les moustiques du paludisme piquent principalement <strong>du coucher au lever du soleil</strong> — protection maximale le soir et la nuit. Ceux de la dengue piquent en journée, surtout en début et fin d'après-midi."),
         ]},
        {"id":"preparation","toc":"Préparer son voyage","short":"Préparer","h2":"Préparer Son Voyage Santé",
         "blocks":[
            ("p","Anticipez la préparation sanitaire : les vaccins demandent du temps (6 semaines minimum pour certains) et un rendez-vous médical est toujours nécessaire."),
            ("h3","Calendrier à respecter"),
            ("p","<strong>6 à 8 semaines avant le départ</strong> : consulter un centre de vaccinations internationales ou un médecin du voyage. Faire le point sur vos vaccins de base, programmer les injections recommandées (hépatite A, typhoïde, éventuellement rage). <strong>4 semaines avant</strong> : obtenir l'ordonnance pour la prophylaxie antipaludique. <strong>1 semaine avant</strong> : préparer la trousse à pharmacie."),
            ("img",5,"Trousse à pharmacie de voyage avec médicaments et bandages"),
            ("h3","Trousse de voyage"),
            ("p","Répulsif anti-moustiques DEET, anti-diarrhéique (lopéramide), antibiotique à spectre large (ciprofloxacine — sur prescription, utile en cas de turista sévère), paracétamol, pansements, crème solaire 50, désinfectant, thermomètre, sérum physiologique."),
            ("box","Souscrivez toujours une <strong>assurance voyage avec rapatriement sanitaire</strong> pour le Vanuatu : le système de santé local est limité, et une évacuation vers l'Australie ou la Nouvelle-Calédonie peut coûter <strong>30 000 à 80 000 €</strong>. Les cartes bancaires premium (Visa Premier, Mastercard Gold) couvrent souvent, mais vérifiez les plafonds avant de compter dessus."),
         ]},
    ],
    "expert_tip":"Le risque sanitaire n°1 au Vanuatu n'est ni le paludisme ni l'hépatite : c'est <strong>la turista et la déshydratation</strong>. Ne buvez que de l'eau en bouteille scellée ou filtrée, évitez les glaçons dans les bars de brousse, pelez vos fruits vous-même. Et emportez un <strong>filtre à eau portable</strong> (Grayl, Sawyer Mini) si vous prévoyez des treks en dehors de Port-Vila et Luganville — c'est plus léger et plus sûr que d'acheter des bouteilles en plastique dans chaque village.",
})

# 5. Eau robinet Australie
ARTICLES.append({
    "slug": "eau-robinet-australie",
    "title": "Peut-on Boire l'Eau du Robinet en Australie ? Guide Complet 2026 | Voyage 7 Continents",
    "og_title": "Eau du Robinet en Australie : Oui, Potable Partout en 2026",
    "desc": "L'eau du robinet est potable dans toute l'Australie urbaine selon les standards NHMRC. Exceptions en Outback, qualité par ville, goût, réglementation : le guide.",
    "crumb": "Eau robinet Australie",
    "h1": "Peut-on Boire l'Eau du Robinet en Australie ?",
    "lead": "Oui, l'eau du robinet est potable dans toute l'Australie urbaine et respecte les standards NHMRC les plus stricts au monde. Quelques précautions en Outback et dans les propriétés privées.",
    "alt1": "Verre d'eau claire remplie au robinet dans une cuisine australienne moderne",
    "caption1": "L'eau du robinet australienne est l'une des plus contrôlées au monde et se boit sans crainte en ville.",
    "sections": [
        {"id":"oui-potable","toc":"Oui, potable partout","short":"Potable","h2":"Oui, l'Eau du Robinet est Potable en Australie",
         "blocks":[
            ("p","<strong>La réponse courte est oui</strong> : l'eau du robinet est potable et sûre à boire dans l'ensemble de l'Australie urbaine et périurbaine. L'Australie applique l'un des systèmes de contrôle de qualité de l'eau potable les plus rigoureux au monde, sous la supervision du <a href=\"https://www.nhmrc.gov.au/about-us/publications/australian-drinking-water-guidelines\" target=\"_blank\" rel=\"noopener nofollow\">NHMRC (National Health and Medical Research Council)</a>, qui publie régulièrement les <em>Australian Drinking Water Guidelines</em>."),
            ("p","Ces directives couvrent plus de <strong>250 paramètres</strong> (bactériologie, métaux lourds, pesticides, résidus chimiques, radioéléments), avec des seuils parfois plus stricts que ceux de l'OMS. Elles sont appliquées et contrôlées par les opérateurs d'eau de chaque État (Sydney Water, Melbourne Water, SA Water, etc.)."),
            ("img",2,"Laboratoire de contrôle qualité de l'eau potable en Australie"),
            ("h3","Source de l'eau"),
            ("p","L'eau provient de <strong>barrages de surface</strong> (le plus courant), <strong>nappes souterraines</strong>, ou d'<strong>usines de désalinisation</strong> (Perth, Sydney, Melbourne ont toutes des usines, activées lors des sécheresses). Elle est traitée par filtration, coagulation, désinfection (chlore, parfois UV ou ozone) avant distribution."),
         ]},
        {"id":"par-ville","toc":"Qualité par ville","short":"Villes","h2":"Qualité de l'Eau par Grande Ville",
         "blocks":[
            ("p","La qualité de l'eau est <strong>uniformément bonne</strong> dans les capitales d'État, mais son goût et sa dureté varient légèrement selon la source."),
            ("h3","Sydney"),
            ("p","Eau provenant des barrages du bassin versant (Warragamba, Nepean). Goût neutre, <strong>dureté moyenne</strong>, légère trace de chlore. Des rapports trimestriels sont publiés en libre accès par Sydney Water. Pas de filtration nécessaire — certains préfèrent une carafe filtrante Brita par goût, pas par sécurité."),
            ("h3","Melbourne"),
            ("p","Parmi les <strong>eaux les plus pures du monde</strong> en eau urbaine : elle provient de bassins versants boisés protégés (Thomson, Upper Yarra), intactes depuis 130 ans. Douce, faiblement chlorée, excellent goût. Peu de gens y installent un filtre."),
            ("img",3,"Barrage de Thomson en forêt protégée, source d'eau de Melbourne"),
            ("h3","Brisbane, Perth, Adelaide"),
            ("p","<strong>Brisbane</strong> : eau traitée, plus dure qu'à Melbourne, goût correct. <strong>Perth</strong> : mélange d'eau souterraine, de désalinisation et de barrages — légèrement plus salée mais bien dans les normes. <strong>Adelaide</strong> : réputée pour son goût plus marqué car elle provient en grande partie du Murray River (eau traitée, parfaitement potable, mais moins « neutre » au palais)."),
            ("h3","Darwin, Hobart, Cairns"),
            ("p","Toutes ces villes ont une <strong>eau potable de qualité</strong>. Hobart (Tasmanie) est souvent citée avec Melbourne comme la meilleure eau d'Australie grâce à ses bassins versants protégés."),
         ]},
        {"id":"outback","toc":"Outback et zones rurales","short":"Outback","h2":"Outback et Zones Rurales : Précautions",
         "blocks":[
            ("p","Hors des villes, certaines zones demandent plus de prudence — non parce que l'eau est dangereuse, mais parce que les sources et traitements peuvent être différents ou moins fréquemment contrôlés."),
            ("h3","Propriétés isolées, fermes, stations"),
            ("p","Dans l'Outback, de nombreuses propriétés (stations agricoles, motels isolés) utilisent des <strong>réservoirs de captage d'eau de pluie</strong> (« rainwater tanks ») sur le toit. Cette eau est généralement potable mais peut contenir des <strong>débris organiques</strong> si le réservoir n'est pas entretenu. Demandez avant de boire, faites bouillir en cas de doute."),
            ("h3","Eau bore (forage)"),
            ("p","Certaines zones utilisent l'<strong>eau de forage profond</strong> (« bore water »), naturellement potable mais parfois <strong>très minéralisée</strong> (goût ferreux ou salé). Elle n'est pas dangereuse, juste peu agréable. Les cafés et restaurants servent souvent de l'eau en bouteille dans ces régions."),
            ("img",4,"Réservoir de captage d'eau de pluie en tôle dans une station d'Australie centrale"),
            ("h4","Panneaux « Non-potable »"),
            ("p","Dans les aires de repos et les campings du Top End (Territoire du Nord) et de l'Outback WA, certains points d'eau sont marqués <strong>« Not suitable for drinking »</strong>. Respectez toujours ces panneaux : l'eau y est destinée au lavage ou à l'arrosage, pas à la consommation."),
         ]},
        {"id":"pratiques","toc":"Conseils pratiques","short":"Conseils","h2":"Conseils Pratiques pour les Voyageurs",
         "blocks":[
            ("p","Voici les bonnes pratiques pour boire l'eau du robinet sans crainte et réduire votre usage de bouteilles en plastique."),
            ("h3","Gourde réutilisable"),
            ("p","Emportez une <strong>gourde en inox ou en plastique BPA-free</strong>. Toutes les villes australiennes multiplient les fontaines publiques gratuites (« drinking fountains », « bubblers ») dans les parcs, gares et centres commerciaux. C'est économique, écologique, et parfaitement sûr."),
            ("h3","Eau chaude des thermos publics"),
            ("p","Beaucoup d'<strong>aires de pique-nique et aires de repos</strong> le long des routes offrent de l'eau chaude gratuite pour le thé et le café (« free boiling water »). Une tradition australienne très pratique pour les road-trippers."),
            ("img",5,"Fontaine à eau publique dans un parc de Sydney avec voyageurs qui remplissent leurs gourdes"),
            ("h3","Si le goût ne vous plaît pas"),
            ("p","Si vous trouvez l'eau trop chlorée, mettez-la au frigo 1 h avant de la boire : le chlore s'évapore et le goût s'adoucit. Une carafe filtrante (Brita) règle le problème pour moins de 20 AUD en supermarché."),
            ("box","En cas de <strong>coupure d'eau</strong> (incendies, inondations, réparations), les autorités émettent un <em>Boil Water Alert</em> diffusé sur tous les médias et via SMS d'urgence. Respectez-le : faire bouillir l'eau 1 minute suffit à éliminer tout risque bactérien."),
         ]},
    ],
    "expert_tip":"Gardez toujours une <strong>gourde remplie d'eau</strong> dans la voiture si vous roulez en Australie, même en ville. Le climat déshydrate vite (chaleur, vent sec, UV puissants), et en cas de panne en Outback — même à 30 minutes d'une ville — vous devez avoir au minimum <strong>4 L d'eau par personne</strong> à bord. Les rangers des parcs nationaux recommandent 10 L/personne/jour pour les zones isolées comme l'Outback du Territoire du Nord ou du WA.",
})

# 6. Sydney Byron Bay pas cher
ARTICLES.append({
    "slug": "sydney-byron-bay-pas-cher",
    "title": "Comment Aller de Sydney à Byron Bay Pas Cher : Guide 2026 | Voyage 7 Continents",
    "og_title": "Sydney → Byron Bay Pas Cher : Bus, Train, Avion, Road Trip",
    "desc": "Bus Greyhound à partir de 55 AUD, train XPT à 80 AUD, avion low-cost à 90 AUD, road trip 2 jours : comment aller de Sydney à Byron Bay au meilleur prix.",
    "crumb": "Sydney → Byron Bay",
    "h1": "Comment Aller de Sydney à Byron Bay Pas Cher",
    "lead": "Byron Bay, à 770 km au nord de Sydney, est l'une des destinations phares de la côte est australienne. Bus, train, avion ou road trip : toutes les options pour y aller sans se ruiner.",
    "alt1": "Plage de Byron Bay au coucher du soleil avec phare et surfeurs",
    "caption1": "Byron Bay, 770 km au nord de Sydney, est l'un des spots de surf et de bien-être les plus courus d'Australie.",
    "sections": [
        {"id":"distance","toc":"Distance et options","short":"Distance","h2":"770 km : les 4 Options Possibles",
         "blocks":[
            ("p","Byron Bay se trouve à <strong>770 km au nord de Sydney</strong> par la Pacific Highway (M1/A1), soit environ <strong>9 heures de route</strong> en voiture sans pause. C'est une distance longue mais pas extrême — équivalente à un Paris-Marseille. Quatre modes de transport principaux existent, avec des prix et des temps très variables."),
            ("p","Le choix dépend de <strong>trois critères</strong> : votre budget, votre temps, et votre envie (ou pas) de voir du paysage en route. Voici les options classées du moins cher au plus cher, avec les prix indicatifs 2026 en aller simple."),
            ("img",2,"Carte schématique du trajet Sydney-Byron Bay par la Pacific Highway"),
            ("h3","Résumé express"),
            ("p","<strong>Bus Greyhound</strong> : 55-90 AUD, 13 h. <strong>Train XPT + bus</strong> : 80-110 AUD, 13 h. <strong>Avion low-cost + transfert</strong> : 90-160 AUD, 4 h. <strong>Road trip voiture de location</strong> : 180-300 AUD pour 2 personnes, 2-4 jours. Le bus reste le <strong>champion du budget solo</strong>, le road trip celui du duo motivé."),
         ]},
        {"id":"bus","toc":"Bus (le moins cher)","short":"Bus","h2":"Bus Greyhound : le Plus Économique",
         "blocks":[
            ("p","Le <strong>bus Greyhound Australia</strong> est la solution la moins chère pour relier Sydney à Byron Bay, surtout en réservant à l'avance. Les bus sont confortables (sièges inclinables, WiFi, USB, toilettes), climatisés, et il y a <strong>2-3 départs quotidiens</strong> depuis Sydney Central Station."),
            ("h3","Prix réel"),
            ("p","Aller simple : <strong>55 AUD en basse saison</strong> avec achat 2-3 semaines à l'avance, jusqu'à <strong>110 AUD</strong> en haute saison (vacances scolaires, Noël, Pâques) si acheté à la dernière minute. La promotion « Whimit Pass » permet de voyager librement pendant 7-30 jours à volonté sur tout le réseau Greyhound — intéressant si Byron Bay n'est qu'une étape d'un plus long road trip côte est."),
            ("img",3,"Bus Greyhound Australia à la gare de Sydney Central Station"),
            ("h3","Durée et horaires"),
            ("p","Environ <strong>13 heures de trajet</strong>, avec plusieurs arrêts à Newcastle, Port Macquarie, Coffs Harbour, Grafton. Le bus de nuit (départ 19h, arrivée 8h du matin) est pratique : vous économisez une nuit d'hôtel et arrivez prêt à petit-déjeuner à Byron."),
            ("h4","Autres compagnies"),
            ("p","<strong>Premier Motor Service</strong> propose une alternative similaire à des prix légèrement inférieurs en basse saison. Comparez sur <a href=\"https://www.busbud.com/\" target=\"_blank\" rel=\"noopener nofollow\">Busbud</a> ou <a href=\"https://www.rome2rio.com/\" target=\"_blank\" rel=\"noopener nofollow\">Rome2Rio</a>."),
         ]},
        {"id":"train","toc":"Train XPT","short":"Train","h2":"Train NSW TrainLink XPT + Bus",
         "blocks":[
            ("p","Il n'existe <strong>pas de train direct</strong> de Sydney à Byron Bay. La ligne ferroviaire de la North Coast s'arrête à <strong>Casino</strong>, à environ 110 km de Byron Bay, puis un bus NSW TrainLink prend le relais jusqu'à la destination finale."),
            ("h3","Comment ça marche"),
            ("p","Vous réservez un billet combiné <strong>Sydney Central → Byron Bay</strong> sur <a href=\"https://www.nswtrainlink.info/\" target=\"_blank\" rel=\"noopener nofollow\">nswtrainlink.info</a>. Le trajet combine le train XPT (départ en soirée, arrivée à Casino le lendemain matin) et un bus qui fait Casino → Byron Bay (1 h 30). Total : environ <strong>13 heures</strong>."),
            ("img",4,"Train XPT NSW TrainLink en gare australienne"),
            ("h3","Prix et confort"),
            ("p","<strong>Économie : environ 80 AUD</strong> en classe standard, <strong>110 AUD</strong> en première. Les cabines-couchettes (<em>sleeper</em>) existent sur le XPT de nuit : environ <strong>200 AUD</strong> pour un lit privatif. Plus cher mais vous dormez vraiment, et vous économisez une nuit d'hôtel."),
            ("h4","Avantages"),
            ("p","Moins de fatigue qu'en bus (espace, possibilité de se lever, plateau-repas), paysages de la côte au lever du soleil, prises électriques à chaque siège. Bon compromis pour les voyageurs moins pressés."),
         ]},
        {"id":"avion","toc":"Avion","short":"Avion","h2":"Avion Low-Cost : le Plus Rapide",
         "blocks":[
            ("p","Byron Bay n'a <strong>pas d'aéroport</strong>. Les vols atterrissent à <strong>Ballina-Byron Gateway Airport (BNK)</strong>, à 25 km au sud, ou à <strong>Gold Coast (OOL)</strong>, à 100 km au nord. Plusieurs compagnies desservent ces deux aéroports depuis Sydney (SYD)."),
            ("h3","Vers Ballina (BNK)"),
            ("p","<strong>Jetstar, Virgin Australia, Rex Airlines</strong> proposent des vols directs Sydney-Ballina. Prix : <strong>90-180 AUD</strong> aller simple en basse saison, <strong>200-300 AUD</strong> en haute saison. Durée : 1 h 15. Transfert Ballina-Byron Bay : <strong>30 AUD</strong> en navette (Byron Easy Bus), <strong>80-100 AUD</strong> en Uber/taxi."),
            ("h3","Vers Gold Coast (OOL)"),
            ("p","Option souvent plus chère sur la navette (100 km vs 25 km) mais plus de fréquences de vol, parfois moins cher avec Jetstar. Compter <strong>1 h 30</strong> en navette de Gold Coast à Byron Bay."),
            ("img",5,"Aéroport de Ballina Byron Gateway avec avion Jetstar sur le tarmac"),
            ("h3","Pour qui ?"),
            ("p","L'avion est pertinent si vous avez <strong>peu de temps</strong> (week-end depuis Sydney) ou si vous trouvez une promo < 100 AUD. Pour un backpacker avec 3 mois sur place, le bus reste imbattable."),
         ]},
        {"id":"road-trip","toc":"Road trip voiture","short":"Road trip","h2":"Road Trip en Voiture de Location",
         "blocks":[
            ("p","Le road trip est <strong>le plus agréable mais pas le moins cher</strong>, sauf à plusieurs. Il permet de s'arrêter à Newcastle, Port Macquarie (visite du refuge des koalas), Coffs Harbour, les Blue Mountains en détour, et de choisir ses propres plages. Le paysage entre Port Macquarie et Byron Bay est l'un des plus beaux d'Australie."),
            ("h3","Coût réel"),
            ("p","Location voiture économique (Hyundai i30) : <strong>50-80 AUD/jour</strong>. Carburant : <strong>120-150 AUD</strong> aller simple. Péages : environ <strong>15 AUD</strong> sur la M1. <strong>Total pour 2 jours à 2 personnes : 250-350 AUD</strong>, soit 125-175 AUD/personne — comparable à l'avion mais bien plus riche en expériences."),
            ("img",6,"Road trip en voiture sur la Pacific Highway avec océan à droite"),
            ("h3","Location one-way"),
            ("p","Vous pouvez rendre le véhicule à Byron Bay ou à Brisbane (le plus courant). Les frais <strong>« one-way fee »</strong> sont importants (100-250 AUD) — négociez ou optez pour Jucy/Hippie qui pratiquent des relocations gratuites si vous êtes flexible sur les dates."),
            ("box","Si vous êtes <strong>seul(e)</strong>, le <strong>bus Greyhound</strong> ou le train reste imbattable. Si vous êtes <strong>à 2+</strong>, le road trip redevient compétitif et offre une expérience incomparable — possibilité de s'arrêter dormir à Port Macquarie ou Coffs Harbour pour couper le trajet."),
         ]},
    ],
    "expert_tip":"Pour vraiment économiser, <strong>réservez votre bus ou avion 3-4 semaines à l'avance</strong> — les prix doublent dans les 7 jours avant le départ. Et évitez les week-ends de festivals à Byron Bay (Splendour in the Grass fin juillet, Falls Festival début janvier) : non seulement les transports explosent, mais les auberges aussi. Si vous êtes flexible, partez en milieu de semaine (mardi-mercredi) : le Greyhound est souvent à 55-65 AUD sur ces créneaux.",
})

# 7. Budget Samoa 1 semaine
ARTICLES.append({
    "slug": "budget-samoa-1-semaine",
    "title": "Budget Voyage Samoa 1 Semaine : 800 à 2 500 € en 2026 | Voyage 7 Continents",
    "og_title": "Budget Samoa 1 Semaine 2026 : 800 à 2 500 € par Personne",
    "desc": "Vol Paris-Apia, hébergement, nourriture, transport, activités : le budget détaillé pour 1 semaine aux Samoa, de 800 € en backpacker à 2 500 € en confort.",
    "crumb": "Budget Samoa",
    "h1": "Budget Voyage Samoa 1 Semaine",
    "lead": "Vol, hébergement, nourriture, transports, activités : combien coûte une semaine aux Samoa en 2026 ? Le budget détaillé, de 800 € en mode backpacker à 2 500 € en confort.",
    "alt1": "Plage de sable blanc et palmiers à Lalomanu sur l'île d'Upolu aux Samoa",
    "caption1": "Lalomanu, sur la côte sud d'Upolu, est l'une des plus belles plages des Samoa et l'un des spots les plus abordables.",
    "sections": [
        {"id":"vol","toc":"Vol international","short":"Vol","h2":"Vol Paris-Apia : le Poste Principal",
         "blocks":[
            ("p","Le <strong>vol international</strong> est et restera le poste de dépense numéro 1 d'un voyage aux Samoa depuis la France. Aucune compagnie ne propose de vol direct : toutes les connexions passent par l'Asie, l'Océanie, voire les USA."),
            ("h3","Itinéraires classiques"),
            ("p","<strong>Via Auckland (Nouvelle-Zélande)</strong> avec Air New Zealand : le plus courant et souvent le plus rapide. Escale à Auckland, puis vol de 4 h vers Apia. Prix : <strong>1 200-1 800 €</strong> aller-retour en classe économique, parfois 2 000-2 200 € en haute saison (juillet-août, Noël)."),
            ("p","<strong>Via Sydney</strong> : avec Qantas, Virgin Australia ou Fiji Airways en correspondance. Prix souvent similaire à Auckland. <strong>Via Los Angeles</strong> avec Fiji Airways puis vol Nadi-Apia : possible, plus long (35-40 h de voyage total), rarement moins cher."),
            ("img",2,"Avion Air New Zealand sur le tarmac de Faleolo International Airport Apia"),
            ("h3","Pour économiser"),
            ("p","Surveillez <a href=\"https://www.skyscanner.fr/\" target=\"_blank\" rel=\"noopener nofollow\">Skyscanner</a> sur 3-6 mois, soyez flexible sur les dates (mars, avril, mai, octobre, novembre sont les meilleures fenêtres), et envisagez de faire escale <strong>plusieurs jours à Auckland</strong> — le stopover est gratuit et permet de découvrir la Nouvelle-Zélande en bonus."),
         ]},
        {"id":"hebergement","toc":"Hébergement","short":"Hébergement","h2":"Hébergement : 3 Gammes de Prix",
         "blocks":[
            ("p","Les Samoa ont une offre d'hébergement étonnamment variée, des <strong>fale de plage</strong> (huttes traditionnelles ouvertes) aux <strong>resorts haut de gamme</strong>. Voici les 3 gammes principales, en prix par nuit pour 2 personnes en basse-moyenne saison."),
            ("h3","Backpacker / fale de plage (30-60 €)"),
            ("p","Les <strong>fale</strong> sont des huttes traditionnelles samoanes construites à même la plage : toit de feuilles, murs ouverts fermés par des nattes tressées, matelas au sol, moustiquaire. Chez l'habitant ou dans des petites adresses familiales (Taufua Beach Fale, Lalomanu Beach, Manase sur Savai'i), compter <strong>60-90 WST (20-30 €)</strong> par personne et par nuit, souvent <strong>avec petit-déjeuner et dîner inclus</strong> (« fale package »). L'expérience la plus authentique et de loin la moins chère."),
            ("img",3,"Fale samoan traditionnel sur la plage à Lalomanu au coucher du soleil"),
            ("h3","Milieu de gamme (80-150 €)"),
            ("p","<strong>Hôtels 3 étoiles et guesthouses</strong> à Apia et dans les zones touristiques d'Upolu. Chambres avec salle de bain privative, climatisation, WiFi, petit-déjeuner souvent inclus. Adresses populaires : Taumeasina Island Resort (Apia), Saletoga Sands, Salamina Beach Villas."),
            ("h3","Resort haut de gamme (200-500 €)"),
            ("p","<strong>Sheraton Samoa Aggie Grey's</strong>, <strong>Return to Paradise Resort</strong>, <strong>Seabreeze Resort</strong> : piscine, spa, plongée, restaurant gastronomique, tout-compris possible. Plus cher mais service impeccable et vrai repos garanti."),
         ]},
        {"id":"nourriture-transport","toc":"Nourriture et transport","short":"Manger","h2":"Nourriture et Transport sur Place",
         "blocks":[
            ("p","La vie quotidienne aux Samoa est <strong>abordable</strong> dès qu'on sort des resorts. Un budget nourriture + transport de <strong>15-25 € par jour</strong> couvre largement un voyageur en mode authentique."),
            ("h3","Nourriture"),
            ("p","<strong>Repas dans un marché local</strong> (Maketi Fou à Apia) : 5-8 WST (2-3 €) pour une assiette de taro, poulet et légumes. <strong>Restaurant simple en ville</strong> : 15-25 WST (5-8 €) pour un plat complet. <strong>Restaurant touristique face à la plage</strong> : 40-70 WST (15-25 €) par personne. <strong>Bière locale Vailima</strong> : 6-8 WST (2-3 €) en épicerie, 10-15 WST (3,50-5 €) en bar."),
            ("img",4,"Assiette de spécialités samoanes au marché Maketi Fou à Apia"),
            ("h3","Transport interne"),
            ("p","<strong>Bus local</strong> colorés (« aiga buses ») : 2-5 WST (0,70-1,70 €) la course, le moyen le plus authentique mais parfois imprévisible. <strong>Taxis</strong> à Apia : 5-15 WST (1,70-5 €) pour un trajet en ville. <strong>Location de voiture</strong> : 60-100 WST/jour (20-35 €), essentiel si vous voulez explorer librement Upolu. <strong>Ferry Upolu-Savai'i</strong> : environ 15 WST/personne (5 €) pour 1 h 30 de traversée."),
         ]},
        {"id":"activites-total","toc":"Activités et total","short":"Total","h2":"Activités et Budget Total",
         "blocks":[
            ("p","Les grandes activités samoanes ne coûtent pas cher et beaucoup sont gratuites. Voici les prix des incontournables et le calcul du budget total."),
            ("h3","Activités populaires"),
            ("p","<strong>To Sua Ocean Trench</strong> (piscine naturelle spectaculaire à Upolu) : 20 WST (7 €) l'entrée. <strong>Piula Cave Pool</strong> : 5 WST (1,70 €). <strong>Plongée bouteille à Savai'i</strong> : 100-150 WST (35-50 €) par plongée. <strong>Kayak, paddle, snorkeling</strong> : souvent inclus ou 20-40 WST en location. <strong>Plages publiques</strong> : gratuit ou 5-10 WST de « frais d'entretien » à l'entrée."),
            ("img",5,"Piscine naturelle To Sua Ocean Trench sur l'île d'Upolu aux Samoa"),
            ("h3","Budget total 1 semaine"),
            ("p","<strong>Backpacker (fale, bus, nourriture locale)</strong> : vol 1 300 € + 7 nuits fale 180 € + nourriture/transport 100 € + activités 60 € = <strong>~1 640 € par personne</strong>, ou ~800 € hors vol si vous combinez avec un plus long voyage Océanie."),
            ("p","<strong>Confort (3 étoiles, voiture louée, resto touristique)</strong> : vol 1 500 € + 7 nuits hôtel 700 € + voiture 150 € + nourriture 200 € + activités 120 € = <strong>~2 670 € par personne</strong>."),
            ("p","<strong>Haut de gamme (resort 5*)</strong> : vol 1 800 € + 7 nuits resort 2 500 € + demi-pension incluse + activités 300 € = <strong>~4 600 € par personne</strong>. Les Samoa ne sont pas Bora Bora — le haut de gamme reste modeste par rapport à la Polynésie française."),
            ("box","L'atout budget majeur des Samoa : la formule <strong>« fale package »</strong> à Lalomanu ou Manase, qui inclut hébergement + petit-déjeuner + dîner pour environ 90 WST (30 €) par personne et par nuit. Avec ça, votre budget sur place chute à 20 € par jour, vol compris."),
         ]},
    ],
    "expert_tip":"Combinez les Samoa avec un <strong>stopover en Nouvelle-Zélande</strong> : c'est le chemin obligatoire et Air New Zealand permet un arrêt gratuit à Auckland sur le même billet. Vous pouvez ainsi faire 5 jours d'Auckland + 7 jours des Samoa pour un prix à peine supérieur. Et ne sous-estimez pas <strong>Savai'i</strong>, la grande île : beaucoup moins touristique qu'Upolu, avec les fale les moins chers et les paysages volcaniques les plus impressionnants du pays.",
})

# 8. Spécialités Nouvelle-Calédonie
ARTICLES.append({
    "slug": "specialites-nouvelle-caledonie",
    "title": "Spécialités Culinaires de Nouvelle-Calédonie : Bougna, Crabe | Voyage 7 Continents",
    "og_title": "Spécialités Culinaires Nouvelle-Calédonie : Le Guide 2026",
    "desc": "Bougna kanak, crabe de palétuvier, cerf de brousse, poisson cru au citron, civet de roussette : les spécialités culinaires de Nouvelle-Calédonie à goûter absolument.",
    "crumb": "Spécialités Nouvelle-Calédonie",
    "h1": "Spécialités Culinaires de Nouvelle-Calédonie",
    "lead": "Entre traditions kanak et influences françaises, asiatiques et polynésiennes, la cuisine calédonienne est une mosaïque unique dans le Pacifique Sud. Les 10 spécialités à goûter absolument.",
    "alt1": "Plat de bougna traditionnel kanak cuit sur pierres chaudes dans des feuilles de bananier",
    "caption1": "Le bougna, plat kanak traditionnel cuit sur pierres chaudes, est l'incontournable de la cuisine calédonienne.",
    "sections": [
        {"id":"bougna","toc":"Le bougna kanak","short":"Bougna","h2":"Le Bougna, Plat Emblème Kanak",
         "blocks":[
            ("p","Le <strong>bougna</strong> est le plat traditionnel kanak par excellence, servi lors des fêtes coutumières, des mariages, des naissances. C'est aussi le plus représentatif de l'identité mélanésienne de la Nouvelle-Calédonie — à goûter obligatoirement lors d'un séjour sur la Grande Terre ou dans les îles Loyauté."),
            ("h3","Ingrédients et préparation"),
            ("p","Le bougna combine <strong>tubercules</strong> (igname, taro, patate douce, manioc), <strong>bananes plantain</strong>, <strong>lait de coco</strong> et <strong>viande ou poisson</strong> (poulet, roussette — une grande chauve-souris comestible —, langouste, crabe, ou poisson de lagon). Tout est enveloppé dans des <strong>feuilles de bananier</strong> soigneusement liées, puis déposé dans un <strong>four traditionnel</strong>."),
            ("p","Le <strong>four kanak</strong> est creusé dans le sol, tapissé de pierres chauffées au feu pendant plusieurs heures. Les paquets de bougna sont posés sur les pierres brûlantes, recouverts de sable ou de terre, et cuisent lentement à l'étouffée pendant <strong>2 à 3 heures</strong>. Le résultat : une cuisson fondante, parfumée, aux arômes de coco et de feuilles de bananier."),
            ("img",2,"Bougna en préparation sur pierres chaudes dans un four traditionnel kanak"),
            ("h4","Où le goûter"),
            ("p","Dans les <strong>accueils en tribu</strong> (île des Pins, Maré, Lifou, Ouvéa, Hienghène), certains restaurants de Nouméa (Le Faré, Le Roof), ou commandé 24 h à l'avance chez des particuliers qui en vendent (demandez à votre hébergement)."),
         ]},
        {"id":"crabe-mer","toc":"Crabe et fruits de mer","short":"Crabe","h2":"Crabe de Palétuvier et Fruits de Mer",
         "blocks":[
            ("p","Les eaux calédoniennes sont parmi les plus poissonneuses du Pacifique, et le <strong>lagon de Nouvelle-Calédonie</strong>, classé à l'UNESCO, nourrit une cuisine de la mer exceptionnelle. Deux spécialités dominent."),
            ("h3","Crabe de palétuvier"),
            ("p","Le <strong>crabe de palétuvier</strong> (<em>Scylla serrata</em>) vit dans la mangrove, se nourrit des racines aériennes des palétuviers. Il peut peser jusqu'à 2 kg. Sa chair est <strong>dense, sucrée, parfumée</strong>, et se prête à toutes les préparations : farci au lait de coco, grillé, en curry, en bisque."),
            ("p","Les meilleures adresses à Nouméa : <strong>Les 3 Brasseurs, Le Faré du Palm Beach</strong>, et les petits restos de l'anse Vata. Compter 30-50 € pour un crabe entier en sauce coco."),
            ("img",3,"Crabe de palétuvier farci au lait de coco sur une assiette calédonienne"),
            ("h3","Poisson cru au citron (style tahitien)"),
            ("p","Le <strong>poisson cru au lait de coco et citron vert</strong> est partagé avec la Polynésie. En Nouvelle-Calédonie, on le fait à partir de <strong>thon rouge, bonite, mahi-mahi</strong>, coupé en dés, mariné 10 minutes dans le jus de citron vert (qui « cuit » chimiquement le poisson), puis mélangé à du lait de coco frais, concombre, oignons rouges, tomates. Frais, léger, idéal après une plongée."),
            ("h3","Langoustes et bénitiers"),
            ("p","Les <strong>langoustes de roche</strong> (pêchées en plongée sur la barrière de corail) sont servies grillées simplement au beurre persillé. Les <strong>bénitiers</strong> (gros coquillages du lagon) se mangent crus en sashimi ou en tartare — texture ferme et iodée."),
         ]},
        {"id":"cerf-brousse","toc":"Cerf de brousse","short":"Cerf","h2":"Le Cerf de Brousse, Viande Calédonienne",
         "blocks":[
            ("p","Particularité étonnante : la Nouvelle-Calédonie est l'un des rares endroits au monde où la <strong>viande de cerf est un plat courant et populaire</strong>. L'explication est historique — les cerfs rusa ont été introduits au XIXe siècle et se sont reproduits sans prédateurs, au point de devenir envahissants. Leur chasse est aujourd'hui encouragée."),
            ("h3","Caractéristiques"),
            ("p","La viande de cerf calédonien est <strong>maigre, ferme, au goût légèrement sauvage</strong> mais moins prononcé que le cerf européen. Elle se prépare en <strong>civet, sauté, brochettes, pavé rôti</strong>. C'est l'équivalent local du bœuf en brasserie — disponible dans presque tous les restaurants de Nouméa."),
            ("img",4,"Pavé de cerf de brousse rôti avec sauce au vin et légumes"),
            ("h3","À goûter"),
            ("p","<strong>Le civet de cerf au vin rouge</strong> (plat d'influence française dans un contexte pacifique), <strong>les brochettes de cerf</strong> grillées aux herbes, <strong>le cerf à la tahitienne</strong> (émincé avec gingembre, lait de coco, citron vert). Comptez 25-35 € pour un plat principal en restaurant."),
            ("h4","Chasse encadrée"),
            ("p","La chasse au cerf est <strong>réglementée</strong> (permis obligatoire, quotas) et pratiquée par de nombreux agriculteurs locaux qui revendent la viande en circuit court à des restaurants et boucheries — la traçabilité est excellente."),
         ]},
        {"id":"autres-desserts","toc":"Autres plats et desserts","short":"Desserts","h2":"Roussette, Roots, Desserts",
         "blocks":[
            ("p","La cuisine calédonienne ne s'arrête pas là. Voici quelques autres spécialités moins connues mais tout aussi emblématiques."),
            ("h3","Civet de roussette"),
            ("p","La <strong>roussette</strong> est une grande chauve-souris frugivore, mangée par les Kanaks de longue date. Le <strong>civet de roussette</strong>, mijoté au vin rouge et aux herbes, a un goût <strong>proche du gibier</strong>, un peu fumé. Plat rare, proposé dans certains restaurants tribaux. À tenter pour l'expérience."),
            ("h3","Ignames, taros, bananes plantain"),
            ("p","Les <strong>ignames</strong> sont sacrées dans la culture kanak — elles symbolisent le clan, la vie, le don. Elles accompagnent quasiment tous les plats traditionnels sous forme bouillie, grillée ou en purée. Le <strong>taro</strong>, plus doux, et la <strong>banane plantain</strong> frite ou cuite au lait de coco complètent la base féculente."),
            ("img",5,"Assortiment d'ignames, taros et bananes plantain sur un marché de Nouméa"),
            ("h3","Desserts"),
            ("p","<strong>Flan coco</strong>, <strong>tarte à la papaye</strong>, <strong>banane flambée</strong>, <strong>pomme-cannelle au sirop</strong> : les desserts combinent fruits tropicaux et techniques françaises. Le <strong>lélé</strong>, dessert traditionnel kanak à base de banane mûre, tapioca et lait de coco, est le plus typique."),
            ("h4","Boissons"),
            ("p","<strong>Bière Number One</strong> (brassée localement depuis 1975, la Numero Uno est la bière nationale), <strong>café de Sarraméa</strong> (petite production locale, tassé et fruité), <strong>jus de fruits frais</strong> (mangue, corossol, ananas, passion)."),
         ]},
    ],
    "expert_tip":"Ne partez pas sans avoir fait <strong>au moins un repas en tribu</strong> — c'est le vrai cœur de la gastronomie calédonienne. Beaucoup d'accueils en tribu (île des Pins, île Ouen, Hienghène) proposent un <strong>« menu coutumier »</strong> qui inclut obligatoirement le bougna, servi dans une grande case traditionnelle avec explications sur les ingrédients et la cuisson. Comptez 35-50 € par personne, souvent avec hébergement possible sur place — une expérience humaine autant que gastronomique.",
})

# 9. Îles Salomon danger
ARTICLES.append({
    "slug": "danger-iles-salomon",
    "title": "Est-ce Dangereux de Voyager aux Îles Salomon en 2026 ? | Voyage 7 Continents",
    "og_title": "Danger Îles Salomon 2026 : Ce que Disent les Ambassades",
    "desc": "Les îles Salomon sont classées vigilance renforcée par la France : troubles politiques, criminalité à Honiara, catastrophes naturelles. Conseils officiels pour voyageurs.",
    "crumb": "Danger Salomon",
    "h1": "Est-ce Dangereux de Voyager aux Îles Salomon ?",
    "lead": "Les îles Salomon sont globalement sûres en zones rurales mais classées « vigilance renforcée » par France Diplomatie à cause de troubles politiques à Honiara et de risques naturels. Le point complet 2026.",
    "alt1": "Vue aérienne d'une île tropicale des Salomon avec lagon turquoise",
    "caption1": "Les îles Salomon, archipel de 900 îles au cœur du Pacifique Sud, restent peu visitées malgré leurs paysages spectaculaires.",
    "sections": [
        {"id":"niveau-risque","toc":"Niveau de risque","short":"Risque","h2":"Niveau de Risque Officiel",
         "blocks":[
            ("p","Selon <a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/iles-salomon/\" target=\"_blank\" rel=\"noopener nofollow\">France Diplomatie</a>, les îles Salomon sont classées en <strong>« vigilance renforcée »</strong> (niveau 2 sur 4) dans l'ensemble, avec certaines zones en <strong>« déconseillé sauf raison impérative »</strong> (niveau 3). Les autorités britanniques (FCDO) et australiennes (Smartraveller) font des recommandations similaires."),
            ("p","Cela ne signifie <strong>pas</strong> que le pays est dangereux en soi — de nombreux voyageurs y vont sans incident. Mais il existe plusieurs catégories de risques spécifiques à connaître : <strong>troubles politiques</strong>, <strong>criminalité urbaine</strong>, <strong>catastrophes naturelles</strong>, <strong>accès aux soins limité</strong>."),
            ("img",2,"Ambassade de France à Canberra qui gère les Salomon"),
            ("h3","Représentation française"),
            ("p","Il n'y a <strong>pas d'ambassade de France aux îles Salomon</strong>. Les ressortissants français dépendent de l'ambassade de France en Australie (Canberra). En cas de problème grave, s'adresser à l'Ambassade d'Australie à Honiara peut aussi aider (accord de coopération consulaire)."),
         ]},
        {"id":"honiara","toc":"Honiara : attention","short":"Honiara","h2":"Honiara : la Capitale à Risque",
         "blocks":[
            ("p","La <strong>capitale Honiara</strong> sur l'île de Guadalcanal concentre presque tous les problèmes de sécurité du pays. Des <strong>émeutes ont eu lieu en 2019 puis en 2021</strong>, avec destructions d'infrastructures dans le quartier chinois, blocages de la ville, vols à main armée. La situation s'est calmée mais reste tendue politiquement."),
            ("h3","Criminalité à Honiara"),
            ("p","<strong>Vols de sacs, cambriolages d'hôtels, agressions</strong> sont signalés, surtout le soir et dans les quartiers périphériques. Les vols de véhicules et les détournements de 4x4 ont lieu occasionnellement. Les zones à éviter : Chinatown le soir, Kukum, certains quartiers résidentiels isolés."),
            ("img",3,"Rue commerçante de Honiara avec boutiques et voitures de 4x4"),
            ("h3","Recommandations"),
            ("p","<strong>Ne pas marcher seul(e) la nuit</strong>, notamment en dehors des hôtels. <strong>Éviter de porter bijoux et montres voyantes</strong>. <strong>Utiliser uniquement des taxis recommandés par l'hôtel</strong> (pas de taxis de rue la nuit). <strong>Limiter le temps à Honiara</strong> : beaucoup de voyageurs ne font qu'y dormir 1-2 nuits avant de rejoindre les îles provinciales en avion."),
            ("h4","Déplacements inter-îles"),
            ("p","Les <strong>vols intérieurs Solomon Airlines</strong> desservent Munda, Gizo, Santa Cruz, Choiseul. Ils sont fiables mais les horaires sont souvent modifiés. Prévoyez 1 jour de marge entre le retour sur Honiara et le vol international. Les ferries inter-îles existent mais sont <strong>peu sûrs</strong> — la France déconseille formellement les bateaux locaux non agréés (risques de naufrage)."),
         ]},
        {"id":"iles-rurales","toc":"Îles rurales","short":"Provinces","h2":"Îles Provinciales : le Vrai Visage",
         "blocks":[
            ("p","Bonne nouvelle : <strong>en dehors de Honiara, les Salomon sont majoritairement calmes et accueillantes</strong>. Les petites îles du Western Province (Munda, Gizo, Marovo Lagoon), le Temotu, Malaita rurale, offrent des paysages spectaculaires et un accueil chaleureux dans des villages traditionnels."),
            ("h3","Western Province"),
            ("p","La plus touristique et la plus sûre. <strong>Munda</strong> est la base pour la plongée sur les épaves de la Seconde Guerre mondiale (bataille de Guadalcanal 1942-1943). <strong>Gizo</strong> est un charmant petit port avec plusieurs dive lodges. <strong>Marovo Lagoon</strong>, le plus grand lagon à double barrière au monde, est un site classé pour la plongée et le kayak."),
            ("img",4,"Marovo Lagoon aux îles Salomon avec kayak et îlots émergeant"),
            ("h3","Contexte culturel"),
            ("p","Les <strong>coutumes de palabre</strong> et le respect des anciens sont très importants. Arrivez toujours dans un village avec un petit geste de respect (un souvenir, une photo offerte, une participation à l'achat de carburant pour la pirogue) si vous n'êtes pas avec un guide agréé. Jamais de photos sans autorisation."),
            ("h3","Zones à éviter"),
            ("p","Certaines parties de <strong>Malaita</strong> (conflits fonciers tribaux), les îles isolées sans tourisme établi, et toute zone où vous ne pourriez pas justifier votre présence. Passez par un tour operator agréé pour les excursions hors des sentiers battus."),
         ]},
        {"id":"risques-naturels","toc":"Risques naturels","short":"Nature","h2":"Risques Naturels et Sanitaires",
         "blocks":[
            ("p","Les îles Salomon sont situées sur la <strong>ceinture de feu du Pacifique</strong> : séismes, tsunamis, éruptions volcaniques et cyclones sont des risques réels et réguliers."),
            ("h3","Séismes et tsunamis"),
            ("p","Les Salomon ont connu plusieurs <strong>séismes majeurs</strong> ces 20 dernières années, dont celui de 2007 (magnitude 8.1) qui a causé un tsunami destructeur à Gizo. Avant de partir en trek ou en camping sauvage, renseignez-vous sur les itinéraires d'évacuation en cas d'alerte."),
            ("img",5,"Panneau d'alerte tsunami sur une plage des îles Salomon"),
            ("h3","Cyclones"),
            ("p","La saison cyclonique va de <strong>novembre à avril</strong>. La meilleure période pour voyager est donc <strong>mai à octobre</strong> (saison sèche). En dehors, les vols peuvent être annulés sans préavis, les ferries suspendus, certaines zones inaccessibles."),
            ("h3","Santé"),
            ("p","Le <strong>paludisme</strong> est présent sur toutes les îles : prophylaxie obligatoire. La <strong>dengue</strong> et le <strong>chikungunya</strong> circulent. L'<strong>accès aux soins est très limité</strong> : l'hôpital national de Honiara est l'unique structure avec des moyens corrects, et les évacuations sanitaires vers Brisbane coûtent <strong>50 000 à 150 000 €</strong>. Une assurance rapatriement est <strong>obligatoire</strong>."),
            ("box","N'envisagez les Salomon qu'avec une <strong>assurance voyage solide</strong> incluant évacuation sanitaire, recherche et sauvetage, et annulation. Et gardez toujours votre ambassade (Canberra pour la France) et votre assureur dans votre téléphone avant de partir en zone isolée."),
         ]},
    ],
    "expert_tip":"Privilégiez un <strong>circuit organisé avec un opérateur local agréé</strong> (Solomon Islands Tourism, Dive Munda, Wilderness Lodge) plutôt que du voyage totalement autonome, surtout pour un premier séjour. Vous bénéficiez de leur connaissance des zones sûres, de leurs contacts coutumiers avec les villages, et d'un plan B en cas de problème. Et <strong>limitez au maximum votre temps à Honiara</strong> : 1 nuit à l'arrivée, 1 nuit au retour, c'est largement suffisant. Le vrai charme des Salomon est dans les îles périphériques.",
})

# 10. Voltage Nouvelle-Zélande
ARTICLES.append({
    "slug": "voltage-prise-nouvelle-zelande",
    "title": "Voltage et Prise Électrique en Nouvelle-Zélande : Guide 2026 | Voyage 7 Continents",
    "og_title": "Voltage Nouvelle-Zélande : 230 V / Type I — Adaptateur Obligatoire",
    "desc": "La Nouvelle-Zélande utilise du 230 V / 50 Hz et des prises de type I (3 broches plates). Un adaptateur est obligatoire pour les appareils français. Guide pratique.",
    "crumb": "Voltage Nouvelle-Zélande",
    "h1": "Voltage et Prise Électrique en Nouvelle-Zélande",
    "lead": "230 V / 50 Hz, prises de type I à 3 broches plates obliques : la Nouvelle-Zélande impose un adaptateur obligatoire pour tous les appareils français. Le guide complet 2026.",
    "alt1": "Prise électrique de type I néo-zélandaise avec 3 broches plates",
    "caption1": "La prise néo-zélandaise de type I, identique à celle de l'Australie, demande un adaptateur spécifique.",
    "sections": [
        {"id":"voltage","toc":"Voltage et fréquence","short":"Voltage","h2":"Voltage : 230 V, 50 Hz",
         "blocks":[
            ("p","La Nouvelle-Zélande utilise un réseau électrique domestique à <strong>230 volts et 50 hertz</strong>, exactement comme la France et le reste de l'Europe continentale. Cela signifie que <strong>le voltage n'est pas un problème</strong> pour les appareils français : pas besoin de transformateur électrique ni de régulateur de tension."),
            ("p","Les appareils modernes (smartphones, ordinateurs portables, appareils photo, rasoirs, brosses à dents électriques) sont <strong>presque tous multi-voltage</strong> — leurs chargeurs acceptent 100-240 V. Vérifiez simplement l'étiquette du chargeur : si vous voyez <strong>« 100-240 V ~ 50/60 Hz »</strong>, vous n'avez besoin <strong>que d'un adaptateur de prise</strong>, pas d'un transformateur."),
            ("img",2,"Étiquette d'un chargeur d'ordinateur portable indiquant 100-240V"),
            ("h3","Cas particuliers"),
            ("p","Certains <strong>sèche-cheveux, bouilloires, fers à lisser</strong> de fabrication européenne ne sont prévus que pour 230 V. Ils fonctionneront parfaitement en Nouvelle-Zélande sans modification. En revanche, les appareils américains ou japonais prévus pour 110-120 V auront besoin d'un transformateur 110→230 V — peu probable si vous venez de France."),
         ]},
        {"id":"prises","toc":"Type de prise","short":"Prise","h2":"Prise de Type I : 3 Broches Plates Obliques",
         "blocks":[
            ("p","Le point qui demande un adaptateur : la forme des prises. La Nouvelle-Zélande utilise la <strong>prise de type I</strong> (norme AS/NZS 3112), identique à celle utilisée en Australie, en Chine et dans plusieurs pays du Pacifique. Elle comporte <strong>trois broches plates disposées en V inversé</strong> : deux broches de phase et neutre obliques en haut, et une broche de terre verticale en bas."),
            ("p","Cette prise est <strong>totalement incompatible</strong> avec la prise française de type E (ronde à 2 broches + trou de terre). Vous <strong>ne pouvez pas</strong> brancher directement un chargeur français sur une prise néo-zélandaise — il faut impérativement un adaptateur physique."),
            ("img",3,"Adaptateur de voyage France vers Nouvelle-Zélande type I"),
            ("h3","Acheter un adaptateur"),
            ("p","Un adaptateur <strong>« France vers Australie/Nouvelle-Zélande »</strong> coûte <strong>5 à 15 €</strong> en France (Fnac, Darty, Decathlon, Amazon). Achetez-le <strong>avant de partir</strong> : à l'aéroport d'arrivée (Auckland, Christchurch), il coûte 25-40 NZD (15-25 €) pour la même chose."),
            ("h4","Adaptateur universel"),
            ("p","Si vous voyagez souvent, investissez dans un <strong>adaptateur universel multi-pays</strong> (15-30 €) qui couvre Australie/NZ, USA, Royaume-Uni, Europe. Certains modèles intègrent aussi <strong>2 ports USB</strong>, très pratiques pour charger plusieurs appareils d'un coup."),
         ]},
        {"id":"multiprise","toc":"Multiprise française","short":"Multiprise","h2":"Astuce : la Multiprise Française",
         "blocks":[
            ("p","Voici l'astuce que tous les voyageurs expérimentés utilisent : plutôt que de prendre plusieurs adaptateurs, emportez <strong>un seul adaptateur France → Nouvelle-Zélande + une multiprise française</strong>. Vous pouvez ainsi brancher <strong>4-6 appareils français</strong> en même temps avec un seul adaptateur."),
            ("h3","Comment ça marche"),
            ("p","L'adaptateur (type I mâle vers type E femelle) reçoit la prise mâle française de votre multiprise. Ensuite, vous branchez vos appareils français normalement dans la multiprise. Ça fonctionne parfaitement tant que le voltage est correct — ce qui est le cas de la Nouvelle-Zélande (230 V)."),
            ("img",4,"Multiprise française branchée sur un adaptateur type I en Nouvelle-Zélande"),
            ("h3","Avantages"),
            ("p","<strong>Économique</strong> : 1 seul adaptateur pour toute la famille. <strong>Pratique</strong> : vous chargez téléphone, ordinateur, appareil photo et batterie de vélo électrique simultanément. <strong>Compact</strong> : prend moins de place dans la valise que 4 adaptateurs séparés."),
            ("h4","Attention à la puissance totale"),
            ("p","Respectez la <strong>puissance maximale</strong> de la multiprise (souvent 3 500 W, indiqué sur l'étiquette). Branchez bien smartphones, ordinateurs et petits appareils, mais évitez de cumuler un sèche-cheveux + fer à lisser + bouilloire sur la même multiprise — vous risquez de déclencher les protections."),
         ]},
        {"id":"camping-car","toc":"Camping-car et 12V","short":"12V","h2":"Camping-Car, Van et 12V",
         "blocks":[
            ("p","Si vous louez un <strong>camping-car ou un van</strong> en Nouvelle-Zélande (Jucy, Britz, Maui, Wicked), vous aurez souvent accès à <strong>deux sources d'électricité</strong> : le 12 V (allume-cigare) en roulant, et le 230 V (prises type I) sur les emplacements de camping avec prise (powered sites)."),
            ("h3","Le 12 V"),
            ("p","L'allume-cigare (douille 12 V) est pratique pour charger un <strong>téléphone, GPS, tablette</strong>. Prévoyez un <strong>chargeur double USB 12V</strong> pour brancher 2 appareils en roulant. Évitez d'y brancher un ordinateur portable ou un gros appareil — pas assez de puissance."),
            ("img",5,"Camping-car sur un emplacement avec prise électrique en Nouvelle-Zélande"),
            ("h3","Le 230 V en camping"),
            ("p","Dans les <strong>campings néo-zélandais équipés « powered sites »</strong> (supplément 5-10 NZD/nuit), vous pouvez brancher le camping-car sur l'électricité du secteur — prise extérieure souvent de type industriel (bleue CEE 17), adaptée par le loueur. Vérifiez les câbles fournis au moment de la prise en main du véhicule."),
            ("h4","Ce qu'il faut savoir"),
            ("p","Tous les loueurs fournissent <strong>gratuitement le câble d'alimentation extérieur</strong> adapté à la NZ. Mais <strong>pas l'adaptateur intérieur français</strong> pour recharger vos appareils personnels — pensez-y avant le départ."),
         ]},
    ],
    "expert_tip":"Prenez <strong>deux adaptateurs</strong> plutôt qu'un seul, surtout en couple ou en famille : en camping-car comme à l'hôtel, les prises disponibles sont souvent éloignées les unes des autres, et vous chargerez ainsi plusieurs appareils en parallèle. Et vérifiez systématiquement le nombre de prises dans votre chambre d'hôtel/backpacker à l'arrivée : certains établissements plus anciens n'ont qu'1 ou 2 prises dans toute la pièce — la multiprise française devient alors indispensable.",
})

if __name__ == "__main__":
    for a in ARTICLES:
        content = render(a)
        path = os.path.join(OUT, f'{a["slug"]}.html')
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f'wrote {path}  {len(content)} chars')
    print(f"done: {len(ARTICLES)} articles")
