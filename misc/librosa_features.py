import librosa
import librosa.display
import numpy as np

# Load an audio file (can be mp3, wav, etc.)
audio_file = 'audio/viva-la-vida.mp3'  # Replace with the path to your audio file
y, sr = librosa.load(audio_file)

# Extract Tempo (BPM)
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
print(f"Tempo: {tempo} BPM")

# Zero-crossing rate
zero_crossings = librosa.feature.zero_crossing_rate(y)
print(f"Zero-Crossing Rate: {np.mean(zero_crossings)}")

# Spectral centroid (brightness of the sound)
spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
print(f"Spectral Centroid: {np.mean(spectral_centroid)}")

# Chroma feature (pitches)
chroma = librosa.feature.chroma_stft(y=y, sr=sr)
print(f"Chroma feature: {np.mean(chroma)}")

# Spectral contrast
spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
print(f"Spectral Contrast: {np.mean(spectral_contrast)}")
