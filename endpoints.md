# HTML Scraper API Endpoints

A Flask web service that scrapes HTML content from any URL. All requests require authentication via an endpoint key.

## Base URL

```
https://petfinder-scraper.onrender.com
```

## Authentication

All requests to the `/scrape` endpoint require a valid endpoint key. The key must be provided in the request.

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy"
}
```

- Status: `200 OK`

---

### 2. Scrape HTML

**GET** `/scrape`

**POST** `/scrape`

Scrapes HTML content from a given URL.

#### Authentication

All requests require a valid endpoint key.

#### GET Request

**Query Parameters:**
- `url` (required): The URL to scrape
- `key` (required): Your endpoint key

**Example:**
```bash
curl "https://petfinder-scraper.onrender.com/scrape?url=https://www.petfinder.com/dog/...&key=YOUR_KEY"
```

**URL Encoded Example:**
```bash
curl "https://petfinder-scraper.onrender.com/scrape?url=https%3A%2F%2Fwww.example.com&key=YOUR_KEY"
```

#### POST Request

**Request Body (JSON):**
```json
{
  "url": "https://www.example.com",
  "key": "YOUR_KEY"
}
```

**Example:**
```bash
curl -X POST https://petfinder-scraper.onrender.com/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.petfinder.com/dog/...",
    "key": "YOUR_KEY"
  }'
```

#### Response

**Success (200 OK):**
- Content-Type: `text/html; charset=utf-8`
- Body: Raw HTML content of the requested page

**Error Responses:**

| Status Code | Description | Response Body |
|------------|-------------|---------------|
| 400 | Missing URL parameter | `{"error": "Missing 'url' parameter..."}` |
| 401 | Invalid or missing endpoint key | `{"error": "Invalid or missing endpoint key"}` |
| 500 | Failed to scrape page | `{"error": "Failed to scrape the page..."}` |
| 500 | Server error | `{"error": "error message"}` |

## Examples

### Python Example

```python
import requests

url = "https://petfinder-scraper.onrender.com/scrape"
params = {
    "url": "https://www.petfinder.com/dog/...",
    "key": "YOUR_KEY"
}

response = requests.get(url, params=params)
if response.status_code == 200:
    html_content = response.text
    print(f"Scraped {len(html_content)} characters")
else:
    print(f"Error: {response.json()}")
```

### JavaScript Example

```javascript
const url = 'https://petfinder-scraper.onrender.com/scrape';
const data = {
    url: 'https://www.petfinder.com/dog/...',
    key: 'YOUR_KEY'
};

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
})
.then(response => {
    if (response.ok) {
        return response.text();
    }
    return response.json().then(err => Promise.reject(err));
})
.then(html => {
    console.log('HTML content:', html);
})
.catch(error => {
    console.error('Error:', error);
});
```

## Error Handling

### Missing Key
```json
{
  "error": "Invalid or missing endpoint key"
}
```
Status: `401 Unauthorized`

### Missing URL
```json
{
  "error": "Missing 'url' parameter. Use ?url=...&key=... for GET or {\"url\": \"...\", \"key\": \"...\"} for POST"
}
```
Status: `400 Bad Request`

### Scraping Failed
```json
{
  "error": "Failed to scrape the page. The site may be blocking requests."
}
```
Status: `500 Internal Server Error`

## Notes

- The endpoint key is required for all `/scrape` requests
- URLs are automatically URL-decoded
- The service returns raw HTML content, not JSON
- Large pages may take several seconds to scrape
- Some websites may block automated requests

## Rate Limiting

Currently, there are no rate limits, but please use the service responsibly.
