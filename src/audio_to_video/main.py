from audio_to_video.sound import Sound
from audio_to_video.test import Test
from audio_to_video.lancement import Frontend

def main() -> None:
    print("Audio to video started")

    # filename = "./src/audio_to_video/media/mp3/PinkPanther_Piano_Only.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/PinkPanther_Piano_Only.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/PinkPanther.midi"

    # filename = "./src/audio_to_video/media/mp3/PinkPanther_Trumpet_Only.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/PinkPanther_Trumpet_Only.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/PinkPanther.midi"
    '''
    filename = "./src/audio_to_video/media/mp3/PinkPanther_Both.mp3"
    exportFilename = "./src/audio_to_video/media/generated_midi/PinkPanther_Both.mid"
    originalFilename = "./src/audio_to_video/media/original_midi/PinkPanther.midi"
    '''

    # filename = "./src/audio_to_video/media/mp3/Ecossaise_Both.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/Ecossaise_Both.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/Ecossaise_Beethoven.midi-7526-1788335886732.mid"

    filename = "./src/audio_to_video/media/mp3/Gamme.mp3"
    exportFilename = "./src/audio_to_video/media/generated_midi/Gamme.mid"
    originalFilename = "./src/audio_to_video/media/original_midi/Gamme.mid"

    # filename = "./src/audio_to_video/media/mp3/Gamme_Trumpet.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/Gamme_Trumpet.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/Gamme.mid"

    # filename = "./src/audio_to_video/media/mp3/Gamme_Piano.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/Gamme_Piano.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/Gamme.mid"

    # filename = "./src/audio_to_video/media/mp3/SSB.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/SSB.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/SSB.mid"

    # filename = "./src/audio_to_video/media/mp3/SSB_Piano.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/SSB_Piano.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/SSB.mid"

    # filename = "./src/audio_to_video/media/mp3/SSB_Trumpet.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/SSB_Trumpet.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/SSB.mid"

    # filename = "./src/audio_to_video/media/mp3/SuperMario.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/SuperMario.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/SuperMario.mid"

    # filename = "./src/audio_to_video/media/mp3/SuperMarion_Piano.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/SuperMario_Piano.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/SuperMario.mid"

    # filename = "./src/audio_to_video/media/mp3/SuperMarion_Trumpet.mp3"
    # exportFilename = "./src/audio_to_video/media/generated_midi/SuperMario_Trumpet.mid"
    # originalFilename = "./src/audio_to_video/media/original_midi/SuperMario.mid"

    sound = Sound(filename)
    sound.startAnalyse(exportFilename)

    test = Test(
        originalFilename,
        exportFilename,
    )
    test.compareByInstrument()

    Frontend.start(exportFilename, filename)


if __name__ == "__main__":
    main()
