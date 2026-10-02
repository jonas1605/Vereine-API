"""
Fügt alle 56 Vereine der Saison 2026/27 per POST zur laufenden API hinzu.

Benutzung:
  1. BASE_URL unten auf deine Render-Adresse setzen (ohne / am Ende),
     z. B. "https://vereine-api-xxxx.onrender.com"
  2. Optional WIPE_FIRST = True setzen, wenn vorher alle vorhandenen
     Vereine gelöscht werden sollen (verhindert Doppelte).
  3. Ausführen:  python add_clubs.py

Hinweis: Auf dem kostenlosen Render-Plan liegen die Daten nur im
Arbeitsspeicher. Nach einem Neustart sind sie wieder weg – dann dieses
Skript erneut laufen lassen (oder die Vereine fest in main.py eintragen).
"""

import requests

BASE_URL = "https://vereine-api.onrender.com"   # <-- hier anpassen!
WIPE_FIRST = False                            # True = vorher alles löschen

CLUBS = [
    # Bundesliga (18)
    ("FC Augsburg", "Bundesliga", "Augsburg", "WWK Arena", 1907),
    ("1. FC Union Berlin", "Bundesliga", "Berlin", "Stadion An der Alten Försterei", 1966),
    ("SV Werder Bremen", "Bundesliga", "Bremen", "Weserstadion", 1899),
    ("Borussia Dortmund", "Bundesliga", "Dortmund", "Signal Iduna Park", 1909),
    ("SV Elversberg", "Bundesliga", "Spiesen-Elversberg", "Ursapharm-Arena an der Kaiserlinde", 1907),
    ("Eintracht Frankfurt", "Bundesliga", "Frankfurt am Main", "Deutsche Bank Park", 1899),
    ("SC Freiburg", "Bundesliga", "Freiburg im Breisgau", "Europa-Park Stadion", 1904),
    ("Hamburger SV", "Bundesliga", "Hamburg", "Volksparkstadion", 1887),
    ("TSG 1899 Hoffenheim", "Bundesliga", "Sinsheim", "PreZero Arena", 1899),
    ("1. FC Köln", "Bundesliga", "Köln", "RheinEnergieStadion", 1948),
    ("RB Leipzig", "Bundesliga", "Leipzig", "Red Bull Arena", 2009),
    ("Bayer 04 Leverkusen", "Bundesliga", "Leverkusen", "BayArena", 1904),
    ("1. FSV Mainz 05", "Bundesliga", "Mainz", "MEWA Arena", 1905),
    ("Borussia Mönchengladbach", "Bundesliga", "Mönchengladbach", "Borussia-Park", 1900),
    ("FC Bayern München", "Bundesliga", "München", "Allianz Arena", 1900),
    ("SC Paderborn 07", "Bundesliga", "Paderborn", "Home Deluxe Arena", 1907),
    ("FC Schalke 04", "Bundesliga", "Gelsenkirchen", "Veltins-Arena", 1904),
    ("VfB Stuttgart", "Bundesliga", "Stuttgart", "MHPArena", 1893),
    # 2. Bundesliga (18)
    ("Hertha BSC", "2. Bundesliga", "Berlin", "Olympiastadion", 1892),
    ("Arminia Bielefeld", "2. Bundesliga", "Bielefeld", "Schüco-Arena", 1905),
    ("VfL Bochum", "2. Bundesliga", "Bochum", "Vonovia Ruhrstadion", 1848),
    ("Eintracht Braunschweig", "2. Bundesliga", "Braunschweig", "Eintracht-Stadion", 1895),
    ("FC Energie Cottbus", "2. Bundesliga", "Cottbus", "LEAG Energie Stadion", 1963),
    ("SV Darmstadt 98", "2. Bundesliga", "Darmstadt", "Merck-Stadion am Böllenfalltor", 1898),
    ("SG Dynamo Dresden", "2. Bundesliga", "Dresden", "Rudolf-Harbig-Stadion", 1953),
    ("SpVgg Greuther Fürth", "2. Bundesliga", "Fürth", "Sportpark Ronhof Thomas Sommer", 1903),
    ("Hannover 96", "2. Bundesliga", "Hannover", "Heinz von Heiden Arena", 1896),
    ("1. FC Heidenheim 1846", "2. Bundesliga", "Heidenheim an der Brenz", "Voith-Arena", 1846),
    ("1. FC Kaiserslautern", "2. Bundesliga", "Kaiserslautern", "Fritz-Walter-Stadion", 1900),
    ("Karlsruher SC", "2. Bundesliga", "Karlsruhe", "BBBank Wildpark", 1894),
    ("Holstein Kiel", "2. Bundesliga", "Kiel", "Holstein-Stadion", 1900),
    ("1. FC Magdeburg", "2. Bundesliga", "Magdeburg", "Avnet Arena", 1965),
    ("1. FC Nürnberg", "2. Bundesliga", "Nürnberg", "Max-Morlock-Stadion", 1900),
    ("VfL Osnabrück", "2. Bundesliga", "Osnabrück", "Stadion an der Bremer Brücke", 1899),
    ("FC St. Pauli", "2. Bundesliga", "Hamburg", "Millerntor-Stadion", 1910),
    ("VfL Wolfsburg", "2. Bundesliga", "Wolfsburg", "Volkswagen Arena", 1945),
    # 3. Liga (20)
    ("Alemannia Aachen", "3. Liga", "Aachen", "Tivoli", 1900),
    ("MSV Duisburg", "3. Liga", "Duisburg", "Schauinsland-Reisen-Arena", 1902),
    ("Fortuna Düsseldorf", "3. Liga", "Düsseldorf", "Merkur Spiel-Arena", 1895),
    ("Rot-Weiss Essen", "3. Liga", "Essen", "Stadion an der Hafenstraße", 1907),
    ("SG Sonnenhof Großaspach", "3. Liga", "Aspach", "WIRmachenDRUCK Arena", 1994),
    ("TSV Havelse", "3. Liga", "Garbsen", "Eilenriedestadion", 1912),
    ("TSG 1899 Hoffenheim II", "3. Liga", "Sinsheim", "Dietmar-Hopp-Stadion", 1899),
    ("FC Ingolstadt 04", "3. Liga", "Ingolstadt", "Audi Sportpark", 2004),
    ("SC Fortuna Köln", "3. Liga", "Köln", "Südstadion", 1948),
    ("FC Viktoria Köln", "3. Liga", "Köln", "Sportpark Höhenberg", 1904),
    ("SV Waldhof Mannheim", "3. Liga", "Mannheim", "Carl-Benz-Stadion", 1907),
    ("SV Meppen", "3. Liga", "Meppen", "Hänsch-Arena", 1912),
    ("SC Preußen Münster", "3. Liga", "Münster", "Preußenstadion", 1906),
    ("SSV Jahn Regensburg", "3. Liga", "Regensburg", "Jahnstadion Regensburg", 1907),
    ("FC Hansa Rostock", "3. Liga", "Rostock", "Ostseestadion", 1965),
    ("1. FC Saarbrücken", "3. Liga", "Saarbrücken", "Ludwigsparkstadion", 1903),
    ("VfB Stuttgart II", "3. Liga", "Stuttgart", "WIRmachenDRUCK Arena", 1893),
    ("SC Verl", "3. Liga", "Verl", "Sportclub Arena", 1924),
    ("SV Wehen Wiesbaden", "3. Liga", "Wiesbaden", "BRITA-Arena", 1926),
    ("Würzburger Kickers", "3. Liga", "Würzburg", "Akon Arena", 1907),
]


def main():
    base = BASE_URL.rstrip("/")

    if WIPE_FIRST:
        existing = requests.get(f"{base}/clubs").json()
        for club in existing:
            requests.delete(f"{base}/clubs/{club['id']}")
        print(f"{len(existing)} vorhandene Vereine gelöscht.")

    ok = 0
    for name, league, city, stadium, founded in CLUBS:
        body = {"name": name, "league": league, "city": city,
                "stadium": stadium, "founded": founded}
        r = requests.post(f"{base}/clubs", json=body)
        if r.status_code == 201:
            ok += 1
        else:
            print(f"Fehler bei {name}: {r.status_code} {r.text}")
    print(f"Fertig: {ok}/{len(CLUBS)} Vereine angelegt.")


if __name__ == "__main__":
    main()