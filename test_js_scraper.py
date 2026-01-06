from scrape_js import scrape_html_js

url = "https://www.petfinder.com/search/dogs-for-adoption/us/ny/newyork/?distance=anywhere&page=2"

print(f"Scraping JavaScript-rendered page: {url}")
print("This may take a moment as we wait for JavaScript to execute...")

html_content = scrape_html_js(url, wait_timeout=20, additional_wait=5)

if html_content:
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML saved to test.html ({len(html_content)} characters)")
else:
    print("Failed to scrape the page.")

