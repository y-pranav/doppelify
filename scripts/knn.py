import os
import psycopg2
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

query = """
    SELECT title, artist, tempo, loudness
    FROM songs
    WHERE tempo IS NOT NULL AND loudness IS NOT NULL
    AND tempo != 0 AND loudness != 0;
"""

df = pd.read_sql(query, conn)  # Fix for SQLAlchemy warning
conn.close()

if df.empty:
    print("No valid songs found in the database.")
    exit()

song_titles = df['title']
song_artists = df['artist']
df_features = df.drop(columns=['title', 'artist'])

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df_features)

knn = NearestNeighbors(n_neighbors=5, algorithm='auto')
knn.fit(scaled_features)

def find_similar_songs(song_name=None):
    if song_name:
        if song_name not in song_titles.values:
            print(f"Song '{song_name}' not found in dataset. Searching using first available song.")
            song_index = 0
        else:
            song_index = song_titles[song_titles == song_name].index[0]
    else:
        song_index = 0  # Default to the first song if no name is provided

    distances, indices = knn.kneighbors([scaled_features[song_index]])
    print(f"Finding songs similar to: {song_titles.iloc[song_index]}")

    for idx, dist in zip(indices[0], distances[0]):
        print(f"Similar Song: {song_titles.iloc[idx]}, Artist: {song_artists.iloc[idx]}, Distance: {dist}")
