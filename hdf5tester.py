import os
import h5py

# Function to extract and print data from an HDF5 file
def process_hdf5_file(h5_file):
    try:
        with h5py.File(h5_file, 'r') as h5:
            # Extract song metadata
            song_id = h5['metadata']['songs']['song_id'][0].decode('utf-8')
            title = h5['metadata']['songs']['title'][0].decode('utf-8')
            artist_name = h5['metadata']['songs']['artist_name'][0].decode('utf-8')
            duration = h5['analysis']['songs']['duration'][0]

            # Print extracted data for testing
            print(f"File: {h5_file}")
            print(f"Song ID: {song_id}")
            print(f"Title: {title}")
            print(f"Artist Name: {artist_name}")
            print(f"Duration: {duration} seconds")
            print("-" * 40)

    except Exception as e:
        print(f"Error processing file {h5_file}: {e}")

# Root directory where your HDF5 files are located
root_dir = '/home/ypranav/Desktop/MillionSongSubset/A'  # Path to the top-level 'A' directory

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
