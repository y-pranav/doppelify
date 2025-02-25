import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Search for a song (Yellow, for example)
result = sp.search(q="Yellow", type="track", limit=1)
track = result['tracks']['items'][0]

print(f"Track: {track['name']}")
print(f"ID: {track['id']}")

# Get audio features for the track
audio_features = sp.audio_features(track['id'])
for k, v in audio_features[0].items():
    print(k, v)
