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
ctr = 0
while True:
    cookie_button.click()
    time.sleep(0.01)    # time.sleep and ctr calculated thru trial-and-error to get 5 seconds.
    if ctr > 120:
        ctr = 0
        unlocked_products = driver.find_elements(By.CSS_SELECTOR, value='.product.unlocked.enabled')
        try:
            unlocked_products[-1].click()
        except IndexError:
            pass
    ctr += 1

# TODO: Stop after 5 minutes and print cookies-per-second.