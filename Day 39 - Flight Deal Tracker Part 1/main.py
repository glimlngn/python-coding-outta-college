#This file will need to use the DataManager, FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
import pandas as pd
import json
from datetime import datetime, timedelta

data_manager = DataManager()
flight_search = FlightSearch()

sheets_data = data_manager.get_sheets_data()

sheets_data_df = pd.DataFrame(sheets_data).drop(columns=['id'])
# print(sheet_data_df.to_dict(orient='records'))

for index, row in sheets_data_df.iterrows():
    if row['iataCode'] == "":
        city_code = flight_search.get_city_code(row['city'])
        sheets_data_df.at[index, 'iataCode'] = city_code

        # WRITE city codes to Google Sheets
        data_manager.add_city_code_to_sheets(index, city_code)

# print(sheets_data_df)

# TODO: Put in flight_data.py
origin_city = 'MNL'
destination_city = 'HAN'
duration = 7 # days
departure_date = datetime.now() + timedelta(days=3*30) # 3 months from now
days_from_now = 0

grand_cheapest_price = 100000 # PHP
grand_cheapest_flight = {}

while days_from_now < 5*30: # 5 months from now
    daywise_flight = flight_search.get_daywise_cheapest_flight(origin_city, destination_city, departure_date, duration)
    
    print(daywise_flight)
    
    # TODO: Load data before comparing prices
    if daywise_flight != 'Search timeout or no flights found':
        if daywise_flight['price'] < grand_cheapest_price:
            grand_cheapest_price = daywise_flight['price']
            grand_cheapest_flight = daywise_flight

    departure_date += timedelta(days=1)
    days_from_now += 1  # check per day

print('---')
print(f"The cheapest flight from {origin_city} to {destination_city} in the next 3-5 months is: ")
print(grand_cheapest_flight)

# TODO: For flight_data.py, have a function to return cheapest prices of ALL cities