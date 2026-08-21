from sound import Sound

def main() -> None:
    print("Audio to video started")
    
    filename = "./src/audio_to_video/media/PinkPanther_Piano_Only.mp3"
    exportFilename = "./src/audio_to_video/media/PinkPanther_Piano_Only.mid"
    sound = Sound(filename)
    sound.startAnalyse(exportFilename)

if __name__ == "__main__":
    main()
