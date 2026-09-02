import librosa
import matplotlib.pyplot as plt
import numpy as np


class Note:
    def __init__(self, note_midi: int, start_time: float, end_time: float, instrument: str) -> None:
        self.note_midi = note_midi
        self.start_time = start_time
        self.end_time = end_time
        self.instrument = instrument

    @staticmethod
    def getNotes(cqt, sound_onset, sr, hop_length: int, n_bins: int, bins_per_octave: int):
        notes = []

        for t in sound_onset:
            t_sec = librosa.frames_to_time(t, sr=sr, hop_length=hop_length) + 0.1
            cqt_slice = Note.getCqtAtTime(cqt, t_sec, sr, hop_length)

            max_values = Note.getMaxPowerNoteAtTime(7, cqt_slice)

            clean_notes = Note.removeAlreadyPlayedNotes(notes, Note.removeHarmony(cqt_slice, max_values, t_sec), t_sec)

            for note in clean_notes:
                end_time = Note.getNoteEnd(cqt, sr, hop_length, t_sec, note)
                instrument = Note.getInstrument(cqt, note, t_sec - 0.12, end_time, cqt_slice, sr, hop_length)
                notes.append(Note(Note.ajustOctave(note, 1), t_sec - 0.12, end_time, instrument))

        return notes

    @staticmethod
    def getMaxPowerNoteAtTime(nbr_max_power_note, cqt_slice):
        cqt_slice_copy = cqt_slice.copy()
        max_values = []
        for i in range(0, nbr_max_power_note):
            idx = np.argmax(cqt_slice_copy)
            if cqt_slice[idx] > max(cqt_slice) * 0.05:
                max_values.append(idx)
            cqt_slice_copy[idx] = 0

            if idx != 83:
                cqt_slice_copy[idx + 1] = 0
            if idx != 0:
                cqt_slice_copy[idx - 1] = 0
        return max_values

    @staticmethod
    def removeAlreadyPlayedNotes(old_notes, new_notes, start_time):
        real_new_notes = []
        for new_note in new_notes:
            is_new_note = True
            for old_note in old_notes:
                if old_note.note_midi == new_note and old_note.end_time > start_time:
                    is_new_note = False
            if is_new_note:
                real_new_notes.append(new_note)

        return real_new_notes

    @staticmethod
    def getInstrument(cqt, note, start_time, end_time, cqt_slice, sr, hop_length):
        piano_probability = 0
        trumpet_probability = 0
        frequency_ratio = Note.getInstrumentByHarmonicRatio(cqt_slice, note, 0.6)
        power_stability = Note.getInstrumentByPowerStability(cqt, note, start_time, end_time, sr, hop_length)
        max_power = Note.getInstrumentByMaxPower(cqt_slice, note, 1.1)

        if frequency_ratio == "piano":
            piano_probability += 1
        if frequency_ratio == "trumpet":
            trumpet_probability += 1
        if power_stability == "piano":
            piano_probability += 1
        if power_stability == "trumpet":
            trumpet_probability += 1
        if max_power == "piano":
            piano_probability += 1
        if max_power == "trumpet":
            trumpet_probability += 1

        instrument = "piano"
        if trumpet_probability > piano_probability:
            instrument = "trumpet"

        return instrument

    @staticmethod
    def getInstrumentByMaxPower(cqt_slice, note, max_trumpet_power):
        if cqt_slice[note] < max_trumpet_power:
            return "trumpet"
        return "piano"

    @staticmethod
    def getInstrumentByPowerStability(cqt, note, start_time, end_time, sr, hop_length):
        note_powers = []
        start_time_frame = librosa.time_to_frames(start_time, sr=sr, hop_length=hop_length)
        end_time_frame = librosa.time_to_frames(start_time + 0.5, sr=sr, hop_length=hop_length)
        if end_time_frame >= cqt.shape[1]:
            end_time_frame = cqt.shape[1]

        if end_time - start_time < 0.5:
            end_time_frame = librosa.time_to_frames(end_time, sr=sr, hop_length=hop_length)

        for frame in range(start_time_frame, end_time_frame):
            cqt_slice = Note.getCqtAtFrame(cqt, frame)
            note_powers.append(cqt_slice[note])

        note_evolution_powers = np.gradient(note_powers)

        start_note_intensity = max(note_evolution_powers)

        instrument = "piano"
        if start_note_intensity < 0.5:
            instrument = "trumpet"

        return instrument

    @staticmethod
    def getInstrumentByFrequencyHight(note, max_note_for_piano):
        if note > librosa.note_to_midi(max_note_for_piano):
            return "trumpet"
        return "piano"

    @staticmethod
    def getInstrumentByHarmonicRatio(cqt_slice, note, min_ratio_for_piano):
        instrument = "piano"
        harmonies_notes_power = []
        harmonies_indices = []
        harmonies_labels = []

        for i in range(1, 7):
            harmony_hz = librosa.midi_to_hz(note) * i
            if librosa.hz_to_midi(harmony_hz) < 84:
                harmony_note = int(librosa.hz_to_midi(harmony_hz))
                harmonies_indices.append(harmony_note)
                harmonies_notes_power.append(cqt_slice[harmony_note])
                harmonies_labels.append(f"H{i}\n({librosa.midi_to_note(harmony_note)})")

        if len(harmonies_notes_power) == 1:
            instrument = "trumpet"
            ratio = 0
        else:
            split_idx = len(harmonies_notes_power) // 2
            low_frequencies_power = harmonies_notes_power[:split_idx]
            hight_frequencies_power = harmonies_notes_power[-split_idx:]

            total_low_frequencies_power = sum(low_frequencies_power)
            total_hight_frequencies_power = sum(hight_frequencies_power)
            ratio = total_low_frequencies_power / (total_low_frequencies_power + total_hight_frequencies_power)

            if ratio < min_ratio_for_piano:
                instrument = "trumpet"

        return instrument

    @staticmethod
    def getNoteEnd(cqt, sr, hop_length: int, time, note):
        endFound = False
        isGoingDown = False
        count = 0
        highest = 0
        frame = librosa.time_to_frames(time, sr=sr, hop_length=hop_length)

        while not endFound:
            cqt_slice = Note.getCqtAtFrame(cqt, (frame + count))
            if cqt_slice[note] > highest:
                highest = cqt_slice[note]
            else:
                isGoingDown = True

            if isGoingDown:
                percentDif = cqt_slice[note] / highest
                # new_notes = Note.getMaxPowerNoteAtTime(8, cqt_slice)
                # for new_note in new_notes:
                #     if (librosa)

                if percentDif < 0.2:
                    endFound = True

            count += 1

        return librosa.frames_to_time(frame + count, sr=sr, hop_length=hop_length)

    @staticmethod
    def ajustOctave(note, nbr_octave: int):
        return note + (nbr_octave * 12)

    @staticmethod
    def removeHarmony(cqt_slice, notes, t_sec):
        notes.sort()
        if len(notes) < 1:
            return []

        final_notes = [notes[0]]

        for note in notes:
            is_new_note = True
            for final_note in final_notes:
                for i in range(1, len(notes) + 8):
                    harmony = librosa.midi_to_hz(final_note) * i
                    note_hz = librosa.midi_to_hz(note)

                    if note_hz > harmony - harmony * 0.05 and note_hz < harmony + harmony * 0.05:
                        is_new_note = False
            if is_new_note:
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
    def displayCqtSliceHz(
        cqt,
        t: float,
        sr: int,
        hop_length: int,
        exportFilename: str = "/home/joseph/Downloads/exportTest.png",
    ) -> None:
        cqt_times = librosa.times_like(cqt, sr=sr, hop_length=hop_length)
        col_idx = np.argmin(np.abs(cqt_times - t))

        spectrum = np.abs(cqt[:, col_idx])

        freqs = librosa.cqt_frequencies(n_bins=len(spectrum), fmin=librosa.note_to_hz("C1"))

        plt.figure(figsize=(10, 4))
        plt.plot(freqs, spectrum)
        plt.xlabel("Fréquence (Hz)")
        plt.ylabel("Amplitude")
        plt.title(f"Spectre CQT à t = {t:.2f} s")
        plt.grid(True)

        plt.savefig(exportFilename)

        return spectrum

    @staticmethod
    def displayCqtSliceNote(
        cqt,
        t: float,
        sr: int,
        hop_length: int,
        exportFilename: str = "/home/joseph/Downloads/exportTest.png",
    ):
        spectrum = Note.getCqtAtTime(cqt, t, sr, hop_length)

        n_bins = len(spectrum)
        freqs = librosa.cqt_frequencies(n_bins=n_bins, fmin=librosa.note_to_hz("C1"))

        note_names = [librosa.hz_to_note(f) for f in freqs]

        step = 12
        tick_indices = np.arange(0, n_bins, step)
        tick_freqs = freqs[tick_indices]
        tick_labels = [note_names[i] for i in tick_indices]

        plt.figure(figsize=(12, 4))
        plt.plot(freqs, spectrum, color="C0", linewidth=1.5)

        plt.xscale("log")

        plt.xticks(tick_freqs, tick_labels)

        plt.xlabel("Notes musicales")
        plt.ylabel("Amplitude")
        plt.title(f"Spectre CQT à t = {t:.2f} s")
        plt.grid(True, which="both", linestyle="--", alpha=0.5)

        plt.savefig(exportFilename)

        return spectrum
