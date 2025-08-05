# TRMNL Dashboard

Eine elegante Flask-Webanwendung zur Anzeige und Überwachung Ihres TRMNL-Terminal-Inhalts über die TRMNL Private API. Bietet eine moderne Dark/Light-Theme-Oberfläche mit Materialize CSS.

![Dashboard Vorschau](https://img.shields.io/badge/Status-Aktiv-brightgreen) ![Python](https://img.shields.io/badge/Python-3.13+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0+-red) ![Docker](https://img.shields.io/badge/Docker-Bereit-blue)

## ✨ Funktionen

- 🎨 **Moderne Benutzeroberfläche**: Sauberes, responsives Interface mit Dark/Light-Theme-Umschaltung
- 🔄 **Echtzeit-Updates**: Automatische Aktualisierung alle 30 Sekunden
- 📱 **Mobilfreundlich**: Responsive Design für alle Bildschirmgrößen
- 🖼️ **Direkter Bildzugriff**: Dedizierter `/image`-Endpunkt für aktuellen Display-Inhalt
- 🛠️ **Entwicklermodus**: Automatisches Neuladen bei Code-Änderungen während der Entwicklung
- 🐳 **Docker-bereit**: Containerisierte Deployment-Unterstützung
- 🔍 **Debug-Modus**: Raw API-Response-Viewer zur Fehlerbehebung
- ⚡ **Schnelle Einrichtung**: Schnelle Installation mit UV Package Manager

## 🚀 Schnellstart

### Voraussetzungen

- Python 3.13+
- UV Package Manager ([Installationsanleitung](https://docs.astral.sh/uv/getting-started/installation/))
- TRMNL-Gerät mit API-Zugriff

### Installation

1. **Klonen und einrichten**:
   ```bash
   git clone <repository-url>
   cd trmnl-dashboard
   uv sync
   ```

2. **TRMNL-Gerät konfigurieren**:
   ```bash
   # .env Datei bearbeiten
   nano .env
   ```
   
   Aktualisieren Sie die `TRMNL_DEVICE_ID` mit der MAC-Adresse Ihres Geräts:
   ```env
   TRMNL_DEVICE_ID=A1:B2:C3:D4:E5:F6  # Ersetzen Sie mit Ihrer Geräte-MAC
   ```

3. **Anwendung starten**:
   ```bash
   uv run python app.py
   ```

4. **Im Browser öffnen**:
   ```
   http://localhost:5001
   ```

## 📋 Konfiguration

### Umgebungsvariablen

Bearbeiten Sie die `.env`-Datei zur Konfiguration:

```env
# TRMNL API Konfiguration
TRMNL_API_KEY=your-api-key-here
TRMNL_DEVICE_ID=XX:XX:XX:XX:XX:XX    # Ihre Geräte-MAC-Adresse
TRMNL_BASE_URL=https://trmnl.app/api

# Flask Konfiguration
FLASK_ENV=development
FLASK_DEBUG=True      # Aktiviert automatisches Neuladen bei Code-Änderungen
FLASK_PORT=5001       # Ändern falls Port 5001 belegt ist
```

### Device ID finden

Ihre TRMNL Device ID ist die MAC-Adresse Ihres Geräts. Sie finden sie:

1. **TRMNL Web-Dashboard**: Bereich Geräteeinstellungen
2. **Geräte-Aufkleber**: Physischer Aufkleber am Gerät
3. **TRMNL Mobile App**: Geräteinformations-Bildschirm

Format: `XX:XX:XX:XX:XX:XX` (z.B. `A1:B2:C3:D4:E5:F6`)

## 🌐 API-Endpunkte

| Endpunkt | Beschreibung | Antwort |
|----------|--------------|---------|
| `/` | Haupt-Dashboard-Interface | HTML-Seite |
| `/api/status` | Aktueller TRMNL-Status und -Inhalt | JSON-Daten |
| `/api/refresh` | TRMNL-Inhalt neu laden erzwingen | JSON-Daten |
| `/image` | Direkte Weiterleitung zum aktuellen Bild | Bild-Weiterleitung |

### Beispiel API-Antwort

```json
{
  "success": true,
  "data": {
    "image_url": "https://trmnl.app/display/image.png",
    "filename": "dashboard.png",
    "update_firmware": false
  },
  "timestamp": "2025-08-05T19:20:00"
}
```

## 🐳 Docker-Deployment

### Schnelle Docker-Einrichtung

1. **Bauen und ausführen**:
   ```bash
   docker-compose up -d
   ```

2. **Logs anzeigen**:
   ```bash
   docker-compose logs -f
   ```

3. **Container stoppen**:
   ```bash
   docker-compose down
   ```

### Manueller Docker-Build

```bash
# Image bauen
docker build -t trmnl-dashboard .

# Container ausführen
docker run -d -p 5001:5000 --env-file .env trmnl-dashboard
```

## 🎨 Benutzeroberflächen-Anleitung

### Dashboard-Funktionen

- **Theme-Umschaltung**: Zwischen dunklem und hellem Modus wechseln (speichert Präferenz)
- **Aktualisieren-Button**: TRMNL-Inhalt manuell aktualisieren
- **Auto-Refresh**: Inhalt wird automatisch alle 30 Sekunden aktualisiert
- **Status-Indikatoren**: Visuelles Feedback für API-Konnektivität
- **Bildanzeige**: Vollauflösung des aktuellen Terminal-Inhalts
- **Debug-Panel**: Raw API-Antwort zur Fehlerbehebung

### Tastaturkürzel

- `Strg/Cmd + R`: Manuelle Aktualisierung
- Theme-Präferenz wird automatisch im Browser-Speicher gespeichert

## 🔧 Entwicklung

### Projektstruktur

```
trmnl-dashboard/
├── app/
│   ├── app.py              # Haupt-Flask-Anwendung
│   ├── templates/
│   │   └── index.html      # Dashboard-Template
│   └── static/
│       └── style.css       # Custom CSS mit Themes
├── .env                    # Umgebungskonfiguration
├── pyproject.toml         # Python-Dependencies
├── Dockerfile             # Container-Definition
├── docker-compose.yml     # Container-Orchestrierung
└── README_DE.md           # Diese Dokumentation
```

### Funktionen hinzufügen

1. **Debug-Modus aktivieren** in `.env`:
   ```env
   FLASK_DEBUG=True
   ```

2. **Änderungen am Code** vornehmen
3. **Auto-Reload** startet den Server automatisch neu

### Tests ausführen

```bash
uv run pytest
```

### Code-Formatierung

```bash
uv run black app/
uv run flake8 app/
```

## 🚨 Fehlerbehebung

### Häufige Probleme

| Problem | Lösung |
|---------|--------|
| Verbindung verweigert | Prüfen ob anderer Service Port 5001 nutzt, `FLASK_PORT` ändern |
| API-Fehler 401 | `TRMNL_API_KEY` und `TRMNL_DEVICE_ID` überprüfen |
| Gerät nicht konfiguriert | `TRMNL_DEVICE_ID` mit korrekter MAC-Adresse aktualisieren |
| Bild lädt nicht | TRMNL-Gerätekonnektivität und API-Antwort prüfen |

### Debug-Schritte

1. **Konfiguration prüfen**:
   ```bash
   cat .env
   ```

2. **API manuell testen**:
   ```bash
   curl http://localhost:5001/api/status
   ```

3. **Anwendungslogs anzeigen**:
   - Nach Fehlermeldungen in der Terminal-Ausgabe suchen
   - Browser-Konsole auf JavaScript-Fehler prüfen

4. **TRMNL-API überprüfen**:
   - Sicherstellen, dass Ihr Gerät online ist
   - TRMNL-Dashboard für Gerätestatus prüfen

## 📝 Mitwirken

1. Repository forken
2. Feature-Branch erstellen: `git checkout -b feature-name`
3. Änderungen vornehmen
4. Gründlich testen
5. Pull Request einreichen

## 📄 Lizenz

MIT-Lizenz - siehe LICENSE-Datei für Details.

## 🙋‍♂️ Support

Für Probleme und Fragen:

1. Fehlerbehebungsanleitung oben prüfen
2. TRMNL-API-Dokumentation durchsehen
3. Issue im Repository erstellen
4. TRMNL-Support für gerätespezifische Probleme kontaktieren

---

**Hinweis**: Diese Anwendung erfordert ein TRMNL-Gerät mit API-Zugriff. Stellen Sie sicher, dass Sie die entsprechenden Berechtigungen zur Nutzung der TRMNL Private API haben.