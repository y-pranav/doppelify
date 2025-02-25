# **Doppelify**  
A music processing pipeline that extracts audio features from the **Million Song Dataset (MSD)** and applies **K-Nearest Neighbors (KNN)** to find similar songs.  

The extracted metadata includes features like **tempo, loudness, energy, and more**. The MSD subset contains **limited available features**, but additional audio properties can be fetched from **Spotify API** or generated using **Librosa** for a more comprehensive similarity analysis.  

### **Prediction Accuracy**  
The accuracy of **song similarity recommendations** improves with **more data** and **more extracted features**. A larger dataset with feature-rich songs leads to **better and more meaningful recommendations**.

---

## **1. Setup Instructions**

### **1.1 Install Dependencies**
```bash
pip install -r requirements.txt
```

---

### **1.2 Download the Million Song Dataset (MSD)**
[Million Song Dataset](http://millionsongdataset.com/)  

Download the **subset** (~2GB) from:  
[Million Song Dataset Subset (HDF5)](http://labrosa.ee.columbia.edu/~dpwe/tmp/millionsongsubset.tar.gz)  

Extract the files into `data/` so your structure looks like:

```
📂 doppelify
│── 📂 data/         # Contains MSD HDF5 files
│── 📂 scripts/
│── 📂 misc/         # Additional scripts for further feature extraction (optional)
```

The **MSD subset contains limited fields**, with many missing values in certain features. To improve **song similarity analysis**, more features can be:
- **Fetched from Spotify API** (e.g., danceability, valence, acousticness)
- **Generated using Librosa** (e.g., tempo, spectral contrast, zero-crossing rate)

These additional scripts are available in the **misc/** folder.

---

### **1.3 Configure Environment Variables**
Create a `.env` file in the root directory with:

```ini
# PostgreSQL Configuration
DB_HOST=localhost
DB_NAME=doppelify
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=3002  # Change if using a different port

# Path to MSD Data
MSD_DATA_DIR=data/
```

---

## **2. Running the Mandatory Steps**

### **2.1 Process MSD HDF5 Files**
```bash
python main.py --process_msd
```
Extracts **tempo, loudness, energy, and duration** from available data in the MSD subset and stores them in the database.

---

### **2.2 Run KNN Similarity Matching**
Find similar songs to a **specific song**:
```bash
python main.py --run_knn --song "Imagine"
```

Find similar songs using the **first available song** in the dataset:
```bash
python main.py --run_knn
```

---

## **3. Running the Full Pipeline**
```bash
python main.py --all
```
Runs the entire process—extracts features from MSD and runs KNN.

---

## **4. How Similar Song Search Works**
Doppelify uses **K-Nearest Neighbors (KNN)** to find songs that are similar based on extracted **tempo and loudness**.  

**The more features available (danceability, energy, valence, etc.), the better the results.**

### **Expected Input**
You provide a **song title** to find similar tracks:

```bash
python main.py --run_knn --song "Imagine"
```

### **Expected Output**
```bash
Finding songs similar to: Imagine

Similar Song: Bohemian Rhapsody, Artist: Queen, Distance: 0.2
Similar Song: Billie Jean, Artist: Michael Jackson, Distance: 0.5
Similar Song: Smells Like Teen Spirit, Artist: Nirvana, Distance: 0.6
```

If the song isn't found in the dataset, it defaults to searching using the first available song.

---

## **5. Code Structure**
```
📂 doppelify
│── 📂 data/         # Contains MSD HDF5 files
│── 📂 scripts/
│   │── dataset_creation.py    # Parses MSD and inserts into PostgreSQL
│   │── knn.py                 # Implements song similarity using KNN
│── 📂 misc/         # Additional scripts for further feature extraction (optional)
│   │── hdf5reader.py          # Reads HDF5 files
│   │── hdf5tester.py          # Tests HDF5 reading functionality
│   │── librosa_features.py    # Extracts features from an audio file
|   |── spotify_features.py    # Spotify API to extract features of a song
│   │── hdf5tester.py          # Tests HDF5 reading functionality
│── main.py                    # Entry point for execution
│── .env                        # Stores database config
│── requirements.txt            # Dependencies
│── README.md                   # Documentation
```
---

## **6. Future Enhancements**
- Expand similarity matching with more **audio features**.
- Improve recommendations using **Neural Networks**.
- Additional features can be included using **Librosa (audio analysis)** and **Spotify API (track metadata and features)** for better KNN classification.

---

## **7. Acknowledgments**
- **Million Song Dataset** – structured music data.  
- **Spotify API** – additional audio analysis.  
- **Librosa** – feature extraction from local audio.
