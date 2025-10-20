import smtplib
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()

EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
AMAZON_URL = 'https://www.amazon.com/dp/B075CYMYK6?th=1'

TARGET_PRICE = 120.00

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(AMAZON_URL)

response = driver.page_source
with open('./day-47-amazon-price-tracker/output.txt', mode='w', encoding='utf-8') as file:
    file.write(response)

product_name = driver.find_element(By.ID, value='productTitle').text
product_price_symbol = driver.find_element(By.CLASS_NAME, value='a-price-symbol').text
product_price_whole = driver.find_element(By.CLASS_NAME, value='a-price-whole').text
product_price_fraction = driver.find_element(By.CLASS_NAME, value='a-price-fraction').text
product_price = float(f'{product_price_whole}.{product_price_fraction}')

if product_price < TARGET_PRICE:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_ADDRESS, 
            to_addrs=EMAIL_ADDRESS, 
            msg=f"Subject:Low price alert on item!\
                  \n\n{product_name}\n{product_price_symbol}{product_price}\n{AMAZON_URL}".encode('utf-8')
        )
    print('Email sent!')

driver.quit()