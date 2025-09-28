import requests
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self, auth_token):
        self.auth_header = {'Authorization': f'Bearer {auth_token}'}

    def get_sheets_data(self, endpoint):
        response = requests.get(url=endpoint, headers=self.auth_header)
        data = response.json()
        return data['prices']

    def add_city_code_to_sheets(self, objectid, city_code, endpoint):
        requests.put(url=f"{endpoint}/{objectid+2}", # WRITE per row
                     headers=self.auth_header,
                     json={'price': {'iataCode': city_code}})