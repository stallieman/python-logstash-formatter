from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sys
import threading
import time
import webbrowser
from utils.formatter import check_pipeline_file, check_pipeline_text

app = Flask(__name__)
app.secret_key = 'fefj;efFWEFGGWEFWFWEFFWEF3R3R'
app.config['UPLOAD_FOLDER'] = 'uploads/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        formatted_output, errors, fixes_applied = check_pipeline_file(file_path)
        if errors or fixes_applied:
            return render_template('index.html', formatted_output=formatted_output, errors=errors, fixes_applied=fixes_applied)
        else:
            flash('File formatted successfully!')
            return render_template('index.html', formatted_output=formatted_output)
    
    return redirect(url_for('index'))

@app.route('/format', methods=['POST'])
def format_pipeline_text():
    pipeline_text = request.form.get("pipeline")
    if not pipeline_text or pipeline_text.strip() == "":
        flash("No pipeline text provided")
        return redirect(url_for('index'))
    formatted_output, errors, fixes_applied = check_pipeline_text(pipeline_text)
    return render_template('index.html', formatted_output=formatted_output, errors=errors, fixes_applied=fixes_applied, pipeline_text=pipeline_text)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    def shutdown_server():
        time.sleep(1)  # Give time for response to be sent
        os._exit(0)
    
    thread = threading.Thread(target=shutdown_server)
    thread.start()
    return "Shutting down..."

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5001')

if __name__ == '__main__':
    print("Starting Logstash Pipeline Formatter...")
    print("Opening browser in 1.5 seconds...")
    
    # Start browser opening in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    app.run(debug=False, port=5001, use_reloader=False)