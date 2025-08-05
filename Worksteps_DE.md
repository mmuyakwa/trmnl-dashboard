# TRMNL Dashboard – Flask Webanwendung

## Projektbeschreibung

Dieses Projekt erstellt eine Flask-Webanwendung, die den aktuellen Inhalt eines TRMNL-Terminals über die TRMNL Private API anzeigt. Die Anwendung verwendet Materialize CSS mit Dark Mode und kann sowohl lokal als auch in einem Docker-Container ausgeführt werden.

---

## Projektstruktur

```text
trmnl-dashboard/
├── app/
│   ├── app.py                 # Hauptanwendung
│   ├── templates/
│   │   └── index.html         # Frontend Template
│   ├── static/
│   │   └── style.css          # Custom CSS Styles
│   └── requirements.txt       # Python Dependencies
├── .env                       # Umgebungsvariablen
├── docker-compose.yml         # Docker Compose Konfiguration
├── Dockerfile                 # Docker Container Definition
├── pyproject.toml             # UV Projekt Konfiguration
└── README.md                  # Projektdokumentation
```

---

## API-Integration

- **Endpoint:** `GET /api/display`
- **Header:**
  - `ID` (Device MAC Address)
  - `Access-Token` (API Key)
- **Base-URL:** `https://trmnl.app/api`

---

## Dateien

### 1. `pyproject.toml`

```toml
[project]
name = "trmnl-dashboard"
version = "0.1.0"
description = "Flask web application to display TRMNL terminal content"
dependencies = [
    "flask>=3.0.0",
    "python-dotenv>=1.0.0",
    "requests>=2.31.0"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0"
]
```

### 2. `.env`

```env
# TRMNL API Konfiguration
TRMNL_API_KEY=your-api-key-here
TRMNL_DEVICE_ID=XX:XX:XX:XX:XX:XX
TRMNL_BASE_URL=https://trmnl.app/api

# Flask Konfiguration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
```

### 3. `app/requirements.txt`

```txt
Flask==3.0.0
python-dotenv==1.0.0
requests==2.31.0
```

### 4. `app/app.py`

```python
from flask import Flask, render_template, jsonify
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
TRMNL_API_KEY = os.getenv('TRMNL_API_KEY')
TRMNL_DEVICE_ID = os.getenv('TRMNL_DEVICE_ID', 'XX:XX:XX:XX:XX:XX')
TRMNL_BASE_URL = os.getenv('TRMNL_BASE_URL', 'https://trmnl.app/api')

class TRMNLClient:
    """Client for TRMNL API interactions"""
    
    def __init__(self, api_key, device_id, base_url):
        self.api_key = api_key
        self.device_id = device_id
        self.base_url = base_url
        
    def get_display_content(self):
        """Fetch current display content from TRMNL API"""
        try:
            headers = {
                'ID': self.device_id,
                'Access-Token': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/display",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': f'API Error: {response.status_code}',
                    'message': response.text,
                    'timestamp': datetime.now().isoformat()
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': 'Connection Error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Initialize TRMNL client
trmnl_client = TRMNLClient(TRMNL_API_KEY, TRMNL_DEVICE_ID, TRMNL_BASE_URL)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                         device_id=TRMNL_DEVICE_ID,
                         api_configured=bool(TRMNL_API_KEY))

@app.route('/api/status')
def api_status():
    """API endpoint to get current TRMNL status"""
    if not TRMNL_API_KEY:
        return jsonify({
            'success': False,
            'error': 'Configuration Error',
            'message': 'TRMNL API key not configured'
        }), 500
    
    result = trmnl_client.get_display_content()
    return jsonify(result)

@app.route('/api/refresh')
def api_refresh():
    """API endpoint to force refresh TRMNL content"""
    return api_status()  # Same as status for now

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', error="Internal server error"), 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
```

### 5. `app/templates/index.html`

```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TRMNL Dashboard</title>
    
    <!-- Materialize CSS -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">
    <!-- Material Icons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet">
</head>
<body class="dark-theme">
    <nav class="nav-wrapper">
        <div class="container">
            <a href="#" class="brand-logo">
                <i class="material-icons">dashboard</i>
                TRMNL Dashboard
            </a>
            <ul id="nav-mobile" class="right">
                <li>
                    <a href="#" onclick="toggleTheme()" class="theme-toggle">
                        <i class="material-icons" id="theme-icon">light_mode</i>
                    </a>
                </li>
                <li>
                    <a href="#" onclick="refreshData()" class="refresh-btn">
                        <i class="material-icons">refresh</i>
                    </a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <div class="row">
            <div class="col s12">
                <h4 class="center-align">
                    <i class="material-icons medium">terminal</i>
                    Terminal Status
                </h4>
            </div>
        </div>

        <!-- Status Card -->
        <div class="row">
            <div class="col s12 m6">
                <div class="card">
                    <div class="card-content">
                        <span class="card-title">
                            <i class="material-icons">info</i>
                            Geräteinformationen
                        </span>
                        <p><strong>Device ID:</strong> {{ device_id }}</p>
                        <p><strong>API Status:</strong> 
                            <span id="api-status" class="status-indicator">
                                {% if api_configured %}
                                <i class="material-icons green-text">check_circle</i> Konfiguriert
                                {% else %}
                                <i class="material-icons red-text">error</i> Nicht konfiguriert
                                {% endif %}
                            </span>
                        </p>
                        <p><strong>Letzte Aktualisierung:</strong> <span id="last-update">Noch nicht geladen</span></p>
                    </div>
                </div>
            </div>

            <div class="col s12 m6">
                <div class="card">
                    <div class="card-content">
                        <span class="card-title">
                            <i class="material-icons">settings</i>
                            Steuerung
                        </span>
                        <div class="card-action">
                            <button class="btn waves-effect waves-light" onclick="refreshData()">
                                <i class="material-icons left">refresh</i>
                                Daten aktualisieren
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Content Display -->
        <div class="row">
            <div class="col s12">
                <div class="card">
                    <div class="card-content">
                        <span class="card-title">
                            <i class="material-icons">image</i>
                            Aktueller Inhalt
                        </span>
                        <div id="content-area">
                            <div class="center-align">
                                <div class="preloader-wrapper big active" id="loading-spinner" style="display: none;">
                                    <div class="spinner-layer spinner-blue-only">
                                        <div class="circle-clipper left">
                                            <div class="circle"></div>
                                        </div>
                                        <div class="gap-patch">
                                            <div class="circle"></div>
                                        </div>
                                        <div class="circle-clipper right">
                                            <div class="circle"></div>
                                        </div>
                                    </div>
                                </div>
                                <p id="status-message">Klicken Sie auf "Daten aktualisieren" um zu beginnen</p>
                            </div>
                        </div>

                        <!-- Image Display Area -->
                        <div id="image-display" style="display: none;">
                            <div class="center-align">
                                <img id="trmnl-image" src="" alt="TRMNL Display" class="responsive-img" style="max-width: 100%; border: 1px solid #ccc;">
                            </div>
                            <div class="content-info">
                                <p><strong>Dateiname:</strong> <span id="filename">-</span></p>
                                <p><strong>Firmware Update:</strong> <span id="firmware-update">-</span></p>
                            </div>
                        </div>

                        <!-- Error Display -->
                        <div id="error-display" style="display: none;">
                            <div class="card-panel red lighten-4">
                                <span class="red-text">
                                    <i class="material-icons left">error</i>
                                    <span id="error-message">Ein Fehler ist aufgetreten</span>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- JSON Data Display (for debugging) -->
        <div class="row">
            <div class="col s12">
                <div class="card">
                    <div class="card-content">
                        <span class="card-title">
                            <i class="material-icons">code</i>
                            Raw API Response
                        </span>
                        <pre id="json-display" class="json-container">Noch keine Daten geladen</pre>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Materialize JavaScript -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    
    <script>
        // Theme management
        function toggleTheme() {
            const body = document.body;
            const themeIcon = document.getElementById('theme-icon');
            
            if (body.classList.contains('dark-theme')) {
                body.classList.remove('dark-theme');
                body.classList.add('light-theme');
                themeIcon.textContent = 'dark_mode';
                localStorage.setItem('theme', 'light');
            } else {
                body.classList.remove('light-theme');
                body.classList.add('dark-theme');
                themeIcon.textContent = 'light_mode';
                localStorage.setItem('theme', 'dark');
            }
        }

        // Load saved theme
        document.addEventListener('DOMContentLoaded', function() {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            const body = document.body;
            const themeIcon = document.getElementById('theme-icon');
            
            if (savedTheme === 'light') {
                body.classList.remove('dark-theme');
                body.classList.add('light-theme');
                themeIcon.textContent = 'dark_mode';
            } else {
                body.classList.add('dark-theme');
                themeIcon.textContent = 'light_mode';
            }
        });

        // Data refresh functionality
        async function refreshData() {
            const loadingSpinner = document.getElementById('loading-spinner');
            const statusMessage = document.getElementById('status-message');
            const imageDisplay = document.getElementById('image-display');
            const errorDisplay = document.getElementById('error-display');
            const jsonDisplay = document.getElementById('json-display');
            const lastUpdate = document.getElementById('last-update');
            
            // Show loading state
            loadingSpinner.style.display = 'block';
            statusMessage.textContent = 'Daten werden geladen...';
            imageDisplay.style.display = 'none';
            errorDisplay.style.display = 'none';
            
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                // Update JSON display
                jsonDisplay.textContent = JSON.stringify(data, null, 2);
                
                // Update last update time
                lastUpdate.textContent = new Date().toLocaleString('de-DE');
                
                if (data.success && data.data) {
                    // Success - show image
                    const imageUrl = data.data.image_url;
                    const filename = data.data.filename || 'Unbekannt';
                    const firmwareUpdate = data.data.update_firmware ? 'Ja' : 'Nein';
                    
                    document.getElementById('trmnl-image').src = imageUrl;
                    document.getElementById('filename').textContent = filename;
                    document.getElementById('firmware-update').textContent = firmwareUpdate;
                    
                    imageDisplay.style.display = 'block';
                    statusMessage.textContent = 'Daten erfolgreich geladen';
                } else {
                    // Error
                    const errorMsg = data.message || data.error || 'Unbekannter Fehler';
                    document.getElementById('error-message').textContent = errorMsg;
                    errorDisplay.style.display = 'block';
                    statusMessage.textContent = 'Fehler beim Laden der Daten';
                }
            } catch (error) {
                // Network or parsing error
                document.getElementById('error-message').textContent = 'Netzwerkfehler: ' + error.message;
                errorDisplay.style.display = 'block';
                statusMessage.textContent = 'Verbindungsfehler';
                jsonDisplay.textContent = 'Fehler beim Laden der Daten';
            } finally {
                loadingSpinner.style.display = 'none';
            }
        }

        // Auto-refresh every 30 seconds
        setInterval(refreshData, 30000);
        
        // Initialize Materialize components
        document.addEventListener('DOMContentLoaded', function() {
            M.AutoInit();
        });
    </script>
</body>
</html>
```

### 6. `app/static/style.css`

```css
/* Dark Theme Variables */
:root {
    --bg-primary: #121212;
    --bg-secondary: #1e1e1e;
    --bg-card: #2d2d2d;
    --text-primary: #ffffff;
    --text-secondary: #b3b3b3;
    --accent: #bb86fc;
    --accent-dark: #985eff;
    --success: #4caf50;
    --error: #f44336;
    --warning: #ff9800;
}

/* Light Theme Variables */
.light-theme {
    --bg-primary: #ffffff;
    --bg-secondary: #f5f5f5;
    --bg-card: #ffffff;
    --text-primary: #212121;
    --text-secondary: #757575;
    --accent: #6200ea;
    --accent-dark: #3700b3;
    --success: #4caf50;
    --error: #f44336;
    --warning: #ff9800;
}

/* Base Styles */
body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    transition: all 0.3s ease;
}

/* Navigation */
nav {
    background-color: var(--accent) !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.brand-logo {
    font-weight: 300 !important;
}

.theme-toggle, .refresh-btn {
    transition: transform 0.2s ease;
}

.theme-toggle:hover, .refresh-btn:hover {
    transform: scale(1.1);
}

/* Cards */
.card {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    transition: box-shadow 0.3s ease;
}

.card:hover {
    box-shadow: 0 8px 16px rgba(0,0,0,0.3) !important;
}

.card-title {
    color: var(--text-primary) !important;
    font-weight: 400 !important;
}

.card-title i {
    vertical-align: middle;
    margin-right: 8px;
}

/* Buttons */
.btn {
    background-color: var(--accent) !important;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn:hover {
    background-color: var(--accent-dark) !important;
    transform: translateY(-2px);
}

.btn:focus {
    background-color: var(--accent-dark) !important;
}

/* Status Indicators */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* Content Areas */
.json-container {
    background-color: var(--bg-secondary);
    color: var(--text-secondary);
    padding: 16px;
    border-radius: 4px;
    border: 1px solid rgba(255,255,255,0.1);
    font-family: 'Courier New', monospace;
    font-size: 12px;
    max-height: 300px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.light-theme .json-container {
    border: 1px solid rgba(0,0,0,0.1);
    background-color: #f8f8f8;
    color: #333;
}

/* Image Display */
#trmnl-image {
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    max-width: 800px;
    width: 100%;
    height: auto;
}

.content-info {
    margin-top: 16px;
    padding: 16px;
    background-color: var(--bg-secondary);
    border-radius: 4px;
    border-left: 4px solid var(--accent);
}

.light-theme .content-info {
    background-color: #f8f8f8;
}

/* Error Display */
.card-panel.red.lighten-4 {
    background-color: rgba(244, 67, 54, 0.1) !important;
    border-left: 4px solid var(--error);
    border-radius: 4px;
}

.light-theme .card-panel.red.lighten-4 {
    background-color: #ffebee !important;
}

/* Preloader */
.preloader-wrapper {
    margin: 20px auto;
}

/* Responsive Design */
@media only screen and (max-width: 768px) {
    .container {
        width: 95%;
    }
    
    .brand-logo {
        font-size: 1.8rem !important;
    }
    
    .json-container {
        font-size: 10px;
        max-height: 200px;
    }
    
    #trmnl-image {
        max-width: 100%;
    }
}

/* Loading Animation */
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.loading {
    animation: pulse 1.5s infinite;
}

/* Smooth Transitions */
* {
    transition: color 0.3s ease, background-color 0.3s ease;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-dark);
}

/* Focus Styles */
.btn:focus,
a:focus {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}

/* Print Styles */
@media print {
    body {
        background-color: white !important;
        color: black !important;
    }
    
    .card {
        background-color: white !important;
        color: black !important;
        box-shadow: none !important;
        border: 1px solid #ccc !important;
    }
    
    nav, .theme-toggle, .refresh-btn {
        display: none !important;
    }
}
```

### 7. `Dockerfile`

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .
COPY .env .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run application
CMD ["python", "app.py"]
```

### 8. `docker-compose.yml`

```yaml
version: '3.8'

services:
  trmnl-dashboard:
    build: .
    container_name: trmnl-dashboard
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=false
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    networks:
      - trmnl-network

networks:
  trmnl-network:
    driver: bridge
```

---

## Installation & Verwendung

### Voraussetzungen

- Python 3.11+
- UV Package Manager
- Docker & Docker Compose (für Container-Deployment)

### Lokale Installation

1. **Repository klonen und Dependencies installieren:**

   ```bash
   git clone <repository-url>
   cd trmnl-dashboard

   # UV installieren (falls nicht vorhanden)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Dependencies installieren
   uv sync
   ```

2. **Umgebungsvariablen konfigurieren:**

   ```bash
   nano .env
   # TRMNL_DEVICE_ID mit der MAC-Adresse Ihres Geräts ersetzen
   # Format: XX:XX:XX:XX:XX:XX (z.B. A1:B2:C3:D4:E5:F6)
   ```

3. **Anwendung starten:**

   ```bash
   cd app
   uv run python app.py
   ```

4. **Im Browser öffnen:**

   [http://localhost:5000](http://localhost:5000)

### Docker Installation

1. **Container erstellen und starten:**

   ```bash
   nano .env
   docker-compose up -d
   ```

2. **Logs anzeigen:**

   ```bash
   docker-compose logs -f
   ```

3. **Container stoppen:**

   ```bash
   docker-compose down
   ```

---

## Konfiguration

### Wichtige Umgebungsvariablen

| Variable           | Beschreibung                                 |
|--------------------|----------------------------------------------|
| TRMNL_API_KEY      | Ihr TRMNL API Schlüssel                      |
| TRMNL_DEVICE_ID    | MAC-Adresse Ihres TRMNL Geräts               |
| TRMNL_BASE_URL     | API Base URL (Standard: https://trmnl.app/api) |

### Device ID ermitteln

Die Device ID ist die MAC-Adresse Ihres TRMNL Geräts, die bei jedem API-Aufruf im 'ID' Header übertragen wird. Sie finden diese:

1. Im TRMNL Web-Dashboard unter "Device Settings"
2. Auf dem Gerät selbst (meist auf einem Aufkleber)
3. In der TRMNL Mobile App

---

## Features

| Feature              | Beschreibung                                      |
|----------------------|---------------------------------------------------|
| Real-time Display    | Zeigt den aktuellen Inhalt Ihres Geräts an         |
| Dark/Light Mode      | Umschaltbare Themes mit Materialize CSS            |
| Auto-Refresh         | Automatische Aktualisierung alle 30 Sekunden       |
| Responsive Design    | Funktioniert auf Desktop und Mobile                |
| Error Handling       | Ausführliche Fehlerbehandlung und -anzeige         |
| Debug Information    | Raw API Response Anzeige für Debugging             |
| Docker Support       | Containerisierte Deployment-Option                 |

---

## API Endpunkte

| Methode | Pfad            | Beschreibung                       |
|---------|-----------------|------------------------------------|
| GET     | /               | Hauptdashboard                      |
| GET     | /api/status     | TRMNL Status und aktueller Inhalt   |
| GET     | /api/refresh    | Daten neu laden (wie /api/status)   |

---

## Troubleshooting

### Häufige Probleme

1. **"Device ID nicht konfiguriert"**
   - Überprüfen Sie die TRMNL_DEVICE_ID in der .env Datei
   - Format muss XX:XX:XX:XX:XX:XX sein

2. **"API Error: 401"**
   - API Key überprüfen
   - Device ID überprüfen

3. **"Connection Error"**
   - Internetverbindung prüfen
   - TRMNL_BASE_URL überprüfen

### Logs anzeigen

```bash
# Lokale Entwicklung
cd app && python app.py

# Docker
docker-compose logs -f trmnl-dashboard
```

---

## Entwicklung

### Dependencies hinzufügen

```bash
uv add <package-name>
```

### Tests ausführen

```bash
uv run pytest
```

### Code formatieren

```bash
uv run black app/
```

---

## Lizenz

MIT License – siehe LICENSE Datei für Details.

---

## Support

Bei Fragen oder Problemen:

1. Überprüfen Sie die .env Konfiguration
2. Prüfen Sie die TRMNL API Dokumentation
3. Kontaktieren Sie den TRMNL Support

---

> **Hinweis:** Stellen Sie sicher, dass Sie über ein TRMNL Developer Edition Gerät oder entsprechende API-Berechtigung verfügen, um die Private API zu nutzen.
