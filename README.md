# Petfinder Web Scraper

Python scripts to scrape HTML from Petfinder pages.

## Files

- `scrape_petfinder.py` - Uses requests library (lightweight, fast)
- `scrape_petfinder_selenium.py` - Uses Selenium with Chrome (handles JavaScript, more reliable for protected sites)

## Installation

### For requests version (scrape_petfinder.py)
```bash
pip install requests
```

### For Selenium version (scrape_petfinder_selenium.py)
```bash
pip install selenium
```

## Linux Server Setup

### Option 1: Requests Version (Recommended for Linux)
The `scrape_petfinder.py` script works out of the box on Linux - no additional setup needed!

```bash
python scrape_petfinder.py
```

### Option 2: Selenium Version (If requests fails)

**Requirements:**
1. Install Chrome or Chromium on your Linux server:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y chromium-browser chromium-chromedriver
   
   # Or for Google Chrome:
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
   ```

2. Install Python dependencies:
   ```bash
   pip install selenium
   # Optional: for automatic ChromeDriver management
   pip install webdriver-manager
   ```

3. If Chrome/Chromium is not in PATH, edit `scrape_petfinder_selenium.py` and uncomment:
   ```python
   chrome_options.binary_location = '/usr/bin/google-chrome'  # or '/usr/bin/chromium-browser'
   ```

4. Run the script:
   ```bash
   python scrape_petfinder_selenium.py
   ```

## Usage

Both scripts will:
1. Fetch the HTML from the Petfinder page
2. Save it to `petfinder_page.html`
3. Display a preview of the content

## Deploying on Render.com

### Web Service API (Ready to Deploy) ✅

**Deploy as a web service that accepts a URL and returns HTML - works perfectly on Render!**

1. Push your code to GitHub/GitLab
2. In Render dashboard, create a new "Web Service"
3. Connect your repository
4. Render will auto-detect `render.yaml` OR manually set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment:** Python 3
5. Deploy!

**API Usage:**

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

**Response:** Returns the full HTML content of the page (not JSON, just raw HTML)

**Endpoints:**
- `GET /` - API documentation
- `GET /health` - Health check
- `GET /scrape?url=...` - Scrape a URL and return HTML
- `POST /scrape` - Scrape a URL (send JSON: `{"url": "https://..."}`) and return HTML

### Option 2: Simple Script (One-time run)

If you just want to run the script once:

1. In Render dashboard, create a new "Web Service" or "Background Worker"
2. Settings:
   - **Build Command:** `pip install requests`
   - **Start Command:** `python scrape_petfinder.py`
3. Deploy!

The requests version requires no special setup and works immediately on Render.

### Option 2: Selenium Version (Advanced)

For Selenium on Render, you need to install Chrome during build:

1. Use the provided `build.sh` script
2. In Render dashboard settings:
   - **Build Command:** `chmod +x build.sh && USE_SELENIUM=true ./build.sh`
   - **Start Command:** `python scrape_petfinder_selenium.py`
   - **Environment:** Python 3
3. Make sure `build.sh` is executable (chmod +x)

**Note:** Selenium on Render requires a paid plan or may hit resource limits on free tier due to Chrome's memory usage.

### Quick Render Setup (Requests Version)

1. Create `render.yaml` in your repo (already included)
2. Connect repo to Render
3. Render will auto-detect and deploy

## Notes

- The requests version is faster and lighter, but may be blocked by some sites
- The Selenium version uses a real browser, so it's less likely to be blocked
- For production Linux servers, the requests version is recommended unless you need JavaScript rendering
- **For Render.com, use the requests version** - it's simpler, faster, and works on free tier

