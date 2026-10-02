# Vereine-API (Bundesliga / 2. Bundesliga / 3. Liga)

Eine REST-API mit **FastAPI**, die Fußballvereine verwaltet – mit allen vier
CRUD-Operationen nach gängigen REST-Konventionen. Dazu gibt es als Bonus eine
**Handy-Web-App**, die die Daten anzeigt, anlegt, ändert und löscht.

## Endpunkte

| Methode | Pfad            | Zweck                          | Erfolg |
|---------|-----------------|--------------------------------|--------|
| GET     | `/clubs`        | Alle Vereine (Filter `?league=`) | 200 |
| GET     | `/clubs/{id}`   | Einen Verein                   | 200 / 404 |
| POST    | `/clubs`        | Verein anlegen                 | 201 (+ `Location`-Header) |
| PUT     | `/clubs/{id}`   | Verein komplett ändern         | 200 / 404 |
| DELETE  | `/clubs/{id}`   | Verein löschen                 | 204 / 404 |

Ungültige Daten (z. B. eine unbekannte Liga) werden automatisch mit **422**
abgewiesen. Erlaubte Ligen: `Bundesliga`, `2. Bundesliga`, `3. Liga`.

- Interaktive Doku (Swagger): `/docs`
- Handy-Web-App: `/` (die Startseite)

## Lokal starten

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Dann im Browser öffnen:
- Web-App:  http://127.0.0.1:8000/
- Swagger:  http://127.0.0.1:8000/docs

## Online stellen (GitHub + Render, kostenlos)

### 1. Auf GitHub laden
```bash
git init
git add .
git commit -m "Vereine-API"
```
Lege auf github.com ein neues (leeres) Repository an und verbinde es:
```bash
git remote add origin https://github.com/DEIN-NAME/bundesliga-api.git
git branch -M main
git push -u origin main
```

### 2. Auf Render deployen
1. Auf [render.com](https://render.com) mit GitHub anmelden.
2. **New → Web Service** und dein Repository auswählen.
3. Dank der Datei `render.yaml` werden Build- und Startbefehl automatisch erkannt.
   Falls du es doch manuell einträgst:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Create Web Service** – nach ein paar Minuten ist die API online, z. B. unter
   `https://bundesliga-api.onrender.com/` (Web-App) bzw. `/docs` (Swagger).

> Hinweis: Auf dem kostenlosen Render-Plan „schläft" der Dienst nach Inaktivität
> ein und braucht beim ersten Aufruf ein paar Sekunden. Außerdem liegen die Daten
> nur im Arbeitsspeicher – nach einem Neustart stehen wieder die Startdaten da.
> Für die Übung ist das in Ordnung; für dauerhafte Speicherung würde man eine
> Datenbank (z. B. SQLite oder PostgreSQL) anbinden.

## Schnelltest (curl)

```bash
# Anlegen
curl -X POST https://DEINE-URL/clubs -H "Content-Type: application/json" \
  -d '{"name":"SC Freiburg","league":"Bundesliga","city":"Freiburg","founded":1904}'

# Ändern (id anpassen)
curl -X PUT https://DEINE-URL/clubs/1 -H "Content-Type: application/json" \
  -d '{"name":"FC Bayern München","league":"Bundesliga","city":"München"}'

# Löschen
curl -X DELETE https://DEINE-URL/clubs/1
```

## Projektstruktur

```
bundesliga-api/
├── main.py            # die FastAPI-API (CRUD) + liefert die Web-App aus
├── requirements.txt   # Abhängigkeiten
├── render.yaml        # Deploy-Konfiguration für Render
├── .gitignore
└── static/
    └── index.html     # Handy-Web-App (Bonus)
```
