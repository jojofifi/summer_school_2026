import pretty_midi
import librosa
from note import Note

class Midi:
    def createFile(self, exportFilename: str, notes: Note) -> None :

        midi_data = pretty_midi.PrettyMIDI(resolution=600)

        # Ajouter un instrument (ex: Piano à queue acoustique = 0)
        instrument = pretty_midi.Instrument(program=0)

        for note in notes:
            pretty_midi_note = pretty_midi.Note(velocity=100, pitch=note.note_midi, start=note.start_time, end=note.end_time)
            instrument.notes.append(pretty_midi_note)

        # Ajouter l'instrument au fichier MIDI et sauvegarder
        midi_data.instruments.append(instrument)
        midi_data.write(exportFilename)
