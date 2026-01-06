from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import os

def scrape_html_js(url, wait_timeout=20, additional_wait=5):
    """
    Scrapes HTML content from a URL that requires JavaScript execution.
    Waits for dynamic content to load before returning HTML.
    
    Args:
        url (str): The URL to scrape
        wait_timeout (int): Maximum time to wait for page load (seconds)
        additional_wait (int): Additional time to wait after page load for JS execution (seconds)
        
    Returns:
        str: HTML content if successful, None otherwise
    """
    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # For Render/Linux servers, auto-detect Chrome binary
        chrome_binary = os.environ.get('CHROME_BINARY')
        if not chrome_binary:
            # Common Chrome binary locations on Linux (including user home directory for Render)
            home_dir = os.path.expanduser('~')
            possible_paths = [
                '/usr/bin/google-chrome-stable',
                '/usr/bin/google-chrome',
                '/usr/bin/chromium-browser',
                '/usr/bin/chromium',
                f'{home_dir}/bin/google-chrome-stable',
                f'{home_dir}/chrome/opt/google/chrome/chrome'
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    chrome_binary = path
                    break
        
        if chrome_binary:
            chrome_options.binary_location = chrome_binary
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException:
            # Fallback: try with webdriver-manager if available
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
            except ImportError:
                raise Exception("ChromeDriver not found. Install Chrome/Chromium or webdriver-manager.")
        
        driver.get(url)
        
        # Wait for page to be in ready state
        WebDriverWait(driver, wait_timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # Wait for body element to be present
        try:
            WebDriverWait(driver, wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            pass
        
        # Wait for network requests to complete (if any)
        try:
            WebDriverWait(driver, wait_timeout).until(
                lambda d: d.execute_script('return jQuery.active == 0') if d.execute_script('return typeof jQuery !== "undefined"') else True
            )
        except:
            pass
        
        # Wait for any pending fetch/XHR requests
        try:
            WebDriverWait(driver, wait_timeout).until(
                lambda d: d.execute_script('''
                    return window.fetch === undefined || 
                    (window.fetch && document.readyState === 'complete')
                ''')
            )
        except:
            pass
        
        # Additional wait for JavaScript to execute and content to load
        time.sleep(additional_wait)
        
        # Scroll to bottom to trigger lazy loading if any
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
        except:
            pass
        
        html_content = driver.page_source
        return html_content
        
    except Exception as e:
        return None
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    url = "https://example.com"
    html_content = scrape_html_js(url)
    
    if html_content:
        with open("js_scraped_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"HTML saved ({len(html_content)} characters)")
    else:
        print("Failed to scrape the page.")

