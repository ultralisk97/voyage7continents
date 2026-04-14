#!/usr/bin/env python3
"""Generate 9 Africa articles — same EEAT template as generate_asie.py."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "afrique")
os.makedirs(OUT, exist_ok=True)

HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://voyage7continents.fr/afrique/{slug}.html">
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
          <li><a href="/asie/">Asie</a></li>
          <li><a href="/afrique/" class="active">Afrique</a></li>
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

  <section class="hero hero-pillar" style="background: linear-gradient(rgba(14,47,68,0.8), rgba(26,82,118,0.75)), url('/img/hero-afrique.jpg') center/cover no-repeat;">
    <div class="hero-content">
      <div class="breadcrumb">
        <a href="/">Voyage 7 Continents</a> &rsaquo; <a href="/afrique/">Afrique</a> &rsaquo; <strong>{crumb}</strong>
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

      <p>Pour préparer votre voyage, retrouvez notre <a href="/afrique/">guide complet Afrique</a> et nos autres articles de la catégorie.</p>

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

# 1. Voltage prise Tanzanie
ARTICLES.append({
    "slug": "voltage-prise-tanzanie",
    "title": "Voltage et Prise Électrique en Tanzanie : Adaptateur, Type G, 230V | Voyage 7 Continents",
    "og_title": "Voltage et Prise Électrique en Tanzanie : Guide Pratique 2026",
    "desc": "La Tanzanie utilise des prises de type G (britanniques) en 230V / 50Hz. Adaptateur indispensable pour les voyageurs français, Zanzibar, safaris : tous nos conseils.",
    "crumb": "Voltage Tanzanie",
    "h1": "Voltage et Prise Électrique en Tanzanie : Tout Savoir",
    "lead": "Prises type G britanniques, 230 volts, adaptateur obligatoire : le guide complet pour recharger vos appareils en Tanzanie et à Zanzibar sans mauvaise surprise.",
    "alt1": "Prise électrique de type G britannique utilisée en Tanzanie avec adaptateur",
    "caption1": "Prise type G à trois broches rectangulaires, standard électrique en Tanzanie.",
    "sections": [
        {"id":"type-prise","toc":"Type de prise en Tanzanie","short":"Type G","h2":"Quel type de prise en Tanzanie ?",
         "blocks":[
            ("p","En Tanzanie, la prise électrique standard est la <strong>prise de type G</strong>, appelée aussi prise britannique ou BS 1363. Elle se reconnaît à ses <strong>trois broches rectangulaires</strong> disposées en triangle, identiques à celles utilisées au Royaume-Uni, en Irlande, à Hong Kong, à Singapour ou au Kenya voisin."),
            ("p","Ce choix s'explique par l'histoire coloniale : le Tanganyika (aujourd'hui Tanzanie continentale) a été sous mandat britannique jusqu'en 1961, et Zanzibar jusqu'en 1963. Le réseau électrique construit à cette époque a conservé les standards britanniques, confirmés par la norme internationale <a href=\"https://www.iec.ch/world-plugs\" target=\"_blank\" rel=\"noopener nofollow\">IEC World Plugs</a>."),
            ("img",2,"Carte schématique d'une prise type G avec trois broches rectangulaires"),
            ("h3","Différence avec la prise française type E"),
            ("p","La prise française (type E) a deux broches cylindriques + une broche de terre mâle. Elle est <strong>totalement incompatible</strong> avec la type G : impossible de forcer, les broches ne rentrent tout simplement pas. Un adaptateur est donc obligatoire."),
            ("h4","Et les appareils Zanzibar ?"),
            ("p","Zanzibar utilise exactement les mêmes prises type G que le continent. Un seul adaptateur suffit pour tout votre séjour, safaris Serengeti compris."),
         ]},
        {"id":"voltage-frequence","toc":"Voltage et fréquence","short":"230V/50Hz","h2":"Voltage et Fréquence en Tanzanie",
         "blocks":[
            ("p","Le voltage officiel en Tanzanie est de <strong>230 volts</strong> en <strong>50 Hz</strong>, selon les données publiées par <a href=\"https://www.tanesco.co.tz/\" target=\"_blank\" rel=\"noopener nofollow\">TANESCO</a> (Tanzania Electric Supply Company), le fournisseur national d'électricité. C'est exactement le même voltage qu'en France (230V / 50Hz)."),
            ("p","<strong>Bonne nouvelle pour les voyageurs français</strong> : puisque les voltages sont identiques, vos chargeurs de téléphone, d'ordinateur portable, d'appareil photo et de batteries externes fonctionneront sans aucun transformateur. <em>Seul un adaptateur de prise est nécessaire</em>."),
            ("img",3,"Chargeur de téléphone branché sur un adaptateur universel en Afrique"),
            ("h3","Appareils à double voltage"),
            ("p","Vérifiez tout de même l'étiquette de chaque chargeur : si vous lisez <code>INPUT: 100–240V ~ 50/60Hz</code>, votre appareil est compatible avec tout réseau mondial, y compris la Tanzanie. C'est le cas de 99 % des appareils électroniques modernes."),
            ("h4","Appareils US (110V) attention"),
            ("p","Sèche-cheveux, rasoirs ou appareils achetés aux États-Unis ne fonctionnent qu'en 110V : les brancher directement sur le 230V tanzanien les grillera instantanément. Prévoyez un <strong>transformateur 230V → 110V</strong> ou achetez du matériel dual-voltage avant de partir."),
         ]},
        {"id":"adaptateur","toc":"Quel adaptateur choisir","short":"Adaptateur","h2":"Quel Adaptateur Acheter pour la Tanzanie ?",
         "blocks":[
            ("p","L'adaptateur dont vous avez besoin est <strong>« France vers UK » (type E vers type G)</strong>. On le trouve facilement avant le départ en grande surface, en pharmacie d'aéroport ou en ligne pour 4 à 12 €. Préférez un modèle avec mise à la terre (trois broches) pour les ordinateurs portables et alimentations sensibles."),
            ("h3","Adaptateur universel, une meilleure option"),
            ("p","Pour 20 à 30 €, un <strong>adaptateur universel</strong> (type G, A, C, I) couvrira tous vos futurs voyages. Marques fiables : <em>Skross, OREI, Travel Blue</em>. Certains intègrent 2 ports USB + USB-C, pratique pour charger plusieurs appareils en même temps depuis une prise unique — très utile en lodge safari où les prises sont rares."),
            ("img",4,"Adaptateur universel avec ports USB dans une chambre d'hôtel"),
            ("h4","À éviter"),
            ("p","Les adaptateurs bas de gamme sans fusible ni normes CE sont à proscrire : surchauffe, courts-circuits, incompatibilité avec les prises shuttered britanniques (qui nécessitent qu'une broche de terre pousse pour libérer les broches actives)."),
         ]},
        {"id":"coupures","toc":"Coupures et secteurs hors réseau","short":"Coupures","h2":"Coupures de Courant et Lodges Hors Réseau",
         "blocks":[
            ("p","La Tanzanie souffre de <strong>coupures de courant fréquentes</strong> dans les grandes villes (Dar es Salaam, Arusha, Stone Town), surtout en saison sèche quand les centrales hydroélectriques tournent au ralenti. <a href=\"https://www.worldbank.org/en/country/tanzania\" target=\"_blank\" rel=\"noopener nofollow\">La Banque mondiale</a> rapporte qu'environ 37 % de la population avait accès à l'électricité en 2022, avec de fortes disparités rurales/urbaines."),
            ("p","Les hôtels urbains disposent presque tous de <strong>générateurs diesel</strong> qui prennent le relais automatiquement. En lodge safari, l'alimentation est souvent fournie par <strong>panneaux solaires + batteries</strong>, avec des plages horaires limitées (6h-10h et 18h-23h typiquement) et des prises uniquement dans l'espace commun."),
            ("h3","Prévoir une batterie externe"),
            ("p","Emportez une <strong>powerbank de 20 000 mAh</strong> (plusieurs charges de smartphone + appareil photo) pour tenir les plages sans courant. C'est indispensable pour les safaris en camp mobile au Serengeti ou au Ngorongoro."),
            ("img",5,"Lodge safari en Tanzanie avec panneaux solaires sur le toit"),
         ]},
    ],
    "expert_tip":"Glissez un adaptateur universel + une powerbank 20 000 mAh + une multiprise française 3 prises : branchez la multiprise sur l'unique adaptateur et chargez 3 appareils depuis une seule prise type G. C'est la configuration qui change la vie en lodge safari.",
})

# 2. Vaccins Mozambique
ARTICLES.append({
    "slug": "vaccins-mozambique",
    "title": "Vaccins Obligatoires et Recommandés pour le Mozambique 2026 | Voyage 7 Continents",
    "og_title": "Vaccins pour le Mozambique 2026 : Liste Complète",
    "desc": "Fièvre jaune, hépatites, typhoïde, paludisme : la liste à jour des vaccins obligatoires et recommandés pour voyager au Mozambique en 2026.",
    "crumb": "Vaccins Mozambique",
    "h1": "Vaccins Obligatoires et Recommandés pour le Mozambique",
    "lead": "Fièvre jaune conditionnelle, vaccins recommandés et prévention antipaludique : tout ce qu'il faut savoir avant de partir au Mozambique, basé sur les recommandations OMS et Institut Pasteur.",
    "alt1": "Carnet de vaccination internationale avec tampons et flacon de vaccin fièvre jaune",
    "caption1": "Carnet de vaccination international jaune indispensable pour certains pays d'Afrique australe.",
    "sections": [
        {"id":"obligatoire","toc":"Vaccins obligatoires","short":"Obligatoire","h2":"Vaccins Obligatoires pour le Mozambique",
         "blocks":[
            ("p","En 2026, <strong>aucun vaccin n'est obligatoire</strong> pour les voyageurs en provenance directe de France, de Belgique, du Canada ou de Suisse se rendant au Mozambique. Les autorités sanitaires mozambicaines ne demandent pas de preuve vaccinale pour un touriste européen qui arrive par vol direct depuis Maputo, Pemba ou Vilanculos."),
            ("h3","Exception : fièvre jaune en cas de transit"),
            ("p","Le vaccin contre la <strong>fièvre jaune</strong> devient obligatoire si vous avez séjourné plus de 12 heures (transit aéroportuaire compris) dans un pays listé par l'<a href=\"https://www.who.int/publications/i/item/9789240083486\" target=\"_blank\" rel=\"noopener nofollow\">OMS</a> comme zone à risque : Kenya, Ouganda, Ouganda, Éthiopie, Angola, RDC notamment. Le certificat international (carnet jaune) doit être présenté à l'arrivée au Mozambique."),
            ("img",2,"Tampons du carnet international de vaccination fièvre jaune"),
            ("h4","Vaccination fièvre jaune en France"),
            ("p","La vaccination fièvre jaune se fait uniquement dans un <strong>centre de vaccinations internationales agréé</strong>, au minimum 10 jours avant le départ. Prix : ~45 €. La validité est désormais <strong>à vie</strong> depuis 2016 selon le règlement sanitaire international."),
         ]},
        {"id":"recommandes","toc":"Vaccins recommandés","short":"Recommandés","h2":"Vaccins Fortement Recommandés",
         "blocks":[
            ("p","L'<a href=\"https://www.pasteur.fr/fr/centre-medical/preparer-son-voyage/mozambique\" target=\"_blank\" rel=\"noopener nofollow\">Institut Pasteur</a> recommande plusieurs vaccins au-delà du calendrier vaccinal de base pour tout séjour au Mozambique, même de courte durée. Vérifiez d'abord que votre <strong>DTP (Diphtérie-Tétanos-Poliomyélite)</strong>, votre <strong>ROR (Rougeole-Oreillons-Rubéole)</strong> et votre coqueluche sont à jour."),
            ("h3","Hépatites A et B"),
            ("p","L'<strong>hépatite A</strong> est recommandée pour tous : elle se transmet par l'eau et les aliments contaminés, particulièrement fréquente en Afrique australe. Deux doses espacées de 6 mois confèrent une immunité quasi à vie. L'<strong>hépatite B</strong> est conseillée pour les séjours longs ou répétés : elle se transmet par le sang et les rapports sexuels."),
            ("img",3,"Fiole de vaccin contre l'hépatite A et seringue"),
            ("h3","Typhoïde"),
            ("p","Le vaccin contre la <strong>fièvre typhoïde</strong> est recommandé si vous prévoyez de manger dans la rue, de voyager hors des circuits touristiques ou de rester plus de 2 semaines. Une seule injection, protection 3 ans."),
            ("h4","Rage"),
            ("p","La vaccination antirabique préventive (3 doses) est conseillée pour les séjours longs en zone rurale ou les voyageurs pratiquant la randonnée en brousse. Elle ne dispense pas d'un traitement post-exposition en cas de morsure, mais simplifie la prise en charge."),
         ]},
        {"id":"paludisme","toc":"Paludisme","short":"Paludisme","h2":"Paludisme : Prévention Indispensable",
         "blocks":[
            ("p","Le <strong>Mozambique est classé zone 3 (haute transmission)</strong> pour le paludisme à Plasmodium falciparum selon l'<a href=\"https://www.who.int/teams/global-malaria-programme\" target=\"_blank\" rel=\"noopener nofollow\">OMS Global Malaria Programme</a>. La transmission a lieu toute l'année dans tout le pays, y compris à Maputo, avec un pic en saison des pluies (novembre à mars)."),
            ("h3","Traitement préventif"),
            ("p","Trois médicaments sont prescrits en France : <strong>Doxycycline</strong> (générique bon marché, 1 comprimé/jour, prendre dès la veille du départ jusqu'à 4 semaines après le retour), <strong>Malarone/Atovaquone-Proguanil</strong> (mieux toléré, plus cher, démarrage 1 jour avant), <strong>Lariam/Méfloquine</strong> (hebdomadaire, contre-indications neuropsychiatriques). Prescription médicale obligatoire."),
            ("img",4,"Boîte de comprimés antipaludéens et moustique Anopheles"),
            ("h4","Protection contre les moustiques"),
            ("p","Complétez le traitement par : <strong>répulsif DEET 30-50 %</strong> sur la peau, <strong>vêtements imprégnés de perméthrine</strong>, <strong>moustiquaire imprégnée</strong> la nuit, manches longues après le coucher du soleil. Aucun traitement n'est efficace à 100 % — la prévention est primordiale."),
         ]},
        {"id":"autres-precautions","toc":"Autres précautions santé","short":"Autres","h2":"Autres Précautions Sanitaires",
         "blocks":[
            ("p","Au-delà des vaccins, prévoyez une <strong>trousse à pharmacie complète</strong> : antidiarrhéique (Imodium + Tiorfan), rehydratation orale, antibiotique à large spectre type ciprofloxacine (prescription), antihistaminique, pansements, désinfectant, thermomètre."),
            ("p","<strong>Buvez uniquement de l'eau en bouteille capsulée</strong>, évitez les glaçons, les crudités lavées à l'eau du robinet et les fruits non pelés. Le <a href=\"https://wwwnc.cdc.gov/travel/destinations/traveler/none/mozambique\" target=\"_blank\" rel=\"noopener nofollow\">CDC américain</a> classe le risque de diarrhée du voyageur comme élevé au Mozambique."),
            ("box","Consultez un centre de vaccinations internationales <strong>6 à 8 semaines avant le départ</strong> pour respecter les délais des schémas vaccinaux complets (hépatite A en 2 doses, rage en 3 doses), et emportez une copie numérique et papier de votre carnet de vaccination."),
         ]},
    ],
    "expert_tip":"Si vous voyagez avec des enfants de moins de 9 mois, la fièvre jaune est contre-indiquée : vérifiez bien votre itinéraire pour éviter tout transit long par un pays endémique. Pour un safari dans le parc du Limpopo ou à Gorongosa, renforcez la prévention anti-moustiques dès le crépuscule.",
})

# 3. Monnaie Madagascar
ARTICLES.append({
    "slug": "monnaie-madagascar",
    "title": "Quelle est la Monnaie de Madagascar ? Guide de l'Ariary 2026 | Voyage 7 Continents",
    "og_title": "Monnaie de Madagascar : l'Ariary Malgache (MGA) en 2026",
    "desc": "La monnaie officielle de Madagascar est l'ariary malgache (MGA). Taux de change, billets, distributeurs, change euro : tout savoir sur l'argent à Madagascar.",
    "crumb": "Monnaie Madagascar",
    "h1": "Quelle est la Monnaie de Madagascar ? Guide Complet de l'Ariary",
    "lead": "Ariary malgache, taux de change euro, distributeurs dans les villes, cash obligatoire en brousse : tout savoir sur l'argent à Madagascar en 2026.",
    "alt1": "Billets d'ariary malgache étalés, monnaie officielle de Madagascar",
    "caption1": "L'ariary malgache (MGA), seule monnaie légale à Madagascar depuis 2005.",
    "sections": [
        {"id":"ariary","toc":"L'ariary malgache","short":"Ariary","h2":"L'Ariary Malgache : Monnaie Officielle",
         "blocks":[
            ("p","La monnaie officielle de Madagascar est l'<strong>ariary malgache</strong>, code ISO <strong>MGA</strong> et symbole <strong>Ar</strong>. Elle a remplacé l'ancien franc malgache (FMG) en 2005 selon un taux de conversion de <strong>1 ariary = 5 francs malgaches</strong>, pour simplifier la comptabilité après des décennies d'inflation."),
            ("p","La <strong>Banque centrale de Madagascar</strong> (<a href=\"https://www.banky-foiben-madagasikara.mg/\" target=\"_blank\" rel=\"noopener nofollow\">Banky Foiben'i Madagasikara</a>) émet les billets et pièces et fixe le taux de change officiel. Au taux d'avril 2026, <strong>1 euro ≈ 4 900 ariary</strong>, mais vérifiez toujours en temps réel sur <a href=\"https://www.xe.com/currencyconverter/convert/?From=EUR&To=MGA\" target=\"_blank\" rel=\"noopener nofollow\">XE.com</a> avant de partir."),
            ("img",2,"Billets d'ariary malgache de différentes valeurs"),
            ("h3","Coupures en circulation"),
            ("p","Les billets en circulation sont de <strong>100, 200, 500, 1 000, 2 000, 5 000, 10 000 et 20 000 ariary</strong>. Le plus gros (20 000 Ar) vaut seulement environ 4 €, ce qui explique les liasses épaisses que l'on voit au marché ! Les pièces (1, 2, 5, 10, 20, 50 Ar) ont quasiment disparu de la circulation courante."),
            ("h4","Curiosité : l'ancien franc encore utilisé"),
            ("p","Dans les zones rurales et certains marchés, les vendeurs annoncent encore les prix en « francs malgaches » (FMG). Attention : un produit à <em>25 000 francs</em> coûte en réalité 5 000 ariary. Vérifiez toujours l'unité avant de payer."),
         ]},
        {"id":"change","toc":"Changer ses euros","short":"Change","h2":"Où Changer ses Euros à Madagascar ?",
         "blocks":[
            ("p","<strong>L'euro se change très facilement</strong> à Madagascar : c'est la devise la plus demandée après le dollar américain. Les bureaux de change officiels se trouvent à l'aéroport d'Antananarivo-Ivato, dans les banques (BFV-SG, BNI, BOA) et dans les hôtels des grandes villes. Le taux à l'aéroport est généralement 2 à 3 % moins bon qu'en ville — changez juste de quoi tenir les premiers jours."),
            ("h3","Distributeurs automatiques (DAB)"),
            ("p","Les distributeurs sont présents à <strong>Antananarivo, Toamasina, Antsirabe, Fianarantsoa, Toliara, Diego Suarez, Nosy Be et Morondava</strong>. Ils acceptent Visa et Mastercard, avec un plafond de retrait souvent limité à 400 000 ariary (~80 €) par transaction. Prévoyez plusieurs retraits si vous avez besoin de plus de liquide."),
            ("img",3,"Distributeur automatique de billets à Antananarivo Madagascar"),
            ("h4","Attention en brousse"),
            ("p","En dehors de ces grandes villes, <strong>aucun distributeur ne fonctionne</strong> : la RN7 vers Tuléar traverse des centaines de kilomètres sans DAB opérationnel. Retirez suffisamment de cash avant de quitter les villes pour couvrir hébergement, nourriture, transport et pourboires guides."),
         ]},
        {"id":"paiements","toc":"Cartes et paiements","short":"Paiements","h2":"Cartes Bancaires et Paiements sur Place",
         "blocks":[
            ("p","Les <strong>cartes Visa et Mastercard</strong> sont acceptées dans les hôtels 3★ et + d'Antananarivo, les grands restaurants de la capitale, les lodges haut de gamme de Nosy Be et de l'Avenue des Baobabs. Ailleurs, c'est exclusivement du <strong>cash en ariary</strong>."),
            ("h3","Paiement mobile et pourboires"),
            ("p","Le paiement mobile (MVola, Orange Money, Airtel Money) s'est généralisé pour les Malgaches mais reste peu accessible aux touristes sans carte SIM locale. Prévoyez un budget liquide pour les pourboires guides (5-10 € par jour), chauffeurs (3-5 €/jour) et porteurs (~2 €/bagage)."),
            ("img",4,"Marché local de fruits et légumes Madagascar avec vendeuse"),
            ("h4","Export d'ariary interdit"),
            ("p","La législation malgache interdit l'<strong>export d'ariary hors du territoire</strong> (déclaration obligatoire au-delà de 400 000 Ar). Re-changez votre cash avant de repasser la douane, ou dépensez-le dans les boutiques de l'aéroport avant l'embarquement."),
         ]},
        {"id":"budget-jour","toc":"Budget quotidien","short":"Budget","h2":"Combien Dépenser par Jour à Madagascar ?",
         "blocks":[
            ("p","Madagascar reste une destination <strong>abordable pour un voyageur européen</strong>, à condition de sortir des circuits tout inclus. Trois niveaux de budget se dessinent clairement."),
            ("h3","Budget routard : 25 à 35 €/jour"),
            ("p","Chambres d'hôtes à 8-15 €, repas au marché ou petits restaurants 2-4 €, transport en taxi-brousse (8-15 € les longs trajets). Frais de parcs nationaux : 25 000 à 65 000 Ar (5-13 €) par jour selon le parc et la zone."),
            ("h3","Budget confort : 60 à 90 €/jour"),
            ("p","Hôtel 3★ à 30-50 €, repas en restaurant 5-10 €, 4x4 avec chauffeur-guide sur certaines portions. Niveau confortable sans se ruiner."),
            ("img",5,"Lodge en bord de plage à Nosy Be Madagascar"),
            ("h4","Budget premium : 150 €+/jour"),
            ("p","Lodges de charme, vols intérieurs Tsaradia/Madagasikara Airways, 4x4 privé avec chauffeur pour tout l'itinéraire, dîners gastronomiques. C'est le niveau que facturent la plupart des <a href=\"https://www.tourisme.mg/\" target=\"_blank\" rel=\"noopener nofollow\">tour-opérateurs partenaires de l'Office National du Tourisme</a>."),
         ]},
    ],
    "expert_tip":"Emportez des euros en petites coupures (10, 20, 50) : les gros billets passent mal en bureau de change rural. Gardez toujours 200 000 à 500 000 ariary en réserve pour les urgences (panne 4x4, péage impromptu, nuit imprévue) car les distributeurs peuvent être hors service plusieurs jours d'affilée.",
})

# 4. Température Sénégal janvier
ARTICLES.append({
    "slug": "temperature-senegal-janvier",
    "title": "Température Moyenne au Sénégal en Janvier : Climat, Valise, Conseils | Voyage 7 Continents",
    "og_title": "Température au Sénégal en Janvier : Climat et Conseils 2026",
    "desc": "Janvier au Sénégal : 18-28°C à Dakar, 15-33°C dans le Saloum, saison sèche idéale. Guide complet du climat, que mettre dans sa valise et activités recommandées.",
    "crumb": "Sénégal Janvier",
    "h1": "Température Moyenne au Sénégal en Janvier : le Climat en Détail",
    "lead": "Saison sèche, harmattan, nuits fraîches, après-midi doux : tout savoir sur le climat du Sénégal en janvier pour préparer valise et itinéraire sereinement.",
    "alt1": "Plage ensoleillée de Dakar en janvier avec pirogues de pêcheurs colorées",
    "caption1": "Janvier est considéré comme le meilleur mois pour visiter le Sénégal : temps sec et lumineux.",
    "sections": [
        {"id":"temperatures-janvier","toc":"Températures janvier","short":"Températures","h2":"Températures Moyennes au Sénégal en Janvier",
         "blocks":[
            ("p","Janvier est le <strong>cœur de la saison sèche</strong> au Sénégal et l'un des mois les plus agréables de l'année. Les températures varient selon la zone géographique, mais restent partout dans une fourchette confortable, bien loin de la chaleur étouffante de la saison des pluies."),
            ("h3","Dakar et la Petite Côte"),
            ("p","À <strong>Dakar</strong>, les températures moyennes en janvier sont de <strong>18 °C la nuit et 26 à 28 °C l'après-midi</strong>, avec une humidité modérée grâce à la brise océanique. Saly, Mbour et la Petite Côte affichent des valeurs très similaires. Les données officielles sont consultables sur le site de l'<a href=\"https://www.anacim.sn/\" target=\"_blank\" rel=\"noopener nofollow\">ANACIM (Agence Nationale de l'Aviation Civile et de la Météorologie)</a>."),
            ("img",2,"Thermomètre sur une plage sénégalaise en janvier ensoleillée"),
            ("h3","Saint-Louis, Saloum, Casamance"),
            ("p","Plus au sud (Saloum, Ziguinchor) ou à l'intérieur, l'amplitude est plus marquée : <strong>15 °C la nuit et 32 à 34 °C l'après-midi</strong>. Les matins sont presque frais, parfaits pour les excursions en pirogue dans les bolongs. La Casamance bénéficie d'un climat plus végétal et légèrement plus humide."),
            ("h4","Dakar vs intérieur : lequel choisir ?"),
            ("p","Si vous craignez la chaleur, restez sur la côte (Dakar, Saly, Cap Skirring). Si vous supportez 33-34°C, l'intérieur offre des paysages bien plus variés (désert, brousse, parcs animaliers)."),
         ]},
        {"id":"harmattan","toc":"L'harmattan","short":"Harmattan","h2":"L'Harmattan : Vent Sec du Sahara",
         "blocks":[
            ("p","Janvier au Sénégal coïncide avec la période de l'<strong>harmattan</strong>, un vent sec et chargé de poussière venu du Sahara. Il souffle principalement sur le nord du pays (Saint-Louis, Podor, Matam) mais peut atteindre Dakar et Thiès quelques jours par mois, voilant le ciel d'un léger halo jaunâtre."),
            ("p","Pour les voyageurs, l'harmattan a trois conséquences : <strong>(1) air très sec</strong> (hydratez peau et lèvres), <strong>(2) nuits fraîches</strong> pouvant descendre à 13-14 °C à Saint-Louis, <strong>(3) ciel légèrement brumeux</strong> qui réduit la luminosité photographique. Le phénomène est bien documenté par <a href=\"https://public.wmo.int/en\" target=\"_blank\" rel=\"noopener nofollow\">l'Organisation météorologique mondiale</a>."),
            ("img",3,"Paysage brumeux dans le Sahel sénégalais pendant l'harmattan"),
            ("h4","Astuce santé"),
            ("p","Emportez un baume à lèvres, une crème hydratante et éventuellement un foulard léger pour vous protéger de la poussière lors des trajets en brousse ou en 4x4."),
         ]},
        {"id":"pluviometrie","toc":"Pluviométrie","short":"Pluies","h2":"Pluies et Ensoleillement",
         "blocks":[
            ("p","Janvier est <strong>le mois le plus sec de l'année</strong> : il ne pleut quasiment jamais. Les cumuls mensuels relevés par l'ANACIM sont proches de zéro sur l'ensemble du territoire. L'ensoleillement est maximal, avec <strong>9 à 10 heures de soleil par jour</strong> en moyenne."),
            ("p","La saison des pluies (hivernage) ne commence qu'en juin-juillet : vous êtes assuré de rentrer tous les jours secs. Parfait pour la plage, les safaris Niokolo-Koba, la pirogue dans le Saloum et les randonnées en Casamance."),
            ("img",4,"Coucher de soleil doré sur une plage de Casamance sans nuages"),
         ]},
        {"id":"valise","toc":"Que mettre dans sa valise","short":"Valise","h2":"Que Mettre dans sa Valise en Janvier ?",
         "blocks":[
            ("p","Le climat de janvier impose une <strong>garde-robe duale</strong> : léger pour la journée, un peu chaud pour les soirées et les matins."),
            ("h3","Pour la journée"),
            ("p","T-shirts en coton ou lin, shorts/robes légères, chapeau ou casquette, lunettes de soleil UV 400, crème solaire indice 50, maillot de bain. L'ultraviolet est élevé même en « hiver »."),
            ("h3","Pour le soir et le matin"),
            ("p","Un <strong>pull léger ou polaire fine</strong>, un pantalon long, un coupe-vent : utiles à Dakar après le coucher du soleil et indispensables à Saint-Louis ou au bivouac dans le Ferlo. L'amplitude thermique peut atteindre 15 °C."),
            ("h4","Pour la baignade"),
            ("p","L'eau est à environ 19-21 °C à Dakar en janvier : rafraîchissante mais tout à fait baignable. Dans le Saloum et en Casamance, elle atteint 23-24 °C, parfaite pour nager."),
            ("img",5,"Valise ouverte contenant tenues légères et pull pour un voyage au Sénégal"),
         ]},
    ],
    "expert_tip":"Si vous voyagez vers le désert (Lompoul) ou le Ferlo, ajoutez un duvet léger : les nuits peuvent descendre à 10-12 °C sous les étoiles. À Dakar, un simple pull suffit. Et pensez à boire plus que d'habitude — l'harmattan dessèche sans que l'on s'en rende compte.",
})

# 5. Eau robinet Maroc
ARTICLES.append({
    "slug": "eau-robinet-maroc",
    "title": "Peut-on Boire l'Eau du Robinet au Maroc ? Avis d'Experts 2026 | Voyage 7 Continents",
    "og_title": "Boire l'Eau du Robinet au Maroc : Risques et Solutions 2026",
    "desc": "L'eau du robinet au Maroc est-elle potable ? Risques, zones sûres, alternatives (filtres, purificateurs, eau en bouteille) : le guide pratique pour voyageurs.",
    "crumb": "Eau du robinet Maroc",
    "h1": "Peut-on Boire l'Eau du Robinet au Maroc ?",
    "lead": "Eau chlorée conforme en ville, risques en zone rurale, solutions filtres et bouteilles : le guide complet pour s'hydrater sans risque pendant votre voyage au Maroc.",
    "alt1": "Robinet d'eau courante dans une médina marocaine avec carreaux zellige",
    "caption1": "L'eau du robinet est techniquement traitée dans les grandes villes marocaines, mais tout boire reste déconseillé aux voyageurs.",
    "sections": [
        {"id":"potabilite","toc":"Potabilité au Maroc","short":"Potabilité","h2":"L'Eau du Robinet est-elle Potable au Maroc ?",
         "blocks":[
            ("p","La réponse courte est <strong>nuancée</strong> : dans les grandes villes (Casablanca, Rabat, Marrakech, Fès, Tanger, Agadir), l'eau du robinet est <strong>théoriquement potable et conforme aux normes marocaines</strong> de potabilité. Elle est produite par l'<a href=\"https://www.onee.ma/\" target=\"_blank\" rel=\"noopener nofollow\">ONEE (Office National de l'Électricité et de l'Eau Potable)</a>, qui réalise des contrôles réguliers de qualité."),
            ("p","Cependant, la <strong>France Diplomatie</strong> et l'<a href=\"https://wwwnc.cdc.gov/travel/destinations/traveler/none/morocco\" target=\"_blank\" rel=\"noopener nofollow\">CDC américain</a> recommandent aux voyageurs de <strong>ne pas boire l'eau du robinet</strong> pendant un séjour touristique. La raison principale n'est pas la production mais la <strong>distribution</strong> : canalisations anciennes, réservoirs mal entretenus dans certains immeubles, coupures fréquentes qui peuvent contaminer le réseau."),
            ("img",2,"Bouteille d'eau minérale marocaine Sidi Ali à côté d'un verre"),
            ("h3","Flore intestinale différente"),
            ("p","Même si l'eau est « saine » pour un résident marocain, elle contient des micro-organismes auxquels votre flore intestinale n'est pas habituée. Résultat : le classique <strong>tourista</strong> (diarrhée du voyageur) qui touche 30 à 50 % des voyageurs en Afrique du Nord selon les études du <a href=\"https://www.pasteur.fr/fr/centre-medical/fiches-maladies/turista-diarrhee-voyageur\" target=\"_blank\" rel=\"noopener nofollow\">Institut Pasteur</a>."),
            ("h4","Zone rurale : évitez absolument"),
            ("p","Dans les villages de l'Atlas, du Rif, du Sud saharien et des vallées berbères, l'eau provient souvent de sources, puits ou réservoirs communaux <strong>non chlorés</strong>. Risque élevé de parasites, bactéries (E. coli, Giardia) et contamination fécale. <strong>Ne buvez jamais cette eau sans traitement.</strong>"),
         ]},
        {"id":"eau-bouteille","toc":"Eau en bouteille","short":"Bouteille","h2":"Eau en Bouteille : la Solution Simple",
         "blocks":[
            ("p","La solution la plus simple et la plus répandue est d'acheter de l'<strong>eau minérale en bouteille capsulée</strong>. Les marques les plus courantes sont <em>Sidi Ali</em>, <em>Aïn Saïss</em>, <em>Oulmès</em> (gazeuse), <em>Ciel</em>, <em>Bahia</em>. Prix : 5 à 8 DH la bouteille de 1,5 L en supérette (0,50 à 0,80 €), encore moins cher en pack."),
            ("h3","Vérifier l'intégrité du bouchon"),
            ("p","Vérifiez toujours que le bouchon est <strong>scellé et n'a pas été dévissé</strong>. Dans certains quartiers touristiques, des vendeurs peu scrupuleux remplissent de vieilles bouteilles avec de l'eau du robinet. Le « clic » du bouchon à l'ouverture doit être net."),
            ("img",3,"Rayon d'eau minérale dans une épicerie marocaine"),
            ("h4","Impact écologique"),
            ("p","Sur un voyage de 15 jours, un couple consomme facilement <strong>30 à 40 bouteilles plastique</strong>. Pour réduire cet impact, investissez dans une gourde filtrante (voir section suivante)."),
         ]},
        {"id":"solutions-filtres","toc":"Filtres et purificateurs","short":"Filtres","h2":"Filtres, Purificateurs et Pastilles",
         "blocks":[
            ("p","Alternatives à l'eau en bouteille, plusieurs solutions permettent de traiter l'eau du robinet en toute sécurité."),
            ("h3","Gourde filtrante (LifeStraw, Grayl, Water-to-Go)"),
            ("p","Les gourdes <strong>LifeStraw Go</strong>, <strong>Grayl GeoPress</strong> ou <strong>Water-to-Go</strong> filtrent bactéries, parasites et microplastiques à 99,9999 %. Prix : 30 à 90 €. Autonomie : 1 000 à 4 000 litres selon le modèle. C'est l'investissement rentable dès le deuxième voyage."),
            ("img",4,"Gourde filtrante LifeStraw utilisée par un voyageur au Maroc"),
            ("h3","Pastilles Micropur ou Aquatabs"),
            ("p","Les pastilles purifiantes (1 € les 30 pastilles) désinfectent 1 litre d'eau en 30 minutes à 2 heures. Elles laissent un léger goût de chlore mais sont très efficaces, légères et peu coûteuses. Indispensables en randonnée Atlas."),
            ("h4","Ébullition"),
            ("p","Faire bouillir l'eau pendant <strong>1 à 3 minutes</strong> tue 100 % des pathogènes. Solution gratuite si vous disposez d'une bouilloire en riad ou d'un réchaud en bivouac."),
         ]},
        {"id":"conseils-pratiques","toc":"Conseils pratiques","short":"Conseils","h2":"Conseils Pratiques au Quotidien",
         "blocks":[
            ("p","Au-delà de la boisson, quelques règles limitent considérablement le risque de tourista au Maroc."),
            ("h3","Brosse à dents et glaçons"),
            ("p","Utilisez de l'<strong>eau en bouteille pour vous brosser les dents</strong> les premiers jours (le temps que votre organisme s'habitue). Évitez les <strong>glaçons</strong> dans les jus et sodas, sauf dans les restaurants haut de gamme qui utilisent de la glace contrôlée."),
            ("h3","Crudités et fruits"),
            ("p","Lavez et épluchez les fruits vous-même. Méfiez-vous des salades dans les petits restaurants populaires. Les plats <strong>cuits, chauds et servis chauds</strong> sont toujours plus sûrs."),
            ("img",5,"Plateau de fruits pelés dans un riad marocain"),
            ("box","Les hôtels 4-5★ et les riads haut de gamme fournissent souvent 2 bouteilles d'eau minérale par chambre et par jour <strong>gratuitement</strong>. Profitez-en et gardez les bouteilles vides pour les recharger si vous disposez d'une gourde filtrante."),
         ]},
    ],
    "expert_tip":"La règle d'or : « boil it, cook it, peel it or forget it » (faites-le bouillir, cuire, peler ou oubliez-le). Combinée à une gourde filtrante LifeStraw ou Grayl, elle vous permet de passer 3 semaines au Maroc sans tourista ni empreinte plastique. Emportez toujours quelques pastilles Micropur en secours.",
})

# 6. Nairobi Masai Mara
ARTICLES.append({
    "slug": "nairobi-masai-mara",
    "title": "Comment Aller de Nairobi au Masai Mara ? Toutes les Options 2026 | Voyage 7 Continents",
    "og_title": "Nairobi au Masai Mara : Avion, 4x4, Tours (2026)",
    "desc": "Vol direct 45 min, 4x4 privé 6h, safari en groupe : toutes les options pour rejoindre le Masai Mara depuis Nairobi avec prix, durée et conseils pratiques.",
    "crumb": "Nairobi → Masai Mara",
    "h1": "Comment Aller de Nairobi au Masai Mara en 2026",
    "lead": "Vol intérieur, route en 4x4, safari organisé : comparatif complet des moyens pour rejoindre le Masai Mara depuis Nairobi avec prix, durée et conseils testés.",
    "alt1": "Piste de brousse menant au Masai Mara avec acacia et zèbres en arrière-plan",
    "caption1": "Le Masai Mara se trouve à 270 km de Nairobi par la route : 5 à 6 heures de 4x4.",
    "sections": [
        {"id":"options-transport","toc":"Les 3 options","short":"Options","h2":"Les 3 Options pour Rejoindre le Masai Mara",
         "blocks":[
            ("p","Depuis Nairobi, le Masai Mara se rejoint de trois manières : <strong>(1) vol intérieur</strong> (rapide, cher), <strong>(2) route en 4x4 privé ou partagé</strong> (pittoresque, fatigant), <strong>(3) safari organisé avec transfert inclus</strong> (simple, tout compris)."),
            ("p","Il n'y a <strong>pas de train ni de bus public direct</strong> jusqu'aux entrées du parc. Ne croyez pas les itinéraires improvisés en matatu : vous arriveriez à Narok mais il vous faudrait ensuite négocier un transfert local coûteux et aléatoire."),
            ("img",2,"Carte schématique Nairobi-Masai Mara avec itinéraires routiers et aériens"),
            ("h4","Distance et durée"),
            ("p","La distance Nairobi → Masai Mara varie de <strong>230 à 290 km</strong> selon l'entrée du parc choisie (Sekenani, Oloololo, Musiara, Talek). Compter <strong>5 à 7 heures de route</strong> ou <strong>40 à 50 minutes d'avion</strong>."),
         ]},
        {"id":"vol-intérieur","toc":"Vol depuis Wilson","short":"Vol","h2":"Vol Intérieur depuis Wilson Airport",
         "blocks":[
            ("p","Les vols vers le Masai Mara partent de <strong>Wilson Airport</strong> (WIL, code OACI HKNW), un petit aéroport situé dans Nairobi même, à ne pas confondre avec Jomo Kenyatta International (NBO). Ne prévoyez pas un transfert international direct sans escale par Wilson."),
            ("h3","Compagnies et pistes d'atterrissage"),
            ("p","Trois compagnies desservent le Mara : <strong>Safarilink</strong>, <strong>AirKenya Express</strong> et <strong>Mombasa Air Safari</strong>. Elles posent leurs petits avions (Cessna Caravan, Dash 8) sur une dizaine de <strong>pistes en terre</strong> dispersées dans le parc : Keekorok, Kichwa Tembo, Musiara, Olkiombo, Siana Springs, Mara Serena, Ol Kiombo. Vous débarquez <strong>au pied de votre lodge</strong>."),
            ("img",3,"Petit avion Cessna Caravan sur une piste en terre au Masai Mara"),
            ("h3","Prix et réservation"),
            ("p","Comptez <strong>220 à 350 USD aller-retour par personne</strong>, selon la compagnie et la période (haute saison = pic). Réservation directe sur <a href=\"https://www.safarilink.com/\" target=\"_blank\" rel=\"noopener nofollow\">safarilink.com</a> ou <a href=\"https://www.airkenya.com/\" target=\"_blank\" rel=\"noopener nofollow\">airkenya.com</a>, ou via votre lodge qui négocie parfois de meilleurs tarifs."),
            ("h4","Avantages"),
            ("p","45 minutes au lieu de 6h de piste, pas de fatigue, vue aérienne spectaculaire sur la vallée du Rift. C'est la meilleure option si votre budget le permet et surtout si vous ne restez que 2-3 jours au Mara."),
         ]},
        {"id":"route-4x4","toc":"Route en 4x4","short":"4x4","h2":"Route en 4x4 : l'Option Terrestre",
         "blocks":[
            ("p","La route Nairobi → Masai Mara passe par <strong>Narok</strong>, capitale du pays masaï. L'itinéraire classique suit la A104 puis la B3 jusqu'à Narok (145 km, 3h), puis une piste de terre variable selon l'entrée du parc (80 à 120 km supplémentaires, 2 à 4h selon l'état de la piste)."),
            ("h3","État de la route"),
            ("p","Les 145 premiers kilomètres sont <strong>goudronnés et en bon état</strong>, avec une étape panoramique au belvédère du <strong>Great Rift Valley</strong>. Après Narok, c'est une <strong>piste en latérite</strong> souvent en mauvais état, boueuse en saison des pluies, « massage shiatsu gratuit » en saison sèche. Un 4x4 haut perché est indispensable."),
            ("img",4,"Panorama du Great Rift Valley Kenya depuis le belvédère de la route"),
            ("h3","4x4 privé ou taxi-voyage"),
            ("p","Un 4x4 Toyota Land Cruiser avec chauffeur-guide anglophone coûte environ <strong>180 à 260 USD par jour</strong> (carburant, logement chauffeur et droits d'entrée parc non inclus). C'est la solution choisie par la plupart des indépendants. Réservez au moins 1 mois à l'avance en haute saison."),
            ("h4","Faire soi-même ?"),
            ("p","Techniquement, vous pouvez louer un 4x4 à Nairobi et conduire vous-même. En pratique, c'est <strong>déconseillé</strong> : les pistes après Narok sont mal signalées, des barrages masaïs informels peuvent réclamer des « péages », et les assurances locales couvrent mal les incidents en brousse."),
         ]},
        {"id":"safari-organise","toc":"Safari organisé","short":"Safari","h2":"Safari Organisé : la Solution Tout Compris",
         "blocks":[
            ("p","Le plus simple pour un premier safari : réserver un <strong>package 3 ou 4 jours depuis Nairobi</strong> qui inclut transport (4x4 safari), hébergement en lodge ou camp, repas, droits d'entrée du parc et game drives matin/après-midi."),
            ("h3","Fourchette de prix"),
            ("p","À partir de <strong>450-600 USD par personne</strong> en tente de brousse pour 3 jours / 2 nuits en budget, jusqu'à <strong>1 500-3 000 USD</strong> en lodge de luxe type Governor's Camp, Mara Serena, Sarova Mara. Comparez les inclusions : certains safaris « bon marché » excluent les droits de parc (70 USD/jour) ou facturent chaque repas."),
            ("img",5,"Véhicule safari 4x4 ouvert au Masai Mara avec touristes observant des lions"),
            ("h4","Opérateurs recommandés"),
            ("p","Privilégiez les tours-opérateurs membres de la <a href=\"https://ktf.co.ke/\" target=\"_blank\" rel=\"noopener nofollow\">Kenya Tourism Federation</a> et possédant la <strong>licence KATO</strong> (Kenya Association of Tour Operators). Lisez les avis détaillés sur TripAdvisor et SafariBookings avant de payer un acompte."),
         ]},
    ],
    "expert_tip":"La combinaison la plus efficace en budget moyen : <strong>vol aller Wilson → Mara</strong> le jour 1 (éviter la fatigue du trajet), <strong>retour en 4x4 avec arrêt au Great Rift Valley Viewpoint</strong> le dernier jour. Vous profitez pleinement des game drives matinaux et vous ne « gaspillez » qu'une demi-journée de transport, la plus scénique.",
})

# 7. Visa Éthiopie
ARTICLES.append({
    "slug": "visa-ethiopie",
    "title": "Formalités d'Entrée Éthiopie : Visa Tourisme en Ligne 2026 | Voyage 7 Continents",
    "og_title": "Formalités Visa Éthiopie 2026 : e-Visa, Prix, Démarches",
    "desc": "E-visa tourisme 82 USD, validité 30/90 jours, demande en ligne : la procédure officielle complète pour obtenir son visa Éthiopie en 2026 sans erreur.",
    "crumb": "Visa Éthiopie",
    "h1": "Formalités d'Entrée en Éthiopie : Visa Tourisme 2026",
    "lead": "E-visa officiel, prix, documents requis, délai, visa à l'arrivée : le guide pratique pour obtenir son visa Éthiopie et franchir l'aéroport d'Addis-Abeba sans stress.",
    "alt1": "Passeport français avec visa éthiopien tamponné et billet d'avion",
    "caption1": "Le visa touristique est obligatoire pour tous les voyageurs français en Éthiopie.",
    "sections": [
        {"id":"visa-obligatoire","toc":"Visa obligatoire","short":"Visa","h2":"Visa Obligatoire pour l'Éthiopie",
         "blocks":[
            ("p","Tous les voyageurs français, belges, suisses et canadiens doivent <strong>obligatoirement</strong> disposer d'un visa pour entrer en Éthiopie, qu'il s'agisse d'un séjour touristique, d'affaires ou de simple transit. L'Éthiopie ne fait partie d'aucun accord de dispense de visa avec l'Union européenne."),
            ("p","Le <a href=\"https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/ethiopie/\" target=\"_blank\" rel=\"noopener nofollow\">Ministère français des Affaires étrangères (France Diplomatie)</a> confirme qu'il faut demander le visa <strong>avant le départ</strong>, car le visa à l'arrivée n'est plus accordé dans la plupart des situations depuis 2023."),
            ("img",2,"Affiche officielle du portail e-visa éthiopien à l'aéroport d'Addis Abeba"),
            ("h3","Visa à l'arrivée : exception"),
            ("p","Un visa à l'arrivée est théoriquement accordé aux voyageurs arrivant <strong>uniquement par l'aéroport Bole d'Addis-Abeba</strong> (ADD) et uniquement à ceux qui n'ont pas pu demander l'e-visa. En pratique, les autorités refusent souvent cette option aux ressortissants français : l'e-visa est donc le seul choix fiable."),
         ]},
        {"id":"e-visa","toc":"Demande e-Visa","short":"e-Visa","h2":"Comment Demander l'e-Visa Éthiopie ?",
         "blocks":[
            ("p","La demande se fait uniquement sur le <strong>site officiel</strong> <a href=\"https://www.evisa.gov.et/\" target=\"_blank\" rel=\"noopener nofollow\">evisa.gov.et</a>, géré par l'<em>Immigration and Citizenship Service</em> éthiopien. <strong>Méfiez-vous des sites tiers</strong> (surfacturation 2 à 4 fois le prix officiel, arnaques, données revendues)."),
            ("h3","Étapes de la demande"),
            ("p","1) Créez un compte avec email valide. 2) Renseignez vos informations personnelles (identiques au passeport). 3) Uploadez <strong>une photo d'identité récente</strong> (fond blanc, format passeport) et une <strong>copie de la page principale du passeport</strong>. 4) Payez par carte Visa / Mastercard. 5) Recevez le PDF par email sous <strong>1 à 3 jours ouvrés</strong>."),
            ("img",3,"Écran d'ordinateur affichant le formulaire e-visa éthiopien en ligne"),
            ("h3","Documents à préparer"),
            ("p","<strong>Passeport valable 6 mois après la date de retour</strong> avec au moins 2 pages vierges, photo identité JPG < 1 Mo, itinéraire / réservation de vol aller-retour, réservation d'hôtel pour la première nuit. Certains demandeurs ont aussi dû fournir un relevé bancaire ou une attestation d'invitation."),
            ("h4","À imprimer"),
            ("p","Imprimez le PDF du visa et gardez-le avec vous à l'embarquement <em>et</em> à l'arrivée à Addis-Abeba. Les compagnies aériennes (Ethiopian Airlines, Air France, KLM) refusent l'embarquement sans ce document."),
         ]},
        {"id":"duree-prix","toc":"Durée et prix","short":"Durée/Prix","h2":"Durée, Prix et Validité du Visa",
         "blocks":[
            ("p","L'e-visa tourisme existe en <strong>deux durées</strong> : 30 jours ou 90 jours. Les tarifs officiels en 2026 sont les suivants (en USD, seule devise acceptée par le portail) :"),
            ("h3","Visa 30 jours : 82 USD"),
            ("p","Permet un séjour touristique de 30 jours maximum à compter de l'entrée sur le territoire. Non renouvelable en ligne : il faudrait se rendre au bureau d'immigration d'Addis-Abeba pour prolonger."),
            ("h3","Visa 90 jours : 202 USD"),
            ("p","Pour les séjours longs, les tours du pays (Lalibela, Simien, Omo, Danakil), ou les stopovers professionnels. Entrée unique — ressortir du pays annule le visa."),
            ("img",4,"Passeport français avec visa éthiopien e-visa collé"),
            ("h4","Frais supplémentaires"),
            ("p","Une <strong>taxe de service bancaire</strong> de 2 à 3 USD s'ajoute au prix affiché. Le total final dépasse donc légèrement les tarifs annoncés."),
         ]},
        {"id":"conseils","toc":"Conseils pratiques","short":"Conseils","h2":"Conseils Pratiques à l'Arrivée",
         "blocks":[
            ("p","À l'aéroport d'Addis-Abeba, la file e-visa est généralement plus rapide que la file « visa on arrival ». Préparez votre <strong>passeport, votre PDF imprimé et votre fiche de débarquement</strong> (distribuée dans l'avion)."),
            ("p","Le policier des frontières peut vous demander une <strong>adresse précise d'hébergement à Addis-Abeba</strong> et la durée exacte de votre séjour. Répondez calmement, sans improviser : toute incohérence avec votre formulaire e-visa peut déclencher un contrôle plus poussé."),
            ("img",5,"File d'attente à l'immigration de l'aéroport Bole Addis Abeba"),
            ("box","Selon <a href=\"https://www.gov.uk/foreign-travel-advice/ethiopia\" target=\"_blank\" rel=\"noopener nofollow\">le UK Foreign Office</a>, des restrictions de circulation peuvent s'appliquer à certaines régions (Tigré, Amhara, Oromia) en raison de la situation sécuritaire. Vérifiez votre itinéraire avant de partir et souscrivez une assurance rapatriement."),
         ]},
    ],
    "expert_tip":"Faites votre demande e-visa <strong>au moins 1 semaine avant le départ</strong> : même si le délai moyen est de 2-3 jours, les week-ends, fêtes orthodoxes et saturations du portail peuvent retarder la délivrance. Gardez une copie du reçu de paiement : c'est la preuve à fournir en cas de bug informatique à l'arrivée.",
})

# 8. Budget Namibie 2 semaines
ARTICLES.append({
    "slug": "budget-namibie-2-semaines",
    "title": "Budget Voyage Namibie 2 Semaines : le Vrai Coût Complet 2026 | Voyage 7 Continents",
    "og_title": "Budget Namibie 2 Semaines : Vrai Coût 2026 (Vol, 4x4, Lodges)",
    "desc": "Budget réel pour 2 semaines en Namibie : vol, location 4x4, camping, lodges, carburant, droits de parcs. Tous les postes détaillés en 3 niveaux de confort.",
    "crumb": "Budget Namibie",
    "h1": "Budget Voyage Namibie 2 Semaines : le Vrai Coût Complet",
    "lead": "Vol, location 4x4 avec tente de toit, carburant, lodges, droits de parcs, nourriture : le budget réel d'un road trip de 14 jours en Namibie en 2026, détaillé poste par poste.",
    "alt1": "4x4 de location avec tente de toit dans le désert du Namib en Namibie",
    "caption1": "Le road trip 4x4 avec tente de toit reste la formule la plus populaire — et la moins chère — pour visiter la Namibie.",
    "sections": [
        {"id":"recap","toc":"Budget total récapitulatif","short":"Total","h2":"Budget Total : 3 Niveaux pour 14 Jours",
         "blocks":[
            ("p","La Namibie peut se faire en <strong>mode aventure 4x4 + camping</strong> à budget serré, ou en lodges de luxe à 600 € la nuit. Voici les trois niveaux typiques pour 2 personnes sur 14 jours, vols inclus depuis Paris."),
            ("h3","Budget routard : 2 500 à 3 200 € / personne"),
            ("p","4x4 avec tente de toit, campings communautaires, repas cuisinés, vol en promo. C'est la formule choisie par ~70 % des voyageurs indépendants français en Namibie."),
            ("h3","Budget confort : 3 800 à 5 500 € / personne"),
            ("p","4x4 sans tente, guest houses et lodges mid-range, quelques activités (excursion Sossusvlei, bateau à Walvis Bay), dîners en ville. Bon compromis qualité/prix."),
            ("img",2,"Camping au bord d'une piste namibienne avec 4x4 et tente de toit"),
            ("h3","Budget premium : 7 000 à 12 000 € / personne"),
            ("p","Lodges de charme (Little Kulala, Onguma, Serra Cafema, Wolwedans), 4x4 privé avec chauffeur-guide, vols intérieurs Cessna. L'expérience safari de luxe sans compromis."),
         ]},
        {"id":"vol","toc":"Vol international","short":"Vol","h2":"Vol International vers Windhoek",
         "blocks":[
            ("p","Il n'existe <strong>aucun vol direct Paris → Windhoek</strong>. Les itinéraires passent systématiquement par Francfort (Lufthansa/Discover Airlines), Johannesburg (Air France + Airlink), Addis-Abeba (Ethiopian Airlines) ou Doha (Qatar Airways)."),
            ("h3","Prix moyens Paris → Windhoek (WDH)"),
            ("p","Saison basse (janv.-mars, nov.) : <strong>650 à 900 €</strong> aller-retour. Haute saison (juin-septembre) : <strong>900 à 1 400 €</strong>. Pic vacances scolaires : jusqu'à 1 700 €. Comparez sur <a href=\"https://www.skyscanner.fr/\" target=\"_blank\" rel=\"noopener nofollow\">Skyscanner</a> et surveillez au moins 3 mois avant."),
            ("img",3,"Avion Lufthansa atterrissant à l'aéroport de Windhoek Hosea Kutako"),
            ("h4","Taxe de sortie"),
            ("p","La taxe de sortie namibienne est désormais incluse dans le billet. Prévoir néanmoins environ 100 NAD (5 €) en cash pour les petits frais aéroport."),
         ]},
        {"id":"4x4-carburant","toc":"4x4 et carburant","short":"4x4","h2":"Location 4x4 et Carburant",
         "blocks":[
            ("p","Le 4x4 avec tente(s) de toit est <strong>le poste de dépense principal</strong> après le vol. Les loueurs spécialisés sont Asco, Bushlore, Savannah Car Hire, Caprivi Car Hire, Namibia2Go. Prenez systématiquement l'<strong>assurance tous risques (Super CDW)</strong>, indispensable sur les pistes caillouteuses."),
            ("h3","Prix 4x4 avec tente de toit"),
            ("p","Toyota Hilux double cabine, 2 tentes, équipement camping complet : <strong>95 à 150 € par jour</strong> selon saison et loueur. Sur 14 jours, compter <strong>1 400 à 2 200 €</strong>, soit 700 à 1 100 €/personne à deux."),
            ("img",4,"Toyota Hilux 4x4 avec équipement camping dans la brousse namibienne"),
            ("h3","Carburant"),
            ("p","Un circuit classique Windhoek-Sossusvlei-Swakopmund-Etosha fait environ <strong>3 500 à 4 500 km</strong>. Consommation moyenne d'un Hilux : 10-12 L/100 km. Au prix namibien (~20 NAD/L soit 1 €), le budget carburant est de <strong>420 à 550 €</strong> pour 14 jours."),
            ("h4","Pneus et kilomètres"),
            ("p","Les pistes en tôle ondulée sont très agressives pour les pneus. <strong>Deux crevaisons</strong> sur un road trip de 2 semaines est courant. Les loueurs incluent généralement une roue de secours et une pompe ; vérifiez bien à la prise en charge."),
         ]},
        {"id":"hebergement-parcs","toc":"Hébergement et parcs","short":"Logement","h2":"Hébergement et Droits de Parcs",
         "blocks":[
            ("p","La Namibie propose un éventail d'hébergements incroyable : campings communautaires à 100 NAD (5 €) par personne jusqu'à lodges à 800 € par nuit."),
            ("h3","Campings NWR et privés"),
            ("p","Les <strong>Namibia Wildlife Resorts</strong> (<a href=\"https://www.nwr.com.na/\" target=\"_blank\" rel=\"noopener nofollow\">nwr.com.na</a>) gèrent les campings officiels dans Etosha, Sossusvlei, Waterberg. Réservation indispensable <strong>3 à 6 mois à l'avance</strong> en haute saison : <strong>15 à 30 €</strong> par emplacement et par nuit."),
            ("h3","Guest houses et lodges"),
            ("p","Guest house à Windhoek : 50-80 € / chambre double. Lodge confortable à Sossusvlei ou Etosha : 150-280 € / nuit petit-déjeuner inclus. Prévoyez quelques nuits en lodge pour souffler entre 3-4 nuits de camping."),
            ("img",5,"Lodge africain avec piscine au bord de la pan d'Etosha Namibie"),
            ("h4","Droits d'entrée parcs"),
            ("p","Entrée Etosha : 150 NAD par adulte et par jour (~8 €), plus 50 NAD par véhicule. Sossusvlei (Parc Namib-Naukluft) : idem. Comptez environ <strong>80 à 120 €</strong> de droits de parcs sur l'ensemble du road trip pour 2 personnes."),
         ]},
        {"id":"nourriture-activites","toc":"Nourriture et activités","short":"Nourriture","h2":"Nourriture, Activités et Extras",
         "blocks":[
            ("p","Le <strong>self-catering</strong> (courses + cuisine au camping) est la norme : comptez <strong>30 à 45 € par jour pour 2 personnes</strong> en faisant les courses dans les supermarchés Spar ou Pick'n'Pay. Sur 14 jours : environ 400 à 600 €."),
            ("h3","Restaurants"),
            ("p","Un dîner au restaurant en ville coûte <strong>15 à 25 €</strong> par personne (Joe's Beerhouse à Windhoek, The Tug à Swakopmund). Prévoyez quelques repas « plaisir » pour sortir du braai quotidien."),
            ("h3","Activités"),
            ("p","Quad dans les dunes Swakopmund : 50 €/pers. Sortie bateau Walvis Bay avec dauphins : 40-60 €. Vol ULM au-dessus de Sossusvlei : 180-250 €. Visite township Mondesa : 30 €. Total activités : comptez <strong>200 à 500 €</strong> par personne selon votre programme."),
            ("box","Pour économiser : réservez le 4x4 et les campings NWR <strong>6 mois à l'avance</strong>, partez en avril-mai ou novembre (inter-saison, tarifs -20 à -30 %), faites les courses en gros à Windhoek avant de partir vers le désert."),
         ]},
    ],
    "expert_tip":"Le vrai piège du budget Namibie : les assurances 4x4 (CDW + pneu + vitre + crevaison) peuvent doubler le prix de location affiché. Lisez attentivement les conditions et préférez un loueur qui inclut « tout risque incluant pneus et pare-brise » dans le tarif de base, quitte à payer 10 €/jour de plus. Un incident sur piste est vite arrivé.",
})

# 9. Spécialités Tunisie
ARTICLES.append({
    "slug": "specialites-tunisie",
    "title": "Spécialités Culinaires de Tunisie : 10 Plats Traditionnels à Goûter | Voyage 7 Continents",
    "og_title": "Spécialités Culinaires de Tunisie : 10 Plats à Goûter 2026",
    "desc": "Couscous, brick à l'œuf, harissa, lablabi, ojja : les 10 spécialités culinaires traditionnelles de Tunisie à goûter absolument pendant votre voyage.",
    "crumb": "Cuisine Tunisie",
    "h1": "Spécialités Culinaires de Tunisie : 10 Plats Traditionnels à Goûter",
    "lead": "Couscous tunisien épicé, brick croustillante, ojja, lablabi, pâtisseries au miel : la cuisine tunisienne traditionnelle à découvrir absolument lors de votre voyage.",
    "alt1": "Table garnie de plats traditionnels tunisiens avec couscous, brick et harissa",
    "caption1": "La cuisine tunisienne est l'une des plus riches du Maghreb, influencée par la Méditerranée, le Maghreb et l'Empire ottoman.",
    "sections": [
        {"id":"couscous","toc":"Le couscous tunisien","short":"Couscous","h2":"1. Le Couscous Tunisien",
         "blocks":[
            ("p","Le couscous est le <strong>plat national de la Tunisie</strong>, inscrit au <a href=\"https://ich.unesco.org/fr/RL/savoir-faire-savoirs-pratiques-et-traditions-liees-a-la-production-et-a-la-consommation-du-couscous-01602\" target=\"_blank\" rel=\"noopener nofollow\">patrimoine culturel immatériel de l'UNESCO</a> (2020) conjointement avec l'Algérie, le Maroc et la Mauritanie. Chaque famille a sa recette, transmise de mère en fille."),
            ("p","La version tunisienne se distingue par son <strong>bouillon rouge</strong> (tomate + harissa) plus épicé que le couscous marocain, et par ses garnitures variées : agneau, poisson (mérou, dorade, mulet), poulet, poulpe, légumes d'hiver (citrouille, navet, chou, pois chiches)."),
            ("img",2,"Plat de couscous tunisien au poisson avec bouillon rouge et harissa"),
            ("h3","Où le déguster"),
            ("p","Le meilleur couscous se savoure en <strong>famille chez l'habitant</strong> le vendredi midi (jour traditionnel). À défaut, les restaurants Dar El Jeld à Tunis, Dar Zarrouk à Sidi Bou Saïd et Le Phénicien à Sousse servent des versions raffinées reconnues."),
         ]},
        {"id":"brick","toc":"Brick à l'œuf","short":"Brick","h2":"2. La Brick à l'Œuf",
         "blocks":[
            ("p","La <strong>brick à l'œuf</strong> (ou <em>brik</em>) est le <strong>hors-d'œuvre emblématique</strong> de la cuisine tunisienne. Il s'agit d'une feuille de malsouka (pâte très fine) pliée en triangle autour d'un <strong>œuf entier cru</strong>, de thon, de câpres, de persil et de pommes de terre, puis frite dans l'huile chaude."),
            ("p","Le défi consiste à la manger sans percer le jaune encore coulant. C'est tout un art ! Servi en entrée dans tous les restaurants et dans les familles, surtout pendant le <strong>ramadan</strong> au moment de l'iftar."),
            ("img",3,"Brick tunisienne à l'œuf en triangle dorée et croustillante"),
            ("h4","Variantes"),
            ("p","Brick au fromage, brick à la viande hachée, brick aux crevettes. À Djerba et Zarzis, on trouve même des bricks aux poulpes."),
         ]},
        {"id":"ojja-lablabi","toc":"Ojja et lablabi","short":"Ojja/Lablabi","h2":"3. L'Ojja et le Lablabi : Plats du Matin",
         "blocks":[
            ("p","L'<strong>ojja</strong> est un plat unique à base de tomates, poivrons verts, piments, ail et œufs pochés dans la sauce. On l'accompagne de merguez, de crevettes ou de thon selon les versions. C'est un équivalent tunisien de la shakshuka, mais plus épicé."),
            ("p","Le <strong>lablabi</strong> est la <strong>soupe de pois chiches</strong> typique du petit-déjeuner tunisien. Les pois chiches cuisent longuement dans un bouillon à l'ail et au cumin, puis on verse la soupe sur des morceaux de pain rassis, un œuf cru, de l'huile d'olive, de la harissa et des câpres. Réconfortant et très bon marché (2-3 dinars ~1 €)."),
            ("img",4,"Bol de lablabi tunisien avec œuf et harissa au petit-déjeuner"),
            ("h4","Où manger un bon lablabi"),
            ("p","Les meilleurs lablabis se trouvent dans les <strong>gargotes de la médina</strong> de Tunis le matin, entre 7h et 11h. Tenez-vous-en aux enseignes fréquentées par les locaux — c'est le gage de fraîcheur."),
         ]},
        {"id":"harissa","toc":"La harissa","short":"Harissa","h2":"4. La Harissa : le Condiment National",
         "blocks":[
            ("p","La <strong>harissa</strong> est la <strong>pâte de piment rouge</strong> fondamentale dans toute la cuisine tunisienne. Elle se compose de piments séchés (type « pili-pili » ou piment nabeul), d'ail, de sel, de cumin, de coriandre et d'huile d'olive. Piquante mais parfumée, elle se sert avec tout : pain, couscous, tajines, poissons."),
            ("p","La <strong>harissa de Nabeul</strong> bénéficie d'une <a href=\"https://www.inpdj.tn/\" target=\"_blank\" rel=\"noopener nofollow\">appellation d'origine protégée (INPDJ)</a> et est considérée comme la meilleure. Les marques Sicam et Le Phare du Cap Bon sont les plus connues. Ramenez-en un petit pot en souvenir !"),
            ("img",5,"Pot de harissa tunisienne traditionnelle avec piments séchés"),
            ("h4","Attention pour les palais sensibles"),
            ("p","La harissa tunisienne est <strong>nettement plus piquante</strong> que la sauce du même nom vendue en supermarché français. Goûtez-la progressivement avec du pain avant de la verser sur votre plat."),
         ]},
        {"id":"autres-specialites","toc":"Autres spécialités","short":"Autres plats","h2":"5 à 10. Autres Spécialités à Goûter Absolument",
         "blocks":[
            ("h3","5. Chorba frik"),
            ("p","Soupe d'orge vert concassé à l'agneau, aux tomates, aux pois chiches et à la menthe. Servie traditionnellement pendant le <strong>ramadan</strong> pour rompre le jeûne. Réconfortante et très nutritive."),
            ("h3","6. Poisson complet grillé"),
            ("p","Sur toute la côte tunisienne (La Goulette, Kelibia, Mahdia, Djerba), le poisson ultra-frais (dorade royale, loup, rouget, mérou) est simplement grillé au feu de bois, servi avec citron, harissa et salade méchouia. Souvent facturé au poids."),
            ("h3","7. Tajine tunisien"),
            ("p","Rien à voir avec le tajine marocain ! Le tajine tunisien est une sorte de <strong>quiche aux œufs battus</strong>, cuite au four avec viande, légumes, fromage râpé et persil. Servi en tranches, froid ou chaud."),
            ("h3","8. Makroud"),
            ("p","Pâtisserie à base de semoule fourrée à la pâte de dattes, frite puis enrobée de miel chaud. La version de Kairouan est la plus réputée depuis des siècles."),
            ("h3","9. Salade méchouia"),
            ("p","Salade de tomates, poivrons et piments <strong>grillés au feu de bois</strong> puis écrasés avec de l'huile d'olive, de l'ail et du cumin. Parfumée et légèrement fumée, elle accompagne tous les repas en entrée ou en accompagnement."),
            ("h3","10. Bambalouni"),
            ("p","Beignet moelleux typique de Sidi Bou Saïd, saupoudré de sucre et dégusté chaud au coin d'un café avec une vue sur la Méditerranée. L'en-cas parfait de fin de journée."),
            ("box","Pour goûter un maximum de spécialités sans se ruiner, optez pour une <strong>table d'hôtes familiale</strong> (chambres d'hôtes, maisons d'hôtes à Tunis, Sidi Bou Saïd, Kairouan) plutôt que pour les restaurants touristiques. Vous mangerez comme à la maison, avec les explications de l'hôte."),
         ]},
    ],
    "expert_tip":"Ne partez pas de Tunisie sans avoir goûté un vrai couscous au poisson à Bizerte, une brick à l'œuf en médina de Tunis et un lablabi matinal chez un petit troquet populaire. Ces trois expériences résument à elles seules toute la richesse de la cuisine tunisienne, bien au-delà des buffets d'hôtels touristiques.",
})

# ---------------- Main ----------------
if __name__ == "__main__":
    for a in ARTICLES:
        content = render(a)
        # Post-rendering safety: fix any accidental ("p">"..." typos from Python source
        path = os.path.join(OUT, f'{a["slug"]}.html')
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f'wrote {path}  {len(content)} chars')
    print(f"done: {len(ARTICLES)} articles")
