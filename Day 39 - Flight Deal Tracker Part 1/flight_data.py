class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        pass

    def get_cheapest_flight_per_city(self, flight_list): # give list of dicts of flight data
        cheapest_price = 100000 # PHP
        cheapest_flight = {}
        for flight in flight_list:
            if flight['price'] < cheapest_price:
                cheapest_price = flight['price']
                cheapest_flight = flight
        return cheapest_flight