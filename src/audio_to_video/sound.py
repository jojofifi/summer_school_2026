import librosa

from audio_to_video.note import Note
from audio_to_video.tools.cqt import CQT
from audio_to_video.tools.midi import Midi
from audio_to_video.tools.onset import Onset
from audio_to_video.tools.stft import STFT


class Sound:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.y, self.sr = librosa.load(filename, sr=None)
        self.hop_length = 512
        print("Sound loaded")

    def startAnalyse(self, exportFilename) -> None:
        print("Analyse start :")
        cqt = CQT.getCQT(self.y, self.sr, self.hop_length)
        CQT.exportCQT(cqt, self.sr)
        print("\tCQT genereted")
        onset_times = Onset.detectOnset(self.y, self.sr)
        print("\tOnset detected")
        notes = Note.getNotes(cqt, onset_times, self.sr, self.hop_length, 12 * 7, 12)

        print(exportFilename)
        midi = Midi()
        midi.createFile(exportFilename, notes)
