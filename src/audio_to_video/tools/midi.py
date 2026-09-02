import pretty_midi
import librosa
from note import Note


class Midi:
    def createFile(self, exportFilename: str, notes: Note) -> None:

        midi_data = pretty_midi.PrettyMIDI(resolution=600)

        # Ajouter un instrument (ex: Piano à queue acoustique = 0)
        piano = pretty_midi.Instrument(program=0)
        trumpet = pretty_midi.Instrument(program=56)

        for note in notes:
            pretty_midi_note = pretty_midi.Note(
                velocity=100, pitch=note.note_midi, start=note.start_time, end=note.end_time
            )
            if note.instrument == "piano":
                piano.notes.append(pretty_midi_note)
            if note.instrument == "trumpet":
                trumpet.notes.append(pretty_midi_note)

        midi_data.instruments.append(piano)
        midi_data.instruments.append(trumpet)
        midi_data.write(exportFilename)
