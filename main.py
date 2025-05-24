import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

def find_broken_images(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    service = Service(executable_path=chromedriver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(3)

    broken_images = []
    images = driver.find_elements(By.TAG_NAME, "img")
    total_images = len(images)
    print(f"total images found: {total_images}")

    for i in range(total_images):
        try:
            images = driver.find_elements(By.TAG_NAME, "img")
            img = images[i]
            src = img.get_attribute("src")
            if not src:
                broken_images.append("(no src attribute)")
                continue

            try:
                response = requests.head(src, allow_redirects=True, timeout=5)
                if response.status_code >= 400:
                    broken_images.append(src)
            except requests.RequestException:
                broken_images.append(src)

        except StaleElementReferenceException:
            continue

    driver.quit()

    if broken_images:
        print(f"\nbroken images found: {len(broken_images)}")
        for b_img in broken_images:
            print(b_img)
    else:
        print("No broken images found.")

if __name__ == "__main__":
    website = input("enter website URL: ")
    find_broken_images(website)
