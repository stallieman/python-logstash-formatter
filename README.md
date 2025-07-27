# Logstash Pipeline Formatter

Een professionele web-based tool voor het formatteren en valideren van Logstash pipeline configuraties met geavanceerde auto-fix functionaliteit.

## ✨ Features

### 🔧 Auto-Fix Functionaliteit
- **Ontbrekende quotes**: Automatisch quotes toevoegen rond waarden
- **Onjuiste quotes**: Slimme quote normalisatie 
- **Ontbrekende accolades**: Automatisch sluitende `}` toevoegen
- **Accolade-tekst splitsing**: `}tcp {` wordt gesplitst naar `}` en `tcp {`
- **Whitespace cleanup**: Overtollige spaties verwijderen en normaliseren
- **Template preservation**: `%{field}` variabelen blijven intact

### 🌐 Web Interface
- Clean, responsive design
- Real-time formatting en validatie
- Copy-to-clipboard functionaliteit
- File upload ondersteuning
- Production-ready met graceful shutdown

### 📦 Deployment
- Standalone executable voor Windows/Mac/Linux
- Geen installatie vereist
- Auto-browser opening
- Complete distributie met documentatie

## 🚀 Quick Start

### Development
```bash
# Clone repository
git clone https://github.com/marcostalman/python-logstash-formatter.git
cd python-logstash-formatter

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Bezoek http://127.0.0.1:5001 in je browser.

### Production Deployment

Download de latest release en pak uit op je machine.

**Windows:**
- Dubbelklik `LogstashPipelineFormatter_v2.exe` 
- Of gebruik `START_WINDOWS_v2.bat` voor vriendelijke interface

**Mac/Linux:**
- `./LogstashPipelineFormatter_v2`

## 🛠️ Building Executable

```bash
# Setup build environment
python -m venv build_env
source build_env/bin/activate
pip install pyinstaller flask

# Build executable
python build_executable.py
```

## 📁 Project Structure

```
python-logstash-formatter/
├── app.py                              # Main Flask application
├── requirements.txt                    # Python dependencies
├── build_executable.py                 # Production build script
├── config/
│   └── settings.py                     # App configuration
├── static/
│   ├── css/styles.css                  # Styling
│   └── js/scripts.js                   # Client-side functionality
├── templates/
│   └── index.html                      # Main web interface
├── utils/
│   └── formatter.py                    # Core formatting logic
└── uploads/                            # File upload directory
```

## 🔧 Configuration

De applicatie gebruikt standaard instellingen die geschikt zijn voor de meeste use cases. Configuratie kan worden aangepast in `config/settings.py`.

## 🤝 Contributing

1. Fork het project
2. Maak een feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit je changes (`git commit -m 'Add some AmazingFeature'`)
4. Push naar de branch (`git push origin feature/AmazingFeature`)
5. Open een Pull Request

## 📝 License

Dit project is gelicenseerd onder de MIT License - zie het [LICENSE](LICENSE) bestand voor details.

## 🎯 Use Cases

- **DevOps Teams**: Valideren van Logstash configuraties voor deployment
- **System Administrators**: Cleanup van legacy configuratiebestanden  
- **Data Engineers**: Formatteren van complexe pipeline definities
- **Security Teams**: Standaardiseren van log processing configuraties

## 🏆 Credits

Ontwikkeld door [Marcos Talman](https://github.com/marcostalman) voor professioneel gebruik in enterprise omgevingen.