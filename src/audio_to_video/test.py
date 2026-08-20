import pretty_midi as pm
from collections import defaultdict


class Test():

    def __init__(self, midiFileCorrect: str, midiFileTest: str) -> None :
        self.midiDataCorrect = pm.PrettyMIDI(midiFileCorrect)
        self.midiDataTest = pm.PrettyMIDI(midiFileTest)

    def compareNbrNotes(self):
        a = []
        cntCorrect = 0
        for instrument in self.midiDataCorrect.instruments:
            for note in instrument.notes:
                cntCorrect += 1

        cntTest= 0
        for instrument in self.midiDataTest.instruments:
            for note in instrument.notes:
                cntTest += 1

        percentage = 100 - (abs(cntTest-cntCorrect)/((cntTest+cntCorrect)/2)*50)

        print("Correct number of Notes: " + str(cntCorrect))
        print("Guessed number of Notes: " + str(cntTest))
        print("Global Percentage difference: "+ str(percentage))


    def compareNotes(self):
        all_notes = defaultdict(list)

        for instrument in self.midiDataCorrect.instruments:
            for note in instrument.notes:
                all_notes[instrument.name].append({
                    'pitch': note.pitch,
                    'start': round(note.start, 1),
                    'end': round(note.start, 1),
                    'verified': False
                })

        for instrument in self.midiDataTest.instruments:
            for note in instrument.notes:
                for everyNote in all_notes[instrument.name]:
                    if everyNote['pitch'] == note.pitch and everyNote['start'] == round(note.start, 1) and everyNote['end'] == round(note.start, 1):
                        everyNote['verified'] = True

        countCorrect = 0
        countFalse = 0

        for everyInstrument in all_notes:
            for everyNote in all_notes[everyInstrument]:
                if  everyNote['verified'] == True:
                    countCorrect += 1
                else:
                    countFalse += 1

        percentage = 100 - (abs(countCorrect - countFalse) / ((countCorrect + countFalse) / 2)*50)

        print("Correctly Guessed number of Notes: " + str(countCorrect))
        print("wrongly Guessed number of Notes: " + str(countFalse))
        print("Global Percentage difference: " + str(percentage))




