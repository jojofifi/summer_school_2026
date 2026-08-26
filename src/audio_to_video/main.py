from audio_to_video.sound import Sound
from audio_to_video.test import Test


def main() -> None:
    print("Audio to video started")

    # filename = "./src/audio_to_video/media/PinkPanther_Piano_Only.mp3"
    # exportFilename = "./src/audio_to_video/media/PinkPanther_Piano_Only.mid"
    # filename = "./src/audio_to_video/media/PinkPanther_Trumpet_Only.mp3"
    # exportFilename = "./src/audio_to_video/media/PinkPanther_Trumpet_Only.mid"
    filename = "./src/audio_to_video/media/PinkPanther_Both.mp3"
    exportFilename = "./src/audio_to_video/media/PinkPanther_Both.mid"
    # filename = "./src/audio_to_video/media/Ecossaise_Both.mp3"
    # exportFilename = "./src/audio_to_video/media/Ecossaise_Both.mid"

    sound = Sound(filename)
    sound.startAnalyse(exportFilename)

    test = Test(
        "/home/joseph/Downloads/PinkPanther.midi-4538-1787227593715.mid",
        exportFilename,
    )
    test.compareByInstrument()
    # test.compareNbrNotes()
    # test.compareNotes()


if __name__ == "__main__":
    main()
