#This file will need to use the DataManager, FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

SHEETS_AUTH_TOKEN = os.environ["SHEETS_AUTH_TOKEN"]
SHEETS_ENDPOINT = os.environ["SHEETS_ENDPOINT"]

AMADEUS_CLIENT_ID = os.environ["AMADEUS_CLIENT_ID"]
AMADEUS_CLIENT_SECRET = os.environ["AMADEUS_CLIENT_SECRET"]
AMADEUS_AUTH_ENDPOINT = os.environ["AMADEUS_AUTH_ENDPOINT"]
AMADEUS_CITY_CODES_ENDPOINT = os.environ["AMADEUS_CITY_CODES_ENDPOINT"]

data_manager = DataManager(SHEETS_AUTH_TOKEN)

flight_search = FlightSearch(AMADEUS_AUTH_ENDPOINT, 
                             AMADEUS_CLIENT_ID,
                             AMADEUS_CLIENT_SECRET)

sheets_data = data_manager.get_sheets_data(SHEETS_ENDPOINT)

sheets_data_df = pd.DataFrame(sheets_data).drop(columns=['id'])
# print(sheet_data_df.to_dict(orient='records'))

for index, row in sheets_data_df.iterrows():
    if row['iataCode'] == "":
        city_code = flight_search.get_city_code(row['city'], AMADEUS_CITY_CODES_ENDPOINT)
        sheets_data_df.at[index, 'iataCode'] = city_code

        # WRITE city codes to Google Sheets
        data_manager.add_city_code_to_sheets(index, city_code, SHEETS_ENDPOINT)

print(sheets_data_df)