import os
import h5py
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

def check_field(h5, group, field):
    try:
        return h5[group][field][:]
    except KeyError:
        return None

def process_hdf5_file(h5_file):
    try:
        with h5py.File(h5_file, 'r') as h5:
            song_ids = check_field(h5, 'metadata/songs', 'song_id')
            titles = check_field(h5, 'metadata/songs', 'title')
            artist_names = check_field(h5, 'metadata/songs', 'artist_name')
            durations = check_field(h5, 'analysis/songs', 'duration')
            danceabilities = check_field(h5, 'analysis/songs', 'danceability')
            energies = check_field(h5, 'analysis/songs', 'energy')
            tempos = check_field(h5, 'analysis/songs', 'tempo')
            loudnesses = check_field(h5, 'analysis/songs', 'loudness')

            if song_ids is not None:
                for i in range(len(song_ids)):
                    title = titles[i].decode('utf-8') if titles is not None else None
                    artist = artist_names[i].decode('utf-8') if artist_names is not None else None
                    duration = float(durations[i]) if durations is not None else None
                    danceability = float(danceabilities[i]) if danceabilities is not None and not pd.isnull(danceabilities[i]) else None
                    energy = float(energies[i]) if energies is not None and not pd.isnull(energies[i]) else None
                    tempo = float(tempos[i]) if tempos is not None and not pd.isnull(tempos[i]) else None
                    loudness = float(loudnesses[i]) if loudnesses is not None and not pd.isnull(loudnesses[i]) else None

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
                            tempo, loudness, None, None, None, None, None, None, None
                        )
                    )
        conn.commit()
    except Exception as e:
        conn.rollback()

def process_hdf5_directory(root_dir):
    for first_level in os.listdir(root_dir):
        first_level_path = os.path.join(root_dir, first_level)
        
        if os.path.isdir(first_level_path):
            for second_level in os.listdir(first_level_path):
                second_level_path = os.path.join(first_level_path, second_level)
                
                if os.path.isdir(second_level_path):
                    for file in os.listdir(second_level_path):
                        if file.endswith(".h5"):
                            h5_file = os.path.join(second_level_path, file)
                            process_hdf5_file(h5_file)

cur.close()
conn.close()
