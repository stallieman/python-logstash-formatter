from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sys
import threading
import time
import webbrowser
from utils.formatter import check_pipeline_file, check_pipeline_text

app = Flask(__name__)
# Voor productie: gebruik een sterkere secret key
app.secret_key = 'your-secret-key-change-this-in-production-2024'
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Zorg ervoor dat de uploads directory bestaat
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Geen bestand geselecteerd')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Geen bestand geselecteerd')
        return redirect(url_for('index'))
    
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        formatted_output, errors, fixes_applied = check_pipeline_file(file_path)
        
        # Verwijder het geüploade bestand na verwerking (voor veiligheid)
        try:
            os.remove(file_path)
        except:
            pass
            
        if errors or fixes_applied:
            return render_template('index.html', 
                                 formatted_output=formatted_output, 
                                 errors=errors, 
                                 fixes_applied=fixes_applied)
        else:
            flash('Bestand succesvol geformatteerd!')
            return render_template('index.html', formatted_output=formatted_output)
    
    return redirect(url_for('index'))

@app.route('/format', methods=['POST'])
def format_pipeline_text():
    pipeline_text = request.form.get("pipeline")
    if not pipeline_text or pipeline_text.strip() == "":
        flash("Geen pipeline tekst opgegeven")
        return redirect(url_for('index'))
    
    formatted_output, errors, fixes_applied = check_pipeline_text(pipeline_text)
    return render_template('index.html', 
                         formatted_output=formatted_output, 
                         errors=errors, 
                         fixes_applied=fixes_applied, 
                         pipeline_text=pipeline_text)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    def shutdown_server():
        time.sleep(1)  # Geef tijd voor response
        print("Application shutting down...")
        os._exit(0)
    
    thread = threading.Thread(target=shutdown_server)
    thread.daemon = True
    thread.start()
    return "Server wordt afgesloten..."

def open_browser():
    """Open browser na een korte vertraging"""
    time.sleep(2)
    try:
        webbrowser.open('http://127.0.0.1:5001')
    except:
        print("Kon browser niet automatisch openen. Ga handmatig naar http://127.0.0.1:5001")

if __name__ == '__main__':
    print("=" * 60)
    print("Logstash Pipeline Formatter wordt gestart...")
    print("=" * 60)
    print("Applicatie draait op: http://127.0.0.1:5001")
    print("Browser wordt automatisch geopend...")
    print("Druk Ctrl+C om te stoppen")
    print("=" * 60)
    
    # Start browser opening in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Start Flask app
        app.run(debug=False, host='127.0.0.1', port=5001, use_reloader=False)
    except KeyboardInterrupt:
        print("\nApplicatie gestopt door gebruiker")
    except Exception as e:
        print(f"Fout bij starten van applicatie: {e}")
        input("Druk Enter om te sluiten...")
