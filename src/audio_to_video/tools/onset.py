import librosa
import numpy as np


class Onset:
    @staticmethod
    def detectOnset(y: np.ndarray, sr: float) -> np.ndarray:
        # logS = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
        # onset_env = librosa.onset.onset_strength(S=logS)
        # onset_peaks = librosa.util.localmax(onset_env)
        return librosa.onset.onset_detect(y=y, backtrack=True, sr=sr)
        # return librosa.util.peak_pick(onset_env, pre_max=2, post_max=2, pre_avg=3, post_avg=5, delta=0.5, wait=10)

    @staticmethod
    def detectOnset2(stft: np.ndarray) -> np.ndarray:
        logS = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
        onset_env = librosa.onset.onset_strength(S=logS)
        # onset_peaks = librosa.util.localmax(onset_env)
        # return librosa.onset.onset_detect(y=y, backtrack=True, sr=sr)
        return librosa.util.peak_pick(
            onset_env,
            pre_max=12,
            post_max=12,
            pre_avg=12,
            post_avg=15,
            delta=2,
            wait=10,
            method="dp_value",
        )
