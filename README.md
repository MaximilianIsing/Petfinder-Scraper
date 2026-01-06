# HTML Scraper API

A Flask web service that scrapes HTML from any URL. Deployed and working on Render.com.

## Files

- `app.py` - Flask web service (main application)
- `scrape_petfinder.py` - Core scraping function using requests library
- `render.yaml` - Render.com deployment configuration
- `requirements.txt` - Python dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Local Development

```bash
python app.py
```

The service will run on `http://localhost:5000`

## API Usage

**GET Request:**
```bash
curl "https://your-app.onrender.com/scrape?url=https://www.petfinder.com/dog/..."
```

**POST Request:**
```bash
curl -X POST https://your-app.onrender.com/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.petfinder.com/dog/..."}'
```

**Response:** Returns the full HTML content of the page (raw HTML, not JSON)

## Endpoints

- `GET /` - API documentation
- `GET /health` - Health check
- `GET /scrape?url=...` - Scrape a URL and return HTML
- `POST /scrape` - Scrape a URL (send JSON: `{"url": "https://..."}`) and return HTML

## Deploying on Render.com

1. Push your code to GitHub/GitLab
2. In Render dashboard, create a new "Web Service"
3. Connect your repository
4. Render will auto-detect `render.yaml` OR manually set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment:** Python 3
5. Deploy!

The service works immediately on Render's free tier with no special configuration needed.
