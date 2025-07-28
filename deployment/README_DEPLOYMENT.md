# Logstash Pipeline Formatter - Deployment Guide

## Voor Windows Server 2019

Deze applicatie is een Flask web-app die Logstash pipeline configuraties kan formatteren en valideren.

## Vereisten
- Python 3.7 of hoger geïnstalleerd op de Windows Server 2019 machine
- Toegang tot internet voor package installatie (alleen bij eerste setup)

## Installatie Instructies

### Stap 1: Extract de ZIP file
1. Download en extract de `logstash-formatter-deployment.zip` naar een map op je Windows Server
2. Bijvoorbeeld: `C:\Tools\logstash-formatter\`

### Stap 2: Installeer dependencies
1. Open Command Prompt als Administrator
2. Navigeer naar de geëxtracte map:
   ```cmd
   cd C:\Tools\logstash-formatter
   ```
3. Installeer de vereiste Python packages:
   ```cmd
   pip install -r requirements.txt
   ```

### Stap 3: Start de applicatie
1. Dubbelklik op `start_app.bat` OF
2. Run via command line:
   ```cmd
   python app.py
   ```

### Stap 4: Gebruik de applicatie
1. De applicatie start automatisch je webbrowser
2. Als dat niet gebeurt, ga naar: http://localhost:5001
3. Upload een Logstash configuratie file of plak de tekst in het tekstveld
4. Klik op "Format" om de configuratie te formatteren

## Stoppen van de applicatie
- Klik op de "Shutdown Server" knop in de web interface, OF
- Druk Ctrl+C in de command prompt waar de app draait

## Troubleshooting

### Python niet gevonden
Als je de fout krijgt dat Python niet gevonden wordt:
1. Controleer of Python geïnstalleerd is: `python --version`
2. Als dat niet werkt, probeer: `py --version` of `python3 --version`
3. Update het `start_app.bat` bestand met het juiste Python commando

### Port 5001 al in gebruik
Als port 5001 al in gebruik is, wijzig de port in `app.py`:
```python
app.run(debug=False, port=5002, use_reloader=False)  # Wijzig 5001 naar 5002
```

### Dependencies installatie faalt
Als pip install faalt:
1. Controleer internetverbinding
2. Probeer: `python -m pip install --upgrade pip`
3. Probeer vervolgens: `python -m pip install -r requirements.txt`

## Security Notes
- Deze applicatie is bedoeld voor interne/ontwikkel gebruik
- De app draait alleen op localhost (127.0.0.1)
- Verander de `secret_key` in `app.py` voor productie gebruik

## Support
Voor vragen of problemen, neem contact op met de IT afdeling.
