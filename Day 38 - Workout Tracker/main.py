from dotenv import load_dotenv
import os
import requests

load_dotenv()

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
GENDER = "male"
WEIGHT = 80
HEIGHT = 170
AGE = 23
EXERCISE_NLP_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

query = input("What exercises did you do today? ")

params = {
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
    "query": query
}

response = requests.post(url=EXERCISE_NLP_ENDPOINT, headers=headers, json=params)
print(response.text)