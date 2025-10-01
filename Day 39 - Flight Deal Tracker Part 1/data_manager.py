from dotenv import load_dotenv
import os

load_dotenv()

from notification_manager import NotificationManager
notification_manager = NotificationManager()

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
        
    def add_flights_to_sheets(self, cheapest_flights_list, sheets_data_df):
        objectid = 0
        for index, row in sheets_data_df.iterrows():
            if cheapest_flights_list[index] != {}:
                flight_price = cheapest_flights_list[index]['price']
                departure_date = cheapest_flights_list[index]['departureDate']
                return_date = cheapest_flights_list[index]['returnDate']
                airline = cheapest_flights_list[index]['airline']
                if cheapest_flights_list[index]['price'] < row['lowestPrice']:    # WRITE cheapest flight price to Google Sheets
                    notification_manager.send_message(cheapest_flights_list[index])
                    requests.put(url=f"{SHEETS_ENDPOINT}/{objectid+2}", # WRITE per row
                                 headers=self.auth_header,
                                 json={'price': {'lowestPrice': flight_price,
                                                 'departureDate': departure_date,
                                                 'returnDate': return_date,
                                                 'airline': airline
                                                 }})
            objectid += 1
        