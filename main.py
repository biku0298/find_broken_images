from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests

def find_broken_images(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    images = driver.find_elements(By.TAG_NAME, "img")
    
    print(f"Total images found: {len(images)}")
    
    for img in images:
        try:
            src = img.get_attribute("src")
            if not src:
                print("image with empty src found")
                continue
            response = requests.head(src, allow_redirects=True, timeout=5)
            if response.status_code >= 400:
                print(f"broken image: {src} (Status code: {response.status_code})")
        except Exception as e:
            print(f"error checking image: {src} - {e}")
    driver.quit()

website = input("enter website URL: ")
find_broken_images(website)
