"""
Flask web service for HTML scraping - Ready for Render.com deployment
Accepts a URL and returns the HTML content
"""
from flask import Flask, request, Response
from scrape_petfinder import scrape_html
import os
from urllib.parse import unquote

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>HTML Scraper API</h1>
    <p>Usage:</p>
    <ul>
        <li><strong>GET:</strong> <code>/scrape?url=https://example.com</code></li>
        <li><strong>POST:</strong> <code>/scrape</code> with JSON body: <code>{"url": "https://example.com"}</code></li>
    </ul>
    <p>Returns the HTML content of the requested URL.</p>
    <p><strong>Example:</strong> <a href="/scrape?url=https://www.petfinder.com">/scrape?url=https://www.petfinder.com</a></p>
    """

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    """
    Scrape HTML from a URL.
    
    GET: /scrape?url=https://example.com
    POST: {"url": "https://example.com"}
    """
    try:
        # Get URL from query parameter (GET) or JSON body (POST)
        if request.method == 'GET':
            url = request.args.get('url')
        else:
            data = request.get_json() or {}
            url = data.get('url')
        
        if not url:
            return {"error": "Missing 'url' parameter. Use ?url=... for GET or {\"url\": \"...\"} for POST"}, 400
        
        # Decode URL if encoded
        url = unquote(url)
        
        # Scrape the HTML
        html_content = scrape_html(url)
        
        if html_content:
            # Return HTML directly with proper content type
            return Response(
                html_content,
                mimetype='text/html',
                headers={'Content-Type': 'text/html; charset=utf-8'}
            ), 200
        else:
            return {"error": "Failed to scrape the page. The site may be blocking requests."}, 500
            
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

