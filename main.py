import argparse
import os
from dotenv import load_dotenv
from scripts.dataset_creation import process_hdf5_directory
from scripts.knn import find_similar_songs

load_dotenv()

HDF5_DATA_DIR = os.getenv("MSD_DATA_DIR", "data/")

def process_msd():
    process_hdf5_directory(HDF5_DATA_DIR)

def run_knn():
    find_similar_songs(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Doppelify Music Processing Pipeline")
    parser.add_argument("--process_msd", action="store_true")
    parser.add_argument("--run_knn", action="store_true")
    parser.add_argument("--all", action="store_true")

    args = parser.parse_args()

    if args.all:
        process_msd()
        run_knn()
    else:
        if args.process_msd:
            process_msd()
        if args.run_knn:
            run_knn()
