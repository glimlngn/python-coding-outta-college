from dotenv import load_dotenv
import os

load_dotenv()

SHEETS_ENDPOINT = os.environ["SHEETS_ENDPOINT"]
SHEETS_AUTH_TOKEN = os.environ["SHEETS_AUTH_TOKEN"]

import requests
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.auth_header = {'Authorization': f'Bearer {SHEETS_AUTH_TOKEN}'}

    def get_sheets_data(self):
        response = requests.get(url=SHEETS_ENDPOINT, headers=self.auth_header)
        data = response.json()
        return data['prices']

    def add_city_code_to_sheets(self, objectid, city_code):
        requests.put(url=f"{SHEETS_ENDPOINT}/{objectid+2}", # WRITE per row
                     headers=self.auth_header,
                     json={'price': {'iataCode': city_code}})