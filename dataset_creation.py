import os
import h5py
import psycopg2
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env
load_dotenv()

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="doppelify",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

# Function to check if a field exists in HDF5
def check_field(h5, group, field):
    try:
        return h5[group][field][:]  # Return the data if field exists
    except KeyError:
        print(f"Field {field} does not appear in this file.")
        return None  # Return None if the field is missing

# Function to extract features from HDF5 file and insert into PostgreSQL
def process_hdf5_file(h5_file):
    try:
        with h5py.File(h5_file, 'r') as h5:
            # Extract song metadata
            song_ids = check_field(h5, 'metadata/songs', 'song_id')
            titles = check_field(h5, 'metadata/songs', 'title')
            artist_names = check_field(h5, 'metadata/songs', 'artist_name')
            durations = check_field(h5, 'analysis/songs', 'duration')
            danceabilities = check_field(h5, 'analysis/songs', 'danceability')
            energies = check_field(h5, 'analysis/songs', 'energy')
            tempos = check_field(h5, 'analysis/songs', 'tempo')
            loudnesses = check_field(h5, 'analysis/songs', 'loudness')

            # Fields will remain empty if they are not present in the HDF5 file
            acousticness = None
            instrumentalness = None
            liveness = None
            mode = None
            key = None
            time_signature = None
            valence = None  # No valence field in MSD, left as None

            # If metadata exists, proceed to process each song
            if song_ids is not None:
                for i in range(len(song_ids)):
                    title = titles[i].decode('utf-8') if titles is not None else None
                    artist = artist_names[i].decode('utf-8') if artist_names is not None else None
                    duration = float(durations[i]) if durations is not None else None
                    danceability = float(danceabilities[i]) if danceabilities is not None and not pd.isnull(danceabilities[i]) else None
                    energy = float(energies[i]) if energies is not None and not pd.isnull(energies[i]) else None
                    tempo = float(tempos[i]) if tempos is not None and not pd.isnull(tempos[i]) else None
                    loudness = float(loudnesses[i]) if loudnesses is not None and not pd.isnull(loudnesses[i]) else None

                    # Insert or update the song features in PostgreSQL
                    cur.execute("""
                        INSERT INTO songs (msd_song_id, title, artist, duration, danceability, energy, tempo, loudness, valence, acousticness, instrumentalness, liveness, mode, key, time_signature)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (msd_song_id) 
                        DO UPDATE SET
                        danceability = EXCLUDED.danceability,
                        energy = EXCLUDED.energy,
                        acousticness = EXCLUDED.acousticness,
                        instrumentalness = EXCLUDED.instrumentalness,
                        liveness = EXCLUDED.liveness,
                        mode = EXCLUDED.mode,
                        key = EXCLUDED.key,
                        time_signature = EXCLUDED.time_signature,
                        valence = EXCLUDED.valence;
                        """,
                        (
                            song_ids[i].decode('utf-8'), title, artist, duration, danceability, energy,
                            tempo, loudness, valence, acousticness, instrumentalness, liveness, mode, key, time_signature
                        )
                    )
        
        # Commit the transaction after successfully processing the HDF5 file
        conn.commit()

    except Exception as e:
        # Rollback the transaction if any error occurs
        conn.rollback()
        print(f"Error processing file {h5_file}: {e}")

# Root directory where your HDF5 files are located
root_dir = '/home/ypranav/Desktop/MillionSongSubset/A'

# Iterate through the 3 levels of directories and find HDF5 files
for first_level in os.listdir(root_dir):
    first_level_path = os.path.join(root_dir, first_level)
    
    if os.path.isdir(first_level_path):  # Check if it's a directory
        for second_level in os.listdir(first_level_path):
            second_level_path = os.path.join(first_level_path, second_level)
            
            if os.path.isdir(second_level_path):  # Check if it's a directory
                for file in os.listdir(second_level_path):
                    if file.endswith(".h5"):  # Only process HDF5 files
                        h5_file = os.path.join(second_level_path, file)
                        process_hdf5_file(h5_file)  # Process each HDF5 file

# Close the connection to PostgreSQL
cur.close()
conn.close()
