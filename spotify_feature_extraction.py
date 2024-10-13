import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve Spotify API credentials from environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

# Set up Spotify credentials
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Search for a song (Coldplay, for example)
result = sp.search(q="Coldplay", type="track", limit=1)
track = result['tracks']['items'][0]

# Display the track name and its ID
print(f"Track: {track['name']}")
print(f"ID: {track['id']}")

# Get audio features for the track
audio_features = sp.audio_features(track['id'])
for k, v in audio_features[0].items():
    print(k, v)
