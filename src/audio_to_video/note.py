import librosa
import numpy as np
import matplotlib.pyplot as plt

from tools.onset import Onset

class Note:
    def __init__(self, note_midi: int, start_time: float, end_time: float) -> None :
        self.note_midi = note_midi
        self.start_time = start_time
        self.end_time = end_time

    @staticmethod
    def getNotes(cqt, sound_onset, sr, hop_length: int, n_bins: int, bins_per_octave: int) -> [] :
        notes = []

        for t in sound_onset:
            t_sec = librosa.frames_to_time(t, sr=sr, hop_length=hop_length) + 0.1
            cqt_slice = Note.getCqtAtTime(cqt, t_sec, sr, hop_length)
            cqt_slice_copy = cqt_slice

            max_values = []
            for i in range(0, 5):
                idx = np.argmax(cqt_slice_copy)
                # if(cqt_slice[idx] >= 1 and idx < librosa.note_to_midi('F4')):
                if(cqt_slice[idx]):
                    max_values.append(idx)
                cqt_slice_copy[idx] = 0

                if(idx != 83):
                    cqt_slice_copy[idx+1] = 0
                if(idx != 0):
                    cqt_slice_copy[idx-1] = 0

            clean_notes = Note.removeHarmony(cqt_slice, max_values, t_sec)
            for note in clean_notes :
                end_time = Note.getNoteEnd(cqt, sr, hop_length, t_sec, note)
                notes.append(Note(Note.ajustOctave(note, 1), t_sec - 0.12, end_time))

        return notes

    @staticmethod
    def getNoteEnd(cqt, sr, hop_length: int, time, idx):
        endFound = False
        isGoingDown = False
        count = 0
        highest = 0
        frame = librosa.time_to_frames(time, sr=sr, hop_length=hop_length)

        while(not endFound):
            cqt_slice = Note.getCqtAtFrame(cqt, (frame+count))
            if(cqt_slice[idx] > highest):
                highest = cqt_slice[idx]
            else:
                isGoingDown = True

            if(isGoingDown):
                percentDif = cqt_slice[idx] / highest
                if(percentDif<0.2):
                    endFound = True
            count += 1

        return librosa.frames_to_time(frame + count, sr=sr, hop_length=hop_length)

    def ajustOctave(note, nbr_octave: int) -> [] :
        return note + (nbr_octave * 12)

    @staticmethod
    def removeHarmony(cqt_slice, notes, t_sec) -> [] :
        notes.sort()
        if (len(notes) < 1):
            return []

        final_notes = [notes[0]]

        for note in notes :
            isNewNote = True
            for final_note in final_notes :
                for i in range(1, len(notes) + 8) :
                    harmony = round(librosa.hz_to_midi(librosa.midi_to_hz(final_note) * i))

                    if (note == harmony) :
                        isNewNote = False
            if (isNewNote) :
                final_notes.append(note)

        return final_notes

    @staticmethod
    def getCqtAtTime(cqt, t: float, sr: int, hop_length: int) -> np.ndarray:
        cqt_times = librosa.times_like(cqt, sr=sr, hop_length=hop_length)
        col_idx = np.argmin(np.abs(cqt_times - t))
        spectrum_at_t = np.abs(cqt[:, col_idx])
        return spectrum_at_t

    @staticmethod
    def getCqtAtFrame(cqt, col_idx):
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

