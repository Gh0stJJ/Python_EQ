
import equalizer

def main():
    # Read the signal
    signal, sample_rate = equalizer.read_signal("audio.wav")
    # Apply the equalizer
    signal = equalizer.equalizer(signal, sample_rate, 0, 0, 0, 0, 0, 0)
    # Store the signal
    equalizer.store_signal(signal, sample_rate, "audio_equalized.wav")


if __name__ == "__main__":
    main()
