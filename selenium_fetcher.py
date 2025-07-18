from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_product_links_selenium(category_url, timeout=30):
    chrome_path = "/usr/bin/chromium"
    chromedriver_path = "/usr/bin/chromedriver"

    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122 Safari/537.36")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.set_page_load_timeout(timeout)
    driver.get(category_url)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # 🍪 Cookies lišta
    try:
        cookie_button = driver.find_element(By.CSS_SELECTOR, ".cookie-accept-button")
        driver.execute_script("arguments[0].click();", cookie_button)
        time.sleep(1)
        driver.execute_script("document.querySelector('#cookie-bar')?.remove();")
    except Exception:
        pass

    # 🔽 Scrollování pro vykreslení tlačítka
    found_button = False
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        try:
            buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Načíst vše')]")
            for btn in buttons:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView();", btn)
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(4)
                    found_button = True
                    print("[INFO] Tlačítko 'Načíst vše' úspěšně kliknuto.")
                    break
            if found_button:
                break
        except Exception:
            continue

    if not found_button:
        print("[WARNING] Tlačítko 'Načíst vše' nebylo nalezeno ani po scrollování.")

    # 🔗 Načtení produktových odkazů
    links = []
    elements = driver.find_elements(By.CSS_SELECTOR, "a.item_link, div.item a[href*='/']")
    for el in elements:
        href = el.get_attribute("href")
        if href and not href.endswith("#") and "ajaxPage" not in href:
            links.append(href)

    driver.quit()
    return list(set(links))
