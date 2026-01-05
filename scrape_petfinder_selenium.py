from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_html_selenium(url):
    """
    Scrapes HTML content from a given URL using Selenium (for JavaScript-heavy sites).
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        str: HTML content if successful, None otherwise
    """
    driver = None
    try:
        # Configure Chrome options (Linux-compatible)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')  # Required for Linux
        chrome_options.add_argument('--disable-dev-shm-usage')  # Required for Linux
        chrome_options.add_argument('--disable-gpu')  # Recommended for headless on Linux
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # For Linux servers/Render, you may need to specify Chrome binary location
        # Uncomment and adjust if Chrome is not in PATH:
        # chrome_options.binary_location = '/usr/bin/google-chrome'  # or '/usr/bin/chromium-browser'
        # For Render.com, typically: '/usr/bin/google-chrome-stable'
        
        # Initialize the driver (Selenium 4.6+ auto-manages ChromeDriver)
        print("Starting browser...")
        try:
            # Try with automatic driver management (Selenium 4.6+)
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            # Fallback: try with webdriver-manager if available
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
            except ImportError:
                print("Note: For automatic ChromeDriver management, install: pip install webdriver-manager")
                raise e
        
        # Navigate to the page
        print(f"Loading page: {url}")
        driver.get(url)
        
        # Wait for page to load (adjust selector based on page structure)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            print("Warning: Page may not have fully loaded")
        
        # Wait a bit more for JavaScript to execute
        time.sleep(3)
        
        # Get the page source
        html_content = driver.page_source
        
        return html_content
        
    except Exception as e:
        print(f"Error fetching the page: {e}")
        return None
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    url = "https://www.petfinder.com/dog/dottie-e9f13b5a-5b60-41f1-a4ca-20e3a8355c3d/ny/new-york/every-last-one-rescue-inc-ny1653/details/"
    
    print(f"Scraping HTML from: {url}")
    html_content = scrape_html_selenium(url)
    
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

