#!/usr/bin/env python3
"""Generate 10 Asia articles from structured content dicts.
Each article follows the EEAT 6-point checklist; images, related block and cover
cards are handled by fetch_wikimedia.py / add_related.py / add_covers.py afterwards.
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "asie")
os.makedirs(OUT, exist_ok=True)

# ---------------- Template ----------------
HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://voyage7continents.fr/asie/{slug}.html">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <link rel="stylesheet" href="/css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{og_title}",
    "description": "{desc}",
    "author": {{"@type": "Organization", "name": "Voyage 7 Continents"}},
    "publisher": {{"@type": "Organization", "name": "Voyage 7 Continents"}},
    "datePublished": "2026-04-14",
    "dateModified": "2026-04-14"
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
          <li><a href="/asie/" class="active">Asie</a></li>
          <li><a href="/afrique/">Afrique</a></li>
          <li><a href="/amerique-nord/">Amérique du Nord</a></li>
          <li><a href="/amerique-sud/">Amérique du Sud</a></li>
          <li><a href="/oceanie/">Océanie</a></li>
          <li><a href="/antarctique/">Antarctique</a></li>
        </ul>
      </nav>
      <button class="menu-toggle" aria-label="Ouvrir le menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <section class="hero hero-pillar" style="background: linear-gradient(rgba(14,47,68,0.8), rgba(26,82,118,0.75)), url('/img/hero-asie.jpg') center/cover no-repeat;">
    <div class="hero-content">
      <div class="breadcrumb">
        <a href="/">Voyage 7 Continents</a> &rsaquo; <a href="/asie/">Asie</a> &rsaquo; <strong>{crumb}</strong>
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

      <figure class="article-hero"><img src="/img/articles/{slug}-1.jpg" alt="{alt1}" loading="lazy" width="800" height="500"><figcaption>{caption1}</figcaption></figure>

{body}

      <div class="info-box tip">
        <strong>Le conseil d'expert</strong>
        <p>{expert_tip}</p>
      </div>

      <p>Pour préparer votre voyage, retrouvez notre <a href="/asie/">guide complet Asie</a> et nos autres articles de la catégorie.</p>

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
        <p>Votre guide de référence pour voyager sur les 7 continents. Des conseils experts, des budgets détaillés et des itinéraires testés.</p>
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
      <p>&copy; 2024 Voyage 7 Continents. Tous droits réservés.</p>
    </div>
  </footer>

  <script src="/js/main.js"></script>
</body>
</html>
"""

def build_body(sections, slug):
    """sections: list of {id, h2, blocks} where blocks is list of tuples:
       ('p', text) | ('h3', text) | ('h4', text) | ('img', n, alt) | ('box', text)
    """
    out = []
    img_counter = 1  # hero is already -1
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
                n = block[1]
                alt = block[2]
                out.append(f'      <img class="article-img" src="/img/articles/{slug}-{n}.jpg" alt="{alt}" loading="lazy" width="800" height="500">')
            elif kind == "box":
                out.append(f'      <div class="info-box tip">\n        <strong>À retenir</strong>\n        <p>{block[1]}</p>\n      </div>')
        out.append("")
    return "\n".join(out)

def render(article):
    toc_items = "\n".join(
        f'          <li><a href="#{s["id"]}">{s["toc"]}</a></li>' for s in article["sections"]
    )
    sidebar_items = "\n".join(
        f'        <li><a href="#{s["id"]}">{s.get("short", s["toc"])}</a></li>' for s in article["sections"]
    )
    body = build_body(article["sections"], article["slug"])
    return HEAD.format(
        title=article["title"],
        desc=article["desc"],
        og_title=article["og_title"],
        slug=article["slug"],
        crumb=article["crumb"],
        h1=article["h1"],
        lead=article["lead"],
        alt1=article["alt1"],
        caption1=article["caption1"],
        toc_items=toc_items,
        sidebar_items=sidebar_items,
        body=body,
        expert_tip=article["expert_tip"],
    )

# ---------------- Articles ----------------
ARTICLES = []

# 1. Monnaie du Laos
ARTICLES.append({
    "slug": "monnaie-laos",
    "title": "Quelle est la monnaie du Laos ? Guide complet du Kip laotien en 2026 | Voyage 7 Continents",
    "og_title": "Quelle est la monnaie du Laos ? Guide du Kip laotien 2026",
    "desc": "La monnaie officielle du Laos est le Kip (LAK). Taux de change, billets, retraits au distributeur, dollar américain et baht thaïlandais : tout ce qu'il faut savoir.",
    "crumb": "Monnaie du Laos",
    "h1": "Quelle est la Monnaie du Laos ? Guide Complet du Kip Laotien",
    "lead": "Kip laotien, dollar, baht thaïlandais, distributeurs, pourboires : tout savoir sur l'argent au Laos pour préparer son voyage sereinement.",
    "alt1": "Billets de kips laotiens en gros plan, monnaie officielle du Laos",
    "caption1": "Le kip laotien (LAK), monnaie officielle en circulation au Laos.",
    "sections": [
        {"id":"kip-laotien","toc":"Le Kip laotien : l'essentiel","short":"Kip en bref",
         "h2":"Le Kip Laotien : l'Essentiel à Connaître",
         "blocks":[
             ("p","La <strong>monnaie officielle du Laos est le Kip laotien</strong>, dont le code international ISO 4217 est <strong>LAK</strong> et le symbole ₭. Émis par la <a href=\"https://www.bol.gov.la/en/\" target=\"_blank\" rel=\"noopener nofollow\">Banque de la République démocratique populaire lao (BCL)</a>, le kip est en circulation depuis 1952 et a remplacé plusieurs monnaies coloniales françaises successives."),
             ("h3","Billets et coupures en circulation"),
             ("p","Les billets couramment utilisés sont de <strong>500, 1 000, 2 000, 5 000, 10 000, 20 000, 50 000 et 100 000 kips</strong>. Les pièces ont quasiment disparu de la vie courante. À titre indicatif, <strong>1 € ≈ 22 000 – 24 000 kips</strong> en 2026 (vérifiez le taux du jour sur <a href=\"https://www.xe.com/fr/\" target=\"_blank\" rel=\"noopener nofollow\">XE.com</a> avant votre départ)."),
             ("h4","Astuce de conversion rapide"),
             ("p","Pour convertir mentalement un prix en euros, <strong>enlevez quatre zéros et divisez par 2,3</strong>. Exemple : 50 000 kips ≈ 2,20 €, 300 000 kips ≈ 13 €."),
         ]},
        {"id":"se-procurer-kip","toc":"Comment se procurer des kips","short":"Obtenir des kips",
         "h2":"Comment se Procurer des Kips",
         "blocks":[
             ("p","Le kip est une <strong>monnaie non convertible</strong> à l'étranger : vous ne pourrez presque jamais l'acheter depuis la France. Le change doit donc se faire sur place."),
             ("h3","Avant le départ"),
             ("p","Emportez plutôt des <strong>euros ou des dollars américains en petites coupures</strong> (billets neufs de préférence, sans marques), que vous changerez à l'arrivée. Les billets de 50 et 100 $ sont mieux valorisés que les petites coupures par les bureaux de change."),
             ("h3","À l'arrivée au Laos"),
             ("p","Trois solutions fiables : (1) <strong>bureau de change</strong> à l'aéroport de Vientiane, Luang Prabang ou Pakse (taux corrects) ; (2) <strong>distributeurs automatiques (ATM)</strong> des grandes villes, ouverts 24h/24 ; (3) <strong>banques</strong> (BCEL, Lao Development Bank, Joint Development Bank) qui offrent les meilleurs taux mais ferment à 16h."),
             ("h4","Frais de retrait au distributeur"),
             ("p","Les distributeurs laotiens facturent en général <strong>20 000 à 40 000 kips</strong> (environ 1 à 1,80 €) par retrait, plafonné à 1 500 000 – 2 000 000 kips (70 à 90 €). Prévoyez plusieurs retraits ou utilisez une carte sans frais à l'international."),
             ("img",2,"Distributeur automatique en centre-ville de Vientiane au Laos"),
         ]},
        {"id":"dollar-baht","toc":"Dollar et baht thaïlandais","short":"USD & baht",
         "h2":"Dollar Américain, Baht Thaïlandais et Euro : Acceptés ?",
         "blocks":[
             ("p","Au Laos, le <strong>dollar américain (USD)</strong> et le <strong>baht thaïlandais (THB)</strong> sont souvent acceptés comme monnaies parallèles, particulièrement dans les hôtels, agences de voyage et pour les <strong>visas à l'arrivée</strong> (qui se paient généralement en USD : 30-42 $ selon la nationalité). L'euro est accepté plus rarement, mais facilement changeable partout."),
             ("h3","Quand payer en dollars plutôt qu'en kips"),
             ("p","Pour les <strong>grosses dépenses</strong> (hôtels de catégorie supérieure, excursions organisées, visa, circuits privés), payer en dollars évite de manipuler d'immenses liasses de kips. Pour les <strong>dépenses du quotidien</strong> (restaurants, marchés, transports locaux, pourboires), le kip est indispensable."),
         ]},
        {"id":"pourboires","toc":"Prix moyens et pourboires","short":"Prix & pourboires",
         "h2":"Prix Moyens et Pourboires au Laos",
         "blocks":[
             ("p","Le Laos reste l'une des destinations les moins chères d'Asie du Sud-Est, bien que les prix aient augmenté ces dernières années."),
             ("h3","Ordres de grandeur"),
             ("p","<strong>Repas dans une gargote locale</strong> : 15 000 à 40 000 kips (0,65 – 1,80 €). <strong>Repas au restaurant touristique</strong> : 50 000 à 120 000 kips (2,25 – 5,50 €). <strong>Bière Lao (grande bouteille)</strong> : 15 000 – 25 000 kips. <strong>Nuit en guesthouse simple</strong> : 100 000 – 200 000 kips (4,50 – 9 €). <strong>Hôtel 3 étoiles</strong> : 350 000 – 700 000 kips (16 – 32 €)."),
             ("h3","Pourboires : une pratique peu ancrée"),
             ("p","Le pourboire n'est <strong>pas une tradition lao</strong>, mais il est apprécié dans les restaurants touristiques et par les guides. Comptez 10 à 15 % pour un guide privé à la journée, 10 000 – 20 000 kips pour un porteur, et l'arrondi au supérieur dans les restaurants où le service n'est pas inclus."),
         ]},
        {"id":"conseils-pratiques","toc":"Conseils pratiques d'utilisation","short":"Conseils",
         "h2":"Conseils Pratiques d'Utilisation",
         "blocks":[
             ("p","Quelques règles simples qui évitent bien des problèmes sur place."),
             ("h3","Privilégiez les petites coupures"),
             ("p","Changez votre argent en <strong>billets de 10 000 à 50 000 kips</strong> : les coupures de 100 000 kips ne sont pas toujours acceptées dans les petits commerces et les transports locaux."),
             ("h3","Vérifiez toujours votre monnaie"),
             ("p","Avec autant de zéros à lire, les erreurs de change sont fréquentes. Prenez le temps de <strong>compter les billets</strong> reçus, et gardez toujours vos plus gros billets séparés pour éviter les confusions."),
             ("h3","Risques et sécurité"),
             ("p","Le Laos est un pays sûr où les fraudes à la monnaie sont rares. Les <a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/laos/\" target=\"_blank\" rel=\"noopener nofollow\">conseils aux voyageurs de France Diplomatie</a> recommandent surtout la vigilance classique (porte-monnaie bien fermé, ne pas exhiber de grosses sommes) et de privilégier les retraits en journée dans les distributeurs situés à l'intérieur des agences bancaires."),
             ("img",3,"Marché traditionnel lao avec échanges en kips"),
         ]},
        {"id":"faq-monnaie","toc":"FAQ rapide","short":"FAQ",
         "h2":"FAQ Rapide sur la Monnaie du Laos",
         "blocks":[
             ("h3","Peut-on payer en euros au Laos ?"),
             ("p","Rarement directement, mais les euros se changent facilement partout dans les bureaux de change. Pour les dépenses locales, le kip reste indispensable."),
             ("h3","Les cartes bancaires sont-elles acceptées ?"),
             ("p","De plus en plus dans les hôtels 3-5 étoiles, les agences et les restaurants touristiques de Vientiane et Luang Prabang. En dehors, prévoyez impérativement du cash."),
             ("h3","Peut-on sortir des kips du Laos ?"),
             ("p","La réglementation autorise l'exportation jusqu'à un certain seuil, mais en pratique, <strong>changez tout votre kip restant à l'aéroport avant le départ</strong>, car il est quasiment invendable hors du pays."),
             ("h3","Que faire en cas de distributeur hors service ?"),
             ("p","Cherchez un distributeur <strong>BCEL</strong> (Banque pour le Commerce Extérieur Lao), le réseau le plus fiable et le plus répandu. En dernier recours, passez par un bureau de change qui accepte les euros ou les dollars."),
             ("img",4,"Billets de kips et dollars américains côte à côte sur un comptoir"),
             ("img",5,"Moines bouddhistes recevant l'aumône du matin à Luang Prabang"),
         ]},
    ],
    "expert_tip":"Pour votre premier jour au Laos, changez environ <strong>200 € en kips</strong> dès l'aéroport (assez pour le taxi, une nuit d'hôtel et les repas), puis utilisez les distributeurs BCEL par petits montants pour le reste du séjour. Gardez toujours 40-50 $ en billets neufs comme roue de secours : c'est la monnaie parallèle la plus fiable en cas d'urgence. Et surtout, ne changez pas tout votre argent au dernier moment, car les derniers kips sont difficiles à écouler.",
})

# 2. Vaccins Cambodge 2026
ARTICLES.append({
    "slug": "vaccins-cambodge-2026",
    "title": "Vaccins Obligatoires et Recommandés Cambodge 2026 | Voyage 7 Continents",
    "og_title": "Vaccins obligatoires Cambodge 2026 : guide complet",
    "desc": "Vaccins obligatoires et recommandés pour voyager au Cambodge en 2026 : fièvre jaune, hépatites, typhoïde, rage, encéphalite japonaise, paludisme. Guide Institut Pasteur.",
    "crumb": "Vaccins Cambodge 2026",
    "h1": "Vaccins Obligatoires et Recommandés pour le Cambodge en 2026",
    "lead": "Fièvre jaune, hépatites, typhoïde, rage, encéphalite japonaise : tout ce qu'il faut savoir pour voyager serein au Royaume du Cambodge.",
    "alt1": "Temples d'Angkor Wat au Cambodge au lever du soleil",
    "caption1": "Le Cambodge, pays d'Angkor, exige une préparation sanitaire rigoureuse.",
    "sections": [
        {"id":"vaccins-obligatoires","toc":"Vaccins obligatoires","short":"Obligatoires",
         "h2":"Vaccins Obligatoires pour Entrer au Cambodge",
         "blocks":[
             ("p","En 2026, <strong>aucun vaccin n'est obligatoire</strong> pour un voyageur français entrant directement au Cambodge depuis la France. Seule la <strong>vaccination contre la fièvre jaune</strong> est exigée si vous arrivez en provenance d'un pays où la maladie est endémique (certains pays d'Afrique et d'Amérique du Sud), conformément au Règlement sanitaire international de l'<a href=\"https://www.who.int/fr\" target=\"_blank\" rel=\"noopener nofollow\">OMS</a>."),
             ("h3","Certificat international"),
             ("p","Si la vaccination fièvre jaune est requise, elle doit être inscrite sur le <strong>carnet international de vaccination</strong> (carnet jaune OMS) et être effectuée au moins <strong>10 jours avant l'arrivée</strong> dans un centre agréé. La vaccination est désormais valable à vie depuis 2016."),
         ]},
        {"id":"vaccins-universels","toc":"Vaccins universels à jour","short":"Universels",
         "h2":"Vaccins Universels à Mettre à Jour",
         "blocks":[
             ("p","Avant tout voyage au Cambodge, l'<a href=\"https://www.pasteur.fr/fr/centre-medical/preparer-son-voyage/cambodge\" target=\"_blank\" rel=\"noopener nofollow\">Institut Pasteur</a> rappelle qu'il faut être à jour des vaccinations recommandées en France."),
             ("h3","Vaccins de base"),
             ("p","<strong>DTP (diphtérie-tétanos-poliomyélite)</strong> : rappel tous les 20 ans à l'âge adulte. <strong>Coqueluche</strong> : recommandée chez les jeunes parents. <strong>ROR (rougeole-oreillons-rubéole)</strong> : deux doses recommandées pour les personnes nées après 1980. <strong>Hépatite B</strong> : recommandée pour les séjours longs ou répétés."),
             ("img",2,"Carnet de vaccination et seringue sur un bureau médical"),
         ]},
        {"id":"vaccins-recommandes","toc":"Vaccins fortement recommandés","short":"Recommandés",
         "h2":"Vaccins Fortement Recommandés",
         "blocks":[
             ("p","Ces vaccins ne sont pas obligatoires mais sont vivement recommandés par l'Institut Pasteur et le Centre des maladies infectieuses pour les voyageurs."),
             ("h3","Hépatite A"),
             ("p","<strong>Très fortement recommandée</strong>, quelle que soit la durée du séjour. Transmission par l'eau et les aliments contaminés, courante au Cambodge. Une injection suffit pour une protection initiale, rappel à 6-12 mois pour une protection longue (10-20 ans)."),
             ("h3","Typhoïde"),
             ("p","Recommandée pour tout séjour dans des conditions d'hygiène précaires, particulièrement en zone rurale ou pour les longs séjours. Injection unique, efficace à environ 60-70 %, valable 3 ans."),
             ("h3","Rage"),
             ("p","La rage est <strong>endémique au Cambodge</strong>. Selon l'<a href=\"https://www.who.int/fr/news-room/fact-sheets/detail/rabies\" target=\"_blank\" rel=\"noopener nofollow\">OMS</a>, l'Asie compte plus de 95 % des décès mondiaux. Vaccination préventive recommandée pour séjours longs, missions humanitaires, zones rurales isolées, enfants et cyclotouristes."),
             ("h4","Et si vous êtes mordu ?"),
             ("p","Toute morsure ou griffure, même superficielle, nécessite un <strong>lavage prolongé au savon</strong> et une consultation médicale en urgence pour recevoir un traitement post-exposition. Les centres Pasteur de Phnom Penh (IPC) sont référents."),
             ("h3","Encéphalite japonaise"),
             ("p","Recommandée pour les séjours en <strong>zone rurale pendant la saison des pluies</strong> (juin à octobre) ou pour les séjours de plus d'un mois. Maladie transmise par le moustique Culex, souvent près des rizières et des élevages porcins. Deux injections espacées de 28 jours."),
             ("img",3,"Campagne cambodgienne avec rizières et élevage traditionnel"),
         ]},
        {"id":"paludisme-dengue","toc":"Paludisme et dengue","short":"Paludisme & dengue",
         "h2":"Paludisme, Dengue et Protection Contre les Moustiques",
         "blocks":[
             ("p","Aucun vaccin n'existe à ce jour contre le paludisme ou la dengue en usage courant pour le voyageur. La <strong>protection individuelle contre les piqûres de moustiques</strong> reste la seule défense efficace."),
             ("h3","Paludisme"),
             ("p","Le risque de paludisme existe dans les zones forestières, frontalières et éloignées des grands centres, particulièrement dans les régions de Pailin, Battambang, Preah Vihear et Mondulkiri. <strong>Pas de risque significatif à Phnom Penh, Siem Reap (Angkor) ni sur la côte</strong>. Une chimioprophylaxie n'est indispensable que pour certaines zones rurales ; consultez votre centre de vaccinations internationales."),
             ("h3","Dengue"),
             ("p","La <strong>dengue est présente toute l'année</strong>, avec un pic en saison des pluies (mai-octobre). Transmise par le moustique Aedes, actif de jour. Protection indispensable : vêtements longs, répulsifs à base de DEET 30-50 %, climatisation, moustiquaires imprégnées."),
         ]},
        {"id":"ou-se-faire-vacciner","toc":"Où se faire vacciner","short":"Où vacciner",
         "h2":"Où se Faire Vacciner en France",
         "blocks":[
             ("p","La vaccination contre la fièvre jaune est réservée aux <strong>centres agréés par l'ARS</strong> (Agence régionale de santé). Les vaccinations classiques peuvent être effectuées chez votre médecin traitant."),
             ("h3","Centres de référence"),
             ("p","L'<strong>Institut Pasteur de Paris, Lille, Lyon et Marseille</strong>, les centres hospitaliers universitaires, et les centres de vaccinations internationales dans la plupart des grandes villes. La liste officielle est publiée par le <a href=\"https://solidarites-sante.gouv.fr/\" target=\"_blank\" rel=\"noopener nofollow\">ministère de la Santé</a>."),
             ("h3","Quand s'y prendre"),
             ("p","Consultez <strong>4 à 8 semaines avant le départ</strong>, car certains vaccins (hépatite B, encéphalite japonaise, rage en préventif) nécessitent plusieurs injections étalées sur plusieurs semaines."),
             ("h3","Coût et remboursement"),
             ("p","Les vaccins universels (DTP, ROR, hépatite B) sont remboursés par la Sécurité sociale. Les vaccins spécifiques au voyage (hépatite A, typhoïde, encéphalite japonaise, rage, fièvre jaune) sont <strong>rarement remboursés</strong> et coûtent entre 30 et 100 € par dose. Certaines mutuelles les prennent partiellement en charge."),
         ]},
        {"id":"trousse-pharmacie","toc":"Trousse à pharmacie","short":"Trousse",
         "h2":"Trousse à Pharmacie Conseillée",
         "blocks":[
             ("p","Au-delà des vaccins, une <strong>trousse de voyage</strong> adaptée vous évitera bien des désagréments."),
             ("h3","Incontournables"),
             ("p","Paracétamol, anti-diarrhéiques, antispasmodiques, antibiotiques à large spectre sur ordonnance, pansements, désinfectant, répulsif moustiques DEET 30-50 %, crème solaire haute protection, sels de réhydratation oraux, traitement de l'eau (Micropur), préservatifs. Les <a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/cambodge/\" target=\"_blank\" rel=\"noopener nofollow\">conseils aux voyageurs de France Diplomatie</a> recommandent également de souscrire une assurance rapatriement."),
             ("img",4,"Trousse de pharmacie de voyage avec médicaments et pansements"),
             ("img",5,"Infirmière préparant un vaccin pour un voyageur avant départ"),
         ]},
    ],
    "expert_tip":"Ne sous-estimez pas la <strong>consultation préalable chez un médecin de voyage</strong> : 30 minutes avec un spécialiste de l'Institut Pasteur vous fera économiser des heures de recherche et adaptera précisément les vaccins à votre itinéraire, à votre durée de séjour et à votre profil médical. Pensez aussi à vérifier votre <strong>carte européenne d'assurance maladie</strong> (inutile hors UE) et souscrivez une assurance voyage incluant rapatriement sanitaire : les hôpitaux français de référence sont à Bangkok ou Singapour.",
})

# 3. Décalage horaire Ouzbékistan
ARTICLES.append({
    "slug": "decalage-horaire-ouzbekistan",
    "title": "Décalage Horaire France-Ouzbékistan : Guide Complet 2026 | Voyage 7 Continents",
    "og_title": "Décalage horaire France-Ouzbékistan : guide complet",
    "desc": "Décalage horaire exact entre la France et l'Ouzbékistan : UTC+5, 4h ou 5h de décalage selon la saison. Fuseau, jet lag, vols : tout pour bien préparer son voyage.",
    "crumb": "Décalage horaire Ouzbékistan",
    "h1": "Décalage Horaire France-Ouzbékistan : Tout Savoir",
    "lead": "UTC+5 toute l'année, 4 à 5 heures d'avance sur Paris selon la saison : décryptage complet du fuseau horaire ouzbek et conseils jet lag.",
    "alt1": "Place du Registan à Samarcande en Ouzbékistan au coucher du soleil",
    "caption1": "Samarcande et l'Ouzbékistan : UTC+5, sans changement d'heure.",
    "sections": [
        {"id":"decalage-exact","toc":"Le décalage horaire exact","short":"Décalage exact",
         "h2":"Le Décalage Horaire Exact entre la France et l'Ouzbékistan",
         "blocks":[
             ("p","L'Ouzbékistan se trouve en fuseau horaire <strong>UTC+5</strong> (aussi appelé Uzbekistan Standard Time, UZT), toute l'année, <strong>sans heure d'été</strong>. Le pays a aboli le changement d'heure saisonnier en 2005. La base de données de référence <a href=\"https://www.iana.org/time-zones\" target=\"_blank\" rel=\"noopener nofollow\">IANA tzdata</a> liste l'Ouzbékistan sous l'identifiant <em>Asia/Tashkent</em>."),
             ("h3","Côté France"),
             ("p","La France métropolitaine applique encore le changement d'heure : UTC+1 en hiver (heure d'hiver), UTC+2 en été (heure d'été). Résultat : le décalage avec l'Ouzbékistan n'est pas constant."),
             ("h3","Décalage concret en 2026"),
             ("p","<strong>Heure d'hiver en France (fin octobre → fin mars)</strong> : l'Ouzbékistan est à <strong>+4 heures</strong>. Quand il est midi à Paris, il est 16h à Tachkent. <strong>Heure d'été en France (fin mars → fin octobre)</strong> : l'Ouzbékistan est à <strong>+4 heures</strong> également (UTC+5 face à UTC+2). Attendez, vérifions : UTC+5 − UTC+2 = 3 heures. Donc en été, le décalage tombe à <strong>+3 heures</strong>."),
             ("h4","Règle simple à retenir"),
             ("p","<strong>+4 h en hiver</strong>, <strong>+3 h en été</strong>. Quand il est 12h00 à Paris en juillet, il est 15h00 à Tachkent ; en décembre, il est 16h00."),
         ]},
        {"id":"heure-locale","toc":"L'heure locale en Ouzbékistan","short":"Heure locale",
         "h2":"L'Heure Locale en Ouzbékistan",
         "blocks":[
             ("p","L'Ouzbékistan étant un pays de plus de 1 500 km d'est en ouest, on pourrait s'attendre à plusieurs fuseaux horaires. Pourtant, <strong>tout le pays vit à la même heure (UTC+5)</strong>, ce qui donne un lever de soleil très tardif à l'ouest (Noukous, Khiva) et un coucher très tôt à l'est (Tachkent, vallée de Ferghana)."),
             ("h3","Lever et coucher du soleil"),
             ("p","En été, le soleil se lève vers 5h00 à Tachkent et se couche vers 20h15. En hiver, lever vers 7h30 et coucher vers 17h30. Les journées à Samarcande et Boukhara sont légèrement plus tardives."),
             ("img",2,"Madrassa Mir-i-Arab à Boukhara en Ouzbékistan"),
         ]},
        {"id":"jet-lag","toc":"Gérer le jet lag","short":"Jet lag",
         "h2":"Gérer le Jet Lag sur un Vol France-Ouzbékistan",
         "blocks":[
             ("p","Un décalage de 3 à 4 heures vers l'est est considéré comme <strong>léger</strong>, mais il peut tout de même perturber votre sommeil les 2 à 3 premiers jours si vous n'anticipez pas un peu."),
             ("h3","Avant le départ"),
             ("p","Commencez à <strong>décaler votre heure de coucher de 30 minutes à 1 heure plus tôt</strong> les 3 jours précédant le vol. Évitez l'alcool et les repas trop copieux la veille du départ. Emportez des bouchons d'oreilles et un masque de sommeil pour le vol."),
             ("h3","Pendant le vol"),
             ("p","Réglez votre montre sur l'heure locale de destination dès le décollage. <strong>Buvez beaucoup d'eau</strong> et évitez café et alcool. Bougez régulièrement (toilettes, étirements) pour prévenir les thromboses et la fatigue musculaire."),
             ("h3","À l'arrivée"),
             ("p","Exposez-vous à la <strong>lumière naturelle dès le matin</strong> et évitez les siestes longues (max 30 minutes). Couchez-vous à l'heure locale même si vous ne tombez pas encore de fatigue. Un décalage vers l'est est toujours plus difficile qu'un décalage vers l'ouest : soyez patient, votre rythme reviendra en 48-72 h."),
             ("h4","Exposition à la lumière"),
             ("p","L'<a href=\"https://www.inserm.fr/\" target=\"_blank\" rel=\"noopener nofollow\">Inserm</a> rappelle que la lumière du matin est le signal le plus puissant pour resynchroniser votre horloge biologique. Sortez prendre un petit-déjeuner en terrasse dès votre premier matin à Tachkent ou Samarcande."),
         ]},
        {"id":"vols-france","toc":"Vols depuis la France","short":"Vols",
         "h2":"Vols depuis la France vers l'Ouzbékistan",
         "blocks":[
             ("p","Il existe des vols directs et indirects entre la France et l'Ouzbékistan. La compagnie nationale <strong>Uzbekistan Airways</strong> opère des liaisons saisonnières Paris-Tachkent en 6h30-7h de vol. Turkish Airlines (via Istanbul), Aeroflot (via Moscou, selon la situation géopolitique) et FlyDubai (via Dubaï) proposent aussi des trajets compétitifs."),
             ("h3","Durée moyenne du vol"),
             ("p","Comptez <strong>6h30 en direct</strong>, 10 à 14 h avec une escale. Le décalage modéré rend le voyage assez confortable, même pour un premier long-courrier."),
             ("img",3,"Avion Uzbekistan Airways décollant de l'aéroport de Tachkent"),
         ]},
        {"id":"pays-voisins","toc":"Décalage avec les pays voisins","short":"Pays voisins",
         "h2":"Décalage avec les Pays Voisins",
         "blocks":[
             ("p","Si vous combinez l'Ouzbékistan avec d'autres pays d'Asie centrale, attention aux petits décalages entre voisins, qui peuvent surprendre."),
             ("h3","Pays à la même heure"),
             ("p","Le <strong>Turkménistan</strong>, le <strong>Tadjikistan</strong> et le <strong>Pakistan</strong> sont aussi à UTC+5. Pas de décalage en traversant les frontières de ces pays."),
             ("h3","Kazakhstan : attention"),
             ("p","Le <strong>Kazakhstan</strong> est à UTC+5 dans l'ouest et UTC+6 dans l'est. Si vous allez à Almaty depuis Tachkent, <strong>avancez votre montre d'une heure</strong>. Le <strong>Kirghizistan</strong> est à UTC+6 : également une heure d'avance."),
             ("img",4,"Gare ferroviaire de Tachkent avec horloge digitale"),
             ("img",5,"Désert du Kyzylkoum en Ouzbékistan au lever du jour"),
         ]},
    ],
    "expert_tip":"Pour un premier voyage en Ouzbékistan, <strong>partez en fin d'après-midi depuis Paris</strong> : vous arriverez à Tachkent le lendemain matin, ce qui vous laisse une journée entière pour récupérer à l'heure locale. Commencez par une balade tranquille au parc Amir Timur, un bon repas (avec plov, la spécialité nationale), puis couchez-vous vers 22h heure locale. Vous serez parfaitement synchronisé dès le deuxième jour, prêt pour Samarcande, Boukhara et Khiva.",
})

# 4. Hanoï-Sapa pas cher
ARTICLES.append({
    "slug": "hanoi-sapa-pas-cher",
    "title": "Comment Aller de Hanoï à Sapa Pas Cher en 2026 | Voyage 7 Continents",
    "og_title": "Comment aller de Hanoï à Sapa pas cher : guide 2026",
    "desc": "Guide complet pour rejoindre Sapa depuis Hanoï en 2026 : bus couchette (12 €), train de nuit, minibus, voiture privée. Durée, prix, réservation et astuces d'économie.",
    "crumb": "Hanoï → Sapa pas cher",
    "h1": "Comment Aller de Hanoï à Sapa Pas Cher en 2026",
    "lead": "Bus couchette, train de nuit, minibus, voiture privée : toutes les options pour rejoindre Sapa depuis Hanoï sans se ruiner.",
    "alt1": "Rizières en terrasse de Sapa au nord du Vietnam",
    "caption1": "Les célèbres rizières en terrasse de Sapa, destination incontournable du nord Vietnam.",
    "sections": [
        {"id":"options","toc":"Les 4 options pour aller à Sapa","short":"Les options",
         "h2":"Les 4 Options pour Rejoindre Sapa depuis Hanoï",
         "blocks":[
             ("p","Sapa se trouve à <strong>environ 320 km au nord-ouest de Hanoï</strong>, dans la province de Lào Cai. Depuis l'ouverture de l'autoroute Nội Bài-Lào Cai en 2014, le trajet est beaucoup plus rapide qu'auparavant. Quatre moyens de transport principaux sont disponibles, avec des prix allant de 10 € à 120 € selon le confort."),
             ("h3","Comparatif rapide"),
             ("p","<strong>Bus couchette</strong> : 10-18 €, 5h30-6h de route, le meilleur rapport qualité-prix. <strong>Train de nuit + navette</strong> : 25-70 €, 8h + 1h, charmant mais plus lent. <strong>Minibus direct</strong> : 15-25 €, 5h30, option intermédiaire. <strong>Voiture privée</strong> : 80-120 €, 5h, flexibilité totale pour les familles ou groupes."),
         ]},
        {"id":"bus-couchette","toc":"Bus couchette : l'option pas chère","short":"Bus couchette",
         "h2":"Bus Couchette : la Meilleure Option Pas Chère",
         "blocks":[
             ("p","Le <strong>bus couchette</strong> (<em>sleeper bus</em>) est de loin la solution la plus économique et la plus confortable pour rejoindre Sapa depuis Hanoï. Les compagnies modernes proposent des bus à 2 étages de couchettes individuelles inclinables, avec couverture, bouteille d'eau, Wi-Fi à bord et prises USB."),
             ("h3","Meilleures compagnies"),
             ("p","<strong>Sapa Express</strong>, <strong>Interbus Lines</strong>, <strong>Green Bus</strong>, <strong>Ecosapa</strong> et <strong>Kingexpress</strong> dominent le marché et offrent un service de qualité équivalente. Réservez votre billet via <a href=\"https://12go.asia/fr\" target=\"_blank\" rel=\"noopener nofollow\">12Go Asia</a>, <a href=\"https://www.bookaway.com/\" target=\"_blank\" rel=\"noopener nofollow\">Bookaway</a> ou directement aux guichets d'hôtels du vieux quartier de Hanoï."),
             ("h3","Tarifs"),
             ("p","<strong>10 à 12 €</strong> pour un bus standard, <strong>15 à 18 €</strong> pour un bus VIP (cabines individuelles fermées, plus de confort). Les bus VIP sont fortement recommandés pour un trajet de nuit."),
             ("h3","Durée et horaires"),
             ("p","Le trajet dure <strong>5h30 à 6 heures</strong> sur l'autoroute. Les bus partent de Hanoï toutes les 1-2 heures en journée (7h à 16h) et de nuit (22h-23h pour arriver à Sapa au lever du jour). Point de départ : généralement devant les hôtels du vieux quartier (ramassage gratuit)."),
             ("h4","Conseil horaire"),
             ("p","Privilégiez le <strong>bus de nuit</strong> : vous économisez une nuit d'hôtel et arrivez à Sapa au lever du soleil, pile pour un petit-déjeuner avec vue sur les montagnes. Attention : le bus de nuit arrive vers 4h-5h du matin, trop tôt pour l'enregistrement en hôtel (check-in souvent à partir de 14h). Demandez à votre hébergement de stocker vos bagages et allez directement observer le lever du soleil."),
             ("img",2,"Intérieur d'un bus couchette vietnamien avec cabines individuelles"),
         ]},
        {"id":"train-nuit","toc":"Train de nuit Hanoi-Lao Cai","short":"Train de nuit",
         "h2":"Le Train de Nuit Hanoï-Lào Cai",
         "blocks":[
             ("p","Option historique, le <strong>train de nuit</strong> est plus long et plus cher que le bus, mais offre une expérience charmante pour qui aime le voyage ferroviaire à l'ancienne."),
             ("h3","Itinéraire"),
             ("p","Le train n'arrive pas directement à Sapa mais à <strong>Lào Cai</strong>, à 38 km. Il faut ensuite prendre un minibus ou un taxi (1h, 3 à 6 €) pour grimper jusqu'à Sapa. Les trains sont opérés par les <a href=\"https://dsvn.vn/\" target=\"_blank\" rel=\"noopener nofollow\">Chemins de fer vietnamiens (Vietnam Railways)</a>."),
             ("h3","Trains touristiques vs train standard"),
             ("p","Deux options : le <strong>train standard SP</strong> (cabines 4 ou 6 couchettes, 18-30 €) et les <strong>trains touristiques privés</strong> (Chapa Express, Sapaly, Fansipan, 40-70 €) avec cabines en bois plus confortables."),
             ("h3","Horaires"),
             ("p","Trains principalement de nuit (départ Hanoï 22h, arrivée Lào Cai 6h). Comptez <strong>8 heures de trajet</strong> pour environ 300 km."),
         ]},
        {"id":"minibus","toc":"Minibus direct","short":"Minibus",
         "h2":"Le Minibus Direct",
         "blocks":[
             ("p","Alternative intermédiaire entre bus couchette et voiture privée, le <strong>minibus direct</strong> transporte 9 à 16 passagers depuis Hanoï jusqu'au centre de Sapa."),
             ("h3","Avantages"),
             ("p","Moins de monde qu'un bus classique, sièges plus confortables, ramassage devant l'hôtel, durée équivalente au bus couchette (5h30-6h). Compter <strong>15 à 25 €</strong>."),
             ("h3","Inconvénients"),
             ("p","Pas de couchettes, donc peu adapté aux trajets de nuit. Arrêts fréquents, ce qui peut rallonger le trajet. Certaines compagnies sont moins fiables : préférez les grandes (Good Morning Sapa, Green Lion)."),
             ("img",3,"Minibus de tourisme garé à Sapa avec vue sur les montagnes"),
         ]},
        {"id":"voiture-privee","toc":"Voiture privée","short":"Voiture privée",
         "h2":"La Voiture Privée avec Chauffeur",
         "blocks":[
             ("p","Pour les <strong>familles, groupes ou voyageurs avec beaucoup de bagages</strong>, la voiture privée avec chauffeur reste une option confortable même si elle coûte plus cher."),
             ("h3","Tarifs et prestataires"),
             ("p","Comptez <strong>80 à 120 €</strong> le trajet pour une berline 4 places, 130 à 180 € pour un minivan 7 places. Prestataires recommandés : Vietnam Easy Rider, Hanoi Private Car, ou les comptoirs des hôtels du vieux quartier."),
             ("h3","Quand choisir cette option"),
             ("p","Si vous <strong>voyagez en famille avec de jeunes enfants</strong>, si vous souhaitez <strong>vous arrêter en route</strong> (marché de Bac Ha, Muong Khuong), ou si vous avez un <strong>horaire d'avion serré</strong> au retour."),
         ]},
        {"id":"astuces","toc":"Astuces pour économiser","short":"Astuces économies",
         "h2":"Astuces pour Économiser sur le Trajet",
         "blocks":[
             ("p","Quelques conseils simples peuvent faire baisser la facture de 20 à 40 %."),
             ("h3","Réservez à l'avance"),
             ("p","En réservant <strong>5-7 jours à l'avance</strong> via 12Go ou Bookaway, vous bénéficiez souvent de réductions de 10-20 % par rapport à l'achat du jour. Les dates les plus demandées sont les week-ends et les vacances scolaires vietnamiennes."),
             ("h3","Évitez les haute saisons vietnamiennes"),
             ("p","<strong>Tết (Nouvel An lunaire), jours fériés vietnamiens et la saison des rizières dorées (septembre-octobre)</strong> font grimper les prix de 20-50 %. Privilégiez mai-juin ou novembre pour le meilleur rapport prix-climat."),
             ("h3","Combinez bus et train"),
             ("p","Aller en bus couchette (10 €) et revenir en train touristique (30-40 €) vous permet de vivre les deux expériences pour <strong>moins de 60 € aller-retour</strong>, moins cher qu'un seul aller simple en voiture privée."),
             ("img",4,"Gare ferroviaire de Lào Cai au nord du Vietnam"),
             ("img",5,"Femme Hmong en tenue traditionnelle à Sapa"),
         ]},
    ],
    "expert_tip":"La <strong>formule gagnante</strong> pour voir Sapa à petit budget : départ de Hanoï en <strong>bus couchette de nuit vers 22h</strong> (12 €), arrivée à Sapa vers 4h-5h du matin, observation du lever du soleil sur les rizières, petit-déjeuner en terrasse, puis check-in à l'hôtel après une balade. Pour le retour, prenez un <strong>bus de jour vers 13h</strong> pour profiter du paysage : vous verrez la transition entre les montagnes du nord et le delta du Fleuve Rouge. Trois nuits à Sapa est le minimum pour profiter des meilleures randonnées (vallée de Muong Hoa, Cat Cat, Y Linh Ho) sans être pressé.",
})

# 5. Température Bhoutan novembre
ARTICLES.append({
    "slug": "temperature-bhoutan-novembre",
    "title": "Température Moyenne au Bhoutan en Novembre : Climat et Conseils | Voyage 7 Continents",
    "og_title": "Température moyenne Bhoutan novembre : climat complet",
    "desc": "Températures moyennes au Bhoutan en novembre ville par ville, climat, vêtements, festival Jambay Lhakhang Drup et conseils de randonnée au Tiger's Nest.",
    "crumb": "Climat Bhoutan en novembre",
    "h1": "Température Moyenne au Bhoutan en Novembre : Climat et Conseils",
    "lead": "Ciel bleu, fraîcheur modérée, montagnes cristallines : novembre est considéré comme la meilleure période pour voyager au Bhoutan.",
    "alt1": "Monastère Taktsang (Tiger's Nest) perché sur une falaise du Bhoutan",
    "caption1": "Le Tiger's Nest, symbole du Bhoutan, par un ciel limpide de novembre.",
    "sections": [
        {"id":"temperatures-ville","toc":"Températures par ville","short":"Par ville",
         "h2":"Températures Moyennes en Novembre Ville par Ville",
         "blocks":[
             ("p","Les températures au Bhoutan varient énormément selon l'altitude. Les données ci-dessous, issues du <a href=\"https://www.nchm.gov.bt/\" target=\"_blank\" rel=\"noopener nofollow\">National Center for Hydrology and Meteorology (NCHM) du Bhoutan</a>, donnent une moyenne pour novembre sur les 10 dernières années."),
             ("h3","Vallée de Paro (2 250 m)"),
             ("p","<strong>Max moyen : 13-15 °C, min moyen : 0-2 °C</strong>. C'est là que vous atterrirez (seul aéroport international du pays) et que se trouve le Tiger's Nest. Journées lumineuses et fraîches, nuits froides."),
             ("h3","Thimphu (2 320 m)"),
             ("p","<strong>Max moyen : 14-16 °C, min moyen : 1-3 °C</strong>. La capitale connaît les mêmes conditions que Paro. L'humidité est basse, l'air particulièrement clair."),
             ("h3","Punakha (1 250 m)"),
             ("p","<strong>Max moyen : 20-23 °C, min moyen : 8-11 °C</strong>. Plus bas en altitude, la vallée de Punakha est nettement plus chaude et agréable le soir. Idéale pour une soirée en terrasse."),
             ("h3","Bumthang (2 600 m)"),
             ("p","<strong>Max moyen : 12-14 °C, min moyen : -2 à 0 °C</strong>. La vallée centrale des monastères : les nuits sont franchement froides, et on peut observer les premières gelées matinales."),
             ("h3","Phuentsholing (300 m)"),
             ("p","<strong>Max moyen : 25-27 °C, min moyen : 14-16 °C</strong>. Poste frontière avec l'Inde, dans les basses terres. Climat subtropical, températures estivales même en novembre."),
             ("img",2,"Vallée de Thimphu au Bhoutan à l'automne"),
         ]},
        {"id":"pourquoi-novembre","toc":"Pourquoi novembre est idéal","short":"Pourquoi novembre",
         "h2":"Pourquoi Novembre est Considéré comme le Meilleur Mois",
         "blocks":[
             ("p","Le Bhoutan est classé par de nombreux guides comme l'une des meilleures destinations de novembre en Asie. Plusieurs raisons l'expliquent."),
             ("h3","Ciel limpide et vues himalayennes"),
             ("p","La mousson est terminée depuis septembre, l'atmosphère est <strong>lavée et cristalline</strong>. Les sommets himalayens sont visibles dans leur gloire depuis les cols de Dochula et Chele La. La visibilité peut dépasser 100 km."),
             ("h3","Pas de pluie"),
             ("p","Novembre est l'un des mois les plus secs de l'année : <strong>moins de 10 mm de précipitations</strong> en moyenne à Thimphu et Paro. Les sentiers sont praticables, les vols rarement annulés."),
             ("h3","Affluence raisonnable"),
             ("p","Contrairement à octobre (pic touristique lié au festival de Thimphu Tshechu), novembre voit la fréquentation baisser tout en conservant un climat idéal. Les permis sont plus faciles à obtenir, les hôtels moins chers."),
         ]},
        {"id":"vetements","toc":"Quoi mettre dans sa valise","short":"Valise",
         "h2":"Quoi Mettre dans sa Valise pour le Bhoutan en Novembre",
         "blocks":[
             ("p","Avec des écarts de 15-20 °C entre le jour et la nuit, et selon l'altitude, le maître-mot est <strong>le système multicouches</strong>."),
             ("h3","Couches vestimentaires"),
             ("p","<strong>Sous-couche thermique</strong> (mérinos ou synthétique), <strong>polaire légère et polaire épaisse</strong> pour l'isolation, <strong>veste coupe-vent imperméable</strong> type softshell ou Gore-Tex, <strong>doudoune légère</strong> (600-700 plumes) pour les soirées et les cols. Un bonnet, une écharpe tube et des gants fins sont indispensables."),
             ("h3","Chaussures"),
             ("p","<strong>Chaussures de randonnée mi-hautes imperméables</strong>, bien cassées avant le départ. Elles serviront pour la montée au Tiger's Nest, les balades dans les monastères et les sentiers de vallée. Prévoyez aussi des baskets confortables pour les villes."),
             ("h3","Accessoires indispensables"),
             ("p","<strong>Lunettes de soleil catégorie 3-4</strong> (l'altitude amplifie la réverbération), <strong>crème solaire SPF 30+</strong>, <strong>baume pour les lèvres</strong>, gourde isotherme, lampe frontale (coupures d'électricité fréquentes en montagne). Pensez aussi à un <strong>adaptateur prise type D/G</strong> (identique à l'Inde) et à une <strong>batterie externe</strong>."),
             ("img",3,"Randonneur équipé sur un sentier bhoutanais en automne"),
         ]},
        {"id":"festival-novembre","toc":"Festival de novembre","short":"Festival",
         "h2":"Le Festival Jambay Lhakhang Drup",
         "blocks":[
             ("p","Novembre est aussi le mois d'un des festivals bouddhistes les plus singuliers du Bhoutan : <strong>Jambay Lhakhang Drup</strong>, dans la vallée de Bumthang."),
             ("h3","Quand et où"),
             ("p","Généralement organisé <strong>autour de la pleine lune de novembre</strong> (dates fixées selon le calendrier lunaire tibétain), il se déroule dans le temple Jambay Lhakhang, l'un des plus anciens du Bhoutan (construit au VIIe siècle)."),
             ("h3","Le célèbre 'Mewang' et 'Tercham'"),
             ("p","Le festival est célèbre pour deux rituels uniques : le <strong>Mewang</strong> (danse du feu, les pèlerins passent sous une arche de flammes pour être purifiés), et le <strong>Tercham</strong> (danse nue sacrée à minuit), rite de fertilité très ancien interdit aux photographes. Ces cérémonies sont documentées par le <a href=\"https://www.bhutan.travel/\" target=\"_blank\" rel=\"noopener nofollow\">Conseil du Tourisme du Bhoutan (Tourism Council of Bhutan)</a>."),
         ]},
        {"id":"randonnee-tiger-nest","toc":"Randonnée au Tiger's Nest","short":"Tiger's Nest",
         "h2":"Randonnée au Tiger's Nest en Novembre",
         "blocks":[
             ("p","L'ascension du monastère de <strong>Taktsang Palphug</strong>, surnommé Tiger's Nest, est l'activité incontournable de tout voyage au Bhoutan. En novembre, les conditions sont <strong>idéales</strong>."),
             ("h3","Profil de la randonnée"),
             ("p","Départ à 2 600 m, arrivée au monastère à 3 120 m. <strong>Dénivelé positif : environ 520 m, durée : 4 à 5 heures aller-retour</strong>, sentier bien tracé mais rocailleux par endroits. En novembre, pas de boue ni de passages verglacés : les conditions les plus sûres de l'année."),
             ("h3","Conseil horaire"),
             ("p","Partez <strong>à 7h-7h30</strong> au plus tard pour éviter la foule et l'effort en plein soleil. Le monastère ouvre à 8h30. Emportez 1,5 L d'eau par personne, une collation, et vos papiers (contrôle de sécurité à l'entrée du temple)."),
             ("img",4,"Randonneurs en chemin vers le monastère Tiger's Nest au Bhoutan"),
             ("img",5,"Paysage himalayen du Bhoutan avec sommets enneigés"),
         ]},
    ],
    "expert_tip":"Pour votre <strong>premier jour à Paro</strong>, résistez à la tentation de monter immédiatement au Tiger's Nest : le décalage horaire et l'altitude ont besoin de 24 heures d'acclimatation. Passez d'abord la journée à Paro ou Thimphu (visites du Dzong de Paro, musée national, marché du weekend), puis faites le Tiger's Nest le <strong>deuxième jour au réveil</strong>, parfaitement reposé. Vous apprécierez bien plus l'expérience, et vous réduirez le risque de mal des montagnes — rare mais possible au-dessus de 3 000 m.",
})

# 6. Danger Kirghizistan
ARTICLES.append({
    "slug": "danger-kirghizistan",
    "title": "Est-ce Dangereux de Voyager au Kirghizistan ? Bilan Sécurité 2026 | Voyage 7 Continents",
    "og_title": "Est-ce dangereux de voyager au Kirghizistan ? 2026",
    "desc": "Le Kirghizistan est-il sûr pour les voyageurs en 2026 ? Bilan complet : zones à éviter, délinquance, routes, altitude, conseils France Diplomatie et FCDO.",
    "crumb": "Kirghizistan : danger ?",
    "h1": "Est-ce Dangereux de Voyager au Kirghizistan ? Bilan Sécurité 2026",
    "lead": "Zones à éviter, délinquance, sécurité routière, altitude : bilan complet et honnête sur la sécurité au Kirghizistan pour voyager serein.",
    "alt1": "Yourtes traditionnelles au bord du lac Song Kul au Kirghizistan",
    "caption1": "Le lac Song Kul et ses yourtes : le Kirghizistan, destination globalement sûre et accueillante.",
    "sections": [
        {"id":"reponse-rapide","toc":"Réponse rapide","short":"Réponse rapide",
         "h2":"Réponse Rapide : Globalement Sûr",
         "blocks":[
             ("p","<strong>Oui, le Kirghizistan est un pays globalement sûr pour les voyageurs</strong>, y compris pour les voyageurs en solo, les femmes et les familles. C'est d'ailleurs l'une des destinations émergentes les plus appréciées d'Asie centrale, avec une forte croissance touristique ces cinq dernières années. Le pays apparaît en zone jaune clair (vigilance normale) dans la carte des conseils aux voyageurs de nombreuses chancelleries occidentales."),
             ("h3","Les chiffres clés"),
             ("p","Selon le <a href=\"https://www.visionofhumanity.org/maps/\" target=\"_blank\" rel=\"noopener nofollow\">Global Peace Index</a> de l'Institute for Economics &amp; Peace, le Kirghizistan se classe autour du 100e rang mondial (sur 163 pays), soit un niveau de paix comparable à plusieurs pays d'Amérique latine et nettement meilleur que la plupart des pays du Moyen-Orient. Le principal risque pour les voyageurs reste la <strong>sécurité routière</strong>, pas la criminalité."),
         ]},
        {"id":"autorites","toc":"Ce que disent les autorités","short":"Autorités",
         "h2":"Ce que Disent les Autorités",
         "blocks":[
             ("h3","France Diplomatie"),
             ("p","Les <a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/kirghizistan/\" target=\"_blank\" rel=\"noopener nofollow\">conseils aux voyageurs de France Diplomatie</a> classent en 2026 la majorité du territoire en <strong>« vigilance normale »</strong>, à l'exception de certaines zones frontalières avec le Tadjikistan et l'Ouzbékistan (vallée de Ferghana, Batken), classées en « vigilance renforcée » en raison de tensions sporadiques."),
             ("h3","UK FCDO"),
             ("p","Le <a href=\"https://www.gov.uk/foreign-travel-advice/kyrgyzstan\" target=\"_blank\" rel=\"noopener nofollow\">Foreign, Commonwealth &amp; Development Office britannique</a> émet des conseils similaires : voyages possibles dans tout le pays, vigilance renforcée aux frontières Batken-Tadjikistan et pendant les rassemblements politiques à Bichkek."),
             ("h3","US State Department"),
             ("p","Les États-Unis placent le pays en <strong>niveau 2 (exercer une vigilance accrue)</strong> sur une échelle de 4, avec les mêmes recommandations concernant certaines zones frontalières."),
         ]},
        {"id":"zones-eviter","toc":"Zones à éviter","short":"Zones à éviter",
         "h2":"Zones à Éviter ou à Aborder avec Prudence",
         "blocks":[
             ("p","Ces zones représentent une fraction minime du territoire et n'affectent pas les itinéraires touristiques classiques (Bichkek, Issyk Kul, Karakol, Song Kul, Tash Rabat)."),
             ("h3","Frontière tadjike (région de Batken)"),
             ("p","Des <strong>incidents frontaliers</strong> entre le Kirghizistan et le Tadjikistan ont eu lieu entre 2021 et 2023 dans la région de Batken. La situation s'est apaisée depuis la signature d'accords de démarcation, mais la zone reste classée en vigilance renforcée. En pratique, <strong>évitez de camper à proximité immédiate de la frontière</strong> et respectez les consignes locales."),
             ("h3","Certaines zones de la vallée de Ferghana"),
             ("p","La partie kirghize de la <strong>vallée de Ferghana</strong> (frontière ouzbèke) a connu des tensions ethniques par le passé. Les villes d'Och et Djalal-Abad sont aujourd'hui sûres et accueillantes pour les touristes, mais <strong>évitez les rassemblements politiques</strong> et les mouvements de foule."),
         ]},
        {"id":"risques-reels","toc":"Risques réels","short":"Vrais risques",
         "h2":"Les Risques Réels pour un Voyageur",
         "blocks":[
             ("p","Plutôt que la sécurité au sens strict, ce sont d'autres risques qui menacent les voyageurs au Kirghizistan."),
             ("h3","Sécurité routière"),
             ("p","C'est, de loin, <strong>le principal danger</strong> au Kirghizistan. Les routes de montagne sont étroites, sinueuses, souvent en mauvais état. Les conducteurs locaux roulent vite, dépassent dans les virages, et les marshrutki (minibus collectifs) sont connus pour être fatigants et peu confortables. Privilégiez les <strong>transports affrétés par des agences sérieuses</strong> pour les longs trajets et les cols de haute altitude."),
             ("h3","Altitude"),
             ("p","De nombreux itinéraires passent au-dessus de <strong>3 000 m</strong> (col de Tosor, Ala-Kul, Pic Lénine à 7 134 m). Le mal des montagnes touche aussi les randonneurs habitués. Acclimatez-vous progressivement et renseignez-vous sur les signes d'œdème. Les guides kirghizes expérimentés suivent les recommandations de l'<a href=\"https://www.theuiaa.org/medical/\" target=\"_blank\" rel=\"noopener nofollow\">UIAA (Union internationale des associations d'alpinisme)</a>."),
             ("h3","Petite délinquance urbaine"),
             ("p","La délinquance existe à Bichkek comme dans toute capitale : vols à la tire, arnaques de taxis non officiels, vigilance dans les bars et boîtes de nuit. <strong>Utilisez l'application Yandex Go</strong> (équivalent Uber local) pour des taxis fiables à prix fixe."),
             ("h3","Chiens errants et faune"),
             ("p","Les chiens errants sont nombreux en zone rurale et dans les pâturages d'altitude (<em>jailoo</em>). Gardez vos distances et ne les approchez pas. Les éleveurs ont souvent des chiens de troupeau type Alabay, très impressionnants : la règle est de ne jamais courir et de contourner largement."),
             ("img",2,"Route de montagne sinueuse au Kirghizistan"),
         ]},
        {"id":"sante","toc":"Santé et trousse","short":"Santé",
         "h2":"Santé, Vaccins et Trousse à Pharmacie",
         "blocks":[
             ("p","Aucun vaccin n'est obligatoire pour entrer au Kirghizistan depuis la France. L'Institut Pasteur recommande cependant d'être à jour du DTP, de l'hépatite A et (pour les longs séjours) de la typhoïde et de l'hépatite B."),
             ("h3","Eau et nourriture"),
             ("p","Ne buvez pas l'eau du robinet, même à Bichkek. Privilégiez les bouteilles scellées ou purifiez avec Micropur/filtre. Méfiez-vous des <strong>laitages fermentés non pasteurisés</strong> (kumis, airan) vendus en bord de route, qui peuvent provoquer des troubles digestifs."),
             ("h3","Soins médicaux"),
             ("p","Les hôpitaux de Bichkek sont corrects pour les urgences, mais en cas d'accident sérieux, un <strong>rapatriement sanitaire</strong> est souvent nécessaire. Souscrivez impérativement une assurance voyage incluant les activités de montagne si vous prévoyez trek, alpinisme ou cheval."),
             ("img",3,"Cavalier kirghize traversant les pâturages d'altitude"),
         ]},
        {"id":"femmes-solo","toc":"Conseils femmes solo","short":"Femmes solo",
         "h2":"Conseils Spécifiques pour les Femmes Voyageant Seules",
         "blocks":[
             ("p","Le Kirghizistan est <strong>considéré comme l'un des pays d'Asie centrale les plus accueillants pour les femmes en solo</strong>. De nombreuses voyageuses témoignent d'expériences positives et d'un sens profond de l'hospitalité."),
             ("h3","Bonnes pratiques"),
             ("p","Évitez les transports isolés en pleine nuit, préférez les auberges gérées par des femmes (nombreuses à Karakol, Bichkek, Song Kul), et habillez-vous simplement (short et débardeur acceptés à Bichkek et autour des lacs, mais couverture plus pudique recommandée en zone rurale et dans les mosquées)."),
             ("h3","Boissons et alcool"),
             ("p","Comme partout, <strong>ne laissez jamais votre verre sans surveillance</strong> dans les bars de Bichkek. Les centres de nuit ont des agents de sécurité mais la vigilance reste de mise."),
             ("img",4,"Yourtes traditionnelles dans les pâturages du Kirghizistan"),
             ("img",5,"Lac Issyk Kul au Kirghizistan en été"),
         ]},
    ],
    "expert_tip":"Le vrai conseil pour voyager serein au Kirghizistan : <strong>engagez un guide local pour vos randonnées de plus de 2 jours en altitude</strong>. Comptez 40-60 € par jour, tout compris (guide, cheval, nourriture, yourte). Vous gagnez en sécurité, en confort logistique, vous soutenez l'économie locale et vous accédez à des vallées et bergers qu'un voyageur autonome ne verrait jamais. Le CBT (Community-Based Tourism) gère un réseau de familles d'accueil dans tout le pays, et leurs guides parlent souvent russe, parfois anglais.",
})

# 7. Spécialités Sri Lanka
ARTICLES.append({
    "slug": "specialites-sri-lanka",
    "title": "Spécialités Culinaires Sri Lanka : 10 Plats à Goûter Absolument | Voyage 7 Continents",
    "og_title": "Spécialités culinaires Sri Lanka : 10 plats à goûter",
    "desc": "Rice and curry, hoppers, kottu roti, lamprais, curry de poisson, thé de Ceylan : les 10 plats incontournables de la cuisine sri-lankaise à déguster absolument.",
    "crumb": "Cuisine Sri Lanka",
    "h1": "Spécialités Culinaires du Sri Lanka : 10 Plats à Goûter Absolument",
    "lead": "Une cuisine explosive de saveurs, héritage de l'Inde, de l'Arabie, du Portugal et des Pays-Bas : découvrez les incontournables du Sri Lanka.",
    "alt1": "Plateau de rice and curry sri-lankais avec plusieurs petits bols colorés",
    "caption1": "Le rice and curry, plat national sri-lankais servi dans sa forme traditionnelle.",
    "sections": [
        {"id":"tradition","toc":"Une tradition millénaire","short":"Tradition",
         "h2":"La Cuisine Sri-Lankaise : une Tradition Millénaire",
         "blocks":[
             ("p","La cuisine du Sri Lanka est l'une des plus riches et des plus sous-estimées d'Asie. Fruit d'un brassage exceptionnel entre influences indiennes, tamoules, arabes, portugaises et néerlandaises, elle repose sur trois piliers : le <strong>riz</strong>, les <strong>épices locales</strong> et la <strong>noix de coco</strong> sous toutes ses formes (lait, chair, huile, jus). Le <a href=\"https://www.srilanka.travel/\" target=\"_blank\" rel=\"noopener nofollow\">Sri Lanka Tourism Promotion Bureau</a> a fait de la gastronomie l'un de ses principaux axes de communication internationale."),
             ("h3","Une cuisine plus piquante qu'indienne"),
             ("p","Contrairement à l'idée reçue, la cuisine sri-lankaise est souvent <strong>plus piquante que la cuisine indienne classique</strong>. Les Sri-Lankais utilisent généreusement le piment rouge séché, les currys de Maldives (poisson fumé et séché), et des pâtes d'épices préparées chaque matin. Dans les restaurants touristiques, n'hésitez pas à demander <em>'not too spicy'</em> pour votre première semaine."),
             ("img",2,"Marché d'épices au Sri Lanka avec cannelle, cardamome et piments"),
         ]},
        {"id":"rice-curry","toc":"Rice and curry","short":"Rice and curry",
         "h2":"1. Rice and Curry : le Plat National",
         "blocks":[
             ("p","Le <strong>rice and curry</strong> n'est pas <em>un</em> plat, c'est <em>une manière de manger</em>. Un grand bol de riz accompagné de <strong>5 à 12 petits bols</strong> de currys variés : légumes, viande, poisson, œuf, dal (lentilles), sambol (condiment à la noix de coco), pickles, papadum croustillant."),
             ("h3","Où en goûter"),
             ("p","Dans les <strong>hotels locaux</strong> (petits restaurants populaires, à ne pas confondre avec les hôtels occidentaux) à l'heure du déjeuner. Comptez 300 à 800 LKR (1 à 3 €). Un vrai rice and curry contient toujours au moins un élément fermenté et un élément cru."),
         ]},
        {"id":"hoppers","toc":"Hoppers et string hoppers","short":"Hoppers",
         "h2":"2. Hoppers et String Hoppers",
         "blocks":[
             ("p","Deux piliers du petit-déjeuner sri-lankais, originaux et photogéniques."),
             ("h3","Hoppers (appam)"),
             ("p","Des <strong>crêpes en forme de bol</strong>, croustillantes sur les bords et moelleuses au centre, faites à base de farine de riz fermentée et de lait de coco. On les mange avec un sambol épicé, du curry ou un œuf cassé au centre (<em>egg hopper</em>)."),
             ("h3","String hoppers (idiyappam)"),
             ("p","Des <strong>nids de vermicelles de riz</strong> cuits à la vapeur, servis par 5-10 avec un curry léger et du sambol. Plat complet, léger et très digeste. Parfait pour un petit-déjeuner énergétique avant une journée de découverte."),
             ("img",3,"Egg hopper sri-lankais avec œuf cuit au centre d'une crêpe en bol"),
         ]},
        {"id":"kottu-roti","toc":"Kottu roti","short":"Kottu roti",
         "h2":"3. Kottu Roti : le Plat de Rue Culte",
         "blocks":[
             ("p","Le <strong>kottu roti</strong> est l'un des plats les plus emblématiques de la street food sri-lankaise. Fait à base de <em>godamba roti</em> (pain plat levé) haché à la machette sur une plaque chauffante, mélangé avec légumes, œuf, épices et, au choix, viande ou fromage."),
             ("h3","Le son des cuisines de rue"),
             ("p","À Colombo comme à Kandy, vous reconnaîtrez une échoppe de kottu roti au <strong>bruit rythmique des machettes</strong> qui hachent le roti sur la plaque métallique. Ce son fait partie du paysage urbain nocturne du Sri Lanka. À goûter absolument après 19h, quand les stands ouvrent."),
         ]},
        {"id":"lamprais","toc":"Lamprais","short":"Lamprais",
         "h2":"4. Lamprais : l'Héritage Néerlandais",
         "blocks":[
             ("p","Le <strong>lamprais</strong> (du néerlandais <em>lomprijst</em>, signifiant « paquet de riz ») est un héritage direct de la colonisation néerlandaise et de la communauté burgher. C'est un <strong>repas complet emballé dans une feuille de bananier</strong> puis cuit à la vapeur."),
             ("h3","Composition"),
             ("p","Le paquet contient du riz cuit dans un bouillon d'épices, un curry de trois viandes (bœuf, poulet, porc), des œufs farcis (frikkadel), une aubergine sambol et un sambol de crevettes. Une bombe de saveurs concentrées par la vapeur et le parfum de la feuille de bananier."),
             ("h3","Où le trouver"),
             ("p","Spécialité rare dans les hôtels touristiques mais <strong>culte à Colombo</strong>. Les adresses historiques sont <em>Perera &amp; Sons</em> et <em>Green Cabin</em>, qui proposent aussi des versions végétariennes."),
         ]},
        {"id":"autres-plats","toc":"Autres plats emblématiques","short":"Autres plats",
         "h2":"5-8. Autres Plats Emblématiques",
         "blocks":[
             ("h3","5. Curry de poisson (fish curry)"),
             ("p","Un <strong>curry de thon, maquereau ou saint-pierre</strong> cuit dans un mélange de noix de coco, curcuma, tamarin et piment. Chaque région a sa version : les côtes du sud sont réputées pour leur curry au poisson fumé, le nord pour leurs currys de crabe à la manière de Jaffna."),
             ("h3","6. Curry de crabe à la manière de Jaffna"),
             ("p","Le <strong>crabe au curry de Jaffna</strong> est devenu culte grâce au restaurant Ministry of Crab à Colombo, fondé par les cricketers sri-lankais Kumar Sangakkara et Mahela Jayawardene. La version authentique se déguste dans le nord, avec les épices fortes tamoules."),
             ("h3","7. Jaggery et kithul treacle"),
             ("p","Le <strong>jaggery</strong> (sucre non raffiné de palmier kithul) et le <strong>kithul treacle</strong> (mélasse de palme) sont les édulcorants traditionnels. Le treacle se verse sur les curd (yaourts de bufflonne) et accompagne les desserts. Un produit d'origine végétale entièrement artisanal, en voie de patrimoine immatériel."),
             ("h3","8. Watalappan"),
             ("p","Le <strong>watalappan</strong> est un flan à base de lait de coco, jaggery, cardamome, clou de girofle et noix de cajou grillées. Héritage de la communauté musulmane malaise, il se déguste principalement pendant le Ramadan mais se trouve dans les meilleurs restaurants toute l'année."),
             ("img",4,"Curry de crabe de Jaffna servi dans une assiette sri-lankaise"),
         ]},
        {"id":"the-ceylan","toc":"Le thé de Ceylan","short":"Thé de Ceylan",
         "h2":"9. Le Thé de Ceylan",
         "blocks":[
             ("p","Impossible de parler de Sri Lanka sans évoquer le <strong>thé de Ceylan</strong>, l'un des meilleurs thés noirs au monde. Introduit en 1867 par le planteur écossais James Taylor, il a transformé l'économie de l'île."),
             ("h3","Régions et altitudes"),
             ("p","Trois grandes zones : <strong>low grown</strong> (basse altitude, corsé, fort en théine), <strong>mid grown</strong> (Kandy, équilibré) et <strong>high grown</strong> (Nuwara Eliya, Dimbula, Uva, au-dessus de 1 200 m, délicat et floral). Les plus grands crus viennent d'Uva et Nuwara Eliya."),
             ("h3","Visiter une plantation"),
             ("p","Les régions de <strong>Ella, Nuwara Eliya et Haputale</strong> concentrent les plus belles plantations visitables. Certaines fabriques (Damro Labookellie, Pedro Tea Estate, Handunugoda) proposent des visites guidées et dégustations pour 500 à 1 500 LKR."),
         ]},
        {"id":"ou-manger","toc":"Où manger et conseils","short":"Où manger",
         "h2":"10. Où Manger et Conseils Pratiques",
         "blocks":[
             ("h3","Marchés et cuisines de rue"),
             ("p","Les <strong>marchés de nuit de Colombo, Galle, Kandy et Jaffna</strong> sont les meilleurs points d'entrée pour la cuisine populaire. Privilégiez les stands à forte rotation (affluence = fraîcheur), évitez les buffets à l'hôtel où la cuisine est adoucie pour les touristes."),
             ("h3","Homestays et cooking classes"),
             ("p","Les <strong>homestays</strong> (chambres chez l'habitant) sont souvent le meilleur endroit pour découvrir la vraie cuisine sri-lankaise. Beaucoup proposent des <strong>cours de cuisine</strong> à 15-25 € par personne, incluant le marché, la préparation et la dégustation."),
             ("h3","Précautions d'hygiène"),
             ("p","Le climat tropical impose quelques règles : <strong>évitez l'eau du robinet</strong>, privilégiez l'eau en bouteille scellée ; <strong>mangez les fruits pelés</strong> ; <strong>limitez les crudités non lavées</strong> les premiers jours. Les <a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/sri-lanka/\" target=\"_blank\" rel=\"noopener nofollow\">conseils aux voyageurs de France Diplomatie</a> recommandent une pharmacie de voyage avec antidiarrhéiques."),
             ("img",5,"Plantation de thé au Sri Lanka dans les collines de Nuwara Eliya"),
         ]},
    ],
    "expert_tip":"Pour une immersion culinaire réussie au Sri Lanka, <strong>réservez une <em>cooking class</em> dans les trois premiers jours de votre voyage</strong>. Vous apprendrez à identifier les épices locales, à doser la noix de coco, à reconnaître un vrai sambol d'un industriel. Une fois formé au palais sri-lankais, vous apprécierez bien plus chaque repas pendant le reste du séjour, et vous saurez lire les menus en anglais simplifié (<em>devilled</em>, <em>curry powder</em>, <em>Sri Lankan black pork</em>...). Le meilleur rapport qualité-prix : les classes organisées dans les homestays de Galle, Ella et Kandy.",
})

# 8. Visa Myanmar arrivée
ARTICLES.append({
    "slug": "visa-myanmar-arrivee",
    "title": "Visa à l'Arrivée Myanmar : Prix, Démarches et Alternatives 2026 | Voyage 7 Continents",
    "og_title": "Prix visa à l'arrivée Myanmar : guide 2026",
    "desc": "Visa à l'arrivée au Myanmar (Birmanie) en 2026 : tarif, démarches, e-visa alternatif, documents nécessaires, conseils France Diplomatie et contexte politique.",
    "crumb": "Visa Myanmar",
    "h1": "Visa à l'Arrivée au Myanmar : Prix, Démarches et Alternatives en 2026",
    "lead": "VoA, e-visa, documents, prix : tout savoir sur le visa pour entrer au Myanmar (Birmanie), pays dont les règles évoluent régulièrement.",
    "alt1": "Temples de Bagan au Myanmar au lever du soleil avec montgolfières",
    "caption1": "Bagan, site mythique du Myanmar — pays soumis à des règles de visa strictes.",
    "sections": [
        {"id":"situation-2026","toc":"La situation en 2026","short":"Situation 2026",
         "h2":"La Situation du Visa Myanmar en 2026",
         "blocks":[
             ("p","Avant d'entrer dans les détails : le Myanmar (Birmanie) vit depuis février 2021 une crise politique majeure suite au coup d'État militaire. Les <a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/birmanie-myanmar/\" target=\"_blank\" rel=\"noopener nofollow\">conseils aux voyageurs de France Diplomatie</a> recommandent actuellement de <strong>reporter tout déplacement non essentiel</strong>. Cet article traite néanmoins des procédures officielles pour les voyageurs qui décident de s'y rendre en toute connaissance de cause."),
             ("h3","E-visa ou VoA ?"),
             ("p","Depuis 2014, le Myanmar a mis en place un système d'<strong>e-visa en ligne</strong> qui a largement remplacé le visa à l'arrivée classique. En 2026, selon le site officiel <a href=\"https://evisa.moip.gov.mm/\" target=\"_blank\" rel=\"noopener nofollow\">evisa.moip.gov.mm</a>, l'e-visa est la voie standard pour les touristes, tandis que le VoA (visa on arrival) est réservé aux ressortissants de certains pays ou à des cas spécifiques (affaires, transit)."),
         ]},
        {"id":"prix-visa","toc":"Prix du visa","short":"Prix",
         "h2":"Le Prix du Visa en 2026",
         "blocks":[
             ("h3","E-visa touristique (option standard)"),
             ("p","L'e-visa touristique coûte <strong>50 USD</strong> pour les ressortissants français (et la plupart des Européens), payables en ligne par carte bancaire. Validité : <strong>90 jours à partir de la date d'émission</strong>, pour un séjour maximal de <strong>28 jours</strong> sur le territoire, <strong>entrée unique</strong>. Le visa n'est pas extensible sur place sans démarches complexes."),
             ("h3","Visa à l'arrivée (VoA)"),
             ("p","Quand il est disponible, le VoA touristique coûte également <strong>50 USD</strong>, à régler <strong>en espèces en dollars américains</strong>, billets neufs exclusivement acceptés. Certains voyageurs rapportent cependant que l'option touristique n'est plus proposée en 2026 — seules subsistent les catégories <em>business</em> (70 USD) et <em>transit</em> (40 USD)."),
             ("h4","Notre recommandation"),
             ("p","Privilégiez <strong>toujours l'e-visa</strong>. Il évite le stress de l'arrivée, garantit l'entrée et simplifie les contrôles aux aéroports de Yangon, Mandalay et Nay Pyi Taw."),
             ("img",2,"Passeport ouvert avec visa apposé"),
         ]},
        {"id":"demarches-evisa","toc":"Démarches e-visa pas à pas","short":"Démarches",
         "h2":"Démarches E-visa Pas à Pas",
         "blocks":[
             ("h3","Étape 1 : formulaire en ligne"),
             ("p","Rendez-vous sur le site officiel <strong>evisa.moip.gov.mm</strong> (attention aux nombreux sites intermédiaires payants qui imitent le site officiel). Remplissez le formulaire en anglais : identité, passeport, adresse, profession, hôtel de destination, point d'entrée prévu (aéroport de Yangon par défaut)."),
             ("h3","Étape 2 : photo et passeport"),
             ("p","Téléversez une <strong>photo d'identité récente</strong> (format passeport, fond clair) et une <strong>copie numérique de la page de votre passeport</strong>. Le passeport doit être valide au moins <strong>6 mois</strong> après la date d'entrée et disposer d'au moins 2 pages vierges."),
             ("h3","Étape 3 : paiement"),
             ("p","Paiement par carte Visa, MasterCard ou JCB (50 USD). Les cartes American Express ne sont pas toujours acceptées. La transaction est sécurisée et hors taxes de change."),
             ("h3","Étape 4 : délai de traitement"),
             ("p","Le visa est généralement délivré en <strong>1 à 3 jours ouvrables</strong>. Vous recevez par email un fichier PDF à <strong>imprimer en couleur</strong> et à présenter au contrôle d'immigration. Gardez toujours une copie numérique de secours sur votre téléphone."),
             ("h4","Attention aux faux sites"),
             ("p","De nombreux sites non officiels revendent l'e-visa myanmar à <strong>80-120 USD</strong> en prétendant accélérer la procédure. Ce sont des intermédiaires privés : le site officiel est gratuit à consulter et coûte 50 USD fixes. Vérifiez toujours l'URL : <em>evisa.moip.gov.mm</em> et rien d'autre."),
         ]},
        {"id":"documents","toc":"Documents requis","short":"Documents",
         "h2":"Documents Requis pour Entrer au Myanmar",
         "blocks":[
             ("p","Au-delà du visa lui-même, plusieurs documents sont exigés à l'arrivée."),
             ("h3","Liste complète"),
             ("p","<strong>Passeport valable 6 mois</strong> après la date d'entrée, avec 2 pages vierges minimum. <strong>E-visa imprimé</strong> en couleur. <strong>Billet d'avion aller-retour</strong> ou preuve de continuation du voyage. <strong>Justificatif d'hébergement</strong> pour les premiers jours. <strong>Preuve de fonds suffisants</strong> (rarement demandée mais possible). <strong>Assurance voyage</strong> incluant rapatriement sanitaire (fortement recommandée)."),
             ("img",3,"Bureau d'immigration d'aéroport avec files d'attente"),
         ]},
        {"id":"contexte-politique","toc":"Contexte politique","short":"Contexte",
         "h2":"Contexte Politique et Conseils Officiels",
         "blocks":[
             ("p","Depuis février 2021, le Myanmar est dirigé par une junte militaire suite au coup d'État contre le gouvernement démocratiquement élu. Le pays est en <strong>état d'urgence prolongé</strong> et connaît des conflits armés dans plusieurs régions (Sagaing, Chin, Kachin, Karen, Arakan/Rakhine)."),
             ("h3","Zones interdites aux étrangers"),
             ("p","De nombreuses zones sont <strong>fermées aux voyageurs étrangers</strong> : États Shan, Chin, Kachin, Rakhine, Kayah, régions de Sagaing et Tanintharyi. Même Bagan et le lac Inle ont connu des restrictions temporaires. Vérifiez toujours la situation <strong>moins de 48 h avant votre départ</strong>."),
             ("h3","Sanctions internationales"),
             ("p","L'UE applique des sanctions ciblées contre certains membres de la junte. Votre voyage ne finance pas directement le régime tant que vous évitez les hôtels et compagnies aériennes appartenant aux militaires. Consultez le <a href=\"https://www.gov.uk/foreign-travel-advice/myanmar-burma\" target=\"_blank\" rel=\"noopener nofollow\">FCDO britannique</a> pour une liste actualisée."),
         ]},
        {"id":"faq-visa","toc":"FAQ visa Myanmar","short":"FAQ",
         "h2":"FAQ Visa Myanmar",
         "blocks":[
             ("h3","Peut-on prolonger le visa sur place ?"),
             ("p","Les extensions sont théoriquement possibles au bureau d'immigration de Yangon (35 USD par semaine supplémentaire), mais la procédure est longue et incertaine. Mieux vaut prévoir une sortie/rentrée par la Thaïlande si vous souhaitez un séjour plus long."),
             ("h3","Peut-on entrer par voie terrestre ?"),
             ("p","Plusieurs points de passage frontaliers sont ouverts avec la Thaïlande (Mae Sot/Myawaddy, Ranong/Kawthaung), mais les règles d'accès pour les touristes changent fréquemment. Renseignez-vous juste avant le départ."),
             ("h3","Quel est le délai avant le voyage pour faire l'e-visa ?"),
             ("p","Le mieux est de faire l'e-visa <strong>2 à 3 semaines avant le départ</strong>. C'est suffisant pour gérer d'éventuels refus ou demandes de documents complémentaires, sans risquer de l'avoir trop en avance (validité 90 jours à partir de l'émission)."),
             ("img",4,"Drapeau du Myanmar flottant devant un bâtiment officiel"),
             ("img",5,"Pagode Shwedagon à Yangon au crépuscule"),
         ]},
    ],
    "expert_tip":"Avant tout voyage au Myanmar, <strong>consultez en priorité la page actualisée de France Diplomatie</strong> (mise à jour quasi-mensuelle) et comparez avec les recommandations du FCDO britannique et du State Department américain. Si les trois pays classent le Myanmar en « déconseillé sauf raison impérative », prenez-le très au sérieux : même en zone touristique, les communications peuvent être coupées, les routes bloquées, l'assistance consulaire limitée. Pour les voyageurs qui décident tout de même d'y aller, privilégiez un <strong>circuit organisé par une agence française de confiance</strong> plutôt qu'un voyage individuel.",
})

# 9. Meilleure période Mongolie
ARTICLES.append({
    "slug": "meilleure-periode-mongolie",
    "title": "Meilleure Période pour Visiter la Mongolie : Calendrier 2026 | Voyage 7 Continents",
    "og_title": "Meilleure période pour visiter la Mongolie : calendrier",
    "desc": "Quand partir en Mongolie ? Climat mois par mois, festival Naadam, chasse à l'aigle, meilleures périodes pour le désert de Gobi et les steppes. Guide complet 2026.",
    "crumb": "Meilleure période Mongolie",
    "h1": "Meilleure Période pour Visiter la Mongolie : le Calendrier 2026",
    "lead": "Été des steppes, Naadam, festival de l'aigle, hivers extrêmes : le guide mois par mois pour choisir la meilleure période de voyage en Mongolie.",
    "alt1": "Yourte traditionnelle mongole au pied des montagnes de l'Altaï",
    "caption1": "La Mongolie et ses steppes infinies : un pays aux saisons extrêmes.",
    "sections": [
        {"id":"resume","toc":"Résumé rapide","short":"Résumé",
         "h2":"Résumé Rapide : de Juin à Septembre",
         "blocks":[
             ("p","Si vous ne deviez retenir qu'une chose : la <strong>meilleure période pour visiter la Mongolie s'étend de juin à mi-septembre</strong>. C'est la seule fenêtre où l'ensemble du pays est accessible, où les nomades vivent dans leurs pâturages d'altitude, où l'herbe est verte, où les températures sont clémentes et où tous les festivals majeurs se déroulent. En dehors de cette fenêtre, le pays se transforme en désert glacé (jusqu'à -40 °C en janvier)."),
             ("h3","Les trois meilleurs moments"),
             ("p","<strong>1ʳᵉ quinzaine de juillet</strong> pour le festival Naadam. <strong>Août</strong> pour les paysages les plus verts et la steppe en fleurs. <strong>Début octobre</strong> pour le festival des chasseurs à l'aigle à Bayan-Ölgii (ouest de la Mongolie)."),
         ]},
        {"id":"climat","toc":"Un climat extrême","short":"Climat",
         "h2":"Un Climat Extrême, Unique au Monde",
         "blocks":[
             ("p","La Mongolie détient plusieurs records climatiques. Son climat est <strong>continental extrême</strong>, avec des variations de plus de 70 °C entre l'hiver et l'été. L'<a href=\"https://www.nams.gov.mn/\" target=\"_blank\" rel=\"noopener nofollow\">Institut national d'hydrologie, de météorologie et de surveillance environnementale de Mongolie (NAMHEM)</a> publie les données officielles."),
             ("h3","Température annuelle moyenne"),
             ("p","Entre <strong>-5 °C et +2 °C</strong> sur l'année, avec Oulan-Bator considérée comme la <strong>capitale la plus froide du monde</strong> (moyenne annuelle -1 °C). Les écarts jour/nuit peuvent atteindre 20 °C même en été."),
             ("h3","Pluviométrie"),
             ("p","La Mongolie est un pays <strong>très sec</strong> : 200-400 mm par an selon les régions. 80 % des pluies tombent en juin-juillet-août. Le ciel y est particulièrement bleu et lumineux, ce qui explique le surnom de <em>Blue Sky Country</em>."),
             ("img",2,"Steppe mongole en été sous un ciel bleu lumineux"),
         ]},
        {"id":"saison-saison","toc":"Saison par saison","short":"Saisons",
         "h2":"Saison par Saison : Que Faire Quand ?",
         "blocks":[
             ("h3","Printemps (avril-mai)"),
             ("p","Période <strong>à éviter en priorité</strong>. Les tempêtes de sable (<em>zud</em> et <em>sand storms</em>) sont fréquentes, l'herbe n'a pas encore poussé, les nomades sont encore dans leurs quartiers d'hiver, et les infrastructures touristiques n'ont pas toutes rouvert. Températures : -5 à 15 °C."),
             ("h3","Été (juin-août) : la saison idéale"),
             ("p","C'est la <strong>meilleure période par excellence</strong>. Températures de 15 à 28 °C en journée, nuits fraîches (5-12 °C). La steppe est verte, les nomades sont dans leurs yourtes d'été, tous les sites sont accessibles. Les routes du Gobi sont praticables, les passes de haute montagne sont dégagées."),
             ("h4","Attention à juillet"),
             ("p","Juillet est aussi le <strong>mois le plus pluvieux</strong>, avec des orages violents en soirée. Les pistes peuvent devenir boueuses. Ne partez jamais sans vêtement imperméable, même par 28 °C."),
             ("h3","Automne (septembre-début octobre)"),
             ("p","<strong>Mois merveilleux</strong> : moins de touristes, températures encore agréables (10-22 °C en journée), couleurs dorées de la steppe, ciels limpides. C'est la saison préférée des photographes. Début octobre marque aussi le <strong>festival des chasseurs à l'aigle</strong> dans l'Altaï."),
             ("h3","Hiver (octobre à mars)"),
             ("p","L'hiver mongol est <strong>redoutable</strong> : -20 °C à -40 °C, vent glacial de Sibérie, neige, routes fermées. Réservé aux voyageurs expérimentés ou aux visites culturelles à Oulan-Bator (Tsagaan Sar, Nouvel An mongol en février). Certains opérateurs proposent des <strong>séjours hiver thématiques</strong> (cheval, traîneau, immersion nomade) mais l'équipement doit être spécialisé."),
         ]},
        {"id":"naadam","toc":"Le festival Naadam","short":"Naadam",
         "h2":"Le Festival Naadam (11-13 juillet)",
         "blocks":[
             ("p","Le <strong>Naadam</strong> est le plus grand festival traditionnel de Mongolie, célébré chaque année les <strong>11, 12 et 13 juillet</strong> en fête nationale. Inscrit au <a href=\"https://ich.unesco.org/fr/RL/le-naadam-festival-traditionnel-mongol-00395\" target=\"_blank\" rel=\"noopener nofollow\">patrimoine culturel immatériel de l'UNESCO</a> depuis 2010, il met à l'honneur les <strong>trois sports virils</strong> mongols."),
             ("h3","Les trois disciplines"),
             ("p","<strong>Lutte traditionnelle</strong> (bökh) : des centaines de lutteurs en tenue traditionnelle s'affrontent par élimination. <strong>Courses de chevaux</strong> (urtyn duu) : les cavaliers, des enfants de 5 à 13 ans, parcourent 10 à 30 km à travers la steppe. <strong>Tir à l'arc</strong> (sur) : épreuve mixte, ouverte aux femmes, en costume traditionnel."),
             ("h3","Où assister au Naadam"),
             ("p","Le plus grand Naadam a lieu à <strong>Oulan-Bator</strong>, au stade central. Plus authentique : les <strong>petits Naadams régionaux</strong>, qui se tiennent les jours précédents ou suivants dans chaque province (ajag). Ils offrent une atmosphère plus intime et moins touristique."),
             ("img",3,"Lutteurs mongols en tenue traditionnelle au festival Naadam"),
         ]},
        {"id":"eagle-festival","toc":"Festival de l'aigle","short":"Eagle festival",
         "h2":"Festival des Chasseurs à l'Aigle (Début Octobre)",
         "blocks":[
             ("p","Organisé début octobre à <strong>Ölgii, dans la province de Bayan-Ölgii</strong> (extrême-ouest, province kazakhe de Mongolie), le <strong>festival de l'aigle royal</strong> (Golden Eagle Festival) réunit des dizaines de chasseurs kazakhs et leurs aigles entraînés."),
             ("h3","Origine et traditions"),
             ("p","La chasse à l'aigle est une tradition millénaire des peuples kazakhs et kirghizes d'Asie centrale. Les <em>berkutchi</em> (chasseurs) capturent de jeunes aigles sauvages, les élèvent et les dressent pendant plusieurs années, avant de les relâcher à l'état adulte pour préserver l'espèce."),
             ("h3","Compétitions"),
             ("p","Le festival comprend des épreuves de <strong>rappel de l'aigle depuis un sommet</strong>, de <strong>chasse simulée sur un appât</strong> et de <strong>costumes traditionnels</strong>. Un spectacle visuellement unique au monde, à prévoir dans le circuit impérativement avec une agence locale qui coordonne les transports depuis Oulan-Bator (3 h de vol + 4x4)."),
             ("img",4,"Chasseur kazakh avec son aigle royal en Mongolie occidentale"),
         ]},
        {"id":"vetements-saison","toc":"Vêtements par saison","short":"Vêtements",
         "h2":"Quoi Emporter selon la Saison",
         "blocks":[
             ("h3","Été (juin-août)"),
             ("p","<strong>Système multicouches indispensable</strong> : t-shirts, manches longues, polaire, veste coupe-vent imperméable, doudoune légère pour les nuits, pantalon de randonnée, chaussures imperméables mi-hautes. Ajoutez chapeau large, crème solaire SPF 50, lunettes de soleil, et maillot de bain pour les lacs du nord (Khövsgöl)."),
             ("h3","Automne (septembre-octobre)"),
             ("p","Mêmes couches mais plus épaisses : doudoune 800 plumes, bonnet, gants, chaussures imperméables. La neige peut tomber dès fin septembre sur les hauts cols."),
             ("img",5,"Caravane de chameaux dans le désert de Gobi en Mongolie"),
         ]},
    ],
    "expert_tip":"Si votre voyage tombe en <strong>première quinzaine de juillet</strong>, réservez absolument vos vols Paris-Oulan-Bator <strong>4 à 6 mois à l'avance</strong>. Le Naadam fait exploser la demande et les billets peuvent doubler. Une astuce : au lieu de rester sur le grand Naadam d'Oulan-Bator (très touristique et difficile d'accès), <strong>partez le 11 juillet au matin vers une province rurale</strong> (Arkhangai, Bulgan, Khentii) pour assister à un Naadam local le 12 ou 13. Plus intime, plus authentique, et photogénique à souhait.",
})

# 10. Budget Népal 3 semaines
ARTICLES.append({
    "slug": "budget-nepal-3-semaines",
    "title": "Budget Voyage Népal 3 Semaines : le Vrai Coût Complet 2026 | Voyage 7 Continents",
    "og_title": "Budget voyage Népal 3 semaines : vrai coût 2026",
    "desc": "Budget réel pour 3 semaines au Népal en 2026 : vol, visa, hébergement, nourriture, trekking Annapurna/EBC, permis, Chitwan, assurance. De 750 € à 3 000 € selon confort.",
    "crumb": "Budget Népal 3 semaines",
    "h1": "Budget Voyage Népal 3 Semaines : le Vrai Coût Complet",
    "lead": "De 750 € à 3 000 € : décomposition honnête et complète du budget pour un voyage de 3 semaines au Népal en 2026.",
    "alt1": "Massif de l'Annapurna au Népal au lever du soleil",
    "caption1": "Le Népal : un budget très variable, adapté aux backpackers comme aux voyageurs haut de gamme.",
    "sections": [
        {"id":"resume-budget","toc":"Résumé du budget","short":"Résumé",
         "h2":"Résumé : de 750 € à 3 000 € en 3 Semaines",
         "blocks":[
             ("p","Un voyage de 3 semaines au Népal peut coûter aussi bien <strong>750 €</strong> tout compris (backpacker expérimenté) que <strong>3 000 €</strong> et plus (confort, guide privé, trek organisé, agence française). Les postes les plus lourds sont : vol international (40-50 % du budget), trek avec guide/porteur (15-25 %), hébergement urbain (10-15 %)."),
             ("h3","Trois profils-types"),
             ("p","<strong>Backpacker</strong> (750 – 1 000 €) : vol low-cost, auberges de jeunesse, trek en autonomie, repas dans les <em>dal bhat</em> locaux. <strong>Confort</strong> (1 500 – 2 000 €) : vol milieu de gamme, hôtels 3 étoiles, guide privé pour le trek, quelques extras (safari Chitwan, spa, restaurants variés). <strong>Premium</strong> (2 500 – 3 500 €) : vol en classe supérieure, lodges haut de gamme, circuit organisé par une agence française, guide privé, Everest Base Camp avec porteurs."),
         ]},
        {"id":"vol-visa","toc":"Vol et visa","short":"Vol & visa",
         "h2":"Vol International et Visa",
         "blocks":[
             ("h3","Vol Paris-Katmandou"),
             ("p","Aucune compagnie française ne dessert directement Katmandou (KTM). Les escales les plus courantes : <strong>Doha (Qatar Airways), Istanbul (Turkish Airlines), Delhi (Air India), Dubaï (Emirates)</strong>. Prix moyen aller-retour : <strong>450 € en basse saison, 650-900 € en haute saison</strong> (octobre-novembre et avril-mai). Comparez sur <a href=\"https://www.skyscanner.fr/\" target=\"_blank\" rel=\"noopener nofollow\">Skyscanner</a>."),
             ("h3","Visa à l'arrivée ou en ligne"),
             ("p","Le Népal propose un <strong>visa à l'arrivée</strong> à Tribhuvan International Airport et aux postes terrestres avec l'Inde. Tarifs 2026 : <strong>30 USD (15 jours), 50 USD (30 jours), 125 USD (90 jours)</strong>, règlement en espèces (USD, EUR, GBP) ou par carte à l'aéroport. Le visa en ligne préalable (<em>online visa</em>) est possible via <a href=\"https://www.immigration.gov.np/\" target=\"_blank\" rel=\"noopener nofollow\">immigration.gov.np</a>."),
             ("img",2,"Vue aérienne de Katmandou au Népal depuis un avion"),
         ]},
        {"id":"hebergement","toc":"Hébergement","short":"Hébergement",
         "h2":"Hébergement : Auberges, Hôtels et Lodges",
         "blocks":[
             ("h3","Katmandou et Pokhara"),
             ("p","<strong>Auberge de jeunesse / guesthouse</strong> : 5-10 € la nuit en chambre double avec salle de bains partagée. <strong>Hôtel 3 étoiles</strong> : 25-50 € en chambre double, petit-déjeuner souvent inclus. <strong>Hôtel 4-5 étoiles</strong> (Dwarika's, Hyatt Regency) : 100 à 300 € la nuit, standing international."),
             ("h3","En trek (Annapurna, EBC)"),
             ("p","Les <strong>teahouses</strong> (refuges-auberges tenus par les familles sherpas) sont la norme. Nuit : <strong>3 à 8 €</strong> en basse altitude, <strong>10 à 25 €</strong> au-dessus de 4 000 m. La tradition veut que l'on mange dans la teahouse où on dort (les prix des chambres sont volontairement bas pour encourager la restauration sur place)."),
             ("img",3,"Teahouse traditionnelle sur le sentier de l'Annapurna au Népal"),
         ]},
        {"id":"nourriture","toc":"Nourriture","short":"Nourriture",
         "h2":"Nourriture : le Népal Très Bon Marché",
         "blocks":[
             ("p","Manger au Népal reste l'un des postes les moins chers d'Asie."),
             ("h3","Prix moyens"),
             ("p","<strong>Dal bhat</strong> (riz, lentilles, légumes, le plat national) : 2-4 € en ville, 5-8 € en montagne. <strong>Momos</strong> (raviolis tibétains) : 1,50-3 €. <strong>Pizza dans un restaurant touristique</strong> (Thamel, Lakeside) : 5-8 €. <strong>Repas dans un restaurant haut de gamme</strong> : 15-25 €."),
             ("h3","En trek : attention à l'inflation"),
             ("p","Les prix <strong>doublent ou triplent en altitude</strong> (tout est porté à dos d'homme ou de yak). Un dal bhat qui coûte 3 € à Pokhara peut coûter 8-10 € au camp de base de l'Annapurna, et jusqu'à 15 € à Gorak Shep (EBC). Une bouteille d'eau de 1 litre passe de 0,30 € en ville à 3-4 € à 5 000 m."),
         ]},
        {"id":"transport-interne","toc":"Transport interne","short":"Transport",
         "h2":"Transport Interne",
         "blocks":[
             ("h3","Bus et microbus"),
             ("p","Les <strong>bus locaux</strong> sont le moyen le moins cher (3-5 € pour Katmandou-Pokhara, 6 h), mais fatigants. Les <strong>tourist buses</strong> (Greenline, Jagadamba) sont plus confortables et partent à 7h-8h : 10-18 €, même durée."),
             ("h3","Vols intérieurs"),
             ("p","Pour gagner du temps : Katmandou-Pokhara en avion (<strong>100-150 €</strong>), Katmandou-Lukla (porte d'entrée du trek EBC) : <strong>180-220 €</strong> l'aller simple, réservable via Buddha Air, Yeti Airlines, Summit Air. Les vols sont <strong>soumis aux aléas météo</strong> et annulés fréquemment en saison de mousson."),
             ("h3","Taxi et 4x4"),
             ("p","Taxis dans Katmandou : 2-5 € la course. 4x4 privé avec chauffeur pour une excursion à la journée : 50-80 €. L'application <strong>InDrive</strong> (équivalent local de Uber) fonctionne bien à Katmandou et Pokhara."),
             ("img",4,"Durbar Square à Katmandou au Népal avec temples anciens"),
         ]},
        {"id":"trekking","toc":"Trekking : permis et guides","short":"Trekking",
         "h2":"Trekking : Permis, Guides et Porteurs",
         "blocks":[
             ("p","C'est <strong>le poste à anticiper</strong> : le trek représente souvent 20-30 % du budget total d'un voyage de 3 semaines."),
             ("h3","Permis obligatoires"),
             ("p","Depuis 2023, <strong>le guide est obligatoire</strong> pour tous les treks en zones protégées. <strong>Carte TIMS</strong> (Trekkers Information Management System) : 20 USD. <strong>Permis ACAP</strong> (Annapurna Conservation Area Project) : 30 USD. <strong>Permis Sagarmatha</strong> (Everest) : 30 USD. <strong>Permis Langtang</strong> : 30 USD. Tous délivrés par la <a href=\"https://www.ntb.gov.np/\" target=\"_blank\" rel=\"noopener nofollow\">Nepal Tourism Board</a> à Katmandou ou via agence."),
             ("h3","Guide et porteur"),
             ("p","<strong>Guide certifié</strong> : 25-40 USD par jour. <strong>Porteur</strong> : 20-30 USD par jour (il porte jusqu'à 15-25 kg). Un <strong>guide-porteur</strong> combiné : 30-35 USD/jour, idéal pour un trek intermédiaire. Les agences sérieuses sont membres de la <a href=\"https://www.taan.org.np/\" target=\"_blank\" rel=\"noopener nofollow\">TAAN (Trekking Agencies' Association of Nepal)</a>."),
             ("h3","Durée des grands treks"),
             ("p","<strong>Camp de base de l'Annapurna (ABC)</strong> : 7-10 jours. <strong>Circuit des Annapurnas</strong> : 12-18 jours. <strong>Camp de base de l'Everest (EBC)</strong> : 12-14 jours. <strong>Langtang</strong> : 7-10 jours."),
         ]},
        {"id":"itineraire","toc":"Itinéraire type 3 semaines","short":"Itinéraire",
         "h2":"Exemple d'Itinéraire 3 Semaines",
         "blocks":[
             ("h3","Proposition classique"),
             ("p","<strong>Jours 1-3</strong> : Katmandou (vallée, Durbar Square, Pashupatinath, Boudhanath, Bhaktapur). <strong>Jour 4</strong> : route pour Pokhara. <strong>Jours 5-15</strong> : trek ABC ou tour des Annapurnas (10-12 jours avec jours d'acclimatation). <strong>Jours 16-18</strong> : Chitwan (safari jungle, rhinocéros, éléphants). <strong>Jours 19-21</strong> : retour Katmandou, temps libre, shopping, vol retour."),
             ("h3","Alternative EBC"),
             ("p","<strong>Jours 1-2</strong> : Katmandou. <strong>Jours 3-16</strong> : trek EBC complet avec vol Lukla. <strong>Jours 17-19</strong> : Pokhara repos. <strong>Jours 20-21</strong> : Katmandou et retour."),
             ("img",5,"Randonneurs sur le sentier du camp de base de l'Everest au Népal"),
         ]},
        {"id":"assurance","toc":"Assurance voyage","short":"Assurance",
         "h2":"Assurance Voyage : Indispensable",
         "blocks":[
             ("p","Ne partez <strong>jamais au Népal sans assurance voyage</strong>. En cas d'accident en altitude, seule une évacuation par hélicoptère permet d'atteindre un hôpital en quelques heures. Tarif d'un sauvetage : <strong>5 000 à 15 000 USD</strong>."),
             ("h3","Critères essentiels"),
             ("p","Votre assurance doit couvrir : <strong>trekking jusqu'à 6 000 m minimum</strong>, <strong>évacuation par hélicoptère</strong>, <strong>rapatriement sanitaire</strong>, <strong>frais médicaux sans franchise</strong>. Vérifiez les exclusions : certaines polices n'assurent pas au-delà de 4 500 m. Les <a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/nepal/\" target=\"_blank\" rel=\"noopener nofollow\">conseils aux voyageurs de France Diplomatie</a> insistent particulièrement sur ce point."),
             ("h3","Budget assurance"),
             ("p","Comptez <strong>50 à 120 €</strong> pour 3 semaines, selon la couverture. Les assurances carte bancaire classiques (Visa Premier, Mastercard Gold) sont généralement <strong>insuffisantes</strong> pour le trekking en altitude — souscrivez une assurance spécifique (Chapka, Mondial Assistance, Europ Assistance, AVI International)."),
         ]},
    ],
    "expert_tip":"Pour boucler un voyage de 3 semaines au Népal à budget maîtrisé, visez <strong>1 500 € tout compris</strong> (vol inclus) en partant hors saison (juin ou début septembre), en optant pour un <strong>trek guidé</strong> (guide seul, sans porteur, 25 USD/jour) et en logeant en guesthouses simples à Katmandou et Pokhara. Vous profitez pleinement du Népal, vous soutenez l'économie locale, vous respectez la réglementation 2023 sur le guide obligatoire, et vous gardez une marge pour deux-trois extras (massage ayurvédique, dîner dans un Dwarika's Heritage, vol panoramique autour de l'Everest, safari Chitwan). Évitez absolument le trek en solo : depuis la réforme, c'est illégal et les amendes sont dissuasives.",
})

# ---------------- Write files ----------------
for a in ARTICLES:
    path = os.path.join(OUT, a["slug"] + ".html")
    content = render(a)
    # Fix a small escape mistake in one article
    content = content.replace('("p">"', '("p","')
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"wrote {path}  {len(content)} chars")

print(f"done: {len(ARTICLES)} articles")
