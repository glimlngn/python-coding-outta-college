import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import pprint
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pickle
from datetime import datetime as dt
import time

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
    artist = song_title.find_next_sibling('span') # type: ignore
    if song_title and artist:
        song_list.append({
            'song_title':song_title.getText().strip(),
            'artist': artist.getText().strip()})
    else: 
        song_list.append({
            'song_title': None,
            'artist': None
        })

for i in range(len(song_list)):
    print(f"{i+1}.", song_list[i])

# ---
# Authentication with YouTube Music (YouTube Data API v3)

client_secrets_file = "day-46-youtube-music-playlist/client-secret-file.json"
scopes = ['https://www.googleapis.com/auth/youtube']
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

# Create a playlist
# TODO: check if there is an existing playlist with the same date, and skip playlist creation
# if date == '':
#     date = dt.now()

# request = youtube.playlists().insert(
#     part="snippet,status",
#     body={
#         "snippet": {
#         "title": f"{dt.strftime(dt.now(), '%Y-%m-%d')} Billboard Hot 100",
#         "description": "Made using blood, sweat, tears, and YouTube Data API v3.",
#         "defaultLanguage": "en"
#         },
#         "status": {
#         "privacyStatus": "public"
#         }
#     }
# )
# response = request.execute()
# pprint.pp(response)

# Search for a YouTube video and add to playlist
for song in song_list[:15]: # Top 15 songs for now
    song_search_response = youtube.search().list(
        part="snippet",
        maxResults=1,
        type='video',
        q=f"{song['song_title']} - {song['artist']}"
    ).execute()
    video_id = song_search_response['items'][0]['id']['videoId']

    # pprint.pp(song_search_response)

    add_to_playlist_response = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
            "playlistId": 'PL4vB_Nnj9gxJzDK3NmK0uUj1bhaYFEaIp',
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
                }
            }
        }
    ).execute()
    time.sleep(5)
    print(f'Added {song_search_response['items'][0]['snippet']['title']} to the playlist')
