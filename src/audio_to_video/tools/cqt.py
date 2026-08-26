import librosa
import numpy as np
import matplotlib.pyplot as plt


class CQT:
    @staticmethod
    def getCQT(y: np.ndarray, sr: float, hop_length: int) -> np.ndarray:
        return np.abs(
            librosa.cqt(
                y,
                sr=sr,
                hop_length=hop_length,
                fmin=librosa.note_to_hz("C0"),
                n_bins=7 * 12,
                bins_per_octave=12,
            )
        )

    @staticmethod
    def exportCQT(cqt: np.ndarray, sr, exportFilename) -> None:
        fig, ax = plt.subplots()
        img = librosa.display.specshow(
            cqt, vscale="dBFS", sr=sr, x_axis="time", y_axis="cqt_note", ax=ax
        )
        ax.set_title("Constant-Q power spectrum")
        librosa.display.colorbar_db(img)

        plt.savefig(exportFilename)
