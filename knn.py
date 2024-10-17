import psycopg2
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Connect to the PostgreSQL database and fetch the song data
conn = psycopg2.connect(
    host="localhost",
    database="doppelify",
    user="postgres",
    password="postgres"
)

# Query to fetch tempo, loudness, and song title
query = """
    SELECT title, artist, tempo, loudness
    FROM songs
    WHERE tempo IS NOT NULL AND loudness IS NOT NULL
    AND tempo != 0 AND loudness != 0;
"""

# Load data into a pandas DataFrame
df = pd.read_sql(query, conn)

# Close the database connection
conn.close()

# Extract the song titles (we will use this later to display song names)
song_titles = df['title']
song_artists = df['artist']

# Drop the song titles column from the features DataFrame
df_features = df.drop(columns=['title', 'artist'])

# Normalize the features using StandardScaler
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df_features)

# Train the KNN model
knn = NearestNeighbors(n_neighbors=5, algorithm='auto')
knn.fit(scaled_features)

# Define a function to get similar songs by index
def find_similar_songs(song_index):
    distances, indices = knn.kneighbors([scaled_features[song_index]])
    return indices[0], distances[0]

# Example: Find 5 songs similar to the first song in the dataset
similar_songs_indices, distances = find_similar_songs(0)

# Display the names of the similar songs
print(f"Song: {song_titles.iloc[0]}")
for idx, dist in zip(similar_songs_indices, distances):
    print(f"Similar Song: {song_titles.iloc[idx]}, - Artist: {song_artists[idx]} Distance: {dist}")
