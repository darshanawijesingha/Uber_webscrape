from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from bs4 import BeautifulSoup

# UberEats Scraping Configuration
#URL = 'link of grocery'
URL = 'https://www.ubereats.com/lk/store/'
SCROLL_PAUSE_TIME = 3
SCROLL_INCREMENT = 500
MAX_NO_NEW_ITEMS_ATTEMPTS = 20

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def scroll_page(driver, increment):
    driver.execute_script(f"window.scrollBy(0, {increment});")

# Extract product data from the page
def extract_data(soup, scraped_items):
    products = soup.find_all('div', {'data-testid': lambda value: value and value.startswith('store-item')})
    data = []

    for product in products:
        item_id = product.get('data-testid')
        if item_id in scraped_items:
            continue

        scraped_items.add(item_id)

        # Extract Current Price
        price1 = product.find('span', {'data-testid': 'rich-text', 'class': lambda c: c and 'g9' in c})

        # Extract Original Price
        price2 = product.find('span', {'data-testid': 'rich-text', 'class': lambda c: c and 'be' in c})

        # Extract Description
        description = product.find('span', {'data-testid': 'rich-text', 'class': 'g7 g8 g9 be bf fq di ga'})

        data.append({
            'Current Price': price1.text.strip() if price1 else 'N/A',
            'Original Price': price2.text.strip() if price2 else 'N/A',
            'Description': description.text.strip() if description else 'N/A'
        })

    return data

def scrape_uber_eats(driver):
    scraped_items = set()
    all_data = []
    no_new_items_attempts = 0

    try:
        driver.get(URL)
        print("Page loaded. Starting scraping...")

        while no_new_items_attempts < MAX_NO_NEW_ITEMS_ATTEMPTS:
            scroll_page(driver, SCROLL_INCREMENT)
            time.sleep(SCROLL_PAUSE_TIME)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            new_data = extract_data(soup, scraped_items)
            if new_data:
                all_data.extend(new_data)
                print(f"Found {len(new_data)} new items. Total items: {len(all_data)}")
                no_new_items_attempts = 0  # Reset attempts
            else:
                no_new_items_attempts += 1
                print(f"No new items found. Attempt {no_new_items_attempts}/{MAX_NO_NEW_ITEMS_ATTEMPTS}")

        print("Scraping completed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    KOTTE = pd.DataFrame(all_data)
    return KOTTE

if __name__ == "__main__":
    driver = init_driver()
    data = scrape_uber_eats(driver)

    # Save to CSV in the current directory
    output_file = "path/ubereats_scraped_data.csv"
    data.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"\n✅ Scraping complete. Data saved to '{output_file}'")
    print(data)
