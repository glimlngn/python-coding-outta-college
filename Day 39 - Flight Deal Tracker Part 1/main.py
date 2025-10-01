#This file will need to use the DataManager, FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
import pandas as pd
import json
from datetime import datetime, timedelta

data_manager = DataManager()
flight_search = FlightSearch()

def get_cheapest_flights_list(sheets_data_df, month_start, month_end, origin_city, duration):
    cheapest_flights_list = []
    for index, row in sheets_data_df.iterrows():

        start_time = datetime.now()

        origin_city = 'MNL'
        destination_city = row['iataCode']
        hits = 0
        total = 0
        days_from_now = month_start*30 # 3 months from now
        departure_date = datetime.now() + timedelta(days=days_from_now)
        flight_list = []

        while days_from_now < month_end*30: # 6 months from now
            print(f'{total+1}. ', end='')
            daywise_flight = flight_search.get_daywise_flight(origin_city, destination_city, departure_date, duration)
            
            if daywise_flight != 'Search timeout or no flights found':
                flight_list.append(daywise_flight)
                hits += 1
                print("O")
            else:
                print("X")

            departure_date += timedelta(days=1)
            days_from_now += 14  # check per week (to reduce API calls)
            total += 1

        cheapest_flight = flight_search.get_cheapest_flight_per_city(flight_list)

        print(f"Score: {hits}/{total}. Hit Rate: {round((hits)/total*100,2)}%")
        print(f"The cheapest flight from {origin_city} to {destination_city} in the next {month_start}-{month_end} months is: ")
        print(cheapest_flight)
        print('------')

        end_time = datetime.now()
        print('Runtime:', round((end_time - start_time).total_seconds(), 0))
        start_time = end_time
        cheapest_flights_list.append(cheapest_flight)

    return cheapest_flights_list

sheets_data = data_manager.get_sheets_data()

sheets_data_df = pd.DataFrame(sheets_data).drop(columns=['id'])
# print(sheet_data_df.to_dict(orient='records'))

for index, row in sheets_data_df.iterrows():
    if row['iataCode'] == "":
        city_code = flight_search.get_city_code(row['city'])
        sheets_data_df.loc[index, 'iataCode'] = city_code # type: ignore

        # WRITE city codes to Google Sheets
        data_manager.add_city_code_to_sheets(index, city_code)

# print(sheets_data_df)

cheapest_flights_list = get_cheapest_flights_list(sheets_data_df, month_start=3, month_end=6, origin_city='MNL', duration=7)

with open("Day 39 - Flight Deal Tracker Part 1/cheapest_flights_list.txt", "w") as txtfile:
    for flight in cheapest_flights_list:
        txtfile.write(str(flight) + "\n")

data_manager.add_flights_to_sheets(cheapest_flights_list, sheets_data_df)