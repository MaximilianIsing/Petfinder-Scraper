import requests
import time
from requests.exceptions import RequestException
from urllib.parse import urlparse

def scrape_html(url):
    """
    Scrapes HTML content from a given URL.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        str: HTML content if successful, None otherwise
    """
    try:
        session = requests.Session()
        
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
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
        
        try:
            session.get(f'{domain}/', headers=headers, timeout=10)
            time.sleep(1)
        except:
            pass
        
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        return response.text
        
    except RequestException as e:
        return None

if __name__ == "__main__":
    url = "https://www.petfinder.com/dog/dottie-e9f13b5a-5b60-41f1-a4ca-20e3a8355c3d/ny/new-york/every-last-one-rescue-inc-ny1653/details/"
    html_content = scrape_html(url)
    
    if html_content:
        with open("petfinder_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"HTML saved ({len(html_content)} characters)")
    else:
        print("Failed to scrape the page.")

