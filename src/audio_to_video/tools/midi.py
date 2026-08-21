import pretty_midi
import librosa

class Midi:
    def createFile(self, exportFilename: str, onset_times: [], onset_midi_numbers: [], sr, hop_length) -> None :

        midi_data = pretty_midi.PrettyMIDI()

        # Ajouter un instrument (ex: Piano à queue acoustique = 0)
        instrument = pretty_midi.Instrument(program=0)

        # Durée par défaut d'une note (si la fin de la note n'est pas connue)
        default_duration = 0.5

        for t, notes in zip(onset_times, onset_midi_numbers):
            t = librosa.frames_to_time(t, sr=sr, hop_length=hop_length)
            for note in notes:
                # Créer une note MIDI (vélocité entre 0 et 127)
                midi_note = pretty_midi.Note(
                    velocity=100, pitch=note, start=t, end=t + default_duration
                )
                instrument.notes.append(midi_note)

# Ajouter l'instrument au fichier MIDI et sauvegarder
        midi_data.instruments.append(instrument)
        midi_data.write(exportFilename)
