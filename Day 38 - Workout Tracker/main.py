from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime

load_dotenv()

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
EXERCISE_NLP_ENDPOINT = os.environ["EXERCISE_NLP_ENDPOINT"]
SHEETS_ENDPOINT = os.environ["SHEETS_ENDPOINT"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]

GENDER = "male"
WEIGHT = 80
HEIGHT = 170
AGE = 23
DATE_NOW = datetime.now().strftime("%m/%d/%Y")
TIME_NOW = datetime.now().strftime("%X")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

query = input("What exercises did you do today? ")

exercise_nlp_params = {
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
    "query": query
}

exercise_nlp_response = requests.post(url=EXERCISE_NLP_ENDPOINT, json=exercise_nlp_params, headers=headers)
exercise = exercise_nlp_response.json()["exercises"][0]["name"]
duration = exercise_nlp_response.json()["exercises"][0]["duration_min"]
calories = exercise_nlp_response.json()["exercises"][0]["nf_calories"]
# print(json.dumps(exercise_nlp_response.json(), indent=4))

sheets_nlp_params = {
    "workout": {
        "date": DATE_NOW,
        "time": TIME_NOW,
        "exercise": exercise.title(),
        "duration": duration,
        "calories": calories
  }
}

print(json.dumps(sheets_nlp_params, indent=4))
sheet_response = requests.post(url=SHEETS_ENDPOINT, json=sheets_nlp_params, auth=(USER, PASSWORD))
# print(sheet_response)