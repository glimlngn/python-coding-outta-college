import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import pprint
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pickle

load_dotenv()

# ---
# Scraping the Billboard Hot 100

BILLBOARD_HOT_100_URL = 'https://www.billboard.com/charts/hot-100'
USER_AGENT = os.environ.get('USER_AGENT')
# date = input('Please enter the date when I\'ll get the Hot 100 Billboard chart from (Format: YYYY-MM-DD): ')
date = ''   # Historical Billboard Hot 100 charts are blocked by paywall; defaulting to most recent Hot 100 chart. 
header = {"User-Agent": USER_AGENT}

response = requests.get(url=f'{BILLBOARD_HOT_100_URL}/{date}', headers=header)
soup = BeautifulSoup(response.content, 'html.parser')
song_list_div = soup.find_all(name='div', class_='o-chart-results-list-row-container')

song_list = []
for song_div in song_list_div:
    song_title = song_div.find(name='h3', id='title-of-a-story')
    if song_title:
        song_list.append(song_title.getText().strip())
    else: 
        song_list.append(None)

for i in range(len(song_list)):
    print(f"{i+1}.", song_list[i])

# ---
# Authentication with YouTube Music (YouTube Data API v3)

client_secrets_file = "day-46-youtube-music-playlist/client-secret-file.json"
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"

if os.path.exists("day-46-youtube-music-playlist/CREDENTIALS_PICKLE_FILE"):
    with open("day-46-youtube-music-playlist/CREDENTIALS_PICKLE_FILE", 'rb') as f:
        credentials = pickle.load(f)
else:
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(port=8080)
    with open("day-46-youtube-music-playlist/CREDENTIALS_PICKLE_FILE", 'wb') as f:
        pickle.dump(credentials, f)

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

# SAMPLE: Search for my YouTube videos
request = youtube.search().list(
    part="snippet",
    forMine=True,
    maxResults=10,
    order="date",
    type="video",
)

response = request.execute()
pprint.pp(response)

# ---
# TODO: Create empty playlist

# ---
# TODO: Search Billboard Hot 100 songs and add songs to playlist