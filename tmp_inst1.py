from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

from urllib.parse import urljoin

def scroll_to_position(driver, target_pos=100000, step=1000, pause=0.5):
    current_pos = 0
    pred_scroll_pos = -1
    while current_pos < target_pos:
        scroll_pos = driver.execute_script("return window.pageYOffset;")
        if scroll_pos == pred_scroll_pos:
            break
        current_pos += step
        if current_pos > target_pos:
            current_pos = target_pos
        driver.execute_script(f"window.scrollTo(0, {current_pos});")
        pred_scroll_pos = scroll_pos
        time.sleep(pause)

def extract_reviews(current_url):
    driver.get(current_url)
    time.sleep(5)
    scroll_to_position(driver)

    reviews = driver.find_elements(By.CSS_SELECTOR, "div.v5r_30")
    print(f"Найдено {len(reviews)} отзывов на товар: {current_url}")

    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        for review in reviews:
            try:
                text_element = review.find_element(By.XPATH, ".//div[contains(@class, 'rq4_30') and contains(@class, 'q2s_30')]//span[contains(@class, 'r4q_30')]")
                review_text = text_element.text.strip()

                date_element = review.find_element(By.XPATH, ".//div[contains(@class, 'qr3_30')]//div[contains(@class, 'q3r_30')]")
                review_date = date_element.text.strip()

                rating = len(review.find_elements(By.CSS_SELECTOR, ".r3q_30 svg[style*='rgb(255, 165, 0)']"))

                like_button = review.find_element(By.XPATH, ".//button[contains(., 'Да')]")
                like_text = like_button.text.strip()
                like_count = int(like_text.replace("Да", "").strip())

                writer.writerow([review_text, review_date, rating, like_count])
            except Exception as e:
                print("Ошибка при получении отзыва:", e)

def get_next_product_url():
    try:
        container = driver.find_element(By.CSS_SELECTOR, ".vj9_24.wj0_24.a310-a")
        link = container.find_element(By.CSS_SELECTOR, "a.tile-clickable-element")
        next_url = link.get_attribute("href")
        return "https://www.ozon.ru" + next_url if next_url.startswith("/") else next_url
    except Exception as e:
        print("Ошибка при поиске рекомендованного товара:", e)
        return None


if __name__ == '__main__':

    START_URL = "https://www.ozon.ru/product/rikor-spb-302-1-noutbuk-15-6-amd-ryzen-5-6600u-ram-16-gb-ssd-512-gb-amd-radeon-660m-windows-pro-1955537740/?at=28t0LVjrKuG1NBmVTW7ly6OuJwEJ6kh14JR9qT9OE2XM"

    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/122.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service("./chromedriver.exe"), options=options)

    csv_file = "data5.csv"
    csv_headers = ["review_text", "review_date", "rating", "like_count"]

    # Создаем CSV, если не существует
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_headers)


    visited = set()
    current_url = START_URL

    while current_url and current_url not in visited:
        visited.add(current_url)
        extract_reviews(current_url)
        next_url = get_next_product_url()

        if next_url and next_url not in visited:
            print("Переходим к следующему товару:", next_url)
            current_url = next_url
        else:
            print("Следующий товар не найден или уже обработан.")
            break

    driver.quit()
