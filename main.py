import os
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET= os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SPOTIFY_DISPLAY_NAME = os.getenv("SPOTIFY_DISPLAY_NAME")

sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        scope = "playlist-modify-private",
        redirect_uri = REDIRECT_URI,
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        show_dialog = True,
        cache_path = "token.txt",
        username = SPOTIFY_DISPLAY_NAME 
    )
)

user_id = sp.current_user()["id"]
song_names = [song.getText().strip() for song in song_names_spans]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
