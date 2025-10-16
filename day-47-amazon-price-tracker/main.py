import requests
import smtplib
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import ast

load_dotenv()

EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
USER_AGENT = os.environ["USER_AGENT"]
ACCEPT_LANGUAGE = os.environ["ACCEPT_LANGUAGE"]
HEADERS = ast.literal_eval(os.environ['HEADERS'])

AMAZON_URL = 'https://www.amazon.com/dp/B075CYMYK6?th=1'

TARGET_PRICE = 120.00

# Web scraping does not work for dynamic web pages that render the final HTML file using JavaScript
# TODO: Change method from Beautiful Soup to Selenium to handle dynamic web page

response = requests.get(AMAZON_URL, headers=HEADERS)
soup = BeautifulSoup(response.content, 'html.parser')

with open('./day-47-amazon-price-tracker/output.txt', mode='w', encoding='utf-8') as file:
    file.write(response.text)

product_name = soup.find(name='span', id='productTitle').getText().split() # type: ignore
product_name = ' '.join(product_name)
print(product_name)
price_symbol = soup.find(name='span', class_='a-price-symbol').getText() # type: ignore
price_whole = soup.find(name='span', class_='a-price-whole').getText() # type: ignore
price_fraction = soup.find(name='span', class_='a-price-fraction').getText() # type: ignore

price_value = float(f'{price_whole}{price_fraction}')
print(price_value)

if price_value < TARGET_PRICE:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL_ADDRESS, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_ADDRESS, 
            to_addrs=EMAIL_ADDRESS, 
            msg=f"Subject:Low price alert on flight deals!\
                  \n\n{product_name}\n{price_symbol}{price_value}\n{AMAZON_URL}".encode('utf-8')
        )