from tools.cqt import CQT
from tools.midi import Midi
from tools.onset import Onset
from tools.stft import STFT
from note import Note
import librosa

class Sound:
    def __init__(self, filename: str) -> None :
        self.filename = filename
        self.y, self.sr = librosa.load(filename, sr=None)
        self.hop_length = 512
        print("Sound loaded")

    def startAnalyse(self, exportFilename) -> None :
        print("Analyse start :")
        stft = STFT.getSTFT(self.y)
        print("\tSTFT genereted")
        cqt = CQT.getCQT(self.y, self.sr, self.hop_length)
        CQT.exportCQT(cqt, self.sr, "/home/joseph/Downloads/Trumpet_CQT.png")
        print("\tCQT genereted")
        onset_times = Onset.detectOnset(stft, self.sr)
        print("\tOnset detected")
        notes = Note.getNotes2(cqt, onset_times, self.sr, self.hop_length, 12*7, 12)

        print(exportFilename)
        print(onset_times)
        print(notes)
        midi = Midi()
        midi.createFile(exportFilename, onset_times, notes, self.sr, self.hop_length)
