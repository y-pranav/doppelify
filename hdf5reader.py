import h5py

# Open the HDF5 file
h5_file = 'msd_summary_file.h5'
with h5py.File(h5_file, 'r') as h5:
    # Access the 'metadata/songs' dataset
    metadata_songs = h5['metadata/songs']

    # Example: Print the first 5 song titles
    titles = metadata_songs['title'][:5]  # Access the 'title' field
    print("First 5 Song Titles:")
    for title in titles:
        print(title.decode('utf-8'))  # Decode from bytes to string if necessary

    # Example: Print the first 5 artist names
    artist_names = metadata_songs['artist_name'][:5]
    print("\nFirst 5 Artist Names:")
    for artist in artist_names:
        print(artist.decode('utf-8'))

    # Access the 'analysis/songs' dataset and print the first 5 tempo values
    analysis_songs = h5['analysis/songs']
    tempos = analysis_songs['tempo'][:5]
    print("\nFirst 5 Tempo Values:")
    print(tempos)

    # Access the 'musicbrainz/songs' dataset and print the first 5 years
    musicbrainz_songs = h5['musicbrainz/songs']
    years = musicbrainz_songs['year'][:5]
    print("\nFirst 5 Years:")
    print(years)
