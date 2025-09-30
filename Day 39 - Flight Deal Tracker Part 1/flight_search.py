from dotenv import load_dotenv
import os
import json

load_dotenv()

AMADEUS_CLIENT_ID = os.environ["AMADEUS_CLIENT_ID"]
AMADEUS_CLIENT_SECRET = os.environ["AMADEUS_CLIENT_SECRET"]
AMADEUS_AUTH_ENDPOINT = os.environ["AMADEUS_AUTH_ENDPOINT"]

AMADEUS_CITY_CODES_ENDPOINT = os.environ["AMADEUS_CITY_CODES_ENDPOINT"]
AMADEUS_FLIGHT_OFFERS_ENDPOINT = os.environ["AMADEUS_FLIGHT_OFFERS_ENDPOINT"]

import requests
from datetime import datetime, timedelta

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.amadeus_auth_token = requests.post(url=AMADEUS_AUTH_ENDPOINT, 
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}, 
                    data=f'grant_type=client_credentials&client_id={AMADEUS_CLIENT_ID}&client_secret={AMADEUS_CLIENT_SECRET}'
                    ).json()['access_token']

    def get_city_code(self, city):
        city_code = requests.get(url=AMADEUS_CITY_CODES_ENDPOINT, 
                   headers={'Authorization': f'Bearer {self.amadeus_auth_token}'}, 
                   params={'keyword': city, 'max': 1}
                   ).json()['data'][0]['iataCode']
        return city_code
    
    def get_daywise_cheapest_flight(self, origin_city, destination_city, departure_date, duration):
        return_date = (departure_date + timedelta(days=duration)).strftime('%Y-%m-%d')
        departure_date = departure_date.strftime('%Y-%m-%d')
        
        cheapest_price = 100000 # PHP
        airline = ""
        airline_code = ""
        origin_airport = ""
        destination_airport = ""
        flight_offers = {"data": []}

        ctr = 0
        while flight_offers["data"] == [] and ctr < 3:
            flight_offers = requests.get(url=AMADEUS_FLIGHT_OFFERS_ENDPOINT, 
                                        headers={'Authorization': f'Bearer {self.amadeus_auth_token}'}, 
                                        params={'originLocationCode': origin_city, 
                                                'destinationLocationCode': destination_city,
                                                'departureDate': departure_date,
                                                'returnDate': return_date,
                                                'adults': 1, 
                                                'nonStop': 'true',
                                                'currencyCode': 'PHP',
                                                'max': 5
                                                }
                                                ).json()
            ctr += 1
        
        # with open("Day 39 - Flight Deal Tracker Part 1/output.txt", "w") as txtfile:
        #     txtfile.write(json.dumps(flight_offers, indent=4))

        if flight_offers["data"] == []:
            print(f"{departure_date} to {return_date}: ", end="")
            return 'Search timeout or no flights found'

        else:
            for offer in flight_offers["data"]:
                offer_price = float(offer["price"]["grandTotal"])
                if offer_price < cheapest_price:
                    cheapest_price = offer_price
                    airline_code = offer['itineraries'][0]['segments'][0]['carrierCode']
                    airline = flight_offers['dictionaries']['carriers'][airline_code] # type: ignore
                    origin_airport = offer['itineraries'][0]['segments'][0]['departure']['iataCode']
                    destination_airport = offer['itineraries'][0]['segments'][0]['arrival']['iataCode']

        cheapest_flight = {
            "price": cheapest_price,
            "currencyCode": "PHP",
            "airline": airline,
            "originAirport": origin_airport,
            "destinationAirport": destination_airport,
            "departureDate": departure_date,
            "returnDate": return_date
        }

        return cheapest_flight