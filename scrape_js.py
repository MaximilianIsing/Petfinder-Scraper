from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import os

def scrape_html_js(url, wait_timeout=15, additional_wait=3):
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
        
        # Memory optimization options for Render's limited resources
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-translate')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-features=TranslateUI')
        chrome_options.add_argument('--disable-component-extensions-with-background-pages')
        chrome_options.add_argument('--disable-breakpad')
        chrome_options.add_argument('--disable-component-update')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')  # Only fatal errors
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--disable-web-security')  # May help with some sites
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
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
        
        # Set timeouts to prevent hanging
        driver.set_page_load_timeout(wait_timeout + additional_wait + 5)
        driver.implicitly_wait(5)
        
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
        
        # Scroll to bottom to trigger lazy loading if any (but limit scrolling to save memory)
        try:
            # Only scroll if page is not too large
            page_height = driver.execute_script("return document.body.scrollHeight")
            if page_height < 50000:  # Only scroll if page is reasonable size
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)  # Reduced wait time
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(0.5)  # Reduced wait time
        except:
            pass
        
        # Get HTML content
        html_content = driver.page_source
        
        # Clean up driver immediately to free memory
        driver.quit()
        driver = None
        
        return html_content
        
    except MemoryError:
        return None
    except Exception as e:
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    url = "https://example.com"
    html_content = scrape_html_js(url)
    
    if html_content:
        with open("js_scraped_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"HTML saved ({len(html_content)} characters)")
    else:
        print("Failed to scrape the page.")

