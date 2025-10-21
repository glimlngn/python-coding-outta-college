from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://ozh.github.io/cookieclicker/')

time.sleep(2)
language = driver.find_element(By.ID, value='langSelect-EN')
language.click()

time.sleep(2)
cookie_button = driver.find_element(By.ID, value='bigCookie')
timeout = time.time() + 300
time_after_5_seconds = time.time() + 5
ctr = 0

while time.time() < timeout:
    cookie_button.click()
    if time.time() > time_after_5_seconds:
        time_after_5_seconds = time.time() + 5
        unlocked_products = driver.find_elements(By.CSS_SELECTOR, value='.product.unlocked.enabled')
        try:
            unlocked_products[-1].click()
        except IndexError:
            pass
    ctr += 1

cookies_per_second = driver.find_element(By.ID, value='cookiesPerSecond')
print(f'cookies {cookies_per_second.text}')