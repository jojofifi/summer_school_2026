import librosa
import numpy as np
import matplotlib.pyplot as plt
from tools.onset import Onset

class Note:
    @staticmethod
    def getNotes(cqt, onset, sr, hop_length: int) -> None :
        cqt_times = librosa.times_like(cqt, sr=sr, hop_length=hop_length)
        freqs = librosa.cqt_frequencies(n_bins=len(cqt), fmin=librosa.note_to_hz("C1"))
        onset_hz = []

        # for t in onset:
        #     t_sec = librosa.frames_to_time(t, sr=sr, hop_length=hop_length)
        #     cqt_at_time = Note.getCqtAtTime(cqt, t_sec, sr, hop_length)
        #     idx_max = np.argmax(cqt_at_time)
        #     freq = freqs[idx_max]
        #
        #     print(str(t_sec) + ": " + str(freq))
        #     onset_hz.append(freq)

        t_sec = 56.6
        cqt_at_time = Note.displayCqtSliceNote(cqt, t_sec, sr, hop_length)
        idx_max = np.argmax(cqt_at_time)
        freq = freqs[idx_max]

        print(str(t_sec) + ": " + str(freq))
        onset_hz.append(freq)

    @staticmethod
    def getNotes2(cqt, sound_onset, sr, hop_length: int, n_bins: int, bins_per_octave: int) -> [] :
        onsets_notes = []

        for t in sound_onset:
            t_sec = librosa.frames_to_time(t, sr=sr, hop_length=hop_length) + 0.1
            cqt_slice = Note.getCqtAtTime(cqt, t_sec, sr, hop_length)
            cqt_slice_copy = cqt_slice

            max_values = []
            for i in range(0, 5):
                idx = np.argmax(cqt_slice_copy)
                # if(cqt_slice[idx] >= 1 and idx < librosa.note_to_midi('F4')):
                if(cqt_slice[idx] >= 0):
                    max_values.append(idx + 24)
                cqt_slice_copy[idx] = 0

                if(idx != 83):
                    cqt_slice_copy[idx+1] = 0
                if(idx != 0):
                    cqt_slice_copy[idx-1] = 0

            if (len(max_values) != 0):
                print(str(t_sec) + ": " + librosa.midi_to_note(max_values))
                onsets_notes.append(max_values)

        return onsets_notes


    @staticmethod
    def getCqtAtTime(cqt, t: float, sr: int, hop_length: int) -> np.ndarray:
        cqt_times = librosa.times_like(cqt, sr=sr, hop_length=hop_length)
        col_idx = np.argmin(np.abs(cqt_times - t))
        spectrum_at_t = np.abs(cqt[:, col_idx])

        return spectrum_at_t

    @staticmethod
    def displayCqtSliceHz(cqt, t: float, sr: int, hop_length: int,exportFilename: str = "/home/joseph/Downloads/exportTest.png") -> None:
        # 1. Indice de la colonne correspondant au temps t
        cqt_times = librosa.times_like(cqt, sr=sr, hop_length=hop_length)
        col_idx = np.argmin(np.abs(cqt_times - t))

        # 2. Récupérer l'amplitude à cet instant
        spectrum = np.abs(cqt[:, col_idx])

        # 3. Générer les fréquences directement en Hz
        freqs = librosa.cqt_frequencies(
            n_bins=len(spectrum), fmin=librosa.note_to_hz("C1")
        )

        # 4. Affichage simple (X: Hz, Y: Amplitude)
        plt.figure(figsize=(10, 4))
        plt.plot(freqs, spectrum)
        plt.xlabel("Fréquence (Hz)")
        plt.ylabel("Amplitude")
        plt.title(f"Spectre CQT à t = {t:.2f} s")
        plt.grid(True)

        plt.savefig(exportFilename)

        return spectrum


    @staticmethod
    def displayCqtSliceNote(cqt, t: float, sr: int, hop_length: int,exportFilename: str = "/home/joseph/Downloads/exportTest.png") -> None:
        # 1. Extraire la tranche CQT à l'instant t
        spectrum = Note.getCqtAtTime(cqt, t, sr, hop_length)

        # 2. Générer les fréquences en Hz
        n_bins = len(spectrum)
        freqs = librosa.cqt_frequencies(n_bins=n_bins, fmin=librosa.note_to_hz("C1"))

        # 3. Générer le nom des notes pour chaque bin (ex: ['C1', 'C#1', 'D1', ...])
        note_names = [librosa.hz_to_note(f) for f in freqs]

        # 4. Sélectionner des repères visuels (ex: 1 note toutes les octaves ou tous les 6 demi-tons)
        step = 12  # Affiche une note tous les 12 demi-tons (chaque octave)
        tick_indices = np.arange(0, n_bins, step)
        tick_freqs = freqs[tick_indices]
        tick_labels = [note_names[i] for i in tick_indices]

        # 5. Tracer le graphique
        plt.figure(figsize=(12, 4))
        plt.plot(freqs, spectrum, color="C0", linewidth=1.5)

        # Échelle logarithmique recommandée pour que les notes soient espacées régulièrement
        plt.xscale("log")

        # Remplacer les graduations en Hz par les noms de notes
        plt.xticks(tick_freqs, tick_labels)

        plt.xlabel("Notes musicales")
        plt.ylabel("Amplitude")
        plt.title(f"Spectre CQT à t = {t:.2f} s")
        plt.grid(True, which="both", linestyle="--", alpha=0.5)

        plt.savefig(exportFilename)

        return spectrum

