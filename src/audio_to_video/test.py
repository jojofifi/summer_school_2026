import pretty_midi as pm
from collections import defaultdict


class Test:
    def __init__(self, midiFileCorrect: str, midiFileTest: str) -> None:
        self.midiDataCorrect = pm.PrettyMIDI(midiFileCorrect)
        self.midiDataTest = pm.PrettyMIDI(midiFileTest)

    def compareNbrNotes(self):
        cntCorrect = 0
        for instrument in self.midiDataCorrect.instruments:
            for note in instrument.notes:
                cntCorrect += 1

        cntTest = 0
        for instrument in self.midiDataTest.instruments:
            for note in instrument.notes:
                cntTest += 1

        percentage = 100 - (
            abs(cntTest - cntCorrect) / ((cntTest + cntCorrect) / 2) * 50
        )

        print("Correct number of Notes: " + str(cntCorrect))
        print("Guessed number of Notes: " + str(cntTest))
        print("Global Percentage difference: " + str(percentage))

    def compareNotes(self):
        all_notes = []
        all_notes_test = []

        for instrument in self.midiDataCorrect.instruments:
            for note in instrument.notes:
                all_notes.append(
                    {
                        "pitch": note.pitch,
                        "start": round(note.start, 1),
                        "end": round(note.start, 1),
                        "verified": False,
                    }
                )

        for instrument in self.midiDataTest.instruments:
            for note in instrument.notes:
                all_notes_test.append(
                    {
                        "pitch": note.pitch,
                        "start": round(note.start, 1),
                        "end": round(note.start, 1),
                    }
                )

        for correct_note in all_notes:
            for test_note in all_notes_test:
                if (
                    correct_note["pitch"] == test_note["pitch"]
                    and correct_note["start"] == test_note["start"]
                    and correct_note["end"] == test_note["end"]
                ):
                    correct_note["verified"] = True

        countCorrect = 0
        countFalse = 0

        for correct_note in all_notes:
            if correct_note["verified"] == True:
                countCorrect += 1
            else:
                countFalse += 1

        if countFalse == 0:
            percentage = 100
        else:
            percentage = 100 - (
                abs(countCorrect) / ((countCorrect + countFalse) / 2) * 50
            )

        print("Correctly Guessed number of Notes: " + str(countCorrect))
        print("wrongly Guessed number of Notes: " + str(countFalse))
        print("Global Percentage difference: " + str(percentage))

    def compareByInstrument(self):
        instruments_correct = {}

        for instrument in self.midiDataCorrect.instruments:
            name = pm.program_to_instrument_name(instrument.program)
            instruments_correct[name] = []

            for note in instrument.notes:
                instruments_correct[name].append(
                    {
                        "pitch": note.pitch,
                        "start": round(note.start, 1),
                        "end": round(note.start, 1),
                        "verified": False,
                    }
                )

        count_not_found = 0
        count_found = 0
        count_nonexistent = 0
        for instrument in self.midiDataTest.instruments:
            name = pm.program_to_instrument_name(instrument.program)
            # print(name)
            # print(instruments_correct[name])

            for note in instrument.notes:
                is_found = False
                for correct_note in instruments_correct[name]:
                    is_correct_pitch = correct_note["pitch"] == note.pitch
                    is_correct_start = correct_note["start"] == round(note.start, 1)

                    if is_correct_pitch and is_correct_start:
                        correct_note["verified"] = True
                        is_found = True

                if not is_found:
                    count_nonexistent += 1

        for instrument, notes in instruments_correct.items():
            count_correct = 0
            count_false = 0
            for note in notes:
                if note["verified"]:
                    count_correct += 1
                    count_found += 1
                else:
                    count_false += 1
                    count_not_found += 1

            print(f"Instrument: {instrument}")
            print(f"  Correct notes: {count_correct}")
            print(f"  False notes: {count_false}")
            percentage = abs(count_correct) / (count_correct + count_false) * 100
            print(f"  Similarity: {percentage:.2f}%")

        print(f"Total notes found: {count_nonexistent + count_found}")
        print(f"Total correct notes: {count_found}")
        print(f"Notes were not in original audio: {count_nonexistent}")
        print(
            f"Total Similarity: {(count_found / (count_found + count_not_found) * 100):.2f}%"
        )
