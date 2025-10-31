import librosa
import numpy as np

def extract_audio_features_from_array(y, sr):
    y = librosa.util.normalize(y)
    pitch, _ = librosa.piptrack(y=y, sr=sr)
    pitch_mean = float(np.mean(pitch[pitch > 0])) if np.any(pitch > 0) else 0.0
    energy = float(np.mean(y ** 2))
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfccs, axis=1).tolist()
    return {
        "pitch_mean": pitch_mean,
        "energy": energy,
        "tempo": float(tempo),
        "mfcc_mean": mfcc_mean
    }
