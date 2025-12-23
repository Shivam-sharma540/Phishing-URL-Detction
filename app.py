from flask import Flask, render_template, request, session
from features import featureExtraction
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session

# Initialize recent_urls in session if not exists
@app.before_request
def before_request():
    if 'recent_urls' not in session:
        session['recent_urls'] = []

@app.route('/')
def index():
    return render_template('index.html', recent_urls=session.get('recent_urls', []))

@app.route('/check', methods=['POST'])
def check():
    url = request.form.get('url')
    if not url:
        return render_template('index.html', 
                           result="Please enter a valid URL.", 
                           recent_urls=session.get('recent_urls', []))

    try:
        # Ensure the URL starts with http:// or https://
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        features = featureExtraction(url).getFeaturesList()
        score = sum(features)
        result = "Likely Safe ✅" if score > 0 else "Likely Phishing ⚠️"
        
        # Add to recent URLs with timestamp and result (max 10)
        recent_urls = session.get('recent_urls', [])
        
        # Remove if already exists to avoid duplicates
        recent_urls = [u for u in recent_urls if u['url'] != url]
        
        # Add new entry to beginning
        recent_urls.insert(0, {
            'url': url,
            'result': result,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        
        # Keep only last 10
        session['recent_urls'] = recent_urls[:10]
        
    except Exception as e:
        result = f"Error: Could not process this URL. Please check if it's valid."

    return render_template('index.html', 
                         result=result, 
                         checked_url=url,
                         recent_urls=session.get('recent_urls', []))

if __name__ == '__main__':
    app.run(debug=True)