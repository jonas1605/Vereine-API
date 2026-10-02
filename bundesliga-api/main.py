"""
Vereine-API (Bundesliga / 2. Bundesliga / 3. Liga)
==================================================

Eine kleine REST-API mit FastAPI, die Fußballvereine verwaltet.
Unterstützt die vier gängigen CRUD-Operationen nach REST-Konventionen:

    GET    /clubs            -> alle Vereine auflisten (optional ?league= Filter)
    GET    /clubs/{id}       -> einen Verein abrufen
    POST   /clubs            -> neuen Verein anlegen        (201 Created)
    PUT    /clubs/{id}       -> einen Verein komplett ändern (200 OK)
    DELETE /clubs/{id}       -> einen Verein löschen        (204 No Content)

Zusätzlich wird unter "/" eine kleine Handy-Web-App ausgeliefert und
unter "/docs" die automatische Swagger-Oberfläche von FastAPI.
"""

from enum import Enum
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Vereine-API",
    description="REST-API für Vereine der Bundesliga, 2. Bundesliga und 3. Liga.",
    version="1.0.0",
)

# CORS erlauben, damit auch externe Web-Apps die API nutzen können.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Datenmodelle
# ---------------------------------------------------------------------------
class League(str, Enum):
    """Erlaubte Ligen. So kann nur ein gültiger Wert gespeichert werden."""

    bundesliga = "Bundesliga"
    bundesliga2 = "2. Bundesliga"
    liga3 = "3. Liga"


class ClubIn(BaseModel):
    """Felder, die beim Anlegen/Ändern mitgeschickt werden (ohne id)."""

    name: str = Field(..., min_length=1, examples=["FC Bayern München"])
    league: League = Field(..., examples=["Bundesliga"])
    city: str | None = Field(None, examples=["München"])
    stadium: str | None = Field(None, examples=["Allianz Arena"])
    founded: int | None = Field(None, ge=1800, le=2100, examples=[1900])


class Club(ClubIn):
    """Verein inklusive seiner id (so wird er nach außen zurückgegeben)."""

    id: int


# ---------------------------------------------------------------------------
# "Datenbank": einfacher Speicher im Arbeitsspeicher
# ---------------------------------------------------------------------------
# Hinweis: Diese Daten liegen nur im RAM. Bei einem Neustart des Servers
# (auf Render-Free passiert das z. B. nach Inaktivität) werden sie wieder
# auf diese Startliste zurückgesetzt. Für die Übung reicht das völlig.
_clubs: dict[int, Club] = {}
_next_id = 1


def _add_seed(name: str, league: League, city: str, stadium: str, founded: int) -> None:
    global _next_id
    _clubs[_next_id] = Club(
        id=_next_id, name=name, league=league, city=city, stadium=stadium, founded=founded
    )
    _next_id += 1


# Startdaten: alle Vereine der Saison 2026/27 (Quelle: Wikipedia).
# Bundesliga (18)
_add_seed("FC Augsburg", League.bundesliga, "Augsburg", "WWK Arena", 1907)
_add_seed("1. FC Union Berlin", League.bundesliga, "Berlin", "Stadion An der Alten Försterei", 1966)
_add_seed("SV Werder Bremen", League.bundesliga, "Bremen", "Weserstadion", 1899)
_add_seed("Borussia Dortmund", League.bundesliga, "Dortmund", "Signal Iduna Park", 1909)
_add_seed("SV Elversberg", League.bundesliga, "Spiesen-Elversberg", "Ursapharm-Arena an der Kaiserlinde", 1907)
_add_seed("Eintracht Frankfurt", League.bundesliga, "Frankfurt am Main", "Deutsche Bank Park", 1899)
_add_seed("SC Freiburg", League.bundesliga, "Freiburg im Breisgau", "Europa-Park Stadion", 1904)
_add_seed("Hamburger SV", League.bundesliga, "Hamburg", "Volksparkstadion", 1887)
_add_seed("TSG 1899 Hoffenheim", League.bundesliga, "Sinsheim", "PreZero Arena", 1899)
_add_seed("1. FC Köln", League.bundesliga, "Köln", "RheinEnergieStadion", 1948)
_add_seed("RB Leipzig", League.bundesliga, "Leipzig", "Red Bull Arena", 2009)
_add_seed("Bayer 04 Leverkusen", League.bundesliga, "Leverkusen", "BayArena", 1904)
_add_seed("1. FSV Mainz 05", League.bundesliga, "Mainz", "MEWA Arena", 1905)
_add_seed("Borussia Mönchengladbach", League.bundesliga, "Mönchengladbach", "Borussia-Park", 1900)
_add_seed("FC Bayern München", League.bundesliga, "München", "Allianz Arena", 1900)
_add_seed("SC Paderborn 07", League.bundesliga, "Paderborn", "Home Deluxe Arena", 1907)
_add_seed("FC Schalke 04", League.bundesliga, "Gelsenkirchen", "Veltins-Arena", 1904)
_add_seed("VfB Stuttgart", League.bundesliga, "Stuttgart", "MHPArena", 1893)

# 2. Bundesliga (18)
_add_seed("Hertha BSC", League.bundesliga2, "Berlin", "Olympiastadion", 1892)
_add_seed("Arminia Bielefeld", League.bundesliga2, "Bielefeld", "Schüco-Arena", 1905)
_add_seed("VfL Bochum", League.bundesliga2, "Bochum", "Vonovia Ruhrstadion", 1848)
_add_seed("Eintracht Braunschweig", League.bundesliga2, "Braunschweig", "Eintracht-Stadion", 1895)
_add_seed("FC Energie Cottbus", League.bundesliga2, "Cottbus", "LEAG Energie Stadion", 1963)
_add_seed("SV Darmstadt 98", League.bundesliga2, "Darmstadt", "Merck-Stadion am Böllenfalltor", 1898)
_add_seed("SG Dynamo Dresden", League.bundesliga2, "Dresden", "Rudolf-Harbig-Stadion", 1953)
_add_seed("SpVgg Greuther Fürth", League.bundesliga2, "Fürth", "Sportpark Ronhof Thomas Sommer", 1903)
_add_seed("Hannover 96", League.bundesliga2, "Hannover", "Heinz von Heiden Arena", 1896)
_add_seed("1. FC Heidenheim 1846", League.bundesliga2, "Heidenheim an der Brenz", "Voith-Arena", 1846)
_add_seed("1. FC Kaiserslautern", League.bundesliga2, "Kaiserslautern", "Fritz-Walter-Stadion", 1900)
_add_seed("Karlsruher SC", League.bundesliga2, "Karlsruhe", "BBBank Wildpark", 1894)
_add_seed("Holstein Kiel", League.bundesliga2, "Kiel", "Holstein-Stadion", 1900)
_add_seed("1. FC Magdeburg", League.bundesliga2, "Magdeburg", "Avnet Arena", 1965)
_add_seed("1. FC Nürnberg", League.bundesliga2, "Nürnberg", "Max-Morlock-Stadion", 1900)
_add_seed("VfL Osnabrück", League.bundesliga2, "Osnabrück", "Stadion an der Bremer Brücke", 1899)
_add_seed("FC St. Pauli", League.bundesliga2, "Hamburg", "Millerntor-Stadion", 1910)
_add_seed("VfL Wolfsburg", League.bundesliga2, "Wolfsburg", "Volkswagen Arena", 1945)

# 3. Liga (20)
_add_seed("Alemannia Aachen", League.liga3, "Aachen", "Tivoli", 1900)
_add_seed("MSV Duisburg", League.liga3, "Duisburg", "Schauinsland-Reisen-Arena", 1902)
_add_seed("Fortuna Düsseldorf", League.liga3, "Düsseldorf", "Merkur Spiel-Arena", 1895)
_add_seed("Rot-Weiss Essen", League.liga3, "Essen", "Stadion an der Hafenstraße", 1907)
_add_seed("SG Sonnenhof Großaspach", League.liga3, "Aspach", "WIRmachenDRUCK Arena", 1994)
_add_seed("TSV Havelse", League.liga3, "Garbsen", "Eilenriedestadion", 1912)
_add_seed("TSG 1899 Hoffenheim II", League.liga3, "Sinsheim", "Dietmar-Hopp-Stadion", 1899)
_add_seed("FC Ingolstadt 04", League.liga3, "Ingolstadt", "Audi Sportpark", 2004)
_add_seed("SC Fortuna Köln", League.liga3, "Köln", "Südstadion", 1948)
_add_seed("FC Viktoria Köln", League.liga3, "Köln", "Sportpark Höhenberg", 1904)
_add_seed("SV Waldhof Mannheim", League.liga3, "Mannheim", "Carl-Benz-Stadion", 1907)
_add_seed("SV Meppen", League.liga3, "Meppen", "Hänsch-Arena", 1912)
_add_seed("SC Preußen Münster", League.liga3, "Münster", "Preußenstadion", 1906)
_add_seed("SSV Jahn Regensburg", League.liga3, "Regensburg", "Jahnstadion Regensburg", 1907)
_add_seed("FC Hansa Rostock", League.liga3, "Rostock", "Ostseestadion", 1965)
_add_seed("1. FC Saarbrücken", League.liga3, "Saarbrücken", "Ludwigsparkstadion", 1903)
_add_seed("VfB Stuttgart II", League.liga3, "Stuttgart", "WIRmachenDRUCK Arena", 1893)
_add_seed("SC Verl", League.liga3, "Verl", "Sportclub Arena", 1924)
_add_seed("SV Wehen Wiesbaden", League.liga3, "Wiesbaden", "BRITA-Arena", 1926)
_add_seed("Würzburger Kickers", League.liga3, "Würzburg", "Akon Arena", 1907)


# ---------------------------------------------------------------------------
# API-Endpunkte
# ---------------------------------------------------------------------------
@app.get("/clubs", response_model=list[Club], tags=["clubs"], summary="Alle Vereine")
def list_clubs(league: League | None = None):
    """Gibt alle Vereine zurück. Mit `?league=Bundesliga` kann gefiltert werden."""
    clubs = list(_clubs.values())
    if league is not None:
        clubs = [c for c in clubs if c.league == league]
    return clubs


@app.get("/clubs/{club_id}", response_model=Club, tags=["clubs"], summary="Einen Verein")
def get_club(club_id: int):
    """Gibt genau einen Verein anhand seiner id zurück (404, falls nicht vorhanden)."""
    club = _clubs.get(club_id)
    if club is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verein nicht gefunden")
    return club


@app.post(
    "/clubs",
    response_model=Club,
    status_code=status.HTTP_201_CREATED,
    tags=["clubs"],
    summary="Verein anlegen",
)
def create_club(data: ClubIn, response: Response):
    """Legt einen neuen Verein an und liefert ihn mit neuer id zurück (201 Created)."""
    global _next_id
    club = Club(id=_next_id, **data.model_dump())
    _clubs[_next_id] = club
    # REST-Konvention: Location-Header zeigt auf die neue Ressource.
    response.headers["Location"] = f"/clubs/{_next_id}"
    _next_id += 1
    return club


@app.put("/clubs/{club_id}", response_model=Club, tags=["clubs"], summary="Verein ändern")
def update_club(club_id: int, data: ClubIn):
    """Ersetzt die Daten eines bestehenden Vereins komplett (404, falls nicht vorhanden)."""
    if club_id not in _clubs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verein nicht gefunden")
    club = Club(id=club_id, **data.model_dump())
    _clubs[club_id] = club
    return club


@app.delete(
    "/clubs/{club_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["clubs"],
    summary="Verein löschen",
)
def delete_club(club_id: int):
    """Löscht einen Verein (204 No Content). 404, falls die id nicht existiert."""
    if club_id not in _clubs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verein nicht gefunden")
    del _clubs[club_id]
    # Bei 204 wird bewusst kein Body zurückgegeben.
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# Handy-Web-App (Bonus) unter "/" ausliefern
# ---------------------------------------------------------------------------
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(BASE_DIR / "static" / "index.html")