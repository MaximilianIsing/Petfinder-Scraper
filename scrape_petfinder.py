import requests
from requests.exceptions import RequestException
import time

def scrape_html(url):
    """
    Scrapes HTML content from a given URL.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        str: HTML content if successful, None otherwise
    """
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # Extract domain for referer
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # Set comprehensive headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': f'{domain}/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        
        # First, visit the main page to get cookies (optional, helps with some sites)
        try:
            print(f"Visiting main page to establish session: {domain}")
            session.get(f'{domain}/', headers=headers, timeout=10)
            # Small delay to appear more human-like
            time.sleep(1)
        except:
            # If main page fails, continue anyway
            pass
        
        # Now make the request to the specific page
        print("Fetching the target page...")
        response = session.get(url, headers=headers, timeout=10)
        
        # Check if request was successful
        response.raise_for_status()
        
        return response.text
        
    except RequestException as e:
        print(f"Error fetching the page: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status code: {e.response.status_code}")
            print(f"Response headers: {dict(e.response.headers)}")
        return None

if __name__ == "__main__":
    url = "https://www.petfinder.com/dog/dottie-e9f13b5a-5b60-41f1-a4ca-20e3a8355c3d/ny/new-york/every-last-one-rescue-inc-ny1653/details/"
    
    print(f"Scraping HTML from: {url}")
    html_content = scrape_html(url)
    
    if html_content:
        # Save to file
        with open("petfinder_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"HTML content saved to 'petfinder_page.html'")
        print(f"Total characters: {len(html_content)}")
        
        # Optionally print first 500 characters as preview
        print("\nFirst 500 characters preview:")
        print(html_content[:500])
    else:
        print("Failed to scrape the page.")

