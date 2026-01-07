from flask import Flask, request, Response
from scrape_petfinder import scrape_html
from scrape_js import scrape_html_js
from urllib.parse import unquote
import os

app = Flask(__name__)

def get_endpoint_key():
    """Get endpoint key from file or environment variable."""
    if os.path.exists('endpointkey.txt'):
        with open('endpointkey.txt', 'r') as f:
            return f.read().strip()
    return os.environ.get('ENDPOINT_KEY', '')

ENDPOINT_KEY = get_endpoint_key()

@app.route('/')
def home():
    return """
    <h1>HTML Scraper API</h1>
    <p>Usage:</p>
    <ul>
        <li><strong>GET:</strong> <code>/scrape?url=https://example.com&key=YOUR_KEY</code></li>
        <li><strong>POST:</strong> <code>/scrape</code> with JSON body: <code>{"url": "https://example.com", "key": "YOUR_KEY"}</code></li>
        <li><strong>GET:</strong> <code>/scrape-js?url=https://example.com&key=YOUR_KEY</code> (for JavaScript-rendered pages)</li>
        <li><strong>POST:</strong> <code>/scrape-js</code> with JSON body: <code>{"url": "https://example.com", "key": "YOUR_KEY"}</code></li>
    </ul>
    <p>Returns the HTML content of the requested URL.</p>
    <p><strong>Note:</strong> All requests require a valid endpoint key.</p>
    <p><strong>/scrape-js</strong> waits for JavaScript to execute and dynamic content to load.</p>
    """

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

@app.route('/scrape-js', methods=['GET', 'POST'])
def scrape_js():
    """
    Scrape HTML from a URL that requires JavaScript execution.
    Waits for dynamic content to load before returning HTML.
    """
    try:
        if request.method == 'GET':
            key = request.args.get('key')
            url = request.args.get('url')
            wait_timeout = int(request.args.get('wait_timeout', 20))
            additional_wait = int(request.args.get('additional_wait', 5))
        else:
            data = request.get_json() or {}
            key = data.get('key')
            url = data.get('url')
            wait_timeout = int(data.get('wait_timeout', 20))
            additional_wait = int(data.get('additional_wait', 5))
        
        if not key or key != ENDPOINT_KEY:
            return {"error": "Invalid or missing endpoint key"}, 401
        
        if not url:
            return {"error": "Missing 'url' parameter. Use ?url=...&key=... for GET or {\"url\": \"...\", \"key\": \"...\"} for POST"}, 400
        
        url = unquote(url)
        
        try:
            html_content = scrape_html_js(url, wait_timeout=wait_timeout, additional_wait=additional_wait)
        except Exception as e:
            return {"error": f"Scraping failed: {str(e)}. Chrome/ChromeDriver may not be installed on the server."}, 500
        
        if html_content:
            return Response(
                html_content,
                mimetype='text/html',
                headers={'Content-Type': 'text/html; charset=utf-8'}
            ), 200
        else:
            return {"error": "Failed to scrape the page. JavaScript execution may have failed or ChromeDriver may not be available. Check server logs for details."}, 500
            
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    try:
        # Get key and URL from request
        if request.method == 'GET':
            key = request.args.get('key')
            url = request.args.get('url')
        else:
            data = request.get_json() or {}
            key = data.get('key')
            url = data.get('url')
        
        # Validate endpoint key
        if not key or key != ENDPOINT_KEY:
            return {"error": "Invalid or missing endpoint key"}, 401
        
        if not url:
            return {"error": "Missing 'url' parameter. Use ?url=...&key=... for GET or {\"url\": \"...\", \"key\": \"...\"} for POST"}, 400
        
        url = unquote(url)
        html_content = scrape_html(url)
        
        if html_content:
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