import librosa
import numpy as np

class STFT:
    @staticmethod
    def getSTFT(y: np.ndarray) -> np.ndarray :
        return librosa.stft(y)
