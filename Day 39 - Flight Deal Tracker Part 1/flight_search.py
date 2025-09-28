import requests

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self, auth_endpoint, client_id, client_secret):
        self.amadeus_auth_token = requests.post(url=auth_endpoint, 
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}, 
                    data=f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
                    ).json()['access_token']

    def get_city_code(self, city, city_codes_endpoint):
        city_code = requests.get(url=city_codes_endpoint, 
                   headers={'Authorization': f'Bearer {self.amadeus_auth_token}'}, 
                   params={'keyword': city, 'max': 1}
                   ).json()['data'][0]['iataCode']
        return city_code