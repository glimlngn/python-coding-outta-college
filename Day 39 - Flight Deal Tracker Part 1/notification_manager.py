from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_FROM_NUMBER = os.environ["TWILIO_FROM_NUMBER"]
TWILIO_TO_NUMBER = os.environ["TWILIO_TO_NUMBER"]

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_message(self, flight):
        currency_code = flight['currencyCode']
        price = flight['price']
        origin_airport = flight['originAirport']
        destination_airport = flight['destinationAirport']
        airline = flight['airline']
        departure_date = flight['departureDate']
        return_date = flight['returnDate']
        message_body =  f"Low price alert! Only {currency_code}{price} to fly \
            from {origin_airport} to {destination_airport} \
            through {airline} from {departure_date} to {return_date}."

        message = self.client.messages.create(
            from_=TWILIO_FROM_NUMBER,
            body = message_body,
            to=TWILIO_TO_NUMBER
        )
        
