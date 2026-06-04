#!/usr/bin/env python3
"""Download high-quality specific images from Wikimedia Commons for each article.
Queries the Commons API for each keyword, picks the first File:... result, fetches an 800px thumb.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "img", "articles")
os.makedirs(OUT, exist_ok=True)

UA = "voyage7continents/1.0 (https://voyage7continents.fr; contact@voyage7continents.fr) python-urllib/3"

# 5 specific queries per article. Queries are tuned to yield real photos, not maps/coats-of-arms.
SPEC = {
    "vermont": [
        "Vermont autumn foliage landscape",
        "Vermont covered bridge",
        "Maple syrup sugar shack Vermont",
        "Green Mountains Vermont",
        "Vermont village church steeple fall",
    ],
    "maine": [
        "Portland Head Light Maine",
        "Acadia National Park Maine",
        "Maine lobster boat",
        "Bar Harbor Maine coast",
        "Maine lighthouse coast",
    ],
    "preparer-usa": [
        "New York City skyline Manhattan",
        "US passport travel document",
        "Grand Canyon landscape Arizona",
        "American airlines plane airport",
        "Statue of Liberty New York",
    ],
    "valise-usa": [
        "Open suitcase packed clothes",
        "Travel backpack airport",
        "Passport boarding pass",
        "Travel toiletries bag",
        "Airport terminal traveler",
    ],
    "shopping-usa": [
        "Fifth Avenue shopping New York",
        "American shopping mall",
        "Outlet shopping center USA",
        "Times Square shopping",
        "Nike sneakers store",
    ],
    "san-vito": [
        "San Vito Lo Capo beach",
        "Riserva dello Zingaro Sicily",
        "San Vito Lo Capo village Sicily",
        "Sicilian couscous",
        "Scopello Sicily tonnara",
    ],
    "castiglione": [
        "Castiglione della Pescaia",
        "Maremma Tuscany landscape",
        "Parco della Maremma",
        "Tuscan medieval village",
        "Tuscan coast sunset",
    ],
    "alicante": [
        "Castillo de Santa Barbara Alicante",
        "Explanada Alicante",
        "Alicante old town Santa Cruz",
        "Playa del Postiguet Alicante",
        "Spanish tapas paella",
    ],
    "plage-canella": [
        "Corsica beach turquoise",
        "Porto-Vecchio Corsica",
        "Corsica pine trees coast",
        "Corsica granite rocks sea",
        "Corsica sunset coast",
    ],
    "morro-sao-paulo": [
        "Morro de Sao Paulo Bahia",
        "Morro de Sao Paulo beach",
        "Bahia Brazil lighthouse",
        "Moqueca Brazilian food",
        "Brazilian tropical beach palm trees",
    ],
    "monnaie-laos": [
        "Laos kip banknote currency",
        "Vientiane Laos market",
        "Luang Prabang Laos temple",
        "Lao kip money",
        "Laos Mekong river landscape",
    ],
    "vaccins-cambodge-2026": [
        "Angkor Wat Cambodia temple",
        "Phnom Penh Cambodia street",
        "Vaccination syringe vial",
        "Cambodia countryside rice field",
        "Tonle Sap Cambodia village",
    ],
    "decalage-horaire-ouzbekistan": [
        "Samarkand Registan Uzbekistan",
        "Bukhara Uzbekistan minaret",
        "Khiva old city Uzbekistan",
        "Tashkent Uzbekistan architecture",
        "Uzbekistan silk road desert",
    ],
    "hanoi-sapa-pas-cher": [
        "Sapa Vietnam rice terraces",
        "Hanoi old quarter Vietnam",
        "Vietnam sleeper train railway",
        "Sapa H'mong village Vietnam",
        "Fansipan Sapa mountain Vietnam",
    ],
    "temperature-bhoutan-novembre": [
        "Paro Taktsang Bhutan monastery",
        "Thimphu Bhutan dzong",
        "Punakha Dzong Bhutan",
        "Bhutan Himalayas mountain autumn",
        "Bhutan traditional house landscape",
    ],
    "danger-kirghizistan": [
        "Song Kol lake Kyrgyzstan yurt",
        "Bishkek Kyrgyzstan square",
        "Tian Shan mountains Kyrgyzstan",
        "Karakol Kyrgyzstan landscape",
        "Kyrgyz nomad horse",
    ],
    "specialites-sri-lanka": [
        "Sri Lanka rice curry",
        "Sri Lanka street food hoppers",
        "Kottu roti Sri Lanka",
        "Sri Lanka spices market",
        "Sri Lanka tea plantation",
    ],
    "visa-myanmar-arrivee": [
        "Bagan temples Myanmar",
        "Shwedagon Pagoda Yangon Myanmar",
        "Inle Lake Myanmar fisherman",
        "Mandalay Myanmar U Bein bridge",
        "Myanmar passport visa stamp",
    ],
    "meilleure-periode-mongolie": [
        "Mongolia steppe yurt landscape",
        "Gobi desert Mongolia",
        "Naadam festival Mongolia",
        "Ulaanbaatar Mongolia monastery",
        "Mongolia horse nomad",
    ],
    "budget-nepal-3-semaines": [
        "Kathmandu Durbar Square Nepal",
        "Annapurna trekking Nepal",
        "Pokhara Nepal lake Phewa",
        "Everest base camp Nepal",
        "Bhaktapur Nepal temple",
    ],
    "voltage-prise-tanzanie": [
        "BS 1363 type G plug socket",
        "UK plug type G socket wall",
        "Zanzibar Stone Town Tanzania",
        "Electricity pylons Tanzania",
        "Safari lodge Serengeti Tanzania",
    ],
    "vaccins-mozambique": [
        "Maputo Mozambique skyline",
        "Yellow fever vaccine vial",
        "Vaccine syringe medical",
        "Anopheles mosquito malaria",
        "Bazaruto Mozambique beach",
    ],
    "monnaie-madagascar": [
        "Madagascar ariary banknote",
        "Antananarivo market Madagascar",
        "Avenue of the Baobabs Madagascar",
        "Nosy Be Madagascar beach",
        "Madagascar ATM bank",
    ],
    "temperature-senegal-janvier": [
        "Dakar Senegal beach pirogues",
        "Saint-Louis Senegal colonial",
        "Sine Saloum Senegal mangrove",
        "Lompoul desert Senegal dunes",
        "Casamance Senegal village",
    ],
    "eau-robinet-maroc": [
        "Moroccan mint tea glass",
        "Medina fountain Morocco zellige",
        "Bottled water Sidi Ali Morocco",
        "Riad courtyard Marrakech",
        "Atlas mountains village Morocco",
    ],
    "nairobi-masai-mara": [
        "Masai Mara Kenya wildebeest",
        "Great Rift Valley Kenya viewpoint",
        "Safari 4x4 Masai Mara lions",
        "Cessna Caravan bush plane Africa",
        "Masai Mara balloon safari sunrise",
    ],
    "visa-ethiopie": [
        "Lalibela rock churches Ethiopia",
        "Addis Ababa Bole airport Ethiopia",
        "Simien Mountains Ethiopia",
        "Ethiopia flag passport",
        "Danakil depression Ethiopia",
    ],
    "budget-namibie-2-semaines": [
        "Sossusvlei Namibia dunes",
        "Etosha National Park Namibia elephants",
        "Namibia 4x4 road trip",
        "Swakopmund Namibia coast",
        "Damaraland Namibia landscape",
    ],
    "specialites-tunisie": [
        "Tunisian couscous dish",
        "Tunisian brik egg pastry",
        "Harissa Tunisia pepper paste",
        "Sidi Bou Said Tunisia cafe",
        "Medina Tunis market food",
    ],
    "ushuaia-antarctique": [
        "Ushuaia port Argentina ships",
        "Ushuaia Tierra del Fuego harbor",
        "Antarctic expedition ship Antarctica",
        "Drake Passage rough sea",
        "Ushuaia travel agency Antarctica",
    ],
    "temperature-antarctique-decembre": [
        "Gentoo penguin Antarctica summer",
        "Antarctic peninsula thermometer zodiac",
        "Antarctic midnight sun iceberg",
        "Polar expedition clothing parka",
        "Antarctic sunshine icebergs blue",
    ],
    "visa-antarctique": [
        "Antarctic Treaty flag base",
        "South Pole marker flags countries",
        "French passport stamp Ushuaia",
        "Antarctic boot cleaning biosecurity",
        "Antarctic research station flag",
    ],
    "meilleure-periode-antarctique": [
        "Adelie penguins colony ice Antarctica",
        "Antarctic sea ice november",
        "Gentoo penguin chick nest january",
        "Humpback whale antarctic march",
        "Paradise Bay Antarctica",
    ],
    "marcher-glace-antarctique": [
        "Tourists walking snow Antarctica",
        "Zodiac landing Antarctic beach",
        "Antarctic pack ice",
        "Antarctica hikers snow",
        "Antarctica tourist snow landing",
    ],
    "budget-croisiere-antarctique": [
        "Ushuaia port sailing yacht Antarctica",
        "Antarctica cruise ship cabin",
        "Ushuaia street travel agencies",
        "Sailing yacht Antarctica",
        "Zodiac boat Antarctica penguin",
    ],
    "animaux-antarctique": [
        "Gentoo penguin colony Antarctica",
        "Gentoo penguin chick parent",
        "Weddell seal ice Antarctica",
        "Humpback whale breach Antarctica",
        "Wandering albatross flight Southern Ocean",
    ],
    "combien-jours-antarctique": [
        "Antarctica cruise ship iceberg",
        "Antarctic peninsula map expedition",
        "Lemaire Channel Antarctica",
        "Antarctic Circle expedition",
        "King penguin colony South Georgia",
    ],
    "assurance-voyage-antarctique": [
        "Medevac helicopter evacuation",
        "Cruise ship clinic medical",
        "Antarctica rescue ship",
        "Passport documents travel",
        "Laptop travel insurance comparison",
    ],
    "decalage-horaire-fidji": [
        "Fiji beach sunset",
        "Suva Fiji skyline",
        "Fiji island aerial",
        "Airplane clock jet lag",
        "Wristwatch airport traveler",
    ],
    "monnaie-papouasie": [
        "Papua New Guinea kina banknote",
        "Port Moresby Papua New Guinea",
        "Papua New Guinea market",
        "ATM machine travel",
        "Papua New Guinea village",
    ],
    "temperature-nouvelle-zelande-juillet": [
        "New Zealand snow mountain winter",
        "Queenstown winter snow",
        "Wellington New Zealand harbour",
        "Auckland skyline New Zealand",
        "Southern Alps New Zealand",
    ],
    "vaccins-vanuatu": [
        "Vanuatu Port Vila beach",
        "Vanuatu village tropical",
        "Vaccination syringe travel",
        "Tanna volcano Vanuatu",
        "Vanuatu Espiritu Santo beach",
    ],
    "eau-robinet-australie": [
        "Sydney water tap drinking",
        "Melbourne Australia cityscape",
        "Australian outback landscape",
        "Water bottle tap refill",
        "Sydney Harbour Bridge",
    ],
    "sydney-byron-bay-pas-cher": [
        "Byron Bay lighthouse",
        "Greyhound bus Australia",
        "Sydney Central Station train",
        "Byron Bay beach surf",
        "New South Wales coastal road",
    ],
    "budget-samoa-1-semaine": [
        "Samoa Upolu beach",
        "Samoa To Sua Ocean Trench",
        "Apia Samoa harbour",
        "Samoa fale beach hut",
        "Lalomanu beach Samoa",
    ],
    "budget-uruguay-1-semaine": [
        "Montevideo Uruguay rambla skyline",
        "Colonia del Sacramento cobblestone street",
        "Punta del Este hand sculpture beach",
        "Uruguayan asado parrilla",
        "Cabo Polonio lighthouse dunes",
    ],
    "specialites-nouvelle-caledonie": [
        "New Caledonia Noumea market",
        "Bougna kanak food",
        "Coconut crab New Caledonia",
        "New Caledonia Melanesian cuisine",
        "Noumea New Caledonia lagoon",
    ],
    "danger-iles-salomon": [
        "Honiara Solomon Islands",
        "Solomon Islands beach village",
        "Guadalcanal Solomon Islands",
        "Solomon Islands lagoon canoe",
        "Munda Solomon Islands",
    ],
    "voltage-prise-nouvelle-zelande": [
        "Electric plug type I",
        "Power socket wall",
        "Travel adapter plug",
        "New Zealand power outlet",
        "Electrical socket AU NZ",
    ],
    "decalage-vancouver": [
        "Vancouver skyline British Columbia",
        "World time zone clock",
        "Vancouver International Airport YVR",
        "Stanley Park Vancouver sunset",
        "Canada Place Vancouver harbor",
    ],
    "transit-miami": [
        "Miami International Airport terminal",
        "Airport immigration passport control",
        "Miami airport baggage claim",
        "Miami airport skytrain terminal",
        "US Customs Border Protection",
    ],
    "eau-mexique": [
        "Bottled water Mexico",
        "Oxxo store Mexico interior",
        "Drinking glass ice water",
        "Mexican market fresh fruit",
        "Mexican street food tacos",
    ],
    "costa-rica": [
        "Arenal Volcano Costa Rica",
        "Tortuguero rainforest lodge Costa Rica",
        "Costa Rica sloth tree",
        "Manuel Antonio beach Costa Rica",
        "Monteverde cloud forest Costa Rica",
    ],
    "quebec-decembre": [
        "Chateau Frontenac Quebec winter snow",
        "Montreal snow street winter",
        "Quebec winter hiker snowshoe",
        "Snowmobile trail Canada forest",
        "Canada Winter Carnival Quebec",
    ],
    "ohrid": [
        "Saint John Kaneo Ohrid lake",
        "Ohrid old town street",
        "Church Saint John Kaneo Ohrid cliff",
        "Saint Naum monastery Ohrid",
        "Ohrid lake evening boat",
    ],
    "eau-robinet-albanie": [
        "Tirana Skanderbeg square fountain",
        "Mineral water bottles supermarket",
        "Tirana Albania street center",
        "Hiker drinking water bottle outdoor",
        "Saranda Albania coast",
    ],
    "code-postal-reykjavik": [
        "Laugavegur Reykjavik street",
        "Reykjavik colorful houses",
        "Hallgrimskirkja Reykjavik",
        "Iceland mailbox post",
    ],
    "meilleure-periode-georgie": [
        "Tbilisi Old Town panoramic view Georgia Caucasus",
        "Telavi vineyard grapevines Alazani valley",
        "Sighnaghi Georgia Kakheti town",
        "Ushguli Svaneti towers Georgia Caucasus",
    ],
    "aller-mer-de-ross": [
        "Ross Ice Shelf Antarctica",
        "Bluff New Zealand harbour Southland",
        "Cape Evans Scott hut Antarctica",
        "Adelie penguin colony Cape Adare Antarctica",
    ],
    "marseille-dangereux-quartiers": [
        "Marseille Vieux-Port Notre-Dame de la Garde",
        "Le Panier Marseille colorful street",
        "Calanque de Sormiou Marseille turquoise",
    ],
    "ile-arz-ou-ile-aux-moines": [
        "Golfe du Morbihan islands aerial sailboats",
        "Ile aux Moines port Morbihan harbour",
        "Moulin a maree Berno Ile-d'Arz Morbihan",
    ],
    "martinique-ou-guadeloupe": [
        "Anse des Salines Martinique plage cocotiers",
        "Basse-Terre Guadeloupe rainforest Soufriere volcano",
        "Caribbean turquoise lagoon beach Antilles",
    ],
}

# Filenames we explicitly want to skip (maps, coats-of-arms, logos, flags, diagrams)
SKIP_RE = re.compile(
    r"\.(svg|tif|tiff)$"
    r"|flag|coat.of.arms|map of|location map|logo|seal of"
    r"|diagram|chart|graph|blank|silhouette"
    r"|NGA \d|atget|daguerr|, c\. 1[6789]|1[6789]\d0s|engraving|lithograph|postcard"
    r"|painting|oil on canvas|Seurat|Monet|Gauguin|Renoir|, 1[6789]\d\d|, 19[0-4]\d",
    re.IGNORECASE,
)

def api_get(params):
    params = {**params, "format": "json"}
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def search_photo(query):
    """Search commons for a photo, return File:title of the best match."""
    data = api_get({
        "action": "query",
        "list": "search",
        "srsearch": query + " filetype:bitmap",
        "srnamespace": 6,
        "srlimit": 20,
    })
    for hit in data.get("query", {}).get("search", []):
        title = hit["title"]  # e.g. "File:Foo.jpg"
        if SKIP_RE.search(title):
            continue
        return title
    return None

def get_thumb_url(title, width=1024):
    data = api_get({
        "action": "query",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url|mime|size",
        "iiurlwidth": width,
    })
    pages = data.get("query", {}).get("pages", {})
    for _, page in pages.items():
        info = page.get("imageinfo", [])
        if info:
            mime = info[0].get("mime", "")
            if mime not in ("image/jpeg", "image/png"):
                return None
            return info[0].get("thumburl") or info[0].get("url")
    return None

def download(url, dest):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "image/*,*/*;q=0.8",
                "Referer": "https://commons.wikimedia.org/",
            })
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            with open(dest, "wb") as f:
                f.write(data)
            return len(data)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(15 + attempt * 15)
                continue
            raise

def main():
    # Allow selecting only some slugs
    only = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    seen_titles = set()
    for slug, queries in SPEC.items():
        if only and slug not in only:
            continue
        for i, q in enumerate(queries, 1):
            dest = os.path.join(OUT, f"{slug}-{i}.jpg")
            if os.path.exists(dest) and os.path.getsize(dest) > 20000:
                print(f"SKIP {slug}-{i}  (exists)")
                continue
            # Try search, avoiding duplicates within site-wide run
            title = None
            for attempt in range(5):
                t = search_photo(q if attempt == 0 else f"{q} photo")
                if not t:
                    # Loosen
                    t = search_photo(q.split()[0] + " photograph")
                if t and t not in seen_titles:
                    title = t
                    seen_titles.add(t)
                    break
                # If duplicate, try a slight variation
                q = q + " landscape"
            if not title:
                print(f"MISS {slug}-{i} :: {queries[i-1]}")
                continue
            url = get_thumb_url(title, 1024)
            if not url:
                print(f"NOURL {slug}-{i} :: {title}")
                continue
            try:
                size = download(url, dest)
                print(f"OK {slug}-{i}  {size:>7}  {title}")
            except Exception as e:
                print(f"ERR {slug}-{i} :: {e}")
            time.sleep(3)
    print("done")

if __name__ == "__main__":
    main()
