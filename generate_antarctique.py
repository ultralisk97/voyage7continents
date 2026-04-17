#!/usr/bin/env python3
"""Generate 9 Antarctica articles — same EEAT template."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "antarctique")
os.makedirs(OUT, exist_ok=True)

HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://voyage7continents.fr/antarctique/{slug}.html">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="apple-touch-icon" href="/favicon.svg">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://voyage7continents.fr/antarctique/{slug}.html">
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
    "mainEntityOfPage": "https://voyage7continents.fr/antarctique/{slug}.html",
    "description": "{desc}",
    "author": {{"@type": "Person", "name": "Claire Moreau", "url": "https://voyage7continents.fr/a-propos.html"}},
    "publisher": {{"@type": "Organization", "name": "Voyage 7 Continents", "logo": {{"@type": "ImageObject", "url": "https://voyage7continents.fr/img/logo.svg"}}}},
    "datePublished": "2026-04-14",
    "dateModified": "2026-04-14"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://voyage7continents.fr/"}},
      {{"@type": "ListItem", "position": 2, "name": "Antarctique", "item": "https://voyage7continents.fr/antarctique/"}},
      {{"@type": "ListItem", "position": 3, "name": "{crumb}", "item": "https://voyage7continents.fr/antarctique/{slug}.html"}}
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
          <li><a href="/oceanie/">Océanie</a></li>
          <li><a href="/antarctique/" class="active">Antarctique</a></li>
        </ul>
      </nav>
      <button class="menu-toggle" aria-label="Ouvrir le menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <section class="hero hero-pillar" style="background: linear-gradient(rgba(14,47,68,0.8), rgba(26,82,118,0.75)), url('/img/hero-antarctique.jpg') center/cover no-repeat;">
    <div class="hero-content">
      <div class="breadcrumb">
        <a href="/">Voyage 7 Continents</a> &rsaquo; <a href="/antarctique/">Antarctique</a> &rsaquo; <strong>{crumb}</strong>
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
        <time datetime="2026-04-14">Publié le 14 avril 2026</time>
        <time class="meta-updated" datetime="2026-04-14">Mis à jour le 14 avril 2026</time>
      </div>

      <figure class="article-hero"><img src="/img/articles/{slug}-1.jpg" alt="{alt1}" loading="lazy" width="800" height="500"><figcaption>{caption1}</figcaption></figure>

{body}

      <div class="info-box tip">
        <strong>Le conseil d'expert</strong>
        <p>{expert_tip}</p>
      </div>

      <p>Pour préparer votre expédition, retrouvez notre <a href="/antarctique/">guide complet Antarctique</a> et nos autres articles de la catégorie.</p>

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

# 1. Ushuaia → Antarctique
ARTICLES.append({
    "slug": "ushuaia-antarctique",
    "title": "Comment Aller en Antarctique depuis Ushuaia : Guide Complet 2026 | Voyage 7 Continents",
    "og_title": "Aller en Antarctique depuis Ushuaia : Croisières, Prix, Passage Drake",
    "desc": "Ushuaia est la porte d'entrée de l'Antarctique : 95% des croisières y partent. Compagnies, types de navires, prix, passage de Drake : tout ce qu'il faut savoir.",
    "crumb": "Ushuaia → Antarctique",
    "h1": "Comment Aller en Antarctique depuis Ushuaia",
    "lead": "95 % des croisières polaires partent d'Ushuaia, à l'extrême sud de l'Argentine. Compagnies, navires, passage de Drake, prix, embarquement : le guide complet 2026.",
    "alt1": "Port d'Ushuaia en Argentine avec navires d'expédition polaire et montagnes enneigées",
    "caption1": "Le port d'Ushuaia, point de départ de quasi toutes les croisières vers l'Antarctique.",
    "sections": [
        {"id":"ushuaia-porte","toc":"Ushuaia, porte d'entrée","short":"Ushuaia","h2":"Pourquoi Ushuaia est la Porte d'Entrée ?",
         "blocks":[
            ("p","<strong>Ushuaia</strong>, capitale de la province de Terre de Feu (Argentine), est située à seulement <strong>1 000 km de la péninsule Antarctique</strong>. C'est la ville habitée la plus australe du monde et, surtout, le port le plus proche du continent blanc, à deux jours de navigation à travers le passage de Drake."),
            ("p","Selon l'<a href=\"https://iaato.org/\" target=\"_blank\" rel=\"noopener nofollow\">IAATO (International Association of Antarctica Tour Operators)</a>, qui régule le tourisme antarctique, <strong>environ 95 % des passagers commerciaux</strong> embarquent depuis Ushuaia chaque saison australe (novembre à mars). Les alternatives (Punta Arenas, Port Stanley, Hobart, Christchurch) représentent moins de 5 % du trafic, souvent pour des expéditions scientifiques ou des croisières plus longues vers la mer de Ross."),
            ("img",2,"Carte indiquant la position d'Ushuaia face à la péninsule Antarctique"),
            ("h3","Comment rejoindre Ushuaia"),
            ("p","Depuis Paris, compter <strong>20 à 24 heures</strong> de trajet : vol long-courrier vers Buenos Aires (Ezeiza, EZE) puis vol intérieur de 3h30 vers Ushuaia (USH) avec Aerolineas Argentinas, JetSMART ou Flybondi. Prix AR total Paris-Ushuaia : <strong>900 à 1 500 €</strong> en achetant séparément."),
            ("h4","Arriver 24 à 48h avant"),
            ("p","Il est <strong>fortement recommandé</strong> d'arriver 1 à 2 jours avant l'embarquement : tout retard du vol intérieur argentin peut vous faire rater le navire, qui ne vous attendra pas. Les compagnies imposent souvent cette marge de sécurité dans leurs conditions générales."),
         ]},
        {"id":"compagnies","toc":"Compagnies et navires","short":"Compagnies","h2":"Compagnies et Types de Navires",
         "blocks":[
            ("p","Une quinzaine d'opérateurs se partagent le marché. On distingue les <strong>petits navires d'expédition</strong> (100 à 200 passagers, débarquements Zodiac inclus) des <strong>grands navires</strong> (300-500+ passagers, débarquements limités voire interdits par l'IAATO au-delà de 500 pax)."),
            ("h3","Expéditions premium (100-200 pax)"),
            ("p","<strong>Hurtigruten / HX Expeditions, Quark Expeditions, Oceanwide, Aurora Expeditions, Ponant</strong>, Silversea, Lindblad/National Geographic, Poseidon Expeditions. Meilleurs débarquements, conférences, guides naturalistes, kayak en option."),
            ("img",3,"Petit navire d'expédition polaire ancré dans une baie antarctique avec icebergs"),
            ("h3","Grands navires (300+ pax)"),
            ("p","Holland America, Princess Cruises, Oceania, Celebrity, Viking : <strong>croisières « cruise only »</strong> qui naviguent au large sans débarquer. Moins chères mais expérience très différente — pas de pied posé sur le continent."),
            ("h4","Voilier"),
            ("p","Une dizaine de voiliers privés proposent des traversées à 8-12 places maximum. Authentique et sportif, très cher (12 000-18 000 € pour 20 jours), et les conditions de Drake peuvent être éprouvantes."),
         ]},
        {"id":"drake","toc":"Le passage de Drake","short":"Drake","h2":"Le Passage de Drake : l'Épreuve",
         "blocks":[
            ("p","Le <strong>passage de Drake</strong> sépare le cap Horn de la péninsule Antarctique : environ 1 000 km de mer souvent agitée, traversés en <strong>36 à 48 heures</strong>. C'est la zone où se rencontrent les courants des trois océans, ce qui peut provoquer une houle énorme."),
            ("p","Deux scénarios selon les voyageurs : <strong>« Drake Lake »</strong> (mer calme, rare, béni) ou <strong>« Drake Shake »</strong> (creux de 4 à 8 m, fréquent en début/fin de saison). Le mal de mer touche 30 à 50 % des passagers ; les navires modernes sont équipés de stabilisateurs, ce qui réduit considérablement les effets."),
            ("img",4,"Mer agitée du passage de Drake avec creux et écume"),
            ("h3","Alternative : Fly the Drake"),
            ("p","Quelques compagnies proposent un vol charter Punta Arenas → Base Frei (Île du Roi George) en 2 heures, pour éviter entièrement le Drake. Surcoût : <strong>+3 000 à +5 000 € par personne</strong>. Option privilégiée par les seniors ou les voyageurs sensibles au mal de mer."),
            ("h4","Patch anti-mal de mer"),
            ("p","Préparez des patchs de scopolamine (prescription médicale) ou du Mercalm/Nautamine. Les médecins de bord distribuent souvent ces médicaments gratuitement les deux premiers jours."),
         ]},
        {"id":"prix","toc":"Prix et réservation","short":"Prix","h2":"Prix et Comment Réserver",
         "blocks":[
            ("p","Les tarifs de <strong>cabines Antarctique depuis Ushuaia</strong> démarrent à environ <strong>6 000-8 000 € par personne</strong> pour une cabine triple, sur un voyage de 10 jours en petit navire d'expédition. Une cabine double classique se situe entre <strong>8 500 et 14 000 €</strong>, une suite avec balcon dépasse facilement <strong>20 000 €</strong>."),
            ("h3","Last minute à Ushuaia"),
            ("p","Historiquement, on pouvait marchander des <strong>cabines invendues</strong> directement dans les agences d'Ushuaia (Rumbo Sur, Antarctica XXI, Freestyle Adventure Travel) avec <strong>30 à 50 % de réduction</strong>. Depuis 2020, les offres last minute se sont raréfiées car la demande est très forte et les compagnies vendent en ligne bien à l'avance."),
            ("img",5,"Agence de voyage à Ushuaia affichant des croisières Antarctique en vitrine"),
            ("h4","Réserver à l'avance"),
            ("p","Pour la saison 2026-2027, réservez <strong>12 à 18 mois avant le départ</strong> pour avoir le meilleur choix de dates et de cabines. Comparez via <a href=\"https://www.polarcruises.com/\" target=\"_blank\" rel=\"noopener nofollow\">polarcruises.com</a> ou directement auprès des opérateurs IAATO."),
         ]},
    ],
    "expert_tip":"Choisissez une cabine <strong>au milieu du navire, pont bas</strong> : c'est là que le roulis est le moins perceptible dans le Drake. Et privilégiez un navire de <strong>moins de 200 passagers</strong> si vous voulez vraiment débarquer et marcher sur le continent — au-delà, l'IAATO limite fortement les débarquements et vous perdez l'essentiel de l'expérience.",
})

# 2. Température décembre
ARTICLES.append({
    "slug": "temperature-antarctique-decembre",
    "title": "Température Moyenne en Antarctique en Décembre : Climat et Équipement | Voyage 7 Continents",
    "og_title": "Température en Antarctique en Décembre : -2 à +2°C sur la Péninsule",
    "desc": "Décembre est l'été austral : -2 à +2°C sur la péninsule Antarctique, -30°C à l'intérieur du continent. Guide du climat et équipement indispensable.",
    "crumb": "Température décembre",
    "h1": "Température Moyenne en Antarctique en Décembre",
    "lead": "Été austral, jour permanent, vent glacial : le vrai climat de l'Antarctique en décembre et ce qu'il faut mettre dans son sac pour une croisière d'expédition.",
    "alt1": "Manchots Papous sur la glace en Antarctique sous un ciel lumineux d'été austral",
    "caption1": "Décembre marque le plein été austral sur la péninsule Antarctique : 20 heures de jour et températures proches de 0°C.",
    "sections": [
        {"id":"temperatures","toc":"Températures par zone","short":"Températures","h2":"Températures Moyennes en Décembre",
         "blocks":[
            ("p","L'Antarctique n'est pas uniforme : la péninsule (seule zone visitée par les touristes) et l'intérieur du continent ont des climats radicalement différents. En décembre, mois du solstice d'été austral, les températures sont à leur maximum annuel — mais restent largement sous zéro à l'intérieur."),
            ("h3","Péninsule Antarctique"),
            ("p","Sur la péninsule (zones visitées par les croisières : îles Shetland du Sud, Anvers, Lemaire, Paradise Bay), les températures moyennes en décembre sont de <strong>-2°C à +2°C</strong>. Les journées ensoleillées peuvent atteindre +4°C ou +5°C ; les matins plus frais tombent à -5°C avec le vent. Ces valeurs sont cohérentes avec les relevés publiés par le <a href=\"https://www.bas.ac.uk/data/our-data/publication/weather-and-climate/\" target=\"_blank\" rel=\"noopener nofollow\">British Antarctic Survey</a>."),
            ("img",2,"Thermomètre sur un zodiac en expédition antarctique montrant une température proche de 0°C"),
            ("h3","Intérieur et pôle Sud"),
            ("p","À l'intérieur du continent, le plateau antarctique reste extrêmement froid même en été : <strong>-25 à -35°C à la station Vostok</strong>, <strong>-28°C en moyenne au pôle Sud (Amundsen-Scott)</strong>. Mais aucune croisière touristique ne s'y rend — il faudrait un vol privé opéré par ALE (Antarctic Logistics & Expeditions) pour plusieurs dizaines de milliers d'euros."),
            ("h4","Ressenti avec le vent"),
            ("p","Le facteur vent (« windchill ») change tout : avec 40 km/h de vent à 0°C réel, le ressenti tombe à <strong>-12°C</strong>. Les rafales sur la péninsule dépassent parfois 60-80 km/h, ce qui justifie un équipement grand froid complet."),
         ]},
        {"id":"ensoleillement","toc":"Ensoleillement","short":"Soleil","h2":"Ensoleillement et Durée du Jour",
         "blocks":[
            ("p","Décembre est le mois du <strong>solstice d'été austral</strong> (21 décembre) : la péninsule Antarctique bénéficie de <strong>18 à 22 heures de luminosité par jour</strong>. La « nuit » ne dépasse jamais le crépuscule bleuté — parfait pour photographier et maximiser les débarquements."),
            ("p","Le soleil reste cependant <strong>bas sur l'horizon</strong> toute la journée : il ne monte pas haut et la lumière est rasante, très chaude photographiquement mais peu puissante en chaleur. Les UV sont néanmoins très élevés à cause de la réverbération sur la glace (jusqu'à 90 %) — <strong>crème solaire indice 50 + lunettes de ski catégorie 4</strong> indispensables."),
            ("img",3,"Soleil bas sur l'horizon antarctique sur des icebergs bleutés"),
            ("h4","Soleil de minuit"),
            ("p","À partir du cercle polaire antarctique (66°33' S), le soleil ne se couche plus pendant quelques jours autour du 21 décembre. Les croisières qui descendent sous le 66ème parallèle (cercle polaire) offrent cette expérience unique."),
         ]},
        {"id":"equipement","toc":"Que mettre dans son sac","short":"Équipement","h2":"Équipement Indispensable pour Décembre",
         "blocks":[
            ("p","Contrairement aux idées reçues, vous n'avez <strong>pas besoin d'une combinaison de grand froid</strong> type -40°C. Le système « 3 couches » classique du ski de randonnée suffit largement, pourvu qu'il soit complet."),
            ("h3","Les 3 couches"),
            ("p","<strong>Couche 1 (sous-vêtement technique)</strong> : mérinos ou synthétique. <strong>Couche 2 (isolation)</strong> : polaire épaisse 300g/m² ou doudoune duvet légère. <strong>Couche 3 (coupe-vent/imperméable)</strong> : veste Gore-Tex ou équivalent. La plupart des compagnies d'expédition <strong>prêtent une grosse parka rouge</strong> incluse dans le prix — vérifiez avant de sur-équiper."),
            ("h3","Bas du corps"),
            ("p","Sous-couche thermique, pantalon de ski imperméable, bottes polaires type Bogs/Muck montantes fournies par le navire (toutes les grandes compagnies les louent gratuitement pendant la croisière pour les débarquements Zodiac)."),
            ("img",4,"Voyageur en équipement polaire trois couches sur un zodiac antarctique"),
            ("h4","Extrémités"),
            ("p","<strong>Bonnet</strong> ou cagoule couvrant les oreilles, <strong>tour de cou</strong> (buff ou cagoule), <strong>gants sous-gants + gants de ski</strong> (doubles), <strong>lunettes catégorie 4</strong>, crème solaire 50, baume à lèvres. Ce sont les extrémités qui souffrent le plus — doublez systématiquement gants et chaussettes."),
         ]},
    ],
    "expert_tip":"Emportez <strong>deux paires de sous-gants fins</strong> : elles vous permettent de photographier sans ôter totalement vos gants dans le froid. Au retour à bord après un débarquement, vos gants extérieurs seront trempés — les sous-gants secs vous sauvent les doigts. Et privilégiez des bottes <strong>une pointure au-dessus</strong> pour glisser 2 paires de chaussettes épaisses sans comprimer la circulation.",
})

# 3. Visa Antarctique
ARTICLES.append({
    "slug": "visa-antarctique",
    "title": "Faut-il un Visa pour Aller en Antarctique ? Réponse Officielle 2026 | Voyage 7 Continents",
    "og_title": "Visa Antarctique : Réponse Officielle et Démarches 2026",
    "desc": "L'Antarctique n'a pas d'autorité souveraine : pas de visa pour le continent. Mais les escales Argentine/Chili et le Traité sur l'Antarctique imposent des formalités précises.",
    "crumb": "Visa Antarctique",
    "h1": "Faut-il un Visa pour Aller en Antarctique ?",
    "lead": "L'Antarctique n'appartient à aucun État et ne délivre pas de visa, mais les escales sud-américaines et le Traité sur l'Antarctique imposent des formalités qu'il faut connaître.",
    "alt1": "Drapeau du Traité sur l'Antarctique flottant près d'une base scientifique",
    "caption1": "L'Antarctique est régi par le Traité sur l'Antarctique de 1959, signé par 54 États.",
    "sections": [
        {"id":"pas-souverainete","toc":"Pas de souveraineté","short":"Souveraineté","h2":"Antarctique : Pas de Visa, Pas de Souveraineté",
         "blocks":[
            ("p","L'<strong>Antarctique n'est rattachée à aucun État souverain</strong>. Sept pays revendiquent historiquement des territoires (Argentine, Chili, Royaume-Uni, Norvège, Australie, Nouvelle-Zélande, France avec la Terre Adélie), mais ces revendications sont <strong>gelées</strong> depuis 1961 par le <a href=\"https://www.ats.aq/e/treaty.html\" target=\"_blank\" rel=\"noopener nofollow\">Traité sur l'Antarctique</a> signé en 1959 et entré en vigueur en 1961."),
            ("p","Conséquence : <strong>aucune autorité n'émet de visa antarctique</strong>. Vous n'avez rien à tamponner pour mettre le pied sur le continent. Le passage se fait « en haute mer » sous le régime du Traité, qui consacre l'Antarctique comme une réserve scientifique dédiée à la paix."),
            ("img",2,"Panneau marquant l'arrivée au pôle Sud avec drapeaux des pays signataires"),
            ("h3","Les 54 signataires"),
            ("p","Le Traité compte désormais <strong>54 États signataires</strong>, dont 29 « parties consultatives » qui mènent des recherches scientifiques sur le continent (France, États-Unis, Russie, Chine, Argentine, Chili, Royaume-Uni, Norvège, Japon, etc.). Les décisions se prennent en consensus aux Réunions consultatives du Traité sur l'Antarctique (ATCM), organisées chaque année."),
         ]},
        {"id":"visas-escales","toc":"Visas des escales","short":"Escales","h2":"Les Visas Nécessaires pour les Escales",
         "blocks":[
            ("p","Si vous n'avez pas besoin de visa antarctique à proprement parler, vous aurez <strong>besoin d'un visa pour transiter par les pays de départ</strong>, principalement l'Argentine (Ushuaia) ou le Chili (Punta Arenas)."),
            ("h3","Argentine"),
            ("p","Les ressortissants français, belges, suisses et canadiens <strong>n'ont pas besoin de visa</strong> pour un séjour touristique en Argentine de moins de 90 jours. Un passeport valable 6 mois après la date de retour suffit. <a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/argentine/\" target=\"_blank\" rel=\"noopener nofollow\">Source : France Diplomatie</a>."),
            ("h3","Chili"),
            ("p","Idem pour le Chili : dispense de visa pour les touristes français jusqu'à 90 jours. À l'entrée, vous recevez une <strong>Tarjeta de Turismo</strong> (formulaire vert) qu'il faut conserver jusqu'à la sortie du pays — sa perte coûte environ 100 USD de remplacement à l'aéroport."),
            ("img",3,"Passeport français tamponné à Ushuaia avec billet d'embarquement croisière antarctique"),
            ("h4","Transit sans ressortir ?"),
            ("p","Quand vous embarquez à Ushuaia pour une croisière Antarctique et revenez au même port, <strong>vous ne re-tamponnez pas votre passeport</strong> : le navire reste sous pavillon étranger et vous ne sortez techniquement pas de la zone frontière argentine. Vérifiez avec votre compagnie pour les modalités précises."),
         ]},
        {"id":"traite-reglementation","toc":"Règles du Traité","short":"Traité","h2":"Règles du Traité et Protocole de Madrid",
         "blocks":[
            ("p","Même sans visa, vous êtes soumis au <strong>Protocole de Madrid (1991)</strong>, qui classe l'Antarctique comme « réserve naturelle consacrée à la paix et à la science ». Il interdit l'exploitation minière, impose des règles strictes aux visiteurs et oblige tout opérateur commercial à obtenir une <strong>autorisation préalable</strong> de son gouvernement de rattachement."),
            ("h3","Autorisation française"),
            ("p","En France, cette autorisation est délivrée par les <a href=\"https://taaf.fr/\" target=\"_blank\" rel=\"noopener nofollow\">TAAF (Terres australes et antarctiques françaises)</a> pour les opérateurs français. Les compagnies étrangères (Hurtigruten, Quark…) obtiennent la leur auprès de leur propre État."),
            ("h3","Règles à bord et à terre"),
            ("p","Distance minimale de 5 mètres avec la faune, pas de déchet (même organique), pas de prélèvement (roches, plumes, fossiles interdits), désinfection obligatoire des bottes avant chaque débarquement pour éviter l'introduction d'espèces invasives. Tous les passagers signent les <strong>IAATO Visitor Guidelines</strong> avant d'embarquer."),
            ("img",4,"Passagers brossant leurs bottes antarctiques sur le pont d'un navire d'expédition"),
         ]},
        {"id":"comment-verifier","toc":"Comment vérifier","short":"Vérifier","h2":"Comment Vérifier sa Compagnie",
         "blocks":[
            ("p","Vérifiez avant toute réservation que votre compagnie est <strong>membre IAATO</strong> (<a href=\"https://iaato.org/field-operations/tour-operator-directory/\" target=\"_blank\" rel=\"noopener nofollow\">Tour Operator Directory</a>). L'adhésion IAATO garantit le respect du Protocole de Madrid, la détention d'une autorisation gouvernementale valide, une assurance adéquate et un ratio de guides expérimentés."),
            ("box","Une compagnie <strong>non membre IAATO</strong> opérant dans la zone peut théoriquement le faire, mais vous perdez toutes les garanties et pourriez vous retrouver dans une situation délicate en cas d'incident. Un seul naufrage d'opérateur non-IAATO, celui du MS Explorer en 2007, a failli causer une catastrophe écologique majeure."),
         ]},
    ],
    "expert_tip":"Pour la France, demandez à votre opérateur de fournir une <strong>copie de l'autorisation TAAF (ou équivalent étranger)</strong> et du <strong>certificat IAATO</strong>. Un opérateur sérieux les communique sans hésiter. Méfiez-vous des offres low-cost sur des navires qui n'ont jamais opéré en Antarctique auparavant : le Protocole de Madrid n'accorde pas de dérogation.",
})

# 4. Meilleure période
ARTICLES.append({
    "slug": "meilleure-periode-antarctique",
    "title": "Quelle est la Meilleure Période pour l'Antarctique ? Calendrier 2026 | Voyage 7 Continents",
    "og_title": "Meilleure Période pour l'Antarctique : Calendrier par Mois 2026",
    "desc": "Novembre (glace vierge), décembre-janvier (bébés manchots), février-mars (baleines) : la meilleure période pour l'Antarctique dépend de votre objectif.",
    "crumb": "Meilleure période",
    "h1": "Quelle est la Meilleure Période pour l'Antarctique ?",
    "lead": "Novembre, décembre, février : chaque mois de la saison australe offre une expérience antarctique différente. Le calendrier complet pour choisir sa croisière selon ses envies.",
    "alt1": "Manchots Adélie en colonie sur la banquise en Antarctique pendant l'été austral",
    "caption1": "La saison touristique antarctique s'étend de fin octobre à fin mars — 5 mois pour visiter le continent blanc.",
    "sections": [
        {"id":"saison","toc":"La saison australe","short":"Saison","h2":"La Saison Australe : Novembre à Mars",
         "blocks":[
            ("p","Le tourisme antarctique n'est possible qu'en <strong>été austral</strong>, du début novembre à la fin mars. En dehors de cette fenêtre, la banquise est trop étendue, la nuit trop longue et les conditions météo trop hostiles pour accéder à la péninsule en sécurité. Aucune croisière commerciale ne navigue hors saison."),
            ("p","Les 5 mois de la saison se répartissent en <strong>3 périodes</strong> aux caractéristiques très différentes : début de saison (novembre-mi-décembre), cœur de saison (fin décembre-janvier) et fin de saison (février-mars). Chacune offre une expérience spécifique."),
            ("img",2,"Carte saisonnière montrant l'évolution de la banquise antarctique entre novembre et mars"),
            ("h3","Statistiques IAATO"),
            ("p","L'<a href=\"https://iaato.org/information-resources/data-statistics/\" target=\"_blank\" rel=\"noopener nofollow\">IAATO publie chaque année les chiffres de fréquentation</a> : environ <strong>120 000 visiteurs</strong> ont rejoint la péninsule Antarctique lors de la saison 2023-2024, en hausse continue depuis 2015 (hors interruption covid)."),
         ]},
        {"id":"novembre","toc":"Novembre","short":"Novembre","h2":"Novembre : Glace Vierge et Parades",
         "blocks":[
            ("p","Début novembre, la banquise fond tout juste et les baies commencent à s'ouvrir aux navires. C'est le <strong>mois des paysages les plus purs</strong> : tout est blanc immaculé, les icebergs sont sculptés par l'hiver qui s'achève, les couleurs du ciel sont éclatantes en l'absence de poussière."),
            ("h3","Faune en novembre"),
            ("p","C'est la <strong>saison des parades nuptiales</strong> : les manchots Adélie, Papou et à jugulaire construisent leurs nids, rassemblent des cailloux, se disputent les meilleures places sur les colonies. Les éléphants de mer mâles se battent encore pour leur harem sur les plages de Géorgie du Sud."),
            ("img",3,"Manchots Adélie en parade nuptiale sur neige immaculée en novembre antarctique"),
            ("h4","Inconvénients"),
            ("p","Certaines baies et canaux restent <strong>encore pris par les glaces</strong> en début de mois, ce qui peut empêcher de descendre loin au sud (cercle polaire). Les prix sont en revanche légèrement inférieurs qu'en haute saison."),
         ]},
        {"id":"dec-jan","toc":"Décembre-janvier","short":"Déc-Janv","h2":"Décembre-Janvier : Pic de Saison",
         "blocks":[
            ("p","Décembre et janvier sont les <strong>mois les plus demandés</strong>. Températures plus clémentes (-2 à +3 °C sur la péninsule), 20 heures de jour, icebergs photogéniques, et surtout : éclosion des <strong>œufs de manchots</strong> et apparition des poussins duveteux fin décembre."),
            ("p","C'est la période <strong>reine pour la photographie animalière</strong> : les poussins grandissent à vue d'œil, les parents font l'aller-retour entre mer et nid à longueur de journée, les phoques de Weddell mettent bas sur la glace. Les krills attirent baleines et oiseaux marins."),
            ("img",4,"Poussins de manchots Papous de quelques semaines dans leur nid en janvier"),
            ("h3","Haute saison = tarifs premium"),
            ("p","Les prix sont à leur maximum : comptez <strong>30 à 40 % de surcoût</strong> par rapport à novembre. Les croisières autour de Noël et nouvel an sont les plus chères de l'année, souvent réservées 12 à 18 mois à l'avance."),
            ("h4","Cercle polaire"),
            ("p","C'est aussi la meilleure fenêtre pour dépasser le <strong>cercle polaire antarctique (66°33' S)</strong> — les canaux sont libres de glace et les navires type brise-glace (Sea Spirit, Ocean Nova) y accèdent régulièrement."),
         ]},
        {"id":"fev-mars","toc":"Février-mars","short":"Fév-Mars","h2":"Février-Mars : Baleines et Couleurs d'Automne",
         "blocks":[
            ("p","Fin de saison : février et mars sont <strong>le meilleur moment pour observer les baleines</strong>. Les bosses, rorquals communs, orques et petits rorquals se nourrissent intensivement avant la migration vers le nord. Vous en verrez <strong>lors de quasiment chaque débarquement Zodiac</strong>."),
            ("p","Les poussins de manchots sont désormais grands, commencent à muer et à prendre la mer : scènes comiques sur les plages. La glace a reculé au maximum, ouvrant des passages nouveaux et des canaux encore peu explorés de la saison."),
            ("img",5,"Baleine à bosse émergeant près d'un zodiac dans un fjord antarctique en mars"),
            ("h3","Paysages automnaux"),
            ("p","La lumière devient dorée et rasante. Les mers sont un peu plus agitées, la neige a parfois un aspect « sale » (algues microscopiques colorant la glace en rose ou vert — phénomène naturel surnommé « neige pastèque »). Les prix redescendent en fin de mars."),
            ("h4","Dernier départ"),
            ("p","La dernière croisière de la saison quitte Ushuaia vers la mi-mars. Au-delà, la banquise se reforme et les conditions deviennent dangereuses."),
         ]},
    ],
    "expert_tip":"Si c'est votre <strong>premier voyage</strong> et que votre budget le permet, visez <strong>fin décembre ou début janvier</strong> : c'est le compromis idéal entre faune active, longueur du jour, conditions de navigation et paysages. Si vous êtes <strong>photographe</strong>, préférez fin février pour les baleines ; si vous cherchez <strong>les paysages vierges</strong>, partez début novembre. Évitez la pleine saison de Noël pour économiser 20-30 % du prix.",
})

# 5. Marcher sur la glace
ARTICLES.append({
    "slug": "marcher-glace-antarctique",
    "title": "Peut-on Marcher sur la Glace en Antarctique ? Ce que Dit l'IAATO | Voyage 7 Continents",
    "og_title": "Marcher sur la Glace Antarctique : Règles IAATO 2026",
    "desc": "Oui, on peut marcher sur certaines zones de glace antarctique lors des débarquements Zodiac — mais les règles IAATO strictes encadrent chaque pas pour protéger le continent.",
    "crumb": "Marcher sur la glace",
    "h1": "Peut-on Marcher sur la Glace en Antarctique ?",
    "lead": "Banquise, glaciers, icebergs : la réponse n'est pas la même selon le type de glace. Les règles IAATO, les risques et la réalité des débarquements en expédition antarctique.",
    "alt1": "Touristes marchant en file indienne sur la neige damée en péninsule Antarctique",
    "caption1": "Les débarquements antarctiques se font sur neige ou roche, pas sur de la banquise instable.",
    "sections": [
        {"id":"oui-mais","toc":"Oui, mais pas partout","short":"Où","h2":"Oui, Mais Pas N'importe Où",
         "blocks":[
            ("p","La réponse courte est <strong>oui, on peut marcher sur la neige et la glace en Antarctique</strong>, mais uniquement lors des débarquements organisés par votre compagnie, dans des zones <strong>validées par l'IAATO</strong> et vos guides d'expédition. Les « débarquements libres » ou les excursions individuelles sont interdits."),
            ("p","En pratique, lors d'une croisière depuis Ushuaia, vous ferez <strong>1 à 2 débarquements par jour</strong> (matin et après-midi) sur des sites sélectionnés : plages rocheuses, colonies de manchots, glaciers stabilisés, bases scientifiques. Entre deux débarquements, vous ne descendez pas sur la banquise flottante pour une question de sécurité."),
            ("img",2,"Zodiac débarquant des passagers sur une plage de galets en péninsule Antarctique"),
         ]},
        {"id":"types-glace","toc":"Types de glace","short":"Types","h2":"Les Différents Types de Glace",
         "blocks":[
            ("p","Toutes les glaces antarctiques ne se valent pas en termes de sécurité. Il est essentiel de comprendre les différences pour savoir ce qui est praticable."),
            ("h3","Glaciers et inlandsis"),
            ("p","Les <strong>glaciers continentaux</strong> (terminus, langues glaciaires) sont praticables à pied dans les zones stabilisées. L'équipe d'expédition <strong>repère les crevasses</strong> au préalable, installe un itinéraire balisé par des piquets, et vous marchez en file indienne. Certains navires proposent même des <strong>randonnées raquettes</strong> (snowshoe) en option sur les glaciers bas."),
            ("h3","Banquise (sea ice)"),
            ("p","La banquise est la glace de mer qui se forme chaque hiver puis fond l'été. On <strong>ne marche pas</strong> sur la banquise flottante depuis un navire : risque de rupture, d'eau ouverte sous la surface, de courants rapides. En revanche, quand la banquise est encore attachée à la côte (« fast ice ») et suffisamment épaisse, certains opérateurs proposent des débarquements contrôlés."),
            ("img",3,"Étendue de banquise fissurée en Antarctique avec eau sombre visible"),
            ("h3","Icebergs"),
            ("p","On <strong>ne monte jamais sur un iceberg flottant</strong> : il peut se retourner à tout moment en quelques secondes, avec des conséquences fatales. Les icebergs se photographient depuis le Zodiac, à distance de sécurité de 3 fois leur hauteur visible."),
         ]},
        {"id":"regles-iaato","toc":"Règles IAATO","short":"Règles","h2":"Les Règles IAATO en 10 Points",
         "blocks":[
            ("p","L'IAATO impose des règles précises à chaque débarquement, détaillées dans les <a href=\"https://iaato.org/visitor-guidelines/\" target=\"_blank\" rel=\"noopener nofollow\">Visitor Guidelines</a>. Voici les principales."),
            ("p","<strong>1)</strong> Maximum <strong>100 personnes à terre</strong> simultanément sur un site. <strong>2)</strong> Distance minimale de <strong>5 mètres</strong> avec la faune. <strong>3)</strong> Rester sur les chemins tracés par les guides pour ne pas piétiner la végétation (mousses, lichens). <strong>4)</strong> Ne rien laisser, ne rien prélever (roche, plume, os)."),
            ("p","<strong>5)</strong> Ne pas marcher sur les nids de manchots. <strong>6)</strong> Ne pas courir ni faire de bruit fort. <strong>7)</strong> Bottes désinfectées avant et après chaque débarquement. <strong>8)</strong> Ne pas s'asseoir sur la neige (contamination et gel). <strong>9)</strong> Parka étanche et gilet de sauvetage obligatoires en Zodiac. <strong>10)</strong> Interdiction de fumer à terre."),
            ("img",4,"Passagers brossant leurs bottes dans un bac de désinfection avant de descendre"),
         ]},
        {"id":"risques","toc":"Risques et sécurité","short":"Risques","h2":"Risques et Sécurité sur la Glace",
         "blocks":[
            ("p","Même dans un cadre ultra-sécurisé, l'Antarctique reste un environnement extrême. Les guides portent radio, GPS, balise PLB, kit de premiers secours et repèrent les crevasses avec une sonde."),
            ("h3","Crevasses"),
            ("p","Les <strong>crevasses cachées</strong> sous un pont de neige sont le principal danger sur glacier. Les guides progressent devant, marquent les zones dangereuses et vous évitent impérativement de sortir du chemin balisé. Ne décrochez jamais du groupe pour « la photo parfaite »."),
            ("h3","Froid et épuisement"),
            ("p","Un pas sur la glace nécessite plus d'efforts qu'un pas sur terre ferme. <strong>Ne surévaluez pas votre niveau</strong> : un débarquement typique fait 1 à 3 km à 0°C et peut fatiguer rapidement. Les seniors et personnes à mobilité réduite bénéficient souvent d'un « landing plus court » alternatif."),
            ("img",5,"Guide d'expédition polaire sondant la neige avant un débarquement groupé"),
            ("box","Vérifiez auprès de votre compagnie si des <strong>randonnées</strong> (hikes de 3-5 km avec dénivelé) sont proposées en option : chez Oceanwide, Aurora, Quark, elles sont incluses ; chez d'autres, elles coûtent un supplément. Si vous voulez marcher plus longtemps, choisissez un opérateur « expédition » plutôt qu'un grand paquebot."),
         ]},
    ],
    "expert_tip":"Ne quittez jamais le groupe et ne vous approchez jamais des bords de falaise ou des fronts de glacier : <strong>les vêlages imprévisibles</strong> peuvent projeter d'énormes blocs à des dizaines de mètres. Gardez toujours 50 mètres de marge avec toute structure glacée active et respectez scrupuleusement les instructions de votre guide — ils ont vu plus d'accidents évitables que vous n'en imaginez.",
})

# 6. Budget petit budget
ARTICLES.append({
    "slug": "budget-croisiere-antarctique",
    "title": "Budget Croisière Antarctique Petit Budget : Comment Payer Moins en 2026 | Voyage 7 Continents",
    "og_title": "Budget Croisière Antarctique Petit Budget 2026 : Astuces",
    "desc": "Last-minute à Ushuaia, cabines triples, basse saison, voilier partagé : toutes les astuces pour partir en Antarctique à partir de 6 000 € au lieu de 15 000 €.",
    "crumb": "Budget petit",
    "h1": "Budget Croisière Antarctique Petit Budget : Comment Payer Moins",
    "lead": "Cabines triples, last-minute Ushuaia, basse saison, vol low-cost, voilier partagé : le guide pour partir en Antarctique sans hypothéquer sa maison en 2026.",
    "alt1": "Port d'Ushuaia en Argentine avec voilier d'expédition polaire amarré",
    "caption1": "Les voiliers partagés offrent le ticket d'entrée le moins cher pour atteindre la péninsule Antarctique.",
    "sections": [
        {"id":"realite-prix","toc":"Réalité des prix","short":"Prix","h2":"La Réalité des Prix en 2026",
         "blocks":[
            ("p","Soyons clairs : l'Antarctique restera toujours un voyage cher. Les prix moyens en 2026 pour une croisière de 10 jours depuis Ushuaia s'échelonnent entre <strong>8 000 et 18 000 € par personne</strong>, plus le vol Paris-Ushuaia (900-1 500 €). Le qualificatif « petit budget » dans le contexte antarctique signifie descendre autour de <strong>6 000-8 000 € tout compris</strong>."),
            ("p","Les voyages à moins de 6 000 € existent mais exigent des compromis : cabines partagées à 4, voilier sportif, basse saison, itinéraires courts (8 jours au lieu de 12). Voici les 6 leviers qui permettent réellement de réduire la facture."),
            ("img",2,"Graphique schématique des prix moyens des croisières antarctiques par catégorie de cabine"),
         ]},
        {"id":"cabine-partagee","toc":"Cabine partagée","short":"Cabine","h2":"1. Cabine Triple ou Quadruple",
         "blocks":[
            ("p","Le levier numéro 1 : prendre une <strong>cabine triple ou quadruple partagée</strong> au lieu d'une double. Économie : <strong>30 à 45 %</strong> par rapport à la même croisière en double standard. Les compagnies qui le proposent : Oceanwide Expeditions (M/V Plancius, Ortelius), Aurora, Quark, Poseidon."),
            ("p","Vous partagez la cabine avec 2 ou 3 inconnus du même sexe. Les lits superposés ne sont pas glamour, mais vous passerez l'essentiel du temps éveillé en ponts, salons, bars ou à terre. Pour dormir, cela fait très bien l'affaire."),
            ("h3","Prix indicatifs"),
            ("p","Cabine triple Oceanwide Plancius, itinéraire classique 10 jours : à partir de <strong>6 200 €</strong> par personne. Cabine double standard sur le même voyage : 8 500-9 500 €. Économie nette : 2 000 à 3 000 €."),
            ("img",3,"Cabine triple avec lits superposés sur un navire d'expédition polaire"),
         ]},
        {"id":"last-minute","toc":"Last-minute Ushuaia","short":"Last-minute","h2":"2. Last-Minute à Ushuaia",
         "blocks":[
            ("p","Historiquement, la stratégie <strong>« j'arrive à Ushuaia sans billet et je négocie »</strong> permettait d'économiser 40 à 50 % sur des cabines invendues. En 2026, cette stratégie <strong>fonctionne encore</strong> mais dans des proportions plus modestes (15 à 30 %) car la demande est devenue très forte."),
            ("h3","Comment procéder"),
            ("p","Arrivez à Ushuaia <strong>en début de saison (novembre) ou en fin de saison (mars)</strong>, posez-vous en auberge de jeunesse 5 à 10 jours, et faites le tour des agences : <em>Rumbo Sur, Freestyle Adventure Travel, All Patagonia, Tolkar</em>. Elles récupèrent les cabines annulées et les revendent en dernière minute."),
            ("img",4,"Rue commerçante d'Ushuaia avec vitrines d'agences d'expéditions antarctiques"),
            ("h4","Risque"),
            ("p","Vous pouvez repartir bredouille ou attendre 10 jours avant qu'un départ se présente. Prévoyez un budget logement Ushuaia (25-40 € / nuit en auberge). Et si vous avez des dates précises à tenir, cette option n'est <strong>pas recommandée</strong>."),
         ]},
        {"id":"basse-saison","toc":"Basse saison","short":"Basse saison","h2":"3. Partir en Début ou Fin de Saison",
         "blocks":[
            ("p","Les prix varient de <strong>20 à 30 %</strong> entre la haute saison (mi-décembre à fin janvier, pic de demande) et la basse saison (début novembre ou mi-mars). Pour un même navire et un même itinéraire, vous pouvez économiser <strong>1 500 à 3 000 €</strong> en décalant votre départ."),
            ("p","Les deux périodes « bon plan » sont les <strong>3 premières semaines de novembre</strong> (glace vierge, parades des manchots) et les <strong>2 dernières semaines de mars</strong> (baleines en abondance, fin des départs). Les compagnies bradent leurs dernières cabines invendues."),
         ]},
        {"id":"voilier","toc":"Voilier partagé","short":"Voilier","h2":"4. Voilier Partagé : l'Aventure Pure",
         "blocks":[
            ("p","Une dizaine de voiliers privés (Dalat, Santa Maria Australis, Pelagic, Podorange, Jonathan III) embarquent 6 à 12 passagers pour des traversées de <strong>15 à 25 jours</strong>. Les prix vont de <strong>6 500 à 10 500 €</strong> par personne selon le bateau, l'itinéraire et la saison."),
            ("h3","Ce qui est différent"),
            ("p","Vous dormez à 2-3 par couchette, participez aux quarts, à la cuisine, à la navigation. L'expérience est <strong>beaucoup plus authentique et sportive</strong> que sur un grand navire. Vous débarquez sur des sites rarement visités et dormez parfois dans des baies isolées sans autre navire à l'horizon."),
            ("img",5,"Voilier d'expédition polaire ancré dans une baie antarctique avec glacier en arrière-plan"),
            ("h4","Prérequis"),
            ("p","Il faut avoir le <strong>pied marin</strong>, être prêt à vivre 3 semaines en promiscuité et accepter l'inconfort d'un voilier à la mer par 7 m de creux dans le Drake. Ce n'est <strong>pas recommandé</strong> aux novices, aux seniors ou aux personnes sujettes au mal de mer."),
         ]},
        {"id":"autres-leviers","toc":"Autres leviers","short":"Autres","h2":"5-6. Autres Leviers d'Économie",
         "blocks":[
            ("h3","5. Voyage en solo ou sans supplément single"),
            ("p","Les suppléments « single » (chambre individuelle) représentent souvent <strong>+50 à +100 %</strong> du tarif. Choisissez une compagnie qui propose des <strong>cabines partagées pour solos</strong> sans supplément : Oceanwide, Aurora, Quark. Vous serez jumelé(e) avec un inconnu du même sexe, mais sans payer le double."),
            ("h3","6. Vol Paris-Ushuaia en promo"),
            ("p","Le vol peut coûter <strong>900 €</strong> en promotion ou <strong>1 500 €</strong> en dernière minute. Surveillez <a href=\"https://www.skyscanner.fr/\" target=\"_blank\" rel=\"noopener nofollow\">Skyscanner</a> sur plusieurs mois et combinez des billets séparés Paris-Buenos Aires + Buenos Aires-Ushuaia (souvent 20-30 % moins cher qu'un billet unique). Aerolineas Argentinas, Latam, Air France et KLM sont les plus utilisés."),
            ("box","<strong>Cumul total</strong> : en combinant cabine triple + basse saison + cabine solo sans supplément + vol en promo, on peut réalistiquement faire une expédition Antarctique à <strong>6 200 € tout compris depuis Paris</strong>. C'est le plancher raisonnable, en-dessous vous entrez dans le voilier sportif ou le camping sauvage (illégal sans autorisation TAAF)."),
         ]},
    ],
    "expert_tip":"Combinez les leviers : <strong>cabine triple + départ mi-novembre ou mi-mars + vol réservé 8 mois avant</strong>. C'est la recette qui fonctionne. Et ne tombez pas dans le piège des « packages tout compris » à 4 000 € : ils n'incluent jamais la vraie croisière, juste un transfert depuis Buenos Aires. Lisez toujours le détail des inclusions avant de payer un acompte non remboursable.",
})

# 7. Animaux
ARTICLES.append({
    "slug": "animaux-antarctique",
    "title": "Quels Animaux Voir en Antarctique ? 15 Espèces à Observer | Voyage 7 Continents",
    "og_title": "Animaux d'Antarctique : 15 Espèces à Observer en Croisière 2026",
    "desc": "Manchots empereur, Adélie, Gentoo, léopards des mers, baleines à bosse, orques : les 15 espèces à voir absolument lors d'une croisière antarctique.",
    "crumb": "Animaux",
    "h1": "Quels Animaux Voir en Antarctique ? Le Guide Complet",
    "lead": "Manchots, phoques, baleines, albatros : 15 espèces emblématiques à observer lors d'une expédition sur la péninsule Antarctique, avec conseils et lieux de rencontre.",
    "alt1": "Colonie de manchots Papous sur un rocher enneigé en péninsule Antarctique",
    "caption1": "Les manchots Papous (Gentoo) sont les plus nombreux et les plus accessibles de la péninsule Antarctique.",
    "sections": [
        {"id":"manchots","toc":"Les manchots","short":"Manchots","h2":"Les Manchots : Stars du Continent Blanc",
         "blocks":[
            ("p","L'Antarctique abrite <strong>8 espèces de manchots</strong>, dont 5 sont visibles lors d'une croisière classique sur la péninsule. Ce sont évidemment les animaux les plus observés : vous les verrez par milliers, voire dizaines de milliers, sur certaines colonies."),
            ("h3","Gentoo (Papou)"),
            ("p","Les <strong>manchots Gentoo</strong>, reconnaissables à leur bec orange et leur tache blanche au-dessus des yeux, sont les plus nombreux et les plus curieux. Environ <strong>120 000 couples</strong> selon les comptages de la <a href=\"https://www.scar.org/\" target=\"_blank\" rel=\"noopener nofollow\">SCAR (Scientific Committee on Antarctic Research)</a>. Vous en verrez à Cuverville, Port Lockroy, Neko Harbour."),
            ("img",2,"Manchot Gentoo avec son poussin sur un nid de cailloux"),
            ("h3","Adélie"),
            ("p","Les <strong>manchots Adélie</strong> (bec noir, cercle blanc autour de l'œil) sont plus nombreux encore à l'échelle du continent : environ <strong>4 millions de couples</strong>. Sur la péninsule, ils se voient surtout à Paulet Island, Devil Island et dans la mer de Weddell."),
            ("h3","Manchot à jugulaire (Chinstrap)"),
            ("p","Le plus reconnaissable avec sa ligne noire sous le menton comme un casque de moto. Environ 4 millions de couples, concentrés sur les îles Shetland du Sud (Half Moon, Deception). Bruyant, grégaire, très photogénique."),
            ("h3","Royal et Empereur"),
            ("p","Le <strong>manchot royal</strong> (similaire à l'empereur mais plus petit) se voit en Géorgie du Sud, lors des croisières longues. Le <strong>manchot empereur</strong>, plus grand (1,20 m, 40 kg), est <strong>très rarement</strong> observé en péninsule — il niche principalement en mer de Weddell et nécessite des croisières spéciales en brise-glace."),
         ]},
        {"id":"phoques","toc":"Phoques","short":"Phoques","h2":"Les Phoques : 6 Espèces à Repérer",
         "blocks":[
            ("p","Six espèces de phoques vivent en Antarctique, toutes observables depuis un Zodiac ou lors des débarquements."),
            ("h3","Léopard des mers"),
            ("p","Le <strong>léopard des mers</strong> est le prédateur suprême de la région, redouté même par les manchots. Reconnaissable à son corps allongé (jusqu'à 3,50 m), sa gueule largement fendue et sa robe tachetée. Solitaire, il se repose souvent sur les banquises à la dérive. <strong>Approche interdite en Zodiac à moins de 15 mètres</strong> : il peut charger."),
            ("h3","Weddell, crabier, éléphant de mer"),
            ("p","Le <strong>phoque de Weddell</strong> (le plus commun sur la côte) se repose sur la glace, photogénique au possible. Le <strong>phoque crabier</strong>, le plus abondant au monde (15 millions d'individus selon <a href=\"https://www.iucnredlist.org/species/3544/45224234\" target=\"_blank\" rel=\"noopener nofollow\">UICN</a>), malgré son nom ne mange que du krill. L'<strong>éléphant de mer austral</strong>, immense (jusqu'à 4 tonnes pour les mâles), se voit surtout en Géorgie du Sud."),
            ("img",3,"Phoque de Weddell dormant sur une plaque de banquise antarctique"),
            ("h4","Ross et fourrure"),
            ("p","Le <strong>phoque de Ross</strong> est le plus rare — observé surtout en mer de Ross. L'<strong>otarie à fourrure antarctique</strong>, disparue près de l'extinction au 19ème siècle, a fortement rebondi et colonise aujourd'hui les îles Shetland en grand nombre."),
         ]},
        {"id":"baleines","toc":"Baleines","short":"Baleines","h2":"Baleines et Cétacés",
         "blocks":[
            ("p","L'Antarctique est l'un des meilleurs endroits au monde pour l'observation des baleines, surtout en <strong>février-mars</strong> quand elles se nourrissent de krill avant leur migration vers les eaux tropicales."),
            ("h3","Baleine à bosse"),
            ("p","La <strong>baleine à bosse</strong> (Megaptera novaeangliae) est la plus fréquemment observée : acrobatique, curieuse, elle s'approche souvent des navires et des Zodiacs. Elle peut faire du « bubble-net feeding » — une technique de chasse coopérative spectaculaire où plusieurs baleines créent un filet de bulles pour concentrer le krill."),
            ("img",4,"Baleine à bosse bondissant hors de l'eau au large de la péninsule Antarctique"),
            ("h3","Rorqual, petit rorqual, orque"),
            ("p","Le <strong>rorqual commun</strong>, 2ème plus grand animal du monde (20-25 m), se voit plus au large. Le <strong>petit rorqual (Minke)</strong> est curieux, souvent près des côtes. L'<strong>orque</strong> (Type A, B, C selon les écotypes antarctiques) est présente toute la saison et se voit lors de chasses spectaculaires de phoques ou de baleines à bosse."),
         ]},
        {"id":"oiseaux","toc":"Oiseaux marins","short":"Oiseaux","h2":"Oiseaux Marins et Albatros",
         "blocks":[
            ("p","L'Antarctique et ses eaux environnantes abritent <strong>une quarantaine d'espèces d'oiseaux marins</strong>. Pendant la traversée du Drake, vous verrez un ballet permanent autour du navire."),
            ("h3","Albatros"),
            ("p","L'<strong>albatros hurleur</strong> (envergure jusqu'à 3,50 m, la plus grande au monde) suit souvent les navires pendant des heures. Il niche en Géorgie du Sud. Les <strong>albatros à sourcils noirs</strong> et à <strong>tête grise</strong> sont également fréquents."),
            ("img",5,"Albatros hurleur planant au-dessus de l'océan austral avec ailes déployées"),
            ("h3","Pétrels et autres"),
            ("p","<strong>Pétrel géant</strong>, <strong>pétrel des neiges</strong> (entièrement blanc, magnifique), <strong>prion antarctique</strong>, <strong>skua</strong> (redouté par les manchots pour qui il est un prédateur des poussins), <strong>cormoran impérial</strong>, <strong>sterne arctique</strong> (qui migre de l'Arctique à l'Antarctique chaque année, record de distance)."),
            ("box","Emportez des <strong>jumelles 8x42 étanches</strong> : elles sont indispensables pour l'observation des oiseaux depuis le pont et des baleines à distance. Prévoyez aussi un téléobjectif 100-400 mm ou 200-600 mm si vous êtes photographe animalier."),
         ]},
    ],
    "expert_tip":"Pour maximiser vos observations : restez <strong>en permanence sur le pont pendant le Drake</strong>, jumelles en main — c'est là que l'on voit le plus d'albatros et de baleines. Et gardez 50 mètres de distance minimum avec tout animal (distance IAATO), même s'il s'approche spontanément : c'est la règle, et elle protège la faune comme vous.",
})

# 8. Combien de jours
ARTICLES.append({
    "slug": "combien-jours-antarctique",
    "title": "Combien de Jours pour Visiter l'Antarctique ? Durées Idéales 2026 | Voyage 7 Continents",
    "og_title": "Combien de Jours en Antarctique : 10 à 22 Jours, le Guide 2026",
    "desc": "Croisière 10 jours classique, 14 jours cercle polaire, 20-22 jours Géorgie du Sud Falklands : toutes les durées d'expédition antarctique avec avantages et prix.",
    "crumb": "Combien de jours",
    "h1": "Combien de Jours pour Visiter l'Antarctique ?",
    "lead": "10 jours pour la péninsule classique, 14 pour le cercle polaire, 20-22 jours pour la Géorgie du Sud et les Falklands : le guide complet des durées d'expédition antarctique.",
    "alt1": "Navire d'expédition polaire naviguant à travers un chenal de glace en Antarctique",
    "caption1": "La durée de votre croisière détermine largement l'étendue des régions que vous pourrez explorer.",
    "sections": [
        {"id":"duree-moyenne","toc":"Durée moyenne","short":"Durée","h2":"Durée Moyenne d'une Expédition",
         "blocks":[
            ("p","La grande majorité des croisières antarctiques depuis Ushuaia durent <strong>10 à 12 jours au total</strong>, Ushuaia à Ushuaia. Cette durée inclut <strong>4 jours de navigation dans le passage de Drake</strong> (2 aller + 2 retour) et <strong>5 à 7 jours effectifs de navigation en péninsule</strong>."),
            ("p","Il est essentiel de comprendre que <strong>ces durées incluent le Drake</strong> : sur une croisière de 10 jours, vous ne voyez « l'Antarctique » que 5 à 6 jours. Les deux jours d'aller et les deux de retour se passent en haute mer sans débarquement."),
            ("img",2,"Schéma calendaire montrant la répartition Drake/péninsule sur une croisière 10 jours"),
         ]},
        {"id":"10-jours","toc":"10 jours : la classique","short":"10 jours","h2":"10 Jours : la Croisière Classique",
         "blocks":[
            ("p","C'est le <strong>format le plus courant et le plus accessible</strong>. Itinéraire type : jour 1 embarquement Ushuaia, jours 2-3 Drake, jours 4-8 péninsule (5 journées avec 2 débarquements/jour), jours 9-10 Drake retour, jour 11 débarquement Ushuaia."),
            ("h3","Ce que vous verrez"),
            ("p","Îles Shetland du Sud, détroit de Gerlache, Paradise Bay, chenal de Lemaire, Cuverville, Port Lockroy, Deception Island. C'est suffisant pour <strong>voir 3 à 4 espèces de manchots</strong>, observer des phoques, des baleines, découvrir plusieurs types de paysages glaciaires."),
            ("img",3,"Zodiac naviguant entre les glaces dans le chenal de Lemaire péninsule antarctique"),
            ("h3","Prix indicatif"),
            ("p","<strong>8 000 à 14 000 €</strong> par personne en cabine double standard selon le navire et la saison. C'est le meilleur rapport qualité/prix pour un premier voyage."),
            ("h4","Pour qui"),
            ("p","Premier voyage, temps limité (2 semaines de vacances max en comptant le trajet), budget moyen."),
         ]},
        {"id":"14-jours","toc":"14 jours : cercle polaire","short":"14 jours","h2":"14 Jours : Avec Cercle Polaire",
         "blocks":[
            ("p","Les croisières de 12 à 14 jours ajoutent une incursion au-delà du <strong>cercle polaire antarctique (66°33' S)</strong>. Il faut des glaces favorables et un navire capable de pénétrer plus au sud (Ocean Nova, Ortelius, Sea Spirit)."),
            ("h3","Ce que vous ajoutez"),
            ("p","Descente jusqu'à Marguerite Bay ou île Stonington selon la glace, passage du cercle polaire (parfois avec cérémonie à bord), colonies de manchots Adélie plus nombreuses, paysages plus extrêmes. C'est la <strong>meilleure option pour les amateurs de glace pure et de latitudes extrêmes</strong>."),
            ("img",4,"Panneau du cercle polaire antarctique franchi par un navire d'expédition"),
            ("h3","Prix indicatif"),
            ("p","<strong>11 000 à 17 000 €</strong> par personne. Le surcoût par rapport à 10 jours est proportionnel à la durée supplémentaire et à la spécificité du parcours."),
         ]},
        {"id":"20-jours","toc":"20-22 jours : Géorgie du Sud","short":"20 jours","h2":"20-22 Jours : Géorgie du Sud et Falklands",
         "blocks":[
            ("p","C'est le <strong>grand voyage de rêve</strong> : 20 à 22 jours qui incluent les <strong>îles Falklands</strong> (Malouines), la <strong>Géorgie du Sud</strong> et la <strong>péninsule Antarctique</strong>. Itinéraire classique : Ushuaia → Falklands (2 jours) → Géorgie du Sud (3 jours) → Péninsule (5 jours) → Ushuaia."),
            ("h3","Ce que vous ajoutez"),
            ("p","<strong>Manchots royaux</strong> par dizaines de milliers en Géorgie du Sud (Salisbury Plain, St Andrews Bay : les plus grandes colonies de manchots royaux au monde, 100 000+ couples), albatros hurleurs nicheurs, éléphants de mer, cimetière d'anciennes stations baleinières à Grytviken, tombe de Shackleton. C'est <strong>l'expérience ultime</strong> pour les naturalistes."),
            ("img",5,"Immense colonie de manchots royaux à Salisbury Plain en Géorgie du Sud"),
            ("h3","Prix indicatif"),
            ("p","<strong>14 000 à 22 000 €</strong> par personne. Réservez <strong>18 mois à l'avance</strong> — ces croisières se remplissent vite."),
            ("h4","Pour qui"),
            ("p","Voyageurs avertis, retraités, photographes, naturalistes. Le voyage « une fois dans sa vie » par excellence."),
         ]},
        {"id":"conseil","toc":"Quel format choisir","short":"Conseil","h2":"Quel Format Choisir ?",
         "blocks":[
            ("p","Notre recommandation dépend de votre profil."),
            ("h3","Budget moyen, 1er voyage"),
            ("p","<strong>10 jours standard</strong> : c'est largement suffisant pour ressentir l'Antarctique, voir les manchots, les phoques et les baleines, et rentrer émerveillé. La majorité des voyageurs ne font qu'un seul voyage en Antarctique dans leur vie et 10 jours les comblent."),
            ("h3","Passionné de nature"),
            ("p","<strong>20-22 jours Géorgie du Sud inclus</strong> : rien ne remplace les millions d'oiseaux et manchots royaux de Géorgie du Sud. Si vous pouvez vous le permettre en argent <em>et</em> en temps, c'est le choix naturaliste par excellence."),
            ("box","Ne partez pas pour <strong>moins de 10 jours</strong> : les croisières de 6-8 jours sur grands paquebots (type cruise only) ne débarquent pas, naviguent très loin des côtes et sont une déception garantie à ce prix. La différence de qualité avec une vraie expédition de 10 jours est énorme."),
         ]},
    ],
    "expert_tip":"Si vous hésitez entre 10 et 14 jours : <strong>prenez 14 jours si vous adorez la glace pure et les paysages extrêmes</strong>, restez à 10 jours si vous préférez la faune classique (manchots, phoques). Pour ceux qui rêvent de Géorgie du Sud : <strong>n'attendez pas</strong> — c'est la destination la plus difficile à organiser en last-minute, elle se planifie 12-18 mois à l'avance.",
})

# 9. Assurance voyage
ARTICLES.append({
    "slug": "assurance-voyage-antarctique",
    "title": "Assurance Voyage Antarctique Obligatoire : Guide Complet 2026 | Voyage 7 Continents",
    "og_title": "Assurance Antarctique Obligatoire : Rapatriement et Garanties",
    "desc": "L'assurance voyage avec évacuation médicale est obligatoire pour toute croisière antarctique. Garanties minimales, compagnies, prix : le guide pratique 2026.",
    "crumb": "Assurance Antarctique",
    "h1": "Assurance Voyage Antarctique Obligatoire",
    "lead": "Évacuation médicale 250 000 USD minimum, frais de sauvetage, annulation : l'assurance spéciale Antarctique est obligatoire. Compagnies, garanties, prix, ce qu'il faut savoir.",
    "alt1": "Hélicoptère médical d'évacuation en Antarctique avec navire d'expédition en arrière-plan",
    "caption1": "Une évacuation médicale depuis la péninsule Antarctique peut coûter plus de 250 000 USD.",
    "sections": [
        {"id":"obligatoire","toc":"Pourquoi obligatoire","short":"Pourquoi","h2":"Pourquoi l'Assurance Voyage est Obligatoire",
         "blocks":[
            ("p","Contrairement aux idées reçues, l'assurance voyage n'est pas seulement « conseillée » pour l'Antarctique : elle est <strong>strictement obligatoire</strong>. Toutes les compagnies membres de l'<a href=\"https://iaato.org/\" target=\"_blank\" rel=\"noopener nofollow\">IAATO</a> exigent la présentation d'une attestation d'assurance avec <strong>couverture médicale et rapatriement sanitaire minimale</strong> avant l'embarquement à Ushuaia."),
            ("p","La raison est simple : l'Antarctique est la zone la plus isolée au monde accessible aux touristes. Aucun hôpital, pas d'urgentiste, pas de chirurgien à bord dans la plupart des cas (les petits navires ont un médecin généraliste). En cas de problème grave, la seule solution est <strong>l'évacuation vers l'Amérique du Sud</strong>, opération qui peut coûter entre 200 000 et 500 000 USD selon les circonstances."),
            ("img",2,"Centre médical à bord d'un navire d'expédition polaire avec équipement de base"),
            ("h3","Pas de Sécurité sociale qui couvre"),
            ("p","Votre Sécurité sociale française ne couvre <strong>rien</strong> en Antarctique : ni la consultation à bord, ni une évacuation, ni une hospitalisation au Chili ou en Argentine. La carte européenne d'assurance maladie n'est valable qu'en Europe. Seule une assurance voyage privée peut vous couvrir."),
         ]},
        {"id":"garanties","toc":"Garanties minimales","short":"Garanties","h2":"Les Garanties Minimales Exigées",
         "blocks":[
            ("p","La plupart des compagnies IAATO exigent les garanties suivantes, à faire figurer <strong>explicitement</strong> sur l'attestation d'assurance fournie au moment de l'embarquement."),
            ("h3","1. Frais médicaux et rapatriement"),
            ("p","Minimum <strong>250 000 USD</strong> pour les frais médicaux et l'évacuation sanitaire. Certaines compagnies (Quark, Ponant, Silversea) exigent <strong>500 000 USD</strong> voire <strong>1 million USD</strong>. Lisez attentivement les conditions de votre opérateur."),
            ("h3","2. Frais de recherche et de sauvetage (SAR)"),
            ("p","Minimum <strong>50 000 à 100 000 USD</strong> spécifiquement couverts. Une intervention d'hélicoptère depuis un navire voisin ou une base scientifique peut coûter cette somme en quelques heures."),
            ("img",3,"Navire d'expédition polaire transférant un patient vers un navire de soins"),
            ("h3","3. Annulation et interruption"),
            ("p","Les croisières antarctiques se paient <strong>intégralement 90 à 120 jours avant le départ</strong>, non remboursable. Une garantie annulation toutes causes (Covid-19, maladie, deuil familial) est fortement recommandée — sinon vous perdez <strong>10 000 à 20 000 €</strong> en cas d'empêchement de dernière minute."),
            ("h4","4. Bagages et retard"),
            ("p","Moins critique mais utile : couverture bagages (équipement photo, vestes techniques) et retards aériens — particulièrement précieux vu le nombre de correspondances nécessaires."),
         ]},
        {"id":"compagnies","toc":"Compagnies adaptées","short":"Compagnies","h2":"Compagnies Adaptées à l'Antarctique",
         "blocks":[
            ("p","Toutes les assurances voyage classiques ne couvrent <strong>pas</strong> l'Antarctique. Il faut spécifiquement vérifier que le contrat <strong>inclut la destination « Antarctique » ou « zones polaires »</strong>. Voici les compagnies reconnues par la profession."),
            ("h3","Compagnies spécialisées expéditions"),
            ("p","<strong>Chapka Assurances</strong> (contrat Cap Aventure) : très populaire auprès des expéditions, couvre explicitement l'Antarctique jusqu'à 200 000 € de frais médicaux et 1 million d'euros de responsabilité civile. Environ <strong>6 à 9 % du prix du voyage</strong>."),
            ("p","<strong>April International</strong> (formule Multirisque Premium) : couvre polaires, plafonds élevés, annulation toutes causes en option. Environ <strong>4,5 à 7 %</strong> du prix du voyage."),
            ("p","<strong>Allianz Travel</strong>, <strong>AXA Assistance</strong>, <strong>Mondial Assistance</strong> : proposent des contrats premium qui couvrent l'Antarctique, à condition de choisir la formule « voyage grand froid » ou « expéditions »."),
            ("img",4,"Attestation d'assurance voyage antarctique imprimée et tamponnée"),
            ("h3","À éviter"),
            ("p","<strong>Les assurances incluses dans les cartes bancaires</strong> (Visa Premier, Gold Mastercard) couvrent <em>théoriquement</em> l'Antarctique mais avec des plafonds trop faibles et des exclusions majeures pour les zones polaires. <strong>Ne comptez pas dessus</strong>."),
         ]},
        {"id":"prix-budget","toc":"Prix et budget","short":"Prix","h2":"Prix et Budget à Prévoir",
         "blocks":[
            ("p","Le prix de l'assurance voyage Antarctique dépend de plusieurs facteurs : prix du voyage, âge des assurés, durée, garanties choisies."),
            ("h3","Estimation pour 2 personnes"),
            ("p","Pour un couple de 45 ans partant 14 jours en Antarctique avec une croisière à 12 000 € par personne, une assurance Chapka Cap Aventure complète (annulation + médical + rapatriement) coûte environ <strong>1 100 à 1 500 € pour les deux</strong>, soit environ 5 % du prix du voyage."),
            ("h3","Les seniors paient plus"),
            ("p","Les voyageurs de plus de 75 ans voient leur prime majorée de 30 à 80 % et peuvent rencontrer des <strong>plafonds médicaux réduits</strong>. Comparez soigneusement et déclarez toute affection préexistante (risque de non-couverture si omission)."),
            ("img",5,"Ordinateur portable affichant un comparateur d'assurances voyage expédition"),
            ("box","Demandez toujours à votre compagnie de croisière la <strong>liste exacte des garanties exigées</strong> avant de souscrire : certaines imposent par exemple une couverture « evacuation by helicopter included » explicite. Si une clause manque, votre embarquement peut vous être refusé à Ushuaia."),
         ]},
    ],
    "expert_tip":"Souscrivez votre assurance <strong>dès que vous payez l'acompte</strong> (et non à la veille du départ) : la garantie annulation ne couvre que les événements postérieurs à la souscription. Un ami qui tombe malade 3 mois avant : la garantie ne vaut que si vous étiez assuré avant sa maladie. Et gardez <strong>toujours une copie numérique de l'attestation sur votre téléphone</strong>, en plus du papier.",
})

if __name__ == "__main__":
    for a in ARTICLES:
        content = render(a)
        path = os.path.join(OUT, f'{a["slug"]}.html')
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f'wrote {path}  {len(content)} chars')
    print(f"done: {len(ARTICLES)} articles")
